from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from marketflow.services import identity_segment_freeze_service as freeze


REPO_ROOT = Path(__file__).resolve().parents[1]


def _candidate() -> dict:
    return freeze.build_identity_segment_candidate_v1()


def _validated(candidate: dict) -> dict:
    return freeze.validate_identity_segment_candidate_v1(candidate)


def test_candidate_builds_offline_with_no_provider_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(freeze.ident, "TickerOverviewTransport", fail_provider_call)
    monkeypatch.setattr(freeze.tkev, "TickerEventsTransport", fail_provider_call)
    monkeypatch.setattr(freeze.tkev, "validate_accepted_source_identity_evidence", fail_provider_call)

    candidate = _candidate()
    receipt = _validated(candidate)

    assert calls == []
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert receipt["provider_requests_made"] is False


def test_candidate_kind_status_and_no_freeze_authority():
    candidate = _candidate()

    assert candidate["artifact_kind"] == "IDENTITY_SEGMENT_CANDIDATE"
    assert candidate["schema_version"] == "identity_segment_evidence_freeze_v1"
    assert candidate["candidate_status"] == "IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW"
    assert candidate["operator_freeze_required"] is True
    assert candidate["identity_segment_frozen"] is False
    assert candidate["automatic_stitching"] is False

    boundary = candidate["authority_boundary"]
    assert boundary["identity_segment_frozen"] is False
    assert boundary["canonical_eligibility"] is False
    assert boundary["registry_eligibility"] is False
    assert boundary["acquisition_generation_freeze"] is False
    assert boundary["calendar_operator_frozen"] is False
    assert boundary["strategy_runtime_migration"] is False
    assert "operator_approval" not in json.dumps(candidate)
    assert "freeze_timestamp" not in json.dumps(candidate)
    assert "freeze_operator_identity" not in json.dumps(candidate)


def test_segment_and_contract_fields_match_fixed_evidence():
    segment = _candidate()["segment"]

    assert segment["ticker"] == "AAPL"
    assert segment["composite_figi"] == "BBG000B9XRY4"
    assert segment["share_class_figi"] == "BBG001S5N8V8"
    assert segment["primary_mic"] == "XNAS"
    assert segment["security_type"] == "CS"
    assert segment["segment_start"] == "2022-01-01"
    assert segment["segment_end"] == "2025-12-31"
    assert segment["acquisition_contract_digest"] == "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"
    assert segment["fixed_acquisition_range"] == {"start": "2022-01-01", "end": "2025-12-31"}


def test_identity_evidence_bindings_match_accepted_six_manifest_chain():
    binding = _candidate()["identity_evidence_binding"]

    assert binding["identity_run_id"] == "ident-509de6e2eb5e4a1db785e034bcfaf045"
    assert binding["continuity_artifact_id"] == "ident-art-8607986a2341423182614a41c6236ed9"
    assert binding["start_snapshot_semantic_digest"] == "75a3fb5cccda09c05001129ec7161ad479457a714a5903828c67c5cfeb965928"
    assert binding["end_snapshot_semantic_digest"] == "5e80a556b6172d8ca8985177f8c17e05183322fb5981ba92def57d4698aa4f50"
    assert binding["continuity_status"] == "IDENTITY_CONTINUITY_SUPPORTED"
    assert binding["artifact_inventory"] == {
        "TICKER_OVERVIEW_RAW_RESPONSE": 2,
        "TICKER_OVERVIEW_SNAPSHOT": 2,
        "IDENTITY_CONTINUITY_CANDIDATE": 1,
        "INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT": 1,
    }
    assert binding["total_manifests"] == 6
    assert binding["active_at_both_boundaries"] is True


