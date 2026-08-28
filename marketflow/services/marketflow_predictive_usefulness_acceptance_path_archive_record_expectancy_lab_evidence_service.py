"""Offline archive record for the not-ready expectancy-lab acceptance path."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_service as selection_service,
)


ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE"
)
SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_EXPECTANCY_LAB_EVIDENCE_V1 = (
    "marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE"
)
ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY = (
    "ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_EXPECTANCY_LAB_EVIDENCE_VALID = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_EXPECTANCY_LAB_EVIDENCE_VALID"
)

EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = "867c7bef90986e0bc13620fb53dc88bdc7de0e9152969d8e3ab8bcf882db8894"
EXPECTED_SOURCE_CLOSURE_DIGEST = selection_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST = selection_service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = selection_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = selection_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_EXECUTION_DIGEST = selection_service.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = selection_service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = selection_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = selection_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_APPROVAL_DIGEST = selection_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = selection_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = selection_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = selection_service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = selection_service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = selection_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = selection_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = selection_service.EXPECTED_SOURCE_RECORDS_DIGEST

TARGET_UNIVERSE = list(selection_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(selection_service.EXPECTED_RECORD_COUNTS)
EXPECTED_LAB_ROW_COUNTS = dict(selection_service.EXPECTED_LAB_ROW_COUNTS)
EXPECTED_EVALUABLE_COUNTS = dict(selection_service.EXPECTED_EVALUABLE_COUNTS)
EXPECTED_UNAVAILABLE_COUNTS = dict(selection_service.EXPECTED_UNAVAILABLE_COUNTS)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

NEXT_CHAIN = [
    "MarketFlow Predictive-Usefulness Final Archive Summary Using Expectancy Lab Evidence v1.",
    "No immediate further action is required for the current archived path.",
    "Future reopening only by a new operator method-selection artifact.",
    "Optional future method/evidence improvement candidate only if separately selected later.",
    "New evidence chain only if separately approved later.",
    "Reassessment/readiness rerun only after new evidence.",
    "Predictive-usefulness acceptance candidate only if a future readiness review passes.",
    "Profitability review only after predictive usefulness is separately accepted.",
    "Runtime migration only if ever separately authorized.",
]

NEXT_GATES = [
    "marketflow_predictive_usefulness_final_archive_summary_using_expectancy_lab_evidence",
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
    "archive_does_not_create_final_summary",
    "archive_does_not_create_method_improvement_candidate",
    "archive_does_not_create_new_evidence_candidate",
    "archive_does_not_create_acceptance_candidate",
    "archive_does_not_accept_predictive_usefulness",
    "archive_does_not_accept_profitability",
    "archive_does_not_authorize_runtime",
    "archive_does_not_authorize_strategy",
    "archive_does_not_authorize_paper_trading",
    "archive_does_not_authorize_broker_execution",
    "archive_does_not_generate_trade_recommendations",
    "archive_does_not_train_models",
    "archive_does_not_score_strategy",
    "archive_does_not_call_providers",
    "archive_does_not_acquire_market_data",
    "archive_does_not_recompute_metrics_from_raw_rows",
    "archive_does_not_rerun_operator_selection",
    "archive_does_not_rerun_closure",
    "archive_does_not_rerun_acceptance_readiness_review",
    "archive_does_not_rerun_predictive_usefulness_reassessment",
    "archive_does_not_rerun_expectancy_backtest_lab_execution",
    "archive_does_not_rerun_expectancy_backtest_lab_results_review",
    "archive_does_not_rerun_vpa_wyckoff_execution",
    "archive_does_not_rerun_vpa_wyckoff_results_review",
    "archive_does_not_rerun_feature_label_matrix_execution",
    "archive_does_not_rerun_feature_label_matrix_results_review",
    "archive_does_not_rerun_signal_feature_generation",
    "archive_does_not_rerun_target_generation",
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
    "source_operator_selection_digest_bound", "source_closure_digest_bound",
    "source_acceptance_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_results_review_digest_bound", "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound", "source_vpa_wyckoff_rule_values_digest_bound",
    "source_matrix_rows_digest_bound", "source_target_values_digest_bound",
    "records_digest_bound", "target_universe_12_preserved", "records_digest_preserved",
    "meta_913_preserved", "selected_option_option_a_bound",
    "selected_decision_archive_current_path_bound", "archive_record_created_true",
    "acceptance_path_archived_true", "current_path_archived_not_ready_true",
    "ready_for_final_archive_summary_true", "final_archive_summary_created_false",
    "method_improvement_candidate_created_false", "new_evidence_candidate_created_false",
    "acceptance_candidate_created_false", "predictive_usefulness_not_accepted",
    "predictive_usefulness_accepted_false", "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "paper_trading_not_authorized",
    "broker_not_authorized", "trade_recommendations_false",
    "archive_classification_completed_research_only",
    "current_acceptance_path_status_archived_not_ready",
    "archive_record_status_archived_selected_path",
    "future_reopening_requires_new_operator_selection", "option_a_archived_selected_path",
    "options_b_to_f_available_only_if_reopened", "option_g_blocked", "option_h_not_allowed",
    "source_backtest_lab_row_count_179190", "evaluable_target_row_count_177090",
    "unavailable_target_row_count_2100", "embargoed_cross_split_forward_horizon_row_count_4200",
    "aggregate_metric_eligible_row_count_172890", "per_ticker_entries_12",
    "per_ticker_digests_present", "model_training_authorized_false",
    "model_training_performed_false", "strategy_scoring_false", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "metric_recomputation_from_raw_rows_false", "operator_selection_rerun_false",
    "closure_rerun_false", "acceptance_readiness_review_rerun_false",
    "predictive_usefulness_reassessment_rerun_false",
    "expectancy_backtest_lab_execution_rerun_false",
    "expectancy_backtest_lab_results_review_rerun_false", "vpa_wyckoff_execution_rerun_false",
    "vpa_wyckoff_results_review_rerun_false", "matrix_execution_rerun_false",
    "matrix_results_review_rerun_false", "signal_feature_generation_rerun_false",
    "target_generation_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(ValueError):
    """Raised when the archive record violates its evidence or authority contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            f"{field} mismatch"
        )


