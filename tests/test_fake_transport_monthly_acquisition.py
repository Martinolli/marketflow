import ast
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from marketflow.historical_data import monthly_acquisition as monthly
from marketflow.historical_data import provider_response
from marketflow.historical_data.fake_transport import (
    FakeTransportError,
    ScriptedExchange,
    ScriptedFakeTransport,
    crash_after_body,
    http_response,
    http_status,
    timeout,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
V2_DIGEST = "59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0"
V21_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"


def _body(
    *,
    ticker: str = "FAKEFLOW",
    t: int = 1704105000000,
    close: str = "100",
    next_url: str | None = None,
    numeric_string: bool = False,
    count: str | None = None,
    row_extra: str = "",
    top_extra: str = "",
) -> bytes:
    close_value = f'"{close}"' if numeric_string else close
    next_part = f',"next_url":"{next_url}"' if next_url else ""
    count_part = f',"count":{count}' if count is not None else ""
    return (
        '{"adjusted":true,"queryCount":1,"results":[{"c":'
        + close_value
        + ',"h":101,"l":99,"n":10,"o":100,"t":'
        + str(t)
        + ',"v":1000,"vw":100.5'
        + row_extra
        + "}],"
        + '"resultsCount":1,"status":"OK","ticker":"'
        + ticker
        + '"'
        + count_part
        + next_part
        + top_extra
        + "}"
    ).encode("utf-8")


def _epoch_ms(value: datetime) -> int:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("test timestamp must be timezone-aware")
    return int(value.astimezone(UTC).timestamp() * 1000)


def _local_epoch_ms(local_date: str, local_time: str, *, timezone: str = "America/New_York") -> int:
    hour, minute = (int(part) for part in local_time.split(":", 1))
    local = datetime.fromisoformat(local_date).replace(hour=hour, minute=minute, tzinfo=ZoneInfo(timezone))
    return _epoch_ms(local)


def _bars_body(
    timestamps: list[int],
    *,
    ticker: str = "FAKEFLOW",
    row_extra: str = ',"vw":100.5,"otc":false',
) -> bytes:
    rows = []
    for index, timestamp in enumerate(timestamps):
        value = 100 + index
        rows.append(
            '{"c":'
            + str(value)
            + ',"h":'
            + str(value + 1)
            + ',"l":'
            + str(value - 1)
            + ',"n":10,"o":'
            + str(value)
            + ',"t":'
            + str(timestamp)
            + ',"v":1000'
            + row_extra
            + "}"
        )
    return (
        '{"adjusted":true,"queryCount":'
        + str(len(rows))
        + ',"results":['
        + ",".join(rows)
        + '],"resultsCount":'
        + str(len(rows))
        + ',"count":'
        + str(len(rows))
        + ',"status":"OK","ticker":"'
        + ticker
        + '"}'
    ).encode("utf-8")


def _request(month_key: str = "2024-01") -> monthly.MonthChunkRequest:
    return monthly.build_month_chunk_request(
        canonical_ticker="FAKEFLOW",
        month_key=month_key,
        effective_start_date="2024-01-01",
        effective_end_date="2024-01-01",
    )


def _request_for_range(month_key: str, effective_start_date: str, effective_end_date: str) -> monthly.MonthChunkRequest:
    return monthly.build_month_chunk_request(
        canonical_ticker="FAKEFLOW",
        month_key=month_key,
        effective_start_date=effective_start_date,
        effective_end_date=effective_end_date,
    )


def _context(request: monthly.MonthChunkRequest) -> provider_response.ResponseRequestContext:
    return provider_response.ResponseRequestContext(
        canonical_ticker=request.canonical_ticker,
        month_key=request.month_key,
        effective_start_date=request.effective_start_date,
        effective_end_date=request.effective_end_date,
        adjusted=request.adjusted,
        sort=request.sort,
        limit=request.limit,
        month_request_digest=request.request_semantic_digest,
    )


def _page_request(request: monthly.MonthChunkRequest, ordinal: int, predecessor: str | None = None, continuation: str | None = None):
    page = monthly.build_logical_page_request(
        request,
        page_ordinal=ordinal,
        predecessor_accepted_page_identity=predecessor,
        sanitized_continuation_identity=continuation,
    )
    return page, monthly.fake_transport_request(request, page)


def _payload_from_manifest(root: Path, manifest: dict) -> bytes:
    return (root / manifest["payload_ref"]).read_bytes()


def _load_json_payload(root: Path, manifest: dict) -> dict:
    return json.loads(_payload_from_manifest(root, manifest))


def _schema_error_diagnostics(body: bytes) -> dict:
    request = _request()
    with pytest.raises(provider_response.ProviderResponseError) as excinfo:
        provider_response.parse_provider_response(body, body_sha256="x", context=_context(request))
    diagnostics = excinfo.value.sanitized_diagnostics
    assert isinstance(diagnostics, dict)
    return diagnostics


def test_reproduces_january_2025_provider_local_after_hours_utc_spill_defect():
    request = _request_for_range("2025-01", "2025-01-01", "2025-01-31")
    body = _bars_body(
        [
            _local_epoch_ms("2025-01-01", "00:00"),
            _epoch_ms(datetime(2025, 2, 1, 0, 0, tzinfo=UTC)),
            _epoch_ms(datetime(2025, 2, 1, 0, 45, tzinfo=UTC)),
        ]
    )

    parsed = provider_response.parse_provider_response(body, body_sha256="x", context=_context(request))

    assert [row.window_start_utc for row in parsed.rows] == [
        "2025-01-01T05:00:00Z",
        "2025-02-01T00:00:00Z",
        "2025-02-01T00:45:00Z",
    ]


def test_provider_local_january_2025_month_end_boundaries_accept_utc_spill_and_reject_next_local_date():
    request = _request_for_range("2025-01", "2025-01-01", "2025-01-31")
    context = _context(request)
    accepted = provider_response.parse_provider_response(
        _bars_body(
            [
                _local_epoch_ms("2025-01-01", "00:00"),
                _local_epoch_ms("2025-01-31", "19:00"),
                _local_epoch_ms("2025-01-31", "19:45"),
                _local_epoch_ms("2025-01-31", "23:45"),
            ]
        ),
        body_sha256="x",
        context=context,
    )

    assert [row.window_start_utc for row in accepted.rows] == [
        "2025-01-01T05:00:00Z",
        "2025-02-01T00:00:00Z",
        "2025-02-01T00:45:00Z",
        "2025-02-01T04:45:00Z",
    ]
    assert accepted.rows[-1].window_end_utc == "2025-02-01T05:00:00Z"

    with pytest.raises(provider_response.ProviderResponseError) as excinfo:
        provider_response.parse_provider_response(
            _bars_body([_local_epoch_ms("2025-02-01", "00:00")]),
            body_sha256="x",
            context=context,
        )

    assert excinfo.value.failure_category == provider_response.TIMESTAMP_RANGE_INVALID
    assert excinfo.value.sanitized_diagnostics["fixed_finding"] == provider_response.SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE


def test_provider_local_summer_dst_month_end_uses_zoneinfo_not_fixed_offset():
    request = _request_for_range("2025-07", "2025-07-01", "2025-07-31")
    context = _context(request)
    accepted = provider_response.parse_provider_response(
        _bars_body([_local_epoch_ms("2025-07-31", "23:45")]),
        body_sha256="x",
        context=context,
    )

    assert accepted.rows[0].window_start_utc == "2025-08-01T03:45:00Z"
    assert accepted.rows[0].window_end_utc == "2025-08-01T04:00:00Z"

    with pytest.raises(provider_response.ProviderResponseError) as excinfo:
        provider_response.parse_provider_response(
            _bars_body([_local_epoch_ms("2025-08-01", "00:00")]),
            body_sha256="x",
            context=context,
        )

    assert excinfo.value.failure_category == provider_response.TIMESTAMP_RANGE_INVALID


def test_provider_local_start_lower_boundary_and_timestamp_order_remain_strict():
    request = _request_for_range("2025-01", "2025-01-01", "2025-01-31")
    context = _context(request)
    accepted = provider_response.parse_provider_response(
        _bars_body([_local_epoch_ms("2025-01-01", "00:00")]),
        body_sha256="x",
        context=context,
    )

    assert accepted.rows[0].window_start_utc == "2025-01-01T05:00:00Z"
    with pytest.raises(provider_response.ProviderResponseError) as before_start:
        provider_response.parse_provider_response(
            _bars_body([_local_epoch_ms("2024-12-31", "23:45")]),
            body_sha256="x",
            context=context,
        )
    with pytest.raises(provider_response.ProviderResponseError) as nonascending:
        provider_response.parse_provider_response(
            _bars_body([_local_epoch_ms("2025-01-01", "00:15"), _local_epoch_ms("2025-01-01", "00:00")]),
            body_sha256="x",
            context=context,
        )
    with pytest.raises(provider_response.ProviderResponseError) as duplicate:
        provider_response.parse_provider_response(
            _bars_body([_local_epoch_ms("2025-01-01", "00:00"), _local_epoch_ms("2025-01-01", "00:00")]),
            body_sha256="x",
            context=context,
        )

    assert before_start.value.failure_category == provider_response.TIMESTAMP_RANGE_INVALID
    assert nonascending.value.failure_category == provider_response.TIMESTAMP_ORDER
    assert duplicate.value.failure_category == provider_response.TIMESTAMP_ORDER


def test_source_window_range_helper_rejects_naive_datetimes():
    aware_start, aware_end = provider_response._local_date_bounds_as_utc(
        datetime.fromisoformat("2025-01-01").date(),
        datetime.fromisoformat("2025-01-31").date(),
    )

    with pytest.raises(provider_response.ProviderResponseError) as excinfo:
        provider_response._validate_source_window_in_effective_local_range(
            window_start=datetime(2025, 1, 1, 5, 0),
            window_end=aware_start + (aware_end - aware_start),
            utc_start=aware_start,
            utc_end_exclusive=aware_end,
            row_index=0,
        )

    assert excinfo.value.failure_category == provider_response.TIMESTAMP_RANGE_INVALID


def test_month_request_binds_contracts_and_rejects_real_ticker():
    request = _request()
    clipped = monthly.build_month_chunk_request(
        canonical_ticker="FAKEFLOW",
        month_key="2024-01",
        effective_start_date="2024-01-05",
        effective_end_date="2024-01-10",
    )

    assert request.contract_v2_base_digest == V2_DIGEST
    assert request.contract_v2_1_digest == V21_DIGEST
    assert request.provider_business_identity == "Massive.com"
    assert request.provider_entitlement_status == "OPERATOR_ATTESTED_CONFIRMED"
    assert request.multiplier == 15
    assert request.timespan == "minute"
    assert request.adjusted is True
    assert request.sort == "asc"
    assert request.limit == 50000
    assert clipped.effective_start_date == "2024-01-05"
    assert clipped.effective_end_date == "2024-01-10"
    with pytest.raises(monthly.MonthlyAcquisitionError):
        monthly.build_month_chunk_request(canonical_ticker="AAPL", month_key="2024-01")
    with pytest.raises(monthly.MonthlyAcquisitionError):
        monthly.build_month_chunk_request(canonical_ticker="FAKEFLOW", month_key="2026-01")


def test_fake_transport_rejects_unexpected_request_and_unconsumed_script():
    request = _request()
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport([ScriptedExchange(expected, timeout()), ScriptedExchange(expected, timeout())])

    assert transport.send(expected).outcome_type == "TRANSPORT_TIMEOUT"
    with pytest.raises(FakeTransportError):
        transport.assert_consumed()


def test_fake_transport_rejects_request_identity_mismatch():
    request = _request()
    _, expected = _page_request(request, 1)
    wrong = monthly.fake_transport_request(
        monthly.build_month_chunk_request(canonical_ticker="TESTFLOW", month_key="2024-01"),
        monthly.build_logical_page_request(monthly.build_month_chunk_request(canonical_ticker="TESTFLOW", month_key="2024-01"), page_ordinal=1),
    )
    transport = ScriptedFakeTransport([ScriptedExchange(expected, timeout())])

    with pytest.raises(FakeTransportError):
        transport.send(wrong)


def test_provider_parser_rejects_numeric_strings_and_bool_ints():
    request = _request()
    context = _context(request)
    with pytest.raises(provider_response.ProviderResponseError):
        provider_response.parse_provider_response(
            _body(numeric_string=True),
            body_sha256="x",
            context=context,
        )
    bad_bool_int = b'{"adjusted":true,"queryCount":1,"results":[{"c":100,"h":101,"l":99,"n":true,"o":100,"t":1704105000000,"v":1000}],"resultsCount":1,"status":"OK","ticker":"FAKEFLOW"}'
    with pytest.raises(provider_response.ProviderResponseError):
        provider_response.parse_provider_response(bad_bool_int, body_sha256="x", context=context)


def test_provider_parser_accepts_optional_count_when_redundant_and_excludes_from_projection():
    request = _request()
    context = _context(request)
    without_count = provider_response.parse_provider_response(_body(), body_sha256="x", context=context)
    with_count = provider_response.parse_provider_response(_body(count="1"), body_sha256="x", context=context)

    assert with_count.results_count == 1
    assert "count" not in with_count.semantic_projection
    assert with_count.semantic_projection_digest == without_count.semantic_projection_digest


def test_provider_parser_rejects_count_mismatch_and_invalid_count_types():
    assert _schema_error_diagnostics(_body(count="0"))["unexpected_top_level_fields"] == []
    assert _schema_error_diagnostics(
        b'{"adjusted":true,"queryCount":2,"results":[{"c":100,"h":101,"l":99,"n":10,"o":100,"t":1704105000000,"v":1000,"vw":100.5}],"resultsCount":2,"status":"OK","ticker":"FAKEFLOW","count":2}'
    )["unexpected_top_level_fields"] == []
    for count in ("true", '"1"', "1.0"):
        diagnostics = _schema_error_diagnostics(_body(count=count))
        assert {"field": "count", "expected_type": "INTEGER", "actual_type": diagnostics["type_mismatches"][0]["actual_type"]} in diagnostics[
            "type_mismatches"
        ]


def test_provider_parser_accepts_optional_otc_bool_and_excludes_from_projection():
    request = _request()
    context = _context(request)
    absent = provider_response.parse_provider_response(_body(), body_sha256="x", context=context)
    otc_true = provider_response.parse_provider_response(_body(row_extra=',"otc":true'), body_sha256="x", context=context)
    otc_false = provider_response.parse_provider_response(_body(row_extra=',"otc":false'), body_sha256="x", context=context)

    assert otc_true.rows[0].close == absent.rows[0].close
    assert otc_false.rows[0].close == absent.rows[0].close
    assert "otc" not in json.dumps(otc_true.semantic_projection, sort_keys=True)
    assert otc_true.semantic_projection_digest == absent.semantic_projection_digest
    assert otc_false.semantic_projection_digest == absent.semantic_projection_digest


def test_provider_parser_rejects_otc_non_bool_and_unknown_fields_with_sanitized_diagnostics():
    for row_extra in (',"otc":"true"', ',"otc":1'):
        diagnostics = _schema_error_diagnostics(_body(row_extra=row_extra))
        assert {
            "field": "otc",
            "row_index": 0,
            "scope": "aggregate_row",
            "expected_type": "BOOL",
            "actual_type": diagnostics["type_mismatches"][0]["actual_type"],
        } in diagnostics["type_mismatches"]

    top_diagnostics = _schema_error_diagnostics(
        _body(
            next_url="https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=opaque-secret-cursor&adjusted=true&sort=asc&limit=50000",
            top_extra=',"request_id":"request-123-next-secret-1000","mysteryField":"request-123-next-secret-1000"',
        )
    )
    assert top_diagnostics["unexpected_top_level_fields"] == ["mysteryField"]
    assert top_diagnostics["top_level_fields"] == sorted(
        ["adjusted", "mysteryField", "queryCount", "results", "resultsCount", "status", "ticker"]
    )
    row_diagnostics = _schema_error_diagnostics(_body(row_extra=',"mysteryRowField":"ohlcv-secret-1000"'))
    assert row_diagnostics["aggregate_row_failures"] == [
        {"row_index": 0, "unexpected_row_fields": ["mysteryRowField"], "missing_row_fields": []}
    ]
    diagnostic_text = json.dumps({"top": top_diagnostics, "row": row_diagnostics}, sort_keys=True)
    for forbidden in (
        "request-123-next-secret-1000",
        "ohlcv-secret-1000",
        "opaque-secret-cursor",
        "Authorization",
        "fictional-smoke-key",
        "apiKey",
        "request_id",
        "next_url",
        "100.5",
    ):
        assert forbidden not in diagnostic_text


def test_provider_parser_rejects_nan_duplicate_keys_and_bad_timestamp():
    request = _request()
    context = _context(request)
    with pytest.raises(provider_response.ProviderResponseError):
        provider_response.parse_provider_response(
            b'{"adjusted":true,"queryCount":1,"results":[{"c":NaN,"h":101,"l":99,"o":100,"t":1704105000000,"v":1000}],"resultsCount":1,"status":"OK","ticker":"FAKEFLOW"}',
            body_sha256="x",
            context=context,
        )
    with pytest.raises(provider_response.ProviderResponseError):
        provider_response.parse_provider_response(
            b'{"adjusted":true,"adjusted":true,"queryCount":0,"results":[],"resultsCount":0,"status":"OK","ticker":"FAKEFLOW"}',
            body_sha256="x",
            context=context,
        )
    with pytest.raises(provider_response.ProviderResponseError):
        provider_response.parse_provider_response(
            _body(t=1704105000001),
            body_sha256="x",
            context=context,
        )
    with pytest.raises(provider_response.ProviderResponseError):
        provider_response.parse_provider_response(
            b'{"adjusted":true,"queryCount":1,"results":[{"c":100,"h":101,"l":99,"o":100,"t":1704105000000,"v":1000}],"resultsCount":1,"status":"ERROR","ticker":"FAKEFLOW"}',
            body_sha256="x",
            context=context,
        )
    with pytest.raises(provider_response.ProviderResponseError):
        provider_response.parse_provider_response(
            b'{"adjusted":true,"queryCount":0,"results":[],"resultsCount":0,"status":"OK","ticker":"FAKEFLOW"}',
            body_sha256="x",
            context=context,
        )


def test_semantic_projection_includes_sanitized_continuation_without_raw_cursor():
    request = _request()
    next_url = "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=opaque-secret-cursor&adjusted=true&sort=asc&limit=50000"
    parsed = provider_response.parse_provider_response(
        _body(next_url=next_url),
        body_sha256="raw-digest",
        context=_context(request),
    )

    assert parsed.semantic_projection["continuation_present"] is True
    assert parsed.semantic_projection["sanitized_continuation_identity"].startswith("cont-")
    assert "opaque-secret-cursor" not in json.dumps(parsed.semantic_projection, sort_keys=True)
    bad_range_url = "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-02/2024-01-01?cursor=opaque&adjusted=true&sort=asc&limit=50000"
    with pytest.raises(provider_response.ProviderResponseError):
        provider_response.parse_provider_response(
            _body(next_url=bad_range_url),
            body_sha256="raw-digest",
            context=_context(request),
        )


def test_completed_two_page_acquisition_writes_lineage_and_paired_normalized_artifacts(tmp_path: Path):
    request = _request()
    next_url = "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=opaque2&adjusted=true&sort=asc&limit=50000"
    first_body = _body(next_url=next_url)
    continuation = provider_response.sanitize_continuation_identity(next_url, _context(request))
    first_page, first_expected = _page_request(request, 1)
    second_page, second_expected = _page_request(request, 2, first_page.logical_page_request_id, continuation)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(first_expected, http_response(200, first_body)),
            ScriptedExchange(second_expected, http_response(200, _body(t=1704105900000, close="101"))),
        ]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-two-page",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["semantic_retry_status"] == monthly.ONE_VALID_ATTEMPT_PER_PAGE
    assert receipt["page_count"] == 2
    assert receipt["row_count"] == 2
    assert receipt["provider_execution_enabled"] is False
    assert receipt["sanitization"].startswith("NO_RAW_OHLCV")
    raw_manifests = [m for m in (tmp_path / "run-two-page").rglob("*.manifest.json") if monthly.ARTIFACT_RAW_PROVIDER_PAGE in m.read_text()]
    assert len(raw_manifests) == 2
    manifests = [json.loads(path.read_text()) for path in (tmp_path / "run-two-page").rglob("*.manifest.json")]
    completeness = next(m for m in manifests if m["artifact_type"] == monthly.ARTIFACT_MONTH_CHUNK_COMPLETENESS_MANIFEST)
    normalized = next(m for m in manifests if m["artifact_type"] == monthly.ARTIFACT_MONTH_NORMALIZED_15M_OHLCV)
    audit = next(m for m in manifests if m["artifact_type"] == monthly.ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS)
    completeness_payload = _load_json_payload(tmp_path, completeness)
    audit_payload = _load_json_payload(tmp_path, audit)
    assert normalized["primary_parent_artifact_id"] == completeness["artifact_id"]
    assert audit["primary_parent_artifact_id"] == completeness["artifact_id"]
    assert completeness_payload["effective_start_date"] == "2024-01-01"
    assert completeness_payload["effective_end_date"] == "2024-01-01"
    assert completeness_payload["pagination_exhausted"] is True
    assert completeness_payload["completion_status"] == "COMPLETE"
    assert completeness_payload["page_chain_digest"]
    assert completeness_payload["first_source_window_start_utc"] == "2024-01-01T10:30:00Z"
    assert _load_json_payload(tmp_path, normalized)["rows"][0]["window_start_utc"] == audit_payload["rows"][0]["window_start_utc"]
    assert audit_payload["rows"][0]["vwap_status"] == provider_response.VWAP_PRESENT
    assert audit_payload["rows"][0]["transaction_count_status"] == provider_response.TRANSACTION_COUNT_PRESENT
    assert receipt["attempt_count"] == 2
    assert receipt["accepted_page_count"] == 2
    assert receipt["failed_or_rejected_attempt_count"] == 0
    assert receipt["completeness_status"] == "COMPLETE"
    assert first_body == next(_payload_from_manifest(tmp_path, m) for m in manifests if m["artifact_type"] == monthly.ARTIFACT_RAW_PROVIDER_PAGE)


