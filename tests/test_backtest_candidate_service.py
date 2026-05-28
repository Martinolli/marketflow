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
    enrich_candidate_snapshot_signal_location,
    locate_candidate_in_source_csv,
    normalize_candidate_snapshot,
    validate_candidate_snapshot,
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


def _write_csv(tmp_path, rows, filename="LOAR_1d_wyckoff_annotated.csv"):
    path = tmp_path / filename
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


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


def test_explicit_row_index_enriches_timestamp(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {"Date": "2026-01-01", "close": 60},
            {"Date": "2026-01-02", "close": 62.34},
        ],
    )

    result = build_candidate_snapshot_from_strategy_candidate(
        _strategy_candidate(csv=str(csv_path), signal_row_index=1, signal_timestamp=None)
    )

    assert result["success"] is True
    assert result["snapshot"]["signal_row_index"] == 1
    assert result["snapshot"]["signal_timestamp"] == "2026-01-02"
    assert result["snapshot"]["signal_timestamp_source"] == "Date"
    assert result["signal_location_enrichment"]["method"] == "explicit_row_index"
    assert result["validation"]["status"] == VALIDATION_VALID


def test_explicit_timestamp_finds_row_index(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {"timestamp": "2026-01-01", "close": 60},
            {"timestamp": "2026-01-02", "close": 62.34},
        ],
    )

    result = build_candidate_snapshot_from_strategy_candidate(
        _strategy_candidate(csv=str(csv_path), signal_row_index=None, signal_timestamp="2026-01-02")
    )

    assert result["success"] is True
    assert result["snapshot"]["signal_row_index"] == 1
    assert result["snapshot"]["signal_timestamp"] == "2026-01-02"
    assert result["snapshot"]["signal_timestamp_source"] == "timestamp"
    assert result["signal_location_enrichment"]["method"] == "explicit_timestamp"


def test_latest_row_fallback_enriches_row_index_and_timestamp(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {"datetime": "2026-01-01", "close": 60},
            {"datetime": "2026-01-02", "close": 61},
            {"datetime": "2026-01-03", "close": 62.34},
        ],
    )

    result = build_candidate_snapshot_from_strategy_candidate(
        _strategy_candidate(csv=str(csv_path), signal_row_index=None, signal_timestamp=None)
    )

    assert result["success"] is True
    assert result["snapshot"]["signal_row_index"] == 2
    assert result["snapshot"]["signal_timestamp"] == "2026-01-03"
    assert result["snapshot"]["signal_timestamp_source"] == "datetime"
    assert result["signal_location_enrichment"]["method"] == "latest_row_assumption"
    assert "signal location inferred from latest source row assumption" in result["validation"]["warnings"]


def test_latest_row_fallback_disabled_leaves_missing_without_other_match(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {"timestamp": "2026-01-01", "open": 60},
            {"timestamp": "2026-01-02", "open": 61},
        ],
    )
    snapshot = normalize_candidate_snapshot(
        _strategy_candidate(csv=str(csv_path), signal_row_index=None, signal_timestamp=None)
    )

    enrichment = enrich_candidate_snapshot_signal_location(snapshot, latest_row_fallback=False)

    assert enrichment["success"] is False
    assert enrichment["match"]["matched"] is False
    assert enrichment["snapshot"]["signal_row_index"] is None
    assert enrichment["snapshot"]["signal_timestamp"] is None


def test_ambiguous_timestamp_does_not_enrich_row_index(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {"timestamp": "2026-01-01", "close": 60},
            {"timestamp": "2026-01-01", "close": 62.34},
        ],
    )
    snapshot = normalize_candidate_snapshot(
        _strategy_candidate(csv=str(csv_path), signal_row_index=None, signal_timestamp="2026-01-01")
    )

    enrichment = enrich_candidate_snapshot_signal_location(snapshot)

    assert enrichment["success"] is False
    assert enrichment["snapshot"]["signal_row_index"] is None
    assert "ambiguous timestamp match" in enrichment["match"]["warnings"][0]


