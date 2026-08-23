"""Offline research-only design execution for the approved expectancy objective."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import marketflow_expectancy_objective_approval_service as approval_service


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_V1 = (
    "marketflow_expectancy_objective_design_execution_v1"
)
MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED_RESEARCH_ONLY = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED_RESEARCH_ONLY"
)
EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_ONLY_NOT_LABEL_GENERATION = (
    "EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_ONLY_NOT_LABEL_GENERATION"
)
SELECTED_OBJECTIVE_PATH = (
    approval_service.SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT
)
DEFAULT_OUTPUT_ROOT = (
    Path(".marketflow") / "expectancy_objective_design" / "expanded_universe_v1"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "4ae9d4e81cc41b9578ac061574669d6fb11a45ed56871f4d05a02aacad165a1d"
)
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST = (
    approval_service.EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST
)

OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "EXPECTANCY_OBJECTIVE_DESIGN_RESEARCH_ONLY"
SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE = "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OUTPUT_FILENAMES = [
    "expectancy_objective_design_manifest.json",
    "objective_family_selection_report.json",
    "expectancy_payoff_objective_specification.json",
    "abstention_support_objective_specification.json",
    "material_move_objective_specification.json",
    "objective_label_generation_plan.json",
    "objective_validation_metric_plan.json",
    "objective_baseline_comparison_plan.json",
    "per_ticker_objective_review.json",
    "operator_summary.json",
    "expectancy_objective_design_digest_manifest.json",
]

OBJECTIVE_FAMILY_DESIGN_ROLES = {
    "OBJECTIVE_EXPECTANCY_POSITIVE_SETUP": "PRIMARY_EXPECTANCY_CORE",
    "OBJECTIVE_PAYOFF_ASYMMETRY_SETUP": "PRIMARY_PAYOFF_CORE",
    "OBJECTIVE_RISK_REWARD_FAVORABLE_SETUP": "PRIMARY_RISK_REWARD_SUPPORT",
    "OBJECTIVE_NO_TRADE_ABSTAIN_ZONE": "SUPPORTING_ABSTENTION_FILTER",
    "OBJECTIVE_TREND_CONTINUATION_SETUP": "SECONDARY_TREND_QUALITY",
    "OBJECTIVE_MATERIAL_MOVE_AFTER_COST": "SECONDARY_MATERIALITY_FILTER",
    "OBJECTIVE_DRAWDOWN_CONTAINED_SETUP": "SECONDARY_RISK_CONTAINMENT",
    "OBJECTIVE_RELATIVE_STRENGTH_LEADER_LAGGARD": "CONTEXTUAL_SELECTION",
    "OBJECTIVE_REGIME_CONDITIONED_OPPORTUNITY": "CONTEXTUAL_REGIME_FILTER",
    "OBJECTIVE_ABSORPTION_REVERSAL_SETUP": "CONTEXTUAL_SETUP_CLASS",
}
EXPECTANCY_PAYOFF_CANDIDATE_FIELDS = [
    "forward_return_after_cost_candidate",
    "maximum_adverse_excursion_candidate",
    "maximum_favorable_excursion_candidate",
    "reward_to_risk_candidate",
    "payoff_asymmetry_candidate",
    "expectancy_score_candidate",
    "setup_quality_score_candidate",
]
ABSTENTION_CANDIDATE_FIELDS = [
    "no_trade_zone_candidate",
    "low_expectancy_zone_candidate",
    "high_noise_zone_candidate",
    "insufficient_material_move_candidate",
    "insufficient_reward_to_risk_candidate",
    "excessive_drawdown_risk_candidate",
]
MATERIAL_MOVE_CANDIDATE_FIELDS = [
    "material_move_after_cost_candidate",
    "trend_continuation_candidate",
    "drawdown_contained_candidate",
    "volatility_adjusted_move_candidate",
    "time_to_move_candidate",
]
LABEL_GENERATION_PLANNED_STEPS = [
    "Define exact formula candidates.",
    "Define forward windows.",
    "Define cost/slippage assumptions.",
    "Define risk and drawdown fields.",
    "Define abstention/no-trade criteria.",
    "Define per-ticker availability rules.",
    "Define no-peek/chronological rules.",
    "Define validation metrics.",
    "Define baseline comparisons.",
    "Submit for separate label-generation candidate review.",
]
VALIDATION_METRICS = [
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
BASELINES = [
    "BASELINE_BUY_AND_HOLD",
    "BASELINE_MAJORITY_OR_NO_TRADE",
    "BASELINE_PREVIOUS_DIRECTION",
    "BASELINE_SIMPLE_TREND_FOLLOWING",
    "BASELINE_SIMPLE_VPA_WYCKOFF_RULE",
    "BASELINE_RELATIVE_STRENGTH_RANKING",
    "BASELINE_RANDOM_OR_SHUFFLED_CONTROL",
]
NEXT_CHAIN = [
    "Expectancy Objective Design Results Review v1.",
    "Future objective label/target generation candidate only after separate review.",
    "Future signal/feature planning only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "expectancy_objective_design_results_review",
    "objective_label_or_target_generation_candidate",
    "objective_label_or_target_generation_approval",
    "signal_or_feature_generation_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "design_execution_does_not_generate_labels",
    "design_execution_does_not_create_targets",
    "design_execution_does_not_generate_features",
    "design_execution_does_not_create_feature_label_matrix",
    "design_execution_does_not_run_backtest",
    "design_execution_does_not_train_models",
    "design_execution_does_not_compute_metrics",
    "design_execution_does_not_score_strategy",
    "design_execution_does_not_generate_trade_recommendations",
    "design_execution_does_not_accept_predictive_usefulness",
    "design_execution_does_not_accept_profitability",
    "design_execution_does_not_authorize_runtime",
    "design_execution_does_not_authorize_strategy",
    "design_execution_does_not_authorize_paper_trading",
    "design_execution_does_not_authorize_broker_execution",
    "design_execution_does_not_call_providers",
    "design_execution_does_not_acquire_market_data",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class MarketFlowExpectancyObjectiveDesignExecutionError(ValueError):
    """Raised when design execution violates its research-only boundary."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _source_attestation() -> dict:
    universe = [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]
    return approval_service.build_marketflow_expectancy_objective_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=approval_service.REQUIRED_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=EXPECTED_SOURCE_CANDIDATE_DIGEST,
        operator_confirms_strategy_charter_approval_digest=EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
        operator_confirms_records_digest="fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044",
        operator_confirms_target_universe=universe,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
        operator_confirms_selected_objective_path=SELECTED_OBJECTIVE_PATH,
        operator_confirms_approval_scope_only=True,
        operator_confirms_objective_selected=True,
        operator_confirms_objective_approved=True,
        operator_confirms_ready_for_design_execution=True,
        operator_confirms_no_objective_generation=True,
        operator_confirms_no_label_generation=True,
        operator_confirms_no_new_targets=True,
        operator_confirms_no_feature_generation=True,
        operator_confirms_no_feature_label_matrix=True,
        operator_confirms_no_backtest_execution=True,
        operator_confirms_no_model_training=True,
        operator_confirms_no_metric_computation=True,
        operator_confirms_no_strategy_scoring=True,
        operator_confirms_no_predictive_usefulness_acceptance=True,
        operator_confirms_no_profitability_acceptance=True,
        operator_confirms_no_runtime_migration_approval=True,
        operator_confirms_no_strategy_authorization=True,
        operator_confirms_no_paper_trading=True,
        operator_confirms_no_broker_execution=True,
        operator_confirms_no_trade_recommendations=True,
        operator_confirms_no_api_key_storage_or_printing=True,
        operator_confirms_no_raw_payload_commit=True,
    )


