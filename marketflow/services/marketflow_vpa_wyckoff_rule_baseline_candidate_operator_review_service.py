"""Offline operator review of the VPA/Wyckoff rule baseline candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_vpa_wyckoff_rule_baseline_candidate_service as candidate_service,
)


ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE"
)
SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"
)
VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL = (
    "VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_VALID = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_VALID"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "7f5bd67e553834978bf6e2fb0a5142e450e55941696704d6da489c1a23b97d66"
)
EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST = (
    candidate_service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST = (
    candidate_service.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST
)
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = candidate_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_FEATURE_VALUES_DIGEST = (
    candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST
)
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = (
    candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
)
EXPECTED_SOURCE_RECORDS_DIGEST = candidate_service.EXPECTED_SOURCE_RECORDS_DIGEST
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER

NEXT_CHAIN = [
    "VPA/Wyckoff Rule Baseline Approval v1, if selected.",
    "VPA/Wyckoff Rule Baseline Execution v1, if approved.",
    "VPA/Wyckoff Rule Baseline Results Review v1.",
    "Expectancy Backtest Lab Candidate only after separate approval.",
    "Results review and readiness gates before any predictive-usefulness acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "vpa_wyckoff_rule_baseline_approval_if_selected",
    "vpa_wyckoff_rule_baseline_execution_if_approved",
    "vpa_wyckoff_rule_baseline_results_review",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_select_vpa_wyckoff_package",
    "review_does_not_approve_vpa_wyckoff_execution",
    "review_does_not_execute_vpa_wyckoff_rules",
    "review_does_not_create_rule_values",
    "review_does_not_create_baseline_outputs",
    "review_does_not_create_expectancy_backtest_lab_candidate",
    "review_does_not_run_backtest",
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
    "review_does_not_rerun_feature_label_matrix_execution",
    "review_does_not_rerun_feature_label_matrix_results_review",
    "review_does_not_rerun_vpa_wyckoff_candidate_creation",
    "do_not_mutate_frozen_dataset",
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
    "source_vpa_wyckoff_candidate_digest_bound",
    "source_matrix_results_review_digest_bound",
    "source_matrix_execution_digest_bound",
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
    "rule_families_reviewed_10",
    "wyckoff_state_families_reviewed_8",
    "recommended_package_reviewed_not_selected",
    "supporting_package_reviewed_not_selected",
    "feature_group_mapping_reviewed",
    "design_questions_reviewed_12",
    "future_outputs_reviewed_not_generated_10",
    "planned_counts_reviewed",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "selection_created_false",
    "approval_created_false",
    "execution_created_false",
    "vpa_wyckoff_rule_baseline_selected_false",
    "vpa_wyckoff_rule_baseline_approved_false",
    "vpa_wyckoff_rule_baseline_authorized_false",
    "vpa_wyckoff_rule_baseline_executed_false",
    "vpa_wyckoff_rule_values_created_false",
    "vpa_wyckoff_baseline_outputs_created_false",
    "expectancy_backtest_lab_candidate_created_false",
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
    "feature_label_matrix_execution_rerun_false",
    "feature_label_matrix_results_review_rerun_false",
    "vpa_wyckoff_candidate_creation_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError(ValueError):
    """Raised when the VPA/Wyckoff operator review violates its boundary."""


def _reviewed_rule_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["proposed_vpa_wyckoff_rule_families"])
    for row in rows:
        row["review_status"] = "REVIEWED_VPA_WYCKOFF_RULE_CANDIDATE_NOT_EXECUTED"
        row["approval_status"] = "NOT_APPROVED_BY_THIS_REVIEW"
    return rows


def _reviewed_state_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["proposed_wyckoff_state_families"])
    for row in rows:
        row["review_status"] = "REVIEWED_WYCKOFF_STATE_CANDIDATE_NOT_EXECUTED"
        row["approval_status"] = "NOT_APPROVED_BY_THIS_REVIEW"
    return rows


def _reviewed_packages(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["proposed_baseline_packages"])
    review_statuses = [
        "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "REVIEWED_AVAILABLE_SUPPORTING_PACKAGE_NOT_SELECTED",
    ]
    for row, review_status in zip(rows, review_statuses, strict=True):
        row["source_status"] = row["status"]
        row["review_status"] = review_status
    return rows


def _reviewed_mappings(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["source_feature_group_mapping"])
    for row in rows:
        row["review_status"] = "REVIEWED_PLANNED_MAPPING_NOT_EXECUTED"
    return rows


def _reviewed_questions(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["rule_design_questions"])
    for row in rows:
        row["review_status"] = "REVIEWED_QUESTION_NOT_ANSWERED"
    return rows


def _reviewed_outputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = deepcopy(source["planned_future_outputs"])
    for row in rows:
        row["review_status"] = "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED"
    return rows


def per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_review_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_entry in source[
        "per_ticker_vpa_wyckoff_rule_baseline_candidate_entries"
    ]:
        ticker = source_entry["ticker"]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "feature_label_matrix_results_review_status": candidate_service.matrix_review.MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE_READY,
            "vpa_wyckoff_rule_baseline_candidate_status": candidate_service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "vpa_wyckoff_rule_baseline_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "selected_matrix_package": candidate_service.execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
            "selected_feature_package": candidate_service.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": candidate_service.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": candidate_service.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "recommended_vpa_wyckoff_package": candidate_service.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
            "planned_matrix_row_count": source_entry["planned_matrix_row_count"],
            "planned_rule_family_count": 10,
            "planned_wyckoff_state_family_count": 8,
            "vpa_wyckoff_rule_baseline_selected": False,
            "vpa_wyckoff_rule_baseline_approved": False,
            "vpa_wyckoff_rule_baseline_authorized": False,
            "vpa_wyckoff_rule_baseline_executed": False,
            "vpa_wyckoff_rule_values_created": False,
            "vpa_wyckoff_baseline_outputs_created": False,
            "expectancy_backtest_lab_candidate_created": False,
            "backtest_execution_authorized": False,
            "model_training_authorized": False,
            "metric_computation_authorized": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_vpa_wyckoff_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            "source_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
            "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_REVIEW"
                if ticker == "META" else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest"] = (
            per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest_v1(entry)
        )
        rows.append(entry)
    return rows


def _base_review(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "review_scope": VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "source_vpa_wyckoff_rule_baseline_candidate_artifact_kind": candidate_service.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1,
        "source_vpa_wyckoff_rule_baseline_candidate_status": candidate_service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_vpa_wyckoff_rule_baseline_candidate_scope": candidate_service.VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "source_vpa_wyckoff_rule_baseline_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_feature_label_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": {
            "marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            **deepcopy(source["source_evidence"]),
        },
        "selected_matrix_package": source["selected_matrix_package"],
        "selected_matrix_layout": source["selected_matrix_layout"],
        "selected_feature_package": source["selected_feature_package"],
        "selected_label_target_package": source["selected_label_target_package"],
        "selected_objective_path": source["selected_objective_path"],
        "dataset_name": source["dataset_name"], "source_profile": source["source_profile"],
        "timeframe": source["timeframe"], "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "records_digest": source["records_digest"],
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": True,
        "matrix_row_count": source["matrix_row_count"],
        "available_matrix_row_count": source["available_matrix_row_count"],
        "unavailable_target_matrix_row_count": source["unavailable_target_matrix_row_count"],
        "feature_group_count_per_matrix_row": source["feature_group_count_per_matrix_row"],
        "feature_group_reference_count": source["feature_group_reference_count"],
        "feature_source_row_count": source["feature_source_row_count"],
        "target_source_row_count": source["target_source_row_count"],
        "candidate_philosophy": source["candidate_philosophy"],
        "candidate_primary_question": source["candidate_primary_question"],
        "candidate_secondary_question": source["candidate_secondary_question"],
        "candidate_boundary": source["candidate_boundary"],
        "reviewed_vpa_wyckoff_rule_families": _reviewed_rule_families(source),
        "reviewed_wyckoff_state_families": _reviewed_state_families(source),
        "recommended_vpa_wyckoff_package": candidate_service.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "supporting_vpa_wyckoff_package": candidate_service.PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT,
        "reviewed_baseline_packages": _reviewed_packages(source),
        "reviewed_feature_group_mapping": _reviewed_mappings(source),
        "reviewed_rule_design_questions": _reviewed_questions(source),
        "reviewed_planned_future_outputs": _reviewed_outputs(source),
        "planned_source_matrix_row_count": source["planned_source_matrix_row_count"],
        "planned_rule_family_count": source["planned_rule_family_count"],
        "planned_wyckoff_state_family_count": source["planned_wyckoff_state_family_count"],
        "planned_primary_package_rule_family_count": source["planned_primary_package_rule_family_count"],
        "planned_primary_package_state_family_count": source["planned_primary_package_state_family_count"],
        "planned_rule_value_rows": source["planned_rule_value_rows"],
        "planned_rule_state_rows": source["planned_rule_state_rows"],
        "planned_rule_evaluation_scope": source["planned_rule_evaluation_scope"],
        "metric_counts_approved": False,
        "per_ticker_vpa_wyckoff_rule_baseline_candidate_review_entries": _per_ticker_review_entries(source),
        "vpa_wyckoff_rule_baseline_candidate_created": True,
        "vpa_wyckoff_rule_baseline_candidate_ready_for_operator_review": True,
        "vpa_wyckoff_rule_baseline_candidate_review_created": True,
        "vpa_wyckoff_rule_baseline_candidate_review_ready": True,
        "ready_for_vpa_wyckoff_rule_baseline_approval": False,
        "vpa_wyckoff_rule_baseline_selected": False,
        "vpa_wyckoff_rule_baseline_approved": False,
        "vpa_wyckoff_rule_baseline_authorized": False,
        "vpa_wyckoff_rule_baseline_executed": False,
        "vpa_wyckoff_rule_values_created": False,
        "vpa_wyckoff_baseline_outputs_created": False,
        "selection_created": False, "approval_created": False, "execution_created": False,
        "generation_created": False, "expectancy_backtest_lab_candidate_created": False,
        "backtest_execution_authorized": False, "backtest_execution_performed": False,
        "model_training_authorized": False, "model_training_performed": False,
        "metric_computation_authorized": False, "metric_computation_performed": False,
        "strategy_scoring_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability": NOT_ACCEPTED, "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False, "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False, "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "vpa_wyckoff_candidate_creation_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "review condition satisfied" if actual else "review condition failed",
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    entries = review.get("per_ticker_vpa_wyckoff_rule_baseline_candidate_review_entries", [])
    values = {
        "source_vpa_wyckoff_candidate_digest_bound": review.get("source_vpa_wyckoff_rule_baseline_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_matrix_results_review_digest_bound": review.get("source_feature_label_matrix_results_review_digest") == EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_execution_digest_bound": review.get("source_feature_label_matrix_execution_digest") == EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_matrix_rows_digest_bound": review.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest_bound": review.get("source_feature_values_digest") == EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest_bound": review.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": review.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": review.get("target_universe") == TARGET_UNIVERSE and review.get("target_universe_count") == 12,
        "records_digest_preserved": review.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": review.get("meta_record_count") == 913,
        "source_candidate_status_ready": review.get("source_vpa_wyckoff_rule_baseline_candidate_status") == candidate_service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "review_created_true": review.get("vpa_wyckoff_rule_baseline_candidate_review_created") is True,
        "review_ready_true": review.get("vpa_wyckoff_rule_baseline_candidate_review_ready") is True,
        "ready_for_approval_false": review.get("ready_for_vpa_wyckoff_rule_baseline_approval") is False,
        "candidate_philosophy_reviewed": review.get("candidate_philosophy") == candidate_service.CANDIDATE_PHILOSOPHY,
        "rule_families_reviewed_10": len(review.get("reviewed_vpa_wyckoff_rule_families", [])) == 10 and all(row.get("review_status") == "REVIEWED_VPA_WYCKOFF_RULE_CANDIDATE_NOT_EXECUTED" for row in review.get("reviewed_vpa_wyckoff_rule_families", [])),
        "wyckoff_state_families_reviewed_8": len(review.get("reviewed_wyckoff_state_families", [])) == 8 and all(row.get("review_status") == "REVIEWED_WYCKOFF_STATE_CANDIDATE_NOT_EXECUTED" for row in review.get("reviewed_wyckoff_state_families", [])),
        "recommended_package_reviewed_not_selected": len(review.get("reviewed_baseline_packages", [])) == 2 and review["reviewed_baseline_packages"][0].get("review_status") == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED" and review["reviewed_baseline_packages"][0].get("selection_created") is False,
        "supporting_package_reviewed_not_selected": len(review.get("reviewed_baseline_packages", [])) == 2 and review["reviewed_baseline_packages"][1].get("review_status") == "REVIEWED_AVAILABLE_SUPPORTING_PACKAGE_NOT_SELECTED" and review["reviewed_baseline_packages"][1].get("selection_created") is False,
        "feature_group_mapping_reviewed": len(review.get("reviewed_feature_group_mapping", [])) == 13 and all(row.get("review_status") == "REVIEWED_PLANNED_MAPPING_NOT_EXECUTED" for row in review.get("reviewed_feature_group_mapping", [])),
        "design_questions_reviewed_12": len(review.get("reviewed_rule_design_questions", [])) == 12 and all(row.get("review_status") == "REVIEWED_QUESTION_NOT_ANSWERED" for row in review.get("reviewed_rule_design_questions", [])),
        "future_outputs_reviewed_not_generated_10": len(review.get("reviewed_planned_future_outputs", [])) == 10 and all(row.get("review_status") == "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED" and row.get("output_status") == "PLANNED_NOT_GENERATED" for row in review.get("reviewed_planned_future_outputs", [])),
        "planned_counts_reviewed": all(review.get(field) == expected for field, expected in {
            "planned_source_matrix_row_count": 179190, "planned_rule_family_count": 10,
            "planned_wyckoff_state_family_count": 8,
            "planned_primary_package_rule_family_count": 8,
            "planned_primary_package_state_family_count": 6,
            "planned_rule_value_rows": 179190, "planned_rule_state_rows": 179190,
        }.items()),
        "per_ticker_entries_12": len(entries) == 12 and [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(row.get("per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest") == per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest_v1(row) for row in entries),
        "selection_created_false": review.get("selection_created") is False,
        "approval_created_false": review.get("approval_created") is False,
        "execution_created_false": review.get("execution_created") is False,
        "vpa_wyckoff_rule_baseline_selected_false": review.get("vpa_wyckoff_rule_baseline_selected") is False,
        "vpa_wyckoff_rule_baseline_approved_false": review.get("vpa_wyckoff_rule_baseline_approved") is False,
        "vpa_wyckoff_rule_baseline_authorized_false": review.get("vpa_wyckoff_rule_baseline_authorized") is False,
        "vpa_wyckoff_rule_baseline_executed_false": review.get("vpa_wyckoff_rule_baseline_executed") is False,
        "vpa_wyckoff_rule_values_created_false": review.get("vpa_wyckoff_rule_values_created") is False,
        "vpa_wyckoff_baseline_outputs_created_false": review.get("vpa_wyckoff_baseline_outputs_created") is False,
        "expectancy_backtest_lab_candidate_created_false": review.get("expectancy_backtest_lab_candidate_created") is False,
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
        "feature_label_matrix_execution_rerun_false": review.get("feature_label_matrix_execution_rerun_performed") is False,
        "feature_label_matrix_results_review_rerun_false": review.get("feature_label_matrix_results_review_rerun_performed") is False,
        "vpa_wyckoff_candidate_creation_rerun_false": review.get("vpa_wyckoff_candidate_creation_rerun_performed") is False,
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
        "total_checks": len(checklist), "passed_checks": passed,
        "failed_checks": failed, "blocker_count": failed,
        "vpa_wyckoff_rule_baseline_candidate_review_created": True,
        "vpa_wyckoff_rule_baseline_candidate_review_ready": True,
        "ready_for_vpa_wyckoff_rule_baseline_approval": False,
        "recommended_vpa_wyckoff_package": candidate_service.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selection_created": False, "approval_created": False, "execution_created": False,
        "vpa_wyckoff_rule_values_created": False,
        "vpa_wyckoff_baseline_outputs_created": False,
        "expectancy_backtest_lab_candidate_created": False,
        "backtest_execution_performed": False, "model_training_performed": False,
        "metric_computation_performed": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    payload.pop("marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest", None)
    return semantic_digest(payload)


def build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(
    candidate: dict | None = None,
) -> dict:
    """Review the candidate without selecting, approving, or executing it."""
    source = (
        candidate_service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_v1()
        if candidate is None else deepcopy(candidate)
    )
    candidate_service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(source)
    if source["marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest"] != EXPECTED_SOURCE_CANDIDATE_DIGEST:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError(
            "source candidate digest does not match the reviewed candidate"
        )
    review = _base_review(source)
    checklist = _review_checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    if review["review_summary"]["blocker_count"]:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError(
            "VPA/Wyckoff candidate operator review checklist contains blockers"
        )
    review["marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest"] = (
        marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest_v1(review)
    )
    validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate the review-only evidence and every closed authority boundary."""
    if not isinstance(review, dict):
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError(
            "operator review must be a JSON object"
        )
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "review_scope": VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "source_vpa_wyckoff_rule_baseline_candidate_artifact_kind": candidate_service.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1,
        "source_vpa_wyckoff_rule_baseline_candidate_status": candidate_service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_vpa_wyckoff_rule_baseline_candidate_scope": candidate_service.VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "source_vpa_wyckoff_rule_baseline_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_feature_label_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_matrix_package": candidate_service.execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": candidate_service.execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": candidate_service.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": candidate_service.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": candidate_service.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "recommended_vpa_wyckoff_package": candidate_service.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "supporting_vpa_wyckoff_package": candidate_service.PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        _expect(review.get(field), expected, field)
    for field in (
        "created_offline", "research_only", "operator_review_required",
        "vpa_wyckoff_rule_baseline_candidate_created",
        "vpa_wyckoff_rule_baseline_candidate_ready_for_operator_review",
        "vpa_wyckoff_rule_baseline_candidate_review_created",
        "vpa_wyckoff_rule_baseline_candidate_review_ready",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    ):
        _expect(review.get(field), True, field)
    for field in (
        "ready_for_vpa_wyckoff_rule_baseline_approval",
        "vpa_wyckoff_rule_baseline_selected", "vpa_wyckoff_rule_baseline_approved",
        "vpa_wyckoff_rule_baseline_authorized", "vpa_wyckoff_rule_baseline_executed",
        "vpa_wyckoff_rule_values_created", "vpa_wyckoff_baseline_outputs_created",
        "selection_created", "approval_created", "execution_created", "generation_created",
        "expectancy_backtest_lab_candidate_created", "backtest_execution_authorized",
        "backtest_execution_performed", "model_training_authorized", "model_training_performed",
        "metric_computation_authorized", "metric_computation_performed",
        "strategy_scoring_performed", "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "vpa_wyckoff_candidate_creation_rerun_performed",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed", "metric_counts_approved",
    ):
        _expect(review.get(field), False, field)
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    expected_structures = {
        "candidate_philosophy": candidate_service.CANDIDATE_PHILOSOPHY,
        "candidate_primary_question": candidate_service.CANDIDATE_PRIMARY_QUESTION,
        "candidate_secondary_question": candidate_service.CANDIDATE_SECONDARY_QUESTION,
        "candidate_boundary": candidate_service.CANDIDATE_BOUNDARY,
    }
    for field, expected in expected_structures.items():
        _expect(review.get(field), expected, field)
    if len(review.get("reviewed_vpa_wyckoff_rule_families", [])) != 10:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError("reviewed rule families mismatch")
    if len(review.get("reviewed_wyckoff_state_families", [])) != 8:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError("reviewed state families mismatch")
    if len(review.get("reviewed_baseline_packages", [])) != 2:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError("reviewed packages mismatch")
    if len(review.get("reviewed_feature_group_mapping", [])) != 13:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError("reviewed mappings mismatch")
    if len(review.get("reviewed_rule_design_questions", [])) != 12:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError("reviewed questions mismatch")
    if len(review.get("reviewed_planned_future_outputs", [])) != 10:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError("reviewed outputs mismatch")
    entries = review.get("per_ticker_vpa_wyckoff_rule_baseline_candidate_review_entries")
    if not isinstance(entries, list) or [row.get("ticker") for row in entries] != TARGET_UNIVERSE:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError("per-ticker review entries mismatch")
    for row in entries:
        _expect(
            row.get("per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest"),
            per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest_v1(row),
            f"{row.get('ticker')} review digest",
        )
    checklist = _review_checklist(review)
    _expect(review.get("review_checklist"), checklist, "review_checklist")
    if any(row["status"] != PASS for row in checklist):
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError(
            "review checklist contains failures"
        )
    _expect(review.get("review_summary"), _summary(checklist), "review_summary")
    digest = review.get(
        "marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError(
            "operator review digest missing"
        )
    _expect(
        digest,
        marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest_v1(review),
        "operator review digest",
    )
    return {
        "status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest": digest,
        "total_checks": review["review_summary"]["total_checks"],
        "passed_checks": review["review_summary"]["passed_checks"],
        "failed_checks": 0, "blocker_count": 0,
    }


