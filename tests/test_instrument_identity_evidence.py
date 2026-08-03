from __future__ import annotations

import ast
import json
import subprocess
import sys
from dataclasses import FrozenInstanceError, asdict, replace
from pathlib import Path

import httpx
import pytest

from marketflow.historical_data.massive_transport import ProviderApiKey
from marketflow.research import acquisition_contract_v2 as acv2
from marketflow.research import acquisition_contract_v2_1 as acv21
from marketflow.research import fixed_date_acquisition_contract as acv1
from marketflow.source_authority import instrument_identity as ident


REPO_ROOT = Path(__file__).resolve().parents[1]
V1_DIGEST = "29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e"
V2_DIGEST = "59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0"
V21_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"


def _response(**overrides) -> bytes:
    results = {
        "ticker": "AAPL",
        "active": True,
        "market": "stocks",
        "locale": "us",
        "currency_name": "usd",
        "primary_exchange": "XNAS",
        "composite_figi": "BBG000B9XRY4",
        "share_class_figi": "BBG001S5N8V8",
        "type": "CS",
        "cik": "320193",
        "list_date": "1980-12-12",
        "delisted_utc": None,
        "name": "Apple Inc.",
        "homepage_url": "https://example.invalid",
        "phone_number": "555-0100",
        "description": "not public evidence",
        "market_cap": 1,
        "total_employees": 1,
        "share_class_shares_outstanding": 1,
        "weighted_shares_outstanding": 1,
        "branding": {"logo_url": "https://example.invalid/logo.png"},
        "address": {"city": "Cupertino"},
    }
    results.update(overrides.pop("results", {}))
    payload = {"status": "OK", "request_id": "rid-secret", "count": 1, "results": results}
    payload.update(overrides)
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _snapshot(body: bytes | None = None, as_of_date: str = ident.START_SNAPSHOT_DATE) -> ident.IdentitySnapshot:
    return ident.parse_ticker_overview_response(body or _response(), as_of_date=as_of_date)


def test_identity_specification_fixed_immutable_and_digest_deterministic():
    spec = ident.default_identity_specification()

    assert spec.schema_version == "marketflow.instrument_identity_specification.v1"
    assert spec.classification == ident.PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL
    assert spec.provider == "MASSIVE.COM"
    assert spec.endpoint_family == ident.TICKER_OVERVIEW_V3
    assert spec.ticker == "AAPL"
    assert spec.start_snapshot_date == "2022-01-01"
    assert spec.end_snapshot_date == "2025-12-31"
    assert spec.expected_market == "stocks"
    assert spec.expected_locale == "us"
    assert spec.expected_currency == "usd"
    assert spec.canonical_eligibility is False
    assert spec.registry_eligibility is False
    assert spec.generation_freeze_eligibility is False
    assert spec.strategy_enabled is False
    assert ident.instrument_identity_specification_digest() == ident.instrument_identity_specification_digest()
    with pytest.raises(FrozenInstanceError):
        spec.ticker = "MSFT"  # type: ignore[misc]


def test_prepare_request_uses_fixed_ticker_dates_host_headers_and_no_key_url():
    prepared = ident.prepare_ticker_overview_request("2022-01-01", ProviderApiKey("fictional-key"))

    assert prepared.method == "GET"
    assert prepared.url == "https://api.massive.com/v3/reference/tickers/AAPL?date=2022-01-01"
    assert prepared.sanitized_url == prepared.url
    assert prepared.headers["Authorization"] == "Bearer fictional-key"
    assert prepared.headers["Accept"] == "application/json"
    assert prepared.headers["Accept-Encoding"] == "identity"
    assert "api" not in prepared.url.lower().split("?", 1)[1].replace("api.massive", "")
    with pytest.raises(ident.InstrumentIdentityError):
        ident.prepare_ticker_overview_request("2023-01-01", ProviderApiKey("fictional-key"))