def test_ticker_events_bindings_and_pre_range_event_do_not_trigger_stitching():
    candidate = _candidate()
    binding = candidate["ticker_events_evidence_binding"]

    assert binding["ticker_events_audit_run_id"] == "tkev-959a591271874fe49bc8cb34bb29be36"
    assert binding["raw_response_artifact_id"] == "tkev-art-5d8ed7c1aa0e451ab1c7b297230dca33"
    assert binding["raw_response_semantic_payload_digest"] == "07082085e9e41c467e020774954c045e83613d9581976ca26e87b74e3bbf15dc"
    assert binding["timeline_artifact_id"] == "tkev-art-54a14c247fb2459a9c588dd4695b4358"
    assert binding["timeline_semantic_digest"] == "36ccff35908df36a7fadb124d6cb846e4ac0cace578830e7591f7edf92bde820"
    assert binding["audit_artifact_id"] == "tkev-art-df20d0c474464b74a28a6f4ed451fef6"
    assert binding["receipt_artifact_id"] == "tkev-art-2168e3f7caec46d59436ab0e4280d49d"
    assert binding["returned_event_count"] == 1
    assert binding["pre_range_events"] == 1
    assert binding["in_range_events"] == 0
    assert binding["post_range_events"] == 0
    assert binding["ticker_events_audit_status"] == "TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE"
    assert binding["combined_identity_candidate_status"] == "IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE"
    assert binding["endpoint_stability"] == "EXPERIMENTAL"
    assert binding["provider_composite_figi_status"] == "PRESENT_MATCHED"
    assert binding["provider_cik_status"] == "PRESENT_MATCHED"
    assert binding["events"] == [
        {
            "event_date": "2003-09-10",
            "event_type": "ticker_change",
            "reported_ticker": "AAPL",
            "range_classification": "BEFORE_CONTRACT_RANGE",
        }
    ]
    assert candidate["automatic_stitching"] is False
    assert candidate["authority_boundary"]["automatic_stitching"] is False


def test_monthly_source_evidence_matches_accepted_january_2025_counts():
    source = _candidate()["monthly_source_evidence"]

    assert source["ticker"] == "AAPL"
    assert source["month"] == "2025-01"
    assert source["normalized_source_rows"] == 1277
    assert source["extended_hours_rows"] == 757
    assert source["expected_rth_rows"] == 520
    assert source["validated_rth_rows"] == 520
    assert source["rth_reconciliation"] == "RTH_SOURCE_ROWS_RECONCILED"
    assert source["full_ordinary_sessions"] == 20
    assert source["incomplete_ordinary_sessions"] == 0
    assert source["swing_rth_half_session_195m_bars"] == 40
    assert source["position_swing_rth_full_session_1d_bars"] == 20
    assert source["requested_calendar"] == "XNAS"
    assert source["resolved_calendar"] == "XNYS"
    assert source["calendar_alias"] == "XNAS_USES_XNYS_SCHEDULE"
    assert source["calendar_authority"] == "NOT_OPERATOR_FROZEN"


