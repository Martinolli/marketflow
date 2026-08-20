"""Offline operator review of the label-objective target-definition candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import label_objective_target_definition_review_candidate_redesigned_evidence_service as candidate_service


ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1 = (
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_v1"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "735d531f39c3eac771694b9044ed67f62c9aecbdc9ca0d5cd3e3368c45caf892"
)
EXPECTED_PATH_SELECTION_DIGEST = candidate_service.EXPECTED_PATH_SELECTION_DIGEST
EXPECTED_CANDIDATE_REVIEW_DIGEST = candidate_service.EXPECTED_CANDIDATE_REVIEW_DIGEST
EXPECTED_METHOD_EVIDENCE_CANDIDATE_DIGEST = candidate_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_READINESS_REVIEW_DIGEST = candidate_service.EXPECTED_READINESS_REVIEW_DIGEST
EXPECTED_REASSESSMENT_DIGEST = candidate_service.EXPECTED_REASSESSMENT_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = candidate_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_MATRIX_DIGEST = candidate_service.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = candidate_service.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = candidate_service.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = candidate_service.EXPECTED_RECORDS_DIGEST
EXPECTED_TARGET_UNIVERSE = list(candidate_service.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)

SOURCE_CANDIDATE_ARTIFACT_KIND = (
    candidate_service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE
)
SOURCE_CANDIDATE_STATUS = (
    candidate_service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW
)
SELECTED_OPTION = candidate_service.SELECTED_OPTION
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEW_DIMENSION_IDS = list(candidate_service.REVIEW_DIMENSION_IDS)
LABEL_FAMILY_IDS = list(candidate_service.LABEL_FAMILY_IDS)
DIAGNOSTIC_QUESTIONS = list(candidate_service.DIAGNOSTIC_QUESTIONS)
DECISION_OPTION_IDS = list(candidate_service.DECISION_OPTION_IDS)
PLANNED_OUTPUT_NAMES = list(candidate_service.PLANNED_OUTPUT_NAMES)
NEXT_CHAIN = list(candidate_service.NEXT_CHAIN)
NEXT_GATES = list(candidate_service.NEXT_GATES)
RISK_CONTROLS = list(candidate_service.RISK_CONTROLS)

REQUIRED_DIGESTS = {
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "method_evidence_improvement_path_selection_using_redesigned_evidence_digest": EXPECTED_PATH_SELECTION_DIGEST,
    "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "method_evidence_improvement_candidate_using_redesigned_evidence_digest": EXPECTED_METHOD_EVIDENCE_CANDIDATE_DIGEST,
    "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": EXPECTED_READINESS_REVIEW_DIGEST,
    "predictive_usefulness_reassessment_using_redesigned_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
    "additional_predictive_evidence_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
    "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
    "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
    "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
    "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
    "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
    "records_digest": EXPECTED_RECORDS_DIGEST,
}

CHECK_IDS = [
    "candidate_kind_matches", "candidate_status_ready_for_review", "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers", "label_objective_target_definition_review_candidate_digest_bound",
    "path_selection_digest_bound", "candidate_review_digest_bound", "readiness_review_digest_bound",
    "reassessment_digest_bound", "results_review_digest_bound", "execution_digest_bound",
    "matrix_digest_bound", "feature_values_digest_bound", "label_values_digest_bound",
    "research_registry_digest_bound", "records_digest_bound", "target_universe_12_preserved",
    "target_universe_matches_candidate_universe", "records_digest_preserved", "meta_913_preserved",
    "selected_option_is_option_a", "label_objective_target_definition_review_candidate_created_true",
    "label_objective_target_definition_review_candidate_review_created_true",
    "label_objective_target_definition_review_candidate_ready_true",
    "label_objective_target_definition_review_approved_false",
    "label_objective_target_definition_review_executed_false", "label_regeneration_false",
    "new_targets_created_false", "target_definition_change_authorized_false",
    "predictive_usefulness_not_accepted", "acceptance_ready_false", "acceptance_candidate_created_false",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "problem_basis_reviewed",
    "candidate_objective_reviewed", "review_dimensions_reviewed", "label_family_review_plan_reviewed",
    "diagnostic_questions_reviewed", "decision_options_reviewed", "planned_outputs_not_generated",
    "planned_outputs_research_only", "per_ticker_entries_12", "per_ticker_candidate_digests_present",
    "per_ticker_review_digests_present", "provider_requests_made_false", "market_data_acquisition_false",
    "dataset_regeneration_false", "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "metric_recomputation_in_review_false",
    "model_training_in_review_false", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "next_chain_reviewed", "next_gates_reviewed", "risk_controls_reviewed", "no_tracked_marketflow_files",
]


class LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(ValueError):
    """Raised when the review package violates its review-only boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
            f"{field} mismatch"
        )


