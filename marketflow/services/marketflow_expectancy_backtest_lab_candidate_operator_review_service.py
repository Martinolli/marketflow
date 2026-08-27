"""Offline operator review of the expectancy backtest-lab candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_expectancy_backtest_lab_candidate_service as candidate_service,
)


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_expectancy_backtest_lab_candidate_operator_review_v1"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"
)
EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL = (
    "EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_VALID = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_VALID"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "8dbca7083455dffa91d42610b7b12ae6407176d9b87e8a9dda1c6bc8f0cf6ad9"
)
EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = (
    candidate_service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST = (
    candidate_service.EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST
)
EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST = (
    candidate_service.EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST
)
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = (
    candidate_service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
)
EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST = (
    candidate_service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = candidate_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_FEATURE_VALUES_DIGEST = candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = candidate_service.EXPECTED_SOURCE_RECORDS_DIGEST
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER

NEXT_CHAIN = [
    "Expectancy Backtest Lab Approval v1, if selected.",
    "Expectancy Backtest Lab Execution v1, if approved.",
    "Expectancy Backtest Lab Results Review v1.",
    "Predictive-usefulness reassessment using expectancy lab evidence.",
    "Acceptance-readiness review only after reassessment.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "expectancy_backtest_lab_approval_if_selected",
    "expectancy_backtest_lab_execution_if_approved",
    "expectancy_backtest_lab_results_review",
    "predictive_usefulness_reassessment_using_expectancy_lab_evidence",
    "predictive_usefulness_acceptance_readiness_if_reassessment_supports_it",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_select_backtest_lab_package",
    "review_does_not_approve_backtest_lab_execution",
    "review_does_not_run_backtest",
    "review_does_not_create_backtest_rows",
    "review_does_not_create_backtest_results",
    "review_does_not_train_models",
    "review_does_not_compute_metrics",
    "review_does_not_score_strategy",
    "review_does_not_generate_trade_recommendations",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution",
    "review_does_not_call_providers",
    "review_does_not_acquire_market_data",
    "review_does_not_rerun_vpa_wyckoff_execution",
    "review_does_not_rerun_vpa_wyckoff_results_review",
    "review_does_not_rerun_feature_label_matrix_execution",
    "review_does_not_rerun_feature_label_matrix_results_review",
    "review_does_not_rerun_signal_feature_generation",
    "review_does_not_rerun_target_generation",
    "review_does_not_rerun_expectancy_backtest_lab_candidate_creation",
    "do_not_mutate_frozen_dataset",
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
    "source_expectancy_backtest_lab_candidate_digest_bound",
    "source_vpa_wyckoff_results_review_digest_bound",
    "source_vpa_wyckoff_execution_digest_bound",
    "source_vpa_wyckoff_output_binding_digest_bound",
    "source_vpa_wyckoff_rule_values_digest_bound",
    "source_matrix_results_review_digest_bound",
    "source_matrix_rows_digest_bound",
    "source_feature_values_digest_bound",
    "source_target_values_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "source_candidate_status_ready",
    "review_created_true",
    "review_ready_true",
    "ready_for_approval_false",
    "candidate_philosophy_reviewed",
    "recommended_backtest_lab_package_reviewed_not_selected",
    "supporting_backtest_lab_packages_reviewed_not_selected",
    "backtest_objectives_reviewed_10",
    "baselines_reviewed_7",
    "chronological_plan_reviewed",
    "metric_families_reviewed_14",
    "no_peek_controls_reviewed_11",
    "future_outputs_reviewed_not_generated_14",
    "planned_counts_reviewed",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "selection_created_false",
    "approval_created_false",
    "execution_created_false",
    "expectancy_backtest_lab_selected_false",
    "expectancy_backtest_lab_approved_false",
    "expectancy_backtest_lab_authorized_false",
    "expectancy_backtest_lab_executed_false",
    "backtest_rows_created_false",
    "backtest_results_created_false",
    "backtest_execution_authorized_false",
    "backtest_execution_performed_false",
    "model_training_authorized_false",
    "model_training_performed_false",
    "metric_computation_authorized_false",
    "metric_computation_performed_false",
    "strategy_scoring_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "vpa_wyckoff_execution_rerun_false",
    "vpa_wyckoff_results_review_rerun_false",
    "matrix_execution_rerun_false",
    "matrix_results_review_rerun_false",
    "signal_feature_generation_rerun_false",
    "target_generation_rerun_false",
    "expectancy_backtest_lab_candidate_creation_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(ValueError):
    """Raised when an operator review violates its review-only boundary."""


def _reviewed_packages(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["backtest_lab_packages"])
    for index, row in enumerate(rows):
        row["source_status"] = row["status"]
        row["review_status"] = (
            "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
            if index == 0
            else "REVIEWED_AVAILABLE_DIAGNOSTIC_PACKAGE_NOT_SELECTED"
        )
    return rows


def _reviewed_objectives(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["proposed_backtest_objectives"])
    for row in rows:
        row["review_status"] = "REVIEWED_CANDIDATE_OBJECTIVE_NOT_EXECUTED"
    return rows


def _reviewed_baselines(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["candidate_baselines"])
    for row in rows:
        row["review_status"] = "REVIEWED_CANDIDATE_BASELINE_NOT_EXECUTED"
    return rows


def _reviewed_chronological_plan(source: Mapping[str, Any]) -> dict[str, Any]:
    row = deepcopy(source["proposed_chronological_plan"])
    row["review_status"] = "REVIEWED_CHRONOLOGICAL_PLAN_NOT_EXECUTED"
    return row


def _reviewed_metrics(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["proposed_metric_families"])
    for row in rows:
        row["review_status"] = "REVIEWED_CANDIDATE_METRIC_NOT_COMPUTED"
    return rows


def _reviewed_controls(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["proposed_no_peek_and_leakage_controls"])
    for row in rows:
        row["review_status"] = "REVIEWED_PLANNED_CONTROL_NOT_EXECUTED"
    return rows


def _reviewed_outputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["proposed_future_outputs"])
    for row in rows:
        row["review_status"] = "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED"
    return rows


def per_ticker_expectancy_backtest_lab_candidate_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_backtest_lab_candidate_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_review_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_entry in source[
        "per_ticker_expectancy_backtest_lab_candidate_entries"
    ]:
        ticker = source_entry["ticker"]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "expectancy_backtest_lab_candidate_status": candidate_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "expectancy_backtest_lab_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "vpa_wyckoff_results_review_status": candidate_service.source_review.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY,
            "recommended_backtest_lab_package": candidate_service.PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
            "planned_matrix_row_count": source_entry["planned_matrix_row_count"],
            "planned_evaluable_target_row_count": source_entry["planned_evaluable_target_row_count"],
            "planned_unavailable_target_row_count": source_entry["planned_unavailable_target_row_count"],
            "planned_rule_value_row_count": source_entry["planned_rule_value_row_count"],
            "planned_state_value_row_count": source_entry["planned_state_value_row_count"],
            "expectancy_backtest_lab_selected": False,
            "expectancy_backtest_lab_approved": False,
            "expectancy_backtest_lab_authorized": False,
            "expectancy_backtest_lab_executed": False,
            "expectancy_backtest_rows_created": False,
            "expectancy_backtest_results_created": False,
            "backtest_execution_authorized": False,
            "model_training_authorized": False,
            "metric_computation_authorized": False,
            "strategy_scoring_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_expectancy_backtest_lab_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            "source_vpa_wyckoff_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
            "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
            "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
            "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_EXPECTANCY_BACKTEST_LAB_CANDIDATE_REVIEW"
                if ticker == "META"
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_expectancy_backtest_lab_candidate_review_digest"] = (
            per_ticker_expectancy_backtest_lab_candidate_review_digest_v1(entry)
        )
        rows.append(entry)
    return rows


def _base_review(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "review_scope": EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_expectancy_backtest_lab_candidate_artifact_kind": candidate_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1,
        "source_expectancy_backtest_lab_candidate_status": candidate_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_expectancy_backtest_lab_candidate_scope": candidate_service.EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "source_expectancy_backtest_lab_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_rule_baseline_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_baseline_execution_digest": EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST,
        "source_vpa_wyckoff_rule_baseline_output_binding_digest": EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": {
            "marketflow_expectancy_backtest_lab_candidate_v1_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            **deepcopy(source["source_evidence"]),
        },
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"],
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": True,
        "selected_vpa_wyckoff_package": source["selected_vpa_wyckoff_package"],
        "selected_matrix_package": source["selected_matrix_package"],
        "selected_matrix_layout": source["selected_matrix_layout"],
        "selected_feature_package": source["selected_feature_package"],
        "selected_label_target_package": source["selected_label_target_package"],
        "selected_objective_path": source["selected_objective_path"],
        "matrix_row_count": source["matrix_row_count"],
        "available_matrix_row_count": source["available_matrix_row_count"],
        "unavailable_target_matrix_row_count": source["unavailable_target_matrix_row_count"],
        "rule_value_row_count": source["rule_value_row_count"],
        "state_value_row_count": source["state_value_row_count"],
        "selected_rule_family_count": source["selected_rule_family_count"],
        "selected_state_family_count": source["selected_state_family_count"],
        "rule_family_reference_count": source["rule_family_reference_count"],
        "state_family_reference_count": source["state_family_reference_count"],
        "target_profile_count": source["target_profile_count"],
        "feature_group_count_per_matrix_row": source["feature_group_count_per_matrix_row"],
        "target_unavailable_row_count": source["target_unavailable_row_count"],
        "candidate_philosophy": source["candidate_philosophy"],
        "candidate_primary_question": source["candidate_primary_question"],
        "candidate_secondary_question": source["candidate_secondary_question"],
        "candidate_boundary": source["candidate_boundary"],
        "recommended_backtest_lab_package": candidate_service.PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
        "reviewed_backtest_lab_packages": _reviewed_packages(source),
        "reviewed_backtest_objectives": _reviewed_objectives(source),
        "reviewed_baselines": _reviewed_baselines(source),
        "reviewed_chronological_plan": _reviewed_chronological_plan(source),
        "reviewed_metric_families": _reviewed_metrics(source),
        "reviewed_no_peek_and_leakage_controls": _reviewed_controls(source),
        "reviewed_future_outputs": _reviewed_outputs(source),
        "reviewed_planned_counts": deepcopy(source["planned_counts"]),
        "per_ticker_expectancy_backtest_lab_candidate_review_entries": _per_ticker_review_entries(source),
        "expectancy_backtest_lab_candidate_created": True,
        "expectancy_backtest_lab_candidate_ready_for_operator_review": True,
        "expectancy_backtest_lab_candidate_review_created": True,
        "expectancy_backtest_lab_candidate_review_ready": True,
        "ready_for_expectancy_backtest_lab_approval": False,
        "expectancy_backtest_lab_selected": False,
        "expectancy_backtest_lab_approved": False,
        "expectancy_backtest_lab_authorized": False,
        "expectancy_backtest_lab_executed": False,
        "expectancy_backtest_rows_created": False,
        "expectancy_backtest_results_created": False,
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
        "generation_created": False,
        "backtest_execution_authorized": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_computation_authorized": False,
        "metric_computation_performed": False,
        "strategy_scoring_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
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
        "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_rerun_performed": False,
        "target_generation_rerun_performed": False,
        "expectancy_backtest_lab_candidate_creation_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if actual else FAIL,
        "expected": True,
        "actual": bool(actual),
        "severity": "INFO" if actual else BLOCKER,
        "message": "review condition satisfied" if actual else "review condition failed",
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    packages = review.get("reviewed_backtest_lab_packages", [])
    objectives = review.get("reviewed_backtest_objectives", [])
    baselines = review.get("reviewed_baselines", [])
    metrics = review.get("reviewed_metric_families", [])
    controls = review.get("reviewed_no_peek_and_leakage_controls", [])
    outputs = review.get("reviewed_future_outputs", [])
    entries = review.get(
        "per_ticker_expectancy_backtest_lab_candidate_review_entries", []
    )
    recommended = [
        row
        for row in packages
        if row.get("package_id")
        == candidate_service.PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB
    ]
    values = {
        "source_expectancy_backtest_lab_candidate_digest_bound": review.get("source_expectancy_backtest_lab_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_results_review_digest_bound": review.get("source_vpa_wyckoff_rule_baseline_results_review_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_execution_digest_bound": review.get("source_vpa_wyckoff_rule_baseline_execution_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST,
        "source_vpa_wyckoff_output_binding_digest_bound": review.get("source_vpa_wyckoff_rule_baseline_output_binding_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": review.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_matrix_results_review_digest_bound": review.get("source_feature_label_matrix_results_review_digest") == EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_rows_digest_bound": review.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest_bound": review.get("source_feature_values_digest") == EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest_bound": review.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": review.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": review.get("target_universe") == TARGET_UNIVERSE and review.get("target_universe_count") == 12,
        "records_digest_preserved": review.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": review.get("meta_record_count") == 913,
        "source_candidate_status_ready": review.get("source_expectancy_backtest_lab_candidate_status") == candidate_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "review_created_true": review.get("expectancy_backtest_lab_candidate_review_created") is True,
        "review_ready_true": review.get("expectancy_backtest_lab_candidate_review_ready") is True,
        "ready_for_approval_false": review.get("ready_for_expectancy_backtest_lab_approval") is False,
        "candidate_philosophy_reviewed": review.get("candidate_philosophy") == candidate_service.CANDIDATE_PHILOSOPHY,
        "recommended_backtest_lab_package_reviewed_not_selected": len(recommended) == 1 and recommended[0].get("review_status") == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED" and recommended[0].get("selection_created") is False,
        "supporting_backtest_lab_packages_reviewed_not_selected": len(packages) == 4 and all(row.get("selection_created") is False and row.get("approval_created") is False and row.get("execution_created") is False for row in packages),
        "backtest_objectives_reviewed_10": len(objectives) == 10 and all(row.get("review_status") == "REVIEWED_CANDIDATE_OBJECTIVE_NOT_EXECUTED" and row.get("objective_status") == "CANDIDATE_OBJECTIVE_NOT_EXECUTED" for row in objectives),
        "baselines_reviewed_7": len(baselines) == 7 and all(row.get("review_status") == "REVIEWED_CANDIDATE_BASELINE_NOT_EXECUTED" and row.get("baseline_status") == "CANDIDATE_BASELINE_NOT_EXECUTED" for row in baselines),
        "chronological_plan_reviewed": review.get("reviewed_chronological_plan") == _reviewed_chronological_plan({"proposed_chronological_plan": candidate_service._chronological_plan()}),
        "metric_families_reviewed_14": len(metrics) == 14 and all(row.get("review_status") == "REVIEWED_CANDIDATE_METRIC_NOT_COMPUTED" and row.get("metric_status") == "CANDIDATE_METRIC_NOT_COMPUTED" for row in metrics),
        "no_peek_controls_reviewed_11": len(controls) == 11 and all(row.get("review_status") == "REVIEWED_PLANNED_CONTROL_NOT_EXECUTED" and row.get("control_status") == "PLANNED_NOT_EXECUTED" for row in controls),
        "future_outputs_reviewed_not_generated_14": len(outputs) == 14 and all(row.get("review_status") == "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED" and row.get("output_status") == "PLANNED_NOT_GENERATED" for row in outputs),
        "planned_counts_reviewed": review.get("reviewed_planned_counts") == candidate_service._planned_counts(),
        "per_ticker_entries_12": len(entries) == 12 and [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(row.get("per_ticker_expectancy_backtest_lab_candidate_review_digest") == per_ticker_expectancy_backtest_lab_candidate_review_digest_v1(row) for row in entries),
        "selection_created_false": review.get("selection_created") is False,
        "approval_created_false": review.get("approval_created") is False,
        "execution_created_false": review.get("execution_created") is False,
        "expectancy_backtest_lab_selected_false": review.get("expectancy_backtest_lab_selected") is False,
        "expectancy_backtest_lab_approved_false": review.get("expectancy_backtest_lab_approved") is False,
        "expectancy_backtest_lab_authorized_false": review.get("expectancy_backtest_lab_authorized") is False,
        "expectancy_backtest_lab_executed_false": review.get("expectancy_backtest_lab_executed") is False,
        "backtest_rows_created_false": review.get("expectancy_backtest_rows_created") is False,
        "backtest_results_created_false": review.get("expectancy_backtest_results_created") is False,
        "backtest_execution_authorized_false": review.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": review.get("backtest_execution_performed") is False,
        "model_training_authorized_false": review.get("model_training_authorized") is False,
        "model_training_performed_false": review.get("model_training_performed") is False,
        "metric_computation_authorized_false": review.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": review.get("metric_computation_performed") is False,
        "strategy_scoring_false": review.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": review.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": review.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": review.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": review.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": review.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": review.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": review.get("provider_requests_made_in_review") is False,
        "market_data_acquisition_false": review.get("market_data_acquisition_performed_in_review") is False,
        "dataset_regeneration_false": review.get("canonical_dataset_regenerated_in_review") is False,
        "vpa_wyckoff_execution_rerun_false": review.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": review.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": review.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": review.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": review.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": review.get("target_generation_rerun_performed") is False,
        "expectancy_backtest_lab_candidate_creation_rerun_false": review.get("expectancy_backtest_lab_candidate_creation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": review.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": review.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": review.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": review.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": review.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True,
    }
    return values


def _review_checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(review)
    return [_check(check_id, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == PASS for row in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": failed,
        "expectancy_backtest_lab_candidate_review_created": True,
        "expectancy_backtest_lab_candidate_review_ready": True,
        "ready_for_expectancy_backtest_lab_approval": False,
        "recommended_backtest_lab_package": candidate_service.PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
        "expectancy_backtest_rows_created": False,
        "expectancy_backtest_results_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_expectancy_backtest_lab_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    payload.pop(
        "marketflow_expectancy_backtest_lab_candidate_operator_review_digest", None
    )
    return semantic_digest(payload)


def build_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
    candidate: dict | None = None,
) -> dict:
    """Review the candidate without selecting, approving, or executing it."""

    source = (
        candidate_service.build_marketflow_expectancy_backtest_lab_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    candidate_service.validate_marketflow_expectancy_backtest_lab_candidate_v1(source)
    if (
        source["marketflow_expectancy_backtest_lab_candidate_v1_digest"]
        != EXPECTED_SOURCE_CANDIDATE_DIGEST
    ):
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "source candidate digest does not match the reviewed candidate"
        )
    review = _base_review(source)
    checklist = _review_checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    if review["review_summary"]["blocker_count"]:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "expectancy backtest-lab candidate review contains blockers"
        )
    review["marketflow_expectancy_backtest_lab_candidate_operator_review_digest"] = (
        marketflow_expectancy_backtest_lab_candidate_operator_review_digest_v1(review)
    )
    validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
    review: dict,
) -> dict[str, Any]:
    """Validate bound evidence and every closed review authority boundary."""

    if not isinstance(review, dict):
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "operator review must be a JSON object"
        )
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "review_scope": EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "source_expectancy_backtest_lab_candidate_artifact_kind": candidate_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1,
        "source_expectancy_backtest_lab_candidate_status": candidate_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_expectancy_backtest_lab_candidate_scope": candidate_service.EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "source_expectancy_backtest_lab_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_vpa_wyckoff_rule_baseline_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_baseline_execution_digest": EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST,
        "source_vpa_wyckoff_rule_baseline_output_binding_digest": EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "recommended_backtest_lab_package": candidate_service.PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
        "candidate_philosophy": candidate_service.CANDIDATE_PHILOSOPHY,
        "candidate_primary_question": candidate_service.CANDIDATE_PRIMARY_QUESTION,
        "candidate_secondary_question": candidate_service.CANDIDATE_SECONDARY_QUESTION,
        "candidate_boundary": candidate_service.CANDIDATE_BOUNDARY,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        _expect(review.get(field), expected, field)
    for field in (
        "created_offline",
        "research_only",
        "operator_review_required",
        "meta_reduced_record_count_preserved",
        "expectancy_backtest_lab_candidate_created",
        "expectancy_backtest_lab_candidate_ready_for_operator_review",
        "expectancy_backtest_lab_candidate_review_created",
        "expectancy_backtest_lab_candidate_review_ready",
        "no_tracked_marketflow_files",
    ):
        _expect(review.get(field), True, field)
    for field in (
        "ready_for_expectancy_backtest_lab_approval",
        "expectancy_backtest_lab_selected",
        "expectancy_backtest_lab_approved",
        "expectancy_backtest_lab_authorized",
        "expectancy_backtest_lab_executed",
        "expectancy_backtest_rows_created",
        "expectancy_backtest_results_created",
        "selection_created",
        "approval_created",
        "execution_created",
        "generation_created",
        "backtest_execution_authorized",
        "backtest_execution_performed",
        "model_training_authorized",
        "model_training_performed",
        "metric_computation_authorized",
        "metric_computation_performed",
        "strategy_scoring_performed",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "trade_recommendations_generated",
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "vpa_wyckoff_rule_baseline_execution_rerun_performed",
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "signal_feature_generation_rerun_performed",
        "target_generation_rerun_performed",
        "expectancy_backtest_lab_candidate_creation_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    ):
        _expect(review.get(field), False, field)
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)

    expected_source_evidence = {
        "marketflow_expectancy_backtest_lab_candidate_v1_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        **deepcopy(candidate_service.SOURCE_EVIDENCE),
    }
    _expect(review.get("source_evidence"), expected_source_evidence, "source_evidence")
    packages = review.get("reviewed_backtest_lab_packages", [])
    if len(packages) != 4 or [row.get("package_id") for row in packages] != [
        candidate_service.PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
        candidate_service.PACKAGE_EXPECTANCY_FEATURE_ONLY_DIAGNOSTIC_LAB,
        candidate_service.PACKAGE_EXPECTANCY_ABSTENTION_QUALITY_DIAGNOSTIC_LAB,
        candidate_service.PACKAGE_EXPECTANCY_COST_SENSITIVITY_DIAGNOSTIC_LAB,
    ]:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "reviewed backtest-lab packages mismatch"
        )
    objectives = review.get("reviewed_backtest_objectives", [])
    if [row.get("objective_id") for row in objectives] != candidate_service.BACKTEST_OBJECTIVE_IDS:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "reviewed backtest objectives mismatch"
        )
    baselines = review.get("reviewed_baselines", [])
    if [row.get("baseline_id") for row in baselines] != candidate_service.BASELINE_IDS:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "reviewed baselines mismatch"
        )
    expected_randomized = next(
        row
        for row in baselines
        if row["baseline_id"] == "BASELINE_RANDOMIZED_NULL_REFERENCE_BLOCKED"
    )
    _expect(expected_randomized.get("allowed_for_future_execution"), False, "randomized baseline allowed")
    _expect(
        review.get("reviewed_chronological_plan"),
        _reviewed_chronological_plan(
            {"proposed_chronological_plan": candidate_service._chronological_plan()}
        ),
        "reviewed_chronological_plan",
    )
    metrics = review.get("reviewed_metric_families", [])
    if [row.get("metric_family_id") for row in metrics] != candidate_service.METRIC_FAMILY_IDS:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "reviewed metric families mismatch"
        )
    bootstrap = next(
        row
        for row in metrics
        if row["metric_family_id"]
        == "METRIC_CONFIDENCE_INTERVAL_OR_BOOTSTRAP_BLOCKED"
    )
    _expect(bootstrap.get("allowed_for_future_execution"), False, "bootstrap allowed")
    controls = review.get("reviewed_no_peek_and_leakage_controls", [])
    if [row.get("control_id") for row in controls] != candidate_service.NO_PEEK_CONTROL_IDS:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "reviewed no-peek controls mismatch"
        )
    outputs = review.get("reviewed_future_outputs", [])
    if [row.get("output_id") for row in outputs] != candidate_service.FUTURE_OUTPUT_IDS:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "reviewed future outputs mismatch"
        )
    _expect(
        review.get("reviewed_planned_counts"),
        candidate_service._planned_counts(),
        "reviewed_planned_counts",
    )
    entries = review.get(
        "per_ticker_expectancy_backtest_lab_candidate_review_entries"
    )
    if not isinstance(entries, list) or [row.get("ticker") for row in entries] != TARGET_UNIVERSE:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "per-ticker review entries mismatch"
        )
    for row in entries:
        _expect(
            row.get("per_ticker_expectancy_backtest_lab_candidate_review_digest"),
            per_ticker_expectancy_backtest_lab_candidate_review_digest_v1(row),
            f"{row.get('ticker')} review digest",
        )
    checklist = _review_checklist(review)
    _expect(review.get("review_checklist"), checklist, "review_checklist")
    if any(row["status"] != PASS for row in checklist):
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "review checklist contains failures"
        )
    _expect(review.get("review_summary"), _summary(checklist), "review_summary")
    digest = review.get(
        "marketflow_expectancy_backtest_lab_candidate_operator_review_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "operator review digest missing"
        )
    _expect(
        digest,
        marketflow_expectancy_backtest_lab_candidate_operator_review_digest_v1(review),
        "operator review digest",
    )
    return {
        "status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_expectancy_backtest_lab_candidate_operator_review_digest": digest,
        "total_checks": review["review_summary"]["total_checks"],
        "passed_checks": review["review_summary"]["passed_checks"],
        "failed_checks": 0,
        "blocker_count": 0,
    }


def build_marketflow_expectancy_backtest_lab_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a validated review package as operator-readable Markdown."""

    validation = validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
        review
    )
    sections = [
        (
            "Expectancy Backtest Lab Candidate Operator Review v1",
            [
                f"Artifact/status/scope: {review['artifact_kind']} / {review['review_status']} / {review['review_scope']}.",
                f"Review digest: {validation['marketflow_expectancy_backtest_lab_candidate_operator_review_digest']}.",
            ],
        ),
        (
            "Source Candidate",
            [
                f"Candidate {EXPECTED_SOURCE_CANDIDATE_DIGEST} was validated and reviewed without selection or rerun."
            ],
        ),
        (
            "Source VPA/Wyckoff Results Review",
            [
                f"Results-review digest {EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST} remains bound."
            ],
        ),
        (
            "Source Feature-Label Matrix Results Review",
            [
                f"Matrix review {EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST} remains bound."
            ],
        ),
        (
            "Bound Evidence",
            [
                "Candidate, VPA/Wyckoff, matrix, feature, target, records, and the complete upstream digest chain remain bound."
            ],
        ),
        (
            "Dataset and Universe",
            [
                "The ordered twelve-ticker universe and 11,946 records are preserved; META remains exactly 913."
            ],
        ),
        (
            "Reviewed Candidate Basis",
            [
                "179,190 matrix/rule/state rows, 177,090 evaluable targets, 2,100 unavailable targets, eight rule families, six state families, thirteen feature groups, and fifteen target profiles were reviewed."
            ],
        ),
        (
            "Reviewed Candidate Philosophy",
            [candidate_service.CANDIDATE_PHILOSOPHY, candidate_service.CANDIDATE_BOUNDARY],
        ),
        (
            "Reviewed Recommended Backtest Lab Package",
            [
                candidate_service.PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB
                + " remains not selected."
            ],
        ),
        (
            "Reviewed Supporting Backtest Lab Packages",
            [row["package_id"] for row in review["reviewed_backtest_lab_packages"][1:]],
        ),
        (
            "Reviewed Backtest Objectives",
            candidate_service.BACKTEST_OBJECTIVE_IDS,
        ),
        ("Reviewed Baselines", candidate_service.BASELINE_IDS),
        (
            "Reviewed Chronological Plan",
            [
                "2022-2023 calibration, 2024 validation, and 2025 holdout remain planned, chronological, unshuffled, embargoed, and unexecuted."
            ],
        ),
        ("Reviewed Metric Families", candidate_service.METRIC_FAMILY_IDS),
        (
            "Reviewed No-Peek and Leakage Controls",
            candidate_service.NO_PEEK_CONTROL_IDS,
        ),
        ("Reviewed Planned Outputs", candidate_service.FUTURE_OUTPUT_IDS),
        (
            "Reviewed Planned Counts",
            [
                f"{key}: {value}"
                for key, value in review["reviewed_planned_counts"].items()
            ],
        ),
        (
            "Per-Ticker Review Summary",
            [
                "Twelve digest-bound entries preserve 15,045 planned rows per non-META ticker and 13,695 for META."
            ],
        ),
        ("Next Chain", NEXT_CHAIN),
        ("Next Gates", NEXT_GATES),
        ("Risk Controls", RISK_CONTROLS),
        (
            "Predictive Usefulness Boundary",
            ["Predictive usefulness remains not accepted."],
        ),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        (
            "Runtime Boundary",
            [
                "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."
            ],
        ),
        (
            "Checklist Summary",
            [
                f"{review['review_summary']['passed_checks']}/{review['review_summary']['total_checks']} checks pass with zero blockers."
            ],
        ),
        (
            "Guardrails",
            [
                "This review selects and approves nothing; it creates no backtest rows/results, metrics, models, scores, recommendations, acceptance, runtime, or trading authority."
            ],
        ),
    ]
    lines: list[str] = []
    for index, (title, body) in enumerate(sections):
        lines.append(("# " if index == 0 else "## ") + title)
        lines.append("")
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Write review JSON and Markdown only to an explicit directory."""

    review = build_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
        candidate
    )
    validation = validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
        review
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_expectancy_backtest_lab_candidate_operator_review_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowExpectancyBacktestLabCandidateOperatorReviewError(
            "operator-review output already exists"
        )
    json_path.write_bytes(canonical_json_bytes(review))
    markdown_path.write_text(
        build_marketflow_expectancy_backtest_lab_candidate_operator_review_markdown_v1(
            review
        ),
        encoding="utf-8",
        newline="\n",
    )
    return {
        **validation,
        "json_path": str(json_path.resolve()),
        "markdown_path": str(markdown_path.resolve()),
    }