def test_missing_source_csv_leaves_missing_location_and_reports_error():
    snapshot = normalize_candidate_snapshot(
        _strategy_candidate(csv=None, source_csv=None, signal_row_index=None, signal_timestamp=None)
    )

    enrichment = enrich_candidate_snapshot_signal_location(snapshot)
    validation = validate_candidate_snapshot(enrichment["snapshot"])

    assert enrichment["success"] is False
    assert enrichment["match"]["errors"]
    assert validation["status"] == VALIDATION_MISSING_SOURCE_CSV


def test_timestampless_csv_enriches_row_index_only(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {"close": 60},
            {"close": 62.34},
        ],
    )

    result = build_candidate_snapshot_from_strategy_candidate(
        _strategy_candidate(csv=str(csv_path), signal_row_index=1, signal_timestamp=None)
    )

    assert result["success"] is True
    assert result["snapshot"]["signal_row_index"] == 1
    assert result["snapshot"]["signal_timestamp"] is None
    assert result["validation"]["status"] == VALIDATION_VALID


def test_invalid_levels_remain_invalid_after_location_enrichment(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {"timestamp": "2026-01-01", "close": 62.34},
        ],
    )

    result = build_candidate_snapshot_from_strategy_candidate(
        _strategy_candidate(csv=str(csv_path), signal_row_index=None, signal_timestamp=None, sl=63)
    )

    assert result["snapshot"]["signal_row_index"] == 0
    assert result["success"] is False
    assert result["validation"]["status"] == VALIDATION_INVALID_LEVELS


def test_signal_location_enrichment_does_not_mutate_input_candidate(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {"timestamp": "2026-01-01", "close": 62.34},
        ],
    )
    candidate = _strategy_candidate(csv=str(csv_path), signal_row_index=None, signal_timestamp=None)
    original = dict(candidate)

    build_candidate_snapshot_from_strategy_candidate(candidate)

    assert candidate == original
    assert "signal_timestamp_source" not in candidate


def test_recent_context_match_when_latest_row_fallback_disabled(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {
                "timestamp": "2026-01-01",
                "close": 60.0,
                "wyckoff_phase": "C",
                "wyckoff_confirmed_event": "TEST",
                "trend": "flat",
            },
            {
                "timestamp": "2026-01-02",
                "close": 62.34,
                "wyckoff_phase": "D",
                "wyckoff_confirmed_event": "SPRING_WEAK",
                "trend": "Up",
            },
        ],
    )
    snapshot = normalize_candidate_snapshot(
        _strategy_candidate(csv=str(csv_path), signal_row_index=None, signal_timestamp=None)
    )

    match = locate_candidate_in_source_csv(snapshot, latest_row_fallback=False)

    assert match["matched"] is True
    assert match["method"] == "recent_context_match"
    assert match["row_index"] == 1
    assert match["timestamp"] == "2026-01-02"
    assert match["confidence"] == "high"


def test_ambiguous_recent_context_match_is_rejected(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        [
            {
                "timestamp": "2026-01-01",
                "close": 62.34,
                "wyckoff_phase": "D",
                "wyckoff_confirmed_event": "SPRING_WEAK",
                "trend": "Up",
            },
            {
                "timestamp": "2026-01-02",
                "close": 62.34,
                "wyckoff_phase": "D",
                "wyckoff_confirmed_event": "SPRING_WEAK",
                "trend": "Up",
            },
        ],
    )
    snapshot = normalize_candidate_snapshot(
        _strategy_candidate(csv=str(csv_path), signal_row_index=None, signal_timestamp=None)
    )

    match = locate_candidate_in_source_csv(snapshot, latest_row_fallback=False)

    assert match["matched"] is False
    assert match["row_index"] is None
    assert "ambiguous recent context match" in match["warnings"][0]
