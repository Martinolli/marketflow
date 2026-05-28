from __future__ import annotations

from copy import deepcopy

import pandas as pd

from marketflow.services.backtest_calibration_service import (
    normalize_outcome,
    read_backtest_results_csv,
    summarize_backtest_results_csv,
    summarize_backtest_results_folder,
    summarize_backtest_results_rows,
)


def _row(outcome="TP_FIRST", **overrides):
    row = {
        "ticker": "AAPL",
        "timeframe": "1d",
        "horizon_bars": 20,
        "tie_break_policy": "conservative",
        "wyckoff_phase": "D",
        "wyckoff_event": "LPS",
        "trend": "up",
        "outcome": outcome,
        "bars_to_hit": 3,
        "realized_R": 1.5,
        "planned_rr": 1.5,
        "outcome_error": "",
        "backtest_success": outcome != "INVALID",
    }
    row.update(overrides)
    return row


def _write_csv(path, rows):
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def test_normalize_outcomes():
    assert normalize_outcome("tp_first") == "TP_FIRST"
    assert normalize_outcome(" Sl_First ") == "SL_FIRST"
    assert normalize_outcome("neither") == "NEITHER"
    assert normalize_outcome("ambiguous") == "AMBIGUOUS"
    assert normalize_outcome("unknown") == "INVALID"
    assert normalize_outcome("") == "INVALID"
    assert normalize_outcome(None) == "INVALID"


def test_one_tp_first_row_summary():
    result = summarize_backtest_results_rows([_row()])
    summary = result["summary"]

    assert result["success"] is True
    assert summary["count"] == 1
    assert summary["valid_count"] == 1
    assert summary["tp_first_count"] == 1
    assert summary["tp_first_rate"] == 1.0
    assert summary["mean_realized_R"] == 1.5
    assert summary["mean_bars_to_hit"] == 3
    assert summary["mean_planned_rr"] == 1.5
    assert summary["small_sample_warning"] == "small_sample"


def test_one_sl_first_row_summary():
    result = summarize_backtest_results_rows([_row("SL_FIRST", realized_R=-1.0)])
    summary = result["summary"]

    assert summary["valid_count"] == 1
    assert summary["sl_first_count"] == 1
    assert summary["mean_realized_R"] == -1.0


def test_neither_counted_as_valid():
    result = summarize_backtest_results_rows([_row("NEITHER", bars_to_hit="", realized_R=0.2)])
    summary = result["summary"]

    assert summary["valid_count"] == 1
    assert summary["neither_count"] == 1
    assert summary["invalid_count"] == 0


def test_ambiguous_counted_as_valid():
    result = summarize_backtest_results_rows([_row("AMBIGUOUS", realized_R="")])
    summary = result["summary"]

    assert summary["valid_count"] == 1
    assert summary["ambiguous_count"] == 1
    assert summary["invalid_count"] == 0


def test_invalid_counted_separately_with_reason():
    result = summarize_backtest_results_rows(
        [_row("INVALID", realized_R="", outcome_error="missing signal location")]
    )
    summary = result["summary"]

    assert summary["invalid_count"] == 1
    assert summary["invalid_rate"] == 1.0
    assert result["invalid_reason_rows"] == [
        {"reason": "missing signal location", "count": 1, "rate": 1.0}
    ]


def test_win_loss_ratio():
    result = summarize_backtest_results_rows(
        [
            _row("TP_FIRST"),
            _row("TP_FIRST", ticker="AI"),
            _row("SL_FIRST", realized_R=-1.0),
        ]
    )

    assert result["summary"]["win_loss_ratio"] == 2.0


def test_grouped_summary_by_ticker_timeframe_horizon_tie_break():
    result = summarize_backtest_results_rows(
        [
            _row("TP_FIRST", ticker="AAPL", timeframe="1d", horizon_bars=20),
            _row("SL_FIRST", ticker="AI", timeframe="1h", horizon_bars=80, realized_R=-1.0),
            _row("NEITHER", ticker="AAPL", timeframe="1d", horizon_bars=20, realized_R=0.0),
        ]
    )
    grouped = {row["group_key"]: row for row in result["grouped_summary_rows"]}

    assert grouped["AAPL|1d|20|conservative"]["count"] == 2
    assert grouped["AAPL|1d|20|conservative"]["tp_first_count"] == 1
    assert grouped["AI|1h|80|conservative"]["count"] == 1
    assert grouped["AI|1h|80|conservative"]["sl_first_count"] == 1


def test_missing_requested_group_columns_warns_and_returns_no_groups():
    result = summarize_backtest_results_rows([_row()], group_columns=("missing_group",))

    assert result["grouped_summary_rows"] == []
    assert any("missing_group" in warning for warning in result["warnings"])
    assert any("No requested group columns" in warning for warning in result["warnings"])


def test_read_csv_success(tmp_path):
    path = _write_csv(tmp_path / "AAPL_1d_backtest_results_20260528.csv", [_row()])

    result = read_backtest_results_csv(path)

    assert result["success"] is True
    assert result["count"] == 1
    assert result["rows"][0]["outcome"] == "TP_FIRST"


def test_read_missing_csv_fails(tmp_path):
    result = read_backtest_results_csv(tmp_path / "missing.csv")

    assert result["success"] is False
    assert result["errors"]


def test_summarize_csv_convenience(tmp_path):
    path = _write_csv(tmp_path / "AAPL_1d_backtest_results_20260528.csv", [_row()])

    result = summarize_backtest_results_csv(path)

    assert result["success"] is True
    assert result["path"] == str(path)
    assert result["read_result"]["count"] == 1
    assert result["summary"]["tp_first_count"] == 1


def test_summarize_folder_discovers_only_backtest_results_csv(tmp_path):
    result_path = _write_csv(tmp_path / "AAPL_1d_backtest_results_20260528.csv", [_row()])
    _write_csv(tmp_path / "AAPL_1d.csv", [_row()])
    _write_csv(tmp_path / "AAPL_1d_backtest_candidates_20260528.csv", [_row()])

    result = summarize_backtest_results_folder(tmp_path)

    assert result["success"] is True
    assert result["file_count"] == 1
    assert result["read_count"] == 1
    assert result["source_result_files"] == [str(result_path)]
    assert result["summary"]["count"] == 1


def test_empty_rows_warning():
    result = summarize_backtest_results_rows([])

    assert result["success"] is False
    assert result["count"] == 0
    assert "No backtest result rows to summarize." in result["warnings"]


def test_no_mutation_of_input_rows():
    rows = [_row(), _row("SL_FIRST", realized_R=-1.0)]
    original = deepcopy(rows)

    summarize_backtest_results_rows(rows)

    assert rows == original
