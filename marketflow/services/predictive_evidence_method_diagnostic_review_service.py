"""Offline method diagnostic review for weak or mixed predictive evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import predictive_evidence_planning_tree_review_service as planning


ARTIFACT_KIND_PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE = (
    "PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_V1 = (
    "predictive_evidence_method_diagnostic_review_v1"
)
PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE_READY"
)

EXPECTED_PLANNING_TREE_REVIEW_DIGEST = (
    "08c16babcfc22b5c1d3dec4d992ede553fdeea22a008021bdc3978a016a8aeb8"
)
EXPECTED_LATEST_READINESS_DIGEST = planning.EXPECTED_LATEST_READINESS_DIGEST
EXPECTED_LATEST_REASSESSMENT_DIGEST = planning.EXPECTED_REFINED_REASSESSMENT_DIGEST
EXPECTED_REFINED_RESULTS_REVIEW_DIGEST = planning.EXPECTED_REFINED_RESULTS_REVIEW_DIGEST
EXPECTED_REFINED_EXECUTION_DIGEST = planning.EXPECTED_REFINED_EXECUTION_DIGEST
EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST = (
    planning.EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST
)
EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST = (
    planning.EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST
)
EXPECTED_ORIGINAL_READINESS_DIGEST = planning.EXPECTED_ORIGINAL_READINESS_DIGEST
EXPECTED_ORIGINAL_REASSESSMENT_DIGEST = planning.EXPECTED_ORIGINAL_REASSESSMENT_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    planning.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_RECORDS_DIGEST = planning.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(planning.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(planning.EXPECTED_RECORD_COUNTS)
REGISTRY_APPROVED_DATASET_METADATA = deepcopy(
    planning.REGISTRY_APPROVED_DATASET_METADATA
)
NOT_ACCEPTED = planning.NOT_ACCEPTED
NOT_AUTHORIZED = planning.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = planning.RESEARCH_ONLY_NON_ACTIONABLE

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
AVAILABLE_FOR_OPERATOR_SELECTION = "AVAILABLE_FOR_OPERATOR_SELECTION_NOT_SELECTED"
COMPLETED_BY_THIS_PACKAGE = "COMPLETED_BY_THIS_PACKAGE"
NOT_ALLOWED_CURRENTLY = "NOT_ALLOWED_CURRENTLY"
RECOMMENDED_NEXT_PATH = "OPERATOR_METHOD_PATH_SELECTION"
RECOMMENDED_IMMEDIATE_ACTION = (
    "OPERATOR_METHOD_PATH_SELECTION_BEFORE_ANY_NEW_EXECUTION"
)
RECOMMENDATION_REASON = (
    "TWO_CONSECUTIVE_READINESS_GATES_NOT_READY_AFTER_ORIGINAL_AND_REFINED_EVIDENCE"
)
ORIGINAL_READINESS_DECISION = planning.ORIGINAL_READINESS_DECISION
REFINED_READINESS_DECISION = planning.REFINED_READINESS_DECISION

DIAGNOSTIC_DOMAIN_IDS = [
    "label_objective_diagnostic",
    "label_horizon_diagnostic",
    "label_threshold_diagnostic",
    "feature_signal_diagnostic",
    "vpa_feature_diagnostic",
    "relative_strength_feature_diagnostic",
    "cross_sectional_context_diagnostic",
    "model_family_diagnostic",
    "baseline_design_diagnostic",
    "walk_forward_protocol_diagnostic",
    "oos_generalization_diagnostic",
    "calibration_stability_diagnostic",
    "class_balance_and_distribution_diagnostic",
    "sample_size_and_universe_scope_diagnostic",
    "data_quality_and_meta_limitation_diagnostic",
    "acceptance_criteria_diagnostic",
]

FAILURE_MECHANISMS = [
    "label_objective_may_not_match_tradeable_signal",
    "prediction_horizon_may_not_match_available_features",
    "thresholds_may_create_noisy_or_imbalanced_classes",
    "feature_set_may_not_capture_repeatable_signal",
    "volume_price_features_may_be_insufficient_in_daily_timeframe",
    "relative_strength_features_may_need_broader_benchmark_context",
    "cross_sectional_universe_may_be_too_small",
    "market_regime_variation_may_dominate_signal",
    "sample_window_may_be_too_short_for_stability",
    "model_family_may_be_too_simple_or_misaligned",
    "baseline_comparison_may_need_redesign",
    "acceptance_thresholds_may_need_formal_definition",
    "META_limitation_is_preserved_and_not_repaired",
]

DOMAIN_DETAILS: dict[str, tuple[str, str, str, str]] = {
    "label_objective_diagnostic": (
        "original_and_refined_label_families_with_two_not_ready_decisions",
        "The label evidence did not yield repeatable acceptance-ready signal.",
        "label_objective_may_not_match_tradeable_signal",
        "review_label_objectives_against_research_questions_without_generating_labels",
    ),
    "label_horizon_diagnostic": (
        "refined_horizon_evidence_and_low_to_mixed_oos_accuracy",
        "Available horizons did not establish stable generalization.",
        "prediction_horizon_may_not_match_available_features",
        "compare_horizon_assumptions_and_feature_information_timing_on_paper",
    ),
    "label_threshold_diagnostic": (
        "label_availability_and_class_distribution_evidence",
        "Threshold construction may contribute noise or imbalance.",
        "thresholds_may_create_noisy_or_imbalanced_classes",
        "review_threshold_rationale_and_distribution_sensitivity_without_recomputation",
    ),
    "feature_signal_diagnostic": (
        "nine_refined_feature_groups_and_weak_or_mixed_signal",
        "The expanded feature set did not establish repeatable signal.",
        "feature_set_may_not_capture_repeatable_signal",
        "map_each_feature_group_to_a_testable_market_hypothesis",
    ),
    "vpa_feature_diagnostic": (
        "daily_timeframe_volume_price_feature_evidence",
        "Daily volume-price features may lack sufficient information content.",
        "volume_price_features_may_be_insufficient_in_daily_timeframe",
        "review_volume_price_hypotheses_and_timeframe_fit_without_feature_generation",
    ),
    "relative_strength_feature_diagnostic": (
        "relative_strength_and_cross_sectional_feature_evidence",
        "Relative-strength context may be too narrow for stable discrimination.",
        "relative_strength_features_may_need_broader_benchmark_context",
        "document_candidate_benchmark_contexts_for_later_operator_selection",
    ),
    "cross_sectional_context_diagnostic": (
        "twelve_ticker_registry_and_cross_sectional_accuracy_evidence",
        "The fixed research universe may provide limited cross-sectional context.",
        "cross_sectional_universe_may_be_too_small",
        "review_universe_scope_tradeoffs_without_creating_an_expansion_candidate",
    ),
    "model_family_diagnostic": (
        "five_model_groups_seven_comparisons_and_three_unavailable_families",
        "Evaluated model families did not provide acceptance evidence.",
        "model_family_may_be_too_simple_or_misaligned",
        "review_model_assumptions_and_unavailable_family_limitations_without_training",
    ),
    "baseline_design_diagnostic": (
        "insufficient_or_mixed_refined_baseline_outperformance",
        "Current baseline definitions do not support a consistent uplift conclusion.",
        "baseline_comparison_may_need_redesign",
        "review_baseline_relevance_and_precommit_comparison_rules",
    ),
    "walk_forward_protocol_diagnostic": (
        "four_folds_chronological_splits_embargo_and_no_lookahead",
        "Leakage controls passed, but fold stability did not establish readiness.",
        "market_regime_variation_may_dominate_signal",
        "review_fold_regime_coverage_and_stability_criteria_without_rerunning",
    ),
    "oos_generalization_diagnostic": (
        "refined_oos_accuracy_range_0.119813_to_0.480924",
        "Out-of-sample results are low to mixed and below acceptance readiness.",
        "sample_window_may_be_too_short_for_stability",
        "review_temporal_coverage_and_generalization_assumptions",
    ),
    "calibration_stability_diagnostic": (
        "original_brier_score_and_refined_calibration_not_acceptance_evidence",
        "Calibration and stability evidence is insufficient for acceptance.",
        "market_regime_variation_may_dominate_signal",
        "define_calibration_and_stability_questions_before_any_future_execution",
    ),
    "class_balance_and_distribution_diagnostic": (
        "label_availability_thresholds_and_oos_distribution_evidence",
        "Class balance and distribution shifts may affect reported accuracy.",
        "thresholds_may_create_noisy_or_imbalanced_classes",
        "review_class_distribution_reporting_requirements_without_recomputation",
    ),
    "sample_size_and_universe_scope_diagnostic": (
        "11946_records_across_twelve_tickers_and_four_walk_forward_folds",
        "Sample breadth and temporal depth may be insufficient for stable inference.",
        "sample_window_may_be_too_short_for_stability",
        "review_scope_and_sample_depth_tradeoffs_without_expanding_data",
    ),
    "data_quality_and_meta_limitation_diagnostic": (
        "pass_with_preserved_source_limitation_and_meta_913_records",
        "META has a preserved reduced record count that must remain explicit.",
        "META_limitation_is_preserved_and_not_repaired",
        "retain_the_limitation_in_any_later_operator_selected_path",
    ),
    "acceptance_criteria_diagnostic": (
        "two_consecutive_not_ready_decisions",
        "Acceptance criteria were not met in either evidence cycle.",
        "acceptance_thresholds_may_need_formal_definition",
        "formalize_precommitted_readiness_thresholds_before_future_execution",
    ),
}

OPTION_IDS = list(planning.OPTION_IDS)
ALLOWED_SELECTIONS_LATER = [
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE",
    "FEATURE_METHOD_REDESIGN_CANDIDATE",
    "DATA_SCOPE_EXPANSION_CANDIDATE",
    "NEW_MODELING_APPROACH_CANDIDATE",
    "PAUSE_AND_ARCHIVE_RESEARCH_CHAIN",
]

RISK_CONTROLS = [
    "no_acceptance_after_failed_readiness",
    "no_runtime_activation",
    "no_strategy_scoring",
    "no_trade_recommendations",
    "no_broker_execution",
    "no_paper_trading",
    "no_more_execution_without_new_review",
    "preserve_frozen_dataset",
    "preserve_meta_record_limitation",
    "research_outputs_non_actionable",
    "operator_review_required_for_any_new_path",
    "method_selection_required_before_more_execution",
    "acceptance_candidate_not_allowed_currently",
]

PLANNED_OUTPUT_NAMES = [
    "label_objective_redesign_candidate_template",
    "feature_method_redesign_candidate_template",
    "data_scope_expansion_candidate_template",
    "new_modeling_approach_candidate_template",
    "pause_and_archive_research_chain_template",
    "operator_method_selection_summary_template",
]

REQUIRED_DIGEST_FIELDS = {
    "predictive_evidence_planning_tree_review_package_digest": EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
    "latest_readiness_rerun_using_refined_evidence_digest": EXPECTED_LATEST_READINESS_DIGEST,
    "latest_reassessment_rerun_using_refined_evidence_digest": EXPECTED_LATEST_REASSESSMENT_DIGEST,
    "refined_results_review_digest": EXPECTED_REFINED_RESULTS_REVIEW_DIGEST,
    "refined_execution_digest": EXPECTED_REFINED_EXECUTION_DIGEST,
    "feature_label_refinement_results_review_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST,
    "feature_label_refinement_execution_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST,
    "original_acceptance_readiness_review_digest": EXPECTED_ORIGINAL_READINESS_DIGEST,
    "original_reassessment_review_digest": EXPECTED_ORIGINAL_REASSESSMENT_DIGEST,
    "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
    "records_digest": EXPECTED_RECORDS_DIGEST,
}

CHECK_IDS = [
    "planning_tree_review_digest_bound",
    "latest_readiness_digest_bound",
    "latest_reassessment_digest_bound",
    "refined_results_review_digest_bound",
    "refined_execution_digest_bound",
    "original_readiness_digest_bound",
    "research_registry_approval_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "original_readiness_not_ready_bound",
    "refined_readiness_not_ready_bound",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "diagnostic_domains_defined",
    "failure_mechanisms_defined",
    "method_path_options_defined",
    "acceptance_option_not_allowed",
    "operator_method_path_selection_recommended",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "no_provider_requests",
    "no_market_data_acquisition",
    "no_dataset_regeneration",
    "no_predictive_rerun",
    "no_metric_recomputation",
    "no_strategy_scoring",
    "no_runtime_activation",
    "no_tracked_marketflow_files",
]


class PredictiveEvidenceMethodDiagnosticReviewError(ValueError):
    """Raised when a diagnostic package violates its diagnosis-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveEvidenceMethodDiagnosticReviewError(f"{field} mismatch")


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


