from __future__ import annotations

import ast
import builtins
import json
import subprocess
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import httpx
import pytest

from marketflow.historical_data.massive_transport import ProviderApiKey
from marketflow.research import acquisition_contract_v2 as acv2
from marketflow.research import acquisition_contract_v2_1 as acv21
from marketflow.research import fixed_date_acquisition_contract as acv1
from marketflow.source_authority import instrument_identity as ident
from marketflow.source_authority import ticker_event_audit as tkev


REPO_ROOT = Path(__file__).resolve().parents[1]
V1_DIGEST = "29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e"
V2_DIGEST = "59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0"
V21_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"
TICKER_EVENT_SPEC_DIGEST = "352710cea4dc09d11023404c8438d62f5df4d303bbc48083a091f6799d680769"


def _event(date: str = "2023-06-01", ticker: str = "AAPL") -> dict[str, object]:
    return {"date": date, "type": tkev.EVENT_TYPE_TICKER_CHANGE, "ticker_change": {"ticker": ticker}}


def _response(events: list[dict[str, object]] | None = None, **overrides: object) -> bytes:
    payload: dict[str, object] = {"status": "OK", "request_id": "rid-secret", "results": {"events": events or [], "name": "not public"}}
    payload.update(overrides)
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _json_objects_from_output(output: str) -> list[dict[str, object]]:
    decoder = json.JSONDecoder()
    objects: list[dict[str, object]] = []
    index = 0
    while index < len(output):
        start = output.find("{", index)
        if start == -1:
            break
        value, offset = decoder.raw_decode(output[start:])
        if isinstance(value, dict):
            objects.append(value)
        index = start + offset
    return objects


def _snapshot_payload(as_of_date: str, artifact_id: str) -> tuple[dict[str, object], str]:
    digest = tkev.SOURCE_START_SNAPSHOT_DIGEST if as_of_date == tkev.START_DATE else tkev.SOURCE_END_SNAPSHOT_DIGEST
    return (
        {
            "schema_version": "marketflow.instrument_identity_snapshot.v1",
            "as_of_date": as_of_date,
            "ticker": tkev.TICKER_CONTEXT,
            "active": True,
            "market": "stocks",
            "locale": "us",
            "currency_name": "usd",
            "primary_exchange": tkev.PRIMARY_EXCHANGE_CONTEXT,
            "composite_figi": tkev.QUERY_IDENTIFIER,
            "share_class_figi": tkev.SHARE_CLASS_FIGI_CONTEXT,
            "type": tkev.SECURITY_TYPE_CONTEXT,
            "cik_status": ident.PRESENT,
            "cik": "320193",
            "list_date_status": ident.PRESENT,
            "list_date": "1980-12-12",
            "delisted_utc_status": ident.NOT_RETURNED,
            "delisted_utc": None,
            "provider_status": "OK",
            "snapshot_status": ident.IDENTITY_SNAPSHOT_COMPLETE,
            "fixed_findings": [],
            "identity_projection_digest": digest,
        },
        artifact_id,
    )


