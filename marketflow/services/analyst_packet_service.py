"""Build structured context packets for a future Wyckoff Volume Analyst."""

from __future__ import annotations

import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.services.report_index import infer_timeframe_from_csv_name


PACKET_VERSION = "0.1"
PROFILE_PATH = Path(__file__).resolve().parents[1] / "config" / "analyst_profile.example.json"
MIN_SUPPORTIVE_PNF_R = 1.0
EXTREME_OBJECTIVE_R = 10.0
EXTREME_OBJECTIVE_DISTANCE_PCT = 0.75


DEFAULT_ANALYST_PROFILE: dict[str, Any] = {
    "account_size": 1000,
    "risk_per_trade_pct": 1.0,
    "risk_per_trade_amount": 10,
    "max_total_open_risk": 25,
    "long_only": True,
    "preferred_price_min": 20,
    "preferred_price_max": 80,
    "main_pop_threshold": 0.52,
    "backup_pop_threshold": 0.45,
    "min_pnf_objective_r": 1.5,
    "min_composite_score": 70,
    "broker": "IBKR",
    "timezone": "Asia/Dubai",
    "holding_period_days": [1, 5],
    "notes": "Personal test profile. Do not treat as financial advice.",
}

TIMEFRAME_TOKENS = ("1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m")


def load_default_analyst_profile() -> dict[str, Any]:
    """
    Load the bundled analyst profile example.

    Return a safe default dictionary if the file cannot be loaded.
    """
    try:
        with open(PROFILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else dict(DEFAULT_ANALYST_PROFILE)
    except Exception:
        return dict(DEFAULT_ANALYST_PROFILE)


def _safe_get(data: Any, path: list[str], default: Any = None) -> Any:
    """Read a nested dictionary path safely."""
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def _first_value(data: dict[str, Any] | None, paths: list[list[str]]) -> Any:
    """Return the first non-empty value found at any path."""
    if not isinstance(data, dict):
        return None
    for path in paths:
        value = _safe_get(data, path)
        if value is not None:
            return value
    return None


def _to_float(value: Any) -> float | None:
    """Convert numeric-like values to float, returning None on failure."""
    if value is None or value == "":
        return None
    try:
        number = float(value)
        return None if math.isnan(number) or math.isinf(number) else number
    except (TypeError, ValueError):
        return None


def _as_list(value: Any) -> list[Any]:
    """Return value as a list without treating strings as iterables."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _level_price(level: Any) -> float | None:
    """Extract a price from common level shapes."""
    if isinstance(level, dict):
        for key in ("price", "level", "value", "y"):
            price = _to_float(level.get(key))
            if price is not None:
                return price
        return None
    return _to_float(level)


def _first_direct_value(data: dict[str, Any] | None, keys: tuple[str, ...]) -> Any:
    """Return the first present top-level value from a dictionary."""
    if not isinstance(data, dict):
        return None
    for key in keys:
        if key in data and data[key] is not None and data[key] != "":
            return data[key]
    return None


def _first_pnf_value(data: dict[str, Any] | None, keys: tuple[str, ...]) -> Any:
    """Return a P&F sidecar value from top-level or common nested containers."""
    direct_value = _first_direct_value(data, keys)
    if direct_value is not None:
        return direct_value

    if not isinstance(data, dict):
        return None
    for container_key in ("count", "pnf", "meta", "summary"):
        container = data.get(container_key)
        nested_value = _first_direct_value(container, keys) if isinstance(container, dict) else None
        if nested_value is not None:
            return nested_value
    return None


def _pnf_float(value: Any) -> float | None:
    """Convert P&F numeric fields without treating booleans as prices."""
    if isinstance(value, bool):
        return None
    return _to_float(value)


def _first_pnf_float(data: dict[str, Any] | None, keys: tuple[str, ...]) -> float | None:
    """Return the first numeric P&F sidecar value from known locations."""
    candidates = [_first_direct_value(data, keys)]
    if isinstance(data, dict):
        for container_key in ("count", "pnf", "meta", "summary"):
            container = data.get(container_key)
            if isinstance(container, dict):
                candidates.append(_first_direct_value(container, keys))

    for candidate in candidates:
        number = _pnf_float(candidate)
        if number is not None:
            return number
    return None


def _pnf_int(value: Any) -> int | None:
    """Convert P&F integer fields defensively."""
    number = _pnf_float(value)
    if number is None:
        return None
    try:
        return int(number)
    except (TypeError, ValueError, OverflowError):
        return None


def _path_match_key(value: Any) -> str | None:
    """Return a stable path key for best-effort CSV path comparisons."""
    if value is None or value == "":
        return None
    try:
        return str(Path(str(value)).expanduser().resolve()).lower()
    except Exception:
        return str(value).replace("\\", "/").lower()


def _filename_key(value: Any) -> str | None:
    """Return a lower-case filename key from a path-like value."""
    if value is None or value == "":
        return None
    return Path(str(value)).name.lower()


def _infer_timeframe_from_text(value: Any) -> str | None:
    """Infer a timeframe token from filenames or paths."""
    if value is None or value == "":
        return None
    inferred = infer_timeframe_from_csv_name(str(value))
    if inferred:
        return inferred
    text = Path(str(value)).stem.lower().replace("-", "_")
    tokens = [token for token in re.split(r"[_\-.\\/\s]+", text) if token]
    for token in reversed(tokens):
        if token in TIMEFRAME_TOKENS:
            return token
    return None


def _compact_pnf_record(record: dict[str, Any] | None) -> dict[str, Any] | None:
    """Return the compact P&F record shape used by packet selection fields."""
    if not isinstance(record, dict):
        return None
    keys = (
        "filename",
        "path",
        "source_csv",
        "source_csv_path",
        "inferred_timeframe",
        "timeframe",
        "box_mode",
        "box_value",
        "box_size",
        "reversal",
        "last_price",
        "objective",
        "breakout_level",
        "objective_direction",
        "objective_supports_trade",
        "objective_distance_pct",
        "objective_r_multiple",
        "objective_quality",
        "objective_notes",
        "trade_direction",
        "direction",
        "match_score",
        "match_reasons",
        "matched_by",
        "generated_by",
        "generated_at",
        "nrows",
    )
    return {key: record.get(key) for key in keys if key in record}


def list_pnf_sidecars(report_dir: str | None) -> list[str]:
    """
    Return P&F sidecar JSON files found in the report directory.

    Search only the report directory, not the whole repo.
    Match files like:
    - *_pnf_meta.json
    - *pnf*.json

    Return paths sorted newest first by modified time.
    """
    if not report_dir:
        return []

    try:
        directory = Path(report_dir)
        if not directory.exists() or not directory.is_dir():
            return []
        paths = {
            path.resolve()
            for pattern in ("*_pnf_meta.json", "*pnf*.json")
            for path in directory.glob(pattern)
            if path.is_file()
        }
        return [
            str(path)
            for path in sorted(
                paths,
                key=lambda item: item.stat().st_mtime,
                reverse=True,
            )
        ]
    except Exception:
        return []


def _normalize_pnf_sidecar(path: str, data: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize a P&F sidecar into a stable schema.
    """
    sidecar_path = Path(path)
    filename = sidecar_path.name
    source_csv = _first_pnf_value(data, ("source_csv", "csv", "csv_file", "csv_filename"))
    source_csv_path = _first_pnf_value(data, ("source_csv_path", "csv_path", "source_path"))
    timeframe_value = _first_pnf_value(data, ("timeframe", "tf", "interval"))
    inferred_timeframe = (
        _first_pnf_value(data, ("inferred_timeframe", "source_timeframe"))
        or timeframe_value
        or _infer_timeframe_from_text(source_csv_path)
        or _infer_timeframe_from_text(source_csv)
        or _infer_timeframe_from_text(filename)
        or _infer_timeframe_from_text(sidecar_path.parent.name)
    )
    direction_value = _first_pnf_value(data, ("direction", "count_direction", "trend"))
    last_price = _first_pnf_float(data, ("last_price", "spot", "current_price", "close"))
    objective = _first_pnf_float(data, ("objective", "objective_price", "target", "target_price"))

    distance_to_objective = None
    distance_to_objective_pct = None
    objective_direction = "unknown"
    objective_notes: list[str] = []
    if last_price is not None and last_price != 0 and objective is not None:
        distance_to_objective = objective - last_price
        distance_to_objective_pct = distance_to_objective / last_price * 100
        objective_direction = "upside" if objective > last_price else "downside" if objective < last_price else "unknown"
    else:
        objective_notes.append("Insufficient P&F metadata for objective direction.")

    return {
        "path": str(sidecar_path),
        "filename": filename,
        "source_csv": str(source_csv) if source_csv is not None else None,
        "source_csv_path": str(source_csv_path) if source_csv_path is not None else None,
        "inferred_timeframe": str(inferred_timeframe) if inferred_timeframe is not None else None,
        "box_mode": _first_pnf_value(data, ("box_mode", "scale", "pnf_scale")),
        "box_value": _first_pnf_float(data, ("box_value", "scale_value", "pnf_scale_value")),
        "generated_by": _first_pnf_value(data, ("generated_by",)),
        "generated_at": _first_pnf_value(data, ("generated_at", "created_at")),
        "nrows": _pnf_int(_first_pnf_value(data, ("nrows", "rows", "row_limit"))),
        "modified_time": sidecar_path.stat().st_mtime if sidecar_path.exists() else None,
        "timeframe": str(timeframe_value) if timeframe_value is not None else None,
        "direction": str(direction_value) if direction_value is not None else None,
        "box_pct": _first_pnf_float(data, ("box_pct", "box_percent")),
        "box_size": _first_pnf_float(data, ("box_size", "box")),
        "reversal": _pnf_int(_first_pnf_value(data, ("reversal", "rev"))),
        "last_price": last_price,
        "breakout_level": _first_pnf_float(data, ("breakout", "breakout_level", "break_level", "breakout_price")),
        "objective": objective,
        "objective_direction": objective_direction,
        "objective_supports_trade": None,
        "objective_distance_pct": (distance_to_objective / last_price) if last_price not in (None, 0) and distance_to_objective is not None else None,
        "objective_r_multiple": None,
        "objective_quality": "unknown",
        "objective_notes": objective_notes,
        "distance_to_objective": distance_to_objective,
        "distance_to_objective_pct": distance_to_objective_pct,
        "trade_direction": None,
        "match_score": 0,
        "match_reasons": [],
        "matched_by": None,
        "raw": data if isinstance(data, dict) else {},
    }


def load_pnf_sidecars(report_dir: str | None) -> list[dict[str, Any]]:
    """
    Load and normalize P&F sidecar JSON files.

    Return a list of normalized P&F records.
    Do not raise UI-breaking exceptions.
    """
    records: list[dict[str, Any]] = []
    for path in list_pnf_sidecars(report_dir):
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict):
                data = {"_error": "P&F sidecar root is not a JSON object.", "value": data}
        except Exception as exc:
            data = {"_error": f"Could not load P&F sidecar: {type(exc).__name__}: {exc}"}

        try:
            records.append(_normalize_pnf_sidecar(path, data))
        except Exception as exc:
            records.append(
                _normalize_pnf_sidecar(
                    path,
                    {"_error": f"Could not normalize P&F sidecar: {type(exc).__name__}: {exc}"},
                )
            )
    return records


