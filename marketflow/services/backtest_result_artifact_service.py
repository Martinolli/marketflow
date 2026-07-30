"""CSV artifact writer for deterministic backtest outcome results."""

from __future__ import annotations

import csv
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


BACKTEST_RESULT_COLUMNS = [
    "created_at",
    "ticker",
    "timeframe",
    "source_csv",
    "source_report_dir",
    "candidate_snapshot_file",
    "signal_timestamp",
    "signal_timestamp_source",
    "signal_row_index",
    "entry",
    "stop_loss",
    "take_profit",
    "risk_reward",
    "strategy_score",
    "wyckoff_phase",
    "wyckoff_event",
    "event_status",
    "event_provenance",
    "event_age_bars",
    "event_max_age_bars",
    "event_scoring_eligible",
    "event_occurrence_row_index",
    "event_occurrence_timestamp",
    "event_decision_row_index",
    "event_superseded_count",
    "event_reason",
    "event_resolution_source",
    "trend",
    "candidate_source",
    "report_date",
    "direction",
    "source_strategy_rank",
    "candidate_validation_status",
    "candidate_snapshot_success",
    "outcome",
    "bars_to_hit",
    "realized_R",
    "same_bar_hit",
    "tie_break_policy",
    "horizon_bars",
    "future_bars_available",
    "evaluation_window_start_index",
    "evaluation_window_end_index",
    "signal_is_latest_row",
    "neither_reason",
    "hit_timestamp",
    "hit_row_index",
    "planned_rr",
    "mark_to_market_close",
    "outcome_error",
    "backtest_success",
]

VALID_OUTCOMES = {"TP_FIRST", "SL_FIRST", "NEITHER", "AMBIGUOUS", "INVALID"}


