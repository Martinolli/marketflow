"""Offline candidate-only plan for MarketFlow expectancy objective research."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_algorithm_strategy_charter_approval_service as approval_service,
)


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_V1 = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_V1 = (
    "marketflow_expectancy_objective_candidate_v1"
)
MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
EXPECTANCY_OBJECTIVE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION = (
    "EXPECTANCY_OBJECTIVE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION"
)
EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE = (
    approval_service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE
)
EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST = (
    "ea6c77007c4827fbdd4015425bc92af40eb59b08daba3d5c2e41090df0762b92"
)
EXPECTED_SOURCE_STRATEGY_CHARTER_REVIEW_DIGEST = (
    approval_service.EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST
)
EXPECTED_SOURCE_STRATEGY_CHARTER_DIGEST = (
    approval_service.EXPECTED_SOURCE_CHARTER_DIGEST
)

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OBJECTIVE_CANDIDATE_PHILOSOPHY = (
    "Define expectancy-oriented objectives before generating any labels or targets."
)
OBJECTIVE_CANDIDATE_PRIMARY_QUESTION = (
    "Which objective can best represent tradable opportunity after risk, costs, "
    "drawdown, and abstention constraints?"
)
OBJECTIVE_CANDIDATE_SECONDARY_QUESTION = (
    "Which objective can avoid the majority-class and flat/no-trade trap seen in "
    "the archived classification chain?"
)
OBJECTIVE_CANDIDATE_BOUNDARY = (
    "Candidate-only; no label, target, feature, metric, backtest, model, or "
    "strategy artifact is generated."
)
RECOMMENDED_OBJECTIVE_PATH = "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"

RESEARCH_QUESTIONS = [
    "What trade setup has positive expectancy after cost and slippage?",
    "What payoff asymmetry is required to offset imperfect direction accuracy?",
    "What minimum material move is needed to justify risk?",
    "What drawdown tolerance invalidates a setup?",
    "What conditions should produce abstention/no-trade?",
    "Can the objective avoid majority-class dominance?",
    "Can objective performance remain stable across tickers?",
    "Can objective performance remain stable across regimes?",
    "Can a simple VPA/Wyckoff baseline validate the objective?",
    "Can the objective support a future watchlist without trade recommendations?",
]
DESIGN_DIMENSIONS = [
    "DIMENSION_FORWARD_RETURN",
    "DIMENSION_DRAWDOWN_PATH",
    "DIMENSION_REWARD_TO_RISK",
    "DIMENSION_COST_AND_SLIPPAGE",
    "DIMENSION_TIME_IN_TRADE",
    "DIMENSION_VOLATILITY_ADJUSTMENT",
    "DIMENSION_RELATIVE_STRENGTH_CONTEXT",
    "DIMENSION_REGIME_CONTEXT",
    "DIMENSION_VOLUME_PRICE_CONFIRMATION",
    "DIMENSION_ABSTENTION_NO_TRADE_FILTER",
    "DIMENSION_TICKER_STABILITY",
    "DIMENSION_CROSS_SECTIONAL_STABILITY",
]
FUTURE_OUTPUTS = [
    "future_expectancy_objective_design_manifest",
    "future_objective_family_selection_report",
    "future_expectancy_payoff_objective_specification",
    "future_abstention_support_objective_specification",
    "future_material_move_objective_specification",
    "future_objective_label_generation_plan",
    "future_objective_validation_metric_plan",
    "future_objective_baseline_comparison_plan",
    "future_per_ticker_objective_review",
    "future_operator_summary",
    "future_digest_manifest",
]
NEXT_CHAIN = [
    "Expectancy Objective Candidate Operator Review v1.",
    "Expectancy Objective Approval v1, if selected.",
    "Expectancy Objective Design Execution v1, if approved.",
    "Expectancy Objective Results Review v1.",
    "Future label/target generation candidate only after separate approval.",
    "Future signal/feature planning only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "expectancy_objective_candidate_operator_review",
    "expectancy_objective_approval_if_selected",
    "expectancy_objective_design_execution_if_approved",
    "expectancy_objective_results_review",
    "objective_label_or_target_generation_candidate",
    "signal_or_feature_generation_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_approve_objective",
    "candidate_does_not_generate_labels",
    "candidate_does_not_create_targets",
    "candidate_does_not_generate_features",
    "candidate_does_not_create_feature_label_matrix",
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
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class MarketFlowExpectancyObjectiveCandidateError(ValueError):
    """Raised when the candidate violates its candidate-only boundary."""


def _documented_source_approval_attestation() -> dict:
    source = (
        approval_service.review_service
        .build_marketflow_algorithm_strategy_charter_operator_review_v1()
    )
    confirmations = {
        field: True
        for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    }
    return approval_service.build_marketflow_algorithm_strategy_charter_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T12:00:00Z",
        operator_attestation_phrase=approval_service.REQUIRED_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_charter_review_digest=approval_service.EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST,
        operator_confirms_charter_digest=approval_service.EXPECTED_SOURCE_CHARTER_DIGEST,
        operator_confirms_final_archive_digest=source["source_final_archive_digest"],
        operator_confirms_records_digest=source["records_digest"],
        operator_confirms_target_universe=list(source["target_universe"]),
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
        operator_confirms_strategy_direction=EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        **confirmations,
    )


def _source_approval() -> dict:
    source = approval_service.build_marketflow_algorithm_strategy_charter_approval_v1(
        operator_attestation=_documented_source_approval_attestation()
    )
    validation = approval_service.validate_marketflow_algorithm_strategy_charter_approval_v1(
        source
    )
    if (
        validation["marketflow_algorithm_strategy_charter_approval_digest"]
        != EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST
    ):
        raise MarketFlowExpectancyObjectiveCandidateError(
            "source strategy charter approval digest mismatch"
        )
    return source


def _objective_families(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "objective_family": name,
            "candidate_status": "OBJECTIVE_CANDIDATE_DEFINED_NOT_GENERATED",
            "source_objective_status": value["objective_status"],
            "operator_review_required": True,
            "approval_required_before_generation": True,
            "label_generation_authorized": False,
            "target_creation_authorized": False,
            "feature_generation_authorized": False,
            "metric_computation_authorized": False,
            "backtest_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for name, value in source["approved_objective_families"].items()
    }


def _objective_clusters() -> dict[str, dict[str, Any]]:
    return {
        "CLUSTER_EXPECTANCY_AND_PAYOFF": {
            "objective_families": [
                "OBJECTIVE_EXPECTANCY_POSITIVE_SETUP",
                "OBJECTIVE_PAYOFF_ASYMMETRY_SETUP",
                "OBJECTIVE_RISK_REWARD_FAVORABLE_SETUP",
            ],
            "candidate_rationale": (
                "Directly targets tradable edge instead of class accuracy."
            ),
            "status": "RECOMMENDED_FOR_OPERATOR_REVIEW",
        },
        "CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE": {
            "objective_families": [
                "OBJECTIVE_TREND_CONTINUATION_SETUP",
                "OBJECTIVE_MATERIAL_MOVE_AFTER_COST",
                "OBJECTIVE_DRAWDOWN_CONTAINED_SETUP",
            ],
            "candidate_rationale": (
                "Focuses on material trend movement after risk and cost constraints."
            ),
            "status": "AVAILABLE_FOR_OPERATOR_REVIEW",
        },
        "CLUSTER_ABSTENTION_AND_NO_TRADE": {
            "objective_families": ["OBJECTIVE_NO_TRADE_ABSTAIN_ZONE"],
            "candidate_rationale": (
                "Controls low-quality/noise conditions and prevents majority/flat "
                "traps from becoming false acceptance evidence."
            ),
            "status": "RECOMMENDED_SUPPORTING_OBJECTIVE",
        },
        "CLUSTER_CONTEXTUAL_SELECTION": {
            "objective_families": [
                "OBJECTIVE_RELATIVE_STRENGTH_LEADER_LAGGARD",
                "OBJECTIVE_REGIME_CONDITIONED_OPPORTUNITY",
                "OBJECTIVE_ABSORPTION_REVERSAL_SETUP",
            ],
            "candidate_rationale": (
                "Improves ticker, regime, and setup discrimination."
            ),
            "status": "AVAILABLE_FOR_OPERATOR_REVIEW",
        },
    }


def _research_questions() -> list[dict[str, Any]]:
    return [
        {
            "question": question,
            "question_status": "NOT_ANSWERED",
            "requires_future_research": True,
            "research_only": True,
        }
        for question in RESEARCH_QUESTIONS
    ]


def _design_dimensions() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "dimension_status": "CANDIDATE_DIMENSION_NOT_EXECUTED",
            "generation_authorized": False,
            "metric_computation_authorized": False,
        }
        for name in DESIGN_DIMENSIONS
    }


def _future_outputs() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "output_status": "PLANNED_NOT_GENERATED",
            "research_only": True,
            "non_actionable": True,
        }
        for name in FUTURE_OUTPUTS
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_objective_candidate_digest", None)
    return payload


def per_ticker_expectancy_objective_candidate_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker candidate entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_strategy_charter_approval_entries"]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": is_meta,
            "strategy_charter_approval_status": source["approval_status"],
            "expectancy_objective_candidate_status": "READY_FOR_OPERATOR_REVIEW",
            "strategy_direction": source["approved_strategy_direction"],
            "recommended_objective_path": RECOMMENDED_OBJECTIVE_PATH,
            "label_generation_authorized": False,
            "new_targets_created": False,
            "feature_generation_authorized": False,
            "feature_label_matrix_created": False,
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
            "source_strategy_charter_approval_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
            "source_strategy_charter_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_DIGEST,
            "candidate_note": (
                "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_CANDIDATE"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_expectancy_objective_candidate_digest"] = (
            per_ticker_expectancy_objective_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _source_digest_chain(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: deepcopy(value)
        for key, value in source.items()
        if key.endswith("_digest") and isinstance(value, str)
    }


def _base_candidate(source: Mapping[str, Any]) -> dict[str, Any]:
    candidate = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": EXPECTANCY_OBJECTIVE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION,
        "candidate_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_strategy_charter_approval_artifact_kind": source["artifact_kind"],
        "source_strategy_charter_approval_status": source["approval_status"],
        "source_strategy_charter_approval_scope": source["approval_scope"],
        "source_strategy_charter_approval_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
        "source_strategy_charter_review_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_REVIEW_DIGEST,
        "source_strategy_charter_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_DIGEST,
        **_source_digest_chain(source),
    }
    candidate.update(
        {
            "marketflow_algorithm_strategy_charter_approved": True,
            "marketflow_algorithm_strategy_charter_authorized": True,
            "ready_for_expectancy_objective_candidate": True,
            "expectancy_objective_candidate_created": True,
            "expectancy_objective_candidate_ready_for_operator_review": True,
            "marketflow_expectancy_objective_candidate_created": True,
            "expectancy_objective_approved": False,
            "expectancy_objective_generation_authorized": False,
            "expectancy_objective_generation_performed": False,
            "label_generation_authorized": False,
            "label_generation_performed": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_label_matrix_created": False,
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
            "raw_provider_payloads_committed": False,
            "api_keys_stored_or_printed": False,
        }
    )
    copied_fields = [
        "dataset_name", "source_profile", "timeframe", "date_range_start", "date_range_end",
        "target_universe", "target_universe_count", "total_canonical_record_count",
        "per_ticker_record_counts", "meta_record_count", "non_meta_record_count",
        "meta_reduced_record_count_preserved", "previous_chain_status",
        "previous_predictive_usefulness_decision", "previous_acceptance_readiness_decision",
        "previous_runtime_decision", "previous_profitability_decision",
        "previous_operator_selected_option", "matrix_row_count", "evaluable_matrix_row_count",
        "unavailable_target_count", "oos_row_count", "majority_accuracy",
        "local_model_accuracy", "cross_sectional_accuracy",
        "cross_sectional_delta_vs_majority", "majority_brier", "local_model_brier",
        "cross_sectional_brier", "optional_tree_model_status",
        "optional_ensemble_model_status", "leakage_control_passed",
        "leakage_failed_control_count", "leakage_control_count", "majority_structure_risk",
        "largest_aggregated_class", "largest_aggregated_class_count", "no_trade_count",
        "strategy_direction", "marketflow_algorithm_identity", "core_philosophy",
    ]
    candidate.update({field: deepcopy(source[field]) for field in copied_fields})
    candidate.update(
        {
            "objective_candidate_philosophy": OBJECTIVE_CANDIDATE_PHILOSOPHY,
            "objective_candidate_primary_question": OBJECTIVE_CANDIDATE_PRIMARY_QUESTION,
            "objective_candidate_secondary_question": OBJECTIVE_CANDIDATE_SECONDARY_QUESTION,
            "objective_candidate_boundary": OBJECTIVE_CANDIDATE_BOUNDARY,
            "objective_candidate_families": _objective_families(source),
            "recommended_objective_clusters": _objective_clusters(),
            "recommended_objective_path": RECOMMENDED_OBJECTIVE_PATH,
            "recommended_primary_objective_cluster": "CLUSTER_EXPECTANCY_AND_PAYOFF",
            "recommended_supporting_objective_cluster": "CLUSTER_ABSTENTION_AND_NO_TRADE",
            "recommended_secondary_cluster": "CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE",
            "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "selection_created": False,
            "approval_created": False,
            "generation_created": False,
            "objective_design_research_questions": _research_questions(),
            "candidate_objective_design_dimensions": _design_dimensions(),
            "candidate_future_outputs": _future_outputs(),
            "per_ticker_expectancy_objective_candidate_entries": _per_ticker_entries(source),
            "next_chain": list(NEXT_CHAIN),
            "next_gates": list(NEXT_GATES),
            "risk_controls": list(RISK_CONTROLS),
            "no_tracked_marketflow_files": True,
        }
    )
    return candidate


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
    return isinstance(entries, list) and len(entries) == 12 and all(
        isinstance(entry, dict)
        and isinstance(entry.get("per_ticker_expectancy_objective_candidate_digest"), str)
        and entry["per_ticker_expectancy_objective_candidate_digest"]
        == per_ticker_expectancy_objective_candidate_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(candidate: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    source = _source_approval()
    entries = candidate.get("per_ticker_expectancy_objective_candidate_entries", [])
    return [
        ("source_strategy_charter_approval_digest_bound", EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST, candidate.get("source_strategy_charter_approval_digest")),
        ("source_strategy_charter_review_digest_bound", EXPECTED_SOURCE_STRATEGY_CHARTER_REVIEW_DIGEST, candidate.get("source_strategy_charter_review_digest")),
        ("source_strategy_charter_digest_bound", EXPECTED_SOURCE_STRATEGY_CHARTER_DIGEST, candidate.get("source_strategy_charter_digest")),
        ("source_final_archive_digest_bound", source["source_final_archive_digest"], candidate.get("source_final_archive_digest")),
        ("source_archive_digest_bound", source["source_archive_digest"], candidate.get("source_archive_digest")),
        ("source_selection_digest_bound", source["source_selection_digest"], candidate.get("source_selection_digest")),
        ("source_closure_digest_bound", source["source_closure_digest"], candidate.get("source_closure_digest")),
        ("source_readiness_digest_bound", source["source_readiness_digest"], candidate.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", source["source_reassessment_digest"], candidate.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", source["source_results_review_digest"], candidate.get("source_results_review_digest")),
        ("source_execution_digest_bound", source["source_execution_digest"], candidate.get("source_execution_digest")),
        ("matrix_digest_bound", source["feature_label_matrix_digest"], candidate.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", source["feature_values_digest"], candidate.get("feature_values_digest")),
        ("label_values_digest_bound", source["redesigned_label_values_digest"], candidate.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", source["research_registry_approval_digest"], candidate.get("research_registry_approval_digest")),
        ("records_digest_bound", source["records_digest"], candidate.get("records_digest")),
        ("target_universe_12_preserved", source["target_universe"], candidate.get("target_universe")),
        ("records_digest_preserved", source["records_digest"], candidate.get("records_digest")),
        ("meta_913_preserved", 913, candidate.get("meta_record_count")),
        ("strategy_charter_approved_true", True, candidate.get("marketflow_algorithm_strategy_charter_approved")),
        ("ready_for_expectancy_objective_candidate_true", True, candidate.get("ready_for_expectancy_objective_candidate")),
        ("expectancy_objective_candidate_created_true", True, candidate.get("expectancy_objective_candidate_created")),
        ("expectancy_objective_candidate_ready_true", True, candidate.get("expectancy_objective_candidate_ready_for_operator_review")),
        ("candidate_scope_only", EXPECTANCY_OBJECTIVE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION, candidate.get("candidate_scope")),
        ("strategy_direction_expectancy_first", EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE, candidate.get("candidate_direction")),
        ("objective_candidate_philosophy_defined", OBJECTIVE_CANDIDATE_PHILOSOPHY, candidate.get("objective_candidate_philosophy")),
        ("objective_families_10_defined", 10, len(candidate.get("objective_candidate_families", {}))),
        ("objective_clusters_defined", _objective_clusters(), candidate.get("recommended_objective_clusters")),
        ("recommended_objective_path_defined", RECOMMENDED_OBJECTIVE_PATH, candidate.get("recommended_objective_path")),
        ("selection_created_false", False, candidate.get("selection_created")),
        ("approval_created_false", False, candidate.get("approval_created")),
        ("generation_created_false", False, candidate.get("generation_created")),
        ("research_questions_defined", _research_questions(), candidate.get("objective_design_research_questions")),
        ("design_dimensions_defined", _design_dimensions(), candidate.get("candidate_objective_design_dimensions")),
        ("future_outputs_not_generated", _future_outputs(), candidate.get("candidate_future_outputs")),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("label_generation_authorized_false", False, candidate.get("label_generation_authorized")),
        ("new_targets_created_false", False, candidate.get("new_targets_created")),
        ("feature_generation_authorized_false", False, candidate.get("feature_generation_authorized")),
        ("feature_label_matrix_created_false", False, candidate.get("feature_label_matrix_created")),
        ("backtest_execution_authorized_false", False, candidate.get("backtest_execution_authorized")),
        ("model_training_authorized_false", False, candidate.get("model_training_authorized")),
        ("metric_computation_authorized_false", False, candidate.get("metric_computation_authorized")),
        ("strategy_scoring_false", False, candidate.get("strategy_scoring_performed")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        ("profitability_not_accepted", NOT_ACCEPTED, candidate.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, candidate.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        ("trade_recommendations_false", False, candidate.get("trade_recommendations_generated")),
        ("provider_requests_made_false", False, candidate.get("provider_requests_made_in_candidate")),
        ("market_data_acquisition_false", False, candidate.get("market_data_acquisition_performed_in_candidate")),
        ("dataset_regeneration_false", False, candidate.get("canonical_dataset_regenerated_in_candidate")),
        ("raw_provider_payloads_not_committed", False, candidate.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, candidate.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, candidate.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, candidate.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        ("no_tracked_marketflow_files", True, candidate.get("no_tracked_marketflow_files")),
    ]


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(*definition) for definition in _check_definitions(candidate)]


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
        "expectancy_objective_candidate_created": True,
        "expectancy_objective_candidate_ready_for_operator_review": True,
        "recommended_objective_path": RECOMMENDED_OBJECTIVE_PATH,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "label_generation_authorized": False,
        "new_targets_created": False,
        "feature_generation_authorized": False,
        "backtest_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(candidate: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(candidate))
    payload.pop("candidate_checklist", None)
    payload.pop("candidate_summary", None)
    payload.pop("marketflow_expectancy_objective_candidate_v1_digest", None)
    return payload


def marketflow_expectancy_objective_candidate_v1_digest(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate artifact."""
    return semantic_digest(_digest_payload(candidate))


