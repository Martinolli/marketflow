"""Offline not-ready closure and method tree for expectancy-lab evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_predictive_usefulness_acceptance_readiness_review_expectancy_lab_evidence_service as readiness,
)


ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_EXPECTANCY_LAB_EVIDENCE"
)
SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_METHOD_TREE_EXPECTANCY_LAB_EVIDENCE_V1 = (
    "marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE"
)
CLOSE_CURRENT_EXPECTANCY_LAB_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_OR_ARCHIVE_SELECTION = (
    "CLOSE_CURRENT_EXPECTANCY_LAB_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_OR_ARCHIVE_SELECTION"
)
PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME = (
    "PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_METHOD_TREE_EXPECTANCY_LAB_EVIDENCE_VALID = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_METHOD_TREE_EXPECTANCY_LAB_EVIDENCE_VALID"
)

EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST = "4a1386468b9fcfb61f67578803685a432a076bddde412438db601813666bed20"
EXPECTED_SOURCE_REASSESSMENT_DIGEST = readiness.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = readiness.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_EXECUTION_DIGEST = readiness.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = readiness.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = readiness.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = readiness.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_APPROVAL_DIGEST = readiness.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = readiness.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = readiness.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = readiness.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = readiness.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = readiness.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = readiness.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = readiness.EXPECTED_SOURCE_RECORDS_DIGEST

TARGET_UNIVERSE = list(readiness.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(readiness.EXPECTED_RECORD_COUNTS)
EXPECTED_LAB_ROW_COUNTS = dict(readiness.EXPECTED_LAB_ROW_COUNTS)
EXPECTED_EVALUABLE_COUNTS = dict(readiness.EXPECTED_EVALUABLE_COUNTS)
EXPECTED_UNAVAILABLE_COUNTS = dict(readiness.EXPECTED_UNAVAILABLE_COUNTS)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

RECOMMENDED_CURRENT_DECISION = "OPTION_A_ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY"
NEXT_ARTIFACT = "OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE"


def _option(
    option_id: str,
    option_status: str,
    description: str,
    rationale: str,
    *,
    requires_operator_selection: bool,
) -> dict[str, Any]:
    return {
        "option_id": option_id,
        "option_status": option_status,
        "description": description,
        "rationale": rationale,
        "requires_operator_selection": requires_operator_selection,
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
        "acceptance_candidate_created": False,
        "runtime_authority_created": False,
        "research_only": True,
        "non_actionable": True,
    }


METHOD_PLANNING_TREE = {
    RECOMMENDED_CURRENT_DECISION: _option(
        RECOMMENDED_CURRENT_DECISION,
        "RECOMMENDED_FOR_OPERATOR_SELECTION_NOT_SELECTED",
        "Archive the current expectancy-lab evidence path as not ready for predictive-usefulness acceptance and preserve all evidence for historical governance.",
        "The reassessment recommends not accepting predictive usefulness; acceptance materiality, baseline outperformance, per-ticker stability, and operator thresholds remain not ready.",
        requires_operator_selection=True,
    ),
    "OPTION_B_DEFINE_OPERATOR_ACCEPTANCE_THRESHOLDS_FOR_EXPECTANCY_EVIDENCE": _option(
        "OPTION_B_DEFINE_OPERATOR_ACCEPTANCE_THRESHOLDS_FOR_EXPECTANCY_EVIDENCE",
        "AVAILABLE_FOR_OPERATOR_SELECTION_NOT_SELECTED",
        "Create a future candidate to define explicit acceptance thresholds for expectancy materiality, baseline outperformance, per-ticker stability, embargo handling, and META treatment.",
        "Explicit operator-approved thresholds would be required before a future readiness decision could be evaluated consistently.",
        requires_operator_selection=True,
    ),
    "OPTION_C_METHOD_IMPROVEMENT_CANDIDATE_FOR_MATERIALITY_AND_STABILITY": _option(
        "OPTION_C_METHOD_IMPROVEMENT_CANDIDATE_FOR_MATERIALITY_AND_STABILITY",
        "AVAILABLE_FOR_OPERATOR_SELECTION_NOT_SELECTED",
        "Create a future method-improvement candidate focused on materiality thresholds, stability review, per-ticker dispersion, and evidence quality.",
        "Current materiality and per-ticker stability findings are not ready for acceptance.",
        requires_operator_selection=True,
    ),
    "OPTION_D_ADDITIONAL_OUT_OF_SAMPLE_OR_EXPANDED_UNIVERSE_EVIDENCE": _option(
        "OPTION_D_ADDITIONAL_OUT_OF_SAMPLE_OR_EXPANDED_UNIVERSE_EVIDENCE",
        "AVAILABLE_FOR_OPERATOR_SELECTION_NOT_SELECTED",
        "Plan additional out-of-sample evidence or expanded-universe evidence before considering another acceptance path.",
        "Additional separately approved evidence could test whether current findings generalize.",
        requires_operator_selection=True,
    ),
    "OPTION_E_VPA_WYCKOFF_RULE_REFINEMENT_CANDIDATE": _option(
        "OPTION_E_VPA_WYCKOFF_RULE_REFINEMENT_CANDIDATE",
        "AVAILABLE_FOR_OPERATOR_SELECTION_NOT_SELECTED",
        "Create a future candidate to review transparent VPA/Wyckoff rule thresholds or supporting reversal context while preventing optimization leakage and preserving chronology.",
        "Any rule refinement requires a new governed evidence chain with chronology and leakage controls preserved.",
        requires_operator_selection=True,
    ),
    "OPTION_F_ABSTENTION_AND_NO_TRADE_OBJECTIVE_REFINEMENT": _option(
        "OPTION_F_ABSTENTION_AND_NO_TRADE_OBJECTIVE_REFINEMENT",
        "AVAILABLE_FOR_OPERATOR_SELECTION_NOT_SELECTED",
        "Create a future candidate to refine abstention/no-trade handling, participation filters, and noise exclusion before rerunning evidence.",
        "The current objective path can be reconsidered only through a separate candidate and approval sequence.",
        requires_operator_selection=True,
    ),
    "OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED": _option(
        "OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED",
        "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE",
        "Profitability and runtime work remain blocked because predictive usefulness has not been accepted.",
        "Predictive usefulness is a mandatory prior gate for profitability and runtime work.",
        requires_operator_selection=False,
    ),
    "OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE": _option(
        "OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "NOT_ALLOWED_CURRENTLY",
        "Acceptance candidate is not allowed because the readiness decision is NOT_READY.",
        "The source readiness review expressly recommends not creating an acceptance candidate.",
        requires_operator_selection=False,
    ),
}

NEXT_CHAIN = [
    "Operator Method or Closure Selection Using Expectancy Lab Evidence v1.",
    "If Option A selected: Predictive-Usefulness Acceptance Path Archive Record Using Expectancy Lab Evidence v1.",
    "If another improvement option is selected: separate candidate, operator review, approval, execution, results review, reassessment, and readiness rerun.",
    "Predictive-usefulness acceptance candidate only if a future readiness review passes.",
    "Profitability review only after predictive usefulness is separately accepted.",
    "Runtime migration only if ever separately authorized.",
]

NEXT_GATES = [
    "operator_method_or_closure_selection_using_expectancy_lab_evidence",
    "archive_record_if_option_a_selected",
    "method_improvement_candidate_if_selected",
    "new_evidence_chain_if_separately_approved",
    "future_predictive_usefulness_reassessment_rerun",
    "future_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_if_predictive_usefulness_accepted",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "closure_does_not_accept_predictive_usefulness",
    "closure_does_not_create_acceptance_candidate",
    "closure_does_not_accept_profitability",
    "closure_does_not_authorize_runtime",
    "closure_does_not_authorize_strategy",
    "closure_does_not_authorize_paper_trading",
    "closure_does_not_authorize_broker_execution",
    "closure_does_not_generate_trade_recommendations",
    "closure_does_not_train_models",
    "closure_does_not_score_strategy",
    "closure_does_not_call_providers",
    "closure_does_not_acquire_market_data",
    "closure_does_not_recompute_metrics_from_raw_rows",
    "closure_does_not_rerun_acceptance_readiness_review",
    "closure_does_not_rerun_predictive_usefulness_reassessment",
    "closure_does_not_rerun_expectancy_backtest_lab_execution",
    "closure_does_not_rerun_expectancy_backtest_lab_results_review",
    "closure_does_not_rerun_vpa_wyckoff_execution",
    "closure_does_not_rerun_vpa_wyckoff_results_review",
    "closure_does_not_rerun_feature_label_matrix_execution",
    "closure_does_not_rerun_feature_label_matrix_results_review",
    "closure_does_not_rerun_signal_feature_generation",
    "closure_does_not_rerun_target_generation",
    "closure_does_not_create_operator_selection",
    "closure_does_not_create_archive_record",
    "closure_does_not_create_method_improvement_candidate",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_expectancy_backtest_lab_outputs",
    "do_not_mutate_vpa_wyckoff_outputs",
    "do_not_mutate_matrix_outputs",
    "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_target_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_acceptance_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_results_review_digest_bound", "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound", "source_vpa_wyckoff_rule_values_digest_bound",
    "source_matrix_rows_digest_bound", "source_target_values_digest_bound",
    "records_digest_bound", "target_universe_12_preserved", "records_digest_preserved",
    "meta_913_preserved", "readiness_decision_not_ready_bound",
    "source_recommendation_do_not_create_acceptance_candidate_bound",
    "not_ready_closure_created_true", "acceptance_path_closed_not_ready_true",
    "method_planning_tree_created_true", "operator_method_or_closure_selection_required_true",
    "ready_for_operator_method_or_closure_selection_true",
    "operator_method_or_closure_selection_created_false", "archive_record_created_false",
    "method_improvement_candidate_created_false", "new_evidence_candidate_created_false",
    "acceptance_candidate_created_false", "predictive_usefulness_not_accepted",
    "predictive_usefulness_accepted_false", "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "paper_trading_not_authorized",
    "broker_not_authorized", "trade_recommendations_false",
    "source_backtest_lab_row_count_179190", "evaluable_target_row_count_177090",
    "unavailable_target_row_count_2100", "embargoed_cross_split_forward_horizon_row_count_4200",
    "aggregate_metric_eligible_row_count_172890", "metric_materiality_not_ready",
    "baseline_outperformance_not_ready", "per_ticker_stability_requires_operator_review",
    "meta_readiness_pass_with_operator_awareness", "option_a_recommended_not_selected",
    "options_b_to_f_available_not_selected", "option_g_blocked", "option_h_not_allowed",
    "all_options_unselected", "per_ticker_entries_12", "per_ticker_digests_present",
    "model_training_authorized_false", "model_training_performed_false",
    "strategy_scoring_false", "provider_requests_made_false", "market_data_acquisition_false",
    "dataset_regeneration_false", "metric_recomputation_from_raw_rows_false",
    "acceptance_readiness_review_rerun_false", "predictive_usefulness_reassessment_rerun_false",
    "expectancy_backtest_lab_execution_rerun_false", "expectancy_backtest_lab_results_review_rerun_false",
    "vpa_wyckoff_execution_rerun_false", "vpa_wyckoff_results_review_rerun_false",
    "matrix_execution_rerun_false", "matrix_results_review_rerun_false",
    "signal_feature_generation_rerun_false", "target_generation_rerun_false",
    "raw_provider_payloads_not_committed", "api_keys_not_stored_or_printed",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(ValueError):
    """Raised when the closure package violates its evidence or authority contract."""


def per_ticker_marketflow_predictive_usefulness_not_ready_closure_expectancy_lab_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker closure entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_not_ready_closure_digest", None)
    return semantic_digest(payload)


def _validate_source_readiness(source_readiness: Mapping[str, Any]) -> None:
    if not isinstance(source_readiness, dict):
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "source_readiness must be an object"
        )
    try:
        readiness.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(
            source_readiness
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "source readiness review is invalid"
        ) from exc
    if source_readiness.get(
        "marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest"
    ) != EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST:
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "source acceptance-readiness digest mismatch"
        )


def _source_evidence(source_readiness: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_readiness is not None:
        _validate_source_readiness(source_readiness)
        return deepcopy(source_readiness["source_evidence"])
    # This is a committed constant snapshot; it performs no source inspection or rerun.
    return readiness.reassessment._canonical_source_evidence()


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "source_acceptance_readiness_status": readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_COMPLETED,
            "source_acceptance_readiness_decision": readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
            "closure_status": "CLOSED_NOT_READY",
            "recommended_option": RECOMMENDED_CURRENT_DECISION,
            "backtest_lab_row_count": EXPECTED_LAB_ROW_COUNTS[ticker],
            "evaluable_target_row_count": EXPECTED_EVALUABLE_COUNTS[ticker],
            "unavailable_target_row_count": EXPECTED_UNAVAILABLE_COUNTS[ticker],
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_accepted": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_recommended": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
            "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
            "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
            "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
            "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
            "closure_note": (
                "PRESERVE_META_LIMITATION_IN_NOT_READY_CLOSURE_USING_EXPECTANCY_LAB_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_not_ready_closure_digest"] = (
            per_ticker_marketflow_predictive_usefulness_not_ready_closure_expectancy_lab_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package(source_readiness: Mapping[str, Any] | None) -> dict[str, Any]:
    execution = readiness.reassessment.execution
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_EXPECTANCY_LAB_EVIDENCE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_METHOD_TREE_EXPECTANCY_LAB_EVIDENCE_V1,
        "closure_status": MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "closure_decision": CLOSE_CURRENT_EXPECTANCY_LAB_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_OR_ARCHIVE_SELECTION,
        "closure_scope": PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "source_acceptance_readiness_artifact_kind": readiness.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_acceptance_readiness_status": readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_COMPLETED,
        "source_acceptance_readiness_decision": readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_acceptance_readiness_scope": readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME,
        "source_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_expectancy_backtest_lab_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_expectancy_backtest_lab_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_expectancy_backtest_lab_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_expectancy_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_expectancy_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_expectancy_backtest_lab_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": _source_evidence(source_readiness),
        "selected_backtest_lab_package": execution.SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": execution.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": execution.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": execution.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": execution.SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": execution.SELECTED_OBJECTIVE_PATH,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "predictive_usefulness_not_ready_closure_created": True,
        "predictive_usefulness_acceptance_path_closed_not_ready": True,
        "method_planning_tree_created": True,
        "operator_method_or_closure_selection_required": True,
        "ready_for_operator_method_or_closure_selection": True,
        "operator_method_or_closure_selection_created": False,
        "archive_record_created": False, "method_improvement_candidate_created": False,
        "new_evidence_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "profitability_acceptance_ready": False, "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False, "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False, "model_training_authorized": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "new_strategy_scoring_performed": False, "trade_recommendations_generated": False,
        "provider_requests_made_in_closure": False,
        "live_provider_transport_enabled_in_closure": False,
        "market_data_acquisition_performed_in_closure": False,
        "dataset_generation_performed_in_closure": False,
        "canonical_dataset_regenerated_in_closure": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "acceptance_readiness_review_rerun_performed": False,
        "predictive_usefulness_reassessment_rerun_performed": False,
        "expectancy_backtest_lab_execution_rerun_performed": False,
        "expectancy_backtest_lab_results_review_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_rerun_performed": False,
        "target_generation_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "readiness_decision": readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "decision_reason": readiness.READINESS_DECISION_REASON,
        "source_reassessment_recommendation": "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "source_readiness_recommendation": "DO_NOT_CREATE_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "source_matrix_row_count": 179190, "expectancy_backtest_lab_row_count": 179190,
        "evaluable_target_row_count": 177090, "unavailable_target_row_count": 2100,
        "embargoed_cross_split_forward_horizon_row_count": 4200,
        "aggregate_metric_eligible_row_count": 172890,
        "approved_metric_family_count": 13, "blocked_metric_family_count": 1,
        "approved_baseline_count": 6, "blocked_baseline_count": 1,
        "evidence_integrity": PASS, "source_output_integrity": PASS,
        "no_peek_and_leakage": PASS,
        "chronology_and_embargo": "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS",
        "metric_materiality_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "per_ticker_stability_readiness": "REQUIRES_OPERATOR_REVIEW",
        "meta_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "acceptance_candidate_allowed": False, "acceptance_candidate_recommended": False,
        "closure_classification": "COMPLETED_RESEARCH_ONLY",
        "current_acceptance_path_status": "CLOSED_NOT_READY",
        "predictive_usefulness_decision": "NOT_ACCEPTED",
        "profitability_decision": "NOT_ACCEPTED",
        "runtime_authority_status": NOT_AUTHORIZED,
        "recommended_current_decision": RECOMMENDED_CURRENT_DECISION,
        "recommended_operator_action": "OPERATOR_METHOD_OR_CLOSURE_SELECTION_REQUIRED",
        "next_artifact_ready": NEXT_ARTIFACT, "next_artifact_created": False,
        "method_planning_tree_options": deepcopy(METHOD_PLANNING_TREE),
        "per_ticker_closure_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and all(
        isinstance(row, dict)
        and row.get("per_ticker_not_ready_closure_digest")
        == per_ticker_marketflow_predictive_usefulness_not_ready_closure_expectancy_lab_evidence_digest_v1(row)
        for row in entries
    )


def _check_values(closure: Mapping[str, Any]) -> dict[str, bool]:
    options = closure.get("method_planning_tree_options")
    entries = closure.get("per_ticker_closure_entries")
    option = lambda key: options.get(key, {}) if isinstance(options, dict) else {}
    return {
        "source_acceptance_readiness_digest_bound": closure.get("source_acceptance_readiness_digest") == EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": closure.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": closure.get("source_expectancy_backtest_lab_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": closure.get("source_expectancy_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": closure.get("source_expectancy_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": closure.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_rows_digest_bound": closure.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest_bound": closure.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": closure.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": closure.get("target_universe") == TARGET_UNIVERSE and closure.get("target_universe_count") == 12,
        "records_digest_preserved": closure.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": closure.get("meta_record_count") == 913,
        "readiness_decision_not_ready_bound": closure.get("readiness_decision") == readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_recommendation_do_not_create_acceptance_candidate_bound": closure.get("source_readiness_recommendation") == "DO_NOT_CREATE_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "not_ready_closure_created_true": closure.get("predictive_usefulness_not_ready_closure_created") is True,
        "acceptance_path_closed_not_ready_true": closure.get("predictive_usefulness_acceptance_path_closed_not_ready") is True,
        "method_planning_tree_created_true": closure.get("method_planning_tree_created") is True,
        "operator_method_or_closure_selection_required_true": closure.get("operator_method_or_closure_selection_required") is True,
        "ready_for_operator_method_or_closure_selection_true": closure.get("ready_for_operator_method_or_closure_selection") is True,
        "operator_method_or_closure_selection_created_false": closure.get("operator_method_or_closure_selection_created") is False,
        "archive_record_created_false": closure.get("archive_record_created") is False,
        "method_improvement_candidate_created_false": closure.get("method_improvement_candidate_created") is False,
        "new_evidence_candidate_created_false": closure.get("new_evidence_candidate_created") is False,
        "acceptance_candidate_created_false": closure.get("predictive_usefulness_acceptance_candidate_created") is False,
        "predictive_usefulness_not_accepted": closure.get("predictive_usefulness") == NOT_ACCEPTED,
        "predictive_usefulness_accepted_false": closure.get("predictive_usefulness_accepted") is False,
        "predictive_usefulness_acceptance_ready_false": closure.get("predictive_usefulness_acceptance_ready") is False,
        "predictive_usefulness_acceptance_recommended_false": closure.get("predictive_usefulness_acceptance_recommended") is False,
        "profitability_not_accepted": closure.get("profitability") == NOT_ACCEPTED and closure.get("profitability_accepted") is False,
        "runtime_not_authorized": closure.get("runtime_use") == NOT_AUTHORIZED and closure.get("runtime_migration_approved") is False,
        "strategy_not_authorized": closure.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": closure.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": closure.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": closure.get("trade_recommendations_generated") is False,
        "source_backtest_lab_row_count_179190": closure.get("expectancy_backtest_lab_row_count") == 179190,
        "evaluable_target_row_count_177090": closure.get("evaluable_target_row_count") == 177090,
        "unavailable_target_row_count_2100": closure.get("unavailable_target_row_count") == 2100,
        "embargoed_cross_split_forward_horizon_row_count_4200": closure.get("embargoed_cross_split_forward_horizon_row_count") == 4200,
        "aggregate_metric_eligible_row_count_172890": closure.get("aggregate_metric_eligible_row_count") == 172890,
        "metric_materiality_not_ready": closure.get("metric_materiality_readiness") == "NOT_READY",
        "baseline_outperformance_not_ready": closure.get("baseline_outperformance_readiness") == "NOT_READY",
        "per_ticker_stability_requires_operator_review": closure.get("per_ticker_stability_readiness") == "REQUIRES_OPERATOR_REVIEW",
        "meta_readiness_pass_with_operator_awareness": closure.get("meta_readiness") == "PASS_WITH_OPERATOR_AWARENESS",
        "option_a_recommended_not_selected": option(RECOMMENDED_CURRENT_DECISION).get("option_status") == "RECOMMENDED_FOR_OPERATOR_SELECTION_NOT_SELECTED" and option(RECOMMENDED_CURRENT_DECISION).get("selection_created") is False,
        "options_b_to_f_available_not_selected": isinstance(options, dict) and all(row.get("option_status") == "AVAILABLE_FOR_OPERATOR_SELECTION_NOT_SELECTED" and row.get("selection_created") is False for row in list(options.values())[1:6]),
        "option_g_blocked": option("OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED").get("option_status") == "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE",
        "option_h_not_allowed": option("OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE").get("option_status") == "NOT_ALLOWED_CURRENTLY",
        "all_options_unselected": isinstance(options, dict) and len(options) == 8 and all(row.get("selection_created") is False for row in options.values()),
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12,
        "per_ticker_digests_present": _per_ticker_digests_valid(entries),
        "model_training_authorized_false": closure.get("model_training_authorized") is False,
        "model_training_performed_false": closure.get("model_training_performed") is False,
        "strategy_scoring_false": closure.get("strategy_scoring_performed") is False and closure.get("new_strategy_scoring_performed") is False,
        "provider_requests_made_false": closure.get("provider_requests_made_in_closure") is False,
        "market_data_acquisition_false": closure.get("market_data_acquisition_performed_in_closure") is False,
        "dataset_regeneration_false": closure.get("canonical_dataset_regenerated_in_closure") is False,
        "metric_recomputation_from_raw_rows_false": closure.get("metric_recomputation_from_raw_rows_performed") is False,
        "acceptance_readiness_review_rerun_false": closure.get("acceptance_readiness_review_rerun_performed") is False,
        "predictive_usefulness_reassessment_rerun_false": closure.get("predictive_usefulness_reassessment_rerun_performed") is False,
        "expectancy_backtest_lab_execution_rerun_false": closure.get("expectancy_backtest_lab_execution_rerun_performed") is False,
        "expectancy_backtest_lab_results_review_rerun_false": closure.get("expectancy_backtest_lab_results_review_rerun_performed") is False,
        "vpa_wyckoff_execution_rerun_false": closure.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": closure.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": closure.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": closure.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": closure.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": closure.get("target_generation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": closure.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": closure.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": closure.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": closure.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": closure.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": closure.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if actual else FAIL,
        "expected": True,
        "actual": actual,
        "severity": BLOCKER,
        "message": "closure evidence matches" if actual else "closure evidence mismatch",
    }


def _checklist(closure: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(closure)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "predictive_usefulness_not_ready_closure_created": True,
        "predictive_usefulness_acceptance_path_closed_not_ready": True,
        "method_planning_tree_created": True,
        "operator_method_or_closure_selection_required": True,
        "ready_for_operator_method_or_closure_selection": True,
        "recommended_current_decision": RECOMMENDED_CURRENT_DECISION,
        "operator_method_or_closure_selection_created": False,
        "archive_record_created": False, "method_improvement_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
        "next_recommended_task": "OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE_V1",
    }


def marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest_v1(
    closure: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the closure package."""
    payload = deepcopy(dict(closure))
    payload.pop("closure_checklist", None)
    payload.pop("closure_summary", None)
    payload.pop("marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest", None)
    return semantic_digest(payload)