def _make_identity_chain(
    root: Path,
    *,
    run_id: str = tkev.SOURCE_IDENTITY_RUN_ID,
    continuity_artifact_id: str = tkev.SOURCE_CONTINUITY_ARTIFACT_ID,
    composite_figi: str = tkev.QUERY_IDENTIFIER,
    start_digest: str = tkev.SOURCE_START_SNAPSHOT_DIGEST,
    continuity_digest: str | None = None,
) -> Path:
    context = ident.create_identity_run(run_root=root, run_id=run_id, created_at_utc="2026-08-03T00:00:00Z")
    start_raw = ident.commit_identity_artifact(payload=b'{"status":"OK","results":{}}', artifact_type=ident.TICKER_OVERVIEW_RAW_RESPONSE, context=context, artifact_id="ident-art-start-raw", as_of_date=tkev.START_DATE)
    end_raw = ident.commit_identity_artifact(payload=b'{"status":"OK","results":{}}', artifact_type=ident.TICKER_OVERVIEW_RAW_RESPONSE, context=context, artifact_id="ident-art-end-raw", as_of_date=tkev.END_DATE)
    start_payload, start_id = _snapshot_payload(tkev.START_DATE, "ident-art-start-snapshot")
    end_payload, end_id = _snapshot_payload(tkev.END_DATE, "ident-art-end-snapshot")
    start_payload["composite_figi"] = composite_figi
    start_payload["identity_projection_digest"] = start_digest
    start_snapshot = ident.commit_identity_artifact(payload=start_payload, artifact_type=ident.TICKER_OVERVIEW_SNAPSHOT, context=context, artifact_id=start_id, as_of_date=tkev.START_DATE, input_manifests=(start_raw["manifest"],), input_manifest_refs=(start_raw["manifest_ref"],))
    end_snapshot = ident.commit_identity_artifact(payload=end_payload, artifact_type=ident.TICKER_OVERVIEW_SNAPSHOT, context=context, artifact_id=end_id, as_of_date=tkev.END_DATE, input_manifests=(end_raw["manifest"],), input_manifest_refs=(end_raw["manifest_ref"],))
    continuity_base = {
        "schema_version": "marketflow.instrument_identity_continuity_candidate.v1",
        "start_as_of_date": tkev.START_DATE,
        "end_as_of_date": tkev.END_DATE,
        "continuity_status": ident.IDENTITY_CONTINUITY_SUPPORTED,
        "ticker_event_audit_status": ident.TICKER_EVENT_AUDIT_NOT_IMPLEMENTED,
        "critical_field_status": "CRITICAL_FIELDS_MATCH",
        "supporting_field_status": "SUPPORTING_FIELDS_NONCONFLICTING",
        "fixed_findings": [],
        "start_identity_projection_digest": start_digest,
        "end_identity_projection_digest": tkev.SOURCE_END_SNAPSHOT_DIGEST,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "generation_freeze_eligibility": False,
        "strategy_enabled": False,
    }
    continuity = continuity_base | {"continuity_digest": continuity_digest or ident._digest(continuity_base)}
    continuity_artifact = ident.commit_identity_artifact(
        payload=continuity,
        artifact_type=ident.IDENTITY_CONTINUITY_CANDIDATE,
        context=context,
        artifact_id=continuity_artifact_id,
        input_manifests=(start_snapshot["manifest"], end_snapshot["manifest"]),
        input_manifest_refs=(start_snapshot["manifest_ref"], end_snapshot["manifest_ref"]),
    )
    receipt = {
        "status": "INSTRUMENT_IDENTITY_EVIDENCE_READY",
        "classification": ident.PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL,
        "run_id": run_id,
        "ticker": tkev.TICKER_CONTEXT,
        "start_snapshot_date": tkev.START_DATE,
        "end_snapshot_date": tkev.END_DATE,
        "start_snapshot_artifact_id": start_id,
        "end_snapshot_artifact_id": end_id,
        "continuity_status": ident.IDENTITY_CONTINUITY_SUPPORTED,
        "start_snapshot_semantic_digest": start_digest,
        "end_snapshot_semantic_digest": tkev.SOURCE_END_SNAPSHOT_DIGEST,
        "ticker_event_audit_status": ident.TICKER_EVENT_AUDIT_NOT_IMPLEMENTED,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "generation_freeze_eligibility": False,
        "strategy_enabled": False,
    }
    ident.commit_identity_artifact(
        payload=receipt,
        artifact_type=ident.INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT,
        context=context,
        artifact_id="ident-art-receipt",
        input_manifests=(continuity_artifact["manifest"],),
        input_manifest_refs=(continuity_artifact["manifest_ref"],),
    )
    return root


def test_specification_fixed_immutable_and_digest_deterministic():
    spec = tkev.default_ticker_event_audit_specification()

    assert spec.schema_version == "marketflow.ticker_event_audit_specification.v1"
    assert spec.classification == tkev.PROVIDER_TICKER_EVENT_AUDIT_CANDIDATE_NONCANONICAL
    assert spec.provider == "MASSIVE.COM"
    assert spec.endpoint_family == tkev.TICKER_EVENTS_EXPERIMENTAL_VX
    assert spec.endpoint_stability == tkev.ENDPOINT_STABILITY_EXPERIMENTAL
    assert spec.query_identifier_type == "COMPOSITE_FIGI"
    assert spec.query_identifier == "BBG000B9XRY4"
    assert spec.ticker_context == "AAPL"
    assert spec.start_date == "2022-01-01"
    assert spec.end_date == "2025-12-31"
    assert spec.event_types == ("ticker_change",)
    assert spec.canonical_eligibility is False
    assert spec.registry_eligibility is False
    assert spec.identity_freeze_eligibility is False
    assert spec.strategy_enabled is False
    assert tkev.ticker_event_audit_specification_digest() == TICKER_EVENT_SPEC_DIGEST
    assert tkev.ticker_event_audit_specification_digest() == tkev.ticker_event_audit_specification_digest()
    with pytest.raises(FrozenInstanceError):
        spec.query_identifier = "AAPL"  # type: ignore[misc]


