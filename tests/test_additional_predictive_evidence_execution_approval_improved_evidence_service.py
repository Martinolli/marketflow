from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    additional_predictive_evidence_execution_approval_improved_evidence_service as approval_service,
)
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_improved_evidence_operator_review_service as review_service,
)


def _attestation(**overrides):
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-22T12:00:00Z",
        "operator_attestation_phrase": approval_service.REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_ATTESTATION_PHRASE,
        **approval_service.DIGEST_CONFIRMATIONS,
        **approval_service.VALUE_CONFIRMATIONS,
        **{field: True for field in approval_service.BOOLEAN_CONFIRMATIONS},
    }
    values.update(overrides)
    return approval_service.build_additional_predictive_evidence_execution_approval_using_improved_evidence_attestation_v1(
        **values
    )


@pytest.fixture(scope="module")
def approval() -> dict:
    return approval_service.build_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == approval_service.OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_IMPROVED_EVIDENCE
    assert attestation["operator_attestation_version"] == approval_service.OPERATOR_ATTESTATION_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_V1
    assert set(approval_service.DIGEST_CONFIRMATIONS) <= set(attestation)
    assert set(approval_service.VALUE_CONFIRMATIONS) <= set(attestation)
    assert set(approval_service.BOOLEAN_CONFIRMATIONS) <= set(attestation)


def test_approval_package_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("socket.socket.connect", lambda *_args, **_kwargs: pytest.fail("network access"))
    package = approval_service.build_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
        operator_attestation=_attestation()
    )
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_approval"] is False
    assert package["live_provider_transport_enabled_in_approval"] is False


def test_artifact_status_and_scope_are_exact(approval: dict) -> None:
    assert approval["artifact_kind"] == approval_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE
    assert approval["approval_status"] == approval_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_IMPROVED_EVIDENCE
    assert approval["approval_scope"] == approval_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY


@pytest.mark.parametrize(("field", "expected"), [
    ("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest", approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST),
    ("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest", approval_service.EXPECTED_CANDIDATE_DIGEST),
    *list(approval_service.BOUND_DIGESTS.items()),
])
def test_all_required_digests_are_bound(approval: dict, field: str, expected: str) -> None:
    assert approval[field] == expected


