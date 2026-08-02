from __future__ import annotations

import ast
import json
import subprocess
import sys
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import httpx
import pytest

from marketflow.historical_data import massive_date_diagnostic as diag
from marketflow.historical_data import massive_smoke as smoke
from marketflow.historical_data import monthly_acquisition as monthly


REPO_ROOT = Path(__file__).resolve().parents[1]
VALID_2026_TIMESTAMP = 1767277800000
SMOKE_SPEC_DIGEST = "2116c4dfa3e8ea759e5bca09cf0f4ccc329134f0cac1329ad871fb7746cdcfe4"
DATE_DIAGNOSTIC_DIGEST = "588e61a824799f24feedfeaa9b4629ed2f623b5ff0490624089562ca0eb63376"


def _body(
    *,
    ticker: str = "AAPL",
    status: str = "OK",
    query_count: int = 1,
    results_count: int = 1,
    count: int | None = 1,
    row_extra: str = ',"vw":9876.54,"otc":false',
    top_extra: str = "",
    row_values: tuple[str, str, str, str, str, str] = ("1234.50", "1235.50", "1233.50", "1234.75", "432100", "7"),
) -> bytes:
    open_value, high_value, low_value, close_value, volume_value, n_value = row_values
    count_part = "" if count is None else f',"count":{count}'
    return (
        '{"adjusted":true,"queryCount":'
        + str(query_count)
        + ',"results":[{"c":'
        + close_value
        + ',"h":'
        + high_value
        + ',"l":'
        + low_value
        + ',"n":'
        + n_value
        + ',"o":'
        + open_value
        + ',"t":'
        + str(VALID_2026_TIMESTAMP)
        + ',"v":'
        + volume_value
        + row_extra
        + '}],"resultsCount":'
        + str(results_count)
        + count_part
        + ',"status":"'
        + status
        + '","ticker":"'
        + ticker
        + '"'
        + top_extra
        + "}"
    ).encode("utf-8")


def _run_with_mock(handler, *, key: str = "fictional-date-diagnostic-key") -> dict[str, object]:
    spec = diag.default_date_diagnostic_spec()
    return diag.run_massive_date_diagnostic_2026_live(
        _input_func=lambda prompt: diag.date_diagnostic_confirmation_phrase(spec),
        _getpass_func=lambda prompt: key,
        _is_interactive=lambda: True,
        _http_transport=httpx.MockTransport(handler),
        _authorization_state=diag._AuthorizationState(),
        _emit_ceremony=False,
    )


def test_existing_2025_smoke_spec_and_digest_remain_unchanged():
    spec = smoke.default_smoke_spec()

    assert spec.provider == "MASSIVE.COM"
    assert spec.ticker == "AAPL"
    assert spec.month_key == "2025-01"
    assert spec.effective_start == "2025-01-01"
    assert spec.effective_end == "2025-01-31"
    assert smoke.smoke_spec_digest(spec) == SMOKE_SPEC_DIGEST


def test_date_diagnostic_spec_exact_values_immutable_and_noncanonical():
    spec = diag.default_date_diagnostic_spec()

    assert spec.schema_version == "marketflow.massive_provider_date_diagnostic.v1"
    assert spec.classification == "NONCANONICAL_PROVIDER_DATE_DIAGNOSTIC"
    assert spec.provider == "MASSIVE.COM"
    assert spec.endpoint == "STOCKS_CUSTOM_BARS_V2"
    assert spec.ticker == "AAPL"
    assert spec.month_key == "2026-01"
    assert spec.effective_start == "2026-01-01"
    assert spec.effective_end == "2026-01-31"
    assert spec.multiplier == 15
    assert spec.timespan == "minute"
    assert spec.adjusted is True
    assert spec.sort == "asc"
    assert spec.limit == 50000
    assert spec.maximum_provider_pages == 1
    assert spec.canonical_eligibility is False
    assert spec.registry_eligibility is False
    assert spec.acquisition_generation_eligibility is False
    assert spec.strategy_enabled is False
    with pytest.raises(FrozenInstanceError):
        spec.ticker = "MSFT"
    with pytest.raises(TypeError):
        diag.default_date_diagnostic_spec(ticker="MSFT")


def test_date_diagnostic_digest_is_deterministic_and_distinct_from_2025_smoke():
    spec = diag.default_date_diagnostic_spec()

    assert diag.date_diagnostic_spec_digest(spec) == DATE_DIAGNOSTIC_DIGEST
    assert diag.date_diagnostic_spec_digest(spec) == diag.date_diagnostic_spec_digest(diag.default_date_diagnostic_spec())
    assert diag.date_diagnostic_spec_digest(spec) != smoke.smoke_spec_digest()
    changed = replace(spec, effective_end="2026-01-30")
    with pytest.raises(diag.MassiveDateDiagnosticError):
        changed.validate()
    assert diag.date_diagnostic_spec_digest(changed) != diag.date_diagnostic_spec_digest(spec)


