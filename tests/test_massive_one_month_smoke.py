from __future__ import annotations

import ast
import json
import subprocess
import sys
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import httpx
import pytest

from marketflow.historical_data import massive_smoke as smoke
from marketflow.historical_data import monthly_acquisition as monthly
from marketflow.historical_data.massive_transport import MassiveRestTransport, ProviderApiKey


REPO_ROOT = Path(__file__).resolve().parents[1]


def _body(*, ticker: str = "AAPL", t: int = 1735741800000, next_url: str | None = None) -> bytes:
    next_part = f',"next_url":"{next_url}"' if next_url else ""
    return (
        '{"adjusted":true,"queryCount":1,"results":[{"c":100,"h":101,"l":99,"n":1,'
        '"o":100,"t":'
        + str(t)
        + ',"v":1000}],"resultsCount":1,"status":"OK","ticker":"'
        + ticker
        + '"'
        + next_part
        + "}"
    ).encode("utf-8")


def _full_month_body() -> bytes:
    return (
        b'{"adjusted":true,"queryCount":2,"results":['
        b'{"c":100,"h":101,"l":99,"n":1,"o":100,"t":1735741800000,"v":1000},'
        b'{"c":101,"h":102,"l":100,"n":1,"o":101,"t":1738333800000,"v":1000}'
        b'],"resultsCount":2,"status":"OK","ticker":"AAPL"}'
    )


def _next_url(cursor: str = "next") -> str:
    return (
        "https://api.massive.com/v2/aggs/ticker/AAPL/range/15/minute/"
        f"2025-01-01/2025-01-31?cursor={cursor}&adjusted=true&sort=asc&limit=50000"
    )


def _mock_factory(handler):
    def factory(month_request: monthly.MonthChunkRequest, api_key: ProviderApiKey) -> MassiveRestTransport:
        return MassiveRestTransport(month_request=month_request, api_key=api_key, http_transport=httpx.MockTransport(handler))

    return factory


def _run_with_mock(tmp_path: Path, handler, *, key: str = "fictional-smoke-key", run_id: str = "smoke-opaque-run"):
    spec = smoke.default_smoke_spec()
    return smoke.run_massive_smoke_live(
        run_root=tmp_path,
        _input_func=lambda prompt: smoke.smoke_confirmation_phrase(spec),
        _getpass_func=lambda prompt: key,
        _is_interactive=lambda: True,
        _transport_factory=_mock_factory(handler),
        _run_id_factory=lambda: run_id,
        _authorization_state=smoke._AuthorizationState(),
        _emit_ceremony=False,
    )


def test_smoke_spec_exact_values_immutable_and_no_override_constructor():
    spec = smoke.default_smoke_spec()

    assert spec.smoke_schema_version == "marketflow.massive_provider_smoke.v1"
    assert spec.classification == "NONCANONICAL_PROVIDER_SMOKE"
    assert spec.provider == "MASSIVE.COM"
    assert spec.endpoint == "STOCKS_CUSTOM_BARS_V2"
    assert spec.ticker == "AAPL"
    assert spec.month_key == "2025-01"
    assert spec.effective_start == "2025-01-01"
    assert spec.effective_end == "2025-01-31"
    assert spec.multiplier == 15
    assert spec.timespan == "minute"
    assert spec.adjusted is True
    assert spec.sort == "asc"
    assert spec.limit == 50000
    assert spec.strategy_enabled is False
    assert spec.calendar_bar_derivation_enabled is False
    assert spec.registry_eligibility is False
    assert spec.canonical_eligibility is False
    with pytest.raises(FrozenInstanceError):
        spec.ticker = "MSFT"
    with pytest.raises(TypeError):
        smoke.default_smoke_spec(ticker="MSFT")


def test_smoke_digest_is_deterministic_and_semantic_change_changes_digest():
    spec = smoke.default_smoke_spec()

    assert smoke.smoke_spec_bytes(spec) == smoke.smoke_spec_bytes(smoke.default_smoke_spec())
    assert smoke.smoke_spec_digest(spec) == smoke.smoke_spec_digest(smoke.default_smoke_spec())
    changed = replace(spec, ticker="MSFT")
    with pytest.raises(smoke.MassiveSmokeError):
        changed.validate()
    assert smoke.smoke_spec_digest(changed) != smoke.smoke_spec_digest(spec)


