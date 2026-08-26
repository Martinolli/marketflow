"""Offline candidate for a future research-only expectancy backtest laboratory."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_vpa_wyckoff_rule_baseline_results_review_service as source_review,
)


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1 = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1 = (
    "marketflow_expectancy_backtest_lab_candidate_v1"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION = (
    "EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
)
MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_VALID = (
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_VALID"
)

PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB = (
    "PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB"
)
PACKAGE_EXPECTANCY_FEATURE_ONLY_DIAGNOSTIC_LAB = (
    "PACKAGE_EXPECTANCY_FEATURE_ONLY_DIAGNOSTIC_LAB"
)
PACKAGE_EXPECTANCY_ABSTENTION_QUALITY_DIAGNOSTIC_LAB = (
    "PACKAGE_EXPECTANCY_ABSTENTION_QUALITY_DIAGNOSTIC_LAB"
)
PACKAGE_EXPECTANCY_COST_SENSITIVITY_DIAGNOSTIC_LAB = (
    "PACKAGE_EXPECTANCY_COST_SENSITIVITY_DIAGNOSTIC_LAB"
)

EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST = (
    "afdb0f141a412652b2dfca5abc08033f3858a6a5fb4b7a9e9eefc032643405fe"
)
EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST = (
    source_review.EXPECTED_SOURCE_EXECUTION_DIGEST
)
EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST = (
    source_review.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST
)
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = (
    source_review.EXPECTED_SOURCE_RULE_VALUES_DIGEST
)
EXPECTED_SOURCE_VPA_WYCKOFF_APPROVAL_DIGEST = (
    source_review.EXPECTED_SOURCE_APPROVAL_DIGEST
)
EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST = (
    source_review.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST = (
    source_review.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST
)
EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST = (
    source_review.EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST
)
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = source_review.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_FEATURE_VALUES_DIGEST = source_review.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = source_review.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_review.EXPECTED_SOURCE_RECORDS_DIGEST

TARGET_UNIVERSE = list(source_review.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(source_review.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = source_review.NOT_ACCEPTED
NOT_AUTHORIZED = source_review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

SOURCE_EVIDENCE = {
    "marketflow_vpa_wyckoff_rule_baseline_results_review_digest": (
        EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST
    ),
    "marketflow_vpa_wyckoff_rule_baseline_execution_digest": (
        EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST
    ),
    "vpa_wyckoff_rule_baseline_output_binding_digest": (
        EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST
    ),
    "vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
    "marketflow_vpa_wyckoff_rule_baseline_approval_digest": (
        EXPECTED_SOURCE_VPA_WYCKOFF_APPROVAL_DIGEST
    ),
    "marketflow_feature_label_matrix_results_review_digest": (
        EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST
    ),
    "marketflow_feature_label_matrix_execution_digest": (
        EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST
    ),
    "feature_label_matrix_output_binding_digest": (
        EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST
    ),
    "feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
    "feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
    "target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
    "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
    **deepcopy(
        source_review.execution.approval_service.review_service.candidate_service.SOURCE_EVIDENCE
    ),
}

CANDIDATE_PHILOSOPHY = (
    "Prepare a future research-only backtest laboratory that compares expectancy "
    "target outcomes, history-only feature bundles, and transparent VPA/Wyckoff "
    "rule-state tags without producing recommendations, runtime authority, or "
    "predictive-usefulness acceptance."
)
CANDIDATE_PRIMARY_QUESTION = (
    "Can expectancy-oriented targets and VPA/Wyckoff rule states produce research "
    "evidence of tradable expectancy after costs, abstention, and risk constraints "
    "better than simple baselines?"
)
CANDIDATE_SECONDARY_QUESTION = (
    "Which combination of target families, VPA/Wyckoff states, feature bundles, "
    "abstention rules, and simple baselines should be evaluated first under "
    "chronological no-peek controls?"
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no backtest rows, results, metrics, models, scores, "
    "recommendations, acceptance, profitability, or runtime artifacts are created."
)

BACKTEST_OBJECTIVE_IDS = [
    "BACKTEST_OBJECTIVE_EXPECTANCY_AFTER_COST",
    "BACKTEST_OBJECTIVE_PAYOFF_ASYMMETRY",
    "BACKTEST_OBJECTIVE_REWARD_TO_RISK_ALIGNMENT",
    "BACKTEST_OBJECTIVE_MATERIAL_MOVE_AFTER_COST",
    "BACKTEST_OBJECTIVE_ABSTENTION_QUALITY",
    "BACKTEST_OBJECTIVE_VPA_WYCKOFF_STATE_ALIGNMENT",
    "BACKTEST_OBJECTIVE_PER_TICKER_STABILITY",
    "BACKTEST_OBJECTIVE_CHRONOLOGICAL_STABILITY",
    "BACKTEST_OBJECTIVE_META_LIMITATION_SENSITIVITY",
    "BACKTEST_OBJECTIVE_SIMPLE_BASELINE_COMPARISON",
]
BASELINE_IDS = [
    "BASELINE_ALWAYS_ABSTAIN",
    "BASELINE_ALWAYS_AVAILABLE_TARGET",
    "BASELINE_SIMPLE_BUY_AND_HOLD_REFERENCE",
    "BASELINE_PREVIOUS_DIRECTION_REFERENCE",
    "BASELINE_RANDOMIZED_NULL_REFERENCE_BLOCKED",
    "BASELINE_VPA_WYCKOFF_RULE_TAG_REFERENCE",
    "BASELINE_TARGET_PROFILE_PRIOR_RATE_REFERENCE",
]
METRIC_FAMILY_IDS = [
    "METRIC_EXPECTANCY_AFTER_COST",
    "METRIC_AVERAGE_TARGET_OUTCOME",
    "METRIC_WIN_RATE_OR_POSITIVE_OUTCOME_RATE",
    "METRIC_PAYOFF_RATIO",
    "METRIC_REWARD_TO_RISK_ALIGNMENT",
    "METRIC_COVERAGE_AND_PARTICIPATION",
    "METRIC_ABSTENTION_QUALITY",
    "METRIC_DRAW_DOWN_OR_ADVERSE_EXCURSION_PROXY",
    "METRIC_MATERIAL_MOVE_CAPTURE_RATE",
    "METRIC_PER_TICKER_STABILITY",
    "METRIC_CHRONOLOGICAL_STABILITY",
    "METRIC_RULE_STATE_CONTRIBUTION",
    "METRIC_BASELINE_DELTA",
    "METRIC_CONFIDENCE_INTERVAL_OR_BOOTSTRAP_BLOCKED",
]
NO_PEEK_CONTROL_IDS = [
    "RULE_USE_ONLY_REVIEWED_MATRIX_ROWS_DIGEST",
    "RULE_USE_ONLY_REVIEWED_VPA_WYCKOFF_RULE_VALUES_DIGEST",
    "RULE_TARGET_VALUES_ARE_OUTCOMES_NOT_PREDICTORS",
    "RULE_TARGET_CLASSES_ARE_OUTCOMES_NOT_PREDICTORS",
    "RULE_FORWARD_RETURNS_NOT_FEATURES",
    "RULE_CHRONOLOGICAL_SPLIT_NO_SHUFFLE",
    "RULE_HORIZON_AWARE_EMBARGO_REQUIRED",
    "RULE_NO_RUNTIME_SCORING",
    "RULE_NO_RECOMMENDATIONS",
    "RULE_NO_BROKER_OR_ORDER_FIELDS",
    "RULE_META_LIMITATION_PRESERVED",
]
FUTURE_OUTPUT_IDS = [
    "future_expectancy_backtest_lab_manifest",
    "future_expectancy_backtest_lab_schema",
    "future_expectancy_backtest_rows_jsonl",
    "future_expectancy_backtest_result_summary",
    "future_expectancy_metric_report",
    "future_baseline_comparison_report",
    "future_vpa_wyckoff_rule_alignment_report",
    "future_abstention_quality_report",
    "future_per_ticker_backtest_report",
    "future_chronological_split_report",
    "future_meta_limitation_report",
    "future_no_peek_report",
    "future_operator_summary",
    "future_digest_manifest",
]

NEXT_CHAIN = [
    "Expectancy Backtest Lab Candidate Operator Review v1.",
    "Expectancy Backtest Lab Approval v1, if selected.",
    "Expectancy Backtest Lab Execution v1, if approved.",
    "Expectancy Backtest Lab Results Review v1.",
    "Predictive-usefulness reassessment using expectancy lab evidence.",
    "Acceptance-readiness review only after reassessment.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "expectancy_backtest_lab_candidate_operator_review",
    "expectancy_backtest_lab_approval_if_selected",
    "expectancy_backtest_lab_execution_if_approved",
    "expectancy_backtest_lab_results_review",
    "predictive_usefulness_reassessment_using_expectancy_lab_evidence",
    "predictive_usefulness_acceptance_readiness_if_reassessment_supports_it",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_run_backtest",
    "candidate_does_not_create_backtest_rows",
    "candidate_does_not_create_backtest_results",
    "candidate_does_not_train_models",
    "candidate_does_not_compute_metrics",
    "candidate_does_not_score_strategy",
    "candidate_does_not_generate_trade_recommendations",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy",
    "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution",
    "candidate_does_not_call_providers",
    "candidate_does_not_acquire_market_data",
    "candidate_does_not_rerun_vpa_wyckoff_execution",
    "candidate_does_not_rerun_vpa_wyckoff_results_review",
    "candidate_does_not_rerun_feature_label_matrix_execution",
    "candidate_does_not_rerun_feature_label_matrix_results_review",
    "candidate_does_not_rerun_signal_feature_generation",
    "candidate_does_not_rerun_target_generation",
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
    "source_vpa_wyckoff_results_review_digest_bound",
    "source_vpa_wyckoff_execution_digest_bound",
    "source_vpa_wyckoff_output_binding_digest_bound",
    "source_vpa_wyckoff_rule_values_digest_bound",
    "source_vpa_wyckoff_approval_digest_bound",
    "source_matrix_results_review_digest_bound",
    "source_matrix_rows_digest_bound",
    "source_feature_values_digest_bound",
    "source_target_values_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "vpa_wyckoff_results_review_ready_true",
    "ready_for_expectancy_backtest_lab_candidate_true",
    "candidate_created_true",
    "candidate_ready_true",
    "candidate_scope_only",
    "candidate_philosophy_defined",
    "recommended_backtest_lab_package_defined",
    "supporting_backtest_lab_packages_defined",
    "backtest_objectives_defined_10",
    "candidate_baselines_defined_7",
    "chronological_plan_defined",
    "metric_families_defined_14",
    "no_peek_controls_defined_11",
    "future_outputs_not_generated_14",
    "planned_counts_defined",
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
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowExpectancyBacktestLabCandidateError(ValueError):
    """Raised when the candidate violates its non-authorizing contract."""


def _packages() -> list[dict[str, Any]]:
    common = {
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
    }
    return [
        {
            "package_id": PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
            "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "uses": [
                "reviewed feature-label matrix rows",
                "reviewed expectancy target profiles",
                "reviewed VPA/Wyckoff rule/state tags",
                "fixed cost/slippage assumptions from target-generation chain",
                "chronological no-peek windows",
                "abstention/no-trade preservation",
            ],
            "planned_scope": "RESEARCH_ONLY_BACKTEST_LAB_CANDIDATE_NOT_EXECUTION",
            **common,
        },
        {
            "package_id": PACKAGE_EXPECTANCY_FEATURE_ONLY_DIAGNOSTIC_LAB,
            "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "purpose": "Evaluate feature-bundle context without VPA/Wyckoff rule tags as a diagnostic comparator.",
            **common,
        },
        {
            "package_id": PACKAGE_EXPECTANCY_ABSTENTION_QUALITY_DIAGNOSTIC_LAB,
            "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "purpose": "Evaluate whether abstention/no-trade context improves research coverage and avoids noisy target rows.",
            **common,
        },
        {
            "package_id": PACKAGE_EXPECTANCY_COST_SENSITIVITY_DIAGNOSTIC_LAB,
            "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "purpose": "Evaluate how fixed-cost assumptions affect expectancy target interpretation.",
            **common,
        },
    ]


def _objectives() -> list[dict[str, Any]]:
    return [{
        "objective_id": objective_id,
        "objective_status": "CANDIDATE_OBJECTIVE_NOT_EXECUTED",
        "operator_review_required": True,
        "approval_required_before_execution": True,
        "metric_computation_authorized": False,
        "backtest_execution_authorized": False,
        "model_training_authorized": False,
        "research_only": True,
        "non_actionable": True,
    } for objective_id in BACKTEST_OBJECTIVE_IDS]


def _baselines() -> list[dict[str, Any]]:
    rows = [{
        "baseline_id": baseline_id,
        "baseline_status": "CANDIDATE_BASELINE_NOT_EXECUTED",
        "metric_computation_authorized": False,
        "backtest_execution_authorized": False,
        "model_training_authorized": False,
        "research_only": True,
        "non_actionable": True,
    } for baseline_id in BASELINE_IDS]
    blocked = next(
        row for row in rows
        if row["baseline_id"] == "BASELINE_RANDOMIZED_NULL_REFERENCE_BLOCKED"
    )
    blocked.update({
        "allowed_for_future_execution": False,
        "reason": (
            "Randomized null references require separate operator approval because "
            "shuffling may conflict with chronological/no-peek controls."
        ),
    })
    return rows


def _metric_families() -> list[dict[str, Any]]:
    rows = [{
        "metric_family_id": metric_id,
        "metric_status": "CANDIDATE_METRIC_NOT_COMPUTED",
        "metric_computation_authorized": False,
        "backtest_execution_authorized": False,
        "model_training_authorized": False,
        "research_only": True,
        "non_actionable": True,
    } for metric_id in METRIC_FAMILY_IDS]
    blocked = next(
        row for row in rows
        if row["metric_family_id"] == "METRIC_CONFIDENCE_INTERVAL_OR_BOOTSTRAP_BLOCKED"
    )
    blocked.update({
        "allowed_for_future_execution": False,
        "reason": (
            "Resampling and bootstrap methods require separate approval due "
            "chronological-dependence concerns."
        ),
    })
    return rows


def _no_peek_controls() -> list[dict[str, Any]]:
    return [{
        "control_id": control_id,
        "control_status": "PLANNED_NOT_EXECUTED",
        "requires_future_backtest_lab_approval": True,
    } for control_id in NO_PEEK_CONTROL_IDS]


def _future_outputs() -> list[dict[str, Any]]:
    return [{
        "output_id": output_id,
        "output_status": "PLANNED_NOT_GENERATED",
        "research_only": True,
        "non_actionable": True,
    } for output_id in FUTURE_OUTPUT_IDS]


def _chronological_plan() -> dict[str, Any]:
    return {
        "training_or_calibration_window": {
            "date_start": "2022-01-01", "date_end": "2023-12-31"
        },
        "validation_window": {
            "date_start": "2024-01-01", "date_end": "2024-12-31"
        },
        "holdout_window": {
            "date_start": "2025-01-01", "date_end": "2025-12-31"
        },
        "split_policy": "CHRONOLOGICAL_NO_SHUFFLE",
        "embargo_policy": "FUTURE_HORIZON_AWARE_EMBARGO_REQUIRED_BEFORE_EXECUTION",
        "split_execution_status": "PLANNED_NOT_EXECUTED",
    }


def _planned_counts() -> dict[str, Any]:
    return {
        "planned_source_matrix_row_count": 179190,
        "planned_evaluable_target_row_count": 177090,
        "planned_unavailable_target_row_count": 2100,
        "planned_vpa_wyckoff_rule_row_count": 179190,
        "planned_vpa_wyckoff_state_row_count": 179190,
        "planned_rule_family_count": 8,
        "planned_state_family_count": 6,
        "planned_target_profile_count": 15,
        "planned_backtest_lab_row_count": 179190,
        "planned_metric_family_count": 14,
        "planned_baseline_count": 7,
        "planned_backtest_execution_scope": "RESEARCH_ONLY_NOT_PRODUCTION_NOT_RUNTIME",
        "metric_values_computed": False,
    }


def per_ticker_expectancy_backtest_lab_candidate_digest(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_backtest_lab_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        historical_count = EXPECTED_RECORD_COUNTS[ticker]
        matrix_count = historical_count * 15
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": historical_count,
            "meta_reduced_record_count_flag": ticker == "META",
            "vpa_wyckoff_results_review_status": source_review.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY,
            "expectancy_backtest_lab_candidate_status": "READY_FOR_OPERATOR_REVIEW",
            "selected_vpa_wyckoff_package": source_review.execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
            "selected_matrix_package": source_review.execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
            "selected_feature_package": source_review.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": source_review.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": source_review.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "recommended_backtest_lab_package": PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
            "planned_matrix_row_count": matrix_count,
            "planned_evaluable_target_row_count": matrix_count - 175,
            "planned_unavailable_target_row_count": 175,
            "planned_rule_value_row_count": matrix_count,
            "planned_state_value_row_count": matrix_count,
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
            "source_vpa_wyckoff_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
            "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
            "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
            "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
            "candidate_note": (
                "PRESERVE_META_LIMITATION_IN_EXPECTANCY_BACKTEST_LAB_CANDIDATE"
                if ticker == "META" else "STANDARD_HISTORY_PRESERVED"
            ),
        }
        entry["per_ticker_expectancy_backtest_lab_candidate_digest"] = (
            per_ticker_expectancy_backtest_lab_candidate_digest(entry)
        )
        rows.append(entry)
    return rows


def _closed_boundary() -> dict[str, Any]:
    return {
        "expectancy_backtest_lab_selected": False,
        "expectancy_backtest_lab_approved": False,
        "expectancy_backtest_lab_authorized": False,
        "expectancy_backtest_lab_executed": False,
        "expectancy_backtest_rows_created": False,
        "expectancy_backtest_results_created": False,
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
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
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_candidate": False,
        "live_provider_transport_enabled_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "canonical_dataset_regenerated_in_candidate": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_rerun_performed": False,
        "target_generation_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
    }


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_vpa_wyckoff_rule_baseline_results_review_artifact_kind": source_review.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE,
        "source_vpa_wyckoff_rule_baseline_results_review_status": source_review.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY,
        "source_vpa_wyckoff_rule_baseline_results_review_scope": source_review.VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "source_vpa_wyckoff_rule_baseline_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_baseline_execution_digest": EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST,
        "source_vpa_wyckoff_rule_baseline_output_binding_digest": EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_vpa_wyckoff_rule_baseline_approval_digest": EXPECTED_SOURCE_VPA_WYCKOFF_APPROVAL_DIGEST,
        "source_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_feature_label_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_feature_label_matrix_output_binding_digest": EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "total_canonical_record_count": sum(EXPECTED_RECORD_COUNTS.values()),
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "non_meta_record_count": next(
            (count for ticker, count in EXPECTED_RECORD_COUNTS.items() if ticker != "META"),
            None,
        ),
        "meta_reduced_record_count_preserved": True,
        "selected_vpa_wyckoff_package": source_review.execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package": source_review.execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": source_review.execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": source_review.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": source_review.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": source_review.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "vpa_wyckoff_rule_baseline_results_review_created": True,
        "vpa_wyckoff_rule_baseline_results_review_ready": True,
        "ready_for_expectancy_backtest_lab_candidate": True,
        "expectancy_backtest_lab_candidate_created": True,
        "expectancy_backtest_lab_candidate_ready_for_operator_review": True,
        "ready_for_expectancy_backtest_lab_candidate_operator_review": True,
        "matrix_row_count": 179190,
        "available_matrix_row_count": 177090,
        "unavailable_target_matrix_row_count": 2100,
        "feature_group_count_per_matrix_row": 13,
        "feature_group_reference_count": 2329470,
        "feature_source_row_count": 155298,
        "target_source_row_count": 179190,
        "rule_value_row_count": 179190,
        "state_value_row_count": 179190,
        "selected_rule_family_count": 8,
        "selected_state_family_count": 6,
        "rule_family_reference_count": 1433520,
        "state_family_reference_count": 1075140,
        "target_profile_count": 15,
        "target_unavailable_row_count": 2100,
        "rule_threshold_policy": "STATIC_TRANSPARENT_BASELINE_NOT_OPTIMIZED",
        "planned_rule_evaluation_scope": "RESEARCH_ONLY_RULE_TAGGING_NOT_BACKTEST",
        "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_primary_question": CANDIDATE_PRIMARY_QUESTION,
        "candidate_secondary_question": CANDIDATE_SECONDARY_QUESTION,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "backtest_lab_packages": _packages(),
        "recommended_backtest_lab_package": PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
        "proposed_backtest_objectives": _objectives(),
        "candidate_baselines": _baselines(),
        "proposed_chronological_plan": _chronological_plan(),
        "proposed_metric_families": _metric_families(),
        "proposed_no_peek_and_leakage_controls": _no_peek_controls(),
        "proposed_future_outputs": _future_outputs(),
        "planned_counts": _planned_counts(),
        "per_ticker_expectancy_backtest_lab_candidate_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
        **_closed_boundary(),
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if actual else FAIL,
        "expected": True,
        "actual": bool(actual),
        "severity": "INFO" if actual else BLOCKER,
        "message": check_id.replace("_", " "),
    }


def _check_values(candidate: Mapping[str, Any]) -> dict[str, bool]:
    packages = candidate.get("backtest_lab_packages", [])
    objectives = candidate.get("proposed_backtest_objectives", [])
    baselines = candidate.get("candidate_baselines", [])
    metrics = candidate.get("proposed_metric_families", [])
    controls = candidate.get("proposed_no_peek_and_leakage_controls", [])
    outputs = candidate.get("proposed_future_outputs", [])
    entries = candidate.get("per_ticker_expectancy_backtest_lab_candidate_entries", [])
    planned = candidate.get("planned_counts", {})
    recommended = [
        row for row in packages
        if row.get("package_id") == PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB
    ]
    return {
        "source_vpa_wyckoff_results_review_digest_bound": candidate.get("source_vpa_wyckoff_rule_baseline_results_review_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_execution_digest_bound": candidate.get("source_vpa_wyckoff_rule_baseline_execution_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST,
        "source_vpa_wyckoff_output_binding_digest_bound": candidate.get("source_vpa_wyckoff_rule_baseline_output_binding_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST,
        "source_vpa_wyckoff_rule_values_digest_bound": candidate.get("source_vpa_wyckoff_rule_values_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_vpa_wyckoff_approval_digest_bound": candidate.get("source_vpa_wyckoff_rule_baseline_approval_digest") == EXPECTED_SOURCE_VPA_WYCKOFF_APPROVAL_DIGEST,
        "source_matrix_results_review_digest_bound": candidate.get("source_feature_label_matrix_results_review_digest") == EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_rows_digest_bound": candidate.get("source_feature_label_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest_bound": candidate.get("source_feature_values_digest") == EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest_bound": candidate.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": candidate.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": candidate.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": candidate.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": candidate.get("meta_record_count") == EXPECTED_RECORD_COUNTS.get("META"),
        "vpa_wyckoff_results_review_ready_true": candidate.get("vpa_wyckoff_rule_baseline_results_review_ready") is True,
        "ready_for_expectancy_backtest_lab_candidate_true": candidate.get("ready_for_expectancy_backtest_lab_candidate") is True,
        "candidate_created_true": candidate.get("expectancy_backtest_lab_candidate_created") is True,
        "candidate_ready_true": candidate.get("expectancy_backtest_lab_candidate_ready_for_operator_review") is True,
        "candidate_scope_only": candidate.get("candidate_scope") == EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "candidate_philosophy_defined": all(candidate.get(field) for field in ("candidate_philosophy", "candidate_primary_question", "candidate_secondary_question", "candidate_boundary")),
        "recommended_backtest_lab_package_defined": len(recommended) == 1 and recommended[0].get("status") == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "supporting_backtest_lab_packages_defined": len(packages) == 4 and all(row.get("selection_created") is False and row.get("approval_created") is False and row.get("execution_created") is False for row in packages),
        "backtest_objectives_defined_10": len(objectives) == 10 and all(row.get("objective_status") == "CANDIDATE_OBJECTIVE_NOT_EXECUTED" for row in objectives),
        "candidate_baselines_defined_7": len(baselines) == 7 and all(row.get("baseline_status") == "CANDIDATE_BASELINE_NOT_EXECUTED" for row in baselines),
        "chronological_plan_defined": candidate.get("proposed_chronological_plan") == _chronological_plan(),
        "metric_families_defined_14": len(metrics) == 14 and all(row.get("metric_status") == "CANDIDATE_METRIC_NOT_COMPUTED" for row in metrics),
        "no_peek_controls_defined_11": len(controls) == 11 and all(row.get("control_status") == "PLANNED_NOT_EXECUTED" for row in controls),
        "future_outputs_not_generated_14": len(outputs) == 14 and all(row.get("output_status") == "PLANNED_NOT_GENERATED" for row in outputs),
        "planned_counts_defined": planned == _planned_counts(),
        "per_ticker_entries_12": len(entries) == len(TARGET_UNIVERSE) and [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(row.get("per_ticker_expectancy_backtest_lab_candidate_digest") == per_ticker_expectancy_backtest_lab_candidate_digest(row) for row in entries),
        "selection_created_false": candidate.get("selection_created") is False,
        "approval_created_false": candidate.get("approval_created") is False,
        "execution_created_false": candidate.get("execution_created") is False,
        "expectancy_backtest_lab_selected_false": candidate.get("expectancy_backtest_lab_selected") is False,
        "expectancy_backtest_lab_approved_false": candidate.get("expectancy_backtest_lab_approved") is False,
        "expectancy_backtest_lab_authorized_false": candidate.get("expectancy_backtest_lab_authorized") is False,
        "expectancy_backtest_lab_executed_false": candidate.get("expectancy_backtest_lab_executed") is False,
        "backtest_rows_created_false": candidate.get("expectancy_backtest_rows_created") is False,
        "backtest_results_created_false": candidate.get("expectancy_backtest_results_created") is False,
        "backtest_execution_authorized_false": candidate.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": candidate.get("backtest_execution_performed") is False,
        "model_training_authorized_false": candidate.get("model_training_authorized") is False,
        "model_training_performed_false": candidate.get("model_training_performed") is False,
        "metric_computation_authorized_false": candidate.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": candidate.get("metric_computation_performed") is False,
        "strategy_scoring_false": candidate.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": candidate.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": candidate.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": candidate.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": candidate.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": candidate.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": candidate.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": candidate.get("provider_requests_made_in_candidate") is False,
        "market_data_acquisition_false": candidate.get("market_data_acquisition_performed_in_candidate") is False,
        "dataset_regeneration_false": candidate.get("canonical_dataset_regenerated_in_candidate") is False,
        "vpa_wyckoff_execution_rerun_false": candidate.get("vpa_wyckoff_rule_baseline_execution_rerun_performed") is False,
        "vpa_wyckoff_results_review_rerun_false": candidate.get("vpa_wyckoff_rule_baseline_results_review_rerun_performed") is False,
        "matrix_execution_rerun_false": candidate.get("feature_label_matrix_execution_rerun_performed") is False,
        "matrix_results_review_rerun_false": candidate.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_rerun_false": candidate.get("signal_feature_generation_rerun_performed") is False,
        "target_generation_rerun_false": candidate.get("target_generation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": candidate.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": candidate.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": candidate.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": candidate.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": candidate.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files") is True,
    }


def _candidate_checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(candidate)
    return [_check(check_id, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def marketflow_expectancy_backtest_lab_candidate_v1_digest(
    candidate: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(candidate))
    payload.pop("marketflow_expectancy_backtest_lab_candidate_v1_digest", None)
    return semantic_digest(payload)


def build_marketflow_expectancy_backtest_lab_candidate_v1() -> dict[str, Any]:
    """Build the deterministic candidate without reading or rerunning source outputs."""

    candidate = _base_candidate()
    candidate["candidate_checklist"] = _candidate_checklist(candidate)
    passed = sum(row["status"] == PASS for row in candidate["candidate_checklist"])
    failed = len(candidate["candidate_checklist"]) - passed
    candidate["candidate_summary"] = {
        "total_checks": len(candidate["candidate_checklist"]),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": sum(row["severity"] == BLOCKER for row in candidate["candidate_checklist"]),
        "expectancy_backtest_lab_candidate_created": True,
        "expectancy_backtest_lab_candidate_ready_for_operator_review": True,
        "recommended_backtest_lab_package": PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
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
    candidate["marketflow_expectancy_backtest_lab_candidate_v1_digest"] = (
        marketflow_expectancy_backtest_lab_candidate_v1_digest(candidate)
    )
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowExpectancyBacktestLabCandidateError(
            f"{field} must equal {expected!r}"
        )


def validate_marketflow_expectancy_backtest_lab_candidate_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Reject evidence drift, missing planning content, or opened authority."""

    if not isinstance(candidate, dict):
        raise MarketFlowExpectancyBacktestLabCandidateError("candidate must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "source_vpa_wyckoff_rule_baseline_results_review_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        "source_vpa_wyckoff_rule_baseline_execution_digest": EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST,
        "source_vpa_wyckoff_rule_baseline_output_binding_digest": EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_vpa_wyckoff_rule_baseline_approval_digest": EXPECTED_SOURCE_VPA_WYCKOFF_APPROVAL_DIGEST,
        "source_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_vpa_wyckoff_package": source_review.execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package": source_review.execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": source_review.execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": source_review.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": source_review.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": source_review.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": len(TARGET_UNIVERSE),
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "vpa_wyckoff_rule_baseline_results_review_ready": True,
        "ready_for_expectancy_backtest_lab_candidate": True,
        "expectancy_backtest_lab_candidate_created": True,
        "expectancy_backtest_lab_candidate_ready_for_operator_review": True,
        "ready_for_expectancy_backtest_lab_candidate_operator_review": True,
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
        "expectancy_backtest_lab_selected": False,
        "expectancy_backtest_lab_approved": False,
        "expectancy_backtest_lab_authorized": False,
        "expectancy_backtest_lab_executed": False,
        "expectancy_backtest_rows_created": False,
        "expectancy_backtest_results_created": False,
        "backtest_execution_authorized": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_computation_authorized": False,
        "metric_computation_performed": False,
        "strategy_scoring_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "canonical_dataset_regenerated_in_candidate": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_rerun_performed": False,
        "target_generation_rerun_performed": False,
        "risk_controls": RISK_CONTROLS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
    }
    for field, value in expected.items():
        _expect(candidate.get(field), value, field)

    required_nonempty = [
        "candidate_philosophy", "candidate_primary_question",
        "candidate_secondary_question", "candidate_boundary",
        "backtest_lab_packages", "proposed_backtest_objectives",
        "candidate_baselines", "proposed_chronological_plan",
        "proposed_metric_families", "proposed_no_peek_and_leakage_controls",
        "proposed_future_outputs", "planned_counts",
    ]
    for field in required_nonempty:
        if not candidate.get(field):
            raise MarketFlowExpectancyBacktestLabCandidateError(f"{field} is required")
    checks = _check_values(candidate)
    failed = [check_id for check_id in REQUIRED_CHECK_IDS if not checks.get(check_id)]
    if failed:
        raise MarketFlowExpectancyBacktestLabCandidateError(
            f"candidate checks failed: {', '.join(failed)}"
        )
    checklist = candidate.get("candidate_checklist")
    if (
        not isinstance(checklist, list)
        or [row.get("check_id") for row in checklist] != REQUIRED_CHECK_IDS
        or any(row.get("status") != PASS for row in checklist)
    ):
        raise MarketFlowExpectancyBacktestLabCandidateError(
            "complete passing candidate checklist is required"
        )
    entries = candidate.get("per_ticker_expectancy_backtest_lab_candidate_entries")
    if not isinstance(entries, list) or len(entries) != len(TARGET_UNIVERSE):
        raise MarketFlowExpectancyBacktestLabCandidateError(
            "per-ticker candidate entries are incomplete"
        )
    for entry in entries:
        _expect(
            entry.get("per_ticker_expectancy_backtest_lab_candidate_digest"),
            per_ticker_expectancy_backtest_lab_candidate_digest(entry),
            "per_ticker_expectancy_backtest_lab_candidate_digest",
        )
    digest = candidate.get("marketflow_expectancy_backtest_lab_candidate_v1_digest")
    if not digest:
        raise MarketFlowExpectancyBacktestLabCandidateError("candidate digest is required")
    _expect(
        digest,
        marketflow_expectancy_backtest_lab_candidate_v1_digest(candidate),
        "marketflow_expectancy_backtest_lab_candidate_v1_digest",
    )
    summary = candidate.get("candidate_summary", {})
    _expect(summary.get("failed_checks"), 0, "candidate_summary.failed_checks")
    _expect(summary.get("blocker_count"), 0, "candidate_summary.blocker_count")
    return {
        "status": MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "marketflow_expectancy_backtest_lab_candidate_v1_digest": digest,
    }


