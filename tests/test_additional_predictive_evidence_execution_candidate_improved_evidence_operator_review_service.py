from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_improved_evidence_operator_review_service as review_service,
)
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_improved_evidence_service as candidate_service,
)


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1()


def test_review_package_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("socket.socket.connect", lambda *_args, **_kwargs: pytest.fail("network access"))
    package = review_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_artifact_kind_and_review_status_are_exact(review_package: dict) -> None:
    assert review_package["artifact_kind"] == review_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE
    assert review_package["review_status"] == review_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE_READY


def test_reviewed_candidate_digest_and_checklist_are_exact(review_package: dict) -> None:
    assert review_package["source_candidate_digest"] == review_service.EXPECTED_CANDIDATE_DIGEST
    assert review_package["source_candidate_checklist_total"] == 78
    assert review_package["source_candidate_checklist_passed"] == 78
    assert review_package["source_candidate_checklist_failed"] == 0
    assert review_package["source_candidate_blocker_count"] == 0


@pytest.mark.parametrize(("field", "expected"), [
    ("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest", review_service.EXPECTED_CANDIDATE_DIGEST),
    *list(candidate_service.BOUND_DIGESTS.items()),
])
def test_all_bound_digests_are_exact(review_package: dict, field: str, expected: str) -> None:
    assert review_package[field] == expected


def test_dataset_universe_and_meta_are_preserved(review_package: dict) -> None:
    assert review_package["target_universe"] == review_service.TARGET_UNIVERSE
    assert review_package["target_universe_count"] == 12
    assert review_package["total_canonical_record_count"] == 11946
    assert review_package["records_digest"] == candidate_service.BOUND_DIGESTS["records_digest"]
    assert review_package["meta_record_count"] == 913
    assert review_package["non_meta_record_count"] == 1003


def test_source_readiness_candidate_and_review_creation_are_true(review_package: dict) -> None:
    assert review_package["source_results_review_ready"] is True
    assert review_package["ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence"] is True
    assert review_package["additional_predictive_evidence_execution_candidate_created"] is True
    assert review_package["additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created"] is True
    assert review_package["additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review"] is True


@pytest.mark.parametrize("field", [
    "additional_predictive_evidence_execution_approved",
    "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
    "additional_predictive_evidence_results_created", "label_regeneration_authorized",
    "label_regeneration_performed", "new_targets_created", "target_definition_change_authorized",
    "target_definition_change_performed", "feature_generation_authorized",
    "feature_generation_performed", "feature_label_matrix_created",
    "metric_recomputation_performed_in_review", "model_training_performed_in_review",
    "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_candidate_created",
    "trade_recommendations_generated", "provider_requests_made_in_review",
    "market_data_acquisition_performed_in_review", "canonical_dataset_regenerated_in_review",
    "predictive_evidence_execution_rerun_performed", "improved_evidence_planning_execution_rerun_performed",
])
def test_all_execution_and_acceptance_actions_remain_false(review_package: dict, field: str) -> None:
    assert review_package[field] is False


def test_predictive_profitability_and_runtime_boundaries_remain_closed(review_package: dict) -> None:
    assert review_package["predictive_usefulness"] == "not accepted"
    assert review_package["profitability"] == "not accepted"
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert review_package[field] == "NOT_AUTHORIZED"


def test_selected_direction_and_candidate_basis_are_reviewed(review_package: dict) -> None:
    assert review_package["selected_redesign_direction"] == candidate_service.SELECTED_DIRECTION
    assert review_package["reviewed_candidate_basis"] == candidate_service.CANDIDATE_BASIS


def test_candidate_objective_is_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_candidate_objective"] == {
        "additional_predictive_evidence_execution_candidate_objective": candidate_service.CANDIDATE_OBJECTIVE,
        "additional_predictive_evidence_execution_candidate_scope": candidate_service.CANDIDATE_SCOPE,
        "additional_predictive_evidence_execution_candidate_mode": candidate_service.CANDIDATE_MODE,
        "additional_predictive_evidence_execution_candidate_authority_status": candidate_service.CANDIDATE_AUTHORITY_STATUS,
    }


