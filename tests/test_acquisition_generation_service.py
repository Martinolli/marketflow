from __future__ import annotations

import ast
import json
import os
from copy import deepcopy
from datetime import UTC, datetime, time
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import acquisition_provider_adapter_service as acquisition_adapter


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDENTITY_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
EXPECTED_CALENDAR_DIGEST = "25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6"
EXPECTED_SCHEDULE_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
EXPECTED_SPLIT_DIGEST = "9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae"
EXPECTED_DIVIDEND_DIGEST = "0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141"
EXPECTED_CONTRACT_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"
EXPECTED_DIVIDEND_IMPLICATION = "ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY"


def _epoch_ms(local_date: str, local_hhmm: str) -> int:
    hour, minute = (int(part) for part in local_hhmm.split(":", 1))
    local = datetime.fromisoformat(local_date).replace(hour=hour, minute=minute, tzinfo=ZoneInfo("America/New_York"))
    return int(local.astimezone(UTC).timestamp() * 1000)


def _row(timestamp_ms: int, index: int, *, optional: bool = True) -> dict:
    row = {
        "o": 100 + index,
        "h": 101 + index,
        "l": 99 + index,
        "c": 100 + index,
        "v": 1000 + index,
        "t": timestamp_ms,
    }
    if optional:
        row["vw"] = 100
        row["n"] = 10
        row["otc"] = False
    return row