def build_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(
    *, source_readiness: dict | None = None,
) -> dict:
    """Build the digest-bound closure without rerunning any source stage."""
    closure = _base_package(source_readiness)
    closure["closure_checklist"] = _checklist(closure)
    closure["closure_summary"] = _summary(closure["closure_checklist"])
    closure["marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest"] = (
        marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest_v1(closure)
    )
    validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(closure)
    return closure


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            f"{field} mismatch"
        )


def validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(
    closure: dict,
) -> dict:
    """Validate all evidence bindings, options, and closed authority gates."""
    if not isinstance(closure, dict):
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "closure must be an object"
        )
    expected = _base_package(None)
    for field, value in expected.items():
        _expect(closure.get(field), value, field)
    entries = closure.get("per_ticker_closure_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "per-ticker closure entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    if not _per_ticker_digests_valid(entries):
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "per-ticker closure digest mismatch"
        )
    checklist = closure.get("closure_checklist")
    if not isinstance(checklist, list):
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "closure checklist missing"
        )
    _expect(checklist, _checklist(closure), "closure checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "closure checklist failed"
        )
    _expect(closure.get("closure_summary"), _summary(checklist), "closure summary")
    digest = closure.get(
        "marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "closure digest missing"
        )
    _expect(
        digest,
        marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest_v1(closure),
        "closure digest",
    )
    return {
        "status": MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_METHOD_TREE_EXPECTANCY_LAB_EVIDENCE_VALID,
        "artifact_kind": closure["artifact_kind"],
        "closure_status": closure["closure_status"],
        "closure_decision": closure["closure_decision"],
        "marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest": digest,
        **{
            key: closure["closure_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_markdown_v1(
    closure: dict,
) -> str:
    """Render a sanitized Markdown view of the validated closure package."""
    validation = validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(closure)
    sections = [
        ("Title", ["Predictive-Usefulness Not-Ready Closure and Method Planning Tree Using Expectancy Lab Evidence v1"]),
        ("Predictive-Usefulness Not-Ready Closure and Method Planning Tree Using Expectancy Lab Evidence v1", [f"Artifact/status: `{closure['artifact_kind']}` / `{closure['closure_status']}`.", f"Digest: `{validation['marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest']}`."]),
        ("Source Acceptance Readiness Review", [f"Decision: `{closure['source_acceptance_readiness_decision']}`.", f"Digest: `{closure['source_acceptance_readiness_digest']}`."]),
        ("Bound Evidence", [f"Reassessment: `{closure['source_reassessment_digest']}`.", f"Results review: `{closure['source_expectancy_backtest_lab_results_review_digest']}`.", f"Rows/metrics: `{closure['source_expectancy_backtest_rows_digest']}` / `{closure['source_expectancy_metric_report_digest']}`."]),
        ("Dataset and Universe", [f"`{closure['dataset_name']}` has `{closure['total_canonical_record_count']}` records across `{closure['target_universe_count']}` tickers.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in closure["target_universe"]) + "."]),
        ("Closure Scope", [f"`{closure['closure_scope']}`; research-only and non-actionable."]),
        ("Closure Basis", [f"`{closure['decision_reason']}`.", f"Rows/evaluable/unavailable: `{closure['expectancy_backtest_lab_row_count']} / {closure['evaluable_target_row_count']} / {closure['unavailable_target_row_count']}`."]),
        ("Closure Classification", [f"`{closure['closure_classification']}`; current path `{closure['current_acceptance_path_status']}`."]),
        ("Method Planning Tree", [f"`{option_id}`: `{row['option_status']}` — {row['description']}" for option_id, row in closure["method_planning_tree_options"].items()]),
        ("Recommended Current Decision", [f"`{closure['recommended_current_decision']}`; no option has been selected."]),
        ("Per-Ticker Closure", [f"`{row['ticker']}`: `{row['closure_status']}`, digest `{row['per_ticker_not_ready_closure_digest']}`." for row in closure["per_ticker_closure_entries"]]),
        ("META Limitation", ["META remains exactly 913 historical records and its reduced-record limitation is preserved."]),
        ("Next Chain", closure["next_chain"]),
        ("Next Gates", closure["next_gates"]),
        ("Risk Controls", closure["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate is created."]),
        ("Profitability Boundary", ["Profitability remains not accepted and blocked behind predictive usefulness."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{closure['closure_summary']['total_checks']} / {closure['closure_summary']['passed_checks']} / {closure['closure_summary']['failed_checks']} / {closure['closure_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, source rerun, raw-row metric recomputation, model training, scoring, recommendation, acceptance, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# Predictive-Usefulness Not-Ready Closure and Method Planning Tree Using Expectancy Lab Evidence v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(
    output_dir: str | Path,
    *,
    source_readiness: dict | None = None,
) -> dict:
    """Write canonical closure JSON without overwriting an existing package."""
    closure = build_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(
        source_readiness=source_readiness
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1.json"
    if path.exists():
        raise MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError(
            "closure output already exists"
        )
    payload = canonical_json_bytes(closure)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": closure["artifact_kind"],
        "closure_status": closure["closure_status"],
        "closure_decision": closure["closure_decision"],
        "marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest": closure["marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
