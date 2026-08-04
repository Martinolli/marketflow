from __future__ import annotations

import ast
import json
from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import identity_segment_freeze_service as freeze
from marketflow.services import identity_segment_operator_freeze_service as ceremony
from marketflow.services import identity_segment_operator_review_service as review


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANDIDATE_DIGEST = "263902ddc149728d095a4f8bc941c92a82c2d4360e0a038d231e0eac6c70dc57"
EXPECTED_REVIEW_DIGEST = "c39ad88e25554de67a52a3383c53a1df2bcac257b89b3d087be68b22bbcc17bd"
TEST_TIMESTAMP = "2026-08-04T00:00:00Z"


def _attestation(**overrides: object) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": TEST_TIMESTAMP,
        "operator_attestation_phrase": ceremony.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_review_package_digest": EXPECTED_REVIEW_DIGEST,
        "operator_confirms_no_provider_requests": True,
        "operator_confirms_no_calendar_freeze": True,
        "operator_confirms_no_canonical_approval": True,
        "operator_confirms_no_registry_approval": True,
        "operator_confirms_no_acquisition_generation_freeze": True,
    }
    values.update(overrides)
    return ceremony.build_identity_segment_operator_attestation_v1(**values)


def _frozen(**overrides: object) -> dict:
    values = {"operator_attestation": _attestation()}
    values.update(overrides)
    return ceremony.build_identity_segment_frozen_v1(**values)


def _recompute_digest(frozen: dict) -> None:
    frozen["identity_segment_frozen_semantic_digest"] = ceremony.identity_segment_frozen_semantic_digest(frozen)


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == "APPROVE_IDENTITY_SEGMENT_FREEZE"
    assert attestation["operator_attestation_phrase"] == ceremony.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    assert attestation["operator_attestation_timestamp_utc"] == TEST_TIMESTAMP
    assert attestation["operator_attestation_version"] == "identity_segment_operator_attestation_v1"
    assert attestation["operator_confirms_candidate_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert attestation["operator_confirms_review_package_digest"] == EXPECTED_REVIEW_DIGEST
    for field in ceremony.OPERATOR_BOUNDARY_CONFIRMATION_FIELDS:
        assert attestation[field] is True


def test_frozen_artifact_builds_offline_without_provider_calls(monkeypatch):
    calls: list[str] = []

    def fail_provider_call(*args, **kwargs):
        calls.append("provider")
        raise AssertionError("provider access must not be used")

    monkeypatch.setattr(freeze.ident, "TickerOverviewTransport", fail_provider_call)
    monkeypatch.setattr(freeze.tkev, "TickerEventsTransport", fail_provider_call)
    monkeypatch.setattr(freeze.tkev, "validate_accepted_source_identity_evidence", fail_provider_call)

    frozen = _frozen()
    receipt = ceremony.validate_identity_segment_frozen_v1(frozen)

    assert calls == []
    assert frozen["created_offline"] is True
    assert frozen["provider_requests_made"] is False
    assert receipt["provider_requests_made"] is False


def test_artifact_kind_status_and_identity_segment_freeze_state():
    frozen = _frozen()

    assert frozen["artifact_kind"] == "IDENTITY_SEGMENT_FROZEN"
    assert frozen["schema_version"] == "identity_segment_operator_freeze_v1"
    assert frozen["freeze_status"] == "IDENTITY_SEGMENT_FROZEN"
    assert frozen["identity_segment_frozen"] is True
    assert frozen["authority_boundary"]["identity_segment_frozen"] is True


def test_source_candidate_and_review_package_digests_are_bound():
    frozen = _frozen()

    assert frozen["source_candidate_kind"] == "IDENTITY_SEGMENT_CANDIDATE"
    assert frozen["source_candidate_status"] == "IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW"
    assert frozen["source_candidate_semantic_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert frozen["source_review_package_kind"] == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE"
    assert frozen["source_review_status"] == "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY"
    assert frozen["source_review_package_semantic_digest"] == EXPECTED_REVIEW_DIGEST


def test_wrong_operator_attestation_phrase_is_rejected():
    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError, match="operator_attestation_phrase"):
        _frozen(operator_attestation=_attestation(operator_attestation_phrase="wrong phrase"))


def test_wrong_operator_decision_is_rejected():
    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError, match="operator_decision"):
        _frozen(operator_attestation=_attestation(operator_decision="REJECT_IDENTITY_SEGMENT_FREEZE"))


