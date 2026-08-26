"""Offline streaming execution of the approved transparent VPA/Wyckoff baseline."""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import (
    marketflow_vpa_wyckoff_rule_baseline_approval_service as approval_service,
)


ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED"
)
ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_BLOCKED = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_V1 = (
    "marketflow_vpa_wyckoff_rule_baseline_execution_v1"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_BLOCKED_MISSING_OR_INVALID_MATRIX_SOURCE = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_BLOCKED_MISSING_OR_INVALID_MATRIX_SOURCE"
)
VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING = (
    "VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_VALID = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_VALID"
)

PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE = (
    approval_service.SELECTED_VPA_WYCKOFF_PACKAGE
)
PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT = (
    approval_service.SUPPORTING_VPA_WYCKOFF_PACKAGE
)
PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX = (
    approval_service.SELECTED_MATRIX_PACKAGE
)
MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE = (
    approval_service.SELECTED_MATRIX_LAYOUT
)
PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET = approval_service.SELECTED_FEATURE_PACKAGE
PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET = (
    approval_service.SELECTED_LABEL_TARGET_PACKAGE
)
EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT = approval_service.SELECTED_OBJECTIVE_PATH

OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "VPA_WYCKOFF_RULE_BASELINE_RESEARCH_ONLY"
RULE_THRESHOLD_POLICY = "STATIC_TRANSPARENT_BASELINE_NOT_OPTIMIZED"
SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE = "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "e8807862a69b4f688becfc2abec3ffade7e1cbb86a884abfc08ac2488db8ed1d"
)
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST = (
    approval_service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST = (
    approval_service.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST
)
EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST = (
    approval_service.review_service.candidate_service.EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST
)
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = approval_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_FEATURE_VALUES_DIGEST = approval_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = approval_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = approval_service.EXPECTED_SOURCE_RECORDS_DIGEST

TARGET_UNIVERSE = list(approval_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = {
    ticker: (913 if ticker == "META" else 1003) for ticker in TARGET_UNIVERSE
}
EXPECTED_SOURCE_MATRIX_ROW_COUNT = 179190
EXPECTED_RULE_VALUE_ROW_COUNT = 179190
EXPECTED_STATE_VALUE_ROW_COUNT = 179190
EXPECTED_RULE_FAMILY_REFERENCE_COUNT = 1433520
EXPECTED_STATE_FAMILY_REFERENCE_COUNT = 1075140
EXPECTED_OUTPUT_COUNT = 10

SELECTED_RULE_FAMILY_IDS = list(approval_service.SELECTED_RULE_FAMILY_IDS)
SUPPORTING_RULE_FAMILY_IDS = list(approval_service.SUPPORTING_RULE_FAMILY_IDS)
SELECTED_STATE_FAMILY_IDS = list(approval_service.SELECTED_STATE_FAMILY_IDS)
SUPPORTING_STATE_FAMILY_IDS = list(approval_service.SUPPORTING_STATE_FAMILY_IDS)

APPROVED_FEATURE_GROUPS = [
    "GROUP_VOLUME_CHANGE_AND_ZSCORE",
    "GROUP_SPREAD_VOLUME_INTERACTION",
    "GROUP_EFFORT_RESULT_DIVERGENCE",
    "GROUP_CLOSE_LOCATION_VALUE",
    "GROUP_INTRADAY_RANGE_AND_BODY",
    "GROUP_MOVING_AVERAGE_SLOPE",
    "GROUP_RELATIVE_STRENGTH_VS_UNIVERSE",
    "GROUP_RELATIVE_STRENGTH_RANK",
    "GROUP_ATR_AND_VOLATILITY_COMPRESSION",
    "GROUP_ABSTENTION_NOISE_CONTEXT",
    "GROUP_DATA_AVAILABILITY_FLAGS",
    "GROUP_META_LIMITATION_FLAGS",
    "GROUP_CLOSE_TO_CLOSE_RETURNS",
]

RULE_THRESHOLDS = {
    "volume_zscore_meaningful_effort": "1.0",
    "volume_zscore_low_effort": "-0.5",
    "close_location_demand_threshold": "0.65",
    "close_location_supply_threshold": "0.35",
    "relative_strength_percentile_leadership": "0.70",
    "relative_strength_percentile_weakness": "0.30",
    "volatility_compression_threshold": "0.80",
    "volatility_expansion_threshold": "1.20",
    "noise_to_trend_high_threshold": "2.0",
    "moving_average_slope_positive_threshold": "0.0",
    "moving_average_slope_negative_threshold": "0.0",
    "spread_volume_interaction_high_threshold": "1.0",
    "effort_result_divergence_threshold": "1.5",
}

DEFAULT_SOURCE_MATRIX_PATH = Path(
    ".marketflow/feature_label_matrix/expanded_universe_v1/matrix_rows.jsonl"
)
DEFAULT_OUTPUT_ROOT = Path(
    ".marketflow/vpa_wyckoff_rule_baseline/expanded_universe_v1"
)
OUTPUT_FILENAMES = [
    "vpa_wyckoff_baseline_manifest.json",
    "vpa_wyckoff_rule_schema.json",
    "vpa_wyckoff_state_schema.json",
    "vpa_wyckoff_rule_values.jsonl",
    "vpa_wyckoff_rule_coverage_report.json",
    "vpa_wyckoff_per_ticker_report.json",
    "vpa_wyckoff_meta_limitation_report.json",
    "vpa_wyckoff_no_peek_report.json",
    "vpa_wyckoff_operator_summary.json",
    "vpa_wyckoff_digest_manifest.json",
]

RULE_OUTPUT_ROW_FIELDS = [
    "dataset_name",
    "ticker",
    "date",
    "source_profile",
    "timeframe",
    "canonical_record_index",
    "target_family",
    "target_horizon_sessions",
    "target_profile",
    "target_available",
    "target_unavailable_reason",
    "selected_vpa_wyckoff_package",
    "selected_matrix_package",
    "selected_matrix_layout",
    "selected_feature_package",
    "selected_label_target_package",
    "selected_objective_path",
    "rule_family_count",
    "state_family_count",
    "rule_values",
    "state_values",
    "rule_values_available",
    "state_values_available",
    "rule_unavailable_reason",
    "state_unavailable_reason",
    "source_matrix_rows_digest",
    "source_matrix_approval_digest",
    "records_digest",
    "research_only",
    "non_actionable",
]
FORBIDDEN_RULE_OUTPUT_FIELDS = {
    "target_value",
    "target_class",
    "forward_return",
    "future_label_value",
    "prediction",
    "strategy_score",
    "trade_recommendation",
    "broker_order",
    "order_id",
    "provider_payload",
    "raw_provider_payload",
    "api_key",
}

NEXT_CHAIN = [
    "VPA/Wyckoff Rule Baseline Results Review v1.",
    "Expectancy Backtest Lab Candidate only after separate approval.",
    "Results review and readiness gates before predictive-usefulness acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "vpa_wyckoff_rule_baseline_results_review",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "execution_creates_only_research_vpa_wyckoff_rule_values",
    "execution_does_not_create_backtest_results",
    "execution_does_not_train_models",
    "execution_does_not_compute_performance_metrics",
    "execution_does_not_score_strategy",
    "execution_does_not_generate_trade_recommendations",
    "execution_does_not_accept_predictive_usefulness",
    "execution_does_not_accept_profitability",
    "execution_does_not_authorize_runtime",
    "execution_does_not_authorize_strategy",
    "execution_does_not_authorize_paper_trading",
    "execution_does_not_authorize_broker_execution",
    "execution_does_not_call_providers",
    "execution_does_not_acquire_market_data",
    "execution_does_not_rerun_feature_label_matrix_execution",
    "execution_does_not_rerun_feature_label_matrix_results_review",
    "execution_does_not_rerun_vpa_wyckoff_candidate_creation",
    "execution_does_not_rerun_vpa_wyckoff_candidate_review",
    "execution_does_not_rerun_vpa_wyckoff_approval",
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


class MarketFlowVpaWyckoffRuleBaselineExecutionError(ValueError):
    """Raised when matrix evidence or execution output violates the contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _decimal(value: Any) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _feature_value(row: Mapping[str, Any], group: str, field: str) -> Any:
    bundle = row.get("feature_bundle")
    if not isinstance(bundle, Mapping):
        return None
    group_row = bundle.get(group)
    if not isinstance(group_row, Mapping):
        return None
    values = group_row.get("feature_values")
    return values.get(field) if isinstance(values, Mapping) else None


def _rule(tag: str, available: bool) -> dict[str, Any]:
    return {"tag": tag if available else "unavailable", "available": available}


def _state(value: bool | None) -> dict[str, Any]:
    return {"value": value, "available": value is not None}


def _evaluate_rules(row: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    volume = _decimal(
        _feature_value(row, "GROUP_VOLUME_CHANGE_AND_ZSCORE", "volume_zscore_20")
    )
    trailing_1 = _decimal(
        _feature_value(row, "GROUP_CLOSE_TO_CLOSE_RETURNS", "trailing_return_1")
    )
    trailing_5 = _decimal(
        _feature_value(row, "GROUP_CLOSE_TO_CLOSE_RETURNS", "trailing_return_5")
    )
    interaction = _decimal(
        _feature_value(
            row, "GROUP_SPREAD_VOLUME_INTERACTION", "spread_volume_interaction"
        )
    )
    effort_ratio = _decimal(
        _feature_value(row, "GROUP_EFFORT_RESULT_DIVERGENCE", "effort_result_ratio")
    )
    close_location = _decimal(
        _feature_value(row, "GROUP_CLOSE_LOCATION_VALUE", "close_location_value")
    )
    slope = _decimal(
        _feature_value(row, "GROUP_MOVING_AVERAGE_SLOPE", "sma_20_slope_10")
    )
    relative_strength = _decimal(
        _feature_value(
            row, "GROUP_RELATIVE_STRENGTH_RANK", "relative_strength_percentile_20"
        )
    )
    compression = _decimal(
        _feature_value(
            row,
            "GROUP_ATR_AND_VOLATILITY_COMPRESSION",
            "volatility_compression_ratio",
        )
    )
    noise = _decimal(
        _feature_value(
            row, "GROUP_ABSTENTION_NOISE_CONTEXT", "noise_to_trend_ratio_20"
        )
    )
    abstention_flag = _feature_value(
        row, "GROUP_ABSTENTION_NOISE_CONTEXT", "abstention_noise_flag"
    )

    if volume is None or trailing_1 is None:
        volume_rule = _rule("unavailable", False)
    elif volume >= Decimal("1.0") and trailing_1 > 0:
        volume_rule = _rule("bullish_effort_confirmed", True)
    elif volume >= Decimal("1.0") and trailing_1 < 0:
        volume_rule = _rule("bearish_effort_confirmed", True)
    elif volume <= Decimal("-0.5"):
        volume_rule = _rule("low_effort", True)
    else:
        volume_rule = _rule("neutral_effort", True)

    if interaction is None or effort_ratio is None or volume is None:
        effort_rule = _rule("unavailable", False)
    elif volume >= Decimal("1.0") and effort_ratio >= Decimal("1.5"):
        effort_rule = _rule("effort_without_result", True)
    elif interaction > 0 and effort_ratio < Decimal("1.5"):
        effort_rule = _rule("efficient_effort_result", True)
    else:
        effort_rule = _rule("neutral", True)

    if close_location is None:
        close_rule = _rule("unavailable", False)
    elif close_location >= Decimal("0.65"):
        close_rule = _rule("demand_pressure", True)
    elif close_location <= Decimal("0.35"):
        close_rule = _rule("supply_pressure", True)
    else:
        close_rule = _rule("neutral_close", True)

    if trailing_5 is None or volume is None or close_location is None:
        breakout_rule = _rule("unavailable", False)
    elif trailing_5 > 0 and volume >= Decimal("1.0") and close_location >= Decimal("0.65"):
        breakout_rule = _rule("breakout_effort_candidate", True)
    else:
        breakout_rule = _rule("weak_breakout_or_no_confirmation", True)

    if trailing_5 is None or slope is None or noise is None:
        pullback_rule = _rule("unavailable", False)
    elif trailing_5 < 0 and slope > 0 and noise <= Decimal("2.0"):
        pullback_rule = _rule("constructive_pullback_candidate", True)
    else:
        pullback_rule = _rule("weak_pullback_or_decline", True)

    if relative_strength is None:
        relative_strength_rule = _rule("unavailable", False)
    elif relative_strength >= Decimal("0.70"):
        relative_strength_rule = _rule("leadership_confirmed", True)
    elif relative_strength <= Decimal("0.30"):
        relative_strength_rule = _rule("weakness_confirmed", True)
    else:
        relative_strength_rule = _rule("neutral_relative_strength", True)

    if compression is None:
        volatility_rule = _rule("unavailable", False)
    elif compression <= Decimal("0.80"):
        volatility_rule = _rule("compression_context", True)
    elif compression >= Decimal("1.20"):
        volatility_rule = _rule("expansion_context", True)
    else:
        volatility_rule = _rule("normal_volatility_context", True)

    if noise is None or not isinstance(abstention_flag, bool):
        noise_rule = _rule("unavailable", False)
    elif abstention_flag or noise >= Decimal("2.0"):
        noise_rule = _rule("abstain_noise_high", True)
    else:
        noise_rule = _rule("tradable_noise_acceptable", True)

    return {
        "VPA_RULE_VOLUME_CONFIRMATION": volume_rule,
        "VPA_RULE_SPREAD_VOLUME_EFFORT_RESULT": effort_rule,
        "VPA_RULE_CLOSE_LOCATION_PRESSURE": close_rule,
        "VPA_RULE_BREAKOUT_EFFORT_CONFIRMATION": breakout_rule,
        "VPA_RULE_PULLBACK_QUALITY": pullback_rule,
        "VPA_RULE_RELATIVE_STRENGTH_CONFIRMATION": relative_strength_rule,
        "VPA_RULE_VOLATILITY_COMPRESSION_EXPANSION": volatility_rule,
        "VPA_RULE_NOISE_ABSTENTION_FILTER": noise_rule,
    }


def _evaluate_states(
    row: Mapping[str, Any], rules: Mapping[str, Mapping[str, Any]]
) -> dict[str, dict[str, Any]]:
    slope = _decimal(
        _feature_value(row, "GROUP_MOVING_AVERAGE_SLOPE", "sma_20_slope_10")
    )
    volume = _decimal(
        _feature_value(row, "GROUP_VOLUME_CHANGE_AND_ZSCORE", "volume_zscore_20")
    )
    compression = _decimal(
        _feature_value(
            row,
            "GROUP_ATR_AND_VOLATILITY_COMPRESSION",
            "volatility_compression_ratio",
        )
    )
    close = rules["VPA_RULE_CLOSE_LOCATION_PRESSURE"]
    relative = rules["VPA_RULE_RELATIVE_STRENGTH_CONFIRMATION"]
    volatility = rules["VPA_RULE_VOLATILITY_COMPRESSION_EXPANSION"]

    accumulation = (
        None
        if not close["available"] or not relative["available"] or not volatility["available"]
        else volatility["tag"] == "compression_context"
        and close["tag"] == "demand_pressure"
        and relative["tag"] != "weakness_confirmed"
    )
    markup = (
        None
        if slope is None or not relative["available"]
        else slope > 0 and relative["tag"] == "leadership_confirmed"
    )
    distribution = (
        None
        if volume is None or not close["available"] or not relative["available"]
        else close["tag"] == "supply_pressure"
        and volume >= Decimal("1.0")
        and relative["tag"] != "leadership_confirmed"
    )
    markdown = (
        None
        if slope is None or not relative["available"]
        else slope < 0 and relative["tag"] == "weakness_confirmed"
    )
    balance = (
        None
        if slope is None or compression is None
        else compression <= Decimal("0.80") and abs(slope) <= Decimal("0.0")
    )
    primary_values = [accumulation, markup, distribution, markdown, balance]
    no_clear = not any(value is True for value in primary_values)
    return {
        "WYCKOFF_STATE_ACCUMULATION_CANDIDATE": _state(accumulation),
        "WYCKOFF_STATE_MARKUP_OR_UPTREND_CANDIDATE": _state(markup),
        "WYCKOFF_STATE_DISTRIBUTION_CANDIDATE": _state(distribution),
        "WYCKOFF_STATE_MARKDOWN_OR_DOWNTREND_CANDIDATE": _state(markdown),
        "WYCKOFF_STATE_TRADING_RANGE_OR_BALANCE": _state(balance),
        "WYCKOFF_STATE_NO_CLEAR_STRUCTURE": _state(no_clear),
    }


def _source_evidence() -> dict[str, str]:
    evidence = deepcopy(
        approval_service.review_service.candidate_service.SOURCE_EVIDENCE
    )
    evidence.update(
        {
            "marketflow_vpa_wyckoff_rule_baseline_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
            "marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
            "marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            "marketflow_feature_label_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
            "marketflow_feature_label_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
            "feature_label_matrix_output_binding_digest": EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST,
            "feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
            "feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
            "target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
            "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        }
    )
    return evidence


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "vpa_wyckoff_rule_baseline_executed": True,
        "vpa_wyckoff_rule_values_created": True,
        "vpa_wyckoff_state_values_created": True,
        "vpa_wyckoff_baseline_outputs_created": True,
        "backtest_execution_authorized": False,
        "model_training_authorized": False,
        "metric_computation_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }


def _report(
    report_kind: str, timestamp: str, payload: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "report_kind": report_kind,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_V1,
        "run_timestamp_utc": timestamp,
        **_common_output_fields(),
        **deepcopy(dict(payload)),
    }


def _blocked_artifact(
    output_root: Path, timestamp: str, failures: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_V1,
        "execution_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_BLOCKED_MISSING_OR_INVALID_MATRIX_SOURCE,
        "execution_scope": VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "run_timestamp_utc": timestamp,
        "generated_output_root": str(output_root).replace("\\", "/"),
        "failures": failures,
        "vpa_wyckoff_rule_baseline_executed": False,
        "vpa_wyckoff_rule_values_created": False,
        "vpa_wyckoff_state_values_created": False,
        "vpa_wyckoff_baseline_outputs_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "strategy_scoring_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "risk_controls": list(RISK_CONTROLS),
    }


def _validate_source_row(row: Mapping[str, Any], line_number: int) -> None:
    expected = {
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
    }
    for field, value in expected.items():
        if row.get(field) != value:
            raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
                f"matrix row {line_number} {field} mismatch"
            )
    if row.get("ticker") not in TARGET_UNIVERSE:
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            f"matrix row {line_number} ticker outside approved universe"
        )
    if not isinstance(row.get("feature_bundle"), Mapping):
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            f"matrix row {line_number} feature_bundle missing"
        )
    if set(row["feature_bundle"]) != set(APPROVED_FEATURE_GROUPS):
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            f"matrix row {line_number} feature groups mismatch"
        )


def _rule_output_row(row: Mapping[str, Any]) -> dict[str, Any]:
    rules = _evaluate_rules(row)
    states = _evaluate_states(row, rules)
    rule_available = all(value["available"] for value in rules.values())
    state_available = all(value["available"] for value in states.values())
    return {
        "dataset_name": row["dataset_name"],
        "ticker": row["ticker"],
        "date": row["date"],
        "source_profile": row["source_profile"],
        "timeframe": row["timeframe"],
        "canonical_record_index": row["canonical_record_index"],
        "target_family": row["target_family"],
        "target_horizon_sessions": row["target_horizon_sessions"],
        "target_profile": row["target_profile"],
        "target_available": row["target_available"],
        "target_unavailable_reason": row.get("target_unavailable_reason"),
        "selected_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "rule_family_count": len(SELECTED_RULE_FAMILY_IDS),
        "state_family_count": len(SELECTED_STATE_FAMILY_IDS),
        "rule_values": rules,
        "state_values": states,
        "rule_values_available": rule_available,
        "state_values_available": state_available,
        "rule_unavailable_reason": (
            None if rule_available else "REQUIRED_FEATURE_VALUES_UNAVAILABLE"
        ),
        "state_unavailable_reason": (
            None if state_available else "REQUIRED_FEATURE_VALUES_UNAVAILABLE"
        ),
        "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_matrix_approval_digest": approval_service.review_service.candidate_service.execution.EXPECTED_SOURCE_APPROVAL_DIGEST,
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "research_only": True,
        "non_actionable": True,
    }


def _empty_coverage() -> dict[str, Counter]:
    return {
        **{rule_id: Counter() for rule_id in SELECTED_RULE_FAMILY_IDS},
        **{state_id: Counter() for state_id in SELECTED_STATE_FAMILY_IDS},
    }


def _update_coverage(
    coverage: Mapping[str, Counter], output_row: Mapping[str, Any]
) -> None:
    for rule_id, value in output_row["rule_values"].items():
        coverage[rule_id][value["tag"]] += 1
    for state_id, value in output_row["state_values"].items():
        key = "unavailable" if not value["available"] else str(value["value"]).lower()
        coverage[state_id][key] += 1


def _write_rule_rows(
    source_path: Path, destination: Path
) -> dict[str, Any]:
    row_count = 0
    per_ticker_counts: Counter[str] = Counter()
    canonical_indexes: dict[str, set[int]] = defaultdict(set)
    coverage = _empty_coverage()
    per_ticker_coverage = {ticker: _empty_coverage() for ticker in TARGET_UNIVERSE}
    output_hasher = hashlib.sha256()
    try:
        with source_path.open("r", encoding="utf-8") as source, destination.open(
            "xb"
        ) as output:
            for line_number, line in enumerate(source, start=1):
                try:
                    source_row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
                        f"matrix row {line_number} invalid JSON"
                    ) from exc
                if not isinstance(source_row, dict):
                    raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
                        f"matrix row {line_number} must be a JSON object"
                    )
                _validate_source_row(source_row, line_number)
                output_row = _rule_output_row(source_row)
                payload = canonical_json_bytes(output_row)
                output.write(payload)
                output_hasher.update(payload)
                ticker = output_row["ticker"]
                row_count += 1
                per_ticker_counts[ticker] += 1
                canonical_indexes[ticker].add(output_row["canonical_record_index"])
                _update_coverage(coverage, output_row)
                _update_coverage(per_ticker_coverage[ticker], output_row)
    except FileExistsError as exc:
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            "temporary rule-values output already exists"
        ) from exc
    return {
        "row_count": row_count,
        "rule_values_digest": output_hasher.hexdigest(),
        "per_ticker_counts": dict(per_ticker_counts),
        "historical_record_counts": {
            ticker: len(canonical_indexes[ticker]) for ticker in TARGET_UNIVERSE
        },
        "coverage": {
            key: dict(sorted(counter.items())) for key, counter in coverage.items()
        },
        "per_ticker_coverage": {
            ticker: {
                key: dict(sorted(counter.items()))
                for key, counter in per_ticker_coverage[ticker].items()
            }
            for ticker in TARGET_UNIVERSE
        },
    }


def per_ticker_vpa_wyckoff_rule_baseline_execution_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_vpa_wyckoff_rule_baseline_execution_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(scan: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for ticker in TARGET_UNIVERSE:
        matrix_rows = scan["per_ticker_counts"].get(ticker, 0)
        historical_count = scan["historical_record_counts"].get(ticker, 0)
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": historical_count,
            "meta_reduced_record_count_flag": ticker == "META",
            "vpa_wyckoff_rule_baseline_approval_status": approval_service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED,
            "vpa_wyckoff_rule_baseline_execution_status": "GENERATED_RESEARCH_ONLY",
            "selected_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
            "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
            "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "source_matrix_row_count": matrix_rows,
            "rule_value_row_count": matrix_rows,
            "state_value_row_count": matrix_rows,
            "selected_rule_family_count": len(SELECTED_RULE_FAMILY_IDS),
            "selected_state_family_count": len(SELECTED_STATE_FAMILY_IDS),
            "vpa_wyckoff_rule_baseline_executed": True,
            "vpa_wyckoff_rule_values_created": True,
            "vpa_wyckoff_state_values_created": True,
            "vpa_wyckoff_baseline_outputs_created": True,
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
            "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
            "generation_note": (
                "PRESERVE_META_LIMITATION_IN_VPA_WYCKOFF_RULE_BASELINE_EXECUTION"
                if ticker == "META"
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_vpa_wyckoff_rule_baseline_execution_digest"] = (
            per_ticker_vpa_wyckoff_rule_baseline_execution_digest_v1(entry)
        )
        rows.append(entry)
    return rows


def _rule_schema(timestamp: str) -> dict[str, Any]:
    logic = {
        "VPA_RULE_VOLUME_CONFIRMATION": "volume z-score and trailing return direction",
        "VPA_RULE_SPREAD_VOLUME_EFFORT_RESULT": "spread-volume interaction and effort-result ratio",
        "VPA_RULE_CLOSE_LOCATION_PRESSURE": "fixed close-location demand and supply bands",
        "VPA_RULE_BREAKOUT_EFFORT_CONFIRMATION": "positive five-session return, high volume, and demand close",
        "VPA_RULE_PULLBACK_QUALITY": "negative five-session return within positive slope and acceptable noise",
        "VPA_RULE_RELATIVE_STRENGTH_CONFIRMATION": "fixed cross-universe percentile bands",
        "VPA_RULE_VOLATILITY_COMPRESSION_EXPANSION": "fixed volatility-compression ratio bands",
        "VPA_RULE_NOISE_ABSTENTION_FILTER": "source abstention flag or fixed noise-to-trend threshold",
    }
    return _report(
        "vpa_wyckoff_rule_schema",
        timestamp,
        {
            "rule_threshold_policy": RULE_THRESHOLD_POLICY,
            "rule_thresholds": dict(RULE_THRESHOLDS),
            "executed_rule_families": [
                {
                    "rule_family_id": rule_id,
                    "execution_status": "EXECUTED_RESEARCH_ONLY",
                    "logic": logic[rule_id],
                }
                for rule_id in SELECTED_RULE_FAMILY_IDS
            ],
            "supporting_rule_families": [
                {
                    "rule_family_id": rule_id,
                    "approval_status": "AVAILABLE_NOT_SELECTED",
                    "execution_performed": False,
                }
                for rule_id in SUPPORTING_RULE_FAMILY_IDS
            ],
        },
    )


def _state_schema(timestamp: str) -> dict[str, Any]:
    logic = {
        "WYCKOFF_STATE_ACCUMULATION_CANDIDATE": "compression plus demand pressure without relative weakness",
        "WYCKOFF_STATE_MARKUP_OR_UPTREND_CANDIDATE": "positive moving-average slope plus leadership",
        "WYCKOFF_STATE_DISTRIBUTION_CANDIDATE": "supply pressure plus high volume without leadership",
        "WYCKOFF_STATE_MARKDOWN_OR_DOWNTREND_CANDIDATE": "negative moving-average slope plus weakness",
        "WYCKOFF_STATE_TRADING_RANGE_OR_BALANCE": "compression plus zero moving-average slope",
        "WYCKOFF_STATE_NO_CLEAR_STRUCTURE": "no other selected state is true or inputs are insufficient",
    }
    return _report(
        "vpa_wyckoff_state_schema",
        timestamp,
        {
            "rule_threshold_policy": RULE_THRESHOLD_POLICY,
            "executed_wyckoff_state_families": [
                {
                    "state_family_id": state_id,
                    "execution_status": "EXECUTED_RESEARCH_ONLY",
                    "logic": logic[state_id],
                }
                for state_id in SELECTED_STATE_FAMILY_IDS
            ],
            "supporting_wyckoff_state_families": [
                {
                    "state_family_id": state_id,
                    "approval_status": "AVAILABLE_NOT_SELECTED",
                    "execution_performed": False,
                }
                for state_id in SUPPORTING_STATE_FAMILY_IDS
            ],
        },
    )


def _reports(
    timestamp: str,
    scan: Mapping[str, Any],
    per_ticker: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    source_rows = scan["row_count"]
    no_peek_controls = {
        "source_feature_bundle_only": True,
        "target_metadata_only": True,
        "target_values_absent": True,
        "target_classes_absent": True,
        "forward_returns_absent": True,
        "future_data_absent": True,
        "prediction_fields_absent": True,
        "strategy_score_fields_absent": True,
        "trade_recommendation_fields_absent": True,
        "broker_order_fields_absent": True,
        "provider_payload_fields_absent": True,
        "api_key_fields_absent": True,
    }
    return {
        "vpa_wyckoff_rule_schema.json": _rule_schema(timestamp),
        "vpa_wyckoff_state_schema.json": _state_schema(timestamp),
        "vpa_wyckoff_rule_coverage_report.json": _report(
            "vpa_wyckoff_rule_coverage_report",
            timestamp,
            {
                "source_matrix_row_count": source_rows,
                "rule_value_row_count": source_rows,
                "state_value_row_count": source_rows,
                "selected_rule_family_count": len(SELECTED_RULE_FAMILY_IDS),
                "selected_state_family_count": len(SELECTED_STATE_FAMILY_IDS),
                "rule_family_reference_count": source_rows
                * len(SELECTED_RULE_FAMILY_IDS),
                "state_family_reference_count": source_rows
                * len(SELECTED_STATE_FAMILY_IDS),
                "coverage": deepcopy(scan["coverage"]),
                "coverage_is_descriptive_not_performance_metric": True,
            },
        ),
        "vpa_wyckoff_per_ticker_report.json": _report(
            "vpa_wyckoff_per_ticker_report",
            timestamp,
            {
                "per_ticker_execution_entries": deepcopy(per_ticker),
                "per_ticker_coverage": deepcopy(scan["per_ticker_coverage"]),
            },
        ),
        "vpa_wyckoff_meta_limitation_report.json": _report(
            "vpa_wyckoff_meta_limitation_report",
            timestamp,
            {
                "ticker": "META",
                "historical_record_count": scan["historical_record_counts"].get(
                    "META", 0
                ),
                "source_matrix_row_count": scan["per_ticker_counts"].get("META", 0),
                "rule_value_row_count": scan["per_ticker_counts"].get("META", 0),
                "state_value_row_count": scan["per_ticker_counts"].get("META", 0),
                "meta_reduced_record_count_flag": True,
                "generation_note": "PRESERVE_META_LIMITATION_IN_VPA_WYCKOFF_RULE_BASELINE_EXECUTION",
                "repair_or_inference_performed": False,
            },
        ),
        "vpa_wyckoff_no_peek_report.json": _report(
            "vpa_wyckoff_no_peek_report",
            timestamp,
            {
                "no_peek_controls": no_peek_controls,
                "forbidden_rule_output_fields": sorted(FORBIDDEN_RULE_OUTPUT_FIELDS),
                "rule_output_row_fields": sorted(RULE_OUTPUT_ROW_FIELDS),
            },
        ),
        "vpa_wyckoff_operator_summary.json": _report(
            "vpa_wyckoff_operator_summary",
            timestamp,
            {
                "execution_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY,
                "rule_threshold_policy": RULE_THRESHOLD_POLICY,
                "source_matrix_row_count": source_rows,
                "rule_value_row_count": source_rows,
                "state_value_row_count": source_rows,
                "generated_output_count": EXPECTED_OUTPUT_COUNT,
                "next_chain": list(NEXT_CHAIN),
                "next_gates": list(NEXT_GATES),
                "risk_controls": list(RISK_CONTROLS),
                "backtest_or_performance_evaluation_performed": False,
            },
        ),
    }


def _output_binding_digest(entries: Iterable[Mapping[str, Any]]) -> str:
    return semantic_digest(
        {
            "output_digest_manifest": list(entries),
            "manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        }
    )


def _per_ticker_digests_valid(entries: Any) -> bool:
    return (
        isinstance(entries, list)
        and [row.get("ticker") for row in entries if isinstance(row, Mapping)]
        == TARGET_UNIVERSE
        and all(
            isinstance(row, Mapping)
            and row.get("per_ticker_vpa_wyckoff_rule_baseline_execution_digest")
            == per_ticker_vpa_wyckoff_rule_baseline_execution_digest_v1(row)
            for row in entries
        )
    )


REQUIRED_CHECK_IDS = [
    "source_approval_digest_bound",
    "source_candidate_review_digest_bound",
    "source_candidate_digest_bound",
    "source_matrix_results_review_digest_bound",
    "source_matrix_execution_digest_bound",
    "source_matrix_rows_digest_bound",
    "source_feature_values_digest_bound",
    "source_target_values_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "selected_vpa_wyckoff_package_preserved",
    "selected_matrix_package_preserved",
    "selected_feature_package_preserved",
    "selected_target_package_preserved",
    "selected_objective_path_preserved",
    "source_baseline_authorized_true",
    "rule_baseline_executed_true",
    "rule_values_created_true",
    "state_values_created_true",
    "baseline_outputs_created_true",
    "source_matrix_row_count_179190",
    "rule_value_row_count_179190",
    "state_value_row_count_179190",
    "selected_rule_family_count_8",
    "selected_state_family_count_6",
    "rule_family_reference_count_1433520",
    "state_family_reference_count_1075140",
    "per_non_meta_ticker_counts_preserved",
    "meta_counts_preserved",
    "generated_output_count_10",
    "rule_values_jsonl_created",
    "rule_schema_created",
    "state_schema_created",
    "coverage_report_created",
    "per_ticker_report_created",
    "meta_limitation_report_created",
    "no_peek_report_created",
    "operator_summary_created",
    "digest_manifest_created",
    "digest_manifest_self_reference_policy_verified",
    "target_values_absent",
    "target_classes_absent",
    "forward_returns_absent",
    "future_data_absent",
    "prediction_fields_absent",
    "strategy_score_fields_absent",
    "trade_recommendation_fields_absent",
    "broker_order_fields_absent",
    "provider_payload_fields_absent",
    "api_key_fields_absent",
    "rule_threshold_policy_static_not_optimized",
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
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "feature_label_matrix_execution_rerun_false",
    "feature_label_matrix_results_review_rerun_false",
    "vpa_wyckoff_candidate_creation_rerun_false",
    "vpa_wyckoff_candidate_review_rerun_false",
    "vpa_wyckoff_approval_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


def _condition_values(artifact: Mapping[str, Any]) -> dict[str, bool]:
    manifest = artifact.get("output_digest_manifest", [])
    names = [entry.get("filename") for entry in manifest if isinstance(entry, Mapping)]
    per_ticker = artifact.get(
        "per_ticker_vpa_wyckoff_rule_baseline_execution_entries", []
    )
    schema = artifact.get("rule_output_schema_validation", {})
    values = {
        "source_approval_digest_bound": artifact.get("source_vpa_wyckoff_rule_baseline_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest_bound": artifact.get("source_candidate_review_digest") == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest_bound": artifact.get("source_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_matrix_results_review_digest_bound": artifact.get("source_matrix_results_review_digest") == EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_execution_digest_bound": artifact.get("source_matrix_execution_digest") == EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_matrix_rows_digest_bound": artifact.get("source_matrix_rows_digest") == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest_bound": artifact.get("source_feature_values_digest") == EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest_bound": artifact.get("source_target_values_digest") == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": artifact.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": artifact.get("target_universe") == TARGET_UNIVERSE and artifact.get("target_universe_count") == len(TARGET_UNIVERSE),
        "records_digest_preserved": artifact.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": artifact.get("meta_record_count") == EXPECTED_RECORD_COUNTS.get("META"),
        "selected_vpa_wyckoff_package_preserved": artifact.get("selected_vpa_wyckoff_package") == PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package_preserved": artifact.get("selected_matrix_package") == PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_feature_package_preserved": artifact.get("selected_feature_package") == PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_target_package_preserved": artifact.get("selected_label_target_package") == PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path_preserved": artifact.get("selected_objective_path") == EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "source_baseline_authorized_true": artifact.get("vpa_wyckoff_rule_baseline_authorized") is True,
        "rule_baseline_executed_true": artifact.get("vpa_wyckoff_rule_baseline_executed") is True,
        "rule_values_created_true": artifact.get("vpa_wyckoff_rule_values_created") is True,
        "state_values_created_true": artifact.get("vpa_wyckoff_state_values_created") is True,
        "baseline_outputs_created_true": artifact.get("vpa_wyckoff_baseline_outputs_created") is True,
        "source_matrix_row_count_179190": artifact.get("source_matrix_row_count") == EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "rule_value_row_count_179190": artifact.get("rule_value_row_count") == EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_value_row_count_179190": artifact.get("state_value_row_count") == EXPECTED_STATE_VALUE_ROW_COUNT,
        "selected_rule_family_count_8": artifact.get("selected_rule_family_count") == len(SELECTED_RULE_FAMILY_IDS),
        "selected_state_family_count_6": artifact.get("selected_state_family_count") == len(SELECTED_STATE_FAMILY_IDS),
        "rule_family_reference_count_1433520": artifact.get("rule_family_reference_count") == EXPECTED_RULE_FAMILY_REFERENCE_COUNT,
        "state_family_reference_count_1075140": artifact.get("state_family_reference_count") == EXPECTED_STATE_FAMILY_REFERENCE_COUNT,
        "per_non_meta_ticker_counts_preserved": all(entry.get("historical_record_count") == EXPECTED_RECORD_COUNTS.get(entry.get("ticker")) and entry.get("source_matrix_row_count") == EXPECTED_RECORD_COUNTS.get(entry.get("ticker"), 0) * 15 for entry in per_ticker if entry.get("ticker") != "META"),
        "meta_counts_preserved": any(entry.get("ticker") == "META" and entry.get("historical_record_count") == EXPECTED_RECORD_COUNTS.get("META") and entry.get("source_matrix_row_count") == EXPECTED_RECORD_COUNTS.get("META", 0) * 15 for entry in per_ticker),
        "generated_output_count_10": artifact.get("generated_output_count") == EXPECTED_OUTPUT_COUNT and artifact.get("observed_output_count") == EXPECTED_OUTPUT_COUNT,
        "rule_values_jsonl_created": "vpa_wyckoff_rule_values.jsonl" in names,
        "rule_schema_created": "vpa_wyckoff_rule_schema.json" in names,
        "state_schema_created": "vpa_wyckoff_state_schema.json" in names,
        "coverage_report_created": "vpa_wyckoff_rule_coverage_report.json" in names,
        "per_ticker_report_created": "vpa_wyckoff_per_ticker_report.json" in names,
        "meta_limitation_report_created": "vpa_wyckoff_meta_limitation_report.json" in names,
        "no_peek_report_created": "vpa_wyckoff_no_peek_report.json" in names,
        "operator_summary_created": "vpa_wyckoff_operator_summary.json" in names,
        "digest_manifest_created": "vpa_wyckoff_digest_manifest.json" in names,
        "digest_manifest_self_reference_policy_verified": bool(manifest) and manifest[-1].get("digest_kind") == SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE and manifest[-1].get("sha256") is None,
        "target_values_absent": schema.get("target_values_absent") is True,
        "target_classes_absent": schema.get("target_classes_absent") is True,
        "forward_returns_absent": schema.get("forward_returns_absent") is True,
        "future_data_absent": schema.get("future_data_absent") is True,
        "prediction_fields_absent": schema.get("prediction_fields_absent") is True,
        "strategy_score_fields_absent": schema.get("strategy_score_fields_absent") is True,
        "trade_recommendation_fields_absent": schema.get("trade_recommendation_fields_absent") is True,
        "broker_order_fields_absent": schema.get("broker_order_fields_absent") is True,
        "provider_payload_fields_absent": schema.get("provider_payload_fields_absent") is True,
        "api_key_fields_absent": schema.get("api_key_fields_absent") is True,
        "rule_threshold_policy_static_not_optimized": artifact.get("rule_threshold_policy") == RULE_THRESHOLD_POLICY,
        "expectancy_backtest_lab_candidate_created_false": artifact.get("expectancy_backtest_lab_candidate_created") is False,
        "backtest_execution_authorized_false": artifact.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": artifact.get("backtest_execution_performed") is False,
        "model_training_authorized_false": artifact.get("model_training_authorized") is False,
        "model_training_performed_false": artifact.get("model_training_performed") is False,
        "metric_computation_authorized_false": artifact.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": artifact.get("metric_computation_performed") is False,
        "strategy_scoring_false": artifact.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": artifact.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": artifact.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": artifact.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": artifact.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": artifact.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": artifact.get("trade_recommendations_generated") is False,
        "per_ticker_entries_12": isinstance(per_ticker, list) and len(per_ticker) == len(TARGET_UNIVERSE),
        "per_ticker_digests_present": _per_ticker_digests_valid(per_ticker),
        "provider_requests_made_false": artifact.get("provider_requests_made_in_execution") is False,
        "market_data_acquisition_false": artifact.get("market_data_acquisition_performed_in_execution") is False,
        "dataset_regeneration_false": artifact.get("canonical_dataset_regenerated_in_execution") is False,
        "feature_label_matrix_execution_rerun_false": artifact.get("feature_label_matrix_execution_rerun_performed") is False,
        "feature_label_matrix_results_review_rerun_false": artifact.get("feature_label_matrix_results_review_rerun_performed") is False,
        "vpa_wyckoff_candidate_creation_rerun_false": artifact.get("vpa_wyckoff_candidate_creation_rerun_performed") is False,
        "vpa_wyckoff_candidate_review_rerun_false": artifact.get("vpa_wyckoff_candidate_review_rerun_performed") is False,
        "vpa_wyckoff_approval_rerun_false": artifact.get("vpa_wyckoff_approval_rerun_performed") is False,
        "raw_provider_payloads_not_committed": artifact.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": artifact.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": artifact.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": artifact.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": artifact.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": artifact.get("no_tracked_marketflow_files") is True,
    }
    if list(values) != REQUIRED_CHECK_IDS:
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            "internal checklist definition mismatch"
        )
    return values


def _checklist(artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": check_id,
            "status": PASS if actual else FAIL,
            "expected": True,
            "actual": actual,
            "severity": BLOCKER,
            "message": f"{check_id} {'passed' if actual else 'failed'}",
        }
        for check_id, actual in _condition_values(artifact).items()
    ]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "vpa_wyckoff_rule_baseline_executed": True,
        "vpa_wyckoff_rule_values_created": True,
        "vpa_wyckoff_state_values_created": True,
        "vpa_wyckoff_baseline_outputs_created": True,
        "selected_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "source_matrix_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "rule_value_row_count": EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_value_row_count": EXPECTED_STATE_VALUE_ROW_COUNT,
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_vpa_wyckoff_rule_baseline_execution_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(artifact))
    payload.pop("generated_output_root", None)
    payload.pop("execution_checklist", None)
    payload.pop("execution_summary", None)
    payload.pop("marketflow_vpa_wyckoff_rule_baseline_execution_digest", None)
    return semantic_digest(payload)


def _build_artifact(
    *,
    timestamp: str,
    output_root: Path,
    source_verification: Mapping[str, Any],
    scan: Mapping[str, Any],
    per_ticker: list[dict[str, Any]],
    output_manifest: list[dict[str, Any]],
    output_binding_digest: str,
) -> dict[str, Any]:
    schema_validation = {
        "target_values_absent": True,
        "target_classes_absent": True,
        "forward_returns_absent": True,
        "future_data_absent": True,
        "prediction_fields_absent": True,
        "strategy_score_fields_absent": True,
        "trade_recommendation_fields_absent": True,
        "broker_order_fields_absent": True,
        "provider_payload_fields_absent": True,
        "api_key_fields_absent": True,
    }
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_V1,
        "execution_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY,
        "execution_scope": VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "run_timestamp_utc": timestamp,
        "generated_output_root": str(output_root).replace("\\", "/"),
        "selected_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_vpa_wyckoff_rule_baseline_approval_artifact_kind": approval_service.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED,
        "source_vpa_wyckoff_rule_baseline_approval_status": approval_service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED,
        "source_vpa_wyckoff_rule_baseline_approval_scope": approval_service.VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ONLY,
        "source_vpa_wyckoff_rule_baseline_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_matrix_output_binding_digest": EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST,
        "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": _source_evidence(),
        "source_verification": deepcopy(dict(source_verification)),
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
            (
                count
                for ticker, count in EXPECTED_RECORD_COUNTS.items()
                if ticker != "META"
            ),
            None,
        ),
        "meta_reduced_record_count_preserved": True,
        "vpa_wyckoff_rule_baseline_selected": True,
        "vpa_wyckoff_rule_baseline_approved": True,
        "vpa_wyckoff_rule_baseline_authorized": True,
        "ready_for_vpa_wyckoff_rule_baseline_execution": True,
        "vpa_wyckoff_rule_baseline_executed": True,
        "vpa_wyckoff_rule_values_created": True,
        "vpa_wyckoff_state_values_created": True,
        "vpa_wyckoff_baseline_outputs_created": True,
        "vpa_wyckoff_rule_baseline_results_created": True,
        "source_matrix_row_count": scan["row_count"],
        "rule_value_row_count": scan["row_count"],
        "state_value_row_count": scan["row_count"],
        "selected_rule_family_count": len(SELECTED_RULE_FAMILY_IDS),
        "selected_state_family_count": len(SELECTED_STATE_FAMILY_IDS),
        "rule_family_reference_count": scan["row_count"]
        * len(SELECTED_RULE_FAMILY_IDS),
        "state_family_reference_count": scan["row_count"]
        * len(SELECTED_STATE_FAMILY_IDS),
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "observed_output_count": len(output_manifest),
        "rule_threshold_policy": RULE_THRESHOLD_POLICY,
        "rule_thresholds": dict(RULE_THRESHOLDS),
        "planned_rule_evaluation_scope": "RESEARCH_ONLY_RULE_TAGGING_NOT_BACKTEST",
        "vpa_wyckoff_rule_values_digest": scan["rule_values_digest"],
        "vpa_wyckoff_rule_baseline_output_binding_digest": output_binding_digest,
        "output_digest_manifest": deepcopy(output_manifest),
        "manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "per_ticker_vpa_wyckoff_rule_baseline_execution_entries": deepcopy(per_ticker),
        "rule_output_schema_validation": schema_validation,
        "expectancy_backtest_lab_candidate_created": False,
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
        "provider_requests_made_in_execution": False,
        "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "vpa_wyckoff_candidate_creation_rerun_performed": False,
        "vpa_wyckoff_candidate_review_rerun_performed": False,
        "vpa_wyckoff_approval_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }
    checklist = _checklist(artifact)
    artifact["execution_checklist"] = checklist
    artifact["execution_summary"] = _summary(checklist)
    digest = marketflow_vpa_wyckoff_rule_baseline_execution_digest_v1(artifact)
    artifact["marketflow_vpa_wyckoff_rule_baseline_execution_digest"] = digest
    artifact["execution_summary"][
        "marketflow_vpa_wyckoff_rule_baseline_execution_digest"
    ] = digest
    return artifact


def _write_bytes_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            f"VPA/Wyckoff output already exists: {path.name}"
        ) from exc


def execute_marketflow_vpa_wyckoff_rule_baseline_v1(
    *,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Stream the reviewed matrix into transparent research-only rule/state tags."""
    timestamp = run_timestamp_utc or _utc_now()
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    source_path = DEFAULT_SOURCE_MATRIX_PATH
    if not source_path.is_file():
        return _blocked_artifact(
            output_path,
            timestamp,
            [
                {
                    "failure_id": "matrix_source_missing",
                    "message": f"missing source matrix: {source_path}",
                }
            ],
        )
    actual_source_digest = sha256_file(source_path)
    if actual_source_digest != EXPECTED_SOURCE_MATRIX_ROWS_DIGEST:
        return _blocked_artifact(
            output_path,
            timestamp,
            [
                {
                    "failure_id": "matrix_source_digest_mismatch",
                    "message": "source matrix rows digest mismatch",
                    "expected": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
                    "actual": actual_source_digest,
                }
            ],
        )
    if output_path.exists() and any(output_path.iterdir()):
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            "VPA/Wyckoff output root is not empty"
        )
    output_path.mkdir(parents=True, exist_ok=True)
    temporary_rule_values = output_path / ".vpa_wyckoff_rule_values.jsonl.tmp"
    source_verification = {
        "source_matrix_path": str(source_path).replace("\\", "/"),
        "before_source_matrix_rows_digest": actual_source_digest,
        "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "streaming_read_used": True,
        "entire_matrix_loaded_into_memory": False,
    }
    try:
        scan = _write_rule_rows(source_path, temporary_rule_values)
    except (OSError, MarketFlowVpaWyckoffRuleBaselineExecutionError) as exc:
        temporary_rule_values.unlink(missing_ok=True)
        return _blocked_artifact(
            output_path,
            timestamp,
            [{"failure_id": "matrix_source_invalid", "message": str(exc)}],
        )
    if scan["row_count"] != EXPECTED_SOURCE_MATRIX_ROW_COUNT:
        temporary_rule_values.unlink(missing_ok=True)
        return _blocked_artifact(
            output_path,
            timestamp,
            [
                {
                    "failure_id": "matrix_source_row_count_mismatch",
                    "message": "source matrix row count mismatch",
                    "expected": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
                    "actual": scan["row_count"],
                }
            ],
        )
    if scan["historical_record_counts"] != EXPECTED_RECORD_COUNTS:
        temporary_rule_values.unlink(missing_ok=True)
        return _blocked_artifact(
            output_path,
            timestamp,
            [
                {
                    "failure_id": "matrix_source_historical_counts_mismatch",
                    "message": "source matrix historical record counts mismatch",
                    "expected": dict(EXPECTED_RECORD_COUNTS),
                    "actual": scan["historical_record_counts"],
                }
            ],
        )
    expected_matrix_counts = {
        ticker: count * 15 for ticker, count in EXPECTED_RECORD_COUNTS.items()
    }
    if scan["per_ticker_counts"] != expected_matrix_counts:
        temporary_rule_values.unlink(missing_ok=True)
        return _blocked_artifact(
            output_path,
            timestamp,
            [
                {
                    "failure_id": "matrix_source_per_ticker_counts_mismatch",
                    "message": "source matrix per-ticker row counts mismatch",
                    "expected": expected_matrix_counts,
                    "actual": scan["per_ticker_counts"],
                }
            ],
        )
    after_source_digest = sha256_file(source_path)
    source_verification.update(
        {
            "after_source_matrix_rows_digest": after_source_digest,
            "source_matrix_unchanged": after_source_digest
            == actual_source_digest
            == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        }
    )
    if not source_verification["source_matrix_unchanged"]:
        temporary_rule_values.unlink(missing_ok=True)
        return _blocked_artifact(
            output_path,
            timestamp,
            [
                {
                    "failure_id": "matrix_source_changed_during_execution",
                    "message": "source matrix changed during streaming execution",
                }
            ],
        )
    per_ticker = _per_ticker_entries(scan)
    reports = _reports(timestamp, scan, per_ticker)
    report_bytes = {name: canonical_json_bytes(report) for name, report in reports.items()}
    output_manifest: list[dict[str, Any]] = []
    for filename in OUTPUT_FILENAMES:
        if filename == OUTPUT_FILENAMES[0]:
            entry = {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_EXECUTION_ARTIFACT",
                "sha256": None,
            }
        elif filename == OUTPUT_FILENAMES[-1]:
            entry = {
                "filename": filename,
                "digest_kind": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
                "sha256": None,
            }
        elif filename == "vpa_wyckoff_rule_values.jsonl":
            entry = {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": scan["rule_values_digest"],
            }
        else:
            entry = {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": sha256_bytes(report_bytes[filename]),
            }
        output_manifest.append(entry)
    output_binding_digest = _output_binding_digest(output_manifest)
    artifact = _build_artifact(
        timestamp=timestamp,
        output_root=output_path,
        source_verification=source_verification,
        scan=scan,
        per_ticker=per_ticker,
        output_manifest=output_manifest,
        output_binding_digest=output_binding_digest,
    )
    validate_marketflow_vpa_wyckoff_rule_baseline_execution_v1(artifact)
    report_bytes[OUTPUT_FILENAMES[0]] = canonical_json_bytes(artifact)
    report_bytes[OUTPUT_FILENAMES[-1]] = canonical_json_bytes(
        _report(
            "vpa_wyckoff_digest_manifest",
            timestamp,
            {
                "marketflow_vpa_wyckoff_rule_baseline_execution_digest": artifact[
                    "marketflow_vpa_wyckoff_rule_baseline_execution_digest"
                ],
                "vpa_wyckoff_rule_baseline_output_binding_digest": output_binding_digest,
                "vpa_wyckoff_rule_values_digest": scan["rule_values_digest"],
                "output_digest_manifest": output_manifest,
                "manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
            },
        )
    )
    for filename in OUTPUT_FILENAMES:
        if filename == "vpa_wyckoff_rule_values.jsonl":
            continue
        _write_bytes_once(output_path / filename, report_bytes[filename])
    temporary_rule_values.replace(output_path / "vpa_wyckoff_rule_values.jsonl")
    return artifact


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(f"{field} mismatch")


def validate_marketflow_vpa_wyckoff_rule_baseline_execution_v1(
    artifact: dict,
) -> dict:
    """Validate output evidence, counts, leakage controls, and closed authorities."""
    if not isinstance(artifact, dict):
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            "artifact must be a JSON object"
        )
    exact_fields = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_V1,
        "execution_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY,
        "execution_scope": VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "selected_vpa_wyckoff_package": PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package": PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "source_vpa_wyckoff_rule_baseline_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": len(TARGET_UNIVERSE),
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "source_matrix_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "rule_value_row_count": EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_value_row_count": EXPECTED_STATE_VALUE_ROW_COUNT,
        "selected_rule_family_count": len(SELECTED_RULE_FAMILY_IDS),
        "selected_state_family_count": len(SELECTED_STATE_FAMILY_IDS),
        "rule_family_reference_count": EXPECTED_RULE_FAMILY_REFERENCE_COUNT,
        "state_family_reference_count": EXPECTED_STATE_FAMILY_REFERENCE_COUNT,
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "observed_output_count": EXPECTED_OUTPUT_COUNT,
        "rule_threshold_policy": RULE_THRESHOLD_POLICY,
        "risk_controls": RISK_CONTROLS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
    }
    for field, value in exact_fields.items():
        _expect(artifact.get(field), value, field)
    for field in (
        "vpa_wyckoff_rule_baseline_authorized",
        "vpa_wyckoff_rule_baseline_executed",
        "vpa_wyckoff_rule_values_created",
        "vpa_wyckoff_state_values_created",
        "vpa_wyckoff_baseline_outputs_created",
        "vpa_wyckoff_rule_baseline_results_created",
    ):
        _expect(artifact.get(field), True, field)
    for field in (
        "expectancy_backtest_lab_candidate_created",
        "backtest_execution_authorized",
        "backtest_execution_performed",
        "model_training_authorized",
        "model_training_performed",
        "metric_computation_authorized",
        "metric_computation_performed",
        "strategy_scoring_performed",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made_in_execution",
        "market_data_acquisition_performed_in_execution",
        "canonical_dataset_regenerated_in_execution",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "vpa_wyckoff_candidate_creation_rerun_performed",
        "vpa_wyckoff_candidate_review_rerun_performed",
        "vpa_wyckoff_approval_rerun_performed",
    ):
        _expect(artifact.get(field), False, field)
    _expect(artifact.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(artifact.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    for field in (
        "vpa_wyckoff_rule_values_digest",
        "vpa_wyckoff_rule_baseline_output_binding_digest",
    ):
        value = artifact.get(field)
        if not isinstance(value, str) or len(value) != 64:
            raise MarketFlowVpaWyckoffRuleBaselineExecutionError(f"{field} missing")
    expected_checklist = _checklist(artifact)
    if artifact.get("execution_checklist") != expected_checklist or any(
        row["status"] != PASS for row in expected_checklist
    ):
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            "execution checklist mismatch"
        )
    if artifact.get("execution_summary") != {
        **_summary(expected_checklist),
        "marketflow_vpa_wyckoff_rule_baseline_execution_digest": artifact.get(
            "marketflow_vpa_wyckoff_rule_baseline_execution_digest"
        ),
    }:
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            "execution summary mismatch"
        )
    digest = artifact.get("marketflow_vpa_wyckoff_rule_baseline_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError("execution digest missing")
    if digest != marketflow_vpa_wyckoff_rule_baseline_execution_digest_v1(artifact):
        raise MarketFlowVpaWyckoffRuleBaselineExecutionError(
            "execution digest mismatch"
        )
    return {
        "status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_VALID,
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "execution_scope": artifact["execution_scope"],
        "marketflow_vpa_wyckoff_rule_baseline_execution_digest": digest,
        "vpa_wyckoff_rule_baseline_output_binding_digest": artifact[
            "vpa_wyckoff_rule_baseline_output_binding_digest"
        ],
        "vpa_wyckoff_rule_values_digest": artifact["vpa_wyckoff_rule_values_digest"],
        **{
            field: artifact["execution_summary"][field]
            for field in (
                "total_checks",
                "passed_checks",
                "failed_checks",
                "blocker_count",
            )
        },
    }


def build_marketflow_vpa_wyckoff_rule_baseline_execution_markdown_v1(
    artifact: dict,
) -> str:
    """Render a sanitized Markdown view of the validated execution artifact."""
    validation = validate_marketflow_vpa_wyckoff_rule_baseline_execution_v1(artifact)
    sections = [
        ("Title", ["VPA/Wyckoff Rule Baseline Execution v1"]),
        (
            "VPA/Wyckoff Rule Baseline Execution v1",
            [
                f"Artifact/status/scope: `{artifact['artifact_kind']}` / "
                f"`{artifact['execution_status']}` / `{artifact['execution_scope']}`.",
                "Execution digest: "
                f"`{validation['marketflow_vpa_wyckoff_rule_baseline_execution_digest']}`.",
            ],
        ),
        (
            "Source Approval",
            [
                f"Approval digest: `{artifact['source_vpa_wyckoff_rule_baseline_approval_digest']}`."
            ],
        ),
        (
            "Bound Evidence",
            [
                f"Candidate review/candidate: `{artifact['source_candidate_review_digest']}` / "
                f"`{artifact['source_candidate_digest']}`.",
                f"Matrix review/rows: `{artifact['source_matrix_results_review_digest']}` / "
                f"`{artifact['source_matrix_rows_digest']}`.",
                f"Feature/target/records: `{artifact['source_feature_values_digest']}` / "
                f"`{artifact['source_target_values_digest']}` / "
                f"`{artifact['records_digest']}`.",
            ],
        ),
        (
            "Dataset and Universe",
            [
                f"`{artifact['dataset_name']}`, {artifact['total_canonical_record_count']} "
                f"records; {', '.join(artifact['target_universe'])}.",
                "META remains exactly 913 records; every other ticker remains 1,003.",
            ],
        ),
        (
            "Execution Scope",
            [
                "Transparent research-only rule and state tagging; no backtest, model, "
                "performance metric, recommendation, runtime, or trading action."
            ],
        ),
        ("Selected VPA/Wyckoff Package", [artifact["selected_vpa_wyckoff_package"]]),
        (
            "Source Matrix Inputs",
            [
                f"{artifact['source_matrix_row_count']} streamed matrix rows; source "
                f"digest `{artifact['source_matrix_rows_digest']}`."
            ],
        ),
        ("Rule Threshold Policy", [artifact["rule_threshold_policy"]]),
        ("Executed Rule Families", list(SELECTED_RULE_FAMILY_IDS)),
        ("Executed Wyckoff State Families", list(SELECTED_STATE_FAMILY_IDS)),
        (
            "Rule Values Output",
            [
                f"{artifact['rule_value_row_count']} rows; digest "
                f"`{artifact['vpa_wyckoff_rule_values_digest']}`."
            ],
        ),
        (
            "State Values Output",
            [f"{artifact['state_value_row_count']} state-tag rows."],
        ),
        (
            "No-Peek and Leakage Controls",
            [
                f"{field}: {value}."
                for field, value in artifact["rule_output_schema_validation"].items()
            ],
        ),
        (
            "Coverage Report",
            [
                f"{artifact['rule_family_reference_count']} rule references and "
                f"{artifact['state_family_reference_count']} state references; "
                "coverage is descriptive, not a performance metric."
            ],
        ),
        (
            "Per-Ticker Report",
            [
                f"{row['ticker']}: records {row['historical_record_count']}, rule/state "
                f"rows {row['rule_value_row_count']}/{row['state_value_row_count']}, "
                f"digest `{row['per_ticker_vpa_wyckoff_rule_baseline_execution_digest']}`."
                for row in artifact[
                    "per_ticker_vpa_wyckoff_rule_baseline_execution_entries"
                ]
            ],
        ),
        (
            "META Limitation",
            ["META's exact 913-record and 13,695-row limitation remains preserved."],
        ),
        (
            "Output Digest Manifest",
            [
                f"{row['filename']}: {row['digest_kind']} / {row['sha256']}."
                for row in artifact["output_digest_manifest"]
            ],
        ),
        ("Next Chain", artifact["next_chain"]),
        ("Next Gates", artifact["next_gates"]),
        ("Risk Controls", artifact["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        (
            "Runtime Boundary",
            [
                "Runtime, strategy, paper trading, and broker execution remain "
                "NOT_AUTHORIZED."
            ],
        ),
        (
            "Checklist Summary",
            [
                f"{artifact['execution_summary']['passed_checks']}/"
                f"{artifact['execution_summary']['total_checks']} checks pass with zero blockers."
            ],
        ),
        (
            "Guardrails",
            [
                "Target outcomes and future-looking fields are absent; outputs are "
                "research-only, non-actionable, and ignored by Git."
            ],
        ),
    ]
    lines = ["# VPA/Wyckoff Rule Baseline Execution v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", "", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines).rstrip() + "\n"
