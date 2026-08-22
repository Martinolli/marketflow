"""Offline candidate for future predictive-evidence execution using improved evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import improved_evidence_planning_results_review_redesigned_evidence_service as source_review


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_V1 = (
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_READY_FOR_OPERATOR_REVIEW = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_VALID = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_VALID"
)

DEFAULT_BRANCH = "feature/additional-predictive-evidence-execution-candidate-improved-evidence-v1"
DEFAULT_BASE_COMMIT = "639b65286db6385204e7b1f5a62f543bd2c2a334"
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = "8f316cceeb2a9303d8d448fcf70cec249ab4d11876acad893b386f89b118a379"
BOUND_DIGESTS = {
    "improved_evidence_planning_results_review_using_redesigned_evidence_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
    **source_review._source_evidence(),
}
TARGET_UNIVERSE = list(source_review.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(source_review.EXPECTED_RECORD_COUNTS)
SELECTED_DIRECTION = source_review.SELECTED_DIRECTION
NOT_ACCEPTED = source_review.NOT_ACCEPTED
NOT_AUTHORIZED = source_review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
PLANNED_NOT_EVALUATED = "PLANNED_NOT_EVALUATED"
PLANNED_NOT_COMPUTED = "PLANNED_NOT_COMPUTED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

CANDIDATE_OBJECTIVE = (
    "PREPARE_OPTIONAL_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_IMPROVED_EVIDENCE_PLAN"
)
CANDIDATE_SCOPE = "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
CANDIDATE_MODE = PLANNED_NOT_EXECUTED
CANDIDATE_AUTHORITY_STATUS = NOT_AUTHORIZED

PLANNED_SOURCE_INPUT_IDS = [
    "SOURCE_INPUT_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW",
    "SOURCE_INPUT_IMPROVED_EVIDENCE_PLANNING_EXECUTION_OUTPUTS",
    "SOURCE_INPUT_SELECTED_NO_TRADE_ABSTAIN_REDESIGN_DIRECTION",
    "SOURCE_INPUT_PROPOSED_LABEL_SCHEMA_PLAN",
    "SOURCE_INPUT_NO_TRADE_ABSTAIN_COVERAGE_PLAN",
    "SOURCE_INPUT_MATERIAL_MOVE_THRESHOLD_PLAN",
    "SOURCE_INPUT_HORIZON_SPECIFIC_VALIDATION_PLAN",
    "SOURCE_INPUT_TICKER_REGIME_SPLIT_VALIDATION_PLAN",
    "SOURCE_INPUT_FEATURE_LABEL_ALIGNMENT_PLAN",
    "SOURCE_INPUT_CHRONOLOGICAL_SPLIT_EMBARGO_PLAN",
    "SOURCE_INPUT_BASELINE_MODEL_COMPARISON_PLAN",
    "SOURCE_INPUT_CALIBRATION_BRIER_PLAN",
    "SOURCE_INPUT_LEAKAGE_NO_PEEK_CONTROL_PLAN",
    "SOURCE_INPUT_PER_TICKER_META_REPORTING_PLAN",
    "SOURCE_INPUT_CANONICAL_DATASET_AND_FROZEN_DIGESTS",
]

PLANNED_EXECUTION_ACTIVITY_IDS = [
    "ACTIVITY_VERIFY_SOURCE_DIGESTS_AND_FROZEN_INPUTS",
    "ACTIVITY_PREPARE_NO_TRADE_ABSTAIN_LABEL_SCHEMA_FOR_FUTURE_EXECUTION",
    "ACTIVITY_PREPARE_MATERIAL_MOVE_THRESHOLD_EVALUATION",
    "ACTIVITY_PREPARE_HORIZON_SPECIFIC_VALIDATION",
    "ACTIVITY_PREPARE_TICKER_REGIME_SPLIT_VALIDATION",
    "ACTIVITY_PREPARE_FEATURE_LABEL_ALIGNMENT_AND_NO_PEEK_CONTROLS",
    "ACTIVITY_PREPARE_CHRONOLOGICAL_SPLIT_AND_EMBARGO_PROFILE",
    "ACTIVITY_PREPARE_BASELINE_LOCAL_AND_CROSS_SECTIONAL_COMPARISON",
    "ACTIVITY_PREPARE_CALIBRATION_BRIER_AND_STABILITY_REVIEW",
    "ACTIVITY_PREPARE_LEAKAGE_QUALITY_AND_DIGEST_MANIFESTS",
    "ACTIVITY_PREPARE_PER_TICKER_AND_META_LIMITATION_REPORTING",
    "ACTIVITY_PREPARE_OPERATOR_RESULTS_REVIEW_SUMMARY",
]

MODEL_FAMILY_IDS = [
    "MODEL_FAMILY_MAJORITY_BASELINE",
    "MODEL_FAMILY_LOCAL_REGULARIZED_BASELINE",
    "MODEL_FAMILY_CROSS_SECTIONAL_BASELINE",
    "MODEL_FAMILY_PREVIOUS_KNOWN_DIRECTION_BASELINE",
    "MODEL_FAMILY_BUY_HOLD_REFERENCE",
    "MODEL_FAMILY_PER_TICKER_COMPARISON",
    "MODEL_FAMILY_GLOBAL_COMPARISON",
    "MODEL_FAMILY_OPTIONAL_TREE_MODEL_UNAVAILABLE_UNTIL_APPROVED",
    "MODEL_FAMILY_OPTIONAL_ENSEMBLE_MODEL_UNAVAILABLE_UNTIL_APPROVED",
]

METRIC_FAMILY_IDS = [
    "METRIC_ACCURACY", "METRIC_MACRO_PRECISION", "METRIC_MACRO_RECALL", "METRIC_MACRO_F1",
    "METRIC_CONFUSION_MATRIX", "METRIC_BRIER_SCORE", "METRIC_CALIBRATION_SUMMARY",
    "METRIC_CLASS_BALANCE_AND_COVERAGE", "METRIC_WALK_FORWARD_STABILITY",
    "METRIC_BASELINE_OUTPERFORMANCE_DELTA",
]

PLANNED_FUTURE_OUTPUT_IDS = [
    "future_additional_predictive_evidence_execution_manifest",
    "future_improved_label_schema_binding_report",
    "future_improved_feature_label_matrix_report",
    "future_walk_forward_results", "future_oos_results", "future_baseline_model_comparison",
    "future_metric_family_results", "future_calibration_stability_report",
    "future_leakage_quality_control_report", "future_per_ticker_meta_review",
    "future_operator_results_review_summary", "future_digest_manifest",
]

NEXT_CHAIN = [
    "Optional Additional Predictive Evidence Execution Candidate Operator Review Using Improved Evidence v1.",
    "Optional Additional Predictive Evidence Execution Approval Using Improved Evidence v1, if selected.",
    "Optional Additional Predictive Evidence Execution Using Improved Evidence v1, if approved.",
    "Optional Additional Predictive Evidence Results Review Using Improved Evidence v1.",
    "Predictive usefulness reassessment rerun using improved evidence, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun using improved evidence, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

NEXT_GATES = [
    "additional_predictive_evidence_execution_candidate_operator_review_using_improved_evidence",
    "additional_predictive_evidence_execution_approval_using_improved_evidence_if_selected",
    "additional_predictive_evidence_execution_using_improved_evidence_if_approved",
    "additional_predictive_evidence_results_review_using_improved_evidence",
    "predictive_usefulness_reassessment_rerun_using_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_using_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required", "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "candidate_does_not_approve_predictive_evidence_execution",
    "candidate_does_not_execute_predictive_evidence", "candidate_does_not_generate_labels",
    "candidate_does_not_create_new_targets", "candidate_does_not_authorize_target_definition_change",
    "candidate_does_not_generate_features", "candidate_does_not_create_feature_label_matrix",
    "candidate_does_not_recompute_metrics", "candidate_does_not_train_models",
    "candidate_does_not_accept_predictive_usefulness", "candidate_does_not_create_acceptance_candidate",
    "candidate_does_not_accept_profitability", "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy", "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution", "candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset", "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs", "do_not_mutate_predictive_evidence_outputs",
    "do_not_mutate_label_objective_review_outputs", "do_not_mutate_label_objective_redesign_outputs",
    "do_not_mutate_improved_evidence_planning_outputs", "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

CANDIDATE_BASIS = {
    "source_results_review_ready": True,
    "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence": True,
    "results_review_classification": "COMPLETED_RESEARCH_ONLY",
    "improved_evidence_planning_classification": "COMPLETED_RESEARCH_ONLY",
    "planning_execution_scope_review": "PLANNING_EXECUTION_ONLY_NOT_EVIDENCE_EXECUTION",
    "selected_redesign_direction_review": "REVIEWED_RESEARCH_ONLY",
    "selected_redesign_direction": SELECTED_DIRECTION,
    "label_schema_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "no_trade_abstain_coverage_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "material_move_threshold_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "horizon_specific_validation_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "ticker_regime_split_validation_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "feature_label_alignment_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "chronological_split_embargo_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "baseline_model_comparison_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "calibration_brier_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "leakage_no_peek_control_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "per_ticker_meta_reporting_plan_review": "REVIEWED_REQUIRES_OPERATOR_SELECTION",
    "additional_predictive_evidence_candidate_readiness": "OPTIONAL_FUTURE_CANDIDATE_REQUIRES_OPERATOR_SELECTION",
    "planning_decision_review": "NO_LABEL_GENERATION_FEATURE_GENERATION_MATRIX_CREATION_OR_PREDICTIVE_EXECUTION_AUTHORIZED",
}


class AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(ValueError):
    """Raised when the candidate violates its candidate-only authority boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(f"{field} mismatch")


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": expected, "actual": actual,
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _planned_source_inputs() -> list[dict[str, Any]]:
    return [{"source_input_id": source_input_id, "source_input_status": "SOURCE_REVIEWED_NOT_REGENERATED",
             "execution_authorized": False, "research_only": True, "non_actionable": True}
            for source_input_id in PLANNED_SOURCE_INPUT_IDS]