def test_transport_two_snapshot_requests_use_mock_no_retry_no_cookie_and_security_settings():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=_response())

    transport = ident.TickerOverviewTransport(api_key=ProviderApiKey("fictional-key"), http_transport=httpx.MockTransport(handler))
    start_body = transport.send("2022-01-01")
    end_body = transport.send("2025-12-31")

    assert start_body == _response()
    assert end_body == _response()
    assert transport.call_count == 2
    assert transport.client.follow_redirects is False
    assert transport.client.trust_env is False
    assert transport.client.timeout.connect == 10
    assert [request.url.params["date"] for request in seen] == ["2022-01-01", "2025-12-31"]
    for request in seen:
        assert request.url.scheme == "https"
        assert request.url.host == "api.massive.com"
        assert request.url.path == "/v3/reference/tickers/AAPL"
        assert set(request.url.params.keys()) == {"date"}
        assert request.headers["Authorization"] == "Bearer fictional-key"
        assert request.headers["Accept-Encoding"] == "identity"
        assert "Cookie" not in request.headers
        assert "key" not in str(request.url).lower()


def test_transport_rejects_non_json_or_non_200_without_retry():
    transport = ident.TickerOverviewTransport(
        api_key=ProviderApiKey("fictional-key"),
        http_transport=httpx.MockTransport(lambda request: httpx.Response(500, content=b"{}")),
    )

    with pytest.raises(ident.InstrumentIdentityError):
        transport.send("2022-01-01")
    assert transport.call_count == 1


def test_parser_accepts_complete_snapshot_count_absent_and_optional_statuses():
    snapshot = _snapshot()
    # Remove count instead of setting JSON null.
    payload = json.loads(_response())
    payload.pop("count")
    absent = _snapshot(json.dumps(payload).encode("utf-8"))

    assert snapshot.snapshot_status == ident.IDENTITY_SNAPSHOT_COMPLETE
    assert absent.snapshot_status == ident.IDENTITY_SNAPSHOT_COMPLETE
    assert snapshot.ticker == "AAPL"
    assert snapshot.active is True
    assert snapshot.market == "stocks"
    assert snapshot.locale == "us"
    assert snapshot.currency_name == "usd"
    assert snapshot.primary_exchange == "XNAS"
    assert snapshot.composite_figi == "BBG000B9XRY4"
    assert snapshot.share_class_figi == "BBG001S5N8V8"
    assert snapshot.type == "CS"
    assert snapshot.cik_status == ident.PRESENT
    assert snapshot.list_date_status == ident.PRESENT
    assert snapshot.delisted_utc_status == ident.NOT_RETURNED
    assert len(snapshot.identity_projection_digest) == 64


@pytest.mark.parametrize(
    "payload",
    [
        {"extra": True},
        {"count": 2},
        {"count": -1},
        {"results": []},
        {"status": "ERROR"},
    ],
)
def test_parser_rejects_top_level_contract_violations(payload: dict[str, object]):
    base = json.loads(_response())
    base.update(payload)

    with pytest.raises(ident.InstrumentIdentityError):
        _snapshot(json.dumps(base).encode("utf-8"))


def test_parser_rejects_unknown_result_field():
    with pytest.raises(ident.InstrumentIdentityError):
        _snapshot(_response(results={"unexpected": "x"}))


def test_parser_missing_critical_field_returns_incomplete_without_fabrication():
    payload = json.loads(_response())
    payload["results"].pop("share_class_figi")
    snapshot = _snapshot(json.dumps(payload).encode("utf-8"))

    assert snapshot.snapshot_status == ident.IDENTITY_SNAPSHOT_INCOMPLETE
    assert snapshot.share_class_figi is None
    assert snapshot.fixed_findings == ("MISSING_CRITICAL_IDENTITY_FIELD",)


@pytest.mark.parametrize(
    "field_value",
    [
        {"primary_exchange": "XN"},
        {"composite_figi": "BAD"},
        {"ticker": "MSFT"},
        {"cik": "notdigits"},
        {"list_date": "1980/12/12"},
    ],
)
def test_parser_missing_critical_field_still_rejects_invalid_present_identity_values(field_value: dict[str, object]):
    payload = json.loads(_response(results=field_value))
    payload["results"].pop("share_class_figi")

    with pytest.raises(ident.InstrumentIdentityError):
        _snapshot(json.dumps(payload).encode("utf-8"))


