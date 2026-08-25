"""Offline candidate for a future transparent VPA/Wyckoff rule baseline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import marketflow_feature_label_matrix_execution_service as execution
from marketflow.services import marketflow_feature_label_matrix_results_review_service as matrix_review


ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1 = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1 = (
    "marketflow_vpa_wyckoff_rule_baseline_candidate_v1"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION = (
    "VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_VALID = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_VALID"
)
PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE = (
    "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE"
)
PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT = (
    "PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT"
)

EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST = (
    "7def4b9c9b7d9c51dd454246e7f7718e86640d971f0b5da1c88bd240796aae30"
)
EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST = matrix_review.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST = (
    matrix_review.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST
)
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = matrix_review.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_FEATURE_VALUES_DIGEST = execution.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = execution.EXPECTED_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = execution.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

SOURCE_EVIDENCE = {
    "marketflow_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
    "marketflow_feature_label_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
    "feature_label_matrix_output_binding_digest": EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST,
    "feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
    "marketflow_feature_label_matrix_approval_digest": execution.EXPECTED_SOURCE_APPROVAL_DIGEST,
    "marketflow_feature_label_matrix_candidate_operator_review_digest": execution.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
    "marketflow_feature_label_matrix_candidate_v1_digest": execution.EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
    **deepcopy(execution.approval_service.BOUND_EVIDENCE),
}

CANDIDATE_PHILOSOPHY = (
    "Prepare a transparent rule-based VPA/Wyckoff baseline to compare against the "
    "expectancy feature-label matrix without training models, optimizing thresholds, "
    "producing recommendations, or creating runtime authority."
)
CANDIDATE_PRIMARY_QUESTION = (
    "Can simple, explainable VPA/Wyckoff-style rule states identify candidate "
    "conditions associated with the expectancy target profiles better than naive baselines?"
)
CANDIDATE_SECONDARY_QUESTION = (
    "Which volume-price, effort-result, close-location, relative-strength, "
    "volatility-compression, and abstention/noise contexts should be represented "
    "in the first transparent baseline?"
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no rule execution, rule values, baselines, backtests, metrics, "
    "strategy scores, recommendations, or runtime artifacts are created."
)

VPA_RULE_FAMILY_IDS = [
    "VPA_RULE_VOLUME_CONFIRMATION",
    "VPA_RULE_SPREAD_VOLUME_EFFORT_RESULT",
    "VPA_RULE_CLOSE_LOCATION_PRESSURE",
    "VPA_RULE_CLIMAX_OR_EXHAUSTION_CONTEXT",
    "VPA_RULE_ABSORPTION_OR_NO_SUPPLY_DEMAND",
    "VPA_RULE_BREAKOUT_EFFORT_CONFIRMATION",
    "VPA_RULE_PULLBACK_QUALITY",
    "VPA_RULE_RELATIVE_STRENGTH_CONFIRMATION",
    "VPA_RULE_VOLATILITY_COMPRESSION_EXPANSION",
    "VPA_RULE_NOISE_ABSTENTION_FILTER",
]
WYCKOFF_STATE_FAMILY_IDS = [
    "WYCKOFF_STATE_ACCUMULATION_CANDIDATE",
    "WYCKOFF_STATE_MARKUP_OR_UPTREND_CANDIDATE",
    "WYCKOFF_STATE_DISTRIBUTION_CANDIDATE",
    "WYCKOFF_STATE_MARKDOWN_OR_DOWNTREND_CANDIDATE",
    "WYCKOFF_STATE_TRADING_RANGE_OR_BALANCE",
    "WYCKOFF_STATE_POSSIBLE_SPRING_OR_SHAKEOUT",
    "WYCKOFF_STATE_POSSIBLE_UPTHRUST_OR_EXHAUSTION",
    "WYCKOFF_STATE_NO_CLEAR_STRUCTURE",
]
PRIMARY_RULE_FAMILIES = [
    "VPA_RULE_VOLUME_CONFIRMATION",
    "VPA_RULE_SPREAD_VOLUME_EFFORT_RESULT",
    "VPA_RULE_CLOSE_LOCATION_PRESSURE",
    "VPA_RULE_BREAKOUT_EFFORT_CONFIRMATION",
    "VPA_RULE_PULLBACK_QUALITY",
    "VPA_RULE_RELATIVE_STRENGTH_CONFIRMATION",
    "VPA_RULE_VOLATILITY_COMPRESSION_EXPANSION",
    "VPA_RULE_NOISE_ABSTENTION_FILTER",
]
PRIMARY_STATE_FAMILIES = [
    "WYCKOFF_STATE_ACCUMULATION_CANDIDATE",
    "WYCKOFF_STATE_MARKUP_OR_UPTREND_CANDIDATE",
    "WYCKOFF_STATE_DISTRIBUTION_CANDIDATE",
    "WYCKOFF_STATE_MARKDOWN_OR_DOWNTREND_CANDIDATE",
    "WYCKOFF_STATE_TRADING_RANGE_OR_BALANCE",
    "WYCKOFF_STATE_NO_CLEAR_STRUCTURE",
]

SOURCE_FEATURE_GROUP_MAPPING = [
    ("GROUP_VOLUME_CHANGE_AND_ZSCORE", ["VPA_RULE_VOLUME_CONFIRMATION"]),
    ("GROUP_SPREAD_VOLUME_INTERACTION", ["VPA_RULE_SPREAD_VOLUME_EFFORT_RESULT"]),
    ("GROUP_EFFORT_RESULT_DIVERGENCE", ["VPA_RULE_SPREAD_VOLUME_EFFORT_RESULT"]),
    ("GROUP_CLOSE_LOCATION_VALUE", ["VPA_RULE_CLOSE_LOCATION_PRESSURE"]),
    ("GROUP_INTRADAY_RANGE_AND_BODY", ["VPA_RULE_CLOSE_LOCATION_PRESSURE"]),
    ("GROUP_MOVING_AVERAGE_SLOPE", [
        "WYCKOFF_STATE_MARKUP_OR_UPTREND_CANDIDATE",
        "WYCKOFF_STATE_MARKDOWN_OR_DOWNTREND_CANDIDATE",
    ]),
    ("GROUP_RELATIVE_STRENGTH_VS_UNIVERSE", ["VPA_RULE_RELATIVE_STRENGTH_CONFIRMATION"]),
    ("GROUP_RELATIVE_STRENGTH_RANK", ["VPA_RULE_RELATIVE_STRENGTH_CONFIRMATION"]),
    ("GROUP_ATR_AND_VOLATILITY_COMPRESSION", ["VPA_RULE_VOLATILITY_COMPRESSION_EXPANSION"]),
    ("GROUP_ABSTENTION_NOISE_CONTEXT", ["VPA_RULE_NOISE_ABSTENTION_FILTER"]),
    ("GROUP_DATA_AVAILABILITY_FLAGS", ["DATA_QUALITY_CONTROL"]),
    ("GROUP_META_LIMITATION_FLAGS", ["META_LIMITATION_CONTROL"]),
    ("GROUP_CLOSE_TO_CLOSE_RETURNS", ["TREND_CONTEXT_SUPPORT"]),
]

RULE_DESIGN_QUESTION_TEXTS = [
    "What volume-zscore threshold should define meaningful effort?",
    "What spread-volume interaction threshold indicates genuine participation?",
    "What close-location value indicates demand-side pressure?",
    "What effort-result divergence indicates absorption or failed effort?",
    "What volatility compression condition should precede breakout context?",
    "What relative-strength rank should confirm leadership?",
    "What conditions separate pullback quality from weakness?",
    "What conditions identify no-trade/noise states?",
    "Should uptrend/downtrend states use moving-average slope only or combine relative strength?",
    "Should reversal contexts be excluded from first baseline execution?",
    "How should META's shorter history affect rule confidence?",
    "Which rule outputs should later be compared with expectancy targets?",
]
FUTURE_OUTPUT_IDS = [
    "future_vpa_wyckoff_baseline_manifest",
    "future_vpa_wyckoff_rule_schema",
    "future_vpa_wyckoff_state_schema",
    "future_vpa_wyckoff_rule_values_jsonl",
    "future_vpa_wyckoff_rule_coverage_report",
    "future_vpa_wyckoff_per_ticker_report",
    "future_vpa_wyckoff_meta_limitation_report",
    "future_vpa_wyckoff_no_peek_report",
    "future_vpa_wyckoff_operator_summary",
    "future_vpa_wyckoff_digest_manifest",
]

NEXT_CHAIN = [
    "VPA/Wyckoff Rule Baseline Candidate Operator Review v1.",
    "VPA/Wyckoff Rule Baseline Approval v1, if selected.",
    "VPA/Wyckoff Rule Baseline Execution v1, if approved.",
    "VPA/Wyckoff Rule Baseline Results Review v1.",
    "Expectancy Backtest Lab Candidate only after separate approval.",
    "Results review and readiness gates before any predictive-usefulness acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "vpa_wyckoff_rule_baseline_candidate_operator_review",
    "vpa_wyckoff_rule_baseline_approval_if_selected",
    "vpa_wyckoff_rule_baseline_execution_if_approved",
    "vpa_wyckoff_rule_baseline_results_review",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_execute_vpa_wyckoff_rules",
    "candidate_does_not_create_rule_values",
    "candidate_does_not_create_baseline_outputs",
    "candidate_does_not_run_backtest",
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
    "candidate_does_not_rerun_feature_label_matrix_execution",
    "candidate_does_not_rerun_feature_label_matrix_results_review",
    "candidate_does_not_rerun_signal_feature_generation_execution",
    "candidate_does_not_rerun_signal_feature_results_review",
    "candidate_does_not_rerun_target_generation_execution",
    "candidate_does_not_rerun_target_results_review",
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
    "source_matrix_results_review_digest_bound", "source_matrix_execution_digest_bound",
    "source_matrix_output_binding_digest_bound", "source_matrix_rows_digest_bound",
    "source_matrix_approval_digest_bound", "source_matrix_candidate_review_digest_bound",
    "source_matrix_candidate_digest_bound", "source_signal_feature_results_review_digest_bound",
    "source_signal_feature_execution_digest_bound", "source_signal_feature_output_binding_digest_bound",
    "source_feature_values_digest_bound", "source_target_results_review_digest_bound",
    "source_target_generation_execution_digest_bound", "source_target_output_binding_digest_bound",
    "source_target_values_digest_bound", "source_target_approval_digest_bound",
    "source_signal_feature_approval_digest_bound", "source_design_results_review_digest_bound",
    "source_design_execution_digest_bound", "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound", "source_strategy_charter_approval_digest_bound",
    "source_strategy_charter_digest_bound", "source_final_archive_digest_bound",
    "source_archive_digest_bound", "source_selection_digest_bound", "source_closure_digest_bound",
    "source_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_results_review_digest_bound", "source_prior_execution_digest_bound",
    "prior_matrix_digest_bound", "prior_feature_values_digest_bound",
    "prior_label_values_digest_bound", "research_registry_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "matrix_results_review_ready_true", "ready_for_vpa_wyckoff_candidate_true",
    "candidate_created_true", "candidate_ready_true", "candidate_scope_only",
    "candidate_philosophy_defined", "rule_families_defined_10",
    "wyckoff_state_families_defined_8", "recommended_package_defined",
    "supporting_package_defined", "feature_group_mapping_defined", "design_questions_defined_12",
    "future_outputs_not_generated_10", "planned_counts_defined", "per_ticker_entries_12",
    "per_ticker_digests_present", "selection_created_false", "approval_created_false",
    "execution_created_false", "vpa_wyckoff_rule_baseline_selected_false",
    "vpa_wyckoff_rule_baseline_approved_false", "vpa_wyckoff_rule_baseline_executed_false",
    "vpa_wyckoff_rule_values_created_false", "vpa_wyckoff_baseline_outputs_created_false",
    "expectancy_backtest_lab_candidate_created_false", "backtest_execution_authorized_false",
    "backtest_execution_performed_false", "model_training_authorized_false",
    "model_training_performed_false", "metric_computation_authorized_false",
    "metric_computation_performed_false", "strategy_scoring_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized",
    "strategy_not_authorized", "broker_not_authorized", "trade_recommendations_false",
    "provider_requests_made_false", "market_data_acquisition_false", "dataset_regeneration_false",
    "feature_label_matrix_execution_rerun_false", "feature_label_matrix_results_review_rerun_false",
    "signal_feature_generation_execution_rerun_false", "signal_feature_results_review_rerun_false",
    "target_generation_execution_rerun_false", "target_results_review_rerun_false",
    "raw_provider_payloads_not_committed", "api_keys_not_stored_or_printed",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowVpaWyckoffRuleBaselineCandidateError(ValueError):
    """Raised when a VPA/Wyckoff candidate violates its closed contract."""


def _rule_families() -> list[dict[str, Any]]:
    return [{
        "rule_family_id": item,
        "candidate_status": "VPA_WYCKOFF_RULE_CANDIDATE_DEFINED_NOT_EXECUTED",
        "operator_review_required": True,
        "approval_required_before_execution": True,
        "rule_execution_authorized": False,
        "rule_values_created": False,
        "baseline_outputs_created": False,
        "backtest_authorized": False,
        "metric_computation_authorized": False,
        "model_training_authorized": False,
        "research_only": True,
        "non_actionable": True,
    } for item in VPA_RULE_FAMILY_IDS]


def _state_families() -> list[dict[str, Any]]:
    return [{
        "state_family_id": item,
        "candidate_status": "WYCKOFF_STATE_CANDIDATE_DEFINED_NOT_EXECUTED",
        "operator_review_required": True,
        "approval_required_before_execution": True,
        "state_values_created": False,
        "baseline_outputs_created": False,
        "research_only": True,
        "non_actionable": True,
    } for item in WYCKOFF_STATE_FAMILY_IDS]


def _packages() -> list[dict[str, Any]]:
    return [
        {
            "package_id": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
            "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "included_rule_families": list(PRIMARY_RULE_FAMILIES),
            "included_state_families": list(PRIMARY_STATE_FAMILIES),
            "rationale": "First transparent baseline uses existing history-only feature groups for interpretable market-state and volume-price tags before statistical backtesting or acceptance.",
            "selection_created": False, "approval_created": False, "execution_created": False,
        },
        {
            "package_id": PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT,
            "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "included_rule_families": [
                "VPA_RULE_CLIMAX_OR_EXHAUSTION_CONTEXT",
                "VPA_RULE_ABSORPTION_OR_NO_SUPPLY_DEMAND",
            ],
            "included_state_families": [
                "WYCKOFF_STATE_POSSIBLE_SPRING_OR_SHAKEOUT",
                "WYCKOFF_STATE_POSSIBLE_UPTHRUST_OR_EXHAUSTION",
            ],
            "rationale": "Supporting reversal and exhaustion context remains separate initially to avoid overloading the first baseline.",
            "selection_created": False, "approval_created": False, "execution_created": False,
        },
    ]


def _feature_group_mappings() -> list[dict[str, Any]]:
    return [{
        "source_feature_group": group,
        "planned_rule_or_state_families": targets,
        "mapping_status": "PLANNED_NOT_EXECUTED",
        "target_values_used": False,
        "future_data_used": False,
        "requires_future_baseline_approval": True,
    } for group, targets in SOURCE_FEATURE_GROUP_MAPPING]


def _design_questions() -> list[dict[str, Any]]:
    return [{
        "question_id": f"VPA_WYCKOFF_RULE_DESIGN_QUESTION_{index:02d}",
        "question": question,
        "question_status": "NOT_ANSWERED",
        "requires_future_operator_review": True,
    } for index, question in enumerate(RULE_DESIGN_QUESTION_TEXTS, start=1)]


def _future_outputs() -> list[dict[str, Any]]:
    return [{
        "output_id": item,
        "output_status": "PLANNED_NOT_GENERATED",
        "research_only": True,
        "non_actionable": True,
    } for item in FUTURE_OUTPUT_IDS]


def per_ticker_vpa_wyckoff_rule_baseline_candidate_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_vpa_wyckoff_rule_baseline_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "feature_label_matrix_results_review_status": matrix_review.MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE_READY,
            "vpa_wyckoff_rule_baseline_candidate_status": "READY_FOR_OPERATOR_REVIEW",
            "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
            "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "recommended_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
            "planned_matrix_row_count": 13695 if is_meta else 15045,
            "planned_rule_family_count": 10,
            "planned_wyckoff_state_family_count": 8,
            "vpa_wyckoff_rule_baseline_selected": False,
            "vpa_wyckoff_rule_baseline_approved": False,
            "vpa_wyckoff_rule_baseline_executed": False,
            "vpa_wyckoff_rule_values_created": False,
            "vpa_wyckoff_baseline_outputs_created": False,
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
            "source_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
            "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
            "candidate_note": (
                "PRESERVE_META_LIMITATION_IN_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_vpa_wyckoff_rule_baseline_candidate_digest"] = (
            per_ticker_vpa_wyckoff_rule_baseline_candidate_digest_v1(entry)
        )
        rows.append(entry)
    return rows


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "source_feature_label_matrix_results_review_artifact_kind": matrix_review.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE,
        "source_feature_label_matrix_results_review_status": matrix_review.MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE_READY,
        "source_feature_label_matrix_results_review_scope": matrix_review.FEATURE_LABEL_MATRIX_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "source_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_feature_label_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_feature_label_matrix_output_binding_digest": EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "matrix_row_count": 179190, "available_matrix_row_count": 177090,
        "unavailable_target_matrix_row_count": 2100,
        "feature_group_count_per_matrix_row": 13,
        "feature_group_reference_count": 2329470,
        "feature_source_row_count": 155298, "target_source_row_count": 179190,
        "feature_label_matrix_results_review_created": True,
        "feature_label_matrix_results_review_ready": True,
        "ready_for_vpa_wyckoff_rule_baseline_candidate": True,
        "vpa_wyckoff_rule_baseline_candidate_created": True,
        "vpa_wyckoff_rule_baseline_candidate_ready_for_operator_review": True,
        "ready_for_vpa_wyckoff_rule_baseline_candidate_operator_review": True,
        "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_primary_question": CANDIDATE_PRIMARY_QUESTION,
        "candidate_secondary_question": CANDIDATE_SECONDARY_QUESTION,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "proposed_vpa_wyckoff_rule_families": _rule_families(),
        "proposed_wyckoff_state_families": _state_families(),
        "recommended_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "supporting_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT,
        "proposed_baseline_packages": _packages(),
        "source_feature_group_mapping": _feature_group_mappings(),
        "rule_design_questions": _design_questions(),
        "planned_future_outputs": _future_outputs(),
        "planned_source_matrix_row_count": 179190,
        "planned_rule_family_count": 10, "planned_wyckoff_state_family_count": 8,
        "planned_primary_package_rule_family_count": 8,
        "planned_primary_package_state_family_count": 6,
        "planned_rule_value_rows": 179190, "planned_rule_state_rows": 179190,
        "planned_rule_evaluation_scope": "RESEARCH_ONLY_RULE_TAGGING_NOT_BACKTEST",
        "metric_counts_approved": False,
        "per_ticker_vpa_wyckoff_rule_baseline_candidate_entries": _per_ticker_entries(),
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
        "provider_requests_made_in_candidate": False,
        "live_provider_transport_enabled_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "canonical_dataset_regenerated_in_candidate": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "signal_feature_generation_execution_rerun_performed": False,
        "signal_feature_results_review_rerun_performed": False,
        "target_generation_execution_rerun_performed": False,
        "target_results_review_rerun_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "candidate condition satisfied" if actual else "candidate condition failed",
    }


def _check_values(candidate: Mapping[str, Any]) -> dict[str, bool]:
    evidence = candidate.get("source_evidence", {})
    entries = candidate.get("per_ticker_vpa_wyckoff_rule_baseline_candidate_entries", [])
    evidence_keys = {
        "source_matrix_results_review_digest_bound": "marketflow_feature_label_matrix_results_review_digest",
        "source_matrix_execution_digest_bound": "marketflow_feature_label_matrix_execution_digest",
        "source_matrix_output_binding_digest_bound": "feature_label_matrix_output_binding_digest",
        "source_matrix_rows_digest_bound": "feature_label_matrix_rows_digest",
        "source_matrix_approval_digest_bound": "marketflow_feature_label_matrix_approval_digest",
        "source_matrix_candidate_review_digest_bound": "marketflow_feature_label_matrix_candidate_operator_review_digest",
        "source_matrix_candidate_digest_bound": "marketflow_feature_label_matrix_candidate_v1_digest",
        "source_signal_feature_results_review_digest_bound": "marketflow_signal_or_feature_generation_results_review_digest",
        "source_signal_feature_execution_digest_bound": "marketflow_signal_or_feature_generation_execution_digest",
        "source_signal_feature_output_binding_digest_bound": "signal_or_feature_generation_output_binding_digest",
        "source_feature_values_digest_bound": "signal_or_feature_values_digest",
        "source_target_results_review_digest_bound": "marketflow_objective_label_or_target_generation_results_review_digest",
        "source_target_generation_execution_digest_bound": "marketflow_objective_label_or_target_generation_execution_digest",
        "source_target_output_binding_digest_bound": "objective_label_or_target_generation_output_binding_digest",
        "source_target_values_digest_bound": "objective_label_or_target_values_digest",
        "source_target_approval_digest_bound": "marketflow_objective_label_or_target_generation_approval_digest",
        "source_signal_feature_approval_digest_bound": "marketflow_signal_or_feature_generation_approval_digest",
        "source_design_results_review_digest_bound": "marketflow_expectancy_objective_design_results_review_digest",
        "source_design_execution_digest_bound": "marketflow_expectancy_objective_design_execution_digest",
        "source_design_output_binding_digest_bound": "expectancy_objective_design_output_binding_digest",
        "source_expectancy_objective_approval_digest_bound": "marketflow_expectancy_objective_approval_digest",
        "source_strategy_charter_approval_digest_bound": "marketflow_algorithm_strategy_charter_approval_digest",
        "source_strategy_charter_digest_bound": "marketflow_algorithm_strategy_charter_v1_digest",
        "source_final_archive_digest_bound": "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest",
        "source_archive_digest_bound": "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest",
        "source_selection_digest_bound": "operator_method_or_closure_selection_using_improved_evidence_digest",
        "source_closure_digest_bound": "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest",
        "source_readiness_digest_bound": "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest",
        "source_reassessment_digest_bound": "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest",
        "source_results_review_digest_bound": "additional_predictive_evidence_results_review_using_improved_evidence_digest",
        "source_prior_execution_digest_bound": "additional_predictive_evidence_execution_using_improved_evidence_digest",
        "prior_matrix_digest_bound": "prior_feature_label_matrix_digest",
        "prior_feature_values_digest_bound": "prior_feature_values_digest",
        "prior_label_values_digest_bound": "redesigned_label_values_digest",
        "research_registry_digest_bound": "research_registry_approval_digest",
        "records_digest_bound": "records_digest",
    }
    values = {
        check_id: evidence.get(key) == SOURCE_EVIDENCE.get(key)
        for check_id, key in evidence_keys.items()
    }
    values.update({
        "target_universe_12_preserved": candidate.get("target_universe") == TARGET_UNIVERSE and candidate.get("target_universe_count") == 12,
        "records_digest_preserved": candidate.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": candidate.get("meta_record_count") == 913,
        "matrix_results_review_ready_true": candidate.get("feature_label_matrix_results_review_ready") is True,
        "ready_for_vpa_wyckoff_candidate_true": candidate.get("ready_for_vpa_wyckoff_rule_baseline_candidate") is True,
        "candidate_created_true": candidate.get("vpa_wyckoff_rule_baseline_candidate_created") is True,
        "candidate_ready_true": candidate.get("vpa_wyckoff_rule_baseline_candidate_ready_for_operator_review") is True and candidate.get("ready_for_vpa_wyckoff_rule_baseline_candidate_operator_review") is True,
        "candidate_scope_only": candidate.get("candidate_scope") == VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "candidate_philosophy_defined": candidate.get("candidate_philosophy") == CANDIDATE_PHILOSOPHY,
        "rule_families_defined_10": candidate.get("proposed_vpa_wyckoff_rule_families") == _rule_families(),
        "wyckoff_state_families_defined_8": candidate.get("proposed_wyckoff_state_families") == _state_families(),
        "recommended_package_defined": candidate.get("recommended_vpa_wyckoff_package") == PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE and candidate.get("proposed_baseline_packages", [None])[0] == _packages()[0],
        "supporting_package_defined": candidate.get("supporting_vpa_wyckoff_package") == PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT and candidate.get("proposed_baseline_packages", [None, None])[1] == _packages()[1],
        "feature_group_mapping_defined": candidate.get("source_feature_group_mapping") == _feature_group_mappings(),
        "design_questions_defined_12": candidate.get("rule_design_questions") == _design_questions(),
        "future_outputs_not_generated_10": candidate.get("planned_future_outputs") == _future_outputs(),
        "planned_counts_defined": all(candidate.get(field) == expected for field, expected in {
            "planned_source_matrix_row_count": 179190, "planned_rule_family_count": 10,
            "planned_wyckoff_state_family_count": 8,
            "planned_primary_package_rule_family_count": 8,
            "planned_primary_package_state_family_count": 6,
            "planned_rule_value_rows": 179190, "planned_rule_state_rows": 179190,
        }.items()),
        "per_ticker_entries_12": len(entries) == 12 and [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(row.get("per_ticker_vpa_wyckoff_rule_baseline_candidate_digest") == per_ticker_vpa_wyckoff_rule_baseline_candidate_digest_v1(row) for row in entries),
        "selection_created_false": candidate.get("selection_created") is False,
        "approval_created_false": candidate.get("approval_created") is False,
        "execution_created_false": candidate.get("execution_created") is False,
        "vpa_wyckoff_rule_baseline_selected_false": candidate.get("vpa_wyckoff_rule_baseline_selected") is False,
        "vpa_wyckoff_rule_baseline_approved_false": candidate.get("vpa_wyckoff_rule_baseline_approved") is False,
        "vpa_wyckoff_rule_baseline_executed_false": candidate.get("vpa_wyckoff_rule_baseline_executed") is False,
        "vpa_wyckoff_rule_values_created_false": candidate.get("vpa_wyckoff_rule_values_created") is False,
        "vpa_wyckoff_baseline_outputs_created_false": candidate.get("vpa_wyckoff_baseline_outputs_created") is False,
        "expectancy_backtest_lab_candidate_created_false": candidate.get("expectancy_backtest_lab_candidate_created") is False,
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
        "feature_label_matrix_execution_rerun_false": candidate.get("feature_label_matrix_execution_rerun_performed") is False,
        "feature_label_matrix_results_review_rerun_false": candidate.get("feature_label_matrix_results_review_rerun_performed") is False,
        "signal_feature_generation_execution_rerun_false": candidate.get("signal_feature_generation_execution_rerun_performed") is False,
        "signal_feature_results_review_rerun_false": candidate.get("signal_feature_results_review_rerun_performed") is False,
        "target_generation_execution_rerun_false": candidate.get("target_generation_execution_rerun_performed") is False,
        "target_results_review_rerun_false": candidate.get("target_results_review_rerun_performed") is False,
        "raw_provider_payloads_not_committed": candidate.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": candidate.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": candidate.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": candidate.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": candidate.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files") is True,
    })
    return values


def _candidate_checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(candidate)
    return [_check(check_id, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == PASS for row in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist), "passed_checks": passed,
        "failed_checks": failed, "blocker_count": failed,
        "vpa_wyckoff_rule_baseline_candidate_created": True,
        "vpa_wyckoff_rule_baseline_candidate_ready_for_operator_review": True,
        "recommended_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selection_created": False, "approval_created": False, "execution_created": False,
        "vpa_wyckoff_rule_values_created": False,
        "vpa_wyckoff_baseline_outputs_created": False,
        "backtest_execution_performed": False, "model_training_performed": False,
        "metric_computation_performed": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest(
    candidate: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(candidate))
    payload.pop("marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest", None)
    return semantic_digest(payload)


def build_marketflow_vpa_wyckoff_rule_baseline_candidate_v1() -> dict:
    """Build candidate-only metadata without reading or executing matrix outputs."""
    candidate = _base_candidate()
    checklist = _candidate_checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(checklist)
    if candidate["candidate_summary"]["blocker_count"]:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateError(
            "VPA/Wyckoff rule baseline candidate checklist contains blockers"
        )
    candidate["marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest"] = (
        marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest(candidate)
    )
    validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate candidate evidence, proposed designs, and closed authorities."""
    if not isinstance(candidate, dict):
        raise MarketFlowVpaWyckoffRuleBaselineCandidateError(
            "VPA/Wyckoff rule baseline candidate must be a JSON object"
        )
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION,
        "source_feature_label_matrix_results_review_artifact_kind": matrix_review.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE,
        "source_feature_label_matrix_results_review_status": matrix_review.MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE_READY,
        "source_feature_label_matrix_results_review_scope": matrix_review.FEATURE_LABEL_MATRIX_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "source_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_feature_label_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_feature_label_matrix_output_binding_digest": EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "recommended_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "supporting_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        _expect(candidate.get(field), expected, field)
    for field in (
        "created_offline", "research_only", "operator_review_required",
        "feature_label_matrix_results_review_created",
        "feature_label_matrix_results_review_ready",
        "ready_for_vpa_wyckoff_rule_baseline_candidate",
        "vpa_wyckoff_rule_baseline_candidate_created",
        "vpa_wyckoff_rule_baseline_candidate_ready_for_operator_review",
        "ready_for_vpa_wyckoff_rule_baseline_candidate_operator_review",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    ):
        _expect(candidate.get(field), True, field)
    for field in (
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
        "provider_requests_made_in_candidate", "live_provider_transport_enabled_in_candidate",
        "market_data_acquisition_performed_in_candidate", "dataset_generation_performed_in_candidate",
        "canonical_dataset_regenerated_in_candidate",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "signal_feature_generation_execution_rerun_performed",
        "signal_feature_results_review_rerun_performed",
        "target_generation_execution_rerun_performed", "target_results_review_rerun_performed",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed", "metric_counts_approved",
    ):
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    structure = {
        "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_primary_question": CANDIDATE_PRIMARY_QUESTION,
        "candidate_secondary_question": CANDIDATE_SECONDARY_QUESTION,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "proposed_vpa_wyckoff_rule_families": _rule_families(),
        "proposed_wyckoff_state_families": _state_families(),
        "proposed_baseline_packages": _packages(),
        "source_feature_group_mapping": _feature_group_mappings(),
        "rule_design_questions": _design_questions(),
        "planned_future_outputs": _future_outputs(),
    }
    for field, expected in structure.items():
        _expect(candidate.get(field), expected, field)
    entries = candidate.get("per_ticker_vpa_wyckoff_rule_baseline_candidate_entries")
    if not isinstance(entries, list) or [row.get("ticker") for row in entries] != TARGET_UNIVERSE:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateError("per-ticker candidate entries mismatch")
    for row in entries:
        _expect(
            row.get("per_ticker_vpa_wyckoff_rule_baseline_candidate_digest"),
            per_ticker_vpa_wyckoff_rule_baseline_candidate_digest_v1(row),
            f"{row.get('ticker')} candidate digest",
        )
    checklist = _candidate_checklist(candidate)
    _expect(candidate.get("candidate_checklist"), checklist, "candidate_checklist")
    if any(row["status"] != PASS for row in checklist):
        raise MarketFlowVpaWyckoffRuleBaselineCandidateError("candidate checklist contains failures")
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate_summary")
    digest = candidate.get("marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowVpaWyckoffRuleBaselineCandidateError("candidate digest missing")
    _expect(
        digest,
        marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest(candidate),
        "candidate digest",
    )
    return {
        "status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest": digest,
        "total_checks": candidate["candidate_summary"]["total_checks"],
        "passed_checks": candidate["candidate_summary"]["passed_checks"],
        "failed_checks": 0, "blocker_count": 0,
    }


def build_marketflow_vpa_wyckoff_rule_baseline_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render a validated VPA/Wyckoff candidate as Markdown."""
    validation = validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(candidate)
    sections = [
        ("VPA/Wyckoff Rule Baseline Candidate v1", [
            f"Artifact/status/scope: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}` / `{candidate['candidate_scope']}`.",
            f"Candidate digest: `{validation['marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest']}`.",
        ]),
        ("Source Feature-Label Matrix Results Review", [f"Digest `{EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST}` is bound; the source review was not rerun."]),
        ("Bound Evidence", ["Matrix execution, output binding, rows, feature/target values, records, and the upstream authority chain are digest-bound."]),
        ("Dataset and Universe", ["`expanded_universe_canonical_dataset_v1`, twelve ordered tickers, 11,946 records; META remains 913."]),
        ("Candidate Basis", ["179,190 reviewed matrix rows, thirteen history-only feature groups, and fifteen expectancy target profiles."]),
        ("Candidate Philosophy", [CANDIDATE_PHILOSOPHY, CANDIDATE_PRIMARY_QUESTION, CANDIDATE_SECONDARY_QUESTION, CANDIDATE_BOUNDARY]),
        ("Proposed VPA/Wyckoff Rule Families", VPA_RULE_FAMILY_IDS),
        ("Proposed Wyckoff State Families", WYCKOFF_STATE_FAMILY_IDS),
        ("Recommended Baseline Package", [PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE]),
        ("Supporting Baseline Package", [PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT]),
        ("Source Feature Group Mapping", [f"{group} -> {', '.join(targets)}" for group, targets in SOURCE_FEATURE_GROUP_MAPPING]),
        ("Rule Design Questions", RULE_DESIGN_QUESTION_TEXTS),
        ("Planned Rule Outputs", FUTURE_OUTPUT_IDS),
        ("Planned Counts", ["179,190 planned rule-value rows; 179,190 planned state rows; ten rule families and eight states. No metric counts are approved."]),
        ("Per-Ticker Candidate Summary", ["Twelve digest-bound entries; non-META plans 15,045 rows each and META plans 13,695."]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES),
        ("Risk Controls", RISK_CONTROLS),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{candidate['candidate_summary']['passed_checks']}/{candidate['candidate_summary']['total_checks']} checks pass with zero blockers."]),
        ("Guardrails", ["This candidate defines future research only; it creates no selection, approval, rule values, output, backtest, metric, recommendation, acceptance, runtime, or trading authority."]),
    ]
    lines: list[str] = []
    for index, (title, body) in enumerate(sections):
        lines.append(("# " if index == 0 else "## ") + title)
        lines.append("")
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(
    output_dir: str | Path,
) -> dict:
    """Write candidate JSON and Markdown only to an explicit directory."""
    candidate = build_marketflow_vpa_wyckoff_rule_baseline_candidate_v1()
    validation = validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(candidate)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_vpa_wyckoff_rule_baseline_candidate_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowVpaWyckoffRuleBaselineCandidateError(
            "candidate output already exists"
        )
    json_path.write_bytes(canonical_json_bytes(candidate))
    markdown_path.write_text(
        build_marketflow_vpa_wyckoff_rule_baseline_candidate_markdown_v1(candidate),
        encoding="utf-8", newline="\n",
    )
    return {
        **validation,
        "json_path": str(json_path.resolve()),
        "markdown_path": str(markdown_path.resolve()),
    }