def test_wrong_candidate_digest_confirmation_is_rejected():
    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError, match="operator_candidate_digest"):
        _frozen(operator_attestation=_attestation(operator_confirms_candidate_digest="0" * 64))


def test_wrong_review_package_digest_confirmation_is_rejected():
    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError, match="operator_review_digest"):
        _frozen(operator_attestation=_attestation(operator_confirms_review_package_digest="1" * 64))


def test_missing_attestation_is_rejected():
    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError, match="operator_attestation"):
        ceremony.build_identity_segment_frozen_v1(operator_attestation=None)


def test_review_package_with_blocker_count_is_rejected():
    package = review.build_identity_segment_candidate_review_package_v1()
    package["review_summary"]["blocker_count"] = 1
    package["review_package_semantic_digest"] = review.review_package_semantic_digest(package)

    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError):
        _frozen(review_package=package)


def test_segment_fields_match_exact_identity_segment():
    segment = _frozen()["frozen_identity_segment"]

    assert segment["ticker"] == "AAPL"
    assert segment["composite_figi"] == "BBG000B9XRY4"
    assert segment["share_class_figi"] == "BBG001S5N8V8"
    assert segment["primary_mic"] == "XNAS"
    assert segment["security_type"] == "CS"
    assert segment["segment_start"] == "2022-01-01"
    assert segment["segment_end"] == "2025-12-31"


def test_contract_digest_matches_exact_value():
    frozen = _frozen()

    assert frozen["acquisition_contract_digest"] == "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"
    assert frozen["frozen_identity_segment"]["acquisition_contract_digest"] == frozen["acquisition_contract_digest"]


def test_identity_evidence_digests_match_exact_values():
    frozen = _frozen()
    identity = frozen["identity_evidence_binding"]
    identity_summary = frozen["identity_evidence"]

    assert identity["identity_run_id"] == "ident-509de6e2eb5e4a1db785e034bcfaf045"
    assert identity["continuity_artifact_id"] == "ident-art-8607986a2341423182614a41c6236ed9"
    assert identity["start_snapshot_semantic_digest"] == "75a3fb5cccda09c05001129ec7161ad479457a714a5903828c67c5cfeb965928"
    assert identity["end_snapshot_semantic_digest"] == "5e80a556b6172d8ca8985177f8c17e05183322fb5981ba92def57d4698aa4f50"
    assert identity["continuity_status"] == "IDENTITY_CONTINUITY_SUPPORTED"
    assert identity["total_manifests"] == 6
    assert identity_summary["artifact_inventory_total"] == 6
    assert identity_summary["identity_run_id"] == identity["identity_run_id"]


def test_ticker_events_evidence_digests_match_exact_values():
    ticker_events = _frozen()["ticker_events_evidence_binding"]

    assert ticker_events["ticker_events_audit_run_id"] == "tkev-959a591271874fe49bc8cb34bb29be36"
    assert ticker_events["raw_response_artifact_id"] == "tkev-art-5d8ed7c1aa0e451ab1c7b297230dca33"
    assert ticker_events["raw_response_semantic_payload_digest"] == "07082085e9e41c467e020774954c045e83613d9581976ca26e87b74e3bbf15dc"
    assert ticker_events["timeline_artifact_id"] == "tkev-art-54a14c247fb2459a9c588dd4695b4358"
    assert ticker_events["timeline_semantic_digest"] == "36ccff35908df36a7fadb124d6cb846e4ac0cace578830e7591f7edf92bde820"
    assert ticker_events["audit_artifact_id"] == "tkev-art-df20d0c474464b74a28a6f4ed451fef6"
    assert ticker_events["receipt_artifact_id"] == "tkev-art-2168e3f7caec46d59436ab0e4280d49d"
    assert ticker_events["endpoint"] == "TICKER_EVENTS_EXPERIMENTAL_VX"
    assert ticker_events["endpoint_stability"] == "EXPERIMENTAL"


def test_in_range_ticker_events_remain_zero():
    ticker_events = _frozen()["ticker_events_evidence_binding"]

    assert ticker_events["pre_range_events"] == 1
    assert ticker_events["in_range_events"] == 0
    assert ticker_events["post_range_events"] == 0
    assert ticker_events["ticker_events_audit_status"] == "TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE"