def test_plan_receipt_is_offline_sanitized_and_writes_nothing(tmp_path: Path):
    before = sorted(tmp_path.rglob("*"))

    receipt = smoke.massive_smoke_plan()

    assert receipt["status"] == "SMOKE_PLAN_VALID"
    assert receipt["network_execution_enabled"] is False
    assert receipt["credential_prompted"] is False
    assert receipt["runtime_artifact_written"] is False
    assert receipt["ticker"] == "AAPL"
    assert receipt["month_key"] == "2025-01"
    assert sorted(tmp_path.rglob("*")) == before


def test_authorization_phrase_accepts_exact_and_rejects_wrong_or_reused():
    spec = smoke.default_smoke_spec()
    state = smoke._AuthorizationState()

    smoke._authorize_smoke(smoke.smoke_confirmation_phrase(spec), spec=spec, state=state)
    with pytest.raises(smoke.MassiveSmokeError):
        smoke._authorize_smoke(smoke.smoke_confirmation_phrase(spec), spec=spec, state=state)
    with pytest.raises(smoke.MassiveSmokeError):
        smoke._authorize_smoke("RUN MARKETFLOW MASSIVE SMOKE wrong", spec=spec, state=smoke._AuthorizationState())
    with pytest.raises(smoke.MassiveSmokeError):
        smoke._authorize_smoke("wrong", spec=spec, state=smoke._AuthorizationState())


def test_default_live_authorization_state_rejects_reused_success(monkeypatch, tmp_path: Path):
    spec = smoke.default_smoke_spec()
    monkeypatch.setattr(smoke, "_LIVE_AUTHORIZATION_STATE", smoke._AuthorizationState())

    first = smoke.run_massive_smoke_live(
        run_root=tmp_path / "first",
        _input_func=lambda prompt: smoke.smoke_confirmation_phrase(spec),
        _getpass_func=lambda prompt: "fictional-smoke-key",
        _is_interactive=lambda: True,
        _transport_factory=_mock_factory(
            lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=_full_month_body())
        ),
        _run_id_factory=lambda: "smoke-default-state-first",
        _emit_ceremony=False,
    )
    second = smoke.run_massive_smoke_live(
        run_root=tmp_path / "second",
        _input_func=lambda prompt: smoke.smoke_confirmation_phrase(spec),
        _getpass_func=lambda prompt: pytest.fail("credential prompt must not occur after reused authorization"),
        _is_interactive=lambda: True,
        _transport_factory=lambda month_request, api_key: pytest.fail("transport must not be constructed"),
        _emit_ceremony=False,
    )

    assert first["smoke_status"] == "SMOKE_COMPLETED_NONCANONICAL"
    assert second["smoke_status"] == "SMOKE_AUTHORIZATION_REJECTED"


def test_wrong_authorization_does_not_prompt_for_credential():
    prompted = {"key": False}
    receipt = smoke.run_massive_smoke_live(
        run_root=Path("unused"),
        _input_func=lambda prompt: "wrong",
        _getpass_func=lambda prompt: prompted.__setitem__("key", True) or "fictional",
        _is_interactive=lambda: True,
        _transport_factory=lambda month_request, api_key: pytest.fail("transport must not be constructed"),
        _authorization_state=smoke._AuthorizationState(),
        _emit_ceremony=False,
    )

    assert receipt["smoke_status"] == "SMOKE_AUTHORIZATION_REJECTED"
    assert prompted["key"] is False


@pytest.mark.parametrize("bad_key", ["", " ", " leading-secret", "trailing-secret ", "bad-secret\rvalue", "bad-secret\nvalue"])
def test_hidden_fictional_key_boundary_rejects_invalid_values(bad_key: str):
    spec = smoke.default_smoke_spec()
    receipt = smoke.run_massive_smoke_live(
        run_root=Path("unused"),
        _input_func=lambda prompt: smoke.smoke_confirmation_phrase(spec),
        _getpass_func=lambda prompt: bad_key,
        _is_interactive=lambda: True,
        _transport_factory=lambda month_request, api_key: pytest.fail("transport must not be constructed"),
        _authorization_state=smoke._AuthorizationState(),
        _emit_ceremony=False,
    )

    assert receipt["smoke_status"] == "SMOKE_CREDENTIAL_REJECTED"
    rendered = json.dumps(receipt, sort_keys=True)
    assert "leading-secret" not in rendered
    assert "trailing-secret" not in rendered
    assert "bad-secret" not in rendered