@lru_cache(maxsize=1)
def _source_approval() -> dict:
    source = approval_service.build_marketflow_expectancy_objective_approval_v1(
        operator_attestation=_source_attestation()
    )
    validation = approval_service.validate_marketflow_expectancy_objective_approval_v1(
        source
    )
    if (
        validation["marketflow_expectancy_objective_approval_digest"]
        != EXPECTED_SOURCE_APPROVAL_DIGEST
    ):
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "source expectancy objective approval digest mismatch"
        )
    return source


def _source_digest_chain(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: deepcopy(value)
        for key, value in source.items()
        if key.endswith("_digest") and isinstance(value, str)
    }


def _objective_family_selection_report() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "design_role": role,
            "design_status": "DESIGNED_RESEARCH_ONLY",
            "label_generation_authorized": False,
            "target_creation_authorized": False,
            "feature_generation_authorized": False,
            "metric_computation_authorized": False,
            "backtest_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for name, role in OBJECTIVE_FAMILY_DESIGN_ROLES.items()
    }


def _objective_specification(cluster: str, fields: list[str]) -> dict[str, Any]:
    return {
        "specification_status": "DESIGNED_RESEARCH_ONLY_NOT_GENERATED",
        "objective_cluster": cluster,
        "objective_path": SELECTED_OBJECTIVE_PATH,
        "future_candidate_fields": list(fields),
        "future_label_generation_authorized": False,
        "future_target_creation_authorized": False,
    }