def _source_candidate(candidate: dict | None) -> dict[str, Any]:
    source = (
        candidate_service.build_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    candidate_service.validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(
        source
    )
    _expect(
        source.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"),
        EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source candidate digest",
    )
    _expect(source["candidate_summary"].get("blocker_count"), 0, "source candidate blockers")
    return source


def _per_ticker_review_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_label_objective_target_definition_review_candidate_review_digest", None)
    return payload


def per_ticker_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker review entry."""
    return semantic_digest(_per_ticker_review_digest_payload(entry))


def _per_ticker_review_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for source_entry in source["per_ticker_candidate_entries"]:
        entry = deepcopy(source_entry)
        entry["label_objective_target_definition_review_candidate_review_status"] = (
            "READY_FOR_OPERATOR_ASSESSMENT"
        )
        entry["target_definition_change_authorized"] = False
        entry["new_targets_created"] = False
        entry["source_label_objective_target_definition_review_candidate_digest"] = (
            EXPECTED_SOURCE_CANDIDATE_DIGEST
        )
        entry["per_ticker_label_objective_target_definition_review_candidate_review_digest"] = (
            per_ticker_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_digest_v1(
                entry
            )
        )
        entries.append(entry)
    return entries


def _base_review_package(source: Mapping[str, Any]) -> dict[str, Any]:
    source_summary = source["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1,
        "review_status": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_candidate_artifact_kind": source["artifact_kind"],
        "source_candidate_status": source["candidate_status"],
        "source_candidate_digest": source["label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"],
        "source_candidate_checklist_total": source_summary["total_checks"],
        "source_candidate_checklist_passed": source_summary["passed_checks"],
        "source_candidate_checklist_failed": source_summary["failed_checks"],
        "source_candidate_blocker_count": source_summary["blocker_count"],
        **REQUIRED_DIGESTS,
        "method_evidence_improvement_path_selected": True,
        "method_evidence_improvement_path_selection_created": True,
        "selected_method_evidence_improvement_option": SELECTED_OPTION,
        "ready_for_label_objective_target_definition_review_candidate_using_redesigned_evidence": True,
        "label_objective_target_definition_review_candidate_created": True,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_created": True,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_created": True,
        "label_objective_target_definition_review_approved": False,
        "label_objective_target_definition_review_authorized": False,
        "label_objective_target_definition_review_executed": False,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "label_objective_redesign_candidate_created": False,
        "threshold_horizon_refinement_candidate_created": False,
        "improved_evidence_planning_candidate_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_migration_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "metric_recomputation_performed_in_review": False,
        "model_training_performed_in_review": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source["meta_reduced_record_count_preserved"],
        "reviewed_problem_basis": deepcopy(source["problem_basis"]),
        "reviewed_label_objective_target_definition_review_objective": source["label_objective_target_definition_review_objective"],
        "reviewed_label_objective_target_definition_review_scope": source["label_objective_target_definition_review_scope"],
        "reviewed_label_objective_target_definition_review_mode": source["label_objective_target_definition_review_mode"],
        "reviewed_label_objective_target_definition_review_authority_status": source["label_objective_target_definition_review_authority_status"],
        "reviewed_dimensions": deepcopy(source["review_dimensions"]),
        "reviewed_label_family_review_plan": deepcopy(source["current_label_family_review_plan"]),
        "reviewed_diagnostic_questions": deepcopy(source["diagnostic_questions"]),
        "reviewed_decision_options": deepcopy(source["decision_options_for_future_review"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
        "per_ticker_review_entries": _per_ticker_review_entries(source),
        "next_chain": deepcopy(source["next_chain"]),
        "next_gates": deepcopy(source["next_gates"]),
        "risk_controls": deepcopy(source["risk_controls"]),
        "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    dimensions = review.get("reviewed_dimensions", [])
    families = review.get("reviewed_label_family_review_plan", [])
    questions = review.get("reviewed_diagnostic_questions", [])
    options = review.get("reviewed_decision_options", [])
    outputs = review.get("reviewed_planned_outputs", [])
    entries = review.get("per_ticker_review_entries", [])
    expected_source = _source_candidate(None)
    actuals = {
        "candidate_kind_matches": review.get("source_candidate_artifact_kind"),
        "candidate_status_ready_for_review": review.get("source_candidate_status"),
        "candidate_digest_matches_expected": review.get("source_candidate_digest"),
        "candidate_checklist_zero_blockers": review.get("source_candidate_blocker_count"),
        "label_objective_target_definition_review_candidate_digest_bound": review.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"),
        "path_selection_digest_bound": review.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
        "candidate_review_digest_bound": review.get("method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"),
        "readiness_review_digest_bound": review.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
        "reassessment_digest_bound": review.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
        "results_review_digest_bound": review.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "execution_digest_bound": review.get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": review.get("feature_label_matrix_digest"),
        "feature_values_digest_bound": review.get("feature_values_digest"),
        "label_values_digest_bound": review.get("redesigned_label_values_digest"),
        "research_registry_digest_bound": review.get("research_registry_approval_digest"),
        "records_digest_bound": review.get("records_digest"),
        "target_universe_12_preserved": review.get("target_universe_count"),
        "target_universe_matches_candidate_universe": review.get("target_universe"),
        "records_digest_preserved": review.get("records_digest"),
        "meta_913_preserved": review.get("meta_record_count"),
        "selected_option_is_option_a": review.get("selected_method_evidence_improvement_option"),
        "label_objective_target_definition_review_candidate_created_true": review.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_created"),
        "label_objective_target_definition_review_candidate_review_created_true": review.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_review_created"),
        "label_objective_target_definition_review_candidate_ready_true": review.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_ready_for_operator_review"),
        "label_objective_target_definition_review_approved_false": review.get("label_objective_target_definition_review_approved"),
        "label_objective_target_definition_review_executed_false": review.get("label_objective_target_definition_review_executed"),
        "label_regeneration_false": review.get("label_regeneration_performed"),
        "new_targets_created_false": review.get("new_targets_created"),
        "target_definition_change_authorized_false": review.get("target_definition_change_authorized"),
        "predictive_usefulness_not_accepted": review.get("predictive_usefulness"),
        "acceptance_ready_false": review.get("predictive_usefulness_acceptance_ready"),
        "acceptance_candidate_created_false": review.get("predictive_usefulness_acceptance_candidate_created"),
        "profitability_not_accepted": review.get("profitability"),
        "runtime_not_authorized": review.get("runtime_use"),
        "strategy_not_authorized": review.get("strategy_use"),
        "broker_not_authorized": review.get("broker_execution"),
        "trade_recommendations_false": review.get("trade_recommendations_generated"),
        "problem_basis_reviewed": review.get("reviewed_problem_basis"),
        "candidate_objective_reviewed": [review.get("reviewed_label_objective_target_definition_review_objective"), review.get("reviewed_label_objective_target_definition_review_scope"), review.get("reviewed_label_objective_target_definition_review_mode"), review.get("reviewed_label_objective_target_definition_review_authority_status")],
        "review_dimensions_reviewed": [row.get("dimension_id") for row in dimensions],
        "label_family_review_plan_reviewed": [row.get("label_family") for row in families],
        "diagnostic_questions_reviewed": [row.get("question") for row in questions],
        "decision_options_reviewed": [row.get("decision_option") for row in options],
        "planned_outputs_not_generated": all(row.get("output_status") == "PLANNED_NOT_GENERATED" for row in outputs) and bool(outputs),
        "planned_outputs_research_only": all(row.get("output_label") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for row in outputs) and bool(outputs),
        "per_ticker_entries_12": len(entries),
        "per_ticker_candidate_digests_present": all(isinstance(row.get("per_ticker_label_objective_target_definition_review_candidate_digest"), str) and len(row["per_ticker_label_objective_target_definition_review_candidate_digest"]) == 64 for row in entries),
        "per_ticker_review_digests_present": all(isinstance(row.get("per_ticker_label_objective_target_definition_review_candidate_review_digest"), str) and len(row["per_ticker_label_objective_target_definition_review_candidate_review_digest"]) == 64 for row in entries),
        "provider_requests_made_false": review.get("provider_requests_made_in_review"),
        "market_data_acquisition_false": review.get("market_data_acquisition_performed_in_review"),
        "dataset_regeneration_false": review.get("canonical_dataset_regenerated_in_review"),
        "redesigned_label_regeneration_false": review.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": review.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": review.get("predictive_evidence_execution_rerun_performed"),
        "metric_recomputation_in_review_false": review.get("metric_recomputation_performed_in_review"),
        "model_training_in_review_false": review.get("model_training_performed_in_review"),
        "no_predictive_usefulness_acceptance_artifact_created": review.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": review.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": review.get("runtime_migration_approval_created"),
        "next_chain_reviewed": review.get("next_chain"),
        "next_gates_reviewed": review.get("next_gates"),
        "risk_controls_reviewed": review.get("risk_controls"),
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files"),
    }
    expected = {
        "candidate_kind_matches": SOURCE_CANDIDATE_ARTIFACT_KIND,
        "candidate_status_ready_for_review": SOURCE_CANDIDATE_STATUS,
        "candidate_digest_matches_expected": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "candidate_checklist_zero_blockers": 0,
        "label_objective_target_definition_review_candidate_digest_bound": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "path_selection_digest_bound": EXPECTED_PATH_SELECTION_DIGEST,
        "candidate_review_digest_bound": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "readiness_review_digest_bound": EXPECTED_READINESS_REVIEW_DIGEST,
        "reassessment_digest_bound": EXPECTED_REASSESSMENT_DIGEST,
        "results_review_digest_bound": EXPECTED_RESULTS_REVIEW_DIGEST,
        "execution_digest_bound": EXPECTED_EXECUTION_DIGEST,
        "matrix_digest_bound": EXPECTED_MATRIX_DIGEST,
        "feature_values_digest_bound": EXPECTED_FEATURE_VALUES_DIGEST,
        "label_values_digest_bound": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_digest_bound": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest_bound": EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": 12,
        "target_universe_matches_candidate_universe": EXPECTED_TARGET_UNIVERSE,
        "records_digest_preserved": EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": 913,
        "selected_option_is_option_a": SELECTED_OPTION,
        "label_objective_target_definition_review_candidate_created_true": True,
        "label_objective_target_definition_review_candidate_review_created_true": True,
        "label_objective_target_definition_review_candidate_ready_true": True,
        "label_objective_target_definition_review_approved_false": False,
        "label_objective_target_definition_review_executed_false": False,
        "label_regeneration_false": False,
        "new_targets_created_false": False,
        "target_definition_change_authorized_false": False,
        "predictive_usefulness_not_accepted": NOT_ACCEPTED,
        "acceptance_ready_false": False,
        "acceptance_candidate_created_false": False,
        "profitability_not_accepted": NOT_ACCEPTED,
        "runtime_not_authorized": NOT_AUTHORIZED,
        "strategy_not_authorized": NOT_AUTHORIZED,
        "broker_not_authorized": NOT_AUTHORIZED,
        "trade_recommendations_false": False,
        "problem_basis_reviewed": expected_source["problem_basis"],
        "candidate_objective_reviewed": [candidate_service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_OBJECTIVE, candidate_service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_SCOPE, candidate_service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_MODE, candidate_service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_AUTHORITY_STATUS],
        "review_dimensions_reviewed": REVIEW_DIMENSION_IDS,
        "label_family_review_plan_reviewed": LABEL_FAMILY_IDS,
        "diagnostic_questions_reviewed": DIAGNOSTIC_QUESTIONS,
        "decision_options_reviewed": DECISION_OPTION_IDS,
        "planned_outputs_not_generated": True,
        "planned_outputs_research_only": True,
        "per_ticker_entries_12": 12,
        "per_ticker_candidate_digests_present": True,
        "per_ticker_review_digests_present": True,
        "provider_requests_made_false": False,
        "market_data_acquisition_false": False,
        "dataset_regeneration_false": False,
        "redesigned_label_regeneration_false": False,
        "feature_regeneration_false": False,
        "predictive_evidence_rerun_false": False,
        "metric_recomputation_in_review_false": False,
        "model_training_in_review_false": False,
        "no_predictive_usefulness_acceptance_artifact_created": False,
        "no_profitability_acceptance_created": False,
        "no_runtime_migration_approval_created": False,
        "next_chain_reviewed": NEXT_CHAIN,
        "next_gates_reviewed": NEXT_GATES,
        "risk_controls_reviewed": RISK_CONTROLS,
        "no_tracked_marketflow_files": True,
    }
    return [_check(check_id, expected[check_id], actuals[check_id]) for check_id in CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    passed = sum(row.get("status") == PASS for row in rows)
    failed = len(rows) - passed
    blockers = sum(row.get("status") == FAIL and row.get("severity") == BLOCKER for row in rows)
    return {
        "total_checks": len(rows),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "ready_for_operator_assessment": True,
        "ready_for_label_objective_target_definition_review_approval": False,
        "label_objective_target_definition_review_approved": False,
        "label_objective_target_definition_review_executed": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(review))
    payload.pop("label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest", None)
    return payload


def label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest_v1(
    review_package: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for the operator review package."""
    return semantic_digest(_digest_payload(review_package))


def build_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
    candidate: dict | None = None,
) -> dict:
    """Build the review package from the validated source candidate."""
    source = _source_candidate(candidate)
    review = _base_review_package(source)
    review["review_checklist"] = _checklist(review)
    review["review_summary"] = _summary(review["review_checklist"])
    review["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"] = (
        label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest_v1(review)
    )
    validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
        review
    )
    return review


