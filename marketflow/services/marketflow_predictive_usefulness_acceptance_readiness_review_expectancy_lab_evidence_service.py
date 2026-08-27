"""Offline acceptance-readiness review using reassessed expectancy-lab evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_predictive_usefulness_reassessment_expectancy_lab_evidence_service as reassessment,
)


ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE"
)
SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_V1 = (
    "marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_COMPLETED = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_COMPLETED"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME"
)
READINESS_DECISION_REASON = (
    "REASSESSMENT_RECOMMENDS_DO_NOT_ACCEPT_AND_ACCEPTANCE_MATERIALITY_STABILITY_AND_OPERATOR_THRESHOLDS_REMAIN_NOT_READY"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_VALID = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_VALID"
)

EXPECTED_SOURCE_REASSESSMENT_DIGEST = "7befe5693744d4b44aa8243270d43bfb7727ae324bc911a2cf5c68bc9ad86bd7"
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = reassessment.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_EXECUTION_DIGEST = reassessment.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = reassessment.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = reassessment.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = reassessment.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_APPROVAL_DIGEST = reassessment.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = reassessment.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = reassessment.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = reassessment.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = reassessment.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = reassessment.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = reassessment.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = reassessment.EXPECTED_SOURCE_RECORDS_DIGEST

TARGET_UNIVERSE = list(reassessment.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(reassessment.EXPECTED_RECORD_COUNTS)
EXPECTED_LAB_ROW_COUNTS = dict(reassessment.EXPECTED_LAB_ROW_COUNTS)
EXPECTED_EVALUABLE_COUNTS = dict(reassessment.EXPECTED_EVALUABLE_COUNTS)
EXPECTED_UNAVAILABLE_COUNTS = dict(reassessment.EXPECTED_UNAVAILABLE_COUNTS)
EXPECTED_AGGREGATE_ELIGIBLE_PER_TICKER = dict(reassessment.EXPECTED_AGGREGATE_ELIGIBLE_PER_TICKER)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CRITERIA_POLICY = {
    "CRITERION_SOURCE_EVIDENCE_INTEGRITY": ("PASS", "Bound source digests match the reassessment evidence."),
    "CRITERION_SOURCE_OUTPUT_INTEGRITY": ("PASS", "The reviewed output set has zero digest mismatches."),
    "CRITERION_NO_PEEK_AND_LEAKAGE": ("PASS", "Reviewed no-peek and leakage controls pass."),
    "CRITERION_CHRONOLOGY_AND_EMBARGO": ("PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS", "Chronological splits and reviewed embargo exclusions are preserved."),
    "CRITERION_METRIC_REPORT_PRESENT": ("PASS", "The research-only metric report is present and reviewed."),
    "CRITERION_BASELINE_COMPARISON_PRESENT": ("PASS", "The research-only baseline comparison is present and reviewed."),
    "CRITERION_VPA_WYCKOFF_ALIGNMENT_PRESENT": ("PASS", "The VPA/Wyckoff alignment report is present and reviewed."),
    "CRITERION_ABSTENTION_QUALITY_PRESENT": ("PASS", "The abstention quality report is present and reviewed."),
    "CRITERION_META_LIMITATION_AWARENESS": ("PASS_WITH_OPERATOR_AWARENESS", "META remains limited to 913 records."),
    "CRITERION_PER_TICKER_STABILITY": ("REQUIRES_OPERATOR_REVIEW", "Per-ticker stability requires operator review."),
    "CRITERION_METRIC_MATERIALITY_FOR_ACCEPTANCE": ("FAIL_OR_NOT_MET", "Acceptance materiality is not established by the reassessment."),
    "CRITERION_BASELINE_OUTPERFORMANCE_MATERIALITY": ("FAIL_OR_NOT_MET", "Material baseline outperformance is not established."),
    "CRITERION_ACCEPTANCE_THRESHOLD_DEFINED": ("FAIL_OR_NOT_MET", "No acceptance threshold has been defined and approved."),
    "CRITERION_SOURCE_REASSESSMENT_RECOMMENDATION": ("FAIL_OR_NOT_MET", "SOURCE_REASSESSMENT_RECOMMENDS_DO_NOT_ACCEPT_AT_REASSESSMENT_STAGE"),
    "CRITERION_PROFITABILITY_BOUNDARY": ("PASS_CLOSED_BOUNDARY", "Profitability remains not accepted and outside this review."),
    "CRITERION_RUNTIME_BOUNDARY": ("PASS_CLOSED_BOUNDARY", "Runtime and trading authority remain closed."),
}

NEXT_CHAIN = [
    "Predictive-Usefulness Not-Ready Closure and Method Planning Tree Using Expectancy Lab Evidence v1.",
    "Operator method-or-closure selection if a future operator chooses to continue or archive.",
    "Optional future method/evidence improvement candidate only if separately selected.",
    "New evidence chain only if separately approved.",
    "Reassessment and readiness rerun only after new evidence.",
    "Predictive-usefulness acceptance candidate only if future readiness passes.",
    "Profitability review only after predictive usefulness is separately accepted.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "predictive_usefulness_not_ready_closure_method_tree_using_expectancy_lab_evidence",
    "operator_method_or_closure_selection_if_required",
    "optional_future_method_or_evidence_improvement_candidate",
    "new_evidence_chain_if_separately_approved",
    "future_predictive_usefulness_reassessment_rerun",
    "future_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_if_predictive_usefulness_accepted",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "readiness_review_does_not_accept_predictive_usefulness",
    "readiness_review_does_not_create_acceptance_candidate",
    "readiness_review_does_not_accept_profitability",
    "readiness_review_does_not_authorize_runtime",
    "readiness_review_does_not_authorize_strategy",
    "readiness_review_does_not_authorize_paper_trading",
    "readiness_review_does_not_authorize_broker_execution",
    "readiness_review_does_not_generate_trade_recommendations",
    "readiness_review_does_not_train_models", "readiness_review_does_not_score_strategy",
    "readiness_review_does_not_call_providers", "readiness_review_does_not_acquire_market_data",
    "readiness_review_does_not_recompute_metrics_from_raw_rows",
    "readiness_review_does_not_rerun_predictive_usefulness_reassessment",
    "readiness_review_does_not_rerun_expectancy_backtest_lab_execution",
    "readiness_review_does_not_rerun_expectancy_backtest_lab_results_review",
    "readiness_review_does_not_rerun_vpa_wyckoff_execution",
    "readiness_review_does_not_rerun_vpa_wyckoff_results_review",
    "readiness_review_does_not_rerun_feature_label_matrix_execution",
    "readiness_review_does_not_rerun_feature_label_matrix_results_review",
    "readiness_review_does_not_rerun_signal_feature_generation",
    "readiness_review_does_not_rerun_target_generation",
    "do_not_mutate_frozen_dataset", "do_not_mutate_expectancy_backtest_lab_outputs",
    "do_not_mutate_vpa_wyckoff_outputs", "do_not_mutate_matrix_outputs",
    "do_not_mutate_signal_or_feature_outputs", "do_not_mutate_target_outputs",
    "do_not_mutate_redesigned_label_outputs", "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs", "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_reassessment_digest_bound", "source_results_review_digest_bound",
    "source_execution_digest_bound", "source_output_binding_digest_bound",
    "source_backtest_rows_digest_bound", "source_metric_report_digest_bound",
    "source_approval_digest_bound", "source_candidate_review_digest_bound",
    "source_candidate_digest_bound", "source_vpa_wyckoff_results_review_digest_bound",
    "source_vpa_wyckoff_rule_values_digest_bound", "source_matrix_rows_digest_bound",
    "source_target_values_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "selected_backtest_lab_package_preserved", "selected_vpa_wyckoff_package_preserved",
    "selected_matrix_package_preserved", "selected_matrix_layout_preserved",
    "selected_feature_package_preserved", "selected_target_package_preserved",
    "selected_objective_path_preserved", "source_reassessment_ready_true",
    "acceptance_readiness_review_created_true", "acceptance_readiness_review_completed_true",
    "readiness_decision_not_ready", "ready_for_acceptance_candidate_false",
    "ready_for_not_ready_closure_or_method_selection_true", "acceptance_candidate_created_false",
    "predictive_usefulness_not_accepted", "predictive_usefulness_accepted_false",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "paper_trading_not_authorized",
    "broker_not_authorized", "trade_recommendations_false",
    "source_backtest_lab_row_count_179190", "evaluable_target_row_count_177090",
    "unavailable_target_row_count_2100",
    "embargoed_cross_split_forward_horizon_row_count_4200",
    "aggregate_metric_eligible_row_count_172890", "approved_metric_family_count_13",
    "blocked_metric_family_count_1", "approved_baseline_count_6",
    "blocked_baseline_count_1", "evidence_integrity_pass", "source_output_integrity_pass",
    "no_peek_and_leakage_pass", "chronology_and_embargo_pass_with_reviewed_exclusions",
    "metric_report_present_pass", "baseline_comparison_present_pass",
    "vpa_wyckoff_alignment_present_pass", "abstention_quality_present_pass",
    "meta_limitation_awareness_pass_with_operator_awareness",
    "per_ticker_stability_requires_operator_review", "metric_materiality_not_ready",
    "baseline_outperformance_materiality_not_ready", "acceptance_threshold_defined_not_ready",
    "source_reassessment_recommendation_do_not_accept", "readiness_criteria_16_present",
    "readiness_findings_present", "per_ticker_entries_12", "per_ticker_digests_present",
    "model_training_authorized_false", "model_training_performed_false",
    "strategy_scoring_false", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "metric_recomputation_from_raw_rows_false", "predictive_usefulness_reassessment_rerun_false",
    "expectancy_backtest_lab_execution_rerun_false",
    "expectancy_backtest_lab_results_review_rerun_false", "vpa_wyckoff_execution_rerun_false",
    "vpa_wyckoff_results_review_rerun_false", "matrix_execution_rerun_false",
    "matrix_results_review_rerun_false", "signal_feature_generation_rerun_false",
    "target_generation_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(ValueError):
    """Raised when the conservative readiness review is invalid."""


def _validate_source_reassessment(source: Mapping[str, Any]) -> None:
    if not isinstance(source, dict):
        raise MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(
            "source_reassessment must be an object"
        )
    reassessment.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(source)
    if source.get("marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest") != EXPECTED_SOURCE_REASSESSMENT_DIGEST:
        raise MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(
            "source reassessment digest mismatch"
        )


def _criteria() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for criterion_id, (finding, reason) in CRITERIA_POLICY.items():
        rows[criterion_id] = {
            "criterion_id": criterion_id,
            "criterion_status": "REVIEWED_RESEARCH_ONLY",
            "finding": finding,
            "acceptance_ready_contribution": finding in {"PASS", "PASS_WITH_OPERATOR_AWARENESS", "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS"},
            "reason": reason,
            "research_only": True,
            "non_actionable": True,
        }
    return rows


def per_ticker_acceptance_readiness_review_digest_v1(entry: Mapping[str, Any]) -> str:
    """Return the deterministic digest for one ticker readiness entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_acceptance_readiness_review_digest", None)
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
            "source_reassessment_status": reassessment.MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE_READY,
            "acceptance_readiness_review_status": "REVIEWED_RESEARCH_ONLY",
            "acceptance_readiness_decision": "NOT_READY",
            "selected_backtest_lab_package": reassessment.execution.SELECTED_BACKTEST_LAB_PACKAGE,
            "selected_vpa_wyckoff_package": reassessment.execution.SELECTED_VPA_WYCKOFF_PACKAGE,
            "selected_matrix_package": reassessment.execution.SELECTED_MATRIX_PACKAGE,
            "selected_feature_package": reassessment.execution.SELECTED_FEATURE_PACKAGE,
            "selected_label_target_package": reassessment.execution.SELECTED_LABEL_TARGET_PACKAGE,
            "selected_objective_path": reassessment.execution.SELECTED_OBJECTIVE_PATH,
            "backtest_lab_row_count": EXPECTED_LAB_ROW_COUNTS[ticker],
            "evaluable_target_row_count": EXPECTED_EVALUABLE_COUNTS[ticker],
            "unavailable_target_row_count": EXPECTED_UNAVAILABLE_COUNTS[ticker],
            "aggregate_metric_eligible_row_count": EXPECTED_AGGREGATE_ELIGIBLE_PER_TICKER[ticker],
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_accepted": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_recommended": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
            "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
            "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
            "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
            "readiness_note": (
                "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_acceptance_readiness_review_digest"] = (
            per_ticker_acceptance_readiness_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package(source_reassessment: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_reassessment is not None:
        _validate_source_reassessment(source_reassessment)
    source_evidence = (
        deepcopy(source_reassessment["source_evidence"])
        if source_reassessment is not None else reassessment._canonical_source_evidence()
    )
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_V1,
        "readiness_status": MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_COMPLETED,
        "readiness_decision": MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "readiness_scope": PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME,
        "decision_reason": READINESS_DECISION_REASON,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "output_label": "RESEARCH_ONLY_NON_ACTIONABLE",
        "source_predictive_usefulness_reassessment_artifact_kind": reassessment.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE,
        "source_predictive_usefulness_reassessment_status": reassessment.MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE_READY,
        "source_predictive_usefulness_reassessment_scope": reassessment.PREDICTIVE_USEFULNESS_REASSESSMENT_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME,
        "source_predictive_usefulness_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
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
        "source_evidence": source_evidence,
        "selected_backtest_lab_package": reassessment.execution.SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package": reassessment.execution.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": reassessment.execution.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": reassessment.execution.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": reassessment.execution.SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": reassessment.execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": reassessment.execution.SELECTED_OBJECTIVE_PATH,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "predictive_usefulness_reassessment_created": True,
        "predictive_usefulness_reassessment_ready": True,
        "predictive_usefulness_acceptance_readiness_review_created": True,
        "predictive_usefulness_acceptance_readiness_review_completed": True,
        "predictive_usefulness_acceptance_readiness_decision": MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "ready_for_predictive_usefulness_not_ready_closure_or_method_selection": True,
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
        "source_matrix_row_count": 179190, "expectancy_backtest_lab_row_count": 179190,
        "evaluable_target_row_count": 177090, "unavailable_target_row_count": 2100,
        "embargoed_cross_split_forward_horizon_row_count": 4200,
        "aggregate_metric_eligible_row_count": 172890,
        "approved_metric_family_count": 13, "blocked_metric_family_count": 1,
        "approved_baseline_count": 6, "blocked_baseline_count": 1,
        "output_digest_mismatch_count": 0, "evidence_integrity": PASS,
        "source_output_integrity": PASS, "no_peek_and_leakage": PASS,
        "chronology_and_embargo": "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS",
        "metric_report_status": "REVIEWED_RESEARCH_ONLY",
        "baseline_comparison_status": "REVIEWED_RESEARCH_ONLY",
        "vpa_wyckoff_alignment_status": "REVIEWED_RESEARCH_ONLY",
        "abstention_quality_status": "REVIEWED_RESEARCH_ONLY",
        "per_ticker_stability_status": "REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "meta_limitation_status": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "predictive_signal_status": "RESEARCH_EVIDENCE_PRESENT_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "source_reassessment_recommendation": "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "readiness_criteria": _criteria(),
        "readiness_classification": "COMPLETED_RESEARCH_ONLY",
        "predictive_signal_readiness": "NOT_READY",
        "metric_materiality_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "per_ticker_stability_readiness": "REQUIRES_OPERATOR_REVIEW",
        "chronology_readiness": "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS",
        "no_peek_readiness": PASS, "meta_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "acceptance_candidate_allowed": False, "acceptance_candidate_recommended": False,
        "predictive_usefulness_acceptance_decision": "NOT_READY",
        "recommendation": "DO_NOT_CREATE_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "next_recommended_action": "CREATE_NOT_READY_CLOSURE_OR_OPERATOR_METHOD_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE",
        "per_ticker_readiness_entries": _per_ticker_entries(),
        "provider_requests_made_in_readiness_review": False,
        "live_provider_transport_enabled_in_readiness_review": False,
        "market_data_acquisition_performed_in_readiness_review": False,
        "dataset_generation_performed_in_readiness_review": False,
        "canonical_dataset_regenerated_in_readiness_review": False,
        "metric_recomputation_from_raw_rows_performed": False,
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
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and all(
        isinstance(row, dict)
        and row.get("per_ticker_acceptance_readiness_review_digest")
        == per_ticker_acceptance_readiness_review_digest_v1(row)
        for row in entries
    )


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    criteria = review.get("readiness_criteria")
    entries = review.get("per_ticker_readiness_entries")
    finding = lambda key: criteria.get(key, {}).get("finding") if isinstance(criteria, dict) else None
    return {
        "source_reassessment_digest_bound": review.get("source_predictive_usefulness_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": review.get("source_expectancy_backtest_lab_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_execution_digest_bound": review.get("source_expectancy_backtest_lab_execution_digest") == EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_output_binding_digest_bound": review.get("source_expectancy_backtest_lab_output_binding_digest") == EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_backtest_rows_digest_bound": review.get("source_expectancy_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": review.get("source_expectancy_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_approval_digest_bound": review.get("source_expectancy_backtest_lab_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest_bound": review.get("source_candidate_review_digest") == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest_bound": review.get("source_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest_bound": review.get("source_vpa_wyckoff_results_review_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": review.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_rows_digest_bound": review.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest_bound": review.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": review.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": review.get("target_universe") == TARGET_UNIVERSE and review.get("target_universe_count") == 12,
        "records_digest_preserved": review.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": review.get("meta_record_count") == 913,
        "selected_backtest_lab_package_preserved": review.get("selected_backtest_lab_package") == reassessment.execution.SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package_preserved": review.get("selected_vpa_wyckoff_package") == reassessment.execution.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package_preserved": review.get("selected_matrix_package") == reassessment.execution.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout_preserved": review.get("selected_matrix_layout") == reassessment.execution.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package_preserved": review.get("selected_feature_package") == reassessment.execution.SELECTED_FEATURE_PACKAGE,
        "selected_target_package_preserved": review.get("selected_label_target_package") == reassessment.execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path_preserved": review.get("selected_objective_path") == reassessment.execution.SELECTED_OBJECTIVE_PATH,
        "source_reassessment_ready_true": review.get("predictive_usefulness_reassessment_ready") is True,
        "acceptance_readiness_review_created_true": review.get("predictive_usefulness_acceptance_readiness_review_created") is True,
        "acceptance_readiness_review_completed_true": review.get("predictive_usefulness_acceptance_readiness_review_completed") is True,
        "readiness_decision_not_ready": review.get("readiness_decision") == MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "ready_for_acceptance_candidate_false": review.get("ready_for_predictive_usefulness_acceptance_candidate") is False,
        "ready_for_not_ready_closure_or_method_selection_true": review.get("ready_for_predictive_usefulness_not_ready_closure_or_method_selection") is True,
        "acceptance_candidate_created_false": review.get("predictive_usefulness_acceptance_candidate_created") is False,
        "predictive_usefulness_not_accepted": review.get("predictive_usefulness") == NOT_ACCEPTED,
        "predictive_usefulness_accepted_false": review.get("predictive_usefulness_accepted") is False,
        "predictive_usefulness_acceptance_ready_false": review.get("predictive_usefulness_acceptance_ready") is False,
        "predictive_usefulness_acceptance_recommended_false": review.get("predictive_usefulness_acceptance_recommended") is False,
        "profitability_not_accepted": review.get("profitability") == NOT_ACCEPTED and review.get("profitability_accepted") is False,
        "runtime_not_authorized": review.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": review.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": review.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": review.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": review.get("trade_recommendations_generated") is False,
        "source_backtest_lab_row_count_179190": review.get("expectancy_backtest_lab_row_count") == 179190,
        "evaluable_target_row_count_177090": review.get("evaluable_target_row_count") == 177090,
        "unavailable_target_row_count_2100": review.get("unavailable_target_row_count") == 2100,
        "embargoed_cross_split_forward_horizon_row_count_4200": review.get("embargoed_cross_split_forward_horizon_row_count") == 4200,
        "aggregate_metric_eligible_row_count_172890": review.get("aggregate_metric_eligible_row_count") == 172890,
        "approved_metric_family_count_13": review.get("approved_metric_family_count") == 13,
        "blocked_metric_family_count_1": review.get("blocked_metric_family_count") == 1,
        "approved_baseline_count_6": review.get("approved_baseline_count") == 6,
        "blocked_baseline_count_1": review.get("blocked_baseline_count") == 1,
        "evidence_integrity_pass": review.get("evidence_integrity") == PASS,
        "source_output_integrity_pass": review.get("source_output_integrity") == PASS,
        "no_peek_and_leakage_pass": review.get("no_peek_and_leakage") == PASS,
        "chronology_and_embargo_pass_with_reviewed_exclusions": review.get("chronology_and_embargo") == "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS",
        "metric_report_present_pass": finding("CRITERION_METRIC_REPORT_PRESENT") == PASS,
        "baseline_comparison_present_pass": finding("CRITERION_BASELINE_COMPARISON_PRESENT") == PASS,
        "vpa_wyckoff_alignment_present_pass": finding("CRITERION_VPA_WYCKOFF_ALIGNMENT_PRESENT") == PASS,
        "abstention_quality_present_pass": finding("CRITERION_ABSTENTION_QUALITY_PRESENT") == PASS,
        "meta_limitation_awareness_pass_with_operator_awareness": finding("CRITERION_META_LIMITATION_AWARENESS") == "PASS_WITH_OPERATOR_AWARENESS",
        "per_ticker_stability_requires_operator_review": finding("CRITERION_PER_TICKER_STABILITY") == "REQUIRES_OPERATOR_REVIEW",
        "metric_materiality_not_ready": finding("CRITERION_METRIC_MATERIALITY_FOR_ACCEPTANCE") == "FAIL_OR_NOT_MET" and review.get("metric_materiality_readiness") == "NOT_READY",
        "baseline_outperformance_materiality_not_ready": finding("CRITERION_BASELINE_OUTPERFORMANCE_MATERIALITY") == "FAIL_OR_NOT_MET" and review.get("baseline_outperformance_readiness") == "NOT_READY",
        "acceptance_threshold_defined_not_ready": finding("CRITERION_ACCEPTANCE_THRESHOLD_DEFINED") == "FAIL_OR_NOT_MET",
        "source_reassessment_recommendation_do_not_accept": finding("CRITERION_SOURCE_REASSESSMENT_RECOMMENDATION") == "FAIL_OR_NOT_MET" and review.get("source_reassessment_recommendation") == "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "readiness_criteria_16_present": isinstance(criteria, dict) and list(criteria) == list(CRITERIA_POLICY),
        "readiness_findings_present": all(review.get(key) is not None for key in ("readiness_classification", "predictive_signal_readiness", "metric_materiality_readiness", "baseline_outperformance_readiness", "per_ticker_stability_readiness", "recommendation")),
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12,
        "per_ticker_digests_present": _per_ticker_digests_valid(entries),
        "model_training_authorized_false": review.get("model_training_authorized") is False,
        "model_training_performed_false": review.get("model_training_performed") is False,
        "strategy_scoring_false": review.get("strategy_scoring_performed") is False,
        "provider_requests_made_false": review.get("provider_requests_made_in_readiness_review") is False,
        "market_data_acquisition_false": review.get("market_data_acquisition_performed_in_readiness_review") is False,
        "dataset_regeneration_false": review.get("canonical_dataset_regenerated_in_readiness_review") is False,
        "metric_recomputation_from_raw_rows_false": review.get("metric_recomputation_from_raw_rows_performed") is False,
        "predictive_usefulness_reassessment_rerun_false": review.get("predictive_usefulness_reassessment_rerun_performed") is False,
        "expectancy_backtest_lab_execution_rerun_false": review.get("expectancy_backtest_lab_execution_rerun_performed") is False,
        "expectancy_backtest_lab_results_review_rerun_false": review.get("expectancy_backtest_lab_results_review_rerun_performed") is False,
        "vpa_wyckoff_execution_rerun_false": review.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": review.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": review.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": review.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": review.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": review.get("target_generation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": review.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": review.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": review.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": review.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": review.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "readiness evidence matches" if actual else "readiness evidence mismatch",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(review)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "predictive_usefulness_acceptance_readiness_review_created": True,
        "predictive_usefulness_acceptance_readiness_review_completed": not failed,
        "predictive_usefulness_acceptance_readiness_decision": MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "ready_for_predictive_usefulness_not_ready_closure_or_method_selection": not failed,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
        "recommendation": "DO_NOT_CREATE_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "next_recommended_task": "PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_EXPECTANCY_LAB_EVIDENCE_V1",
    }


def marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the readiness review."""
    payload = deepcopy(dict(review))
    payload.pop("readiness_checklist", None)
    payload.pop("readiness_summary", None)
    payload.pop("marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest", None)
    return semantic_digest(payload)


def build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(
    *, source_reassessment: dict | None = None,
) -> dict:
    """Build the NOT_READY review without rerunning source evidence."""
    review = _base_package(source_reassessment)
    review["readiness_checklist"] = _checklist(review)
    review["readiness_summary"] = _summary(review["readiness_checklist"])
    review["marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest"] = (
        marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest_v1(review)
    )
    validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(
            f"{field} mismatch"
        )


def validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(
    review: dict,
) -> dict:
    """Validate NOT_READY findings, evidence bindings, and closed authority gates."""
    if not isinstance(review, dict):
        raise MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(
            "review must be an object"
        )
    expected = _base_package(None)
    for field, value in expected.items():
        if field not in {"source_evidence", "readiness_criteria", "per_ticker_readiness_entries"}:
            _expect(review.get(field), value, field)
    _expect(review.get("source_evidence"), expected["source_evidence"], "source_evidence")
    _expect(review.get("readiness_criteria"), expected["readiness_criteria"], "readiness_criteria")
    entries = review.get("per_ticker_readiness_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(
            "per-ticker readiness entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    for expected_entry, entry in zip(expected["per_ticker_readiness_entries"], entries):
        _expect(entry, expected_entry, f"{expected_entry['ticker']} per-ticker entry")
        _expect(
            entry.get("per_ticker_acceptance_readiness_review_digest"),
            per_ticker_acceptance_readiness_review_digest_v1(entry),
            f"{entry['ticker']} per-ticker digest",
        )
    checklist = review.get("readiness_checklist")
    if not isinstance(checklist, list):
        raise MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(
            "readiness checklist missing"
        )
    _expect(checklist, _checklist(review), "readiness checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(
            "readiness checklist failed"
        )
    _expect(review.get("readiness_summary"), _summary(checklist), "readiness summary")
    digest = review.get(
        "marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(
            "readiness review digest missing"
        )
    _expect(
        digest,
        marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest_v1(review),
        "readiness review digest",
    )
    return {
        "status": MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_VALID,
        "artifact_kind": review["artifact_kind"], "readiness_status": review["readiness_status"],
        "readiness_decision": review["readiness_decision"],
        "marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest": digest,
        **{
            key: review["readiness_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated readiness review."""
    validation = validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(review)
    sections = [
        ("Title", ["Predictive-Usefulness Acceptance Readiness Review Using Expectancy Lab Evidence v1"]),
        ("Predictive-Usefulness Acceptance Readiness Review Using Expectancy Lab Evidence v1", [f"Artifact/status: `{review['artifact_kind']}` / `{review['readiness_status']}`.", f"Digest: `{validation['marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest']}`."]),
        ("Source Reassessment", [f"Digest: `{review['source_predictive_usefulness_reassessment_digest']}`.", f"Recommendation: `{review['source_reassessment_recommendation']}`."]),
        ("Bound Evidence", [f"Results review: `{review['source_expectancy_backtest_lab_results_review_digest']}`.", f"Rows: `{review['source_expectancy_backtest_rows_digest']}`.", f"Metrics: `{review['source_expectancy_metric_report_digest']}`."]),
        ("Dataset and Universe", [f"Dataset/records: `{review['dataset_name']}` / `{review['total_canonical_record_count']}`.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in review["target_universe"]) + "."]),
        ("Readiness Scope", [f"`{review['readiness_scope']}`; research-only and non-actionable."]),
        ("Readiness Basis", [f"Rows/evaluable/unavailable: `{review['expectancy_backtest_lab_row_count']} / {review['evaluable_target_row_count']} / {review['unavailable_target_row_count']}`."]),
        ("Readiness Criteria", [f"`{name}`: `{row['finding']}` — {row['reason']}" for name, row in review["readiness_criteria"].items()]),
        ("Readiness Findings", [f"Signal/materiality/baseline: `{review['predictive_signal_readiness']} / {review['metric_materiality_readiness']} / {review['baseline_outperformance_readiness']}`."]),
        ("Metric Materiality Readiness", [f"`{review['metric_materiality_readiness']}`."]),
        ("Baseline Outperformance Readiness", [f"`{review['baseline_outperformance_readiness']}`."]),
        ("Per-Ticker Stability Readiness", [f"`{review['per_ticker_stability_readiness']}`."]),
        ("Chronology and Embargo", [f"`{review['chronology_readiness']}`; 4,200 embargoed rows remain excluded from aggregate values."]),
        ("No-Peek and Leakage", [f"`{review['no_peek_readiness']}`."]),
        ("META Limitation", ["META remains exactly 913 historical records and requires operator awareness."]),
        ("Readiness Decision", [f"`{review['readiness_decision']}`: `{review['decision_reason']}`.", f"Recommendation: `{review['recommendation']}`."]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate is created."]),
        ("Profitability Boundary", ["Profitability remains not accepted and outside this review."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Per-Ticker Readiness", [f"`{row['ticker']}`: `{row['acceptance_readiness_decision']}`, digest `{row['per_ticker_acceptance_readiness_review_digest']}`." for row in review["per_ticker_readiness_entries"]]),
        ("Next Chain", review["next_chain"]), ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{review['readiness_summary']['total_checks']} / {review['readiness_summary']['passed_checks']} / {review['readiness_summary']['failed_checks']} / {review['readiness_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, source rerun, raw-row metric recomputation, model training, scoring, recommendation, acceptance, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# Predictive-Usefulness Acceptance Readiness Review Using Expectancy Lab Evidence v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(
    output_dir: str | Path, *, source_reassessment: dict | None = None,
) -> dict:
    """Write canonical readiness-review JSON without overwriting an existing package."""
    review = build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(
        source_reassessment=source_reassessment
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1.json"
    if path.exists():
        raise MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError(
            "readiness review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "readiness_status": review["readiness_status"],
        "readiness_decision": review["readiness_decision"],
        "marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest": review["marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
