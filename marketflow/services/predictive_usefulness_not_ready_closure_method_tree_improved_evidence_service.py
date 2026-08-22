"""Offline not-ready closure and method-planning tree using improved evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_usefulness_acceptance_readiness_review_using_improved_evidence_service as readiness


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE_V1 = (
    "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE"
)
CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION = (
    "CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION"
)
CLOSURE_REASON = (
    "SMALL_CROSS_SECTIONAL_EDGE_LOCAL_MODEL_MATCHES_MAJORITY_OPTIONAL_MODEL_COVERAGE_INCOMPLETE_AND_ACCEPTANCE_READINESS_NOT_READY"
)

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
SELECTED_DIRECTION = readiness.SELECTED_DIRECTION

EXPECTED_READINESS_DIGEST = "e3a8803e6a72a45c4b0355bd0c8870917496325f4c9718bb977156611d5713f0"
EXPECTED_REASSESSMENT_DIGEST = readiness.EXPECTED_REASSESSMENT_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = readiness.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = readiness.EXPECTED_EXECUTION_DIGEST
EXPECTED_OUTPUT_BINDING_DIGEST = readiness.EXPECTED_OUTPUT_BINDING_DIGEST
EXPECTED_MATRIX_DIGEST = readiness.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = readiness.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = readiness.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = readiness.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = readiness.EXPECTED_RECORDS_DIGEST
SOURCE_EVIDENCE = deepcopy(readiness.SOURCE_EVIDENCE)

TARGET_UNIVERSE = list(readiness.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(readiness.EXPECTED_RECORD_COUNTS)

RECOMMENDED_CURRENT_DECISION = "OPTION_A_STOP_ACCEPTANCE_PATH_CURRENT_DATASET"
RECOMMENDED_NEXT_OPERATOR_ACTION = "OPERATOR_METHOD_OR_CLOSURE_SELECTION"
RECOMMENDED_NEXT_ARTIFACT_IF_CONTINUING = (
    "METHOD_OR_EVIDENCE_IMPROVEMENT_PATH_SELECTION_USING_IMPROVED_EVIDENCE"
)
RECOMMENDED_NEXT_ARTIFACT_IF_CLOSING = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE"
)

METHOD_PLANNING_TREE = {
    "OPTION_A_STOP_ACCEPTANCE_PATH_CURRENT_DATASET": {
        "option_status": "RECOMMENDED_CURRENT_DECISION",
        "rationale": "Current improved evidence does not meet acceptance readiness. Cross-sectional edge is small, local model matches majority baseline, optional model coverage is incomplete, and acceptance candidate is not allowed.",
        "allowed_action": ["Document closure and pause current acceptance chain."],
        "not_allowed": ["No acceptance candidate, no runtime, no trading, no profitability approval."],
        "selected": False,
    },
    "OPTION_B_RESEARCH_NEW_OBJECTIVE_OUTSIDE_ACCEPTANCE_CHAIN": {
        "option_status": "AVAILABLE_FUTURE_RESEARCH_OPTION_NOT_SELECTED",
        "rationale": "Investigate whether a different target objective is required before another acceptance path.",
        "examples": [
            "expectancy-based labels",
            "payoff/asymmetry labels",
            "risk-adjusted return labels",
            "abstention-first classifier",
            "material move targets",
            "drawdown-aware labels",
        ],
        "not_allowed": ["No immediate label regeneration or target change."],
        "selected": False,
    },
    "OPTION_C_EXPECTANCY_FIRST_RESEARCH_PATH": {
        "option_status": "AVAILABLE_FUTURE_RESEARCH_OPTION_NOT_SELECTED",
        "rationale": "Accuracy-first classification may be insufficient for trading usefulness. Future research may prioritize expected value, payoff ratio, drawdown, and cost-aware performance.",
        "not_allowed": ["No trade recommendations, no strategy scoring, no runtime activation."],
        "selected": False,
    },
    "OPTION_D_EXPAND_DATASET_OR_UNIVERSE": {
        "option_status": "AVAILABLE_FUTURE_RESEARCH_OPTION_NOT_SELECTED",
        "rationale": "Current 12-ticker, 2022-2025 daily RTH dataset may be too limited for robust market-regime evidence.",
        "examples": ["longer history", "broader universe", "sector-specific cohorts", "additional regimes", "alternative timeframes"],
        "not_allowed": ["No market-data acquisition in this artifact."],
        "selected": False,
    },
    "OPTION_E_MODEL_FAMILY_EXPANSION_AFTER_OBJECTIVE_REVIEW": {
        "option_status": "AVAILABLE_FUTURE_RESEARCH_OPTION_NOT_SELECTED",
        "rationale": "Tree/ensemble models remain unavailable. Model expansion should wait until target/objective quality is reviewed to limit overfitting risk.",
        "not_allowed": ["No model training in this artifact."],
        "selected": False,
    },
    "OPTION_F_FEATURE_ENGINEERING_REVIEW": {
        "option_status": "AVAILABLE_FUTURE_RESEARCH_OPTION_NOT_SELECTED",
        "rationale": "Future research may inspect whether current feature families fail to capture tradable structure.",
        "not_allowed": ["No feature generation in this artifact."],
        "selected": False,
    },
    "OPTION_G_STOP_PROJECT_OR_ARCHIVE_CURRENT_PREDICTIVE_ACCEPTANCE_CHAIN": {
        "option_status": "AVAILABLE_FUTURE_GOVERNANCE_OPTION_NOT_SELECTED",
        "rationale": "If the operator decides no further research is justified, archive the current acceptance path as not ready.",
        "not_allowed": ["No deletion or mutation of evidence."],
        "selected": False,
    },
    "OPTION_H_ACCEPTANCE_CANDIDATE": {
        "option_status": "NOT_ALLOWED_CURRENTLY",
        "rationale": "Acceptance readiness is not ready.",
        "not_allowed": ["Acceptance candidate creation is prohibited."],
        "selected": False,
    },
}

NEXT_CHAIN = [
    "Operator Method or Closure Selection Using Improved Evidence v1.",
    "If continuing: selected method/evidence improvement candidate.",
    "If closing: acceptance-path archive record.",
    "Any future evidence work requires separate candidate, review, approval, execution, results review, reassessment, and readiness gates.",
    "Acceptance candidate only if future readiness passes.",
    "Profitability review only after predictive usefulness acceptance path is separately approved.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "operator_method_or_closure_selection_using_improved_evidence",
    "method_or_evidence_improvement_candidate_if_selected",
    "method_or_evidence_improvement_review",
    "method_or_evidence_improvement_approval",
    "future_evidence_candidate_review_approval_execution_if_selected",
    "future_reassessment_after_new_evidence",
    "future_acceptance_readiness_after_new_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "closure_does_not_accept_predictive_usefulness",
    "closure_does_not_create_acceptance_candidate",
    "closure_does_not_create_acceptance_ceremony",
    "closure_does_not_accept_profitability",
    "closure_does_not_authorize_runtime",
    "closure_does_not_authorize_strategy",
    "closure_does_not_authorize_paper_trading",
    "closure_does_not_authorize_broker_execution",
    "closure_does_not_generate_trade_recommendations",
    "closure_does_not_regenerate_labels",
    "closure_does_not_create_new_targets",
    "closure_does_not_authorize_target_definition_change",
    "closure_does_not_generate_features",
    "closure_does_not_create_canonical_feature_label_matrix",
    "closure_does_not_rerun_predictive_evidence",
    "closure_does_not_rerun_reassessment",
    "closure_does_not_rerun_readiness_review",
    "closure_does_not_recompute_metrics",
    "closure_does_not_train_models",
    "closure_does_not_select_future_method",
    "closure_does_not_create_future_improvement_candidate",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_prior_predictive_evidence_outputs",
    "do_not_mutate_improved_evidence_planning_outputs",
    "do_not_mutate_current_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(ValueError):
    """Raised when the not-ready closure package is invalid."""


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_not_ready_closure_digest", None)
    return payload


def per_ticker_predictive_usefulness_not_ready_closure_using_improved_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker closure entry."""
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
            "readiness_decision": readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
            "closure_status": "ACCEPTANCE_PATH_CLOSED_NOT_READY_FOR_CURRENT_IMPROVED_EVIDENCE",
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_readiness_digest": EXPECTED_READINESS_DIGEST,
            "closure_note": (
                "PRESERVE_META_LIMITATION_IN_NOT_READY_CLOSURE_USING_IMPROVED_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_not_ready_closure_digest"] = (
            per_ticker_predictive_usefulness_not_ready_closure_using_improved_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE_V1,
        "closure_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "closure_decision": CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION,
        "closure_reason": CLOSURE_REASON,
        "created_offline": True,
        "research_only": True,
        "operator_review_required_for_future_work": True,
        "source_readiness_artifact_kind": readiness.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE,
        "source_readiness_status": readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_COMPLETED,
        "source_readiness_decision": readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "source_readiness_digest": EXPECTED_READINESS_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest": EXPECTED_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        **deepcopy(SOURCE_EVIDENCE),
        "predictive_usefulness_acceptance_path_closed_for_current_improved_evidence": True,
        "current_improved_evidence_acceptance_path_closure_created": True,
        "method_planning_tree_created": True,
        "operator_future_method_selection_required": True,
        "future_method_selected": False,
        "future_improvement_candidate_created": False,
        "next_artifact_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_ceremony_allowed": False,
        "additional_evidence_or_method_improvement_required": True,
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
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_closure": False,
        "model_training_performed_in_closure": False,
        "provider_requests_made_in_closure": False,
        "live_provider_transport_enabled_in_closure": False,
        "market_data_acquisition_performed_in_closure": False,
        "dataset_generation_performed_in_closure": False,
        "canonical_dataset_regenerated_in_closure": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "additional_predictive_evidence_execution_rerun_performed": False,
        "predictive_usefulness_reassessment_rerun_performed": False,
        "predictive_usefulness_acceptance_readiness_rerun_performed": False,
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
        "selected_redesign_direction": SELECTED_DIRECTION,
        "readiness_decision": readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "readiness_reason": readiness.READINESS_REASON,
        "predictive_signal_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "local_model_readiness": "NOT_READY",
        "cross_sectional_edge_readiness": "NOT_READY",
        "oos_performance_readiness": "NOT_READY",
        "walk_forward_readiness": "REQUIRES_OPERATOR_REVIEW",
        "calibration_brier_readiness": "REQUIRES_OPERATOR_REVIEW",
        "leakage_readiness": "PASS",
        "meta_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "acceptance_candidate_allowed": False,
        "acceptance_ceremony_allowed": False,
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
        "global_five_session_threshold": "0.026556108631",
        "benchmark_relative_threshold": "0.02058653801",
        "method_planning_tree_options": deepcopy(METHOD_PLANNING_TREE),
        "recommended_current_decision": RECOMMENDED_CURRENT_DECISION,
        "recommended_next_operator_action": RECOMMENDED_NEXT_OPERATOR_ACTION,
        "recommended_next_artifact_if_continuing": RECOMMENDED_NEXT_ARTIFACT_IF_CONTINUING,
        "recommended_next_artifact_if_closing": RECOMMENDED_NEXT_ARTIFACT_IF_CLOSING,
        "per_ticker_closure_entries": _per_ticker_entries(),
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
        isinstance(entry.get("per_ticker_not_ready_closure_digest"), str)
        and entry["per_ticker_not_ready_closure_digest"]
        == per_ticker_predictive_usefulness_not_ready_closure_using_improved_evidence_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(package: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    entries = package.get("per_ticker_closure_entries", [])
    options = package.get("method_planning_tree_options", {})
    unavailable = "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    return [
        ("source_readiness_digest_bound", EXPECTED_READINESS_DIGEST, package.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", EXPECTED_REASSESSMENT_DIGEST, package.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, package.get("source_results_review_digest")),
        ("source_execution_digest_bound", EXPECTED_EXECUTION_DIGEST, package.get("source_execution_digest")),
        ("source_output_binding_digest_bound", EXPECTED_OUTPUT_BINDING_DIGEST, package.get("source_output_binding_digest")),
        ("matrix_digest_bound", EXPECTED_MATRIX_DIGEST, package.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", EXPECTED_FEATURE_VALUES_DIGEST, package.get("feature_values_digest")),
        ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, package.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, package.get("research_registry_approval_digest")),
        ("records_digest_bound", EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, package.get("target_universe")),
        ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        ("meta_913_preserved", 913, package.get("meta_record_count")),
        ("readiness_decision_not_ready", readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE, package.get("readiness_decision")),
        ("closure_created_true", True, package.get("current_improved_evidence_acceptance_path_closure_created")),
        ("acceptance_path_closed_true", True, package.get("predictive_usefulness_acceptance_path_closed_for_current_improved_evidence")),
        ("method_planning_tree_created_true", True, package.get("method_planning_tree_created")),
        ("operator_future_method_selection_required_true", True, package.get("operator_future_method_selection_required")),
        ("acceptance_candidate_created_false", False, package.get("predictive_usefulness_acceptance_candidate_created")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, package.get("predictive_usefulness")),
        ("acceptance_ready_false", False, package.get("predictive_usefulness_acceptance_ready")),
        ("acceptance_recommended_false", False, package.get("predictive_usefulness_acceptance_recommended")),
        ("acceptance_ceremony_allowed_false", False, package.get("predictive_usefulness_acceptance_ceremony_allowed")),
        ("profitability_not_accepted", NOT_ACCEPTED, package.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        ("trade_recommendations_false", False, package.get("trade_recommendations_generated")),
        ("label_regeneration_authorized_false", False, package.get("label_regeneration_authorized")),
        ("label_regeneration_performed_false", False, package.get("label_regeneration_performed")),
        ("new_targets_created_false", False, package.get("new_targets_created")),
        ("target_definition_change_authorized_false", False, package.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, package.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, package.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, package.get("feature_label_matrix_created")),
        ("metric_recomputation_in_closure_false", False, package.get("metric_recomputation_performed_in_closure")),
        ("model_training_in_closure_false", False, package.get("model_training_performed_in_closure")),
        ("predictive_evidence_rerun_false", False, package.get("additional_predictive_evidence_execution_rerun_performed")),
        ("reassessment_rerun_false", False, package.get("predictive_usefulness_reassessment_rerun_performed")),
        ("readiness_rerun_false", False, package.get("predictive_usefulness_acceptance_readiness_rerun_performed")),
        ("matrix_rows_preserved", 143352, package.get("matrix_row_count")),
        ("evaluable_rows_preserved", 142200, package.get("evaluable_matrix_row_count")),
        ("unavailable_targets_preserved", 1152, package.get("unavailable_target_count")),
        ("oos_rows_preserved", 34848, package.get("oos_row_count")),
        ("small_cross_sectional_edge_preserved", "0.00309917", package.get("cross_sectional_delta_vs_majority")),
        ("local_model_equivalence_preserved", package.get("majority_accuracy"), package.get("local_model_accuracy")),
        ("brier_values_preserved", ["0.04867526", "0.04867526", "0.04831065"], [package.get("majority_brier"), package.get("local_model_brier"), package.get("cross_sectional_brier")]),
        ("optional_models_unavailable_preserved", [unavailable, unavailable], [package.get("optional_tree_model_status"), package.get("optional_ensemble_model_status")]),
        ("leakage_controls_passed", [True, 0, 8], [package.get("leakage_control_passed"), package.get("leakage_failed_control_count"), package.get("leakage_control_count")]),
        ("meta_limitation_preserved", True, package.get("meta_reduced_record_count_preserved")),
        ("method_tree_options_present", list(METHOD_PLANNING_TREE), list(options) if isinstance(options, dict) else []),
        ("recommended_option_a_stop_current_dataset", RECOMMENDED_CURRENT_DECISION, package.get("recommended_current_decision")),
        ("acceptance_candidate_option_not_allowed", "NOT_ALLOWED_CURRENTLY", options.get("OPTION_H_ACCEPTANCE_CANDIDATE", {}).get("option_status") if isinstance(options, dict) else None),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("provider_requests_made_false", False, package.get("provider_requests_made_in_closure")),
        ("market_data_acquisition_false", False, package.get("market_data_acquisition_performed_in_closure")),
        ("dataset_regeneration_false", False, package.get("canonical_dataset_regenerated_in_closure")),
        ("raw_provider_payloads_not_committed", False, package.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, package.get("api_keys_stored_or_printed")),
        ("no_predictive_usefulness_acceptance_artifact_created", False, package.get("predictive_usefulness_acceptance_artifact_created")),
        ("no_profitability_acceptance_created", False, package.get("profitability_acceptance_created")),
        ("no_runtime_migration_approval_created", False, package.get("runtime_migration_approval_created")),
        ("next_chain_defined", NEXT_CHAIN, package.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, package.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, package.get("risk_controls")),
        ("no_tracked_marketflow_files", True, package.get("no_tracked_marketflow_files")),
    ]


def _checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(check_id, expected, actual) for check_id, expected, actual in _check_definitions(package)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "closure_created": not failed,
        "acceptance_path_closed_for_current_improved_evidence": not failed,
        "readiness_decision": readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "recommended_current_decision": RECOMMENDED_CURRENT_DECISION,
        "operator_future_method_selection_required": True,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(package: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(package))
    payload.pop(
        "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest",
        None,
    )
    return payload


def predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest_v1(
    closure: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the closure package."""
    return semantic_digest(_digest_payload(closure))


def build_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1() -> dict:
    """Build the offline closure and unselected future method-planning tree."""
    package = _base_package()
    checklist = _checklist(package)
    package["closure_checklist"] = checklist
    package["closure_summary"] = _summary(checklist)
    package[
        "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest"
    ] = predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest_v1(
        package
    )
    validate_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(
        package
    )
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            f"{field} must be true"
        )


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            f"{field} must be false"
        )


def validate_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(
    closure: dict,
) -> dict:
    """Validate evidence bindings, closure semantics, and closed authority gates."""
    if not isinstance(closure, dict):
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            "closure must be an object"
        )

    expected_fields = {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE_V1,
        "closure_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        "closure_decision": CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION,
        "closure_reason": CLOSURE_REASON,
        "source_readiness_artifact_kind": readiness.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE,
        "source_readiness_status": readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_COMPLETED,
        "source_readiness_decision": readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "source_readiness_digest": EXPECTED_READINESS_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest": EXPECTED_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "readiness_decision": readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE,
        "readiness_reason": readiness.READINESS_REASON,
        "predictive_signal_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "local_model_readiness": "NOT_READY",
        "cross_sectional_edge_readiness": "NOT_READY",
        "oos_performance_readiness": "NOT_READY",
        "walk_forward_readiness": "REQUIRES_OPERATOR_REVIEW",
        "calibration_brier_readiness": "REQUIRES_OPERATOR_REVIEW",
        "leakage_readiness": "PASS",
        "meta_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
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
        "method_planning_tree_options": METHOD_PLANNING_TREE,
        "recommended_current_decision": RECOMMENDED_CURRENT_DECISION,
        "recommended_next_operator_action": RECOMMENDED_NEXT_OPERATOR_ACTION,
        "recommended_next_artifact_if_continuing": RECOMMENDED_NEXT_ARTIFACT_IF_CONTINUING,
        "recommended_next_artifact_if_closing": RECOMMENDED_NEXT_ARTIFACT_IF_CLOSING,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    expected_fields.update(SOURCE_EVIDENCE)
    for field, value in expected_fields.items():
        _expect(closure.get(field), value, field)

    true_fields = (
        "created_offline",
        "research_only",
        "operator_review_required_for_future_work",
        "predictive_usefulness_acceptance_path_closed_for_current_improved_evidence",
        "current_improved_evidence_acceptance_path_closure_created",
        "method_planning_tree_created",
        "operator_future_method_selection_required",
        "additional_evidence_or_method_improvement_required",
        "leakage_control_passed",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    )
    for field in true_fields:
        _expect_true(closure.get(field), field)

    false_fields = (
        "future_method_selected",
        "future_improvement_candidate_created",
        "next_artifact_created",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_artifact_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_ceremony_allowed",
        "acceptance_candidate_allowed",
        "acceptance_ceremony_allowed",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "profitability_acceptance_created",
        "runtime_migration_approved",
        "runtime_migration_active",
        "runtime_migration_approval_created",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "feature_generation_authorized",
        "feature_generation_performed",
        "feature_label_matrix_created",
        "metric_recomputation_performed_in_closure",
        "model_training_performed_in_closure",
        "provider_requests_made_in_closure",
        "live_provider_transport_enabled_in_closure",
        "market_data_acquisition_performed_in_closure",
        "dataset_generation_performed_in_closure",
        "canonical_dataset_regenerated_in_closure",
        "redesigned_label_regeneration_performed",
        "feature_regeneration_performed",
        "additional_predictive_evidence_execution_rerun_performed",
        "predictive_usefulness_reassessment_rerun_performed",
        "predictive_usefulness_acceptance_readiness_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    )
    for field in false_fields:
        _expect_false(closure.get(field), field)

    options = closure.get("method_planning_tree_options")
    if not isinstance(options, dict) or list(options) != list(METHOD_PLANNING_TREE):
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            "method planning tree options mismatch"
        )
    for option, expected in METHOD_PLANNING_TREE.items():
        _expect(options.get(option), expected, f"{option} option")
        _expect_false(options[option].get("selected"), f"{option} selected")
    _expect(
        options["OPTION_H_ACCEPTANCE_CANDIDATE"].get("option_status"),
        "NOT_ALLOWED_CURRENTLY",
        "acceptance candidate option",
    )

    entries = closure.get("per_ticker_closure_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            "per-ticker closure entries mismatch"
        )
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker order")
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(entry.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        _expect(entry.get("readiness_decision"), readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE, f"{ticker} readiness")
        _expect(entry.get("closure_status"), "ACCEPTANCE_PATH_CLOSED_NOT_READY_FOR_CURRENT_IMPROVED_EVIDENCE", f"{ticker} closure")
        _expect(entry.get("source_readiness_digest"), EXPECTED_READINESS_DIGEST, f"{ticker} readiness digest")
        _expect(entry.get("predictive_usefulness"), NOT_ACCEPTED, f"{ticker} usefulness")
        _expect(entry.get("profitability"), NOT_ACCEPTED, f"{ticker} profitability")
        _expect_false(entry.get("predictive_usefulness_acceptance_ready"), f"{ticker} acceptance ready")
        _expect_false(entry.get("predictive_usefulness_acceptance_candidate_created"), f"{ticker} candidate")
        _expect_false(entry.get("trade_recommendations_generated"), f"{ticker} recommendations")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, f"{ticker} {field}")
        if ticker == "META":
            _expect(
                entry.get("closure_note"),
                "PRESERVE_META_LIMITATION_IN_NOT_READY_CLOSURE_USING_IMPROVED_EVIDENCE",
                "META closure_note",
            )
        digest = entry.get("per_ticker_not_ready_closure_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
                f"{ticker} per-ticker digest missing"
            )
        _expect(
            digest,
            per_ticker_predictive_usefulness_not_ready_closure_using_improved_evidence_digest_v1(entry),
            f"{ticker} per-ticker digest",
        )

    checklist = closure.get("closure_checklist")
    expected_check_ids = [definition[0] for definition in _check_definitions(closure)]
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != expected_check_ids:
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            "closure checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            "closure checklist failed"
        )
    _expect(closure.get("closure_summary"), _summary(checklist), "closure summary")

    digest = closure.get(
        "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            "closure digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest_v1(
            closure
        ),
        "closure digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_METHOD_TREE_USING_IMPROVED_EVIDENCE_VALID",
        "artifact_kind": closure["artifact_kind"],
        "closure_status": closure["closure_status"],
        "closure_decision": closure["closure_decision"],
        "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest": digest,
        **{
            key: closure["closure_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_markdown_v1(
    closure: dict,
) -> str:
    """Render a sanitized Markdown view of the validated closure package."""
    validation = validate_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(
        closure
    )
    sections = [
        ("Title", ["Predictive Usefulness Not-Ready Closure and Method Planning Tree Using Improved Evidence"]),
        (
            "Predictive Usefulness Not-Ready Closure and Method Planning Tree Using Improved Evidence",
            [
                f"Artifact/status: `{closure['artifact_kind']}` / `{closure['closure_status']}`.",
                f"Digest: `{validation['predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest']}`.",
            ],
        ),
        (
            "Source Readiness Review",
            [
                f"Artifact/status: `{closure['source_readiness_artifact_kind']}` / `{closure['source_readiness_status']}`.",
                f"Decision/digest: `{closure['source_readiness_decision']}` / `{closure['source_readiness_digest']}`.",
            ],
        ),
        (
            "Bound Evidence",
            [
                f"Reassessment/results review/execution: `{closure['source_reassessment_digest']}` / `{closure['source_results_review_digest']}` / `{closure['source_execution_digest']}`.",
                f"Matrix/features/labels: `{closure['feature_label_matrix_digest']}` / `{closure['feature_values_digest']}` / `{closure['redesigned_label_values_digest']}`.",
            ],
        ),
        (
            "Dataset and Universe",
            [
                f"Dataset/records: `{closure['dataset_name']}` / `{closure['total_canonical_record_count']}`.",
                "Universe: " + ", ".join(f"`{ticker}`" for ticker in closure["target_universe"]) + ".",
                "META remains `913`; each non-META ticker remains `1003`.",
            ],
        ),
        (
            "Closure Decision",
            [
                f"Decision: `{closure['closure_decision']}`.",
                f"Reason: `{closure['closure_reason']}`.",
            ],
        ),
        (
            "Closure Basis",
            [
                f"Readiness decision/reason: `{closure['readiness_decision']}` / `{closure['readiness_reason']}`.",
                "Signal, baseline, local, cross-sectional, and OOS readiness remain `NOT_READY`.",
            ],
        ),
        (
            "Evidence Summary",
            [
                f"Matrix/evaluable/unavailable/OOS: `{closure['matrix_row_count']} / {closure['evaluable_matrix_row_count']} / {closure['unavailable_target_count']} / {closure['oos_row_count']}`.",
                f"Majority/local/cross-sectional accuracy: `{closure['majority_accuracy']} / {closure['local_model_accuracy']} / {closure['cross_sectional_accuracy']}`.",
            ],
        ),
        (
            "Why Acceptance Is Not Ready",
            ["The cross-sectional edge is small, the local model matches the majority baseline, optional model coverage is incomplete, and the source readiness review is not ready."],
        ),
        (
            "Method Planning Tree",
            [
                f"`{name}`: `{value['option_status']}` — {value['rationale']}"
                for name, value in closure["method_planning_tree_options"].items()
            ],
        ),
        (
            "Recommended Current Decision",
            [
                f"Current decision: `{closure['recommended_current_decision']}`.",
                f"Next operator action: `{closure['recommended_next_operator_action']}`.",
                "No next artifact or future method is selected or created by this closure.",
            ],
        ),
        (
            "Per-Ticker Closure",
            [
                f"`{row['ticker']}`: `{row['closure_status']}`, records `{row['historical_record_count']}`, digest `{row['per_ticker_not_ready_closure_digest']}`."
                for row in closure["per_ticker_closure_entries"]
            ],
        ),
        ("Next Chain", closure["next_chain"]),
        ("Next Gates", closure["next_gates"]),
        ("Risk Controls", closure["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted and no acceptance candidate or ceremony is allowed."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        (
            "Checklist Summary",
            [
                f"Total/passed/failed/blockers: `{closure['closure_summary']['total_checks']} / {closure['closure_summary']['passed_checks']} / {closure['closure_summary']['failed_checks']} / {closure['closure_summary']['blocker_count']}`."
            ],
        ),
        (
            "Guardrails",
            ["No provider, acquisition, regeneration, readiness rerun, reassessment rerun, predictive rerun, metric recomputation, model training, future-method selection, acceptance, runtime, broker, or trading action occurred."],
        ),
    ]
    lines = ["# Predictive Usefulness Not-Ready Closure and Method Planning Tree Using Improved Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical closure JSON without overwriting an existing package."""
    package = build_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1()
    validation = validate_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(
        package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1.json"
    if path.exists():
        raise PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError(
            "closure output already exists"
        )
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "closure_status": package["closure_status"],
        "closure_decision": package["closure_decision"],
        "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest": validation[
            "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