def test_dataset_universe_and_meta_are_preserved(approval: dict) -> None:
    assert approval["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert approval["target_universe"] == approval_service.TARGET_UNIVERSE
    assert approval["target_universe_count"] == 12
    assert approval["total_canonical_record_count"] == 11946
    assert approval["records_digest"] == approval_service.BOUND_DIGESTS["records_digest"]
    assert approval["meta_record_count"] == 913
    assert approval["non_meta_record_count"] == 1003


def test_selected_redesign_direction_is_preserved(approval: dict) -> None:
    assert approval["selected_redesign_direction"] == approval_service.SELECTED_DIRECTION
    assert approval["operator_attestation"]["selected_redesign_direction"] == approval_service.SELECTED_DIRECTION


@pytest.mark.parametrize("field", [
    "additional_predictive_evidence_execution_approved",
    "additional_predictive_evidence_execution_approval_created",
    "additional_predictive_evidence_execution_authorized",
    "ready_for_additional_predictive_evidence_execution_using_improved_evidence",
])
def test_approval_authorization_and_readiness_are_true(approval: dict, field: str) -> None:
    assert approval[field] is True


@pytest.mark.parametrize("field", [
    "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
    "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
    "target_definition_change_authorized", "target_definition_change_performed",
    "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
    "metric_recomputation_performed_in_approval", "model_training_performed_in_approval",
    "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
    "predictive_usefulness_acceptance_candidate_created", "profitability_acceptance_ready",
    "profitability_acceptance_recommended", "runtime_migration_approved", "runtime_migration_active",
    "new_strategy_scoring_performed", "trade_recommendations_generated",
    "provider_requests_made_in_approval", "market_data_acquisition_performed_in_approval",
    "canonical_dataset_regenerated_in_approval", "redesigned_label_regeneration_performed",
    "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
    "improved_evidence_planning_execution_rerun_performed", "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
])
def test_execution_acceptance_and_external_actions_remain_false(approval: dict, field: str) -> None:
    assert approval[field] is False


def test_predictive_profitability_and_runtime_boundaries_remain_closed(approval: dict) -> None:
    assert approval["predictive_usefulness"] == "not accepted"
    assert approval["profitability"] == "not accepted"
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert approval[field] == "NOT_AUTHORIZED"


def test_approved_candidate_basis_and_objective_are_exact(approval: dict) -> None:
    assert approval["approved_candidate_basis"] == review_service.candidate_service.CANDIDATE_BASIS
    assert approval["approved_objective"] == {
        "additional_predictive_evidence_execution_objective": approval_service.EXECUTION_OBJECTIVE,
        "additional_predictive_evidence_execution_scope": approval_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "additional_predictive_evidence_execution_mode": "AUTHORIZED_NOT_EXECUTED",
        "additional_predictive_evidence_execution_authority_status": approval_service.EXECUTION_AUTHORITY_STATUS,
    }


def test_approved_source_inputs_count_and_status(approval: dict) -> None:
    rows = approval["approved_source_inputs"]
    assert len(rows) == 15
    assert [row["source_input_id"] for row in rows] == review_service.candidate_service.PLANNED_SOURCE_INPUT_IDS
    assert all(row["approval_status"] == "APPROVED_FOR_FUTURE_RESEARCH_EVIDENCE_EXECUTION_ONLY" for row in rows)
    assert all(row["execution_performed"] is False and row["source_regenerated"] is False for row in rows)


def test_approved_execution_activities_count_and_status(approval: dict) -> None:
    rows = approval["approved_execution_activities"]
    assert len(rows) == 12
    assert [row["activity_id"] for row in rows] == review_service.candidate_service.PLANNED_EXECUTION_ACTIVITY_IDS
    assert all(row["activity_status"] == "AUTHORIZED_NOT_EXECUTED" for row in rows)
    assert all(row["execution_authorized"] is True and row["execution_performed"] is False for row in rows)
    assert all(row["label_generation_authorized"] is False and row["feature_generation_authorized"] is False for row in rows)


def test_label_feature_matrix_boundaries_are_exact(approval: dict) -> None:
    assert approval["approved_label_feature_matrix_boundaries"] == approval_service._approved_boundaries()


def test_approved_model_metric_and_output_families(approval: dict) -> None:
    assert len(approval["approved_model_and_baseline_families"]) == 9
    assert all(row["model_family_status"] == "AUTHORIZED_NOT_EVALUATED" for row in approval["approved_model_and_baseline_families"])
    assert len(approval["approved_metric_families"]) == 10
    assert all(row["metric_status"] == "AUTHORIZED_NOT_COMPUTED" for row in approval["approved_metric_families"])
    assert len(approval["approved_future_outputs"]) == 12
    assert all(row["output_status"] == "AUTHORIZED_NOT_GENERATED" and row["generated"] is False for row in approval["approved_future_outputs"])


def test_per_ticker_approval_entries_preserve_meta(approval: dict) -> None:
    entries = approval["per_ticker_approval_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval_service.TARGET_UNIVERSE
    assert all(row["additional_predictive_evidence_execution_authorized"] is True for row in entries)
    assert all(row["additional_predictive_evidence_executed"] is False for row in entries)
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["approval_note"] == "PRESERVE_META_LIMITATION_IN_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE"
    assert all(row["historical_record_count"] == 1003 for row in entries if row["ticker"] != "META")


def test_per_ticker_approval_digests_are_present_and_deterministic(approval: dict) -> None:
    for row in approval["per_ticker_approval_entries"]:
        digest = row["per_ticker_additional_predictive_evidence_execution_approval_digest"]
        assert len(digest) == 64
        assert digest == approval_service.per_ticker_additional_predictive_evidence_execution_approval_using_improved_evidence_digest_v1(row)


def test_next_chain_gates_and_risk_controls_are_exact(approval: dict) -> None:
    assert approval["next_chain"] == approval_service.NEXT_CHAIN
    assert approval["next_gates"] == approval_service.NEXT_GATES
    assert approval["risk_controls"] == approval_service.RISK_CONTROLS


def test_checklist_passes_exactly(approval: dict) -> None:
    assert len(approval_service.REQUIRED_CHECK_IDS) == 80
    assert [row["check_id"] for row in approval["approval_checklist"]] == approval_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in approval["approval_checklist"])
    assert approval["approval_summary"]["total_checks"] == 80
    assert approval["approval_summary"]["passed_checks"] == 80
    assert approval["approval_summary"]["failed_checks"] == 0
    assert approval["approval_summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic_and_exact(approval: dict) -> None:
    digest = approval["additional_predictive_evidence_execution_approval_using_improved_evidence_digest"]
    assert digest == "c2ce4254de6c4fa3934a6c1fddb04f8bad334054ba914119c915f6b6071c558f"
    assert digest == approval_service.additional_predictive_evidence_execution_approval_using_improved_evidence_digest_v1(approval)


def test_validator_accepts_valid_approval(approval: dict) -> None:
    result = approval_service.validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(approval)
    assert result["status"] == approval_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_IMPROVED_EVIDENCE_VALID
    assert result["blocker_count"] == 0
    assert result["additional_predictive_evidence_execution_authorized"] is True
    assert result["additional_predictive_evidence_executed"] is False


@pytest.mark.parametrize(("field", "value"), [
    ("artifact_kind", "WRONG"), ("approval_status", "WRONG"), ("approval_scope", "WRONG"),
    ("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest", None),
    ("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest", None),
    ("improved_evidence_planning_results_review_using_redesigned_evidence_digest", None),
    ("records_digest", None), ("target_universe", ["AAPL"]), ("target_universe_count", 11),
    ("meta_record_count", 1003), ("selected_redesign_direction", "WRONG"),
    ("additional_predictive_evidence_execution_approved", False),
    ("additional_predictive_evidence_execution_authorized", False),
    ("ready_for_additional_predictive_evidence_execution_using_improved_evidence", False),
    ("additional_predictive_evidence_executed", True),
    ("additional_predictive_evidence_results_created", True),
    ("label_regeneration_authorized", True), ("label_regeneration_performed", True),
    ("new_targets_created", True), ("target_definition_change_authorized", True),
    ("feature_generation_authorized", True), ("feature_generation_performed", True),
    ("feature_label_matrix_created", True), ("metric_recomputation_performed_in_approval", True),
    ("model_training_performed_in_approval", True), ("predictive_usefulness", "accepted"),
    ("predictive_usefulness_acceptance_ready", True),
    ("predictive_usefulness_acceptance_candidate_created", True), ("profitability", "accepted"),
    ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True),
])
def test_validator_rejects_changed_or_forbidden_fields(approval: dict, field: str, value) -> None:
    changed = deepcopy(approval)
    changed[field] = value
    with pytest.raises(approval_service.AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError):
        approval_service.validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(changed)


@pytest.mark.parametrize(("field", "value"), [
    ("operator_decision", "WRONG"),
    ("operator_attestation_phrase", "WRONG"),
    ("selected_redesign_direction", "WRONG"),
    ("operator_attestation_version", "WRONG"),
    ("operator_reference", ""),
    ("operator_attestation_timestamp_utc", ""),
    *[(field, "WRONG") for field in approval_service.DIGEST_CONFIRMATIONS],
    ("operator_confirms_target_universe", ["AAPL"]),
    ("operator_confirms_target_count", 11),
    ("operator_confirms_meta_record_count", 1003),
    ("operator_confirms_non_meta_record_count", 913),
    ("operator_confirms_selected_redesign_direction", "WRONG"),
    *[(field, False) for field in approval_service.BOOLEAN_CONFIRMATIONS],
])
def test_validator_rejects_incorrect_attestation_confirmation(
    approval: dict, field: str, value
) -> None:
    changed = deepcopy(approval)
    changed["operator_attestation"][field] = value
    with pytest.raises(approval_service.AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError):
        approval_service.validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(changed)


def test_builder_rejects_attestation_with_missing_confirmation() -> None:
    attestation = _attestation()
    attestation.pop("operator_confirms_no_execution_performed")
    with pytest.raises(approval_service.AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError):
        approval_service.build_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
            operator_attestation=attestation
        )