def test_candidate_semantic_digest_is_deterministic_across_repeated_builds():
    first = _candidate()
    second = _candidate()

    assert first == second
    assert len(first["candidate_semantic_digest"]) == 64
    assert first["candidate_semantic_digest"] == freeze.candidate_semantic_digest(first)
    assert first["candidate_semantic_digest"] == second["candidate_semantic_digest"]


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("segment", "composite_figi"), "BBG000B9XRZ5"),
        (("segment", "share_class_figi"), "BBG001S5N8W9"),
        (("segment", "segment_start"), "2022-01-02"),
        (("segment", "segment_end"), "2025-12-30"),
        (("segment", "acquisition_contract_digest"), "0" * 64),
        (("identity_evidence_binding", "identity_run_id"), "ident-wrong"),
        (("identity_evidence_binding", "continuity_artifact_id"), "ident-art-wrong"),
        (("identity_evidence_binding", "start_snapshot_semantic_digest"), "1" * 64),
        (("identity_evidence_binding", "end_snapshot_semantic_digest"), "2" * 64),
        (("ticker_events_evidence_binding", "ticker_events_audit_run_id"), "tkev-wrong"),
        (("ticker_events_evidence_binding", "raw_response_artifact_id"), "tkev-art-wrong"),
        (("ticker_events_evidence_binding", "raw_response_semantic_payload_digest"), "3" * 64),
        (("ticker_events_evidence_binding", "timeline_artifact_id"), "tkev-art-wrong"),
        (("ticker_events_evidence_binding", "timeline_semantic_digest"), "4" * 64),
        (("ticker_events_evidence_binding", "audit_artifact_id"), "tkev-art-wrong"),
        (("ticker_events_evidence_binding", "receipt_artifact_id"), "tkev-art-wrong"),
        (("ticker_events_evidence_binding", "in_range_events"), 1),
        (("ticker_events_evidence_binding", "ticker_events_audit_status"), "TICKER_EVENT_CHANGE_REQUIRES_SEGMENT_REVIEW"),
    ],
)
def test_validator_rejects_modified_bound_evidence(path: tuple[str, str], value: object):
    candidate = _candidate()
    candidate[path[0]][path[1]] = value
    candidate["candidate_semantic_digest"] = freeze.candidate_semantic_digest(candidate)

    with pytest.raises(freeze.IdentitySegmentFreezeError):
        _validated(candidate)


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("artifact_kind",), "IDENTITY_SEGMENT_FROZEN"),
        (("candidate_status",), "IDENTITY_SEGMENT_FROZEN"),
        (("identity_segment_frozen",), True),
        (("authority_boundary", "identity_segment_frozen"), True),
        (("authority_boundary", "canonical_eligibility"), True),
        (("authority_boundary", "registry_eligibility"), True),
        (("authority_boundary", "acquisition_generation_freeze"), True),
        (("authority_boundary", "calendar_operator_frozen"), True),
        (("authority_boundary", "strategy_runtime_migration"), True),
        (("lineage_guardrails", "raw_source_evidence_copied"), True),
        (("lineage_guardrails", "raw_source_evidence_rewritten"), True),
        (("lineage_guardrails", "provider_requests_made"), True),
    ],
)
def test_validator_rejects_freeze_authority_and_reference_only_violations(path: tuple[str, ...], value: object):
    candidate = _candidate()
    target = candidate
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    candidate["candidate_semantic_digest"] = freeze.candidate_semantic_digest(candidate)

    with pytest.raises(freeze.IdentitySegmentFreezeError):
        _validated(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "operator_approval",
        "operator_approved_by",
        "operator_approval_timestamp",
        "freeze_timestamp",
        "freeze_operator_identity",
    ],
)
def test_validator_rejects_operator_approval_and_freeze_fields(field: str):
    candidate = _candidate()
    candidate[field] = "not allowed"
    candidate["candidate_semantic_digest"] = freeze.candidate_semantic_digest(candidate)

    with pytest.raises(freeze.IdentitySegmentFreezeError):
        _validated(candidate)


def test_validator_rejects_stale_candidate_digest():
    candidate = _candidate()
    candidate["segment"]["composite_figi"] = "BBG000B9XRZ5"

    with pytest.raises(freeze.IdentitySegmentFreezeError, match="segment mismatch"):
        _validated(candidate)


def test_write_candidate_artifact_is_offline_json_and_no_overwrite(tmp_path: Path):
    result = freeze.write_identity_segment_candidate_v1(tmp_path)
    path = Path(result["path"])

    assert result["artifact_kind"] == "IDENTITY_SEGMENT_CANDIDATE"
    assert result["candidate_status"] == "IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW"
    assert result["identity_segment_frozen"] is False
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["candidate_semantic_digest"] == result["candidate_semantic_digest"]
    assert payload["artifact_kind"] == "IDENTITY_SEGMENT_CANDIDATE"
    assert result["candidate_payload_digest"] == freeze.sha256_bytes(path.read_bytes())
    with pytest.raises(freeze.IdentitySegmentFreezeError, match="already exists"):
        freeze.write_identity_segment_candidate_v1(tmp_path)


def test_source_assurance_service_has_no_provider_strategy_or_runtime_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "identity_segment_freeze_service.py"
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
    assert "IDENTITY_SEGMENT_CANDIDATE" in source
    assert "IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW" in source
    assert "IDENTITY_SEGMENT_FROZEN" in source
    assert "next_allowed_operator_ceremony" in source
    assert "canonical_eligibility" in source
    assert "registry_eligibility" in source
