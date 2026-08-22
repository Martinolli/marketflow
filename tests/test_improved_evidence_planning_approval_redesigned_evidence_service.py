from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import (
    improved_evidence_planning_approval_redesigned_evidence_service as approval_service,
)


def build_valid_attestation() -> dict:
    return approval_service.build_improved_evidence_planning_approval_using_redesigned_evidence_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-22T00:00:00Z",
        operator_attestation_phrase=approval_service.REQUIRED_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=approval_service.EXPECTED_CANDIDATE_DIGEST,
        operator_confirms_redesign_results_review_digest=approval_service.BOUND_DIGESTS["label_objective_redesign_results_review_using_redesigned_evidence_digest"],
        operator_confirms_redesign_execution_digest=approval_service.BOUND_DIGESTS["label_objective_redesign_execution_using_redesigned_evidence_digest"],
        operator_confirms_records_digest=approval_service.BOUND_DIGESTS["records_digest"],
        operator_confirms_target_universe=approval_service.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
        operator_confirms_selected_redesign_direction=approval_service.SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        operator_confirms_approval_scope_only=True,
        operator_confirms_planning_authorized=True,
        operator_confirms_ready_for_planning_execution=True,
        operator_confirms_no_planning_execution=True,
        operator_confirms_no_label_regeneration=True,
        operator_confirms_no_new_targets=True,
        operator_confirms_no_target_definition_change_authorization=True,
        operator_confirms_no_feature_generation=True,
        operator_confirms_no_feature_label_matrix_creation=True,
        operator_confirms_no_additional_predictive_evidence_execution_candidate=True,
        operator_confirms_no_predictive_evidence_execution=True,
        operator_confirms_no_predictive_evidence_rerun=True,
        operator_confirms_no_metric_recomputation=True,
        operator_confirms_no_model_training=True,
        operator_confirms_no_predictive_usefulness_acceptance=True,
        operator_confirms_no_profitability_acceptance=True,
        operator_confirms_no_runtime_migration_approval=True,
        operator_confirms_no_strategy_authorization=True,
        operator_confirms_no_paper_trading=True,
        operator_confirms_no_broker_execution=True,
        operator_confirms_no_trade_recommendations=True,
        operator_confirms_no_api_key_storage_or_printing=True,
        operator_confirms_no_raw_payload_commit=True,
    )


@pytest.fixture(scope="module")
def attestation() -> dict:
    return build_valid_attestation()


@pytest.fixture(scope="module")
def approval(attestation: dict) -> dict:
    return approval_service.build_improved_evidence_planning_approved_using_redesigned_evidence_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_fields(attestation: dict) -> None:
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == "2026-08-22T00:00:00Z"
    assert attestation["operator_attestation_phrase"] == approval_service.REQUIRED_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_ATTESTATION_PHRASE
    assert attestation["operator_decision"] == approval_service.OPERATOR_DECISION_APPROVE_IMPROVED_EVIDENCE_PLANNING_USING_REDESIGNED_EVIDENCE
    assert attestation["operator_attestation_version"] == approval_service.OPERATOR_ATTESTATION_VERSION_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_V1


