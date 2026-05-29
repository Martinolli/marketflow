"""Markdown artifact writer for Monte Carlo forecast calibration summaries."""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

from marketflow.services.monte_carlo_calibration_service import summarize_monte_carlo_calibration_folder


MONTE_CARLO_CALIBRATION_SUMMARY_KIND = "monte_carlo_calibration_summary_md"

SUMMARY_COLUMNS = [
    "sample_count",
    "joined_count",
    "scoreable_count",
    "not_scoreable_count",
    "eligible_count",
    "not_yet_mature_count",
    "horizon_mismatch_count",
    "partial_future_window_count",
    "invalid_count",
    "ambiguous_count",
    "tp_actual_rate",
    "sl_actual_rate",
    "neither_actual_rate",
    "mean_forecast_tp_probability",
    "mean_forecast_sl_probability",
    "mean_forecast_neither_probability",
    "brier_score_tp",
    "brier_score_sl",
    "brier_score_neither",
    "small_sample_warning",
]
JOIN_COLUMNS = [
    "forecast_file",
    "ticker",
    "timeframe",
    "model",
    "mc_horizon_bars",
    "actual_horizon_bars",
    "actual_outcome",
    "future_bars_available",
    "join_method",
    "eligibility_status",
    "scoreable",
    "scoreable_reason",
]
UNMATCHED_FORECAST_COLUMNS = [
    "forecast_file",
    "ticker",
    "timeframe",
    "model",
    "mc_horizon_bars",
    "join_status",
    "join_warning",
]
UNMATCHED_OUTCOME_COLUMNS = [
    "actual_ticker",
    "actual_timeframe",
    "actual_candidate_snapshot_file",
    "actual_signal_row_index",
    "actual_outcome",
    "actual_horizon_bars",
    "join_status",
    "join_warning",
]


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if type(value).__name__ == "NAType":
        return True
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            return _is_missing(value.item())
        except (AttributeError, TypeError, ValueError):
            pass
    if isinstance(value, float) and math.isnan(value):
        return True
    return False


def _md_value(value: Any) -> str:
    if _is_missing(value):
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, Path):
        value = str(value)
    elif isinstance(value, float):
        value = f"{value:.4f}".rstrip("0").rstrip(".")
    elif isinstance(value, (list, tuple, set, dict)):
        try:
            value = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
        except (TypeError, ValueError):
            value = str(value)
    text = str(value)
    return text.replace("|", "\\|").replace("\r\n", " ").replace("\n", " ")


def _markdown_table(
    rows: list[dict[str, Any]],
    columns: list[str] | None = None,
    *,
    max_rows: int | None = None,
) -> str:
    if not rows:
        return "_No rows._"

    table_columns = list(columns) if columns is not None else list(rows[0].keys())
    display_rows = rows[:max_rows] if max_rows is not None else rows
    header = "| " + " | ".join(_md_value(column) for column in table_columns) + " |"
    separator = "| " + " | ".join("---" for _ in table_columns) + " |"
    body = [
        "| " + " | ".join(_md_value(row.get(column)) for column in table_columns) + " |"
        for row in display_rows
    ]
    table = "\n".join([header, separator, *body])
    if max_rows is not None and len(rows) > max_rows:
        table += f"\n\n_Showing {max_rows} of {len(rows)} rows._"
    return table


def _safe_filename_part(value: str | None) -> str | None:
    if _is_missing(value):
        return None
    safe = "".join(character if character.isalnum() or character in "._-" else "_" for character in str(value).strip())
    safe = safe.strip("._-")
    return safe or None


def _timestamp_for_filename(timestamp: str | None = None) -> str:
    safe_timestamp = _safe_filename_part(timestamp)
    if safe_timestamp:
        return safe_timestamp
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def build_monte_carlo_calibration_summary_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> str:
    stamp = _timestamp_for_filename(timestamp)
    ticker_part = _safe_filename_part(ticker)
    timeframe_part = _safe_filename_part(timeframe)
    if ticker_part and timeframe_part:
        return f"{ticker_part}_{timeframe_part}_monte_carlo_calibration_summary_{stamp}.md"
    return f"marketflow_monte_carlo_calibration_summary_{stamp}.md"


def _bullet_list(items: list[Any]) -> str:
    clean_items = [item for item in items if not _is_missing(item)]
    if not clean_items:
        return "_None._"
    return "\n".join(f"- {_md_value(item)}" for item in clean_items)


def _summary_rows(calibration_result: dict[str, Any]) -> list[dict[str, Any]]:
    rows = list(calibration_result.get("summary_rows") or [])
    if not rows and isinstance(calibration_result.get("summary"), dict) and calibration_result.get("summary"):
        rows = [calibration_result["summary"]]
    return rows


def _forecast_sources(calibration_result: dict[str, Any]) -> list[Any]:
    sources: list[Any] = []
    for row in calibration_result.get("forecast_rows") or []:
        if not isinstance(row, dict):
            continue
        sources.append(row.get("forecast_path") or row.get("forecast_file"))
    return sources


