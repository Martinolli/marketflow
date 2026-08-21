"""Build the offline, candidate-only label-objective redesign plan."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1 = (
    "label_objective_redesign_candidate_using_redesigned_evidence_v1"
)
LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
)
LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID"
)

SOURCE_RESULTS_REVIEW_ARTIFACT_KIND = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE"
)
SOURCE_RESULTS_REVIEW_STATUS = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY"
)
EXPECTED_RESULTS_REVIEW_DIGEST = "682907f87575b8fde514c6db17b141420bfd55781b0b77c297ba358a378aff46"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

TARGET_UNIVERSE = [
    "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
]
EXPECTED_RECORD_COUNTS = {ticker: (913 if ticker == "META" else 1003) for ticker in TARGET_UNIVERSE}

SOURCE_EVIDENCE = {
    "label_objective_target_definition_results_review_using_redesigned_evidence_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
    "label_objective_target_definition_review_execution_using_redesigned_evidence_digest": "7b5c299191abfd6aa8ef33ebed804757a2d57a6fb966ed1d51c78d1b233abe30",
    "label_objective_target_definition_review_output_binding_digest": "7efd91b24e1af35f93e37dc9bbb5e90fe03f1080f6296abe57afdbd326d0fbee",
    "label_objective_target_definition_review_approval_using_redesigned_evidence_digest": "01f667deeea9a478dca8e1f326b672ffbcedbf9c0a0b3da93d3fac1714c622db",
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest": "ebf9f1dddddc37167c457c64f28baab021b50249987e888e1ea0a31c78102d45",
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_digest": "735d531f39c3eac771694b9044ed67f62c9aecbdc9ca0d5cd3e3368c45caf892",
    "method_evidence_improvement_path_selection_using_redesigned_evidence_digest": "d56519f9eb9dbb3249a365893db080d65fee8fcccbea2a8f0839300f8d006c22",
    "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": "6c6e5019a5ce312b12e4b792ce989524ba5bf16f82b5f6e532ec742f99eba4da",
    "predictive_usefulness_reassessment_using_redesigned_evidence_digest": "32cd6e52de25584df7b54866034fbb378fad8dfe1e3f1656994dbd554d1b4985",
    "additional_predictive_evidence_results_review_using_redesigned_labels_digest": "90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed",
    "additional_predictive_evidence_execution_using_redesigned_labels_digest": "8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b",
    "feature_label_matrix_digest": "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad",
    "feature_values_digest": "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1",
    "redesigned_label_values_digest": "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f",
    "research_registry_approval_digest": "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958",
    "records_digest": "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044",
}

CANDIDATE_BASIS = {
    "results_review_classification": "COMPLETED_RESEARCH_ONLY",
    "target_decision_review": "NO_TARGET_CHANGE_AUTHORIZED",
    "redesign_or_refinement_candidate_readiness": "OPTIONAL_FUTURE_CANDIDATE_REQUIRES_OPERATOR_SELECTION",
    "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
    "largest_aggregated_class": "FLAT",
    "largest_aggregated_class_count": 13600,
    "oos_evaluated_rows": 34848,
    "majority_accuracy": "0.58626033",
    "local_model_accuracy": "0.58626033",
    "cross_sectional_accuracy": "0.58935950",
    "cross_sectional_delta_vs_majority": "0.00309917",
    "local_model_equivalence_review": "MATCHES_MAJORITY_BASELINE",
    "cross_sectional_edge_materiality_review": "SMALL_NOT_ACCEPTANCE_EVIDENCE",
    "horizon_noise_review": "REQUIRES_OPERATOR_REVIEW",
    "threshold_materiality_review": "REQUIRES_OPERATOR_REVIEW",
    "class_balance_review": "REQUIRES_OPERATOR_REVIEW",
    "per_ticker_behavior_review": "REQUIRES_OPERATOR_REVIEW",
    "meta_behavior_review": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
}

REDESIGN_THEME_IDS = [
    "REDESIGN_THEME_REDUCE_MAJORITY_CLASS_DOMINANCE",
    "REDESIGN_THEME_STRENGTHEN_TRADEABLE_SIGNAL_ALIGNMENT",
    "REDESIGN_THEME_REVIEW_FLAT_CLASS_OBJECTIVE",
    "REDESIGN_THEME_REVIEW_NO_TRADE_OR_ABSTAIN_OBJECTIVE",
    "REDESIGN_THEME_REVIEW_PER_TICKER_OR_REGIME_SPLIT_TARGET",
    "REDESIGN_THEME_REVIEW_MULTI_HORIZON_OBJECTIVE_STRUCTURE",
    "REDESIGN_THEME_REVIEW_THRESHOLD_MATERIALITY",
    "REDESIGN_THEME_REVIEW_CROSS_SECTIONAL_EDGE_REQUIREMENTS",
    "REDESIGN_THEME_REVIEW_LOCAL_MODEL_OBJECTIVE_ALIGNMENT",
    "REDESIGN_THEME_REVIEW_META_LIMITATION_EFFECT_ON_TARGETS",
    "REDESIGN_THEME_REVIEW_ACCEPTANCE_THRESHOLD_PREREQUISITES",
]
REDESIGN_OPTION_IDS = [
    "REDESIGN_OPTION_RETAIN_OBJECTIVE_AND_RAISE_ACCEPTANCE_THRESHOLD",
    "REDESIGN_OPTION_REFINE_FLAT_ZONE_DEFINITION",
    "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS",
    "REDESIGN_OPTION_SPLIT_TARGET_BY_HORIZON",
    "REDESIGN_OPTION_SPLIT_TARGET_BY_TICKER_OR_REGIME",
    "REDESIGN_OPTION_REDEFINE_TARGET_AS_MATERIAL_MOVE_ONLY",
    "REDESIGN_OPTION_REDEFINE_TARGET_AS_RISK_ADJUSTED_MOVE",
    "REDESIGN_OPTION_STOP_CURRENT_TARGET_PATH_PENDING_STRONGER_EVIDENCE",
]
RECOMMENDED_REDESIGN_DIRECTION = "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS"
RECOMMENDATION_RATIONALE = (
    "FLAT_CLASS_DOMINANCE_AND_MAJORITY_BASELINE_MATCH_SUGGEST_TARGET_STRUCTURE_MAY_NEED_"
    "ABSTAIN_OR_MATERIAL_MOVE_OBJECTIVE_BEFORE_MORE_EVIDENCE"
)

LABEL_FAMILIES = [
    "direction_with_flat_zone", "redesigned_return_buckets", "multi_horizon_5_10_20",
    "benchmark_relative_return", "volatility_adjusted_return", "drawdown_avoidance",
    "asymmetric_risk_reward", "regime_conditioned_direction", "per_ticker_calibrated_target",
    "no_trade_zone_class",
]
REDESIGN_QUESTIONS = [
    "should_flat_or_no_trade_objective_become_primary_or_filtering_target",
    "should_material_move_threshold_replace_current_direction_objective",
    "should_target_definition_require_cross_sectional_materiality",
    "should_label_objective_be_split_by_horizon",
    "should_label_objective_be_split_by_ticker_or_regime",
    "should_risk_adjusted_return_replace_raw_return_bucket_logic",
    "should_current_no_trade_zone_class_be_elevated_to_decision_layer",
    "should_targets_exclude_low_signal_or_high_noise_regions",
    "should_meta_limitation_require_separate_target_handling",
    "should_acceptance_thresholds_be_defined_before_any_new_labels",
]
PLANNED_OUTPUT_NAMES = [
    "label_objective_redesign_candidate_manifest", "flat_class_and_majority_structure_redesign_template",
    "no_trade_abstain_objective_template", "material_move_target_definition_template",
    "horizon_specific_target_design_template", "ticker_or_regime_split_target_template",
    "risk_adjusted_target_definition_template", "label_family_impact_review_template",
    "meta_target_limitation_review_template", "acceptance_threshold_prerequisite_template",
    "operator_review_summary_template",
]
NEXT_CHAIN = [
    "Optional Label Objective Redesign Candidate Operator Review Using Redesigned Evidence v1.",
    "Optional Label Objective Redesign Approval Using Redesigned Evidence v1, if selected.",
    "Optional Label Objective Redesign Execution Using Redesigned Evidence v1, if approved.",
    "Optional Label Objective Redesign Results Review Using Redesigned Evidence v1.",
    "Optional improved evidence planning candidate, if redesign results support it.",
    "Optional improved evidence execution approval and execution, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "label_objective_redesign_candidate_operator_review_using_redesigned_evidence",
    "label_objective_redesign_approval_using_redesigned_evidence_if_selected",
    "label_objective_redesign_execution_using_redesigned_evidence_if_approved",
    "label_objective_redesign_results_review_using_redesigned_evidence",
    "improved_evidence_planning_candidate_if_supported", "improved_evidence_execution_approval_if_required",
    "improved_evidence_execution_if_approved", "predictive_usefulness_reassessment_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready", "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_approve_redesign", "candidate_does_not_execute_redesign",
    "candidate_does_not_regenerate_labels", "candidate_does_not_create_new_targets",
    "candidate_does_not_authorize_target_definition_change",
    "candidate_does_not_create_threshold_horizon_refinement_candidate",
    "candidate_does_not_generate_new_evidence", "candidate_does_not_rerun_predictive_evidence",
    "candidate_does_not_retrain_models", "candidate_does_not_recompute_metrics",
    "candidate_does_not_accept_predictive_usefulness", "candidate_does_not_create_acceptance_candidate",
    "candidate_does_not_accept_profitability", "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy", "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution", "candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset", "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs", "do_not_mutate_predictive_evidence_outputs",
    "do_not_mutate_label_objective_review_outputs", "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

CHECK_IDS = [
    "results_review_digest_bound", "execution_digest_bound", "output_binding_digest_bound",
    "approval_digest_bound", "candidate_review_digest_bound", "candidate_digest_bound",
    "path_selection_digest_bound", "readiness_review_digest_bound", "reassessment_digest_bound",
    "predictive_results_review_digest_bound", "predictive_execution_digest_bound", "matrix_digest_bound",
    "feature_values_digest_bound", "label_values_digest_bound", "research_registry_digest_bound",
    "records_digest_bound", "target_universe_12_preserved", "records_digest_preserved",
    "meta_913_preserved", "results_review_ready_true",
    "ready_for_optional_redesign_or_refinement_candidate_true", "label_objective_redesign_candidate_created_true",
    "label_objective_redesign_candidate_ready_true", "label_objective_redesign_approved_false",
    "label_objective_redesign_executed_false", "label_regeneration_authorized_false",
    "label_regeneration_performed_false", "new_targets_created_false",
    "target_definition_change_authorized_false", "target_definition_change_performed_false",
    "threshold_horizon_refinement_candidate_created_false", "improved_evidence_planning_candidate_created_false",
    "predictive_usefulness_not_accepted", "acceptance_ready_false", "acceptance_candidate_created_false",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "candidate_basis_preserved",
    "candidate_objective_defined", "redesign_themes_defined", "redesign_options_defined",
    "recommended_redesign_direction_defined", "label_family_impact_review_defined",
    "redesign_questions_defined", "planned_outputs_not_generated", "planned_outputs_research_only",
    "per_ticker_entries_12", "per_ticker_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false", "redesigned_label_regeneration_false",
    "feature_regeneration_false", "predictive_evidence_rerun_false",
    "label_objective_review_execution_rerun_false", "metric_recomputation_in_candidate_false",
    "model_training_in_candidate_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]

TRUE_FIELDS = [
    "created_offline", "research_only", "operator_review_required",
    "label_objective_target_definition_review_executed",
    "label_objective_target_definition_review_results_created",
    "label_objective_target_definition_results_review_created",
    "label_objective_target_definition_results_review_ready",
    "ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence",
    "label_objective_redesign_candidate_created",
    "label_objective_redesign_candidate_using_redesigned_evidence_created",
    "label_objective_redesign_candidate_using_redesigned_evidence_ready_for_operator_review",
    "meta_reduced_record_count_preserved",
]
FALSE_FIELDS = [
    "label_objective_redesign_candidate_using_redesigned_evidence_review_created",
    "label_objective_redesign_approved", "label_objective_redesign_authorized",
    "label_objective_redesign_executed", "label_regeneration_authorized",
    "label_regeneration_performed", "new_targets_created", "target_definition_change_authorized",
    "target_definition_change_performed", "threshold_horizon_refinement_candidate_created",
    "improved_evidence_planning_candidate_created", "additional_predictive_evidence_execution_candidate_created",
    "additional_predictive_evidence_executed", "predictive_usefulness_acceptance_candidate_created",
    "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
    "profitability_acceptance_ready", "profitability_acceptance_recommended", "runtime_migration_approved",
    "runtime_migration_active", "automatic_stitching", "new_strategy_scoring_performed",
    "trade_recommendations_generated", "provider_requests_made_in_candidate",
    "live_provider_transport_enabled_in_candidate", "market_data_acquisition_performed_in_candidate",
    "dataset_generation_performed_in_candidate", "canonical_dataset_regenerated_in_candidate",
    "redesigned_label_regeneration_performed", "feature_regeneration_performed",
    "predictive_evidence_execution_rerun_performed",
    "label_objective_target_definition_review_execution_rerun_performed",
    "metric_recomputation_performed_in_candidate", "model_training_performed_in_candidate",
    "raw_provider_payloads_committed", "api_keys_stored_or_printed",
]


class LabelObjectiveRedesignCandidateRedesignedEvidenceError(ValueError):
    """Raised when the redesign candidate crosses its closed authority boundary."""


def label_objective_redesign_candidate_using_redesigned_evidence_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    clone = deepcopy(dict(candidate))
    clone.pop("label_objective_redesign_candidate_using_redesigned_evidence_digest", None)
    return semantic_digest(clone)


def per_ticker_label_objective_redesign_candidate_digest_v1(entry: Mapping[str, Any]) -> str:
    clone = deepcopy(dict(entry))
    clone.pop("per_ticker_label_objective_redesign_candidate_digest", None)
    return semantic_digest(clone)


def _check(check_id: str, passed: bool, expected: Any = True, actual: Any = True) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": "PASS" if passed else "FAIL",
        "expected": expected, "actual": actual, "severity": "BLOCKER",
        "message": f"{check_id} {'passed' if passed else 'failed'}",
    }


def _build_checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    evidence = candidate["source_evidence"]
    facts = {
        "results_review_digest_bound": evidence["label_objective_target_definition_results_review_using_redesigned_evidence_digest"] == SOURCE_EVIDENCE["label_objective_target_definition_results_review_using_redesigned_evidence_digest"],
        "execution_digest_bound": evidence["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"] == SOURCE_EVIDENCE["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"],
        "output_binding_digest_bound": evidence["label_objective_target_definition_review_output_binding_digest"] == SOURCE_EVIDENCE["label_objective_target_definition_review_output_binding_digest"],
        "approval_digest_bound": evidence["label_objective_target_definition_review_approval_using_redesigned_evidence_digest"] == SOURCE_EVIDENCE["label_objective_target_definition_review_approval_using_redesigned_evidence_digest"],
        "candidate_review_digest_bound": evidence["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"] == SOURCE_EVIDENCE["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"],
        "candidate_digest_bound": evidence["label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"] == SOURCE_EVIDENCE["label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"],
        "path_selection_digest_bound": evidence["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"] == SOURCE_EVIDENCE["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"],
        "readiness_review_digest_bound": evidence["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"] == SOURCE_EVIDENCE["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"],
        "reassessment_digest_bound": evidence["predictive_usefulness_reassessment_using_redesigned_evidence_digest"] == SOURCE_EVIDENCE["predictive_usefulness_reassessment_using_redesigned_evidence_digest"],
        "predictive_results_review_digest_bound": evidence["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] == SOURCE_EVIDENCE["additional_predictive_evidence_results_review_using_redesigned_labels_digest"],
        "predictive_execution_digest_bound": evidence["additional_predictive_evidence_execution_using_redesigned_labels_digest"] == SOURCE_EVIDENCE["additional_predictive_evidence_execution_using_redesigned_labels_digest"],
        "matrix_digest_bound": evidence["feature_label_matrix_digest"] == SOURCE_EVIDENCE["feature_label_matrix_digest"],
        "feature_values_digest_bound": evidence["feature_values_digest"] == SOURCE_EVIDENCE["feature_values_digest"],
        "label_values_digest_bound": evidence["redesigned_label_values_digest"] == SOURCE_EVIDENCE["redesigned_label_values_digest"],
        "research_registry_digest_bound": evidence["research_registry_approval_digest"] == SOURCE_EVIDENCE["research_registry_approval_digest"],
        "records_digest_bound": evidence["records_digest"] == SOURCE_EVIDENCE["records_digest"],
        "target_universe_12_preserved": candidate["target_universe"] == TARGET_UNIVERSE and candidate["target_universe_count"] == 12,
        "records_digest_preserved": candidate["records_digest"] == SOURCE_EVIDENCE["records_digest"],
        "meta_913_preserved": candidate["meta_record_count"] == 913 and candidate["meta_reduced_record_count_preserved"] is True,
        "results_review_ready_true": candidate["label_objective_target_definition_results_review_ready"] is True,
        "ready_for_optional_redesign_or_refinement_candidate_true": candidate["ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence"] is True,
        "label_objective_redesign_candidate_created_true": candidate["label_objective_redesign_candidate_created"] is True,
        "label_objective_redesign_candidate_ready_true": candidate["label_objective_redesign_candidate_using_redesigned_evidence_ready_for_operator_review"] is True,
        "label_objective_redesign_approved_false": candidate["label_objective_redesign_approved"] is False,
        "label_objective_redesign_executed_false": candidate["label_objective_redesign_executed"] is False,
        "label_regeneration_authorized_false": candidate["label_regeneration_authorized"] is False,
        "label_regeneration_performed_false": candidate["label_regeneration_performed"] is False,
        "new_targets_created_false": candidate["new_targets_created"] is False,
        "target_definition_change_authorized_false": candidate["target_definition_change_authorized"] is False,
        "target_definition_change_performed_false": candidate["target_definition_change_performed"] is False,
        "threshold_horizon_refinement_candidate_created_false": candidate["threshold_horizon_refinement_candidate_created"] is False,
        "improved_evidence_planning_candidate_created_false": candidate["improved_evidence_planning_candidate_created"] is False,
        "predictive_usefulness_not_accepted": candidate["predictive_usefulness"] == NOT_ACCEPTED,
        "acceptance_ready_false": candidate["predictive_usefulness_acceptance_ready"] is False,
        "acceptance_candidate_created_false": candidate["predictive_usefulness_acceptance_candidate_created"] is False,
        "profitability_not_accepted": candidate["profitability"] == NOT_ACCEPTED,
        "runtime_not_authorized": candidate["runtime_use"] == NOT_AUTHORIZED,
        "strategy_not_authorized": candidate["strategy_use"] == NOT_AUTHORIZED,
        "broker_not_authorized": candidate["broker_execution"] == NOT_AUTHORIZED,
        "trade_recommendations_false": candidate["trade_recommendations_generated"] is False,
        "candidate_basis_preserved": candidate["candidate_basis"] == CANDIDATE_BASIS,
        "candidate_objective_defined": candidate["label_objective_redesign_candidate_objective"] == "PREPARE_OPTIONAL_LABEL_OBJECTIVE_REDESIGN_PATH_AFTER_RESULTS_REVIEW_FOUND_MAJORITY_STRUCTURE_AND_WEAK_EDGE",
        "redesign_themes_defined": len(candidate["redesign_themes"]) == 11,
        "redesign_options_defined": len(candidate["redesign_options"]) == 8,
        "recommended_redesign_direction_defined": candidate["recommended_redesign_direction"] == RECOMMENDED_REDESIGN_DIRECTION,
        "label_family_impact_review_defined": len(candidate["current_label_family_impact_review"]) == 10,
        "redesign_questions_defined": len(candidate["planned_redesign_questions"]) == 10,
        "planned_outputs_not_generated": all(item["output_status"] == "PLANNED_NOT_GENERATED" for item in candidate["planned_outputs"]),
        "planned_outputs_research_only": all(item["output_scope"] == "RESEARCH_ONLY_NON_ACTIONABLE" for item in candidate["planned_outputs"]),
        "per_ticker_entries_12": len(candidate["per_ticker_candidate_entries"]) == 12,
        "per_ticker_digests_present": all(item.get("per_ticker_label_objective_redesign_candidate_digest") for item in candidate["per_ticker_candidate_entries"]),
        "provider_requests_made_false": candidate["provider_requests_made_in_candidate"] is False,
        "market_data_acquisition_false": candidate["market_data_acquisition_performed_in_candidate"] is False,
        "dataset_regeneration_false": candidate["canonical_dataset_regenerated_in_candidate"] is False,
        "redesigned_label_regeneration_false": candidate["redesigned_label_regeneration_performed"] is False,
        "feature_regeneration_false": candidate["feature_regeneration_performed"] is False,
        "predictive_evidence_rerun_false": candidate["predictive_evidence_execution_rerun_performed"] is False,
        "label_objective_review_execution_rerun_false": candidate["label_objective_target_definition_review_execution_rerun_performed"] is False,
        "metric_recomputation_in_candidate_false": candidate["metric_recomputation_performed_in_candidate"] is False,
        "model_training_in_candidate_false": candidate["model_training_performed_in_candidate"] is False,
        "raw_provider_payloads_not_committed": candidate["raw_provider_payloads_committed"] is False,
        "api_keys_not_stored_or_printed": candidate["api_keys_stored_or_printed"] is False,
        "no_predictive_usefulness_acceptance_artifact_created": candidate["predictive_usefulness_acceptance_candidate_created"] is False,
        "no_profitability_acceptance_created": candidate["profitability_acceptance_ready"] is False,
        "no_runtime_migration_approval_created": candidate["runtime_migration_approved"] is False,
        "next_chain_defined": candidate["next_chain"] == NEXT_CHAIN,
        "next_gates_defined": candidate["next_gates"] == NEXT_GATES,
        "risk_controls_defined": candidate["risk_controls"] == RISK_CONTROLS,
        "no_tracked_marketflow_files": candidate["no_tracked_marketflow_files"] is True,
    }
    return [_check(check_id, facts[check_id]) for check_id in CHECK_IDS]


def build_label_objective_redesign_candidate_using_redesigned_evidence_v1() -> dict[str, Any]:
    theme_common = {
        "theme_status": "PLANNED_NOT_EXECUTED", "approval_required_before_execution": True,
        "execution_authorized": False, "execution_performed": False,
        "label_regeneration_authorized": False, "target_definition_change_authorized": False,
        "research_only": True, "non_actionable": True,
    }
    option_common = {
        "option_status": "AVAILABLE_FOR_OPERATOR_REVIEW", "selected": False, "approved": False,
        "executed": False, "creates_new_labels": False, "creates_new_targets": False,
        "label_regeneration_authorized": False, "target_definition_change_authorized": False,
        "research_only": True, "non_actionable": True,
    }
    family_common = {
        "impact_review_status": "PLANNED_NOT_EXECUTED", "possible_redesign_impact": "TO_BE_REVIEWED",
        "label_regeneration_authorized": False, "target_definition_change_authorized": False,
        "research_only": True, "non_actionable": True,
    }
    question_common = {
        "question_status": "NOT_ANSWERED", "requires_separate_review_or_execution": True,
        "research_only": True, "non_actionable": True,
    }
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1,
        "candidate_status": LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "source_results_review_artifact_kind": SOURCE_RESULTS_REVIEW_ARTIFACT_KIND,
        "source_results_review_status": SOURCE_RESULTS_REVIEW_STATUS,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "dataset_name": "expanded_universe_canonical_dataset_v1", "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d", "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": SOURCE_EVIDENCE["records_digest"],
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "candidate_basis": deepcopy(CANDIDATE_BASIS),
        "label_objective_redesign_candidate_objective": "PREPARE_OPTIONAL_LABEL_OBJECTIVE_REDESIGN_PATH_AFTER_RESULTS_REVIEW_FOUND_MAJORITY_STRUCTURE_AND_WEAK_EDGE",
        "label_objective_redesign_candidate_scope": "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION",
        "label_objective_redesign_candidate_mode": "PLANNED_NOT_EXECUTED",
        "label_objective_redesign_candidate_authority_status": NOT_AUTHORIZED,
        "redesign_themes": [{"theme": item, **theme_common} for item in REDESIGN_THEME_IDS],
        "redesign_options": [{"option": item, **option_common} for item in REDESIGN_OPTION_IDS],
        "recommended_redesign_direction": RECOMMENDED_REDESIGN_DIRECTION,
        "recommended_redesign_direction_rationale": RECOMMENDATION_RATIONALE,
        "current_label_family_impact_review": [{"label_family": item, **family_common} for item in LABEL_FAMILIES],
        "planned_redesign_questions": [{"question": item, **question_common} for item in REDESIGN_QUESTIONS],
        "planned_outputs": [{"output_name": item, "output_status": "PLANNED_NOT_GENERATED", "output_scope": "RESEARCH_ONLY_NON_ACTIONABLE"} for item in PLANNED_OUTPUT_NAMES],
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
    }
    for field in TRUE_FIELDS:
        candidate[field] = True
    for field in FALSE_FIELDS:
        candidate[field] = False

    entries = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker, "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN", "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "label_objective_target_definition_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "label_objective_redesign_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
            "label_objective_redesign_approved": False, "label_objective_redesign_executed": False,
            "label_regeneration_authorized": False, "label_regeneration_performed": False,
            "new_targets_created": False, "target_definition_change_authorized": False,
            "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False, "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        }
        if ticker == "META":
            entry["candidate_note"] = "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_REDESIGN_CANDIDATE"
        entry["per_ticker_label_objective_redesign_candidate_digest"] = per_ticker_label_objective_redesign_candidate_digest_v1(entry)
        entries.append(entry)
    candidate["per_ticker_candidate_entries"] = entries
    candidate["checklist"] = _build_checklist(candidate)
    passed = sum(item["status"] == "PASS" for item in candidate["checklist"])
    candidate["summary"] = {
        "total_checks": len(candidate["checklist"]), "passed_checks": passed,
        "failed_checks": len(candidate["checklist"]) - passed,
        "blocker_count": sum(item["status"] == "FAIL" for item in candidate["checklist"]),
        "label_objective_redesign_candidate_ready": True, "ready_for_operator_review": True,
        "recommended_redesign_direction": RECOMMENDED_REDESIGN_DIRECTION,
        "label_objective_redesign_approved": False, "label_objective_redesign_executed": False,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }
    candidate["label_objective_redesign_candidate_using_redesigned_evidence_digest"] = (
        label_objective_redesign_candidate_using_redesigned_evidence_digest_v1(candidate)
    )
    validate_label_objective_redesign_candidate_using_redesigned_evidence_v1(candidate)
    return candidate


def validate_label_objective_redesign_candidate_using_redesigned_evidence_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    failures: list[str] = []
    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    require(candidate.get("artifact_kind") == ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE, "wrong artifact kind")
    require(candidate.get("candidate_status") == LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW, "wrong candidate status")
    require(candidate.get("source_results_review_digest") == EXPECTED_RESULTS_REVIEW_DIGEST, "missing or wrong results review digest")
    evidence = candidate.get("source_evidence")
    require(isinstance(evidence, dict), "missing source evidence")
    if isinstance(evidence, dict):
        for key, expected in SOURCE_EVIDENCE.items():
            require(evidence.get(key) == expected, f"missing or wrong {key}")
    require(candidate.get("records_digest") == SOURCE_EVIDENCE["records_digest"], "missing or wrong records digest")
    require(candidate.get("target_universe") == TARGET_UNIVERSE, "target universe mismatch")
    require(candidate.get("target_universe_count") == 12, "target count not 12")
    require(candidate.get("meta_record_count") == 913, "META count not 913")
    for field in TRUE_FIELDS:
        require(candidate.get(field) is True, f"{field} must be true")
    for field in FALSE_FIELDS:
        require(candidate.get(field) is False, f"{field} must be false")
    require(candidate.get("predictive_usefulness") == NOT_ACCEPTED, "predictive usefulness accepted")
    require(candidate.get("profitability") == NOT_ACCEPTED, "profitability accepted")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        require(candidate.get(field) == NOT_AUTHORIZED, f"{field} authorized")
    require(candidate.get("candidate_basis") == CANDIDATE_BASIS, "missing or changed candidate basis")
    require(candidate.get("label_objective_redesign_candidate_objective") == "PREPARE_OPTIONAL_LABEL_OBJECTIVE_REDESIGN_PATH_AFTER_RESULTS_REVIEW_FOUND_MAJORITY_STRUCTURE_AND_WEAK_EDGE", "missing or wrong candidate objective")
    require(candidate.get("label_objective_redesign_candidate_scope") == "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION", "wrong candidate scope")
    require(candidate.get("label_objective_redesign_candidate_mode") == "PLANNED_NOT_EXECUTED", "wrong candidate mode")
    require(candidate.get("label_objective_redesign_candidate_authority_status") == NOT_AUTHORIZED, "candidate authority authorized")
    require(bool(candidate.get("redesign_themes")), "missing redesign themes")
    require(bool(candidate.get("redesign_options")), "missing redesign options")
    require(bool(candidate.get("current_label_family_impact_review")), "missing label family impact review")
    require(bool(candidate.get("planned_redesign_questions")), "missing redesign questions")
    require(bool(candidate.get("next_chain")), "missing next chain")
    require(bool(candidate.get("risk_controls")), "missing risk controls")
    entries = candidate.get("per_ticker_candidate_entries")
    require(isinstance(entries, list) and len(entries) == 12, "per-ticker entries must contain 12 tickers")
    if isinstance(entries, list):
        for entry in entries:
            require(bool(entry.get("per_ticker_label_objective_redesign_candidate_digest")), "missing per-ticker digest")
            if entry.get("per_ticker_label_objective_redesign_candidate_digest"):
                require(entry["per_ticker_label_objective_redesign_candidate_digest"] == per_ticker_label_objective_redesign_candidate_digest_v1(entry), "wrong per-ticker digest")
    digest = candidate.get("label_objective_redesign_candidate_using_redesigned_evidence_digest")
    require(bool(digest), "missing candidate digest")
    if digest:
        require(digest == label_objective_redesign_candidate_using_redesigned_evidence_digest_v1(candidate), "wrong candidate digest")
    if failures:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceError("; ".join(failures))
    return {
        "validation_status": LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID,
        "failure_count": 0, "failures": [],
    }


def build_label_objective_redesign_candidate_using_redesigned_evidence_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    validate_label_objective_redesign_candidate_using_redesigned_evidence_v1(candidate)
    sections = [
        ("Optional Label Objective Redesign Candidate Using Redesigned Evidence", candidate["candidate_status"]),
        ("Source Results Review", candidate["source_results_review_digest"]),
        ("Bound Evidence", f"{len(candidate['source_evidence'])} deterministic source digests are bound."),
        ("Dataset and Universe", f"{candidate['dataset_name']}; {', '.join(candidate['target_universe'])}; META=913."),
        ("Candidate Basis", json.dumps(candidate["candidate_basis"], sort_keys=True)),
        ("Candidate Objective", f"{candidate['label_objective_redesign_candidate_objective']}; scope/mode/authority: {candidate['label_objective_redesign_candidate_scope']} / {candidate['label_objective_redesign_candidate_mode']} / {candidate['label_objective_redesign_candidate_authority_status']}."),
        ("Redesign Themes", "\n".join(f"- {item['theme']}" for item in candidate["redesign_themes"])),
        ("Redesign Options", "\n".join(f"- {item['option']} (selected: false)" for item in candidate["redesign_options"])),
        ("Current Label Family Impact Review", "\n".join(f"- {item['label_family']}: {item['impact_review_status']}" for item in candidate["current_label_family_impact_review"])),
        ("Planned Redesign Questions", "\n".join(f"- {item['question']}" for item in candidate["planned_redesign_questions"])),
        ("Planned Outputs", "\n".join(f"- {item['output_name']}: {item['output_status']}" for item in candidate["planned_outputs"])),
        ("Per-Ticker Candidate Entries", "\n".join(f"- {item['ticker']}: {item['historical_record_count']} records" for item in candidate["per_ticker_candidate_entries"])),
        ("Next Chain", "\n".join(f"{index}. {item}" for index, item in enumerate(candidate["next_chain"], 1))),
        ("Next Gates", "\n".join(f"- {item}" for item in candidate["next_gates"])),
        ("Risk Controls", "\n".join(f"- {item}" for item in candidate["risk_controls"])),
        ("Predictive Usefulness Boundary", "Predictive usefulness is not accepted."),
        ("Profitability Boundary", "Profitability is not accepted."),
        ("Runtime Boundary", "Runtime, strategy, paper trading, and broker execution are NOT_AUTHORIZED."),
        ("Checklist Summary", f"{candidate['summary']['passed_checks']}/{candidate['summary']['total_checks']} checks passed; 0 blockers."),
        ("Guardrails", "Candidate only: no approval, execution, regeneration, new target, provider, runtime, or trading action."),
    ]
    return "\n\n".join(f"{'#' if index == 0 else '##'} {title}\n\n{body}" for index, (title, body) in enumerate(sections)) + "\n"


def write_label_objective_redesign_candidate_using_redesigned_evidence_v1(
    output_dir: str | Path,
) -> dict[str, Any]:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    candidate = build_label_objective_redesign_candidate_using_redesigned_evidence_v1()
    path = root / "label_objective_redesign_candidate_using_redesigned_evidence_v1.json"
    payload = canonical_json_bytes(candidate)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise LabelObjectiveRedesignCandidateRedesignedEvidenceError(
            "refusing to overwrite label-objective redesign candidate"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "payload_sha256": sha256_bytes(payload),
        "candidate_digest": candidate["label_objective_redesign_candidate_using_redesigned_evidence_digest"],
    }
