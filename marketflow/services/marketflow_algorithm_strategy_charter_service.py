"""Offline concept-only charter for MarketFlow's next algorithm research phase."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_predictive_usefulness_final_archive_summary_improved_evidence_service as final_archive


ARTIFACT_KIND_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_V1 = "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_V1"
SCHEMA_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_V1 = "marketflow_algorithm_strategy_charter_v1"
MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_READY_FOR_OPERATOR_REVIEW"
)
EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE = "EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE"
STRATEGY_CHARTER_ONLY_NOT_EXECUTION = "STRATEGY_CHARTER_ONLY_NOT_EXECUTION"

MARKETFLOW_ALGORITHM_DEFINITION = (
    "MarketFlow is an expectancy-first trend-and-flow engine designed to identify tradable "
    "directional structure using price, volume, relative strength, volatility, regime context, "
    "and abstention/no-trade logic."
)
CORE_PHILOSOPHY = (
    "Do not optimize for classification accuracy alone. Optimize for tradable expectancy, "
    "risk-adjusted opportunity, and abstention quality."
)
PRIMARY_QUESTION = (
    "Can MarketFlow identify conditions with positive expected value after risk, costs, "
    "drawdown, and position-management constraints?"
)
SECONDARY_QUESTION = "Can MarketFlow classify direction or regime better than simple baselines?"

EXPECTED_FINAL_ARCHIVE_DIGEST = "31b61c934f3bc4970973dd2cfc0e18fb3ea4ca76e02c815bed5cf509e4a5440b"
EXPECTED_ARCHIVE_DIGEST = final_archive.EXPECTED_ARCHIVE_DIGEST
EXPECTED_SELECTION_DIGEST = final_archive.EXPECTED_SELECTION_DIGEST
EXPECTED_CLOSURE_DIGEST = final_archive.EXPECTED_CLOSURE_DIGEST
EXPECTED_READINESS_DIGEST = final_archive.EXPECTED_READINESS_DIGEST
EXPECTED_REASSESSMENT_DIGEST = final_archive.EXPECTED_REASSESSMENT_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = final_archive.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = final_archive.EXPECTED_EXECUTION_DIGEST
EXPECTED_OUTPUT_BINDING_DIGEST = final_archive.EXPECTED_OUTPUT_BINDING_DIGEST
EXPECTED_MATRIX_DIGEST = final_archive.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = final_archive.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = final_archive.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = final_archive.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = final_archive.EXPECTED_RECORDS_DIGEST
SOURCE_EVIDENCE = deepcopy(final_archive.SOURCE_EVIDENCE)
TARGET_UNIVERSE = list(final_archive.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(final_archive.EXPECTED_RECORD_COUNTS)

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

STRATEGY_PRINCIPLES = [
    "PRINCIPLE_EXPECTANCY_FIRST",
    "PRINCIPLE_TREND_QUALITY_OVER_DIRECTION_ONLY",
    "PRINCIPLE_VOLUME_PRICE_CONFIRMATION",
    "PRINCIPLE_RELATIVE_STRENGTH_CONTEXT",
    "PRINCIPLE_REGIME_AWARENESS",
    "PRINCIPLE_ABSTENTION_IS_A_VALID_OUTPUT",
    "PRINCIPLE_RISK_REWARD_BEFORE_ACCURACY",
    "PRINCIPLE_COST_AND_SLIPPAGE_AWARENESS",
    "PRINCIPLE_SIMPLE_RULE_BASELINE_BEFORE_COMPLEX_MODELS",
    "PRINCIPLE_NO_RUNTIME_WITHOUT_SEPARATE_AUTHORIZATION",
]
RESEARCH_QUESTIONS = [
    "Can trend-quality states be identified before material movement?",
    "Can volume-price behavior separate continuation from exhaustion?",
    "Can relative strength improve ticker selection?",
    "Can abstention reduce low-quality/noise trades?",
    "Can expectancy remain positive after cost/slippage assumptions?",
    "Can the system outperform a simple VPA/Wyckoff rule baseline?",
    "Can results remain stable across tickers and regimes?",
    "Can risk/reward and drawdown filters improve edge quality?",
    "Can the model avoid majority-class/flat-class traps?",
    "Can the algorithm produce a useful watchlist without generating trade recommendations?",
]
OBJECTIVE_FAMILY_NAMES = [
    "OBJECTIVE_EXPECTANCY_POSITIVE_SETUP",
    "OBJECTIVE_RISK_REWARD_FAVORABLE_SETUP",
    "OBJECTIVE_MATERIAL_MOVE_AFTER_COST",
    "OBJECTIVE_TREND_CONTINUATION_SETUP",
    "OBJECTIVE_ABSORPTION_REVERSAL_SETUP",
    "OBJECTIVE_DRAWDOWN_CONTAINED_SETUP",
    "OBJECTIVE_NO_TRADE_ABSTAIN_ZONE",
    "OBJECTIVE_RELATIVE_STRENGTH_LEADER_LAGGARD",
    "OBJECTIVE_REGIME_CONDITIONED_OPPORTUNITY",
    "OBJECTIVE_PAYOFF_ASYMMETRY_SETUP",
]
SIGNAL_FAMILY_NAMES = [
    "SIGNAL_TREND_STRUCTURE",
    "SIGNAL_VOLUME_PRICE_ANALYSIS",
    "SIGNAL_CLOSE_LOCATION_AND_SPREAD",
    "SIGNAL_EFFORT_RESULT_BEHAVIOR",
    "SIGNAL_RELATIVE_STRENGTH",
    "SIGNAL_VOLATILITY_COMPRESSION_EXPANSION",
    "SIGNAL_BREAKOUT_PULLBACK_STRUCTURE",
    "SIGNAL_ABSORPTION_OR_DISTRIBUTION",
    "SIGNAL_REGIME_CONTEXT",
    "SIGNAL_NOISE_AND_ABSTENTION_FILTER",
]
VALIDATION_METRIC_NAMES = [
    "METRIC_EXPECTANCY_PER_TRADE",
    "METRIC_PROFIT_FACTOR",
    "METRIC_AVERAGE_WIN_LOSS_RATIO",
    "METRIC_MAX_DRAWDOWN",
    "METRIC_RETURN_OVER_MAX_DRAWDOWN",
    "METRIC_HIT_RATE",
    "METRIC_COST_ADJUSTED_RETURN",
    "METRIC_TURNOVER",
    "METRIC_TIME_IN_MARKET",
    "METRIC_R_MULTIPLE_DISTRIBUTION",
    "METRIC_STABILITY_ACROSS_TICKERS",
    "METRIC_STABILITY_ACROSS_REGIMES",
    "METRIC_BASELINE_OUTPERFORMANCE",
    "METRIC_ABSTENTION_QUALITY",
]
BASELINE_NAMES = [
    "BASELINE_BUY_AND_HOLD",
    "BASELINE_MAJORITY_OR_NO_TRADE",
    "BASELINE_PREVIOUS_DIRECTION",
    "BASELINE_SIMPLE_TREND_FOLLOWING",
    "BASELINE_SIMPLE_VPA_WYCKOFF_RULE",
    "BASELINE_RELATIVE_STRENGTH_RANKING",
    "BASELINE_RANDOM_OR_SHUFFLED_CONTROL",
]
PHASE_NAMES = [
    "PHASE_1_STRATEGY_CHARTER",
    "PHASE_2_EXPECTANCY_OBJECTIVE_CANDIDATE",
    "PHASE_3_OPERATOR_REVIEW_AND_APPROVAL",
    "PHASE_4_EXPECTANCY_OBJECTIVE_EXECUTION",
    "PHASE_5_VPA_WYCKOFF_RULE_BASELINE",
    "PHASE_6_EXPECTANCY_BACKTEST_LAB",
    "PHASE_7_RESULTS_REVIEW_AND_REASSESSMENT",
    "PHASE_8_READINESS_REVIEW_FOR_PAPER_RESEARCH_ONLY",
    "PHASE_9_RUNTIME_CHAIN_ONLY_IF_SEPARATELY_AUTHORIZED",
]
ACCEPTANCE_GATE_NAMES = [
    "GATE_OBJECTIVE_DEFINITION_REVIEW",
    "GATE_LABEL_OR_TARGET_GENERATION_APPROVAL",
    "GATE_FEATURE_GENERATION_APPROVAL",
    "GATE_BACKTEST_LAB_APPROVAL",
    "GATE_RESULTS_REVIEW",
    "GATE_EXPECTANCY_READINESS_REVIEW",
    "GATE_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "GATE_PROFITABILITY_REVIEW",
    "GATE_RUNTIME_MIGRATION_APPROVAL",
    "GATE_BROKER_OR_PAPER_TRADING_AUTHORITY",
]
NON_GOALS = [
    "No trade recommendation.",
    "No live trading.",
    "No paper trading.",
    "No broker execution.",
    "No runtime activation.",
    "No profitability claim.",
    "No predictive-usefulness acceptance.",
    "No strategy scoring.",
    "No market-data acquisition.",
    "No label generation.",
    "No feature generation.",
    "No model training.",
    "No backtest execution in this charter.",
]
NEXT_CHAIN = [
    "Operator review of MarketFlow Algorithm Strategy Charter v1.",
    "If approved, Expectancy Objective Candidate v1.",
    "Operator review and approval before any objective/label generation.",
    "Future feature/backtest work only after separate gates.",
    "Predictive usefulness remains not accepted until a new evidence chain passes readiness.",
    "Profitability and runtime remain separately gated.",
]
NEXT_GATES = [
    "marketflow_algorithm_strategy_charter_operator_review",
    "marketflow_algorithm_strategy_charter_approval_if_selected",
    "expectancy_objective_candidate_if_approved",
    "expectancy_objective_operator_review",
    "expectancy_objective_generation_approval",
    "feature_generation_approval",
    "expectancy_backtest_lab_approval",
    "results_review_and_reassessment",
    "paper_research_readiness_review",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "charter_does_not_create_labels",
    "charter_does_not_create_targets",
    "charter_does_not_generate_features",
    "charter_does_not_create_feature_label_matrix",
    "charter_does_not_run_backtest",
    "charter_does_not_train_models",
    "charter_does_not_recompute_metrics",
    "charter_does_not_score_strategy",
    "charter_does_not_generate_trade_recommendations",
    "charter_does_not_accept_predictive_usefulness",
    "charter_does_not_accept_profitability",
    "charter_does_not_authorize_runtime",
    "charter_does_not_authorize_strategy",
    "charter_does_not_authorize_paper_trading",
    "charter_does_not_authorize_broker_execution",
    "charter_does_not_call_providers",
    "charter_does_not_acquire_market_data",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class MarketFlowAlgorithmStrategyCharterError(ValueError):
    """Raised when the charter violates its concept-only authority boundary."""


def _candidate_objectives() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "status": "CANDIDATE_OBJECTIVE_NOT_GENERATED",
            "label_generation_authorized": False,
            "target_creation_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for name in OBJECTIVE_FAMILY_NAMES
    }


def _candidate_signals() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "status": "CANDIDATE_SIGNAL_NOT_GENERATED",
            "feature_generation_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for name in SIGNAL_FAMILY_NAMES
    }


def _candidate_metrics() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "status": "CANDIDATE_METRIC_NOT_COMPUTED",
            "metric_computation_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for name in VALIDATION_METRIC_NAMES
    }


def _candidate_baselines() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "status": "CANDIDATE_BASELINE_NOT_EXECUTED",
            "model_training_authorized": False,
            "backtest_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for name in BASELINE_NAMES
    }


def _phase_plan() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "status": "COMPLETED_BY_THIS_ARTIFACT" if index == 0 else "FUTURE_NOT_STARTED"
        }
        for index, name in enumerate(PHASE_NAMES)
    }


def _acceptance_gates() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "status": "CLOSED_FUTURE_GATE",
            "approval_created": False,
            "execution_created": False,
        }
        for name in ACCEPTANCE_GATE_NAMES
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_strategy_charter_digest", None)
    return payload


def per_ticker_marketflow_algorithm_strategy_charter_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker charter entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


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
            "source_final_archive_status": final_archive.MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY,
            "algorithm_strategy_charter_status": "READY_FOR_OPERATOR_REVIEW",
            "strategy_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_final_archive_digest": EXPECTED_FINAL_ARCHIVE_DIGEST,
            "charter_note": (
                "PRESERVE_META_LIMITATION_IN_ALGORITHM_STRATEGY_CHARTER"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_strategy_charter_digest"] = (
            per_ticker_marketflow_algorithm_strategy_charter_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_charter() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_V1,
        "charter_status": MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_READY_FOR_OPERATOR_REVIEW,
        "charter_scope": STRATEGY_CHARTER_ONLY_NOT_EXECUTION,
        "strategy_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_final_archive_artifact_kind": final_archive.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE,
        "source_final_archive_status": final_archive.MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY,
        "source_final_archive_digest": EXPECTED_FINAL_ARCHIVE_DIGEST,
        "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest": EXPECTED_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest": EXPECTED_ARCHIVE_DIGEST,
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest": EXPECTED_ARCHIVE_DIGEST,
        "source_selection_digest": EXPECTED_SELECTION_DIGEST,
        "operator_method_or_closure_selection_using_improved_evidence_digest": EXPECTED_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_CLOSURE_DIGEST,
        "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest": EXPECTED_CLOSURE_DIGEST,
        "source_readiness_digest": EXPECTED_READINESS_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest": EXPECTED_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        **deepcopy(SOURCE_EVIDENCE),
        "marketflow_algorithm_strategy_charter_created": True,
        "marketflow_algorithm_strategy_charter_ready_for_operator_review": True,
        "marketflow_next_algorithm_phase_defined": True,
        "expectancy_first_research_direction_defined": True,
        "current_predictive_usefulness_chain_archived_not_ready": True,
        "current_predictive_usefulness_not_accepted": True,
        "current_runtime_not_authorized": True,
        "future_research_requires_new_method_concept": True,
        "future_runtime_requires_separate_authorization": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_migration_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "label_generation_authorized": False,
        "label_generation_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "backtest_execution_authorized": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_recomputation_performed_in_charter": False,
        "provider_requests_made_in_charter": False,
        "live_provider_transport_enabled_in_charter": False,
        "market_data_acquisition_performed_in_charter": False,
        "dataset_generation_performed_in_charter": False,
        "canonical_dataset_regenerated_in_charter": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
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
        "previous_chain_status": "ARCHIVED_NOT_READY",
        "previous_predictive_usefulness_decision": "NOT_ACCEPTED",
        "previous_acceptance_readiness_decision": "NOT_READY",
        "previous_runtime_decision": NOT_AUTHORIZED,
        "previous_profitability_decision": "NOT_ACCEPTED",
        "previous_reason": final_archive.FINAL_OUTCOME_REASON,
        "previous_operator_selected_option": final_archive.archive_service.selection.SELECTED_OPTION,
        "matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_count": 1152,
        "oos_row_count": 34848,
        "majority_accuracy": "0.58626033",
        "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950",
        "cross_sectional_delta_vs_majority": "0.00309917",
        "majority_brier": "0.04867526",
        "local_model_brier": "0.04867526",
        "cross_sectional_brier": "0.04831065",
        "optional_tree_model_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "optional_ensemble_model_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "leakage_control_passed": True,
        "leakage_failed_control_count": 0,
        "leakage_control_count": 8,
        "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "largest_aggregated_class": "FLAT",
        "largest_aggregated_class_count": 13600,
        "no_trade_count": 1540,
        "marketflow_algorithm_identity": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "marketflow_algorithm_definition": MARKETFLOW_ALGORITHM_DEFINITION,
        "core_philosophy": CORE_PHILOSOPHY,
        "primary_question": PRIMARY_QUESTION,
        "secondary_question": SECONDARY_QUESTION,
        "strategy_philosophy": {
            "marketflow_algorithm_identity": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
            "marketflow_algorithm_definition": MARKETFLOW_ALGORITHM_DEFINITION,
            "core_philosophy": CORE_PHILOSOPHY,
            "primary_question": PRIMARY_QUESTION,
            "secondary_question": SECONDARY_QUESTION,
        },
        "strategy_principles": list(STRATEGY_PRINCIPLES),
        "research_questions": list(RESEARCH_QUESTIONS),
        "candidate_objective_families": _candidate_objectives(),
        "candidate_signal_families": _candidate_signals(),
        "candidate_validation_metrics": _candidate_metrics(),
        "candidate_baselines": _candidate_baselines(),
        "proposed_phase_plan": _phase_plan(),
        "proposed_acceptance_gates": _acceptance_gates(),
        "non_goals": list(NON_GOALS),
        "per_ticker_charter_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }


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


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and all(
        isinstance(entry, dict)
        and isinstance(entry.get("per_ticker_strategy_charter_digest"), str)
        and entry["per_ticker_strategy_charter_digest"]
        == per_ticker_marketflow_algorithm_strategy_charter_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(charter: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    entries = charter.get("per_ticker_charter_entries", [])
    return [
        ("source_final_archive_digest_bound", EXPECTED_FINAL_ARCHIVE_DIGEST, charter.get("source_final_archive_digest")),
        ("source_archive_digest_bound", EXPECTED_ARCHIVE_DIGEST, charter.get("source_archive_digest")),
        ("source_selection_digest_bound", EXPECTED_SELECTION_DIGEST, charter.get("source_selection_digest")),
        ("source_closure_digest_bound", EXPECTED_CLOSURE_DIGEST, charter.get("source_closure_digest")),
        ("source_readiness_digest_bound", EXPECTED_READINESS_DIGEST, charter.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", EXPECTED_REASSESSMENT_DIGEST, charter.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, charter.get("source_results_review_digest")),
        ("source_execution_digest_bound", EXPECTED_EXECUTION_DIGEST, charter.get("source_execution_digest")),
        ("matrix_digest_bound", EXPECTED_MATRIX_DIGEST, charter.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", EXPECTED_FEATURE_VALUES_DIGEST, charter.get("feature_values_digest")),
        ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, charter.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, charter.get("research_registry_approval_digest")),
        ("records_digest_bound", EXPECTED_RECORDS_DIGEST, charter.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, charter.get("target_universe")),
        ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, charter.get("records_digest")),
        ("meta_913_preserved", 913, charter.get("meta_record_count")),
        ("final_archive_status_bound", final_archive.MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY, charter.get("source_final_archive_status")),
        ("previous_chain_archived_not_ready", "ARCHIVED_NOT_READY", charter.get("previous_chain_status")),
        ("previous_predictive_usefulness_not_accepted", "NOT_ACCEPTED", charter.get("previous_predictive_usefulness_decision")),
        ("strategy_direction_expectancy_first", EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE, charter.get("strategy_direction")),
        ("charter_created_true", True, charter.get("marketflow_algorithm_strategy_charter_created")),
        ("charter_ready_for_operator_review_true", True, charter.get("marketflow_algorithm_strategy_charter_ready_for_operator_review")),
        ("next_algorithm_phase_defined_true", True, charter.get("marketflow_next_algorithm_phase_defined")),
        ("expectancy_first_research_direction_defined_true", True, charter.get("expectancy_first_research_direction_defined")),
        ("strategy_philosophy_defined", _base_charter_philosophy(), charter.get("strategy_philosophy")),
        ("strategy_principles_defined", STRATEGY_PRINCIPLES, charter.get("strategy_principles")),
        ("research_questions_defined", RESEARCH_QUESTIONS, charter.get("research_questions")),
        ("objective_families_defined", _candidate_objectives(), charter.get("candidate_objective_families")),
        ("signal_families_defined", _candidate_signals(), charter.get("candidate_signal_families")),
        ("validation_metrics_defined", _candidate_metrics(), charter.get("candidate_validation_metrics")),
        ("baselines_defined", _candidate_baselines(), charter.get("candidate_baselines")),
        ("phase_plan_defined", _phase_plan(), charter.get("proposed_phase_plan")),
        ("acceptance_gates_defined", _acceptance_gates(), charter.get("proposed_acceptance_gates")),
        ("non_goals_defined", NON_GOALS, charter.get("non_goals")),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("label_generation_authorized_false", False, charter.get("label_generation_authorized")),
        ("new_targets_created_false", False, charter.get("new_targets_created")),
        ("feature_generation_authorized_false", False, charter.get("feature_generation_authorized")),
        ("feature_label_matrix_created_false", False, charter.get("feature_label_matrix_created")),
        ("backtest_execution_authorized_false", False, charter.get("backtest_execution_authorized")),
        ("model_training_authorized_false", False, charter.get("model_training_authorized")),
        ("metric_recomputation_in_charter_false", False, charter.get("metric_recomputation_performed_in_charter")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, charter.get("predictive_usefulness")),
        ("profitability_not_accepted", NOT_ACCEPTED, charter.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, charter.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, charter.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, charter.get("broker_execution")),
        ("trade_recommendations_false", False, charter.get("trade_recommendations_generated")),
        ("provider_requests_made_false", False, charter.get("provider_requests_made_in_charter")),
        ("market_data_acquisition_false", False, charter.get("market_data_acquisition_performed_in_charter")),
        ("dataset_regeneration_false", False, charter.get("canonical_dataset_regenerated_in_charter")),
        ("raw_provider_payloads_not_committed", False, charter.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, charter.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, charter.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, charter.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, charter.get("risk_controls")),
        ("no_tracked_marketflow_files", True, charter.get("no_tracked_marketflow_files")),
    ]


def _base_charter_philosophy() -> dict[str, str]:
    return {
        "marketflow_algorithm_identity": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "marketflow_algorithm_definition": MARKETFLOW_ALGORITHM_DEFINITION,
        "core_philosophy": CORE_PHILOSOPHY,
        "primary_question": PRIMARY_QUESTION,
        "secondary_question": SECONDARY_QUESTION,
    }


def _checklist(charter: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(*definition) for definition in _check_definitions(charter)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = sum(row.get("status") != PASS for row in rows)
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - failed,
        "failed_checks": failed,
        "blocker_count": sum(
            row.get("status") != PASS and row.get("severity") == BLOCKER for row in rows
        ),
        "strategy_charter_created": True,
        "strategy_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "current_predictive_usefulness_chain_archived_not_ready": True,
        "future_research_requires_new_method_concept": True,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(charter: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(charter))
    payload.pop("charter_checklist", None)
    payload.pop("charter_summary", None)
    payload.pop("marketflow_algorithm_strategy_charter_v1_digest", None)
    return payload


def marketflow_algorithm_strategy_charter_digest_v1(charter: Mapping[str, Any]) -> str:
    """Return the deterministic semantic digest for the strategy charter."""
    return semantic_digest(_digest_payload(charter))


def build_marketflow_algorithm_strategy_charter_v1() -> dict:
    """Build the concept-only charter without providers, generation, or execution."""
    charter = _base_charter()
    checklist = _checklist(charter)
    charter["charter_checklist"] = checklist
    charter["charter_summary"] = _summary(checklist)
    charter["marketflow_algorithm_strategy_charter_v1_digest"] = (
        marketflow_algorithm_strategy_charter_digest_v1(charter)
    )
    validate_marketflow_algorithm_strategy_charter_v1(charter)
    return charter


def validate_marketflow_algorithm_strategy_charter_v1(charter: dict) -> dict:
    """Validate exact source bindings, candidate catalogs, and closed authorities."""
    if not isinstance(charter, dict):
        raise MarketFlowAlgorithmStrategyCharterError("charter must be an object")
    expected = _base_charter()
    for field, value in expected.items():
        if charter.get(field) != value:
            raise MarketFlowAlgorithmStrategyCharterError(f"{field} mismatch")
    checklist = charter.get("charter_checklist")
    expected_checklist = _checklist(charter)
    if checklist != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowAlgorithmStrategyCharterError("charter checklist mismatch")
    if charter.get("charter_summary") != _summary(expected_checklist):
        raise MarketFlowAlgorithmStrategyCharterError("charter summary mismatch")
    digest = charter.get("marketflow_algorithm_strategy_charter_v1_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowAlgorithmStrategyCharterError("charter digest missing")
    expected_digest = marketflow_algorithm_strategy_charter_digest_v1(charter)
    if digest != expected_digest:
        raise MarketFlowAlgorithmStrategyCharterError("charter digest mismatch")
    return {
        "status": "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_VALID",
        "artifact_kind": charter["artifact_kind"],
        "charter_status": charter["charter_status"],
        "strategy_direction": charter["strategy_direction"],
        "marketflow_algorithm_strategy_charter_v1_digest": digest,
        **{
            key: charter["charter_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_algorithm_strategy_charter_markdown_v1(charter: dict) -> str:
    """Render a sanitized Markdown view of the validated charter."""
    validation = validate_marketflow_algorithm_strategy_charter_v1(charter)
    sections = [
        ("Title", ["MarketFlow Algorithm Strategy Charter v1"]),
        (
            "MarketFlow Algorithm Strategy Charter v1",
            [
                f"Artifact/status/scope: `{charter['artifact_kind']}` / `{charter['charter_status']}` / `{charter['charter_scope']}`.",
                f"Direction/digest: `{charter['strategy_direction']}` / `{validation['marketflow_algorithm_strategy_charter_v1_digest']}`.",
            ],
        ),
        (
            "Source Final Archive Summary",
            [
                f"Artifact/status: `{charter['source_final_archive_artifact_kind']}` / `{charter['source_final_archive_status']}`.",
                f"Digest: `{charter['source_final_archive_digest']}`.",
            ],
        ),
        (
            "Bound Evidence",
            [
                f"Archive/selection/readiness: `{charter['source_archive_digest']}` / `{charter['source_selection_digest']}` / `{charter['source_readiness_digest']}`.",
                f"Matrix/features/labels: `{charter['feature_label_matrix_digest']}` / `{charter['feature_values_digest']}` / `{charter['redesigned_label_values_digest']}`.",
            ],
        ),
        (
            "Dataset and Universe",
            [
                f"Dataset/records: `{charter['dataset_name']}` / `{charter['total_canonical_record_count']}`.",
                "Universe: " + ", ".join(f"`{ticker}`" for ticker in charter["target_universe"]) + ".",
                "META remains `913`; each non-META ticker remains `1003`.",
            ],
        ),
        (
            "Why the Previous Chain Was Archived",
            [
                f"Previous chain/usefulness/readiness: `{charter['previous_chain_status']}` / `{charter['previous_predictive_usefulness_decision']}` / `{charter['previous_acceptance_readiness_decision']}`.",
                f"Reason: `{charter['previous_reason']}`.",
            ],
        ),
        ("Algorithm Identity", [charter["marketflow_algorithm_definition"]]),
        (
            "Strategy Philosophy",
            [charter["core_philosophy"], charter["primary_question"], charter["secondary_question"]],
        ),
        ("Strategy Principles", charter["strategy_principles"]),
        ("Research Questions", charter["research_questions"]),
        ("Candidate Objective Families", [f"`{name}`: `{value['status']}`." for name, value in charter["candidate_objective_families"].items()]),
        ("Candidate Signal Families", [f"`{name}`: `{value['status']}`." for name, value in charter["candidate_signal_families"].items()]),
        ("Candidate Validation Metrics", [f"`{name}`: `{value['status']}`." for name, value in charter["candidate_validation_metrics"].items()]),
        ("Candidate Baselines", [f"`{name}`: `{value['status']}`." for name, value in charter["candidate_baselines"].items()]),
        ("Proposed Phase Plan", [f"`{name}`: `{value['status']}`." for name, value in charter["proposed_phase_plan"].items()]),
        ("Acceptance Gates", [f"`{name}`: `{value['status']}`." for name, value in charter["proposed_acceptance_gates"].items()]),
        ("Non-Goals", charter["non_goals"]),
        (
            "Per-Ticker Charter Summary",
            [
                f"`{row['ticker']}`: `{row['algorithm_strategy_charter_status']}`, records `{row['historical_record_count']}`, digest `{row['per_ticker_strategy_charter_digest']}`."
                for row in charter["per_ticker_charter_entries"]
            ],
        ),
        ("Next Chain", charter["next_chain"]),
        ("Next Gates", charter["next_gates"]),
        ("Risk Controls", charter["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; this charter creates no acceptance candidate."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        (
            "Checklist Summary",
            [
                f"Total/passed/failed/blockers: `{charter['charter_summary']['total_checks']} / {charter['charter_summary']['passed_checks']} / {charter['charter_summary']['failed_checks']} / {charter['charter_summary']['blocker_count']}`."
            ],
        ),
        (
            "Guardrails",
            ["No labels, targets, features, matrix, backtest, training, metrics, scoring, recommendations, provider action, acceptance, profitability, runtime, broker, or trading authority is created."],
        ),
    ]
    lines = ["# MarketFlow Algorithm Strategy Charter v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_algorithm_strategy_charter_v1(output_dir: str | Path) -> dict:
    """Write canonical charter JSON without overwriting an existing artifact."""
    charter = build_marketflow_algorithm_strategy_charter_v1()
    validation = validate_marketflow_algorithm_strategy_charter_v1(charter)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_algorithm_strategy_charter_v1.json"
    if path.exists():
        raise MarketFlowAlgorithmStrategyCharterError("charter output already exists")
    payload = canonical_json_bytes(charter)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": charter["artifact_kind"],
        "charter_status": charter["charter_status"],
        "strategy_direction": charter["strategy_direction"],
        "marketflow_algorithm_strategy_charter_v1_digest": validation[
            "marketflow_algorithm_strategy_charter_v1_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
