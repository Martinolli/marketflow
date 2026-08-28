"""Offline terminal summary for the archived expectancy-lab usefulness path."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_service as archive_service,
)


ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE"
)
SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_EXPECTANCY_LAB_EVIDENCE_V1 = (
    "marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE"
)
CURRENT_EXPECTANCY_LAB_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED = (
    "CURRENT_EXPECTANCY_LAB_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED"
)
PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_ONLY_NOT_REOPENING_NOT_ACCEPTANCE_NOT_RUNTIME = (
    "PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_ONLY_NOT_REOPENING_NOT_ACCEPTANCE_NOT_RUNTIME"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_EXPECTANCY_LAB_EVIDENCE_VALID = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_EXPECTANCY_LAB_EVIDENCE_VALID"
)

EXPECTED_SOURCE_ARCHIVE_RECORD_DIGEST = "96f0dfae1aa1de4e6cd286f5b7ec327f8b7a2c735914f16feb480ca61240ffd2"
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = archive_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = archive_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST = archive_service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = archive_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = archive_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = archive_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = archive_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = archive_service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = archive_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = archive_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = archive_service.EXPECTED_SOURCE_RECORDS_DIGEST

TARGET_UNIVERSE = list(archive_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(archive_service.EXPECTED_RECORD_COUNTS)
EXPECTED_LAB_ROW_COUNTS = dict(archive_service.EXPECTED_LAB_ROW_COUNTS)
EXPECTED_EVALUABLE_COUNTS = dict(archive_service.EXPECTED_EVALUABLE_COUNTS)
EXPECTED_UNAVAILABLE_COUNTS = dict(archive_service.EXPECTED_UNAVAILABLE_COUNTS)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

COMPLETED_PHASE_IDS = [
    "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_V1",
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_AND_APPROVAL_CHAIN",
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CHAIN",
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CHAIN",
    "MARKETFLOW_FEATURE_LABEL_MATRIX_CHAIN",
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CHAIN",
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CHAIN",
    "MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE",
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE",
    "MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_EXPECTANCY_LAB_EVIDENCE",
    "MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE",
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE",
    "MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE",
]

NEXT_CHAIN = [
    "Current path terminal: no immediate next action required.",
    "Future reopening only by a new operator method-selection artifact.",
    "Optional future method/evidence improvement candidate only if separately selected later.",
    "New evidence chain only if separately approved later.",
    "Reassessment/readiness rerun only after new evidence.",
    "Predictive-usefulness acceptance candidate only if a future readiness review passes.",
    "Profitability review only after predictive usefulness is separately accepted.",
    "Runtime migration only if ever separately authorized.",
]

NEXT_GATES = [
    "current_path_terminal_no_immediate_action",
    "future_operator_method_selection_if_reopened",
    "optional_future_method_or_evidence_improvement_candidate",
    "new_evidence_chain_if_separately_approved",
    "future_predictive_usefulness_reassessment_rerun",
    "future_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_if_predictive_usefulness_accepted",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "final_summary_does_not_create_reopening_artifact",
    "final_summary_does_not_create_method_improvement_candidate",
    "final_summary_does_not_create_new_evidence_candidate",
    "final_summary_does_not_create_acceptance_candidate",
    "final_summary_does_not_accept_predictive_usefulness",
    "final_summary_does_not_accept_profitability",
    "final_summary_does_not_authorize_runtime",
    "final_summary_does_not_authorize_strategy",
    "final_summary_does_not_authorize_paper_trading",
    "final_summary_does_not_authorize_broker_execution",
    "final_summary_does_not_generate_trade_recommendations",
    "final_summary_does_not_train_models",
    "final_summary_does_not_score_strategy",
    "final_summary_does_not_call_providers",
    "final_summary_does_not_acquire_market_data",
    "final_summary_does_not_recompute_metrics_from_raw_rows",
    "final_summary_does_not_rerun_archive_record",
    "final_summary_does_not_rerun_operator_selection",
    "final_summary_does_not_rerun_closure",
    "final_summary_does_not_rerun_acceptance_readiness_review",
    "final_summary_does_not_rerun_predictive_usefulness_reassessment",
    "final_summary_does_not_rerun_expectancy_backtest_lab_execution",
    "final_summary_does_not_rerun_expectancy_backtest_lab_results_review",
    "final_summary_does_not_rerun_vpa_wyckoff_execution",
    "final_summary_does_not_rerun_vpa_wyckoff_results_review",
    "final_summary_does_not_rerun_feature_label_matrix_execution",
    "final_summary_does_not_rerun_feature_label_matrix_results_review",
    "final_summary_does_not_rerun_signal_feature_generation",
    "final_summary_does_not_rerun_target_generation",
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
    "source_archive_record_digest_bound", "source_operator_selection_digest_bound",
    "source_closure_digest_bound", "source_acceptance_readiness_digest_bound",
    "source_reassessment_digest_bound", "source_results_review_digest_bound",
    "source_backtest_rows_digest_bound", "source_metric_report_digest_bound",
    "source_vpa_wyckoff_rule_values_digest_bound", "source_matrix_rows_digest_bound",
    "source_target_values_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "selected_option_option_a_bound", "selected_decision_archive_current_path_bound",
    "archive_record_created_true", "acceptance_path_archived_true",
    "current_path_archived_not_ready_true", "final_archive_summary_created_true",
    "predictive_usefulness_chain_finalized_true", "current_path_finalized_archived_not_ready_true",
    "no_immediate_next_action_required_true", "future_reopening_requires_new_operator_selection_true",
    "future_reopening_created_false", "method_improvement_candidate_created_false",
    "new_evidence_candidate_created_false", "acceptance_candidate_created_false",
    "predictive_usefulness_not_accepted", "predictive_usefulness_accepted_false",
    "predictive_usefulness_acceptance_ready_false", "predictive_usefulness_acceptance_recommended_false",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "paper_trading_not_authorized", "broker_not_authorized", "trade_recommendations_false",
    "final_summary_classification_completed_research_only",
    "current_evidence_path_status_finalized_archived_not_ready",
    "final_decision_predictive_usefulness_not_accepted",
    "future_reopening_does_not_inherit_acceptance_authority",
    "future_reopening_does_not_inherit_profitability_authority",
    "future_reopening_does_not_inherit_runtime_authority", "completed_phases_present",
    "completed_phases_count_13", "option_a_finalized_archived_selected_path",
    "options_b_to_f_available_only_if_reopened", "option_g_blocked", "option_h_not_allowed",
    "source_backtest_lab_row_count_179190", "evaluable_target_row_count_177090",
    "unavailable_target_row_count_2100", "embargoed_cross_split_forward_horizon_row_count_4200",
    "aggregate_metric_eligible_row_count_172890", "per_ticker_entries_12",
    "per_ticker_digests_present", "model_training_authorized_false",
    "model_training_performed_false", "strategy_scoring_false", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "metric_recomputation_from_raw_rows_false", "archive_record_rerun_false",
    "operator_selection_rerun_false", "closure_rerun_false",
    "acceptance_readiness_review_rerun_false", "predictive_usefulness_reassessment_rerun_false",
    "expectancy_backtest_lab_execution_rerun_false",
    "expectancy_backtest_lab_results_review_rerun_false", "vpa_wyckoff_execution_rerun_false",
    "vpa_wyckoff_results_review_rerun_false", "matrix_execution_rerun_false",
    "matrix_results_review_rerun_false", "signal_feature_generation_rerun_false",
    "target_generation_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(ValueError):
    """Raised when the terminal summary violates its evidence or authority contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            f"{field} mismatch"
        )


