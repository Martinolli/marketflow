"""Markdown artifact writer for Data Horizon / Parameter Sufficiency diagnostics."""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

from marketflow.services.data_sufficiency_service import summarize_report_folder_data_sufficiency


DATA_SUFFICIENCY_SUMMARY_KIND = "data_sufficiency_summary_md"

CSV_ROW_COLUMNS = [
    "ticker",
    "timeframe",
    "source_csv_name",
    "rows_available",
    "first_timestamp",
    "last_timestamp",
    "configured_period",
    "eigen_window",
    "monte_carlo_horizon",
    "backtest_horizon",
    "minimum_rows_required",
    "future_bars_available",
    "bars_remaining_to_maturity",
    "data_sufficiency_status",
    "eigen_sufficiency_status",
    "monte_carlo_sufficiency_status",
    "backtest_sufficiency_status",
    "calibration_sufficiency_status",
    "noise_warning",
    "provider_limit_warning",
]

SUMMARY_COLUMNS = [
    "csv_file_count",
    "sufficient_count",
    "limited_count",
    "insufficient_count",
    "provider_limited_count",
    "not_yet_mature_count",
    "unknown_count",
    "noise_warning_count",
    "provider_limit_warning_count",
    "minimum_rows_required_max",
    "rows_available_min",
    "rows_available_max",
]

STATUS_LABELS = [
    "sufficient",
    "limited",
    "insufficient",
    "provider_limited",
    "not_yet_mature",
    "unknown",
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


def build_data_sufficiency_summary_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> str:
    stamp = _timestamp_for_filename(timestamp)
    ticker_part = _safe_filename_part(ticker)
    timeframe_part = _safe_filename_part(timeframe)
    if ticker_part and timeframe_part:
        return f"{ticker_part}_{timeframe_part}_data_sufficiency_summary_{stamp}.md"
    if ticker_part:
        return f"{ticker_part}_data_sufficiency_summary_{stamp}.md"
    return f"marketflow_data_sufficiency_summary_{stamp}.md"


def _bullet_list(items: list[Any]) -> str:
    clean_items = [item for item in items if not _is_missing(item)]
    if not clean_items:
        return "_None._"
    return "\n".join(f"- {_md_value(item)}" for item in clean_items)


def _summary_row(sufficiency_result: dict[str, Any]) -> dict[str, Any]:
    summary = sufficiency_result.get("summary") if isinstance(sufficiency_result.get("summary"), dict) else {}
    return dict(summary)


def _status_review_rows(sufficiency_result: dict[str, Any]) -> list[dict[str, Any]]:
    rows = list(sufficiency_result.get("rows") or [])
    summary = _summary_row(sufficiency_result)
    return [
        {
            "status": label,
            "data_status_count": summary.get(f"{label}_count"),
            "calibration_status_count": sum(
                1 for row in rows if isinstance(row, dict) and row.get("calibration_sufficiency_status") == label
            ),
        }
        for label in STATUS_LABELS
    ]


def _warning_review_rows(sufficiency_result: dict[str, Any]) -> list[dict[str, Any]]:
    warning_rows: list[dict[str, Any]] = []
    for row in sufficiency_result.get("rows") or []:
        if not isinstance(row, dict):
            continue
        if _is_missing(row.get("noise_warning")) and _is_missing(row.get("provider_limit_warning")):
            continue
        warning_rows.append(
            {
                "ticker": row.get("ticker"),
                "timeframe": row.get("timeframe"),
                "source_csv_name": row.get("source_csv_name"),
                "rows_available": row.get("rows_available"),
                "noise_warning": row.get("noise_warning"),
                "provider_limit_warning": row.get("provider_limit_warning"),
                "notes": row.get("notes"),
            }
        )
    return warning_rows


def build_data_sufficiency_summary_markdown(
    sufficiency_result: dict[str, Any],
    *,
    title: str = "MarketFlow Data Horizon / Parameter Sufficiency Summary",
    created_at: str | None = None,
) -> str:
    result = dict(sufficiency_result) if isinstance(sufficiency_result, dict) else {}
    summary = _summary_row(result)
    rows = list(result.get("rows") or [])
    created = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warnings = list(result.get("warnings") or [])
    errors = list(result.get("errors") or [])

    sections = [
        f"# {title}",
        "## Metadata",
        f"- Created: {_md_value(created)}",
        f"- Report directory: {_md_value(result.get('report_dir'))}",
        f"- CSV file count: {_md_value(result.get('csv_file_count') or summary.get('csv_file_count'))}",
        f"- Row count: {_md_value(len(rows))}",
        f"- Sufficient count: {_md_value(summary.get('sufficient_count'))}",
        f"- Limited count: {_md_value(summary.get('limited_count'))}",
        f"- Insufficient count: {_md_value(summary.get('insufficient_count'))}",
        f"- Unknown count: {_md_value(summary.get('unknown_count'))}",
        f"- Noise warning count: {_md_value(summary.get('noise_warning_count'))}",
        f"- Provider-limit warning count: {_md_value(summary.get('provider_limit_warning_count'))}",
        "## Summary",
        _markdown_table([summary] if summary else [], SUMMARY_COLUMNS),
        "## CSV Sufficiency Rows",
        _markdown_table(rows, CSV_ROW_COLUMNS, max_rows=100),
        "## Status Review",
        _markdown_table(_status_review_rows(result)),
        "## Warning Review",
        _markdown_table(_warning_review_rows(result)),
        "## Errors",
        _bullet_list(errors),
        "## Warnings",
        _bullet_list(warnings),
        "## Guardrails",
        "- Diagnostics only.",
        "- This is not financial advice.",
        "- This does not create buy/sell signals.",
        "- This does not optimize parameters automatically.",
        "- Sufficient data does not imply predictive validity.",
        "- Low-timeframe noise must remain visible.",
        "- Provider limitations must remain visible.",
        "- No future data leakage.",
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


def write_data_sufficiency_summary_markdown(
    sufficiency_result: dict[str, Any],
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
        "kind": DATA_SUFFICIENCY_SUMMARY_KIND,
        "errors": [],
        "warnings": [],
    }

    try:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        filename = build_data_sufficiency_summary_filename(
            ticker=ticker,
            timeframe=timeframe,
            timestamp=timestamp,
        )
        path = _collision_safe_path(directory, filename)
        markdown = build_data_sufficiency_summary_markdown(sufficiency_result)
        path.write_text(markdown, encoding="utf-8")
        result["success"] = True
        result["path"] = str(path)
        result["filename"] = path.name
        result["warnings"].extend(sufficiency_result.get("warnings") or [])
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def summarize_folder_to_data_sufficiency_markdown(
    report_dir: str | Path,
    *,
    parameter_context: dict[str, Any] | None = None,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    sufficiency_result = summarize_report_folder_data_sufficiency(
        report_dir,
        parameter_context=parameter_context,
    )
    write_result = write_data_sufficiency_summary_markdown(
        sufficiency_result,
        report_dir,
        ticker=ticker,
        timeframe=timeframe,
        timestamp=timestamp,
    )

    errors = list(sufficiency_result.get("errors") or []) + list(write_result.get("errors") or [])
    warnings = list(sufficiency_result.get("warnings") or []) + list(write_result.get("warnings") or [])
    return {
        "success": bool(sufficiency_result.get("success")) and bool(write_result.get("success")),
        "sufficiency_result": sufficiency_result,
        "write_result": write_result,
        "path": write_result.get("path"),
        "filename": write_result.get("filename"),
        "errors": errors,
        "warnings": warnings,
    }