def test_monthly_normalization_retains_provider_local_after_hours_source_bars(tmp_path: Path):
    request = _request_for_range("2025-01", "2025-01-01", "2025-01-31")
    _, expected = _page_request(request, 1)
    body = _bars_body([_local_epoch_ms("2025-01-01", "00:00"), _local_epoch_ms("2025-01-31", "23:45")])
    transport = ScriptedFakeTransport([ScriptedExchange(expected, http_response(200, body))])

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-provider-local-hours",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["completeness_status"] == "COMPLETE"
    assert receipt["row_count"] == 2
    manifests = [json.loads(path.read_text()) for path in (tmp_path / "run-provider-local-hours").rglob("*.manifest.json")]
    normalized = next(m for m in manifests if m["artifact_type"] == monthly.ARTIFACT_MONTH_NORMALIZED_15M_OHLCV)
    normalized_payload = _load_json_payload(tmp_path, normalized)
    assert [row["window_start_utc"] for row in normalized_payload["rows"]] == [
        "2025-01-01T05:00:00Z",
        "2025-02-01T04:45:00Z",
    ]
    assert normalized_payload["rows"][-1]["window_end_utc"] == "2025-02-01T05:00:00Z"


def test_timeout_retry_records_backoff_and_accepts_second_attempt(tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(expected, timeout()),
            ScriptedExchange(expected, http_response(200, _body())),
        ]
    )
    sleeper = monthly.RecordingSleeper([])

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-timeout",
        clock=monthly.DeterministicClock(),
        sleeper=sleeper,
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["semantic_retry_status"] == monthly.ONE_VALID_ATTEMPT_PER_PAGE
    assert receipt["recorded_retry_delays_seconds"] == [2]
    attempts = [
        _load_json_payload(tmp_path, json.loads(path.read_text()))
        for path in (tmp_path / "run-timeout").rglob("*.manifest.json")
        if json.loads(path.read_text())["artifact_type"] == monthly.ARTIFACT_REQUEST_ATTEMPT_RECORD
    ]
    assert [attempt["attempt_status"] for attempt in attempts] == [monthly.ATTEMPT_RETRY_SCHEDULED, monthly.ATTEMPT_ACCEPTED]
    assert attempts[0]["attempt_id"].endswith("-attempt-1")
    assert attempts[0]["response_body_available"] is False
    assert attempts[1]["response_body_available"] is True
    assert attempts[1]["response_body_complete"] is True


