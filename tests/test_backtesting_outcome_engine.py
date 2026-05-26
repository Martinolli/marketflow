from __future__ import annotations

import pandas as pd
import pytest

from marketflow.backtesting import (
    CandidateSnapshot,
    evaluate_candidate_outcome,
    evaluate_candidate_outcome_from_csv,
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
    return CandidateSnapshot(**data)


def _frame(rows):
    return pd.DataFrame(rows)


def test_tp_first_outcome():
    data = _frame(
        [
            {"timestamp": "2026-01-01", "open": 100, "high": 101, "low": 99, "close": 100},
            {"timestamp": "2026-01-02", "open": 101, "high": 109, "low": 99, "close": 105},
            {"timestamp": "2026-01-03", "open": 106, "high": 111, "low": 100, "close": 110},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(), horizon_bars=5)

    assert result.outcome == "TP_FIRST"
    assert result.bars_to_hit == 2
    assert result.hit_row_index == 2
    assert result.hit_timestamp == "2026-01-03"
    assert result.realized_R == pytest.approx(2.0)


def test_sl_first_outcome():
    data = _frame(
        [
            {"timestamp": "2026-01-01", "open": 100, "high": 101, "low": 99, "close": 100},
            {"timestamp": "2026-01-02", "open": 99, "high": 104, "low": 94, "close": 96},
            {"timestamp": "2026-01-03", "open": 96, "high": 112, "low": 95, "close": 108},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(), horizon_bars=5)

    assert result.outcome == "SL_FIRST"
    assert result.bars_to_hit == 1
    assert result.realized_R == -1.0


def test_neither_outcome_uses_mark_to_market_r():
    data = _frame(
        [
            {"timestamp": "2026-01-01", "open": 100, "high": 101, "low": 99, "close": 100},
            {"timestamp": "2026-01-02", "open": 101, "high": 106, "low": 98, "close": 101},
            {"timestamp": "2026-01-03", "open": 102, "high": 107, "low": 99, "close": 103},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(), horizon_bars=5)

    assert result.outcome == "NEITHER"
    assert result.bars_to_hit is None
    assert result.mark_to_market_close == 103
    assert result.realized_R == pytest.approx(0.6)


def test_same_bar_conservative_tie_break():
    data = _frame(
        [
            {"open": 100, "high": 101, "low": 99, "close": 100},
            {"open": 100, "high": 111, "low": 94, "close": 100},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(), tie_break_policy="conservative")

    assert result.outcome == "SL_FIRST"
    assert result.same_bar_hit is True
    assert result.bars_to_hit == 1
    assert result.realized_R == -1.0


def test_same_bar_optimistic_tie_break():
    data = _frame(
        [
            {"open": 100, "high": 101, "low": 99, "close": 100},
            {"open": 100, "high": 111, "low": 94, "close": 100},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(), tie_break_policy="optimistic")

    assert result.outcome == "TP_FIRST"
    assert result.same_bar_hit is True
    assert result.realized_R == pytest.approx(2.0)


def test_same_bar_unknown_tie_break():
    data = _frame(
        [
            {"open": 100, "high": 101, "low": 99, "close": 100},
            {"open": 100, "high": 111, "low": 94, "close": 100},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(), tie_break_policy="unknown")

    assert result.outcome == "AMBIGUOUS"
    assert result.same_bar_hit is True
    assert result.realized_R is None


def test_same_bar_open_proximity_tie_break_tp_first():
    data = _frame(
        [
            {"open": 100, "high": 101, "low": 99, "close": 100},
            {"open": 108, "high": 111, "low": 94, "close": 100},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(), tie_break_policy="open_proximity")

    assert result.outcome == "TP_FIRST"
    assert result.realized_R == pytest.approx(2.0)


def test_same_bar_open_proximity_tie_break_sl_first():
    data = _frame(
        [
            {"open": 100, "high": 101, "low": 99, "close": 100},
            {"open": 96, "high": 111, "low": 94, "close": 100},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(), tie_break_policy="open_proximity")

    assert result.outcome == "SL_FIRST"
    assert result.realized_R == -1.0


def test_missing_required_columns_returns_invalid():
    data = _frame(
        [
            {"open": 100, "low": 99, "close": 100},
            {"open": 101, "low": 98, "close": 102},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate())

    assert result.outcome == "INVALID"
    assert "Missing required OHLC column" in str(result.error)


def test_invalid_candidate_levels_return_invalid():
    data = _frame(
        [
            {"high": 101, "low": 99, "close": 100},
            {"high": 102, "low": 98, "close": 101},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(stop_loss=105.0))

    assert result.outcome == "INVALID"
    assert "long setups only" in str(result.error)


def test_signal_row_index_ignores_earlier_rows():
    data = _frame(
        [
            {"timestamp": "2026-01-01", "open": 100, "high": 111, "low": 99, "close": 110},
            {"timestamp": "2026-01-02", "open": 100, "high": 100, "low": 94, "close": 95},
            {"timestamp": "2026-01-03", "open": 100, "high": 101, "low": 99, "close": 100},
            {"timestamp": "2026-01-04", "open": 101, "high": 112, "low": 100, "close": 111},
        ]
    )

    result = evaluate_candidate_outcome(data, _candidate(signal_row_index=2), horizon_bars=2)

    assert result.outcome == "TP_FIRST"
    assert result.signal_row_index == 2
    assert result.bars_to_hit == 1
    assert result.hit_timestamp == "2026-01-04"


def test_signal_timestamp_selects_matching_row():
    data = _frame(
        [
            {"timestamp": "2026-01-01", "open": 100, "high": 111, "low": 99, "close": 110},
            {"timestamp": "2026-01-02", "open": 100, "high": 101, "low": 99, "close": 100},
            {"timestamp": "2026-01-03", "open": 101, "high": 112, "low": 100, "close": 111},
        ]
    )

    result = evaluate_candidate_outcome(
        data,
        {"entry": 100, "sl": 95, "tp": 110, "signal_timestamp": "2026-01-02"},
        horizon_bars=2,
    )

    assert result.outcome == "TP_FIRST"
    assert result.signal_row_index == 1
    assert result.signal_timestamp == "2026-01-02"
    assert result.bars_to_hit == 1


def test_csv_convenience_function(tmp_path):
    data = _frame(
        [
            {"timestamp": "2026-01-01", "open": 100, "high": 101, "low": 99, "close": 100},
            {"timestamp": "2026-01-02", "open": 99, "high": 104, "low": 94, "close": 96},
        ]
    )
    csv_path = tmp_path / "synthetic.csv"
    data.to_csv(csv_path, index=False)

    result = evaluate_candidate_outcome_from_csv(csv_path, _candidate(), horizon_bars=2)

    assert result.outcome == "SL_FIRST"
    assert result.realized_R == -1.0