def test_live_run_requires_interactive_tty_and_rejects_piped_key():
    prompted = {"key": False}
    receipt = smoke.run_massive_smoke_live(
        run_root=Path("unused"),
        _input_func=lambda prompt: smoke.smoke_confirmation_phrase(),
        _getpass_func=lambda prompt: prompted.__setitem__("key", True) or "fictional",
        _is_interactive=lambda: False,
        _transport_factory=lambda month_request, api_key: pytest.fail("transport must not be constructed"),
    )

    assert receipt["smoke_status"] == "SMOKE_AUTHORIZATION_REJECTED"
    assert receipt["fixed_findings"] == ["LIVE_SMOKE_REQUIRES_INTERACTIVE_TTY"]
    assert prompted["key"] is False


def test_one_page_success_uses_exact_month_request_and_sanitized_receipt(tmp_path: Path):
    seen: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["authorization"] = request.headers.get("Authorization", "")
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=_full_month_body())

    receipt = _run_with_mock(tmp_path, handler)

    assert receipt["smoke_status"] == "SMOKE_COMPLETED_NONCANONICAL"
    assert receipt["provider_execution_enabled"] is True
    assert "/v2/aggs/ticker/AAPL/range/15/minute/2025-01-01/2025-01-31" in seen["url"]
    assert "adjusted=true" in seen["url"]
    assert "sort=asc" in seen["url"]
    assert "limit=50000" in seen["url"]
    assert "apiKey" not in seen["url"] and "api_key" not in seen["url"]
    assert seen["authorization"] == "Bearer fictional-smoke-key"
    rendered = json.dumps(receipt, sort_keys=True)
    assert "fictional-smoke-key" not in rendered
    assert "Authorization" not in rendered
    assert "next_url" not in rendered
    assert '"open"' not in rendered and '"close"' not in rendered
    assert receipt["raw_page_count"] == 1
    assert receipt["total_normalized_row_count"] == 2


def test_credential_like_continuation_is_rejected_before_raw_persistence(tmp_path: Path):
    bad_next_url = (
        "https://api.massive.com/v2/aggs/ticker/AAPL/range/15/minute/"
        "2025-01-01/2025-01-31?cursor=opaque&apiKey=leak&adjusted=true&sort=asc&limit=50000"
    )
    receipt = _run_with_mock(
        tmp_path,
        lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body(next_url=bad_next_url)),
        run_id="smoke-bad-continuation-run",
    )

    assert receipt["smoke_status"] == "SMOKE_PROVIDER_RESPONSE_REJECTED"
    assert receipt["request_status"] == monthly.MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED
    assert receipt["pagination_status"] == monthly.PAGINATION_NOT_STARTED
    assert receipt["raw_page_count"] == 0
    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in tmp_path.rglob("*") if path.is_file())
    assert "apiKey" not in all_text
    assert "leak" not in all_text
    assert "next_url" not in all_text


def test_first_page_401_maps_to_credential_rejected_without_artifacts_or_retry(tmp_path: Path):
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(401, headers={"Content-Type": "application/json"}, content=b"")

    receipt = _run_with_mock(tmp_path, handler, run_id="smoke-auth-401-run")

    assert receipt["smoke_status"] == "SMOKE_CREDENTIAL_REJECTED"
    assert receipt["request_status"] == monthly.MONTH_ACQUISITION_AUTHENTICATION_FAILED
    assert receipt["pagination_status"] == monthly.PAGINATION_NOT_STARTED
    assert receipt["completeness_status"] == "INCOMPLETE"
    assert receipt["fixed_findings"] == [monthly.AUTHENTICATION_FAILURE]
    assert receipt["attempt_count"] == 1
    assert receipt["accepted_page_count"] == 0
    assert receipt["raw_page_count"] == 0
    assert receipt["normalized_artifact_receipts"] == []
    assert len(seen_urls) == 1
    assert "apiKey" not in seen_urls[0] and "api_key" not in seen_urls[0]

    receipt_text = json.dumps(receipt, sort_keys=True)
    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in tmp_path.rglob("*") if path.is_file())
    for text in (receipt_text, all_text):
        assert "fictional-smoke-key" not in text
        assert "Authorization" not in text
        assert "Bearer" not in text
        assert "apiKey" not in text and "api_key" not in text
        assert "next_url" not in text


