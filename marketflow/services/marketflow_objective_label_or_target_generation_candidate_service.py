"""Offline candidate for future expectancy-oriented label or target generation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    marketflow_expectancy_objective_design_results_review_service as review_service,
)


ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_V1 = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_V1 = (
    "marketflow_objective_label_or_target_generation_candidate_v1"
)
MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION = (
    "OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION"
)

EXPECTED_SOURCE_DESIGN_RESULTS_REVIEW_DIGEST = (
    "434d589b566f8bf7feae6df2988d571cab386506b4c6fcb5ec0ee4ce17b2fe1e"
)
EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST = (
    review_service.EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST
)
EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST = (
    review_service.EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST
)
EXPECTED_SOURCE_APPROVAL_DIGEST = review_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    review_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST

SELECTED_OBJECTIVE_PATH = review_service.SELECTED_OBJECTIVE_PATH
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

TARGET_UNIVERSE = [
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",
    "JPM",
    "XOM",
    "JNJ",
    "WMT",
    "CAT",
    "LMT",
]
EXPECTED_RECORD_COUNTS = {
    ticker: 913 if ticker == "META" else 1003 for ticker in TARGET_UNIVERSE
}

SOURCE_EVIDENCE_DIGESTS = {
    "source_expectancy_objective_design_results_review_digest": EXPECTED_SOURCE_DESIGN_RESULTS_REVIEW_DIGEST,
    "source_expectancy_objective_design_execution_digest": EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST,
    "source_expectancy_objective_design_output_binding_digest": EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST,
    "source_expectancy_objective_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
    "source_expectancy_objective_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
    "source_expectancy_objective_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "source_strategy_charter_approval_digest": "ea6c77007c4827fbdd4015425bc92af40eb59b08daba3d5c2e41090df0762b92",
    "source_strategy_charter_review_digest": "d75e541f3f9d16593eb3a4da6f4f6de7a451c259295ce4e3e8f09171bbcbe8f9",
    "source_strategy_charter_digest": "3f5e3fd4088c38c5783618642c378874d2c0fbcc72954945cdca9fca68281853",
    "source_final_archive_digest": "31b61c934f3bc4970973dd2cfc0e18fb3ea4ca76e02c815bed5cf509e4a5440b",
    "source_archive_digest": "e38963a93be3518b531f60c55924b985d42761b60c07300450944b3e876dce99",
    "source_selection_digest": "fccd75c360f68fcb7181bcbbc3afb98ba57b1f667cd0b930a2e45d0041b2a048",
    "source_closure_digest": "ca179fdfe2fcc3c1572339d7e35f8f201177d59d3b7fa5dc245b58620987cbda",
    "source_readiness_digest": "e3a8803e6a72a45c4b0355bd0c8870917496325f4c9718bb977156611d5713f0",
    "source_reassessment_digest": "1ccd45069f10284923c0ac2e93f02d0a5d787c78a1f9d7feb216855fd44356e5",
    "source_results_review_digest": "75a69f5a20a4309dcfe4d9e82333d0348f8459e4ecfe2ac3a9f4373d4af3551f",
    "source_execution_digest": "b6e6429fefd2d8b0ed450845d104aab415e0142740d62bd49fc76678677aab17",
    "source_output_binding_digest": "d6d272c9369430546c73f96d220c3e33183631de98a0a5cf9471c9179bf0710a",
    "feature_label_matrix_digest": "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad",
    "feature_values_digest": "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1",
    "redesigned_label_values_digest": "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f",
    "research_registry_approval_digest": "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958",
    "records_digest": "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044",
}

LABEL_TARGET_FAMILY_IDS = [
    "TARGET_EXPECTANCY_SCORE",
    "TARGET_PAYOFF_ASYMMETRY_SCORE",
    "TARGET_REWARD_TO_RISK_CLASS",
    "TARGET_MATERIAL_MOVE_AFTER_COST_CLASS",
    "TARGET_DRAWDOWN_CONTAINED_CLASS",
    "TARGET_NO_TRADE_ABSTAIN_CLASS",
    "TARGET_TREND_CONTINUATION_QUALITY_CLASS",
    "TARGET_RELATIVE_STRENGTH_CONTEXT_CLASS",
    "TARGET_REGIME_CONDITIONED_OPPORTUNITY_CLASS",
    "TARGET_COMPOSITE_EXPECTANCY_OPPORTUNITY_CLASS",
]
RECOMMENDED_PACKAGE_ID = "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"
RECOMMENDED_PACKAGE_FAMILIES = [
    "TARGET_EXPECTANCY_SCORE",
    "TARGET_PAYOFF_ASYMMETRY_SCORE",
    "TARGET_REWARD_TO_RISK_CLASS",
    "TARGET_NO_TRADE_ABSTAIN_CLASS",
    "TARGET_MATERIAL_MOVE_AFTER_COST_CLASS",
]
SUPPORTING_PACKAGE_ID = "PACKAGE_TREND_CONTEXT_QUALITY_LABEL_SET"
SUPPORTING_PACKAGE_FAMILIES = [
    "TARGET_TREND_CONTINUATION_QUALITY_CLASS",
    "TARGET_RELATIVE_STRENGTH_CONTEXT_CLASS",
    "TARGET_REGIME_CONDITIONED_OPPORTUNITY_CLASS",
    "TARGET_DRAWDOWN_CONTAINED_CLASS",
    "TARGET_COMPOSITE_EXPECTANCY_OPPORTUNITY_CLASS",
]
FORMULA_DIMENSION_IDS = [
    "FORMULA_FORWARD_RETURN_AFTER_COST",
    "FORMULA_MAXIMUM_ADVERSE_EXCURSION",
    "FORMULA_MAXIMUM_FAVORABLE_EXCURSION",
    "FORMULA_REWARD_TO_RISK_RATIO",
    "FORMULA_EXPECTANCY_ESTIMATE",
    "FORMULA_PAYOFF_ASYMMETRY",
    "FORMULA_ABSTENTION_CONDITION",
    "FORMULA_MATERIAL_MOVE_THRESHOLD",
    "FORMULA_DRAWDOWN_LIMIT",
    "FORMULA_TIME_TO_MOVE",
    "FORMULA_VOLATILITY_ADJUSTMENT",
    "FORMULA_RELATIVE_STRENGTH_CONTEXT",
    "FORMULA_REGIME_CONTEXT",
    "FORMULA_VOLUME_PRICE_CONFIRMATION",
]
AVAILABILITY_NO_PEEK_RULE_IDS = [
    "RULE_CHRONOLOGICAL_FORWARD_WINDOW_ONLY",
    "RULE_NO_CURRENT_ROW_FUTURE_LEAKAGE",
    "RULE_FORWARD_OUTCOME_NULL_WHEN_INSUFFICIENT_FUTURE_BARS",
    "RULE_COST_AND_SLIPPAGE_ASSUMPTIONS_MUST_BE_DECLARED",
    "RULE_MAE_MFE_COMPUTED_ONLY_FROM_ALLOWED_FORWARD_WINDOW",
    "RULE_ABSTAIN_TARGET_MUST_NOT_BE_USED_AS_PREDICTOR",
    "RULE_PER_TICKER_AVAILABILITY_REPORT_REQUIRED",
    "RULE_META_LIMITATION_PRESERVED_NO_REPAIR",
    "RULE_TRAIN_VALIDATION_OOS_SPLITS_REQUIRE_SEPARATE_APPROVAL",
    "RULE_DIGEST_MANIFEST_REQUIRED",
]
PLANNED_QUALITY_CHECK_IDS = [
    "CHECK_LABEL_TARGET_SCHEMA_COMPLETENESS",
    "CHECK_FORWARD_WINDOW_ALIGNMENT",
    "CHECK_COST_SLIPPAGE_DECLARATION",
    "CHECK_NO_PEEK_FEATURE_EXCLUSION",
    "CHECK_UNAVAILABLE_TAIL_TARGETS_NULL",
    "CHECK_PER_TICKER_COVERAGE",
    "CHECK_META_LIMITATION_PRESERVED",
    "CHECK_CLASS_BALANCE_OR_TARGET_DISTRIBUTION",
    "CHECK_DIGEST_MANIFEST",
    "CHECK_RESEARCH_ONLY_AUTHORITY_BOUNDARY",
]
FUTURE_OUTPUT_IDS = [
    "future_objective_label_target_generation_manifest",
    "future_label_target_schema",
    "future_formula_definition_report",
    "future_availability_no_peek_rule_report",
    "future_cost_slippage_assumption_report",
    "future_target_values_jsonl",
    "future_target_coverage_report",
    "future_per_ticker_target_report",
    "future_meta_limitation_report",
    "future_operator_summary",
    "future_digest_manifest",
]

NEXT_CHAIN = [
    "Objective Label or Target Generation Candidate Operator Review v1.",
    "Objective Label or Target Generation Approval v1, if selected.",
    "Objective Label or Target Generation Execution v1, if approved.",
    "Objective Label or Target Generation Results Review v1.",
    "Future signal/feature planning only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "objective_label_or_target_generation_candidate_operator_review",
    "objective_label_or_target_generation_approval_if_selected",
    "objective_label_or_target_generation_execution_if_approved",
    "objective_label_or_target_generation_results_review",
    "signal_or_feature_generation_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_generate_labels",
    "candidate_does_not_create_targets",
    "candidate_does_not_create_target_values",
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
    "candidate_does_not_rerun_design_execution",
    "candidate_does_not_rerun_design_results_review",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_design_results_review_digest_bound",
    "source_design_execution_digest_bound",
    "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound",
    "source_candidate_review_digest_bound",
    "source_candidate_digest_bound",
    "source_strategy_charter_approval_digest_bound",
    "source_strategy_charter_digest_bound",
    "source_final_archive_digest_bound",
    "source_archive_digest_bound",
    "source_selection_digest_bound",
    "source_closure_digest_bound",
    "source_readiness_digest_bound",
    "source_reassessment_digest_bound",
    "source_results_review_digest_bound",
    "source_execution_digest_bound",
    "matrix_digest_bound",
    "feature_values_digest_bound",
    "label_values_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "design_results_review_ready_true",
    "ready_for_label_or_target_candidate_true",
    "candidate_created_true",
    "candidate_ready_true",
    "candidate_scope_only",
    "selected_objective_path_preserved",
    "candidate_philosophy_defined",
    "label_target_families_defined_10",
    "recommended_package_defined",
    "supporting_package_defined",
    "formula_dimensions_defined",
    "availability_rules_defined",
    "quality_checks_defined",
    "future_outputs_not_generated",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "selection_created_false",
    "approval_created_false",
    "generation_created_false",
    "label_generation_authorized_false",
    "label_generation_performed_false",
    "new_targets_created_false",
    "target_values_created_false",
    "target_definition_change_authorized_false",
    "feature_generation_authorized_false",
    "feature_generation_performed_false",
    "feature_label_matrix_created_false",
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
    "design_execution_rerun_false",
    "design_results_review_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowObjectiveLabelOrTargetGenerationCandidateError(ValueError):
    """Raised when the candidate violates its non-authorizing boundary."""


def _label_target_families() -> list[dict[str, Any]]:
    return [
        {
            "label_target_family_id": family_id,
            "candidate_status": "LABEL_OR_TARGET_CANDIDATE_DEFINED_NOT_GENERATED",
            "operator_review_required": True,
            "approval_required_before_generation": True,
            "label_generation_authorized": False,
            "target_creation_authorized": False,
            "target_values_created": False,
            "feature_generation_authorized": False,
            "metric_computation_authorized": False,
            "backtest_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family_id in LABEL_TARGET_FAMILY_IDS
    ]


def _package(
    *, package_id: str, status: str, includes: list[str], rationale: str
) -> dict[str, Any]:
    return {
        "package_id": package_id,
        "status": status,
        "includes": list(includes),
        "rationale": rationale,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _formula_dimensions() -> list[dict[str, Any]]:
    return [
        {
            "formula_dimension_id": dimension_id,
            "formula_status": "CANDIDATE_FORMULA_NOT_COMPUTED",
            "generation_authorized": False,
            "metric_computation_authorized": False,
        }
        for dimension_id in FORMULA_DIMENSION_IDS
    ]


def _availability_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": rule_id,
            "rule_status": "PLANNED_NOT_EXECUTED",
            "requires_future_generation_approval": True,
        }
        for rule_id in AVAILABILITY_NO_PEEK_RULE_IDS
    ]


def _quality_checks() -> list[dict[str, Any]]:
    return [
        {
            "quality_check_id": check_id,
            "quality_check_status": "PLANNED_NOT_EXECUTED",
        }
        for check_id in PLANNED_QUALITY_CHECK_IDS
    ]


def _future_outputs() -> list[dict[str, Any]]:
    return [
        {
            "future_output_id": output_id,
            "output_status": "PLANNED_NOT_GENERATED",
            "generated": False,
            "research_only": True,
            "non_actionable": True,
        }
        for output_id in FUTURE_OUTPUT_IDS
    ]


def per_ticker_objective_label_or_target_generation_candidate_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for one ticker candidate."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_objective_label_or_target_generation_candidate_digest", None)
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
            "design_results_review_status": review_service.MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE_READY,
            "objective_label_or_target_generation_candidate_status": "READY_FOR_OPERATOR_REVIEW",
            "selected_objective_path": SELECTED_OBJECTIVE_PATH,
            "recommended_label_target_package": RECOMMENDED_PACKAGE_ID,
            "label_generation_authorized": False,
            "label_generation_performed": False,
            "new_targets_created": False,
            "target_values_created": False,
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
            "source_design_results_review_digest": EXPECTED_SOURCE_DESIGN_RESULTS_REVIEW_DIGEST,
            "source_design_execution_digest": EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST,
            "candidate_note": (
                "PRESERVE_META_LIMITATION_IN_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry[
            "per_ticker_objective_label_or_target_generation_candidate_digest"
        ] = per_ticker_objective_label_or_target_generation_candidate_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    recommended = _package(
        package_id=RECOMMENDED_PACKAGE_ID,
        status="RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        includes=RECOMMENDED_PACKAGE_FAMILIES,
        rationale=(
            "The first generation package should directly test expectancy, "
            "payoff asymmetry, reward/risk, material move after cost, and "
            "abstention/no-trade behavior."
        ),
    )
    supporting = _package(
        package_id=SUPPORTING_PACKAGE_ID,
        status="AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        includes=SUPPORTING_PACKAGE_FAMILIES,
        rationale=(
            "Secondary package for trend quality, relative strength, regime "
            "filtering, drawdown control, and composite opportunity scoring."
        ),
    )
    candidate = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "source_expectancy_objective_design_results_review_artifact_kind": review_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE,
        "source_expectancy_objective_design_results_review_status": review_service.MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE_READY,
        "source_expectancy_objective_design_results_review_scope": review_service.EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_ONLY_NOT_GENERATION,
        **SOURCE_EVIDENCE_DIGESTS,
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
        "candidate_basis": dict(review_service.REVIEW_STATUSES),
        "source_expected_output_count": 11,
        "source_observed_output_count": 11,
        "source_output_digest_mismatch_count": 0,
        "source_output_file_inspection_performed": True,
        "source_digest_manifest_self_reference_policy": review_service.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "source_objective_family_count": 10,
        "source_expectancy_payoff_candidate_field_count": 7,
        "source_abstention_candidate_field_count": 6,
        "source_material_move_candidate_field_count": 5,
        "source_label_generation_plan_step_count": 10,
        "source_validation_metric_count": 14,
        "source_baseline_count": 7,
        "source_per_ticker_review_count": 12,
        "candidate_philosophy": (
            "Prepare the future generation of expectancy-oriented labels or "
            "target definitions while preserving all no-generation boundaries."
        ),
        "candidate_primary_question": (
            "Which label or target specification should be generated first to "
            "represent expectancy/payoff opportunity with abstention support?"
        ),
        "candidate_secondary_question": (
            "How can generated labels or targets avoid recreating the "
            "majority/flat-class trap of the archived classification chain?"
        ),
        "candidate_boundary": (
            "Candidate-only; no label values, target values, feature values, "
            "matrix rows, metrics, models, backtests, signals, recommendations, "
            "or runtime artifacts are generated."
        ),
        "proposed_label_target_families": _label_target_families(),
        "recommended_label_target_package": recommended,
        "supporting_label_target_package": supporting,
        "formula_candidate_dimensions": _formula_dimensions(),
        "availability_no_peek_rules": _availability_rules(),
        "planned_quality_checks": _quality_checks(),
        "future_outputs": _future_outputs(),
        "future_outputs_generated": False,
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "expectancy_objective_selected": True,
        "expectancy_objective_approved": True,
        "expectancy_objective_authorized": True,
        "expectancy_objective_design_executed": True,
        "expectancy_objective_design_results_review_ready": True,
        "ready_for_objective_label_or_target_generation_candidate": True,
        "objective_label_or_target_generation_candidate_created": True,
        "objective_label_or_target_generation_candidate_ready_for_operator_review": True,
        "ready_for_objective_label_or_target_generation_candidate_operator_review": True,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "objective_label_or_target_generation_approved": False,
        "objective_label_or_target_generation_authorized": False,
        "objective_label_or_target_generation_performed": False,
        "label_generation_authorized": False,
        "label_generation_performed": False,
        "new_targets_created": False,
        "target_values_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
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
        "objective_design_execution_rerun_performed": False,
        "objective_design_results_review_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }
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
        isinstance(entry, Mapping)
        and entry.get(
            "per_ticker_objective_label_or_target_generation_candidate_digest"
        )
        == per_ticker_objective_label_or_target_generation_candidate_digest_v1(
            entry
        )
        for entry in entries
    )


def _all_future_outputs_not_generated(candidate: Mapping[str, Any]) -> bool:
    rows = candidate.get("future_outputs")
    return isinstance(rows, list) and len(rows) == len(FUTURE_OUTPUT_IDS) and all(
        row.get("output_status") == "PLANNED_NOT_GENERATED"
        and row.get("generated") is False
        for row in rows
        if isinstance(row, Mapping)
    )


def _check_definitions(candidate: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    evidence = SOURCE_EVIDENCE_DIGESTS
    entries = candidate.get("per_ticker_candidate_entries", [])
    return [
        ("source_design_results_review_digest_bound", evidence["source_expectancy_objective_design_results_review_digest"], candidate.get("source_expectancy_objective_design_results_review_digest")),
        ("source_design_execution_digest_bound", evidence["source_expectancy_objective_design_execution_digest"], candidate.get("source_expectancy_objective_design_execution_digest")),
        ("source_design_output_binding_digest_bound", evidence["source_expectancy_objective_design_output_binding_digest"], candidate.get("source_expectancy_objective_design_output_binding_digest")),
        ("source_expectancy_objective_approval_digest_bound", evidence["source_expectancy_objective_approval_digest"], candidate.get("source_expectancy_objective_approval_digest")),
        ("source_candidate_review_digest_bound", evidence["source_expectancy_objective_candidate_review_digest"], candidate.get("source_expectancy_objective_candidate_review_digest")),
        ("source_candidate_digest_bound", evidence["source_expectancy_objective_candidate_digest"], candidate.get("source_expectancy_objective_candidate_digest")),
        ("source_strategy_charter_approval_digest_bound", evidence["source_strategy_charter_approval_digest"], candidate.get("source_strategy_charter_approval_digest")),
        ("source_strategy_charter_digest_bound", evidence["source_strategy_charter_digest"], candidate.get("source_strategy_charter_digest")),
        ("source_final_archive_digest_bound", evidence["source_final_archive_digest"], candidate.get("source_final_archive_digest")),
        ("source_archive_digest_bound", evidence["source_archive_digest"], candidate.get("source_archive_digest")),
        ("source_selection_digest_bound", evidence["source_selection_digest"], candidate.get("source_selection_digest")),
        ("source_closure_digest_bound", evidence["source_closure_digest"], candidate.get("source_closure_digest")),
        ("source_readiness_digest_bound", evidence["source_readiness_digest"], candidate.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", evidence["source_reassessment_digest"], candidate.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", evidence["source_results_review_digest"], candidate.get("source_results_review_digest")),
        ("source_execution_digest_bound", evidence["source_execution_digest"], candidate.get("source_execution_digest")),
        ("matrix_digest_bound", evidence["feature_label_matrix_digest"], candidate.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", evidence["feature_values_digest"], candidate.get("feature_values_digest")),
        ("label_values_digest_bound", evidence["redesigned_label_values_digest"], candidate.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", evidence["research_registry_approval_digest"], candidate.get("research_registry_approval_digest")),
        ("records_digest_bound", evidence["records_digest"], candidate.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, candidate.get("target_universe")),
        ("records_digest_preserved", evidence["records_digest"], candidate.get("records_digest")),
        ("meta_913_preserved", 913, candidate.get("meta_record_count")),
        ("design_results_review_ready_true", True, candidate.get("expectancy_objective_design_results_review_ready")),
        ("ready_for_label_or_target_candidate_true", True, candidate.get("ready_for_objective_label_or_target_generation_candidate")),
        ("candidate_created_true", True, candidate.get("objective_label_or_target_generation_candidate_created")),
        ("candidate_ready_true", True, candidate.get("objective_label_or_target_generation_candidate_ready_for_operator_review")),
        ("candidate_scope_only", OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION, candidate.get("candidate_scope")),
        ("selected_objective_path_preserved", SELECTED_OBJECTIVE_PATH, candidate.get("selected_objective_path")),
        ("candidate_philosophy_defined", True, bool(candidate.get("candidate_philosophy"))),
        ("label_target_families_defined_10", 10, len(candidate.get("proposed_label_target_families", []))),
        ("recommended_package_defined", RECOMMENDED_PACKAGE_ID, candidate.get("recommended_label_target_package", {}).get("package_id")),
        ("supporting_package_defined", SUPPORTING_PACKAGE_ID, candidate.get("supporting_label_target_package", {}).get("package_id")),
        ("formula_dimensions_defined", 14, len(candidate.get("formula_candidate_dimensions", []))),
        ("availability_rules_defined", 10, len(candidate.get("availability_no_peek_rules", []))),
        ("quality_checks_defined", 10, len(candidate.get("planned_quality_checks", []))),
        ("future_outputs_not_generated", True, _all_future_outputs_not_generated(candidate)),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("selection_created_false", False, candidate.get("selection_created")),
        ("approval_created_false", False, candidate.get("approval_created")),
        ("generation_created_false", False, candidate.get("generation_created")),
        ("label_generation_authorized_false", False, candidate.get("label_generation_authorized")),
        ("label_generation_performed_false", False, candidate.get("label_generation_performed")),
        ("new_targets_created_false", False, candidate.get("new_targets_created")),
        ("target_values_created_false", False, candidate.get("target_values_created")),
        ("target_definition_change_authorized_false", False, candidate.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, candidate.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, candidate.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, candidate.get("feature_label_matrix_created")),
        ("backtest_execution_authorized_false", False, candidate.get("backtest_execution_authorized")),
        ("backtest_execution_performed_false", False, candidate.get("backtest_execution_performed")),
        ("model_training_authorized_false", False, candidate.get("model_training_authorized")),
        ("model_training_performed_false", False, candidate.get("model_training_performed")),
        ("metric_computation_authorized_false", False, candidate.get("metric_computation_authorized")),
        ("metric_computation_performed_false", False, candidate.get("metric_computation_performed")),
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
        ("design_execution_rerun_false", False, candidate.get("objective_design_execution_rerun_performed")),
        ("design_results_review_rerun_false", False, candidate.get("objective_design_results_review_rerun_performed")),
        ("raw_provider_payloads_not_committed", False, candidate.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, candidate.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, candidate.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, candidate.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        ("no_tracked_marketflow_files", True, candidate.get("no_tracked_marketflow_files")),
    ]


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    definitions = _check_definitions(candidate)
    if [definition[0] for definition in definitions] != REQUIRED_CHECK_IDS:
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateError(
            "internal checklist definition mismatch"
        )
    return [_check(*definition) for definition in definitions]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "objective_label_or_target_generation_candidate_created": not failed,
        "objective_label_or_target_generation_candidate_ready_for_operator_review": not failed,
        "recommended_label_target_package": RECOMMENDED_PACKAGE_ID,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "label_generation_performed": False,
        "new_targets_created": False,
        "target_values_created": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(candidate: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(candidate))
    payload.pop(
        "marketflow_objective_label_or_target_generation_candidate_v1_digest",
        None,
    )
    return payload


def marketflow_objective_label_or_target_generation_candidate_v1_digest(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_marketflow_objective_label_or_target_generation_candidate_v1() -> dict:
    """Build the candidate offline without reading or generating runtime outputs."""
    candidate = _base_candidate()
    checklist = _checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(checklist)
    candidate[
        "marketflow_objective_label_or_target_generation_candidate_v1_digest"
    ] = marketflow_objective_label_or_target_generation_candidate_v1_digest(
        candidate
    )
    validate_marketflow_objective_label_or_target_generation_candidate_v1(
        candidate
    )
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateError(
            f"{field} mismatch"
        )


def validate_marketflow_objective_label_or_target_generation_candidate_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Validate the complete candidate content and every closed authority gate."""
    if not isinstance(candidate, dict):
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateError(
            "candidate must be a JSON object"
        )
    expected = _base_candidate()
    for field, value in expected.items():
        _expect(candidate.get(field), value, field)
    entries = candidate.get("per_ticker_candidate_entries")
    if not _per_ticker_digests_valid(entries):
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateError(
            "per-ticker candidate digests mismatch"
        )
    expected_checklist = _checklist(candidate)
    _expect(candidate.get("candidate_checklist"), expected_checklist, "candidate checklist")
    if any(row.get("status") != PASS for row in expected_checklist):
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateError(
            "candidate checklist failed"
        )
    _expect(candidate.get("candidate_summary"), _summary(expected_checklist), "candidate summary")
    digest = candidate.get(
        "marketflow_objective_label_or_target_generation_candidate_v1_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateError(
            "candidate digest missing"
        )
    _expect(
        digest,
        marketflow_objective_label_or_target_generation_candidate_v1_digest(
            candidate
        ),
        "candidate digest",
    )
    return {
        "status": "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_objective_label_or_target_generation_candidate_v1_digest": digest,
        **{
            key: candidate["candidate_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_objective_label_or_target_generation_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render a sanitized Markdown view of the validated candidate."""
    validation = validate_marketflow_objective_label_or_target_generation_candidate_v1(
        candidate
    )
    sections = [
        ("Title", ["Objective Label or Target Generation Candidate v1"]),
        ("Objective Label or Target Generation Candidate v1", [f"Artifact/status/scope: {candidate['artifact_kind']} / {candidate['candidate_status']} / {candidate['candidate_scope']}.", f"Candidate digest: {validation['marketflow_objective_label_or_target_generation_candidate_v1_digest']}."]),
        ("Source Design Results Review", [f"Review/execution/output-binding digests: {candidate['source_expectancy_objective_design_results_review_digest']} / {candidate['source_expectancy_objective_design_execution_digest']} / {candidate['source_expectancy_objective_design_output_binding_digest']}."]),
        ("Bound Evidence", [f"Approval/candidate review/candidate: {candidate['source_expectancy_objective_approval_digest']} / {candidate['source_expectancy_objective_candidate_review_digest']} / {candidate['source_expectancy_objective_candidate_digest']}.", f"Matrix/features/labels/records: {candidate['feature_label_matrix_digest']} / {candidate['feature_values_digest']} / {candidate['redesigned_label_values_digest']} / {candidate['records_digest']}."]),
        ("Dataset and Universe", [f"{candidate['dataset_name']} / {candidate['total_canonical_record_count']} records.", "Universe: " + ", ".join(candidate["target_universe"]) + ".", "META remains 913; every non-META ticker remains 1003."]),
        ("Candidate Basis", [f"{key}: {value}." for key, value in candidate["candidate_basis"].items()]),
        ("Candidate Philosophy", [candidate["candidate_philosophy"], candidate["candidate_primary_question"], candidate["candidate_secondary_question"], candidate["candidate_boundary"]]),
        ("Proposed Label/Target Families", [f"{row['label_target_family_id']}: {row['candidate_status']}." for row in candidate["proposed_label_target_families"]]),
        ("Recommended Label/Target Package", [f"{candidate['recommended_label_target_package']['package_id']}: {candidate['recommended_label_target_package']['status']}.", candidate["recommended_label_target_package"]["rationale"]]),
        ("Supporting Label/Target Package", [f"{candidate['supporting_label_target_package']['package_id']}: {candidate['supporting_label_target_package']['status']}.", candidate["supporting_label_target_package"]["rationale"]]),
        ("Formula Candidate Dimensions", [row["formula_dimension_id"] for row in candidate["formula_candidate_dimensions"]]),
        ("Availability and No-Peek Rules", [row["rule_id"] for row in candidate["availability_no_peek_rules"]]),
        ("Planned Quality Checks", [row["quality_check_id"] for row in candidate["planned_quality_checks"]]),
        ("Future Outputs", [f"{row['future_output_id']}: {row['output_status']}." for row in candidate["future_outputs"]]),
        ("Per-Ticker Candidate Summary", [f"{row['ticker']}: records {row['historical_record_count']}, digest {row['per_ticker_objective_label_or_target_generation_candidate_digest']}." for row in candidate["per_ticker_candidate_entries"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: {candidate['candidate_summary']['total_checks']} / {candidate['candidate_summary']['passed_checks']} / {candidate['candidate_summary']['failed_checks']} / {candidate['candidate_summary']['blocker_count']}."]),
        ("Guardrails", [candidate["candidate_boundary"]]),
    ]
    lines = ["# Objective Label or Target Generation Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_objective_label_or_target_generation_candidate_v1(
    output_dir: str | Path,
) -> dict[str, Any]:
    """Write canonical candidate JSON once in an explicitly supplied directory."""
    candidate = build_marketflow_objective_label_or_target_generation_candidate_v1()
    validation = validate_marketflow_objective_label_or_target_generation_candidate_v1(
        candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_objective_label_or_target_generation_candidate_v1.json"
    payload = canonical_json_bytes(candidate)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateError(
            "objective label or target generation candidate output already exists"
        ) from exc
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "marketflow_objective_label_or_target_generation_candidate_v1_digest": validation[
            "marketflow_objective_label_or_target_generation_candidate_v1_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