def test_source_identity_binding_accepts_exact_six_manifest_chain(tmp_path: Path):
    root = _make_identity_chain(tmp_path)

    binding = tkev.validate_accepted_source_identity_evidence(identity_run_root=root)

    assert binding.source_identity_run_id == tkev.SOURCE_IDENTITY_RUN_ID
    assert binding.source_continuity_artifact_id == tkev.SOURCE_CONTINUITY_ARTIFACT_ID
    assert binding.source_continuity_status == ident.IDENTITY_CONTINUITY_SUPPORTED
    assert len(binding.source_continuity_semantic_digest) == 64
    assert binding.start_snapshot_semantic_digest == tkev.SOURCE_START_SNAPSHOT_DIGEST
    assert binding.end_snapshot_semantic_digest == tkev.SOURCE_END_SNAPSHOT_DIGEST
    assert binding.composite_figi == tkev.QUERY_IDENTIFIER


def test_source_identity_binding_rejects_wrong_run_continuity_figi_digest_and_incomplete(tmp_path: Path):
    with pytest.raises(tkev.TickerEventAuditError, match=tkev.TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID):
        tkev.validate_accepted_source_identity_evidence(identity_run_root=_make_identity_chain(tmp_path / "wrong-run", run_id="ident-wrong"))
    with pytest.raises(tkev.TickerEventAuditError, match=tkev.TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID):
        tkev.validate_accepted_source_identity_evidence(identity_run_root=_make_identity_chain(tmp_path / "wrong-cont", continuity_artifact_id="ident-art-wrong"))
    with pytest.raises(tkev.TickerEventAuditError, match=tkev.TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID):
        tkev.validate_accepted_source_identity_evidence(identity_run_root=_make_identity_chain(tmp_path / "wrong-figi", composite_figi="BBG000BADFIG"))
    with pytest.raises(tkev.TickerEventAuditError, match=tkev.TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID):
        tkev.validate_accepted_source_identity_evidence(identity_run_root=_make_identity_chain(tmp_path / "wrong-digest", start_digest="1" * 64))
    with pytest.raises(tkev.TickerEventAuditError, match=tkev.TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID):
        tkev.validate_accepted_source_identity_evidence(identity_run_root=_make_identity_chain(tmp_path / "wrong-continuity-digest", continuity_digest="0" * 64))
    incomplete = tmp_path / "incomplete"
    context = ident.create_identity_run(run_root=incomplete, run_id=tkev.SOURCE_IDENTITY_RUN_ID)
    ident.commit_identity_artifact(payload=b"{}", artifact_type=ident.TICKER_OVERVIEW_RAW_RESPONSE, context=context, artifact_id="only-raw", as_of_date=tkev.START_DATE)
    with pytest.raises(tkev.TickerEventAuditError, match=tkev.TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID):
        tkev.validate_accepted_source_identity_evidence(identity_run_root=incomplete)


def test_request_is_fixed_composite_figi_bearer_header_and_one_call():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=_response([]))

    transport = tkev.TickerEventsTransport(api_key=ProviderApiKey("fictional-key"), http_transport=httpx.MockTransport(handler))
    prepared = transport.prepare_request()
    body = transport.send()
    transport.close()

    assert body
    assert prepared.method == "GET"
    assert prepared.sanitized_path == "/vX/reference/tickers/BBG000B9XRY4/events"
    assert prepared.query == (("types", "ticker_change"),)
    assert prepared.headers["Authorization"] == "<redacted>"
    assert transport.call_count == 1
    assert len(seen) == 1
    assert seen[0].url.scheme == "https"
    assert seen[0].url.host == "api.massive.com"
    assert seen[0].url.path == "/vX/reference/tickers/BBG000B9XRY4/events"
    assert dict(seen[0].url.params) == {"types": "ticker_change"}
    assert seen[0].headers["Authorization"] == "Bearer fictional-key"
    assert "apikey" not in str(seen[0].url).lower()
    assert "api_key" not in str(seen[0].url).lower()
    assert "AAPL" not in seen[0].url.path


@pytest.mark.parametrize(
    "payload",
    [
        {"extra": True},
        {"results": {"events": [], "extra": True}},
        {"results": {"events": [{"date": "2023-01-01", "type": "ticker_change", "ticker_change": {"ticker": "AAPL"}, "extra": True}]}},
        {"results": {"events": [{"date": "2023-01-01", "type": "ticker_change", "ticker_change": {"ticker": "AAPL", "extra": True}}]}},
    ],
)
def test_parser_rejects_unknown_schema_fields(payload: dict[str, object]):
    base = {"status": "OK", "results": {"events": []}}
    base.update(payload)
    with pytest.raises(tkev.TickerEventAuditError):
        tkev.parse_ticker_events_response(json.dumps(base).encode("utf-8"), source_binding=tkev._synthetic_source_binding())