def _body(timestamps: list[int], *, optional: bool = True) -> bytes:
    rows = [_row(timestamp, index, optional=optional) for index, timestamp in enumerate(timestamps)]
    payload = {
        "adjusted": True,
        "queryCount": len(rows),
        "results": rows,
        "resultsCount": len(rows),
        "count": len(rows),
        "status": "OK",
        "ticker": "AAPL",
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _single_month_timestamp(month: str) -> int:
    return _epoch_ms(f"{month}-01", "04:00")


def _january_2025_timestamps() -> list[int]:
    schedule = acquisition.calendar_service.build_exchange_calendar_schedule_rows_v1()
    january_sessions = [row for row in schedule if row["session_date"].startswith("2025-01") and row["is_full_session"] is True]
    rth: list[int] = []
    extended_candidates: list[int] = []
    for session in january_sessions:
        session_date = session["session_date"]
        for hour, minute in [(4, 0), (4, 15), (4, 30), (4, 45), (5, 0), (5, 15), (5, 30), (5, 45), (6, 0), (6, 15), (6, 30), (6, 45), (7, 0), (7, 15), (7, 30), (7, 45), (8, 0), (8, 15), (8, 30), (8, 45), (9, 0), (9, 15)]:
            extended_candidates.append(_epoch_ms(session_date, f"{hour:02d}:{minute:02d}"))
        for hour in range(9, 16):
            start_minute = 30 if hour == 9 else 0
            for minute in range(start_minute, 60, 15):
                if hour == 15 and minute > 45:
                    continue
                rth.append(_epoch_ms(session_date, f"{hour:02d}:{minute:02d}"))
        for hour, minute in [(16, 0), (16, 15), (16, 30), (16, 45), (17, 0), (17, 15), (17, 30), (17, 45), (18, 0), (18, 15), (18, 30), (18, 45), (19, 0), (19, 15), (19, 30), (19, 45), (20, 0), (20, 15), (20, 30), (20, 45), (21, 0)]:
            extended_candidates.append(_epoch_ms(session_date, f"{hour:02d}:{minute:02d}"))
    timestamps = sorted(rth + sorted(extended_candidates)[:757])
    assert len(rth) == 520
    assert len(timestamps) == 1277
    return timestamps


@lru_cache(maxsize=1)
def _provider_responses() -> tuple[dict, ...]:
    responses = []
    for chunk in acquisition.build_acquisition_month_chunks_v1():
        month = chunk["month"]
        timestamps = _january_2025_timestamps() if month == "2025-01" else [_single_month_timestamp(month)]
        responses.append({"month": month, "response": _body(timestamps)})
    return tuple(responses)


def _candidate() -> dict:
    return acquisition.build_acquisition_generation_candidate_v1(provider_responses=[deepcopy(item) for item in _provider_responses()])


def _monthly_smoke(api_key: str = "fake-live-smoke-key") -> dict:
    def transport(request: dict) -> bytes:
        assert request["provider_endpoint_path"] == "/v2/aggs/ticker/AAPL/range/15/minute/2025-01-01/2025-01-31"
        return _body(_january_2025_timestamps())

    return acquisition.build_acquisition_generation_monthly_live_smoke_v1(
        api_key=api_key,
        transport=transport,
        request_timestamp_utc="2026-08-06T00:00:00Z",
    )


def _full_live_candidate_with_transport(transport, api_key: str = "fake-full-live-key") -> dict:
    return acquisition.build_acquisition_generation_live_candidate_v1(
        api_key=api_key,
        transport=transport,
        provider_request_timestamp_utc="2026-08-07T00:00:00Z",
    )


def _transport_from_monthly_bodies(monthly_bodies: dict[str, bytes], calls: list[str] | None = None):
    def transport(request: dict) -> bytes:
        if calls is not None:
            calls.append(request["provider_endpoint_path"])
        month = str(request["provider_query_start"])[:7]
        return monthly_bodies[month]

    return transport


def _default_monthly_bodies() -> dict[str, bytes]:
    return {item["month"]: item["response"] for item in _provider_responses()}


def _recompute_digest(candidate: dict) -> None:
    candidate["acquisition_generation_candidate_semantic_digest"] = acquisition.acquisition_generation_candidate_semantic_digest(candidate)


def _recompute_smoke_digest(smoke: dict) -> None:
    smoke["acquisition_smoke_receipt_digest"] = acquisition.semantic_digest(acquisition._smoke_receipt_payload(smoke))
    smoke["acquisition_monthly_smoke_candidate_digest"] = acquisition.acquisition_monthly_smoke_candidate_digest_v1(smoke)


def _triage_row(
    month: str,
    *,
    status: str = "RTH_SOURCE_ROWS_RECONCILED",
    normalized_rows: int = 1280,
    rth_rows: int = 520,
    expected_rth_rows: int = 520,
    extended_rows: int = 760,
    incomplete_sessions: int = 0,
) -> dict:
    full_sessions = expected_rth_rows // 26
    return {
        "month": month,
        "rth_reconciliation_status": status,
        "normalized_source_rows": normalized_rows,
        "rth_rows": rth_rows,
        "extended_hours_rows": extended_rows,
        "expected_rth_rows": expected_rth_rows,
        "validated_rth_rows": rth_rows,
        "full_ordinary_sessions": full_sessions,
        "incomplete_ordinary_sessions": incomplete_sessions,
        "swing_rth_half_session_195m_bars": full_sessions * 2,
        "position_swing_rth_full_session_1d_bars": full_sessions,
    }


def _recompute_triage_digest(triage: dict) -> None:
    triage["triage_semantic_digest"] = acquisition.acquisition_monthly_reconciliation_triage_semantic_digest_v1(triage)


def _iso_utc(local_date: str, local_hhmm: str) -> str:
    hour, minute = (int(part) for part in local_hhmm.split(":", 1))
    local = datetime.fromisoformat(local_date).replace(hour=hour, minute=minute, tzinfo=ZoneInfo("America/New_York"))
    return local.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _normalized_source_row(local_date: str, local_hhmm: str, index: int = 0) -> dict:
    return {
        "ticker": "AAPL",
        "timestamp_utc": _iso_utc(local_date, local_hhmm),
        "timestamp_source": _epoch_ms(local_date, local_hhmm),
        "timestamp_source_timezone": "America/New_York",
        "source_interval_minutes": 15,
        "source_row_index": index,
        "source_chunk_id": f"AAPL-{local_date[:7]}",
        "source_month": local_date[:7],
        "raw_row_digest": "0" * 64,
    }


def _full_session_rows(session_date: str) -> list[dict]:
    rows: list[dict] = []
    index = 0
    for hour in range(9, 16):
        start_minute = 30 if hour == 9 else 0
        for minute in range(start_minute, 60, 15):
            rows.append(_normalized_source_row(session_date, f"{hour:02d}:{minute:02d}", index))
            index += 1
    return rows


def _half_session_rows(session_date: str) -> list[dict]:
    rows: list[dict] = []
    index = 0
    for hour, minute in [
        (9, 30),
        (9, 45),
        (10, 0),
        (10, 15),
        (10, 30),
        (10, 45),
        (11, 0),
        (11, 15),
        (11, 30),
        (11, 45),
        (12, 0),
        (12, 15),
        (12, 30),
        (12, 45),
    ]:
        rows.append(_normalized_source_row(session_date, f"{hour:02d}:{minute:02d}", index))
        index += 1
    return rows


def _single_session_schedule(session_date: str, *, close_local_hhmm: str = "16:00", session_minutes: int = 390) -> list[dict]:
    return [
        {
            "session_date": session_date,
            "market_open_utc": _iso_utc(session_date, "09:30"),
            "market_close_utc": _iso_utc(session_date, close_local_hhmm),
            "market_open_local": f"{session_date}T09:30:00-05:00",
            "market_close_local": f"{session_date}T{close_local_hhmm}:00-05:00",
            "session_minutes": session_minutes,
            "is_full_session": session_minutes == 390,
            "is_half_session": session_minutes == 210,
        }
    ]


def _recompute_per_session_digest(diagnostics: dict) -> None:
    diagnostics["per_session_diagnostics_semantic_digest"] = (
        acquisition.acquisition_per_session_reconciliation_diagnostics_semantic_digest_v1(diagnostics)
    )


def test_request_metadata_builds_without_api_key_leakage():
    request = acquisition.build_massive_custom_bars_request_v1(ticker="AAPL", start_date="2022-01-01", end_date="2022-01-31", api_key="secret")

    assert request["provider_endpoint"] == "/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}"
    assert request["provider_endpoint_path"] == "/v2/aggs/ticker/AAPL/range/15/minute/2022-01-01/2022-01-31"
    assert request["provider_multiplier"] == 15
    assert request["provider_timespan"] == "minute"
    assert request["provider_adjusted"] is True
    assert request["provider_sort"] == "asc"
    assert request["provider_limit"] == 50000
    assert request["api_key_supplied"] is True
    assert request["api_key_stored"] is False
    assert "secret" not in repr(request)
    assert "apiKey" not in request["request_url_without_credentials"]


def test_monthly_chunking_produces_48_chunks_for_fixed_range():
    chunks = acquisition.build_acquisition_month_chunks_v1()

    assert len(chunks) == 48
    assert chunks[0]["month"] == "2022-01"
    assert chunks[-1]["month"] == "2025-12"
    assert chunks[0]["effective_start_date"] == "2022-01-01"
    assert chunks[-1]["effective_end_date"] == "2025-12-31"
    assert [chunk["chunk_ordinal"] for chunk in chunks] == list(range(1, 49))


def test_fake_transport_can_generate_provider_response_without_live_calls():
    calls: list[str] = []

    def transport(request: dict) -> bytes:
        calls.append(request["provider_endpoint_path"])
        return _body([_single_month_timestamp("2025-01")])

    result = acquisition.fetch_massive_custom_bars_v1(
        ticker="AAPL",
        start_date="2025-01-01",
        end_date="2025-01-31",
        api_key="fake-key",
        transport=transport,
    )

    assert calls == ["/v2/aggs/ticker/AAPL/range/15/minute/2025-01-01/2025-01-31"]
    assert result["provider_response_status"] == "OK"
    assert result["provider_response_row_count"] == 1
    assert "fake-key" not in repr(result)


def test_provider_response_rows_normalize_deterministically_and_preserve_timestamps():
    chunk = next(item for item in acquisition.build_acquisition_month_chunks_v1() if item["month"] == "2025-01")
    result = acquisition.normalize_provider_response_rows_v1(chunk=chunk, provider_response_data=_body([_epoch_ms("2025-01-02", "09:30")]))
    row = result["normalized_rows"][0]

    assert row["ticker"] == "AAPL"
    assert row["timestamp_utc"] == "2025-01-02T14:30:00Z"
    assert row["timestamp_source"] == _epoch_ms("2025-01-02", "09:30")
    assert row["timestamp_source_timezone"] == "America/New_York"
    assert row["open"] == "100"
    assert row["high"] == "101"
    assert row["low"] == "99"
    assert row["close"] == "100"
    assert row["volume"] == "1000"
    assert row["vwap"] == "100"
    assert row["transactions"] == 10
    assert row["otc"] is False
    assert row["adjusted"] is True
    assert row["source_interval_minutes"] == 15
    assert row["source_chunk_id"] == "AAPL-2025-01"
    assert len(row["raw_row_digest"]) == 64


def test_missing_optional_provider_fields_remain_null():
    chunk = next(item for item in acquisition.build_acquisition_month_chunks_v1() if item["month"] == "2025-01")
    row = acquisition.normalize_provider_response_rows_v1(
        chunk=chunk,
        provider_response_data=_body([_epoch_ms("2025-01-02", "09:30")], optional=False),
    )["normalized_rows"][0]

    assert row["vwap"] is None
    assert row["transactions"] is None
    assert row["otc"] is None


def test_normalized_source_rows_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["normalized_source_rows_digest"] == second["normalized_source_rows_digest"]
    assert first["normalized_source_rows_digest"] == acquisition.normalized_source_rows_digest_v1(first["normalized_source_rows"])


def test_chunk_manifest_digest_is_deterministic():
    chunks = acquisition.build_acquisition_month_chunks_v1()

    assert acquisition.chunk_manifest_digest_v1(chunks) == acquisition.chunk_manifest_digest_v1(acquisition.build_acquisition_month_chunks_v1())


def test_monthly_reconciliation_digest_is_deterministic():
    candidate = _candidate()

    assert candidate["monthly_reconciliation_digest"] == acquisition.monthly_reconciliation_digest_v1(candidate["monthly_reconciliation"])


def test_candidate_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first == second
    assert len(first["acquisition_generation_candidate_semantic_digest"]) == 64
    assert first["acquisition_generation_candidate_semantic_digest"] == acquisition.acquisition_generation_candidate_semantic_digest(first)


def test_candidate_binds_required_frozen_authority_digests():
    candidate = _candidate()

    assert candidate["identity_segment_frozen_digest"] == EXPECTED_IDENTITY_DIGEST
    assert candidate["exchange_calendar_frozen_digest"] == EXPECTED_CALENDAR_DIGEST
    assert candidate["schedule_semantic_digest"] == EXPECTED_SCHEDULE_DIGEST
    assert candidate["split_event_audit_frozen_digest"] == EXPECTED_SPLIT_DIGEST
    assert candidate["dividend_event_audit_frozen_digest"] == EXPECTED_DIVIDEND_DIGEST
    assert candidate["acquisition_contract_digest"] == EXPECTED_CONTRACT_DIGEST


def test_candidate_preserves_dividend_implication():
    candidate = _candidate()

    assert candidate["in_range_dividends_found"] is True
    assert candidate["in_range_dividend_count"] == 16
    assert candidate["in_range_dividend_implication"] == EXPECTED_DIVIDEND_IMPLICATION


def test_candidate_status_is_ready_for_completed_fake_generation():
    candidate = _candidate()

    assert candidate["artifact_kind"] == "ACQUISITION_GENERATION_CANDIDATE"
    assert candidate["schema_version"] == "acquisition_generation_candidate_v1"
    assert candidate["candidate_status"] == "ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW"
    assert candidate["provider_response_injected"] is True
    assert candidate["provider_requests_made"] is False
    assert candidate["acquisition_generation_complete"] is True
    assert candidate["chunk_count_completed"] == 48
    assert candidate["failed_chunk_count"] == 0


def test_full_fake_live_orchestration_runs_all_48_monthly_chunks():
    calls: list[str] = []
    candidate = _full_live_candidate_with_transport(_transport_from_monthly_bodies(_default_monthly_bodies(), calls))

    assert len(calls) == 48
    assert calls[0] == "/v2/aggs/ticker/AAPL/range/15/minute/2022-01-01/2022-01-31"
    assert calls[-1] == "/v2/aggs/ticker/AAPL/range/15/minute/2025-12-01/2025-12-31"
    assert candidate["candidate_status"] == "ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW"
    assert candidate["provider_request_mode"] == "FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION"
    assert candidate["provider_requests_made"] is False
    assert candidate["provider_response_injected"] is True
    assert candidate["chunk_count_completed"] == 48
    assert candidate["failed_chunk_count"] == 0
    assert len(candidate["provider_chunk_records"]) == 48
    assert all("raw_row_count" in record for record in candidate["provider_chunk_records"])
    assert all("monthly_reconciliation_digest" in record for record in candidate["provider_chunk_records"])


def test_candidate_without_provider_responses_requires_live_execution_without_freeze():
    candidate = acquisition.build_acquisition_generation_candidate_v1()

    assert candidate["candidate_status"] == "ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION"
    assert candidate["provider_response_injected"] is False
    assert candidate["provider_requests_made"] is False
    assert candidate["acquisition_generation_complete"] is False
    assert candidate["acquisition_generation_freeze"] is False


def test_live_generation_records_failed_chunk_without_claiming_complete():
    bodies = _default_monthly_bodies()

    def transport(request: dict) -> bytes:
        if request["provider_query_start"].startswith("2022-02"):
            raise acquisition.AcquisitionGenerationError("synthetic provider failure")
        return bodies[str(request["provider_query_start"])[:7]]

    candidate = _full_live_candidate_with_transport(transport)
    validation = acquisition.validate_acquisition_generation_candidate_v1(candidate)

    assert candidate["candidate_status"] == "ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE"
    assert candidate["acquisition_generation_complete"] is False
    assert candidate["chunk_count_completed"] == 47
    assert candidate["failed_chunk_count"] == 1
    assert candidate["failed_chunks"][0]["chunk_id"] == "AAPL-2022-02"
    assert validation["candidate_status"] == "ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE"


def test_2025_01_cross_check_mismatch_prevents_ready_status():
    bodies = _default_monthly_bodies()
    bodies["2025-01"] = _body([_epoch_ms("2025-01-02", "09:30")])

    candidate = _full_live_candidate_with_transport(_transport_from_monthly_bodies(bodies))

    assert candidate["candidate_status"] == "ACQUISITION_GENERATION_2025_01_CROSS_CHECK_MISMATCH"
    assert candidate["acquisition_generation_complete"] is False
    acquisition.validate_acquisition_generation_candidate_v1(candidate)


def test_candidate_does_not_set_freeze_canonical_registry_or_runtime_eligibility():
    candidate = _candidate()

    assert candidate["acquisition_generation_freeze"] is False
    assert candidate["canonical_eligibility"] is False
    assert candidate["registry_eligibility"] is False
    assert candidate["strategy_runtime_migration"] is False
    assert candidate["automatic_stitching"] is False
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["profitability"] == "not accepted"


def test_validator_accepts_valid_fake_completed_candidate():
    receipt = acquisition.validate_acquisition_generation_candidate_v1(_candidate())

    assert receipt["status"] == "ACQUISITION_GENERATION_CANDIDATE_VALID"
    assert receipt["artifact_kind"] == "ACQUISITION_GENERATION_CANDIDATE"
    assert receipt["candidate_status"] == "ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW"
    assert receipt["chunk_count_expected"] == 48
    assert receipt["chunk_count_completed"] == 48
    assert receipt["failed_chunk_count"] == 0
    assert receipt["provider_requests_made"] is False


def test_validator_accepts_provider_backed_completed_candidate_without_freeze():
    candidate = acquisition.build_acquisition_generation_candidate_v1(
        provider_responses=[deepcopy(item) for item in _provider_responses()],
        provider_request_mode="LIVE_PROVIDER_REQUEST",
        provider_requests_made=True,
        provider_response_injected=False,
        created_offline=False,
        provider_request_timestamp_utc="2026-08-07T00:00:00Z",
    )
    receipt = acquisition.validate_acquisition_generation_candidate_v1(candidate)

    assert receipt["candidate_status"] == "ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW"
    assert receipt["provider_requests_made"] is True
    assert candidate["provider_response_injected"] is False
    assert candidate["acquisition_generation_freeze"] is False
    assert candidate["canonical_eligibility"] is False
    assert candidate["registry_eligibility"] is False
    assert candidate["strategy_runtime_migration"] is False


@pytest.mark.parametrize(
    ("field", "binding_field"),
    [
        ("identity_segment_frozen_digest", "identity_segment_frozen_digest"),
        ("exchange_calendar_frozen_digest", "exchange_calendar_frozen_digest"),
        ("schedule_semantic_digest", "schedule_semantic_digest"),
        ("split_event_audit_frozen_digest", "split_event_audit_frozen_digest"),
        ("dividend_event_audit_frozen_digest", "dividend_event_audit_frozen_digest"),
        ("acquisition_contract_digest", "acquisition_contract_digest"),
    ],
)
def test_validator_rejects_wrong_authority_digest(field: str, binding_field: str):
    candidate = _candidate()
    candidate[field] = "0" * 64
    candidate["authority_bindings"][binding_field] = "0" * 64
    _recompute_digest(candidate)

    with pytest.raises(acquisition.AcquisitionGenerationError, match=field):
        acquisition.validate_acquisition_generation_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "acquisition_generation_freeze",
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_validator_rejects_disallowed_authority_flags_true(field: str):
    candidate = _candidate()
    candidate[field] = True
    candidate["authority_boundary"][field] = True
    _recompute_digest(candidate)

    with pytest.raises(acquisition.AcquisitionGenerationError, match=field):
        acquisition.validate_acquisition_generation_candidate_v1(candidate)


@pytest.mark.parametrize("field", ["predictive_usefulness", "profitability"])
def test_validator_rejects_predictive_or_profitability_accepted(field: str):
    candidate = _candidate()
    candidate[field] = "accepted"
    candidate["authority_boundary"][field] = "accepted"
    _recompute_digest(candidate)

    with pytest.raises(acquisition.AcquisitionGenerationError, match=field):
        acquisition.validate_acquisition_generation_candidate_v1(candidate)


def test_validator_rejects_failed_chunks_while_complete():
    candidate = _candidate()
    candidate["failed_chunk_count"] = 1
    candidate["provider_failed_chunk_count"] = 1
    _recompute_digest(candidate)

    with pytest.raises(acquisition.AcquisitionGenerationError, match="failed_chunk_count"):
        acquisition.validate_acquisition_generation_candidate_v1(candidate)


@pytest.mark.parametrize("field", ["normalized_source_rows_digest", "monthly_reconciliation_digest"])
def test_validator_rejects_missing_required_digest_while_complete(field: str):
    candidate = _candidate()
    candidate[field] = None
    _recompute_digest(candidate)

    with pytest.raises(acquisition.AcquisitionGenerationError, match=field):
        acquisition.validate_acquisition_generation_candidate_v1(candidate)


def test_validator_rejects_2025_01_cross_check_mismatch_when_present():
    candidate = _candidate()
    january = next(item for item in candidate["monthly_reconciliation"] if item["month"] == "2025-01")
    january["validated_rth_rows"] = 519
    _recompute_digest(candidate)

    with pytest.raises(acquisition.AcquisitionGenerationError, match="2025-01.validated_rth_rows"):
        acquisition.validate_acquisition_generation_candidate_v1(candidate)


def test_accepted_2025_01_fixture_cross_check_passes_exactly():
    candidate = _candidate()
    january = next(item for item in candidate["monthly_reconciliation"] if item["month"] == "2025-01")

    assert january["normalized_source_rows"] == 1277
    assert january["extended_hours_rows"] == 757
    assert january["expected_rth_rows"] == 520
    assert january["validated_rth_rows"] == 520
    assert january["rth_reconciliation_status"] == "RTH_SOURCE_ROWS_RECONCILED"
    assert january["full_ordinary_sessions"] == 20
    assert january["incomplete_ordinary_sessions"] == 0
    assert january["swing_rth_half_session_195m_bars"] == 40
    assert january["position_swing_rth_full_session_1d_bars"] == 20


def test_rth_and_extended_hours_classification_counts_are_deterministic():
    candidate = _candidate()

    assert candidate["normalized_source_row_count"] == 1324
    assert candidate["rth_row_count"] == 520
    assert candidate["extended_hours_row_count"] == 788
    assert candidate["out_of_calendar_range_row_count"] == 16
    assert candidate["unknown_session_row_count"] == 0


def test_writer_is_json_no_overwrite(tmp_path: Path):
    result = acquisition.write_acquisition_generation_candidate_v1(tmp_path, candidate=_candidate())
    path = Path(result["path"])

    assert result["artifact_kind"] == "ACQUISITION_GENERATION_CANDIDATE"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["acquisition_generation_candidate_semantic_digest"] == result["acquisition_generation_candidate_semantic_digest"]
    with pytest.raises(acquisition.AcquisitionGenerationError, match="already exists"):
        acquisition.write_acquisition_generation_candidate_v1(tmp_path, candidate=_candidate())


def test_remaining_roadmap_tracks_post_candidate_work():
    roadmap = _candidate()["remaining_roadmap"]

    assert roadmap == [
        "Full live acquisition smoke/generation.",
        "Acquisition generation operator review package.",
        "Acquisition generation freeze.",
        "SWING canonical dataset candidate.",
        "POSITION_SWING canonical dataset candidate.",
    ]


def test_source_assurance_has_no_legacy_provider_strategy_runtime_or_broker_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "acquisition_generation_service.py"
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    called_attrs = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}

    forbidden_modules = {
        "httpx",
        "requests",
        "socket",
        "urllib",
        "polygon",
        "marketflow.marketflow_strategy",
        "marketflow.marketflow_data_provider",
        "marketflow.historical_data.massive_transport",
        "marketflow.historical_data.live_month_rth_diagnostic",
        "marketflow.historical_data.monthly_acquisition",
    }
    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert {"send", "post", "put", "delete", "request"}.isdisjoint(called_attrs)
    assert "ACQUISITION_GENERATION_FROZEN" in source