def _planned_execution_activities() -> list[dict[str, Any]]:
    return [{"activity_id": activity_id, "activity_status": PLANNED_NOT_EXECUTED,
             "approval_required_before_execution": True, "execution_authorized": False,
             "execution_performed": False, "label_generation_authorized": False,
             "feature_generation_authorized": False, "feature_label_matrix_creation_authorized": False,
             "metric_computation_authorized": False, "model_training_authorized": False,
             "research_only": True, "non_actionable": True}
            for activity_id in PLANNED_EXECUTION_ACTIVITY_IDS]


def _planned_model_families() -> list[dict[str, Any]]:
    return [{"model_family_id": model_family_id, "model_family_status": PLANNED_NOT_EVALUATED,
             "training_authorized": False, "training_performed": False,
             "metric_computation_authorized": False, "research_only": True, "non_actionable": True}
            for model_family_id in MODEL_FAMILY_IDS]


def _planned_metric_families() -> list[dict[str, Any]]:
    return [{"metric_family_id": metric_family_id, "metric_status": PLANNED_NOT_COMPUTED,
             "metric_computation_authorized": False, "metric_computation_performed": False,
             "research_only": True, "non_actionable": True}
            for metric_family_id in METRIC_FAMILY_IDS]


def _planned_future_outputs() -> list[dict[str, Any]]:
    return [{"future_output_id": output_id, "output_status": PLANNED_NOT_GENERATED,
             "output_label": RESEARCH_ONLY_NON_ACTIONABLE, "generated": False,
             "research_only": True, "non_actionable": True}
            for output_id in PLANNED_FUTURE_OUTPUT_IDS]