def test_parser_empty_events_valid_and_missing_events_incomplete():
    timeline = tkev.parse_ticker_events_response(_response([]), source_binding=tkev._synthetic_source_binding())

    assert timeline.event_count == 0
    assert timeline.empty_events_status == tkev.NO_TICKER_CHANGE_EVENTS_RETURNED
    assert timeline.in_range_event_count == 0
    with pytest.raises(tkev.TickerEventAuditError, match=tkev.TICKER_EVENT_EVIDENCE_INCOMPLETE):
        tkev.parse_ticker_events_response(_response([], results={}), source_binding=tkev._synthetic_source_binding())


def test_parser_canonicalizes_provider_order_and_classifies_ranges():
    timeline = tkev.parse_ticker_events_response(
        _response(
            [
                _event("2026-01-01", "POST"),
                _event("2023-06-01", "MID"),
                _event("2021-12-31", "PRE"),
            ]
        ),
        source_binding=tkev._synthetic_source_binding(),
    )

    assert [event.date for event in timeline.events] == ["2021-12-31", "2023-06-01", "2026-01-01"]
    assert [event.range_classification for event in timeline.events] == [
        tkev.BEFORE_CONTRACT_RANGE,
        tkev.WITHIN_CONTRACT_RANGE,
        tkev.AFTER_CONTRACT_RANGE,
    ]
    assert timeline.pre_range_event_count == 1
    assert timeline.in_range_event_count == 1
    assert timeline.post_range_event_count == 1


@pytest.mark.parametrize(
    "event",
    [
        {"date": "2023-01-01", "type": "other", "ticker_change": {"ticker": "AAPL"}},
        {"date": "2023-99-01", "type": "ticker_change", "ticker_change": {"ticker": "AAPL"}},
        {"type": "ticker_change", "ticker_change": {"ticker": "AAPL"}},
        {"date": "2023-01-01", "type": "ticker_change", "ticker_change": {}},
        {"date": "2023-01-01", "type": "ticker_change", "ticker_change": {"ticker": 1}},
    ],
)
def test_parser_rejects_malformed_events(event: dict[str, object]):
    with pytest.raises(tkev.TickerEventAuditError):
        tkev.parse_ticker_events_response(_response([event]), source_binding=tkev._synthetic_source_binding())


def test_parser_rejects_duplicate_and_conflicting_duplicate_events():
    with pytest.raises(tkev.TickerEventAuditError, match="duplicate identical"):
        tkev.parse_ticker_events_response(_response([_event("2023-01-01", "AAPL"), _event("2023-01-01", "AAPL")]), source_binding=tkev._synthetic_source_binding())
    with pytest.raises(tkev.TickerEventAuditError, match="conflicting duplicate"):
        tkev.parse_ticker_events_response(_response([_event("2023-01-01", "AAPL"), _event("2023-01-01", "AAPL2")]), source_binding=tkev._synthetic_source_binding())


def test_audit_statuses_for_no_events_pre_post_in_range_and_boundaries():
    binding = tkev._synthetic_source_binding()
    for events in ([], [_event("2021-12-31", "PRE")], [_event("2026-01-01", "POST")]):
        timeline = tkev.parse_ticker_events_response(_response(events), source_binding=binding)
        audit = tkev.build_supporting_audit(timeline, binding)
        assert audit.audit_status == tkev.TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE
        assert audit.combined_identity_candidate_status == tkev.IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE
    for events in ([_event("2022-01-01", "START")], [_event("2025-12-31", "END")], [_event("2023-06-01", "MID")]):
        timeline = tkev.parse_ticker_events_response(_response(events), source_binding=binding)
        audit = tkev.build_supporting_audit(timeline, binding)
        assert audit.audit_status == tkev.TICKER_EVENT_CHANGE_REQUIRES_SEGMENT_REVIEW
        assert audit.combined_identity_candidate_status == tkev.IDENTITY_CONTINUITY_REQUIRES_TICKER_EVENT_SEGMENT_REVIEW
        assert audit.canonical_eligibility is False
        assert audit.registry_eligibility is False
        assert audit.identity_freeze_eligibility is False
        assert audit.strategy_enabled is False


