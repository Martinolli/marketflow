"""Offline label-objective and target-definition review candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import method_evidence_improvement_path_selection_redesigned_evidence_service as selection_service


ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1 = (
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_v1"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_PATH_SELECTION_DIGEST = "d56519f9eb9dbb3249a365893db080d65fee8fcccbea2a8f0839300f8d006c22"
EXPECTED_CANDIDATE_REVIEW_DIGEST = selection_service.EXPECTED_CANDIDATE_REVIEW_DIGEST
EXPECTED_CANDIDATE_DIGEST = selection_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_READINESS_REVIEW_DIGEST = selection_service.EXPECTED_READINESS_REVIEW_DIGEST
EXPECTED_REASSESSMENT_DIGEST = selection_service.EXPECTED_REASSESSMENT_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = selection_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = selection_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_MATRIX_DIGEST = selection_service.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = selection_service.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = selection_service.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = selection_service.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = selection_service.EXPECTED_RECORDS_DIGEST
EXPECTED_TARGET_UNIVERSE = list(selection_service.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(selection_service.EXPECTED_RECORD_COUNTS)

SOURCE_PATH_SELECTION_ARTIFACT_KIND = (
    selection_service.ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE
)
SOURCE_PATH_SELECTION_SCOPE = selection_service.METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ONLY
SELECTED_OPTION = selection_service.SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION
NEXT_ARTIFACT_KIND = selection_service.NEXT_ARTIFACT_KIND
SELECTED_OPTION_RATIONALE = selection_service.SELECTED_OPTION_RATIONALE
READINESS_DECISION = selection_service.SOURCE_READINESS_DECISION
READINESS_DECISION_REASON = (
    "SMALL_CROSS_SECTIONAL_EDGE_LOCAL_MODEL_MATCHES_MAJORITY_AND_STABILITY_REQUIRES_REVIEW"
)

LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_OBJECTIVE = (
    "REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION_AFTER_NOT_READY_REDESIGNED_EVIDENCE_DECISION"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_SCOPE = "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_MODE = "PLANNED_NOT_EXECUTED"
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_AUTHORITY_STATUS = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEW_DIMENSION_IDS = [
    "LABEL_OBJECTIVE_ALIGNMENT_WITH_TRADEABLE_SIGNAL",
    "TARGET_DEFINITION_VS_MAJORITY_CLASS_STRUCTURE",
    "CROSS_SECTIONAL_EDGE_MATERIALITY",
    "LOCAL_MODEL_EQUIVALENCE_TO_MAJORITY_BASELINE",
    "HORIZON_DESIGN_AND_NOISE_REVIEW",
    "THRESHOLD_MATERIALITY_REVIEW",
    "CLASS_BALANCE_AND_TARGET_DISTRIBUTION",
    "PER_TICKER_TARGET_BEHAVIOR",
    "META_LIMITATION_TARGET_BEHAVIOR",
    "CALIBRATION_RELEVANCE_TO_TARGET_DEFINITION",
    "ACCEPTANCE_THRESHOLD_PREREQUISITE",
    "STOP_OR_CONTINUE_ACCEPTANCE_PATH_DECISION",
]
LABEL_FAMILY_IDS = [
    "direction_with_flat_zone", "redesigned_return_buckets", "multi_horizon_5_10_20",
    "benchmark_relative_return", "volatility_adjusted_return", "drawdown_avoidance",
    "asymmetric_risk_reward", "regime_conditioned_direction", "per_ticker_calibrated_target",
    "no_trade_zone_class",
]
DIAGNOSTIC_QUESTIONS = [
    "does_label_objective_reward_tradeable_signal_or_majority_class_membership",
    "does_target_definition_have_material_cross_sectional_edge",
    "does_local_model_failure_indicate_target_problem_or_feature_problem",
    "are_label_horizons_aligned_with_available_signal_decay",
    "are_thresholds_too_small_large_or_noise_sensitive",
    "does_class_balance_create_majority_baseline_dominance",
    "does_per_ticker_behavior_support_global_target_definition",
    "does_meta_limitation_bias_target_distribution_or_evaluation",
    "should_acceptance_thresholds_be_defined_before_more_evidence",
    "should_current_target_definition_be_retained_modified_or_retired",
]
DECISION_OPTION_IDS = [
    "TARGET_DECISION_RETAIN_CURRENT_LABEL_OBJECTIVE",
    "TARGET_DECISION_REFINE_THRESHOLDS_ONLY",
    "TARGET_DECISION_REFINE_HORIZONS_ONLY",
    "TARGET_DECISION_REDEFINE_LABEL_OBJECTIVE",
    "TARGET_DECISION_SPLIT_TARGET_BY_TICKER_OR_REGIME",
    "TARGET_DECISION_ADD_NO_TRADE_OR_ABSTAIN_OBJECTIVE",
    "TARGET_DECISION_STOP_ACCEPTANCE_PATH_UNTIL_STRONGER_EVIDENCE",
]
PLANNED_OUTPUT_NAMES = [
    "label_objective_target_definition_review_candidate_manifest",
    "current_label_family_objective_map_template",
    "target_definition_vs_majority_structure_template",
    "cross_sectional_edge_materiality_template",
    "horizon_noise_review_template",
    "threshold_materiality_review_template",
    "class_balance_target_distribution_template",
    "per_ticker_target_behavior_template",
    "meta_target_behavior_template",
    "target_decision_options_template",
    "operator_review_summary_template",
]
NEXT_CHAIN = [
    "Label Objective / Target Definition Review Candidate Operator Review Using Redesigned Evidence v1.",
    "Label Objective / Target Definition Review Approval v1, if selected.",
    "Label Objective / Target Definition Review Execution v1.",
    "Label Objective / Target Definition Results Review v1.",
    "Optional label objective redesign or threshold/horizon refinement candidate, if review supports it.",
    "Optional improved evidence planning and execution, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "label_objective_target_definition_review_candidate_operator_review_using_redesigned_evidence",
    "label_objective_target_definition_review_approval_if_selected",
    "label_objective_target_definition_review_execution_if_approved",
    "label_objective_target_definition_results_review",
    "label_objective_redesign_or_threshold_horizon_refinement_candidate_if_supported",
    "improved_evidence_planning_candidate_if_supported",
    "improved_evidence_execution_approval_if_required",
    "improved_evidence_execution_if_approved",
    "predictive_usefulness_reassessment_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_execute_label_objective_review",
    "candidate_does_not_approve_label_objective_review",
    "candidate_does_not_regenerate_labels",
    "candidate_does_not_create_new_targets",
    "candidate_does_not_generate_new_evidence",
    "candidate_does_not_rerun_predictive_evidence",
    "candidate_does_not_retrain_models",
    "candidate_does_not_recompute_metrics",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_create_acceptance_candidate",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy",
    "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution",
    "candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_DIGESTS = {
    "method_evidence_improvement_path_selection_using_redesigned_evidence_digest": EXPECTED_PATH_SELECTION_DIGEST,
    "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "method_evidence_improvement_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
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
    "path_selection_digest_bound", "candidate_review_digest_bound", "candidate_digest_bound",
    "readiness_review_digest_bound", "reassessment_digest_bound", "results_review_digest_bound",
    "execution_digest_bound", "matrix_digest_bound", "feature_values_digest_bound",
    "label_values_digest_bound", "research_registry_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "selected_option_is_option_a", "ready_for_label_objective_target_definition_review_candidate_true",
    "label_objective_target_definition_review_candidate_created_true",
    "label_objective_target_definition_review_candidate_ready_true",
    "label_objective_target_definition_review_approved_false",
    "label_objective_target_definition_review_executed_false", "label_regeneration_false",
    "new_targets_created_false", "predictive_usefulness_not_accepted", "acceptance_ready_false",
    "acceptance_candidate_created_false", "profitability_not_accepted", "runtime_not_authorized",
    "strategy_not_authorized", "broker_not_authorized", "trade_recommendations_false",
    "problem_basis_preserved", "candidate_objective_defined", "review_dimensions_defined",
    "label_family_review_plan_defined", "diagnostic_questions_defined", "decision_options_defined",
    "planned_outputs_not_generated", "planned_outputs_research_only", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false", "market_data_acquisition_false",
    "dataset_regeneration_false", "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "metric_recomputation_in_candidate_false",
    "model_training_in_candidate_false", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(ValueError):
    """Raised when the candidate violates its planning-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
            f"{field} mismatch"
        )


