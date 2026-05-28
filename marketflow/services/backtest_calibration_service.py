"""Service-only summaries for deterministic backtest result CSV artifacts."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.services.artifact_service import list_report_artifacts


VALID_OUTCOMES = {"TP_FIRST", "SL_FIRST", "NEITHER", "AMBIGUOUS"}
INVALID_OUTCOME = "INVALID"
OUTCOME_COLUMNS = ("outcome",)
DEFAULT_GROUP_COLUMNS = ("ticker", "timeframe", "horizon_bars", "tie_break_policy")
SECONDARY_GROUP_COLUMNS = ("wyckoff_phase", "wyckoff_event", "trend")
SMALL_SAMPLE_THRESHOLD = 10
CAUTION_SAMPLE_THRESHOLD = 30


def _json_safe_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            value = value.item()
        except (AttributeError, TypeError, ValueError):
            pass
    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
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


def _to_bool(value: Any) -> bool:
    value = _json_safe_value(value)
    if value is True:
        return True
    if value is False or value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return bool(value)
    return False


def normalize_outcome(value: Any) -> str:
    """Normalize supported outcome labels, treating missing/unknown as INVALID."""

    if hasattr(value, "name") and not isinstance(value, (str, bytes, bytearray)):
        normalized = normalize_outcome(getattr(value, "name"))
        if normalized != INVALID_OUTCOME:
            return normalized
    if hasattr(value, "value") and not isinstance(value, (str, bytes, bytearray)):
        normalized = normalize_outcome(getattr(value, "value"))
        if normalized != INVALID_OUTCOME:
            return normalized

    value = _json_safe_value(value)
    if _is_missing(value):
        return INVALID_OUTCOME
    label = str(value).strip().upper()
    if label in VALID_OUTCOMES or label == INVALID_OUTCOME:
        return label
    return INVALID_OUTCOME


def read_backtest_results_csv(path: str | Path) -> dict[str, Any]:
    result = {
        "success": False,
        "path": str(path),
        "count": 0,
        "rows": [],
        "errors": [],
        "warnings": [],
    }

    try:
        dataframe = pd.read_csv(Path(path))
    except pd.errors.EmptyDataError:
        result["success"] = True
        result["warnings"].append("Backtest results CSV is empty.")
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result

    rows = [
        {str(key): _json_safe_value(value) for key, value in row.items()}
        for row in dataframe.where(pd.notna(dataframe), None).to_dict(orient="records")
    ]
    result["success"] = True
    result["count"] = len(rows)
    result["rows"] = rows
    if not rows:
        result["warnings"].append("Backtest results CSV is empty.")
    return result


def _numeric_values(rows: list[dict[str, Any]], column: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        parsed = _to_float(row.get(column))
        if parsed is not None:
            values.append(parsed)
    return values


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    sorted_values = sorted(values)
    midpoint = len(sorted_values) // 2
    if len(sorted_values) % 2:
        return sorted_values[midpoint]
    return (sorted_values[midpoint - 1] + sorted_values[midpoint]) / 2


def _rate(count: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return count / denominator


def _small_sample_warning(count: int) -> str | None:
    if count < SMALL_SAMPLE_THRESHOLD:
        return "small_sample"
    if count < CAUTION_SAMPLE_THRESHOLD:
        return "caution_sample"
    return None


def _summary_for_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    outcomes = [normalize_outcome(row.get("outcome")) for row in rows]
    count = len(rows)
    tp_first_count = outcomes.count("TP_FIRST")
    sl_first_count = outcomes.count("SL_FIRST")
    neither_count = outcomes.count("NEITHER")
    ambiguous_count = outcomes.count("AMBIGUOUS")
    invalid_count = outcomes.count(INVALID_OUTCOME)
    valid_count = count - invalid_count
    realized_values = _numeric_values(rows, "realized_R")
    bars_to_hit_values = _numeric_values(rows, "bars_to_hit")
    planned_rr_values = _numeric_values(rows, "planned_rr")
    future_bars_values = _numeric_values(rows, "future_bars_available")
    no_future_bars_count = sum(
        1
        for row in rows
        if _to_float(row.get("future_bars_available")) == 0
        or str(_json_safe_value(row.get("neither_reason")) or "").strip() == "no_future_bars_available"
    )
    partial_future_window_count = sum(
        1
        for row in rows
        if str(_json_safe_value(row.get("neither_reason")) or "").strip() == "partial_future_window_no_hit"
    )
    full_horizon_count = sum(
        1
        for row in rows
        if str(_json_safe_value(row.get("neither_reason")) or "").strip() == "full_horizon_no_hit"
    )

    return {
        "count": count,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "invalid_rate": _rate(invalid_count, count),
        "tp_first_count": tp_first_count,
        "sl_first_count": sl_first_count,
        "neither_count": neither_count,
        "ambiguous_count": ambiguous_count,
        "tp_first_rate": _rate(tp_first_count, count),
        "sl_first_rate": _rate(sl_first_count, count),
        "neither_rate": _rate(neither_count, count),
        "ambiguous_rate": _rate(ambiguous_count, count),
        "mean_realized_R": _mean(realized_values),
        "median_realized_R": _median(realized_values),
        "win_loss_ratio": None if sl_first_count == 0 else tp_first_count / sl_first_count,
        "mean_bars_to_hit": _mean(bars_to_hit_values),
        "median_bars_to_hit": _median(bars_to_hit_values),
        "mean_planned_rr": _mean(planned_rr_values),
        "mean_future_bars_available": _mean(future_bars_values),
        "median_future_bars_available": _median(future_bars_values),
        "no_future_bars_count": no_future_bars_count,
        "partial_future_window_count": partial_future_window_count,
        "full_horizon_count": full_horizon_count,
        "no_future_bars_rate": _rate(no_future_bars_count, count),
        "partial_future_window_rate": _rate(partial_future_window_count, count),
        "full_horizon_rate": _rate(full_horizon_count, count),
        "small_sample_warning": _small_sample_warning(count),
    }


def _available_group_columns(
    rows: list[dict[str, Any]],
    requested_columns: tuple[str, ...],
    warnings: list[str],
) -> list[str]:
    available_columns: list[str] = []
    for column in requested_columns:
        if any(column in row for row in rows):
            available_columns.append(column)
        else:
            warnings.append(f"Requested group column `{column}` is missing from all rows.")
    return available_columns


def _group_value(row: dict[str, Any], column: str) -> Any:
    value = _json_safe_value(row.get(column))
    if _is_missing(value):
        return "UNKNOWN"
    return value


def _group_key(values: tuple[Any, ...]) -> str:
    return "|".join(str(_json_safe_value(value)) for value in values)


def _sort_grouped_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    preferred = ("ticker", "timeframe", "horizon_bars", "tie_break_policy")

    def sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
        return tuple(str(row.get(column) or "") for column in preferred) + (str(row.get("group_key") or ""),)

    return sorted(rows, key=sort_key)


def _grouped_summary_rows(rows: list[dict[str, Any]], group_columns: list[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for row in rows:
        key = tuple(_group_value(row, column) for column in group_columns)
        grouped.setdefault(key, []).append(row)

    summary_rows: list[dict[str, Any]] = []
    for key, group_rows in grouped.items():
        summary = _summary_for_rows(group_rows)
        group_values = dict(zip(group_columns, key))
        summary_rows.append(
            {
                **group_values,
                "group_key": _group_key(key),
                **summary,
            }
        )
    return _sort_grouped_rows(summary_rows)


def _invalid_reason(row: dict[str, Any]) -> str:
    reason = row.get("outcome_error")
    if _is_missing(reason):
        reason = row.get("error")
    if _is_missing(reason):
        return "unspecified"
    return str(_json_safe_value(reason)).strip()


def _invalid_reason_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    invalid_rows = [row for row in rows if normalize_outcome(row.get("outcome")) == INVALID_OUTCOME]
    total_invalid = len(invalid_rows)
    counts: dict[str, int] = {}
    for row in invalid_rows:
        reason = _invalid_reason(row)
        counts[reason] = counts.get(reason, 0) + 1
    return [
        {"reason": reason, "count": count, "rate": _rate(count, total_invalid)}
        for reason, count in sorted(counts.items(), key=lambda item: item[0])
    ]


def summarize_backtest_results_rows(
    rows: list[dict[str, Any]],
    *,
    group_columns: tuple[str, ...] | list[str] | None = None,
) -> dict[str, Any]:
    warnings: list[str] = []
    errors: list[str] = []
    source_rows = [dict(row) for row in rows or [] if isinstance(row, dict)]

    if not source_rows:
        warnings.append("No backtest result rows to summarize.")
        return {
            "success": False,
            "count": 0,
            "summary": {},
            "summary_rows": [],
            "grouped_summary_rows": [],
            "invalid_reason_rows": [],
            "warnings": warnings,
            "errors": errors,
        }

    normalized_rows = [{**row, "outcome": normalize_outcome(row.get("outcome"))} for row in source_rows]
    requested_group_columns = tuple(group_columns) if group_columns is not None else DEFAULT_GROUP_COLUMNS
    available_group_columns = _available_group_columns(normalized_rows, requested_group_columns, warnings)

    grouped_rows: list[dict[str, Any]] = []
    if available_group_columns:
        grouped_rows = _grouped_summary_rows(normalized_rows, available_group_columns)
    else:
        warnings.append("No requested group columns are available; grouped summary is empty.")

    summary = _summary_for_rows(normalized_rows)
    return {
        "success": True,
        "count": len(normalized_rows),
        "summary": summary,
        "summary_rows": [summary],
        "grouped_summary_rows": grouped_rows,
        "invalid_reason_rows": _invalid_reason_rows(normalized_rows),
        "warnings": warnings,
        "errors": errors,
    }


def summarize_backtest_results_csv(
    path: str | Path,
    *,
    group_columns: tuple[str, ...] | list[str] | None = None,
) -> dict[str, Any]:
    read_result = read_backtest_results_csv(path)
    if not read_result.get("success"):
        return {
            "success": False,
            "path": str(path),
            "read_result": read_result,
            "count": 0,
            "summary": {},
            "summary_rows": [],
            "grouped_summary_rows": [],
            "invalid_reason_rows": [],
            "warnings": list(read_result.get("warnings") or []),
            "errors": list(read_result.get("errors") or []),
        }

    summary_result = summarize_backtest_results_rows(
        read_result.get("rows") or [],
        group_columns=group_columns,
    )
    warnings = list(read_result.get("warnings") or []) + list(summary_result.get("warnings") or [])
    errors = list(read_result.get("errors") or []) + list(summary_result.get("errors") or [])
    return {
        **summary_result,
        "success": bool(summary_result.get("success")),
        "path": str(path),
        "read_result": read_result,
        "warnings": warnings,
        "errors": errors,
    }


def summarize_backtest_results_folder(
    report_dir: str | Path,
    *,
    group_columns: tuple[str, ...] | list[str] | None = None,
) -> dict[str, Any]:
    report_path = Path(report_dir)
    warnings: list[str] = []
    errors: list[str] = []
    artifacts = list_report_artifacts(str(report_path))
    result_files = [
        str(artifact.get("path"))
        for artifact in artifacts
        if artifact.get("kind") == "backtest_results_csv" and artifact.get("path")
    ]

    if not result_files:
        warning = "No backtest_results_csv artifacts found."
        return {
            "success": False,
            "report_dir": str(report_path),
            "source_result_files": [],
            "file_count": 0,
            "read_count": 0,
            "count": 0,
            "summary": {},
            "summary_rows": [],
            "grouped_summary_rows": [],
            "invalid_reason_rows": [],
            "warnings": [warning],
            "errors": [warning],
        }

    all_rows: list[dict[str, Any]] = []
    read_count = 0
    for result_file in result_files:
        read_result = read_backtest_results_csv(result_file)
        warnings.extend(read_result.get("warnings") or [])
        if not read_result.get("success"):
            errors.extend(f"{result_file}: {error}" for error in read_result.get("errors") or [])
            continue
        read_count += 1
        rows = read_result.get("rows") or []
        for row in rows:
            all_rows.append({**row, "source_result_file": result_file})

    summary_result = summarize_backtest_results_rows(all_rows, group_columns=group_columns)
    warnings.extend(summary_result.get("warnings") or [])
    errors.extend(summary_result.get("errors") or [])

    return {
        "success": bool(summary_result.get("success")),
        "report_dir": str(report_path),
        "source_result_files": result_files,
        "file_count": len(result_files),
        "read_count": read_count,
        "count": summary_result.get("count", 0),
        "summary": summary_result.get("summary", {}),
        "summary_rows": summary_result.get("summary_rows", []),
        "grouped_summary_rows": summary_result.get("grouped_summary_rows", []),
        "invalid_reason_rows": summary_result.get("invalid_reason_rows", []),
        "warnings": warnings,
        "errors": errors,
    }