def test_run_writes_four_artifacts_lineage_and_sanitized_receipt(tmp_path: Path):
    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(str(request.url))
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=_response([_event("2021-12-31", "PRE")]))

    receipt = tkev._run_ticker_event_audit(
        tkev.ticker_event_audit_confirmation_phrase(),
        api_key=ProviderApiKey("fictional-key"),
        http_transport=httpx.MockTransport(handler),
        run_root=tmp_path,
        run_id_factory=lambda: "tkev-run",
        source_binding=tkev._synthetic_source_binding(),
    )

    assert receipt["provider_request_count"] == 1
    assert receipt["audit_status"] == tkev.TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE
    assert receipt["endpoint_stability"] == "EXPERIMENTAL"
    assert receipt["source_continuity_semantic_digest"] == "0" * 64
    rendered = json.dumps(receipt, sort_keys=True)
    for forbidden in ("fictional-key", "rid-secret", "Authorization", "https://", "raw response"):
        assert forbidden not in rendered
    manifests = [json.loads(path.read_text(encoding="utf-8")) for path in (tmp_path / "tkev-run").rglob("*.manifest.json")]
    assert len(manifests) == 4
    counts = {item["artifact_type"]: 0 for item in manifests}
    for item in manifests:
        counts[item["artifact_type"]] += 1
        tkev.validate_ticker_event_manifest(item, run_root=tmp_path)
    assert counts == {
        tkev.TICKER_EVENTS_RAW_RESPONSE: 1,
        tkev.TICKER_EVENT_TIMELINE: 1,
        tkev.TICKER_EVENT_AUDIT_CANDIDATE: 1,
        tkev.TICKER_EVENT_AUDIT_RECEIPT: 1,
    }
    raw = next(item for item in manifests if item["artifact_type"] == tkev.TICKER_EVENTS_RAW_RESPONSE)
    timeline = next(item for item in manifests if item["artifact_type"] == tkev.TICKER_EVENT_TIMELINE)
    audit = next(item for item in manifests if item["artifact_type"] == tkev.TICKER_EVENT_AUDIT_CANDIDATE)
    final_receipt = next(item for item in manifests if item["artifact_type"] == tkev.TICKER_EVENT_AUDIT_RECEIPT)
    timeline_payload = tkev.load_ticker_event_payload(timeline["payload_ref"] + ".manifest.json", run_root=tmp_path)
    assert timeline["input_artifact_ids"] == [raw["artifact_id"]]
    assert timeline["source_continuity_semantic_digest"] == "0" * 64
    assert timeline_payload["endpoint_stability"] == tkev.ENDPOINT_STABILITY_EXPERIMENTAL
    assert audit["input_artifact_ids"] == [raw["artifact_id"], timeline["artifact_id"]]
    assert final_receipt["input_artifact_ids"] == [audit["artifact_id"]]
    assert all(tkev.SOURCE_CONTINUITY_ARTIFACT_ID in item["external_source_artifact_ids"] for item in manifests)

    corrupt_timeline = dict(timeline)
    corrupt_timeline["input_artifact_ids"] = ["tkev-art-wrong"]
    with pytest.raises(tkev.TickerEventAuditError, match="input reference mismatch"):
        tkev.validate_ticker_event_manifest(corrupt_timeline, run_root=tmp_path)

    corrupt_audit = dict(audit)
    corrupt_audit["lineage_artifact_ids"] = [timeline["artifact_id"]]
    with pytest.raises(tkev.TickerEventAuditError, match="lineage mismatch"):
        tkev.validate_ticker_event_manifest(corrupt_audit, run_root=tmp_path)

    corrupt_digest = dict(raw)
    corrupt_digest["source_continuity_semantic_digest"] = "not-a-digest"
    with pytest.raises(tkev.TickerEventAuditError, match="source continuity semantic digest"):
        tkev.validate_ticker_event_manifest_shape_without_payload(corrupt_digest)

    corrupt_raw = dict(raw)
    corrupt_raw["external_source_artifact_ids"] = [tkev.SOURCE_CONTINUITY_ARTIFACT_ID, tkev.SOURCE_CONTINUITY_ARTIFACT_ID]
    with pytest.raises(tkev.TickerEventAuditError, match="unique"):
        tkev.validate_ticker_event_manifest_shape_without_payload(corrupt_raw)


