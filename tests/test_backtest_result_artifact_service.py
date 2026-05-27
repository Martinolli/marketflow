from __future__ import annotations

import csv

import pandas as pd

from marketflow.services.backtest_result_artifact_service import (
    BACKTEST_RESULT_COLUMNS,
    backtest_result_row,
    build_backtest_results_filename,
    write_backtest_result_csv,
    write_backtest_results_csv,
)


def _snapshot_row(**overrides):
    row = {
        "ticker": "LOAR",
        "timeframe": "1d",
        "source_csv": "LOAR_1d_wyckoff_annotated.csv",
        "source_report_dir": "reports/2026-05-26/LOAR",
        "signal_timestamp": "2026-05-01 09:30:00",
        "signal_timestamp_source": "timestamp",
        "signal_row_index": 42,
        "entry": 62.34,
        "stop_loss": 55.76,
        "take_profit": 72.20,
        "risk_reward": 1.5,
        "strategy_score": 73.33,
        "wyckoff_phase": "D",
        "wyckoff_event": "SPRING_WEAK",
        "trend": "Up",
        "candidate_source": "strategy_ranking",
        "report_date": "2026-05-26",
        "direction": "long",
        "source_strategy_rank": 1,
        "validation_status": "valid",
        "snapshot_success": True,
    }
    row.update(overrides)
    return row


def _result_row(outcome="TP_FIRST", **overrides):
    outcome_result = {
        "outcome": outcome,
        "bars_to_hit": 3,
        "realized_R": 1.5,
        "same_bar_hit": False,
        "tie_break_policy": "conservative",
        "horizon_bars": 20,
        "hit_timestamp": "2026-05-04 09:30:00",
        "hit_row_index": 45,
        "planned_rr": 1.5,
        "mark_to_market_close": None,
        "error": None,
    }
    outcome_result.update(overrides)
    return backtest_result_row(
        snapshot_row=_snapshot_row(),
        outcome_result=outcome_result,
        candidate_snapshot_file="LOAR_1d_backtest_candidates_20260526_150000.csv",
        created_at="2026-05-26 16:00:00",
    )


def test_filename_with_ticker_timeframe():
    filename = build_backtest_results_filename(ticker="LOAR", timeframe="1d", timestamp="20260526_160000")

    assert filename == "LOAR_1d_backtest_results_20260526_160000.csv"


def test_fallback_filename():
    filename = build_backtest_results_filename(timestamp="20260526_160000")

    assert filename == "marketflow_backtest_results_20260526_160000.csv"


def test_unsafe_filename_parts_are_sanitized():
    filename = build_backtest_results_filename(ticker="LO/AR Inc", timeframe="1 d", timestamp="20260526_160000")

    assert "/" not in filename
    assert " " not in filename
    assert filename == "LO_AR_Inc_1_d_backtest_results_20260526_160000.csv"


def test_row_conversion_tp_first_preserves_contract():
    row = _result_row()

    assert list(row.keys()) == BACKTEST_RESULT_COLUMNS
    assert row["backtest_success"] is True
    assert row["outcome"] == "TP_FIRST"
    assert row["bars_to_hit"] == 3
    assert row["realized_R"] == 1.5
    assert row["same_bar_hit"] is False
    assert row["tie_break_policy"] == "conservative"
    assert row["horizon_bars"] == 20
    assert row["entry"] == 62.34
    assert row["stop_loss"] == 55.76
    assert row["take_profit"] == 72.20
    assert row["candidate_snapshot_file"] == "LOAR_1d_backtest_candidates_20260526_150000.csv"


def test_row_conversion_sl_first():
    row = _result_row(outcome="SL_FIRST", realized_R=None, realized_r=-1.0)

    assert row["outcome"] == "SL_FIRST"
    assert row["backtest_success"] is True
    assert row["realized_R"] == -1.0


def test_row_conversion_neither():
    row = _result_row(outcome="NEITHER", bars_to_hit=None, realized_R=0.25, mark_to_market_close=64.12)

    assert row["outcome"] == "NEITHER"
    assert row["backtest_success"] is True
    assert row["mark_to_market_close"] == 64.12


def test_row_conversion_ambiguous():
    row = _result_row(outcome="AMBIGUOUS", realized_R=None, same_bar_hit=True)

    assert row["outcome"] == "AMBIGUOUS"
    assert row["backtest_success"] is True
    assert row["same_bar_hit"] is True


def test_row_conversion_invalid():
    row = _result_row(outcome="INVALID", realized_R=None, error="Missing OHLC data.")

    assert row["outcome"] == "INVALID"
    assert row["backtest_success"] is False
    assert row["outcome_error"] == "Missing OHLC data."


def test_validation_mapping():
    row = backtest_result_row(
        snapshot_row=_snapshot_row(validation_status="valid", snapshot_success=True),
        outcome_result={"outcome": "TP_FIRST"},
        created_at="2026-05-26 16:00:00",
    )

    assert row["candidate_validation_status"] == "valid"
    assert row["candidate_snapshot_success"] is True


def test_write_one_result(tmp_path):
    result = write_backtest_result_csv(
        _result_row(),
        tmp_path,
        ticker="LOAR",
        timeframe="1d",
        timestamp="20260526_160000",
    )

    assert result["success"] is True
    assert result["count"] == 1
    assert result["success_count"] == 1
    assert result["invalid_count"] == 0

    path = tmp_path / result["filename"]
    assert path.exists()
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    assert list(rows[0].keys()) == BACKTEST_RESULT_COLUMNS
    assert rows[0]["outcome"] == "TP_FIRST"


def test_write_mixed_valid_and_invalid_result_rows(tmp_path):
    result = write_backtest_results_csv(
        [_result_row(), _result_row(outcome="INVALID", realized_R=None, error="Invalid candidate.")],
        tmp_path,
        ticker="LOAR",
        timeframe="1d",
        timestamp="20260526_160000",
    )

    assert result["success"] is True
    assert result["count"] == 2
    assert result["success_count"] == 1
    assert result["invalid_count"] == 1
    assert (tmp_path / result["filename"]).exists()


def test_empty_list_returns_error_without_file(tmp_path):
    result = write_backtest_results_csv([], tmp_path, timestamp="20260526_160000")

    assert result["success"] is False
    assert result["path"] is None
    assert result["count"] == 0
    assert result["errors"]
    assert list(tmp_path.iterdir()) == []


def test_collision_suffix_fallback(tmp_path):
    first = write_backtest_result_csv(
        _result_row(),
        tmp_path,
        ticker="LOAR",
        timeframe="1d",
        timestamp="20260526_160000",
    )
    second = write_backtest_result_csv(
        _result_row(),
        tmp_path,
        ticker="LOAR",
        timeframe="1d",
        timestamp="20260526_160000",
    )

    assert first["filename"] == "LOAR_1d_backtest_results_20260526_160000.csv"
    assert second["filename"] == "LOAR_1d_backtest_results_20260526_160000_2.csv"


def test_csv_value_safety_for_result_fields():
    row = _result_row(
        outcome="INVALID",
        realized_R=None,
        mark_to_market_close=pd.NA,
        outcome_error={"reason": "bad", "codes": [1, 2]},
    )
    list_row = _result_row(outcome="INVALID", realized_R=None, outcome_error=["first", {"code": "x"}])

    assert row["outcome_error"] == '{"codes":[1,2],"reason":"bad"}'
    assert row["mark_to_market_close"] == ""
    assert list_row["outcome_error"] == 'first; {"code":"x"}'
