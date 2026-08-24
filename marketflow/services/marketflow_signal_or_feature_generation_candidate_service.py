"""Offline candidate for future signal or feature generation."""

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
    marketflow_objective_label_or_target_generation_results_review_service as review_service,
)


ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1 = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1 = (
    "marketflow_signal_or_feature_generation_candidate_v1"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION = (
    "SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_VALID = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_VALID"
)

PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET = (
    "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"
)
EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT = (
    "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
)
PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET = "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"
PACKAGE_REGIME_CONTEXT_SIGNAL_SET = "PACKAGE_REGIME_CONTEXT_SIGNAL_SET"

EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = (
    "41afa9e7159f2788f8dce3c44343c2058414fb51efb95b5d6714246ab866e47c"
)
EXPECTED_SOURCE_EXECUTION_DIGEST = review_service.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = (
    review_service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST
)
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = (
    review_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
)
EXPECTED_SOURCE_APPROVAL_DIGEST = review_service.EXPECTED_SOURCE_APPROVAL_DIGEST

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
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
    "marketflow_objective_label_or_target_generation_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
    "marketflow_objective_label_or_target_generation_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
    "objective_label_or_target_generation_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
    "objective_label_or_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
    "marketflow_objective_label_or_target_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
    "marketflow_objective_label_or_target_generation_candidate_operator_review_digest": "ec9e117ad735e984a52c5600374ae274aceec8e58bc5aeb9e75a4357dcfd5e1b",
    "marketflow_objective_label_or_target_generation_candidate_v1_digest": "26f26f739a8161633beb27e7993cd1af445a070978fbc61699c2df68adcdfff9",
    "marketflow_expectancy_objective_design_results_review_digest": "434d589b566f8bf7feae6df2988d571cab386506b4c6fcb5ec0ee4ce17b2fe1e",
    "marketflow_expectancy_objective_design_execution_digest": "ba9661d34b57dbd464b6ec559c5b3e48df5ff78847102aa16d2d9e45f076ec11",
    "expectancy_objective_design_output_binding_digest": "3ee2acfb7461769fc054e1afb34e222302297b04d66a08b21fb411613e0585a4",
    "marketflow_expectancy_objective_approval_digest": "4ae9d4e81cc41b9578ac061574669d6fb11a45ed56871f4d05a02aacad165a1d",
    "marketflow_expectancy_objective_candidate_operator_review_digest": "baac33f292d77d26eae6eacc4cffaa5cdabe17785cb2c090c053c82d1bfe551d",
    "marketflow_expectancy_objective_candidate_v1_digest": "9b241ab1be15921384d97d75a11ac7858065d041c0b8a02144e97c3e3ed3bc17",
    "marketflow_algorithm_strategy_charter_approval_digest": "ea6c77007c4827fbdd4015425bc92af40eb59b08daba3d5c2e41090df0762b92",
    "marketflow_algorithm_strategy_charter_operator_review_digest": "d75e541f3f9d16593eb3a4da6f4f6de7a451c259295ce4e3e8f09171bbcbe8f9",
    "marketflow_algorithm_strategy_charter_v1_digest": "3f5e3fd4088c38c5783618642c378874d2c0fbcc72954945cdca9fca68281853",
    "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest": "31b61c934f3bc4970973dd2cfc0e18fb3ea4ca76e02c815bed5cf509e4a5440b",
    "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest": "e38963a93be3518b531f60c55924b985d42761b60c07300450944b3e876dce99",
    "operator_method_or_closure_selection_using_improved_evidence_digest": "fccd75c360f68fcb7181bcbbc3afb98ba57b1f667cd0b930a2e45d0041b2a048",
    "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest": "ca179fdfe2fcc3c1572339d7e35f8f201177d59d3b7fa5dc245b58620987cbda",
    "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest": "e3a8803e6a72a45c4b0355bd0c8870917496325f4c9718bb977156611d5713f0",
    "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": "1ccd45069f10284923c0ac2e93f02d0a5d787c78a1f9d7feb216855fd44356e5",
    "additional_predictive_evidence_results_review_using_improved_evidence_digest": "75a69f5a20a4309dcfe4d9e82333d0348f8459e4ecfe2ac3a9f4373d4af3551f",
    "additional_predictive_evidence_execution_using_improved_evidence_digest": "b6e6429fefd2d8b0ed450845d104aab415e0142740d62bd49fc76678677aab17",
    "additional_predictive_evidence_output_binding_digest": "d6d272c9369430546c73f96d220c3e33183631de98a0a5cf9471c9179bf0710a",
    "feature_label_matrix_digest": "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad",
    "feature_values_digest": "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1",
    "redesigned_label_values_digest": "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f",
    "research_registry_approval_digest": "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958",
    "records_digest": "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044",
}

