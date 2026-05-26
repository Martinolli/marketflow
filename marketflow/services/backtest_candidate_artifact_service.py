"""CSV artifact writer for backtest candidate snapshots."""

from __future__ import annotations

import csv
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


BACKTEST_CANDIDATE_COLUMNS = [
    "created_at",
    "ticker",
    "timeframe",
    "source_csv",
    "source_report_dir",
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
    "trend",
    "candidate_source",
    "report_date",
    "direction",
    "source_strategy_rank",
    "validation_status",
    "validation_errors",
    "validation_warnings",
    "snapshot_success",
]


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


def build_backtest_candidates_filename(
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> str:
    stamp = _timestamp_for_filename(timestamp)
    ticker_part = _safe_filename_part(ticker)
    timeframe_part = _safe_filename_part(timeframe)
    if ticker_part and timeframe_part:
        return f"{ticker_part}_{timeframe_part}_backtest_candidates_{stamp}.csv"
    return f"marketflow_backtest_candidates_{stamp}.csv"


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
        return _messages_to_string(value)
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
    if isinstance(is_missing, bool) and is_missing:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _messages_to_string(messages: Any) -> str:
    if messages is None:
        return ""
    try:
        is_missing = pd.isna(messages)
    except (TypeError, ValueError):
        is_missing = False
    if isinstance(is_missing, bool) and is_missing:
        return ""
    if isinstance(messages, str):
        return messages
    if isinstance(messages, (list, tuple, set)):
        return "; ".join(str(_csv_safe_value(message)) for message in messages if _csv_safe_value(message) != "")
    return str(_csv_safe_value(messages))


def candidate_snapshot_row(
    snapshot_result: dict[str, Any],
    *,
    created_at: str | None = None,
) -> dict[str, Any]:
    if not isinstance(snapshot_result, dict):
        snapshot_result = {}

    snapshot = snapshot_result.get("snapshot")
    if not isinstance(snapshot, dict):
        snapshot = {}
    validation = snapshot_result.get("validation")
    if not isinstance(validation, dict):
        validation = {}

    validation_status = validation.get("status") or "unknown"
    row = {
        "created_at": created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ticker": snapshot.get("ticker"),
        "timeframe": snapshot.get("timeframe"),
        "source_csv": snapshot.get("source_csv"),
        "source_report_dir": snapshot.get("source_report_dir"),
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
        "trend": snapshot.get("trend"),
        "candidate_source": snapshot.get("candidate_source"),
        "report_date": snapshot.get("report_date"),
        "direction": snapshot.get("direction"),
        "source_strategy_rank": snapshot.get("source_strategy_rank"),
        "validation_status": validation_status,
        "validation_errors": _messages_to_string(validation.get("errors")),
        "validation_warnings": _messages_to_string(validation.get("warnings")),
        "snapshot_success": validation_status == "valid",
    }
    return {column: _csv_safe_value(row.get(column)) for column in BACKTEST_CANDIDATE_COLUMNS}


def write_backtest_candidates_csv(
    snapshot_results: list[dict[str, Any]],
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
        "valid_count": 0,
        "invalid_count": 0,
        "errors": [],
        "warnings": [],
    }

    if not snapshot_results:
        result["errors"].append("No snapshot results were provided.")
        return result

    rows = [candidate_snapshot_row(snapshot_result) for snapshot_result in snapshot_results]
    valid_count = sum(1 for row in rows if row.get("snapshot_success") is True)
    result["count"] = len(rows)
    result["valid_count"] = valid_count
    result["invalid_count"] = len(rows) - valid_count

    try:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        filename = build_backtest_candidates_filename(ticker=ticker, timeframe=timeframe, timestamp=timestamp)
        path = _collision_safe_path(directory, filename)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=BACKTEST_CANDIDATE_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        result["success"] = True
        result["path"] = str(path)
        result["filename"] = path.name
        return result
    except Exception as exc:
        result["errors"].append(f"{type(exc).__name__}: {exc}")
        return result


def write_backtest_candidate_csv(
    snapshot_result: dict[str, Any],
    output_dir: str | Path,
    *,
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    return write_backtest_candidates_csv(
        [snapshot_result],
        output_dir,
        ticker=ticker,
        timeframe=timeframe,
        timestamp=timestamp,
    )