def _source_evidence(source_archive: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_archive is None:
        return archive_service._source_evidence(None)
    if not isinstance(source_archive, dict):
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "source_archive must be an object"
        )
    try:
        archive_service.validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(
            source_archive
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "source archive record is invalid"
        ) from exc
    if source_archive.get(
        "marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest"
    ) != EXPECTED_SOURCE_ARCHIVE_RECORD_DIGEST:
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "source archive record digest mismatch"
        )
    return deepcopy(source_archive["source_evidence"])


def _completed_phases() -> list[dict[str, Any]]:
    return [
        {
            "phase_number": index,
            "phase_id": phase_id,
            "phase_status": "COMPLETED_OR_BOUND_SOURCE_EVIDENCE",
            "research_only": True,
            "acceptance_authority_created": False,
            "runtime_authority_created": False,
        }
        for index, phase_id in enumerate(COMPLETED_PHASE_IDS, start=1)
    ]


def _archived_options() -> dict[str, dict[str, Any]]:
    states = {
        "OPTION_A_ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY": "FINALIZED_ARCHIVED_SELECTED_PATH",
        "OPTION_B_DEFINE_OPERATOR_ACCEPTANCE_THRESHOLDS_FOR_EXPECTANCY_EVIDENCE": "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED",
        "OPTION_C_METHOD_IMPROVEMENT_CANDIDATE_FOR_MATERIALITY_AND_STABILITY": "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED",
        "OPTION_D_ADDITIONAL_OUT_OF_SAMPLE_OR_EXPANDED_UNIVERSE_EVIDENCE": "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED",
        "OPTION_E_VPA_WYCKOFF_RULE_REFINEMENT_CANDIDATE": "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED",
        "OPTION_F_ABSTENTION_AND_NO_TRADE_OBJECTIVE_REFINEMENT": "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED",
        "OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED": "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE",
        "OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE": "NOT_ALLOWED_CURRENTLY",
    }
    return {
        option_id: {
            "option_id": option_id,
            "status_after_final_summary": status,
            "research_only": True,
            "acceptance_authority_created": False,
            "runtime_authority_created": False,
        }
        for option_id, status in states.items()
    }