@pytest.mark.parametrize("field", [
    "approved_candidate_basis", "approved_source_inputs", "approved_execution_activities",
    "approved_label_feature_matrix_boundaries", "approved_model_and_baseline_families",
    "approved_metric_families", "approved_future_outputs", "next_chain", "next_gates",
    "risk_controls", "additional_predictive_evidence_execution_approval_using_improved_evidence_digest",
])
def test_validator_rejects_missing_required_structures(approval: dict, field: str) -> None:
    changed = deepcopy(approval)
    changed.pop(field)
    with pytest.raises(approval_service.AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError):
        approval_service.validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(changed)


def test_validator_rejects_missing_per_ticker_approval_digest(approval: dict) -> None:
    changed = deepcopy(approval)
    changed["per_ticker_approval_entries"][0].pop(
        "per_ticker_additional_predictive_evidence_execution_approval_digest"
    )
    with pytest.raises(approval_service.AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError):
        approval_service.validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(changed)


def test_builder_rejects_changed_source_review_digest() -> None:
    source = review_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1()
    source["additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest"] = "0" * 64
    with pytest.raises(
        review_service.AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError
    ):
        approval_service.build_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
            candidate_review_package=source, operator_attestation=_attestation()
        )


def test_markdown_includes_all_required_sections(approval: dict) -> None:
    markdown = approval_service.build_additional_predictive_evidence_execution_approved_using_improved_evidence_markdown_v1(
        approval
    )
    for section in (
        "## Title", "## Optional Additional Predictive Evidence Execution Approval Using Improved Evidence",
        "## Operator Attestation", "## Source Candidate Review", "## Bound Evidence",
        "## Dataset and Universe", "## Approved Candidate Basis", "## Approved Objective",
        "## Approved Source Inputs", "## Approved Execution Activities",
        "## Approved Label / Feature / Matrix Boundaries", "## Approved Model and Baseline Families",
        "## Approved Metric Families", "## Approved Future Outputs", "## Per-Ticker Approval Entries",
        "## Next Chain", "## Next Gates", "## Risk Controls", "## Predictive Usefulness Boundary",
        "## Profitability Boundary", "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    ):
        assert section in markdown


def test_public_exports_are_available() -> None:
    assert services.build_additional_predictive_evidence_execution_approval_using_improved_evidence_attestation_v1 is approval_service.build_additional_predictive_evidence_execution_approval_using_improved_evidence_attestation_v1
    assert services.build_additional_predictive_evidence_execution_approved_using_improved_evidence_v1 is approval_service.build_additional_predictive_evidence_execution_approved_using_improved_evidence_v1
    assert services.validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1 is approval_service.validate_additional_predictive_evidence_execution_approved_using_improved_evidence_v1


def test_writer_is_no_overwrite_and_uses_temporary_directory(tmp_path) -> None:
    result = approval_service.write_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
        tmp_path, operator_attestation=_attestation()
    )
    assert result["payload_byte_size"] > 0
    assert len(result["payload_sha256"]) == 64
    with pytest.raises(approval_service.AdditionalPredictiveEvidenceExecutionApprovalImprovedEvidenceError):
        approval_service.write_additional_predictive_evidence_execution_approved_using_improved_evidence_v1(
            tmp_path, operator_attestation=_attestation()
        )