def test_artifacts_reject_overwrite_and_unsafe_refs(tmp_path: Path):
    binding = tkev._synthetic_source_binding()
    context = tkev.create_ticker_event_run(run_root=tmp_path, run_id="tkev-run")
    tkev.commit_ticker_event_artifact(payload=b"{}", artifact_type=tkev.TICKER_EVENTS_RAW_RESPONSE, context=context, source_binding=binding, artifact_id="raw")

    with pytest.raises(tkev.TickerEventAuditError, match="already exists|artifact output"):
        tkev.commit_ticker_event_artifact(payload=b"{}", artifact_type=tkev.TICKER_EVENTS_RAW_RESPONSE, context=context, source_binding=binding, artifact_id="raw")
    manifest = json.loads(next(tmp_path.rglob("*.manifest.json")).read_text(encoding="utf-8"))
    manifest["payload_ref"] = "../escape.bin"
    with pytest.raises(tkev.TickerEventAuditError):
        tkev.validate_ticker_event_manifest_shape_without_payload(manifest)


def test_artifacts_reject_symlink_payload(tmp_path: Path):
    binding = tkev._synthetic_source_binding()
    context = tkev.create_ticker_event_run(run_root=tmp_path, run_id="tkev-run")
    result = tkev.commit_ticker_event_artifact(payload=b"{}", artifact_type=tkev.TICKER_EVENTS_RAW_RESPONSE, context=context, source_binding=binding, artifact_id="raw")
    payload = tmp_path / result["manifest"]["payload_ref"]
    outside = tmp_path / "outside.bin"
    outside.write_bytes(b"{}")
    payload.unlink()
    try:
        payload.symlink_to(outside)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")

    with pytest.raises(tkev.TickerEventAuditError):
        tkev.load_ticker_event_manifest(result["manifest_ref"], run_root=tmp_path)


def test_plan_and_self_check_are_offline_sanitized_and_cli_accessible():
    plan = tkev.ticker_event_audit_plan()
    self_check = tkev.ticker_event_audit_self_check()

    assert plan["credential_required"] is False
    assert plan["writes_artifacts"] is False
    assert plan["live_audit_occurred"] is False
    assert plan["endpoint_stability"] == "EXPERIMENTAL"
    assert self_check["self_check_status"] == "TICKER_EVENT_AUDIT_SELF_CHECK_COMPLETE"
    assert self_check["mock_transport_only"] is True
    assert self_check["persistent_artifacts_written"] is False
    assert self_check["incomplete_response_status"] == tkev.TICKER_EVENT_EVIDENCE_INCOMPLETE

    result = subprocess.run(
        [sys.executable, "-m", "marketflow.source_authority", "--ticker-event-audit-plan"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert json.loads(result.stdout)["status"] == "TICKER_EVENT_AUDIT_PLAN_READY"
    assert "fictional" not in result.stdout


def test_live_command_boundaries_confirmation_preflight_before_getpass(monkeypatch, tmp_path: Path, capsys):
    events: list[str] = []
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)

    def confirm(prompt: str) -> str:
        events.append("confirmation")
        return tkev.ticker_event_audit_confirmation_phrase()

    def preflight() -> dict[str, object]:
        events.append("preflight")
        raise tkev.TickerEventAuditError(tkev.TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)

    def fail_getpass(prompt: str) -> str:
        events.append("getpass")
        raise AssertionError("getpass must not run")

    monkeypatch.setattr(builtins, "input", confirm)

    assert tkev.live_command(getpass_fn=fail_getpass, _preflight=preflight) == 2
    output = capsys.readouterr().out
    receipt = _json_objects_from_output(output)[-1]

    assert events == ["confirmation", "preflight"]
    assert receipt["status"] == tkev.TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_FAILED
    assert receipt["credential_prompted"] is False
    assert "Traceback" not in output
    assert str(tmp_path) not in output


def test_live_command_success_uses_one_mock_request_after_getpass(monkeypatch, tmp_path: Path, capsys):
    events: list[str] = []
    seen: list[str] = []
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(builtins, "input", lambda prompt: events.append("confirmation") or tkev.ticker_event_audit_confirmation_phrase())
    monkeypatch.setattr(tkev, "_ticker_event_runtime_root", lambda *, repository_root=None: tmp_path)

    def key_prompt(prompt: str) -> str:
        events.append("getpass")
        return "fictional-key"

    def key_factory(secret: str) -> ProviderApiKey:
        events.append("key")
        return ProviderApiKey(secret)

    def preflight() -> dict[str, object]:
        events.append("preflight")
        return {"status": tkev.TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_READY}

    def handler(request: httpx.Request) -> httpx.Response:
        events.append("request")
        seen.append(str(request.url))
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=_response([]))

    assert (
        tkev.live_command(
            getpass_fn=key_prompt,
            _provider_key_factory=key_factory,
            _http_transport=httpx.MockTransport(handler),
            _run_id_factory=lambda: "tkev-live-mock",
            _preflight=preflight,
        )
        == 0
    )
    output = capsys.readouterr().out
    receipt = _json_objects_from_output(output)[-1]

    assert events[:4] == ["confirmation", "preflight", "getpass", "key"]
    assert events.count("request") == 1
    assert receipt["provider_request_count"] == 1
    assert seen[0].endswith("/vX/reference/tickers/BBG000B9XRY4/events?types=ticker_change")
    assert "fictional-key" not in output
    assert "rid-secret" not in output


