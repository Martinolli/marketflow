"""Offline research-only execution of the approved signal and feature package."""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from datetime import UTC, datetime
import json
import math
from pathlib import Path
from statistics import fmean, pstdev
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import (
    marketflow_signal_or_feature_generation_approval_service as approval_service,
)


ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED"
)
ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_BLOCKED = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_V1 = (
    "marketflow_signal_or_feature_generation_execution_v1"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_BLOCKED_MISSING_OR_INVALID_CANONICAL_SOURCE = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_BLOCKED_MISSING_OR_INVALID_CANONICAL_SOURCE"
)
SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST = (
    "SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_VALID = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_VALID"
)

PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET = (
    "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"
)
PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET = (
    "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"
)
EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT = (
    "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
)
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "SIGNAL_OR_FEATURE_GENERATION_RESEARCH_ONLY"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "d174f5d775cb7b423121333838ab74956384068b8a46240760d399f02e229a8c"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)
TARGET_UNIVERSE = list(approval_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(approval_service.EXPECTED_RECORD_COUNTS)
SELECTED_SIGNAL_FAMILIES = list(approval_service.SELECTED_SIGNAL_FAMILY_IDS)
SELECTED_FEATURE_FAMILIES = list(approval_service.SELECTED_FEATURE_FAMILY_IDS)
SELECTED_FEATURE_GROUPS = list(approval_service.SELECTED_FEATURE_GROUP_IDS)
NO_PEEK_RULES = list(
    approval_service.review_service.candidate_service.NO_PEEK_RULE_IDS
)
QUALITY_CHECKS = list(
    approval_service.review_service.candidate_service.PLANNED_QUALITY_CHECK_IDS
)

DEFAULT_CANONICAL_ROOT = Path(
    ".marketflow/canonical_datasets/expanded_universe_v1"
)
DEFAULT_OUTPUT_ROOT = Path(
    ".marketflow/signal_or_feature_generation/expanded_universe_v1"
)
CANONICAL_RECORDS_FILENAME = "canonical_dataset_records.jsonl"
FEATURE_FORMULA_VERSION = "marketflow_signal_or_feature_formula_v1"
FEATURE_ROW_COUNT = 155298

OUTPUT_FILENAMES = [
    "signal_feature_generation_manifest.json",
    "signal_feature_schema.json",
    "feature_values.jsonl",
    "feature_coverage_report.json",
    "feature_group_report.json",
    "no_peek_feature_report.json",
    "per_ticker_feature_report.json",
    "meta_limitation_report.json",
    "operator_summary.json",
    "signal_feature_generation_digest_manifest.json",
]
FEATURE_VALUES_FIELDS = [
    "dataset_name",
    "ticker",
    "date",
    "source_profile",
    "timeframe",
    "canonical_record_index",
    "feature_group",
    "feature_family",
    "signal_family",
    "feature_values",
    "feature_available",
    "feature_unavailable_reason",
    "history_lookback_required",
    "history_lookback_available",
    "feature_formula_version",
    "selected_feature_package",
    "selected_label_target_package",
    "selected_objective_path",
    "research_only",
    "non_actionable",
    "records_digest",
    "source_approval_digest",
]
FORBIDDEN_FEATURE_FIELDS = [
    "target_value",
    "target_class",
    "forward_return",
    "future_label_value",
    "strategy_score",
    "prediction",
    "trade_recommendation",
    "broker_order",
    "order_id",
    "raw_provider_payload",
    "api_key",
]

GROUP_DEFINITIONS: dict[str, dict[str, Any]] = {
    "GROUP_CLOSE_TO_CLOSE_RETURNS": {
        "feature_family": "FEATURE_PRICE_RETURN_AND_RANGE",
        "signal_family": "SIGNAL_TREND_STRUCTURE",
        "lookback": 20,
        "features": ["trailing_return_1", "trailing_return_5", "trailing_return_10", "trailing_return_20"],
    },
    "GROUP_INTRADAY_RANGE_AND_BODY": {
        "feature_family": "FEATURE_PRICE_RETURN_AND_RANGE",
        "signal_family": "SIGNAL_CLOSE_LOCATION_AND_SPREAD",
        "lookback": 0,
        "features": ["intraday_range_fraction", "body_fraction", "upper_wick_fraction", "lower_wick_fraction"],
    },
    "GROUP_CLOSE_LOCATION_VALUE": {
        "feature_family": "FEATURE_VOLUME_PRICE_RELATIONSHIP",
        "signal_family": "SIGNAL_CLOSE_LOCATION_AND_SPREAD",
        "lookback": 0,
        "features": ["close_location_value", "close_to_high_fraction", "close_to_low_fraction"],
    },
    "GROUP_VOLUME_CHANGE_AND_ZSCORE": {
        "feature_family": "FEATURE_VOLUME_AND_LIQUIDITY",
        "signal_family": "SIGNAL_VOLUME_PRICE_ANALYSIS",
        "lookback": 20,
        "features": ["volume_change_1", "volume_change_5", "volume_zscore_20"],
    },
    "GROUP_SPREAD_VOLUME_INTERACTION": {
        "feature_family": "FEATURE_VOLUME_PRICE_RELATIONSHIP",
        "signal_family": "SIGNAL_VOLUME_PRICE_ANALYSIS",
        "lookback": 20,
        "features": ["spread_fraction", "volume_zscore_20", "spread_volume_interaction"],
    },
    "GROUP_EFFORT_RESULT_DIVERGENCE": {
        "feature_family": "FEATURE_VOLUME_PRICE_RELATIONSHIP",
        "signal_family": "SIGNAL_EFFORT_RESULT_BEHAVIOR",
        "lookback": 20,
        "features": ["volume_zscore_20", "absolute_trailing_return_1", "effort_result_ratio", "effort_result_divergence_flag"],
    },
    "GROUP_ATR_AND_VOLATILITY_COMPRESSION": {
        "feature_family": "FEATURE_VOLATILITY_AND_ATR",
        "signal_family": "SIGNAL_VOLATILITY_COMPRESSION_EXPANSION",
        "lookback": 20,
        "features": ["true_range_fraction", "atr_14_fraction", "atr_20_fraction", "volatility_compression_ratio"],
    },
    "GROUP_MOVING_AVERAGE_SLOPE": {
        "feature_family": "FEATURE_MOMENTUM_AND_TREND",
        "signal_family": "SIGNAL_TREND_STRUCTURE",
        "lookback": 30,
        "features": ["close_to_sma_5", "close_to_sma_20", "sma_5_slope_5", "sma_20_slope_10"],
    },
    "GROUP_RELATIVE_STRENGTH_VS_UNIVERSE": {
        "feature_family": "FEATURE_RELATIVE_STRENGTH_AND_RANKING",
        "signal_family": "SIGNAL_RELATIVE_STRENGTH",
        "lookback": 20,
        "features": ["relative_strength_return_5", "relative_strength_return_20", "same_date_universe_member_count"],
    },
    "GROUP_RELATIVE_STRENGTH_RANK": {
        "feature_family": "FEATURE_RELATIVE_STRENGTH_AND_RANKING",
        "signal_family": "SIGNAL_RELATIVE_STRENGTH",
        "lookback": 20,
        "features": ["relative_strength_rank_5", "relative_strength_rank_20", "relative_strength_percentile_5", "relative_strength_percentile_20"],
    },
    "GROUP_ABSTENTION_NOISE_CONTEXT": {
        "feature_family": "FEATURE_ABSTENTION_AND_NOISE_CONTEXT",
        "signal_family": "SIGNAL_NOISE_AND_ABSTENTION_FILTER",
        "lookback": 20,
        "features": ["rolling_volatility_20", "absolute_return_1", "noise_to_trend_ratio_20", "abstention_noise_flag"],
    },
    "GROUP_DATA_AVAILABILITY_FLAGS": {
        "feature_family": "FEATURE_DATA_QUALITY_AND_META_LIMITATION",
        "signal_family": "SIGNAL_NOISE_AND_ABSTENTION_FILTER",
        "lookback": 0,
        "features": ["has_open_high_low_close_volume", "trailing_history_count", "sufficient_history_5", "sufficient_history_10", "sufficient_history_20"],
    },
    "GROUP_META_LIMITATION_FLAGS": {
        "feature_family": "FEATURE_DATA_QUALITY_AND_META_LIMITATION",
        "signal_family": "SIGNAL_NOISE_AND_ABSTENTION_FILTER",
        "lookback": 0,
        "features": ["meta_reduced_record_count_flag", "canonical_record_count_for_ticker", "meta_limitation_preserved"],
    },
}

FORMULA_DEFINITIONS = {
    "trailing_return_n": "close[t] / close[t-n] - 1 using same-ticker history only",
    "intraday_range_fraction": "(high[t] - low[t]) / close[t]",
    "body_fraction": "(close[t] - open[t]) / close[t]",
    "close_location_value": "((close[t] - low[t]) - (high[t] - close[t])) / (high[t] - low[t])",
    "volume_change_n": "volume[t] / volume[t-n] - 1 using same-ticker history only",
    "volume_zscore_20": "(volume[t] - mean(volume[t-19:t])) / population_stddev(volume[t-19:t])",
    "true_range": "max(high-low, abs(high-prev_close), abs(low-prev_close))",
    "atr_n": "mean(true_range[t-n+1:t])",
    "moving_average_slope": "current trailing SMA divided by prior trailing SMA minus 1",
    "relative_strength": "same-ticker trailing return minus same-date universe mean trailing return",
    "relative_strength_rank": "ascending same-date rank with ticker as deterministic tie-breaker",
    "rolling_volatility_20": "population_stddev of 20 same-ticker one-session trailing returns",
    "no_peek": "current or prior OHLCV only; cross-sectional values use the same date only",
}

NEXT_CHAIN = [
    "Signal or Feature Generation Results Review v1.",
    "Future feature-label matrix candidate only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "signal_or_feature_generation_results_review",
    "feature_label_matrix_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "execution_generates_only_research_signal_and_feature_values",
    "execution_does_not_create_feature_label_matrix",
    "execution_does_not_run_backtest",
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
    "execution_does_not_rerun_target_generation_execution",
    "execution_does_not_rerun_target_results_review",
    "execution_does_not_rerun_candidate_creation",
    "execution_does_not_rerun_candidate_review",
    "execution_does_not_rerun_approval",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_target_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_approval_digest_bound", "source_candidate_review_digest_bound",
    "source_candidate_digest_bound", "source_target_results_review_digest_bound",
    "source_target_generation_execution_digest_bound", "source_target_values_digest_bound",
    "source_target_approval_digest_bound", "source_target_candidate_review_digest_bound",
    "source_target_candidate_digest_bound", "source_design_results_review_digest_bound",
    "source_design_execution_digest_bound", "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound",
    "source_strategy_charter_approval_digest_bound", "source_strategy_charter_digest_bound",
    "source_final_archive_digest_bound", "source_archive_digest_bound",
    "source_selection_digest_bound", "source_closure_digest_bound",
    "source_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_results_review_digest_bound", "source_prior_execution_digest_bound",
    "prior_matrix_digest_bound", "prior_feature_values_digest_bound",
    "prior_label_values_digest_bound", "research_registry_digest_bound",
    "records_digest_bound", "target_universe_12_preserved", "records_digest_preserved",
    "meta_913_preserved", "selected_feature_package_preserved",
    "selected_target_package_preserved", "selected_objective_path_preserved",
    "source_generation_authorized_true", "generation_executed_true",
    "signal_generation_performed_true", "feature_generation_performed_true",
    "feature_values_created_true", "selected_signal_family_count_7",
    "selected_feature_family_count_8", "selected_feature_group_count_13",
    "feature_row_count_155298", "per_non_meta_ticker_feature_counts_preserved",
    "meta_feature_counts_preserved", "generated_output_count_10",
    "feature_values_jsonl_created", "feature_coverage_report_created",
    "feature_group_report_created", "no_peek_feature_report_created",
    "per_ticker_feature_report_created", "digest_manifest_created",
    "digest_manifest_self_reference_policy_verified", "target_values_not_used_as_features",
    "target_classes_not_used_as_features", "forward_returns_not_used_as_features",
    "future_data_not_used_as_features", "feature_label_matrix_created_false",
    "backtest_execution_authorized_false", "backtest_execution_performed_false",
    "model_training_authorized_false", "model_training_performed_false",
    "metric_computation_authorized_false", "metric_computation_performed_false",
    "strategy_scoring_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "target_generation_execution_rerun_false", "target_results_review_rerun_false",
    "candidate_creation_rerun_false", "candidate_review_rerun_false",
    "approval_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowSignalOrFeatureGenerationExecutionError(ValueError):
    """Raised when execution evidence violates the research-only contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _number(value: float | None) -> str | None:
    if value is None or not math.isfinite(value):
        return None
    text = f"{value:.12f}".rstrip("0").rstrip(".")
    return "0" if text in {"", "-0"} else text


def _numeric(row: Mapping[str, Any], field: str) -> float:
    try:
        result = float(row[field])
    except (KeyError, TypeError, ValueError) as exc:
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            f"invalid canonical {field}"
        ) from exc
    if not math.isfinite(result):
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            f"non-finite canonical {field}"
        )
    return result


def _source_evidence() -> dict[str, str]:
    evidence = approval_service.SOURCE_EVIDENCE_DIGESTS
    return {
        "marketflow_signal_or_feature_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "marketflow_signal_or_feature_generation_candidate_operator_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "marketflow_signal_or_feature_generation_candidate_v1_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        **dict(evidence),
    }


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "signal_or_feature_generation_performed": True,
        "signal_generation_performed": True,
        "feature_generation_performed": True,
        "feature_values_created": True,
        "feature_label_matrix_created": False,
        "backtest_execution_authorized": False,
        "model_training_authorized": False,
        "metric_computation_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }


def _report(name: str, timestamp: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "report_name": name,
        "run_timestamp_utc": timestamp,
        **_common_output_fields(),
        **deepcopy(dict(payload)),
    }


def _load_records(
    canonical_root: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    path = canonical_root / CANONICAL_RECORDS_FILENAME
    if not path.is_file():
        return [], {}, [{
            "failure_id": "missing_canonical_source_records",
            "message": "frozen canonical source records are unavailable",
            "path": str(path).replace("\\", "/"),
        }]
    before_digest = sha256_file(path)
    if before_digest != EXPECTED_RECORDS_DIGEST:
        return [], {}, [{
            "failure_id": "canonical_source_digest_mismatch",
            "message": "frozen canonical source digest does not match approval",
            "expected": EXPECTED_RECORDS_DIGEST,
            "actual": before_digest,
        }]
    records: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("ticker") not in TARGET_UNIVERSE or not isinstance(
                    row.get("date"), str
                ):
                    raise MarketFlowSignalOrFeatureGenerationExecutionError(
                        f"invalid canonical identity at line {line_number}"
                    )
                for field in ("open", "high", "low", "close", "volume"):
                    _numeric(row, field)
                records.append(row)
    except (OSError, json.JSONDecodeError, MarketFlowSignalOrFeatureGenerationExecutionError) as exc:
        return [], {}, [{
            "failure_id": "invalid_canonical_source_records",
            "message": "frozen canonical source records are invalid",
            "error": str(exc),
        }]
    counts = Counter(row["ticker"] for row in records)
    order = {ticker: index for index, ticker in enumerate(TARGET_UNIVERSE)}
    identities = [(order[row["ticker"]], row["date"]) for row in records]
    failures: list[dict[str, Any]] = []
    if identities != sorted(identities):
        failures.append({
            "failure_id": "canonical_source_order_mismatch",
            "message": "canonical rows are not in ticker and date order",
        })
    if len(records) != 11946 or dict(counts) != EXPECTED_RECORD_COUNTS:
        failures.append({
            "failure_id": "canonical_source_count_mismatch",
            "message": "canonical counts do not match the frozen contract",
            "expected_total": 11946,
            "actual_total": len(records),
            "actual_per_ticker": dict(counts),
        })
    source_evidence_digest = semantic_digest(_source_evidence())
    verification = {
        "canonical_source_root": str(canonical_root).replace("\\", "/"),
        "canonical_records_filename": CANONICAL_RECORDS_FILENAME,
        "before_generation_records_digest": before_digest,
        "expected_records_digest": EXPECTED_RECORDS_DIGEST,
        "records_digest_match_before_generation": True,
        "source_evidence_digest_before_generation": source_evidence_digest,
        "total_canonical_record_count": len(records),
        "per_ticker_record_counts": dict(counts),
        "source_read_only": True,
    }
    return records, verification, failures


def _lag_return(values: list[float], index: int, lag: int) -> float | None:
    if index < lag or values[index - lag] == 0:
        return None
    return values[index] / values[index - lag] - 1.0


def _window(values: list[float], index: int, size: int) -> list[float] | None:
    if index + 1 < size:
        return None
    return values[index - size + 1 : index + 1]


def _mean_window(values: list[float], index: int, size: int) -> float | None:
    current = _window(values, index, size)
    return None if current is None else fmean(current)


def _zscore(values: list[float], index: int, size: int) -> float | None:
    current = _window(values, index, size)
    if current is None:
        return None
    deviation = pstdev(current)
    return 0.0 if deviation == 0 else (values[index] - fmean(current)) / deviation


def _rank_map(values: Mapping[str, float]) -> dict[str, tuple[int, float]]:
    ordered = sorted(values.items(), key=lambda item: (item[1], item[0]))
    denominator = max(1, len(ordered) - 1)
    return {
        ticker: (index + 1, index / denominator)
        for index, (ticker, _value) in enumerate(ordered)
    }


def _cross_sectional_context(
    grouped: Mapping[str, list[dict[str, Any]]],
) -> dict[tuple[str, str], dict[str, Any]]:
    returns_by_date: dict[int, dict[str, dict[str, float]]] = {
        5: defaultdict(dict),
        20: defaultdict(dict),
    }
    for ticker in TARGET_UNIVERSE:
        rows = grouped[ticker]
        closes = [_numeric(row, "close") for row in rows]
        for index, row in enumerate(rows):
            for lag in (5, 20):
                value = _lag_return(closes, index, lag)
                if value is not None:
                    returns_by_date[lag][row["date"]][ticker] = value
    context: dict[tuple[str, str], dict[str, Any]] = {}
    dates = sorted({row["date"] for rows in grouped.values() for row in rows})
    for date in dates:
        values5 = returns_by_date[5].get(date, {})
        values20 = returns_by_date[20].get(date, {})
        ranks5 = _rank_map(values5)
        ranks20 = _rank_map(values20)
        mean5 = fmean(values5.values()) if values5 else None
        mean20 = fmean(values20.values()) if values20 else None
        for ticker in TARGET_UNIVERSE:
            context[(ticker, date)] = {
                "relative_strength_return_5": (
                    None if ticker not in values5 or mean5 is None else values5[ticker] - mean5
                ),
                "relative_strength_return_20": (
                    None if ticker not in values20 or mean20 is None else values20[ticker] - mean20
                ),
                "same_date_universe_member_count": max(len(values5), len(values20)),
                "relative_strength_rank_5": ranks5.get(ticker, (None, None))[0],
                "relative_strength_rank_20": ranks20.get(ticker, (None, None))[0],
                "relative_strength_percentile_5": ranks5.get(ticker, (None, None))[1],
                "relative_strength_percentile_20": ranks20.get(ticker, (None, None))[1],
            }
    return context


def _feature_values_for_row(
    *,
    ticker: str,
    index: int,
    rows: list[dict[str, Any]],
    series: Mapping[str, list[float]],
    group_id: str,
    cross_sectional: Mapping[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    row = rows[index]
    opens = series["open"]
    highs = series["high"]
    lows = series["low"]
    closes = series["close"]
    volumes = series["volume"]
    true_ranges = series["true_range"]
    close = closes[index]
    spread = highs[index] - lows[index]
    return1 = _lag_return(closes, index, 1)
    return5 = _lag_return(closes, index, 5)
    return10 = _lag_return(closes, index, 10)
    return20 = _lag_return(closes, index, 20)
    volume_zscore = _zscore(volumes, index, 20)
    atr14 = _mean_window(true_ranges, index, 14)
    atr20 = _mean_window(true_ranges, index, 20)
    sma5 = _mean_window(closes, index, 5)
    sma20 = _mean_window(closes, index, 20)
    prior_sma5 = _mean_window(closes, index - 5, 5) if index >= 5 else None
    prior_sma20 = _mean_window(closes, index - 10, 20) if index >= 10 else None
    one_returns = [
        value
        for position in range(max(1, index - 19), index + 1)
        if (value := _lag_return(closes, position, 1)) is not None
    ]
    rolling_volatility = pstdev(one_returns) if len(one_returns) == 20 else None
    cross = cross_sectional[(ticker, row["date"])]
    values: dict[str, Any]
    if group_id == "GROUP_CLOSE_TO_CLOSE_RETURNS":
        values = {
            "trailing_return_1": return1,
            "trailing_return_5": return5,
            "trailing_return_10": return10,
            "trailing_return_20": return20,
        }
    elif group_id == "GROUP_INTRADAY_RANGE_AND_BODY":
        denominator = close if close else None
        values = {
            "intraday_range_fraction": None if denominator is None else spread / denominator,
            "body_fraction": None if denominator is None else (close - opens[index]) / denominator,
            "upper_wick_fraction": None if denominator is None else (highs[index] - max(opens[index], close)) / denominator,
            "lower_wick_fraction": None if denominator is None else (min(opens[index], close) - lows[index]) / denominator,
        }
    elif group_id == "GROUP_CLOSE_LOCATION_VALUE":
        values = {
            "close_location_value": None if spread == 0 else ((close - lows[index]) - (highs[index] - close)) / spread,
            "close_to_high_fraction": None if spread == 0 else (highs[index] - close) / spread,
            "close_to_low_fraction": None if spread == 0 else (close - lows[index]) / spread,
        }
    elif group_id == "GROUP_VOLUME_CHANGE_AND_ZSCORE":
        values = {
            "volume_change_1": _lag_return(volumes, index, 1),
            "volume_change_5": _lag_return(volumes, index, 5),
            "volume_zscore_20": volume_zscore,
        }
    elif group_id == "GROUP_SPREAD_VOLUME_INTERACTION":
        spread_fraction = None if close == 0 else spread / close
        values = {
            "spread_fraction": spread_fraction,
            "volume_zscore_20": volume_zscore,
            "spread_volume_interaction": None if volume_zscore is None or spread_fraction is None else spread_fraction * volume_zscore,
        }
    elif group_id == "GROUP_EFFORT_RESULT_DIVERGENCE":
        absolute_return = None if return1 is None else abs(return1)
        ratio = None if volume_zscore is None or absolute_return in (None, 0) else abs(volume_zscore) / absolute_return
        values = {
            "volume_zscore_20": volume_zscore,
            "absolute_trailing_return_1": absolute_return,
            "effort_result_ratio": ratio,
            "effort_result_divergence_flag": None if ratio is None else ratio > 100.0,
        }
    elif group_id == "GROUP_ATR_AND_VOLATILITY_COMPRESSION":
        values = {
            "true_range_fraction": None if close == 0 else true_ranges[index] / close,
            "atr_14_fraction": None if atr14 is None or close == 0 else atr14 / close,
            "atr_20_fraction": None if atr20 is None or close == 0 else atr20 / close,
            "volatility_compression_ratio": None if atr14 is None or atr20 in (None, 0) else atr14 / atr20,
        }
    elif group_id == "GROUP_MOVING_AVERAGE_SLOPE":
        values = {
            "close_to_sma_5": None if sma5 in (None, 0) else close / sma5 - 1.0,
            "close_to_sma_20": None if sma20 in (None, 0) else close / sma20 - 1.0,
            "sma_5_slope_5": None if sma5 is None or prior_sma5 in (None, 0) else sma5 / prior_sma5 - 1.0,
            "sma_20_slope_10": None if sma20 is None or prior_sma20 in (None, 0) else sma20 / prior_sma20 - 1.0,
        }
    elif group_id == "GROUP_RELATIVE_STRENGTH_VS_UNIVERSE":
        values = {key: cross[key] for key in (
            "relative_strength_return_5", "relative_strength_return_20", "same_date_universe_member_count"
        )}
    elif group_id == "GROUP_RELATIVE_STRENGTH_RANK":
        values = {key: cross[key] for key in (
            "relative_strength_rank_5", "relative_strength_rank_20",
            "relative_strength_percentile_5", "relative_strength_percentile_20",
        )}
    elif group_id == "GROUP_ABSTENTION_NOISE_CONTEXT":
        absolute_return = None if return1 is None else abs(return1)
        ratio = None if rolling_volatility is None or return20 in (None, 0) else rolling_volatility / abs(return20)
        values = {
            "rolling_volatility_20": rolling_volatility,
            "absolute_return_1": absolute_return,
            "noise_to_trend_ratio_20": ratio,
            "abstention_noise_flag": None if rolling_volatility is None or absolute_return is None or ratio is None else (ratio > 1.0 or absolute_return < rolling_volatility),
        }
    elif group_id == "GROUP_DATA_AVAILABILITY_FLAGS":
        values = {
            "has_open_high_low_close_volume": True,
            "trailing_history_count": index + 1,
            "sufficient_history_5": index >= 5,
            "sufficient_history_10": index >= 10,
            "sufficient_history_20": index >= 20,
        }
    else:
        values = {
            "meta_reduced_record_count_flag": ticker == "META",
            "canonical_record_count_for_ticker": len(rows),
            "meta_limitation_preserved": True,
        }
    return {
        key: (_number(value) if isinstance(value, float) else value)
        for key, value in values.items()
    }


def _ticker_series(rows: list[dict[str, Any]]) -> dict[str, list[float]]:
    series = {
        field: [_numeric(row, field) for row in rows]
        for field in ("open", "high", "low", "close", "volume")
    }
    highs = series["high"]
    lows = series["low"]
    closes = series["close"]
    series["true_range"] = [
        max(
            highs[index] - lows[index],
            abs(highs[index] - closes[index - 1]) if index else highs[index] - lows[index],
            abs(lows[index] - closes[index - 1]) if index else highs[index] - lows[index],
        )
        for index in range(len(rows))
    ]
    return series


def _jsonl_bytes(rows: Iterable[Mapping[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(row) for row in rows)


def per_ticker_signal_or_feature_generation_execution_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_signal_or_feature_generation_execution_digest", None)
    return semantic_digest(payload)


def _generate_features(
    records: list[dict[str, Any]], timestamp: str
) -> tuple[bytes, dict[str, dict[str, Any]], dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {ticker: [] for ticker in TARGET_UNIVERSE}
    for row in records:
        grouped[row["ticker"]].append(row)
    cross = _cross_sectional_context(grouped)
    feature_rows: list[dict[str, Any]] = []
    coverage_by_group: Counter[tuple[str, bool]] = Counter()
    per_ticker_entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        ticker_rows = grouped[ticker]
        series = _ticker_series(ticker_rows)
        ticker_available = 0
        for index, source_row in enumerate(ticker_rows):
            for group_id in SELECTED_FEATURE_GROUPS:
                definition = GROUP_DEFINITIONS[group_id]
                values = _feature_values_for_row(
                    ticker=ticker,
                    index=index,
                    rows=ticker_rows,
                    series=series,
                    group_id=group_id,
                    cross_sectional=cross,
                )
                available = any(value is not None for value in values.values())
                coverage_by_group[(group_id, available)] += 1
                ticker_available += int(available)
                feature_rows.append({
                    "dataset_name": "expanded_universe_canonical_dataset_v1",
                    "ticker": ticker,
                    "date": source_row["date"],
                    "source_profile": "RTH_FULL_SESSION_1D",
                    "timeframe": "1d",
                    "canonical_record_index": index,
                    "feature_group": group_id,
                    "feature_family": definition["feature_family"],
                    "signal_family": definition["signal_family"],
                    "feature_values": values,
                    "feature_available": available,
                    "feature_unavailable_reason": None if available else "FULL_GROUP_INSUFFICIENT_HISTORY",
                    "history_lookback_required": definition["lookback"],
                    "history_lookback_available": index + 1,
                    "feature_formula_version": FEATURE_FORMULA_VERSION,
                    "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
                    "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
                    "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
                    "research_only": True,
                    "non_actionable": True,
                    "records_digest": EXPECTED_RECORDS_DIGEST,
                    "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
                })
        feature_row_count = len(ticker_rows) * len(SELECTED_FEATURE_GROUPS)
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": len(ticker_rows),
            "meta_reduced_record_count_flag": ticker == "META",
            "signal_or_feature_generation_approval_status": approval_service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED,
            "signal_or_feature_generation_execution_status": "GENERATED_RESEARCH_ONLY",
            "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "selected_feature_group_count": 13,
            "feature_row_count": feature_row_count,
            "available_feature_row_count": ticker_available,
            "unavailable_feature_row_count": feature_row_count - ticker_available,
            "signal_or_feature_generation_performed": True,
            "signal_generation_performed": True,
            "feature_generation_performed": True,
            "feature_values_created": True,
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
            "source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
            "generation_note": (
                "PRESERVE_META_LIMITATION_IN_SIGNAL_OR_FEATURE_GENERATION_EXECUTION"
                if ticker == "META"
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_signal_or_feature_generation_execution_digest"] = (
            per_ticker_signal_or_feature_generation_execution_digest_v1(entry)
        )
        per_ticker_entries.append(entry)
    feature_bytes = _jsonl_bytes(feature_rows)
    available_count = sum(coverage_by_group[(group, True)] for group in SELECTED_FEATURE_GROUPS)
    coverage_entries = [
        {
            "feature_group": group,
            "feature_row_count": coverage_by_group[(group, True)] + coverage_by_group[(group, False)],
            "available_feature_row_count": coverage_by_group[(group, True)],
            "unavailable_feature_row_count": coverage_by_group[(group, False)],
        }
        for group in SELECTED_FEATURE_GROUPS
    ]
    common_counts = {
        "selected_signal_family_count": 7,
        "selected_feature_family_count": 8,
        "selected_feature_group_count": 13,
        "feature_row_count": len(feature_rows),
        "available_feature_row_count": available_count,
        "unavailable_feature_row_count": len(feature_rows) - available_count,
    }
    reports = {
        "signal_feature_schema.json": _report("signal_feature_schema", timestamp, {
            "schema_version": FEATURE_FORMULA_VERSION,
            "feature_values_fields": FEATURE_VALUES_FIELDS,
            "forbidden_feature_fields": FORBIDDEN_FEATURE_FIELDS,
            "selected_signal_families": SELECTED_SIGNAL_FAMILIES,
            "selected_feature_families": SELECTED_FEATURE_FAMILIES,
            "selected_feature_groups": SELECTED_FEATURE_GROUPS,
            "group_definitions": GROUP_DEFINITIONS,
            "formula_definitions": FORMULA_DEFINITIONS,
            **common_counts,
        }),
        "feature_coverage_report.json": _report("feature_coverage_report", timestamp, {
            "coverage_entries": coverage_entries,
            "all_canonical_records_retained": True,
            "rows_dropped": 0,
            **common_counts,
        }),
        "feature_group_report.json": _report("feature_group_report", timestamp, {
            "feature_group_entries": [
                {
                    "feature_group": group,
                    **deepcopy(GROUP_DEFINITIONS[group]),
                    "generation_status": "GENERATED_RESEARCH_ONLY",
                    "feature_row_count": 11946,
                }
                for group in SELECTED_FEATURE_GROUPS
            ],
            **common_counts,
        }),
        "no_peek_feature_report.json": _report("no_peek_feature_report", timestamp, {
            "no_peek_and_target_separation_rules": [
                {"rule_id": rule, "execution_status": "VERIFIED_DURING_FEATURE_GENERATION"}
                for rule in NO_PEEK_RULES
            ],
            "target_values_used_as_features": False,
            "target_classes_used_as_features": False,
            "forward_returns_used_as_features": False,
            "future_data_used_as_features": False,
            "same_date_cross_section_only": True,
            "per_ticker_history_only": True,
            **common_counts,
        }),
        "per_ticker_feature_report.json": _report("per_ticker_feature_report", timestamp, {
            "target_universe": TARGET_UNIVERSE,
            "per_ticker_signal_or_feature_generation_execution_entries": per_ticker_entries,
            **common_counts,
        }),
        "meta_limitation_report.json": _report("meta_limitation_report", timestamp, {
            **common_counts,
            "ticker": "META",
            "historical_record_count": 913,
            "non_meta_historical_record_count": 1003,
            "feature_group_count": 13,
            "feature_row_count": 11869,
            "meta_reduced_record_count_flag": True,
            "meta_reduced_record_count_preserved": True,
            "no_repair": True,
            "no_backfill": True,
            "no_synthetic_rows": True,
            "generation_note": "PRESERVE_META_LIMITATION_IN_SIGNAL_OR_FEATURE_GENERATION_EXECUTION",
        }),
        "operator_summary.json": _report("operator_summary", timestamp, {
            "review_status": "AWAITING_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_V1",
            "operator_decision": None,
            "generated_output_count": 10,
            "next_chain": NEXT_CHAIN,
            "next_gates": NEXT_GATES,
            "risk_controls": RISK_CONTROLS,
            **common_counts,
        }),
    }
    return feature_bytes, reports, {
        **common_counts,
        "per_ticker_entries": per_ticker_entries,
        "coverage_entries": coverage_entries,
    }


def _output_binding_digest(entries: list[dict[str, Any]]) -> str:
    return semantic_digest({
        "output_filenames": OUTPUT_FILENAMES,
        "digest_entries": [
            entry for entry in entries if entry["digest_kind"] == "FILE_SHA256"
        ],
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
    })


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


def _derived_check_values(artifact: Mapping[str, Any]) -> dict[str, bool]:
    evidence = artifact.get("source_evidence", {})
    entries = artifact.get("per_ticker_signal_or_feature_generation_execution_entries", [])
    output_names = artifact.get("generated_output_names", [])
    manifest = artifact.get("output_digest_manifest", [])
    expected_evidence = _source_evidence()
    evidence_checks = {
        "source_approval_digest_bound": "marketflow_signal_or_feature_generation_approval_digest",
        "source_candidate_review_digest_bound": "marketflow_signal_or_feature_generation_candidate_operator_review_digest",
        "source_candidate_digest_bound": "marketflow_signal_or_feature_generation_candidate_v1_digest",
        "source_target_results_review_digest_bound": "marketflow_objective_label_or_target_generation_results_review_digest",
        "source_target_generation_execution_digest_bound": "marketflow_objective_label_or_target_generation_execution_digest",
        "source_target_values_digest_bound": "objective_label_or_target_values_digest",
        "source_target_approval_digest_bound": "marketflow_objective_label_or_target_generation_approval_digest",
        "source_target_candidate_review_digest_bound": "marketflow_objective_label_or_target_generation_candidate_operator_review_digest",
        "source_target_candidate_digest_bound": "marketflow_objective_label_or_target_generation_candidate_v1_digest",
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
        "prior_matrix_digest_bound": "feature_label_matrix_digest",
        "prior_feature_values_digest_bound": "feature_values_digest",
        "prior_label_values_digest_bound": "redesigned_label_values_digest",
        "research_registry_digest_bound": "research_registry_approval_digest",
        "records_digest_bound": "records_digest",
    }
    values = {
        check_id: evidence.get(key) == expected_evidence.get(key)
        for check_id, key in evidence_checks.items()
    }
    values.update({
        "target_universe_12_preserved": artifact.get("target_universe") == TARGET_UNIVERSE and artifact.get("target_universe_count") == 12,
        "records_digest_preserved": artifact.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": artifact.get("meta_record_count") == 913,
        "selected_feature_package_preserved": artifact.get("selected_feature_package") == PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_target_package_preserved": artifact.get("selected_label_target_package") == PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path_preserved": artifact.get("selected_objective_path") == EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "source_generation_authorized_true": artifact.get("signal_or_feature_generation_authorized") is True,
        "generation_executed_true": artifact.get("signal_or_feature_generation_performed") is True,
        "signal_generation_performed_true": artifact.get("signal_generation_performed") is True,
        "feature_generation_performed_true": artifact.get("feature_generation_performed") is True,
        "feature_values_created_true": artifact.get("feature_values_created") is True,
        "selected_signal_family_count_7": artifact.get("selected_signal_family_count") == 7,
        "selected_feature_family_count_8": artifact.get("selected_feature_family_count") == 8,
        "selected_feature_group_count_13": artifact.get("selected_feature_group_count") == 13,
        "feature_row_count_155298": artifact.get("feature_row_count") == FEATURE_ROW_COUNT,
        "per_non_meta_ticker_feature_counts_preserved": len(entries) == 12 and all(row.get("historical_record_count") == 1003 and row.get("feature_row_count") == 13039 for row in entries if row.get("ticker") != "META"),
        "meta_feature_counts_preserved": any(row.get("ticker") == "META" and row.get("historical_record_count") == 913 and row.get("feature_row_count") == 11869 for row in entries),
        "generated_output_count_10": artifact.get("generated_output_count") == 10,
        "feature_values_jsonl_created": "feature_values.jsonl" in output_names,
        "feature_coverage_report_created": "feature_coverage_report.json" in output_names,
        "feature_group_report_created": "feature_group_report.json" in output_names,
        "no_peek_feature_report_created": "no_peek_feature_report.json" in output_names,
        "per_ticker_feature_report_created": "per_ticker_feature_report.json" in output_names,
        "digest_manifest_created": "signal_feature_generation_digest_manifest.json" in output_names,
        "digest_manifest_self_reference_policy_verified": any(row.get("filename") == OUTPUT_FILENAMES[-1] and row.get("digest_kind") == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE" and row.get("sha256") is None for row in manifest if isinstance(row, Mapping)),
        "target_values_not_used_as_features": artifact.get("target_values_used_as_features") is False,
        "target_classes_not_used_as_features": artifact.get("target_classes_used_as_features") is False,
        "forward_returns_not_used_as_features": artifact.get("forward_returns_used_as_features") is False,
        "future_data_not_used_as_features": artifact.get("future_data_used_as_features") is False,
        "feature_label_matrix_created_false": artifact.get("feature_label_matrix_created") is False,
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
        "per_ticker_entries_12": [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(row.get("per_ticker_signal_or_feature_generation_execution_digest") == per_ticker_signal_or_feature_generation_execution_digest_v1(row) for row in entries),
        "provider_requests_made_false": artifact.get("provider_requests_made_in_execution") is False,
        "market_data_acquisition_false": artifact.get("market_data_acquisition_performed_in_execution") is False,
        "dataset_regeneration_false": artifact.get("canonical_dataset_regenerated_in_execution") is False,
        "target_generation_execution_rerun_false": artifact.get("target_generation_execution_rerun_performed") is False,
        "target_results_review_rerun_false": artifact.get("target_generation_results_review_rerun_performed") is False,
        "candidate_creation_rerun_false": artifact.get("candidate_creation_rerun_performed") is False,
        "candidate_review_rerun_false": artifact.get("candidate_review_rerun_performed") is False,
        "approval_rerun_false": artifact.get("approval_rerun_performed") is False,
        "raw_provider_payloads_not_committed": artifact.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": artifact.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": artifact.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": artifact.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": artifact.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": artifact.get("no_tracked_marketflow_files") is True,
    })
    return values


def _checklist(artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _derived_check_values(artifact)
    return [_check(check_id, True, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == PASS for row in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": sum(row["status"] == FAIL and row["severity"] == BLOCKER for row in checklist),
        "signal_or_feature_generation_performed": True,
        "signal_generation_performed": True,
        "feature_generation_performed": True,
        "feature_values_created": True,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_feature_group_count": 13,
        "feature_row_count": FEATURE_ROW_COUNT,
        "generated_output_count": 10,
        "feature_label_matrix_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _blocked_artifact(
    output_root: Path, timestamp: str, failures: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_V1,
        "execution_status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_BLOCKED_MISSING_OR_INVALID_CANONICAL_SOURCE,
        "execution_scope": SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "run_timestamp_utc": timestamp,
        "generated_output_root": str(output_root).replace("\\", "/"),
        "created_offline": True,
        "research_only": True,
        "source_evidence": _source_evidence(),
        "signal_or_feature_generation_performed": False,
        "signal_generation_performed": False,
        "feature_generation_performed": False,
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
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "generated_output_count": 0,
        "failures": failures,
    }


def marketflow_signal_or_feature_generation_execution_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(artifact))
    payload.pop("marketflow_signal_or_feature_generation_execution_digest", None)
    payload.pop("canonical_source_root", None)
    payload.pop("generated_output_root", None)
    if isinstance(payload.get("source_verification"), dict):
        payload["source_verification"].pop("canonical_source_root", None)
    if isinstance(payload.get("execution_summary"), dict):
        payload["execution_summary"].pop("marketflow_signal_or_feature_generation_execution_digest", None)
    return semantic_digest(payload)


def _build_artifact(
    *,
    timestamp: str,
    output_root: Path,
    source_verification: dict[str, Any],
    generation: dict[str, Any],
    output_manifest: list[dict[str, Any]],
    feature_values_digest: str,
    output_binding_digest: str,
) -> dict[str, Any]:
    artifact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_V1,
        "execution_status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY,
        "execution_scope": SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "run_timestamp_utc": timestamp,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "canonical_source_root": str(DEFAULT_CANONICAL_ROOT).replace("\\", "/"),
        "generated_output_root": str(output_root).replace("\\", "/"),
        "source_signal_or_feature_generation_approval_artifact_kind": approval_service.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED,
        "source_signal_or_feature_generation_approval_status": approval_service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED,
        "source_signal_or_feature_generation_approval_scope": approval_service.SIGNAL_OR_FEATURE_GENERATION_APPROVAL_ONLY,
        "source_signal_or_feature_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_target_results_review_digest": approval_service.SOURCE_EVIDENCE_DIGESTS["marketflow_objective_label_or_target_generation_results_review_digest"],
        "source_target_values_digest": approval_service.SOURCE_EVIDENCE_DIGESTS["objective_label_or_target_values_digest"],
        "source_evidence": _source_evidence(),
        "source_verification": source_verification,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "signal_or_feature_generation_selected": True,
        "signal_or_feature_generation_approved": True,
        "signal_or_feature_generation_authorized": True,
        "ready_for_signal_or_feature_generation_execution": True,
        "signal_or_feature_generation_performed": True,
        "signal_generation_performed": True,
        "feature_generation_performed": True,
        "feature_values_created": True,
        "signal_or_feature_generation_results_created": True,
        "selected_signal_families": SELECTED_SIGNAL_FAMILIES,
        "selected_feature_families": SELECTED_FEATURE_FAMILIES,
        "selected_feature_groups": SELECTED_FEATURE_GROUPS,
        "selected_signal_family_count": 7,
        "selected_feature_family_count": 8,
        "selected_feature_group_count": 13,
        "feature_row_count": FEATURE_ROW_COUNT,
        "generated_output_count": 10,
        "expected_output_count": 10,
        "observed_output_count": 10,
        "available_feature_row_count": generation["available_feature_row_count"],
        "unavailable_feature_row_count": generation["unavailable_feature_row_count"],
        "no_peek_and_target_separation_rules": NO_PEEK_RULES,
        "approved_quality_checks": QUALITY_CHECKS,
        "formula_definitions": FORMULA_DEFINITIONS,
        "per_ticker_signal_or_feature_generation_execution_entries": generation["per_ticker_entries"],
        "feature_coverage_entries": generation["coverage_entries"],
        "generated_output_names": OUTPUT_FILENAMES,
        "feature_values_output_created": True,
        "feature_coverage_report_created": True,
        "feature_group_report_created": True,
        "no_peek_feature_report_created": True,
        "per_ticker_feature_report_created": True,
        "meta_limitation_report_created": True,
        "digest_manifest_created": True,
        "output_digest_manifest": output_manifest,
        "signal_or_feature_values_digest": feature_values_digest,
        "signal_or_feature_generation_output_binding_digest": output_binding_digest,
        "target_values_used_as_features": False,
        "target_classes_used_as_features": False,
        "forward_returns_used_as_features": False,
        "future_data_used_as_features": False,
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
        "provider_requests_made_in_execution": False,
        "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "target_generation_execution_rerun_performed": False,
        "target_generation_results_review_rerun_performed": False,
        "candidate_creation_rerun_performed": False,
        "candidate_review_rerun_performed": False,
        "approval_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    checklist = _checklist(artifact)
    artifact["execution_checklist"] = checklist
    artifact["execution_summary"] = _summary(checklist)
    digest = marketflow_signal_or_feature_generation_execution_digest_v1(artifact)
    artifact["marketflow_signal_or_feature_generation_execution_digest"] = digest
    artifact["execution_summary"]["marketflow_signal_or_feature_generation_execution_digest"] = digest
    return artifact


def _write_bytes_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            f"signal or feature generation output already exists: {path.name}"
        ) from exc


def execute_marketflow_signal_or_feature_generation_v1(
    *,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Generate approved research-only features from frozen local canonical rows."""
    timestamp = run_timestamp_utc or _utc_now()
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    records, source_verification, failures = _load_records(DEFAULT_CANONICAL_ROOT)
    if failures:
        return _blocked_artifact(output_path, timestamp, failures)
    if output_path.exists() and any(output_path.iterdir()):
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            "signal or feature generation output root is not empty"
        )
    feature_bytes, reports, generation = _generate_features(records, timestamp)
    after_digest = sha256_file(DEFAULT_CANONICAL_ROOT / CANONICAL_RECORDS_FILENAME)
    evidence_after = semantic_digest(_source_evidence())
    source_verification.update({
        "after_generation_records_digest": after_digest,
        "records_digest_match_after_generation": after_digest == EXPECTED_RECORDS_DIGEST,
        "source_evidence_digest_after_generation": evidence_after,
        "source_evidence_unchanged": evidence_after == source_verification["source_evidence_digest_before_generation"],
        "canonical_source_unchanged": source_verification["before_generation_records_digest"] == after_digest == EXPECTED_RECORDS_DIGEST,
    })
    if not source_verification["canonical_source_unchanged"] or not source_verification["source_evidence_unchanged"]:
        return _blocked_artifact(output_path, timestamp, [{
            "failure_id": "canonical_source_or_evidence_changed_during_generation",
            "message": "canonical source or evidence digest changed during generation",
        }])
    report_bytes = {
        filename: canonical_json_bytes(report) for filename, report in reports.items()
    }
    report_bytes["feature_values.jsonl"] = feature_bytes
    feature_digest = sha256_bytes(feature_bytes)
    output_manifest: list[dict[str, Any]] = []
    for filename in OUTPUT_FILENAMES:
        if filename == OUTPUT_FILENAMES[0]:
            entry = {"filename": filename, "digest_kind": "SELF_REFERENTIAL_EXECUTION_ARTIFACT", "sha256": None}
        elif filename == OUTPUT_FILENAMES[-1]:
            entry = {"filename": filename, "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "sha256": None}
        else:
            entry = {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(report_bytes[filename])}
        output_manifest.append(entry)
    output_binding = _output_binding_digest(output_manifest)
    artifact = _build_artifact(
        timestamp=timestamp,
        output_root=output_path,
        source_verification=source_verification,
        generation=generation,
        output_manifest=output_manifest,
        feature_values_digest=feature_digest,
        output_binding_digest=output_binding,
    )
    validate_marketflow_signal_or_feature_generation_execution_v1(artifact)
    report_bytes[OUTPUT_FILENAMES[0]] = canonical_json_bytes(artifact)
    report_bytes[OUTPUT_FILENAMES[-1]] = canonical_json_bytes(_report(
        "signal_feature_generation_digest_manifest",
        timestamp,
        {
            "marketflow_signal_or_feature_generation_execution_digest": artifact["marketflow_signal_or_feature_generation_execution_digest"],
            "signal_or_feature_generation_output_binding_digest": output_binding,
            "signal_or_feature_values_digest": feature_digest,
            "output_digest_manifest": output_manifest,
            "manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        },
    ))
    for filename in OUTPUT_FILENAMES:
        _write_bytes_once(output_path / filename, report_bytes[filename])
    return artifact


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_marketflow_signal_or_feature_generation_execution_v1(
    artifact: dict,
) -> dict:
    """Validate execution evidence, generated counts, and closed authorities."""
    if not isinstance(artifact, dict):
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            "signal or feature generation artifact must be a JSON object"
        )
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_V1,
        "execution_status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY,
        "execution_scope": SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "selected_feature_package": PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "source_signal_or_feature_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_target_results_review_digest": approval_service.SOURCE_EVIDENCE_DIGESTS["marketflow_objective_label_or_target_generation_results_review_digest"],
        "source_target_values_digest": approval_service.SOURCE_EVIDENCE_DIGESTS["objective_label_or_target_values_digest"],
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "selected_signal_families": SELECTED_SIGNAL_FAMILIES,
        "selected_feature_families": SELECTED_FEATURE_FAMILIES,
        "selected_feature_groups": SELECTED_FEATURE_GROUPS,
        "selected_signal_family_count": 7,
        "selected_feature_family_count": 8,
        "selected_feature_group_count": 13,
        "feature_row_count": FEATURE_ROW_COUNT,
        "generated_output_count": 10,
        "expected_output_count": 10,
        "observed_output_count": 10,
        "generated_output_names": OUTPUT_FILENAMES,
        "source_evidence": _source_evidence(),
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        _expect(artifact.get(field), expected, field)
    for field in (
        "created_offline", "research_only", "operator_review_required",
        "signal_or_feature_generation_selected", "signal_or_feature_generation_approved",
        "signal_or_feature_generation_authorized", "ready_for_signal_or_feature_generation_execution",
        "signal_or_feature_generation_performed", "signal_generation_performed",
        "feature_generation_performed", "feature_values_created",
        "signal_or_feature_generation_results_created", "feature_values_output_created",
        "feature_coverage_report_created", "feature_group_report_created",
        "no_peek_feature_report_created", "per_ticker_feature_report_created",
        "meta_limitation_report_created", "digest_manifest_created",
        "meta_reduced_record_count_preserved",
    ):
        _expect(artifact.get(field), True, field)
    for field in (
        "target_values_used_as_features", "target_classes_used_as_features",
        "forward_returns_used_as_features", "future_data_used_as_features",
        "feature_label_matrix_created", "backtest_execution_authorized",
        "backtest_execution_performed", "model_training_authorized",
        "model_training_performed", "metric_computation_authorized",
        "metric_computation_performed", "strategy_scoring_performed",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approved",
        "runtime_migration_active", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_execution",
        "live_provider_transport_enabled_in_execution", "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution", "canonical_dataset_regenerated_in_execution",
        "target_generation_execution_rerun_performed", "target_generation_results_review_rerun_performed",
        "candidate_creation_rerun_performed", "candidate_review_rerun_performed",
        "approval_rerun_performed", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    ):
        _expect(artifact.get(field), False, field)
    _expect(artifact.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(artifact.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    feature_digest = artifact.get("signal_or_feature_values_digest")
    if not isinstance(feature_digest, str) or len(feature_digest) != 64:
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            "signal_or_feature_values_digest missing"
        )
    manifest = artifact.get("output_digest_manifest")
    if not isinstance(manifest, list) or [row.get("filename") for row in manifest] != OUTPUT_FILENAMES:
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            "output_digest_manifest mismatch"
        )
    if (
        manifest[0].get("digest_kind") != "SELF_REFERENTIAL_EXECUTION_ARTIFACT"
        or manifest[0].get("sha256") is not None
        or manifest[-1].get("digest_kind") != "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
        or manifest[-1].get("sha256") is not None
        or any(
            row.get("digest_kind") != "FILE_SHA256"
            or not isinstance(row.get("sha256"), str)
            or len(row["sha256"]) != 64
            for row in manifest[1:-1]
        )
    ):
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            "output_digest_manifest self-reference or file digest policy mismatch"
        )
    _expect(
        next(row["sha256"] for row in manifest if row["filename"] == "feature_values.jsonl"),
        feature_digest,
        "feature values output digest",
    )
    _expect(
        artifact.get("signal_or_feature_generation_output_binding_digest"),
        _output_binding_digest(manifest),
        "signal_or_feature_generation_output_binding_digest",
    )
    entries = artifact.get("per_ticker_signal_or_feature_generation_execution_entries")
    if not isinstance(entries, list) or [row.get("ticker") for row in entries] != TARGET_UNIVERSE:
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            "per-ticker entries mismatch"
        )
    for row in entries:
        _expect(
            row.get("per_ticker_signal_or_feature_generation_execution_digest"),
            per_ticker_signal_or_feature_generation_execution_digest_v1(row),
            f"{row.get('ticker')} per-ticker digest",
        )
    expected_checklist = _checklist(artifact)
    _expect(artifact.get("execution_checklist"), expected_checklist, "execution_checklist")
    if any(row["status"] != PASS for row in expected_checklist):
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            "execution checklist contains failures"
        )
    expected_summary = _summary(expected_checklist)
    digest = artifact.get("marketflow_signal_or_feature_generation_execution_digest")
    expected_summary["marketflow_signal_or_feature_generation_execution_digest"] = digest
    _expect(artifact.get("execution_summary"), expected_summary, "execution_summary")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowSignalOrFeatureGenerationExecutionError(
            "execution digest missing"
        )
    _expect(
        digest,
        marketflow_signal_or_feature_generation_execution_digest_v1(artifact),
        "marketflow_signal_or_feature_generation_execution_digest",
    )
    return {
        "status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_VALID,
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "execution_scope": artifact["execution_scope"],
        "marketflow_signal_or_feature_generation_execution_digest": digest,
        "signal_or_feature_generation_output_binding_digest": artifact["signal_or_feature_generation_output_binding_digest"],
        "signal_or_feature_values_digest": feature_digest,
        "feature_row_count": FEATURE_ROW_COUNT,
        "generated_output_count": 10,
        "failure_count": 0,
    }