def test_first_page_schema_failure_maps_to_provider_response_rejected(tmp_path: Path):
    seen_urls: list[str] = []
    body = (
        b'{"adjusted":true,"queryCount":1,"results":[{"c":100,"h":101,"l":99,"n":1,'
        b'"o":100,"t":1735741800000,"v":1000}],"resultsCount":1,"status":"OK",'
        b'"ticker":"AAPL","mysteryField":"request-123-next-secret-1000"}'
    )

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=body)

    receipt = _run_with_mock(tmp_path, handler, run_id="smoke-schema-200-run")

    assert receipt["smoke_status"] == "SMOKE_PROVIDER_RESPONSE_REJECTED"
    assert receipt["request_status"] == monthly.MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED
    assert receipt["pagination_status"] == monthly.PAGINATION_NOT_STARTED
    assert receipt["completeness_status"] == "INCOMPLETE"
    assert receipt["fixed_findings"] == [monthly.RESPONSE_SCHEMA_INVALID]
    assert receipt["attempt_count"] == 1
    assert receipt["accepted_page_count"] == 0
    assert receipt["raw_page_count"] == 0
    assert receipt["normalized_artifact_receipts"] == []
    assert len(seen_urls) == 1

    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in tmp_path.rglob("*") if path.is_file())
    for forbidden in ("fictional-smoke-key", "Authorization", "Bearer", "apiKey", "next_url", "request-123-next-secret-1000"):
        assert forbidden not in all_text


def test_first_page_timestamp_range_failure_is_invalid_not_schema_rejected(tmp_path: Path):
    receipt = _run_with_mock(
        tmp_path,
        lambda request: httpx.Response(
            200,
            headers={"Content-Type": "application/json"},
            content=_body(t=1738396800000),
        ),
        run_id="smoke-timestamp-range-run",
    )

    assert receipt["smoke_status"] == "SMOKE_INVALID"
    assert receipt["request_status"] == monthly.MONTH_ACQUISITION_INVALID
    assert receipt["fixed_findings"] == [monthly.TIMESTAMP_RANGE_INVALID]
    assert receipt["raw_page_count"] == 0
    assert receipt["normalized_artifact_receipts"] == []


def test_multi_page_success_retry_then_success_and_no_automatic_rerun(tmp_path: Path):
    responses = iter(
        [
            httpx.Response(500, headers={"Content-Type": "application/json"}, content=b'{"status":"ERROR"}'),
            httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body(next_url=_next_url())),
            httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body(t=1738333800000)),
        ]
    )
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return next(responses)

    receipt = _run_with_mock(tmp_path, handler, run_id="smoke-retry-run")

    assert receipt["smoke_status"] == "SMOKE_COMPLETED_NONCANONICAL"
    assert receipt["request_status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["pagination_status"] == monthly.PAGINATION_EXHAUSTED
    assert receipt["completeness_status"] == "COMPLETE"
    assert receipt["attempt_count"] == 3
    assert receipt["accepted_page_count"] == 2
    assert receipt["raw_page_count"] == 2
    assert len(receipt["normalized_artifact_receipts"]) == 2
    assert len(seen_urls) == 3
    assert "cursor=next" in seen_urls[-1]


def test_transport_failure_and_sparse_one_page_month_statuses(tmp_path: Path):
    failed = _run_with_mock(
        tmp_path / "failed",
        lambda request: httpx.Response(500, headers={"Content-Type": "application/json"}, content=b'{"status":"ERROR"}'),
        run_id="smoke-failed-run",
    )
    sparse = _run_with_mock(
        tmp_path / "sparse",
        lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body(t=1735828200000)),
        run_id="smoke-sparse-run",
    )

    assert failed["smoke_status"] == "SMOKE_TRANSPORT_FAILED"
    assert failed["attempt_count"] == 3
    assert sparse["smoke_status"] == "SMOKE_COMPLETED_NONCANONICAL"
    assert sparse["request_status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert sparse["pagination_status"] == monthly.PAGINATION_EXHAUSTED
    assert sparse["completeness_status"] == "COMPLETE"
    assert sparse["accepted_page_count"] == 1
    assert sparse["raw_page_count"] == 1
    assert sparse["total_normalized_row_count"] > 0
    assert sparse["normalized_artifact_receipts"]
    assert "RANGE_COVERAGE_INCOMPLETE" not in sparse["fixed_findings"]


def test_pagination_failure_is_invalid_without_second_run(tmp_path: Path):
    responses = iter(
        [
            httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body(next_url=_next_url("dup"))),
            httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body()),
        ]
    )
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return next(responses)

    receipt = _run_with_mock(tmp_path, handler, run_id="smoke-pagination-run")

    assert receipt["smoke_status"] == "SMOKE_INVALID"
    assert receipt["request_status"] == monthly.MONTH_ACQUISITION_PAGINATION_INVALID
    assert receipt["pagination_status"] == monthly.PAGINATION_CHAIN_INVALID
    assert "PAGINATION_DUPLICATE_TIMESTAMP" in receipt["fixed_findings"]
    assert len(seen_urls) == 2


