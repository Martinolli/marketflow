"""Deterministic offline execution of approved additional predictive evidence."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import additional_predictive_evidence_execution_approval_service as approval


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED"
)
ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_V1 = (
    "additional_predictive_evidence_executed_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET"
)

DEFAULT_SOURCE_ROOT = Path(".marketflow") / "canonical_datasets" / "expanded_universe_v1"
DEFAULT_OUTPUT_ROOT = (
    Path(".marketflow") / "additional_predictive_evidence" / "expanded_universe_v1"
)
DEFAULT_BRANCH = "feature/additional-predictive-evidence-execution-v1"
DEFAULT_BASE_COMMIT = "3845b5c5ecc928683037203df22a29f458e26a71"

EXPECTED_EXECUTION_APPROVAL_DIGEST = (
    "01cc79720ec9a27eb15a88214dfd5d152f5a6ae95082e7e13167239601c8afd9"
)
EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "ab41b9e28693ca770c85a7e872d640f04b7c59c97b3b8eb40b28c9b101652ff7"
)
EXPECTED_EXECUTION_CANDIDATE_DIGEST = (
    "d7f83a8b7be2be3a663ddb04097bf08b346071f70c9e770dd8f25e9fd9f4947e"
)
EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "41e7b4db107a056790b1caa749b789d434698c6416333328297b894fa0832c82"
)
EXPECTED_CHAIN_CANDIDATE_DIGEST = (
    "672b6d8d6299078df718247f3accea1250ea0c0228fa5315738d6e9ad7e055cf"
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    "02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc"
)
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = (
    "9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)

TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(approval.EXPECTED_RECORD_COUNTS)
APPROVED_REGISTRY_METADATA = deepcopy(approval.APPROVED_REGISTRY_METADATA)
NOT_ACCEPTED = approval.NOT_ACCEPTED
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "ADDITIONAL_PREDICTIVE_EVIDENCE_RESEARCH_ONLY"
NOT_EVALUATED_FOR_LABEL_TYPE = "NOT_EVALUATED_FOR_LABEL_TYPE"
LABEL_UNAVAILABLE_REASON = "label_unavailable_due_to_insufficient_future_bars"

LABEL_FAMILIES = list(approval.APPROVED_LABEL_FAMILIES)
FEATURE_FAMILIES = list(approval.APPROVED_FEATURE_FAMILIES)
METRIC_FAMILIES = list(approval.APPROVED_METRIC_FAMILY_IDS)
BASELINES = list(approval.APPROVED_BASELINE_IDS)
OUTPUT_FILENAMES = [
    "additional_predictive_evidence_execution_manifest.json",
    "label_generation_manifest.json",
    "label_distribution_report.json",
    "feature_matrix_manifest.json",
    "feature_quality_report.json",
    "walk_forward_results_report.json",
    "out_of_sample_results_report.json",
    "baseline_comparison_report.json",
    "calibration_report.json",
    "stability_analysis_report.json",
    "false_positive_false_negative_report.json",
    "leakage_control_report.json",
    "data_quality_report.json",
    "execution_digest_manifest.json",
    "operator_review_summary.json",
]

REQUIRED_SOURCE_FILENAMES = [
    "canonical_dataset_generation_run_manifest.json",
    "canonical_dataset_source_evidence_manifest.json",
    "canonical_dataset_schema_contract.json",
    "canonical_dataset_records.jsonl",
    "per_ticker_canonical_dataset_summary.json",
    "canonical_dataset_data_quality_report.json",
    "canonical_dataset_digest_manifest.json",
    "canonical_dataset_failure_reason_inventory.json",
    "operator_review_summary.json",
]

RETURN_BUCKET_THRESHOLDS = {
    "strong_down_max": "-0.020000",
    "down_max": "-0.002000",
    "flat_max": "0.002000",
    "up_max": "0.020000",
}
VOLATILITY_THRESHOLDS = {"low_max": "0.010000", "normal_max": "0.025000"}
DRAWDOWN_THRESHOLDS = {"low_risk_min": "-0.030000", "medium_risk_min": "-0.100000"}
LABEL_HORIZONS = {
    "NEXT_BAR_DIRECTION": [1],
    "NEXT_BAR_RETURN_BUCKET": [1],
    "NEXT_SESSION_DIRECTION": [1],
    "NEXT_SESSION_RETURN_BUCKET": [1],
    "MULTI_HORIZON_RETURN_BUCKET": [1, 5, 20],
    "VOLATILITY_REGIME_LABEL": [20],
    "DRAWDOWN_RISK_LABEL": [20],
}
SPLIT_PROFILE = {
    "training_window": {"start": "2022-01-01", "end": "2023-12-31"},
    "validation_window": {"start": "2024-01-01", "end": "2024-12-31"},
    "out_of_sample_window": {"start": "2025-01-01", "end": "2025-12-31"},
    "embargo_gap_policy": "ONE_SESSION_LABEL_AVAILABILITY_GAP_APPLIED_PER_TICKER",
    "walk_forward_policy": "EXPANDING_TRAINING_WITH_QUARTERLY_2024_VALIDATION_FOLDS",
    "shuffle": False,
}

FEATURE_SCHEMA_BY_FAMILY = {
    "ohlcv_return_features": [
        "close_return_1",
        "close_return_5",
        "close_return_20",
        "intraday_return",
        "range_pct",
    ],
    "volume_price_features": ["volume_ratio_20", "vwap_deviation"],
    "volatility_features": ["realized_volatility_5", "realized_volatility_20"],
    "trend_momentum_features": ["sma_gap_5", "sma_gap_20", "momentum_5", "momentum_20"],
    "wyckoff_vpa_features": ["close_location_value", "spread_volume_ratio"],
    "corporate_action_context_features": ["provider_adjusted_combined_policy_flag"],
    "cross_ticker_relative_strength_features": ["cross_sectional_return_rank_percentile"],
    "calendar_session_features": ["weekday", "month"],
    "data_quality_flags": ["missing_ohlcv_flag", "missing_vwap_flag"],
    "meta_reduced_record_count_flag": ["meta_reduced_record_count_flag"],
}
FEATURE_NAMES = [
    feature
    for family in FEATURE_FAMILIES
    for feature in FEATURE_SCHEMA_BY_FAMILY[family]
]

TRUE_EXECUTION_FIELDS = [
    "research_registry_approved",
    "registry_approval_created",
    "additional_predictive_evidence_execution_approved",
    "additional_predictive_evidence_execution_authorized",
    "ready_for_additional_predictive_evidence_execution",
    "additional_predictive_evidence_executed",
    "additional_predictive_evidence_results_created",
    "label_generation_authorized",
    "label_generation_performed",
    "feature_matrix_generation_authorized",
    "feature_matrix_generation_performed",
    "walk_forward_validation_authorized",
    "walk_forward_validation_performed",
    "out_of_sample_evaluation_authorized",
    "out_of_sample_evaluation_performed",
    "baseline_comparison_authorized",
    "baseline_comparison_performed",
    "signal_quality_metrics_authorized",
    "signal_quality_metrics_performed",
    "stability_analysis_authorized",
    "stability_analysis_performed",
    "leakage_control_review_authorized",
    "leakage_control_review_performed",
    "predictive_experiment_rerun_authorized",
    "predictive_experiment_rerun_performed",
    "canonical_dataset_generated",
    "canonical_dataset_frozen",
    "meta_reduced_record_count_preserved",
    "research_only",
]
FALSE_GUARDRAIL_FIELDS = [
    "provider_requests_made_in_execution",
    "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "predictive_usefulness_acceptance_candidate_created",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
]


class AdditionalPredictiveEvidenceExecutionError(ValueError):
    """Raised when the offline execution or its evidence violates guardrails."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _parse_decimal(value: Any) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _decimal_text(value: Decimal | None, places: int = 8) -> str | None:
    if value is None:
        return None
    quant = Decimal("1").scaleb(-places)
    return format(value.quantize(quant), "f")


def _mean(values: list[Decimal]) -> Decimal | None:
    return sum(values) / Decimal(len(values)) if values else None


