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
    composite_score: float | None = None
    score_status: str | None = None
    score_reason: str | None = None
    active_evidence_profile: str | None = None
    configured_weight_total: float | None = None
    active_weight_total: float | None = None
    available_weight_total: float | None = None
    evidence_coverage: float | None = None
    missing_components: list[str] | None = None
    disabled_components: list[str] | None = None
    invalid_components: list[str] | None = None
    rank_eligible: bool | None = None
    score_profile_calibration: str | None = None
    phase_evidence_status: str | None = None
    phase_evidence_score: float | None = None
    phase_evidence_configured_weight: float | None = None
    phase_evidence_active_weight: float | None = None
    phase_evidence_provenance: str | None = None
    phase_evidence_reason: str | None = None
    phase_evidence_expected_by_profile: bool | None = None
    phase_evidence_scoring_eligible: bool | None = None
    event_evidence_status: str | None = None
    event_evidence_score: float | None = None
    event_evidence_configured_weight: float | None = None
    event_evidence_active_weight: float | None = None
    event_evidence_provenance: str | None = None
    event_evidence_reason: str | None = None
    event_evidence_expected_by_profile: bool | None = None
    event_evidence_scoring_eligible: bool | None = None
    pnf_score: float | None = None
    pnf_evidence_status: str | None = None
    pnf_evidence_score: float | None = None
    pnf_evidence_configured_weight: float | None = None
    pnf_evidence_active_weight: float | None = None
    pnf_evidence_provenance: str | None = None
    pnf_evidence_reason: str | None = None
    pnf_evidence_expected_by_profile: bool | None = None
    pnf_evidence_scoring_eligible: bool | None = None
    pop_evidence_status: str | None = None
    pop_evidence_score: float | None = None
    pop_evidence_configured_weight: float | None = None
    pop_evidence_active_weight: float | None = None
    pop_evidence_provenance: str | None = None
    pop_evidence_reason: str | None = None
    pop_evidence_expected_by_profile: bool | None = None
    pop_evidence_scoring_eligible: bool | None = None
    trend_evidence_status: str | None = None
    trend_evidence_score: float | None = None
    trend_evidence_configured_weight: float | None = None
    trend_evidence_active_weight: float | None = None
    trend_evidence_provenance: str | None = None
    trend_evidence_reason: str | None = None
    trend_evidence_expected_by_profile: bool | None = None
    trend_evidence_scoring_eligible: bool | None = None
    wyckoff_phase: str | None = None
    wyckoff_event: str | None = None
    event_status: str | None = None
    event_provenance: str | None = None
    event_age_bars: int | None = None
    event_max_age_bars: int | None = None
    event_scoring_eligible: bool | None = None
    event_occurrence_row_index: int | None = None
    event_occurrence_timestamp: str | None = None
    event_decision_row_index: int | None = None
    event_superseded_count: int | None = None
    event_reason: str | None = None
    event_resolution_source: str | None = None
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
    future_bars_available: int | None = None
    evaluation_window_start_index: int | None = None
    evaluation_window_end_index: int | None = None
    signal_is_latest_row: bool | None = None
    neither_reason: str | None = None