def test_service_exports_acquisition_generation_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE == "ACQUISITION_GENERATION_CANDIDATE"
    assert services.ARTIFACT_KIND_ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE == "ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE"
    assert services.ARTIFACT_KIND_ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE == "ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE"
    assert (
        services.ARTIFACT_KIND_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS
        == "ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS"
    )
    assert services.ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW == "ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW"
    assert services.ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE == "ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE"
    assert services.ACQUISITION_GENERATION_2025_01_CROSS_CHECK_MISMATCH == "ACQUISITION_GENERATION_2025_01_CROSS_CHECK_MISMATCH"
    assert services.ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_READY == "ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_READY"
    assert services.ACQUISITION_PER_SESSION_DIAGNOSTICS_COMPLETE == "ACQUISITION_PER_SESSION_DIAGNOSTICS_COMPLETE"
    assert services.LIVE_ACQUISITION_GENERATION_BLOCKED_GATE_NOT_ENABLED == "LIVE_ACQUISITION_GENERATION_BLOCKED_GATE_NOT_ENABLED"
    assert services.LIVE_ACQUISITION_GENERATION_BLOCKED_MISSING_API_KEY == "LIVE_ACQUISITION_GENERATION_BLOCKED_MISSING_API_KEY"
    assert services.ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW == "ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW"
    assert services.build_acquisition_generation_candidate_v1 is acquisition.build_acquisition_generation_candidate_v1
    assert services.build_acquisition_generation_live_candidate_v1 is acquisition.build_acquisition_generation_live_candidate_v1
    assert services.build_acquisition_generation_live_status_markdown_v1 is acquisition.build_acquisition_generation_live_status_markdown_v1
    assert services.build_acquisition_monthly_reconciliation_triage_v1 is acquisition.build_acquisition_monthly_reconciliation_triage_v1
    assert services.build_acquisition_monthly_reconciliation_triage_markdown_v1 is acquisition.build_acquisition_monthly_reconciliation_triage_markdown_v1
    assert (
        services.build_acquisition_per_session_reconciliation_diagnostics_v1
        is acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1
    )
    assert services.build_per_session_reconciliation_rows_v1 is acquisition.build_per_session_reconciliation_rows_v1
    assert services.build_acquisition_generation_monthly_live_smoke_v1 is acquisition.build_acquisition_generation_monthly_live_smoke_v1
    assert services.build_acquisition_month_chunks_v1 is acquisition.build_acquisition_month_chunks_v1
    assert services.build_massive_custom_bars_request_v1 is acquisition.build_massive_custom_bars_request_v1
    assert services.build_massive_custom_bars_live_request_v1 is acquisition_adapter.build_massive_custom_bars_live_request_v1
    assert services.validate_acquisition_generation_candidate_v1 is acquisition.validate_acquisition_generation_candidate_v1
    assert services.validate_acquisition_generation_monthly_live_smoke_v1 is acquisition.validate_acquisition_generation_monthly_live_smoke_v1
    assert services.validate_acquisition_monthly_reconciliation_triage_v1 is acquisition.validate_acquisition_monthly_reconciliation_triage_v1
    assert (
        services.validate_acquisition_per_session_reconciliation_diagnostics_v1
        is acquisition.validate_acquisition_per_session_reconciliation_diagnostics_v1
    )
    assert services.write_acquisition_generation_candidate_v1 is acquisition.write_acquisition_generation_candidate_v1
    assert services.write_acquisition_generation_live_status_v1 is acquisition.write_acquisition_generation_live_status_v1
    assert services.write_acquisition_monthly_reconciliation_triage_status_v1 is acquisition.write_acquisition_monthly_reconciliation_triage_status_v1
    assert (
        services.write_acquisition_per_session_reconciliation_diagnostics_status_v1
        is acquisition.write_acquisition_per_session_reconciliation_diagnostics_status_v1
    )
    assert services.write_per_session_reconciliation_csv_v1 is acquisition.write_per_session_reconciliation_csv_v1
    assert services.write_acquisition_generation_monthly_live_smoke_status_v1 is acquisition.write_acquisition_generation_monthly_live_smoke_status_v1
    assert services.classify_monthly_reconciliation_issue_v1 is acquisition.classify_monthly_reconciliation_issue_v1
    assert services.classify_session_reconciliation_issue_v1 is acquisition.classify_session_reconciliation_issue_v1
    assert services.parse_acquisition_live_status_chunk_manifest_v1 is acquisition.parse_acquisition_live_status_chunk_manifest_v1


