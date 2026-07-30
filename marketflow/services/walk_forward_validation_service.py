"""Service-only historical walk-forward validation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4
import math

import pandas as pd

from marketflow.services.parameter_profile_service import (
    build_parameter_context_from_profile,
    get_timeframe_posture,
)
from marketflow.services.backtest_result_service import evaluate_candidate_snapshot_rows
from marketflow.marketflow_strategy import (
    RR_BELOW_MINIMUM,
    RR_GATE_PASSED,
    RR_INVALID_INPUT,
    TARGET_NOT_AVAILABLE,
    _resolve_wyckoff_event,
    _resolve_long_target,
    _rr,
)


WALK_FORWARD_METADATA_VERSION = "walk_forward_validation_v1"

DEFAULT_RISK_REWARD = 1.5
DEFAULT_RISK_FRACTION = 0.02
DEFAULT_TIE_BREAK_POLICY = "conservative"
WALK_FORWARD_SOURCE_STATUS_EXACT_MATCH = "EXACT_MATCH"
WALK_FORWARD_SOURCE_REASON_IDENTITY_MISMATCH = "DATASET_IDENTITY_MISMATCH"
WALK_FORWARD_SOURCE_REASON_IDENTITY_UNKNOWN = "DATASET_IDENTITY_UNKNOWN"

DEFAULT_TIMESTAMP_COLUMNS = (
    "timestamp",
    "datetime",
    "date",
    "time",
    "Date",
    "Datetime",
)

DEFAULT_EVENT_COLUMNS = (
    "wyckoff_confirmed_event",
    "confirmed_wyckoff_event",
    "confirmed_event",
    "wyckoff_event_confirmed",
    "wyckoff_event",
    "event",
    "phase_event",
)

DEFAULT_CONFIRMED_EVENT_COLUMNS = (
    "wyckoff_confirmed_event",
    "confirmed_wyckoff_event",
    "confirmed_event",
    "wyckoff_event_confirmed",
)

DEFAULT_PHASE_COLUMNS = (
    "wyckoff_phase",
    "phase",
)

DEFAULT_TREND_COLUMNS = (
    "trend",
    "trend_label",
)

TIMEFRAME_TOKENS = ("1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m")


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    try:
        is_missing = pd.isna(value)
    except (TypeError, ValueError):
        return False
    if isinstance(is_missing, bool):
        return is_missing
    return False


def _to_int(value: Any) -> int | None:
    if _is_missing(value) or isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed


def _to_float(value: Any) -> float | None:
    if _is_missing(value) or isinstance(value, bool):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def _json_safe_value(value: Any) -> Any:
    if value is None:
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
    if value is None:
        return None
    try:
        is_missing = pd.isna(value)
    except (TypeError, ValueError):
        is_missing = False
    if isinstance(is_missing, bool) and is_missing:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if hasattr(value, "isoformat") and not isinstance(value, (str, bytes, bytearray)):
        try:
            return value.isoformat()
        except (AttributeError, TypeError, ValueError):
            pass
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _json_safe_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {str(key): _json_safe_value(value) for key, value in data.items()}


def detect_walk_forward_timestamp_column(columns: list[str]) -> str | None:
    column_list = list(columns or [])
    for candidate in DEFAULT_TIMESTAMP_COLUMNS:
        if candidate in column_list:
            return candidate
    lower_map = {str(column).strip().lower(): column for column in column_list}
    for candidate in DEFAULT_TIMESTAMP_COLUMNS:
        match = lower_map.get(candidate.lower())
        if match is not None:
            return match
    for column in column_list:
        lowered = str(column).strip().lower()
        if "timestamp" in lowered or lowered in {"datetime", "date", "time"}:
            return column
    return None


def _first_existing_column(columns: list[str], candidates: tuple[str, ...]) -> str | None:
    column_list = list(columns or [])
    for candidate in candidates:
        if candidate in column_list:
            return candidate
    lower_map = {str(column).strip().lower(): column for column in column_list}
    for candidate in candidates:
        match = lower_map.get(candidate.lower())
        if match is not None:
            return match
    return None


def _column_value(row: pd.Series, column: str | None) -> Any:
    if column is None:
        return None
    try:
        if column not in row.index:
            return None
        return row.get(column)
    except AttributeError:
        if isinstance(row, dict):
            return row.get(column)
    return None


def _price_column(columns: list[str], preferred: str) -> str | None:
    normalized = str(preferred or "").strip().lower().replace(" ", "_")
    aliases = {
        "open": ("open", "Open"),
        "high": ("high", "High"),
        "low": ("low", "Low"),
        "close": ("close", "Close", "adj_close", "Adj Close", "adjusted_close"),
    }
    candidates = aliases.get(normalized, (preferred,))
    return _first_existing_column(columns, tuple(str(candidate) for candidate in candidates))


def _extract_ohlc_columns(data: pd.DataFrame) -> dict[str, str | None]:
    columns = [str(column) for column in data.columns]
    return {
        "open": _price_column(columns, "open"),
        "high": _price_column(columns, "high"),
        "low": _price_column(columns, "low"),
        "close": _price_column(columns, "close"),
    }


def infer_walk_forward_ticker_from_csv_name(path: str | Path | None) -> str | None:
    if path is None:
        return None
    stem = Path(str(path)).stem
    if not stem:
        return None
    first = stem.split("_", 1)[0].strip()
    return first.upper() if first else None


def infer_walk_forward_timeframe_from_csv_name(path: str | Path | None) -> str | None:
    if path is None:
        return None
    parts = [part.strip().lower() for part in Path(str(path)).stem.replace("-", "_").replace(".", "_").split("_")]
    for token in TIMEFRAME_TOKENS:
        if token in parts:
            return token
    stem = Path(str(path)).stem.lower()
    for token in TIMEFRAME_TOKENS:
        if f"_{token}_" in f"_{stem}_":
            return token
    return None


def _walk_forward_source_identity(
    path: str | Path,
    ticker: str | None,
    timeframe: str | None,
) -> dict[str, Any]:
    source_ticker = infer_walk_forward_ticker_from_csv_name(path)
    source_timeframe = infer_walk_forward_timeframe_from_csv_name(path)
    requested_ticker = str(ticker).upper() if ticker is not None and str(ticker).strip() else None
    requested_timeframe = str(timeframe).lower() if timeframe is not None and str(timeframe).strip() else None
    errors: list[str] = []

    if requested_ticker and source_ticker and requested_ticker != source_ticker:
        errors.append(WALK_FORWARD_SOURCE_REASON_IDENTITY_MISMATCH)
    if requested_timeframe and source_timeframe and requested_timeframe != source_timeframe:
        errors.append(WALK_FORWARD_SOURCE_REASON_IDENTITY_MISMATCH)
    if not source_ticker:
        errors.append(WALK_FORWARD_SOURCE_REASON_IDENTITY_UNKNOWN)
    if not source_timeframe:
        errors.append(WALK_FORWARD_SOURCE_REASON_IDENTITY_UNKNOWN)

    reason = errors[0] if errors else None
    status = WALK_FORWARD_SOURCE_STATUS_EXACT_MATCH
    if reason == WALK_FORWARD_SOURCE_REASON_IDENTITY_UNKNOWN:
        status = WALK_FORWARD_SOURCE_REASON_IDENTITY_UNKNOWN
    elif reason is not None:
        status = WALK_FORWARD_SOURCE_REASON_IDENTITY_MISMATCH

    return {
        "ticker": source_ticker,
        "timeframe": source_timeframe,
        "source_ticker": source_ticker,
        "source_timeframe": source_timeframe,
        "status": status,
        "reason": reason,
        "errors": errors,
    }


def _minimum_lookback_rows_from_profile(profile_context: dict[str, Any]) -> int:
    parameter_context = profile_context.get("parameter_context") or {}
    values = [
        _to_int(parameter_context.get("minimum_rows_floor")),
        (_to_int(parameter_context.get("eigen_window")) or 0) * 3,
        (_to_int(parameter_context.get("backtest_horizon")) or 0) * 3,
        (_to_int(parameter_context.get("monte_carlo_horizon")) or 0) * 3,
        100,
    ]
    return max(value for value in values if value is not None)


def _profile_horizon(profile_context: dict[str, Any]) -> int | None:
    backtest_context = profile_context.get("backtest_context") or {}
    parameter_context = profile_context.get("parameter_context") or {}
    monte_carlo_context = profile_context.get("monte_carlo_context") or {}
    return (
        _to_int(backtest_context.get("horizon_bars"))
        or _to_int(parameter_context.get("backtest_horizon"))
        or _to_int(monte_carlo_context.get("horizon"))
    )


def _row_matches_event_filters(
    row: pd.Series,
    event_column: str | None,
    event_filters: list[str] | None,
) -> bool:
    if not event_filters:
        return True
    if event_column is None:
        return False
    value = _column_value(row, event_column)
    if _is_missing(value):
        return False
    normalized_value = str(value).strip().upper()
    return normalized_value in {str(item).strip().upper() for item in event_filters if not _is_missing(item)}


def _first_present_row_value(row: pd.Series | dict[str, Any], columns: tuple[str, ...]) -> Any:
    keys = list(row.index) if isinstance(row, pd.Series) else list(row.keys())
    column = _first_existing_column([str(key) for key in keys], columns)
    if isinstance(row, pd.Series):
        return _column_value(row, column)
    if column is None:
        return None
    return row.get(column)


def build_walk_forward_candidate_from_row(
    row: pd.Series | dict[str, Any],
    *,
    csv_path: str | Path,
    signal_row_index: int,
    total_rows: int,
    profile_name: str,
    profile_context: dict[str, Any],
    ticker: str | None = None,
    timeframe: str | None = None,
    timestamp_column: str | None = None,
    ohlc_columns: dict[str, str | None] | None = None,
    event_column: str | None = None,
    phase_column: str | None = None,
    trend_column: str | None = None,
    risk_reward: float = DEFAULT_RISK_REWARD,
    risk_fraction: float = DEFAULT_RISK_FRACTION,
    max_event_age_bars: int | None = None,
    decision_frame: pd.DataFrame | None = None,
    walk_forward_run_id: str | None = None,
) -> dict[str, Any]:
    ohlc = ohlc_columns or {}
    row_series = row if isinstance(row, pd.Series) else pd.Series(row)
    errors: list[str] = []
    run_id = walk_forward_run_id or str(uuid4())
    horizon = _profile_horizon(profile_context)

    close = _to_float(_column_value(row_series, ohlc.get("close")))
    open_price = _to_float(_column_value(row_series, ohlc.get("open")))
    low = _to_float(_column_value(row_series, ohlc.get("low")))
    entry = close if close is not None else open_price
    if entry is None:
        errors.append("missing entry price")

    stop_loss = None
    if entry is not None:
        if low is not None and low < entry:
            stop_loss = low
        else:
            stop_loss = entry * (1 - risk_fraction)
        if stop_loss >= entry:
            stop_loss = entry * (1 - risk_fraction)
        if stop_loss >= entry:
            errors.append("stop_loss is not below entry")

    take_profit = None
    calculated_rr = None
    target_status = TARGET_NOT_AVAILABLE
    target_provenance = None
    target_structural_level_kind = None
    rr_status = RR_INVALID_INPUT
    if entry is not None and stop_loss is not None:
        target_frame = decision_frame if decision_frame is not None else pd.DataFrame([row_series])
        target = _resolve_long_target(target_frame, entry=entry, decision_row_index=len(target_frame) - 1)
        target_status = target.status
        target_provenance = target.provenance
        target_structural_level_kind = target.structural_level_kind
        if not target.success or target.target_price is None:
            rr_status = target.status
            errors.append(target.reason or target.status)
        else:
            take_profit = target.target_price
            calculated_rr = _rr(entry, stop_loss, take_profit)
            minimum_rr = _to_float(risk_reward)
            if minimum_rr is None or minimum_rr <= 0:
                errors.append(RR_INVALID_INPUT)
            elif calculated_rr is None:
                errors.append(RR_INVALID_INPUT)
            elif calculated_rr < minimum_rr:
                rr_status = RR_BELOW_MINIMUM
                errors.append(RR_BELOW_MINIMUM)
            else:
                rr_status = RR_GATE_PASSED

    timestamp = _column_value(row_series, timestamp_column)
    strategy_score = _first_present_row_value(row_series, ("strategy_score", "score"))
    wyckoff_phase = _column_value(row_series, phase_column)
    if _is_missing(wyckoff_phase):
        wyckoff_phase = _first_present_row_value(row_series, DEFAULT_PHASE_COLUMNS)
    wyckoff_event = _column_value(row_series, event_column)
    if _is_missing(wyckoff_event):
        wyckoff_event = _first_present_row_value(row_series, DEFAULT_EVENT_COLUMNS)
    event_frame = decision_frame if decision_frame is not None else pd.DataFrame([row_series])
    event_frame_columns = [str(column) for column in event_frame.columns] if not event_frame.empty else []
    resolved_event_column = (
        event_column
        if event_column in DEFAULT_CONFIRMED_EVENT_COLUMNS
        else _first_existing_column(event_frame_columns, DEFAULT_CONFIRMED_EVENT_COLUMNS)
    )
    event_resolution = _resolve_wyckoff_event(
        event_frame,
        max_event_age_bars,
        decision_row_index=len(event_frame) - 1,
        event_column=resolved_event_column or "wyckoff_confirmed_event",
    )
    resolved_wyckoff_event = event_resolution.event if event_resolution.event is not None else wyckoff_event
    trend = _column_value(row_series, trend_column)
    if _is_missing(trend):
        trend = _first_present_row_value(row_series, DEFAULT_TREND_COLUMNS)
    future_start = signal_row_index + 1
    future_end = min(signal_row_index + horizon, total_rows - 1) if horizon is not None else total_rows - 1

    base = {
        "snapshot_success": not errors,
        "candidate_validation_status": "valid" if not errors else "invalid",
        "candidate_validation_errors": errors,
        "validation_status": "valid" if not errors else "invalid",
        "ticker": ticker or infer_walk_forward_ticker_from_csv_name(csv_path),
        "timeframe": timeframe or infer_walk_forward_timeframe_from_csv_name(csv_path),
        "source_csv": str(csv_path),
        "signal_row_index": int(signal_row_index),
        "signal_timestamp": _json_safe_value(timestamp),
        "signal_timestamp_source": timestamp_column,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_reward": calculated_rr,
        "target_status": target_status,
        "target_provenance": target_provenance,
        "target_structural_level_kind": target_structural_level_kind,
        "rr_status": rr_status,
        "strategy_score": _to_float(strategy_score),
        "wyckoff_phase": _json_safe_value(wyckoff_phase),
        "wyckoff_event": _json_safe_value(resolved_wyckoff_event),
        "event_status": event_resolution.status,
        "event_provenance": event_resolution.provenance,
        "event_age_bars": event_resolution.event_age_bars,
        "event_max_age_bars": event_resolution.max_event_age_bars,
        "event_scoring_eligible": event_resolution.scoring_eligible,
        "event_occurrence_row_index": event_resolution.occurrence_row_index,
        "event_occurrence_timestamp": event_resolution.occurrence_timestamp,
        "event_decision_row_index": event_resolution.decision_row_index,
        "event_superseded_count": event_resolution.superseded_event_count,
        "event_reason": event_resolution.reason,
        "trend": _json_safe_value(trend),
        "wyckoff_event_source": event_column,
        "event_resolution_source": resolved_event_column,
        "wyckoff_phase_source": phase_column,
        "trend_source": trend_column,
        "direction": "long",
        "candidate_source": "walk_forward_validation",
        "profile_name": profile_name,
        "walk_forward_run_id": run_id,
        "walk_forward_case_id": str(uuid4()),
        "walk_forward_metadata_version": WALK_FORWARD_METADATA_VERSION,
        "lookback_rows_available": signal_row_index + 1,
        "future_bars_available": total_rows - signal_row_index - 1,
        "lookback_start_index": 0,
        "lookback_end_index": signal_row_index,
        "future_window_start_index": future_start,
        "future_window_end_index": future_end,
    }
    return _json_safe_dict(base)


def build_walk_forward_cases_from_csv(
    csv_path: str | Path,
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
    include_invalid_cases: bool = False,
    risk_reward: float = DEFAULT_RISK_REWARD,
    risk_fraction: float = DEFAULT_RISK_FRACTION,
    max_event_age_bars: int | None = None,
    walk_forward_run_id: str | None = None,
) -> dict[str, Any]:
    path = Path(csv_path)
    run_id = walk_forward_run_id or str(uuid4())
    warnings: list[str] = []
    errors: list[str] = []
    filters = list(event_filters or [])
    source_identity = _walk_forward_source_identity(path, ticker, timeframe)
    base_result: dict[str, Any] = {
        "success": False,
        "csv_path": str(path),
        "source_csv_name": path.name,
        "ticker": source_identity["ticker"],
        "timeframe": source_identity["timeframe"],
        "source_ticker": source_identity["source_ticker"],
        "source_timeframe": source_identity["source_timeframe"],
        "source_status": source_identity["status"],
        "source_reason": source_identity["reason"],
        "profile_name": profile_name,
        "walk_forward_run_id": run_id,
        "row_count": 0,
        "minimum_lookback_rows": None,
        "horizon_bars": None,
        "require_mature_future": bool(require_mature_future),
        "case_count": 0,
        "cases": [],
        "skipped_count": 0,
        "invalid_count": 0,
        "event_filters": filters,
        "timestamp_column": None,
        "event_column": None,
        "max_event_age_bars": max_event_age_bars,
        "phase_column": None,
        "trend_column": None,
        "ohlc_columns": {"open": None, "high": None, "low": None, "close": None},
        "warnings": warnings,
        "errors": errors,
    }

    if source_identity["errors"]:
        errors.extend(source_identity["errors"])
        return _json_safe_dict(base_result)

    try:
        data = pd.read_csv(path)
    except Exception as exc:
        errors.append(f"Could not read CSV: {type(exc).__name__}: {exc}")
        return _json_safe_dict(base_result)

    base_result["row_count"] = len(data)
    if data.empty:
        errors.append("CSV is empty.")
        return _json_safe_dict(base_result)

    profile_context = build_parameter_context_from_profile(profile_name)
    if not profile_context.get("success"):
        errors.extend(str(item) for item in profile_context.get("errors") or ["Invalid profile."])
        warnings.extend(str(item) for item in profile_context.get("warnings") or [])
        return _json_safe_dict(base_result)

    effective_profile = str(profile_context.get("profile_name") or profile_name)
    base_result["profile_name"] = effective_profile
    minimum_lookback = _minimum_lookback_rows_from_profile(profile_context)
    horizon = _profile_horizon(profile_context)
    base_result["minimum_lookback_rows"] = minimum_lookback
    base_result["horizon_bars"] = horizon

    effective_timeframe = base_result["timeframe"]
    posture = get_timeframe_posture(effective_profile, effective_timeframe)
    if posture.get("warnings"):
        warnings.extend(str(item) for item in posture.get("warnings") or [])

    columns = [str(column) for column in data.columns]
    timestamp_column = detect_walk_forward_timestamp_column(columns)
    event_column = _first_existing_column(columns, DEFAULT_EVENT_COLUMNS)
    phase_column = _first_existing_column(columns, DEFAULT_PHASE_COLUMNS)
    trend_column = _first_existing_column(columns, DEFAULT_TREND_COLUMNS)
    ohlc_columns = _extract_ohlc_columns(data)
    base_result["timestamp_column"] = timestamp_column
    base_result["event_column"] = event_column
    base_result["phase_column"] = phase_column
    base_result["trend_column"] = trend_column
    base_result["ohlc_columns"] = ohlc_columns

    if step < 1:
        warnings.append("step must be at least 1; using 1.")
        step = 1

    start = max(min_signal_row if min_signal_row is not None else 0, minimum_lookback - 1)
    end = max_signal_row if max_signal_row is not None else len(data) - 1
    end = min(end, len(data) - 1)
    if require_mature_future and horizon is not None:
        end = min(end, len(data) - horizon - 1)

    if start >= len(data):
        warnings.append("No cases built: source CSV has insufficient rows for the selected profile lookback.")
        return _json_safe_dict(base_result)
    if end < start:
        warnings.append("No cases built: no row range satisfies lookback and future-bar requirements.")
        return _json_safe_dict(base_result)
    if filters and event_column is None:
        warnings.append("No cases built: event filters were provided but no event column was found.")
        return _json_safe_dict(base_result)

    cases: list[dict[str, Any]] = []
    invalid_count = 0
    skipped_count = 0
    for index in range(start, end + 1, step):
        row = data.iloc[index]
        if not _row_matches_event_filters(row, event_column, filters):
            skipped_count += 1
            continue
        candidate = build_walk_forward_candidate_from_row(
            row,
            csv_path=path,
            signal_row_index=index,
            total_rows=len(data),
            profile_name=effective_profile,
            profile_context=profile_context,
            ticker=base_result["ticker"],
            timeframe=effective_timeframe,
            timestamp_column=timestamp_column,
            ohlc_columns=ohlc_columns,
            event_column=event_column,
            phase_column=phase_column,
            trend_column=trend_column,
            risk_reward=risk_reward,
            risk_fraction=risk_fraction,
            max_event_age_bars=max_event_age_bars,
            decision_frame=data.iloc[: index + 1],
            walk_forward_run_id=run_id,
        )
        if not candidate.get("snapshot_success"):
            invalid_count += 1
            if not include_invalid_cases:
                skipped_count += 1
                continue
        cases.append(candidate)
        if max_cases is not None and len(cases) >= max_cases:
            break

    if not cases:
        warnings.append("No walk-forward cases were built.")

    base_result.update(
        {
            "success": bool(cases),
            "case_count": len(cases),
            "cases": cases,
            "skipped_count": skipped_count,
            "invalid_count": invalid_count,
        }
    )
    return _json_safe_dict(base_result)


def evaluate_walk_forward_cases(
    cases: list[dict[str, Any]],
    *,
    profile_name: str,
    horizon_bars: int | None = None,
    tie_break_policy: str = DEFAULT_TIE_BREAK_POLICY,
    write_invalid_rows: bool = True,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    horizon = horizon_bars
    if horizon is None:
        profile_context = build_parameter_context_from_profile(profile_name)
        if not profile_context.get("success"):
            errors.extend(str(item) for item in profile_context.get("errors") or ["Invalid profile."])
            warnings.extend(str(item) for item in profile_context.get("warnings") or [])
        else:
            horizon = _profile_horizon(profile_context)
            warnings.extend(str(item) for item in profile_context.get("warnings") or [])

    if horizon is None:
        errors.append("Could not determine profile horizon.")
        return {
            "success": False,
            "profile_name": profile_name,
            "horizon_bars": None,
            "case_count": len(cases or []),
            "evaluated_count": 0,
            "success_count": 0,
            "invalid_count": 0,
            "result_rows": [],
            "results": [],
            "warnings": warnings,
            "errors": errors,
        }

    evaluation = evaluate_candidate_snapshot_rows(
        list(cases or []),
        horizon_bars=int(horizon),
        tie_break_policy=tie_break_policy,
        write_invalid_rows=write_invalid_rows,
    )
    result = {
        "success": evaluation.get("success"),
        "profile_name": profile_name,
        "horizon_bars": int(horizon),
        "case_count": len(cases or []),
        "evaluated_count": evaluation.get("evaluated_count", 0),
        "success_count": evaluation.get("success_count", 0),
        "invalid_count": evaluation.get("invalid_count", 0),
        "result_rows": evaluation.get("result_rows") or [],
        "results": evaluation.get("results") or [],
        "warnings": [*warnings, *(evaluation.get("warnings") or [])],
        "errors": [*errors, *(evaluation.get("errors") or [])],
    }
    return _json_safe_dict(result)


def summarize_walk_forward_validation(
    evaluated_result: dict[str, Any] | list[dict[str, Any]],
) -> dict[str, Any]:
    if isinstance(evaluated_result, dict):
        if isinstance(evaluated_result.get("evaluation_result"), dict):
            rows = evaluated_result.get("evaluation_result", {}).get("result_rows") or []
        else:
            rows = evaluated_result.get("result_rows") or []
    else:
        rows = list(evaluated_result or [])

    warnings: list[str] = []
    errors: list[str] = []
    sample_count = len(rows)
    tp_first_count = 0
    sl_first_count = 0
    neither_count = 0
    invalid_count = 0
    ambiguous_count = 0
    not_mature_count = 0
    horizon_mismatch_count = 0
    scoreable_count = 0
    scoreable_tp_first_count = 0
    scoreable_sl_first_count = 0
    scoreable_neither_count = 0
    realized_values: list[float] = []

    for row in rows:
        outcome = str(row.get("outcome") or "").strip().upper()
        horizon = _to_int(row.get("horizon_bars"))
        future_bars = _to_int(row.get("future_bars_available"))
        error = row.get("outcome_error") or row.get("error")
        if outcome == "TP_FIRST":
            tp_first_count += 1
        elif outcome == "SL_FIRST":
            sl_first_count += 1
        elif outcome == "NEITHER":
            neither_count += 1
        elif outcome == "AMBIGUOUS":
            ambiguous_count += 1
        elif outcome == "INVALID":
            invalid_count += 1

        if horizon is not None and future_bars is not None and future_bars < horizon:
            not_mature_count += 1

        mc_horizon = _to_int(row.get("monte_carlo_horizon") or row.get("mc_horizon"))
        if mc_horizon is not None and horizon is not None and mc_horizon != horizon:
            horizon_mismatch_count += 1

        scoreable = (
            outcome in {"TP_FIRST", "SL_FIRST", "NEITHER"}
            and horizon is not None
            and future_bars is not None
            and future_bars >= horizon
            and outcome not in {"INVALID", "AMBIGUOUS"}
            and _is_missing(error)
        )
        if scoreable:
            scoreable_count += 1
            if outcome == "TP_FIRST":
                scoreable_tp_first_count += 1
            elif outcome == "SL_FIRST":
                scoreable_sl_first_count += 1
            elif outcome == "NEITHER":
                scoreable_neither_count += 1

        realized_r = _to_float(row.get("realized_R"))
        if realized_r is not None and scoreable:
            realized_values.append(realized_r)

    mean_realized = sum(realized_values) / len(realized_values) if realized_values else None
    median_realized = None
    if realized_values:
        ordered = sorted(realized_values)
        midpoint = len(ordered) // 2
        if len(ordered) % 2:
            median_realized = ordered[midpoint]
        else:
            median_realized = (ordered[midpoint - 1] + ordered[midpoint]) / 2

    result = {
        "success": sample_count > 0,
        "sample_count": sample_count,
        "scoreable_count": scoreable_count,
        "tp_first_count": tp_first_count,
        "sl_first_count": sl_first_count,
        "neither_count": neither_count,
        "invalid_count": invalid_count,
        "ambiguous_count": ambiguous_count,
        "not_mature_count": not_mature_count,
        "horizon_mismatch_count": horizon_mismatch_count,
        "mean_realized_R": mean_realized,
        "median_realized_R": median_realized,
        "win_rate": scoreable_tp_first_count / scoreable_count if scoreable_count else None,
        "loss_rate": scoreable_sl_first_count / scoreable_count if scoreable_count else None,
        "neither_rate": scoreable_neither_count / scoreable_count if scoreable_count else None,
        "warnings": warnings,
        "errors": errors,
    }
    return _json_safe_dict(result)


def build_and_evaluate_walk_forward_cases_from_csv(
    csv_path: str | Path,
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
    risk_reward: float = DEFAULT_RISK_REWARD,
    risk_fraction: float = DEFAULT_RISK_FRACTION,
    max_event_age_bars: int | None = None,
    tie_break_policy: str = DEFAULT_TIE_BREAK_POLICY,
) -> dict[str, Any]:
    build_result = build_walk_forward_cases_from_csv(
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
        risk_reward=risk_reward,
        risk_fraction=risk_fraction,
        max_event_age_bars=max_event_age_bars,
    )
    if not build_result.get("success"):
        summary = summarize_walk_forward_validation([])
        return _json_safe_dict(
            {
                "success": False,
                "build_result": build_result,
                "evaluation_result": {
                    "success": False,
                    "profile_name": profile_name,
                    "horizon_bars": build_result.get("horizon_bars"),
                    "case_count": 0,
                    "evaluated_count": 0,
                    "success_count": 0,
                    "invalid_count": 0,
                    "result_rows": [],
                    "results": [],
                    "warnings": [],
                    "errors": [],
                },
                "summary": summary,
                "warnings": build_result.get("warnings") or [],
                "errors": build_result.get("errors") or [],
            }
        )

    evaluation_result = evaluate_walk_forward_cases(
        build_result.get("cases") or [],
        profile_name=str(build_result.get("profile_name") or profile_name),
        horizon_bars=_to_int(build_result.get("horizon_bars")),
        tie_break_policy=tie_break_policy,
    )
    summary = summarize_walk_forward_validation(evaluation_result)
    errors = [*(build_result.get("errors") or []), *(evaluation_result.get("errors") or [])]
    warnings = [*(build_result.get("warnings") or []), *(evaluation_result.get("warnings") or [])]
    return _json_safe_dict(
        {
            "success": bool(build_result.get("success")) and bool(evaluation_result.get("success")),
            "build_result": build_result,
            "evaluation_result": evaluation_result,
            "summary": summary,
            "warnings": warnings,
            "errors": errors,
        }
    )