def _validate_source_selection(source_selection: Mapping[str, Any]) -> None:
    if not isinstance(source_selection, dict):
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "source_selection must be an object"
        )
    try:
        selection_service.validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
            source_selection
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "source operator selection is invalid"
        ) from exc
    if source_selection.get(
        "marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest"
    ) != EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST:
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "source operator-selection digest mismatch"
        )


def _source_evidence(source_selection: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_selection is not None:
        _validate_source_selection(source_selection)
        return deepcopy(source_selection["source_evidence"])
    return selection_service._source_evidence(None)


def _archived_options() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for option_id, source in selection_service._selection_options().items():
        if option_id == selection_service.SELECTED_OPERATOR_OPTION:
            status = "ARCHIVED_SELECTED_PATH"
        elif option_id.startswith(("OPTION_B_", "OPTION_C_", "OPTION_D_", "OPTION_E_", "OPTION_F_")):
            status = "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED"
        elif option_id.startswith("OPTION_G_"):
            status = "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE"
        else:
            status = "NOT_ALLOWED_CURRENTLY"
        rows[option_id] = {
            "option_id": option_id,
            "source_status_after_selection": source["status_after_selection"],
            "status_after_archive": status,
            "archived_selected_path": option_id == selection_service.SELECTED_OPERATOR_OPTION,
            "future_reopening_selection_required": option_id != selection_service.SELECTED_OPERATOR_OPTION,
            "acceptance_candidate_created": False,
            "runtime_authority_created": False,
            "research_only": True,
            "non_actionable": True,
        }
    return rows


def per_ticker_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker archive entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_acceptance_path_archive_record_digest", None)
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
            "source_operator_selection_status": selection_service.MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_EXPECTANCY_LAB_EVIDENCE,
            "archive_status": "ARCHIVED_NOT_READY",
            "selected_operator_option": selection_service.SELECTED_OPERATOR_OPTION,
            "selected_operator_decision": selection_service.SELECTED_OPERATOR_DECISION,
            "backtest_lab_row_count": EXPECTED_LAB_ROW_COUNTS[ticker],
            "evaluable_target_row_count": EXPECTED_EVALUABLE_COUNTS[ticker],
            "unavailable_target_row_count": EXPECTED_UNAVAILABLE_COUNTS[ticker],
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_accepted": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_recommended": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
            "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
            "source_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
            "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
            "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
            "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
            "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
            "archive_note": (
                "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_acceptance_path_archive_record_digest"] = (
            per_ticker_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_archive(source_selection: Mapping[str, Any] | None) -> dict[str, Any]:
    execution = selection_service.closure_service.readiness.reassessment.execution
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_EXPECTANCY_LAB_EVIDENCE_V1,
        "archive_status": MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "archive_decision": ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY,
        "archive_scope": PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME,
        "created_offline": True, "research_only": True, "operator_review_required": False,
        "source_operator_selection_artifact_kind": selection_service.ARTIFACT_KIND_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_operator_selection_status": selection_service.MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_operator_selection_scope": selection_service.OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY_NOT_ARCHIVE_NOT_ACCEPTANCE_NOT_RUNTIME,
        "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_expectancy_backtest_lab_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_expectancy_backtest_lab_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_expectancy_backtest_lab_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": _source_evidence(source_selection),
        "selected_operator_option": selection_service.SELECTED_OPERATOR_OPTION,
        "selected_operator_decision": selection_service.SELECTED_OPERATOR_DECISION,
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
        "operator_method_or_closure_selection_created": True,
        "operator_method_or_closure_selection_completed": True,
        "archive_record_created": True,
        "predictive_usefulness_acceptance_path_archived": True,
        "current_expectancy_lab_evidence_path_archived_not_ready": True,
        "ready_for_marketflow_predictive_usefulness_final_archive_summary_using_expectancy_lab_evidence": True,
        "final_archive_summary_created": False,
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
        "provider_requests_made_in_archive": False,
        "live_provider_transport_enabled_in_archive": False,
        "market_data_acquisition_performed_in_archive": False,
        "dataset_generation_performed_in_archive": False,
        "canonical_dataset_regenerated_in_archive": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "operator_selection_rerun_performed": False, "closure_rerun_performed": False,
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
        "source_selected_option": selection_service.SELECTED_OPERATOR_OPTION,
        "source_selected_decision": selection_service.SELECTED_OPERATOR_DECISION,
        "source_closure_recommended_current_decision": selection_service.SELECTED_OPERATOR_OPTION,
        "source_readiness_decision": selection_service.closure_service.readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_closure_classification": "COMPLETED_RESEARCH_ONLY",
        "source_acceptance_path_status": "CLOSED_NOT_READY",
        "metric_materiality_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "per_ticker_stability_readiness": "REQUIRES_OPERATOR_REVIEW",
        "meta_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "source_matrix_row_count": 179190, "expectancy_backtest_lab_row_count": 179190,
        "evaluable_target_row_count": 177090, "unavailable_target_row_count": 2100,
        "embargoed_cross_split_forward_horizon_row_count": 4200,
        "aggregate_metric_eligible_row_count": 172890,
        "archive_classification": "COMPLETED_RESEARCH_ONLY",
        "current_acceptance_path_status": "ARCHIVED_NOT_READY",
        "archive_record_status": "ARCHIVED_SELECTED_PATH",
        "acceptance_candidate_allowed": False, "acceptance_candidate_recommended": False,
        "predictive_usefulness_decision": "NOT_ACCEPTED",
        "profitability_decision": "NOT_ACCEPTED", "runtime_authority_status": NOT_AUTHORIZED,
        "archive_reason": "OPERATOR_SELECTED_OPTION_A_AFTER_NOT_READY_EXPECTANCY_LAB_EVIDENCE_PATH",
        "future_reopening_requirement": "NEW_OPERATOR_METHOD_SELECTION_REQUIRED",
        "immediate_next_required_action": "NONE_FOR_CURRENT_ARCHIVED_PATH",
        "next_artifact_ready": "MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE",
        "next_artifact_created": False,
        "archived_options": _archived_options(),
        "per_ticker_archive_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and all(
        isinstance(row, dict)
        and row.get("per_ticker_acceptance_path_archive_record_digest")
        == per_ticker_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest_v1(row)
        for row in entries
    )


def _check_values(archive: Mapping[str, Any]) -> dict[str, bool]:
    options = archive.get("archived_options")
    entries = archive.get("per_ticker_archive_entries")
    option = lambda key: options.get(key, {}) if isinstance(options, dict) else {}
    return {
        "source_operator_selection_digest_bound": archive.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": archive.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_acceptance_readiness_digest_bound": archive.get("source_acceptance_readiness_digest") == EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": archive.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": archive.get("source_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": archive.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": archive.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": archive.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_rows_digest_bound": archive.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest_bound": archive.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": archive.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": archive.get("target_universe") == TARGET_UNIVERSE and archive.get("target_universe_count") == 12,
        "records_digest_preserved": archive.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": archive.get("meta_record_count") == 913,
        "selected_option_option_a_bound": archive.get("selected_operator_option") == selection_service.SELECTED_OPERATOR_OPTION,
        "selected_decision_archive_current_path_bound": archive.get("selected_operator_decision") == selection_service.SELECTED_OPERATOR_DECISION,
        "archive_record_created_true": archive.get("archive_record_created") is True,
        "acceptance_path_archived_true": archive.get("predictive_usefulness_acceptance_path_archived") is True,
        "current_path_archived_not_ready_true": archive.get("current_expectancy_lab_evidence_path_archived_not_ready") is True,
        "ready_for_final_archive_summary_true": archive.get("ready_for_marketflow_predictive_usefulness_final_archive_summary_using_expectancy_lab_evidence") is True,
        "final_archive_summary_created_false": archive.get("final_archive_summary_created") is False,
        "method_improvement_candidate_created_false": archive.get("method_improvement_candidate_created") is False,
        "new_evidence_candidate_created_false": archive.get("new_evidence_candidate_created") is False,
        "acceptance_candidate_created_false": archive.get("predictive_usefulness_acceptance_candidate_created") is False,
        "predictive_usefulness_not_accepted": archive.get("predictive_usefulness") == NOT_ACCEPTED,
        "predictive_usefulness_accepted_false": archive.get("predictive_usefulness_accepted") is False,
        "predictive_usefulness_acceptance_ready_false": archive.get("predictive_usefulness_acceptance_ready") is False,
        "predictive_usefulness_acceptance_recommended_false": archive.get("predictive_usefulness_acceptance_recommended") is False,
        "profitability_not_accepted": archive.get("profitability") == NOT_ACCEPTED and archive.get("profitability_accepted") is False,
        "runtime_not_authorized": archive.get("runtime_use") == NOT_AUTHORIZED and archive.get("runtime_migration_approved") is False,
        "strategy_not_authorized": archive.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": archive.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": archive.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": archive.get("trade_recommendations_generated") is False,
        "archive_classification_completed_research_only": archive.get("archive_classification") == "COMPLETED_RESEARCH_ONLY",
        "current_acceptance_path_status_archived_not_ready": archive.get("current_acceptance_path_status") == "ARCHIVED_NOT_READY",
        "archive_record_status_archived_selected_path": archive.get("archive_record_status") == "ARCHIVED_SELECTED_PATH",
        "future_reopening_requires_new_operator_selection": archive.get("future_reopening_requirement") == "NEW_OPERATOR_METHOD_SELECTION_REQUIRED",
        "option_a_archived_selected_path": option(selection_service.SELECTED_OPERATOR_OPTION).get("status_after_archive") == "ARCHIVED_SELECTED_PATH",
        "options_b_to_f_available_only_if_reopened": isinstance(options, dict) and all(row.get("status_after_archive") == "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED" for row in list(options.values())[1:6]),
        "option_g_blocked": option("OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED").get("status_after_archive") == "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE",
        "option_h_not_allowed": option("OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE").get("status_after_archive") == "NOT_ALLOWED_CURRENTLY",
        "source_backtest_lab_row_count_179190": archive.get("expectancy_backtest_lab_row_count") == 179190,
        "evaluable_target_row_count_177090": archive.get("evaluable_target_row_count") == 177090,
        "unavailable_target_row_count_2100": archive.get("unavailable_target_row_count") == 2100,
        "embargoed_cross_split_forward_horizon_row_count_4200": archive.get("embargoed_cross_split_forward_horizon_row_count") == 4200,
        "aggregate_metric_eligible_row_count_172890": archive.get("aggregate_metric_eligible_row_count") == 172890,
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12,
        "per_ticker_digests_present": _per_ticker_digests_valid(entries),
        "model_training_authorized_false": archive.get("model_training_authorized") is False,
        "model_training_performed_false": archive.get("model_training_performed") is False,
        "strategy_scoring_false": archive.get("strategy_scoring_performed") is False and archive.get("new_strategy_scoring_performed") is False,
        "provider_requests_made_false": archive.get("provider_requests_made_in_archive") is False,
        "market_data_acquisition_false": archive.get("market_data_acquisition_performed_in_archive") is False,
        "dataset_regeneration_false": archive.get("canonical_dataset_regenerated_in_archive") is False,
        "metric_recomputation_from_raw_rows_false": archive.get("metric_recomputation_from_raw_rows_performed") is False,
        "operator_selection_rerun_false": archive.get("operator_selection_rerun_performed") is False,
        "closure_rerun_false": archive.get("closure_rerun_performed") is False,
        "acceptance_readiness_review_rerun_false": archive.get("acceptance_readiness_review_rerun_performed") is False,
        "predictive_usefulness_reassessment_rerun_false": archive.get("predictive_usefulness_reassessment_rerun_performed") is False,
        "expectancy_backtest_lab_execution_rerun_false": archive.get("expectancy_backtest_lab_execution_rerun_performed") is False,
        "expectancy_backtest_lab_results_review_rerun_false": archive.get("expectancy_backtest_lab_results_review_rerun_performed") is False,
        "vpa_wyckoff_execution_rerun_false": archive.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": archive.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": archive.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": archive.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": archive.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": archive.get("target_generation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": archive.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": archive.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": archive.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": archive.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": archive.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": archive.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "archive evidence matches" if actual else "archive evidence mismatch",
    }


def _checklist(archive: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(archive)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "archive_record_created": True,
        "predictive_usefulness_acceptance_path_archived": True,
        "current_expectancy_lab_evidence_path_archived_not_ready": True,
        "ready_for_marketflow_predictive_usefulness_final_archive_summary_using_expectancy_lab_evidence": True,
        "final_archive_summary_created": False,
        "method_improvement_candidate_created": False, "new_evidence_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
        "next_recommended_task": "MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE_V1",
    }


def marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest_v1(
    archive: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the archive record."""
    payload = deepcopy(dict(archive))
    payload.pop("archive_checklist", None)
    payload.pop("archive_summary", None)
    payload.pop("marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest", None)
    return semantic_digest(payload)


def build_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(
    *, source_selection: dict | None = None,
) -> dict:
    """Build the archive record without rerunning the source selection or evidence."""
    archive = _base_archive(source_selection)
    archive["archive_checklist"] = _checklist(archive)
    archive["archive_summary"] = _summary(archive["archive_checklist"])
    archive["marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest"] = (
        marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest_v1(archive)
    )
    validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(archive)
    return archive


def validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(
    archive: dict,
) -> dict:
    """Validate evidence bindings, archived disposition, and closed authority gates."""
    if not isinstance(archive, dict):
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "archive must be an object"
        )
    expected = _base_archive(None)
    for field, value in expected.items():
        _expect(archive.get(field), value, field)
    entries = archive.get("per_ticker_archive_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "per-ticker archive entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    if not _per_ticker_digests_valid(entries):
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "per-ticker archive digest mismatch"
        )
    checklist = archive.get("archive_checklist")
    if not isinstance(checklist, list):
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "archive checklist missing"
        )
    _expect(checklist, _checklist(archive), "archive checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "archive checklist failed"
        )
    _expect(archive.get("archive_summary"), _summary(checklist), "archive summary")
    digest = archive.get(
        "marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "archive digest missing"
        )
    _expect(
        digest,
        marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest_v1(archive),
        "archive digest",
    )
    return {
        "status": MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_EXPECTANCY_LAB_EVIDENCE_VALID,
        "artifact_kind": archive["artifact_kind"], "archive_status": archive["archive_status"],
        "archive_decision": archive["archive_decision"],
        "marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest": digest,
        **{
            key: archive["archive_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_markdown_v1(
    archive: dict,
) -> str:
    """Render a sanitized Markdown view of the validated archive record."""
    validation = validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(archive)
    sections = [
        ("Title", ["Predictive-Usefulness Acceptance Path Archive Record Using Expectancy Lab Evidence v1"]),
        ("Predictive-Usefulness Acceptance Path Archive Record Using Expectancy Lab Evidence v1", [f"Artifact/status: `{archive['artifact_kind']}` / `{archive['archive_status']}`.", f"Digest: `{validation['marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest']}`."]),
        ("Source Operator Selection", [f"Selected option/decision: `{archive['selected_operator_option']}` / `{archive['selected_operator_decision']}`.", f"Digest: `{archive['source_operator_selection_digest']}`."]),
        ("Bound Evidence", [f"Closure/readiness/reassessment: `{archive['source_closure_digest']}` / `{archive['source_acceptance_readiness_digest']}` / `{archive['source_reassessment_digest']}`.", f"Rows/metrics: `{archive['source_backtest_rows_digest']}` / `{archive['source_metric_report_digest']}`."]),
        ("Dataset and Universe", [f"`{archive['dataset_name']}` has `{archive['total_canonical_record_count']}` records across `{archive['target_universe_count']}` tickers.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in archive["target_universe"]) + "."]),
        ("Archive Scope", [f"`{archive['archive_scope']}`; research-only and non-actionable."]),
        ("Archive Basis", [f"The selected Option A path was closed not ready before archive; materiality/baseline/stability remain `{archive['metric_materiality_readiness']} / {archive['baseline_outperformance_readiness']} / {archive['per_ticker_stability_readiness']}`."]),
        ("Archive Classification", [f"`{archive['archive_classification']}`; current path `{archive['current_acceptance_path_status']}`."]),
        ("Archived Options", [f"`{option_id}`: `{row['status_after_archive']}`." for option_id, row in archive["archived_options"].items()]),
        ("Per-Ticker Archive", [f"`{row['ticker']}`: `{row['archive_status']}`, digest `{row['per_ticker_acceptance_path_archive_record_digest']}`." for row in archive["per_ticker_archive_entries"]]),
        ("META Limitation", ["META remains exactly 913 historical records and its reduced-record limitation is preserved."]),
        ("Future Reopening Conditions", [f"`{archive['future_reopening_requirement']}`; no immediate action is required for the archived path."]),
        ("Next Chain", archive["next_chain"]), ("Next Gates", archive["next_gates"]),
        ("Risk Controls", archive["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate is created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{archive['archive_summary']['total_checks']} / {archive['archive_summary']['passed_checks']} / {archive['archive_summary']['failed_checks']} / {archive['archive_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, source rerun, raw-row metric recomputation, model training, scoring, recommendation, acceptance, final summary, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# Predictive-Usefulness Acceptance Path Archive Record Using Expectancy Lab Evidence v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(
    output_dir: str | Path,
    *,
    source_selection: dict | None = None,
) -> dict:
    """Write canonical archive JSON without overwriting an existing record."""
    archive = build_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(
        source_selection=source_selection
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1.json"
    if path.exists():
        raise MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError(
            "archive output already exists"
        )
    payload = canonical_json_bytes(archive)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": archive["artifact_kind"],
        "archive_status": archive["archive_status"], "archive_decision": archive["archive_decision"],
        "marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest": archive["marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