def test_direct_live_request_builder_sanitizes_api_key():
    request = acquisition_adapter.build_massive_custom_bars_live_request_v1(
        ticker="AAPL",
        start_date="2025-01-01",
        end_date="2025-01-31",
        api_key="do-not-store-this-key",
        request_timestamp_utc="2026-08-06T00:00:00Z",
    )

    assert request["provider_endpoint"] == "/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}"
    assert request["provider_endpoint_path"] == "/v2/aggs/ticker/AAPL/range/15/minute/2025-01-01/2025-01-31"
    assert request["sanitized_url"] == "https://api.massive.com/v2/aggs/ticker/AAPL/range/15/minute/2025-01-01/2025-01-31?adjusted=true&sort=asc&limit=50000"
    assert request["headers"]["Authorization"] == "<redacted>"
    assert request["api_key_stored"] is False
    assert "do-not-store-this-key" not in repr(request)
    assert "apiKey" not in request["sanitized_url"]
    assert "api_key" not in request["sanitized_url"]


def test_direct_live_smoke_path_is_gated_and_fails_safely(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("MARKETFLOW_ENABLE_LIVE_ACQUISITION_GENERATION", raising=False)
    monkeypatch.delenv("MASSIVE_API_KEY", raising=False)
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)

    gate_blocked = acquisition.build_acquisition_generation_monthly_live_smoke_v1(request_timestamp_utc="2026-08-06T00:00:00Z")
    assert gate_blocked["candidate_status"] == "LIVE_ACQUISITION_SMOKE_BLOCKED_GATE_NOT_ENABLED"
    assert gate_blocked["provider_requests_made"] is False
    assert gate_blocked["acquisition_generation_freeze"] is False

    monkeypatch.setenv("MARKETFLOW_ENABLE_LIVE_ACQUISITION_GENERATION", "1")
    key_blocked = acquisition.build_acquisition_generation_monthly_live_smoke_v1(request_timestamp_utc="2026-08-06T00:00:00Z")
    assert key_blocked["candidate_status"] == "LIVE_ACQUISITION_SMOKE_BLOCKED_MISSING_API_KEY"
    assert key_blocked["provider_requests_made"] is False
    assert key_blocked["canonical_eligibility"] is False