def _diagnostic_domains() -> list[dict[str, Any]]:
    domains: list[dict[str, Any]] = []
    for domain_id in DIAGNOSTIC_DOMAIN_IDS:
        evidence, observation, mechanism, investigation = DOMAIN_DETAILS[domain_id]
        domains.append(
            {
                "domain_id": domain_id,
                "domain_status": "DIAGNOSIS_RECORDED_RESEARCH_ONLY",
                "evidence_basis": evidence,
                "diagnostic_observation": observation,
                "possible_failure_mechanism": mechanism,
                "recommended_investigation": investigation,
                "execution_required": False,
                "research_only": True,
                "non_actionable": True,
            }
        )
    return domains


def _method_path_options() -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = []
    for option_id in OPTION_IDS:
        if option_id == "OPTION_B_METHOD_DIAGNOSTIC_REVIEW":
            status = COMPLETED_BY_THIS_PACKAGE
        elif option_id == "OPTION_G_ACCEPTANCE_CANDIDATE":
            status = NOT_ALLOWED_CURRENTLY
        else:
            status = AVAILABLE_FOR_OPERATOR_SELECTION
        options.append(
            {
                "option_id": option_id,
                "status": status,
                "selected_or_approved": False,
                "execution_authorized": False,
                "authority": "NON_AUTHORIZING_METHOD_PATH_OPTION_ONLY",
            }
        )
    return options


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "output_name": name,
            "status": PLANNED_NOT_GENERATED,
            "label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_V1,
        "review_status": PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "method_diagnostic_review_created": True,
        "method_diagnostic_review_ready": True,
        "ready_for_operator_method_path_selection": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_regeneration_performed_in_review": False,
        "original_predictive_evidence_rerun_performed": False,
        "refined_predictive_evidence_rerun_performed": False,
        "label_generation_rerun_performed": False,
        "feature_generation_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "model_training_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "label_objective_redesign_candidate_created": False,
        "feature_method_redesign_candidate_created": False,
        "data_scope_expansion_candidate_created": False,
        "new_modeling_approach_candidate_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
        **REQUIRED_DIGEST_FIELDS,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "registry_approved_dataset_metadata": deepcopy(
            REGISTRY_APPROVED_DATASET_METADATA
        ),
        "original_readiness_decision": ORIGINAL_READINESS_DECISION,
        "refined_readiness_decision": REFINED_READINESS_DECISION,
        "overall_method_signal_status": "WEAK_OR_MIXED",
        "baseline_outperformance_status": "INSUFFICIENT_OR_MIXED",
        "oos_generalization_status": "LOW_TO_MIXED",
        "acceptance_readiness_status": "NOT_READY_TWICE",
        "method_diagnostic_conclusion": (
            "METHOD_REVIEW_REQUIRED_BEFORE_MORE_EXECUTION"
        ),
        "evidence_comparison": {
            "original_oos_majority_accuracy": "0.539491",
            "original_oos_previous_direction_accuracy": "0.495984",
            "original_oos_ticker_cross_sectional_accuracy": "0.502677",
            "original_oos_brier_score": "0.24875351",
            "refined_oos_accuracy_range": "0.119813 to 0.480924",
            "refined_signal_consistency": "WEAK_OR_MIXED",
            "refined_baseline_outperformance": "INSUFFICIENT_OR_MIXED",
            "refined_model_comparison": (
                "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE"
            ),
        },
        "two_readiness_gates_not_ready": True,
        "refined_evidence_did_not_create_acceptance_readiness": True,
        "diagnostic_domains": _diagnostic_domains(),
        "possible_failure_mechanisms": list(FAILURE_MECHANISMS),
        "method_path_options": _method_path_options(),
        "recommended_next_path": RECOMMENDED_NEXT_PATH,
        "allowed_selections_later": list(ALLOWED_SELECTIONS_LATER),
        "operator_method_path_selected": False,
        "approved_execution_path": None,
        "recommended_immediate_action": RECOMMENDED_IMMEDIATE_ACTION,
        "recommendation_reason": RECOMMENDATION_REASON,
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
    }