def test_all_planned_structures_are_reviewed_without_execution(review_package: dict) -> None:
    assert review_package["reviewed_planned_source_inputs"] == candidate_service._planned_source_inputs()
    assert review_package["reviewed_planned_execution_activities"] == candidate_service._planned_execution_activities()
    assert review_package["reviewed_label_feature_matrix_boundaries"] == candidate_service._label_feature_matrix_boundaries()
    assert review_package["reviewed_planned_model_and_baseline_families"] == candidate_service._planned_model_families()
    assert review_package["reviewed_planned_metric_families"] == candidate_service._planned_metric_families()
    assert review_package["reviewed_planned_future_outputs"] == candidate_service._planned_future_outputs()


def test_planned_structures_preserve_not_executed_statuses(review_package: dict) -> None:
    assert all(row["source_input_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for row in review_package["reviewed_planned_source_inputs"])
    assert all(row["activity_status"] == "PLANNED_NOT_EXECUTED" for row in review_package["reviewed_planned_execution_activities"])
    assert all(row["model_family_status"] == "PLANNED_NOT_EVALUATED" for row in review_package["reviewed_planned_model_and_baseline_families"])
    assert all(row["metric_status"] == "PLANNED_NOT_COMPUTED" for row in review_package["reviewed_planned_metric_families"])
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" and row["generated"] is False for row in review_package["reviewed_planned_future_outputs"])


def test_per_ticker_review_entries_and_meta_limitation(review_package: dict) -> None:
    entries = review_package["per_ticker_review_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == candidate_service.TARGET_UNIVERSE
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["candidate_note"] == "PRESERVE_META_LIMITATION_IN_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE"


def test_per_ticker_candidate_and_review_digests_are_present_and_deterministic(review_package: dict) -> None:
    for row in review_package["per_ticker_review_entries"]:
        candidate_digest = row["per_ticker_additional_predictive_evidence_execution_candidate_digest"]
        review_digest = row["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"]
        assert len(candidate_digest) == 64
        assert len(review_digest) == 64
        assert review_digest == review_service.per_ticker_additional_predictive_evidence_execution_candidate_review_digest_v1(row)


def test_next_chain_gates_and_risk_controls_are_reviewed(review_package: dict) -> None:
    assert review_package["next_chain"] == candidate_service.NEXT_CHAIN
    assert review_package["next_gates"] == candidate_service.NEXT_GATES
    assert review_package["risk_controls"] == candidate_service.RISK_CONTROLS


def test_review_checklist_passes(review_package: dict) -> None:
    assert len(review_service.REQUIRED_CHECK_IDS) == 84
    assert [row["check_id"] for row in review_package["review_checklist"]] == review_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review_package["review_checklist"])
    assert review_package["review_summary"]["total_checks"] == 84
    assert review_package["review_summary"]["passed_checks"] == 84
    assert review_package["review_summary"]["blocker_count"] == 0
    assert review_package["review_summary"]["ready_for_additional_predictive_evidence_execution_approval"] is False


def test_review_digest_is_deterministic(review_package: dict) -> None:
    assert review_package["additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest"] == review_service.additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest_v1(review_package)


def test_validator_accepts_valid_review(review_package: dict) -> None:
    result = review_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(review_package)
    assert result["status"] == review_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_REVIEW_PACKAGE_VALID
    assert result["blocker_count"] == 0
    assert result["ready_for_additional_predictive_evidence_execution_approval"] is False


@pytest.mark.parametrize(("field", "value"), [
    ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("source_candidate_digest", "0" * 64),
    ("source_candidate_status", "WRONG"), ("source_candidate_blocker_count", 1),
    ("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest", None),
    ("improved_evidence_planning_results_review_using_redesigned_evidence_digest", None),
    ("records_digest", None), ("target_universe", ["AAPL"]), ("target_universe_count", 11),
    ("meta_record_count", 1003), ("source_results_review_ready", False),
    ("ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence", False),
    ("additional_predictive_evidence_execution_candidate_created", False),
    ("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created", False),
    ("additional_predictive_evidence_execution_approved", True),
    ("additional_predictive_evidence_execution_authorized", True),
    ("additional_predictive_evidence_executed", True),
    ("additional_predictive_evidence_results_created", True), ("label_regeneration_performed", True),
    ("new_targets_created", True), ("target_definition_change_authorized", True),
    ("feature_generation_performed", True), ("feature_label_matrix_created", True),
    ("metric_recomputation_performed_in_review", True), ("model_training_performed_in_review", True),
    ("predictive_usefulness", "accepted"), ("predictive_usefulness_acceptance_ready", True),
    ("predictive_usefulness_acceptance_candidate_created", True), ("profitability", "accepted"),
    ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True), ("predictive_evidence_execution_rerun_performed", True),
])
def test_validator_rejects_forbidden_or_changed_fields(review_package: dict, field: str, value) -> None:
    changed = deepcopy(review_package)
    changed[field] = value
    with pytest.raises(review_service.AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError):
        review_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(changed)


@pytest.mark.parametrize("field", [
    "reviewed_candidate_basis", "reviewed_planned_source_inputs",
    "reviewed_planned_execution_activities", "reviewed_label_feature_matrix_boundaries",
    "reviewed_planned_model_and_baseline_families", "reviewed_planned_metric_families",
    "next_chain", "risk_controls",
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest",
])
def test_validator_rejects_missing_required_structures(review_package: dict, field: str) -> None:
    changed = deepcopy(review_package)
    changed.pop(field)
    with pytest.raises(review_service.AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError):
        review_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(changed)


@pytest.mark.parametrize("digest_field", [
    "per_ticker_additional_predictive_evidence_execution_candidate_digest",
    "per_ticker_additional_predictive_evidence_execution_candidate_review_digest",
])
def test_validator_rejects_missing_per_ticker_digest(review_package: dict, digest_field: str) -> None:
    changed = deepcopy(review_package)
    changed["per_ticker_review_entries"][0].pop(digest_field)
    with pytest.raises(review_service.AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError):
        review_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(changed)


def test_markdown_includes_all_required_sections(review_package: dict) -> None:
    markdown = review_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_markdown_v1(review_package)
    for section in (
        "## Title", "## Optional Additional Predictive Evidence Execution Candidate Review Using Improved Evidence",
        "## Reviewed Candidate", "## Source Improved Evidence Planning Results Review", "## Bound Evidence",
        "## Dataset and Universe", "## Reviewed Candidate Basis", "## Reviewed Candidate Objective",
        "## Reviewed Planned Source Inputs", "## Reviewed Planned Execution Activities",
        "## Reviewed Label / Feature / Matrix Boundaries", "## Reviewed Planned Model and Baseline Families",
        "## Reviewed Planned Metric Families", "## Reviewed Planned Future Outputs",
        "## Per-Ticker Review Entries", "## Next Chain", "## Next Gates", "## Risk Controls",
        "## Predictive Usefulness Boundary", "## Profitability Boundary", "## Runtime Boundary",
        "## Checklist Summary", "## Guardrails",
    ):
        assert section in markdown


def test_public_exports_are_available() -> None:
    assert services.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1 is review_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1
    assert services.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1 is review_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1


def test_writer_is_no_overwrite_and_uses_temporary_directory(tmp_path) -> None:
    result = review_service.write_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(tmp_path)
    assert result["payload_byte_size"] > 0
    assert len(result["payload_sha256"]) == 64
    with pytest.raises(review_service.AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceOperatorReviewError):
        review_service.write_additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_v1(tmp_path)