def build_marketflow_expectancy_backtest_lab_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render the candidate as an operator-readable Markdown document."""

    sections = [
        ("Expectancy Backtest Lab Candidate v1", [f"Status: `{candidate['candidate_status']}`."]),
        ("Source VPA/Wyckoff Results Review", [f"Digest: `{candidate['source_vpa_wyckoff_rule_baseline_results_review_digest']}`."]),
        ("Source Feature-Label Matrix Results Review", [f"Digest: `{candidate['source_feature_label_matrix_results_review_digest']}`."]),
        ("Bound Evidence", ["The complete VPA/Wyckoff, matrix, feature, target, expectancy, archive, registry, and records chain is bound."]),
        ("Dataset and Universe", [f"`{candidate['dataset_name']}` preserves {candidate['target_universe_count']} ordered tickers and META 913."]),
        ("Candidate Basis", [f"{candidate['matrix_row_count']} matrix rows and {candidate['rule_value_row_count']} reviewed rule rows are planned inputs only."]),
        ("Candidate Philosophy", [candidate["candidate_philosophy"], candidate["candidate_primary_question"], candidate["candidate_secondary_question"], candidate["candidate_boundary"]]),
        ("Recommended Backtest Lab Package", [candidate["recommended_backtest_lab_package"]]),
        ("Supporting Backtest Lab Packages", [row["package_id"] for row in candidate["backtest_lab_packages"][1:]]),
        ("Proposed Backtest Objectives", [row["objective_id"] for row in candidate["proposed_backtest_objectives"]]),
        ("Candidate Baselines", [row["baseline_id"] for row in candidate["candidate_baselines"]]),
        ("Chronological Plan", [f"Split policy: `{candidate['proposed_chronological_plan']['split_policy']}`; status: `PLANNED_NOT_EXECUTED`."]),
        ("Metric Families", [row["metric_family_id"] for row in candidate["proposed_metric_families"]]),
        ("No-Peek and Leakage Controls", [row["control_id"] for row in candidate["proposed_no_peek_and_leakage_controls"]]),
        ("Planned Future Outputs", [row["output_id"] for row in candidate["proposed_future_outputs"]]),
        ("Planned Counts", [f"{key}: `{value}`" for key, value in candidate["planned_counts"].items()]),
        ("Per-Ticker Candidate Summary", [f"{len(candidate['per_ticker_expectancy_backtest_lab_candidate_entries'])} candidate-only ticker entries; META limitation preserved."]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain unauthorized."]),
        ("Checklist Summary", [f"{candidate['candidate_summary']['passed_checks']} / {candidate['candidate_summary']['total_checks']} checks passed; {candidate['candidate_summary']['blocker_count']} blockers."]),
        ("Guardrails", ["This candidate creates no selection, approval, execution, backtest rows/results, metrics, models, scores, recommendations, acceptance, runtime authority, or trading authority."]),
    ]
    lines = ["# MarketFlow Expectancy Backtest Lab Candidate v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", ""])
        lines.extend(f"- {value}" for value in values)
        lines.append("")
    return "\n".join(lines)


def write_marketflow_expectancy_backtest_lab_candidate_v1(
    output_dir: str | Path,
) -> dict[str, Any]:
    """Write candidate JSON and Markdown only to an explicit destination."""

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    candidate = build_marketflow_expectancy_backtest_lab_candidate_v1()
    json_path = destination / "marketflow_expectancy_backtest_lab_candidate_v1.json"
    markdown_path = destination / "marketflow_expectancy_backtest_lab_candidate_v1.md"
    json_path.write_bytes(canonical_json_bytes(candidate))
    markdown_path.write_text(
        build_marketflow_expectancy_backtest_lab_candidate_markdown_v1(candidate),
        encoding="utf-8",
    )
    return {
        "candidate": candidate,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