def _derived_checks(package: dict[str, Any]) -> dict[str, Any]:
    domains = package.get("diagnostic_domains", [])
    options = package.get("method_path_options", [])
    planned_outputs = package.get("planned_outputs", [])
    option_map = {
        item.get("option_id"): item
        for item in options
        if isinstance(item, dict)
    } if isinstance(options, list) else {}
    return {
        "planning_tree_review_digest_bound": package.get(
            "predictive_evidence_planning_tree_review_package_digest"
        )
        == EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
        "latest_readiness_digest_bound": package.get(
            "latest_readiness_rerun_using_refined_evidence_digest"
        )
        == EXPECTED_LATEST_READINESS_DIGEST,
        "latest_reassessment_digest_bound": package.get(
            "latest_reassessment_rerun_using_refined_evidence_digest"
        )
        == EXPECTED_LATEST_REASSESSMENT_DIGEST,
        "refined_results_review_digest_bound": package.get(
            "refined_results_review_digest"
        )
        == EXPECTED_REFINED_RESULTS_REVIEW_DIGEST,
        "refined_execution_digest_bound": package.get("refined_execution_digest")
        == EXPECTED_REFINED_EXECUTION_DIGEST,
        "original_readiness_digest_bound": package.get(
            "original_acceptance_readiness_review_digest"
        )
        == EXPECTED_ORIGINAL_READINESS_DIGEST,
        "research_registry_approval_digest_bound": package.get(
            "research_registry_approval_digest"
        )
        == EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest_bound": package.get("records_digest")
        == EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": package.get("target_universe_count") == 12
        and package.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": package.get("records_digest")
        == EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": package.get("meta_record_count") == 913
        and package.get("per_ticker_record_counts", {}).get("META") == 913,
        "original_readiness_not_ready_bound": package.get(
            "original_readiness_decision"
        )
        == ORIGINAL_READINESS_DECISION,
        "refined_readiness_not_ready_bound": package.get(
            "refined_readiness_decision"
        )
        == REFINED_READINESS_DECISION,
        "predictive_usefulness_not_accepted": package.get("predictive_usefulness")
        == NOT_ACCEPTED,
        "profitability_not_accepted": package.get("profitability")
        == NOT_ACCEPTED,
        "runtime_not_authorized": package.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": package.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": package.get("broker_execution")
        == NOT_AUTHORIZED,
        "trade_recommendations_false": package.get(
            "trade_recommendations_generated"
        )
        is False,
        "diagnostic_domains_defined": isinstance(domains, list)
        and [item.get("domain_id") for item in domains if isinstance(item, dict)]
        == DIAGNOSTIC_DOMAIN_IDS,
        "failure_mechanisms_defined": package.get("possible_failure_mechanisms")
        == FAILURE_MECHANISMS,
        "method_path_options_defined": list(option_map) == OPTION_IDS,
        "acceptance_option_not_allowed": option_map.get(
            "OPTION_G_ACCEPTANCE_CANDIDATE", {}
        ).get("status")
        == NOT_ALLOWED_CURRENTLY,
        "operator_method_path_selection_recommended": package.get(
            "recommended_next_path"
        )
        == RECOMMENDED_NEXT_PATH,
        "risk_controls_defined": package.get("risk_controls") == RISK_CONTROLS,
        "planned_outputs_not_generated": isinstance(planned_outputs, list)
        and len(planned_outputs) == len(PLANNED_OUTPUT_NAMES)
        and all(
            item.get("status") == PLANNED_NOT_GENERATED
            for item in planned_outputs
        ),
        "planned_outputs_research_only": isinstance(planned_outputs, list)
        and len(planned_outputs) == len(PLANNED_OUTPUT_NAMES)
        and all(
            item.get("label") == RESEARCH_ONLY_NON_ACTIONABLE
            for item in planned_outputs
        ),
        "no_provider_requests": package.get("provider_requests_made_in_review")
        is False,
        "no_market_data_acquisition": package.get(
            "market_data_acquisition_performed_in_review"
        )
        is False,
        "no_dataset_regeneration": package.get(
            "dataset_regeneration_performed_in_review"
        )
        is False,
        "no_predictive_rerun": package.get(
            "original_predictive_evidence_rerun_performed"
        )
        is False
        and package.get("refined_predictive_evidence_rerun_performed") is False,
        "no_metric_recomputation": package.get("metrics_recomputation_performed")
        is False,
        "no_strategy_scoring": package.get("new_strategy_scoring_performed")
        is False,
        "no_runtime_activation": package.get("runtime_migration_approved") is False
        and package.get("runtime_migration_active") is False,
        "no_tracked_marketflow_files": package.get("no_tracked_marketflow_files")
        is True
        and package.get("tracked_marketflow_files") == [],
    }