def test_fake_monthly_live_smoke_result_normalizes_rows_deterministically():
    smoke = _monthly_smoke()

    assert smoke["artifact_kind"] == "ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE"
    assert smoke["candidate_status"] == "ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW"
    assert smoke["provider_request_mode"] == "FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION"
    assert smoke["provider_requests_made"] is False
    assert smoke["provider_response_injected"] is True
    assert smoke["provider_raw_row_count"] == 1277
    assert smoke["normalized_source_row_count"] == 1277
    assert smoke["normalized_source_rows"][0]["ticker"] == "AAPL"
    assert smoke["normalized_source_rows"][0]["timestamp_source_timezone"] == "America/New_York"


def test_fake_monthly_live_smoke_digests_are_deterministic():
    first = _monthly_smoke()
    second = _monthly_smoke()

    assert first["provider_raw_response_digest"] == second["provider_raw_response_digest"]
    assert first["normalized_source_rows_digest"] == second["normalized_source_rows_digest"]
    assert first["monthly_reconciliation_digest"] == second["monthly_reconciliation_digest"]
    assert first["acquisition_smoke_receipt_digest"] == second["acquisition_smoke_receipt_digest"]
    assert first["acquisition_monthly_smoke_candidate_digest"] == second["acquisition_monthly_smoke_candidate_digest"]
    assert first["normalized_source_rows_digest"] == acquisition.normalized_source_rows_digest_v1(first["normalized_source_rows"])
    assert first["monthly_reconciliation_digest"] == acquisition.monthly_reconciliation_digest_v1(first["monthly_reconciliation"])


def test_fake_monthly_live_smoke_validates_accepted_2025_01_cross_check():
    smoke = _monthly_smoke()
    validation = acquisition.validate_acquisition_generation_monthly_live_smoke_v1(smoke)

    assert validation["status"] == "ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE_VALID"
    assert validation["normalized_source_row_count"] == 1277
    assert validation["extended_hours_row_count"] == 757
    assert validation["expected_rth_rows"] == 520
    assert validation["rth_row_count"] == 520
    assert validation["rth_reconciliation_status"] == "RTH_SOURCE_ROWS_RECONCILED"
    assert validation["full_ordinary_sessions"] == 20
    assert validation["incomplete_ordinary_sessions"] == 0
    assert validation["accepted_2025_01_cross_check_passed"] is True


def test_monthly_live_smoke_validator_rejects_accepted_cross_check_mismatch():
    smoke = _monthly_smoke()
    smoke["validated_rth_rows"] = 519
    _recompute_smoke_digest(smoke)

    with pytest.raises(acquisition.AcquisitionGenerationError, match="validated_rth_rows"):
        acquisition.validate_acquisition_generation_monthly_live_smoke_v1(smoke)


def test_monthly_live_smoke_validator_rejects_mismatch_status_with_provider_digest():
    smoke = _monthly_smoke()
    smoke["candidate_status"] = "ACQUISITION_MONTHLY_LIVE_SMOKE_RECONCILIATION_MISMATCH"
    smoke["accepted_2025_01_cross_check_passed"] = False
    _recompute_smoke_digest(smoke)

    with pytest.raises(acquisition.AcquisitionGenerationError, match="candidate_status"):
        acquisition.validate_acquisition_generation_monthly_live_smoke_v1(smoke)