def test_retry_after_valid_uses_max_configured_backoff(tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(expected, http_status(429, headers={"Retry-After": "7"})),
            ScriptedExchange(expected, http_response(200, _body())),
        ]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-retry-after",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["semantic_retry_status"] == monthly.ONE_VALID_ATTEMPT_PER_PAGE
    assert receipt["recorded_retry_delays_seconds"] == [7]


@pytest.mark.parametrize("status_code", [429, 503])
def test_retryable_http_statuses_retry_once_then_accept(status_code: int, tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(expected, http_status(status_code)),
            ScriptedExchange(expected, http_response(200, _body())),
        ]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id=f"run-retry-{status_code}",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["attempt_count"] == 2
    assert receipt["recorded_retry_delays_seconds"] == [2]
    assert receipt["accepted_page_count"] == 1
    assert receipt["pagination_status"] == monthly.PAGINATION_CHAIN_VALID


def test_first_page_authentication_failure_is_terminal_before_pagination(tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport(
        [ScriptedExchange(expected, http_status(401, headers={"failure_category": monthly.AUTHENTICATION_FAILURE}))]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-auth-401",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_AUTHENTICATION_FAILED
    assert receipt["pagination_status"] == monthly.PAGINATION_NOT_STARTED
    assert receipt["completeness_status"] == "INCOMPLETE"
    assert receipt["fixed_findings"] == [monthly.AUTHENTICATION_FAILURE]
    assert receipt["attempt_count"] == 1
    assert receipt["accepted_page_count"] == 0
    assert receipt["raw_page_count"] == 0
    assert receipt["recorded_retry_delays_seconds"] == []
    attempts = [
        _load_json_payload(tmp_path, json.loads(path.read_text()))
        for path in (tmp_path / "run-auth-401").rglob("*.manifest.json")
        if json.loads(path.read_text())["artifact_type"] == monthly.ARTIFACT_REQUEST_ATTEMPT_RECORD
    ]
    assert len(attempts) == 1
    assert attempts[0]["attempt_status"] == monthly.ATTEMPT_REJECTED_NON_RETRYABLE
    assert attempts[0]["failure_category"] == monthly.AUTHENTICATION_FAILURE
    assert attempts[0]["http_status"] == 401
    assert attempts[0]["response_body_available"] is False
    assert attempts[0]["response_body_complete"] is False


def test_first_page_authentication_failure_with_body_does_not_persist_raw_page(tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(
                expected,
                http_response(
                    401,
                    b'{"status":"ERROR","message":"credential rejected body must not persist"}',
                    headers={"failure_category": monthly.AUTHENTICATION_FAILURE},
                ),
            )
        ]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-auth-401-body",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_AUTHENTICATION_FAILED
    assert receipt["pagination_status"] == monthly.PAGINATION_NOT_STARTED
    assert receipt["fixed_findings"] == [monthly.AUTHENTICATION_FAILURE]
    assert receipt["attempt_count"] == 1
    assert receipt["accepted_page_count"] == 0
    assert receipt["raw_page_count"] == 0
    assert receipt["recorded_retry_delays_seconds"] == []
    attempts = [
        _load_json_payload(tmp_path, json.loads(path.read_text()))
        for path in (tmp_path / "run-auth-401-body").rglob("*.manifest.json")
        if json.loads(path.read_text())["artifact_type"] == monthly.ARTIFACT_REQUEST_ATTEMPT_RECORD
    ]
    assert len(attempts) == 1
    assert attempts[0]["attempt_status"] == monthly.ATTEMPT_REJECTED_NON_RETRYABLE
    assert attempts[0]["response_body_available"] is True
    assert attempts[0]["response_body_complete"] is True
    assert attempts[0]["raw_page_artifact_id"] is None
    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in tmp_path.rglob("*") if path.is_file())
    assert "credential rejected body must not persist" not in all_text


def test_first_page_schema_failure_is_terminal_before_pagination_with_sanitized_diagnostics(tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    body = _body(top_extra=',"mysteryField":"request-123-next-secret-1000"')
    transport = ScriptedFakeTransport([ScriptedExchange(expected, http_response(200, body))])

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-schema-200",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED
    assert receipt["pagination_status"] == monthly.PAGINATION_NOT_STARTED
    assert receipt["completeness_status"] == "INCOMPLETE"
    assert receipt["fixed_findings"] == [monthly.RESPONSE_SCHEMA_INVALID]
    assert receipt["attempt_count"] == 1
    assert receipt["accepted_page_count"] == 0
    assert receipt["raw_page_count"] == 0
    assert receipt["recorded_retry_delays_seconds"] == []
    attempts = [
        _load_json_payload(tmp_path, json.loads(path.read_text()))
        for path in (tmp_path / "run-schema-200").rglob("*.manifest.json")
        if json.loads(path.read_text())["artifact_type"] == monthly.ARTIFACT_REQUEST_ATTEMPT_RECORD
    ]
    assert len(attempts) == 1
    assert attempts[0]["attempt_status"] == monthly.ATTEMPT_REJECTED_NON_RETRYABLE
    assert attempts[0]["failure_category"] == monthly.SCHEMA_FAILURE
    assert attempts[0]["http_status"] == 200
    assert attempts[0]["response_body_available"] is True
    assert attempts[0]["response_body_complete"] is True
    assert attempts[0]["raw_page_artifact_id"] is None
    assert attempts[0]["sanitized_schema_diagnostics"]["unexpected_top_level_fields"] == ["mysteryField"]
    diagnostic_text = json.dumps(attempts[0]["sanitized_schema_diagnostics"], sort_keys=True)
    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in tmp_path.rglob("*") if path.is_file())
    for forbidden in ("request-123-next-secret-1000", "Authorization", "apiKey", "next_url", "100.5"):
        assert forbidden not in diagnostic_text
        assert forbidden not in all_text
    assert monthly.ARTIFACT_MONTH_CHUNK_COMPLETENESS_MANIFEST not in {
        json.loads(path.read_text())["artifact_type"] for path in (tmp_path / "run-schema-200").rglob("*.manifest.json")
    }
    assert monthly.ARTIFACT_MONTH_NORMALIZED_15M_OHLCV not in {
        json.loads(path.read_text())["artifact_type"] for path in (tmp_path / "run-schema-200").rglob("*.manifest.json")
    }
    assert monthly.ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS not in {
        json.loads(path.read_text())["artifact_type"] for path in (tmp_path / "run-schema-200").rglob("*.manifest.json")
    }


def test_timestamp_range_failure_is_not_reported_as_schema_failure(tmp_path: Path):
    request = _request_for_range("2025-01", "2025-01-01", "2025-01-31")
    _, expected = _page_request(request, 1)
    body = _bars_body([_local_epoch_ms("2025-02-01", "00:00")])
    transport = ScriptedFakeTransport([ScriptedExchange(expected, http_response(200, body))])

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-timestamp-range",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_INVALID
    assert receipt["fixed_findings"] == [monthly.TIMESTAMP_RANGE_INVALID]
    assert receipt["pagination_status"] == monthly.PAGINATION_NOT_STARTED
    assert receipt["raw_page_count"] == 0
    attempts = [
        _load_json_payload(tmp_path, json.loads(path.read_text()))
        for path in (tmp_path / "run-timestamp-range").rglob("*.manifest.json")
        if json.loads(path.read_text())["artifact_type"] == monthly.ARTIFACT_REQUEST_ATTEMPT_RECORD
    ]
    assert attempts[0]["failure_category"] == monthly.TIMESTAMP_RANGE_INVALID
    assert attempts[0]["failure_category"] != monthly.SCHEMA_FAILURE
    assert attempts[0]["sanitized_error_code"] == monthly.SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE
    assert attempts[0]["sanitized_schema_diagnostics"]["failure_stage"] == provider_response.TIMESTAMP_RANGE


def test_retry_after_policy_violation_blocks_without_completeness(tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport([ScriptedExchange(expected, http_status(503, headers={"Retry-After": "61"}))])

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-retry-after-invalid",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_INVALID
    assert receipt["pagination_status"] == monthly.PAGINATION_NOT_STARTED
    assert receipt["recorded_retry_delays_seconds"] == []
    assert monthly.ARTIFACT_MONTH_CHUNK_COMPLETENESS_MANIFEST not in {
        json.loads(path.read_text())["artifact_type"] for path in (tmp_path / "run-retry-after-invalid").rglob("*.manifest.json")
    }


def test_semantically_equivalent_retries_accept_lowest_valid_attempt(tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(expected, crash_after_body(200, _body(close="100"))),
            ScriptedExchange(expected, http_response(200, _body(close="100.0"))),
        ]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-equivalent",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["semantic_retry_status"] == monthly.SEMANTICALLY_EQUIVALENT_RETRIES
    attempts = [
        _load_json_payload(tmp_path, json.loads(path.read_text()))
        for path in (tmp_path / "run-equivalent").rglob("*.manifest.json")
        if json.loads(path.read_text())["artifact_type"] == monthly.ARTIFACT_REQUEST_ATTEMPT_RECORD
    ]
    assert [attempt["attempt_status"] for attempt in attempts] == [monthly.ATTEMPT_ACCEPTED, monthly.ATTEMPT_VALID_NOT_ACCEPTED]
    assert [attempt["accepted_attempt"] for attempt in attempts] == [True, False]


def test_saved_monthly_manifest_validation_rejects_wrong_type_stage_and_inputs(tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=ScriptedFakeTransport([ScriptedExchange(expected, http_response(200, _body()))]),
        run_root=tmp_path,
        run_id="run-validate-manifest",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )
    assert receipt["status"] == monthly.MONTH_ACQUISITION_COMPLETED
    manifest = next(
        json.loads(path.read_text())
        for path in (tmp_path / "run-validate-manifest").rglob("*.manifest.json")
        if json.loads(path.read_text())["artifact_type"] == monthly.ARTIFACT_MONTH_NORMALIZED_15M_OHLCV
    )

    monthly.validate_saved_monthly_manifest(
        manifest,
        run_root=tmp_path,
        expected_run_id="run-validate-manifest",
        expected_artifact_type=monthly.ARTIFACT_MONTH_NORMALIZED_15M_OHLCV,
    )
    wrong_type = dict(manifest)
    wrong_type["artifact_type"] = monthly.ARTIFACT_RAW_PROVIDER_PAGE
    with pytest.raises(monthly.MonthlyAcquisitionError):
        monthly.validate_saved_monthly_manifest(wrong_type, run_root=tmp_path)
    wrong_stage = dict(manifest)
    wrong_stage["stage"] = "raw_provider_page"
    with pytest.raises(monthly.MonthlyAcquisitionError):
        monthly.validate_saved_monthly_manifest(wrong_stage, run_root=tmp_path)
    with pytest.raises(monthly.MonthlyAcquisitionError):
        monthly.validate_saved_monthly_manifest(manifest, run_root=tmp_path, expected_input_refs=("missing.json",))


def test_provider_response_variance_blocks_month(tmp_path: Path):
    request = _request()
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(expected, crash_after_body(200, _body(close="100"))),
            ScriptedExchange(expected, http_response(200, _body(close="100.0000001"))),
        ]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-variance",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_RESPONSE_VARIANCE
    assert receipt["semantic_retry_status"] == monthly.PROVIDER_RESPONSE_VARIANCE
    assert monthly.MONTH_ACQUISITION_RESPONSE_VARIANCE in receipt["fixed_findings"]


def test_different_continuation_projection_blocks_month(tmp_path: Path):
    request = _request()
    url_one = "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=one&adjusted=true&sort=asc&limit=50000"
    url_two = "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=two&adjusted=true&sort=asc&limit=50000"
    _, expected = _page_request(request, 1)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(expected, crash_after_body(200, _body(next_url=url_one))),
            ScriptedExchange(expected, http_response(200, _body(next_url=url_two))),
        ]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-continuation-variance",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_RESPONSE_VARIANCE
    assert receipt["semantic_retry_status"] == monthly.PROVIDER_RESPONSE_VARIANCE