def test_plan_receipt_is_offline_sanitized_and_writes_nothing(tmp_path: Path):
    before = sorted(tmp_path.rglob("*"))

    receipt = diag.massive_date_diagnostic_2026_plan()

    assert receipt["status"] == diag.DATE_DIAGNOSTIC_PLAN_VALID
    assert receipt["network_execution_enabled"] is False
    assert receipt["credential_prompted"] is False
    assert receipt["request_performed"] is False
    assert receipt["raw_provider_body_persisted"] is False
    assert receipt["normalized_artifact_created"] is False
    assert receipt["monthly_executor_invoked"] is False
    assert receipt["ticker"] == "AAPL"
    assert receipt["effective_start"] == "2026-01-01"
    assert receipt["effective_end"] == "2026-01-31"
    assert receipt["operator_confirmation_phrase"] == "RUN MARKETFLOW MASSIVE DATE DIAGNOSTIC 588e61a82479"
    assert sorted(tmp_path.rglob("*")) == before


def test_canonical_monthly_acquisition_range_still_blocks_2026():
    with pytest.raises(monthly.MonthlyAcquisitionError, match="fixed 2022-01-01 through 2025-12-31 range"):
        monthly.build_month_chunk_request(
            canonical_ticker="FAKEFLOW",
            month_key="2026-01",
            effective_start_date="2026-01-01",
            effective_end_date="2026-01-31",
        )


def test_valid_response_is_schema_accepted_with_one_exact_request_and_no_pagination():
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body())

    receipt = _run_with_mock(handler)

    assert receipt["status"] == diag.DATE_DIAGNOSTIC_SCHEMA_ACCEPTED
    assert receipt["parser_status"] == diag.PARSER_SCHEMA_ACCEPTED
    assert receipt["http_status"] == 200
    assert receipt["response_body_complete"] is True
    assert receipt["query_count"] == 1
    assert receipt["results_count"] == 1
    assert receipt["results_present"] is True
    assert receipt["continuation_present"] is False
    assert receipt["transport_invocation_count"] == 1
    assert receipt["pagination_followed"] is False
    assert receipt["retry_attempted"] is False
    assert len(calls) == 1
    assert calls[0].method == "GET"
    assert calls[0].url.scheme == "https"
    assert calls[0].url.host == "api.massive.com"
    assert calls[0].url.path == "/v2/aggs/ticker/AAPL/range/15/minute/2026-01-01/2026-01-31"
    assert calls[0].url.params["adjusted"] == "true"
    assert calls[0].url.params["sort"] == "asc"
    assert calls[0].url.params["limit"] == "50000"
    assert calls[0].headers["Authorization"] == "Bearer fictional-date-diagnostic-key"
    assert calls[0].headers["Accept-Encoding"] == "identity"


def test_unknown_top_level_and_continuation_are_reported_by_structure_only():
    secret_next_url = (
        "https://api.massive.com/v2/aggs/ticker/AAPL/range/15/minute/"
        "2026-01-01/2026-01-31?cursor=opaque-secret-cursor&adjusted=true&sort=asc&limit=50000"
    )
    body = _body(top_extra=f',"mysteryTop":"secret-top-value","request_id":"secret-request","next_url":"{secret_next_url}"')
    receipt = _run_with_mock(lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=body))

    assert receipt["status"] == diag.DATE_DIAGNOSTIC_SCHEMA_REJECTED
    assert receipt["parser_status"] == diag.PARSER_SCHEMA_REJECTED
    assert receipt["continuation_present"] is True
    assert receipt["unexpected_top_level_fields"] == ["mysteryTop"]
    rendered = json.dumps(receipt, sort_keys=True)
    assert "secret-top-value" not in rendered
    assert "secret-request" not in rendered
    assert "opaque-secret-cursor" not in rendered
    assert "next_url" not in rendered
    assert "request_id" not in rendered


def test_unknown_row_field_and_missing_row_field_include_failing_row_index_only():
    body = _body(row_extra=',"mystery_row":"secret-row-value"')
    receipt = _run_with_mock(lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=body))

    assert receipt["status"] == diag.DATE_DIAGNOSTIC_SCHEMA_REJECTED
    assert receipt["aggregate_row_failures"] == [
        {"row_index": 0, "unexpected_row_fields": ["mystery_row"], "missing_row_fields": []}
    ]
    assert "secret-row-value" not in json.dumps(receipt, sort_keys=True)