def _checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(package)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    blockers = sum(
        item.get("status") == FAIL and item.get("severity") == BLOCKER
        for item in checklist
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "method_diagnostic_review_ready": blockers == 0,
        "recommended_next_path": RECOMMENDED_NEXT_PATH,
        "acceptance_candidate_allowed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(package)
    payload.pop("predictive_evidence_method_diagnostic_review_package_digest", None)
    return payload


def predictive_evidence_method_diagnostic_review_package_digest_v1(
    package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the diagnostic package."""
    return semantic_digest(_digest_payload(package))


def build_predictive_evidence_method_diagnostic_review_package_v1() -> dict:
    """Build the offline diagnosis-only method review package."""
    package = _base_package()
    package["review_checklist"] = _checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    package["predictive_evidence_method_diagnostic_review_package_digest"] = (
        predictive_evidence_method_diagnostic_review_package_digest_v1(package)
    )
    validate_predictive_evidence_method_diagnostic_review_package_v1(package)
    return package


def _reject_forbidden_authority(value: Any, *, path: str = "package") -> None:
    forbidden_artifacts = {
        "LABEL_OBJECTIVE_REDESIGN_CANDIDATE",
        "FEATURE_METHOD_REDESIGN_CANDIDATE",
        "DATA_SCOPE_EXPANSION_CANDIDATE",
        "NEW_MODELING_APPROACH_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true_fields = {
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_regeneration_performed_in_review",
        "original_predictive_evidence_rerun_performed",
        "refined_predictive_evidence_rerun_performed",
        "label_generation_rerun_performed",
        "feature_generation_rerun_performed",
        "metrics_recomputation_performed",
        "model_training_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "label_objective_redesign_candidate_created",
        "feature_method_redesign_candidate_created",
        "data_scope_expansion_candidate_created",
        "new_modeling_approach_candidate_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
        "selected_or_approved",
        "execution_authorized",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise PredictiveEvidenceMethodDiagnosticReviewError(
                    f"{current} must remain false"
                )
            if isinstance(item, str) and item in forbidden_artifacts:
                raise PredictiveEvidenceMethodDiagnosticReviewError(
                    f"{current} must not create {item}"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise PredictiveEvidenceMethodDiagnosticReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveEvidenceMethodDiagnosticReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_predictive_evidence_method_diagnostic_review_package_v1(
    package: dict,
) -> dict:
    """Validate exact evidence bindings and all diagnosis-only boundaries."""
    if not isinstance(package, dict):
        raise PredictiveEvidenceMethodDiagnosticReviewError(
            "method diagnostic review package must be a JSON object"
        )
    _reject_forbidden_authority(package)
    expected_base = _base_package()
    for field, expected in expected_base.items():
        _expect(package.get(field), expected, field)
    checklist = package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveEvidenceMethodDiagnosticReviewError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(package)
    _expect(checklist, expected_checklist, "review_checklist")
    if any(item["status"] != PASS for item in expected_checklist):
        raise PredictiveEvidenceMethodDiagnosticReviewError(
            "review_checklist contains a failed check"
        )
    expected_summary = _summary(expected_checklist)
    _expect(package.get("review_summary"), expected_summary, "review_summary")
    digest = package.get(
        "predictive_evidence_method_diagnostic_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveEvidenceMethodDiagnosticReviewError(
            "predictive evidence method diagnostic review package digest missing"
        )
    _expect(
        digest,
        predictive_evidence_method_diagnostic_review_package_digest_v1(package),
        "predictive_evidence_method_diagnostic_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE_VALID",
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "predictive_evidence_method_diagnostic_review_package_digest": digest,
        "diagnostic_domain_count": len(package["diagnostic_domains"]),
        "failure_mechanism_count": len(package["possible_failure_mechanisms"]),
        "recommended_next_path": package["recommended_next_path"],
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_predictive_evidence_method_diagnostic_review_markdown_v1(
    package: dict,
) -> str:
    """Render a sanitized Markdown summary of the method diagnosis."""
    validation = validate_predictive_evidence_method_diagnostic_review_package_v1(
        package
    )
    evidence = package["evidence_comparison"]
    summary = package["review_summary"]
    lines = [
        "# MarketFlow Predictive Evidence Method Diagnostic Review",
        "",
        "## Title",
        "- Predictive Evidence Method Diagnostic Review v1.",
        "",
        "## Method Diagnostic Review",
        f"- Artifact/status: `{package['artifact_kind']}` / `{package['review_status']}`.",
        f"- Digest: `{validation['predictive_evidence_method_diagnostic_review_package_digest']}`.",
        f"- Conclusion: `{package['method_diagnostic_conclusion']}`.",
        "",
        "## Bound Evidence",
    ]
    lines.extend(
        f"- `{field}`: `{digest}`"
        for field, digest in REQUIRED_DIGEST_FIELDS.items()
    )
    lines.extend(
        [
            "",
            "## Dataset and Universe",
            f"- Dataset/profile/timeframe: `{package['dataset_name']}` / `{package['source_profile']}` / `{package['timeframe']}`.",
            f"- Universe: `{', '.join(package['target_universe'])}`.",
            "- Records: `11946`; META remains `913`, every other ticker remains `1003`.",
            "",
            "## Evidence Comparison",
            f"- Original OOS majority/previous/cross-sectional: `{evidence['original_oos_majority_accuracy']}` / `{evidence['original_oos_previous_direction_accuracy']}` / `{evidence['original_oos_ticker_cross_sectional_accuracy']}`.",
            f"- Original Brier: `{evidence['original_oos_brier_score']}`.",
            f"- Refined OOS/signal/baseline: `{evidence['refined_oos_accuracy_range']}` / `{evidence['refined_signal_consistency']}` / `{evidence['refined_baseline_outperformance']}`.",
            "",
            "## Diagnostic Domains",
        ]
    )
    lines.extend(
        f"- `{item['domain_id']}`: {item['diagnostic_observation']}"
        for item in package["diagnostic_domains"]
    )
    lines.extend(["", "## Possible Failure Mechanisms"])
    lines.extend(
        f"- `{mechanism}`" for mechanism in package["possible_failure_mechanisms"]
    )
    lines.extend(["", "## Method Path Options"])
    lines.extend(
        f"- `{item['option_id']}`: `{item['status']}`"
        for item in package["method_path_options"]
    )
    lines.extend(
        [
            "",
            "## Recommended Next Path",
            f"- Path/action: `{package['recommended_next_path']}` / `{package['recommended_immediate_action']}`.",
            f"- Reason: `{package['recommendation_reason']}`.",
            "- No later method path is selected or approved by this package.",
            "",
            "## Risk Controls",
        ]
    )
    lines.extend(f"- `{control}`" for control in package["risk_controls"])
    lines.extend(
        [
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- This diagnosis-only package creates no redesign candidate, execution, approval, acceptance, profitability, runtime, strategy, paper, broker, or recommendation authority.",
            "- No provider request, acquisition, dataset regeneration, predictive rerun, label/feature regeneration, metric recomputation, model training, scoring, or recommendation occurred.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_evidence_method_diagnostic_review_package_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict:
    """Write one canonical diagnostic JSON package without overwriting."""
    package = build_predictive_evidence_method_diagnostic_review_package_v1()
    validation = validate_predictive_evidence_method_diagnostic_review_package_v1(
        package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_evidence_method_diagnostic_review_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveEvidenceMethodDiagnosticReviewError(
            "method diagnostic review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveEvidenceMethodDiagnosticReviewError(
            "method diagnostic review output already exists"
        )
    payload = canonical_json_bytes(package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