@pytest.mark.parametrize(
    "field_value",
    [
        {"composite_figi": "BAD"},
        {"share_class_figi": "123456789012"},
        {"primary_exchange": "XN"},
        {"cik": "notdigits"},
        {"ticker": "MSFT"},
        {"market": "crypto"},
        {"locale": "global"},
        {"currency_name": "eur"},
        {"active": "true"},
        {"list_date": "1980/12/12"},
        {"delisted_utc": "not-a-date"},
        {"type": "common stock"},
    ],
)
def test_parser_rejects_invalid_identity_values_without_coercion(field_value: dict[str, object]):
    with pytest.raises(ident.InstrumentIdentityError):
        _snapshot(_response(results=field_value))


def test_projection_and_receipt_do_not_leak_private_provider_fields():
    snapshot = _snapshot()
    end = _snapshot(as_of_date=ident.END_SNAPSHOT_DATE)
    continuity = ident.compare_identity_snapshots(snapshot, end)
    receipt = ident.sanitized_receipt(run_id="ident-test", start_snapshot=snapshot, end_snapshot=end, continuity=continuity)
    rendered = json.dumps(receipt, sort_keys=True)
    projection = json.dumps(asdict(snapshot), sort_keys=True)

    for forbidden in (
        "rid-secret",
        "homepage",
        "phone",
        "description",
        "market_cap",
        "employees",
        "shares_outstanding",
        "branding",
        "address",
        "Authorization",
        "api_key",
    ):
        assert forbidden.lower() not in rendered.lower()
        assert forbidden.lower() not in projection.lower()


def test_identity_artifacts_commit_validate_no_overwrite_and_load_payload(tmp_path: Path):
    context = ident.create_identity_run(run_root=tmp_path, run_id="ident-run", created_at_utc="2026-01-01T00:00:00Z")
    snapshot = _snapshot()
    result = ident.commit_identity_artifact(
        payload=snapshot,
        artifact_type=ident.TICKER_OVERVIEW_SNAPSHOT,
        context=context,
        artifact_id="ident-art-start",
        as_of_date="2022-01-01",
    )

    manifest = result["manifest"]
    assert manifest["schema_version"] == ident.IDENTITY_ARTIFACT_MANIFEST_SCHEMA_VERSION
    assert manifest["artifact_type"] == ident.TICKER_OVERVIEW_SNAPSHOT
    assert manifest["payload_ref"] == "ident-run/snapshots/ident-art-start.json"
    assert manifest["payload_sha256"]
    assert manifest["semantic_payload_digest"] == snapshot.identity_projection_digest or manifest["semantic_payload_digest"]
    assert result["payload_path"].exists()
    assert result["manifest_path"].exists()
    loaded = ident.load_identity_payload(result["manifest_ref"], run_root=tmp_path)
    assert loaded["ticker"] == "AAPL"
    with pytest.raises(ident.InstrumentIdentityError):
        ident.commit_identity_artifact(
            payload=snapshot,
            artifact_type=ident.TICKER_OVERVIEW_SNAPSHOT,
            context=context,
            artifact_id="ident-art-start",
            as_of_date="2022-01-01",
        )


def test_raw_response_artifact_loads_as_validated_bytes_only(tmp_path: Path):
    context = ident.create_identity_run(run_root=tmp_path, run_id="ident-run", created_at_utc="2026-01-01T00:00:00Z")
    raw = ident.commit_identity_artifact(
        payload=_response(),
        artifact_type=ident.TICKER_OVERVIEW_RAW_RESPONSE,
        context=context,
        artifact_id="ident-art-raw",
        as_of_date="2022-01-01",
    )

    assert raw["manifest"]["artifact_type"] == ident.TICKER_OVERVIEW_RAW_RESPONSE
    assert raw["manifest"]["payload_ref"] == "ident-run/raw_response/ident-art-raw.bin"
    assert raw["manifest"]["payload_media_type"] == ident.PAYLOAD_MEDIA_TYPE_PROVIDER_RAW_BYTES
    assert raw["manifest"]["payload_sha256"] == raw["manifest"]["semantic_payload_digest"]
    assert ident.load_identity_raw_bytes(raw["manifest_ref"], run_root=tmp_path) == _response()
    with pytest.raises(ident.InstrumentIdentityError):
        ident.load_identity_payload(raw["manifest_ref"], run_root=tmp_path)