def _label_generation_plan() -> dict[str, Any]:
    return {
        "plan_status": "PLANNED_NOT_EXECUTED",
        "label_generation_authorized": False,
        "target_creation_authorized": False,
        "requires_separate_candidate": True,
        "requires_operator_review": True,
        "requires_approval_before_generation": True,
        "planned_steps": list(LABEL_GENERATION_PLANNED_STEPS),
    }


def _validation_metric_plan() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "metric_status": "PLANNED_NOT_COMPUTED",
            "metric_computation_authorized": False,
        }
        for name in VALIDATION_METRICS
    }


def _baseline_comparison_plan() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "baseline_status": "PLANNED_NOT_EXECUTED",
            "backtest_authorized": False,
            "model_training_authorized": False,
            "metric_computation_authorized": False,
        }
        for name in BASELINES
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_objective_design_digest", None)
    return payload


def per_ticker_expectancy_objective_design_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker design entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_expectancy_objective_approval_entries"]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": is_meta,
            "expectancy_objective_approval_status": source["approval_status"],
            "expectancy_objective_design_status": "DESIGNED_RESEARCH_ONLY",
            "selected_objective_path": SELECTED_OBJECTIVE_PATH,
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
            "source_expectancy_objective_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
            "design_note": (
                "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_expectancy_objective_design_digest"] = (
            per_ticker_expectancy_objective_design_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _common_output_fields(artifact: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "run_timestamp_utc": artifact["run_timestamp_utc"],
        "dataset_name": artifact["dataset_name"],
        "records_digest": artifact["records_digest"],
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "expectancy_objective_design_executed": True,
        "expectancy_objective_design_results_created": True,
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
        "model_training_authorized": False,
        "metric_computation_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }


def _report_payloads(artifact: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    common = _common_output_fields(artifact)
    return {
        "objective_family_selection_report.json": {
            **common,
            "report_name": "objective_family_selection_report",
            "objective_families": deepcopy(artifact["objective_family_selection_report"]),
        },
        "expectancy_payoff_objective_specification.json": {
            **common,
            "report_name": "expectancy_payoff_objective_specification",
            **deepcopy(artifact["expectancy_payoff_objective_specification"]),
        },
        "abstention_support_objective_specification.json": {
            **common,
            "report_name": "abstention_support_objective_specification",
            **deepcopy(artifact["abstention_support_objective_specification"]),
        },
        "material_move_objective_specification.json": {
            **common,
            "report_name": "material_move_objective_specification",
            **deepcopy(artifact["material_move_objective_specification"]),
        },
        "objective_label_generation_plan.json": {
            **common,
            "report_name": "objective_label_generation_plan",
            **deepcopy(artifact["objective_label_generation_plan"]),
        },
        "objective_validation_metric_plan.json": {
            **common,
            "report_name": "objective_validation_metric_plan",
            "validation_metrics": deepcopy(artifact["objective_validation_metric_plan"]),
        },
        "objective_baseline_comparison_plan.json": {
            **common,
            "report_name": "objective_baseline_comparison_plan",
            "baselines": deepcopy(artifact["objective_baseline_comparison_plan"]),
        },
        "per_ticker_objective_review.json": {
            **common,
            "report_name": "per_ticker_objective_review",
            "target_universe": deepcopy(artifact["target_universe"]),
            "per_ticker_entries": deepcopy(artifact["per_ticker_objective_review"]),
        },
        "operator_summary.json": {
            **common,
            "report_name": "operator_summary",
            "execution_status": artifact["execution_status"],
            "execution_scope": artifact["execution_scope"],
            "generated_output_count": 11,
            "objective_family_count": 10,
            "validation_metric_count": 14,
            "baseline_count": 7,
            "per_ticker_entry_count": 12,
            "next_chain": deepcopy(artifact["next_chain"]),
            "next_gates": deepcopy(artifact["next_gates"]),
            "risk_controls": deepcopy(artifact["risk_controls"]),
        },
    }


def _output_binding_entries(artifact: Mapping[str, Any]) -> list[dict[str, str]]:
    payloads = _report_payloads(artifact)
    return [
        {"filename": name, "semantic_digest": semantic_digest(payloads[name])}
        for name in OUTPUT_FILENAMES
        if name in payloads
    ]


def expectancy_objective_design_output_binding_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    """Bind the nine non-manifest design reports without circular references."""
    return semantic_digest(
        {
            "output_binding_entries": _output_binding_entries(artifact),
            "generated_output_names": OUTPUT_FILENAMES,
            "digest_manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        }
    )


def _base_artifact(
    source: Mapping[str, Any],
    *,
    run_timestamp_utc: str,
    output_root: Path,
) -> dict[str, Any]:
    artifact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_V1,
        "execution_status": MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED_RESEARCH_ONLY,
        "execution_scope": EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_ONLY_NOT_LABEL_GENERATION,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "approved_primary_objective_cluster": source["approved_primary_objective_cluster"],
        "approved_supporting_objective_cluster": source["approved_supporting_objective_cluster"],
        "approved_secondary_objective_cluster": source["approved_secondary_objective_cluster"],
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "run_timestamp_utc": run_timestamp_utc,
        "generated_output_root": _path_text(output_root),
        "source_expectancy_objective_approval_artifact_kind": source["artifact_kind"],
        "source_expectancy_objective_approval_status": source["approval_status"],
        "source_expectancy_objective_approval_scope": source["approval_scope"],
        "source_expectancy_objective_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_expectancy_objective_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_expectancy_objective_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_strategy_charter_approval_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
        **_source_digest_chain(source),
    }
    artifact.update(
        {
            "expectancy_objective_selected": True,
            "expectancy_objective_approved": True,
            "expectancy_objective_authorized": True,
            "ready_for_expectancy_objective_design_execution": True,
            "expectancy_objective_design_execution_authorized": True,
            "expectancy_objective_design_executed": True,
            "expectancy_objective_design_results_created": True,
            "future_objective_design_outputs_created": True,
            "expectancy_objective_generation_authorized": False,
            "expectancy_objective_generation_performed": False,
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
            "metric_computation_authorized": False,
            "metric_computation_performed": False,
            "strategy_scoring_performed": False,
            "generated_output_count": 11,
            "generated_output_names": list(OUTPUT_FILENAMES),
            "output_digest_manifest_created": True,
            "digest_manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
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
            "provider_requests_made_in_execution": False,
            "live_provider_transport_enabled_in_execution": False,
            "market_data_acquisition_performed_in_execution": False,
            "dataset_generation_performed_in_execution": False,
            "canonical_dataset_regenerated_in_execution": False,
            "raw_provider_payloads_committed": False,
            "api_keys_stored_or_printed": False,
        }
    )
    copied_fields = [
        "dataset_name", "source_profile", "timeframe", "date_range_start",
        "date_range_end", "target_universe", "target_universe_count",
        "total_canonical_record_count", "per_ticker_record_counts",
        "records_digest", "meta_record_count", "non_meta_record_count",
        "meta_reduced_record_count_preserved", "strategy_direction",
        "marketflow_algorithm_identity", "core_philosophy",
    ]
    artifact.update({field: deepcopy(source[field]) for field in copied_fields})
    artifact.update(
        {
            "objective_design_philosophy": "Translate the approved expectancy/payoff objective path into research-only design specifications before any label or target generation.",
            "objective_design_primary_goal": "Define how future labels or targets may represent positive expectancy after risk, costs, drawdown, payoff asymmetry, and abstention constraints.",
            "objective_design_boundary": "Design-only. No labels, targets, features, matrix rows, metrics, models, backtests, signals, recommendations, or runtime artifacts are generated.",
            "objective_family_selection_report": _objective_family_selection_report(),
            "expectancy_payoff_objective_specification": _objective_specification(
                "CLUSTER_EXPECTANCY_AND_PAYOFF", EXPECTANCY_PAYOFF_CANDIDATE_FIELDS
            ),
            "abstention_support_objective_specification": _objective_specification(
                "CLUSTER_ABSTENTION_AND_NO_TRADE", ABSTENTION_CANDIDATE_FIELDS
            ),
            "material_move_objective_specification": _objective_specification(
                "CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE", MATERIAL_MOVE_CANDIDATE_FIELDS
            ),
            "objective_label_generation_plan": _label_generation_plan(),
            "objective_validation_metric_plan": _validation_metric_plan(),
            "objective_baseline_comparison_plan": _baseline_comparison_plan(),
            "per_ticker_objective_review": _per_ticker_entries(source),
            "next_chain": list(NEXT_CHAIN),
            "next_gates": list(NEXT_GATES),
            "risk_controls": list(RISK_CONTROLS),
            "no_tracked_marketflow_files": True,
        }
    )
    return artifact


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
        and isinstance(entry.get("per_ticker_expectancy_objective_design_digest"), str)
        and entry["per_ticker_expectancy_objective_design_digest"]
        == per_ticker_expectancy_objective_design_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(artifact: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    source = _source_approval()
    entries = artifact.get("per_ticker_objective_review", [])
    return [
        ("source_expectancy_objective_approval_digest_bound", EXPECTED_SOURCE_APPROVAL_DIGEST, artifact.get("source_expectancy_objective_approval_digest")),
        ("source_candidate_review_digest_bound", EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST, artifact.get("source_expectancy_objective_candidate_review_digest")),
        ("source_candidate_digest_bound", EXPECTED_SOURCE_CANDIDATE_DIGEST, artifact.get("source_expectancy_objective_candidate_digest")),
        ("source_strategy_charter_approval_digest_bound", EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST, artifact.get("source_strategy_charter_approval_digest")),
        ("source_strategy_charter_digest_bound", source["source_strategy_charter_digest"], artifact.get("source_strategy_charter_digest")),
        ("source_final_archive_digest_bound", source["source_final_archive_digest"], artifact.get("source_final_archive_digest")),
        ("source_archive_digest_bound", source["source_archive_digest"], artifact.get("source_archive_digest")),
        ("source_selection_digest_bound", source["source_selection_digest"], artifact.get("source_selection_digest")),
        ("source_closure_digest_bound", source["source_closure_digest"], artifact.get("source_closure_digest")),
        ("source_readiness_digest_bound", source["source_readiness_digest"], artifact.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", source["source_reassessment_digest"], artifact.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", source["source_results_review_digest"], artifact.get("source_results_review_digest")),
        ("source_execution_digest_bound", source["source_execution_digest"], artifact.get("source_execution_digest")),
        ("matrix_digest_bound", source["feature_label_matrix_digest"], artifact.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", source["feature_values_digest"], artifact.get("feature_values_digest")),
        ("label_values_digest_bound", source["redesigned_label_values_digest"], artifact.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", source["research_registry_approval_digest"], artifact.get("research_registry_approval_digest")),
        ("records_digest_bound", source["records_digest"], artifact.get("records_digest")),
        ("target_universe_12_preserved", source["target_universe"], artifact.get("target_universe")),
        ("records_digest_preserved", source["records_digest"], artifact.get("records_digest")),
        ("meta_913_preserved", 913, artifact.get("meta_record_count")),
        ("objective_selected_true", True, artifact.get("expectancy_objective_selected")),
        ("objective_approved_true", True, artifact.get("expectancy_objective_approved")),
        ("ready_for_design_execution_true", True, artifact.get("ready_for_expectancy_objective_design_execution")),
        ("design_execution_authorized_true", True, artifact.get("expectancy_objective_design_execution_authorized")),
        ("design_executed_true", True, artifact.get("expectancy_objective_design_executed")),
        ("design_results_created_true", True, artifact.get("expectancy_objective_design_results_created")),
        ("generated_output_count_11", 11, artifact.get("generated_output_count")),
        ("selected_objective_path_preserved", SELECTED_OBJECTIVE_PATH, artifact.get("selected_objective_path")),
        ("objective_family_selection_report_created", 10, len(artifact.get("objective_family_selection_report", {}))),
        ("expectancy_payoff_spec_created", True, bool(artifact.get("expectancy_payoff_objective_specification"))),
        ("abstention_support_spec_created", True, bool(artifact.get("abstention_support_objective_specification"))),
        ("material_move_spec_created", True, bool(artifact.get("material_move_objective_specification"))),
        ("label_generation_plan_created_without_generation", "PLANNED_NOT_EXECUTED", artifact.get("objective_label_generation_plan", {}).get("plan_status")),
        ("validation_metric_plan_created_without_computation", 14, len(artifact.get("objective_validation_metric_plan", {}))),
        ("baseline_comparison_plan_created_without_execution", 7, len(artifact.get("objective_baseline_comparison_plan", {}))),
        ("per_ticker_objective_review_created", 12, len(entries) if isinstance(entries, list) else 0),
        ("output_digest_manifest_created", True, artifact.get("output_digest_manifest_created")),
        ("label_generation_authorized_false", False, artifact.get("label_generation_authorized")),
        ("label_generation_performed_false", False, artifact.get("label_generation_performed")),
        ("new_targets_created_false", False, artifact.get("new_targets_created")),
        ("target_definition_change_authorized_false", False, artifact.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, artifact.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, artifact.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, artifact.get("feature_label_matrix_created")),
        ("backtest_execution_authorized_false", False, artifact.get("backtest_execution_authorized")),
        ("backtest_execution_performed_false", False, artifact.get("backtest_execution_performed")),
        ("model_training_authorized_false", False, artifact.get("model_training_authorized")),
        ("model_training_performed_false", False, artifact.get("model_training_performed")),
        ("metric_computation_authorized_false", False, artifact.get("metric_computation_authorized")),
        ("metric_computation_performed_false", False, artifact.get("metric_computation_performed")),
        ("strategy_scoring_false", False, artifact.get("strategy_scoring_performed")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        ("profitability_not_accepted", NOT_ACCEPTED, artifact.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, artifact.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, artifact.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, artifact.get("broker_execution")),
        ("trade_recommendations_false", False, artifact.get("trade_recommendations_generated")),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("provider_requests_made_false", False, artifact.get("provider_requests_made_in_execution")),
        ("market_data_acquisition_false", False, artifact.get("market_data_acquisition_performed_in_execution")),
        ("dataset_regeneration_false", False, artifact.get("canonical_dataset_regenerated_in_execution")),
        ("raw_provider_payloads_not_committed", False, artifact.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, artifact.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, artifact.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, artifact.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, artifact.get("risk_controls")),
        ("no_tracked_marketflow_files", True, artifact.get("no_tracked_marketflow_files")),
    ]


def _checklist(artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(*definition) for definition in _check_definitions(artifact)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = sum(row.get("status") != PASS for row in rows)
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - failed,
        "failed_checks": failed,
        "blocker_count": sum(
            row.get("status") != PASS and row.get("severity") == BLOCKER
            for row in rows
        ),
        "expectancy_objective_design_executed": True,
        "expectancy_objective_design_results_created": True,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "generated_output_count": 11,
        "label_generation_performed": False,
        "new_targets_created": False,
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


def _digest_payload(artifact: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(artifact))
    payload.pop("execution_checklist", None)
    payload.pop("execution_summary", None)
    payload.pop("marketflow_expectancy_objective_design_execution_digest", None)
    payload.pop("generated_output_root", None)
    return payload


def marketflow_expectancy_objective_design_execution_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the execution artifact."""
    return semantic_digest(_digest_payload(artifact))


def _build_artifact(*, run_timestamp_utc: str, output_root: Path) -> dict[str, Any]:
    source = _source_approval()
    artifact = _base_artifact(
        source,
        run_timestamp_utc=run_timestamp_utc,
        output_root=output_root,
    )
    artifact["expectancy_objective_design_output_binding_digest"] = (
        expectancy_objective_design_output_binding_digest_v1(artifact)
    )
    checklist = _checklist(artifact)
    artifact["execution_checklist"] = checklist
    artifact["execution_summary"] = _summary(checklist)
    artifact["marketflow_expectancy_objective_design_execution_digest"] = (
        marketflow_expectancy_objective_design_execution_digest_v1(artifact)
    )
    validate_marketflow_expectancy_objective_design_execution_v1(artifact)
    return artifact


def _write_json_once(path: Path, payload: dict[str, Any]) -> str:
    data = canonical_json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            f"expectancy objective design output already exists: {path.name}"
        ) from exc
    return sha256_bytes(data)


def execute_marketflow_expectancy_objective_design_v1(
    *,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Create exactly 11 research-only design outputs without provider access."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "run_timestamp_utc required"
        )
    if root.exists() and any(root.iterdir()):
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "expectancy objective design output root is not empty"
        )
    artifact = _build_artifact(run_timestamp_utc=timestamp, output_root=root)
    report_payloads = _report_payloads(artifact)
    payloads = {
        "expectancy_objective_design_manifest.json": artifact,
        **report_payloads,
    }
    file_digests = {
        filename: _write_json_once(root / filename, payloads[filename])
        for filename in OUTPUT_FILENAMES
        if filename != "expectancy_objective_design_digest_manifest.json"
    }
    digest_entries = [
        (
            {
                "filename": filename,
                "digest_kind": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
                "sha256": None,
            }
            if filename == "expectancy_objective_design_digest_manifest.json"
            else {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": file_digests[filename],
            }
        )
        for filename in OUTPUT_FILENAMES
    ]
    digest_manifest = {
        **_common_output_fields(artifact),
        "report_name": "expectancy_objective_design_digest_manifest",
        "generated_output_count": 11,
        "output_digest_entries": digest_entries,
        "all_non_self_output_digests_present": True,
        "self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "marketflow_expectancy_objective_design_execution_digest": artifact[
            "marketflow_expectancy_objective_design_execution_digest"
        ],
        "expectancy_objective_design_output_binding_digest": artifact[
            "expectancy_objective_design_output_binding_digest"
        ],
    }
    _write_json_once(
        root / "expectancy_objective_design_digest_manifest.json",
        digest_manifest,
    )
    return artifact


def validate_marketflow_expectancy_objective_design_execution_v1(
    artifact: dict,
) -> dict:
    """Validate source bindings, design catalogs, digests, and closed authorities."""
    if not isinstance(artifact, dict):
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "design execution artifact must be an object"
        )
    timestamp = artifact.get("run_timestamp_utc")
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "run_timestamp_utc required"
        )
    root = Path(str(artifact.get("generated_output_root", DEFAULT_OUTPUT_ROOT)))
    expected = _base_artifact(
        _source_approval(),
        run_timestamp_utc=timestamp,
        output_root=root,
    )
    for field, value in expected.items():
        if artifact.get(field) != value:
            raise MarketFlowExpectancyObjectiveDesignExecutionError(
                f"{field} mismatch"
            )
    binding = artifact.get("expectancy_objective_design_output_binding_digest")
    if not isinstance(binding, str) or len(binding) != 64:
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "output binding digest missing"
        )
    if binding != expectancy_objective_design_output_binding_digest_v1(artifact):
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "output binding digest mismatch"
        )
    expected_checklist = _checklist(artifact)
    if artifact.get("execution_checklist") != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "execution checklist mismatch"
        )
    if artifact.get("execution_summary") != _summary(expected_checklist):
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "execution summary mismatch"
        )
    digest = artifact.get("marketflow_expectancy_objective_design_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "execution digest missing"
        )
    if digest != marketflow_expectancy_objective_design_execution_digest_v1(artifact):
        raise MarketFlowExpectancyObjectiveDesignExecutionError(
            "execution digest mismatch"
        )
    return {
        "status": "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_VALID",
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "execution_scope": artifact["execution_scope"],
        "selected_objective_path": artifact["selected_objective_path"],
        "marketflow_expectancy_objective_design_execution_digest": digest,
        "expectancy_objective_design_output_binding_digest": binding,
        **{
            key: artifact["execution_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_expectancy_objective_design_execution_markdown_v1(
    artifact: dict,
) -> str:
    """Render a sanitized Markdown view of the validated design execution."""
    validation = validate_marketflow_expectancy_objective_design_execution_v1(
        artifact
    )
    sections = [
        ("Title", ["Expectancy Objective Design Execution v1"]),
        ("Expectancy Objective Design Execution v1", [
            "Artifact/status/scope: "
            f"{artifact['artifact_kind']} / {artifact['execution_status']} / "
            f"{artifact['execution_scope']}.",
            "Execution/output-binding digests: "
            f"{validation['marketflow_expectancy_objective_design_execution_digest']} / "
            f"{validation['expectancy_objective_design_output_binding_digest']}.",
        ]),
        ("Source Expectancy Objective Approval", [
            "Artifact/status/scope: "
            f"{artifact['source_expectancy_objective_approval_artifact_kind']} / "
            f"{artifact['source_expectancy_objective_approval_status']} / "
            f"{artifact['source_expectancy_objective_approval_scope']}.",
            f"Digest: {artifact['source_expectancy_objective_approval_digest']}.",
        ]),
        ("Bound Evidence", [
            "Review/candidate/charter approval: "
            f"{artifact['source_expectancy_objective_candidate_review_digest']} / "
            f"{artifact['source_expectancy_objective_candidate_digest']} / "
            f"{artifact['source_strategy_charter_approval_digest']}.",
            "Matrix/features/labels/records: "
            f"{artifact['feature_label_matrix_digest']} / "
            f"{artifact['feature_values_digest']} / "
            f"{artifact['redesigned_label_values_digest']} / "
            f"{artifact['records_digest']}.",
        ]),
        ("Dataset and Universe", [
            f"Dataset/records: {artifact['dataset_name']} / "
            f"{artifact['total_canonical_record_count']}.",
            "Universe: " + ", ".join(artifact["target_universe"]) + ".",
            "META remains 913; every non-META ticker remains 1003.",
        ]),
        ("Execution Scope", [artifact["execution_scope"]]),
        ("Selected Objective Path", [artifact["selected_objective_path"]]),
        ("Design Philosophy", [
            artifact["objective_design_philosophy"],
            artifact["objective_design_primary_goal"],
            artifact["objective_design_boundary"],
        ]),
        ("Objective Family Selection Report", [
            f"{name}: {value['design_role']} / {value['design_status']}."
            for name, value in artifact["objective_family_selection_report"].items()
        ]),
        ("Expectancy Payoff Objective Specification", [
            ", ".join(artifact["expectancy_payoff_objective_specification"]["future_candidate_fields"])
        ]),
        ("Abstention Support Objective Specification", [
            ", ".join(artifact["abstention_support_objective_specification"]["future_candidate_fields"])
        ]),
        ("Material Move Objective Specification", [
            ", ".join(artifact["material_move_objective_specification"]["future_candidate_fields"])
        ]),
        ("Objective Label Generation Plan", artifact["objective_label_generation_plan"]["planned_steps"]),
        ("Validation Metric Plan", list(artifact["objective_validation_metric_plan"])),
        ("Baseline Comparison Plan", list(artifact["objective_baseline_comparison_plan"])),
        ("Per-Ticker Objective Review", [
            f"{row['ticker']}: {row['expectancy_objective_design_status']}, "
            f"records {row['historical_record_count']}, "
            f"digest {row['per_ticker_expectancy_objective_design_digest']}."
            for row in artifact["per_ticker_objective_review"]
        ]),
        ("Output Digest Manifest", [
            f"{len(OUTPUT_FILENAMES)} outputs; self-reference policy "
            f"{SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE}."
        ]),
        ("Next Chain", artifact["next_chain"]),
        ("Next Gates", artifact["next_gates"]),
        ("Risk Controls", artifact["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", [
            "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."
        ]),
        ("Checklist Summary", [
            "Total/passed/failed/blockers: "
            f"{artifact['execution_summary']['total_checks']} / "
            f"{artifact['execution_summary']['passed_checks']} / "
            f"{artifact['execution_summary']['failed_checks']} / "
            f"{artifact['execution_summary']['blocker_count']}."
        ]),
        ("Guardrails", [artifact["objective_design_boundary"]]),
    ]
    lines = ["# Expectancy Objective Design Execution v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