def _review_dimensions() -> list[dict[str, Any]]:
    return [{
        "dimension_id": item,
        "dimension_status": PLANNED_NOT_EXECUTED,
        "approval_required_before_execution": True,
        "execution_authorized": False,
        "execution_performed": False,
        "research_only": True,
        "non_actionable": True,
    } for item in REVIEW_DIMENSION_IDS]


def _label_family_review_plan() -> list[dict[str, Any]]:
    return [{
        "label_family": item,
        "review_status": PLANNED_NOT_EXECUTED,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "target_definition_change_authorized": False,
        "research_only": True,
        "non_actionable": True,
    } for item in LABEL_FAMILY_IDS]


def _diagnostic_questions() -> list[dict[str, Any]]:
    return [{
        "question": item,
        "question_status": "NOT_ANSWERED",
        "requires_separate_review_or_execution": True,
        "research_only": True,
        "non_actionable": True,
    } for item in DIAGNOSTIC_QUESTIONS]


def _decision_options() -> list[dict[str, Any]]:
    return [{
        "decision_option": item,
        "decision_status": "PLANNED_FOR_OPERATOR_REVIEW",
        "selected": False,
        "approved": False,
        "executed": False,
        "creates_new_labels": False,
        "research_only": True,
        "non_actionable": True,
    } for item in DECISION_OPTION_IDS]


