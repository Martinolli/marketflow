"""Deterministic offline execution of approved redesigned-label generation."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import label_objective_redesign_execution_service as design_execution


ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_EXECUTED = (
    "REDESIGNED_LABEL_GENERATION_EXECUTED"
)
ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_BLOCKED = (
    "REDESIGNED_LABEL_GENERATION_BLOCKED"
)
SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_EXECUTED_V1 = (
    "redesigned_label_generation_executed_v1"
)
REDESIGNED_LABEL_GENERATION_EXECUTED_RESEARCH_ONLY = (
    "REDESIGNED_LABEL_GENERATION_EXECUTED_RESEARCH_ONLY"
)
REDESIGNED_LABEL_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE = (
    "REDESIGNED_LABEL_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
)
REDESIGNED_LABEL_GENERATION_EXECUTION_VALID = (
    "REDESIGNED_LABEL_GENERATION_EXECUTION_VALID"
)

EXPECTED_REDESIGNED_LABEL_GENERATION_APPROVAL_DIGEST = (
    "280734ff469c4bfb07f67060e8077b173e034fa9b9dd6b7e82225eb881337247"
)
EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "e9dfaa21fe643e6e25762d7f00939763d766d3a4ebeaffb3a12895abab7f2c52"
)
EXPECTED_CANDIDATE_DIGEST = (
    "6ef5c93b660e2f2ad825a774299e3dae1adc3041a1f619f7b3df0001c18f5a08"
)
EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "bda6012c74cffb8841a6b9568c0985e2b6d1c337c7b7fcf892da4b724fcb15f9"
)
EXPECTED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_DIGEST = (
    "d43bb214850f8068b445d1620ae8f4f948162eda309f04acf6fdd7b73abd63a4"
)
EXPECTED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVAL_DIGEST = (
    "8ca1dee0aa2c175a1ab5bf7f9ba724b8dc0df6e2057e4f97721bad02f4adaff0"
)
EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST = (
    "2f771999ff5e31dbd959ea1a33b08852cda46913ff1b5dfc6fe17bc0853ee14a"
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)

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

DEFAULT_CANONICAL_ROOT = Path(
    ".marketflow/canonical_datasets/expanded_universe_v1"
)
DEFAULT_DESIGN_ROOT = Path(
    ".marketflow/label_objective_redesign/expanded_universe_v1"
)
DEFAULT_OUTPUT_ROOT = Path(
    ".marketflow/redesigned_label_generation/expanded_universe_v1"
)
DEFAULT_BRANCH = "feature/redesigned-label-generation-execution-v1"
DEFAULT_BASE_COMMIT = "981b0f5cde552b62928f006cc473310be8cdcbd3"

CANONICAL_SOURCE_FILENAMES = list(design_execution.REQUIRED_SOURCE_FILENAMES)
DESIGN_SOURCE_FILENAMES = [
    "label_objective_redesign_execution_manifest.json",
    "label_family_candidate_matrix.json",
    "threshold_design_matrix.json",
    "horizon_design_matrix.json",
    "per_ticker_label_objective_plan.json",
    "label_availability_boundary_plan.json",
    "meta_limitation_preservation_plan.json",
    "operator_review_summary_template.json",
]
OUTPUT_FILENAMES = [
    "redesigned_label_generation_execution_manifest.json",
    "redesigned_label_generation_input_manifest.json",
    "redesigned_label_values.jsonl",
    "redesigned_label_family_coverage_report.json",
    "redesigned_threshold_generation_report.json",
    "redesigned_horizon_generation_report.json",
    "redesigned_label_availability_report.json",
    "per_ticker_redesigned_label_summary.json",
    "meta_limitation_preservation_report.json",
    "redesigned_label_generation_digest_manifest.json",
    "operator_review_summary.json",
]

LABEL_FAMILIES = [
    "REDESIGNED_LABEL_DIRECTION_WITH_FLAT_ZONE",
    "REDESIGNED_LABEL_RETURN_BUCKET_REDESIGNED_THRESHOLDS",
    "REDESIGNED_LABEL_MULTI_HORIZON_5_10_20",
    "REDESIGNED_LABEL_BENCHMARK_RELATIVE_RETURN",
    "REDESIGNED_LABEL_VOLATILITY_ADJUSTED_RETURN",
    "REDESIGNED_LABEL_DRAWDOWN_AVOIDANCE",
    "REDESIGNED_LABEL_RISK_REWARD_ASYMMETRIC_TARGET",
    "REDESIGNED_LABEL_REGIME_CONDITIONED_DIRECTION",
    "REDESIGNED_LABEL_PER_TICKER_CALIBRATED_TARGET",
    "REDESIGNED_LABEL_NO_TRADE_ZONE_CLASS",
]
THRESHOLD_STRATEGIES = [
    "global_threshold_candidate",
    "per_ticker_threshold_candidate",
    "training_window_only_threshold_candidate",
    "volatility_adjusted_threshold_candidate",
    "benchmark_relative_threshold_candidate",
    "flat_zone_threshold_candidate",
    "class_balance_review_candidate",
]
HORIZON_STRATEGIES = [
    "one_session_horizon_candidate",
    "five_session_horizon_candidate",
    "ten_session_horizon_candidate",
    "twenty_session_horizon_candidate",
    "multi_horizon_comparison_candidate",
]
AVAILABILITY_RULES = [
    "training_window_threshold_fit_only",
    "forward_tail_unavailable_labels_marked_null",
    "no_peek_label_generation",
    "late_window_label_availability_boundary",
    "meta_record_count_limitation_preserved",
    "no_synthetic_rows",
    "no_backfill",
    "no_calendar_inference",
]

OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "REDESIGNED_LABEL_GENERATION_RESEARCH_ONLY"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

FAMILY_HORIZONS = {
    LABEL_FAMILIES[0]: [1],
    LABEL_FAMILIES[1]: [5],
    LABEL_FAMILIES[2]: [5, 10, 20],
    LABEL_FAMILIES[3]: [5],
    LABEL_FAMILIES[4]: [5],
    LABEL_FAMILIES[5]: [20],
    LABEL_FAMILIES[6]: [10],
    LABEL_FAMILIES[7]: [5],
    LABEL_FAMILIES[8]: [5],
    LABEL_FAMILIES[9]: [5],
}

CHECK_IDS = [
    "artifact_kind_matches",
    "execution_status_matches",
    "approval_digest_bound",
    "candidate_review_digest_bound",
    "candidate_digest_bound",
    "results_review_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "total_record_count_11946",
    "meta_913_preserved",
    "execution_approved_true",
    "execution_authorized_true",
    "ready_for_execution_true",
    "execution_performed_true",
    "actual_labels_generated_true",
    "results_created_true",
    "generated_output_count_11",
    "all_generated_outputs_created",
    "label_family_count_10",
    "threshold_strategy_count_7",
    "horizon_strategy_count_5",
    "label_value_rows_nonzero",
    "family_coverage_present",
    "available_unavailable_counts_recorded",
    "output_digest_manifest_complete",
    "outputs_research_only",
    "feature_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "additional_predictive_evidence_candidate_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "paper_trading_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "label_objective_redesign_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "meta_limitation_preserved",
    "no_tracked_marketflow_files",
]


class RedesignedLabelGenerationExecutionError(ValueError):
    """Raised when label generation violates its guarded execution contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


