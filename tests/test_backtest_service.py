from __future__ import annotations

import math

import pandas as pd

from marketflow.backtesting.schemas import OutcomeResult
from marketflow.services.backtest_service import (
    candidate_snapshot_to_dict,
    evaluate_backtest_candidate,
    evaluate_backtest_candidate_from_csv,
    evaluate_backtest_candidates_from_csv,
    outcome_result_to_dict,
)


def _frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"timestamp": "2026-01-01", "open": 100, "high": 101, "low": 99, "close": 100},
            {"timestamp": "2026-01-02", "open": 101, "high": 112, "low": 100, "close": 111},
            {"timestamp": "2026-01-03", "open": 111, "high": 112, "low": 98, "close": 104},
        ]
    )


def _candidate(**overrides):
    data = {
        "ticker": "TEST",
        "timeframe": "1d",
        "entry": 100.0,
        "stop_loss": 95.0,
        "take_profit": 110.0,
    }
    data.update(overrides)
    return data


def test_single_dataframe_candidate_returns_success_dict():
    result = evaluate_backtest_candidate(_frame(), _candidate(), horizon_bars=2)

    assert result["success"] is True
    assert result["csv_path"] is None
    assert result["settings"] == {"horizon_bars": 2, "tie_break_policy": "conservative"}
    assert result["outcome"]["outcome"] == "TP_FIRST"
    assert result["outcome"]["realized_R"] == 2.0
    assert result["error"] is None


def test_single_csv_candidate_returns_json_safe_success_dict(tmp_path):
    csv_path = tmp_path / "synthetic.csv"
    _frame().to_csv(csv_path, index=False)

    result = evaluate_backtest_candidate_from_csv(csv_path, _candidate(), horizon_bars=2)

    assert result["success"] is True
    assert result["csv_path"] == str(csv_path)
    assert result["outcome"]["outcome"] == "TP_FIRST"
    assert isinstance(result["outcome"]["realized_R"], float)
    assert not any(isinstance(value, float) and math.isnan(value) for value in result["outcome"].values())


def test_invalid_candidate_returns_success_false():
    result = evaluate_backtest_candidate(_frame(), _candidate(stop_loss=105.0), horizon_bars=2)

    assert result["success"] is False
    assert result["outcome"]["outcome"] == "INVALID"
    assert result["error"]


def test_batch_evaluates_multiple_candidates_from_one_csv(tmp_path):
    csv_path = tmp_path / "synthetic.csv"
    _frame().to_csv(csv_path, index=False)
    candidates = [
        _candidate(),
        _candidate(stop_loss=105.0),
    ]

    result = evaluate_backtest_candidates_from_csv(csv_path, candidates, horizon_bars=2)

    assert result["success"] is False
    assert result["csv_path"] == str(csv_path)
    assert result["count"] == 2
    assert result["success_count"] == 1
    assert result["invalid_count"] == 1
    assert [item["outcome"]["outcome"] for item in result["results"]] == ["TP_FIRST", "INVALID"]


def test_dict_aliases_normalize_candidate_fields():
    candidate = {
        "ticker": "TEST",
        "tf": "4h",
        "csv": "TEST_4h.csv",
        "entry": 100,
        "sl": 95,
        "tp": 110,
        "rr": 2,
        "score": 72,
        "phase": "D",
        "event": "SOS",
    }

    normalized = candidate_snapshot_to_dict(candidate)

    assert normalized["timeframe"] == "4h"
    assert normalized["source_csv"] == "TEST_4h.csv"
    assert normalized["stop_loss"] == 95
    assert normalized["take_profit"] == 110
    assert normalized["risk_reward"] == 2
    assert normalized["strategy_score"] == 72
    assert normalized["wyckoff_phase"] == "D"
    assert normalized["wyckoff_event"] == "SOS"


def test_outcome_result_to_dict_converts_nan_to_none():
    result = OutcomeResult(
        outcome="NEITHER",
        bars_to_hit=None,
        realized_R=float("nan"),
        same_bar_hit=False,
        tie_break_policy="conservative",
        horizon_bars=20,
        signal_row_index=0,
        signal_timestamp=None,
        hit_timestamp=None,
        hit_row_index=None,
        entry=100,
        stop_loss=95,
        take_profit=110,
        planned_rr=2,
        mark_to_market_close=float("nan"),
        error=None,
    )

    data = outcome_result_to_dict(result)

    assert data["realized_R"] is None
    assert data["mark_to_market_close"] is None
