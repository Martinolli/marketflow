"""Deterministic TP/SL outcome engine for candidate backtesting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.backtesting.schemas import CandidateSnapshot, OutcomeResult, TieBreakPolicy


REQUIRED_COLUMNS = ("high", "low", "close")
TIMESTAMP_COLUMNS = ("timestamp", "datetime", "date")
VALID_TIE_BREAK_POLICIES = {"conservative", "optimistic", "open_proximity", "unknown"}


def _to_float(value: Any) -> float | None:
    """Convert a scalar value to float when possible."""
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if pd.isna(number):
        return None
    return number


def _to_int(value: Any) -> int | None:
    """Convert a scalar value to int when possible."""
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _candidate_from_mapping(candidate: dict[str, Any]) -> CandidateSnapshot:
    """Normalize dict-like candidate fields into a CandidateSnapshot."""
    return CandidateSnapshot(
        ticker=candidate.get("ticker"),
        timeframe=candidate.get("timeframe") or candidate.get("tf"),
        source_csv=candidate.get("source_csv") or candidate.get("csv"),
        signal_timestamp=candidate.get("signal_timestamp"),
        signal_row_index=_to_int(candidate.get("signal_row_index")),
        entry=_to_float(candidate.get("entry")),
        stop_loss=_to_float(candidate.get("stop_loss") if "stop_loss" in candidate else candidate.get("sl")),
        take_profit=_to_float(candidate.get("take_profit") if "take_profit" in candidate else candidate.get("tp")),
        risk_reward=_to_float(candidate.get("risk_reward") if "risk_reward" in candidate else candidate.get("rr")),
        strategy_score=_to_float(candidate.get("strategy_score") if "strategy_score" in candidate else candidate.get("score")),
        wyckoff_phase=candidate.get("wyckoff_phase") or candidate.get("phase"),
        wyckoff_event=candidate.get("wyckoff_event") or candidate.get("event"),
        trend=candidate.get("trend"),
        candidate_source=candidate.get("candidate_source"),
        report_date=candidate.get("report_date"),
    )


def _normalize_candidate(candidate: CandidateSnapshot | dict[str, Any]) -> CandidateSnapshot:
    """Return a CandidateSnapshot from supported candidate inputs."""
    if isinstance(candidate, CandidateSnapshot):
        return CandidateSnapshot(
            ticker=candidate.ticker,
            timeframe=candidate.timeframe,
            source_csv=candidate.source_csv,
            signal_timestamp=candidate.signal_timestamp,
            signal_row_index=_to_int(candidate.signal_row_index),
            entry=_to_float(candidate.entry),
            stop_loss=_to_float(candidate.stop_loss),
            take_profit=_to_float(candidate.take_profit),
            risk_reward=_to_float(candidate.risk_reward),
            strategy_score=_to_float(candidate.strategy_score),
            wyckoff_phase=candidate.wyckoff_phase,
            wyckoff_event=candidate.wyckoff_event,
            trend=candidate.trend,
            candidate_source=candidate.candidate_source,
            report_date=candidate.report_date,
        )
    if isinstance(candidate, dict):
        return _candidate_from_mapping(candidate)
    return CandidateSnapshot()


def _timestamp_from_row(row: pd.Series) -> str | None:
    """Extract a timestamp-like value from a row."""
    for column in TIMESTAMP_COLUMNS:
        if column in row.index:
            value = row.get(column)
            if value is not None and value != "" and not pd.isna(value):
                return str(value)
    return None


def _invalid_result(
    *,
    candidate: CandidateSnapshot,
    horizon_bars: int,
    tie_break_policy: TieBreakPolicy,
    error: str,
    signal_row_index: int | None = None,
    signal_timestamp: str | None = None,
    planned_rr: float | None = None,
    future_bars_available: int | None = None,
    evaluation_window_start_index: int | None = None,
    evaluation_window_end_index: int | None = None,
    signal_is_latest_row: bool | None = None,
    neither_reason: str | None = None,
) -> OutcomeResult:
    """Build an INVALID outcome result."""
    return OutcomeResult(
        outcome="INVALID",
        bars_to_hit=None,
        realized_R=None,
        same_bar_hit=False,
        tie_break_policy=tie_break_policy,
        horizon_bars=horizon_bars,
        signal_row_index=signal_row_index,
        signal_timestamp=signal_timestamp or candidate.signal_timestamp,
        hit_timestamp=None,
        hit_row_index=None,
        entry=_to_float(candidate.entry),
        stop_loss=_to_float(candidate.stop_loss),
        take_profit=_to_float(candidate.take_profit),
        planned_rr=planned_rr,
        mark_to_market_close=None,
        error=error,
        future_bars_available=future_bars_available,
        evaluation_window_start_index=evaluation_window_start_index,
        evaluation_window_end_index=evaluation_window_end_index,
        signal_is_latest_row=signal_is_latest_row,
        neither_reason=neither_reason,
    )


def _required_columns_error(data: pd.DataFrame) -> str | None:
    """Return a missing-columns error message when required OHLC columns are absent."""
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        return f"Missing required OHLC column(s): {', '.join(missing)}."
    return None


def _find_signal_row_index(data: pd.DataFrame, candidate: CandidateSnapshot) -> int | None:
    """Find the signal row position using index, timestamp, or default row 0."""
    if candidate.signal_row_index is not None:
        if 0 <= candidate.signal_row_index < len(data):
            return int(candidate.signal_row_index)
        return None

    if candidate.signal_timestamp:
        timestamp_columns = [column for column in TIMESTAMP_COLUMNS if column in data.columns]
        for column in timestamp_columns:
            exact = data[column].astype(str) == str(candidate.signal_timestamp)
            if exact.any():
                return next(int(position) for position, matched in enumerate(exact) if bool(matched))

        try:
            target = pd.to_datetime(candidate.signal_timestamp)
            for column in timestamp_columns:
                values = pd.to_datetime(data[column], errors="coerce")
                matches = values == target
                if matches.any():
                    return next(int(position) for position, matched in enumerate(matches) if bool(matched))
        except Exception:
            return None

        if timestamp_columns:
            return None

    return 0 if len(data) else None


def _validate_candidate(
    candidate: CandidateSnapshot,
    *,
    horizon_bars: int,
) -> tuple[str | None, float | None]:
    """Validate candidate levels and return an error plus planned R when available."""
    entry = _to_float(candidate.entry)
    stop_loss = _to_float(candidate.stop_loss)
    take_profit = _to_float(candidate.take_profit)
    if horizon_bars < 1:
        return "horizon_bars must be at least 1.", None
    if entry is None:
        return "Candidate entry is missing or non-numeric.", None
    if stop_loss is None:
        return "Candidate stop_loss is missing or non-numeric.", None
    if take_profit is None:
        return "Candidate take_profit is missing or non-numeric.", None
    if entry == stop_loss:
        return "Candidate entry and stop_loss cannot be equal.", None
    if not stop_loss < entry < take_profit:
        return "Phase 1 outcome engine supports long setups only: stop_loss < entry < take_profit is required.", None

    planned_rr = _to_float(candidate.risk_reward)
    if planned_rr is None:
        planned_rr = (take_profit - entry) / (entry - stop_loss)
    return None, planned_rr


def _close_for_mark_to_market(
    data: pd.DataFrame,
    *,
    signal_index: int,
    future_rows: pd.DataFrame,
) -> float | None:
    """Return the close used to mark a NEITHER outcome to market."""
    if not future_rows.empty:
        return _to_float(future_rows.iloc[-1].get("close"))
    if 0 <= signal_index < len(data):
        return _to_float(data.iloc[signal_index].get("close"))
    return None


def _future_window_diagnostics(
    data: pd.DataFrame,
    *,
    signal_index: int,
    horizon_bars: int,
) -> tuple[pd.DataFrame, dict[str, int | bool | None]]:
    """Return future rows plus deterministic evaluation-window diagnostics."""
    future_rows = data.iloc[signal_index + 1 : signal_index + 1 + horizon_bars]
    future_bars_available = len(future_rows)
    return future_rows, {
        "future_bars_available": future_bars_available,
        "evaluation_window_start_index": signal_index + 1 if future_bars_available > 0 else None,
        "evaluation_window_end_index": signal_index + future_bars_available if future_bars_available > 0 else None,
        "signal_is_latest_row": signal_index >= len(data) - 1,
    }


def _neither_reason(*, future_bars_available: int, horizon_bars: int) -> str:
    """Explain why a NEITHER outcome had no TP/SL hit."""
    if future_bars_available == 0:
        return "no_future_bars_available"
    if future_bars_available < horizon_bars:
        return "partial_future_window_no_hit"
    return "full_horizon_no_hit"


def _mark_to_market_r(close: float | None, entry: float, stop_loss: float) -> float | None:
    """Compute long mark-to-market R."""
    if close is None:
        return None
    return (close - entry) / (entry - stop_loss)


def _same_bar_outcome(
    row: pd.Series,
    *,
    entry: float,
    stop_loss: float,
    take_profit: float,
    planned_rr: float,
    tie_break_policy: TieBreakPolicy,
) -> tuple[str, float | None]:
    """Apply same-bar tie-break policy."""
    if tie_break_policy == "conservative":
        return "SL_FIRST", -1.0
    if tie_break_policy == "optimistic":
        return "TP_FIRST", planned_rr
    if tie_break_policy == "unknown":
        return "AMBIGUOUS", None
    if tie_break_policy == "open_proximity":
        open_price = _to_float(row.get("open"))
        if open_price is None:
            return "AMBIGUOUS", None
        stop_distance = abs(open_price - stop_loss)
        target_distance = abs(take_profit - open_price)
        if target_distance < stop_distance:
            return "TP_FIRST", planned_rr
        if stop_distance < target_distance:
            return "SL_FIRST", -1.0
        return "AMBIGUOUS", None
    return "AMBIGUOUS", None


def evaluate_candidate_outcome(
    data: pd.DataFrame,
    candidate: CandidateSnapshot | dict[str, Any],
    *,
    horizon_bars: int = 20,
    tie_break_policy: TieBreakPolicy = "conservative",
) -> OutcomeResult:
    """Evaluate the actual TP/SL/neither outcome for one candidate snapshot."""
    normalized = _normalize_candidate(candidate)
    if tie_break_policy not in VALID_TIE_BREAK_POLICIES:
        tie_break_policy = "conservative"

    column_error = _required_columns_error(data)
    if column_error:
        return _invalid_result(
            candidate=normalized,
            horizon_bars=horizon_bars,
            tie_break_policy=tie_break_policy,
            error=column_error,
        )

    validation_error, planned_rr = _validate_candidate(normalized, horizon_bars=horizon_bars)
    if validation_error:
        return _invalid_result(
            candidate=normalized,
            horizon_bars=horizon_bars,
            tie_break_policy=tie_break_policy,
            error=validation_error,
            planned_rr=planned_rr,
        )

    signal_index = _find_signal_row_index(data, normalized)
    if signal_index is None:
        return _invalid_result(
            candidate=normalized,
            horizon_bars=horizon_bars,
            tie_break_policy=tie_break_policy,
            error="Could not locate a valid signal row.",
            planned_rr=planned_rr,
        )

    signal_timestamp = _timestamp_from_row(data.iloc[signal_index]) if len(data) else normalized.signal_timestamp
    entry = float(normalized.entry)  # validated above
    stop_loss = float(normalized.stop_loss)  # validated above
    take_profit = float(normalized.take_profit)  # validated above
    planned_rr = float(planned_rr) if planned_rr is not None else None
    future_rows, diagnostics = _future_window_diagnostics(
        data,
        signal_index=signal_index,
        horizon_bars=horizon_bars,
    )

    for position, (_, row) in enumerate(future_rows.iterrows(), start=1):
        high = _to_float(row.get("high"))
        low = _to_float(row.get("low"))
        if high is None or low is None:
            continue

        hit_tp = high >= take_profit
        hit_sl = low <= stop_loss
        hit_index = signal_index + position
        hit_timestamp = _timestamp_from_row(row)

        if hit_tp and hit_sl:
            outcome, realized_r = _same_bar_outcome(
                row,
                entry=entry,
                stop_loss=stop_loss,
                take_profit=take_profit,
                planned_rr=planned_rr,
                tie_break_policy=tie_break_policy,
            )
            return OutcomeResult(
                outcome=outcome,
                bars_to_hit=position,
                realized_R=realized_r,
                same_bar_hit=True,
                tie_break_policy=tie_break_policy,
                horizon_bars=horizon_bars,
                signal_row_index=signal_index,
                signal_timestamp=signal_timestamp,
                hit_timestamp=hit_timestamp,
                hit_row_index=hit_index,
                entry=entry,
                stop_loss=stop_loss,
                take_profit=take_profit,
                planned_rr=planned_rr,
                mark_to_market_close=None,
                error=None,
                **diagnostics,
            )
        if hit_tp:
            return OutcomeResult(
                outcome="TP_FIRST",
                bars_to_hit=position,
                realized_R=planned_rr,
                same_bar_hit=False,
                tie_break_policy=tie_break_policy,
                horizon_bars=horizon_bars,
                signal_row_index=signal_index,
                signal_timestamp=signal_timestamp,
                hit_timestamp=hit_timestamp,
                hit_row_index=hit_index,
                entry=entry,
                stop_loss=stop_loss,
                take_profit=take_profit,
                planned_rr=planned_rr,
                mark_to_market_close=None,
                error=None,
                **diagnostics,
            )
        if hit_sl:
            return OutcomeResult(
                outcome="SL_FIRST",
                bars_to_hit=position,
                realized_R=-1.0,
                same_bar_hit=False,
                tie_break_policy=tie_break_policy,
                horizon_bars=horizon_bars,
                signal_row_index=signal_index,
                signal_timestamp=signal_timestamp,
                hit_timestamp=hit_timestamp,
                hit_row_index=hit_index,
                entry=entry,
                stop_loss=stop_loss,
                take_profit=take_profit,
                planned_rr=planned_rr,
                mark_to_market_close=None,
                error=None,
                **diagnostics,
            )

    mark_to_market_close = _close_for_mark_to_market(data, signal_index=signal_index, future_rows=future_rows)
    future_bars_available = int(diagnostics["future_bars_available"] or 0)
    return OutcomeResult(
        outcome="NEITHER",
        bars_to_hit=None,
        realized_R=_mark_to_market_r(mark_to_market_close, entry, stop_loss),
        same_bar_hit=False,
        tie_break_policy=tie_break_policy,
        horizon_bars=horizon_bars,
        signal_row_index=signal_index,
        signal_timestamp=signal_timestamp,
        hit_timestamp=None,
        hit_row_index=None,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        planned_rr=planned_rr,
        mark_to_market_close=mark_to_market_close,
        error=None,
        neither_reason=_neither_reason(
            future_bars_available=future_bars_available,
            horizon_bars=horizon_bars,
        ),
        **diagnostics,
    )


def evaluate_candidate_outcome_from_csv(
    csv_path: str | Path,
    candidate: CandidateSnapshot | dict[str, Any],
    *,
    horizon_bars: int = 20,
    tie_break_policy: TieBreakPolicy = "conservative",
) -> OutcomeResult:
    """Read a CSV and evaluate one candidate outcome."""
    normalized = _normalize_candidate(candidate)
    try:
        data = pd.read_csv(csv_path)
    except Exception as exc:
        return _invalid_result(
            candidate=normalized,
            horizon_bars=horizon_bars,
            tie_break_policy=tie_break_policy,
            error=f"Could not read CSV: {type(exc).__name__}: {exc}",
        )

    return evaluate_candidate_outcome(
        data,
        normalized,
        horizon_bars=horizon_bars,
        tie_break_policy=tie_break_policy,
    )