@pytest.mark.parametrize(
    "field", approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_attestation_builder_preserves_required_confirmation(attestation: dict, field: str) -> None:
    assert attestation[field] is True


def test_approval_package_builds_offline(monkeypatch: pytest.MonkeyPatch, attestation: dict) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    result = approval_service.build_improved_evidence_planning_approved_using_redesigned_evidence_v1(operator_attestation=attestation)
    assert result["created_offline"] is True
    assert result["provider_requests_made_in_approval"] is False
    assert result["market_data_acquisition_performed_in_approval"] is False


def test_artifact_kind_is_correct(approval: dict) -> None:
    assert approval["artifact_kind"] == approval_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE


def test_approval_status_is_correct(approval: dict) -> None:
    assert approval["approval_status"] == approval_service.IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE


def test_approval_scope_is_correct(approval: dict) -> None:
    assert approval["approval_scope"] == approval_service.IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY


def test_candidate_review_digest_is_bound(approval: dict) -> None:
    assert approval["improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"] == approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_candidate_digest_is_bound(approval: dict) -> None:
    assert approval["improved_evidence_planning_candidate_using_redesigned_evidence_digest"] == approval_service.EXPECTED_CANDIDATE_DIGEST


@pytest.mark.parametrize(
    ("field", "expected"), list(approval_service.BOUND_DIGESTS.items())
)
def test_bound_digest_is_exact(approval: dict, field: str, expected: str) -> None:
    assert approval[field] == expected


def test_universe_count_and_order_are_preserved(approval: dict) -> None:
    assert approval["target_universe_count"] == 12
    assert approval["target_universe"] == approval_service.TARGET_UNIVERSE


def test_meta_913_is_preserved(approval: dict) -> None:
    assert approval["meta_record_count"] == 913
    assert approval["per_ticker_record_counts"]["META"] == 913
    assert approval["meta_reduced_record_count_preserved"] is True


def test_selected_redesign_direction_is_preserved(approval: dict) -> None:
    assert approval["selected_direction"] == approval_service.SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION


def test_approval_authorization_and_ready_are_true(approval: dict) -> None:
    assert approval["improved_evidence_planning_approved"] is True
    assert approval["improved_evidence_planning_approval_created"] is True
    assert approval["improved_evidence_planning_authorized"] is True
    assert approval["ready_for_improved_evidence_planning_execution_using_redesigned_evidence"] is True


@pytest.mark.parametrize(
    "field",
    [
        "improved_evidence_planning_executed",
        "improved_evidence_planning_execution_created",
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "feature_generation_authorized",
        "feature_generation_performed",
        "feature_label_matrix_created",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_executed",
        "trade_recommendations_generated",
    ],
)
def test_unapproved_action_remains_false(approval: dict, field: str) -> None:
    assert approval[field] is False


def test_predictive_usefulness_is_not_accepted(approval: dict) -> None:
    assert approval["predictive_usefulness"] == "not accepted"
    assert approval["predictive_usefulness_acceptance_ready"] is False
    assert approval["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_is_not_accepted(approval: dict) -> None:
    assert approval["profitability"] == "not accepted"
    assert approval["profitability_acceptance_ready"] is False


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_are_not_authorized(approval: dict, field: str) -> None:
    assert approval[field] == "NOT_AUTHORIZED"


def test_approved_candidate_basis_is_preserved(approval: dict) -> None:
    assert approval["approved_candidate_basis"] == approval_service.review_service.candidate_service.CANDIDATE_BASIS


def test_approved_objective_is_defined(approval: dict) -> None:
    assert approval["improved_evidence_planning_objective"] == approval_service.APPROVED_OBJECTIVE
    assert approval["improved_evidence_planning_scope"] == approval_service.APPROVED_SCOPE
    assert approval["improved_evidence_planning_mode"] == "AUTHORIZED_NOT_EXECUTED"
    assert approval["improved_evidence_planning_authority_status"] == "AUTHORIZED_FOR_FUTURE_RESEARCH_ONLY_PLANNING_EXECUTION"


def test_approved_themes_count_is_eleven(approval: dict) -> None:
    rows = approval["approved_improved_evidence_themes"]
    assert len(rows) == 11
    assert [row["theme_id"] for row in rows] == approval_service.review_service.candidate_service.IMPROVED_EVIDENCE_THEME_IDS
    assert all(row["approval_status"] == approval_service.APPROVED_FOR_FUTURE_RESEARCH_PLANNING_EXECUTION_ONLY for row in rows)
    assert all(row["execution_performed"] is False for row in rows)


def test_approved_components_count_is_thirteen(approval: dict) -> None:
    rows = approval["approved_planned_evidence_components"]
    assert len(rows) == 13
    assert [row["component_id"] for row in rows] == approval_service.review_service.candidate_service.PLANNED_EVIDENCE_COMPONENT_IDS
    assert all(row["feature_label_matrix_creation_authorized"] is False for row in rows)


def test_approved_data_products_count_is_thirteen(approval: dict) -> None:
    rows = approval["approved_data_products"]
    assert len(rows) == 13
    assert [row["data_product_id"] for row in rows] == approval_service.APPROVED_DATA_PRODUCT_IDS
    assert all(row["output_status"] == "AUTHORIZED_NOT_GENERATED" for row in rows)
    assert all(row["generated"] is False for row in rows)


def test_approved_future_outputs_count_is_twelve(approval: dict) -> None:
    rows = approval["approved_future_outputs"]
    assert len(rows) == 12
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["generated"] is False for row in rows)


def test_per_ticker_approval_entries_count_is_twelve(approval: dict) -> None:
    entries = approval["per_ticker_approval_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval_service.TARGET_UNIVERSE


def test_per_ticker_approval_digests_are_present(approval: dict) -> None:
    for entry in approval["per_ticker_approval_entries"]:
        digest = entry["per_ticker_improved_evidence_planning_approval_digest"]
        assert len(digest) == 64
        assert digest == approval_service.per_ticker_improved_evidence_planning_approval_digest_v1(entry)


def test_meta_approval_entry_preserves_limitation(approval: dict) -> None:
    meta = next(row for row in approval["per_ticker_approval_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["approval_note"] == "PRESERVE_META_LIMITATION_IN_IMPROVED_EVIDENCE_PLANNING_APPROVAL"


def test_next_chain_is_defined(approval: dict) -> None:
    assert approval["next_chain"] == approval_service.NEXT_CHAIN


def test_next_gates_are_defined(approval: dict) -> None:
    assert approval["next_gates"] == approval_service.NEXT_GATES


def test_risk_controls_are_defined(approval: dict) -> None:
    assert approval["risk_controls"] == approval_service.RISK_CONTROLS


def test_checklist_passes(approval: dict) -> None:
    checklist = approval["approval_checklist"]
    assert [row["check_id"] for row in checklist] == approval_service.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == "PASS" for row in checklist)
    assert approval["approval_summary"]["total_checks"] == 79
    assert approval["approval_summary"]["passed_checks"] == 79
    assert approval["approval_summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic(approval: dict) -> None:
    first = approval_service.improved_evidence_planning_approval_using_redesigned_evidence_digest_v1(approval)
    second = approval_service.improved_evidence_planning_approval_using_redesigned_evidence_digest_v1(deepcopy(approval))
    assert first == second == approval["improved_evidence_planning_approval_using_redesigned_evidence_digest"]


def test_per_ticker_approval_digests_are_deterministic(approval: dict) -> None:
    for entry in approval["per_ticker_approval_entries"]:
        first = approval_service.per_ticker_improved_evidence_planning_approval_digest_v1(entry)
        second = approval_service.per_ticker_improved_evidence_planning_approval_digest_v1(deepcopy(entry))
        assert first == second


def test_validator_accepts_valid_approval(approval: dict) -> None:
    validation = approval_service.validate_improved_evidence_planning_approved_using_redesigned_evidence_v1(deepcopy(approval))
    assert validation["status"] == approval_service.IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_VALID
    assert validation["improved_evidence_planning_authorized"] is True
    assert validation["improved_evidence_planning_executed"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest", None),
        ("improved_evidence_planning_candidate_using_redesigned_evidence_digest", None),
        ("label_objective_redesign_results_review_using_redesigned_evidence_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(approval_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("selected_direction", "WRONG"),
        ("improved_evidence_planning_approved", False),
        ("improved_evidence_planning_authorized", False),
        ("ready_for_improved_evidence_planning_execution_using_redesigned_evidence", False),
        ("improved_evidence_planning_executed", True),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("target_definition_change_authorized", True),
        ("feature_generation_performed", True),
        ("feature_label_matrix_created", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("additional_predictive_evidence_executed", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("predictive_evidence_execution_rerun_performed", True),
        ("metric_recomputation_performed_in_approval", True),
        ("model_training_performed_in_approval", True),
    ],
)
def test_validator_rejects_invalid_approval_boundary(approval: dict, field: str, value) -> None:
    changed = deepcopy(approval)
    changed[field] = value
    with pytest.raises(approval_service.ImprovedEvidencePlanningApprovalRedesignedEvidenceError):
        approval_service.validate_improved_evidence_planning_approved_using_redesigned_evidence_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "WRONG"),
        ("selected_redesign_direction", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
        ("operator_confirms_candidate_review_digest", "0" * 64),
        ("operator_confirms_candidate_digest", "0" * 64),
        ("operator_confirms_redesign_results_review_digest", "0" * 64),
        ("operator_confirms_redesign_execution_digest", "0" * 64),
        ("operator_confirms_records_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(approval_service.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_meta_record_count", 1003),
        ("operator_confirms_non_meta_record_count", 913),
        ("operator_confirms_selected_redesign_direction", "WRONG"),
    ],
)
def test_builder_rejects_wrong_attestation_value(attestation: dict, field: str, value) -> None:
    changed = deepcopy(attestation)
    changed[field] = value
    with pytest.raises(approval_service.ImprovedEvidencePlanningApprovalRedesignedEvidenceError):
        approval_service.build_improved_evidence_planning_approved_using_redesigned_evidence_v1(operator_attestation=changed)


@pytest.mark.parametrize(
    "field", approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_builder_rejects_missing_required_confirmation(attestation: dict, field: str) -> None:
    changed = deepcopy(attestation)
    changed[field] = False
    with pytest.raises(approval_service.ImprovedEvidencePlanningApprovalRedesignedEvidenceError):
        approval_service.build_improved_evidence_planning_approved_using_redesigned_evidence_v1(operator_attestation=changed)


def test_validator_rejects_missing_risk_controls(approval: dict) -> None:
    changed = deepcopy(approval)
    changed.pop("risk_controls")
    with pytest.raises(approval_service.ImprovedEvidencePlanningApprovalRedesignedEvidenceError):
        approval_service.validate_improved_evidence_planning_approved_using_redesigned_evidence_v1(changed)


def test_validator_rejects_missing_approval_digest(approval: dict) -> None:
    changed = deepcopy(approval)
    changed.pop("improved_evidence_planning_approval_using_redesigned_evidence_digest")
    with pytest.raises(approval_service.ImprovedEvidencePlanningApprovalRedesignedEvidenceError):
        approval_service.validate_improved_evidence_planning_approved_using_redesigned_evidence_v1(changed)


def test_validator_rejects_missing_per_ticker_approval_digest(approval: dict) -> None:
    changed = deepcopy(approval)
    changed["per_ticker_approval_entries"][0].pop("per_ticker_improved_evidence_planning_approval_digest")
    with pytest.raises(approval_service.ImprovedEvidencePlanningApprovalRedesignedEvidenceError):
        approval_service.validate_improved_evidence_planning_approved_using_redesigned_evidence_v1(changed)


def test_markdown_includes_required_sections(approval: dict) -> None:
    markdown = approval_service.build_improved_evidence_planning_approved_using_redesigned_evidence_markdown_v1(approval)
    sections = [
        "Title",
        "Optional Improved Evidence Planning Approval Using Redesigned Evidence",
        "Operator Attestation",
        "Source Candidate Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Approved Candidate Basis",
        "Approved Objective",
        "Approved Improved Evidence Themes",
        "Approved Planned Evidence Components",
        "Approved Data Products",
        "Approved Future Outputs",
        "Per-Ticker Approval Entries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    for section in sections:
        assert f"## {section}" in markdown


def test_writer_writes_canonical_approval_once(approval: dict, attestation: dict, tmp_path) -> None:
    result = approval_service.write_improved_evidence_planning_approved_using_redesigned_evidence_v1(tmp_path, operator_attestation=attestation)
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written == approval
    with pytest.raises(approval_service.ImprovedEvidencePlanningApprovalRedesignedEvidenceError):
        approval_service.write_improved_evidence_planning_approved_using_redesigned_evidence_v1(tmp_path, operator_attestation=attestation)


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE is approval_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE
    assert services.IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY is approval_service.IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY
    assert services.build_improved_evidence_planning_approval_using_redesigned_evidence_attestation_v1 is approval_service.build_improved_evidence_planning_approval_using_redesigned_evidence_attestation_v1
    assert services.build_improved_evidence_planning_approved_using_redesigned_evidence_v1 is approval_service.build_improved_evidence_planning_approved_using_redesigned_evidence_v1
    assert services.validate_improved_evidence_planning_approved_using_redesigned_evidence_v1 is approval_service.validate_improved_evidence_planning_approved_using_redesigned_evidence_v1
    assert services.write_improved_evidence_planning_approved_using_redesigned_evidence_v1 is approval_service.write_improved_evidence_planning_approved_using_redesigned_evidence_v1
