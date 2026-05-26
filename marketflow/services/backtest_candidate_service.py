"""Candidate snapshot normalization for future backtest calibration workflows."""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.backtesting.schemas import CandidateSnapshot


VALIDATION_VALID = "valid"
VALIDATION_MISSING_LEVELS = "missing_levels"
VALIDATION_MISSING_SOURCE_CSV = "missing_source_csv"
VALIDATION_MISSING_SIGNAL_LOCATION = "missing_signal_location"
VALIDATION_INVALID_LEVELS = "invalid_levels"
VALIDATION_UNSUPPORTED_DIRECTION = "unsupported_direction"

SUPPORTED_DIRECTIONS = {"long"}
TIMEFRAME_TOKENS = ("15m", "30m", "1m", "5m", "1h", "4h", "1d", "1w")

SNAPSHOT_FIELDS = [
    "ticker",
    "timeframe",
    "source_csv",
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
    "source_report_dir",
    "source_strategy_rank",
]


def _json_safe_value(value: Any) -> Any:
    """Return a scalar value suitable for JSON serialization."""

    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "item") and not isinstance(value, (str, bytes, bytearray)):
        try:
            value = value.item()
        except (AttributeError, ValueError, TypeError):
            pass
    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    try:
        is_missing = pd.isna(value)
    except (TypeError, ValueError):
        is_missing = False
    if isinstance(is_missing, bool) and is_missing:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


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


def _to_int(value: Any) -> int | None:
    value = _json_safe_value(value)
    if value is None or isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed


def _infer_timeframe_from_text(text: str | None) -> str | None:
    if not text:
        return None
    name = Path(str(text)).name.lower()
    for token in TIMEFRAME_TOKENS:
        pattern = rf"(^|[_\-.]){re.escape(token)}([_\-.]|$)"
        if re.search(pattern, name):
            return token
    return None


def _infer_ticker_from_csv(path: str | Path | None) -> str | None:
    if path is None:
        return None
    stem = Path(str(path)).name
    if not stem:
        return None
    stem = Path(stem).stem
    if not stem:
        return None
    return stem.split("_", 1)[0].upper()


def _first_present(candidate: dict[str, Any], *keys: str) -> tuple[Any, str | None]:
    for key in keys:
        if key in candidate:
            value = _json_safe_value(candidate.get(key))
            if value is not None:
                return value, key
    return None, None


def _computed_risk_reward(entry: float | None, stop_loss: float | None, take_profit: float | None) -> float | None:
    if entry is None or stop_loss is None or take_profit is None:
        return None
    if not (stop_loss < entry < take_profit):
        return None
    risk = entry - stop_loss
    if risk == 0:
        return None
    return (take_profit - entry) / risk


def normalize_candidate_snapshot(candidate: dict[str, Any]) -> dict[str, Any]:
    """Normalize a Strategy Ranking style candidate into a frozen snapshot dict."""

    source_csv, _ = _first_present(candidate, "source_csv", "csv")
    ticker, _ = _first_present(candidate, "ticker")
    timeframe, _ = _first_present(candidate, "timeframe", "tf")
    signal_timestamp, signal_timestamp_source = _first_present(
        candidate,
        "signal_timestamp",
        "timestamp",
        "datetime",
        "date",
    )

    entry = _to_float(_first_present(candidate, "entry", "close")[0])
    stop_loss = _to_float(_first_present(candidate, "stop_loss", "sl")[0])
    take_profit = _to_float(_first_present(candidate, "take_profit", "tp")[0])
    risk_reward = _to_float(_first_present(candidate, "risk_reward", "rr")[0])
    if risk_reward is None:
        risk_reward = _computed_risk_reward(entry, stop_loss, take_profit)

    snapshot = {
        "ticker": ticker or _infer_ticker_from_csv(source_csv),
        "timeframe": timeframe or _infer_timeframe_from_text(str(source_csv) if source_csv else None),
        "source_csv": source_csv,
        "signal_timestamp": signal_timestamp,
        "signal_timestamp_source": signal_timestamp_source,
        "signal_row_index": _to_int(
            _first_present(candidate, "signal_row_index", "row_index", "source_row_index", "index")[0]
        ),
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_reward": risk_reward,
        "strategy_score": _to_float(_first_present(candidate, "strategy_score", "score")[0]),
        "wyckoff_phase": _first_present(candidate, "wyckoff_phase", "phase")[0],
        "wyckoff_event": _first_present(candidate, "wyckoff_event", "event")[0],
        "trend": _first_present(candidate, "trend")[0],
        "candidate_source": _first_present(candidate, "candidate_source", "source")[0] or "strategy_ranking",
        "report_date": _first_present(candidate, "report_date")[0],
        "direction": _first_present(candidate, "direction")[0] or "long",
        "source_report_dir": _first_present(candidate, "source_report_dir")[0],
        "source_strategy_rank": _to_int(_first_present(candidate, "source_strategy_rank", "rank")[0]),
    }
    return {field: _json_safe_value(snapshot.get(field)) for field in SNAPSHOT_FIELDS}