def _planned_outputs() -> list[dict[str, Any]]:
    return [{
        "output_name": item,
        "output_status": "PLANNED_NOT_GENERATED",
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
    } for item in PLANNED_OUTPUT_NAMES]


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_label_objective_target_definition_review_candidate_digest", None)
    return payload


def per_ticker_label_objective_target_definition_review_candidate_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker candidate entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries = []
    for ticker in EXPECTED_TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "path_selection_status": "SELECTED_OPTION_A_FOR_NEXT_CANDIDATE_ONLY",
            "label_objective_target_definition_review_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
            "label_objective_target_definition_review_executed": False,
            "label_regeneration_authorized": False,
            "label_regeneration_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_path_selection_digest": EXPECTED_PATH_SELECTION_DIGEST,
        }
        if ticker == "META":
            entry["candidate_note"] = (
                "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW"
            )
        entry["per_ticker_label_objective_target_definition_review_candidate_digest"] = (
            per_ticker_label_objective_target_definition_review_candidate_using_redesigned_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1,
        "candidate_status": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_path_selection_artifact_kind": SOURCE_PATH_SELECTION_ARTIFACT_KIND,
        "source_path_selection_scope": SOURCE_PATH_SELECTION_SCOPE,
        "source_selected_option": SELECTED_OPTION,
        "source_next_artifact_kind": NEXT_ARTIFACT_KIND,
        "source_next_artifact_created": False,
        **REQUIRED_DIGESTS,
        "method_evidence_improvement_path_selected": True,
        "method_evidence_improvement_path_selection_created": True,
        "selected_method_evidence_improvement_option": SELECTED_OPTION,
        "ready_for_label_objective_target_definition_review_candidate_using_redesigned_evidence": True,
        "label_objective_target_definition_review_candidate_created": True,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_created": True,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_created": False,
        "label_objective_target_definition_review_approved": False,
        "label_objective_target_definition_review_authorized": False,
        "label_objective_target_definition_review_executed": False,
        "label_objective_redesign_candidate_created": False,
        "threshold_horizon_refinement_candidate_created": False,
        "improved_evidence_planning_candidate_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "new_targets_created": False,
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
        "provider_requests_made_in_candidate": False,
        "live_provider_transport_enabled_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "canonical_dataset_regenerated_in_candidate": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "metric_recomputation_performed_in_candidate": False,
        "model_training_performed_in_candidate": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": deepcopy(EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "problem_basis": {
            "readiness_decision": READINESS_DECISION,
            "readiness_decision_reason": READINESS_DECISION_REASON,
            "selected_option": SELECTED_OPTION,
            "selected_option_rationale": SELECTED_OPTION_RATIONALE,
            "oos_cross_sectional_delta_vs_majority": "0.00309917",
            "oos_local_model_delta_vs_majority": "0",
            "predictive_signal_readiness": "NOT_READY",
            "baseline_outperformance_readiness": "NOT_READY",
            "local_model_readiness": "NOT_READY",
            "stability_readiness": "NOT_READY",
            "calibration_readiness": "REQUIRES_OPERATOR_REVIEW",
            "optional_model_coverage_sufficiency": "FAIL_OR_NOT_MET",
        },
        "label_objective_target_definition_review_objective": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_OBJECTIVE,
        "label_objective_target_definition_review_scope": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_SCOPE,
        "label_objective_target_definition_review_mode": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_MODE,
        "label_objective_target_definition_review_authority_status": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_AUTHORITY_STATUS,
        "review_dimensions": _review_dimensions(),
        "current_label_family_review_plan": _label_family_review_plan(),
        "diagnostic_questions": _diagnostic_questions(),
        "decision_options_for_future_review": _decision_options(),
        "planned_outputs": _planned_outputs(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "next_chain": deepcopy(NEXT_CHAIN),
        "next_gates": deepcopy(NEXT_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS),
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


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    dimensions = candidate.get("review_dimensions", [])
    families = candidate.get("current_label_family_review_plan", [])
    questions = candidate.get("diagnostic_questions", [])
    options = candidate.get("decision_options_for_future_review", [])
    outputs = candidate.get("planned_outputs", [])
    entries = candidate.get("per_ticker_candidate_entries", [])
    actuals = {
        "path_selection_digest_bound": candidate.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
        "candidate_review_digest_bound": candidate.get("method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"),
        "candidate_digest_bound": candidate.get("method_evidence_improvement_candidate_using_redesigned_evidence_digest"),
        "readiness_review_digest_bound": candidate.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
        "reassessment_digest_bound": candidate.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
        "results_review_digest_bound": candidate.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "execution_digest_bound": candidate.get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": candidate.get("feature_label_matrix_digest"),
        "feature_values_digest_bound": candidate.get("feature_values_digest"),
        "label_values_digest_bound": candidate.get("redesigned_label_values_digest"),
        "research_registry_digest_bound": candidate.get("research_registry_approval_digest"),
        "records_digest_bound": candidate.get("records_digest"),
        "target_universe_12_preserved": candidate.get("target_universe_count"),
        "records_digest_preserved": candidate.get("records_digest"),
        "meta_913_preserved": candidate.get("meta_record_count"),
        "selected_option_is_option_a": candidate.get("selected_method_evidence_improvement_option"),
        "ready_for_label_objective_target_definition_review_candidate_true": candidate.get("ready_for_label_objective_target_definition_review_candidate_using_redesigned_evidence"),
        "label_objective_target_definition_review_candidate_created_true": candidate.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_created"),
        "label_objective_target_definition_review_candidate_ready_true": candidate.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_ready_for_operator_review"),
        "label_objective_target_definition_review_approved_false": candidate.get("label_objective_target_definition_review_approved"),
        "label_objective_target_definition_review_executed_false": candidate.get("label_objective_target_definition_review_executed"),
        "label_regeneration_false": candidate.get("redesigned_label_regeneration_performed"),
        "new_targets_created_false": candidate.get("new_targets_created"),
        "predictive_usefulness_not_accepted": candidate.get("predictive_usefulness"),
        "acceptance_ready_false": candidate.get("predictive_usefulness_acceptance_ready"),
        "acceptance_candidate_created_false": candidate.get("predictive_usefulness_acceptance_candidate_created"),
        "profitability_not_accepted": candidate.get("profitability"),
        "runtime_not_authorized": candidate.get("runtime_use"),
        "strategy_not_authorized": candidate.get("strategy_use"),
        "broker_not_authorized": candidate.get("broker_execution"),
        "trade_recommendations_false": candidate.get("trade_recommendations_generated"),
        "problem_basis_preserved": candidate.get("problem_basis"),
        "candidate_objective_defined": [candidate.get("label_objective_target_definition_review_objective"), candidate.get("label_objective_target_definition_review_scope"), candidate.get("label_objective_target_definition_review_mode"), candidate.get("label_objective_target_definition_review_authority_status")],
        "review_dimensions_defined": [row.get("dimension_id") for row in dimensions],
        "label_family_review_plan_defined": [row.get("label_family") for row in families],
        "diagnostic_questions_defined": [row.get("question") for row in questions],
        "decision_options_defined": [row.get("decision_option") for row in options],
        "planned_outputs_not_generated": all(row.get("output_status") == "PLANNED_NOT_GENERATED" for row in outputs) and len(outputs) == len(PLANNED_OUTPUT_NAMES),
        "planned_outputs_research_only": all(row.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE for row in outputs) and bool(outputs),
        "per_ticker_entries_12": len(entries),
        "per_ticker_digests_present": all(isinstance(row.get("per_ticker_label_objective_target_definition_review_candidate_digest"), str) and len(row["per_ticker_label_objective_target_definition_review_candidate_digest"]) == 64 for row in entries),
        "provider_requests_made_false": candidate.get("provider_requests_made_in_candidate"),
        "market_data_acquisition_false": candidate.get("market_data_acquisition_performed_in_candidate"),
        "dataset_regeneration_false": candidate.get("canonical_dataset_regenerated_in_candidate"),
        "redesigned_label_regeneration_false": candidate.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": candidate.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": candidate.get("predictive_evidence_execution_rerun_performed"),
        "metric_recomputation_in_candidate_false": candidate.get("metric_recomputation_performed_in_candidate"),
        "model_training_in_candidate_false": candidate.get("model_training_performed_in_candidate"),
        "no_predictive_usefulness_acceptance_artifact_created": candidate.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": candidate.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": candidate.get("runtime_migration_approval_created"),
        "next_chain_defined": candidate.get("next_chain"),
        "next_gates_defined": candidate.get("next_gates"),
        "risk_controls_defined": candidate.get("risk_controls"),
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files"),
    }
    expected_base = _base_candidate()
    expected = {
        "path_selection_digest_bound": EXPECTED_PATH_SELECTION_DIGEST,
        "candidate_review_digest_bound": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "candidate_digest_bound": EXPECTED_CANDIDATE_DIGEST,
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
        "records_digest_preserved": EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": 913,
        "selected_option_is_option_a": SELECTED_OPTION,
        "ready_for_label_objective_target_definition_review_candidate_true": True,
        "label_objective_target_definition_review_candidate_created_true": True,
        "label_objective_target_definition_review_candidate_ready_true": True,
        "label_objective_target_definition_review_approved_false": False,
        "label_objective_target_definition_review_executed_false": False,
        "label_regeneration_false": False,
        "new_targets_created_false": False,
        "predictive_usefulness_not_accepted": NOT_ACCEPTED,
        "acceptance_ready_false": False,
        "acceptance_candidate_created_false": False,
        "profitability_not_accepted": NOT_ACCEPTED,
        "runtime_not_authorized": NOT_AUTHORIZED,
        "strategy_not_authorized": NOT_AUTHORIZED,
        "broker_not_authorized": NOT_AUTHORIZED,
        "trade_recommendations_false": False,
        "problem_basis_preserved": expected_base["problem_basis"],
        "candidate_objective_defined": [LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_OBJECTIVE, LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_SCOPE, LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_MODE, LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_AUTHORITY_STATUS],
        "review_dimensions_defined": REVIEW_DIMENSION_IDS,
        "label_family_review_plan_defined": LABEL_FAMILY_IDS,
        "diagnostic_questions_defined": DIAGNOSTIC_QUESTIONS,
        "decision_options_defined": DECISION_OPTION_IDS,
        "planned_outputs_not_generated": True,
        "planned_outputs_research_only": True,
        "per_ticker_entries_12": 12,
        "per_ticker_digests_present": True,
        "provider_requests_made_false": False,
        "market_data_acquisition_false": False,
        "dataset_regeneration_false": False,
        "redesigned_label_regeneration_false": False,
        "feature_regeneration_false": False,
        "predictive_evidence_rerun_false": False,
        "metric_recomputation_in_candidate_false": False,
        "model_training_in_candidate_false": False,
        "no_predictive_usefulness_acceptance_artifact_created": False,
        "no_profitability_acceptance_created": False,
        "no_runtime_migration_approval_created": False,
        "next_chain_defined": NEXT_CHAIN,
        "next_gates_defined": NEXT_GATES,
        "risk_controls_defined": RISK_CONTROLS,
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
        "label_objective_target_definition_review_candidate_ready": True,
        "ready_for_operator_review": True,
        "selected_option": SELECTED_OPTION,
        "label_objective_target_definition_review_approved": False,
        "label_objective_target_definition_review_executed": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(candidate: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(candidate))
    payload.pop("label_objective_target_definition_review_candidate_using_redesigned_evidence_digest", None)
    return payload


def label_objective_target_definition_review_candidate_using_redesigned_evidence_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for the candidate package."""
    return semantic_digest(_digest_payload(candidate))


def build_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1() -> dict:
    """Build the offline candidate without executing review or regenerating labels."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"] = (
        label_objective_target_definition_review_candidate_using_redesigned_evidence_digest_v1(candidate)
    )
    validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(candidate)
    return candidate


def _reject_forbidden_authority(value: Any, *, path: str = "candidate") -> None:
    forbidden_true_fields = {
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_created",
        "label_objective_target_definition_review_approved",
        "label_objective_target_definition_review_authorized",
        "label_objective_target_definition_review_executed",
        "label_objective_redesign_candidate_created", "threshold_horizon_refinement_candidate_created",
        "improved_evidence_planning_candidate_created",
        "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
        "new_targets_created", "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended", "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_artifact_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "profitability_acceptance_created",
        "runtime_migration_approved", "runtime_migration_active", "runtime_migration_approval_created",
        "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_candidate", "live_provider_transport_enabled_in_candidate",
        "market_data_acquisition_performed_in_candidate", "dataset_generation_performed_in_candidate",
        "canonical_dataset_regenerated_in_candidate", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
        "metric_recomputation_performed_in_candidate", "model_training_performed_in_candidate",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed", "label_regeneration_authorized",
        "label_regeneration_performed", "target_definition_change_authorized", "execution_authorized",
        "execution_performed", "selected", "approved", "executed", "creates_new_labels",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(
    candidate: dict,
) -> dict:
    """Validate bindings, planned structures, digests, and closed authorities."""
    if not isinstance(candidate, dict):
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
            "candidate must be an object"
        )
    _reject_forbidden_authority(candidate)
    expected_base = _base_candidate()
    for field, value in expected_base.items():
        _expect(candidate.get(field), value, field)
    entries = candidate.get("per_ticker_candidate_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
            "per-ticker candidate entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], EXPECTED_TARGET_UNIVERSE, "per-ticker order")
    for row in entries:
        ticker = row["ticker"]
        _expect(row.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(row.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        digest = row.get("per_ticker_label_objective_target_definition_review_candidate_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
                f"{ticker} per-ticker digest missing"
            )
        _expect(
            digest,
            per_ticker_label_objective_target_definition_review_candidate_using_redesigned_evidence_digest_v1(row),
            f"{ticker} per-ticker digest",
        )
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
            "candidate checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], CHECK_IDS, "candidate checklist IDs")
    expected_checklist = _checklist(candidate)
    _expect(checklist, expected_checklist, "candidate checklist")
    if any(row["status"] != PASS for row in checklist):
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
            "candidate checklist failed"
        )
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate summary")
    digest = candidate.get("label_objective_target_definition_review_candidate_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
            "candidate digest missing"
        )
    _expect(
        digest,
        label_objective_target_definition_review_candidate_using_redesigned_evidence_digest_v1(candidate),
        "candidate digest",
    )
    return {
        "status": "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_digest": digest,
        **{key: candidate["candidate_summary"][key] for key in (
            "total_checks", "passed_checks", "failed_checks", "blocker_count"
        )},
    }


def build_label_objective_target_definition_review_candidate_using_redesigned_evidence_markdown_v1(
    candidate: dict,
) -> str:
    """Render a sanitized Markdown view of the validated candidate."""
    validation = validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(
        candidate
    )
    summary = candidate["candidate_summary"]
    sections = [
        ("Title", ["Label Objective / Target Definition Review Candidate Using Redesigned Evidence"]),
        ("Label Objective / Target Definition Review Candidate Using Redesigned Evidence", [
            f"Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.",
            f"Digest: `{validation['label_objective_target_definition_review_candidate_using_redesigned_evidence_digest']}`.",
        ]),
        ("Source Path Selection", [
            f"Artifact/scope: `{candidate['source_path_selection_artifact_kind']}` / `{candidate['source_path_selection_scope']}`.",
            f"Selected option: `{candidate['source_selected_option']}`; digest: `{candidate['method_evidence_improvement_path_selection_using_redesigned_evidence_digest']}`.",
        ]),
        ("Bound Evidence", [f"`{field}`: `{digest}`." for field, digest in REQUIRED_DIGESTS.items()]),
        ("Dataset and Universe", [
            f"Dataset/profile/timeframe: `{candidate['dataset_name']}` / `{candidate['source_profile']}` / `{candidate['timeframe']}`.",
            "Universe: " + ", ".join(f"`{ticker}`" for ticker in candidate["target_universe"]) + ".",
            "META remains `913`; every other ticker remains `1003`.",
        ]),
        ("Problem Basis", [f"`{key}`: `{value}`." for key, value in candidate["problem_basis"].items()]),
        ("Candidate Objective", [
            f"Objective: `{candidate['label_objective_target_definition_review_objective']}`.",
            f"Scope/mode/authority: `{candidate['label_objective_target_definition_review_scope']}` / `{candidate['label_objective_target_definition_review_mode']}` / `{candidate['label_objective_target_definition_review_authority_status']}`.",
        ]),
        ("Review Dimensions", [f"`{row['dimension_id']}`: `{row['dimension_status']}`." for row in candidate["review_dimensions"]]),
        ("Current Label Family Review Plan", [f"`{row['label_family']}`: `{row['review_status']}`." for row in candidate["current_label_family_review_plan"]]),
        ("Diagnostic Questions", [f"`{row['question']}`: `{row['question_status']}`." for row in candidate["diagnostic_questions"]]),
        ("Decision Options", [f"`{row['decision_option']}`: `{row['decision_status']}`; selected `{row['selected']}`." for row in candidate["decision_options_for_future_review"]]),
        ("Planned Outputs", [f"`{row['output_name']}`: `{row['output_status']}` / `{row['output_label']}`." for row in candidate["planned_outputs"]]),
        ("Per-Ticker Candidate Entries", [f"`{row['ticker']}`: records `{row['historical_record_count']}`, status `{row['label_objective_target_definition_review_candidate_status']}`, digest `{row['per_ticker_label_objective_target_definition_review_candidate_digest']}`." for row in candidate["per_ticker_candidate_entries"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate was created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{summary['total_checks']} / {summary['passed_checks']} / {summary['failed_checks']} / {summary['blocker_count']}`."]),
        ("Guardrails", ["This artifact creates only a review candidate. It does not approve or execute review, regenerate labels, create targets or evidence, accept usefulness or profitability, or authorize runtime or trading."]),
    ]
    lines = ["# Label Objective / Target Definition Review Candidate Using Redesigned Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1()
    validation = validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(
        candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "label_objective_target_definition_review_candidate_using_redesigned_evidence_v1.json"
    if path.exists():
        raise LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError(
            "candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