def _actual_sources(calibration_result: dict[str, Any]) -> list[Any]:
    sources: list[Any] = []
    for row in calibration_result.get("actual_rows") or []:
        if not isinstance(row, dict):
            continue
        sources.append(
            row.get("actual_candidate_snapshot_file")
            or row.get("actual_source_csv")
            or row.get("actual_join_key_preferred")
        )
    return sources


def build_monte_carlo_calibration_summary_markdown(
    calibration_result: dict[str, Any],
    *,
    title: str = "MarketFlow Monte Carlo Forecast Calibration Summary",
    created_at: str | None = None,
) -> str:
    result = dict(calibration_result) if isinstance(calibration_result, dict) else {}
    summary_rows = _summary_rows(result)
    summary = result.get("summary") if isinstance(result.get("summary"), dict) else {}
    created = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warnings = list(result.get("warnings") or [])
    errors = list(result.get("errors") or [])

    sections = [
        f"# {title}",
        "## Metadata",
        f"- Created: {_md_value(created)}",
        f"- Report directory: {_md_value(result.get('report_dir'))}",
        f"- Forecast files: {_md_value(result.get('forecast_file_count'))}",
        f"- Actual result files: {_md_value(result.get('actual_file_count'))}",
        f"- Forecast row count: {_md_value(len(result.get('forecast_rows') or []))}",
        f"- Actual row count: {_md_value(len(result.get('actual_rows') or []))}",
        f"- Joined row count: {_md_value(len(result.get('join_rows') or []))}",
        f"- Scoreable row count: {_md_value(summary.get('scoreable_count'))}",
        "- Forecast artifacts:",
        _bullet_list(_forecast_sources(result)),
        "- Actual outcome sources:",
        _bullet_list(_actual_sources(result)),
        "## Calibration Summary",
        _markdown_table(summary_rows, SUMMARY_COLUMNS),
        "## Grouped Summary",
        _markdown_table(list(result.get("grouped_summary_rows") or []), max_rows=100),
        "## Join Rows",
        _markdown_table(list(result.get("join_rows") or []), JOIN_COLUMNS, max_rows=50),
        "## Unmatched Forecasts",
        _markdown_table(list(result.get("unmatched_forecasts") or []), UNMATCHED_FORECAST_COLUMNS, max_rows=50),
        "## Unmatched Outcomes",
        _markdown_table(list(result.get("unmatched_outcomes") or []), UNMATCHED_OUTCOME_COLUMNS, max_rows=50),
        "## Warnings",
        _bullet_list(warnings),
        "## Errors",
        _bullet_list(errors),
        "## Guardrails",
        "- Calibration only.",
        "- This is not financial advice.",
        "- This does not create buy/sell signals.",
        "- This does not optimize parameters automatically.",
        "- Rows with no future bars are not forecast failures.",
        "- Horizon mismatches are not scoreable.",
        "- Small samples should not be overinterpreted.",
        "- Compare models only under similar ticker/timeframe/horizon conditions.",
        "",
    ]
    return "\n\n".join(sections)


def _collision_safe_path(output_dir: Path, filename: str) -> Path:
    target = output_dir / filename
    if not target.exists():
        return target

    stem = target.stem
    suffix = target.suffix or ".md"
    counter = 2
    while True:
        candidate = output_dir / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def write_monte_carlo_calibration_summary_markdown(
    calibration_result: dict[str, Any],
    output_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    result = {
        "success": False,
        "path": None,
        "filename": None,
        "kind": MONTE_CARLO_CALIBRATION_SUMMARY_KIND,
        "errors": [],
        "warnings": [],
    }

    try:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        filename = build_monte_carlo_calibration_summary_filename(
            ticker=ticker,
            timeframe=timeframe,
            timestamp=timestamp,
        )
        path = _collision_safe_path(directory, filename)
        markdown = build_monte_carlo_calibration_summary_markdown(calibration_result)
        path.write_text(markdown, encoding="utf-8")
        result["success"] = True
        result["path"] = str(path)
        result["filename"] = path.name
        result["warnings"].extend(calibration_result.get("warnings") or [])
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def summarize_folder_to_monte_carlo_calibration_markdown(
    report_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    calibration_result = summarize_monte_carlo_calibration_folder(report_dir)
    write_result = write_monte_carlo_calibration_summary_markdown(
        calibration_result,
        report_dir,
        ticker=ticker,
        timeframe=timeframe,
        timestamp=timestamp,
    )

    errors = list(calibration_result.get("errors") or []) + list(write_result.get("errors") or [])
    warnings = list(calibration_result.get("warnings") or []) + list(write_result.get("warnings") or [])
    return {
        "success": bool(calibration_result.get("success")) and bool(write_result.get("success")),
        "calibration_result": calibration_result,
        "write_result": write_result,
        "path": write_result.get("path"),
        "filename": write_result.get("filename"),
        "errors": errors,
        "warnings": warnings,
    }