def test_rejected_status_count_mismatch_and_type_mismatch_are_structural_only():
    body = _body(status="ERROR", count=0, row_values=("1234.50", "1235.50", "1233.50", "1234.75", "432100", '"bad-n"'))
    receipt = _run_with_mock(lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=body))

    assert receipt["status"] == diag.DATE_DIAGNOSTIC_SCHEMA_REJECTED
    assert receipt["provider_response_status"] == "ERROR"
    assert receipt["query_count"] == 1
    assert receipt["results_count"] == 1
    assert {"scope": "aggregate_row", "row_index": 0, "field": "n", "expected_type": "INTEGER", "actual_type": "STRING"} in receipt[
        "type_mismatches"
    ]
    assert "bad-n" not in json.dumps(receipt, sort_keys=True)


def test_top_level_type_mismatch_reports_fixed_json_categories():
    body = b'{"adjusted":true,"queryCount":"1","results":"not-array","resultsCount":1,"status":"OK","ticker":"AAPL"}'
    receipt = _run_with_mock(lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=body))

    assert receipt["status"] == diag.DATE_DIAGNOSTIC_SCHEMA_REJECTED
    assert receipt["results_present"] is False
    assert receipt["results_type"] == "STRING"
    assert {"scope": "top_level", "field": "queryCount", "expected_type": "INTEGER", "actual_type": "STRING"} in receipt[
        "type_mismatches"
    ]


def test_receipt_excludes_key_auth_url_body_market_values_and_request_metadata():
    body = _body(top_extra=',"request_id":"secret-request-id"')
    receipt = _run_with_mock(lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=body))

    rendered = json.dumps(receipt, sort_keys=True)
    forbidden = [
        "fictional-date-diagnostic-key",
        "Authorization",
        "Bearer",
        "api.massive.com",
        "/v2/aggs",
        "secret-request-id",
        "1234.50",
        "1235.50",
        "1233.50",
        "1234.75",
        "432100",
        "9876.54",
    ]
    for value in forbidden:
        assert value not in rendered


def test_live_mode_requires_tty_and_authorization_before_getpass_or_http():
    prompted = {"key": 0}
    requested = {"http": 0}
    noninteractive = diag.run_massive_date_diagnostic_2026_live(
        _input_func=lambda prompt: diag.date_diagnostic_confirmation_phrase(),
        _getpass_func=lambda prompt: prompted.__setitem__("key", prompted["key"] + 1) or "fictional",
        _is_interactive=lambda: False,
        _http_transport=httpx.MockTransport(lambda request: requested.__setitem__("http", requested["http"] + 1) or httpx.Response(200)),
        _authorization_state=diag._AuthorizationState(),
        _emit_ceremony=False,
    )
    wrong_phrase = diag.run_massive_date_diagnostic_2026_live(
        _input_func=lambda prompt: "wrong",
        _getpass_func=lambda prompt: prompted.__setitem__("key", prompted["key"] + 1) or "fictional",
        _is_interactive=lambda: True,
        _http_transport=httpx.MockTransport(lambda request: requested.__setitem__("http", requested["http"] + 1) or httpx.Response(200)),
        _authorization_state=diag._AuthorizationState(),
        _emit_ceremony=False,
    )

    assert noninteractive["status"] == diag.DATE_DIAGNOSTIC_INVALID
    assert noninteractive["fixed_findings"] == ["DATE_DIAGNOSTIC_REQUIRES_INTERACTIVE_TTY"]
    assert wrong_phrase["status"] == diag.DATE_DIAGNOSTIC_INVALID
    assert wrong_phrase["fixed_findings"] == ["DATE_DIAGNOSTIC_AUTHORIZATION_REJECTED"]
    assert prompted["key"] == 0
    assert requested["http"] == 0


def test_authorization_is_digest_bound_and_single_use():
    spec = diag.default_date_diagnostic_spec()
    state = diag._AuthorizationState()

    diag._authorize_diagnostic(diag.date_diagnostic_confirmation_phrase(spec), spec=spec, state=state)
    with pytest.raises(diag.MassiveDateDiagnosticError):
        diag._authorize_diagnostic(diag.date_diagnostic_confirmation_phrase(spec), spec=spec, state=state)
    with pytest.raises(diag.MassiveDateDiagnosticError):
        diag._authorize_diagnostic("RUN MARKETFLOW MASSIVE DATE DIAGNOSTIC wrong", spec=spec, state=diag._AuthorizationState())