def test_automatic_stitching_remains_false():
    frozen = _frozen()

    assert frozen["automatic_stitching"] is False
    assert frozen["authority_boundary"]["automatic_stitching"] is False
    assert frozen["lineage_guardrails"]["provider_requests_made"] is False


def test_calendar_canonical_registry_acquisition_and_runtime_flags_remain_false():
    frozen = _frozen()
    boundary = frozen["authority_boundary"]

    for field in (
        "calendar_operator_frozen",
        "canonical_eligibility",
        "registry_eligibility",
        "acquisition_generation_freeze",
        "strategy_runtime_migration",
    ):
        assert frozen[field] is False
        assert boundary[field] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    frozen = _frozen()
    boundary = frozen["authority_boundary"]

    assert frozen["predictive_usefulness"] == "not accepted"
    assert frozen["profitability"] == "not accepted"
    assert boundary["predictive_usefulness"] == "not accepted"
    assert boundary["profitability"] == "not accepted"


def test_frozen_artifact_digest_is_deterministic_for_same_attestation():
    attestation = _attestation()
    first = ceremony.build_identity_segment_frozen_v1(operator_attestation=attestation)
    second = ceremony.build_identity_segment_frozen_v1(operator_attestation=deepcopy(attestation))

    assert first == second
    assert len(first["identity_segment_frozen_semantic_digest"]) == 64
    assert first["identity_segment_frozen_semantic_digest"] == ceremony.identity_segment_frozen_semantic_digest(first)


@pytest.mark.parametrize(
    "field",
    [
        "calendar_operator_frozen",
        "canonical_eligibility",
        "registry_eligibility",
        "acquisition_generation_freeze",
        "strategy_runtime_migration",
    ],
)
def test_validator_rejects_boundary_flag_flipped_true(field: str):
    frozen = _frozen()
    frozen[field] = True
    frozen["authority_boundary"][field] = True
    _recompute_digest(frozen)

    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError):
        ceremony.validate_identity_segment_frozen_v1(frozen)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("composite_figi", "BBG000B9XRZ5"),
        ("segment_start", "2022-01-02"),
        ("segment_end", "2025-12-30"),
        ("security_type", "ETF"),
    ],
)
def test_validator_rejects_changed_segment_figi_dates_or_security_type(field: str, value: str):
    frozen = _frozen()
    frozen["frozen_identity_segment"][field] = value
    _recompute_digest(frozen)

    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError):
        ceremony.validate_identity_segment_frozen_v1(frozen)


def test_validator_rejects_provider_requests_made_true():
    frozen = _frozen()
    frozen["provider_requests_made"] = True
    _recompute_digest(frozen)

    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError, match="provider_requests_made"):
        ceremony.validate_identity_segment_frozen_v1(frozen)


def test_validator_rejects_changed_identity_evidence_digest():
    frozen = _frozen()
    frozen["identity_evidence_binding"]["start_snapshot_semantic_digest"] = "2" * 64
    _recompute_digest(frozen)

    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError):
        ceremony.validate_identity_segment_frozen_v1(frozen)


def test_validator_rejects_changed_ticker_events_digest_and_in_range_count():
    frozen = _frozen()
    frozen["ticker_events_evidence_binding"]["timeline_semantic_digest"] = "3" * 64
    frozen["ticker_events_evidence_binding"]["in_range_events"] = 1
    _recompute_digest(frozen)

    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError):
        ceremony.validate_identity_segment_frozen_v1(frozen)


@pytest.mark.parametrize("field", ceremony.OPERATOR_BOUNDARY_CONFIRMATION_FIELDS)
def test_any_false_operator_boundary_confirmation_is_rejected(field: str):
    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError, match=field):
        _frozen(operator_attestation=_attestation(**{field: False}))