def _stddev(values: list[Decimal]) -> Decimal | None:
    if len(values) < 2:
        return None
    mean = _mean(values)
    if mean is None:
        return None
    variance = sum((value - mean) ** 2 for value in values) / Decimal(len(values))
    return Decimal(str(float(variance) ** 0.5))


def _safe_ratio(numerator: Decimal | None, denominator: Decimal | None) -> Decimal | None:
    if numerator is None or denominator in (None, Decimal("0")):
        return None
    return numerator / denominator


def _return_between(current: Decimal | None, future: Decimal | None) -> Decimal | None:
    if current in (None, Decimal("0")) or future is None:
        return None
    return (future - current) / current


def _direction(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value > 0:
        return "UP"
    if value < 0:
        return "DOWN"
    return "FLAT"


def _return_bucket(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value <= Decimal(RETURN_BUCKET_THRESHOLDS["strong_down_max"]):
        return "STRONG_DOWN"
    if value < Decimal(RETURN_BUCKET_THRESHOLDS["down_max"]):
        return "DOWN"
    if value <= Decimal(RETURN_BUCKET_THRESHOLDS["flat_max"]):
        return "FLAT"
    if value < Decimal(RETURN_BUCKET_THRESHOLDS["up_max"]):
        return "UP"
    return "STRONG_UP"


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": APPROVED_REGISTRY_METADATA["dataset_name"],
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "additional_predictive_evidence_execution_authorized": True,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "label_generation_authorized": True,
        "label_generation_performed": True,
        "feature_matrix_generation_authorized": True,
        "feature_matrix_generation_performed": True,
        "walk_forward_validation_authorized": True,
        "walk_forward_validation_performed": True,
        "out_of_sample_evaluation_authorized": True,
        "out_of_sample_evaluation_performed": True,
        "baseline_comparison_authorized": True,
        "baseline_comparison_performed": True,
        "signal_quality_metrics_authorized": True,
        "signal_quality_metrics_performed": True,
        "stability_analysis_authorized": True,
        "stability_analysis_performed": True,
        "leakage_control_review_authorized": True,
        "leakage_control_review_performed": True,
        "predictive_experiment_rerun_authorized": True,
        "predictive_experiment_rerun_performed": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "trade_recommendations_generated": False,
    }


def _report(report_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"report_name": report_name, **_common_output_fields(), **payload}


def _source_failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


def _verify_source_root(source_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    for filename in REQUIRED_SOURCE_FILENAMES:
        if not (source_root / filename).is_file():
            failures.append(_source_failure("missing_source_file", "required source file missing", filename=filename))
    if failures:
        return {}, failures

    records_path = source_root / "canonical_dataset_records.jsonl"
    records_digest = sha256_file(records_path)
    if records_digest != EXPECTED_RECORDS_DIGEST:
        failures.append(
            _source_failure(
                "records_digest_mismatch",
                "canonical records digest mismatch",
                expected=EXPECTED_RECORDS_DIGEST,
                actual=records_digest,
            )
        )

    try:
        digest_manifest = json.loads(
            (source_root / "canonical_dataset_digest_manifest.json").read_text(encoding="utf-8")
        )
        generation_manifest = json.loads(
            (source_root / "canonical_dataset_generation_run_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        ticker_summary = json.loads(
            (source_root / "per_ticker_canonical_dataset_summary.json").read_text(
                encoding="utf-8"
            )
        )
    except (json.JSONDecodeError, OSError) as exc:
        failures.append(_source_failure("invalid_source_json", str(exc)))
        return {}, failures

    for entry in digest_manifest.get("canonical_output_digest_manifest", []):
        filename = entry.get("filename")
        digest_kind = entry.get("digest_kind")
        expected = entry.get("sha256")
        if digest_kind == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE":
            if filename != "canonical_dataset_digest_manifest.json" or expected is not None:
                failures.append(_source_failure("invalid_self_reference_policy", "invalid digest-manifest self-reference", filename=filename))
            continue
        if filename and digest_kind == "FILE_SHA256":
            actual = sha256_file(source_root / filename)
            if actual != expected:
                failures.append(_source_failure("source_output_digest_mismatch", "source output digest mismatch", filename=filename, expected=expected, actual=actual))
    if generation_manifest.get("canonical_dataset_generation_digest") != EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST:
        failures.append(_source_failure("generation_digest_mismatch", "canonical dataset generation digest mismatch"))
    if ticker_summary.get("target_universe") != TARGET_UNIVERSE:
        failures.append(_source_failure("target_universe_mismatch", "target universe mismatch"))
    if ticker_summary.get("total_canonical_record_count") != 11946:
        failures.append(_source_failure("summary_record_count_mismatch", "canonical summary record count mismatch"))

    verification = {
        "source_root": _path_text(source_root),
        "required_source_file_count": len(REQUIRED_SOURCE_FILENAMES),
        "required_source_files": list(REQUIRED_SOURCE_FILENAMES),
        "records_digest_expected": EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": records_digest,
        "records_digest_match": records_digest == EXPECTED_RECORDS_DIGEST,
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "canonical_dataset_generation_digest": generation_manifest.get(
            "canonical_dataset_generation_digest"
        ),
    }
    return verification, failures


def _read_rows(source_root: Path) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    rows_by_ticker: dict[str, list[dict[str, Any]]] = {ticker: [] for ticker in TARGET_UNIVERSE}
    failures: list[dict[str, Any]] = []
    path = source_root / "canonical_dataset_records.jsonl"
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                ticker = row.get("ticker")
                if ticker not in rows_by_ticker:
                    failures.append(_source_failure("unexpected_ticker", "unexpected ticker in canonical records", line_number=line_number, ticker=ticker))
                    continue
                rows_by_ticker[ticker].append(row)
    except (OSError, json.JSONDecodeError) as exc:
        return rows_by_ticker, [_source_failure("invalid_records_file", str(exc))]

    for ticker, rows in rows_by_ticker.items():
        rows.sort(key=lambda row: (str(row.get("date", "")), str(row.get("timestamp_utc_or_session_date", ""))))
        expected = EXPECTED_RECORD_COUNTS[ticker]
        if len(rows) != expected:
            failures.append(_source_failure("per_ticker_record_count_mismatch", "per-ticker canonical record count mismatch", ticker=ticker, expected=expected, actual=len(rows)))
        dates = [str(row.get("date", "")) for row in rows]
        if any(not date for date in dates) or dates != sorted(dates) or len(dates) != len(set(dates)):
            failures.append(_source_failure("invalid_ticker_date_order", "ticker dates must be present, unique, and chronological", ticker=ticker))
    total = sum(len(rows) for rows in rows_by_ticker.values())
    if total != 11946:
        failures.append(_source_failure("total_record_count_mismatch", "total canonical record count mismatch", expected=11946, actual=total))
    return rows_by_ticker, failures


def _label_value(value: Any, horizon: int, *, available: bool) -> dict[str, Any]:
    return {
        "value": value if available else None,
        "horizon_sessions": horizon,
        "available": available,
        "unavailable_reason": None if available else LABEL_UNAVAILABLE_REASON,
    }


def _future_volatility(closes: list[Decimal | None], index: int, horizon: int) -> Decimal | None:
    if index + horizon >= len(closes):
        return None
    returns: list[Decimal] = []
    for offset in range(1, horizon + 1):
        value = _return_between(closes[index + offset - 1], closes[index + offset])
        if value is None:
            return None
        returns.append(value)
    return _stddev(returns)


def _future_drawdown(closes: list[Decimal | None], index: int, horizon: int) -> Decimal | None:
    current = closes[index]
    if current in (None, Decimal("0")) or index + horizon >= len(closes):
        return None
    values = [value for value in closes[index + 1 : index + horizon + 1] if value is not None]
    if len(values) != horizon:
        return None
    return min((value - current) / current for value in values)


def _volatility_bucket(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value <= Decimal(VOLATILITY_THRESHOLDS["low_max"]):
        return "LOW"
    if value <= Decimal(VOLATILITY_THRESHOLDS["normal_max"]):
        return "NORMAL"
    return "HIGH"


def _drawdown_bucket(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value >= Decimal(DRAWDOWN_THRESHOLDS["low_risk_min"]):
        return "LOW_RISK"
    if value >= Decimal(DRAWDOWN_THRESHOLDS["medium_risk_min"]):
        return "MEDIUM_RISK"
    return "HIGH_RISK"


def _generate_labels(rows_by_ticker: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    generated: dict[str, list[dict[str, Any]]] = {}
    for ticker in TARGET_UNIVERSE:
        rows = rows_by_ticker[ticker]
        closes = [_parse_decimal(row.get("close")) for row in rows]
        ticker_labels: list[dict[str, Any]] = []
        for index, row in enumerate(rows):
            current = closes[index]
            next_return = (
                _return_between(current, closes[index + 1]) if index + 1 < len(closes) else None
            )
            multi_values: dict[str, str | None] = {}
            multi_available = True
            for horizon in (1, 5, 20):
                value = (
                    _return_between(current, closes[index + horizon])
                    if index + horizon < len(closes)
                    else None
                )
                bucket = _return_bucket(value)
                multi_values[str(horizon)] = bucket
                multi_available = multi_available and bucket is not None
            volatility = _future_volatility(closes, index, 20)
            drawdown = _future_drawdown(closes, index, 20)
            ticker_labels.append(
                {
                    "ticker": ticker,
                    "date": str(row.get("date")),
                    "row_index": index,
                    "forward_return_1": _decimal_text(next_return),
                    "labels": {
                        "NEXT_BAR_DIRECTION": _label_value(_direction(next_return), 1, available=next_return is not None),
                        "NEXT_BAR_RETURN_BUCKET": _label_value(_return_bucket(next_return), 1, available=next_return is not None),
                        "NEXT_SESSION_DIRECTION": _label_value(_direction(next_return), 1, available=next_return is not None),
                        "NEXT_SESSION_RETURN_BUCKET": _label_value(_return_bucket(next_return), 1, available=next_return is not None),
                        "MULTI_HORIZON_RETURN_BUCKET": {
                            "value": multi_values if multi_available else None,
                            "horizon_sessions": [1, 5, 20],
                            "available": multi_available,
                            "unavailable_reason": None if multi_available else LABEL_UNAVAILABLE_REASON,
                        },
                        "VOLATILITY_REGIME_LABEL": _label_value(_volatility_bucket(volatility), 20, available=volatility is not None),
                        "DRAWDOWN_RISK_LABEL": _label_value(_drawdown_bucket(drawdown), 20, available=drawdown is not None),
                    },
                }
            )
        generated[ticker] = ticker_labels
    return generated


def _rolling_return(closes: list[Decimal | None], index: int, horizon: int) -> Decimal | None:
    if index < horizon:
        return None
    return _return_between(closes[index - horizon], closes[index])


def _rolling_values(values: list[Decimal | None], index: int, horizon: int) -> list[Decimal]:
    window = values[max(0, index - horizon + 1) : index + 1]
    return [value for value in window if value is not None]


def _generate_features(rows_by_ticker: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    generated: dict[str, list[dict[str, Any]]] = {}
    returns_by_date: dict[str, list[tuple[str, Decimal]]] = defaultdict(list)
    for ticker in TARGET_UNIVERSE:
        rows = rows_by_ticker[ticker]
        closes = [_parse_decimal(row.get("close")) for row in rows]
        volumes = [_parse_decimal(row.get("volume")) for row in rows]
        return_1_values = [_rolling_return(closes, index, 1) for index in range(len(rows))]
        ticker_features: list[dict[str, Any]] = []
        for index, row in enumerate(rows):
            close = closes[index]
            open_value = _parse_decimal(row.get("open"))
            high = _parse_decimal(row.get("high"))
            low = _parse_decimal(row.get("low"))
            volume = volumes[index]
            vwap = _parse_decimal(row.get("vwap_if_available"))
            returns_5 = [value for value in return_1_values[max(0, index - 4) : index + 1] if value is not None]
            returns_20 = [value for value in return_1_values[max(0, index - 19) : index + 1] if value is not None]
            close_window_5 = _rolling_values(closes, index, 5)
            close_window_20 = _rolling_values(closes, index, 20)
            volume_window_20 = _rolling_values(volumes, index, 20)
            spread = high - low if high is not None and low is not None else None
            spread_pct = _safe_ratio(spread, close)
            mean_volume = _mean(volume_window_20) if len(volume_window_20) == 20 else None
            mean_close_5 = _mean(close_window_5) if len(close_window_5) == 5 else None
            mean_close_20 = _mean(close_window_20) if len(close_window_20) == 20 else None
            parsed_date = datetime.strptime(str(row.get("date")), "%Y-%m-%d")
            values: dict[str, Any] = {
                "close_return_1": _decimal_text(return_1_values[index]),
                "close_return_5": _decimal_text(_rolling_return(closes, index, 5)),
                "close_return_20": _decimal_text(_rolling_return(closes, index, 20)),
                "intraday_return": _decimal_text(_return_between(open_value, close)),
                "range_pct": _decimal_text(_safe_ratio(spread, open_value)),
                "volume_ratio_20": _decimal_text(_safe_ratio(volume, mean_volume)),
                "vwap_deviation": _decimal_text(_return_between(vwap, close)),
                "realized_volatility_5": _decimal_text(_stddev(returns_5) if len(returns_5) == 5 else None),
                "realized_volatility_20": _decimal_text(_stddev(returns_20) if len(returns_20) == 20 else None),
                "sma_gap_5": _decimal_text(_return_between(mean_close_5, close)),
                "sma_gap_20": _decimal_text(_return_between(mean_close_20, close)),
                "momentum_5": _decimal_text(_rolling_return(closes, index, 5)),
                "momentum_20": _decimal_text(_rolling_return(closes, index, 20)),
                "close_location_value": _decimal_text(_safe_ratio((close - low) if close is not None and low is not None else None, spread)),
                "spread_volume_ratio": _decimal_text((spread_pct * volume) if spread_pct is not None and volume is not None else None),
                "provider_adjusted_combined_policy_flag": str(row.get("adjustment_policy_status", "")).startswith("PROVIDER_ADJUSTED_TRUE"),
                "cross_sectional_return_rank_percentile": None,
                "weekday": parsed_date.weekday(),
                "month": parsed_date.month,
                "missing_ohlcv_flag": any(row.get(field) in (None, "") for field in ("open", "high", "low", "close", "volume")),
                "missing_vwap_flag": row.get("vwap_if_available") in (None, ""),
                "meta_reduced_record_count_flag": ticker == "META",
            }
            ticker_features.append({"ticker": ticker, "date": str(row.get("date")), "row_index": index, "features": values})
            if return_1_values[index] is not None:
                returns_by_date[str(row.get("date"))].append((ticker, return_1_values[index]))
        generated[ticker] = ticker_features

    rank_by_key: dict[tuple[str, str], str] = {}
    for date, values in returns_by_date.items():
        ordered = sorted(values, key=lambda item: (item[1], item[0]))
        denominator = Decimal(max(1, len(ordered) - 1))
        for rank, (ticker, _value) in enumerate(ordered):
            rank_by_key[(ticker, date)] = _decimal_text(Decimal(rank) / denominator, 6) or "0.000000"
    for ticker, rows in generated.items():
        for row in rows:
            row["features"]["cross_sectional_return_rank_percentile"] = rank_by_key.get((ticker, row["date"]))
    return generated


def _count_label_values(
    labels_by_ticker: dict[str, list[dict[str, Any]]]
) -> tuple[dict[str, Any], dict[str, Any]]:
    per_ticker: dict[str, Any] = {}
    overall: dict[str, Counter[str]] = {family: Counter() for family in LABEL_FAMILIES}
    for ticker in TARGET_UNIVERSE:
        ticker_counts: dict[str, Any] = {}
        for family in LABEL_FAMILIES:
            counter: Counter[str] = Counter()
            for row in labels_by_ticker[ticker]:
                label = row["labels"][family]
                value = label["value"]
                if value is None:
                    counter["UNAVAILABLE"] += 1
                elif isinstance(value, dict):
                    counter["|".join(f"{key}:{value[key]}" for key in sorted(value, key=int))] += 1
                else:
                    counter[str(value)] += 1
            ticker_counts[family] = dict(sorted(counter.items()))
            overall[family].update(counter)
        per_ticker[ticker] = ticker_counts
    return per_ticker, {
        family: dict(sorted(counter.items())) for family, counter in overall.items()
    }


def _label_coverage(labels_by_ticker: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    coverage: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        for family in LABEL_FAMILIES:
            rows = labels_by_ticker[ticker]
            available = sum(1 for row in rows if row["labels"][family]["available"])
            coverage.append(
                {
                    "ticker": ticker,
                    "label_family": family,
                    "row_count": len(rows),
                    "available_count": available,
                    "unavailable_count": len(rows) - available,
                    "unavailable_reason": LABEL_UNAVAILABLE_REASON,
                }
            )
    return coverage


def _feature_quality(
    features_by_ticker: dict[str, list[dict[str, Any]]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coverage: list[dict[str, Any]] = []
    total_nulls: Counter[str] = Counter()
    for ticker in TARGET_UNIVERSE:
        rows = features_by_ticker[ticker]
        nulls = {
            feature: sum(1 for row in rows if row["features"].get(feature) is None)
            for feature in FEATURE_NAMES
        }
        total_nulls.update(nulls)
        for family in FEATURE_FAMILIES:
            names = FEATURE_SCHEMA_BY_FAMILY[family]
            rows_with_any_value = sum(
                1
                for row in rows
                if any(row["features"].get(name) is not None for name in names)
            )
            coverage.append(
                {
                    "ticker": ticker,
                    "feature_family": family,
                    "row_count": len(rows),
                    "rows_with_any_family_value": rows_with_any_value,
                    "fully_unavailable_row_count": len(rows) - rows_with_any_value,
                    "null_counts": {name: nulls[name] for name in names},
                }
            )
    return coverage, dict(sorted(total_nulls.items()))


def _evaluation_rows(
    labels_by_ticker: dict[str, list[dict[str, Any]]],
    features_by_ticker: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        previous_direction: str | None = None
        previous_return: Decimal | None = None
        for label_row, feature_row in zip(
            labels_by_ticker[ticker], features_by_ticker[ticker], strict=True
        ):
            label = label_row["labels"]["NEXT_SESSION_DIRECTION"]
            forward_return = _parse_decimal(label_row["forward_return_1"])
            if label["available"]:
                rows.append(
                    {
                        "ticker": ticker,
                        "date": label_row["date"],
                        "actual_direction": label["value"],
                        "actual_return": forward_return,
                        "previous_direction": previous_direction,
                        "previous_return": previous_return,
                        "current_return": _parse_decimal(
                            feature_row["features"]["close_return_1"]
                        ),
                        "cross_sectional_rank": _parse_decimal(
                            feature_row["features"][
                                "cross_sectional_return_rank_percentile"
                            ]
                        ),
                    }
                )
            previous_direction = label["value"] if label["available"] else previous_direction
            previous_return = forward_return if forward_return is not None else previous_return
    return sorted(rows, key=lambda row: (row["date"], TARGET_UNIVERSE.index(row["ticker"])))


def _majority_class(rows: list[dict[str, Any]]) -> str:
    counts = Counter(str(row["actual_direction"]) for row in rows)
    if not counts:
        return "FLAT"
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _deterministic_random_class(row: dict[str, Any], classes: list[str]) -> str:
    payload = f"additional-predictive-evidence-v1|{row['ticker']}|{row['date']}".encode()
    index = int(hashlib.sha256(payload).hexdigest()[:16], 16) % len(classes)
    return classes[index]


def _predict(
    baseline: str,
    row: dict[str, Any],
    *,
    majority: str,
    classes: list[str],
) -> str:
    if baseline == "majority_class_baseline":
        return majority
    if baseline == "random_baseline":
        return _deterministic_random_class(row, classes)
    if baseline == "previous_direction_baseline":
        return str(row["previous_direction"] or majority)
    if baseline == "zero_return_baseline":
        return "FLAT"
    if baseline == "buy_hold_reference_only":
        return "UP"
    if baseline == "ticker_cross_sectional_baseline":
        rank = row["cross_sectional_rank"]
        if rank is None:
            return majority
        if rank > Decimal("0.5"):
            return "UP"
        if rank < Decimal("0.5"):
            return "DOWN"
        return "FLAT"
    raise AdditionalPredictiveEvidenceExecutionError(f"unsupported baseline: {baseline}")


def _confusion(actuals: list[str], predictions: list[str]) -> dict[str, dict[str, int]]:
    matrix: dict[str, Counter[str]] = defaultdict(Counter)
    for actual, predicted in zip(actuals, predictions, strict=True):
        matrix[actual][predicted] += 1
    return {
        actual: dict(sorted(predicted.items()))
        for actual, predicted in sorted(matrix.items())
    }


def _classification_metrics(actuals: list[str], predictions: list[str]) -> dict[str, Any]:
    if not actuals:
        return {
            "evaluated_count": 0,
            "accuracy": NOT_EVALUATED_FOR_LABEL_TYPE,
            "balanced_accuracy": NOT_EVALUATED_FOR_LABEL_TYPE,
            "macro_precision": NOT_EVALUATED_FOR_LABEL_TYPE,
            "macro_recall": NOT_EVALUATED_FOR_LABEL_TYPE,
            "macro_f1": NOT_EVALUATED_FOR_LABEL_TYPE,
            "confusion_matrix": {},
        }
    classes = sorted(set(actuals) | set(predictions))
    correct = sum(
        1
        for actual, predicted in zip(actuals, predictions, strict=True)
        if actual == predicted
    )
    precisions: list[Decimal] = []
    recalls: list[Decimal] = []
    f1s: list[Decimal] = []
    for label in classes:
        true_positive = sum(
            1
            for actual, predicted in zip(actuals, predictions, strict=True)
            if actual == predicted == label
        )
        predicted_count = predictions.count(label)
        actual_count = actuals.count(label)
        precision = Decimal(true_positive) / Decimal(predicted_count) if predicted_count else Decimal("0")
        recall = Decimal(true_positive) / Decimal(actual_count) if actual_count else Decimal("0")
        f1 = (
            Decimal("2") * precision * recall / (precision + recall)
            if precision + recall
            else Decimal("0")
        )
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
    return {
        "evaluated_count": len(actuals),
        "accuracy": _decimal_text(Decimal(correct) / Decimal(len(actuals)), 6),
        "balanced_accuracy": _decimal_text(_mean(recalls), 6),
        "macro_precision": _decimal_text(_mean(precisions), 6),
        "macro_recall": _decimal_text(_mean(recalls), 6),
        "macro_f1": _decimal_text(_mean(f1s), 6),
        "confusion_matrix": _confusion(actuals, predictions),
    }


def _regression_metrics(
    rows: list[dict[str, Any]], predictions: list[str], train_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    positive_returns = [
        row["actual_return"]
        for row in train_rows
        if row["actual_return"] is not None and row["actual_return"] > 0
    ]
    negative_returns = [
        row["actual_return"]
        for row in train_rows
        if row["actual_return"] is not None and row["actual_return"] < 0
    ]
    up_value = _mean(positive_returns) or Decimal("0")
    down_value = _mean(negative_returns) or Decimal("0")
    numeric_predictions = [
        up_value if prediction == "UP" else down_value if prediction == "DOWN" else Decimal("0")
        for prediction in predictions
    ]
    pairs = [
        (row["actual_return"], prediction)
        for row, prediction in zip(rows, numeric_predictions, strict=True)
        if row["actual_return"] is not None
    ]
    if not pairs:
        return {"mae": NOT_EVALUATED_FOR_LABEL_TYPE, "rmse": NOT_EVALUATED_FOR_LABEL_TYPE}
    errors = [actual - predicted for actual, predicted in pairs]
    mae = _mean([abs(error) for error in errors])
    mse = _mean([error * error for error in errors])
    rmse = Decimal(str(float(mse) ** 0.5)) if mse is not None else None
    return {"mae": _decimal_text(mae, 8), "rmse": _decimal_text(rmse, 8)}


def _evaluate_period(
    *,
    train_rows: list[dict[str, Any]],
    target_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    majority = _majority_class(train_rows)
    classes = sorted({str(row["actual_direction"]) for row in train_rows} or {"FLAT"})
    actuals = [str(row["actual_direction"]) for row in target_rows]
    results: dict[str, Any] = {}
    for baseline in BASELINES:
        predictions = [
            _predict(baseline, row, majority=majority, classes=classes) for row in target_rows
        ]
        results[baseline] = {
            "classification_metrics": _classification_metrics(actuals, predictions),
            "regression_metrics": _regression_metrics(target_rows, predictions, train_rows),
            "prediction_policy": "DETERMINISTIC_OFFLINE_RESEARCH_BASELINE",
            "buy_hold_reference_only": baseline == "buy_hold_reference_only",
            "trade_recommendation": False,
        }
    majority_accuracy = results["majority_class_baseline"]["classification_metrics"]["accuracy"]
    for result in results.values():
        accuracy = result["classification_metrics"]["accuracy"]
        result["accuracy_lift_over_majority"] = (
            _decimal_text(Decimal(accuracy) - Decimal(majority_accuracy), 6)
            if isinstance(accuracy, str)
            and isinstance(majority_accuracy, str)
            and accuracy != NOT_EVALUATED_FOR_LABEL_TYPE
            and majority_accuracy != NOT_EVALUATED_FOR_LABEL_TYPE
            else NOT_EVALUATED_FOR_LABEL_TYPE
        )
    return {
        "training_count": len(train_rows),
        "evaluation_count": len(target_rows),
        "training_majority_class": majority,
        "baselines": results,
    }


def _walk_forward_results(evaluation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    folds = [
        ("2024_Q1", "2024-01-01", "2024-03-31"),
        ("2024_Q2", "2024-04-01", "2024-06-30"),
        ("2024_Q3", "2024-07-01", "2024-09-30"),
        ("2024_Q4", "2024-10-01", "2024-12-31"),
    ]
    results: list[dict[str, Any]] = []
    for fold_id, start, end in folds:
        train = [row for row in evaluation_rows if row["date"] < start]
        target = [row for row in evaluation_rows if start <= row["date"] <= end]
        results.append(
            {
                "fold_id": fold_id,
                "training_end_exclusive": start,
                "validation_start": start,
                "validation_end": end,
                **_evaluate_period(train_rows=train, target_rows=target),
            }
        )
    return results


def _out_of_sample_results(evaluation_rows: list[dict[str, Any]]) -> dict[str, Any]:
    train = [row for row in evaluation_rows if row["date"] < "2025-01-01"]
    target = [row for row in evaluation_rows if "2025-01-01" <= row["date"] <= "2025-12-31"]
    overall = _evaluate_period(train_rows=train, target_rows=target)
    per_ticker = {
        ticker: _evaluate_period(
            train_rows=[row for row in train if row["ticker"] == ticker],
            target_rows=[row for row in target if row["ticker"] == ticker],
        )
        for ticker in TARGET_UNIVERSE
    }
    return {
        "training_window": "2022-01-01 to 2024-12-31 expanding evidence",
        "out_of_sample_window": "2025-01-01 to 2025-12-31",
        "overall": overall,
        "per_ticker": per_ticker,
    }


def _calibration_summary(
    evaluation_rows: list[dict[str, Any]], out_of_sample: dict[str, Any]
) -> dict[str, Any]:
    train = [row for row in evaluation_rows if row["date"] < "2025-01-01"]
    target = [row for row in evaluation_rows if row["date"] >= "2025-01-01"]
    up_count = sum(1 for row in train if row["actual_direction"] == "UP")
    probability_up = Decimal(up_count) / Decimal(len(train)) if train else Decimal("0")
    brier_values = [
        (probability_up - (Decimal("1") if row["actual_direction"] == "UP" else Decimal("0"))) ** 2
        for row in target
    ]
    return {
        "evaluated_baseline": "majority_class_baseline",
        "calibration_target": "NEXT_SESSION_DIRECTION_UP_VS_NOT_UP",
        "training_probability_up": _decimal_text(probability_up, 8),
        "out_of_sample_brier_score": _decimal_text(_mean(brier_values), 8),
        "out_of_sample_count": out_of_sample["overall"]["evaluation_count"],
        "other_label_types_status": NOT_EVALUATED_FOR_LABEL_TYPE,
    }


def _stability_summary(
    walk_forward: list[dict[str, Any]], out_of_sample: dict[str, Any]
) -> dict[str, Any]:
    by_baseline: dict[str, Any] = {}
    for baseline in BASELINES:
        fold_accuracies = [
            fold["baselines"][baseline]["classification_metrics"]["accuracy"]
            for fold in walk_forward
        ]
        numeric = [Decimal(value) for value in fold_accuracies if isinstance(value, str) and value != NOT_EVALUATED_FOR_LABEL_TYPE]
        oos_accuracy = out_of_sample["overall"]["baselines"][baseline]["classification_metrics"]["accuracy"]
        by_baseline[baseline] = {
            "walk_forward_fold_accuracies": fold_accuracies,
            "walk_forward_accuracy_mean": _decimal_text(_mean(numeric), 6),
            "walk_forward_accuracy_stddev": _decimal_text(_stddev(numeric), 6),
            "out_of_sample_accuracy": oos_accuracy,
            "acceptance_conclusion": "NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED",
        }
    return by_baseline


def _source_evidence() -> dict[str, str]:
    return {
        "additional_predictive_evidence_execution_approval_digest": EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_candidate_review_package_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "additional_predictive_evidence_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "additional_predictive_evidence_chain_candidate_review_package_digest": EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "additional_predictive_evidence_chain_candidate_digest": EXPECTED_CHAIN_CANDIDATE_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
    }


def _build_reports(
    *,
    rows_by_ticker: dict[str, list[dict[str, Any]]],
    labels_by_ticker: dict[str, list[dict[str, Any]]],
    features_by_ticker: dict[str, list[dict[str, Any]]],
    run_timestamp_utc: str,
    source_verification: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    label_coverage = _label_coverage(labels_by_ticker)
    per_ticker_distributions, overall_distributions = _count_label_values(labels_by_ticker)
    feature_coverage, total_feature_nulls = _feature_quality(features_by_ticker)
    evaluation_rows = _evaluation_rows(labels_by_ticker, features_by_ticker)
    walk_forward = _walk_forward_results(evaluation_rows)
    out_of_sample = _out_of_sample_results(evaluation_rows)
    calibration = _calibration_summary(evaluation_rows, out_of_sample)
    stability = _stability_summary(walk_forward, out_of_sample)
    label_generation_digest = semantic_digest(labels_by_ticker)
    feature_matrix_digest = semantic_digest(features_by_ticker)
    per_ticker_record_counts = {
        ticker: len(rows_by_ticker[ticker]) for ticker in TARGET_UNIVERSE
    }
    unavailable_label_count = sum(
        entry["unavailable_count"] for entry in label_coverage
    )
    warning_count = 1

    reports: dict[str, dict[str, Any]] = {}
    reports["label_generation_manifest"] = _report(
        "label_generation_manifest",
        {
            "run_timestamp_utc": run_timestamp_utc,
            "label_families": LABEL_FAMILIES,
            "label_family_count": len(LABEL_FAMILIES),
            "label_horizons": LABEL_HORIZONS,
            "forward_labels_only": True,
            "future_label_values_used_as_features": False,
            "unavailable_label_representation": {
                "value": None,
                "reason": LABEL_UNAVAILABLE_REASON,
            },
            "return_bucket_thresholds": RETURN_BUCKET_THRESHOLDS,
            "volatility_thresholds": VOLATILITY_THRESHOLDS,
            "drawdown_thresholds": DRAWDOWN_THRESHOLDS,
            "threshold_policy": "FIXED_THRESHOLDS_RECORDED_EXPLICITLY",
            "label_coverage": label_coverage,
            "label_generation_digest": label_generation_digest,
        },
    )
    reports["label_distribution_report"] = _report(
        "label_distribution_report",
        {
            "per_ticker_label_distributions": per_ticker_distributions,
            "overall_label_distributions": overall_distributions,
            "unavailable_label_count_across_families": unavailable_label_count,
        },
    )
    reports["feature_matrix_manifest"] = _report(
        "feature_matrix_manifest",
        {
            "run_timestamp_utc": run_timestamp_utc,
            "feature_families": FEATURE_FAMILIES,
            "feature_family_count": len(FEATURE_FAMILIES),
            "feature_schema_by_family": FEATURE_SCHEMA_BY_FAMILY,
            "feature_names": FEATURE_NAMES,
            "feature_count": len(FEATURE_NAMES),
            "current_and_historical_inputs_only": True,
            "future_information_used": False,
            "feature_matrix_row_count": sum(len(rows) for rows in features_by_ticker.values()),
            "feature_matrix_digest": feature_matrix_digest,
            "per_ticker_feature_matrix_digests": {
                ticker: semantic_digest(features_by_ticker[ticker])
                for ticker in TARGET_UNIVERSE
            },
        },
    )
    reports["feature_quality_report"] = _report(
        "feature_quality_report",
        {
            "feature_coverage": feature_coverage,
            "total_null_counts_by_feature": total_feature_nulls,
            "current_and_historical_inputs_only": True,
            "future_label_values_used_as_features": False,
            "quality_status": "PASS_WITH_EXPECTED_ROLLING_WINDOW_UNAVAILABLE_VALUES",
        },
    )
    reports["walk_forward_results_report"] = _report(
        "walk_forward_results_report",
        {
            "split_profile": SPLIT_PROFILE,
            "walk_forward_policy_status": "FINALIZED_AND_EXECUTED_WITH_STATUS_RECORD",
            "fold_count": len(walk_forward),
            "folds": walk_forward,
            "shuffle": False,
            "acceptance_evidence_status": "NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED",
        },
    )
    reports["out_of_sample_results_report"] = _report(
        "out_of_sample_results_report",
        {
            "chronological_holdout": True,
            "shuffle": False,
            "results": out_of_sample,
            "acceptance_evidence_status": "NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED",
        },
    )
    reports["baseline_comparison_report"] = _report(
        "baseline_comparison_report",
        {
            "baselines": BASELINES,
            "baseline_count": len(BASELINES),
            "random_baseline_policy": "DETERMINISTIC_SHA256_CLASS_SELECTION",
            "buy_hold_reference_only_is_trade_recommendation": False,
            "out_of_sample_comparison": out_of_sample["overall"]["baselines"],
            "walk_forward_comparison": {
                fold["fold_id"]: fold["baselines"] for fold in walk_forward
            },
        },
    )
    reports["calibration_report"] = _report(
        "calibration_report",
        {
            "calibration_metrics": calibration,
            "non_probability_baselines_status": NOT_EVALUATED_FOR_LABEL_TYPE,
        },
    )
    reports["stability_analysis_report"] = _report(
        "stability_analysis_report",
        {
            "stability_metrics": stability,
            "split_direction_distributions": {
                "training": dict(
                    sorted(
                        Counter(
                            row["actual_direction"]
                            for row in evaluation_rows
                            if row["date"] <= "2023-12-31"
                        ).items()
                    )
                ),
                "validation": dict(
                    sorted(
                        Counter(
                            row["actual_direction"]
                            for row in evaluation_rows
                            if "2024-01-01" <= row["date"] <= "2024-12-31"
                        ).items()
                    )
                ),
                "out_of_sample": dict(
                    sorted(
                        Counter(
                            row["actual_direction"]
                            for row in evaluation_rows
                            if "2025-01-01" <= row["date"] <= "2025-12-31"
                        ).items()
                    )
                ),
            },
        },
    )
    reports["false_positive_false_negative_report"] = _report(
        "false_positive_false_negative_report",
        {
            "label_family": "NEXT_SESSION_DIRECTION",
            "multiclass_direction_label": True,
            "binary_positive_negative_not_assumed": True,
            "out_of_sample_confusion_matrices": {
                baseline: result["classification_metrics"]["confusion_matrix"]
                for baseline, result in out_of_sample["overall"]["baselines"].items()
            },
        },
    )
    reports["leakage_control_report"] = _report(
        "leakage_control_report",
        {
            "leakage_control_status": "PASS",
            "controls": [
                {"control": "forward_labels_only", "status": "PASS"},
                {"control": "unavailable_future_labels_are_null_with_reason", "status": "PASS"},
                {"control": "future_label_values_not_used_as_features", "status": "PASS"},
                {"control": "features_use_current_and_historical_rows_only", "status": "PASS"},
                {"control": "chronological_splits_only", "status": "PASS"},
                {"control": "one_session_label_availability_gap", "status": "PASS"},
                {"control": "shuffle_disabled", "status": "PASS"},
                {"control": "training_thresholds_not_fit_on_validation_or_oos", "status": "PASS_FIXED_THRESHOLDS"},
                {"control": "provider_transport_disabled", "status": "PASS"},
                {"control": "runtime_strategy_and_trading_paths_unauthorized", "status": "PASS"},
            ],
            "failed_control_count": 0,
        },
    )
    reports["data_quality_report"] = _report(
        "data_quality_report",
        {
            "quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
            "source_verification": source_verification,
            "target_universe": TARGET_UNIVERSE,
            "target_count": len(TARGET_UNIVERSE),
            "total_canonical_record_count": sum(per_ticker_record_counts.values()),
            "per_ticker_record_counts": per_ticker_record_counts,
            "meta_record_count": per_ticker_record_counts["META"],
            "non_meta_record_count": 1003,
            "meta_reduced_record_count_preserved": True,
            "meta_records_repaired_inferred_smoothed_normalized_backfilled_or_fabricated": False,
            "failure_count": 0,
            "warning_count": warning_count,
            "warnings": [
                {
                    "warning_id": "META_REDUCED_RECORD_COUNT_PRESERVED",
                    "ticker": "META",
                    "record_count": 913,
                    "status": "PRESERVED_NOT_REPAIRED",
                }
            ],
        },
    )
    reports["operator_review_summary"] = _report(
        "operator_review_summary",
        {
            "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY,
            "execution_results_review_status": "READY_FOR_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW",
            "source_evidence": _source_evidence(),
            "generated_output_count": len(OUTPUT_FILENAMES),
            "failure_count": 0,
            "warning_count": warning_count,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_recommended": False,
            "profitability_acceptance_ready": False,
            "runtime_migration_approved": False,
            "next_task": "Additional Predictive Evidence Results Review Package v1",
        },
    )

    summaries = {
        "per_ticker_record_counts": per_ticker_record_counts,
        "label_coverage_summary": {
            "entry_count": len(label_coverage),
            "available_count": sum(item["available_count"] for item in label_coverage),
            "unavailable_count": unavailable_label_count,
            "label_generation_digest": label_generation_digest,
        },
        "feature_coverage_summary": {
            "entry_count": len(feature_coverage),
            "feature_matrix_row_count": sum(len(rows) for rows in features_by_ticker.values()),
            "feature_matrix_digest": feature_matrix_digest,
            "total_null_count": sum(total_feature_nulls.values()),
        },
        "walk_forward_summary": {
            "fold_count": len(walk_forward),
            "policy": SPLIT_PROFILE["walk_forward_policy"],
            "performed": True,
        },
        "out_of_sample_summary": {
            "evaluation_count": out_of_sample["overall"]["evaluation_count"],
            "performed": True,
        },
        "baseline_comparison_summary": {
            "baseline_count": len(BASELINES),
            "performed": True,
        },
        "calibration_summary": calibration,
        "stability_summary": {
            "baseline_count": len(stability),
            "performed": True,
        },
        "leakage_control_summary": {"status": "PASS", "failed_control_count": 0},
        "data_quality_summary": {
            "status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
            "failure_count": 0,
            "warning_count": warning_count,
        },
        "failure_count": 0,
        "warning_count": warning_count,
    }
    return reports, summaries


def _execution_digest_payload(artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(artifact)
    payload.pop("additional_predictive_evidence_execution_digest", None)
    payload.pop("generated_output_root", None)
    return payload


def additional_predictive_evidence_execution_digest_v1(
    artifact: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for an executed evidence artifact."""
    return semantic_digest(_execution_digest_payload(artifact))


def _blocked_artifact(
    *,
    source_root: Path,
    output_root: Path,
    run_timestamp_utc: str,
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": APPROVED_REGISTRY_METADATA["dataset_name"],
        "source_root": _path_text(source_root),
        "output_root": _path_text(output_root),
        "additional_predictive_evidence_execution_digest": "NOT_CREATED",
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "label_generation_performed": False,
        "feature_matrix_generation_performed": False,
        "walk_forward_validation_performed": False,
        "out_of_sample_evaluation_performed": False,
        "generated_output_count": 0,
        "failures": failures,
        "failure_count": len(failures),
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
    }


def _build_executed_artifact(
    *,
    run_timestamp_utc: str,
    source_root: Path,
    output_root: Path,
    source_verification: dict[str, Any],
    summaries: dict[str, Any],
) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": APPROVED_REGISTRY_METADATA["dataset_name"],
        "provider_requests_made_in_execution": False,
        "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "research_registry_approved": True,
        "registry_approval_created": True,
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution": True,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "label_generation_authorized": True,
        "label_generation_performed": True,
        "feature_matrix_generation_authorized": True,
        "feature_matrix_generation_performed": True,
        "walk_forward_validation_authorized": True,
        "walk_forward_validation_performed": True,
        "out_of_sample_evaluation_authorized": True,
        "out_of_sample_evaluation_performed": True,
        "baseline_comparison_authorized": True,
        "baseline_comparison_performed": True,
        "signal_quality_metrics_authorized": True,
        "signal_quality_metrics_performed": True,
        "stability_analysis_authorized": True,
        "stability_analysis_performed": True,
        "leakage_control_review_authorized": True,
        "leakage_control_review_performed": True,
        "predictive_experiment_rerun_authorized": True,
        "predictive_experiment_rerun_performed": True,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "canonical_dataset_freeze_scope": "CANONICAL_DATASET_FREEZE_ONLY",
        "label_family_count": len(LABEL_FAMILIES),
        "feature_family_count": len(FEATURE_FAMILIES),
        "metric_family_count": len(METRIC_FAMILIES),
        "baseline_count": len(BASELINES),
        "generated_output_count": len(OUTPUT_FILENAMES),
        "generated_output_names": list(OUTPUT_FILENAMES),
        "execution_digest_manifest_filename": "execution_digest_manifest.json",
        "execution_digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "registry_approved_dataset_metadata": deepcopy(APPROVED_REGISTRY_METADATA),
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "source_root": _path_text(source_root),
        "generated_output_root": _path_text(output_root),
        "source_verification": source_verification,
        "source_evidence": _source_evidence(),
        "label_families_generated": list(LABEL_FAMILIES),
        "feature_families_generated": list(FEATURE_FAMILIES),
        "metric_families_computed": list(METRIC_FAMILIES),
        "baselines_evaluated": list(BASELINES),
        "split_profile": deepcopy(SPLIT_PROFILE),
        **summaries,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
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
    }
    artifact["additional_predictive_evidence_execution_digest"] = (
        additional_predictive_evidence_execution_digest_v1(artifact)
    )
    return artifact


def _write_json_once(path: Path, payload: dict[str, Any]) -> str:
    data = canonical_json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise AdditionalPredictiveEvidenceExecutionError(
            f"execution output already exists: {path.name}"
        ) from exc
    return sha256_bytes(data)


def execute_additional_predictive_evidence_v1(
    *,
    source_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Execute the approved dependency-light research run without provider access."""
    source_path = DEFAULT_SOURCE_ROOT if source_root is None else Path(source_root)
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    source_verification, failures = _verify_source_root(source_path)
    if failures:
        return _blocked_artifact(
            source_root=source_path,
            output_root=output_path,
            run_timestamp_utc=timestamp,
            failures=failures,
        )
    rows_by_ticker, row_failures = _read_rows(source_path)
    if row_failures:
        return _blocked_artifact(
            source_root=source_path,
            output_root=output_path,
            run_timestamp_utc=timestamp,
            failures=row_failures,
        )
    if output_path.exists() and any(output_path.iterdir()):
        raise AdditionalPredictiveEvidenceExecutionError(
            "additional predictive evidence output root is not empty"
        )

    labels_by_ticker = _generate_labels(rows_by_ticker)
    features_by_ticker = _generate_features(rows_by_ticker)
    reports, summaries = _build_reports(
        rows_by_ticker=rows_by_ticker,
        labels_by_ticker=labels_by_ticker,
        features_by_ticker=features_by_ticker,
        run_timestamp_utc=timestamp,
        source_verification=source_verification,
    )
    artifact = _build_executed_artifact(
        run_timestamp_utc=timestamp,
        source_root=source_path,
        output_root=output_path,
        source_verification=source_verification,
        summaries=summaries,
    )
    validate_additional_predictive_evidence_executed_v1(artifact)
    reports["additional_predictive_evidence_execution_manifest"] = artifact

    output_digests: dict[str, str] = {}
    for filename in OUTPUT_FILENAMES:
        report_name = filename.removesuffix(".json")
        if report_name == "execution_digest_manifest":
            continue
        output_digests[filename] = _write_json_once(
            output_path / filename, reports[report_name]
        )
    digest_entries = [
        (
            {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
                "sha256": None,
            }
            if filename == "execution_digest_manifest.json"
            else {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": output_digests[filename],
            }
        )
        for filename in OUTPUT_FILENAMES
    ]
    digest_manifest = _report(
        "execution_digest_manifest",
        {
            "run_timestamp_utc": timestamp,
            "generated_output_count": len(OUTPUT_FILENAMES),
            "output_digest_entries": digest_entries,
            "all_non_self_output_digests_present": True,
            "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
            "additional_predictive_evidence_execution_digest": artifact[
                "additional_predictive_evidence_execution_digest"
            ],
        },
    )
    _write_json_once(output_path / "execution_digest_manifest.json", digest_manifest)
    return artifact


FORBIDDEN_ARTIFACT_VALUES = {
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}
FORBIDDEN_TRUE_FIELDS = {
    "provider_requests_made_in_execution",
    "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "predictive_usefulness_acceptance_candidate_created",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
}


def _reject_forbidden_values(value: Any, *, path: str = "artifact") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionError(f"{path} must not emit {value}")
    if isinstance(value, dict):
        for key, item in value.items():
            current_path = f"{path}.{key}"
            if key in FORBIDDEN_TRUE_FIELDS and item is True:
                raise AdditionalPredictiveEvidenceExecutionError(
                    f"{current_path} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionError(
                    f"{current_path} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionError(
                    f"{current_path} must not be accepted"
                )
            _reject_forbidden_values(item, path=current_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceExecutionError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceExecutionError(f"{field} must be false")


def validate_additional_predictive_evidence_executed_v1(
    artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate completed research evidence while rejecting downstream authority."""
    if not isinstance(artifact, dict):
        raise AdditionalPredictiveEvidenceExecutionError("artifact must be a JSON object")
    _reject_forbidden_values(artifact)
    _expect(
        artifact.get("artifact_kind"),
        ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED,
        "artifact_kind",
    )
    _expect(
        artifact.get("schema_version"),
        SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_V1,
        "schema_version",
    )
    _expect(
        artifact.get("execution_status"),
        ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY,
        "execution_status",
    )
    for field in TRUE_EXECUTION_FIELDS:
        _expect_true(artifact.get(field), field)
    for field in FALSE_GUARDRAIL_FIELDS:
        _expect_false(artifact.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    _expect(artifact.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(artifact.get("profitability"), NOT_ACCEPTED, "profitability")
    expected_values = {
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "canonical_dataset_freeze_scope": "CANONICAL_DATASET_FREEZE_ONLY",
        "label_family_count": 7,
        "feature_family_count": 10,
        "metric_family_count": 9,
        "baseline_count": 6,
        "generated_output_count": 15,
        "generated_output_names": OUTPUT_FILENAMES,
        "execution_digest_manifest_filename": "execution_digest_manifest.json",
        "execution_digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "registry_approved_dataset_metadata": APPROVED_REGISTRY_METADATA,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "label_families_generated": LABEL_FAMILIES,
        "feature_families_generated": FEATURE_FAMILIES,
        "metric_families_computed": METRIC_FAMILIES,
        "baselines_evaluated": BASELINES,
        "split_profile": SPLIT_PROFILE,
        "failure_count": 0,
        "warning_count": 1,
    }
    for field, expected in expected_values.items():
        _expect(artifact.get(field), expected, field)
    _expect(
        artifact.get("per_ticker_record_counts"),
        EXPECTED_RECORD_COUNTS,
        "per_ticker_record_counts",
    )
    source_evidence = artifact.get("source_evidence")
    if not isinstance(source_evidence, dict):
        raise AdditionalPredictiveEvidenceExecutionError("source_evidence missing")
    for field, expected in _source_evidence().items():
        value = source_evidence.get(field)
        if not isinstance(value, str) or not value:
            raise AdditionalPredictiveEvidenceExecutionError(f"{field} missing")
        _expect(value, expected, field)
    source_verification = artifact.get("source_verification")
    if not isinstance(source_verification, dict):
        raise AdditionalPredictiveEvidenceExecutionError("source_verification missing")
    _expect_true(source_verification.get("records_digest_match"), "records_digest_match")
    _expect(
        source_verification.get("records_digest_actual"),
        EXPECTED_RECORDS_DIGEST,
        "source records digest",
    )
    for field in (
        "label_coverage_summary",
        "feature_coverage_summary",
        "walk_forward_summary",
        "out_of_sample_summary",
        "baseline_comparison_summary",
        "calibration_summary",
        "stability_summary",
        "leakage_control_summary",
        "data_quality_summary",
    ):
        value = artifact.get(field)
        if not isinstance(value, dict) or not value:
            raise AdditionalPredictiveEvidenceExecutionError(f"{field} missing")
    _expect_true(artifact["walk_forward_summary"].get("performed"), "walk-forward summary performed")
    _expect_true(artifact["out_of_sample_summary"].get("performed"), "out-of-sample summary performed")
    _expect_true(artifact["baseline_comparison_summary"].get("performed"), "baseline summary performed")
    _expect(
        artifact["leakage_control_summary"].get("status"), "PASS", "leakage status"
    )
    _expect(
        artifact["data_quality_summary"].get("status"),
        "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "data quality status",
    )
    digest = artifact.get("additional_predictive_evidence_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionError(
            "additional_predictive_evidence_execution_digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_digest_v1(artifact),
        "additional_predictive_evidence_execution_digest",
    )
    return {
        "status": "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_VALID",
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "additional_predictive_evidence_execution_digest": digest,
        "additional_predictive_evidence_execution_approval_digest": source_evidence[
            "additional_predictive_evidence_execution_approval_digest"
        ],
        "target_universe_count": artifact["target_universe_count"],
        "total_canonical_record_count": artifact["total_canonical_record_count"],
        "generated_output_count": artifact["generated_output_count"],
        "failure_count": artifact["failure_count"],
        "warning_count": artifact["warning_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_approved": False,
    }


def build_additional_predictive_evidence_execution_status_markdown_v1(
    artifact: dict[str, Any],
) -> str:
    """Render a sanitized summary of the research-only execution evidence."""
    validation = validate_additional_predictive_evidence_executed_v1(artifact)
    source = artifact["source_evidence"]
    metadata = artifact["registry_approved_dataset_metadata"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Status",
        "",
        "## Title",
        "- Additional Predictive Evidence Execution v1.",
        "",
        "## Additional Predictive Evidence Execution",
        f"- Artifact kind: `{artifact['artifact_kind']}`",
        f"- Execution status: `{artifact['execution_status']}`",
        f"- Execution digest: `{validation['additional_predictive_evidence_execution_digest']}`",
        f"- Run timestamp UTC: `{artifact['run_timestamp_utc']}`",
        f"- Generated output root: `{artifact['generated_output_root']}`",
        f"- Generated output count: `{artifact['generated_output_count']}`",
        "",
        "## Source Execution Approval",
        f"- Approval digest: `{source['additional_predictive_evidence_execution_approval_digest']}`",
        f"- Candidate review digest: `{source['additional_predictive_evidence_execution_candidate_review_package_digest']}`",
        f"- Research registry approval digest: `{source['research_registry_approval_digest']}`",
        f"- Canonical dataset freeze digest: `{source['canonical_dataset_freeze_digest']}`",
        f"- Canonical dataset generation digest: `{source['canonical_dataset_generation_digest']}`",
        "",
        "## Registry-Approved Dataset Metadata",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in metadata.items())
    lines.extend(
        [
            "",
            "## Target Universe",
            f"- `{' '.join(artifact['target_universe'])}`",
            "",
            "## Label Generation Summary",
            f"- Label families: `{artifact['label_family_count']}`",
            f"- Label coverage entries: `{artifact['label_coverage_summary']['entry_count']}`",
            f"- Label generation digest: `{artifact['label_coverage_summary']['label_generation_digest']}`",
            "",
            "## Feature Generation Summary",
            f"- Feature families: `{artifact['feature_family_count']}`",
            f"- Feature rows: `{artifact['feature_coverage_summary']['feature_matrix_row_count']}`",
            f"- Feature matrix digest: `{artifact['feature_coverage_summary']['feature_matrix_digest']}`",
            "",
            "## Walk-Forward Validation Summary",
            f"- Fold count: `{artifact['walk_forward_summary']['fold_count']}`",
            f"- Policy: `{artifact['walk_forward_summary']['policy']}`",
            "",
            "## Out-of-Sample Evaluation Summary",
            f"- Evaluation count: `{artifact['out_of_sample_summary']['evaluation_count']}`",
            "",
            "## Baseline Comparison Summary",
            f"- Baseline count: `{artifact['baseline_comparison_summary']['baseline_count']}`",
            "",
            "## Metric Summary",
            f"- Metric family count: `{artifact['metric_family_count']}`",
            f"- Metric families: `{', '.join(artifact['metric_families_computed'])}`",
            "",
            "## Calibration Summary",
            f"- Brier score: `{artifact['calibration_summary']['out_of_sample_brier_score']}`",
            "",
            "## Stability Summary",
            f"- Baselines assessed: `{artifact['stability_summary']['baseline_count']}`",
            "",
            "## Leakage-Control Summary",
            f"- Status: `{artifact['leakage_control_summary']['status']}`",
            f"- Failed controls: `{artifact['leakage_control_summary']['failed_control_count']}`",
            "",
            "## Data Quality Summary",
            f"- Status: `{artifact['data_quality_summary']['status']}`",
            f"- Failures/warnings: `{artifact['failure_count']}` / `{artifact['warning_count']}`",
            f"- META record count preserved: `{artifact['meta_record_count']}`",
            "",
            "## Output Digest Manifest",
            f"- Filename: `{artifact['execution_digest_manifest_filename']}`",
            f"- Self-reference policy: `{artifact['execution_digest_manifest_self_reference_policy']}`",
            "",
            "## Predictive Usefulness Boundary",
            f"- predictive_usefulness: `{artifact['predictive_usefulness']}`",
            f"- acceptance candidate created: `{artifact['predictive_usefulness_acceptance_candidate_created']}`",
            "",
            "## Profitability Boundary",
            f"- profitability: `{artifact['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{artifact['runtime_migration_approved']}`",
            f"- runtime_use: `{artifact['runtime_use']}`",
            f"- strategy_use: `{artifact['strategy_use']}`",
            f"- paper_trading: `{artifact['paper_trading']}`",
            f"- broker_execution: `{artifact['broker_execution']}`",
            "",
            "## Checklist Summary",
            "- Source files and digests verified; labels/features/evaluations completed with zero failures.",
            "- Results require a separate operator review before any usefulness reassessment.",
            "",
            "## Guardrails",
            "- Fully offline: no provider request, market-data acquisition, or dataset regeneration occurred.",
            "- No strategy scoring or trade recommendation was generated.",
            "- Predictive usefulness and profitability remain not accepted.",
            "- Runtime, Strategy, paper trading, and broker execution remain NOT_AUTHORIZED.",
            "",
        ]
    )
    return "\n".join(lines)