def _reject_forbidden_authority(value: Any, *, path: str = "review") -> None:
    forbidden_true_fields = {
        "label_objective_target_definition_review_approved",
        "label_objective_target_definition_review_authorized",
        "label_objective_target_definition_review_executed", "label_regeneration_authorized",
        "label_regeneration_performed", "new_targets_created", "target_definition_change_authorized",
        "label_objective_redesign_candidate_created", "threshold_horizon_refinement_candidate_created",
        "improved_evidence_planning_candidate_created",
        "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "profitability_acceptance_created", "runtime_migration_approved", "runtime_migration_active",
        "runtime_migration_approval_created", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review", "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review", "canonical_dataset_regenerated_in_review",
        "redesigned_label_regeneration_performed", "feature_regeneration_performed",
        "predictive_evidence_execution_rerun_performed", "metric_recomputation_performed_in_review",
        "model_training_performed_in_review", "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "target_definition_change_authorized", "execution_authorized", "execution_performed",
        "selected", "approved", "executed", "creates_new_labels",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
    review_package: dict,
) -> dict:
    """Validate the source binding, review structures, digests, and closed authorities."""
    if not isinstance(review_package, dict):
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
            "review package must be an object"
        )
    _reject_forbidden_authority(review_package)
    source = _source_candidate(None)
    expected_base = _base_review_package(source)
    for field, value in expected_base.items():
        _expect(review_package.get(field), value, field)
    entries = review_package.get("per_ticker_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
            "per-ticker review entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], EXPECTED_TARGET_UNIVERSE, "per-ticker order")
    for row in entries:
        ticker = row["ticker"]
        _expect(row.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(row.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        candidate_digest = row.get("per_ticker_label_objective_target_definition_review_candidate_digest")
        review_digest = row.get("per_ticker_label_objective_target_definition_review_candidate_review_digest")
        if not isinstance(candidate_digest, str) or len(candidate_digest) != 64:
            raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
                f"{ticker} candidate digest missing"
            )
        if not isinstance(review_digest, str) or len(review_digest) != 64:
            raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
                f"{ticker} review digest missing"
            )
        _expect(
            review_digest,
            per_ticker_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_digest_v1(row),
            f"{ticker} review digest",
        )
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
            "review checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], CHECK_IDS, "review checklist IDs")
    expected_checklist = _checklist(review_package)
    _expect(checklist, expected_checklist, "review checklist")
    if any(row["status"] != PASS for row in checklist):
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
            "review checklist failed"
        )
    _expect(review_package.get("review_summary"), _summary(checklist), "review summary")
    digest = review_package.get(
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
            "review digest missing"
        )
    _expect(
        digest,
        label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest_v1(
            review_package
        ),
        "review digest",
    )
    return {
        "status": "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest": digest,
        **{key: review_package["review_summary"][key] for key in (
            "total_checks", "passed_checks", "failed_checks", "blocker_count"
        )},
    }


