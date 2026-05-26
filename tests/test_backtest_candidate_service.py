from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

from marketflow.backtesting.schemas import CandidateSnapshot
from marketflow.services.backtest_candidate_service import (
    VALIDATION_INVALID_LEVELS,
    VALIDATION_MISSING_LEVELS,
    VALIDATION_MISSING_SIGNAL_LOCATION,
    VALIDATION_MISSING_SOURCE_CSV,
    VALIDATION_UNSUPPORTED_DIRECTION,
    VALIDATION_VALID,
    build_candidate_snapshot_from_strategy_candidate,
    candidate_snapshot_dict_to_dataclass,
    normalize_candidate_snapshot,
)


def _strategy_candidate(**overrides):
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


def test_normalize_selected_strategy_ranking_style_candidate():
    snapshot = normalize_candidate_snapshot(_strategy_candidate())

    assert snapshot["ticker"] == "LOAR"
    assert snapshot["timeframe"] == "1d"
    assert snapshot["source_csv"] == "LOAR_1d_wyckoff_annotated.csv"
    assert snapshot["entry"] == 62.34
    assert snapshot["stop_loss"] == 55.76
    assert snapshot["take_profit"] == 72.20
    assert snapshot["risk_reward"] == 1.5
    assert snapshot["strategy_score"] == 73.33
    assert snapshot["wyckoff_phase"] == "D"
    assert snapshot["wyckoff_event"] == "SPRING_WEAK"
    assert snapshot["direction"] == "long"
    assert snapshot["candidate_source"] == "strategy_ranking"


def test_infers_ticker_and_timeframe_from_csv_when_missing():
    snapshot = normalize_candidate_snapshot(
        {
            "csv": "IONQ_1w_wyckoff_annotated.csv",
            "entry": 100,
            "sl": 95,
            "tp": 110,
            "signal_timestamp": "2026-01-01",
        }
    )

    assert snapshot["ticker"] == "IONQ"
    assert snapshot["timeframe"] == "1w"


def test_computes_risk_reward_when_missing_and_levels_valid():
    snapshot = normalize_candidate_snapshot(
        {
            "csv": "TEST_1d.csv",
            "entry": 100,
            "sl": 95,
            "tp": 110,
            "signal_row_index": 10,
        }
    )

    assert snapshot["risk_reward"] == 2.0


def test_validate_valid_snapshot_and_build_success():
    result = build_candidate_snapshot_from_strategy_candidate(_strategy_candidate())

    assert result["success"] is True
    assert result["validation"]["status"] == VALIDATION_VALID
    assert result["validation"]["errors"] == []


def test_missing_source_csv_is_invalid():
    result = build_candidate_snapshot_from_strategy_candidate(_strategy_candidate(csv=None, source_csv=None))

    assert result["success"] is False
    assert result["validation"]["status"] == VALIDATION_MISSING_SOURCE_CSV


def test_missing_levels_is_invalid():
    result = build_candidate_snapshot_from_strategy_candidate(_strategy_candidate(sl=None, stop_loss=None))

    assert result["success"] is False
    assert result["validation"]["status"] == VALIDATION_MISSING_LEVELS


def test_missing_signal_location_is_invalid():
    result = build_candidate_snapshot_from_strategy_candidate(
        _strategy_candidate(signal_row_index=None, signal_timestamp=None)
    )

    assert result["success"] is False
    assert result["validation"]["status"] == VALIDATION_MISSING_SIGNAL_LOCATION


def test_invalid_levels_are_invalid():
    result = build_candidate_snapshot_from_strategy_candidate(_strategy_candidate(sl=100))

    assert result["success"] is False
    assert result["validation"]["status"] == VALIDATION_INVALID_LEVELS

    result = build_candidate_snapshot_from_strategy_candidate(_strategy_candidate(tp=60))

    assert result["success"] is False
    assert result["validation"]["status"] == VALIDATION_INVALID_LEVELS


def test_unsupported_direction_has_highest_priority():
    result = build_candidate_snapshot_from_strategy_candidate(_strategy_candidate(direction="short", csv=None))

    assert result["success"] is False
    assert result["validation"]["status"] == VALIDATION_UNSUPPORTED_DIRECTION
    assert any("long" in error for error in result["validation"]["errors"])


def test_timestamp_source_tracks_datetime_alias():
    snapshot = normalize_candidate_snapshot(_strategy_candidate(signal_row_index=None, datetime="2026-01-01 10:30:00"))

    assert snapshot["signal_timestamp"] == "2026-01-01 10:30:00"
    assert snapshot["signal_timestamp_source"] == "datetime"


def test_dataclass_conversion_uses_schema_fields_only():
    snapshot = normalize_candidate_snapshot(_strategy_candidate())
    candidate = candidate_snapshot_dict_to_dataclass(snapshot)

    assert isinstance(candidate, CandidateSnapshot)
    assert candidate.ticker == "LOAR"
    assert candidate.timeframe == "1d"
    assert candidate.source_csv == "LOAR_1d_wyckoff_annotated.csv"
    assert candidate.entry == 62.34
    assert candidate.stop_loss == 55.76
    assert candidate.take_profit == 72.20


def test_json_safety_converts_nan_and_path_values():
    snapshot = normalize_candidate_snapshot(
        {
            "csv": Path("LOAR_1d_wyckoff_annotated.csv"),
            "entry": pd.Series([100.0]).iloc[0],
            "sl": 95.0,
            "tp": 110.0,
            "score": float("nan"),
            "signal_row_index": 5,
        }
    )

    assert snapshot["source_csv"] == "LOAR_1d_wyckoff_annotated.csv"
    assert snapshot["strategy_score"] is None
    assert not any(isinstance(value, float) and math.isnan(value) for value in snapshot.values())
