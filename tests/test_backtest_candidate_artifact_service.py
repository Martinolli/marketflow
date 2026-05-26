from __future__ import annotations

import csv

import pandas as pd

from marketflow.services.backtest_candidate_artifact_service import (
    BACKTEST_CANDIDATE_COLUMNS,
    build_backtest_candidates_filename,
    candidate_snapshot_row,
    write_backtest_candidate_csv,
    write_backtest_candidates_csv,
)
from marketflow.services.backtest_candidate_service import build_candidate_snapshot_from_strategy_candidate


def _candidate(**overrides):
    candidate = {
        "ticker": "LOAR",
        "tf": "1d",
        "csv": "LOAR_1d_wyckoff_annotated.csv",
        "close": 62.34,
        "sl": 55.76,
        "tp": 72.20,
        "rr": 1.5,
        "phase": "D",
        "event": "SPRING_WEAK",
        "trend": "Up",
        "score": 73.33,
        "signal_row_index": 200,
    }
    candidate.update(overrides)
    return candidate


def _snapshot_result(**overrides):
    return build_candidate_snapshot_from_strategy_candidate(_candidate(**overrides))


def test_filename_with_ticker_timeframe():
    filename = build_backtest_candidates_filename(ticker="LOAR", timeframe="1d", timestamp="20260526_151500")

    assert filename == "LOAR_1d_backtest_candidates_20260526_151500.csv"


def test_fallback_filename():
    filename = build_backtest_candidates_filename(timestamp="20260526_151500")

    assert filename == "marketflow_backtest_candidates_20260526_151500.csv"


def test_unsafe_filename_parts_are_sanitized():
    filename = build_backtest_candidates_filename(ticker="LO/AR Inc", timeframe="1 d", timestamp="20260526_151500")

    assert "/" not in filename
    assert " " not in filename
    assert filename == "LO_AR_Inc_1_d_backtest_candidates_20260526_151500.csv"


def test_row_conversion_valid_snapshot_preserves_contract():
    result = _snapshot_result()
    row = candidate_snapshot_row(result, created_at="2026-05-26 15:15:00")

    assert list(row.keys()) == BACKTEST_CANDIDATE_COLUMNS
    assert row["snapshot_success"] is True
    assert row["validation_status"] == "valid"
    assert row["validation_errors"] == ""
    assert row["entry"] == 62.34
    assert row["stop_loss"] == 55.76
    assert row["take_profit"] == 72.20


def test_row_conversion_invalid_snapshot_serializes_errors():
    result = _snapshot_result(csv=None, signal_row_index=None)
    row = candidate_snapshot_row(result, created_at="2026-05-26 15:15:00")

    assert row["snapshot_success"] is False
    assert row["validation_status"] == "missing_source_csv"
    assert "Missing source_csv." in row["validation_errors"]
    assert "Missing signal_row_index or signal_timestamp." in row["validation_errors"]


def test_write_one_snapshot(tmp_path):
    result = write_backtest_candidate_csv(
        _snapshot_result(),
        tmp_path,
        ticker="LOAR",
        timeframe="1d",
        timestamp="20260526_151500",
    )

    assert result["success"] is True
    assert result["count"] == 1
    assert result["valid_count"] == 1
    assert result["invalid_count"] == 0

    path = tmp_path / result["filename"]
    assert path.exists()
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    assert list(rows[0].keys()) == BACKTEST_CANDIDATE_COLUMNS
    assert rows[0]["validation_status"] == "valid"


def test_write_mixed_valid_and_invalid_snapshots(tmp_path):
    result = write_backtest_candidates_csv(
        [_snapshot_result(), _snapshot_result(csv=None)],
        tmp_path,
        ticker="LOAR",
        timeframe="1d",
        timestamp="20260526_151500",
    )

    assert result["success"] is True
    assert result["count"] == 2
    assert result["valid_count"] == 1
    assert result["invalid_count"] == 1
    assert (tmp_path / result["filename"]).exists()


def test_empty_list_returns_error_without_file(tmp_path):
    result = write_backtest_candidates_csv([], tmp_path, timestamp="20260526_151500")

    assert result["success"] is False
    assert result["path"] is None
    assert result["count"] == 0
    assert result["errors"]
    assert list(tmp_path.iterdir()) == []


def test_collision_suffix_fallback(tmp_path):
    first = write_backtest_candidate_csv(
        _snapshot_result(),
        tmp_path,
        ticker="LOAR",
        timeframe="1d",
        timestamp="20260526_151500",
    )
    second = write_backtest_candidate_csv(
        _snapshot_result(),
        tmp_path,
        ticker="LOAR",
        timeframe="1d",
        timestamp="20260526_151500",
    )

    assert first["filename"] == "LOAR_1d_backtest_candidates_20260526_151500.csv"
    assert second["filename"] == "LOAR_1d_backtest_candidates_20260526_151500_2.csv"


def test_csv_value_safety_for_validation_warnings_and_dicts():
    row = candidate_snapshot_row(
        {
            "success": True,
            "snapshot": {
                "ticker": "LOAR",
                "timeframe": "1d",
                "source_csv": "LOAR_1d.csv",
                "entry": 100,
                "stop_loss": 95,
                "take_profit": 110,
                "strategy_score": pd.Series([72.5]).iloc[0],
            },
            "validation": {
                "status": "valid",
                "errors": [],
                "warnings": ["first warning", "second warning"],
                "extra": {"ignored": True},
            },
        }
    )

    assert row["validation_warnings"] == "first warning; second warning"
    assert row["strategy_score"] == 72.5
