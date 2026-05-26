"""JSON-safe service wrappers for deterministic backtest outcome evaluation."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.backtesting import (
    CandidateSnapshot,
    OutcomeResult,
    evaluate_candidate_outcome,
    evaluate_candidate_outcome_from_csv,
)
from marketflow.backtesting.schemas import TieBreakPolicy


CANDIDATE_FIELDS = (
    "ticker",
    "timeframe",
    "source_csv",
    "signal_timestamp",
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
)


def _json_safe_value(value: Any) -> Any:
    """Convert scalar values to JSON-safe Python primitives."""
    if value is None:
        return None
    if hasattr(value, "item"):
        try:
            value = value.item()
        except Exception:
            pass
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    return str(value)


def _json_safe_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Convert a flat dictionary to JSON-safe scalar values."""
    return {key: _json_safe_value(value) for key, value in data.items()}


def outcome_result_to_dict(result: OutcomeResult) -> dict[str, Any]:
    """Convert an OutcomeResult dataclass into a JSON-safe dictionary."""
    return _json_safe_dict(asdict(result))


def candidate_snapshot_to_dict(candidate: CandidateSnapshot | dict[str, Any]) -> dict[str, Any]:
    """Normalize a candidate snapshot into JSON-safe service fields."""
    if isinstance(candidate, CandidateSnapshot) or is_dataclass(candidate):
        source = asdict(candidate)
    elif isinstance(candidate, dict):
        source = {
            "ticker": candidate.get("ticker"),
            "timeframe": candidate.get("timeframe") or candidate.get("tf"),
            "source_csv": candidate.get("source_csv") or candidate.get("csv"),
            "signal_timestamp": candidate.get("signal_timestamp"),
            "signal_row_index": candidate.get("signal_row_index"),
            "entry": candidate.get("entry"),
            "stop_loss": candidate.get("stop_loss") if "stop_loss" in candidate else candidate.get("sl"),
            "take_profit": candidate.get("take_profit") if "take_profit" in candidate else candidate.get("tp"),
            "risk_reward": candidate.get("risk_reward") if "risk_reward" in candidate else candidate.get("rr"),
            "strategy_score": candidate.get("strategy_score") if "strategy_score" in candidate else candidate.get("score"),
            "wyckoff_phase": candidate.get("wyckoff_phase") or candidate.get("phase"),
            "wyckoff_event": candidate.get("wyckoff_event") or candidate.get("event"),
            "trend": candidate.get("trend"),
            "candidate_source": candidate.get("candidate_source"),
            "report_date": candidate.get("report_date"),
        }
    else:
        source = {}
    return _json_safe_dict({field: source.get(field) for field in CANDIDATE_FIELDS})


def _settings(horizon_bars: int, tie_break_policy: TieBreakPolicy) -> dict[str, Any]:
    """Return service settings in a stable shape."""
    return {
        "horizon_bars": int(horizon_bars),
        "tie_break_policy": tie_break_policy,
    }


def _service_result(
    *,
    csv_path: str | None,
    candidate: CandidateSnapshot | dict[str, Any],
    result: OutcomeResult,
    horizon_bars: int,
    tie_break_policy: TieBreakPolicy,
) -> dict[str, Any]:
    """Build one JSON-safe service response."""
    outcome = outcome_result_to_dict(result)
    return {
        "success": result.outcome != "INVALID",
        "csv_path": csv_path,
        "candidate": candidate_snapshot_to_dict(candidate),
        "settings": _settings(horizon_bars, tie_break_policy),
        "outcome": outcome,
        "error": outcome.get("error") if result.outcome == "INVALID" else None,
    }


def evaluate_backtest_candidate(
    data: pd.DataFrame,
    candidate: CandidateSnapshot | dict[str, Any],
    *,
    horizon_bars: int = 20,
    tie_break_policy: TieBreakPolicy = "conservative",
) -> dict[str, Any]:
    """Evaluate one candidate against an in-memory OHLC dataframe."""
    result = evaluate_candidate_outcome(
        data,
        candidate,
        horizon_bars=horizon_bars,
        tie_break_policy=tie_break_policy,
    )
    return _service_result(
        csv_path=None,
        candidate=candidate,
        result=result,
        horizon_bars=horizon_bars,
        tie_break_policy=tie_break_policy,
    )


def evaluate_backtest_candidate_from_csv(
    csv_path: str | Path,
    candidate: CandidateSnapshot | dict[str, Any],
    *,
    horizon_bars: int = 20,
    tie_break_policy: TieBreakPolicy = "conservative",
) -> dict[str, Any]:
    """Evaluate one candidate against a CSV file."""
    result = evaluate_candidate_outcome_from_csv(
        csv_path,
        candidate,
        horizon_bars=horizon_bars,
        tie_break_policy=tie_break_policy,
    )
    return _service_result(
        csv_path=str(csv_path),
        candidate=candidate,
        result=result,
        horizon_bars=horizon_bars,
        tie_break_policy=tie_break_policy,
    )


def evaluate_backtest_candidates_from_csv(
    csv_path: str | Path,
    candidates: list[CandidateSnapshot | dict[str, Any]],
    *,
    horizon_bars: int = 20,
    tie_break_policy: TieBreakPolicy = "conservative",
) -> dict[str, Any]:
    """Evaluate multiple candidates against one CSV read."""
    try:
        data = pd.read_csv(csv_path)
    except Exception as exc:
        error = f"Could not read CSV: {type(exc).__name__}: {exc}"
        results = [
            {
                "success": False,
                "csv_path": str(csv_path),
                "candidate": candidate_snapshot_to_dict(candidate),
                "settings": _settings(horizon_bars, tie_break_policy),
                "outcome": {
                    "outcome": "INVALID",
                    "bars_to_hit": None,
                    "realized_R": None,
                    "same_bar_hit": False,
                    "tie_break_policy": tie_break_policy,
                    "horizon_bars": int(horizon_bars),
                    "signal_row_index": None,
                    "signal_timestamp": None,
                    "hit_timestamp": None,
                    "hit_row_index": None,
                    "entry": candidate_snapshot_to_dict(candidate).get("entry"),
                    "stop_loss": candidate_snapshot_to_dict(candidate).get("stop_loss"),
                    "take_profit": candidate_snapshot_to_dict(candidate).get("take_profit"),
                    "planned_rr": None,
                    "mark_to_market_close": None,
                    "error": error,
                },
                "error": error,
            }
            for candidate in candidates
        ]
        return {
            "success": False,
            "csv_path": str(csv_path),
            "settings": _settings(horizon_bars, tie_break_policy),
            "count": len(candidates),
            "success_count": 0,
            "invalid_count": len(candidates),
            "results": results,
            "error": error,
        }

    results = [
        evaluate_backtest_candidate(
            data,
            candidate,
            horizon_bars=horizon_bars,
            tie_break_policy=tie_break_policy,
        )
        for candidate in candidates
    ]
    for item in results:
        item["csv_path"] = str(csv_path)

    success_count = sum(1 for item in results if item.get("success"))
    invalid_count = len(results) - success_count
    return {
        "success": invalid_count == 0,
        "csv_path": str(csv_path),
        "settings": _settings(horizon_bars, tie_break_policy),
        "count": len(candidates),
        "success_count": success_count,
        "invalid_count": invalid_count,
        "results": results,
    }