def build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a validated operator-review package as Markdown."""
    validation = validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(review)
    sections = [
        ("VPA/Wyckoff Rule Baseline Candidate Operator Review v1", [
            f"Artifact/status/scope: `{review['artifact_kind']}` / `{review['review_status']}` / `{review['review_scope']}`.",
            f"Review digest: `{validation['marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest']}`.",
        ]),
        ("Source VPA/Wyckoff Candidate", [f"Candidate `{EXPECTED_SOURCE_CANDIDATE_DIGEST}` was validated and reviewed without selection or rerun."]),
        ("Source Feature-Label Matrix Results Review", [f"Matrix review `{EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST}` remains bound evidence."]),
        ("Bound Evidence", ["Candidate, matrix execution/rows, feature/target values, records, and the upstream chain remain digest-bound."]),
        ("Dataset and Universe", ["The ordered twelve-ticker universe and 11,946 records are preserved; META remains 913."]),
        ("Reviewed Candidate Basis", ["179,190 matrix rows, thirteen feature groups, and candidate-only planned rule/state outputs were reviewed."]),
        ("Reviewed Candidate Philosophy", [candidate_service.CANDIDATE_PHILOSOPHY, candidate_service.CANDIDATE_BOUNDARY]),
        ("Reviewed VPA/Wyckoff Rule Families", candidate_service.VPA_RULE_FAMILY_IDS),
        ("Reviewed Wyckoff State Families", candidate_service.WYCKOFF_STATE_FAMILY_IDS),
        ("Reviewed Recommended Package", [candidate_service.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE + " remains not selected."]),
        ("Reviewed Supporting Package", [candidate_service.PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT + " remains not selected."]),
        ("Reviewed Feature Group Mapping", [f"{group} -> {', '.join(targets)}" for group, targets in candidate_service.SOURCE_FEATURE_GROUP_MAPPING]),
        ("Reviewed Rule Design Questions", candidate_service.RULE_DESIGN_QUESTION_TEXTS),
        ("Reviewed Planned Outputs", candidate_service.FUTURE_OUTPUT_IDS),
        ("Reviewed Planned Counts", ["Ten rule families, eight states, and 179,190 planned rule/state rows were reviewed; no metric count is approved."]),
        ("Per-Ticker Review Summary", ["Twelve digest-bound entries preserve 15,045 planned rows per non-META ticker and 13,695 for META."]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES),
        ("Risk Controls", RISK_CONTROLS),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{review['review_summary']['passed_checks']}/{review['review_summary']['total_checks']} checks pass with zero blockers."]),
        ("Guardrails", ["This review selects and approves nothing; it creates no rule values, outputs, backtests, models, metrics, recommendations, acceptance, runtime, or trading authority."]),
    ]
    lines: list[str] = []
    for index, (title, body) in enumerate(sections):
        lines.append(("# " if index == 0 else "## ") + title)
        lines.append("")
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict:
    """Write review JSON and Markdown only to an explicit directory."""
    review = build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(
        candidate
    )
    validation = validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(
        review
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError(
            "operator-review output already exists"
        )
    json_path.write_bytes(canonical_json_bytes(review))
    markdown_path.write_text(
        build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_markdown_v1(review),
        encoding="utf-8", newline="\n",
    )
    return {
        **validation,
        "json_path": str(json_path.resolve()),
        "markdown_path": str(markdown_path.resolve()),
    }