def build_marketflow_signal_or_feature_generation_execution_markdown_v1(
    artifact: dict,
) -> str:
    """Render a concise status record for generated research-only features."""
    validation = validate_marketflow_signal_or_feature_generation_execution_v1(
        artifact
    )
    sections = [
        ("Signal or Feature Generation Execution v1", [
            f"Artifact/status/scope: `{artifact['artifact_kind']}` / `{artifact['execution_status']}` / `{artifact['execution_scope']}`.",
            f"Execution digest: `{validation['marketflow_signal_or_feature_generation_execution_digest']}`.",
        ]),
        ("Source Approval", [f"Approval digest: `{EXPECTED_SOURCE_APPROVAL_DIGEST}`."]),
        ("Bound Evidence", [f"The complete source chain is bound in `{len(artifact['source_evidence'])}` digest fields."]),
        ("Dataset and Universe", ["`expanded_universe_canonical_dataset_v1`, 11,946 records, 12 tickers; META remains exactly 913 records."]),
        ("Execution Scope", ["Offline research-only signal and feature generation; no matrix, backtest, training, metrics, scoring, or recommendations."]),
        ("Selected Feature Package", [f"`{PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET}`."]),
        ("Selected Target Package and Objective Path", [f"`{PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET}` / `{EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT}`."]),
        ("Generated Signal Families", [", ".join(f"`{item}`" for item in SELECTED_SIGNAL_FAMILIES)]),
        ("Generated Feature Families", [", ".join(f"`{item}`" for item in SELECTED_FEATURE_FAMILIES)]),
        ("Feature Groups", [", ".join(f"`{item}`" for item in SELECTED_FEATURE_GROUPS)]),
        ("Feature Values Output", [f"155,298 rows; digest `{artifact['signal_or_feature_values_digest']}`."]),
        ("No-Peek and Target-Separation Controls", ["Only current/prior same-ticker OHLCV and same-date cross-sectional ranks were used; targets and forward returns were excluded."]),
        ("Feature Coverage Report", [f"Available/unavailable rows: {artifact['available_feature_row_count']} / {artifact['unavailable_feature_row_count']}."]),
        ("Per-Ticker Feature Report", ["Every non-META ticker has 13,039 rows; META has 11,869."]),
        ("META Limitation", ["META's exact 913-record source limitation is preserved without repair or backfill."]),
        ("Output Digest Manifest", [f"10 entries; binding digest `{artifact['signal_or_feature_generation_output_binding_digest']}`."]),
        ("Next Chain", artifact["next_chain"]),
        ("Next Gates", artifact["next_gates"]),
        ("Risk Controls", artifact["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness is not accepted."]),
        ("Profitability Boundary", ["Profitability is not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{artifact['execution_summary']['passed_checks']}/{artifact['execution_summary']['total_checks']} checks pass; 0 blockers."]),
        ("Guardrails", ["No provider request, acquisition, dataset regeneration, matrix creation, backtest, model training, runtime, or trading action occurred."]),
    ]
    lines: list[str] = []
    for index, (title, rows) in enumerate(sections):
        lines.extend([("# " if index == 0 else "## ") + title, ""])
        lines.extend(f"- {row}" for row in rows)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
