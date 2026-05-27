from __future__ import annotations

import csv

import pandas as pd

from marketflow.services.backtest_result_artifact_service import BACKTEST_RESULT_COLUMNS
from marketflow.services.backtest_result_service import (
    evaluate_candidate_snapshot_csv,
    evaluate_candidate_snapshot_csv_to_results_csv,
    evaluate_candidate_snapshot_row,
    evaluate_candidate_snapshot_rows,
    read_candidate_snapshot_csv,
)


def _ohlc_path(tmp_path, rows, name="ohlc.csv"):
    path = tmp_path / name
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def _tp_ohlc_path(tmp_path):
    return _ohlc_path(
        tmp_path,
        [
            {"timestamp": "2026-01-01", "open": 100, "high": 101, "low": 99, "close": 100},
            {"timestamp": "2026-01-02", "open": 101, "high": 111, "low": 100, "close": 110},
        ],
        name="tp.csv",
    )


def _sl_ohlc_path(tmp_path):
    return _ohlc_path(
        tmp_path,
        [
            {"timestamp": "2026-01-01", "open": 100, "high": 101, "low": 99, "close": 100},
            {"timestamp": "2026-01-02", "open": 99, "high": 101, "low": 94, "close": 96},
        ],
        name="sl.csv",
    )


def _snapshot_row(source_csv, **overrides):
    row = {
        "ticker": "LOAR",
        "timeframe": "1d",
        "source_csv": str(source_csv),
        "source_report_dir": str(source_csv.parent) if hasattr(source_csv, "parent") else "",
        "signal_timestamp": "",
        "signal_timestamp_source": "row_index",
        "signal_row_index": 0,
        "entry": 100.0,
        "stop_loss": 95.0,
        "take_profit": 110.0,
        "risk_reward": 2.0,
        "strategy_score": 72.5,
        "wyckoff_phase": "D",
        "wyckoff_event": "SOS",
        "trend": "Up",
        "candidate_source": "strategy_ranking",
        "report_date": "2026-05-27",
        "direction": "long",
        "source_strategy_rank": 1,
        "validation_status": "valid",
        "snapshot_success": True,
    }
    row.update(overrides)
    return row


def _candidate_csv(tmp_path, rows, name="LOAR_1d_backtest_candidates_20260527_120000.csv"):
    path = tmp_path / name
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def test_read_candidate_snapshot_csv_success(tmp_path):
    ohlc_path = _tp_ohlc_path(tmp_path)
    candidates_path = _candidate_csv(tmp_path, [_snapshot_row(ohlc_path)])

    result = read_candidate_snapshot_csv(candidates_path)

    assert result["success"] is True
    assert result["count"] == 1
    assert result["rows"][0]["ticker"] == "LOAR"


def test_read_candidate_snapshot_csv_missing_file(tmp_path):
    result = read_candidate_snapshot_csv(tmp_path / "missing.csv")

    assert result["success"] is False
    assert result["errors"]


def test_evaluate_invalid_snapshot_row_writes_invalid_row(tmp_path):
    row = _snapshot_row(_tp_ohlc_path(tmp_path), snapshot_success=False)

    result = evaluate_candidate_snapshot_row(row)

    assert result["success"] is False
    assert result["result_row"]["outcome"] == "INVALID"
    assert result["result_row"]["backtest_success"] is False
    assert "candidate snapshot is not valid" in result["result_row"]["outcome_error"]


def test_evaluate_rows_with_invalid_rows_enabled(tmp_path):
    row = _snapshot_row(_tp_ohlc_path(tmp_path), signal_row_index="", signal_timestamp="")

    result = evaluate_candidate_snapshot_rows([row], write_invalid_rows=True)

    assert len(result["result_rows"]) == 1
    assert result["invalid_count"] == 1
    assert result["skipped_count"] == 0


def test_evaluate_rows_with_invalid_rows_disabled(tmp_path):
    row = _snapshot_row(_tp_ohlc_path(tmp_path), signal_row_index="", signal_timestamp="")

    result = evaluate_candidate_snapshot_rows([row], write_invalid_rows=False)

    assert len(result["result_rows"]) == 0
    assert result["invalid_count"] == 0
    assert result["skipped_count"] == 1


def test_evaluate_valid_snapshot_row_tp_first(tmp_path):
    row = _snapshot_row(_tp_ohlc_path(tmp_path))

    result = evaluate_candidate_snapshot_row(row, horizon_bars=2)

    assert result["success"] is True
    assert result["result_row"]["outcome"] == "TP_FIRST"
    assert result["result_row"]["backtest_success"] is True
    assert result["result_row"]["ticker"] == "LOAR"
    assert result["result_row"]["entry"] == 100.0


def test_evaluate_valid_snapshot_row_sl_first(tmp_path):
    row = _snapshot_row(_sl_ohlc_path(tmp_path))

    result = evaluate_candidate_snapshot_row(row, horizon_bars=2)

    assert result["success"] is True
    assert result["result_row"]["outcome"] == "SL_FIRST"
    assert result["result_row"]["backtest_success"] is True
    assert result["result_row"]["realized_R"] == -1.0


def test_evaluate_candidate_snapshot_csv(tmp_path):
    ohlc_path = _tp_ohlc_path(tmp_path)
    candidates_path = _candidate_csv(tmp_path, [_snapshot_row(ohlc_path)])

    result = evaluate_candidate_snapshot_csv(candidates_path, horizon_bars=2)

    assert result["success"] is True
    assert len(result["result_rows"]) == 1
    assert result["result_rows"][0]["outcome"] == "TP_FIRST"


def test_evaluate_candidate_snapshot_csv_to_results_csv(tmp_path):
    ohlc_path = _tp_ohlc_path(tmp_path)
    candidates_path = _candidate_csv(tmp_path, [_snapshot_row(ohlc_path)])

    result = evaluate_candidate_snapshot_csv_to_results_csv(
        candidates_path,
        horizon_bars=2,
        timestamp="20260527_120100",
    )

    assert result["success"] is True
    assert result["filename"] == "LOAR_1d_backtest_results_20260527_120100.csv"

    path = tmp_path / result["filename"]
    assert path.exists()
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    assert list(rows[0].keys()) == BACKTEST_RESULT_COLUMNS
    assert rows[0]["outcome"] == "TP_FIRST"


def test_missing_source_csv_creates_invalid_result(tmp_path):
    missing_ohlc_path = tmp_path / "missing_ohlc.csv"
    row = _snapshot_row(missing_ohlc_path)

    result = evaluate_candidate_snapshot_row(row, horizon_bars=2)

    assert result["success"] is False
    assert result["result_row"]["outcome"] == "INVALID"
    assert "Could not read CSV" in result["result_row"]["outcome_error"]


def test_candidate_snapshot_file_preserved_when_evaluating_from_csv(tmp_path):
    ohlc_path = _tp_ohlc_path(tmp_path)
    candidates_path = _candidate_csv(tmp_path, [_snapshot_row(ohlc_path)])

    result = evaluate_candidate_snapshot_csv(candidates_path, horizon_bars=2)

    assert result["result_rows"][0]["candidate_snapshot_file"] == candidates_path.name