def test_artifact_rejects_unsafe_refs_and_symlink_payload(tmp_path: Path):
    context = ident.create_identity_run(run_root=tmp_path, run_id="ident-run", created_at_utc="2026-01-01T00:00:00Z")
    result = ident.commit_identity_artifact(
        payload=_snapshot(),
        artifact_type=ident.TICKER_OVERVIEW_SNAPSHOT,
        context=context,
        artifact_id="ident-art-start",
        as_of_date="2022-01-01",
    )
    with pytest.raises(ident.InstrumentIdentityError):
        ident.load_identity_manifest("../escape.manifest.json", run_root=tmp_path)
    outside = tmp_path / "outside.json"
    outside.write_bytes(result["payload_path"].read_bytes())
    result["payload_path"].unlink()
    try:
        result["payload_path"].symlink_to(outside)
    except OSError:
        pytest.skip("symlink creation is unavailable")
    with pytest.raises(ident.InstrumentIdentityError):
        ident.validate_identity_manifest(result["manifest"], run_root=tmp_path)


@pytest.mark.parametrize(
    "mutation",
    [
        {"payload_media_type": "application/json"},
        {"lineage_artifact_ids": ["../escape"]},
        {"lineage_artifact_ids": [1]},
        {"input_artifact_ids": ["bad/id"], "input_manifest_refs": ["ident-run/snapshots/ident-art-start.json.manifest.json"]},
    ],
)
def test_manifest_validation_rejects_tampered_media_type_and_lineage_shape(tmp_path: Path, mutation: dict[str, object]):
    context = ident.create_identity_run(run_root=tmp_path, run_id="ident-run", created_at_utc="2026-01-01T00:00:00Z")
    result = ident.commit_identity_artifact(
        payload=_snapshot(),
        artifact_type=ident.TICKER_OVERVIEW_SNAPSHOT,
        context=context,
        artifact_id="ident-art-start",
        as_of_date="2022-01-01",
    )
    tampered = dict(result["manifest"])
    tampered.update(mutation)

    with pytest.raises(ident.InstrumentIdentityError):
        ident.validate_identity_manifest_shape_without_payload(tampered)


def test_continuity_supported_for_matching_snapshots_and_events_pending():
    continuity = ident.compare_identity_snapshots(_snapshot(), _snapshot(as_of_date=ident.END_SNAPSHOT_DATE))

    assert continuity.continuity_status == ident.IDENTITY_CONTINUITY_SUPPORTED
    assert continuity.ticker_event_audit_status == ident.TICKER_EVENT_AUDIT_NOT_IMPLEMENTED
    assert continuity.canonical_eligibility is False
    assert continuity.registry_eligibility is False
    assert continuity.generation_freeze_eligibility is False
    assert continuity.strategy_enabled is False


@pytest.mark.parametrize(
    "field_value",
    [
        {"composite_figi": "BBG000B9XRZ5"},
        {"share_class_figi": "BBG001S5N8W9"},
        {"primary_exchange": "XNYS"},
        {"ticker": "MSFT"},
        {"currency_name": "cad"},
    ],
)
def test_continuity_requires_segment_review_for_critical_change(field_value: dict[str, object]):
    start = _snapshot()
    if set(field_value).issubset({"ticker", "currency_name"}):
        end = replace(start, as_of_date=ident.END_SNAPSHOT_DATE, **field_value)
    else:
        end = _snapshot(_response(results=field_value), as_of_date=ident.END_SNAPSHOT_DATE)

    assert ident.compare_identity_snapshots(start, end).continuity_status == ident.IDENTITY_CHANGE_REQUIRES_SEGMENT_REVIEW