@pytest.mark.parametrize("bad_key", ["", " ", " leading", "trailing ", "bad\rkey", "bad\nkey"])
def test_invalid_credential_values_are_rejected_without_http_or_secret_leak(bad_key: str):
    requested = {"http": 0}
    spec = diag.default_date_diagnostic_spec()
    receipt = diag.run_massive_date_diagnostic_2026_live(
        _input_func=lambda prompt: diag.date_diagnostic_confirmation_phrase(spec),
        _getpass_func=lambda prompt: bad_key,
        _is_interactive=lambda: True,
        _http_transport=httpx.MockTransport(lambda request: requested.__setitem__("http", requested["http"] + 1) or httpx.Response(200)),
        _authorization_state=diag._AuthorizationState(),
        _emit_ceremony=False,
    )

    assert receipt["status"] == diag.DATE_DIAGNOSTIC_AUTHENTICATION_FAILED
    assert receipt["credential_prompted"] is True
    assert requested["http"] == 0
    stripped = bad_key.strip()
    if stripped:
        assert stripped not in json.dumps(receipt, sort_keys=True)


def test_authentication_and_transport_failures_are_bounded_without_raw_exception():
    auth = _run_with_mock(lambda request: httpx.Response(401, headers={"Content-Type": "application/json"}, content=b'{"secret":"x"}'))

    def fail_transport(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("secret-host-value", request=request)

    failed = _run_with_mock(fail_transport)

    assert auth["status"] == diag.DATE_DIAGNOSTIC_AUTHENTICATION_FAILED
    assert auth["http_status"] == 401
    assert auth["response_body_complete"] is False
    assert failed["status"] == diag.DATE_DIAGNOSTIC_TRANSPORT_FAILED
    assert failed["fixed_findings"] == ["TRANSPORT_FAILURE"]
    assert "secret-host-value" not in json.dumps(failed, sort_keys=True)


def test_self_check_uses_mock_http_and_fictional_key_without_persistent_artifacts():
    receipt = diag.massive_date_diagnostic_2026_self_check()

    assert receipt["status"] == "MASSIVE_DATE_DIAGNOSTIC_2026_SELF_CHECK"
    assert receipt["diagnostic_specification_digest"] == DATE_DIAGNOSTIC_DIGEST
    assert receipt["valid_schema_status"] == diag.DATE_DIAGNOSTIC_SCHEMA_ACCEPTED
    assert receipt["rejected_schema_status"] == diag.DATE_DIAGNOSTIC_SCHEMA_REJECTED
    assert receipt["mock_http_only"] is True
    assert receipt["real_provider_call_performed"] is False
    assert receipt["persistent_artifact_written"] is False
    assert receipt["request_count"] == 2
    assert "fictional-date-diagnostic-key" not in json.dumps(receipt, sort_keys=True)


def test_cli_plan_self_check_run_and_override_boundaries():
    plan = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-date-diagnostic-2026-plan"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    plan_receipt = json.loads(plan.stdout)
    self_check = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-date-diagnostic-2026-self-check"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    run_noninteractive = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-date-diagnostic-2026-run"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    override = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-date-diagnostic-2026-plan", "--ticker", "MSFT"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert plan_receipt["status"] == diag.DATE_DIAGNOSTIC_PLAN_VALID
    assert plan_receipt["diagnostic_specification_digest"] == DATE_DIAGNOSTIC_DIGEST
    assert json.loads(self_check.stdout)["status"] == "MASSIVE_DATE_DIAGNOSTIC_2026_SELF_CHECK"
    assert run_noninteractive.returncode == 2
    assert json.loads(run_noninteractive.stdout)["fixed_findings"] == ["DATE_DIAGNOSTIC_REQUIRES_INTERACTIVE_TTY"]
    assert override.returncode != 0
    assert "unrecognized arguments" in override.stderr


def test_source_boundary_has_no_month_request_monthly_executor_strategy_or_credential_file_access():
    source = (REPO_ROOT / "marketflow" / "historical_data" / "massive_date_diagnostic.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    forbidden_text = [
        "MonthChunkRequest",
        "build_month_chunk_request",
        "execute_fake_monthly_acquisition",
        "ARTIFACT_MONTH_NORMALIZED_15M_OHLCV",
        "marketflow_strategy",
        "backtest",
        "monte",
        "os.environ",
        "getenv",
        "--api-key",
    ]
    for value in forbidden_text:
        assert value not in source
    assert "os" not in imported_roots
    assert "getpass" in imported_roots
