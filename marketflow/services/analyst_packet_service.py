"""Build structured context packets for a future Wyckoff Volume Analyst."""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKET_VERSION = "0.1"
PROFILE_PATH = Path(__file__).resolve().parents[1] / "config" / "analyst_profile.example.json"


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
    timeframe_value = _first_pnf_value(data, ("timeframe", "tf", "interval"))
    direction_value = _first_pnf_value(data, ("direction", "count_direction", "trend"))
    last_price = _first_pnf_float(data, ("last_price", "spot", "current_price", "close"))
    objective = _first_pnf_float(data, ("objective", "objective_price", "target", "target_price"))

    distance_to_objective = None
    distance_to_objective_pct = None
    if last_price is not None and last_price != 0 and objective is not None:
        distance_to_objective = objective - last_price
        distance_to_objective_pct = distance_to_objective / last_price * 100

    return {
        "path": str(sidecar_path),
        "filename": sidecar_path.name,
        "timeframe": str(timeframe_value) if timeframe_value is not None else None,
        "direction": str(direction_value) if direction_value is not None else None,
        "box_pct": _first_pnf_float(data, ("box_pct", "box_percent")),
        "box_size": _first_pnf_float(data, ("box_size", "box")),
        "reversal": _pnf_int(_first_pnf_value(data, ("reversal", "rev"))),
        "last_price": last_price,
        "breakout_level": _first_pnf_float(data, ("breakout", "breakout_level", "break_level", "breakout_price")),
        "objective": objective,
        "objective_r_multiple": None,
        "distance_to_objective": distance_to_objective,
        "distance_to_objective_pct": distance_to_objective_pct,
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
    gate: str = "pending",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    """Build the packet P&F section."""
    return {
        "available": bool(records),
        "sidecars": records,
        "best_objective": _best_pnf_objective(records),
        "gate": gate,
        "notes": notes or [],
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


def _extract_wyckoff_vpa(report_json: dict[str, Any] | None) -> dict[str, Any]:
    """Extract Wyckoff phase/event context across timeframes."""
    phases: dict[str, Any] = {}
    events: list[dict[str, Any]] = []
    warnings: list[str] = []

    for timeframe, data in _timeframe_source(report_json).items():
        wyckoff = data.get("wyckoff") if isinstance(data, dict) else None
        if not isinstance(wyckoff, dict):
            continue
        phases[str(timeframe)] = _compact_phases(wyckoff.get("phases"))
        for event in _compact_events(wyckoff.get("events")):
            events.append({"timeframe": str(timeframe), "event": event})

    if not phases:
        warnings.append("No Wyckoff phase data found in report JSON.")
    if not events:
        warnings.append("No Wyckoff event data found in report JSON.")

    return {"phases": phases, "events": events, "warnings": warnings}


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
    best_pnf = pnf.get("best_objective") if isinstance(pnf, dict) else None
    best_pnf_r = _to_float(best_pnf.get("objective_r_multiple")) if isinstance(best_pnf, dict) else None
    min_pnf_objective_r = _to_float(profile.get("min_pnf_objective_r")) or 1.5

    if not pnf_records:
        pnf_gate = "pending"
        notes.append("No P&F sidecars found; P&F gate remains pending.")
    elif best_pnf_r is None:
        pnf_gate = "unknown"
        notes.append("P&F sidecars found, but objective R could not be computed.")
    elif best_pnf_r >= min_pnf_objective_r:
        pnf_gate = "pass"
        notes.append("P&F objective meets configured R threshold.")
    else:
        pnf_gate = "fail"
        notes.append("P&F objective is below configured R threshold.")

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
    return {
        "statistical_analysis": {
            "market_snapshot": market_snapshot,
            "strategy_candidate": strategy_candidate,
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
            {"item": "Wyckoff events present", "available": bool(wyckoff_vpa.get("events"))},
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
    monte_carlo: dict[str, Any] | None,
    go_no_go: dict[str, Any],
    pnf: dict[str, Any],
    report_json: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build compact top-level packet status for UI and future analyst flows."""
    candidate_available = normalized_candidate is not None
    monte_carlo_available = monte_carlo is not None
    report_context_available = isinstance(report_json, dict)
    best_pnf = pnf.get("best_objective") if isinstance(pnf, dict) else None
    return {
        "ticker": ticker,
        "current_price": market_snapshot.get("current_price"),
        "candidate_available": candidate_available,
        "monte_carlo_available": monte_carlo_available,
        "pop_gate": go_no_go.get("pop_gate"),
        "pnf_available": bool((pnf or {}).get("available")) if isinstance(pnf, dict) else False,
        "pnf_gate": go_no_go.get("pnf_gate"),
        "best_pnf_objective": best_pnf.get("objective") if isinstance(best_pnf, dict) else None,
        "best_pnf_objective_r": best_pnf.get("objective_r_multiple") if isinstance(best_pnf, dict) else None,
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
    levels, level_warnings = _extract_levels(
        report_json,
        market_snapshot.get("current_price"),
        normalized_candidate,
    )
    warnings.extend(level_warnings)
    wyckoff_vpa = _extract_wyckoff_vpa(report_json)
    warnings.extend(wyckoff_vpa.get("warnings", []))
    pnf_records = _attach_pnf_objective_r(load_pnf_sidecars(report_dir), normalized_candidate)
    pnf = _build_pnf_section(pnf_records)
    if not pnf.get("available"):
        warnings.append("No P&F data included yet; P&F gate remains pending.")

    go_no_go = _build_go_no_go(clean_profile, normalized_candidate, monte_carlo, pnf, warnings)
    pnf["gate"] = go_no_go.get("pnf_gate")
    pnf["notes"] = [
        note
        for note in go_no_go.get("notes", [])
        if note.startswith("P&F") or note.startswith("No P&F")
    ]
    packet_summary = _build_packet_summary(
        inferred_ticker,
        market_snapshot,
        normalized_candidate,
        monte_carlo,
        go_no_go,
        pnf,
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
        "monte_carlo": monte_carlo,
        "pnf": pnf,
        "levels": levels,
        "wyckoff_vpa": wyckoff_vpa,
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