def test_continuity_conflict_for_optional_cik_inactive_or_delisted_and_incomplete():
    start = _snapshot()
    cik_conflict = _snapshot(_response(results={"cik": "999999"}), as_of_date=ident.END_SNAPSHOT_DATE)
    inactive = _snapshot(_response(results={"active": False}), as_of_date=ident.END_SNAPSHOT_DATE)
    delisted = _snapshot(_response(results={"delisted_utc": "2024-01-01"}), as_of_date=ident.END_SNAPSHOT_DATE)

    assert ident.compare_identity_snapshots(start, cik_conflict).continuity_status == ident.IDENTITY_EVIDENCE_CONFLICT
    assert ident.compare_identity_snapshots(start, inactive).continuity_status == ident.IDENTITY_EVIDENCE_CONFLICT
    assert ident.compare_identity_snapshots(start, delisted).continuity_status == ident.IDENTITY_EVIDENCE_CONFLICT
    assert ident.compare_identity_snapshots(None, start).continuity_status == ident.IDENTITY_EVIDENCE_INCOMPLETE


def test_plan_cli_is_offline_sanitized_and_has_no_overrides():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.source_authority", "--instrument-identity-plan"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["ticker"] == "AAPL"
    assert receipt["start_snapshot_date"] == "2022-01-01"
    assert receipt["end_snapshot_date"] == "2025-12-31"
    assert receipt["provider_verified_identity"] is False
    assert receipt["ticker_event_audit_status"] == ident.TICKER_EVENT_AUDIT_NOT_IMPLEMENTED
    assert receipt["canonical_eligibility"] is False
    blocked = subprocess.run(
        [sys.executable, "-m", "marketflow.source_authority", "--instrument-identity-plan", "--ticker", "MSFT"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert blocked.returncode != 0


def test_self_check_cli_uses_mock_only_and_no_persistent_output():
    before = sorted((REPO_ROOT / ".marketflow" / "source_authority" / "identity" / "runs").glob("*")) if (REPO_ROOT / ".marketflow" / "source_authority" / "identity" / "runs").exists() else []
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.source_authority", "--instrument-identity-self-check"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    after = sorted((REPO_ROOT / ".marketflow" / "source_authority" / "identity" / "runs").glob("*")) if (REPO_ROOT / ".marketflow" / "source_authority" / "identity" / "runs").exists() else []
    receipt = json.loads(result.stdout)

    assert before == after
    assert receipt["self_check_status"] == "INSTRUMENT_IDENTITY_SELF_CHECK_COMPLETE"
    assert receipt["mock_transport_only"] is True
    assert receipt["persistent_artifacts_written"] is False
    assert receipt["observed_request_count"] == 2
    assert receipt["continuity_status"] == ident.IDENTITY_CONTINUITY_SUPPORTED
    assert receipt["changed_identity_status"] == ident.IDENTITY_CHANGE_REQUIRES_SEGMENT_REVIEW
    assert "fictional-self-check-key" not in result.stdout


def test_live_command_requires_tty_and_delays_getpass(monkeypatch):
    called = False

    def fake_getpass(prompt: str) -> str:
        nonlocal called
        called = True
        return "secret"

    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)

    assert ident.live_command(getpass_fn=fake_getpass) == 2
    assert called is False


def test_run_identity_evidence_private_mock_seam_makes_exactly_two_requests(tmp_path: Path):
    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(str(request.url))
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=_response())

    receipt = ident._run_instrument_identity_evidence(
        ident.diagnostic_confirmation_phrase(),
        api_key=ProviderApiKey("fictional-key"),
        http_transport=httpx.MockTransport(handler),
        run_root=tmp_path,
        run_id_factory=lambda: "ident-run",
    )

    assert receipt["provider_request_count"] == 2
    assert [url.rsplit("=", 1)[1] for url in seen] == ["2022-01-01", "2025-12-31"]
    assert receipt["continuity_status"] == ident.IDENTITY_CONTINUITY_SUPPORTED
    rendered = json.dumps(receipt, sort_keys=True)
    assert "fictional-key" not in rendered
    assert "rid-secret" not in rendered
    manifests = [json.loads(path.read_text(encoding="utf-8")) for path in tmp_path.rglob("*.manifest.json")]
    raw_manifests = [item for item in manifests if item["artifact_type"] == ident.TICKER_OVERVIEW_RAW_RESPONSE]
    snapshot_manifests = [item for item in manifests if item["artifact_type"] == ident.TICKER_OVERVIEW_SNAPSHOT]
    assert len(raw_manifests) == 2
    assert len(snapshot_manifests) == 2
    raw_ids = {item["artifact_id"] for item in raw_manifests}
    assert all(item["payload_media_type"] == ident.PAYLOAD_MEDIA_TYPE_PROVIDER_RAW_BYTES for item in raw_manifests)
    assert all(len(item["input_artifact_ids"]) == 1 for item in snapshot_manifests)
    assert all(set(item["input_artifact_ids"]).issubset(raw_ids) for item in snapshot_manifests)
    assert all(len(item["input_manifest_refs"]) == 1 for item in snapshot_manifests)