SIGNAL_FAMILY_IDS = [
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
FEATURE_FAMILY_IDS = [
    "FEATURE_PRICE_RETURN_AND_RANGE",
    "FEATURE_VOLUME_AND_LIQUIDITY",
    "FEATURE_VOLUME_PRICE_RELATIONSHIP",
    "FEATURE_VOLATILITY_AND_ATR",
    "FEATURE_MOMENTUM_AND_TREND",
    "FEATURE_RELATIVE_STRENGTH_AND_RANKING",
    "FEATURE_REGIME_AND_MARKET_CONTEXT",
    "FEATURE_ABSTENTION_AND_NOISE_CONTEXT",
    "FEATURE_TARGET_ALIGNMENT_METADATA_ONLY",
    "FEATURE_DATA_QUALITY_AND_META_LIMITATION",
]
FEATURE_GROUP_IDS = [
    "GROUP_CLOSE_TO_CLOSE_RETURNS",
    "GROUP_INTRADAY_RANGE_AND_BODY",
    "GROUP_CLOSE_LOCATION_VALUE",
    "GROUP_VOLUME_CHANGE_AND_ZSCORE",
    "GROUP_SPREAD_VOLUME_INTERACTION",
    "GROUP_EFFORT_RESULT_DIVERGENCE",
    "GROUP_ATR_AND_VOLATILITY_COMPRESSION",
    "GROUP_MOVING_AVERAGE_SLOPE",
    "GROUP_BREAKOUT_PULLBACK_CONTEXT",
    "GROUP_RELATIVE_STRENGTH_VS_UNIVERSE",
    "GROUP_RELATIVE_STRENGTH_RANK",
    "GROUP_MARKET_REGIME_CONTEXT",
    "GROUP_TICKER_REGIME_CONTEXT",
    "GROUP_ABSTENTION_NOISE_CONTEXT",
    "GROUP_TARGET_PROFILE_METADATA_ONLY",
    "GROUP_DATA_AVAILABILITY_FLAGS",
    "GROUP_META_LIMITATION_FLAGS",
]
NO_PEEK_RULE_IDS = [
    "RULE_FEATURES_USE_ONLY_CURRENT_OR_PRIOR_OHLCV",
    "RULE_NO_FORWARD_RETURN_AS_FEATURE",
    "RULE_NO_TARGET_VALUE_AS_FEATURE",
    "RULE_NO_TARGET_CLASS_AS_FEATURE",
    "RULE_TARGET_PROFILE_ALLOWED_AS_METADATA_ONLY",
    "RULE_TARGET_HORIZON_ALLOWED_AS_METADATA_ONLY",
    "RULE_CHRONOLOGICAL_SPLITS_REQUIRE_SEPARATE_APPROVAL",
    "RULE_PER_TICKER_HISTORY_ONLY_WINDOWS",
    "RULE_META_LIMITATION_PRESERVED_NO_REPAIR",
    "RULE_FEATURE_DIGEST_MANIFEST_REQUIRED",
]
PLANNED_QUALITY_CHECK_IDS = [
    "CHECK_FEATURE_SCHEMA_COMPLETENESS",
    "CHECK_HISTORY_ONLY_FEATURE_WINDOWS",
    "CHECK_NO_TARGET_VALUE_IN_FEATURES",
    "CHECK_NO_TARGET_CLASS_IN_FEATURES",
    "CHECK_NO_FORWARD_RETURN_IN_FEATURES",
    "CHECK_PER_TICKER_FEATURE_COVERAGE",
    "CHECK_META_LIMITATION_PRESERVED",
    "CHECK_MISSINGNESS_AND_AVAILABILITY",
    "CHECK_DIGEST_MANIFEST",
    "CHECK_RESEARCH_ONLY_AUTHORITY_BOUNDARY",
]
FUTURE_OUTPUT_IDS = [
    "future_signal_feature_generation_manifest",
    "future_signal_feature_schema",
    "future_feature_values_jsonl",
    "future_feature_coverage_report",
    "future_feature_group_report",
    "future_no_peek_feature_report",
    "future_per_ticker_feature_report",
    "future_meta_limitation_report",
    "future_operator_summary",
    "future_digest_manifest",
]

RECOMMENDED_SIGNAL_FAMILIES = [
    "SIGNAL_TREND_STRUCTURE",
    "SIGNAL_VOLUME_PRICE_ANALYSIS",
    "SIGNAL_CLOSE_LOCATION_AND_SPREAD",
    "SIGNAL_EFFORT_RESULT_BEHAVIOR",
    "SIGNAL_RELATIVE_STRENGTH",
    "SIGNAL_VOLATILITY_COMPRESSION_EXPANSION",
    "SIGNAL_NOISE_AND_ABSTENTION_FILTER",
]
RECOMMENDED_FEATURE_FAMILIES = [
    "FEATURE_PRICE_RETURN_AND_RANGE",
    "FEATURE_VOLUME_AND_LIQUIDITY",
    "FEATURE_VOLUME_PRICE_RELATIONSHIP",
    "FEATURE_VOLATILITY_AND_ATR",
    "FEATURE_MOMENTUM_AND_TREND",
    "FEATURE_RELATIVE_STRENGTH_AND_RANKING",
    "FEATURE_ABSTENTION_AND_NOISE_CONTEXT",
    "FEATURE_DATA_QUALITY_AND_META_LIMITATION",
]
SUPPORTING_SIGNAL_FAMILIES = [
    "SIGNAL_REGIME_CONTEXT",
    "SIGNAL_BREAKOUT_PULLBACK_STRUCTURE",
    "SIGNAL_ABSORPTION_OR_DISTRIBUTION",
]
SUPPORTING_FEATURE_FAMILIES = [
    "FEATURE_REGIME_AND_MARKET_CONTEXT",
    "FEATURE_TARGET_ALIGNMENT_METADATA_ONLY",
]

NEXT_CHAIN = [
    "Signal or Feature Generation Candidate Operator Review v1.",
    "Signal or Feature Generation Approval v1, if selected.",
    "Signal or Feature Generation Execution v1, if approved.",
    "Signal or Feature Generation Results Review v1.",
    "Future feature-label matrix candidate only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "signal_or_feature_generation_candidate_operator_review",
    "signal_or_feature_generation_approval_if_selected",
    "signal_or_feature_generation_execution_if_approved",
    "signal_or_feature_generation_results_review",
    "feature_label_matrix_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "candidate_does_not_generate_signal_values",
    "candidate_does_not_generate_feature_values",
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
    "candidate_does_not_rerun_target_generation_execution",
    "candidate_does_not_rerun_target_results_review",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_target_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class MarketFlowSignalOrFeatureGenerationCandidateError(ValueError):
    """Raised when the candidate violates its offline governance contract."""


def _signal_families() -> list[dict[str, Any]]:
    return [
        {
            "signal_family_id": family_id,
            "candidate_status": "SIGNAL_CANDIDATE_DEFINED_NOT_GENERATED",
            "operator_review_required": True,
            "approval_required_before_generation": True,
            "signal_generation_authorized": False,
            "feature_generation_authorized": False,
            "feature_values_created": False,
            "feature_label_matrix_created": False,
            "metric_computation_authorized": False,
            "backtest_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family_id in SIGNAL_FAMILY_IDS
    ]


def _feature_families() -> list[dict[str, Any]]:
    return [
        {
            "feature_family_id": family_id,
            "candidate_status": "FEATURE_CANDIDATE_DEFINED_NOT_GENERATED",
            "operator_review_required": True,
            "approval_required_before_generation": True,
            "feature_generation_authorized": False,
            "feature_values_created": False,
            "feature_label_matrix_created": False,
            "target_values_used_as_features": False,
            "future_data_used_as_features": False,
            "metric_computation_authorized": False,
            "backtest_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family_id in FEATURE_FAMILY_IDS
    ]


def _package(
    *, package_id: str, status: str, signal_families: list[str],
    feature_families: list[str], rationale: str
) -> dict[str, Any]:
    return {
        "package_id": package_id,
        "status": status,
        "includes_signal_families": list(signal_families),
        "includes_feature_families": list(feature_families),
        "rationale": rationale,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _feature_groups() -> list[dict[str, Any]]:
    return [
        {
            "feature_group_id": group_id,
            "group_status": "FEATURE_GROUP_CANDIDATE_NOT_GENERATED",
            "requires_future_generation_approval": True,
            "target_values_used_as_features": False,
            "future_data_used_as_features": False,
        }
        for group_id in FEATURE_GROUP_IDS
    ]


def _no_peek_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": rule_id,
            "rule_status": "PLANNED_NOT_EXECUTED",
            "requires_future_generation_approval": True,
        }
        for rule_id in NO_PEEK_RULE_IDS
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


def per_ticker_signal_or_feature_generation_candidate_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for one ticker entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_signal_or_feature_generation_candidate_digest", None)
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
            "target_generation_results_review_status": review_service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
            "signal_or_feature_generation_candidate_status": "READY_FOR_OPERATOR_REVIEW",
            "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "recommended_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "target_profile_count": 15,
            "target_row_count": 13695 if is_meta else 15045,
            "available_target_row_count": 13520 if is_meta else 14870,
            "unavailable_target_row_count": 175,
            "signal_generation_authorized": False,
            "signal_generation_performed": False,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_values_created": False,
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
            "source_target_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
            "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
            "candidate_note": (
                "PRESERVE_META_LIMITATION_IN_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_signal_or_feature_generation_candidate_digest"] = (
            per_ticker_signal_or_feature_generation_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    recommended = _package(
        package_id=PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        status="RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        signal_families=RECOMMENDED_SIGNAL_FAMILIES,
        feature_families=RECOMMENDED_FEATURE_FAMILIES,
        rationale=(
            "This package focuses on historical trend quality, volume-price "
            "confirmation, relative strength, volatility context, and "
            "abstention/noise filtering to support expectancy-target research."
        ),
    )
    supporting = _package(
        package_id=PACKAGE_REGIME_CONTEXT_SIGNAL_SET,
        status="AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        signal_families=SUPPORTING_SIGNAL_FAMILIES,
        feature_families=SUPPORTING_FEATURE_FAMILIES,
        rationale=(
            "Supporting package for regime, setup context, target-profile "
            "alignment metadata, and later VPA/Wyckoff baseline preparation."
        ),
    )
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "source_objective_label_or_target_generation_results_review_artifact_kind": review_service.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE,
        "source_objective_label_or_target_generation_results_review_status": review_service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
        "source_objective_label_or_target_generation_results_review_scope": review_service.OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_GENERATION_NOT_BACKTEST,
        "source_objective_label_or_target_generation_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_objective_label_or_target_generation_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_objective_label_or_target_generation_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_objective_label_or_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_objective_label_or_target_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
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
        "target_results_review_ready": True,
        "target_profile_count": 15,
        "target_row_count": 179190,
        "available_target_row_count": 177090,
        "unavailable_target_row_count": 2100,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "candidate_philosophy": (
            "Prepare future historical signal and feature generation that can "
            "explain or anticipate the research-only expectancy target outputs "
            "without using target values, future data, strategy scores, or "
            "recommendations as features."
        ),
        "candidate_primary_question": (
            "Which history-only price, volume, relative-strength, volatility, "
            "regime, and abstention-context features should be generated first "
            "to support expectancy-target research?"
        ),
        "candidate_secondary_question": (
            "How can feature generation preserve no-peek controls and avoid "
            "leaking target values into predictors?"
        ),
        "candidate_boundary": (
            "Candidate-only; no signal values, feature values, feature-label "
            "matrix rows, metrics, models, backtests, strategy scores, "
            "recommendations, or runtime artifacts are generated."
        ),
        "proposed_signal_families": _signal_families(),
        "proposed_feature_families": _feature_families(),
        "recommended_feature_package": recommended,
        "supporting_feature_package": supporting,
        "proposed_feature_groups": _feature_groups(),
        "no_peek_and_target_separation_rules": _no_peek_rules(),
        "planned_quality_checks": _quality_checks(),
        "future_outputs": _future_outputs(),
        "future_outputs_generated": False,
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "objective_label_or_target_generation_results_review_created": True,
        "objective_label_or_target_generation_results_review_ready": True,
        "ready_for_signal_or_feature_generation_candidate": True,
        "signal_or_feature_generation_candidate_created": True,
        "signal_or_feature_generation_candidate_ready_for_operator_review": True,
        "ready_for_signal_or_feature_generation_candidate_operator_review": True,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "signal_or_feature_generation_selected": False,
        "signal_or_feature_generation_approved": False,
        "signal_or_feature_generation_authorized": False,
        "signal_or_feature_generation_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "signal_generation_authorized": False,
        "signal_generation_performed": False,
        "feature_values_created": False,
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
        "target_generation_execution_rerun_performed": False,
        "target_generation_results_review_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
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


def _ids(rows: Any, key: str) -> list[Any]:
    if not isinstance(rows, list) or not all(isinstance(row, Mapping) for row in rows):
        return []
    return [row.get(key) for row in rows]


def _per_ticker_digests_valid(entries: Any) -> bool:
    return (
        isinstance(entries, list)
        and [entry.get("ticker") for entry in entries if isinstance(entry, Mapping)]
        == TARGET_UNIVERSE
        and all(
            isinstance(entry, Mapping)
            and entry.get("per_ticker_signal_or_feature_generation_candidate_digest")
            == per_ticker_signal_or_feature_generation_candidate_digest_v1(entry)
            for entry in entries
        )
    )


def _all_future_outputs_not_generated(candidate: Mapping[str, Any]) -> bool:
    rows = candidate.get("future_outputs")
    return (
        _ids(rows, "future_output_id") == FUTURE_OUTPUT_IDS
        and all(
            row.get("output_status") == "PLANNED_NOT_GENERATED"
            and row.get("generated") is False
            for row in rows
        )
    )


def _check_definitions(candidate: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    evidence = SOURCE_EVIDENCE_DIGESTS
    entries = candidate.get("per_ticker_candidate_entries", [])
    return [
        ("source_target_results_review_digest_bound", EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST, candidate.get("source_objective_label_or_target_generation_results_review_digest")),
        ("source_target_generation_execution_digest_bound", EXPECTED_SOURCE_EXECUTION_DIGEST, candidate.get("source_objective_label_or_target_generation_execution_digest")),
        ("source_target_output_binding_digest_bound", EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST, candidate.get("source_objective_label_or_target_generation_output_binding_digest")),
        ("source_target_values_digest_bound", EXPECTED_SOURCE_TARGET_VALUES_DIGEST, candidate.get("source_objective_label_or_target_values_digest")),
        ("source_target_approval_digest_bound", EXPECTED_SOURCE_APPROVAL_DIGEST, candidate.get("source_objective_label_or_target_generation_approval_digest")),
        ("source_candidate_review_digest_bound", evidence["marketflow_objective_label_or_target_generation_candidate_operator_review_digest"], candidate.get("marketflow_objective_label_or_target_generation_candidate_operator_review_digest")),
        ("source_candidate_digest_bound", evidence["marketflow_objective_label_or_target_generation_candidate_v1_digest"], candidate.get("marketflow_objective_label_or_target_generation_candidate_v1_digest")),
        ("source_design_results_review_digest_bound", evidence["marketflow_expectancy_objective_design_results_review_digest"], candidate.get("marketflow_expectancy_objective_design_results_review_digest")),
        ("source_design_execution_digest_bound", evidence["marketflow_expectancy_objective_design_execution_digest"], candidate.get("marketflow_expectancy_objective_design_execution_digest")),
        ("source_design_output_binding_digest_bound", evidence["expectancy_objective_design_output_binding_digest"], candidate.get("expectancy_objective_design_output_binding_digest")),
        ("source_expectancy_objective_approval_digest_bound", evidence["marketflow_expectancy_objective_approval_digest"], candidate.get("marketflow_expectancy_objective_approval_digest")),
        ("source_strategy_charter_approval_digest_bound", evidence["marketflow_algorithm_strategy_charter_approval_digest"], candidate.get("marketflow_algorithm_strategy_charter_approval_digest")),
        ("source_strategy_charter_digest_bound", evidence["marketflow_algorithm_strategy_charter_v1_digest"], candidate.get("marketflow_algorithm_strategy_charter_v1_digest")),
        ("source_final_archive_digest_bound", evidence["marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest"], candidate.get("marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest")),
        ("source_archive_digest_bound", evidence["predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest"], candidate.get("predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest")),
        ("source_selection_digest_bound", evidence["operator_method_or_closure_selection_using_improved_evidence_digest"], candidate.get("operator_method_or_closure_selection_using_improved_evidence_digest")),
        ("source_closure_digest_bound", evidence["predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest"], candidate.get("predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest")),
        ("source_readiness_digest_bound", evidence["predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest"], candidate.get("predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest")),
        ("source_reassessment_digest_bound", evidence["predictive_usefulness_reassessment_rerun_using_improved_evidence_digest"], candidate.get("predictive_usefulness_reassessment_rerun_using_improved_evidence_digest")),
        ("source_results_review_digest_bound", evidence["additional_predictive_evidence_results_review_using_improved_evidence_digest"], candidate.get("additional_predictive_evidence_results_review_using_improved_evidence_digest")),
        ("source_prior_execution_digest_bound", evidence["additional_predictive_evidence_execution_using_improved_evidence_digest"], candidate.get("additional_predictive_evidence_execution_using_improved_evidence_digest")),
        ("matrix_digest_bound", evidence["feature_label_matrix_digest"], candidate.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", evidence["feature_values_digest"], candidate.get("feature_values_digest")),
        ("label_values_digest_bound", evidence["redesigned_label_values_digest"], candidate.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", evidence["research_registry_approval_digest"], candidate.get("research_registry_approval_digest")),
        ("records_digest_bound", evidence["records_digest"], candidate.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, candidate.get("target_universe")),
        ("records_digest_preserved", evidence["records_digest"], candidate.get("records_digest")),
        ("meta_913_preserved", 913, candidate.get("meta_record_count")),
        ("target_results_review_ready_true", True, candidate.get("target_results_review_ready")),
        ("ready_for_signal_or_feature_candidate_true", True, candidate.get("ready_for_signal_or_feature_generation_candidate")),
        ("candidate_created_true", True, candidate.get("signal_or_feature_generation_candidate_created")),
        ("candidate_ready_true", True, candidate.get("signal_or_feature_generation_candidate_ready_for_operator_review")),
        ("candidate_scope_only", SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION, candidate.get("candidate_scope")),
        ("selected_label_target_package_preserved", PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET, candidate.get("selected_label_target_package")),
        ("selected_objective_path_preserved", EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT, candidate.get("selected_objective_path")),
        ("target_profile_count_15_preserved", 15, candidate.get("target_profile_count")),
        ("target_row_counts_preserved", [179190, 177090, 2100], [candidate.get("target_row_count"), candidate.get("available_target_row_count"), candidate.get("unavailable_target_row_count")]),
        ("candidate_philosophy_defined", True, all(bool(candidate.get(field)) for field in ("candidate_philosophy", "candidate_primary_question", "candidate_secondary_question", "candidate_boundary"))),
        ("signal_families_defined_10", SIGNAL_FAMILY_IDS, _ids(candidate.get("proposed_signal_families"), "signal_family_id")),
        ("feature_families_defined_10", FEATURE_FAMILY_IDS, _ids(candidate.get("proposed_feature_families"), "feature_family_id")),
        ("recommended_feature_package_defined", PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET, candidate.get("recommended_feature_package", {}).get("package_id")),
        ("supporting_feature_package_defined", PACKAGE_REGIME_CONTEXT_SIGNAL_SET, candidate.get("supporting_feature_package", {}).get("package_id")),
        ("feature_groups_defined_17", FEATURE_GROUP_IDS, _ids(candidate.get("proposed_feature_groups"), "feature_group_id")),
        ("no_peek_rules_defined_10", NO_PEEK_RULE_IDS, _ids(candidate.get("no_peek_and_target_separation_rules"), "rule_id")),
        ("quality_checks_defined_10", PLANNED_QUALITY_CHECK_IDS, _ids(candidate.get("planned_quality_checks"), "quality_check_id")),
        ("future_outputs_not_generated", True, _all_future_outputs_not_generated(candidate)),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("selection_created_false", False, candidate.get("selection_created")),
        ("approval_created_false", False, candidate.get("approval_created")),
        ("generation_created_false", False, candidate.get("generation_created")),
        ("signal_generation_authorized_false", False, candidate.get("signal_generation_authorized")),
        ("signal_generation_performed_false", False, candidate.get("signal_generation_performed")),
        ("feature_generation_authorized_false", False, candidate.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, candidate.get("feature_generation_performed")),
        ("feature_values_created_false", False, candidate.get("feature_values_created")),
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
        ("target_generation_execution_rerun_false", False, candidate.get("target_generation_execution_rerun_performed")),
        ("target_results_review_rerun_false", False, candidate.get("target_generation_results_review_rerun_performed")),
        ("raw_provider_payloads_not_committed", False, candidate.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, candidate.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, candidate.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, candidate.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        ("no_tracked_marketflow_files", True, candidate.get("no_tracked_marketflow_files")),
    ]


REQUIRED_CHECK_IDS = [row[0] for row in _check_definitions(_base_candidate())]


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    definitions = _check_definitions(candidate)
    if [row[0] for row in definitions] != REQUIRED_CHECK_IDS:
        raise MarketFlowSignalOrFeatureGenerationCandidateError(
            "internal checklist definition mismatch"
        )
    return [_check(*row) for row in definitions]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "signal_or_feature_generation_candidate_created": not failed,
        "signal_or_feature_generation_candidate_ready_for_operator_review": not failed,
        "recommended_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "signal_generation_performed": False,
        "feature_generation_performed": False,
        "feature_values_created": False,
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
    payload.pop("marketflow_signal_or_feature_generation_candidate_v1_digest", None)
    return payload


def marketflow_signal_or_feature_generation_candidate_v1_digest(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the complete candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_marketflow_signal_or_feature_generation_candidate_v1() -> dict:
    """Build the candidate offline without reading or generating runtime outputs."""
    candidate = _base_candidate()
    checklist = _checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(checklist)
    candidate["marketflow_signal_or_feature_generation_candidate_v1_digest"] = (
        marketflow_signal_or_feature_generation_candidate_v1_digest(candidate)
    )
    validate_marketflow_signal_or_feature_generation_candidate_v1(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowSignalOrFeatureGenerationCandidateError(
            f"{field} mismatch"
        )


def validate_marketflow_signal_or_feature_generation_candidate_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Validate the candidate content and every closed authority gate."""
    if not isinstance(candidate, dict):
        raise MarketFlowSignalOrFeatureGenerationCandidateError(
            "candidate must be a JSON object"
        )
    expected = _base_candidate()
    for field, value in expected.items():
        _expect(candidate.get(field), value, field)
    if not _per_ticker_digests_valid(candidate.get("per_ticker_candidate_entries")):
        raise MarketFlowSignalOrFeatureGenerationCandidateError(
            "per-ticker candidate digests mismatch"
        )
    expected_checklist = _checklist(candidate)
    _expect(candidate.get("candidate_checklist"), expected_checklist, "candidate checklist")
    if any(row.get("status") != PASS for row in expected_checklist):
        raise MarketFlowSignalOrFeatureGenerationCandidateError(
            "candidate checklist failed"
        )
    _expect(candidate.get("candidate_summary"), _summary(expected_checklist), "candidate summary")
    digest = candidate.get("marketflow_signal_or_feature_generation_candidate_v1_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowSignalOrFeatureGenerationCandidateError(
            "candidate digest missing"
        )
    _expect(
        digest,
        marketflow_signal_or_feature_generation_candidate_v1_digest(candidate),
        "candidate digest",
    )
    return {
        "status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_signal_or_feature_generation_candidate_v1_digest": digest,
        **{
            key: candidate["candidate_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_signal_or_feature_generation_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render a sanitized Markdown view of the validated candidate."""
    validation = validate_marketflow_signal_or_feature_generation_candidate_v1(
        candidate
    )
    sections = [
        ("Title", ["Signal or Feature Generation Candidate v1"]),
        ("Signal or Feature Generation Candidate v1", [f"Artifact/status/scope: {candidate['artifact_kind']} / {candidate['candidate_status']} / {candidate['candidate_scope']}.", f"Candidate digest: {validation['marketflow_signal_or_feature_generation_candidate_v1_digest']}."]),
        ("Source Target Results Review", [f"Review/execution/output-binding/target-values digests: {candidate['source_objective_label_or_target_generation_results_review_digest']} / {candidate['source_objective_label_or_target_generation_execution_digest']} / {candidate['source_objective_label_or_target_generation_output_binding_digest']} / {candidate['source_objective_label_or_target_values_digest']}."]),
        ("Bound Evidence", [f"Approval/candidate-review/candidate: {candidate['source_objective_label_or_target_generation_approval_digest']} / {candidate['marketflow_objective_label_or_target_generation_candidate_operator_review_digest']} / {candidate['marketflow_objective_label_or_target_generation_candidate_v1_digest']}.", f"Matrix/features/labels/records: {candidate['feature_label_matrix_digest']} / {candidate['feature_values_digest']} / {candidate['redesigned_label_values_digest']} / {candidate['records_digest']}."]),
        ("Dataset and Universe", [f"{candidate['dataset_name']} / {candidate['total_canonical_record_count']} records.", "Universe: " + ", ".join(candidate["target_universe"]) + ".", "META remains 913; every non-META ticker remains 1003."]),
        ("Candidate Basis", [f"Package/path: {candidate['selected_label_target_package']} / {candidate['selected_objective_path']}.", f"Profiles/rows/available/unavailable: {candidate['target_profile_count']} / {candidate['target_row_count']} / {candidate['available_target_row_count']} / {candidate['unavailable_target_row_count']}."]),
        ("Candidate Philosophy", [candidate["candidate_philosophy"], candidate["candidate_primary_question"], candidate["candidate_secondary_question"], candidate["candidate_boundary"]]),
        ("Proposed Signal Families", [f"{row['signal_family_id']}: {row['candidate_status']}." for row in candidate["proposed_signal_families"]]),
        ("Proposed Feature Families", [f"{row['feature_family_id']}: {row['candidate_status']}." for row in candidate["proposed_feature_families"]]),
        ("Recommended Feature Package", [f"{candidate['recommended_feature_package']['package_id']}: {candidate['recommended_feature_package']['status']}.", candidate["recommended_feature_package"]["rationale"]]),
        ("Supporting Feature Package", [f"{candidate['supporting_feature_package']['package_id']}: {candidate['supporting_feature_package']['status']}.", candidate["supporting_feature_package"]["rationale"]]),
        ("Feature Groups", [row["feature_group_id"] for row in candidate["proposed_feature_groups"]]),
        ("No-Peek and Target-Separation Rules", [row["rule_id"] for row in candidate["no_peek_and_target_separation_rules"]]),
        ("Planned Quality Checks", [row["quality_check_id"] for row in candidate["planned_quality_checks"]]),
        ("Future Outputs", [f"{row['future_output_id']}: {row['output_status']}." for row in candidate["future_outputs"]]),
        ("Per-Ticker Candidate Summary", [f"{row['ticker']}: records {row['historical_record_count']}, targets {row['target_row_count']}, digest {row['per_ticker_signal_or_feature_generation_candidate_digest']}." for row in candidate["per_ticker_candidate_entries"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: {candidate['candidate_summary']['total_checks']} / {candidate['candidate_summary']['passed_checks']} / {candidate['candidate_summary']['failed_checks']} / {candidate['candidate_summary']['blocker_count']}."]),
        ("Guardrails", [candidate["candidate_boundary"]]),
    ]
    lines = ["# Signal or Feature Generation Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_signal_or_feature_generation_candidate_v1(
    output_dir: str | Path,
) -> dict[str, Any]:
    """Write canonical candidate JSON once in an explicitly supplied directory."""
    candidate = build_marketflow_signal_or_feature_generation_candidate_v1()
    validation = validate_marketflow_signal_or_feature_generation_candidate_v1(
        candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_signal_or_feature_generation_candidate_v1.json"
    payload = canonical_json_bytes(candidate)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowSignalOrFeatureGenerationCandidateError(
            "signal or feature generation candidate output already exists"
        ) from exc
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "marketflow_signal_or_feature_generation_candidate_v1_digest": validation[
            "marketflow_signal_or_feature_generation_candidate_v1_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
