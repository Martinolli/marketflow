"""Service-only data horizon and parameter sufficiency diagnostics."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.services.artifact_service import list_report_artifacts


SUFFICIENT = "sufficient"
LIMITED = "limited"
INSUFFICIENT = "insufficient"
PROVIDER_LIMITED = "provider_limited"
NOT_YET_MATURE = "not_yet_mature"
UNKNOWN = "unknown"

LOW_TIMEFRAME_REVIEW = {"1m", "5m"}
MICRO_TIMEFRAMES = {"15m", "30m"}
TACTICAL_TIMEFRAMES = {"1h", "2h", "4h"}
MACRO_TIMEFRAMES = {"1d", "1w", "1mo"}

DEFAULT_MINIMUM_ROWS_FLOOR = 100
DEFAULT_MULTIPLIER = 3

DEFAULT_TIMEFRAME_PERIODS = {
    "1mo": "5y",
    "1w": "2y",
    "1d": "365d",
    "4h": "100d",
    "2h": "60d",
    "1h": "150d",
    "30m": "20d",
    "15m": "20d",
    "5m": "20d",
    "1m": "20d",
}

TIMEFRAME_TOKENS = tuple(DEFAULT_TIMEFRAME_PERIODS.keys())
DERIVATIVE_CSV_MARKERS = (
    "_pv_eigen.csv",
    "_backtest_candidates",
    "_backtest_results",
)


def _json_safe_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _json_safe_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe_value(item) for item in value]
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            value = value.item()
        except (AttributeError, TypeError, ValueError):
            pass
    if hasattr(value, "isoformat") and not isinstance(value, (str, bytes, bytearray)):
        try:
            return value.isoformat()
        except (TypeError, ValueError):
            pass
    try:
        is_missing = pd.isna(value)
    except (TypeError, ValueError):
        is_missing = False
    try:
        if bool(is_missing):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _is_missing(value: Any) -> bool:
    value = _json_safe_value(value)
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def _to_int(value: Any) -> int | None:
    value = _json_safe_value(value)
    if value is None or isinstance(value, bool):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    if not parsed.is_integer():
        return None
    return int(parsed)


def _to_float(value: Any) -> float | None:
    value = _json_safe_value(value)
    if value is None or isinstance(value, bool):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def infer_timeframe_from_csv_name(path: str | Path | None) -> str | None:
    if _is_missing(path):
        return None
    stem = Path(str(path)).stem.lower().replace("-", "_")
    tokens = [token for token in stem.split("_") if token]
    for token in tokens:
        if token in TIMEFRAME_TOKENS:
            return token
    for token in TIMEFRAME_TOKENS:
        if f"_{token}_" in f"_{stem}_":
            return token
    return None


def infer_ticker_from_csv_name(path: str | Path | None) -> str | None:
    if _is_missing(path):
        return None
    name = Path(str(path)).name
    stem = Path(name).stem.replace("-", "_")
    tokens = [token for token in stem.split("_") if token]
    timeframe = infer_timeframe_from_csv_name(path)
    if timeframe:
        for index, token in enumerate(tokens):
            if token.lower() == timeframe:
                return "_".join(tokens[:index]) or None
    return tokens[0] if tokens else None


def detect_timestamp_column(columns: list[str]) -> str | None:
    preferred = ["timestamp", "datetime", "date", "time", "Date", "Datetime"]
    column_names = [str(column) for column in columns or []]
    for name in preferred:
        if name in column_names:
            return name
    lower_to_column = {name.lower(): name for name in column_names}
    for name in preferred:
        match = lower_to_column.get(name.lower())
        if match:
            return match
    for name in column_names:
        lowered = name.lower()
        if "timestamp" in lowered or "datetime" in lowered:
            return name
    return None


def calculate_minimum_rows_required(
    *,
    eigen_window: int | None = None,
    monte_carlo_horizon: int | None = None,
    backtest_horizon: int | None = None,
    floor: int = DEFAULT_MINIMUM_ROWS_FLOOR,
    multiplier: int = DEFAULT_MULTIPLIER,
) -> int:
    requirements = [_to_int(floor) or DEFAULT_MINIMUM_ROWS_FLOOR]
    for value in (eigen_window, monte_carlo_horizon, backtest_horizon):
        parsed = _to_int(value)
        if parsed is not None and parsed > 0:
            requirements.append(parsed * int(multiplier))
    return max(requirements)


def classify_row_sufficiency(
    *,
    rows_available: int | None,
    minimum_rows_required: int | None,
) -> str:
    rows = _to_int(rows_available)
    minimum = _to_int(minimum_rows_required)
    if rows is None or minimum is None or minimum <= 0:
        return UNKNOWN
    if rows < minimum * 0.5:
        return INSUFFICIENT
    if rows < minimum:
        return LIMITED
    return SUFFICIENT


def classify_window_sufficiency(rows_available: int | None, window: int | None) -> str:
    rows = _to_int(rows_available)
    parsed_window = _to_int(window)
    if rows is None or parsed_window is None or parsed_window <= 0:
        return UNKNOWN
    if rows < parsed_window:
        return INSUFFICIENT
    if rows < parsed_window * DEFAULT_MULTIPLIER:
        return LIMITED
    return SUFFICIENT


def build_timeframe_warnings(timeframe: str | None, rows_available: int | None = None) -> dict[str, Any]:
    normalized_timeframe = str(timeframe).strip().lower() if not _is_missing(timeframe) else None
    rows = _to_int(rows_available)
    notes: list[str] = []
    provider_limit_warning: str | None = None
    noise_warning: str | None = None

    if not normalized_timeframe:
        notes.append("timeframe_unknown")
    elif normalized_timeframe in LOW_TIMEFRAME_REVIEW:
        noise_warning = "high_noise_review_only"
        notes.append("low_timeframe_review_only")
    elif normalized_timeframe == "15m":
        noise_warning = "strong_noise_caution"
        notes.append("micro_timeframe_noise_caution")
    elif normalized_timeframe == "30m":
        noise_warning = "noise_caution"
        notes.append("micro_timeframe_noise_caution")

    if normalized_timeframe in LOW_TIMEFRAME_REVIEW | MICRO_TIMEFRAMES and rows is not None and rows < 200:
        provider_limit_warning = "possible_intraday_provider_limit"
        notes.append("small_intraday_row_count")

    return {
        "provider_limit_warning": provider_limit_warning,
        "noise_warning": noise_warning,
        "notes": notes,
    }


def _bars_remaining_to_maturity(backtest_horizon: int | None, future_bars_available: int | None) -> int | None:
    horizon = _to_int(backtest_horizon)
    future_bars = _to_int(future_bars_available)
    if horizon is None or future_bars is None:
        return None
    return max(horizon - future_bars, 0)


def _calibration_status(
    *,
    data_sufficiency_status: str,
    backtest_sufficiency_status: str,
    backtest_horizon: int | None,
    future_bars_available: int | None,
) -> str:
    future_bars = _to_int(future_bars_available)
    horizon = _to_int(backtest_horizon)
    if future_bars is not None:
        if future_bars == 0:
            return NOT_YET_MATURE
        if horizon is not None and 0 < future_bars < horizon:
            return NOT_YET_MATURE
    if data_sufficiency_status == INSUFFICIENT or backtest_sufficiency_status == INSUFFICIENT:
        return INSUFFICIENT
    if data_sufficiency_status == UNKNOWN and backtest_sufficiency_status == UNKNOWN:
        return UNKNOWN
    if data_sufficiency_status == LIMITED or backtest_sufficiency_status == LIMITED:
        return LIMITED
    return data_sufficiency_status if data_sufficiency_status != UNKNOWN else backtest_sufficiency_status


def assess_csv_data_sufficiency(
    csv_path: str | Path,
    *,
    timeframe: str | None = None,
    configured_period: str | None = None,
    eigen_window: int | None = None,
    monte_carlo_horizon: int | None = None,
    backtest_horizon: int | None = None,
    future_bars_available: int | None = None,
) -> dict[str, Any]:
    path = Path(csv_path)
    result = {
        "success": False,
        "ticker": infer_ticker_from_csv_name(path),
        "timeframe": timeframe or infer_timeframe_from_csv_name(path),
        "source_csv": str(path),
        "source_csv_name": path.name,
        "rows_available": None,
        "first_timestamp": None,
        "last_timestamp": None,
        "timestamp_column": None,
        "configured_period": configured_period,
        "eigen_window": _to_int(eigen_window),
        "monte_carlo_horizon": _to_int(monte_carlo_horizon),
        "backtest_horizon": _to_int(backtest_horizon),
        "minimum_rows_required": None,
        "future_bars_available": _to_int(future_bars_available),
        "bars_remaining_to_maturity": None,
        "data_sufficiency_status": UNKNOWN,
        "eigen_sufficiency_status": UNKNOWN,
        "monte_carlo_sufficiency_status": UNKNOWN,
        "backtest_sufficiency_status": UNKNOWN,
        "calibration_sufficiency_status": UNKNOWN,
        "provider_limit_warning": None,
        "noise_warning": None,
        "notes": [],
        "warnings": [],
        "errors": [],
    }

    if _is_missing(result["configured_period"]) and result["timeframe"] in DEFAULT_TIMEFRAME_PERIODS:
        result["configured_period"] = DEFAULT_TIMEFRAME_PERIODS[result["timeframe"]]

    try:
        dataframe = pd.read_csv(path)
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result

    rows_available = len(dataframe)
    result["rows_available"] = rows_available
    timestamp_column = detect_timestamp_column([str(column) for column in dataframe.columns])
    result["timestamp_column"] = timestamp_column
    if timestamp_column:
        series = dataframe[timestamp_column].dropna()
        if not series.empty:
            result["first_timestamp"] = _json_safe_value(series.iloc[0])
            result["last_timestamp"] = _json_safe_value(series.iloc[-1])
    else:
        result["warnings"].append("No timestamp column was detected.")
        result["notes"].append("timestamp_column_missing")

    minimum_rows_required = calculate_minimum_rows_required(
        eigen_window=result["eigen_window"],
        monte_carlo_horizon=result["monte_carlo_horizon"],
        backtest_horizon=result["backtest_horizon"],
    )
    result["minimum_rows_required"] = minimum_rows_required
    result["data_sufficiency_status"] = classify_row_sufficiency(
        rows_available=rows_available,
        minimum_rows_required=minimum_rows_required,
    )
    result["eigen_sufficiency_status"] = classify_window_sufficiency(rows_available, result["eigen_window"])
    result["monte_carlo_sufficiency_status"] = classify_window_sufficiency(rows_available, result["monte_carlo_horizon"])
    result["backtest_sufficiency_status"] = classify_window_sufficiency(rows_available, result["backtest_horizon"])
    result["bars_remaining_to_maturity"] = _bars_remaining_to_maturity(
        result["backtest_horizon"],
        result["future_bars_available"],
    )
    result["calibration_sufficiency_status"] = _calibration_status(
        data_sufficiency_status=result["data_sufficiency_status"],
        backtest_sufficiency_status=result["backtest_sufficiency_status"],
        backtest_horizon=result["backtest_horizon"],
        future_bars_available=result["future_bars_available"],
    )

    timeframe_warnings = build_timeframe_warnings(result["timeframe"], rows_available)
    result["provider_limit_warning"] = timeframe_warnings.get("provider_limit_warning")
    result["noise_warning"] = timeframe_warnings.get("noise_warning")
    result["notes"].extend(timeframe_warnings.get("notes") or [])
    result["success"] = True
    return {key: _json_safe_value(value) for key, value in result.items()}


def build_timeframe_sufficiency_profile(
    timeframe: str,
    rows_available: int,
    parameter_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    context = dict(parameter_context) if isinstance(parameter_context, dict) else {}
    configured_period = context.get("configured_period") or DEFAULT_TIMEFRAME_PERIODS.get(timeframe)
    eigen_window = _to_int(context.get("eigen_window"))
    monte_carlo_horizon = _to_int(context.get("monte_carlo_horizon"))
    backtest_horizon = _to_int(context.get("backtest_horizon"))
    minimum_rows_required = calculate_minimum_rows_required(
        eigen_window=eigen_window,
        monte_carlo_horizon=monte_carlo_horizon,
        backtest_horizon=backtest_horizon,
    )
    warnings = build_timeframe_warnings(timeframe, rows_available)
    profile = {
        "timeframe": timeframe,
        "rows_available": _to_int(rows_available),
        "configured_period": configured_period,
        "eigen_window": eigen_window,
        "monte_carlo_horizon": monte_carlo_horizon,
        "backtest_horizon": backtest_horizon,
        "minimum_rows_required": minimum_rows_required,
        "data_sufficiency_status": classify_row_sufficiency(
            rows_available=rows_available,
            minimum_rows_required=minimum_rows_required,
        ),
        "eigen_sufficiency_status": classify_window_sufficiency(rows_available, eigen_window),
        "monte_carlo_sufficiency_status": classify_window_sufficiency(rows_available, monte_carlo_horizon),
        "backtest_sufficiency_status": classify_window_sufficiency(rows_available, backtest_horizon),
        "provider_limit_warning": warnings.get("provider_limit_warning"),
        "noise_warning": warnings.get("noise_warning"),
        "notes": warnings.get("notes") or [],
    }
    return {key: _json_safe_value(value) for key, value in profile.items()}


def _is_canonical_source_csv(artifact: dict[str, Any]) -> bool:
    name = str(artifact.get("name") or "").lower()
    return name.endswith("_wyckoff_annotated.csv")


def _is_derivative_csv_name(name: str) -> bool:
    lowered = name.lower()
    return any(marker in lowered for marker in DERIVATIVE_CSV_MARKERS)


def _readable_fallback_csvs(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        artifact
        for artifact in artifacts
        if str(artifact.get("path") or "").lower().endswith(".csv")
        and not _is_derivative_csv_name(str(artifact.get("name") or artifact.get("path") or ""))
    ]


def _context_for_timeframe(parameter_context: dict[str, Any] | None, timeframe: str | None) -> dict[str, Any]:
    if not isinstance(parameter_context, dict):
        return {}
    context = {key: value for key, value in parameter_context.items() if key != "by_timeframe"}
    by_timeframe = parameter_context.get("by_timeframe")
    if isinstance(by_timeframe, dict) and timeframe in by_timeframe and isinstance(by_timeframe[timeframe], dict):
        context.update(by_timeframe[timeframe])
    return context


def _summary_for_rows(rows: list[dict[str, Any]], csv_file_count: int) -> dict[str, Any]:
    rows_available_values = [_to_int(row.get("rows_available")) for row in rows]
    rows_available_values = [value for value in rows_available_values if value is not None]
    minimum_values = [_to_int(row.get("minimum_rows_required")) for row in rows]
    minimum_values = [value for value in minimum_values if value is not None]
    statuses = [row.get("data_sufficiency_status") for row in rows]
    calibration_statuses = [row.get("calibration_sufficiency_status") for row in rows]
    return {
        "csv_file_count": csv_file_count,
        "sufficient_count": statuses.count(SUFFICIENT),
        "limited_count": statuses.count(LIMITED),
        "insufficient_count": statuses.count(INSUFFICIENT),
        "provider_limited_count": statuses.count(PROVIDER_LIMITED)
        + sum(1 for row in rows if not _is_missing(row.get("provider_limit_warning"))),
        "not_yet_mature_count": calibration_statuses.count(NOT_YET_MATURE),
        "unknown_count": statuses.count(UNKNOWN),
        "noise_warning_count": sum(1 for row in rows if not _is_missing(row.get("noise_warning"))),
        "provider_limit_warning_count": sum(1 for row in rows if not _is_missing(row.get("provider_limit_warning"))),
        "minimum_rows_required_max": max(minimum_values) if minimum_values else None,
        "rows_available_min": min(rows_available_values) if rows_available_values else None,
        "rows_available_max": max(rows_available_values) if rows_available_values else None,
    }


def summarize_report_folder_data_sufficiency(
    report_dir: str | Path,
    *,
    parameter_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    report_path = Path(report_dir)
    warnings: list[str] = []
    errors: list[str] = []
    artifacts = list_report_artifacts(str(report_path))
    csv_artifacts = [artifact for artifact in artifacts if str(artifact.get("path") or "").lower().endswith(".csv")]
    canonical_csvs = [artifact for artifact in csv_artifacts if _is_canonical_source_csv(artifact)]
    selected_csvs = canonical_csvs or _readable_fallback_csvs(csv_artifacts)
    if not canonical_csvs and selected_csvs:
        warnings.append("No canonical *_wyckoff_annotated.csv files found; using fallback readable CSVs.")

    rows: list[dict[str, Any]] = []
    for artifact in selected_csvs:
        path = artifact.get("path")
        timeframe = artifact.get("timeframe") or infer_timeframe_from_csv_name(path)
        context = _context_for_timeframe(parameter_context, timeframe)
        row = assess_csv_data_sufficiency(
            str(path),
            timeframe=timeframe,
            configured_period=context.get("configured_period"),
            eigen_window=context.get("eigen_window"),
            monte_carlo_horizon=context.get("monte_carlo_horizon"),
            backtest_horizon=context.get("backtest_horizon"),
            future_bars_available=context.get("future_bars_available"),
        )
        warnings.extend(f"{path}: {warning}" for warning in row.get("warnings") or [])
        if not row.get("success"):
            errors.extend(f"{path}: {error}" for error in row.get("errors") or [])
        rows.append(row)

    summary = _summary_for_rows(rows, len(selected_csvs))
    if not selected_csvs:
        warnings.append("No source CSV artifacts were found for data sufficiency assessment.")

    return {
        "success": bool(rows) and not errors,
        "report_dir": str(report_path),
        "csv_file_count": len(selected_csvs),
        "rows": rows,
        "summary": summary,
        "warnings": warnings,
        "errors": errors,
    }