@pytest.mark.parametrize(
    "field",
    [
        "acquisition_generation_freeze",
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_monthly_live_smoke_validator_rejects_disallowed_authority_flags_true(field: str):
    smoke = _monthly_smoke()
    smoke[field] = True
    smoke["authority_boundary"][field] = True
    _recompute_smoke_digest(smoke)

    with pytest.raises(acquisition.AcquisitionGenerationError, match=field):
        acquisition.validate_acquisition_generation_monthly_live_smoke_v1(smoke)


def test_monthly_live_smoke_status_doc_contains_no_api_key_or_raw_payload(tmp_path: Path):
    secret = "secret-live-smoke-value"
    smoke = _monthly_smoke(api_key=secret)
    text = acquisition.build_acquisition_generation_monthly_live_smoke_markdown_v1(smoke)
    result = acquisition.write_acquisition_generation_monthly_live_smoke_status_v1(tmp_path / "smoke.md", smoke=smoke)
    written = Path(result["path"]).read_text(encoding="utf-8")

    assert secret not in repr(smoke)
    assert secret not in text
    assert secret not in written
    assert '"results"' not in text
    assert "Raw provider payload stored in this document: `False`" in text
    assert "No acquisition-generation freeze was created." in text
    assert "No canonical, registry, runtime, predictive, or profitability approval occurred." in text


def test_full_live_status_doc_contains_required_sanitized_summary(tmp_path: Path):
    secret = "secret-full-live-value"
    candidate = _full_live_candidate_with_transport(_transport_from_monthly_bodies(_default_monthly_bodies()), api_key=secret)
    text = acquisition.build_acquisition_generation_live_status_markdown_v1(candidate)
    result = acquisition.write_acquisition_generation_live_status_v1(
        tmp_path / "MARKETFLOW_ACQUISITION_LIVE_GENERATION_2022_2025_STATUS.md",
        candidate=candidate,
    )
    written = Path(result["path"]).read_text(encoding="utf-8")

    assert secret not in repr(candidate)
    assert secret not in text
    assert secret not in written
    assert '"results"' not in text
    assert "Endpoint used: `/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}`" in text
    assert "Expected chunk count: `48`" in text
    assert "Completed chunk count: `48`" in text
    assert "2025-01 cross-check result: `PASSED`" in text
    assert "API key stored: `False`" in text
    assert "No acquisition-generation freeze was created." in text
    assert "No canonical, registry, runtime, predictive, or profitability approval occurred." in text


def test_triage_identifies_reconciled_months():
    row = acquisition.classify_monthly_reconciliation_issue_v1(_triage_row("2025-01", normalized_rows=1277, extended_rows=757))

    assert row["issue_category"] == "RECONCILED"
    assert row["issue_severity"] == "INFO"
    assert row["requires_operator_review"] is False


def test_triage_identifies_non_reconciled_months_and_delta():
    row = acquisition.classify_monthly_reconciliation_issue_v1(
        _triage_row(
            "2024-11",
            status="RTH_SOURCE_ROWS_NOT_RECONCILED",
            rth_rows=508,
            expected_rth_rows=520,
            incomplete_sessions=1,
        )
    )

    assert row["issue_category"] == "MISSING_PROVIDER_ROWS"
    assert row["issue_severity"] == "HIGH"
    assert row["rth_row_delta"] == -12
    assert row["requires_provider_recheck"] is True


def test_triage_computes_39_9_summary_from_committed_status_fixture():
    status_text = (REPO_ROOT / "docs" / "status" / "MARKETFLOW_ACQUISITION_LIVE_GENERATION_2022_2025_STATUS.md").read_text(encoding="utf-8")
    rows = acquisition.parse_acquisition_live_status_chunk_manifest_v1(status_text)
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1(rows)

    assert triage["total_months"] == 48
    assert triage["reconciled_months"] == 39
    assert triage["not_reconciled_months"] == 9
    assert triage["non_reconciled_months"] == [
        "2022-11",
        "2023-07",
        "2023-11",
        "2024-07",
        "2024-11",
        "2024-12",
        "2025-07",
        "2025-11",
        "2025-12",
    ]


def test_non_reconciled_unknown_detail_months_are_high_severity():
    status_text = (REPO_ROOT / "docs" / "status" / "MARKETFLOW_ACQUISITION_LIVE_GENERATION_2022_2025_STATUS.md").read_text(encoding="utf-8")
    rows = acquisition.parse_acquisition_live_status_chunk_manifest_v1(status_text)
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1(rows)
    unresolved = [row for row in triage["triage_rows"] if row["reconciliation_status"] == "RTH_SOURCE_ROWS_NOT_RECONCILED"]

    assert len(unresolved) == 9
    assert {row["issue_category"] for row in unresolved} == {"INSUFFICIENT_DETAIL"}
    assert {row["issue_severity"] for row in unresolved} == {"HIGH"}


def test_2025_01_reconciled_fixture_is_info_and_not_blocker():
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1(
        [_triage_row("2025-01", normalized_rows=1277, extended_rows=757)]
    )
    row = triage["triage_rows"][0]

    assert triage["accepted_2025_01_cross_check_status"] == "PASSED"
    assert row["issue_category"] == "RECONCILED"
    assert row["issue_severity"] == "INFO"
    assert triage["blocker_count"] == 0


def test_2025_01_mismatch_becomes_blocker():
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1(
        [
            _triage_row(
                "2025-01",
                status="RTH_SOURCE_ROWS_NOT_RECONCILED",
                normalized_rows=1276,
                rth_rows=519,
                expected_rth_rows=520,
                extended_rows=757,
                incomplete_sessions=1,
            )
        ]
    )

    assert triage["accepted_2025_01_cross_check_status"] == "FAILED"
    assert triage["blocker_count"] == 1
    assert triage["triage_rows"][0]["issue_severity"] == "BLOCKER"


def test_triage_with_unresolved_non_reconciled_months_blocks_acquisition_review():
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1(
        [
            _triage_row("2024-10"),
            _triage_row(
                "2024-11",
                status="RTH_SOURCE_ROWS_NOT_RECONCILED",
                rth_rows=508,
                expected_rth_rows=520,
                incomplete_sessions=1,
            ),
        ]
    )

    assert triage["ready_for_acquisition_review"] is False
    assert triage["operator_review_required"] is True
    assert triage["triage_status"] == "ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_BLOCKS_ACQUISITION_REVIEW"


def test_triage_with_all_months_reconciled_allows_acquisition_review():
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1(
        [_triage_row("2024-10"), _triage_row("2024-12", expected_rth_rows=520, rth_rows=520)]
    )

    assert triage["ready_for_acquisition_review"] is True
    assert triage["operator_review_required"] is False
    assert triage["triage_status"] == "ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_READY"


def test_triage_preserves_no_freeze_canonical_registry_or_runtime_authority():
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1([_triage_row("2025-01")])

    assert triage["acquisition_generation_freeze"] is False
    assert triage["canonical_eligibility"] is False
    assert triage["registry_eligibility"] is False
    assert triage["strategy_runtime_migration"] is False
    assert triage["authority_boundary"]["acquisition_generation_freeze"] is False


def test_triage_validator_rejects_wrong_source_acquisition_candidate_digest():
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1([_triage_row("2025-01")])
    triage["source_acquisition_candidate_digest"] = "0" * 64
    _recompute_triage_digest(triage)

    with pytest.raises(acquisition.AcquisitionGenerationError, match="source_acquisition_candidate_digest"):
        acquisition.validate_acquisition_monthly_reconciliation_triage_v1(triage)


@pytest.mark.parametrize(
    "field",
    [
        "acquisition_generation_freeze",
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
    ],
)
def test_triage_validator_rejects_disallowed_authority_flags_true(field: str):
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1([_triage_row("2025-01")])
    triage[field] = True
    _recompute_triage_digest(triage)

    with pytest.raises(acquisition.AcquisitionGenerationError, match=field):
        acquisition.validate_acquisition_monthly_reconciliation_triage_v1(triage)


def test_triage_status_doc_contains_non_reconciled_month_summary(tmp_path: Path):
    status_text = (REPO_ROOT / "docs" / "status" / "MARKETFLOW_ACQUISITION_LIVE_GENERATION_2022_2025_STATUS.md").read_text(encoding="utf-8")
    rows = acquisition.parse_acquisition_live_status_chunk_manifest_v1(status_text)
    triage = acquisition.build_acquisition_monthly_reconciliation_triage_v1(rows)
    text = acquisition.build_acquisition_monthly_reconciliation_triage_markdown_v1(triage)
    result = acquisition.write_acquisition_monthly_reconciliation_triage_status_v1(tmp_path / "triage.md", triage=triage)
    written = Path(result["path"]).read_text(encoding="utf-8")

    assert "Non-reconciled months: `9`" in text
    assert "2022-11, 2023-07, 2023-11, 2024-07, 2024-11, 2024-12, 2025-07, 2025-11, 2025-12" in text
    assert "Acquisition operator review: `BLOCKED`" in text
    assert "No provider refresh was performed." in text
    assert '"results"' not in written
    assert "API_KEY" not in written


def test_per_session_reconciliation_identifies_reconciled_full_session():
    rows = acquisition.build_per_session_reconciliation_rows_v1(
        _full_session_rows("2025-01-02"),
        target_months=["2025-01"],
        schedule_rows=_single_session_schedule("2025-01-02"),
    )

    assert len(rows) == 1
    assert rows[0]["expected_15m_bars"] == 26
    assert rows[0]["observed_15m_bars"] == 26
    assert rows[0]["rth_row_delta"] == 0
    assert rows[0]["issue_category"] == "RECONCILED"
    assert rows[0]["issue_severity"] == "INFO"


def test_per_session_reconciliation_identifies_missing_rth_bars():
    rows = acquisition.build_per_session_reconciliation_rows_v1(
        _full_session_rows("2024-11-04")[:-2],
        target_months=["2024-11"],
        schedule_rows=_single_session_schedule("2024-11-04"),
    )

    assert rows[0]["expected_15m_bars"] == 26
    assert rows[0]["observed_15m_bars"] == 24
    assert rows[0]["rth_row_delta"] == -2
    assert rows[0]["missing_count"] == 2
    assert rows[0]["issue_category"] == "MISSING_RTH_BARS"
    assert rows[0]["issue_severity"] == "HIGH"
    assert rows[0]["requires_provider_recheck"] is True


def test_per_session_reconciliation_identifies_extra_rth_bars():
    source_rows = _full_session_rows("2024-07-01")
    source_rows.append(_normalized_source_row("2024-07-01", "15:45", 99))

    rows = acquisition.build_per_session_reconciliation_rows_v1(
        source_rows,
        target_months=["2024-07"],
        schedule_rows=_single_session_schedule("2024-07-01"),
    )

    assert rows[0]["observed_15m_bars"] == 27
    assert rows[0]["rth_row_delta"] == 1
    assert rows[0]["extra_count"] == 1
    assert rows[0]["issue_category"] == "EXTRA_RTH_BARS"
    assert rows[0]["requires_calendar_logic_review"] is True


def test_per_session_reconciliation_excludes_timestamp_at_exact_market_close():
    source_rows = _full_session_rows("2025-01-02")
    source_rows.append(_normalized_source_row("2025-01-02", "16:00", 100))

    rows = acquisition.build_per_session_reconciliation_rows_v1(
        source_rows,
        target_months=["2025-01"],
        schedule_rows=_single_session_schedule("2025-01-02"),
    )

    assert rows[0]["observed_15m_bars"] == 26
    assert rows[0]["issue_category"] == "RECONCILED"


def test_per_session_reconciliation_excludes_premarket_row():
    source_rows = [_normalized_source_row("2025-01-02", "09:15", 100)] + _full_session_rows("2025-01-02")

    rows = acquisition.build_per_session_reconciliation_rows_v1(
        source_rows,
        target_months=["2025-01"],
        schedule_rows=_single_session_schedule("2025-01-02"),
    )

    assert rows[0]["observed_15m_bars"] == 26
    assert rows[0]["first_observed_rth_timestamp_utc"] == _iso_utc("2025-01-02", "09:30")


def test_per_session_reconciliation_supports_early_close_session():
    rows = acquisition.build_per_session_reconciliation_rows_v1(
        _half_session_rows("2025-11-28"),
        target_months=["2025-11"],
        schedule_rows=_single_session_schedule("2025-11-28", close_local_hhmm="13:00", session_minutes=210),
    )

    assert rows[0]["session_type"] == "HALF"
    assert rows[0]["expected_15m_bars"] == 14
    assert rows[0]["observed_15m_bars"] == 14
    assert rows[0]["issue_category"] == "RECONCILED"


def test_per_session_reconciliation_flags_non_15_minute_session_duration():
    rows = acquisition.build_per_session_reconciliation_rows_v1(
        [],
        target_months=["2025-11"],
        schedule_rows=_single_session_schedule("2025-11-28", close_local_hhmm="13:05", session_minutes=215),
    )

    assert rows[0]["expected_15m_bars"] is None
    assert rows[0]["issue_category"] == "CALENDAR_SESSION_DURATION_REVIEW_REQUIRED"
    assert rows[0]["issue_severity"] == "HIGH"
    assert rows[0]["requires_calendar_logic_review"] is True


def test_per_session_reconciliation_records_first_last_and_chunk_metadata():
    rows = acquisition.build_per_session_reconciliation_rows_v1(
        _full_session_rows("2025-01-02"),
        target_months=["2025-01"],
        schedule_rows=_single_session_schedule("2025-01-02"),
    )

    assert rows[0]["first_observed_rth_timestamp_utc"] == _iso_utc("2025-01-02", "09:30")
    assert rows[0]["last_observed_rth_timestamp_utc"] == _iso_utc("2025-01-02", "15:45")
    assert rows[0]["provider_chunk_id"] == "AAPL-2025-01"
    assert rows[0]["provider_chunk_month"] == "2025-01"


def test_per_session_diagnostics_blocks_when_row_level_data_is_missing():
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1()

    assert diagnostics["diagnostics_status"] == "ACQUISITION_PER_SESSION_DIAGNOSTICS_BLOCKED_MISSING_ROW_LEVEL_DATA"
    assert diagnostics["row_level_source_available"] is False
    assert diagnostics["session_diagnostics_available"] is False
    assert diagnostics["blocked_reason"] == "ROW_LEVEL_NORMALIZED_SOURCE_DATA_NOT_AVAILABLE"
    assert diagnostics["target_months"] == [
        "2022-11",
        "2023-07",
        "2023-11",
        "2024-07",
        "2024-11",
        "2024-12",
        "2025-07",
        "2025-11",
        "2025-12",
    ]


def test_per_session_diagnostics_missing_row_level_data_keeps_acquisition_review_blocked():
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1()

    assert diagnostics["ready_for_acquisition_review"] is False
    assert diagnostics["operator_review_required"] is True
    assert diagnostics["provider_requests_made"] is False
    assert diagnostics["provider_refresh_performed"] is False
    assert diagnostics["full_rerun_performed"] is False


def test_per_session_diagnostics_summarizes_reconciled_sessions():
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1(
        _full_session_rows("2025-01-02"),
        target_months=["2025-01"],
        schedule_rows=_single_session_schedule("2025-01-02"),
    )

    assert diagnostics["diagnostics_status"] == "ACQUISITION_PER_SESSION_DIAGNOSTICS_COMPLETE"
    assert diagnostics["total_sessions_evaluated"] == 1
    assert diagnostics["reconciled_sessions"] == 1
    assert diagnostics["non_reconciled_sessions"] == 0
    assert diagnostics["ready_for_acquisition_review"] is True


def test_per_session_diagnostics_summarizes_non_reconciled_sessions_as_high():
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1(
        _full_session_rows("2024-12-02")[:-1],
        target_months=["2024-12"],
        schedule_rows=_single_session_schedule("2024-12-02"),
    )

    assert diagnostics["diagnostics_status"] == "ACQUISITION_PER_SESSION_DIAGNOSTICS_REQUIRES_OPERATOR_REVIEW"
    assert diagnostics["missing_bar_sessions"] == 1
    assert diagnostics["high_count"] == 1
    assert diagnostics["issue_category_summary"] == {"MISSING_RTH_BARS": 1}
    assert diagnostics["ready_for_acquisition_review"] is False


def test_per_session_diagnostics_2025_01_reconciled_is_not_blocker():
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1(
        _full_session_rows("2025-01-02"),
        target_months=["2025-01"],
        schedule_rows=_single_session_schedule("2025-01-02"),
    )

    assert diagnostics["accepted_2025_01_cross_check_status"] == "PASSED"
    assert diagnostics["blocker_count"] == 0
    assert diagnostics["session_diagnostics"][0]["issue_severity"] == "INFO"


def test_per_session_diagnostics_2025_01_mismatch_is_blocker():
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1(
        _full_session_rows("2025-01-02")[:-1],
        target_months=["2025-01"],
        schedule_rows=_single_session_schedule("2025-01-02"),
    )

    assert diagnostics["accepted_2025_01_cross_check_status"] == "FAILED"
    assert diagnostics["blocker_count"] == 1
    assert diagnostics["session_diagnostics"][0]["issue_severity"] == "BLOCKER"


def test_per_session_diagnostics_preserves_no_freeze_canonical_registry_or_runtime_authority():
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1()

    assert diagnostics["acquisition_generation_freeze"] is False
    assert diagnostics["canonical_eligibility"] is False
    assert diagnostics["registry_eligibility"] is False
    assert diagnostics["strategy_runtime_migration"] is False
    assert diagnostics["automatic_stitching"] is False
    assert diagnostics["authority_boundary"]["acquisition_generation_freeze"] is False


def test_per_session_diagnostics_validator_rejects_wrong_source_acquisition_candidate_digest():
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1()
    diagnostics["source_acquisition_candidate_digest"] = "0" * 64
    _recompute_per_session_digest(diagnostics)

    with pytest.raises(acquisition.AcquisitionGenerationError, match="source_acquisition_candidate_digest"):
        acquisition.validate_acquisition_per_session_reconciliation_diagnostics_v1(diagnostics)


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "provider_refresh_performed",
        "full_rerun_performed",
        "acquisition_generation_freeze",
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_per_session_diagnostics_validator_rejects_disallowed_authority_or_provider_flags_true(field: str):
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1()
    diagnostics[field] = True
    _recompute_per_session_digest(diagnostics)

    with pytest.raises(acquisition.AcquisitionGenerationError, match=field):
        acquisition.validate_acquisition_per_session_reconciliation_diagnostics_v1(diagnostics)


def test_per_session_diagnostics_validator_rejects_summary_count_drift():
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1(
        _full_session_rows("2025-01-02"),
        target_months=["2025-01"],
        schedule_rows=_single_session_schedule("2025-01-02"),
    )
    diagnostics["reconciled_sessions"] = 0
    _recompute_per_session_digest(diagnostics)

    with pytest.raises(acquisition.AcquisitionGenerationError, match="reconciled_sessions"):
        acquisition.validate_acquisition_per_session_reconciliation_diagnostics_v1(diagnostics)


def test_per_session_diagnostics_status_doc_reports_blocked_missing_row_level_data(tmp_path: Path):
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1()
    text = acquisition.build_acquisition_per_session_reconciliation_diagnostics_markdown_v1(diagnostics)
    result = acquisition.write_acquisition_per_session_reconciliation_diagnostics_status_v1(
        tmp_path / "per_session.md",
        diagnostics=diagnostics,
    )
    written = Path(result["path"]).read_text(encoding="utf-8")

    assert "Diagnostics status: `ACQUISITION_PER_SESSION_DIAGNOSTICS_BLOCKED_MISSING_ROW_LEVEL_DATA`" in text
    assert "Blocked reason: `ROW_LEVEL_NORMALIZED_SOURCE_DATA_NOT_AVAILABLE`" in text
    assert "Acquisition operator review: `BLOCKED`" in text
    assert "No provider refresh was performed." in written
    assert "No per-session rows were fabricated from monthly totals." in written
    assert "API_KEY" not in written


def test_per_session_diagnostics_csv_writer_uses_compact_non_raw_columns(tmp_path: Path):
    diagnostics = acquisition.build_acquisition_per_session_reconciliation_diagnostics_v1(
        _full_session_rows("2025-01-02"),
        target_months=["2025-01"],
        schedule_rows=_single_session_schedule("2025-01-02"),
    )

    result = acquisition.write_per_session_reconciliation_csv_v1(
        tmp_path / "sessions.csv",
        diagnostics["session_diagnostics"],
    )
    text = Path(result["path"]).read_text(encoding="utf-8")
    header = text.splitlines()[0].split(",")

    assert result["row_count"] == 1
    assert header == acquisition.PER_SESSION_RECONCILIATION_CSV_COLUMNS
    assert "open" not in header
    assert "high" not in header
    assert "low" not in header
    assert "close" not in header
    assert "volume" not in header
    assert "raw_row_digest" not in text


@pytest.mark.skipif(
    os.environ.get("MARKETFLOW_ENABLE_LIVE_ACQUISITION_GENERATION") != "1"
    or not (os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")),
    reason="live acquisition generation is explicitly gated and requires an API key",
)
def test_optional_live_smoke_is_not_part_of_default_suite():
    smoke = acquisition.build_acquisition_generation_monthly_live_smoke_v1(request_timestamp_utc="2026-08-06T00:00:00Z")
    if smoke["candidate_status"] != "ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW":
        pytest.fail(f"manual live acquisition smoke did not pass: {smoke['candidate_status']}")
    acquisition.validate_acquisition_generation_monthly_live_smoke_v1(smoke)