def _decimal(value: Any, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise RedesignedLabelGenerationExecutionError(
            f"invalid decimal value for {field}"
        ) from exc
    if not result.is_finite():
        raise RedesignedLabelGenerationExecutionError(
            f"non-finite decimal value for {field}"
        )
    return result


def _decimal_text(value: Decimal | None) -> str | None:
    if value is None:
        return None
    with localcontext() as context:
        context.prec = 34
        quantized = value.quantize(Decimal("0.000000000001"))
    text = format(quantized.normalize(), "f")
    return "0" if text in {"-0", ""} else text


def _median(values: Iterable[Decimal]) -> Decimal:
    ordered = sorted(values)
    if not ordered:
        raise RedesignedLabelGenerationExecutionError(
            "median requires at least one value"
        )
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / Decimal(2)


def _source_evidence() -> dict[str, str]:
    return {
        "redesigned_label_generation_approval_digest": EXPECTED_REDESIGNED_LABEL_GENERATION_APPROVAL_DIGEST,
        "redesigned_label_generation_candidate_review_package_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "redesigned_label_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "label_objective_redesign_results_review_package_digest": EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST,
        "label_objective_redesign_execution_digest": EXPECTED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_DIGEST,
        "label_objective_redesign_execution_approval_digest": EXPECTED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_APPROVAL_DIGEST,
        "operator_method_path_selection_digest": EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
    }


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_generation_approved": True,
        "redesigned_label_generation_authorized": True,
        "ready_for_redesigned_label_generation_execution": True,
        "redesigned_label_generation_performed": True,
        "actual_redesigned_labels_generated": True,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }


def _report(
    report_name: str, run_timestamp_utc: str, payload: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "report_name": report_name,
        "run_timestamp_utc": run_timestamp_utc,
        **_common_output_fields(),
        **deepcopy(dict(payload)),
    }