def _attach_pnf_objective_r(
    records: list[dict[str, Any]],
    strategy_candidate: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Compute objective R multiples when trade entry and stop are available."""
    if not isinstance(strategy_candidate, dict):
        return records

    entry = _to_float(strategy_candidate.get("close") if strategy_candidate.get("close") is not None else strategy_candidate.get("entry"))
    stop_loss = _to_float(
        strategy_candidate.get("stop_loss") if strategy_candidate.get("stop_loss") is not None else strategy_candidate.get("sl")
    )
    if entry is None or stop_loss is None:
        return records

    risk = entry - stop_loss
    if risk <= 0:
        return records

    for record in records:
        objective = _to_float(record.get("objective"))
        if objective is not None:
            record["objective_r_multiple"] = (objective - entry) / risk
    return records


def _profile_min_pnf_objective_r(profile: dict[str, Any] | None) -> float:
    """Return the configured P&F R threshold or the local fallback."""
    if isinstance(profile, dict):
        configured = _to_float(profile.get("min_pnf_objective_r"))
        if configured is not None:
            return configured
    return MIN_SUPPORTIVE_PNF_R


def _candidate_trade_direction(strategy_candidate: dict[str, Any] | None) -> str | None:
    """Return the locally derived trade direction for current strategy candidates."""
    return "long" if isinstance(strategy_candidate, dict) else None


def _pnf_objective_direction(
    objective: float | None,
    last_price: float | None,
    entry: float | None,
) -> str:
    """Infer whether the objective is above or below the selected setup reference."""
    if objective is None:
        return "unknown"

    references = [value for value in (entry, last_price) if value is not None]
    if not references:
        return "unknown"

    if any(objective > value for value in references) and not any(objective < value for value in references):
        return "upside"
    if any(objective < value for value in references) and not any(objective > value for value in references):
        return "downside"
    if entry is not None:
        return "upside" if objective > entry else "downside" if objective < entry else "unknown"
    return "upside" if objective > references[0] else "downside" if objective < references[0] else "unknown"


def _attach_pnf_objective_interpretation(
    records: list[dict[str, Any]],
    strategy_candidate: dict[str, Any] | None,
    profile: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Attach direction, support, quality, and notes to normalized P&F sidecars."""
    trade_direction = _candidate_trade_direction(strategy_candidate)
    entry = _to_float((strategy_candidate or {}).get("entry") or (strategy_candidate or {}).get("close"))
    min_pnf_objective_r = _profile_min_pnf_objective_r(profile)

    for record in records:
        if not isinstance(record, dict):
            continue

        objective = _to_float(record.get("objective"))
        last_price = _to_float(record.get("last_price"))
        objective_r = _to_float(record.get("objective_r_multiple"))
        objective_distance_pct = None
        if objective is not None and last_price is not None and last_price != 0:
            objective_distance_pct = (objective - last_price) / last_price

        objective_direction = _pnf_objective_direction(objective, last_price, entry)
        objective_supports_trade: bool | None = None
        if trade_direction == "long":
            if objective_direction == "upside":
                objective_supports_trade = True
            elif objective_direction == "downside":
                objective_supports_trade = False

        notes: list[str] = []
        existing_notes = record.get("objective_notes")
        if isinstance(existing_notes, list):
            notes.extend(str(item) for item in existing_notes if item)
        elif existing_notes:
            notes.append(str(existing_notes))

        if objective_direction == "unknown":
            notes.append("Insufficient P&F metadata for objective direction.")
        elif trade_direction == "long" and objective_direction == "downside":
            notes.append("P&F objective contradicts selected long setup.")
        elif trade_direction == "long" and objective_direction == "upside":
            notes.append("P&F objective is above the selected long setup reference.")

        if objective_r is None:
            notes.append("P&F objective R could not be computed from selected trade levels.")
        elif objective_r < 0:
            notes.append("P&F objective R is negative.")

        if objective_distance_pct is not None and abs(objective_distance_pct) > EXTREME_OBJECTIVE_DISTANCE_PCT:
            notes.append("P&F objective is unusually far from last price.")
        if objective_r is not None and abs(objective_r) > EXTREME_OBJECTIVE_R:
            notes.append("P&F objective R is unusually large.")

        if objective_supports_trade is False:
            objective_quality = "risk"
        elif objective_supports_trade is True and objective_r is not None:
            objective_quality = "supportive" if objective_r > min_pnf_objective_r else "weak"
        else:
            objective_quality = "unknown"

        record["trade_direction"] = trade_direction
        record["objective_direction"] = objective_direction
        record["objective_supports_trade"] = objective_supports_trade
        record["objective_distance_pct"] = objective_distance_pct
        record["objective_quality"] = objective_quality
        record["objective_notes"] = list(dict.fromkeys(notes))

    return records


def _candidate_csv_value(
    strategy_candidate: dict[str, Any] | None,
    monte_carlo_result: dict[str, Any] | None,
) -> Any:
    if isinstance(strategy_candidate, dict) and strategy_candidate.get("csv"):
        return strategy_candidate.get("csv")
    if isinstance(monte_carlo_result, dict):
        return monte_carlo_result.get("csv") or monte_carlo_result.get("csv_path")
    return None


def _candidate_timeframe_value(
    strategy_candidate: dict[str, Any] | None,
    monte_carlo_result: dict[str, Any] | None,
) -> str | None:
    tf = None
    if isinstance(strategy_candidate, dict):
        tf = strategy_candidate.get("tf")
    if not tf and isinstance(monte_carlo_result, dict):
        tf = monte_carlo_result.get("tf") or monte_carlo_result.get("timeframe")
    if tf:
        return str(tf)
    return _infer_timeframe_from_text(_candidate_csv_value(strategy_candidate, monte_carlo_result))


def _candidate_price_values(
    strategy_candidate: dict[str, Any] | None,
    monte_carlo_result: dict[str, Any] | None,
) -> list[tuple[str, float]]:
    values: list[tuple[str, float]] = []
    for label, value in (
        ("candidate entry", (strategy_candidate or {}).get("entry")),
        ("candidate close", (strategy_candidate or {}).get("close")),
        ("monte carlo spot", (monte_carlo_result or {}).get("spot_s0")),
        ("monte carlo entry", (monte_carlo_result or {}).get("entry")),
        ("monte carlo current price", (monte_carlo_result or {}).get("current_price")),
    ):
        number = _to_float(value)
        if number is not None:
            values.append((label, number))
    deduped: list[tuple[str, float]] = []
    seen: set[float] = set()
    for label, number in values:
        rounded = round(number, 8)
        if rounded not in seen:
            seen.add(rounded)
            deduped.append((label, number))
    return deduped


def _price_match_reason(last_price: float | None, price_values: list[tuple[str, float]]) -> tuple[int, str | None]:
    if last_price is None or not price_values:
        return 0, None

    best: tuple[float, str, float] | None = None
    for label, price in price_values:
        if price == 0:
            continue
        delta_pct = abs(last_price - price) / abs(price) * 100
        if best is None or delta_pct < best[0]:
            best = (delta_pct, label, price)
    if best is None:
        return 0, None

    delta_pct, label, _price = best
    if delta_pct <= 0.5:
        return 20, f"last price within 0.5% of {label}"
    if delta_pct <= 1.0:
        return 12, f"last price within 1% of {label}"
    if delta_pct <= 3.0:
        return 6, f"last price within 3% of {label}"
    return -5, f"last price differs from selected trade price by {delta_pct:.1f}%"


def _matched_by_from_reasons(reasons: list[str]) -> str | None:
    for key, label in (
        ("source CSV path", "source_csv_path"),
        ("source CSV filename", "source_csv"),
        ("timeframe", "timeframe"),
        ("filename contains candidate timeframe", "filename_timeframe"),
        ("last price", "price"),
        ("newest", "recency"),
        ("objective", "objective"),
    ):
        if any(key in reason for reason in reasons):
            return label
    return None


def _score_pnf_sidecar(
    sidecar: dict[str, Any],
    *,
    candidate_csv: Any,
    candidate_tf: str | None,
    candidate_prices: list[tuple[str, float]],
    has_timeframe_match: bool,
    newest_modified_time: float | None,
) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    candidate_path_key = _path_match_key(candidate_csv)
    sidecar_source_path_key = _path_match_key(sidecar.get("source_csv_path"))
    candidate_name = _filename_key(candidate_csv)
    source_name = _filename_key(sidecar.get("source_csv") or sidecar.get("source_csv_path"))

    if candidate_path_key and sidecar_source_path_key and candidate_path_key == sidecar_source_path_key:
        score += 100
        reasons.append("source CSV path matched selected candidate CSV")
    if candidate_name and source_name and candidate_name == source_name:
        score += 80
        reasons.append("source CSV filename matched selected candidate CSV")

    sidecar_tf = sidecar.get("inferred_timeframe") or sidecar.get("timeframe")
    if candidate_tf:
        filename = str(sidecar.get("filename") or "").lower()
        if sidecar_tf and str(sidecar_tf) == str(candidate_tf):
            score += 35
            reasons.append(f"timeframe matched candidate tf {candidate_tf}")
        elif f"_{candidate_tf}_" in f"_{filename}_":
            score += 25
            reasons.append(f"filename contains candidate timeframe {candidate_tf}")
        elif has_timeframe_match and sidecar_tf and str(sidecar_tf) != str(candidate_tf):
            score -= 90
            reasons.append(f"timeframe {sidecar_tf} differs from candidate tf {candidate_tf}")

    price_score, price_reason = _price_match_reason(_to_float(sidecar.get("last_price")), candidate_prices)
    score += price_score
    if price_reason:
        reasons.append(price_reason)

    entry = next((price for label, price in candidate_prices if "entry" in label), None)
    objective = _to_float(sidecar.get("objective"))
    if entry is not None and objective is not None and objective > entry:
        score += 10
        reasons.append("objective is above selected long entry")
    elif objective is not None:
        score += 2
        reasons.append("objective is present")

    objective_r = _to_float(sidecar.get("objective_r_multiple"))
    if objective_r is not None and objective_r > 0:
        score += 5
        reasons.append("objective R is positive")

    modified_time = _to_float(sidecar.get("modified_time"))
    if newest_modified_time is not None and modified_time == newest_modified_time and score > 0:
        score += 5
        reasons.append("newest matching sidecar")

    return score, reasons


def select_best_pnf_sidecar(
    sidecars: list[dict[str, Any]],
    strategy_candidate: dict[str, Any] | None,
    monte_carlo_result: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Select the P&F sidecar that best matches the selected strategy candidate."""
    if not sidecars:
        return None

    candidate_csv = _candidate_csv_value(strategy_candidate, monte_carlo_result)
    candidate_tf = _candidate_timeframe_value(strategy_candidate, monte_carlo_result)
    candidate_prices = _candidate_price_values(strategy_candidate, monte_carlo_result)
    has_timeframe_match = bool(
        candidate_tf
        and any(
            str(item.get("inferred_timeframe") or item.get("timeframe") or "") == str(candidate_tf)
            or f"_{candidate_tf}_" in f"_{str(item.get('filename') or '').lower()}_"
            for item in sidecars
            if isinstance(item, dict)
        )
    )
    modified_times = [
        item
        for item in (_to_float(record.get("modified_time")) for record in sidecars if isinstance(record, dict))
        if item is not None
    ]
    newest_modified_time = max(modified_times) if modified_times else None

    for sidecar in sidecars:
        if not isinstance(sidecar, dict):
            continue
        score, reasons = _score_pnf_sidecar(
            sidecar,
            candidate_csv=candidate_csv,
            candidate_tf=candidate_tf,
            candidate_prices=candidate_prices,
            has_timeframe_match=has_timeframe_match,
            newest_modified_time=newest_modified_time,
        )
        sidecar["match_score"] = score
        sidecar["match_reasons"] = reasons
        sidecar["matched_by"] = _matched_by_from_reasons(reasons)

    scored = [item for item in sidecars if isinstance(item, dict)]
    if not scored:
        return None
    return max(
        scored,
        key=lambda item: (
            _to_float(item.get("match_score")) or 0,
            _to_float(item.get("modified_time")) or float("-inf"),
        ),
    )


def _best_pnf_objective(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Choose the most useful P&F objective record for packet summaries."""
    r_records = [
        record
        for record in records
        if _to_float(record.get("objective_r_multiple")) is not None
    ]
    if r_records:
        return max(r_records, key=lambda record: _to_float(record.get("objective_r_multiple")) or float("-inf"))

    distance_records = [
        record
        for record in records
        if (_to_float(record.get("distance_to_objective_pct")) or 0) > 0
    ]
    if distance_records:
        return max(distance_records, key=lambda record: _to_float(record.get("distance_to_objective_pct")) or float("-inf"))
    return None


def _build_pnf_section(
    records: list[dict[str, Any]],
    strategy_candidate: dict[str, Any] | None = None,
    monte_carlo_result: dict[str, Any] | None = None,
    gate: str = "pending",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    """Build the packet P&F section."""
    selected = select_best_pnf_sidecar(records, strategy_candidate, monte_carlo_result)
    candidate_csv = _candidate_csv_value(strategy_candidate, monte_carlo_result)
    candidate_tf = _candidate_timeframe_value(strategy_candidate, monte_carlo_result)
    selected_compact = _compact_pnf_record(selected)
    objective_interpretation = {
        "trade_direction": selected_compact.get("trade_direction") if isinstance(selected_compact, dict) else _candidate_trade_direction(strategy_candidate),
        "objective_direction": selected_compact.get("objective_direction") if isinstance(selected_compact, dict) else "unknown",
        "objective_supports_trade": selected_compact.get("objective_supports_trade") if isinstance(selected_compact, dict) else None,
        "objective_distance_pct": selected_compact.get("objective_distance_pct") if isinstance(selected_compact, dict) else None,
        "objective_r_multiple": selected_compact.get("objective_r_multiple") if isinstance(selected_compact, dict) else None,
        "objective_quality": selected_compact.get("objective_quality") if isinstance(selected_compact, dict) else "unknown",
        "notes": selected_compact.get("objective_notes") if isinstance(selected_compact, dict) else ["Insufficient P&F metadata for objective direction."],
    }
    if not isinstance(objective_interpretation["notes"], list):
        objective_interpretation["notes"] = _as_list(objective_interpretation["notes"])
    selection_notes: list[str] = []
    selection_warnings: list[str] = []

    if selected:
        score = _to_float(selected.get("match_score")) or 0
        selected_tf = selected.get("inferred_timeframe") or selected.get("timeframe")
        if candidate_csv and not selected.get("source_csv") and not selected.get("source_csv_path"):
            selection_notes.append("P&F sidecar selected by fallback matching; source CSV metadata missing.")
        if candidate_tf and selected_tf and str(selected_tf) != str(candidate_tf):
            selection_warnings.append(
                f"P&F sidecar timeframe {selected_tf} differs from candidate timeframe {candidate_tf}."
            )
        if len(records) > 1 and score < 50:
            selection_warnings.append(
                "Multiple P&F sidecars found. Verify selected sidecar before relying on P&F gate."
            )
        for note in selected.get("objective_notes") or []:
            if "contradicts" in str(note) or "negative" in str(note) or "unusually" in str(note):
                selection_warnings.append(str(note))

    return {
        "available": bool(records),
        "sidecars": records,
        "best_objective": _best_pnf_objective(records),
        "selected_sidecar": selected_compact,
        "objective_interpretation": objective_interpretation,
        "selection": {
            "selected_filename": selected.get("filename") if isinstance(selected, dict) else None,
            "matched_by": selected.get("matched_by") if isinstance(selected, dict) else None,
            "match_score": selected.get("match_score") if isinstance(selected, dict) else None,
            "match_reasons": selected.get("match_reasons") if isinstance(selected, dict) else [],
            "candidate_csv": str(candidate_csv) if candidate_csv else None,
            "candidate_timeframe": candidate_tf,
        },
        "gate": gate,
        "notes": [*(notes or []), *selection_notes],
        "warnings": selection_warnings,
    }


def _distance_band(delta_pct_abs: float | None) -> str | None:
    """Assign a heatmap distance band."""
    if delta_pct_abs is None:
        return None
    if delta_pct_abs <= 1:
        return "within_1_pct"
    if delta_pct_abs <= 3:
        return "one_to_3_pct"
    if delta_pct_abs <= 6:
        return "three_to_6_pct"
    return "greater_than_6_pct"


def _normalize_level(
    kind: str,
    value: Any,
    current_price: float | None,
    timeframe: str | None = None,
    label: str | None = None,
) -> dict[str, Any]:
    """Build a normalized level record."""
    price = _level_price(value)
    delta = price - current_price if price is not None and current_price is not None else None
    delta_pct = (delta / current_price * 100) if delta is not None and current_price else None
    return {
        "kind": kind,
        "timeframe": timeframe,
        "label": label,
        "price": price,
        "delta": delta,
        "delta_pct": delta_pct,
        "band": _distance_band(abs(delta_pct) if delta_pct is not None else None),
    }


def _timeframe_source(report_json: dict[str, Any] | None) -> dict[str, Any]:
    """Return timeframe data from known report schemas."""
    if not isinstance(report_json, dict):
        return {}
    source = report_json.get("timeframe_data") or report_json.get("timeframes") or {}
    return source if isinstance(source, dict) else {}


def _compact_phases(phases: Any) -> Any:
    """Summarize Wyckoff phase series without carrying every bar."""
    if isinstance(phases, list):
        latest = phases[-1] if phases else None
        recent_names = []
        for item in phases[-5:]:
            if isinstance(item, dict):
                recent_names.append(item.get("phase_name") or item.get("phase"))
            else:
                recent_names.append(str(item))
        return {"count": len(phases), "latest": latest, "recent_names": recent_names}
    return phases


def _compact_events(events: Any, max_items: int = 20) -> list[Any]:
    """Return a compact recent event list."""
    compact: list[Any] = []
    for event in _as_list(events)[-max_items:]:
        if isinstance(event, dict):
            compact.append(
                {
                    "event": event.get("event"),
                    "event_name": event.get("event_name"),
                    "timestamp": event.get("timestamp"),
                    "price": event.get("price"),
                    "volume": event.get("volume"),
                    "vol_spike": event.get("vol_spike"),
                }
            )
        else:
            compact.append(event)
    return compact


def _present(value: Any) -> bool:
    """Return True when a report/CSV value is meaningfully populated."""
    if value is None:
        return False
    if isinstance(value, float) and math.isnan(value):
        return False
    text = str(value).strip()
    return bool(text and text.lower() not in {"nan", "none", "null"})


def _extract_market_snapshot(report_json: dict[str, Any] | None, missing_data: list[str]) -> dict[str, Any]:
    """Extract common market and risk fields."""
    current_price = _to_float(_first_value(report_json, [["current_price"], ["market_snapshot", "current_price"]]))
    signal_type = _first_value(report_json, [["vpa_signal", "type"], ["signal", "type"]])
    signal_strength = _first_value(report_json, [["vpa_signal", "strength"], ["signal", "strength"]])
    stop_loss = _to_float(_first_value(report_json, [["risk_assessment", "stop_loss"], ["risk", "stop_loss"]]))
    take_profit = _to_float(_first_value(report_json, [["risk_assessment", "take_profit"], ["risk", "take_profit"]]))
    risk_reward = _to_float(
        _first_value(report_json, [["risk_assessment", "risk_reward_ratio"], ["risk", "risk_reward"]])
    )

    expected = {
        "current_price": current_price,
        "signal_type": signal_type,
        "signal_strength": signal_strength,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_reward": risk_reward,
    }
    for key, value in expected.items():
        if value is None:
            missing_data.append(f"market_snapshot.{key}")

    return {
        "current_price": current_price,
        "signal_type": signal_type,
        "signal_strength": signal_strength,
        "risk": {
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": risk_reward,
        },
        "report_baseline_risk": {
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": risk_reward,
        },
    }


def _extract_timeframes(report_json: dict[str, Any] | None) -> dict[str, Any]:
    """Extract compact per-timeframe context."""
    compact: dict[str, Any] = {}
    for timeframe, data in _timeframe_source(report_json).items():
        if not isinstance(data, dict):
            compact[str(timeframe)] = data
            continue
        wyckoff = data.get("wyckoff") if isinstance(data.get("wyckoff"), dict) else {}
        support_resistance = (
            data.get("support_resistance") if isinstance(data.get("support_resistance"), dict) else {}
        )
        compact[str(timeframe)] = {
            "trend": data.get("trend"),
            "wyckoff_context": wyckoff.get("context"),
            "wyckoff_phases": _compact_phases(wyckoff.get("phases")),
            "wyckoff_events": _compact_events(wyckoff.get("events")),
            "support_count": len(_as_list(support_resistance.get("support"))),
            "resistance_count": len(_as_list(support_resistance.get("resistance"))),
            "volume_at_levels_count": len(_as_list(support_resistance.get("volume_at_levels"))),
        }
    return compact


def _extract_levels(
    report_json: dict[str, Any] | None,
    current_price: float | None,
    strategy_candidate: dict[str, Any] | None,
) -> tuple[dict[str, Any], list[str]]:
    """Extract support/resistance and trade levels with heatmap bands."""
    warnings: list[str] = []
    support: list[dict[str, Any]] = []
    resistance: list[dict[str, Any]] = []
    trade_levels: list[dict[str, Any]] = []
    heatmap = {
        "within_1_pct": [],
        "one_to_3_pct": [],
        "three_to_6_pct": [],
        "greater_than_6_pct": [],
    }

    if current_price is None:
        warnings.append("Current price unavailable; level distance heatmap is incomplete.")

    for timeframe, data in _timeframe_source(report_json).items():
        support_resistance = data.get("support_resistance") if isinstance(data, dict) else None
        if not isinstance(support_resistance, dict):
            continue
        for level in _as_list(support_resistance.get("support")):
            support.append(_normalize_level("support", level, current_price, str(timeframe)))
        for level in _as_list(support_resistance.get("resistance")):
            resistance.append(_normalize_level("resistance", level, current_price, str(timeframe)))

    if isinstance(strategy_candidate, dict):
        trade_level_inputs = {
            "entry": strategy_candidate.get("entry") or strategy_candidate.get("close"),
            "stop_loss": strategy_candidate.get("sl") or strategy_candidate.get("stop_loss"),
            "take_profit": strategy_candidate.get("tp") or strategy_candidate.get("take_profit"),
        }
        for label, value in trade_level_inputs.items():
            if value is not None:
                trade_levels.append(_normalize_level("trade", value, current_price, None, label))

    for level in support + resistance + trade_levels:
        band = level.get("band")
        if band in heatmap:
            heatmap[band].append(
                {
                    "kind": level.get("kind"),
                    "timeframe": level.get("timeframe"),
                    "label": level.get("label"),
                    "price": level.get("price"),
                    "delta_pct": level.get("delta_pct"),
                }
            )

    return {
        "support": support,
        "resistance": resistance,
        "trade_levels": trade_levels,
        "heatmap": heatmap,
    }, warnings


def _phase_name(phase: Any) -> str | None:
    """Return a phase label from common phase record shapes."""
    if isinstance(phase, dict):
        return phase.get("phase_name") or phase.get("phase")
    if _present(phase):
        return str(phase)
    return None


def _compact_phase_context(phases: Any) -> dict[str, Any] | None:
    """Return compact current/recent phase context from report JSON phase data."""
    phase_list = _as_list(phases)
    phase_list = [item for item in phase_list if _present(_phase_name(item))]
    if not phase_list:
        return None

    latest = phase_list[-1]
    if isinstance(latest, dict):
        current_phase = latest.get("phase")
        current_phase_name = latest.get("phase_name") or current_phase
    else:
        current_phase = str(latest)
        current_phase_name = str(latest)

    recent_phase_names = [
        name
        for name in (_phase_name(item) for item in phase_list[-5:])
        if _present(name)
    ]
    return {
        "current_phase": current_phase,
        "current_phase_name": current_phase_name,
        "recent_phase_names": recent_phase_names,
    }


def _compact_wyckoff_event(timeframe: str | None, event: Any) -> dict[str, Any] | None:
    """Normalize one Wyckoff event record."""
    if isinstance(event, dict):
        event_value = event.get("event") or event.get("wyckoff_event")
        event_name = event.get("event_name") or event.get("wyckoff_confirmed_event")
        if not _present(event_value) and not _present(event_name):
            return None
        return {
            "timeframe": timeframe,
            "timestamp": event.get("timestamp"),
            "event": event_value,
            "event_name": event_name,
            "price": _to_float(event.get("price") or event.get("close")),
            "volume": _to_float(event.get("volume")),
        }

    if not _present(event):
        return None
    return {
        "timeframe": timeframe,
        "timestamp": None,
        "event": str(event),
        "event_name": None,
        "price": None,
        "volume": None,
    }


def _compact_wyckoff_events(timeframe: str | None, events: Any, max_items: int = 20) -> list[dict[str, Any]]:
    """Return compact recent Wyckoff events."""
    compact: list[dict[str, Any]] = []
    for event in _as_list(events)[-max_items:]:
        normalized = _compact_wyckoff_event(timeframe, event)
        if normalized:
            compact.append(normalized)
    return compact


def _compact_trading_ranges(timeframe: str | None, ranges: Any, max_items: int = 10) -> list[dict[str, Any]]:
    """Return compact Wyckoff trading range records."""
    compact: list[dict[str, Any]] = []
    for item in _as_list(ranges)[-max_items:]:
        if not isinstance(item, dict):
            continue
        compact.append(
            {
                "timeframe": timeframe,
                "support": _to_float(item.get("support")),
                "resistance": _to_float(item.get("resistance")),
                "context": item.get("context"),
                "start_timestamp": item.get("start_timestamp"),
                "end_timestamp": item.get("end_timestamp"),
            }
        )
    return compact


def _annotated_data_metadata(data: Any) -> dict[str, Any] | None:
    """Return metadata for report JSON annotated data without carrying all rows."""
    if not isinstance(data, dict):
        return None
    columns = data.get("columns") if isinstance(data.get("columns"), list) else []
    rows = data.get("data") if isinstance(data.get("data"), list) else []
    index = data.get("index") if isinstance(data.get("index"), list) else []
    return {
        "columns": columns,
        "row_count": len(rows) or len(index),
        "latest_timestamp": index[-1] if index else None,
    }


def load_wyckoff_context_from_csv(csv_path: str | None, max_events: int = 20) -> dict[str, Any]:
    """
    Load compact Wyckoff context from an annotated CSV.
    Return empty/default context if missing or malformed.
    """
    empty = {
        "available": False,
        "phase": None,
        "recent_phase_names": [],
        "events": [],
        "confirmed_events": [],
        "tr_low": None,
        "tr_high": None,
        "warnings": [],
    }
    if not csv_path:
        return empty

    path = Path(str(csv_path))
    if not path.exists() or not path.is_file():
        return empty

    columns = {
        "timestamp",
        "wyckoff_event",
        "wyckoff_phase",
        "wyckoff_confirmed_event",
        "wyckoff_confidence",
        "wyckoff_reasons",
        "tr_low",
        "tr_high",
        "price",
        "close",
        "volume",
    }
    try:
        dataframe = pd.read_csv(path, usecols=lambda column: column in columns)
    except Exception as exc:
        result = dict(empty)
        result["warnings"] = [f"Could not load Wyckoff CSV context: {type(exc).__name__}: {exc}"]
        return result

    if dataframe.empty:
        return empty

    result = dict(empty)
    result["available"] = True

    if "wyckoff_phase" in dataframe.columns:
        phases = dataframe["wyckoff_phase"].dropna().astype(str).str.strip()
        phases = phases[phases.ne("") & phases.str.lower().ne("nan")]
        if not phases.empty:
            result["phase"] = phases.iloc[-1]
            result["recent_phase_names"] = phases.tail(5).tolist()

    def event_rows(column: str) -> list[dict[str, Any]]:
        if column not in dataframe.columns:
            return []
        series = dataframe[column].dropna().astype(str).str.strip()
        series = series[series.ne("") & series.str.lower().ne("nan")]
        rows: list[dict[str, Any]] = []
        for index in series.tail(max_events).index:
            row = dataframe.loc[index]
            rows.append(
                {
                    "timestamp": row.get("timestamp"),
                    "event": row.get(column),
                    "event_name": row.get(column),
                    "price": _to_float(row.get("close") if "close" in row else row.get("price")),
                    "volume": _to_float(row.get("volume")),
                    "confidence": _to_float(row.get("wyckoff_confidence")),
                    "reasons": row.get("wyckoff_reasons"),
                }
            )
        return rows

    result["events"] = event_rows("wyckoff_event")
    result["confirmed_events"] = event_rows("wyckoff_confirmed_event")

    for key in ("tr_low", "tr_high"):
        if key in dataframe.columns:
            values = pd.to_numeric(dataframe[key], errors="coerce").dropna()
            if not values.empty:
                result[key] = float(values.iloc[-1])

    return result


def _build_selected_timeframe_context(
    selected_tf: str | None,
    phases: dict[str, Any],
    events: list[dict[str, Any]],
    csv_context: dict[str, Any],
) -> dict[str, Any] | None:
    """Build selected timeframe context from report JSON plus selected CSV supplement."""
    if not selected_tf and not csv_context.get("available"):
        return None

    tf = str(selected_tf) if selected_tf else "selected_csv"
    phase_context = phases.get(tf) if isinstance(phases.get(tf), dict) else {}
    recent_events = [event for event in events if event.get("timeframe") == tf][-10:]
    confirmed_events = [
        {"timeframe": tf, **event}
        for event in (csv_context.get("confirmed_events") or [])[-10:]
        if isinstance(event, dict)
    ]
    phase = phase_context.get("current_phase_name") or phase_context.get("current_phase") or csv_context.get("phase")

    if not phase and not recent_events and not confirmed_events and not csv_context.get("available"):
        return None

    return {
        "tf": tf,
        "phase": phase,
        "recent_events": recent_events,
        "confirmed_events": confirmed_events,
        "tr_low": csv_context.get("tr_low"),
        "tr_high": csv_context.get("tr_high"),
    }


def _extract_wyckoff_vpa(
    report_json: dict[str, Any] | None,
    csv_context: dict[str, Any] | None = None,
    selected_tf: str | None = None,
) -> dict[str, Any]:
    """Extract Wyckoff phase/event context across timeframes."""
    phases: dict[str, Any] = {}
    events: list[dict[str, Any]] = []
    confirmed_events: list[dict[str, Any]] = []
    trading_ranges: list[dict[str, Any]] = []
    annotated_data: dict[str, Any] = {}
    warnings: list[str] = []
    csv_context = csv_context or {}

    for timeframe, data in _timeframe_source(report_json).items():
        if not isinstance(data, dict):
            continue
        tf = str(timeframe)
        wyckoff = data.get("wyckoff") if isinstance(data.get("wyckoff"), dict) else {}
        phase_context = _compact_phase_context(data.get("wyckoff_phases") or wyckoff.get("phases"))
        if phase_context:
            phases[tf] = phase_context
        events.extend(_compact_wyckoff_events(tf, data.get("wyckoff_events") or wyckoff.get("events")))
        trading_ranges.extend(_compact_trading_ranges(tf, data.get("wyckoff_trading_ranges")))
        metadata = _annotated_data_metadata(data.get("wyckoff_annotated_data"))
        if metadata:
            annotated_data[tf] = metadata

    if csv_context.get("available"):
        tf = str(selected_tf) if selected_tf else "selected_csv"
        if tf not in phases and csv_context.get("phase"):
            phases[tf] = {
                "current_phase": csv_context.get("phase"),
                "current_phase_name": csv_context.get("phase"),
                "recent_phase_names": csv_context.get("recent_phase_names") or [],
            }
        for event in csv_context.get("events") or []:
            if isinstance(event, dict):
                events.append({"timeframe": tf, **event})
        for event in csv_context.get("confirmed_events") or []:
            if isinstance(event, dict):
                confirmed_events.append({"timeframe": tf, **event})

    selected_context = _build_selected_timeframe_context(selected_tf, phases, events, csv_context)

    if not phases:
        warnings.append("No Wyckoff phase data found in report JSON or selected CSV.")
    if not events and not confirmed_events:
        warnings.append("No Wyckoff event data found in report JSON or selected CSV.")

    return {
        "phases": phases,
        "events": events,
        "confirmed_events": confirmed_events,
        "trading_ranges": trading_ranges,
        "annotated_data": annotated_data,
        "selected_timeframe_context": selected_context,
        "csv_context_available": bool(csv_context.get("available")),
        "warnings": warnings,
    }


def _normalize_strategy_candidate(candidate: dict[str, Any] | None) -> dict[str, Any] | None:
    """Normalize strategy candidate fields for analyst context."""
    if not isinstance(candidate, dict):
        return None
    close = _to_float(candidate.get("close") if candidate.get("close") is not None else candidate.get("entry"))
    return {
        "ticker": candidate.get("ticker"),
        "tf": candidate.get("tf"),
        "csv": candidate.get("csv"),
        "close": close,
        "entry": close,
        "trade_direction": "long",
        "stop_loss": _to_float(candidate.get("sl") if candidate.get("sl") is not None else candidate.get("stop_loss")),
        "take_profit": _to_float(candidate.get("tp") if candidate.get("tp") is not None else candidate.get("take_profit")),
        "rr": _to_float(candidate.get("rr")),
        "pop": _to_float(candidate.get("pop")),
        "phase": candidate.get("phase"),
        "event": candidate.get("event"),
        "trend": candidate.get("trend"),
        "score": _to_float(candidate.get("score")),
    }


def _extract_monte_carlo(monte_carlo_result: dict[str, Any] | None) -> dict[str, Any] | None:
    """Extract Monte Carlo metrics from either UI wrapper or raw simulator result."""
    if not isinstance(monte_carlo_result, dict):
        return None

    wrapper = monte_carlo_result if "result" in monte_carlo_result else {}
    raw = wrapper.get("result") if isinstance(wrapper.get("result"), dict) else monte_carlo_result
    params = raw.get("params") if isinstance(raw.get("params"), dict) else {}
    metrics = raw.get("metrics_from_entry") or raw.get("metrics_from_now") or {}
    spot = raw.get("spot") if isinstance(raw.get("spot"), dict) else {}
    calibration = raw.get("calibration") if isinstance(raw.get("calibration"), dict) else {}

    return {
        "csv": wrapper.get("csv_path") or raw.get("csv"),
        "tf": wrapper.get("timeframe") or raw.get("tf"),
        "model": params.get("model"),
        "paths": _to_float(params.get("paths")),
        "horizon_bars": _to_float(params.get("horizon_bars")),
        "entry": _to_float(params.get("entry")),
        "stop_loss": _to_float(params.get("sl")),
        "take_profit": _to_float(params.get("tp")),
        "spot_s0": _to_float(spot.get("S0_now")),
        "pop_tp_first": _to_float(metrics.get("pop_tp_first")),
        "p_sl_first": _to_float(metrics.get("p_sl_first")),
        "p_neither": _to_float(metrics.get("p_neither")),
        "t_hit_tp_median": _to_float(metrics.get("t_hit_tp_median")),
        "t_hit_sl_median": _to_float(metrics.get("t_hit_sl_median")),
        "r_mean": _to_float(metrics.get("R_mean") or metrics.get("r_mean")),
        "model_used": calibration.get("model_used"),
        "output_files": wrapper.get("output_files") or [],
        "trade_plan": wrapper.get("trade_plan"),
        "alignment": wrapper.get("alignment"),
        "matches_strategy_candidate": wrapper.get("matches_strategy_candidate"),
        "manual_scenario": wrapper.get("manual_scenario"),
    }


def _risk_reward(entry: float | None, stop_loss: float | None, take_profit: float | None) -> float | None:
    """Compute long-side risk/reward from trade levels."""
    if entry is None or stop_loss is None or take_profit is None:
        return None
    risk = entry - stop_loss
    if risk <= 0:
        return None
    return (take_profit - entry) / risk


def _build_strategy_trade_plan(
    strategy_candidate: dict[str, Any] | None,
    monte_carlo: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build selected strategy/MC trade plan levels for packet clarity."""
    entry = _to_float((strategy_candidate or {}).get("entry") or (strategy_candidate or {}).get("close"))
    stop_loss = _to_float((strategy_candidate or {}).get("stop_loss"))
    take_profit = _to_float((strategy_candidate or {}).get("take_profit"))
    risk_reward = _to_float((strategy_candidate or {}).get("rr"))
    source = "strategy_candidate" if strategy_candidate else None

    if entry is None:
        entry = _to_float((monte_carlo or {}).get("entry"))
        source = source or ("monte_carlo" if entry is not None else None)
    if stop_loss is None:
        stop_loss = _to_float((monte_carlo or {}).get("stop_loss"))
        source = source or ("monte_carlo" if stop_loss is not None else None)
    if take_profit is None:
        take_profit = _to_float((monte_carlo or {}).get("take_profit"))
        source = source or ("monte_carlo" if take_profit is not None else None)
    if risk_reward is None:
        risk_reward = _risk_reward(entry, stop_loss, take_profit)

    return {
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_reward": risk_reward,
        "source": source,
    }


def _build_go_no_go(
    profile: dict[str, Any],
    strategy_candidate: dict[str, Any] | None,
    monte_carlo: dict[str, Any] | None,
    pnf: dict[str, Any],
    warnings: list[str],
) -> dict[str, Any]:
    """Build basic decision-support labels without issuing recommendations."""
    pop = _to_float((monte_carlo or {}).get("pop_tp_first"))
    if pop is None:
        pop = _to_float((strategy_candidate or {}).get("pop"))
    main_threshold = _to_float(profile.get("main_pop_threshold")) or 0.52
    backup_threshold = _to_float(profile.get("backup_pop_threshold")) or 0.45
    score = _to_float((strategy_candidate or {}).get("score"))
    min_score = _to_float(profile.get("min_composite_score")) or 70
    notes: list[str] = []

    if pop is None:
        pop_gate = "unknown"
        notes.append("POP gate unknown because Monte Carlo or candidate POP is unavailable.")
    elif pop >= main_threshold:
        pop_gate = "pass"
    elif pop >= backup_threshold:
        pop_gate = "backup_pass"
        notes.append("POP meets backup threshold but not the main threshold.")
    else:
        pop_gate = "fail"
        notes.append("POP is below configured thresholds.")

    pnf_records = pnf.get("sidecars") if isinstance(pnf, dict) else []
    selected_pnf = pnf.get("selected_sidecar") if isinstance(pnf, dict) else None
    gate_pnf = selected_pnf
    gate_pnf_r = _to_float(gate_pnf.get("objective_r_multiple")) if isinstance(gate_pnf, dict) else None
    pnf_interpretation = pnf.get("objective_interpretation") if isinstance(pnf, dict) else {}
    if not isinstance(pnf_interpretation, dict):
        pnf_interpretation = {}
    objective_direction = pnf_interpretation.get("objective_direction") or (
        gate_pnf.get("objective_direction") if isinstance(gate_pnf, dict) else None
    )
    objective_supports_trade = pnf_interpretation.get("objective_supports_trade")
    objective_quality = pnf_interpretation.get("objective_quality") or (
        gate_pnf.get("objective_quality") if isinstance(gate_pnf, dict) else None
    )
    min_pnf_objective_r = _profile_min_pnf_objective_r(profile)

    if not pnf_records:
        pnf_gate = "pending"
        notes.append("No P&F sidecars found; P&F gate remains pending.")
    elif isinstance(strategy_candidate, dict) and not isinstance(selected_pnf, dict):
        pnf_gate = "unknown"
        notes.append("P&F sidecars found, but no sidecar matched the selected candidate.")
    elif isinstance(strategy_candidate, dict) and objective_direction == "downside":
        pnf_gate = "fail"
        notes.append("Selected P&F sidecar objective contradicts the selected long setup.")
    elif isinstance(strategy_candidate, dict) and objective_direction in (None, "unknown"):
        pnf_gate = "unknown"
        notes.append("Selected P&F sidecar objective direction is unknown.")
    elif isinstance(strategy_candidate, dict) and objective_supports_trade is False:
        pnf_gate = "fail"
        notes.append("Selected P&F sidecar objective does not support the selected long setup.")
    elif gate_pnf_r is None:
        pnf_gate = "unknown"
        notes.append("P&F sidecars found, but selected objective R could not be computed.")
    elif gate_pnf_r < 0:
        pnf_gate = "fail"
        notes.append("Selected P&F sidecar objective R is negative.")
    elif gate_pnf_r >= min_pnf_objective_r:
        pnf_gate = "pass"
        if isinstance(strategy_candidate, dict):
            notes.append("Selected P&F sidecar objective meets configured R threshold.")
        else:
            notes.append("P&F objective meets configured R threshold.")
    else:
        pnf_gate = "fail"
        if isinstance(strategy_candidate, dict):
            notes.append("Selected P&F sidecar objective is below configured R threshold.")
        else:
            notes.append("P&F objective is below configured R threshold.")

    if objective_quality == "risk":
        notes.append("Selected P&F objective quality is risk.")
    if objective_quality == "weak":
        notes.append("Selected P&F objective quality is weak.")

    if pop_gate == "unknown" and score is None:
        risk_rank = None
    elif pop_gate == "pass" and score is not None and score >= min_score and not warnings:
        risk_rank = 1
    elif pop_gate in {"pass", "backup_pass", "unknown"}:
        risk_rank = 2
    else:
        risk_rank = 3

    return {
        "pop_gate": pop_gate,
        "pnf_gate": pnf_gate,
        "composite_score": score,
        "risk_rank": risk_rank,
        "notes": notes,
    }


def _build_analyst_sections(
    market_snapshot: dict[str, Any],
    summary_text: str | None,
    levels: dict[str, Any],
    wyckoff_vpa: dict[str, Any],
    strategy_candidate: dict[str, Any] | None,
    strategy_trade_plan: dict[str, Any],
    monte_carlo: dict[str, Any] | None,
    pnf: dict[str, Any],
    go_no_go: dict[str, Any],
) -> dict[str, Any]:
    """Build structured bridge sections for a future analyst prompt."""
    best_pnf = pnf.get("best_objective") if isinstance(pnf, dict) else None
    pnf_objective_present = any(
        _to_float(record.get("objective")) is not None
        for record in (pnf.get("sidecars") if isinstance(pnf, dict) else []) or []
        if isinstance(record, dict)
    )
    wyckoff_events_present = bool(wyckoff_vpa.get("events") or wyckoff_vpa.get("confirmed_events"))
    return {
        "statistical_analysis": {
            "market_snapshot": market_snapshot,
            "strategy_candidate": strategy_candidate,
            "strategy_trade_plan": strategy_trade_plan,
            "monte_carlo": monte_carlo,
            "pnf": pnf,
            "go_no_go": go_no_go,
        },
        "narrative_inputs": {
            "summary_text_preview": (summary_text or "")[:4000] if summary_text else None,
            "signal_type": market_snapshot.get("signal_type"),
            "signal_strength": market_snapshot.get("signal_strength"),
        },
        "annotations_checklist": [
            {"item": "Report JSON loaded", "available": market_snapshot.get("current_price") is not None},
            {"item": "Wyckoff phases present", "available": bool(wyckoff_vpa.get("phases"))},
            {"item": "Wyckoff events present", "available": wyckoff_events_present},
            {"item": "Support/resistance levels present", "available": bool(levels.get("support") or levels.get("resistance"))},
            {"item": "Strategy candidate present", "available": strategy_candidate is not None},
            {"item": "Monte Carlo metrics present", "available": monte_carlo is not None},
            {"item": "P&F objective present", "available": pnf_objective_present},
        ],
        "levels_heatmap": levels,
        "final_summary_inputs": {
            "go_no_go": go_no_go,
            "pnf_gate": go_no_go.get("pnf_gate"),
            "best_pnf_objective": best_pnf,
            "report_baseline_risk": market_snapshot.get("report_baseline_risk") or market_snapshot.get("risk"),
            "strategy_trade_plan": strategy_trade_plan,
            "selected_timeframe_context": wyckoff_vpa.get("selected_timeframe_context"),
            "risk": market_snapshot.get("risk"),
            "key_warnings": wyckoff_vpa.get("warnings", []),
        },
    }


def _missing_data_messages(missing_keys: list[str]) -> list[str]:
    """Convert internal missing-data keys into user-facing messages."""
    messages = {
        "report_json": "No report JSON available. Load or run a report first for full market context.",
        "summary_text": "No summary text available. Narrative inputs will be limited.",
        "strategy_candidate": "No strategy candidate selected. Use Strategy Ranking first if trade setup context is required.",
        "monte_carlo": "No Monte Carlo result available. Run Monte Carlo first if POP metrics are required.",
        "timeframes": "No timeframe analysis found in the report JSON.",
        "market_snapshot.current_price": "No current price found in report JSON.",
        "market_snapshot.signal_type": "No signal type found in report JSON.",
        "market_snapshot.signal_strength": "No signal strength found in report JSON.",
        "market_snapshot.stop_loss": "No stop loss found in report JSON.",
        "market_snapshot.take_profit": "No take profit found in report JSON.",
        "market_snapshot.risk_reward": "No risk/reward ratio found in report JSON.",
    }
    return [messages.get(key, key) for key in sorted(set(missing_keys))]


def _build_packet_summary(
    ticker: str | None,
    market_snapshot: dict[str, Any],
    normalized_candidate: dict[str, Any] | None,
    strategy_trade_plan: dict[str, Any],
    monte_carlo: dict[str, Any] | None,
    go_no_go: dict[str, Any],
    pnf: dict[str, Any],
    wyckoff_vpa: dict[str, Any],
    report_json: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build compact top-level packet status for UI and future analyst flows."""
    candidate_available = normalized_candidate is not None
    monte_carlo_available = monte_carlo is not None
    report_context_available = isinstance(report_json, dict)
    best_pnf = pnf.get("best_objective") if isinstance(pnf, dict) else None
    pnf_interpretation = pnf.get("objective_interpretation") if isinstance(pnf, dict) else {}
    if not isinstance(pnf_interpretation, dict):
        pnf_interpretation = {}
    selected_context = wyckoff_vpa.get("selected_timeframe_context") if isinstance(wyckoff_vpa, dict) else None
    return {
        "ticker": ticker,
        "current_price": market_snapshot.get("current_price"),
        "trade_entry": strategy_trade_plan.get("entry") if isinstance(strategy_trade_plan, dict) else None,
        "trade_stop_loss": strategy_trade_plan.get("stop_loss") if isinstance(strategy_trade_plan, dict) else None,
        "trade_take_profit": strategy_trade_plan.get("take_profit") if isinstance(strategy_trade_plan, dict) else None,
        "trade_risk_reward": strategy_trade_plan.get("risk_reward") if isinstance(strategy_trade_plan, dict) else None,
        "candidate_available": candidate_available,
        "monte_carlo_available": monte_carlo_available,
        "pop_gate": go_no_go.get("pop_gate"),
        "pnf_available": bool((pnf or {}).get("available")) if isinstance(pnf, dict) else False,
        "pnf_gate": go_no_go.get("pnf_gate"),
        "best_pnf_objective": best_pnf.get("objective") if isinstance(best_pnf, dict) else None,
        "best_pnf_objective_r": best_pnf.get("objective_r_multiple") if isinstance(best_pnf, dict) else None,
        "pnf_objective_direction": pnf_interpretation.get("objective_direction"),
        "pnf_objective_quality": pnf_interpretation.get("objective_quality"),
        "pnf_objective_supports_trade": pnf_interpretation.get("objective_supports_trade"),
        "wyckoff_events_available": bool((wyckoff_vpa or {}).get("events") or (wyckoff_vpa or {}).get("confirmed_events")),
        "wyckoff_phases_available": bool((wyckoff_vpa or {}).get("phases")),
        "selected_timeframe": (selected_context or {}).get("tf") if isinstance(selected_context, dict) else (
            normalized_candidate.get("tf") if isinstance(normalized_candidate, dict) else None
        ),
        "risk_rank": go_no_go.get("risk_rank"),
        "ready_for_analyst": bool(
            report_context_available and candidate_available and monte_carlo_available
        ),
    }


def build_analyst_packet(
    ticker: str,
    report_json: dict[str, Any] | None = None,
    summary_text: str | None = None,
    report_dir: str | None = None,
    strategy_candidate: dict[str, Any] | None = None,
    monte_carlo_result: dict[str, Any] | None = None,
    profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build a compact, structured packet for the Wyckoff Volume Analyst.

    This does not make trading decisions automatically. It organizes
    observations, decision-support metrics, risk context, and missing-data
    warnings for a future analyst workflow.
    """
    missing_data: list[str] = []
    warnings: list[str] = []
    clean_profile = profile or load_default_analyst_profile()
    inferred_ticker = (
        (strategy_candidate or {}).get("ticker")
        or ticker
        or _first_value(report_json, [["ticker"]])
    )
    market_snapshot = _extract_market_snapshot(report_json, missing_data)
    timeframes = _extract_timeframes(report_json)
    if not timeframes:
        missing_data.append("timeframes")

    normalized_candidate = _normalize_strategy_candidate(strategy_candidate)
    monte_carlo = _extract_monte_carlo(monte_carlo_result)
    if isinstance(monte_carlo, dict):
        if monte_carlo.get("manual_scenario"):
            warnings.append("Monte Carlo result was included as an explicit manual scenario and does not match the selected Strategy Ranking candidate.")
        elif monte_carlo.get("matches_strategy_candidate") is False:
            warnings.append("Monte Carlo result does not match the selected Strategy Ranking candidate.")
    strategy_trade_plan = _build_strategy_trade_plan(normalized_candidate, monte_carlo)
    levels, level_warnings = _extract_levels(
        report_json,
        market_snapshot.get("current_price"),
        normalized_candidate,
    )
    warnings.extend(level_warnings)
    csv_context = load_wyckoff_context_from_csv(
        normalized_candidate.get("csv") if isinstance(normalized_candidate, dict) else None
    )
    wyckoff_vpa = _extract_wyckoff_vpa(
        report_json,
        csv_context=csv_context,
        selected_tf=normalized_candidate.get("tf") if isinstance(normalized_candidate, dict) else None,
    )
    warnings.extend(wyckoff_vpa.get("warnings", []))
    pnf_records = _attach_pnf_objective_interpretation(
        _attach_pnf_objective_r(load_pnf_sidecars(report_dir), normalized_candidate),
        normalized_candidate,
        clean_profile,
    )
    pnf = _build_pnf_section(pnf_records, normalized_candidate, monte_carlo)
    if not pnf.get("available"):
        warnings.append("No P&F data included yet; P&F gate remains pending.")
    warnings.extend(pnf.get("warnings") or [])

    go_no_go = _build_go_no_go(clean_profile, normalized_candidate, monte_carlo, pnf, warnings)
    pnf["gate"] = go_no_go.get("pnf_gate")
    existing_pnf_notes = pnf.get("notes") or []
    pnf["notes"] = [
        *existing_pnf_notes,
        *[
            note
            for note in go_no_go.get("notes", [])
            if note.startswith("P&F") or note.startswith("No P&F") or note.startswith("Selected P&F")
        ],
    ]
    packet_summary = _build_packet_summary(
        inferred_ticker,
        market_snapshot,
        normalized_candidate,
        strategy_trade_plan,
        monte_carlo,
        go_no_go,
        pnf,
        wyckoff_vpa,
        report_json,
    )

    if not isinstance(report_json, dict):
        missing_data.append("report_json")
    if not summary_text:
        missing_data.append("summary_text")
    if normalized_candidate is None:
        missing_data.append("strategy_candidate")
    if monte_carlo is None:
        missing_data.append("monte_carlo")

    analyst_sections = _build_analyst_sections(
        market_snapshot,
        summary_text,
        levels,
        wyckoff_vpa,
        normalized_candidate,
        strategy_trade_plan,
        monte_carlo,
        pnf,
        go_no_go,
    )

    packet = {
        "packet_version": PACKET_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "ticker": inferred_ticker,
        "packet_summary": packet_summary,
        "profile": clean_profile,
        "source_files": {
            "report_dir": report_dir,
            "report_json_available": isinstance(report_json, dict),
            "summary_text_available": bool(summary_text),
            "strategy_candidate_available": normalized_candidate is not None,
            "monte_carlo_available": monte_carlo is not None,
            "pnf_sidecars_available": bool(pnf_records),
            "pnf_sidecar_count": len(pnf_records),
        },
        "market_snapshot": market_snapshot,
        "timeframes": timeframes,
        "strategy_candidate": normalized_candidate,
        "strategy_trade_plan": strategy_trade_plan,
        "report_baseline_risk": market_snapshot.get("report_baseline_risk") or market_snapshot.get("risk"),
        "monte_carlo": monte_carlo,
        "pnf": pnf,
        "levels": levels,
        "wyckoff_vpa": wyckoff_vpa,
        "selected_timeframe_context": wyckoff_vpa.get("selected_timeframe_context"),
        "go_no_go": go_no_go,
        "analyst_sections": analyst_sections,
        "missing_data": _missing_data_messages(missing_data),
        "warnings": sorted(set(warnings)),
    }
    return _json_safe(packet)


def _json_safe(value: Any) -> Any:
    """Convert common Python/data-science values into JSON-safe objects."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if hasattr(value, "item"):
        try:
            return _json_safe(value.item())
        except Exception:
            pass
    if hasattr(value, "tolist"):
        try:
            return _json_safe(value.tolist())
        except Exception:
            pass
    return str(value)


def packet_to_pretty_json(packet: dict[str, Any]) -> str:
    """
    Return a pretty JSON string using safe serialization.

    Handles common non-JSON values by converting them to strings, floats, or
    nulls through the same sanitizer used by the packet builder.
    """
    return json.dumps(_json_safe(packet), indent=2, sort_keys=True, ensure_ascii=False)