def _safe_filename_part(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", text)
    safe = safe.strip("._-")
    return safe or None


def _timestamp_for_filename(timestamp: str | None = None) -> str:
    if timestamp:
        safe = _safe_filename_part(timestamp)
        if safe:
            return safe
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def build_backtest_results_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> str:
    stamp = _timestamp_for_filename(timestamp)
    ticker_part = _safe_filename_part(ticker)
    timeframe_part = _safe_filename_part(timeframe)
    if ticker_part and timeframe_part:
        return f"{ticker_part}_{timeframe_part}_backtest_results_{stamp}.csv"
    return f"marketflow_backtest_results_{stamp}.csv"


def _collision_safe_path(output_dir: Path, filename: str) -> Path:
    target = output_dir / filename
    if not target.exists():
        return target

    stem = target.stem
    suffix = target.suffix or ".csv"
    counter = 2
    while True:
        candidate = output_dir / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def _csv_safe_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return "; ".join(str(_csv_safe_value(item)) for item in value if _csv_safe_value(item) != "")
    if isinstance(value, dict):
        try:
            return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
        except (TypeError, ValueError):
            return str(value)
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            value = value.item()
        except (AttributeError, TypeError, ValueError):
            pass
    try:
        is_missing = pd.isna(value)
    except (TypeError, ValueError):
        is_missing = False
    try:
        if bool(is_missing):
            return ""
    except (TypeError, ValueError):
        pass
    if isinstance(value, float) and math.isnan(value):
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _label_from_value(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return _label_from_value(value.get("outcome") or value.get("status") or value.get("result"))
    if hasattr(value, "name"):
        name = _label_from_value(getattr(value, "name"))
        if name in VALID_OUTCOMES:
            return name
    if hasattr(value, "value") and not isinstance(value, (str, bytes, bytearray)):
        enum_value = _label_from_value(getattr(value, "value"))
        if enum_value:
            return enum_value
    text = str(value).strip()
    if not text:
        return None
    return text.upper()


def _outcome_label(outcome_result: dict[str, Any]) -> str:
    if not isinstance(outcome_result, dict):
        return "INVALID"
    for key in ("outcome", "status", "result"):
        label = _label_from_value(outcome_result.get(key))
        if label in VALID_OUTCOMES:
            return label
    return "INVALID"


def _flatten_outcome_result(outcome_result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(outcome_result, dict):
        return {}
    flattened = dict(outcome_result)
    nested_outcome = outcome_result.get("outcome")
    if isinstance(nested_outcome, dict):
        flattened.update(nested_outcome)
    settings = outcome_result.get("settings")
    if isinstance(settings, dict):
        for key in ("tie_break_policy", "horizon_bars"):
            flattened.setdefault(key, settings.get(key))
    return flattened


def _outcome_error(outcome_data: dict[str, Any], raw_outcome_result: Any) -> Any:
    error = outcome_data.get("outcome_error")
    if error in (None, ""):
        error = outcome_data.get("error")
    if error in (None, "") and not isinstance(raw_outcome_result, dict):
        error = "Malformed outcome result."
    return error


def backtest_result_row(
    *,
    snapshot_row: dict[str, Any],
    outcome_result: dict[str, Any],
    candidate_snapshot_file: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    snapshot = dict(snapshot_row) if isinstance(snapshot_row, dict) else {}
    outcome_data = _flatten_outcome_result(outcome_result)
    outcome = _outcome_label(outcome_data)
    realized_r = outcome_data.get("realized_R")
    if realized_r in (None, ""):
        realized_r = outcome_data.get("realized_r")

    row = {
        "created_at": created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ticker": snapshot.get("ticker"),
        "timeframe": snapshot.get("timeframe"),
        "source_csv": snapshot.get("source_csv"),
        "source_report_dir": snapshot.get("source_report_dir"),
        "candidate_snapshot_file": candidate_snapshot_file,
        "signal_timestamp": snapshot.get("signal_timestamp"),
        "signal_timestamp_source": snapshot.get("signal_timestamp_source"),
        "signal_row_index": snapshot.get("signal_row_index"),
        "entry": snapshot.get("entry"),
        "stop_loss": snapshot.get("stop_loss"),
        "take_profit": snapshot.get("take_profit"),
        "risk_reward": snapshot.get("risk_reward"),
        "strategy_score": snapshot.get("strategy_score"),
        "wyckoff_phase": snapshot.get("wyckoff_phase"),
        "wyckoff_event": snapshot.get("wyckoff_event"),
        "event_status": snapshot.get("event_status"),
        "event_provenance": snapshot.get("event_provenance"),
        "event_age_bars": snapshot.get("event_age_bars"),
        "event_max_age_bars": snapshot.get("event_max_age_bars"),
        "event_scoring_eligible": snapshot.get("event_scoring_eligible"),
        "event_occurrence_row_index": snapshot.get("event_occurrence_row_index"),
        "event_occurrence_timestamp": snapshot.get("event_occurrence_timestamp"),
        "event_decision_row_index": snapshot.get("event_decision_row_index"),
        "event_superseded_count": snapshot.get("event_superseded_count"),
        "event_reason": snapshot.get("event_reason"),
        "event_resolution_source": snapshot.get("event_resolution_source"),
        "trend": snapshot.get("trend"),
        "candidate_source": snapshot.get("candidate_source"),
        "report_date": snapshot.get("report_date"),
        "direction": snapshot.get("direction"),
        "source_strategy_rank": snapshot.get("source_strategy_rank"),
        "candidate_validation_status": snapshot.get("validation_status"),
        "candidate_snapshot_success": snapshot.get("snapshot_success"),
        "outcome": outcome,
        "bars_to_hit": outcome_data.get("bars_to_hit"),
        "realized_R": realized_r,
        "same_bar_hit": outcome_data.get("same_bar_hit"),
        "tie_break_policy": outcome_data.get("tie_break_policy"),
        "horizon_bars": outcome_data.get("horizon_bars"),
        "future_bars_available": outcome_data.get("future_bars_available"),
        "evaluation_window_start_index": outcome_data.get("evaluation_window_start_index"),
        "evaluation_window_end_index": outcome_data.get("evaluation_window_end_index"),
        "signal_is_latest_row": outcome_data.get("signal_is_latest_row"),
        "neither_reason": outcome_data.get("neither_reason"),
        "hit_timestamp": outcome_data.get("hit_timestamp"),
        "hit_row_index": outcome_data.get("hit_row_index"),
        "planned_rr": outcome_data.get("planned_rr"),
        "mark_to_market_close": outcome_data.get("mark_to_market_close"),
        "outcome_error": _outcome_error(outcome_data, outcome_result),
        "backtest_success": outcome != "INVALID",
    }
    return {column: _csv_safe_value(row.get(column)) for column in BACKTEST_RESULT_COLUMNS}


def _is_backtest_success(row: dict[str, Any]) -> bool:
    value = row.get("backtest_success")
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return False


def _normalize_result_row(row: dict[str, Any]) -> dict[str, Any]:
    source = row if isinstance(row, dict) else {}
    return {column: _csv_safe_value(source.get(column)) for column in BACKTEST_RESULT_COLUMNS}


def write_backtest_results_csv(
    result_rows: list[dict[str, Any]],
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
        "count": 0,
        "success_count": 0,
        "invalid_count": 0,
        "errors": [],
        "warnings": [],
    }

    if not result_rows:
        result["errors"].append("No backtest result rows were provided.")
        return result

    rows = [_normalize_result_row(row) for row in result_rows]
    success_count = sum(1 for row in rows if _is_backtest_success(row))
    result["count"] = len(rows)
    result["success_count"] = success_count
    result["invalid_count"] = len(rows) - success_count

    try:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        filename = build_backtest_results_filename(ticker=ticker, timeframe=timeframe, timestamp=timestamp)
        path = _collision_safe_path(directory, filename)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=BACKTEST_RESULT_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        result["success"] = True
        result["path"] = str(path)
        result["filename"] = path.name
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def write_backtest_result_csv(
    result_row: dict[str, Any],
    output_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    return write_backtest_results_csv(
        [result_row],
        output_dir,
        ticker=ticker,
        timeframe=timeframe,
        timestamp=timestamp,
    )