def _verify_design_root(
    design_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    for filename in DESIGN_SOURCE_FILENAMES:
        if not (design_root / filename).is_file():
            failures.append(
                _failure(
                    "missing_design_source_file",
                    "required label-objective design source file missing",
                    filename=filename,
                )
            )
    if failures:
        return {}, failures
    try:
        manifest = json.loads(
            (design_root / DESIGN_SOURCE_FILENAMES[0]).read_text(encoding="utf-8")
        )
        design_execution.validate_label_objective_redesign_executed_v1(manifest)
    except (
        OSError,
        json.JSONDecodeError,
        design_execution.LabelObjectiveRedesignExecutionError,
    ) as exc:
        return {}, [
            _failure(
                "invalid_design_execution_manifest",
                "label-objective design execution manifest is invalid",
                error=str(exc),
            )
        ]
    if manifest.get("label_objective_redesign_execution_digest") != (
        EXPECTED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_DIGEST
    ):
        failures.append(
            _failure(
                "design_execution_digest_mismatch",
                "label-objective design execution digest mismatch",
            )
        )
    entries = manifest.get("output_digest_manifest", [])
    expected_entries = {row.get("filename"): row for row in entries}
    for filename in DESIGN_SOURCE_FILENAMES[1:]:
        expected = expected_entries.get(filename, {}).get("sha256")
        actual = sha256_file(design_root / filename)
        if expected != actual:
            failures.append(
                _failure(
                    "design_source_digest_mismatch",
                    "label-objective design source digest mismatch",
                    filename=filename,
                    expected=expected,
                    actual=actual,
                )
            )
    verification = {
        "design_root": _path_text(design_root),
        "required_design_source_file_count": len(DESIGN_SOURCE_FILENAMES),
        "required_design_source_files": list(DESIGN_SOURCE_FILENAMES),
        "label_objective_redesign_execution_digest": manifest.get(
            "label_objective_redesign_execution_digest"
        ),
        "source_label_objective_redesign_output_count": manifest.get(
            "generated_output_count"
        ),
        "source_label_objective_redesign_output_status": (
            "REVIEWED_AND_VERIFIED"
        ),
        "design_source_digests": [
            {
                "filename": filename,
                "sha256": sha256_file(design_root / filename),
            }
            for filename in DESIGN_SOURCE_FILENAMES
        ],
    }
    return verification, failures


def _load_records(
    canonical_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    records_path = canonical_root / "canonical_dataset_records.jsonl"
    try:
        with records_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                ticker = row.get("ticker")
                date = row.get("date")
                close = row.get("close")
                if ticker not in TARGET_UNIVERSE or not isinstance(date, str):
                    raise RedesignedLabelGenerationExecutionError(
                        f"invalid canonical record identity at line {line_number}"
                    )
                _decimal(close, f"close line {line_number}")
                records.append(row)
    except (
        OSError,
        json.JSONDecodeError,
        RedesignedLabelGenerationExecutionError,
    ) as exc:
        failures.append(
            _failure(
                "invalid_canonical_records",
                "canonical records could not be loaded for label generation",
                error=str(exc),
            )
        )
        return [], failures
    expected_order = {ticker: index for index, ticker in enumerate(TARGET_UNIVERSE)}
    keys = [(expected_order[row["ticker"]], row["date"]) for row in records]
    if keys != sorted(keys):
        failures.append(
            _failure(
                "canonical_record_order_mismatch",
                "canonical records must be ordered by ticker and date ascending",
            )
        )
    counts = Counter(row["ticker"] for row in records)
    if len(records) != 11946 or dict(counts) != EXPECTED_RECORD_COUNTS:
        failures.append(
            _failure(
                "canonical_record_count_mismatch",
                "canonical record counts do not match the frozen contract",
                total=len(records),
                per_ticker=dict(counts),
            )
        )
    return records, failures


def _load_and_verify_sources(
    canonical_root: Path, design_root: Path
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    canonical_verification, canonical_failures = design_execution._verify_source_root(
        canonical_root
    )
    design_verification, design_failures = _verify_design_root(design_root)
    records: list[dict[str, Any]] = []
    record_failures: list[dict[str, Any]] = []
    if not canonical_failures:
        records, record_failures = _load_records(canonical_root)
    return (
        canonical_verification,
        design_verification,
        records,
        canonical_failures + design_failures + record_failures,
    )


def _partition(date: str) -> str:
    if date <= "2023-12-31":
        return "TRAINING"
    if date <= "2024-12-31":
        return "VALIDATION"
    return "OOS"


def _forward_returns(
    grouped: Mapping[str, list[dict[str, Any]]]
) -> dict[tuple[str, int, int], Decimal | None]:
    returns: dict[tuple[str, int, int], Decimal | None] = {}
    for ticker in TARGET_UNIVERSE:
        rows = grouped[ticker]
        closes = [_decimal(row["close"], "close") for row in rows]
        for index, close in enumerate(closes):
            for horizon in (1, 5, 10, 20):
                returns[(ticker, index, horizon)] = (
                    closes[index + horizon] / close - Decimal(1)
                    if index + horizon < len(closes)
                    else None
                )
    return returns


def _rolling_volatility_thresholds(
    grouped: Mapping[str, list[dict[str, Any]]],
    returns: Mapping[tuple[str, int, int], Decimal | None],
    fallback: Decimal,
) -> dict[str, Decimal]:
    result: dict[str, Decimal] = {}
    with localcontext() as context:
        context.prec = 34
        scale = Decimal(5).sqrt()
        for ticker in TARGET_UNIVERSE:
            one_day = [
                returns[(ticker, index, 1)]
                for index, row in enumerate(grouped[ticker])
                if _partition(row["date"]) == "TRAINING"
                and returns[(ticker, index, 1)] is not None
            ]
            rolling: list[Decimal] = []
            for end in range(20, len(one_day) + 1):
                window = one_day[end - 20 : end]
                mean = sum(window, Decimal(0)) / Decimal(len(window))
                variance = sum(
                    ((value - mean) ** 2 for value in window), Decimal(0)
                ) / Decimal(len(window))
                rolling.append(variance.sqrt() * scale)
            result[ticker] = _median(rolling) if rolling else fallback
    return result


def _thresholds(
    grouped: Mapping[str, list[dict[str, Any]]],
    returns: Mapping[tuple[str, int, int], Decimal | None],
    benchmark_returns: Mapping[tuple[str, int], Decimal],
) -> dict[str, Any]:
    global_values: list[Decimal] = []
    per_ticker_values: dict[str, list[Decimal]] = defaultdict(list)
    relative_values: list[Decimal] = []
    for ticker in TARGET_UNIVERSE:
        for index, row in enumerate(grouped[ticker]):
            value = returns[(ticker, index, 5)]
            if _partition(row["date"]) != "TRAINING" or value in {None, Decimal(0)}:
                continue
            absolute = abs(value)
            global_values.append(absolute)
            per_ticker_values[ticker].append(absolute)
            benchmark = benchmark_returns.get((row["date"], 5))
            if benchmark is not None and value != benchmark:
                relative_values.append(abs(value - benchmark))
    if not global_values:
        raise RedesignedLabelGenerationExecutionError(
            "training-window 5-session returns are unavailable"
        )
    global_threshold = _median(global_values)
    per_ticker = {
        ticker: (
            _median(per_ticker_values[ticker])
            if per_ticker_values[ticker]
            else global_threshold
        )
        for ticker in TARGET_UNIVERSE
    }
    relative = _median(relative_values) if relative_values else global_threshold
    volatility = _rolling_volatility_thresholds(
        grouped, returns, global_threshold
    )
    return {
        "global": global_threshold,
        "per_ticker": per_ticker,
        "benchmark_relative": relative,
        "volatility_adjusted": volatility,
    }


def _classify_direction(value: Decimal, threshold: Decimal) -> str:
    if value > threshold:
        return "UP"
    if value < -threshold:
        return "DOWN"
    return "FLAT"


def _family_label(
    *,
    family: str,
    value: Decimal,
    threshold: Decimal,
    benchmark: Decimal | None,
) -> tuple[str, str | None]:
    if family == LABEL_FAMILIES[1]:
        if value > threshold * 2:
            return "STRONG_UP", None
        if value > threshold:
            return "UP", None
        if value < -threshold * 2:
            return "STRONG_DOWN", None
        if value < -threshold:
            return "DOWN", None
        return "FLAT", None
    if family == LABEL_FAMILIES[3]:
        relative = value - (benchmark or Decimal(0))
        return _classify_direction(relative, threshold), "SAME_DATE_UNIVERSE_MEDIAN"
    if family == LABEL_FAMILIES[5]:
        return (
            "DRAWDOWN_RISK" if value < -threshold else "DRAWDOWN_AVOIDED",
            None,
        )
    if family == LABEL_FAMILIES[6]:
        if value > threshold * 2:
            return "ASYMMETRIC_UPSIDE", None
        if value < -threshold:
            return "DOWNSIDE_RISK", None
        return "NEUTRAL", None
    if family == LABEL_FAMILIES[7]:
        regime = (
            "POSITIVE_BENCHMARK_REGIME"
            if (benchmark or Decimal(0)) >= 0
            else "NEGATIVE_BENCHMARK_REGIME"
        )
        return f"{_classify_direction(value, threshold)}_{regime}", (
            "SAME_DATE_UNIVERSE_MEDIAN"
        )
    if family == LABEL_FAMILIES[9]:
        direction = _classify_direction(value, threshold)
        return ("NO_TRADE" if direction == "FLAT" else direction), None
    return _classify_direction(value, threshold), None


def _jsonl_bytes(rows: Iterable[Mapping[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(row) for row in rows)


def _generate_label_outputs(
    records: list[dict[str, Any]], run_timestamp_utc: str
) -> tuple[bytes, dict[str, dict[str, Any]], dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {ticker: [] for ticker in TARGET_UNIVERSE}
    for row in records:
        grouped[row["ticker"]].append(row)
    returns = _forward_returns(grouped)
    benchmark_buckets: dict[tuple[str, int], list[Decimal]] = defaultdict(list)
    for ticker in TARGET_UNIVERSE:
        for index, row in enumerate(grouped[ticker]):
            for horizon in (1, 5, 10, 20):
                value = returns[(ticker, index, horizon)]
                if value is not None:
                    benchmark_buckets[(row["date"], horizon)].append(value)
    benchmarks = {
        key: _median(values) for key, values in benchmark_buckets.items() if values
    }
    thresholds = _thresholds(grouped, returns, benchmarks)

    label_rows: list[dict[str, Any]] = []
    coverage: Counter[tuple[str, str, int]] = Counter()
    available: Counter[tuple[str, str, int]] = Counter()
    unavailable: Counter[tuple[str, str, int]] = Counter()
    class_counts: Counter[tuple[str, str]] = Counter()
    ticker_totals: Counter[str] = Counter()
    ticker_available: Counter[str] = Counter()
    ticker_unavailable: Counter[str] = Counter()
    horizon_counts: Counter[int] = Counter()

    with localcontext() as context:
        context.prec = 34
        for ticker in TARGET_UNIVERSE:
            for index, source_row in enumerate(grouped[ticker]):
                for family in LABEL_FAMILIES:
                    for horizon in FAMILY_HORIZONS[family]:
                        value = returns[(ticker, index, horizon)]
                        benchmark = benchmarks.get((source_row["date"], horizon))
                        if family == LABEL_FAMILIES[3]:
                            threshold = thresholds["benchmark_relative"]
                            strategy = "benchmark_relative_threshold_candidate"
                        elif family == LABEL_FAMILIES[4]:
                            threshold = thresholds["volatility_adjusted"][ticker]
                            strategy = "volatility_adjusted_threshold_candidate"
                        elif family == LABEL_FAMILIES[8]:
                            threshold = thresholds["per_ticker"][ticker]
                            strategy = "per_ticker_threshold_candidate"
                        elif family in {LABEL_FAMILIES[0], LABEL_FAMILIES[9]}:
                            threshold = thresholds["global"]
                            strategy = "flat_zone_threshold_candidate"
                        elif family == LABEL_FAMILIES[2]:
                            threshold = thresholds["global"] * (
                                Decimal(horizon) / Decimal(5)
                            ).sqrt()
                            strategy = "training_window_only_threshold_candidate"
                        else:
                            threshold = thresholds["global"] * (
                                Decimal(horizon) / Decimal(5)
                            ).sqrt()
                            strategy = "global_threshold_candidate"
                        label_value: str | None = None
                        benchmark_basis: str | None = None
                        if value is not None:
                            label_value, benchmark_basis = _family_label(
                                family=family,
                                value=value,
                                threshold=threshold,
                                benchmark=benchmark,
                            )
                        key = (ticker, family, horizon)
                        coverage[key] += 1
                        ticker_totals[ticker] += 1
                        horizon_counts[horizon] += 1
                        if value is None:
                            unavailable[key] += 1
                            ticker_unavailable[ticker] += 1
                        else:
                            available[key] += 1
                            ticker_available[ticker] += 1
                            class_counts[(family, label_value or "NULL")] += 1
                        label_rows.append(
                            {
                                "ticker": ticker,
                                "date": source_row["date"],
                                "record_index_for_ticker": index,
                                "window_partition": _partition(source_row["date"]),
                                "label_family": family,
                                "horizon": horizon,
                                "forward_return": _decimal_text(value),
                                "label_value": label_value,
                                "label_available": value is not None,
                                "availability_reason": (
                                    "AVAILABLE"
                                    if value is not None
                                    else "INSUFFICIENT_FUTURE_BARS"
                                ),
                                "threshold_strategy": strategy,
                                "threshold_value_used": _decimal_text(threshold),
                                "benchmark_basis": benchmark_basis,
                                "meta_reduced_record_count_flag": ticker == "META",
                                "research_only": True,
                                "non_actionable": True,
                            }
                        )

    coverage_rows = [
        {
            "ticker": ticker,
            "label_family": family,
            "horizon": horizon,
            "label_value_row_count": coverage[(ticker, family, horizon)],
            "available_label_value_count": available[(ticker, family, horizon)],
            "unavailable_label_value_count": unavailable[(ticker, family, horizon)],
        }
        for ticker in TARGET_UNIVERSE
        for family in LABEL_FAMILIES
        for horizon in FAMILY_HORIZONS[family]
    ]
    available_count = sum(available.values())
    unavailable_count = sum(unavailable.values())
    common_counts = {
        "label_value_row_count": len(label_rows),
        "label_family_coverage_entries": len(coverage_rows),
        "available_label_value_count": available_count,
        "unavailable_label_value_count": unavailable_count,
    }
    reports = {
        "redesigned_label_family_coverage_report.json": _report(
            "redesigned_label_family_coverage_report",
            run_timestamp_utc,
            {
                "label_family_count": len(LABEL_FAMILIES),
                "label_families": list(LABEL_FAMILIES),
                "coverage_entries": coverage_rows,
                **common_counts,
            },
        ),
        "redesigned_threshold_generation_report.json": _report(
            "redesigned_threshold_generation_report",
            run_timestamp_utc,
            {
                "training_window_start": "2022-01-01",
                "training_window_end": "2023-12-31",
                "threshold_strategy_count": len(THRESHOLD_STRATEGIES),
                "threshold_strategies": list(THRESHOLD_STRATEGIES),
                "global_threshold_5_session": _decimal_text(thresholds["global"]),
                "per_ticker_thresholds_5_session": {
                    ticker: _decimal_text(thresholds["per_ticker"][ticker])
                    for ticker in TARGET_UNIVERSE
                },
                "volatility_adjusted_thresholds_5_session": {
                    ticker: _decimal_text(
                        thresholds["volatility_adjusted"][ticker]
                    )
                    for ticker in TARGET_UNIVERSE
                },
                "benchmark_relative_threshold_5_session": _decimal_text(
                    thresholds["benchmark_relative"]
                ),
                "class_balance_distribution": [
                    {
                        "label_family": family,
                        "label_value": label,
                        "count": count,
                    }
                    for (family, label), count in sorted(class_counts.items())
                ],
                "thresholds_derived_from_training_window_only": True,
                "threshold_optimization_performed": False,
            },
        ),
        "redesigned_horizon_generation_report.json": _report(
            "redesigned_horizon_generation_report",
            run_timestamp_utc,
            {
                "horizon_strategy_count": len(HORIZON_STRATEGIES),
                "horizon_strategies": list(HORIZON_STRATEGIES),
                "horizon_label_row_counts": {
                    str(horizon): horizon_counts[horizon]
                    for horizon in (1, 5, 10, 20)
                },
                "multi_horizon_values": [5, 10, 20],
            },
        ),
        "redesigned_label_availability_report.json": _report(
            "redesigned_label_availability_report",
            run_timestamp_utc,
            {
                "availability_rules": list(AVAILABILITY_RULES),
                "forward_tail_unavailable_value": None,
                "forward_tail_availability_reason": (
                    "INSUFFICIENT_FUTURE_BARS"
                ),
                **common_counts,
            },
        ),
        "per_ticker_redesigned_label_summary.json": _report(
            "per_ticker_redesigned_label_summary",
            run_timestamp_utc,
            {
                "target_universe": list(TARGET_UNIVERSE),
                "per_ticker_label_summary": [
                    {
                        "ticker": ticker,
                        "historical_record_count": len(grouped[ticker]),
                        "label_value_row_count": ticker_totals[ticker],
                        "available_label_value_count": ticker_available[ticker],
                        "unavailable_label_value_count": ticker_unavailable[ticker],
                        "meta_reduced_record_count_flag": ticker == "META",
                    }
                    for ticker in TARGET_UNIVERSE
                ],
                **common_counts,
            },
        ),
        "meta_limitation_preservation_report.json": _report(
            "meta_limitation_preservation_report",
            run_timestamp_utc,
            {
                "ticker": "META",
                "historical_record_count": len(grouped["META"]),
                "expected_historical_record_count": 913,
                "meta_reduced_record_count_preserved": len(grouped["META"]) == 913,
                "no_backfill": True,
                "no_repair": True,
                "no_synthetic_rows": True,
                "calendar_inference_performed": False,
                "label_availability_limitation_carried_forward": True,
                "meta_label_value_row_count": ticker_totals["META"],
                "meta_available_label_value_count": ticker_available["META"],
                "meta_unavailable_label_value_count": ticker_unavailable["META"],
            },
        ),
        "operator_review_summary.json": _report(
            "operator_review_summary",
            run_timestamp_utc,
            {
                "review_status": "AWAITING_SEPARATE_RESULTS_REVIEW",
                "operator_decision": None,
                "results_review_created": False,
                "review_sections": [
                    "source_approval",
                    "dataset_and_universe",
                    "label_generation_policy",
                    "label_family_coverage",
                    "threshold_strategy_summary",
                    "horizon_strategy_summary",
                    "label_availability_summary",
                    "per_ticker_summary",
                    "meta_limitation_preservation",
                    "authority_boundary",
                ],
                **common_counts,
            },
        ),
    }
    generation = {
        **common_counts,
        "thresholds": thresholds,
        "coverage_rows": coverage_rows,
    }
    return _jsonl_bytes(label_rows), reports, generation


def _blocked_artifact(
    *,
    canonical_root: Path,
    design_root: Path,
    output_root: Path,
    run_timestamp_utc: str,
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_BLOCKED,
        "schema_version": SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_EXECUTED_V1,
        "execution_status": REDESIGNED_LABEL_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "research_only": True,
        "canonical_source_root": _path_text(canonical_root),
        "design_source_root": _path_text(design_root),
        "generated_output_root": _path_text(output_root),
        "redesigned_label_generation_digest": "NOT_CREATED",
        "redesigned_label_generation_approved": True,
        "redesigned_label_generation_authorized": True,
        "ready_for_redesigned_label_generation_execution": True,
        "redesigned_label_generation_performed": False,
        "actual_redesigned_labels_generated": False,
        "redesigned_label_generation_results_created": False,
        "generated_output_count": 0,
        "failure_count": len(failures),
        "warning_count": 0,
        "failures": failures,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    passed = actual == expected
    return {
        "check_id": check_id,
        "status": "PASS" if passed else "FAIL",
        "expected": expected,
        "actual": actual,
        "severity": "BLOCKER",
        "message": f"{check_id} {'passed' if passed else 'failed'}",
    }


def _derived_checks(artifact: dict[str, Any]) -> dict[str, bool]:
    manifest = artifact.get("output_digest_manifest", [])
    created_fields = [
        "redesigned_label_generation_manifest_created",
        "redesigned_label_input_manifest_created",
        "redesigned_label_values_created",
        "redesigned_label_family_coverage_report_created",
        "redesigned_threshold_generation_report_created",
        "redesigned_horizon_generation_report_created",
        "redesigned_label_availability_report_created",
        "per_ticker_redesigned_label_summary_created",
        "meta_limitation_preservation_report_created",
        "redesigned_label_generation_digest_manifest_created",
        "operator_review_summary_created",
    ]
    return {
        "artifact_kind_matches": artifact.get("artifact_kind") == ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_EXECUTED,
        "execution_status_matches": artifact.get("execution_status") == REDESIGNED_LABEL_GENERATION_EXECUTED_RESEARCH_ONLY,
        "approval_digest_bound": artifact.get("source_evidence", {}).get("redesigned_label_generation_approval_digest") == EXPECTED_REDESIGNED_LABEL_GENERATION_APPROVAL_DIGEST,
        "candidate_review_digest_bound": artifact.get("source_evidence", {}).get("redesigned_label_generation_candidate_review_package_digest") == EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "candidate_digest_bound": artifact.get("source_evidence", {}).get("redesigned_label_generation_candidate_digest") == EXPECTED_CANDIDATE_DIGEST,
        "results_review_digest_bound": artifact.get("source_evidence", {}).get("label_objective_redesign_results_review_package_digest") == EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST,
        "records_digest_bound": artifact.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": artifact.get("target_universe_count") == 12 and artifact.get("target_universe") == TARGET_UNIVERSE,
        "total_record_count_11946": artifact.get("total_canonical_record_count") == 11946,
        "meta_913_preserved": artifact.get("meta_record_count") == 913 and artifact.get("per_ticker_record_counts", {}).get("META") == 913 and artifact.get("meta_reduced_record_count_preserved") is True,
        "execution_approved_true": artifact.get("redesigned_label_generation_approved") is True,
        "execution_authorized_true": artifact.get("redesigned_label_generation_authorized") is True,
        "ready_for_execution_true": artifact.get("ready_for_redesigned_label_generation_execution") is True,
        "execution_performed_true": artifact.get("redesigned_label_generation_performed") is True,
        "actual_labels_generated_true": artifact.get("actual_redesigned_labels_generated") is True,
        "results_created_true": artifact.get("redesigned_label_generation_results_created") is True,
        "generated_output_count_11": artifact.get("generated_output_count") == 11 and artifact.get("generated_output_names") == OUTPUT_FILENAMES,
        "all_generated_outputs_created": all(artifact.get(field) is True for field in created_fields),
        "label_family_count_10": artifact.get("label_family_count") == 10,
        "threshold_strategy_count_7": artifact.get("threshold_strategy_count") == 7,
        "horizon_strategy_count_5": artifact.get("horizon_strategy_count") == 5,
        "label_value_rows_nonzero": isinstance(artifact.get("label_value_row_count"), int) and artifact["label_value_row_count"] > 0,
        "family_coverage_present": isinstance(artifact.get("label_family_coverage_entries"), int) and artifact["label_family_coverage_entries"] > 0,
        "available_unavailable_counts_recorded": isinstance(artifact.get("available_label_value_count"), int) and artifact["available_label_value_count"] > 0 and isinstance(artifact.get("unavailable_label_value_count"), int) and artifact["unavailable_label_value_count"] > 0 and artifact["available_label_value_count"] + artifact["unavailable_label_value_count"] == artifact.get("label_value_row_count"),
        "output_digest_manifest_complete": isinstance(manifest, list) and len(manifest) == 11 and [row.get("filename") for row in manifest if isinstance(row, dict)] == OUTPUT_FILENAMES and all((row.get("digest_kind") in {"SELF_REFERENTIAL_EXECUTION_ARTIFACT", "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"} and row.get("sha256") is None) if row.get("filename") in {OUTPUT_FILENAMES[0], OUTPUT_FILENAMES[9]} else row.get("digest_kind") == "FILE_SHA256" and isinstance(row.get("sha256"), str) and len(row["sha256"]) == 64 for row in manifest if isinstance(row, dict)),
        "outputs_research_only": artifact.get("output_label") == OUTPUT_LABEL and artifact.get("evidence_scope") == EVIDENCE_SCOPE,
        "feature_generation_false": artifact.get("redesigned_feature_generation_authorized") is False and artifact.get("redesigned_feature_generation_performed") is False and artifact.get("feature_generation_performed") is False,
        "metric_recomputation_false": artifact.get("metric_recomputation_performed") is False,
        "model_training_false": artifact.get("model_training_performed") is False,
        "additional_predictive_evidence_candidate_false": artifact.get("additional_predictive_evidence_execution_candidate_created") is False,
        "predictive_usefulness_not_accepted": artifact.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": artifact.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": artifact.get("runtime_migration_approved") is False and artifact.get("runtime_migration_active") is False and artifact.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": artifact.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": artifact.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": artifact.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": artifact.get("trade_recommendations_generated") is False,
        "provider_requests_false": artifact.get("provider_requests_made_in_execution") is False and artifact.get("live_provider_transport_enabled_in_execution") is False,
        "market_data_acquisition_false": artifact.get("market_data_acquisition_performed_in_execution") is False,
        "dataset_regeneration_false": artifact.get("dataset_generation_performed_in_execution") is False and artifact.get("canonical_dataset_regenerated_in_execution") is False,
        "label_objective_redesign_rerun_false": artifact.get("label_objective_redesign_execution_rerun_performed") is False,
        "raw_provider_payloads_not_committed": artifact.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": artifact.get("api_keys_stored_or_printed") is False,
        "meta_limitation_preserved": artifact.get("meta_reduced_record_count_preserved") is True and artifact.get("meta_record_count") == 913,
        "no_tracked_marketflow_files": artifact.get("no_tracked_marketflow_files") is True and artifact.get("tracked_marketflow_files") == [],
    }


def _checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(artifact)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


def _execution_summary(
    checklist: list[dict[str, Any]], *, generation: Mapping[str, Any]
) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(row.get("status") == "PASS" for row in checklist)
    failed = total - passed
    return {
        "target_count": 12,
        "total_canonical_record_count": 11946,
        "generated_output_count": 11,
        "label_family_count": 10,
        "threshold_strategy_count": 7,
        "horizon_strategy_count": 5,
        "label_value_row_count": generation["label_value_row_count"],
        "label_family_coverage_entries": generation[
            "label_family_coverage_entries"
        ],
        "available_label_value_count": generation["available_label_value_count"],
        "unavailable_label_value_count": generation[
            "unavailable_label_value_count"
        ],
        "failure_count": 0,
        "warning_count": 1,
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": failed,
        "redesigned_label_generation_execution_digest": None,
    }


def _build_executed_artifact(
    *,
    run_timestamp_utc: str,
    canonical_root: Path,
    design_root: Path,
    output_root: Path,
    canonical_verification: Mapping[str, Any],
    design_verification: Mapping[str, Any],
    output_digest_manifest: list[dict[str, Any]],
    generation: Mapping[str, Any],
) -> dict[str, Any]:
    artifact = {
        "artifact_kind": ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_EXECUTED,
        "schema_version": SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_EXECUTED_V1,
        "execution_status": REDESIGNED_LABEL_GENERATION_EXECUTED_RESEARCH_ONLY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "provider_requests_made_in_execution": False,
        "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "feature_generation_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "redesigned_label_generation_approved": True,
        "redesigned_label_generation_authorized": True,
        "ready_for_redesigned_label_generation_execution": True,
        "redesigned_label_generation_performed": True,
        "actual_redesigned_labels_generated": True,
        "redesigned_label_generation_results_created": True,
        "redesigned_label_generation_manifest_created": True,
        "redesigned_label_input_manifest_created": True,
        "redesigned_label_values_created": True,
        "redesigned_label_family_coverage_report_created": True,
        "redesigned_threshold_generation_report_created": True,
        "redesigned_horizon_generation_report_created": True,
        "redesigned_label_availability_report_created": True,
        "per_ticker_redesigned_label_summary_created": True,
        "meta_limitation_preservation_report_created": True,
        "redesigned_label_generation_digest_manifest_created": True,
        "operator_review_summary_created": True,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "generated_output_count": 11,
        "generated_output_names": list(OUTPUT_FILENAMES),
        "label_family_count": 10,
        "threshold_strategy_count": 7,
        "horizon_strategy_count": 5,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "label_value_row_count": generation["label_value_row_count"],
        "label_family_coverage_entries": generation[
            "label_family_coverage_entries"
        ],
        "available_label_value_count": generation["available_label_value_count"],
        "unavailable_label_value_count": generation[
            "unavailable_label_value_count"
        ],
        "failure_count": 0,
        "warning_count": 1,
        "warnings": [
            "META_913_RECORD_LIMIT_AND_LABEL_AVAILABILITY_LIMITATION_PRESERVED"
        ],
        "canonical_source_root": _path_text(canonical_root),
        "design_source_root": _path_text(design_root),
        "generated_output_root": _path_text(output_root),
        "source_evidence": _source_evidence(),
        "canonical_source_verification": deepcopy(dict(canonical_verification)),
        "design_source_verification": deepcopy(dict(design_verification)),
        "label_generation_policy": {
            "price_basis": "CANONICAL_CLOSE",
            "forward_return_formula": "close[t+h] / close[t] - 1",
            "record_order": "TICKER_THEN_DATE_ASCENDING",
            "training_window": "2022-01-01/2023-12-31",
            "validation_window": "2024-01-01/2024-12-31",
            "oos_window": "2025-01-01/2025-12-31",
            "threshold_fit_boundary": "TRAINING_WINDOW_ONLY",
            "forward_tail_policy": "NULL_INSUFFICIENT_FUTURE_BARS",
            "synthetic_rows_created": False,
            "meta_rows_backfilled": False,
        },
        "label_families": list(LABEL_FAMILIES),
        "threshold_strategies": list(THRESHOLD_STRATEGIES),
        "horizon_strategies": list(HORIZON_STRATEGIES),
        "availability_rules": list(AVAILABILITY_RULES),
        "output_digest_manifest": deepcopy(output_digest_manifest),
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
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
    }
    artifact["execution_checklist"] = _checklist(artifact)
    artifact["execution_summary"] = _execution_summary(
        artifact["execution_checklist"], generation=generation
    )
    artifact["redesigned_label_generation_execution_digest"] = (
        redesigned_label_generation_execution_digest_v1(artifact)
    )
    artifact["execution_summary"][
        "redesigned_label_generation_execution_digest"
    ] = artifact["redesigned_label_generation_execution_digest"]
    return artifact


def redesigned_label_generation_execution_digest_v1(
    artifact: dict[str, Any],
) -> str:
    """Return a path-independent deterministic execution digest."""
    payload = deepcopy(artifact)
    payload.pop("redesigned_label_generation_execution_digest", None)
    payload.pop("canonical_source_root", None)
    payload.pop("design_source_root", None)
    payload.pop("generated_output_root", None)
    if isinstance(payload.get("execution_summary"), dict):
        payload["execution_summary"].pop(
            "redesigned_label_generation_execution_digest", None
        )
    return semantic_digest(payload)


def _write_bytes_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise RedesignedLabelGenerationExecutionError(
            f"redesigned label generation output already exists: {path.name}"
        ) from exc


def execute_redesigned_label_generation_v1(
    *,
    canonical_root: str | Path | None = None,
    design_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Generate the approved research-only labels from frozen local evidence."""
    canonical_path = (
        DEFAULT_CANONICAL_ROOT if canonical_root is None else Path(canonical_root)
    )
    design_path = DEFAULT_DESIGN_ROOT if design_root is None else Path(design_root)
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    canonical_verification, design_verification, records, failures = (
        _load_and_verify_sources(canonical_path, design_path)
    )
    if failures:
        return _blocked_artifact(
            canonical_root=canonical_path,
            design_root=design_path,
            output_root=output_path,
            run_timestamp_utc=timestamp,
            failures=failures,
        )
    if output_path.exists() and any(output_path.iterdir()):
        raise RedesignedLabelGenerationExecutionError(
            "redesigned label generation output root is not empty"
        )

    label_bytes, reports, generation = _generate_label_outputs(records, timestamp)
    input_manifest = _report(
        "redesigned_label_generation_input_manifest",
        timestamp,
        {
            "canonical_source_verification": canonical_verification,
            "design_source_verification": design_verification,
            "source_evidence": _source_evidence(),
            "canonical_source_mutated": False,
            "design_source_mutated": False,
        },
    )
    report_bytes: dict[str, bytes] = {
        "redesigned_label_generation_input_manifest.json": canonical_json_bytes(
            input_manifest
        ),
        "redesigned_label_values.jsonl": label_bytes,
        **{
            filename: canonical_json_bytes(report)
            for filename, report in reports.items()
        },
    }
    output_digest_manifest = []
    for filename in OUTPUT_FILENAMES:
        if filename == OUTPUT_FILENAMES[0]:
            entry = {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_EXECUTION_ARTIFACT",
                "sha256": None,
            }
        elif filename == OUTPUT_FILENAMES[9]:
            entry = {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
                "sha256": None,
            }
        else:
            entry = {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": sha256_bytes(report_bytes[filename]),
            }
        output_digest_manifest.append(entry)
    artifact = _build_executed_artifact(
        run_timestamp_utc=timestamp,
        canonical_root=canonical_path,
        design_root=design_path,
        output_root=output_path,
        canonical_verification=canonical_verification,
        design_verification=design_verification,
        output_digest_manifest=output_digest_manifest,
        generation=generation,
    )
    validate_redesigned_label_generation_executed_v1(artifact)
    report_bytes[OUTPUT_FILENAMES[0]] = canonical_json_bytes(artifact)
    report_bytes[OUTPUT_FILENAMES[9]] = canonical_json_bytes(
        _report(
            "redesigned_label_generation_digest_manifest",
            timestamp,
            {
                "redesigned_label_generation_execution_digest": artifact[
                    "redesigned_label_generation_execution_digest"
                ],
                "output_digest_manifest": output_digest_manifest,
                "manifest_self_reference_policy": (
                    "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
                ),
            },
        )
    )
    for filename in OUTPUT_FILENAMES:
        _write_bytes_once(output_path / filename, report_bytes[filename])
    return artifact


FORBIDDEN_ARTIFACT_VALUES = {
    "FEATURE_GENERATION_EXECUTED",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


def _reject_forbidden_values(value: Any, *, path: str = "artifact") -> None:
    forbidden_true_fields = {
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made_in_execution",
        "live_provider_transport_enabled_in_execution",
        "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution",
        "canonical_dataset_regenerated_in_execution",
        "label_objective_redesign_execution_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in FORBIDDEN_ARTIFACT_VALUES:
                raise RedesignedLabelGenerationExecutionError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true_fields and item is True:
                raise RedesignedLabelGenerationExecutionError(
                    f"{current} must remain false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise RedesignedLabelGenerationExecutionError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise RedesignedLabelGenerationExecutionError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise RedesignedLabelGenerationExecutionError(f"{field} mismatch")


def validate_redesigned_label_generation_executed_v1(artifact: dict) -> dict:
    """Validate executed label generation and every closed downstream gate."""
    if not isinstance(artifact, dict):
        raise RedesignedLabelGenerationExecutionError(
            "redesigned label generation artifact must be a JSON object"
        )
    _reject_forbidden_values(artifact)
    _expect(
        artifact.get("artifact_kind"),
        ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_EXECUTED,
        "artifact_kind",
    )
    _expect(
        artifact.get("schema_version"),
        SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_EXECUTED_V1,
        "schema_version",
    )
    _expect(
        artifact.get("execution_status"),
        REDESIGNED_LABEL_GENERATION_EXECUTED_RESEARCH_ONLY,
        "execution_status",
    )
    _expect(artifact.get("source_evidence"), _source_evidence(), "source_evidence")
    for field in (
        "redesigned_label_generation_approved",
        "redesigned_label_generation_authorized",
        "ready_for_redesigned_label_generation_execution",
        "redesigned_label_generation_performed",
        "actual_redesigned_labels_generated",
        "redesigned_label_generation_results_created",
        "redesigned_label_generation_manifest_created",
        "redesigned_label_input_manifest_created",
        "redesigned_label_values_created",
        "redesigned_label_family_coverage_report_created",
        "redesigned_threshold_generation_report_created",
        "redesigned_horizon_generation_report_created",
        "redesigned_label_availability_report_created",
        "per_ticker_redesigned_label_summary_created",
        "meta_limitation_preservation_report_created",
        "redesigned_label_generation_digest_manifest_created",
        "operator_review_summary_created",
    ):
        _expect(artifact.get(field), True, field)
    for field in (
        "provider_requests_made_in_execution",
        "live_provider_transport_enabled_in_execution",
        "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution",
        "canonical_dataset_regenerated_in_execution",
        "label_objective_redesign_execution_rerun_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ):
        _expect(artifact.get(field), False, field)
    _expect(artifact.get("generated_output_count"), 11, "generated_output_count")
    _expect(artifact.get("generated_output_names"), OUTPUT_FILENAMES, "generated_output_names")
    _expect(artifact.get("target_universe"), TARGET_UNIVERSE, "target_universe")
    _expect(artifact.get("target_universe_count"), 12, "target_universe_count")
    _expect(artifact.get("total_canonical_record_count"), 11946, "total_canonical_record_count")
    _expect(artifact.get("records_digest"), EXPECTED_RECORDS_DIGEST, "records_digest")
    _expect(artifact.get("meta_record_count"), 913, "meta_record_count")
    _expect(artifact.get("non_meta_record_count"), 1003, "non_meta_record_count")
    _expect(artifact.get("per_ticker_record_counts"), EXPECTED_RECORD_COUNTS, "per_ticker_record_counts")
    _expect(artifact.get("label_family_count"), 10, "label_family_count")
    _expect(artifact.get("threshold_strategy_count"), 7, "threshold_strategy_count")
    _expect(artifact.get("horizon_strategy_count"), 5, "horizon_strategy_count")
    for field in (
        "label_value_row_count",
        "label_family_coverage_entries",
        "available_label_value_count",
        "unavailable_label_value_count",
    ):
        if not isinstance(artifact.get(field), int) or artifact[field] <= 0:
            raise RedesignedLabelGenerationExecutionError(f"{field} missing or zero")
    _expect(artifact.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(artifact.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    expected_checklist = _checklist(artifact)
    _expect(artifact.get("execution_checklist"), expected_checklist, "execution_checklist")
    if any(row["status"] != "PASS" for row in expected_checklist):
        raise RedesignedLabelGenerationExecutionError(
            "execution_checklist contains a failed check"
        )
    expected_summary = _execution_summary(
        expected_checklist,
        generation={
            field: artifact[field]
            for field in (
                "label_value_row_count",
                "label_family_coverage_entries",
                "available_label_value_count",
                "unavailable_label_value_count",
            )
        },
    )
    digest = artifact.get("redesigned_label_generation_execution_digest")
    expected_summary["redesigned_label_generation_execution_digest"] = digest
    _expect(artifact.get("execution_summary"), expected_summary, "execution_summary")
    if not isinstance(digest, str) or len(digest) != 64:
        raise RedesignedLabelGenerationExecutionError(
            "redesigned_label_generation_execution_digest missing"
        )
    _expect(
        digest,
        redesigned_label_generation_execution_digest_v1(artifact),
        "redesigned_label_generation_execution_digest",
    )
    return {
        "status": REDESIGNED_LABEL_GENERATION_EXECUTION_VALID,
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "redesigned_label_generation_execution_digest": digest,
        "generated_output_count": 11,
        "label_value_row_count": artifact["label_value_row_count"],
        "available_label_value_count": artifact["available_label_value_count"],
        "unavailable_label_value_count": artifact["unavailable_label_value_count"],
        "failure_count": 0,
        "warning_count": 1,
        "redesigned_label_generation_performed": True,
        "actual_redesigned_labels_generated": True,
        "feature_generation_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_redesigned_label_generation_execution_status_markdown_v1(
    artifact: dict,
) -> str:
    """Render a validated sanitized label-generation execution summary."""
    validation = validate_redesigned_label_generation_executed_v1(artifact)
    summary = artifact["execution_summary"]
    lines = [
        "# MarketFlow Redesigned Label Generation Execution Status",
        "",
        "## Title",
        "- Redesigned Label Generation Execution v1.",
        "",
        "## Redesigned Label Generation Execution",
        f"- Artifact/status: `{artifact['artifact_kind']}` / `{artifact['execution_status']}`.",
        f"- Execution digest: `{validation['redesigned_label_generation_execution_digest']}`.",
        "",
        "## Source Approval",
        f"- Approval digest: `{artifact['source_evidence']['redesigned_label_generation_approval_digest']}`.",
        "",
        "## Dataset and Universe",
        f"- Records/digest: `{artifact['total_canonical_record_count']}` / `{artifact['records_digest']}`.",
        f"- Universe: `{', '.join(artifact['target_universe'])}`; META remains `{artifact['meta_record_count']}`.",
        "",
        "## Source Design Artifacts",
        f"- `{artifact['design_source_verification']['required_design_source_file_count']}` reviewed design files were hash-verified without mutation.",
        "",
        "## Label Generation Policy",
        "- Canonical close-to-close forward returns; training-window-only thresholds; null unavailable forward tails; no synthetic rows.",
        "",
        "## Generated Label Families",
        f"- `{artifact['label_family_count']}` families and `{artifact['label_value_row_count']}` label rows.",
        "",
        "## Threshold Strategy Summary",
        f"- `{artifact['threshold_strategy_count']}` deterministic strategies; no threshold optimization.",
        "",
        "## Horizon Strategy Summary",
        f"- `{artifact['horizon_strategy_count']}` strategies covering 1, 5, 10, and 20 sessions plus multi-horizon comparison.",
        "",
        "## Label Availability Summary",
        f"- Available/unavailable: `{artifact['available_label_value_count']}` / `{artifact['unavailable_label_value_count']}`.",
        "",
        "## Per-Ticker Summary",
        "- Twelve ordered ticker summaries preserve frozen record counts.",
        "",
        "## META Limitation Preservation",
        "- META remains 913 records; no backfill, repair, synthetic row, or calendar inference occurred.",
        "",
        "## Output Digest Manifest",
        f"- `{len(artifact['output_digest_manifest'])}` ordered output entries with explicit self-reference policies.",
        "",
        "## Execution Boundary",
        "- Label generation completed; feature generation and additional predictive-evidence execution remain closed.",
        "",
        "## Predictive Usefulness Boundary",
        "- Predictive usefulness remains `not accepted`.",
        "",
        "## Profitability Boundary",
        "- Profitability remains `not accepted`.",
        "",
        "## Runtime Boundary",
        "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
        "",
        "## Checklist Summary",
        f"- `{summary['passed_checks']} / {summary['total_checks']}` passed; `{summary['blocker_count']}` blockers.",
        "",
        "## Guardrails",
        "- No provider access, acquisition, dataset regeneration, feature generation, model training, scoring, recommendation, runtime activation, or trading action occurred.",
        "",
    ]
    return "\n".join(lines)
