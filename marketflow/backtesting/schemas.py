"""Lightweight schemas for deterministic backtesting utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


TieBreakPolicy = Literal["conservative", "optimistic", "open_proximity", "unknown"]
OutcomeLabel = Literal["TP_FIRST", "SL_FIRST", "NEITHER", "AMBIGUOUS", "INVALID"]


@dataclass(frozen=True)
class CandidateSnapshot:
    ticker: str | None = None
    timeframe: str | None = None
    source_csv: str | None = None
    signal_timestamp: str | None = None
    signal_row_index: int | None = None
    entry: float | None = None
    stop_loss: float | None = None
    take_profit: float | None = None
    risk_reward: float | None = None
    strategy_score: float | None = None
    wyckoff_phase: str | None = None
    wyckoff_event: str | None = None
    trend: str | None = None
    candidate_source: str | None = None
    report_date: str | None = None


@dataclass(frozen=True)
class OutcomeResult:
    outcome: OutcomeLabel
    bars_to_hit: int | None
    realized_R: float | None
    same_bar_hit: bool
    tie_break_policy: TieBreakPolicy
    horizon_bars: int
    signal_row_index: int | None
    signal_timestamp: str | None
    hit_timestamp: str | None
    hit_row_index: int | None
    entry: float | None
    stop_loss: float | None
    take_profit: float | None
    planned_rr: float | None
    mark_to_market_close: float | None
    error: str | None = None