def build_marketflow_expectancy_objective_candidate_v1() -> dict:
    """Build a candidate-only artifact without generation or execution."""
    candidate = _base_candidate(_source_approval())
    checklist = _checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(checklist)
    candidate["marketflow_expectancy_objective_candidate_v1_digest"] = (
        marketflow_expectancy_objective_candidate_v1_digest(candidate)
    )
    validate_marketflow_expectancy_objective_candidate_v1(candidate)
    return candidate


def validate_marketflow_expectancy_objective_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate source bindings, candidate definitions, and closed authorities."""
    if not isinstance(candidate, dict):
        raise MarketFlowExpectancyObjectiveCandidateError(
            "candidate must be an object"
        )
    expected = _base_candidate(_source_approval())
    for field, value in expected.items():
        if candidate.get(field) != value:
            raise MarketFlowExpectancyObjectiveCandidateError(
                f"{field} mismatch"
            )
    checklist = candidate.get("candidate_checklist")
    expected_checklist = _checklist(candidate)
    if checklist != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowExpectancyObjectiveCandidateError(
            "candidate checklist mismatch"
        )
    if candidate.get("candidate_summary") != _summary(expected_checklist):
        raise MarketFlowExpectancyObjectiveCandidateError(
            "candidate summary mismatch"
        )
    digest = candidate.get("marketflow_expectancy_objective_candidate_v1_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowExpectancyObjectiveCandidateError(
            "candidate digest missing"
        )
    if digest != marketflow_expectancy_objective_candidate_v1_digest(candidate):
        raise MarketFlowExpectancyObjectiveCandidateError(
            "candidate digest mismatch"
        )
    return {
        "status": "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "candidate_direction": candidate["candidate_direction"],
        "marketflow_expectancy_objective_candidate_v1_digest": digest,
        **{
            key: candidate["candidate_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_expectancy_objective_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render a sanitized Markdown view of a validated candidate artifact."""
    validation = validate_marketflow_expectancy_objective_candidate_v1(candidate)
    sections = [
        ("Title", ["Expectancy Objective Candidate v1"]),
        ("Expectancy Objective Candidate v1", [
            "Artifact/status/scope: "
            f"{candidate['artifact_kind']} / {candidate['candidate_status']} / "
            f"{candidate['candidate_scope']}.",
            "Candidate digest: "
            f"{validation['marketflow_expectancy_objective_candidate_v1_digest']}.",
        ]),
        ("Source Strategy Charter Approval", [
            "Artifact/status/scope: "
            f"{candidate['source_strategy_charter_approval_artifact_kind']} / "
            f"{candidate['source_strategy_charter_approval_status']} / "
            f"{candidate['source_strategy_charter_approval_scope']}.",
            f"Digest: {candidate['source_strategy_charter_approval_digest']}.",
        ]),
        ("Bound Evidence", [
            "Review/charter/final archive: "
            f"{candidate['source_strategy_charter_review_digest']} / "
            f"{candidate['source_strategy_charter_digest']} / "
            f"{candidate['source_final_archive_digest']}.",
            "Matrix/features/labels: "
            f"{candidate['feature_label_matrix_digest']} / "
            f"{candidate['feature_values_digest']} / "
            f"{candidate['redesigned_label_values_digest']}.",
        ]),
        ("Dataset and Universe", [
            f"Dataset/records: {candidate['dataset_name']} / "
            f"{candidate['total_canonical_record_count']}.",
            "Universe: " + ", ".join(candidate["target_universe"]) + ".",
            "META remains 913; every non-META ticker remains 1003.",
        ]),
        ("Candidate Basis", [
            f"Direction: {candidate['strategy_direction']}.",
            f"Previous chain: {candidate['previous_chain_status']}.",
            f"Core philosophy: {candidate['core_philosophy']}",
        ]),
        ("Objective Candidate Philosophy", [
            candidate["objective_candidate_philosophy"],
            candidate["objective_candidate_primary_question"],
            candidate["objective_candidate_secondary_question"],
            candidate["objective_candidate_boundary"],
        ]),
        ("Objective Candidate Families", [
            f"{name}: {value['candidate_status']}."
            for name, value in candidate["objective_candidate_families"].items()
        ]),
        ("Recommended Objective Clusters", [
            f"{name}: {value['status']} — {value['candidate_rationale']}"
            for name, value in candidate["recommended_objective_clusters"].items()
        ]),
        ("Candidate Recommendation", [
            f"Path: {candidate['recommended_objective_path']}.",
            f"Status: {candidate['recommendation_status']}.",
            "No selection, approval, or generation is created.",
        ]),
        ("Research Questions", [
            f"{value['question']} Status: {value['question_status']}."
            for value in candidate["objective_design_research_questions"]
        ]),
        ("Objective Design Dimensions", [
            f"{name}: {value['dimension_status']}."
            for name, value in candidate["candidate_objective_design_dimensions"].items()
        ]),
        ("Future Outputs", [
            f"{name}: {value['output_status']}."
            for name, value in candidate["candidate_future_outputs"].items()
        ]),
        ("Per-Ticker Candidate Summary", [
            f"{row['ticker']}: {row['expectancy_objective_candidate_status']}, "
            f"records {row['historical_record_count']}, "
            f"digest {row['per_ticker_expectancy_objective_candidate_digest']}."
            for row in candidate["per_ticker_expectancy_objective_candidate_entries"]
        ]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
        ("Predictive Usefulness Boundary", [
            "Predictive usefulness remains not accepted."
        ]),
        ("Profitability Boundary", [
            "Profitability remains not accepted."
        ]),
        ("Runtime Boundary", [
            "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."
        ]),
        ("Checklist Summary", [
            "Total/passed/failed/blockers: "
            f"{candidate['candidate_summary']['total_checks']} / "
            f"{candidate['candidate_summary']['passed_checks']} / "
            f"{candidate['candidate_summary']['failed_checks']} / "
            f"{candidate['candidate_summary']['blocker_count']}."
        ]),
        ("Guardrails", [
            "This candidate creates no selection, approval, labels, targets, features, "
            "matrix, backtest, model, metric, scoring, recommendation, acceptance, "
            "profitability, runtime, provider, market-data, paper-trading, or broker authority."
        ]),
    ]
    lines = ["# Expectancy Objective Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_expectancy_objective_candidate_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_marketflow_expectancy_objective_candidate_v1()
    validation = validate_marketflow_expectancy_objective_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_expectancy_objective_candidate_v1.json"
    if path.exists():
        raise MarketFlowExpectancyObjectiveCandidateError(
            "candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_expectancy_objective_candidate_v1_digest": validation[
            "marketflow_expectancy_objective_candidate_v1_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