def test_live_command_parse_failure_reports_request_and_raw_artifact(monkeypatch, tmp_path: Path, capsys):
    events: list[str] = []
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(builtins, "input", lambda prompt: events.append("confirmation") or tkev.ticker_event_audit_confirmation_phrase())
    monkeypatch.setattr(tkev, "_ticker_event_runtime_root", lambda *, repository_root=None: tmp_path)

    def handler(request: httpx.Request) -> httpx.Response:
        events.append("request")
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=b'{"status":"OK","results":{}}')

    assert (
        tkev.live_command(
            getpass_fn=lambda prompt: "fictional-key",
            _http_transport=httpx.MockTransport(handler),
            _run_id_factory=lambda: "tkev-live-bad-json",
            _preflight=lambda: {"status": tkev.TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_READY},
        )
        == 2
    )
    output = capsys.readouterr().out
    receipt = _json_objects_from_output(output)[-1]

    assert events == ["confirmation", "request"]
    assert receipt["provider_request_count"] == 1
    assert receipt["runtime_artifact_written"] is True
    assert receipt["failure_category"] == tkev.TICKER_EVENT_EVIDENCE_INCOMPLETE
    assert len(list((tmp_path / "tkev-live-bad-json").rglob("*.manifest.json"))) == 1
    assert "fictional-key" not in output
    assert "Authorization" not in output
    assert "https://" not in output


def test_live_command_endpoint_failure_reports_request_without_artifact(monkeypatch, tmp_path: Path, capsys):
    events: list[str] = []
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(builtins, "input", lambda prompt: events.append("confirmation") or tkev.ticker_event_audit_confirmation_phrase())
    monkeypatch.setattr(tkev, "_ticker_event_runtime_root", lambda *, repository_root=None: tmp_path)

    def handler(request: httpx.Request) -> httpx.Response:
        events.append("request")
        return httpx.Response(503, headers={"Content-Type": "application/json"}, content=b'{"status":"ERROR"}')

    assert (
        tkev.live_command(
            getpass_fn=lambda prompt: "fictional-key",
            _http_transport=httpx.MockTransport(handler),
            _run_id_factory=lambda: "tkev-live-503",
            _preflight=lambda: {"status": tkev.TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_READY},
        )
        == 2
    )
    output = capsys.readouterr().out
    receipt = _json_objects_from_output(output)[-1]

    assert events == ["confirmation", "request"]
    assert receipt["status"] == tkev.TICKER_EVENT_AUDIT_TRANSPORT_FAILED
    assert receipt["failure_category"] == tkev.TICKER_EVENT_ENDPOINT_UNAVAILABLE
    assert receipt["provider_request_count"] == 1
    assert receipt["runtime_artifact_written"] is False
    assert list((tmp_path / "tkev-live-503").rglob("*.manifest.json")) == []
    assert "fictional-key" not in output
    assert "https://" not in output


def test_live_command_sanitizes_getpass_and_key_construction_failures(monkeypatch, tmp_path: Path, capsys):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(builtins, "input", lambda prompt: tkev.ticker_event_audit_confirmation_phrase())
    monkeypatch.setattr(tkev, "_ticker_event_runtime_root", lambda *, repository_root=None: tmp_path)

    assert (
        tkev.live_command(
            getpass_fn=lambda prompt: (_ for _ in ()).throw(RuntimeError(f"path {tmp_path}")),
            _preflight=lambda: {"status": tkev.TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_READY},
        )
        == 2
    )
    prompt_output = capsys.readouterr().out
    prompt_receipt = _json_objects_from_output(prompt_output)[-1]
    assert prompt_receipt["status"] == tkev.TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED
    assert prompt_receipt["failure_category"] == tkev.TICKER_EVENT_AUDIT_UNEXPECTED_FAILURE
    assert prompt_receipt["credential_prompted"] is True
    assert prompt_receipt["provider_request_count"] == 0
    assert prompt_receipt["runtime_artifact_written"] is False
    assert "Traceback" not in prompt_output
    assert str(tmp_path) not in prompt_output

    assert (
        tkev.live_command(
            getpass_fn=lambda prompt: " bad-key",
            _preflight=lambda: {"status": tkev.TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_READY},
        )
        == 2
    )
    key_output = capsys.readouterr().out
    key_receipt = _json_objects_from_output(key_output)[-1]
    assert key_receipt["status"] == tkev.TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED
    assert key_receipt["failure_category"] == tkev.TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED
    assert key_receipt["provider_request_count"] == 0
    assert key_receipt["runtime_artifact_written"] is False
    assert " bad-key" not in key_output