def test_repeated_continuation_blocks_pagination(tmp_path: Path):
    request = _request()
    next_url = "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=repeat&adjusted=true&sort=asc&limit=50000"
    continuation = provider_response.sanitize_continuation_identity(next_url, _context(request))
    first_page, first_expected = _page_request(request, 1)
    _, second_expected = _page_request(request, 2, first_page.logical_page_request_id, continuation)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(first_expected, http_response(200, _body(next_url=next_url))),
            ScriptedExchange(second_expected, http_response(200, _body(t=1704105900000, next_url=next_url))),
        ]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-repeated-cont",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_PAGINATION_INVALID
    assert receipt["pagination_status"] == monthly.PAGINATION_CHAIN_INVALID
    assert "PAGINATION_REPEATED_CONTINUATION" in receipt["fixed_findings"]


def test_duplicate_timestamp_across_pages_blocks_pagination(tmp_path: Path):
    request = _request()
    next_url = "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=dup&adjusted=true&sort=asc&limit=50000"
    continuation = provider_response.sanitize_continuation_identity(next_url, _context(request))
    first_page, first_expected = _page_request(request, 1)
    _, second_expected = _page_request(request, 2, first_page.logical_page_request_id, continuation)
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(first_expected, http_response(200, _body(next_url=next_url))),
            ScriptedExchange(second_expected, http_response(200, _body())),
        ]
    )

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-dup-ts",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_PAGINATION_INVALID
    assert receipt["pagination_status"] == monthly.PAGINATION_CHAIN_INVALID
    assert "PAGINATION_DUPLICATE_TIMESTAMP" in receipt["fixed_findings"]