def _label_feature_matrix_boundaries() -> dict[str, Any]:
    return {
        "improved_label_schema_generation_status": PLANNED_NOT_GENERATED,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_status": PLANNED_NOT_GENERATED,
        "feature_generation_authorized": False, "feature_generation_performed": False,
        "feature_label_matrix_status": "PLANNED_NOT_CREATED", "feature_label_matrix_created": False,
    }


def per_ticker_additional_predictive_evidence_execution_candidate_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_additional_predictive_evidence_execution_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker, "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN", "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "improved_evidence_planning_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "additional_predictive_evidence_execution_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "additional_predictive_evidence_execution_approved": False,
            "additional_predictive_evidence_execution_authorized": False,
            "additional_predictive_evidence_executed": False,
            "label_regeneration_authorized": False, "label_regeneration_performed": False,
            "new_targets_created": False, "target_definition_change_authorized": False,
            "feature_generation_authorized": False, "feature_generation_performed": False,
            "feature_label_matrix_created": False, "metric_recomputation_performed_in_candidate": False,
            "model_training_performed_in_candidate": False, "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False, "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        }
        if is_meta:
            entry["candidate_note"] = (
                "PRESERVE_META_LIMITATION_IN_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE"
            )
        entry["per_ticker_additional_predictive_evidence_execution_candidate_digest"] = (
            per_ticker_additional_predictive_evidence_execution_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


CHECK_FIELD_SPECS = [
    ("improved_evidence_planning_results_review_digest_bound", EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST, "improved_evidence_planning_results_review_using_redesigned_evidence_digest"),
    ("improved_evidence_planning_execution_digest_bound", BOUND_DIGESTS["improved_evidence_planning_execution_using_redesigned_evidence_digest"], "improved_evidence_planning_execution_using_redesigned_evidence_digest"),
    ("improved_evidence_planning_output_binding_digest_bound", BOUND_DIGESTS["improved_evidence_planning_output_binding_digest"], "improved_evidence_planning_output_binding_digest"),
    ("improved_evidence_planning_approval_digest_bound", BOUND_DIGESTS["improved_evidence_planning_approval_using_redesigned_evidence_digest"], "improved_evidence_planning_approval_using_redesigned_evidence_digest"),
    ("improved_evidence_planning_candidate_review_digest_bound", BOUND_DIGESTS["improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"], "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"),
    ("improved_evidence_planning_candidate_digest_bound", BOUND_DIGESTS["improved_evidence_planning_candidate_using_redesigned_evidence_digest"], "improved_evidence_planning_candidate_using_redesigned_evidence_digest"),
    ("redesign_results_review_digest_bound", BOUND_DIGESTS["label_objective_redesign_results_review_using_redesigned_evidence_digest"], "label_objective_redesign_results_review_using_redesigned_evidence_digest"),
    ("redesign_execution_digest_bound", BOUND_DIGESTS["label_objective_redesign_execution_using_redesigned_evidence_digest"], "label_objective_redesign_execution_using_redesigned_evidence_digest"),
    ("redesign_output_binding_digest_bound", BOUND_DIGESTS["label_objective_redesign_output_binding_digest"], "label_objective_redesign_output_binding_digest"),
    ("target_definition_results_review_digest_bound", BOUND_DIGESTS["label_objective_target_definition_results_review_using_redesigned_evidence_digest"], "label_objective_target_definition_results_review_using_redesigned_evidence_digest"),
    ("target_definition_execution_digest_bound", BOUND_DIGESTS["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"),
    ("path_selection_digest_bound", BOUND_DIGESTS["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"], "method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
    ("readiness_review_digest_bound", BOUND_DIGESTS["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"], "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
    ("reassessment_digest_bound", BOUND_DIGESTS["predictive_usefulness_reassessment_using_redesigned_evidence_digest"], "predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
    ("predictive_results_review_digest_bound", BOUND_DIGESTS["additional_predictive_evidence_results_review_using_redesigned_labels_digest"], "additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
    ("predictive_execution_digest_bound", BOUND_DIGESTS["additional_predictive_evidence_execution_using_redesigned_labels_digest"], "additional_predictive_evidence_execution_using_redesigned_labels_digest"),
    ("matrix_digest_bound", BOUND_DIGESTS["feature_label_matrix_digest"], "feature_label_matrix_digest"),
    ("feature_values_digest_bound", BOUND_DIGESTS["feature_values_digest"], "feature_values_digest"),
    ("label_values_digest_bound", BOUND_DIGESTS["redesigned_label_values_digest"], "redesigned_label_values_digest"),
    ("research_registry_digest_bound", BOUND_DIGESTS["research_registry_approval_digest"], "research_registry_approval_digest"),
    ("records_digest_bound", BOUND_DIGESTS["records_digest"], "records_digest"),
    ("target_universe_12_preserved", TARGET_UNIVERSE, "target_universe"),
    ("records_digest_preserved", BOUND_DIGESTS["records_digest"], "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("source_results_review_ready_true", True, "source_results_review_ready"),
    ("ready_for_additional_predictive_evidence_candidate_true", True, "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence"),
    ("candidate_created_true", True, "additional_predictive_evidence_execution_candidate_created"),
    ("candidate_ready_true", True, "additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review"),
    ("candidate_review_created_false", False, "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created"),
    ("execution_approved_false", False, "additional_predictive_evidence_execution_approved"),
    ("execution_authorized_false", False, "additional_predictive_evidence_execution_authorized"),
    ("execution_performed_false", False, "additional_predictive_evidence_executed"),
    ("results_created_false", False, "additional_predictive_evidence_results_created"),
    ("selected_redesign_direction_preserved", SELECTED_DIRECTION, "selected_redesign_direction"),
    ("label_regeneration_authorized_false", False, "label_regeneration_authorized"),
    ("label_regeneration_performed_false", False, "label_regeneration_performed"),
    ("new_targets_created_false", False, "new_targets_created"),
    ("target_definition_change_authorized_false", False, "target_definition_change_authorized"),
    ("target_definition_change_performed_false", False, "target_definition_change_performed"),
    ("feature_generation_authorized_false", False, "feature_generation_authorized"),
    ("feature_generation_performed_false", False, "feature_generation_performed"),
    ("feature_label_matrix_created_false", False, "feature_label_matrix_created"),
    ("metric_recomputation_in_candidate_false", False, "metric_recomputation_performed_in_candidate"),
    ("model_training_in_candidate_false", False, "model_training_performed_in_candidate"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("acceptance_ready_false", False, "predictive_usefulness_acceptance_ready"),
    ("acceptance_candidate_created_false", False, "predictive_usefulness_acceptance_candidate_created"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("broker_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("trade_recommendations_false", False, "trade_recommendations_generated"),
    ("candidate_basis_preserved", CANDIDATE_BASIS, "candidate_basis"),
    ("candidate_objective_defined", CANDIDATE_OBJECTIVE, "additional_predictive_evidence_execution_candidate_objective"),
    ("planned_source_inputs_defined", True, "planned_source_inputs_valid"),
    ("planned_execution_activities_defined", True, "planned_execution_activities_valid"),
    ("label_feature_matrix_boundaries_defined", _label_feature_matrix_boundaries(), "label_feature_matrix_boundaries"),
    ("model_families_planned_not_evaluated", True, "model_families_valid"),
    ("metric_families_planned_not_computed", True, "metric_families_valid"),
    ("future_outputs_not_generated", True, "future_outputs_valid"),
    ("per_ticker_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_digests_present", True, "per_ticker_digests_valid"),
    ("provider_requests_made_false", False, "provider_requests_made_in_candidate"),
    ("market_data_acquisition_false", False, "market_data_acquisition_performed_in_candidate"),
    ("dataset_regeneration_false", False, "canonical_dataset_regenerated_in_candidate"),
    ("redesigned_label_regeneration_false", False, "redesigned_label_regeneration_performed"),
    ("feature_regeneration_false", False, "feature_regeneration_performed"),
    ("predictive_evidence_rerun_false", False, "predictive_evidence_execution_rerun_performed"),
    ("improved_evidence_planning_execution_rerun_false", False, "improved_evidence_planning_execution_rerun_performed"),
    ("raw_provider_payloads_not_committed", False, "raw_provider_payloads_committed"),
    ("api_keys_not_stored_or_printed", False, "api_keys_stored_or_printed"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("next_chain_defined", NEXT_CHAIN, "next_chain"),
    ("next_gates_defined", NEXT_GATES, "next_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [row[0] for row in CHECK_FIELD_SPECS]


def _derived_fields(candidate: Mapping[str, Any]) -> dict[str, Any]:
    source_inputs = candidate.get("planned_source_inputs", [])
    activities = candidate.get("planned_execution_activities", [])
    models = candidate.get("planned_model_and_baseline_families", [])
    metrics = candidate.get("planned_metric_families", [])
    outputs = candidate.get("planned_future_outputs", [])
    entries = candidate.get("per_ticker_candidate_entries", [])
    return {
        **candidate,
        "planned_source_inputs_valid": source_inputs == _planned_source_inputs(),
        "planned_execution_activities_valid": activities == _planned_execution_activities(),
        "model_families_valid": models == _planned_model_families(),
        "metric_families_valid": metrics == _planned_metric_families(),
        "future_outputs_valid": outputs == _planned_future_outputs(),
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_digests_valid": (
            isinstance(entries, list) and len(entries) == 12 and all(
                isinstance(row.get("per_ticker_additional_predictive_evidence_execution_candidate_digest"), str)
                and len(row["per_ticker_additional_predictive_evidence_execution_candidate_digest"]) == 64
                and row["per_ticker_additional_predictive_evidence_execution_candidate_digest"]
                == per_ticker_additional_predictive_evidence_execution_candidate_digest_v1(row)
                for row in entries
            )
        ),
    }


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    fields = _derived_fields(candidate)
    return [_check(check_id, expected, fields.get(field))
            for check_id, expected, field in CHECK_FIELD_SPECS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "additional_predictive_evidence_execution_candidate_ready": not failed,
        "ready_for_operator_review": not failed, "selected_redesign_direction": SELECTED_DIRECTION,
        "additional_predictive_evidence_execution_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False, "feature_generation_performed": False,
        "feature_label_matrix_created": False, "metric_recomputation_performed": False,
        "model_training_performed": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_V1,
        "candidate_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "branch": DEFAULT_BRANCH, "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "source_results_review_artifact_kind": source_review.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE,
        "source_results_review_status": source_review.IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        **BOUND_DIGESTS,
        "improved_evidence_planning_executed": True, "improved_evidence_planning_results_created": True,
        "improved_evidence_planning_results_review_created": True,
        "improved_evidence_planning_results_review_ready": True, "source_results_review_ready": True,
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence": True,
        "additional_predictive_evidence_execution_candidate_created": True,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_created": True,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created": False,
        "additional_predictive_evidence_execution_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False, "additional_predictive_evidence_results_created": False,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "target_definition_change_performed": False, "feature_generation_authorized": False,
        "feature_generation_performed": False, "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_candidate": False, "model_training_performed_in_candidate": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability": NOT_ACCEPTED, "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False, "profitability_acceptance_created": False,
        "runtime_migration_approved": False, "runtime_migration_active": False,
        "runtime_migration_approval_created": False, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "automatic_stitching": False,
        "new_strategy_scoring_performed": False, "trade_recommendations_generated": False,
        "provider_requests_made_in_candidate": False, "live_provider_transport_enabled_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "canonical_dataset_regenerated_in_candidate": False,
        "redesigned_label_regeneration_performed": False, "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "label_objective_target_definition_review_execution_rerun_performed": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "improved_evidence_planning_execution_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "dataset_name": "expanded_universe_canonical_dataset_v1", "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d", "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": 12,
        "total_canonical_record_count": 11946, "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "records_digest": BOUND_DIGESTS["records_digest"], "meta_record_count": 913,
        "non_meta_record_count": 1003, "meta_reduced_record_count_preserved": True,
        "candidate_basis": deepcopy(CANDIDATE_BASIS), "selected_redesign_direction": SELECTED_DIRECTION,
        "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "largest_aggregated_class": "FLAT", "largest_aggregated_class_count": 13600,
        "no_trade_count": 1540, "oos_evaluated_rows": 34848,
        "majority_accuracy": "0.58626033", "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950", "cross_sectional_delta_vs_majority": "0.00309917",
        "global_five_session_threshold": "0.026556108631",
        "benchmark_relative_threshold": "0.02058653801",
        "additional_predictive_evidence_execution_candidate_objective": CANDIDATE_OBJECTIVE,
        "additional_predictive_evidence_execution_candidate_scope": CANDIDATE_SCOPE,
        "additional_predictive_evidence_execution_candidate_mode": CANDIDATE_MODE,
        "additional_predictive_evidence_execution_candidate_authority_status": CANDIDATE_AUTHORITY_STATUS,
        "planned_source_inputs": _planned_source_inputs(),
        "planned_execution_activities": _planned_execution_activities(),
        "label_feature_matrix_boundaries": _label_feature_matrix_boundaries(),
        "planned_model_and_baseline_families": _planned_model_families(),
        "planned_metric_families": _planned_metric_families(),
        "planned_future_outputs": _planned_future_outputs(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def additional_predictive_evidence_execution_candidate_using_improved_evidence_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(candidate))
    payload.pop("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest", None)
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1() -> dict[str, Any]:
    """Build the candidate from committed review facts without executing evidence."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["additional_predictive_evidence_execution_candidate_using_improved_evidence_digest"] = (
        additional_predictive_evidence_execution_candidate_using_improved_evidence_digest_v1(candidate)
    )
    validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(candidate)
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    forbidden_artifacts = {
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED", "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE", "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED", "RUNTIME_MIGRATION_APPROVED", "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION", "TRADE_RECOMMENDATIONS",
    }
    forbidden_true = {
        "additional_predictive_evidence_execution_approved", "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "metric_recomputation_performed_in_candidate", "model_training_performed_in_candidate",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approved", "runtime_migration_active",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(
                    f"{current} must remain NOT_AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(
                    f"{current} must remain not accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Fail closed unless the artifact is exactly the candidate-only contract."""
    if not isinstance(candidate, dict):
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(
            "candidate must be a JSON object"
        )
    _expect(candidate.get("artifact_kind"),
            ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE,
            "artifact_kind")
    _expect(candidate.get("schema_version"),
            SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_V1,
            "schema_version")
    _expect(candidate.get("candidate_status"),
            ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
            "candidate_status")
    _reject_forbidden_values(candidate)
    expected = {
        **BOUND_DIGESTS,
        "source_results_review_artifact_kind": source_review.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE,
        "source_results_review_status": source_review.IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1", "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d", "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "records_digest": BOUND_DIGESTS["records_digest"], "meta_record_count": 913,
        "non_meta_record_count": 1003, "candidate_basis": CANDIDATE_BASIS,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "largest_aggregated_class": "FLAT", "largest_aggregated_class_count": 13600,
        "no_trade_count": 1540, "oos_evaluated_rows": 34848,
        "majority_accuracy": "0.58626033", "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950", "cross_sectional_delta_vs_majority": "0.00309917",
        "global_five_session_threshold": "0.026556108631",
        "benchmark_relative_threshold": "0.02058653801",
        "additional_predictive_evidence_execution_candidate_objective": CANDIDATE_OBJECTIVE,
        "additional_predictive_evidence_execution_candidate_scope": CANDIDATE_SCOPE,
        "additional_predictive_evidence_execution_candidate_mode": CANDIDATE_MODE,
        "additional_predictive_evidence_execution_candidate_authority_status": CANDIDATE_AUTHORITY_STATUS,
        "planned_source_inputs": _planned_source_inputs(),
        "planned_execution_activities": _planned_execution_activities(),
        "label_feature_matrix_boundaries": _label_feature_matrix_boundaries(),
        "planned_model_and_baseline_families": _planned_model_families(),
        "planned_metric_families": _planned_metric_families(),
        "planned_future_outputs": _planned_future_outputs(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(candidate.get(field), expected_value, field)
    true_fields = [
        "created_offline", "research_only", "operator_review_required", "improved_evidence_planning_executed",
        "improved_evidence_planning_results_created", "improved_evidence_planning_results_review_created",
        "improved_evidence_planning_results_review_ready", "source_results_review_ready",
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_created",
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    ]
    false_fields = [
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created",
        "additional_predictive_evidence_execution_approved", "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "metric_recomputation_performed_in_candidate", "model_training_performed_in_candidate",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "profitability_acceptance_created", "runtime_migration_approved", "runtime_migration_active",
        "runtime_migration_approval_created", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_candidate",
        "live_provider_transport_enabled_in_candidate", "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate", "canonical_dataset_regenerated_in_candidate",
        "redesigned_label_regeneration_performed", "feature_regeneration_performed",
        "predictive_evidence_execution_rerun_performed",
        "label_objective_target_definition_review_execution_rerun_performed",
        "label_objective_redesign_execution_rerun_performed",
        "improved_evidence_planning_execution_rerun_performed", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    ]
    for field in true_fields:
        _expect(candidate.get(field), True, field)
    for field in false_fields:
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(
            "candidate_checklist mismatch"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS,
            "candidate_checklist check ids")
    _expect(checklist, _checklist(candidate), "candidate_checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(
            "candidate_checklist must pass"
        )
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate_summary")
    digest = candidate.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(
            "missing candidate digest"
        )
    _expect(digest,
            additional_predictive_evidence_execution_candidate_using_improved_evidence_digest_v1(candidate),
            "candidate digest")
    return {
        "status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_VALID,
        "artifact_kind": candidate["artifact_kind"], "candidate_status": candidate["candidate_status"],
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest": digest,
        "per_ticker_candidate_entry_count": len(candidate["per_ticker_candidate_entries"]),
        "blocker_count": candidate["candidate_summary"]["blocker_count"],
        "ready_for_operator_review": True, "additional_predictive_evidence_execution_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_authorized": False,
    }


def build_additional_predictive_evidence_execution_candidate_using_improved_evidence_markdown_v1(
    candidate: dict,
) -> str:
    """Render the candidate without implying approval or execution authority."""
    validation = validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(candidate)
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Candidate Using Improved Evidence Status", "",
        "## Title", "- Optional Additional Predictive Evidence Execution Candidate Using Improved Evidence v1.", "",
        "## Optional Additional Predictive Evidence Execution Candidate Using Improved Evidence",
        f"- Artifact/status/digest: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}` / `{validation['additional_predictive_evidence_execution_candidate_using_improved_evidence_digest']}`.", "",
        "## Source Improved Evidence Planning Results Review",
        f"- `{candidate['source_results_review_artifact_kind']}` / `{candidate['source_results_review_status']}` / `{candidate['source_results_review_digest']}`.", "",
        "## Bound Evidence", f"- The complete 27-digest source chain is bound; records: `{candidate['records_digest']}`.", "",
        "## Dataset and Universe", f"- `{candidate['dataset_name']}` has 11,946 frozen rows across 12 ordered tickers; META remains 913.", "",
        "## Candidate Basis", f"- `{candidate['candidate_basis']}`", "",
        "## Candidate Objective", f"- `{candidate['additional_predictive_evidence_execution_candidate_objective']}` / `{candidate['additional_predictive_evidence_execution_candidate_scope']}` / `{candidate['additional_predictive_evidence_execution_candidate_mode']}`.", "",
        "## Planned Source Inputs",
    ]
    lines.extend(f"- `{row['source_input_id']}`: `{row['source_input_status']}`."
                 for row in candidate["planned_source_inputs"])
    lines.extend(["", "## Planned Execution Activities"])
    lines.extend(f"- `{row['activity_id']}`: `{row['activity_status']}`."
                 for row in candidate["planned_execution_activities"])
    lines.extend(["", "## Label / Feature / Matrix Boundaries",
                  f"- `{candidate['label_feature_matrix_boundaries']}`", "",
                  "## Planned Model and Baseline Families"])
    lines.extend(f"- `{row['model_family_id']}`: `{row['model_family_status']}`."
                 for row in candidate["planned_model_and_baseline_families"])
    lines.extend(["", "## Planned Metric Families"])
    lines.extend(f"- `{row['metric_family_id']}`: `{row['metric_status']}`."
                 for row in candidate["planned_metric_families"])
    lines.extend(["", "## Planned Future Outputs"])
    lines.extend(f"- `{row['future_output_id']}`: `{row['output_status']}`."
                 for row in candidate["planned_future_outputs"])
    lines.extend(["", "## Per-Ticker Candidate Entries",
                  "- Twelve digest-bound entries preserve registry order; META remains 913 and every other ticker 1003.",
                  "", "## Next Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(candidate["next_chain"], 1))
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in candidate["next_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend([
        "", "## Predictive Usefulness Boundary", "- Predictive usefulness remains `not accepted`.",
        "", "## Profitability Boundary", "- Profitability remains `not accepted`.",
        "", "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
        "", "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails",
        "- This research-only candidate approves and executes nothing, regenerates no labels or features, creates no targets or matrix rows, computes no metrics, trains no model, and produces no trading action.", "",
    ])
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(
    output_dir: str | Path,
) -> dict[str, Any]:
    """Write one canonical candidate JSON without overwriting."""
    candidate = build_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1()
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "additional_predictive_evidence_execution_candidate_using_improved_evidence_v1.json"
    payload = canonical_json_bytes(candidate)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError(
            "candidate output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"), "filename": path.name,
        "payload_byte_size": len(payload), "payload_sha256": sha256_bytes(payload),
        "candidate_status": candidate["candidate_status"],
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest": candidate[
            "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest"
        ],
    }