def test_freeze_checklist_totals_authority_and_review_counts():
    frozen = _frozen()
    summary = frozen["freeze_summary"]

    assert [item["check_id"] for item in frozen["freeze_checklist"]] == ceremony.REQUIRED_FREEZE_CHECK_IDS
    assert summary["total_checks"] == len(ceremony.REQUIRED_FREEZE_CHECK_IDS)
    assert summary["passed_checks"] == len(ceremony.REQUIRED_FREEZE_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["identity_segment_freeze_authorized_by_operator"] is True
    assert summary["software_auto_approval"] is False
    assert frozen["source_review_checklist_total"] == 33
    assert frozen["source_review_checklist_passed"] == 33
    assert frozen["source_review_checklist_failed"] == 0
    assert frozen["source_review_blocker_count"] == 0


def test_remaining_roadmap_includes_required_future_work():
    roadmap = _frozen()["remaining_roadmap"]
    rendered = "\n".join(roadmap)

    assert "Official/operator-frozen exchange-calendar evidence." in roadmap
    assert "Split-event audit." in roadmap
    assert "Dividend-event audit." in roadmap
    assert "Full 2022-2025 acquisition generation." in roadmap
    assert "Acquisition-generation freeze." in roadmap
    assert "SWING canonical dataset and registry approval." in roadmap
    assert "POSITION_SWING canonical dataset and registry approval." in roadmap
    assert "Normal runtime migration." in roadmap
    assert "Applicability/research campaign." in roadmap
    assert "Predictive and profitability evaluation." in roadmap
    assert "canonical dataset" in rendered


def test_markdown_writer_includes_required_sections_and_guardrails():
    frozen = _frozen()
    markdown = ceremony.build_identity_segment_frozen_markdown_v1(frozen)

    for heading in (
        "# Identity Segment Frozen v1",
        "## Frozen Identity Segment",
        "## Operator Attestation",
        "## Source Candidate",
        "## Source Review Package",
        "## Evidence Bound",
        "## Freeze Checklist Summary",
        "## Authority Boundary",
        "## Remaining Roadmap",
        "## Guardrails",
    ):
        assert heading in markdown
    assert EXPECTED_CANDIDATE_DIGEST in markdown
    assert EXPECTED_REVIEW_DIGEST in markdown
    assert "No provider requests were made." in markdown
    assert "No calendar evidence is frozen." in markdown
    assert "Predictive usefulness and profitability remain not accepted." in markdown


def test_write_frozen_artifact_is_offline_json_and_no_overwrite(tmp_path: Path):
    result = ceremony.write_identity_segment_frozen_v1(tmp_path, operator_attestation=_attestation())
    path = Path(result["path"])

    assert result["artifact_kind"] == "IDENTITY_SEGMENT_FROZEN"
    assert result["freeze_status"] == "IDENTITY_SEGMENT_FROZEN"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["identity_segment_frozen_semantic_digest"] == result["identity_segment_frozen_semantic_digest"]
    assert result["frozen_payload_digest"] == ceremony.sha256_bytes(path.read_bytes())
    with pytest.raises(ceremony.IdentitySegmentOperatorFreezeError, match="already exists"):
        ceremony.write_identity_segment_frozen_v1(tmp_path, operator_attestation=_attestation())


def test_source_assurance_freeze_service_has_no_provider_strategy_or_runtime_calls():
    source_path = REPO_ROOT / "marketflow" / "services" / "identity_segment_operator_freeze_service.py"
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
    assert "IDENTITY_SEGMENT_FROZEN" in source
    assert "APPROVE_IDENTITY_SEGMENT_FREEZE" in source
    assert "provider_requests_made" in source
    assert "strategy_runtime_migration" in source


def test_service_exports_freeze_functions_and_constants():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_IDENTITY_SEGMENT_FROZEN == "IDENTITY_SEGMENT_FROZEN"
    assert services.IDENTITY_SEGMENT_FROZEN == "IDENTITY_SEGMENT_FROZEN"
    assert services.OPERATOR_DECISION_APPROVE_IDENTITY_SEGMENT_FREEZE == "APPROVE_IDENTITY_SEGMENT_FREEZE"
    assert services.REQUIRED_OPERATOR_ATTESTATION_PHRASE == ceremony.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    assert services.build_identity_segment_operator_attestation_v1 is ceremony.build_identity_segment_operator_attestation_v1
    assert services.build_identity_segment_frozen_v1 is ceremony.build_identity_segment_frozen_v1
    assert services.validate_identity_segment_frozen_v1 is ceremony.validate_identity_segment_frozen_v1
    assert services.write_identity_segment_frozen_v1 is ceremony.write_identity_segment_frozen_v1
    assert services.build_identity_segment_frozen_markdown_v1 is ceremony.build_identity_segment_frozen_markdown_v1
