"""Markdown artifact writer for Backtest Calibration Summary results."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from marketflow.services.backtest_calibration_service import summarize_backtest_results_folder


BACKTEST_CALIBRATION_SUMMARY_KIND = "backtest_calibration_summary_md"


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
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
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value).strip())
    safe = safe.strip("._-")
    return safe or None


def _timestamp_for_filename(timestamp: str | None = None) -> str:
    safe_timestamp = _safe_filename_part(timestamp)
    if safe_timestamp:
        return safe_timestamp
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def build_backtest_calibration_summary_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> str:
    stamp = _timestamp_for_filename(timestamp)
    ticker_part = _safe_filename_part(ticker)
    timeframe_part = _safe_filename_part(timeframe)
    if ticker_part and timeframe_part:
        return f"{ticker_part}_{timeframe_part}_backtest_calibration_summary_{stamp}.md"
    return f"marketflow_backtest_calibration_summary_{stamp}.md"


def _bullet_list(items: list[Any]) -> str:
    clean_items = [item for item in items if not _is_missing(item)]
    if not clean_items:
        return "_None._"
    return "\n".join(f"- {_md_value(item)}" for item in clean_items)


def _metadata_value(calibration_result: dict[str, Any], key: str) -> Any:
    value = calibration_result.get(key)
    if value is not None:
        return value
    read_result = calibration_result.get("read_result")
    if isinstance(read_result, dict):
        return read_result.get(key)
    return None


def build_backtest_calibration_summary_markdown(
    calibration_result: dict[str, Any],
    *,
    title: str = "MarketFlow Backtest Calibration Summary",
    created_at: str | None = None,
) -> str:
    source_files = list(calibration_result.get("source_result_files") or [])
    source_path = calibration_result.get("path")
    if source_path and not source_files:
        source_files = [source_path]

    summary_rows = calibration_result.get("summary_rows") or []
    if not summary_rows and isinstance(calibration_result.get("summary"), dict) and calibration_result.get("summary"):
        summary_rows = [calibration_result["summary"]]

    created = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warnings = list(calibration_result.get("warnings") or [])
    errors = list(calibration_result.get("errors") or [])

    sections = [
        f"# {title}",
        "## Metadata",
        f"- Created: {_md_value(created)}",
        f"- Report directory: {_md_value(calibration_result.get('report_dir'))}",
        "- Source result files:",
        _bullet_list(source_files),
        f"- File count: {_md_value(calibration_result.get('file_count'))}",
        f"- Row count: {_md_value(_metadata_value(calibration_result, 'count'))}",
        "## Global Summary",
        _markdown_table(list(summary_rows)),
        "## Grouped Summary",
        _markdown_table(list(calibration_result.get("grouped_summary_rows") or []), max_rows=100),
        "## Invalid Row Review",
        _markdown_table(list(calibration_result.get("invalid_reason_rows") or [])),
        "## Warnings",
        _bullet_list(warnings),
        "## Errors",
        _bullet_list(errors),
        "## Guardrails",
        "- Calibration only.",
        "- This is not financial advice.",
        "- This does not optimize parameters automatically.",
        "- This does not create buy/sell signals.",
        "- Small samples should not be overinterpreted.",
        "- Compare horizons within the same timeframe first.",
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


def write_backtest_calibration_summary_markdown(
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
        "kind": BACKTEST_CALIBRATION_SUMMARY_KIND,
        "errors": [],
        "warnings": [],
    }

    try:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        filename = build_backtest_calibration_summary_filename(
            ticker=ticker,
            timeframe=timeframe,
            timestamp=timestamp,
        )
        path = _collision_safe_path(directory, filename)
        markdown = build_backtest_calibration_summary_markdown(calibration_result)
        path.write_text(markdown, encoding="utf-8")
        result["success"] = True
        result["path"] = str(path)
        result["filename"] = path.name
        result["warnings"].extend(calibration_result.get("warnings") or [])
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def summarize_folder_to_backtest_calibration_markdown(
    report_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    calibration_result = summarize_backtest_results_folder(report_dir)
    output_dir = Path(report_dir)
    write_result = (
        write_backtest_calibration_summary_markdown(
            calibration_result,
            output_dir,
            ticker=ticker,
            timeframe=timeframe,
            timestamp=timestamp,
        )
        if calibration_result.get("success")
        else {
            "success": False,
            "path": None,
            "filename": None,
            "kind": BACKTEST_CALIBRATION_SUMMARY_KIND,
            "errors": [],
            "warnings": [],
        }
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