def test_contract_digests_and_prior_integrity_unchanged():
    assert acv1.contract_digest(acv1.load_contract_toml(REPO_ROOT / "config" / "fixed_date_acquisition_contract.example.toml")) == V1_DIGEST
    assert acv2.contract_digest(acv2.default_contract()) == V2_DIGEST
    assert acv21.contract_digest(acv21.default_contract()) == V21_DIGEST


def test_source_assurance_identity_package_boundaries():
    source_path = REPO_ROOT / "marketflow" / "source_authority" / "instrument_identity.py"
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    called_attrs = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
    exported = (REPO_ROOT / "marketflow" / "source_authority" / "__init__.py").read_text(encoding="utf-8")

    forbidden_modules = {
        "polygon",
        "requests",
        "socket",
        "streamlit",
        "openai",
        "marketflow.marketflow_strategy",
        "marketflow.services.monte_carlo_service",
        "marketflow.services.backtest_result_service",
        "marketflow.services.walk_forward_validation_service",
        "marketflow.historical_data.live_month_rth_diagnostic",
        "marketflow.historical_data.monthly_acquisition",
        "marketflow.historical_data.rth_bar_engine",
    }
    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert "getenv" not in called_attrs
    assert "environ" not in called_attrs
    assert "apiKey" not in source
    assert "Ticker Events" not in source
    assert "ticker_events" not in source.lower()
    assert "newest" not in source.lower()
    assert "automatic_stitch" not in source.lower()
    assert "_run_instrument_identity_evidence" in source
    assert "run_instrument_identity_evidence" not in exported
    assert "http_transport" not in exported
    assert "run_root" not in exported
    assert "run_id_factory" not in exported


def test_identity_documentation_records_offline_authority_and_credential_boundaries():
    docs = {
        "plan": REPO_ROOT / "docs" / "plans" / "MARKETFLOW_INSTRUMENT_IDENTITY_EVIDENCE_PLAN.md",
        "status": REPO_ROOT / "docs" / "status" / "MARKETFLOW_INSTRUMENT_IDENTITY_EVIDENCE_STATUS.md",
        "authority": REPO_ROOT / "docs" / "architecture" / "MARKETFLOW_INSTRUMENT_IDENTITY_AUTHORITY.md",
        "credential": REPO_ROOT / "docs" / "security" / "MARKETFLOW_IDENTITY_CREDENTIAL_BOUNDARY.md",
    }

    rendered = "\n".join(path.read_text(encoding="utf-8") for path in docs.values())

    for path in docs.values():
        assert path.is_file()
    assert "No live identity request occurred" in rendered
    assert "No actual Massive.com key was requested" in rendered
    assert "TICKER_EVENT_AUDIT_NOT_IMPLEMENTED" in rendered
    assert "PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL" in rendered
    assert "2022-01-01" in rendered
    assert "2025-12-31" in rendered
    assert "canonical registry authority" in rendered
    assert "getpass" in rendered