def build_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render a sanitized Markdown view of the validated review package."""
    validation = validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    sections = [
        ("Title", ["Label Objective / Target Definition Review Candidate Review Using Redesigned Evidence"]),
        ("Label Objective / Target Definition Review Candidate Review Using Redesigned Evidence", [
            f"Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.",
            f"Digest: `{validation['label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest']}`.",
        ]),
        ("Reviewed Candidate", [
            f"Artifact/status: `{review_package['source_candidate_artifact_kind']}` / `{review_package['source_candidate_status']}`.",
            f"Digest/checks: `{review_package['source_candidate_digest']}` / `{review_package['source_candidate_checklist_passed']} of {review_package['source_candidate_checklist_total']}`.",
        ]),
        ("Source Path Selection", [f"Digest/option: `{review_package['method_evidence_improvement_path_selection_using_redesigned_evidence_digest']}` / `{review_package['selected_method_evidence_improvement_option']}`."]),
        ("Bound Evidence", [f"`{field}`: `{digest}`." for field, digest in REQUIRED_DIGESTS.items()]),
        ("Dataset and Universe", [
            f"Dataset/profile/timeframe: `{review_package['dataset_name']}` / `{review_package['source_profile']}` / `{review_package['timeframe']}`.",
            "Universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]) + ".",
            "META remains `913`; every other ticker remains `1003`.",
        ]),
        ("Reviewed Problem Basis", [f"`{key}`: `{value}`." for key, value in review_package["reviewed_problem_basis"].items()]),
        ("Reviewed Candidate Objective", [
            f"Objective: `{review_package['reviewed_label_objective_target_definition_review_objective']}`.",
            f"Scope/mode/authority: `{review_package['reviewed_label_objective_target_definition_review_scope']}` / `{review_package['reviewed_label_objective_target_definition_review_mode']}` / `{review_package['reviewed_label_objective_target_definition_review_authority_status']}`.",
        ]),
        ("Reviewed Dimensions", [f"`{row['dimension_id']}`: `{row['dimension_status']}`." for row in review_package["reviewed_dimensions"]]),
        ("Reviewed Label Family Review Plan", [f"`{row['label_family']}`: `{row['review_status']}`." for row in review_package["reviewed_label_family_review_plan"]]),
        ("Reviewed Diagnostic Questions", [f"`{row['question']}`: `{row['question_status']}`." for row in review_package["reviewed_diagnostic_questions"]]),
        ("Reviewed Decision Options", [f"`{row['decision_option']}`: `{row['decision_status']}`; selected `{row['selected']}`." for row in review_package["reviewed_decision_options"]]),
        ("Reviewed Planned Outputs", [f"`{row['output_name']}`: `{row['output_status']}` / `{row['output_label']}`." for row in review_package["reviewed_planned_outputs"]]),
        ("Per-Ticker Review Entries", [f"`{row['ticker']}`: records `{row['historical_record_count']}`, status `{row['label_objective_target_definition_review_candidate_review_status']}`, digest `{row['per_ticker_label_objective_target_definition_review_candidate_review_digest']}`." for row in review_package["per_ticker_review_entries"]]),
        ("Next Chain", review_package["next_chain"]),
        ("Next Gates", review_package["next_gates"]),
        ("Risk Controls", review_package["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate was created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{summary['total_checks']} / {summary['passed_checks']} / {summary['failed_checks']} / {summary['blocker_count']}`."]),
        ("Guardrails", ["This review package assesses the candidate only. It does not approve or execute review, regenerate labels, change targets, accept usefulness or profitability, or authorize runtime or trading."]),
    ]
    lines = ["# Label Objective / Target Definition Review Candidate Review Using Redesigned Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
        candidate
    )
    validation = validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_v1.json"
    if path.exists():
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError(
            "review output already exists"
        )
    payload = canonical_json_bytes(review)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