def validate_candidate_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Validate a normalized candidate snapshot without modifying source logic."""

    errors: list[str] = []
    warnings: list[str] = []
    statuses: list[str] = []

    direction = str(snapshot.get("direction") or "").lower()
    if direction not in SUPPORTED_DIRECTIONS:
        statuses.append(VALIDATION_UNSUPPORTED_DIRECTION)
        errors.append("Only long candidate snapshots are supported in this phase.")

    if not snapshot.get("source_csv"):
        statuses.append(VALIDATION_MISSING_SOURCE_CSV)
        errors.append("Missing source_csv.")

    entry = _to_float(snapshot.get("entry"))
    stop_loss = _to_float(snapshot.get("stop_loss"))
    take_profit = _to_float(snapshot.get("take_profit"))
    if entry is None or stop_loss is None or take_profit is None:
        statuses.append(VALIDATION_MISSING_LEVELS)
        errors.append("Missing entry, stop_loss, or take_profit.")

    if snapshot.get("signal_row_index") is None and not snapshot.get("signal_timestamp"):
        statuses.append(VALIDATION_MISSING_SIGNAL_LOCATION)
        errors.append("Missing signal_row_index or signal_timestamp.")

    if entry is not None and stop_loss is not None and take_profit is not None:
        if stop_loss >= entry or take_profit <= entry or entry == stop_loss:
            statuses.append(VALIDATION_INVALID_LEVELS)
            errors.append("Invalid long levels; expected stop_loss < entry < take_profit.")

    if not snapshot.get("ticker"):
        warnings.append("Missing ticker.")
    if not snapshot.get("timeframe"):
        warnings.append("Missing timeframe.")
    if _to_float(snapshot.get("risk_reward")) is None:
        warnings.append("risk_reward missing or could not be computed.")
    if snapshot.get("signal_timestamp") and not snapshot.get("signal_timestamp_source"):
        warnings.append("signal_timestamp present without signal_timestamp_source.")

    priority = [
        VALIDATION_UNSUPPORTED_DIRECTION,
        VALIDATION_MISSING_SOURCE_CSV,
        VALIDATION_MISSING_LEVELS,
        VALIDATION_MISSING_SIGNAL_LOCATION,
        VALIDATION_INVALID_LEVELS,
    ]
    status = VALIDATION_VALID
    for candidate_status in priority:
        if candidate_status in statuses:
            status = candidate_status
            break

    return {"status": status, "errors": errors, "warnings": warnings}


def build_candidate_snapshot_from_strategy_candidate(
    candidate: dict[str, Any],
    *,
    report_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Normalize and validate a selected Strategy Ranking candidate."""

    snapshot = normalize_candidate_snapshot(candidate)
    if report_dir is not None:
        snapshot["source_report_dir"] = str(report_dir)
    validation = validate_candidate_snapshot(snapshot)
    return {
        "success": validation["status"] == VALIDATION_VALID,
        "snapshot": snapshot,
        "validation": validation,
    }


def candidate_snapshot_dict_to_dataclass(snapshot: dict[str, Any]) -> CandidateSnapshot:
    """Convert a normalized snapshot dict to the lightweight dataclass schema."""

    return CandidateSnapshot(
        ticker=snapshot.get("ticker"),
        timeframe=snapshot.get("timeframe"),
        source_csv=snapshot.get("source_csv"),
        signal_timestamp=snapshot.get("signal_timestamp"),
        signal_row_index=_to_int(snapshot.get("signal_row_index")),
        entry=_to_float(snapshot.get("entry")),
        stop_loss=_to_float(snapshot.get("stop_loss")),
        take_profit=_to_float(snapshot.get("take_profit")),
        risk_reward=_to_float(snapshot.get("risk_reward")),
        strategy_score=_to_float(snapshot.get("strategy_score")),
        wyckoff_phase=snapshot.get("wyckoff_phase"),
        wyckoff_event=snapshot.get("wyckoff_event"),
        trend=snapshot.get("trend"),
        candidate_source=snapshot.get("candidate_source"),
        report_date=snapshot.get("report_date"),
    )