def test_smoke_artifacts_are_isolated_opaque_noncanonical_and_sanitized(tmp_path: Path):
    receipt = _run_with_mock(
        tmp_path,
        lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=_full_month_body()),
        run_id="smoke-opaque-123",
    )

    run_dirs = [item for item in tmp_path.iterdir() if item.is_dir()]
    assert [item.name for item in run_dirs] == ["smoke-opaque-123"]
    assert "AAPL" not in run_dirs[0].name
    assert "2025-01" not in run_dirs[0].name
    assert receipt["smoke_receipt_ref"] == "smoke-opaque-123/smoke_receipt/smoke-receipt.json"
    assert receipt["classification"] == "NONCANONICAL_PROVIDER_SMOKE"
    assert receipt["request_status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["pagination_status"] == monthly.PAGINATION_EXHAUSTED
    assert receipt["completeness_status"] == "COMPLETE"
    assert receipt["provenance"] == "LIVE_PROVIDER_SMOKE_NONCANONICAL"
    assert receipt["canonical_eligibility"] is False
    assert receipt["registry_eligibility"] is False
    assert receipt["strategy_enabled"] is False
    assert receipt["calendar_bar_derivation_enabled"] is False

    for manifest_path in tmp_path.rglob("*.manifest.json"):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["provenance"] == "LIVE_PROVIDER_SMOKE_NONCANONICAL"
    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in tmp_path.rglob("*") if path.is_file())
    assert "fictional-smoke-key" not in all_text
    assert "Authorization" not in all_text
    assert "apiKey" not in all_text and "api_key" not in all_text
    assert "CANONICAL" in all_text
    assert "canonical_eligibility\":false" in all_text


def test_plan_and_self_check_cli_are_offline_sanitized_and_live_cli_is_noninteractive_rejected():
    plan = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-smoke-plan"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    plan_receipt = json.loads(plan.stdout)
    assert plan_receipt["status"] == "SMOKE_PLAN_VALID"
    assert plan_receipt["credential_prompted"] is False
    assert plan_receipt["network_execution_enabled"] is False

    self_check = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-smoke-self-check"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(self_check.stdout)
    assert receipt["status"] == "MASSIVE_SMOKE_SELF_CHECK"
    assert receipt["mock_http_only"] is True
    assert receipt["real_provider_call_performed"] is False
    assert receipt["persistent_artifact_written"] is False
    assert "fictional-smoke-self-check-key" not in self_check.stdout

    live = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-smoke-run"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert live.returncode == 2
    assert json.loads(live.stdout)["smoke_status"] == "SMOKE_AUTHORIZATION_REJECTED"


def test_cli_accepts_no_semantic_or_key_overrides():
    blocked = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-smoke-plan", "--ticker", "MSFT", "--api-key", "secret"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert blocked.returncode != 0
    assert "unrecognized arguments" in blocked.stderr


def test_massive_smoke_source_assurance_boundaries():
    source = REPO_ROOT.joinpath("marketflow/historical_data/massive_smoke.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    attrs = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}

    assert "getpass" in imported
    assert "os" not in imported
    assert "getenv" not in attrs
    assert "environ" not in attrs
    assert "SMOKE_TICKER = \"AAPL\"" in source
    assert "SMOKE_MONTH_KEY = \"2025-01\"" in source
    assert "NONCANONICAL_PROVIDER_SMOKE" in source
    assert "registry_eligibility=False" in source
    assert "canonical_eligibility=False" in source
    assert "ProviderApiKey(_getpass_func(" in source
    assert "--api-key" not in source
    assert "?apiKey" not in source
    assert "api.polygon.io" not in source
    assert {None, "getpass", "json", "sys", "tempfile", "uuid", "dataclasses", "pathlib", "typing", "httpx"}.issuperset(imported)
    forbidden_modules = {
        "marketflow.marketflow_strategy",
        "marketflow.historical_data.frozen_calendar",
        "marketflow.historical_data.rth_bar_engine",
        "marketflow.historical_data.pipeline",
        "marketflow.services.monte_carlo_service",
        "marketflow.services.backtest_result_service",
        "marketflow.services.backtesting.outcome_engine",
    }
    assert forbidden_modules.isdisjoint(imported_from)
