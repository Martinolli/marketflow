"""Markdown artifact writer for Historical Walk-Forward Validation summaries."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any
from datetime import datetime
import json
import math

from marketflow.services.walk_forward_validation_service import (
    build_and_evaluate_walk_forward_cases_from_csv,
    summarize_walk_forward_validation,
)
from marketflow.services.walk_forward_run_registry_service import (
    build_walk_forward_run_metadata,
    build_walk_forward_run_registry_csv_filename,
    build_walk_forward_run_registry_json_filename,
    normalize_run_event_filter,
    upsert_walk_forward_run_registry,
    write_walk_forward_run_registry_csv,
)


WALK_FORWARD_VALIDATION_SUMMARY_KIND = "walk_forward_validation_summary_md"
WALK_FORWARD_CASES_CSV_KIND = "walk_forward_cases_csv"
WALK_FORWARD_RESULTS_CSV_KIND = "walk_forward_results_csv"
WALK_FORWARD_SUMMARY_CSV_KIND = "walk_forward_summary_csv"

CASE_COLUMNS = [
    "ticker",
    "timeframe",
    "profile_name",
    "signal_row_index",
    "signal_timestamp",
    "entry",
    "stop_loss",
    "take_profit",
    "risk_reward",
    "strategy_score",
    "wyckoff_phase",
    "wyckoff_event",
    "trend",
    "direction",
    "lookback_rows_available",
    "future_bars_available",
    "lookback_end_index",
    "future_window_start_index",
    "future_window_end_index",
    "snapshot_success",
    "wyckoff_event_source",
    "wyckoff_phase_source",
    "trend_source",
    "event_filters",
    "walk_forward_run_id",
    "walk_forward_case_id",
]

RESULT_COLUMNS = [
    "ticker",
    "timeframe",
    "profile_name",
    "signal_row_index",
    "signal_timestamp",
    "entry",
    "stop_loss",
    "take_profit",
    "outcome",
    "future_bars_available",
    "horizon_bars",
    "bars_to_hit",
    "realized_R",
    "same_bar_hit",
    "neither_reason",
    "backtest_success",
    "wyckoff_phase",
    "wyckoff_event",
    "trend",
    "wyckoff_event_source",
    "walk_forward_run_id",
    "walk_forward_case_id",
    "candidate_source",
    "run_id",
    "run_signature",
    "run_event_filter",
    "run_step",
    "run_max_cases",
    "run_require_mature_future",
    "source_csv_sha256",
]

SUMMARY_COLUMNS = [
    "sample_count",
    "scoreable_count",
    "tp_first_count",
    "sl_first_count",
    "neither_count",
    "invalid_count",
    "ambiguous_count",
    "not_mature_count",
    "mean_realized_R",
    "median_realized_R",
    "win_rate",
    "loss_rate",
    "neither_rate",
]

SUMMARY_CSV_COLUMNS = [
    "ticker",
    "timeframe",
    "profile_name",
    "source_csv",
    "row_count",
    "minimum_lookback_rows",
    "horizon_bars",
    "require_mature_future",
    "case_count",
    "evaluated_count",
    *SUMMARY_COLUMNS,
]


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
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


def _json_safe_value(value: Any) -> Any:
    if _is_missing(value):
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
    if _is_missing(value):
        return None
    if hasattr(value, "isoformat") and not isinstance(value, (str, bytes, bytearray)):
        try:
            return value.isoformat()
        except (AttributeError, TypeError, ValueError):
            pass
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _md_value(value: Any) -> str:
    if _is_missing(value):
        return ""
    if isinstance(value, bool):
        value = "yes" if value else "no"
    elif isinstance(value, Path):
        value = str(value)
    elif isinstance(value, float):
        value = f"{value:.4f}".rstrip("0").rstrip(".")
    elif isinstance(value, (list, tuple, set, dict)):
        try:
            value = json.dumps(_json_safe_value(value), sort_keys=True, separators=(",", ":"), default=str)
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


def build_walk_forward_validation_summary_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    profile_name: str | None = None,
    timestamp: str | None = None,
) -> str:
    stamp = _timestamp_for_filename(timestamp)
    ticker_part = _safe_filename_part(ticker)
    timeframe_part = _safe_filename_part(timeframe)
    profile_part = _safe_filename_part(profile_name)
    if ticker_part and timeframe_part and profile_part:
        return f"{ticker_part}_{timeframe_part}_{profile_part}_walk_forward_validation_summary_{stamp}.md"
    if ticker_part and timeframe_part:
        return f"{ticker_part}_{timeframe_part}_walk_forward_validation_summary_{stamp}.md"
    return f"marketflow_walk_forward_validation_summary_{stamp}.md"


def build_walk_forward_cases_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    profile_name: str | None = None,
    timestamp: str | None = None,
) -> str:
    stamp = _timestamp_for_filename(timestamp)
    ticker_part = _safe_filename_part(ticker)
    timeframe_part = _safe_filename_part(timeframe)
    profile_part = _safe_filename_part(profile_name)
    if ticker_part and timeframe_part and profile_part:
        return f"{ticker_part}_{timeframe_part}_{profile_part}_walk_forward_cases_{stamp}.csv"
    return f"marketflow_walk_forward_cases_{stamp}.csv"


def build_walk_forward_results_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    profile_name: str | None = None,
    timestamp: str | None = None,
) -> str:
    stamp = _timestamp_for_filename(timestamp)
    ticker_part = _safe_filename_part(ticker)
    timeframe_part = _safe_filename_part(timeframe)
    profile_part = _safe_filename_part(profile_name)
    if ticker_part and timeframe_part and profile_part:
        return f"{ticker_part}_{timeframe_part}_{profile_part}_walk_forward_results_{stamp}.csv"
    return f"marketflow_walk_forward_results_{stamp}.csv"


def build_walk_forward_summary_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    profile_name: str | None = None,
    timestamp: str | None = None,
) -> str:
    stamp = _timestamp_for_filename(timestamp)
    ticker_part = _safe_filename_part(ticker)
    timeframe_part = _safe_filename_part(timeframe)
    profile_part = _safe_filename_part(profile_name)
    if ticker_part and timeframe_part and profile_part:
        return f"{ticker_part}_{timeframe_part}_{profile_part}_walk_forward_summary_{stamp}.csv"
    return f"marketflow_walk_forward_summary_{stamp}.csv"


def _extract_cases(result: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(result, dict):
        return []
    build_result = result.get("build_result")
    if isinstance(build_result, dict):
        return [dict(row) for row in build_result.get("cases") or [] if isinstance(row, dict)]
    return [dict(row) for row in result.get("cases") or [] if isinstance(row, dict)]


def _extract_result_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(result, dict):
        return []
    evaluation_result = result.get("evaluation_result")
    if isinstance(evaluation_result, dict):
        return [dict(row) for row in evaluation_result.get("result_rows") or [] if isinstance(row, dict)]
    return [dict(row) for row in result.get("result_rows") or [] if isinstance(row, dict)]


def _extract_summary(result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict):
        return summarize_walk_forward_validation([])
    summary = result.get("summary")
    if isinstance(summary, dict) and summary:
        return dict(summary)
    result_rows = _extract_result_rows(result)
    if result_rows:
        return summarize_walk_forward_validation(result_rows)
    if any(key in result for key in SUMMARY_COLUMNS):
        return {key: result.get(key) for key in SUMMARY_COLUMNS if key in result}
    return summarize_walk_forward_validation([])


def _build_result(result: dict[str, Any]) -> dict[str, Any]:
    build_result = result.get("build_result") if isinstance(result, dict) else {}
    return build_result if isinstance(build_result, dict) else result


def _evaluation_result(result: dict[str, Any]) -> dict[str, Any]:
    evaluation_result = result.get("evaluation_result") if isinstance(result, dict) else {}
    return evaluation_result if isinstance(evaluation_result, dict) else result


def _case_lookup(result: dict[str, Any]) -> dict[tuple[Any, Any], dict[str, Any]]:
    lookup: dict[tuple[Any, Any], dict[str, Any]] = {}
    for case in _extract_cases(result):
        case_id = case.get("walk_forward_case_id")
        if not _is_missing(case_id):
            lookup[("case_id", str(case_id))] = case
        row_index = case.get("signal_row_index")
        timestamp = case.get("signal_timestamp")
        if not _is_missing(row_index):
            lookup[("row_index", str(row_index))] = case
        if not _is_missing(timestamp):
            lookup[("timestamp", str(timestamp))] = case
    return lookup


def _matching_case(row: dict[str, Any], lookup: dict[tuple[Any, Any], dict[str, Any]]) -> dict[str, Any]:
    case_id = row.get("walk_forward_case_id")
    if not _is_missing(case_id) and ("case_id", str(case_id)) in lookup:
        return lookup[("case_id", str(case_id))]
    row_index = row.get("signal_row_index")
    if not _is_missing(row_index) and ("row_index", str(row_index)) in lookup:
        return lookup[("row_index", str(row_index))]
    timestamp = row.get("signal_timestamp")
    if not _is_missing(timestamp) and ("timestamp", str(timestamp)) in lookup:
        return lookup[("timestamp", str(timestamp))]
    return {}


def _result_messages(result: dict[str, Any], key: str) -> list[Any]:
    messages: list[Any] = []
    if not isinstance(result, dict):
        return messages
    messages.extend(result.get(key) or [])
    build_result = result.get("build_result")
    if isinstance(build_result, dict):
        messages.extend(build_result.get(key) or [])
    evaluation_result = result.get("evaluation_result")
    if isinstance(evaluation_result, dict):
        messages.extend(evaluation_result.get(key) or [])
    return messages


def _bullet_list(items: list[Any]) -> str:
    clean_items = [item for item in items if not _is_missing(item)]
    if not clean_items:
        return "_None._"
    return "\n".join(f"- {_md_value(item)}" for item in clean_items)


def _csv_safe_value(value: Any) -> Any:
    if _is_missing(value):
        return ""
    if isinstance(value, bool):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (dict, list, tuple, set)):
        try:
            return json.dumps(_json_safe_value(value), sort_keys=True, separators=(",", ":"), default=str)
        except (TypeError, ValueError):
            return str(value)
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            value = value.item()
        except (AttributeError, TypeError, ValueError):
            pass
    if _is_missing(value):
        return ""
    if hasattr(value, "isoformat") and not isinstance(value, (str, bytes, bytearray)):
        try:
            return value.isoformat()
        except (AttributeError, TypeError, ValueError):
            pass
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _csv_safe_rows(rows: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [
        {column: _csv_safe_value(row.get(column)) for column in columns}
        for row in rows
        if isinstance(row, dict)
    ]


def _write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(_csv_safe_rows(rows, columns))


def _outcome_review_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    scoreable = summary.get("scoreable_count")
    return [
        {"metric": "TP_FIRST", "count": summary.get("tp_first_count"), "rate": summary.get("win_rate")},
        {"metric": "SL_FIRST", "count": summary.get("sl_first_count"), "rate": summary.get("loss_rate")},
        {"metric": "NEITHER", "count": summary.get("neither_count"), "rate": summary.get("neither_rate")},
        {"metric": "INVALID", "count": summary.get("invalid_count"), "rate": None},
        {"metric": "AMBIGUOUS", "count": summary.get("ambiguous_count"), "rate": None},
        {"metric": "not mature", "count": summary.get("not_mature_count"), "rate": None},
        {"metric": "scoreable", "count": scoreable, "rate": None},
    ]


def build_walk_forward_validation_summary_markdown(
    walk_forward_result: dict[str, Any],
    *,
    title: str = "MarketFlow Historical Walk-Forward Validation Summary",
    created_at: str | None = None,
    max_case_rows: int = 50,
    max_result_rows: int = 100,
) -> str:
    result = dict(walk_forward_result) if isinstance(walk_forward_result, dict) else {}
    build_result = _build_result(result)
    evaluation_result = _evaluation_result(result)
    summary = _extract_summary(result)
    cases = _extract_cases(result)
    result_rows = _extract_result_rows(result)
    created = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warnings = _result_messages(result, "warnings")
    errors = _result_messages(result, "errors")

    sections = [
        f"# {title}",
        "## Metadata",
        f"- Created: {_md_value(created)}",
        f"- CSV path: {_md_value(build_result.get('csv_path') or result.get('csv_path'))}",
        f"- Source CSV: {_md_value(build_result.get('source_csv_name') or result.get('source_csv_name'))}",
        f"- Ticker: {_md_value(build_result.get('ticker') or result.get('ticker'))}",
        f"- Timeframe: {_md_value(build_result.get('timeframe') or result.get('timeframe'))}",
        f"- Profile: {_md_value(build_result.get('profile_name') or evaluation_result.get('profile_name') or result.get('profile_name'))}",
        f"- Walk-forward run id: {_md_value(build_result.get('walk_forward_run_id') or result.get('walk_forward_run_id'))}",
        f"- Row count: {_md_value(build_result.get('row_count') or result.get('row_count'))}",
        f"- Minimum lookback rows: {_md_value(build_result.get('minimum_lookback_rows') or result.get('minimum_lookback_rows'))}",
        f"- Horizon bars: {_md_value(build_result.get('horizon_bars') or evaluation_result.get('horizon_bars') or result.get('horizon_bars'))}",
        f"- Require mature future: {_md_value(build_result.get('require_mature_future') if 'require_mature_future' in build_result else result.get('require_mature_future'))}",
        f"- Case count: {_md_value(build_result.get('case_count') if 'case_count' in build_result else len(cases))}",
        f"- Evaluated count: {_md_value(evaluation_result.get('evaluated_count') if 'evaluated_count' in evaluation_result else len(result_rows))}",
        f"- Scoreable count: {_md_value(summary.get('scoreable_count'))}",
        "## Summary",
        _markdown_table([summary], SUMMARY_COLUMNS),
        "## Walk-Forward Cases",
        _markdown_table(cases, CASE_COLUMNS, max_rows=max_case_rows),
        "## Deterministic Outcome Rows",
        _markdown_table(result_rows, RESULT_COLUMNS, max_rows=max_result_rows),
        "## Outcome Review",
        _markdown_table(_outcome_review_rows(summary), ["metric", "count", "rate"]),
        "## No-Leakage Review",
        "- Each case records `lookback_end_index` equal to `signal_row_index`.",
        "- `future_window_start_index` starts after `signal_row_index`.",
        "- Future rows are for outcome evaluation only.",
        "- This service does not add Monte Carlo integration yet.",
        "## Warnings",
        _bullet_list(warnings),
        "## Errors",
        _bullet_list(errors),
        "## Guardrails",
        "- Walk-forward validation only.",
        "- This is not financial advice.",
        "- This does not create buy/sell signals.",
        "- This does not optimize parameters automatically.",
        "- Historical validation does not guarantee future performance.",
        "- No future data leakage.",
        "- Low-timeframe noise must remain visible.",
        "- Small samples should not be overinterpreted.",
        "- Candidate quality remains separate from workflow validity.",
        "",
    ]
    return "\n\n".join(sections)


def _collision_safe_path(output_dir: Path, filename: str | None = None) -> Path:
    target = output_dir / filename if filename is not None else output_dir
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


def write_walk_forward_cases_csv(
    walk_forward_result: dict[str, Any],
    output_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    profile_name: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    result = {
        "success": False,
        "path": None,
        "filename": None,
        "kind": WALK_FORWARD_CASES_CSV_KIND,
        "row_count": 0,
        "errors": [],
        "warnings": [],
    }
    try:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        build_result = _build_result(walk_forward_result if isinstance(walk_forward_result, dict) else {})
        cases = _extract_cases(walk_forward_result)
        event_filters = build_result.get("event_filters")
        rows = []
        for case in cases:
            row = dict(case)
            row.setdefault("event_filters", event_filters)
            row.setdefault("walk_forward_run_id", build_result.get("walk_forward_run_id"))
            rows.append(row)
        if not rows:
            result["warnings"].append("No walk-forward cases were available.")
        filename = build_walk_forward_cases_filename(
            ticker=ticker or build_result.get("ticker"),
            timeframe=timeframe or build_result.get("timeframe"),
            profile_name=profile_name or build_result.get("profile_name"),
            timestamp=timestamp,
        )
        path = _collision_safe_path(directory, filename)
        _write_csv(path, rows, CASE_COLUMNS)
        result["success"] = True
        result["path"] = str(path)
        result["filename"] = path.name
        result["row_count"] = len(rows)
        result["warnings"].extend(_result_messages(walk_forward_result, "warnings"))
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def write_walk_forward_results_csv(
    walk_forward_result: dict[str, Any],
    output_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    profile_name: str | None = None,
    timestamp: str | None = None,
    run_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "success": False,
        "path": None,
        "filename": None,
        "kind": WALK_FORWARD_RESULTS_CSV_KIND,
        "row_count": 0,
        "errors": [],
        "warnings": [],
    }
    try:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        build_result = _build_result(walk_forward_result if isinstance(walk_forward_result, dict) else {})
        evaluation_result = _evaluation_result(walk_forward_result if isinstance(walk_forward_result, dict) else {})
        case_lookup = _case_lookup(walk_forward_result if isinstance(walk_forward_result, dict) else {})
        rows = []
        metadata = run_metadata if isinstance(run_metadata, dict) else {}
        for result_row in _extract_result_rows(walk_forward_result):
            row = dict(result_row)
            case = _matching_case(row, case_lookup)
            for key in (
                "wyckoff_event_source",
                "walk_forward_run_id",
                "walk_forward_case_id",
                "candidate_source",
            ):
                if _is_missing(row.get(key)):
                    row[key] = case.get(key)
            row.setdefault("profile_name", build_result.get("profile_name") or evaluation_result.get("profile_name"))
            row["run_id"] = metadata.get("run_id")
            row["run_signature"] = metadata.get("run_signature")
            row["run_event_filter"] = metadata.get("run_event_filter")
            row["run_step"] = metadata.get("step")
            row["run_max_cases"] = metadata.get("max_cases")
            row["run_require_mature_future"] = metadata.get("require_mature_future")
            row["source_csv_sha256"] = metadata.get("source_csv_sha256")
            rows.append(row)
        if not rows:
            result["warnings"].append("No walk-forward result rows were available.")
        filename = build_walk_forward_results_filename(
            ticker=ticker or build_result.get("ticker"),
            timeframe=timeframe or build_result.get("timeframe"),
            profile_name=profile_name or build_result.get("profile_name") or evaluation_result.get("profile_name"),
            timestamp=timestamp,
        )
        path = _collision_safe_path(directory, filename)
        _write_csv(path, rows, RESULT_COLUMNS)
        result["success"] = True
        result["path"] = str(path)
        result["filename"] = path.name
        result["row_count"] = len(rows)
        result["warnings"].extend(_result_messages(walk_forward_result, "warnings"))
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def write_walk_forward_summary_csv(
    walk_forward_result: dict[str, Any],
    output_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    profile_name: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    result = {
        "success": False,
        "path": None,
        "filename": None,
        "kind": WALK_FORWARD_SUMMARY_CSV_KIND,
        "row_count": 0,
        "errors": [],
        "warnings": [],
    }
    try:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        source = walk_forward_result if isinstance(walk_forward_result, dict) else {}
        build_result = _build_result(source)
        evaluation_result = _evaluation_result(source)
        summary = _extract_summary(source)
        row = {
            "ticker": ticker or build_result.get("ticker") or source.get("ticker"),
            "timeframe": timeframe or build_result.get("timeframe") or source.get("timeframe"),
            "profile_name": profile_name or build_result.get("profile_name") or evaluation_result.get("profile_name"),
            "source_csv": build_result.get("csv_path") or build_result.get("source_csv_name") or source.get("csv_path"),
            "row_count": build_result.get("row_count"),
            "minimum_lookback_rows": build_result.get("minimum_lookback_rows"),
            "horizon_bars": build_result.get("horizon_bars") or evaluation_result.get("horizon_bars"),
            "require_mature_future": build_result.get("require_mature_future"),
            "case_count": build_result.get("case_count"),
            "evaluated_count": evaluation_result.get("evaluated_count"),
            **summary,
        }
        filename = build_walk_forward_summary_filename(
            ticker=row.get("ticker"),
            timeframe=row.get("timeframe"),
            profile_name=row.get("profile_name"),
            timestamp=timestamp,
        )
        path = _collision_safe_path(directory, filename)
        _write_csv(path, [row], SUMMARY_CSV_COLUMNS)
        result["success"] = True
        result["path"] = str(path)
        result["filename"] = path.name
        result["row_count"] = 1
        result["warnings"].extend(_result_messages(source, "warnings"))
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def write_walk_forward_validation_csv_artifacts(
    walk_forward_result: dict[str, Any],
    output_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    profile_name: str | None = None,
    timestamp: str | None = None,
    include_cases: bool = True,
    include_results: bool = True,
    include_summary: bool = True,
    run_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cases_result = (
        write_walk_forward_cases_csv(
            walk_forward_result,
            output_dir,
            ticker=ticker,
            timeframe=timeframe,
            profile_name=profile_name,
            timestamp=timestamp,
        )
        if include_cases
        else None
    )
    results_result = (
        write_walk_forward_results_csv(
            walk_forward_result,
            output_dir,
            ticker=ticker,
            timeframe=timeframe,
            profile_name=profile_name,
            timestamp=timestamp,
            run_metadata=run_metadata,
        )
        if include_results
        else None
    )
    summary_result = (
        write_walk_forward_summary_csv(
            walk_forward_result,
            output_dir,
            ticker=ticker,
            timeframe=timeframe,
            profile_name=profile_name,
            timestamp=timestamp,
        )
        if include_summary
        else None
    )
    selected_results = [item for item in (cases_result, results_result, summary_result) if isinstance(item, dict)]
    artifacts = [item for item in selected_results if item.get("path")]
    errors = [error for item in selected_results for error in item.get("errors") or []]
    warnings = [warning for item in selected_results for warning in item.get("warnings") or []]
    if not selected_results:
        warnings.append("No walk-forward CSV artifacts were selected.")
    return {
        "success": bool(selected_results) and all(bool(item.get("success")) for item in selected_results),
        "artifacts": artifacts,
        "cases_result": cases_result,
        "results_result": results_result,
        "summary_result": summary_result,
        "errors": errors,
        "warnings": warnings,
    }


def _run_event_filter_value(event_filters: list[str] | None) -> str:
    return normalize_run_event_filter(",".join(str(item) for item in event_filters or []))


def _write_walk_forward_run_registry_artifacts(
    *,
    walk_forward_result: dict[str, Any],
    source_csv_path: str | Path,
    output_dir: Path,
    ticker: str | None,
    event_filters: list[str] | None,
    step: int | None,
    max_cases: int | None,
    require_mature_future: bool | None,
    artifacts: list[dict[str, Any]],
    created_at: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    metadata = build_walk_forward_run_metadata(
        validation_result=walk_forward_result,
        source_csv_path=source_csv_path,
        run_event_filter=_run_event_filter_value(event_filters),
        step=step,
        max_cases=max_cases,
        require_mature_future=require_mature_future,
        artifacts=artifacts,
        created_at=created_at,
    )
    json_path = output_dir / build_walk_forward_run_registry_json_filename(ticker=ticker)
    csv_path = output_dir / build_walk_forward_run_registry_csv_filename(ticker=ticker)
    registry_result = upsert_walk_forward_run_registry(
        registry_path=json_path,
        run_metadata=metadata,
    )
    registry_csv_result = write_walk_forward_run_registry_csv(
        registry_json_path=json_path,
        registry_csv_path=csv_path,
    )
    return metadata, registry_result, registry_csv_result


def write_walk_forward_validation_summary_markdown(
    walk_forward_result: dict[str, Any],
    output_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    profile_name: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    result = {
        "success": False,
        "path": None,
        "filename": None,
        "kind": WALK_FORWARD_VALIDATION_SUMMARY_KIND,
        "errors": [],
        "warnings": [],
    }

    try:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        build_result = _build_result(walk_forward_result if isinstance(walk_forward_result, dict) else {})
        filename = build_walk_forward_validation_summary_filename(
            ticker=ticker or build_result.get("ticker"),
            timeframe=timeframe or build_result.get("timeframe"),
            profile_name=profile_name or build_result.get("profile_name"),
            timestamp=timestamp,
        )
        path = _collision_safe_path(directory, filename)
        markdown = build_walk_forward_validation_summary_markdown(walk_forward_result)
        path.write_text(markdown, encoding="utf-8")
        result["success"] = True
        result["path"] = str(path)
        result["filename"] = path.name
        result["warnings"].extend(_result_messages(walk_forward_result, "warnings"))
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def summarize_csv_to_walk_forward_validation_markdown(
    csv_path: str | Path,
    output_dir: str | Path | None = None,
    *,
    profile_name: str,
    timeframe: str | None = None,
    ticker: str | None = None,
    min_signal_row: int | None = None,
    max_signal_row: int | None = None,
    step: int = 1,
    event_filters: list[str] | None = None,
    max_cases: int | None = None,
    require_mature_future: bool = True,
    timestamp: str | None = None,
) -> dict[str, Any]:
    walk_forward_result = build_and_evaluate_walk_forward_cases_from_csv(
        csv_path,
        profile_name=profile_name,
        timeframe=timeframe,
        ticker=ticker,
        min_signal_row=min_signal_row,
        max_signal_row=max_signal_row,
        step=step,
        event_filters=event_filters,
        max_cases=max_cases,
        require_mature_future=require_mature_future,
    )
    directory = Path(output_dir) if output_dir is not None else Path(csv_path).parent
    build_result = walk_forward_result.get("build_result") if isinstance(walk_forward_result, dict) else {}
    write_result = write_walk_forward_validation_summary_markdown(
        walk_forward_result,
        directory,
        ticker=ticker or (build_result.get("ticker") if isinstance(build_result, dict) else None),
        timeframe=timeframe or (build_result.get("timeframe") if isinstance(build_result, dict) else None),
        profile_name=profile_name,
        timestamp=timestamp,
    )
    created_at = datetime.now().isoformat(timespec="seconds")
    registry_metadata = None
    registry_result = None
    registry_csv_result = None
    if write_result.get("path"):
        registry_metadata, registry_result, registry_csv_result = _write_walk_forward_run_registry_artifacts(
            walk_forward_result=walk_forward_result,
            source_csv_path=csv_path,
            output_dir=directory,
            ticker=ticker or (build_result.get("ticker") if isinstance(build_result, dict) else None),
            event_filters=event_filters,
            step=step,
            max_cases=max_cases,
            require_mature_future=require_mature_future,
            artifacts=[write_result],
            created_at=created_at,
        )
    errors = list(walk_forward_result.get("errors") or []) + list(write_result.get("errors") or [])
    warnings = list(walk_forward_result.get("warnings") or []) + list(write_result.get("warnings") or [])
    for registry_artifact in (registry_result, registry_csv_result):
        if isinstance(registry_artifact, dict):
            errors.extend(registry_artifact.get("errors") or [])
            warnings.extend(registry_artifact.get("warnings") or [])
    registry_success = all(
        bool(item.get("success"))
        for item in (registry_result, registry_csv_result)
        if isinstance(item, dict)
    )
    return {
        "success": (
            bool(walk_forward_result.get("success"))
            and bool(write_result.get("success"))
            and registry_success
        ),
        "walk_forward_result": walk_forward_result,
        "write_result": write_result,
        "run_metadata": registry_metadata,
        "registry_result": registry_result,
        "registry_csv_result": registry_csv_result,
        "artifacts": [
            item
            for item in (write_result, registry_result, registry_csv_result)
            if isinstance(item, dict) and item.get("path")
        ],
        "path": write_result.get("path"),
        "filename": write_result.get("filename"),
        "errors": errors,
        "warnings": warnings,
    }


def summarize_csv_to_walk_forward_validation_artifacts(
    csv_path: str | Path,
    output_dir: str | Path | None = None,
    *,
    profile_name: str,
    timeframe: str | None = None,
    ticker: str | None = None,
    min_signal_row: int | None = None,
    max_signal_row: int | None = None,
    step: int = 1,
    event_filters: list[str] | None = None,
    max_cases: int | None = None,
    require_mature_future: bool = True,
    timestamp: str | None = None,
    save_markdown: bool = True,
    save_cases_csv: bool = True,
    save_results_csv: bool = True,
    save_summary_csv: bool = True,
) -> dict[str, Any]:
    walk_forward_result = build_and_evaluate_walk_forward_cases_from_csv(
        csv_path,
        profile_name=profile_name,
        timeframe=timeframe,
        ticker=ticker,
        min_signal_row=min_signal_row,
        max_signal_row=max_signal_row,
        step=step,
        event_filters=event_filters,
        max_cases=max_cases,
        require_mature_future=require_mature_future,
    )
    directory = Path(output_dir) if output_dir is not None else Path(csv_path).parent
    build_result = walk_forward_result.get("build_result") if isinstance(walk_forward_result, dict) else {}
    artifact_ticker = ticker or (build_result.get("ticker") if isinstance(build_result, dict) else None)
    artifact_timeframe = timeframe or (build_result.get("timeframe") if isinstance(build_result, dict) else None)
    artifact_profile = profile_name or (build_result.get("profile_name") if isinstance(build_result, dict) else None)
    created_at = datetime.now().isoformat(timespec="seconds")
    preliminary_run_metadata = build_walk_forward_run_metadata(
        validation_result=walk_forward_result,
        source_csv_path=csv_path,
        run_event_filter=_run_event_filter_value(event_filters),
        step=step,
        max_cases=max_cases,
        require_mature_future=require_mature_future,
        artifacts=None,
        created_at=created_at,
    )

    markdown_result = (
        write_walk_forward_validation_summary_markdown(
            walk_forward_result,
            directory,
            ticker=artifact_ticker,
            timeframe=artifact_timeframe,
            profile_name=artifact_profile,
            timestamp=timestamp,
        )
        if save_markdown
        else None
    )
    csv_result = write_walk_forward_validation_csv_artifacts(
        walk_forward_result,
        directory,
        ticker=artifact_ticker,
        timeframe=artifact_timeframe,
        profile_name=artifact_profile,
        timestamp=timestamp,
        include_cases=save_cases_csv,
        include_results=save_results_csv,
        include_summary=save_summary_csv,
        run_metadata=preliminary_run_metadata,
    )
    if not (save_cases_csv or save_results_csv or save_summary_csv):
        csv_result = None

    artifact_results = [
        item
        for item in [
            markdown_result,
            *((csv_result or {}).get("artifacts") or []),
        ]
        if isinstance(item, dict) and item.get("path")
    ]
    registry_metadata = None
    registry_result = None
    registry_csv_result = None
    if artifact_results:
        registry_metadata, registry_result, registry_csv_result = _write_walk_forward_run_registry_artifacts(
            walk_forward_result=walk_forward_result,
            source_csv_path=csv_path,
            output_dir=directory,
            ticker=artifact_ticker,
            event_filters=event_filters,
            step=step,
            max_cases=max_cases,
            require_mature_future=require_mature_future,
            artifacts=artifact_results,
            created_at=created_at,
        )
        artifact_results.extend(
            item
            for item in (registry_result, registry_csv_result)
            if isinstance(item, dict) and item.get("path")
        )
    errors = list(walk_forward_result.get("errors") or [])
    warnings = list(walk_forward_result.get("warnings") or [])
    if isinstance(markdown_result, dict):
        errors.extend(markdown_result.get("errors") or [])
        warnings.extend(markdown_result.get("warnings") or [])
    if isinstance(csv_result, dict):
        errors.extend(csv_result.get("errors") or [])
        warnings.extend(csv_result.get("warnings") or [])
    for registry_artifact in (registry_result, registry_csv_result):
        if isinstance(registry_artifact, dict):
            errors.extend(registry_artifact.get("errors") or [])
            warnings.extend(registry_artifact.get("warnings") or [])

    selected_write_results = [
        item
        for item in [
            markdown_result,
            csv_result,
            registry_result,
            registry_csv_result,
        ]
        if isinstance(item, dict)
    ]
    writes_success = all(bool(item.get("success")) for item in selected_write_results) if selected_write_results else True
    return {
        "success": bool(walk_forward_result.get("success")) and writes_success,
        "walk_forward_result": walk_forward_result,
        "markdown_result": markdown_result,
        "csv_result": csv_result,
        "run_metadata": registry_metadata or preliminary_run_metadata,
        "registry_result": registry_result,
        "registry_csv_result": registry_csv_result,
        "artifacts": artifact_results,
        "errors": errors,
        "warnings": warnings,
    }
