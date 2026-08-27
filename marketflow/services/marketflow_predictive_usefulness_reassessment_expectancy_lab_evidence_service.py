"""Offline predictive-usefulness reassessment using reviewed expectancy-lab evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_expectancy_backtest_lab_results_review_service as results_review
from marketflow.services import marketflow_expectancy_backtest_lab_execution_service as execution


ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE"
)
SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_V1 = (
    "marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE_READY = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE_READY"
)
PREDICTIVE_USEFULNESS_REASSESSMENT_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME"
)
MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_VALID = (
    "MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_VALID"
)

EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = "8cae8ae37bd21cdf50b23a323c0e501b009010673043f338bceb913566b78ae5"
EXPECTED_SOURCE_EXECUTION_DIGEST = results_review.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = results_review.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = results_review.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = results_review.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_APPROVAL_DIGEST = results_review.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = results_review.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = results_review.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = results_review.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = results_review.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = results_review.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = results_review.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = results_review.EXPECTED_SOURCE_RECORDS_DIGEST

TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
EXPECTED_LAB_ROW_COUNTS = dict(execution.EXPECTED_LAB_ROW_COUNTS)
EXPECTED_EVALUABLE_COUNTS = dict(execution.EXPECTED_EVALUABLE_COUNTS)
EXPECTED_UNAVAILABLE_COUNTS = dict(execution.EXPECTED_UNAVAILABLE_COUNTS)
EXPECTED_EMBARGOED_PER_TICKER = {ticker: 350 for ticker in TARGET_UNIVERSE}
EXPECTED_AGGREGATE_ELIGIBLE_PER_TICKER = {
    ticker: EXPECTED_EVALUABLE_COUNTS[ticker] - EXPECTED_EMBARGOED_PER_TICKER[ticker]
    for ticker in TARGET_UNIVERSE
}

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

DOMAIN_IDS = [
    "DOMAIN_SOURCE_EVIDENCE_INTEGRITY", "DOMAIN_DATASET_AND_UNIVERSE",
    "DOMAIN_TARGET_VALUES", "DOMAIN_FEATURE_LABEL_MATRIX_ROWS",
    "DOMAIN_VPA_WYCKOFF_RULE_VALUES", "DOMAIN_BACKTEST_LAB_ROWS",
    "DOMAIN_CHRONOLOGICAL_SPLITS", "DOMAIN_EMBARGO_EXCLUSIONS",
    "DOMAIN_BASELINE_COMPARISON", "DOMAIN_EXPECTANCY_METRICS",
    "DOMAIN_ABSTENTION_QUALITY", "DOMAIN_VPA_WYCKOFF_ALIGNMENT",
    "DOMAIN_PER_TICKER_STABILITY", "DOMAIN_META_LIMITATION",
    "DOMAIN_NO_PEEK_AND_LEAKAGE", "DOMAIN_PREDICTIVE_USEFULNESS_BOUNDARY",
    "DOMAIN_PROFITABILITY_BOUNDARY", "DOMAIN_RUNTIME_BOUNDARY",
]
BOUNDARY_DOMAINS = {"DOMAIN_PROFITABILITY_BOUNDARY", "DOMAIN_RUNTIME_BOUNDARY"}

NEXT_CHAIN = [
    "Predictive-Usefulness Acceptance Readiness Review Using Expectancy Lab Evidence v1.",
    "Predictive-Usefulness Acceptance Candidate only if readiness passes.",
    "Predictive-Usefulness Acceptance Ceremony only if separately approved.",
    "Profitability Review only after predictive usefulness is separately accepted.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "predictive_usefulness_acceptance_approval_if_candidate_passes",
    "profitability_review_if_predictive_usefulness_accepted",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "reassessment_does_not_accept_predictive_usefulness",
    "reassessment_does_not_create_acceptance_readiness_review",
    "reassessment_does_not_create_acceptance_candidate",
    "reassessment_does_not_accept_profitability",
    "reassessment_does_not_authorize_runtime",
    "reassessment_does_not_authorize_strategy",
    "reassessment_does_not_authorize_paper_trading",
    "reassessment_does_not_authorize_broker_execution",
    "reassessment_does_not_generate_trade_recommendations",
    "reassessment_does_not_train_models",
    "reassessment_does_not_score_strategy",
    "reassessment_does_not_call_providers",
    "reassessment_does_not_acquire_market_data",
    "reassessment_does_not_recompute_metrics_from_raw_rows",
    "reassessment_does_not_rerun_expectancy_backtest_lab_execution",
    "reassessment_does_not_rerun_expectancy_backtest_lab_results_review",
    "reassessment_does_not_rerun_vpa_wyckoff_execution",
    "reassessment_does_not_rerun_vpa_wyckoff_results_review",
    "reassessment_does_not_rerun_feature_label_matrix_execution",
    "reassessment_does_not_rerun_feature_label_matrix_results_review",
    "reassessment_does_not_rerun_signal_feature_generation",
    "reassessment_does_not_rerun_target_generation",
    "do_not_mutate_frozen_dataset", "do_not_mutate_expectancy_backtest_lab_outputs",
    "do_not_mutate_vpa_wyckoff_outputs", "do_not_mutate_matrix_outputs",
    "do_not_mutate_signal_or_feature_outputs", "do_not_mutate_target_outputs",
    "do_not_mutate_redesigned_label_outputs", "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs", "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_results_review_digest_bound", "source_execution_digest_bound",
    "source_output_binding_digest_bound", "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound", "source_approval_digest_bound",
    "source_candidate_review_digest_bound", "source_candidate_digest_bound",
    "source_vpa_wyckoff_results_review_digest_bound",
    "source_vpa_wyckoff_rule_values_digest_bound", "source_matrix_rows_digest_bound",
    "source_target_values_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "selected_backtest_lab_package_preserved", "selected_vpa_wyckoff_package_preserved",
    "selected_matrix_package_preserved", "selected_matrix_layout_preserved",
    "selected_feature_package_preserved", "selected_target_package_preserved",
    "selected_objective_path_preserved", "source_results_review_ready_true",
    "reassessment_created_true", "reassessment_ready_true",
    "ready_for_acceptance_readiness_review_true", "acceptance_readiness_review_created_false",
    "acceptance_candidate_created_false", "predictive_usefulness_not_accepted",
    "predictive_usefulness_accepted_false", "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "paper_trading_not_authorized",
    "broker_not_authorized", "trade_recommendations_false",
    "source_backtest_lab_row_count_179190", "evaluable_target_row_count_177090",
    "unavailable_target_row_count_2100",
    "embargoed_cross_split_forward_horizon_row_count_4200",
    "aggregate_metric_eligible_row_count_172890", "approved_metric_family_count_13",
    "blocked_metric_family_count_1", "approved_baseline_count_6",
    "blocked_baseline_count_1", "output_digest_mismatch_count_zero",
    "evidence_integrity_pass", "source_output_integrity_pass",
    "no_peek_and_leakage_pass", "chronology_and_embargo_pass_with_reviewed_exclusions",
    "metric_report_reviewed_research_only", "baseline_comparison_reviewed_research_only",
    "vpa_wyckoff_alignment_reviewed_research_only",
    "abstention_quality_reviewed_research_only",
    "per_ticker_stability_requires_readiness_review", "meta_limitation_preserved",
    "reassessment_domains_present", "reassessment_domains_research_only",
    "per_ticker_entries_12", "per_ticker_digests_present",
    "model_training_authorized_false", "model_training_performed_false",
    "strategy_scoring_false", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "metric_recomputation_from_raw_rows_false", "expectancy_backtest_lab_execution_rerun_false",
    "expectancy_backtest_lab_results_review_rerun_false", "vpa_wyckoff_execution_rerun_false",
    "vpa_wyckoff_results_review_rerun_false", "matrix_execution_rerun_false",
    "matrix_results_review_rerun_false", "signal_feature_generation_rerun_false",
    "target_generation_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(ValueError):
    """Raised when the reassessment violates its conservative contract."""


def _canonical_source_evidence() -> dict[str, Any]:
    upstream = deepcopy(execution.approval_service.review_service.candidate_service.SOURCE_EVIDENCE)
    return {
        "marketflow_expectancy_backtest_lab_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "marketflow_expectancy_backtest_lab_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "expectancy_backtest_lab_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "expectancy_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "expectancy_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "marketflow_expectancy_backtest_lab_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        **upstream,
    }


def _validate_source_review(source_review: Mapping[str, Any]) -> None:
    if not isinstance(source_review, dict):
        raise MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(
            "source_review must be an object"
        )
    results_review.validate_marketflow_expectancy_backtest_lab_results_review_v1(source_review)
    expected = {
        "artifact_kind": results_review.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE,
        "review_status": results_review.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": results_review.EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_ONLY_NOT_REASSESSMENT_NOT_RUNTIME,
        "marketflow_expectancy_backtest_lab_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
    }
    for field, value in expected.items():
        if source_review.get(field) != value:
            raise MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(
                f"source review {field} mismatch"
            )


def _domains() -> dict[str, dict[str, Any]]:
    domains: dict[str, dict[str, Any]] = {}
    for domain_id in DOMAIN_IDS:
        boundary = domain_id in BOUNDARY_DOMAINS
        domains[domain_id] = {
            "domain_status": "REVIEWED_RESEARCH_ONLY",
            "acceptance_evidence": False,
            "requires_acceptance_readiness_review": not boundary,
            "research_only": True,
            "non_actionable": True,
        }
        if boundary:
            domains[domain_id]["authority_boundary_closed"] = True
    return domains


def per_ticker_predictive_usefulness_reassessment_digest_v1(entry: Mapping[str, Any]) -> str:
    """Return the deterministic digest for one ticker reassessment entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_predictive_usefulness_reassessment_digest", None)
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
            "expectancy_backtest_lab_results_review_status": results_review.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE_READY,
            "predictive_usefulness_reassessment_status": "REVIEWED_RESEARCH_ONLY",
            "selected_backtest_lab_package": execution.SELECTED_BACKTEST_LAB_PACKAGE,
            "selected_vpa_wyckoff_package": execution.SELECTED_VPA_WYCKOFF_PACKAGE,
            "selected_matrix_package": execution.SELECTED_MATRIX_PACKAGE,
            "selected_feature_package": execution.SELECTED_FEATURE_PACKAGE,
            "selected_label_target_package": execution.SELECTED_LABEL_TARGET_PACKAGE,
            "selected_objective_path": execution.SELECTED_OBJECTIVE_PATH,
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
            "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
            "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
            "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
            "reassessment_note": (
                "PRESERVE_META_LIMITATION_IN_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_predictive_usefulness_reassessment_digest"] = (
            per_ticker_predictive_usefulness_reassessment_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package(source_review: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_review is not None:
        _validate_source_review(source_review)
    source_evidence = (
        deepcopy(source_review["source_evidence"])
        if source_review is not None else _canonical_source_evidence()
    )
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_V1,
        "reassessment_status": MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE_READY,
        "reassessment_scope": PREDICTIVE_USEFULNESS_REASSESSMENT_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "output_label": "RESEARCH_ONLY_NON_ACTIONABLE",
        "evidence_scope": "PREDICTIVE_USEFULNESS_REASSESSMENT_EXPECTANCY_LAB_EVIDENCE_RESEARCH_ONLY",
        "source_expectancy_backtest_lab_results_review_artifact_kind": results_review.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE,
        "source_expectancy_backtest_lab_results_review_status": results_review.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE_READY,
        "source_expectancy_backtest_lab_results_review_scope": results_review.EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_ONLY_NOT_REASSESSMENT_NOT_RUNTIME,
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
        "expectancy_backtest_lab_results_review_created": True,
        "expectancy_backtest_lab_results_review_ready": True,
        "predictive_usefulness_reassessment_created": True,
        "predictive_usefulness_reassessment_ready": True,
        "ready_for_predictive_usefulness_acceptance_readiness_review": True,
        "predictive_usefulness_acceptance_readiness_review_created": False,
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
        "output_digest_mismatch_count": 0, "backtest_rows_jsonl_schema_verified": True,
        "metric_report_verified": True, "baseline_comparison_report_verified": True,
        "vpa_wyckoff_rule_alignment_report_verified": True,
        "abstention_quality_report_verified": True, "per_ticker_backtest_report_verified": True,
        "chronological_split_report_verified": True, "meta_limitation_report_verified": True,
        "no_peek_report_verified": True, "operator_summary_verified": True,
        "chronological_split_policy": "CHRONOLOGICAL_NO_SHUFFLE",
        "horizon_aware_embargo_status": "APPLIED_AS_RESEARCH_CONTROL_NOT_MODEL_TRAINING",
        "blocked_randomized_null_reference_executed": False,
        "blocked_bootstrap_metric_computed": False,
        "target_values_used_as_predictors": False, "target_classes_used_as_predictors": False,
        "forward_returns_used_as_features": False, "prediction_fields_present": False,
        "strategy_score_fields_present": False, "trade_recommendation_fields_present": False,
        "broker_order_fields_present": False, "provider_payload_fields_present": False,
        "api_key_fields_present": False,
        "reassessment_classification": "COMPLETED_RESEARCH_ONLY",
        "evidence_integrity": PASS, "source_output_integrity": PASS,
        "no_peek_and_leakage": PASS,
        "chronology_and_embargo": "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS",
        "metric_report_status": "REVIEWED_RESEARCH_ONLY",
        "baseline_comparison_status": "REVIEWED_RESEARCH_ONLY",
        "vpa_wyckoff_alignment_status": "REVIEWED_RESEARCH_ONLY",
        "abstention_quality_status": "REVIEWED_RESEARCH_ONLY",
        "per_ticker_stability_status": "REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "meta_limitation_status": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "predictive_signal_status": "RESEARCH_EVIDENCE_PRESENT_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "predictive_usefulness_decision": "NOT_ACCEPTED_AT_REASSESSMENT_STAGE",
        "recommendation": "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "readiness_for_acceptance_readiness_review": True,
        "reassessment_domains": _domains(),
        "per_ticker_reassessment_entries": _per_ticker_entries(),
        "provider_requests_made_in_reassessment": False,
        "live_provider_transport_enabled_in_reassessment": False,
        "market_data_acquisition_performed_in_reassessment": False,
        "dataset_generation_performed_in_reassessment": False,
        "canonical_dataset_regenerated_in_reassessment": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "expectancy_backtest_lab_execution_rerun_performed": False,
        "expectancy_backtest_lab_results_review_rerun_performed": False,
        "expectancy_backtest_lab_approval_rerun_performed": False,
        "expectancy_backtest_lab_candidate_review_rerun_performed": False,
        "expectancy_backtest_lab_candidate_creation_rerun_performed": False,
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
        and row.get("per_ticker_predictive_usefulness_reassessment_digest")
        == per_ticker_predictive_usefulness_reassessment_digest_v1(row)
        for row in entries
    )


def _check_values(package: Mapping[str, Any]) -> dict[str, bool]:
    entries = package.get("per_ticker_reassessment_entries")
    domains = package.get("reassessment_domains")
    return {
        "source_results_review_digest_bound": package.get("source_expectancy_backtest_lab_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_execution_digest_bound": package.get("source_expectancy_backtest_lab_execution_digest") == EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_output_binding_digest_bound": package.get("source_expectancy_backtest_lab_output_binding_digest") == EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_backtest_rows_digest_bound": package.get("source_expectancy_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": package.get("source_expectancy_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_approval_digest_bound": package.get("source_expectancy_backtest_lab_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest_bound": package.get("source_candidate_review_digest") == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest_bound": package.get("source_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest_bound": package.get("source_vpa_wyckoff_results_review_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": package.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_rows_digest_bound": package.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest_bound": package.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": package.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": package.get("target_universe") == TARGET_UNIVERSE and package.get("target_universe_count") == 12,
        "records_digest_preserved": package.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": package.get("meta_record_count") == 913,
        "selected_backtest_lab_package_preserved": package.get("selected_backtest_lab_package") == execution.SELECTED_BACKTEST_LAB_PACKAGE,
        "selected_vpa_wyckoff_package_preserved": package.get("selected_vpa_wyckoff_package") == execution.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package_preserved": package.get("selected_matrix_package") == execution.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout_preserved": package.get("selected_matrix_layout") == execution.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package_preserved": package.get("selected_feature_package") == execution.SELECTED_FEATURE_PACKAGE,
        "selected_target_package_preserved": package.get("selected_label_target_package") == execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path_preserved": package.get("selected_objective_path") == execution.SELECTED_OBJECTIVE_PATH,
        "source_results_review_ready_true": package.get("expectancy_backtest_lab_results_review_ready") is True,
        "reassessment_created_true": package.get("predictive_usefulness_reassessment_created") is True,
        "reassessment_ready_true": package.get("predictive_usefulness_reassessment_ready") is True,
        "ready_for_acceptance_readiness_review_true": package.get("ready_for_predictive_usefulness_acceptance_readiness_review") is True,
        "acceptance_readiness_review_created_false": package.get("predictive_usefulness_acceptance_readiness_review_created") is False,
        "acceptance_candidate_created_false": package.get("predictive_usefulness_acceptance_candidate_created") is False,
        "predictive_usefulness_not_accepted": package.get("predictive_usefulness") == NOT_ACCEPTED,
        "predictive_usefulness_accepted_false": package.get("predictive_usefulness_accepted") is False,
        "predictive_usefulness_acceptance_ready_false": package.get("predictive_usefulness_acceptance_ready") is False,
        "predictive_usefulness_acceptance_recommended_false": package.get("predictive_usefulness_acceptance_recommended") is False,
        "profitability_not_accepted": package.get("profitability") == NOT_ACCEPTED and package.get("profitability_accepted") is False,
        "runtime_not_authorized": package.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": package.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": package.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": package.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": package.get("trade_recommendations_generated") is False,
        "source_backtest_lab_row_count_179190": package.get("expectancy_backtest_lab_row_count") == 179190,
        "evaluable_target_row_count_177090": package.get("evaluable_target_row_count") == 177090,
        "unavailable_target_row_count_2100": package.get("unavailable_target_row_count") == 2100,
        "embargoed_cross_split_forward_horizon_row_count_4200": package.get("embargoed_cross_split_forward_horizon_row_count") == 4200,
        "aggregate_metric_eligible_row_count_172890": package.get("aggregate_metric_eligible_row_count") == 172890,
        "approved_metric_family_count_13": package.get("approved_metric_family_count") == 13,
        "blocked_metric_family_count_1": package.get("blocked_metric_family_count") == 1,
        "approved_baseline_count_6": package.get("approved_baseline_count") == 6,
        "blocked_baseline_count_1": package.get("blocked_baseline_count") == 1,
        "output_digest_mismatch_count_zero": package.get("output_digest_mismatch_count") == 0,
        "evidence_integrity_pass": package.get("evidence_integrity") == PASS,
        "source_output_integrity_pass": package.get("source_output_integrity") == PASS,
        "no_peek_and_leakage_pass": package.get("no_peek_and_leakage") == PASS,
        "chronology_and_embargo_pass_with_reviewed_exclusions": package.get("chronology_and_embargo") == "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS",
        "metric_report_reviewed_research_only": package.get("metric_report_status") == "REVIEWED_RESEARCH_ONLY",
        "baseline_comparison_reviewed_research_only": package.get("baseline_comparison_status") == "REVIEWED_RESEARCH_ONLY",
        "vpa_wyckoff_alignment_reviewed_research_only": package.get("vpa_wyckoff_alignment_status") == "REVIEWED_RESEARCH_ONLY",
        "abstention_quality_reviewed_research_only": package.get("abstention_quality_status") == "REVIEWED_RESEARCH_ONLY",
        "per_ticker_stability_requires_readiness_review": package.get("per_ticker_stability_status") == "REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "meta_limitation_preserved": package.get("meta_limitation_status") == "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "reassessment_domains_present": isinstance(domains, dict) and list(domains) == DOMAIN_IDS,
        "reassessment_domains_research_only": isinstance(domains, dict) and all(
            row.get("domain_status") == "REVIEWED_RESEARCH_ONLY"
            and row.get("acceptance_evidence") is False
            and row.get("research_only") is True and row.get("non_actionable") is True
            for row in domains.values()
        ),
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12,
        "per_ticker_digests_present": _per_ticker_digests_valid(entries),
        "model_training_authorized_false": package.get("model_training_authorized") is False,
        "model_training_performed_false": package.get("model_training_performed") is False,
        "strategy_scoring_false": package.get("strategy_scoring_performed") is False,
        "provider_requests_made_false": package.get("provider_requests_made_in_reassessment") is False,
        "market_data_acquisition_false": package.get("market_data_acquisition_performed_in_reassessment") is False,
        "dataset_regeneration_false": package.get("canonical_dataset_regenerated_in_reassessment") is False,
        "metric_recomputation_from_raw_rows_false": package.get("metric_recomputation_from_raw_rows_performed") is False,
        "expectancy_backtest_lab_execution_rerun_false": package.get("expectancy_backtest_lab_execution_rerun_performed") is False,
        "expectancy_backtest_lab_results_review_rerun_false": package.get("expectancy_backtest_lab_results_review_rerun_performed") is False,
        "vpa_wyckoff_execution_rerun_false": package.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": package.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": package.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": package.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": package.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": package.get("target_generation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": package.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": package.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": package.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": package.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": package.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": package.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "reassessment evidence matches" if actual else "reassessment evidence mismatch",
    }


def _checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(package)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "predictive_usefulness_reassessment_created": True,
        "predictive_usefulness_reassessment_ready": not failed,
        "ready_for_predictive_usefulness_acceptance_readiness_review": not failed,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
        "recommendation": "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "next_recommended_task": "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_V1",
    }


def marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest_v1(
    reassessment: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the reassessment."""
    payload = deepcopy(dict(reassessment))
    payload.pop("reassessment_checklist", None)
    payload.pop("reassessment_summary", None)
    payload.pop("marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest", None)
    return semantic_digest(payload)


def build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(
    *, source_review: dict | None = None,
) -> dict:
    """Build the reassessment from reviewed constants without rerunning source inspection."""
    package = _base_package(source_review)
    package["reassessment_checklist"] = _checklist(package)
    package["reassessment_summary"] = _summary(package["reassessment_checklist"])
    package["marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest"] = (
        marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest_v1(package)
    )
    validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(
            f"{field} mismatch"
        )


def validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(
    reassessment: dict,
) -> dict:
    """Validate evidence bindings, conservative classification, and closed gates."""
    if not isinstance(reassessment, dict):
        raise MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(
            "reassessment must be an object"
        )
    expected = _base_package(None)
    for field, value in expected.items():
        if field not in {"source_evidence", "per_ticker_reassessment_entries", "reassessment_domains"}:
            _expect(reassessment.get(field), value, field)
    _expect(reassessment.get("source_evidence"), expected["source_evidence"], "source_evidence")
    _expect(reassessment.get("reassessment_domains"), expected["reassessment_domains"], "reassessment_domains")
    entries = reassessment.get("per_ticker_reassessment_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(
            "per-ticker entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    for expected_entry, entry in zip(expected["per_ticker_reassessment_entries"], entries):
        _expect(entry, expected_entry, f"{expected_entry['ticker']} per-ticker entry")
        digest = entry.get("per_ticker_predictive_usefulness_reassessment_digest")
        _expect(
            digest, per_ticker_predictive_usefulness_reassessment_digest_v1(entry),
            f"{entry['ticker']} per-ticker digest",
        )
    checklist = reassessment.get("reassessment_checklist")
    if not isinstance(checklist, list):
        raise MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(
            "reassessment checklist missing"
        )
    _expect(checklist, _checklist(reassessment), "reassessment checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(
            "reassessment checklist failed"
        )
    _expect(reassessment.get("reassessment_summary"), _summary(checklist), "reassessment summary")
    digest = reassessment.get(
        "marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(
            "reassessment digest missing"
        )
    _expect(
        digest,
        marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest_v1(
            reassessment
        ),
        "reassessment digest",
    )
    return {
        "status": MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_VALID,
        "artifact_kind": reassessment["artifact_kind"],
        "reassessment_status": reassessment["reassessment_status"],
        "marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest": digest,
        **{
            key: reassessment["reassessment_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_markdown_v1(
    reassessment: dict,
) -> str:
    """Render a sanitized Markdown view of the validated reassessment."""
    validation = validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(
        reassessment
    )
    sections = [
        ("Title", ["Predictive-Usefulness Reassessment Using Expectancy Lab Evidence v1"]),
        ("Predictive-Usefulness Reassessment Using Expectancy Lab Evidence v1", [f"Artifact/status: `{reassessment['artifact_kind']}` / `{reassessment['reassessment_status']}`.", f"Digest: `{validation['marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest']}`."]),
        ("Source Expectancy Backtest Lab Results Review", [f"Digest: `{reassessment['source_expectancy_backtest_lab_results_review_digest']}`."]),
        ("Bound Evidence", [f"Execution: `{reassessment['source_expectancy_backtest_lab_execution_digest']}`.", f"Rows: `{reassessment['source_expectancy_backtest_rows_digest']}`.", f"Metrics: `{reassessment['source_expectancy_metric_report_digest']}`."]),
        ("Dataset and Universe", [f"Dataset/records: `{reassessment['dataset_name']}` / `{reassessment['total_canonical_record_count']}`.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in reassessment["target_universe"]) + "."]),
        ("Reassessment Scope", [f"`{reassessment['reassessment_scope']}`; research-only and non-actionable."]),
        ("Evidence Basis", [f"Rows/evaluable/unavailable: `{reassessment['expectancy_backtest_lab_row_count']} / {reassessment['evaluable_target_row_count']} / {reassessment['unavailable_target_row_count']}`."]),
        ("Metric Evidence Summary", [f"Thirteen reviewed metric families; status `{reassessment['metric_report_status']}`."]),
        ("Baseline Comparison Summary", [f"Six approved baselines; status `{reassessment['baseline_comparison_status']}`."]),
        ("VPA/Wyckoff Alignment Summary", [f"`{reassessment['vpa_wyckoff_alignment_status']}`."]),
        ("Abstention Quality Summary", [f"`{reassessment['abstention_quality_status']}`."]),
        ("Chronology and Embargo", [f"`{reassessment['chronological_split_policy']}`; `{reassessment['chronology_and_embargo']}`."]),
        ("No-Peek and Leakage", [f"`{reassessment['no_peek_and_leakage']}`; target and future fields remain outside predictors."]),
        ("Per-Ticker Reassessment", [f"`{row['ticker']}`: rows `{row['backtest_lab_row_count']}`, digest `{row['per_ticker_predictive_usefulness_reassessment_digest']}`." for row in reassessment["per_ticker_reassessment_entries"]]),
        ("META Limitation", ["META remains exactly 913 historical records; the reduced record limitation is preserved."]),
        ("Reassessment Classification", [f"`{reassessment['reassessment_classification']}`; `{reassessment['recommendation']}`."]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no readiness review or acceptance candidate is created."]),
        ("Profitability Boundary", ["Profitability remains not accepted and is not inferred from this evidence."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Next Chain", reassessment["next_chain"]), ("Next Gates", reassessment["next_gates"]),
        ("Risk Controls", reassessment["risk_controls"]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{reassessment['reassessment_summary']['total_checks']} / {reassessment['reassessment_summary']['passed_checks']} / {reassessment['reassessment_summary']['failed_checks']} / {reassessment['reassessment_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, source rerun, raw-row metric recomputation, model training, scoring, recommendation, acceptance, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# Predictive-Usefulness Reassessment Using Expectancy Lab Evidence v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(
    output_dir: str | Path, *, source_review: dict | None = None,
) -> dict:
    """Write canonical reassessment JSON without overwriting an existing package."""
    package = build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(
        source_review=source_review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1.json"
    if path.exists():
        raise MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError(
            "reassessment output already exists"
        )
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": package["artifact_kind"],
        "reassessment_status": package["reassessment_status"],
        "marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest": package["marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