def per_ticker_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker final-summary entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_final_archive_summary_digest", None)
    return semantic_digest(payload)


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
            "source_archive_status": archive_service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
            "final_summary_status": "FINALIZED_ARCHIVED_NOT_READY",
            "selected_operator_option": archive_service.selection_service.SELECTED_OPERATOR_OPTION,
            "selected_operator_decision": archive_service.selection_service.SELECTED_OPERATOR_DECISION,
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
            "source_archive_digest": EXPECTED_SOURCE_ARCHIVE_RECORD_DIGEST,
            "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
            "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
            "source_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
            "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
            "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
            "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
            "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
            "final_summary_note": (
                "PRESERVE_META_LIMITATION_IN_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_final_archive_summary_digest"] = (
            per_ticker_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_summary(source_archive: Mapping[str, Any] | None) -> dict[str, Any]:
    execution = archive_service.selection_service.closure_service.readiness.reassessment.execution
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_EXPECTANCY_LAB_EVIDENCE_V1,
        "final_summary_status": MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "final_summary_decision": CURRENT_EXPECTANCY_LAB_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED,
        "final_summary_scope": PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_ONLY_NOT_REOPENING_NOT_ACCEPTANCE_NOT_RUNTIME,
        "created_offline": True, "research_only": True, "operator_review_required": False,
        "source_archive_record_artifact_kind": archive_service.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_archive_record_status": archive_service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_archive_record_decision": archive_service.ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY,
        "source_archive_record_scope": archive_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME,
        "source_archive_record_digest": EXPECTED_SOURCE_ARCHIVE_RECORD_DIGEST,
        "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": _source_evidence(source_archive),
        "selected_operator_option": archive_service.selection_service.SELECTED_OPERATOR_OPTION,
        "selected_operator_decision": archive_service.selection_service.SELECTED_OPERATOR_DECISION,
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
        "archive_record_created": True,
        "predictive_usefulness_acceptance_path_archived": True,
        "current_expectancy_lab_evidence_path_archived_not_ready": True,
        "final_archive_summary_created": True,
        "predictive_usefulness_chain_finalized": True,
        "current_expectancy_lab_evidence_path_finalized_archived_not_ready": True,
        "no_immediate_next_action_required_for_current_archived_path": True,
        "future_reopening_requires_new_operator_method_selection": True,
        "future_reopening_created": False,
        "operator_method_or_closure_selection_rerun_performed": False,
        "method_improvement_candidate_created": False, "new_evidence_candidate_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
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
        "provider_requests_made_in_final_summary": False,
        "live_provider_transport_enabled_in_final_summary": False,
        "market_data_acquisition_performed_in_final_summary": False,
        "dataset_generation_performed_in_final_summary": False,
        "canonical_dataset_regenerated_in_final_summary": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "archive_record_rerun_performed": False, "operator_selection_rerun_performed": False,
        "closure_rerun_performed": False, "acceptance_readiness_review_rerun_performed": False,
        "predictive_usefulness_reassessment_rerun_performed": False,
        "expectancy_backtest_lab_execution_rerun_performed": False,
        "expectancy_backtest_lab_results_review_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_rerun_performed": False, "target_generation_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "source_selected_option": archive_service.selection_service.SELECTED_OPERATOR_OPTION,
        "source_selected_decision": archive_service.selection_service.SELECTED_OPERATOR_DECISION,
        "source_archive_decision": archive_service.ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY,
        "source_readiness_decision": archive_service.selection_service.closure_service.readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_closure_classification": "COMPLETED_RESEARCH_ONLY",
        "source_archive_classification": "COMPLETED_RESEARCH_ONLY",
        "source_acceptance_path_status": "ARCHIVED_NOT_READY",
        "metric_materiality_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "per_ticker_stability_readiness": "REQUIRES_OPERATOR_REVIEW",
        "meta_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "source_matrix_row_count": 179190, "expectancy_backtest_lab_row_count": 179190,
        "evaluable_target_row_count": 177090, "unavailable_target_row_count": 2100,
        "embargoed_cross_split_forward_horizon_row_count": 4200,
        "aggregate_metric_eligible_row_count": 172890,
        "final_summary_classification": "COMPLETED_RESEARCH_ONLY",
        "current_evidence_path_status": "FINALIZED_ARCHIVED_NOT_READY",
        "archive_record_status": "ARCHIVED_SELECTED_PATH",
        "final_decision": "PREDICTIVE_USEFULNESS_NOT_ACCEPTED_FOR_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH",
        "acceptance_candidate_allowed": False, "acceptance_candidate_recommended": False,
        "predictive_usefulness_decision": "NOT_ACCEPTED",
        "profitability_decision": "NOT_ACCEPTED", "runtime_authority_status": NOT_AUTHORIZED,
        "immediate_next_required_action": "NONE_FOR_CURRENT_ARCHIVED_PATH",
        "future_reopening_requirement": "NEW_OPERATOR_METHOD_SELECTION_REQUIRED",
        "future_reopening_inherits_acceptance_authority": False,
        "future_reopening_inherits_profitability_authority": False,
        "future_reopening_inherits_runtime_authority": False,
        "completed_phases": _completed_phases(),
        "archived_options_summary": _archived_options(),
        "per_ticker_final_summary_entries": _per_ticker_entries(),
        "future_reopening_conditions": {
            "future_reopening_allowed": True,
            "future_reopening_requires_new_operator_method_selection": True,
            "future_reopening_requires_new_candidate_review_approval_chain": True,
            "future_reopening_requires_new_evidence_if_execution_selected": True,
            "future_reopening_requires_new_reassessment_and_readiness": True,
            "future_reopening_does_not_inherit_acceptance_authority": True,
            "future_reopening_does_not_inherit_profitability_authority": True,
            "future_reopening_does_not_inherit_runtime_authority": True,
        },
        "current_path_terminal_state": "FINALIZED_ARCHIVED_NOT_READY",
        "next_recommended_task": "NONE_FOR_CURRENT_ARCHIVED_PATH",
        "optional_future_task_if_reopened": "NEW_OPERATOR_METHOD_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE_OR_NEW_EVIDENCE_CONTEXT",
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and all(
        isinstance(entry, dict)
        and isinstance(entry.get("per_ticker_final_archive_summary_digest"), str)
        and entry["per_ticker_final_archive_summary_digest"]
        == per_ticker_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest_v1(entry)
        for entry in entries
    )


def _check_values(summary: Mapping[str, Any]) -> dict[str, bool]:
    entries = summary.get("per_ticker_final_summary_entries", [])
    phases = summary.get("completed_phases", [])
    options = summary.get("archived_options_summary", {})
    reopen = summary.get("future_reopening_conditions", {})
    option = lambda option_id: options.get(option_id, {}) if isinstance(options, dict) else {}
    rerun_fields = [
        "archive_record_rerun_performed", "operator_selection_rerun_performed",
        "closure_rerun_performed", "acceptance_readiness_review_rerun_performed",
        "predictive_usefulness_reassessment_rerun_performed",
        "expectancy_backtest_lab_execution_rerun_performed",
        "expectancy_backtest_lab_results_review_rerun_performed",
        "vpa_wyckoff_rule_baseline_execution_rerun_performed",
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "signal_feature_generation_rerun_performed", "target_generation_rerun_performed",
    ]
    values = {
        "source_archive_record_digest_bound": summary.get("source_archive_record_digest") == EXPECTED_SOURCE_ARCHIVE_RECORD_DIGEST,
        "source_operator_selection_digest_bound": summary.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": summary.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_acceptance_readiness_digest_bound": summary.get("source_acceptance_readiness_digest") == EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": summary.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": summary.get("source_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": summary.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": summary.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": summary.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_rows_digest_bound": summary.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest_bound": summary.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": summary.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": summary.get("target_universe") == TARGET_UNIVERSE and summary.get("target_universe_count") == 12,
        "records_digest_preserved": summary.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": summary.get("meta_record_count") == 913,
        "selected_option_option_a_bound": summary.get("selected_operator_option") == archive_service.selection_service.SELECTED_OPERATOR_OPTION,
        "selected_decision_archive_current_path_bound": summary.get("selected_operator_decision") == archive_service.selection_service.SELECTED_OPERATOR_DECISION,
        "archive_record_created_true": summary.get("archive_record_created") is True,
        "acceptance_path_archived_true": summary.get("predictive_usefulness_acceptance_path_archived") is True,
        "current_path_archived_not_ready_true": summary.get("current_expectancy_lab_evidence_path_archived_not_ready") is True,
        "final_archive_summary_created_true": summary.get("final_archive_summary_created") is True,
        "predictive_usefulness_chain_finalized_true": summary.get("predictive_usefulness_chain_finalized") is True,
        "current_path_finalized_archived_not_ready_true": summary.get("current_expectancy_lab_evidence_path_finalized_archived_not_ready") is True,
        "no_immediate_next_action_required_true": summary.get("no_immediate_next_action_required_for_current_archived_path") is True,
        "future_reopening_requires_new_operator_selection_true": summary.get("future_reopening_requires_new_operator_method_selection") is True,
        "future_reopening_created_false": summary.get("future_reopening_created") is False,
        "method_improvement_candidate_created_false": summary.get("method_improvement_candidate_created") is False,
        "new_evidence_candidate_created_false": summary.get("new_evidence_candidate_created") is False,
        "acceptance_candidate_created_false": summary.get("predictive_usefulness_acceptance_candidate_created") is False,
        "predictive_usefulness_not_accepted": summary.get("predictive_usefulness") == NOT_ACCEPTED,
        "predictive_usefulness_accepted_false": summary.get("predictive_usefulness_accepted") is False,
        "predictive_usefulness_acceptance_ready_false": summary.get("predictive_usefulness_acceptance_ready") is False,
        "predictive_usefulness_acceptance_recommended_false": summary.get("predictive_usefulness_acceptance_recommended") is False,
        "profitability_not_accepted": summary.get("profitability") == NOT_ACCEPTED and summary.get("profitability_accepted") is False,
        "runtime_not_authorized": summary.get("runtime_use") == NOT_AUTHORIZED and summary.get("runtime_migration_approved") is False,
        "strategy_not_authorized": summary.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": summary.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": summary.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": summary.get("trade_recommendations_generated") is False,
        "final_summary_classification_completed_research_only": summary.get("final_summary_classification") == "COMPLETED_RESEARCH_ONLY",
        "current_evidence_path_status_finalized_archived_not_ready": summary.get("current_evidence_path_status") == "FINALIZED_ARCHIVED_NOT_READY",
        "final_decision_predictive_usefulness_not_accepted": summary.get("final_decision") == "PREDICTIVE_USEFULNESS_NOT_ACCEPTED_FOR_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH",
        "future_reopening_does_not_inherit_acceptance_authority": reopen.get("future_reopening_does_not_inherit_acceptance_authority") is True,
        "future_reopening_does_not_inherit_profitability_authority": reopen.get("future_reopening_does_not_inherit_profitability_authority") is True,
        "future_reopening_does_not_inherit_runtime_authority": reopen.get("future_reopening_does_not_inherit_runtime_authority") is True,
        "completed_phases_present": isinstance(phases, list) and [row.get("phase_id") for row in phases] == COMPLETED_PHASE_IDS,
        "completed_phases_count_13": isinstance(phases, list) and len(phases) == 13,
        "option_a_finalized_archived_selected_path": option(archive_service.selection_service.SELECTED_OPERATOR_OPTION).get("status_after_final_summary") == "FINALIZED_ARCHIVED_SELECTED_PATH",
        "options_b_to_f_available_only_if_reopened": isinstance(options, dict) and all(row.get("status_after_final_summary") == "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED" for row in list(options.values())[1:6]),
        "option_g_blocked": option("OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED").get("status_after_final_summary") == "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE",
        "option_h_not_allowed": option("OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE").get("status_after_final_summary") == "NOT_ALLOWED_CURRENTLY",
        "source_backtest_lab_row_count_179190": summary.get("expectancy_backtest_lab_row_count") == 179190,
        "evaluable_target_row_count_177090": summary.get("evaluable_target_row_count") == 177090,
        "unavailable_target_row_count_2100": summary.get("unavailable_target_row_count") == 2100,
        "embargoed_cross_split_forward_horizon_row_count_4200": summary.get("embargoed_cross_split_forward_horizon_row_count") == 4200,
        "aggregate_metric_eligible_row_count_172890": summary.get("aggregate_metric_eligible_row_count") == 172890,
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12,
        "per_ticker_digests_present": _per_ticker_digests_valid(entries),
        "model_training_authorized_false": summary.get("model_training_authorized") is False,
        "model_training_performed_false": summary.get("model_training_performed") is False,
        "strategy_scoring_false": summary.get("strategy_scoring_performed") is False and summary.get("new_strategy_scoring_performed") is False,
        "provider_requests_made_false": summary.get("provider_requests_made_in_final_summary") is False,
        "market_data_acquisition_false": summary.get("market_data_acquisition_performed_in_final_summary") is False,
        "dataset_regeneration_false": summary.get("canonical_dataset_regenerated_in_final_summary") is False,
        "metric_recomputation_from_raw_rows_false": summary.get("metric_recomputation_from_raw_rows_performed") is False,
        "archive_record_rerun_false": summary.get("archive_record_rerun_performed") is False,
        "operator_selection_rerun_false": summary.get("operator_selection_rerun_performed") is False and summary.get("operator_method_or_closure_selection_rerun_performed") is False,
        "closure_rerun_false": summary.get("closure_rerun_performed") is False,
        "acceptance_readiness_review_rerun_false": summary.get("acceptance_readiness_review_rerun_performed") is False,
        "predictive_usefulness_reassessment_rerun_false": summary.get("predictive_usefulness_reassessment_rerun_performed") is False,
        "expectancy_backtest_lab_execution_rerun_false": summary.get("expectancy_backtest_lab_execution_rerun_performed") is False,
        "expectancy_backtest_lab_results_review_rerun_false": summary.get("expectancy_backtest_lab_results_review_rerun_performed") is False,
        "vpa_wyckoff_execution_rerun_false": summary.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": summary.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": summary.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": summary.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": summary.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": summary.get("target_generation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": summary.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": summary.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": summary.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": summary.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": summary.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": summary.get("no_tracked_marketflow_files") is True,
    }
    assert set(values) == set(REQUIRED_CHECK_IDS)
    assert all(summary.get(field) is False for field in rerun_fields)
    return values


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "final archive summary evidence matches" if actual else "final archive summary evidence mismatch",
    }


def _checklist(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(summary)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "final_archive_summary_created": True, "predictive_usefulness_chain_finalized": True,
        "current_expectancy_lab_evidence_path_finalized_archived_not_ready": True,
        "no_immediate_next_action_required_for_current_archived_path": True,
        "future_reopening_requires_new_operator_method_selection": True,
        "future_reopening_created": False, "method_improvement_candidate_created": False,
        "new_evidence_candidate_created": False, "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
        "next_recommended_task": "NONE_FOR_CURRENT_ARCHIVED_PATH",
    }


def marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest_v1(
    summary: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the final archive summary."""
    payload = deepcopy(dict(summary))
    payload.pop("final_summary_checklist", None)
    payload.pop("final_summary_checklist_summary", None)
    payload.pop("marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest", None)
    return semantic_digest(payload)


def build_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(
    *, source_archive: dict | None = None,
) -> dict:
    """Build the terminal summary without rerunning the source archive or evidence."""
    summary = _base_summary(source_archive)
    summary["final_summary_checklist"] = _checklist(summary)
    summary["final_summary_checklist_summary"] = _summary(summary["final_summary_checklist"])
    summary["marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest"] = (
        marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest_v1(summary)
    )
    validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(summary)
    return summary


def validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(
    summary: dict,
) -> dict:
    """Validate bindings, terminal disposition, and every closed authority gate."""
    if not isinstance(summary, dict):
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "summary must be an object"
        )
    expected = _base_summary(None)
    for field, value in expected.items():
        _expect(summary.get(field), value, field)
    entries = summary.get("per_ticker_final_summary_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "per-ticker final summary entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    if not _per_ticker_digests_valid(entries):
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "per-ticker final summary digest mismatch"
        )
    checklist = summary.get("final_summary_checklist")
    if not isinstance(checklist, list):
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "final summary checklist missing"
        )
    _expect(checklist, _checklist(summary), "final summary checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "final summary checklist failed"
        )
    _expect(summary.get("final_summary_checklist_summary"), _summary(checklist), "checklist summary")
    digest = summary.get(
        "marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "final summary digest missing"
        )
    _expect(
        digest,
        marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest_v1(summary),
        "final summary digest",
    )
    return {
        "status": MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_EXPECTANCY_LAB_EVIDENCE_VALID,
        "artifact_kind": summary["artifact_kind"],
        "final_summary_status": summary["final_summary_status"],
        "final_summary_decision": summary["final_summary_decision"],
        "marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest": digest,
        **{
            key: summary["final_summary_checklist_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_markdown_v1(
    summary: dict,
) -> str:
    """Render a sanitized Markdown view of the validated terminal summary."""
    validation = validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(summary)
    sections = [
        ("Title", ["MarketFlow Predictive-Usefulness Final Archive Summary Using Expectancy Lab Evidence v1"]),
        ("MarketFlow Predictive-Usefulness Final Archive Summary Using Expectancy Lab Evidence v1", [f"Artifact/status: `{summary['artifact_kind']}` / `{summary['final_summary_status']}`.", f"Digest: `{validation['marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest']}`."]),
        ("Source Archive Record", [f"`{summary['source_archive_record_artifact_kind']}` with digest `{summary['source_archive_record_digest']}`."]),
        ("Bound Evidence", [f"Selection/closure/readiness/reassessment: `{summary['source_operator_selection_digest']}` / `{summary['source_closure_digest']}` / `{summary['source_acceptance_readiness_digest']}` / `{summary['source_reassessment_digest']}`.", f"Rows/metrics: `{summary['source_backtest_rows_digest']}` / `{summary['source_metric_report_digest']}`."]),
        ("Dataset and Universe", [f"`{summary['dataset_name']}` has `{summary['total_canonical_record_count']}` records across `{summary['target_universe_count']}` tickers.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in summary["target_universe"]) + "."]),
        ("Final Summary Scope", [f"`{summary['final_summary_scope']}`; research-only and non-actionable."]),
        ("Final Summary Basis", [f"Option A is finalized after the archived-not-ready record; materiality/baseline/stability remain `{summary['metric_materiality_readiness']} / {summary['baseline_outperformance_readiness']} / {summary['per_ticker_stability_readiness']}`."]),
        ("Final Classification", [f"`{summary['final_summary_classification']}`; current path `{summary['current_evidence_path_status']}` and decision `{summary['final_decision']}`."]),
        ("Completed Phases", [f"{row['phase_number']}. `{row['phase_id']}`: `{row['phase_status']}`." for row in summary["completed_phases"]]),
        ("Archived Options Summary", [f"`{option_id}`: `{row['status_after_final_summary']}`." for option_id, row in summary["archived_options_summary"].items()]),
        ("Per-Ticker Final Summary", [f"`{row['ticker']}`: `{row['final_summary_status']}`, digest `{row['per_ticker_final_archive_summary_digest']}`." for row in summary["per_ticker_final_summary_entries"]]),
        ("META Limitation", ["META remains exactly 913 historical records, 13,695 lab rows, and 13,520 evaluable targets; the reduced-record limitation is preserved."]),
        ("Future Reopening Conditions", [f"`{key}`: `{value}`." for key, value in summary["future_reopening_conditions"].items()]),
        ("No Immediate Next Action", [f"Terminal state `{summary['current_path_terminal_state']}`; next task `{summary['next_recommended_task']}`."]),
        ("Next Chain", summary["next_chain"]), ("Next Gates", summary["next_gates"]),
        ("Risk Controls", summary["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate is created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{summary['final_summary_checklist_summary']['total_checks']} / {summary['final_summary_checklist_summary']['passed_checks']} / {summary['final_summary_checklist_summary']['failed_checks']} / {summary['final_summary_checklist_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, source rerun, raw-row metric recomputation, model training, scoring, recommendation, acceptance, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Predictive-Usefulness Final Archive Summary Using Expectancy Lab Evidence v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(
    output_dir: str | Path,
    *,
    source_archive: dict | None = None,
) -> dict:
    """Write canonical summary JSON without overwriting an existing record."""
    summary = build_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(
        source_archive=source_archive
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1.json"
    if path.exists():
        raise MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError(
            "final archive summary output already exists"
        )
    payload = canonical_json_bytes(summary)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": summary["artifact_kind"],
        "final_summary_status": summary["final_summary_status"],
        "final_summary_decision": summary["final_summary_decision"],
        "marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest": summary["marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