def test_live_command_requires_tty_and_wrong_confirmation_stops_early(monkeypatch, capsys):
    called = False

    def fake_getpass(prompt: str) -> str:
        nonlocal called
        called = True
        return "secret"

    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    assert tkev.live_command(getpass_fn=fake_getpass) == 2
    assert called is False

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(builtins, "input", lambda prompt: "WRONG")
    assert tkev.live_command(getpass_fn=fake_getpass, _preflight=lambda: (_ for _ in ()).throw(AssertionError("no preflight"))) == 2
    assert called is False
    assert "TICKER_EVENT_AUDIT_CONFIRMATION_REJECTED" in capsys.readouterr().out


def test_public_api_and_source_assurance_boundaries():
    source = (REPO_ROOT / "marketflow" / "source_authority" / "ticker_event_audit.py").read_text(encoding="utf-8")
    main_source = (REPO_ROOT / "marketflow" / "source_authority" / "__main__.py").read_text(encoding="utf-8")
    exported = (REPO_ROOT / "marketflow" / "source_authority" / "__init__.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    called_attrs = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
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
    assert "Path.cwd" not in source
    assert "MASSIVE_CUSTOM_BARS_PATH_TEMPLATE" not in source
    assert "splits" not in source.lower()
    assert "dividends" not in source.lower()
    assert "pagination" not in source.lower()
    assert "retry" not in source.lower()
    assert '"/vX/reference/tickers/{QUERY_IDENTIFIER}/events"' in source
    assert "(\"types\", EVENT_TYPE_TICKER_CHANGE)" in source
    assert "TICKER_EVENTS_EXPERIMENTAL_VX" in source
    assert "validate_accepted_source_identity_evidence()" in source
    assert "secret = getpass_fn" in source
    assert source.find("validate_accepted_source_identity_evidence()") < source.find("secret = getpass_fn")
    for name in ("_run_ticker_event_audit", "http_transport", "run_root", "run_id_factory", "source_binding"):
        assert name not in exported
    for forbidden in ("--repository-root", "--run-root", "--output-root", "--identifier", "--composite-figi", "--date", "--api-key"):
        assert forbidden not in main_source


def test_contract_identity_and_prior_integrity_remain_unchanged():
    assert acv1.contract_digest(acv1.load_contract_toml(REPO_ROOT / "config" / "fixed_date_acquisition_contract.example.toml")) == V1_DIGEST
    assert acv2.contract_digest(acv2.default_contract()) == V2_DIGEST
    assert acv21.contract_digest(acv21.default_contract()) == V21_DIGEST
    assert ident.instrument_identity_specification_digest() == "a728408f59948cd3cd244816fe99a1d85e8d381b53f8e03d61e2d751c22ff3ba"


def test_documentation_records_ticker_event_audit_boundaries():
    docs = [
        REPO_ROOT / "docs" / "plans" / "MARKETFLOW_TICKER_EVENT_AUDIT_PLAN.md",
        REPO_ROOT / "docs" / "status" / "MARKETFLOW_TICKER_EVENT_AUDIT_STATUS.md",
        REPO_ROOT / "docs" / "status" / "MARKETFLOW_TICKER_EVENT_AUDIT_ACCEPTANCE.md",
        REPO_ROOT / "docs" / "architecture" / "MARKETFLOW_TICKER_EVENT_SUPPORTING_AUTHORITY.md",
        REPO_ROOT / "docs" / "security" / "MARKETFLOW_TICKER_EVENT_CREDENTIAL_BOUNDARY.md",
    ]
    rendered = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())

    for path in docs:
        assert path.is_file()
    assert "MarketFlow Ticker Events Supporting Audit v1" in rendered
    assert "EXPERIMENTAL" in rendered
    assert "No live Ticker Events request occurred" in rendered
    assert "No actual Massive.com key was requested" in rendered
    assert "Status: PASS" in rendered
    assert "supporting evidence" in rendered
    assert "no automatic stitching" in rendered
    assert "identity freeze remains pending" in rendered
    assert "calendar, splits, dividends, registry, and Strategy remain pending" in rendered