def test_cli_monthly_acquisition_self_check_is_sanitized_and_rejects_ticker_args():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--monthly-acquisition-self-check"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["status"] == "MARKETFLOW_FAKE_TRANSPORT_MONTHLY_ACQUISITION_SELF_CHECK"
    assert receipt["monthly_acquisition_status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["provider_execution_enabled"] is False
    assert receipt["acquisition_enabled"] is False
    assert receipt["runtime_migration_performed"] is False
    assert "api_key" not in result.stdout.lower()
    assert "next_url" not in result.stdout.lower()
    blocked = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--monthly-acquisition-self-check", "--ticker", "AAPL"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert blocked.returncode != 0


def test_monthly_acquisition_source_assurance_boundaries():
    package_files = [
        REPO_ROOT / "marketflow" / "historical_data" / "fake_transport.py",
        REPO_ROOT / "marketflow" / "historical_data" / "provider_response.py",
        REPO_ROOT / "marketflow" / "historical_data" / "monthly_acquisition.py",
    ]
    forbidden_modules = {
        "polygon",
        "requests",
        "httpx",
        "socket",
        "urllib",
        "yfinance",
        "openai",
        "marketflow.marketflow_data_provider",
        "marketflow.marketflow_polygon_tools",
        "marketflow.marketflow_strategy",
        "marketflow.backtesting.outcome_engine",
        "marketflow.historical_data.frozen_calendar",
        "marketflow.historical_data.rth_bar_engine",
    }
    combined = ""
    for path in package_files:
        source = path.read_text(encoding="utf-8")
        combined += source
        tree = ast.parse(source)
        imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
        assert forbidden_modules.isdisjoint(imported)
        assert forbidden_modules.isdisjoint(imported_from)
    assert "getenv" not in combined
    assert "environ" not in combined
    assert "os.replace" not in combined
    assert "glob(" not in combined
    assert "provider_native_4h" not in combined
    assert "provider_native_1d" not in combined
    assert "SCRIPTED_FAKE_TRANSPORT_FIXTURE" in combined
    assert "ZoneInfo(contract_v21.SESSION_MAPPING_TIMEZONE)" in combined
    assert "datetime.now()" not in combined
    assert ".astimezone()" not in combined
