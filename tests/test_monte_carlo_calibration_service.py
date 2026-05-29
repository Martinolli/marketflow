from __future__ import annotations

import csv
import json
from copy import deepcopy

import pytest

from marketflow.services.monte_carlo_calibration_service import (
    build_forecast_actual_join_rows,
    build_joined_calibration_row,
    normalize_actual_outcome_row,
    read_monte_carlo_forecast_artifact,
    summarize_forecast_calibration_rows,
    summarize_monte_carlo_calibration_folder,
)


def _mc_payload(**overrides):
    payload = {
        "csv": "IONQ_15m_wyckoff_annotated.csv",
        "tf": "15m",
        "params": {
            "tp": 42.0,
            "sl": 38.0,
            "entry": 40.0,
            "horizon_bars": 20,
            "model": "bootstrap",
            "paths": 30000,
            "block_len": 8,
            "seed": 42,
        },
        "metrics_from_now": {
            "pop_tp_first": 0.8,
            "p_sl_first": 0.15,
            "p_neither": 0.05,
            "R_mean": 0.55,
            "R_p50": 1.0,
            "R_p05": -1.0,
            "R_p95": 1.0,
            "t_hit_tp_median": 7,
            "t_hit_sl_median": 9,
        },
        "calibration": {
            "mu_bar": 0.001,
            "sigma_bar": 0.02,
            "model_used": "bootstrap",
        },
        "join_metadata": {
            "metadata_version": "mc_join_metadata_v1",
            "ticker": "IONQ",
            "timeframe": "15m",
            "source_csv": "IONQ_15m_wyckoff_annotated.csv",
            "source_csv_path": r"C:\reports\IONQ_15m_wyckoff_annotated.csv",
            "source_report_dir": r"C:\reports",
            "candidate_snapshot_file": "IONQ_15m_backtest_candidates_20260529_075913.csv",
            "signal_row_index": 831,
            "signal_timestamp": "2026-05-28 20:00:00+00:00",
            "entry": 40.0,
            "stop_loss": 38.0,
            "take_profit": 42.0,
            "risk_reward": 1.5,
            "strategy_score": 72.0,
            "wyckoff_phase": "D",
            "wyckoff_event": "SOS",
            "trend": "up",
            "join_key_preferred": "IONQ|15m|IONQ_15m_backtest_candidates_20260529_075913.csv",
            "join_key_secondary": "IONQ|15m|IONQ_15m_wyckoff_annotated.csv|831",
        },
        "ticker": "IONQ",
        "timeframe": "15m",
        "source_csv": "IONQ_15m_wyckoff_annotated.csv",
        "candidate_snapshot_file": "IONQ_15m_backtest_candidates_20260529_075913.csv",
    }
    payload.update(overrides)
    return payload


def _forecast_row(**overrides):
    row = {
        "forecast_path": None,
        "forecast_file": "20260529_075920_mc_summary.json",
        "ticker": "IONQ",
        "timeframe": "15m",
        "source_csv": "IONQ_15m_wyckoff_annotated.csv",
        "candidate_snapshot_file": "IONQ_15m_backtest_candidates_20260529_075913.csv",
        "signal_row_index": 831,
        "signal_timestamp": "2026-05-28 20:00:00+00:00",
        "join_key_preferred": "IONQ|15m|IONQ_15m_backtest_candidates_20260529_075913.csv",
        "join_key_secondary": "IONQ|15m|IONQ_15m_wyckoff_annotated.csv|831",
        "model": "bootstrap",
        "model_used": "bootstrap",
        "mc_horizon_bars": 20,
        "paths": 30000,
        "forecast_tp_probability": 0.8,
        "forecast_sl_probability": 0.15,
        "forecast_neither_probability": 0.05,
        "forecast_R_mean": 0.55,
        "entry": 40.0,
        "stop_loss": 38.0,
        "take_profit": 42.0,
    }
    row.update(overrides)
    return row


def _actual_raw(**overrides):
    row = {
        "ticker": "IONQ",
        "timeframe": "15m",
        "source_csv": r"C:\reports\IONQ_15m_wyckoff_annotated.csv",
        "candidate_snapshot_file": "IONQ_15m_backtest_candidates_20260529_075913.csv",
        "signal_row_index": 831,
        "signal_timestamp": "2026-05-28 20:00:00+00:00",
        "entry": 40.0,
        "stop_loss": 38.0,
        "take_profit": 42.0,
        "outcome": "TP_FIRST",
        "realized_R": 1.5,
        "bars_to_hit": 5,
        "tie_break_policy": "conservative",
        "horizon_bars": 20,
        "future_bars_available": 20,
        "evaluation_window_start_index": 832,
        "evaluation_window_end_index": 851,
        "signal_is_latest_row": False,
        "neither_reason": "",
        "outcome_error": "",
        "backtest_success": True,
    }
    row.update(overrides)
    return row


def _actual_row(**overrides):
    return normalize_actual_outcome_row(_actual_raw(**overrides))


def test_read_normalize_mc_forecast_artifact_with_join_metadata(tmp_path):
    path = tmp_path / "20260529_075920_mc_summary.json"
    path.write_text(json.dumps(_mc_payload()), encoding="utf-8")

    result = read_monte_carlo_forecast_artifact(path)

    assert result["success"] is True
    row = result["forecast_row"]
    assert row["ticker"] == "IONQ"
    assert row["timeframe"] == "15m"
    assert row["source_csv"] == "IONQ_15m_wyckoff_annotated.csv"
    assert row["candidate_snapshot_file"] == "IONQ_15m_backtest_candidates_20260529_075913.csv"
    assert row["signal_row_index"] == 831
    assert row["forecast_tp_probability"] == 0.8
    assert row["forecast_sl_probability"] == 0.15
    assert row["forecast_neither_probability"] == 0.05
    assert row["forecast_file"] == path.name


def test_normalize_actual_outcome_row_generates_join_keys_with_source_basename():
    row = normalize_actual_outcome_row(
        _actual_raw(
            ticker="AAAU",
            timeframe="30m",
            source_csv=r"C:\reports\AAAU_30m_wyckoff_annotated.csv",
            candidate_snapshot_file="AAAU_30m_backtest_candidates_20260529_080722.csv",
            signal_row_index="303",
        )
    )

    assert row["actual_join_key_preferred"] == "AAAU|30m|AAAU_30m_backtest_candidates_20260529_080722.csv"
    assert row["actual_join_key_secondary"] == "AAAU|30m|AAAU_30m_wyckoff_annotated.csv|303"


def test_preferred_join_works():
    result = build_forecast_actual_join_rows([_forecast_row()], [_actual_row()])

    assert len(result["join_rows"]) == 1
    assert result["join_rows"][0]["join_method"] == "preferred"


def test_secondary_join_works_when_preferred_key_missing():
    forecast = _forecast_row(join_key_preferred=None)
    actual = _actual_row()

    result = build_forecast_actual_join_rows([forecast], [actual])

    assert len(result["join_rows"]) == 1
    assert result["join_rows"][0]["join_method"] == "secondary"


def test_ambiguous_preferred_join_rejected():
    result = build_forecast_actual_join_rows([_forecast_row()], [_actual_row(), _actual_row(actual_realized_R=0.5)])

    assert result["join_rows"] == []
    assert result["unmatched_forecasts"][0]["join_status"] == "ambiguous"
    assert "Ambiguous exact join" in result["unmatched_forecasts"][0]["join_warning"]


def test_fallback_level_join_works_only_when_unambiguous():
    forecast = _forecast_row(join_key_preferred=None, join_key_secondary=None)
    actual = _actual_row(actual_candidate_snapshot_file=None)
    actual["actual_join_key_preferred"] = None
    actual["actual_join_key_secondary"] = None

    result = build_forecast_actual_join_rows([forecast], [actual])

    assert len(result["join_rows"]) == 1
    assert result["join_rows"][0]["join_method"] == "fallback_levels"


def test_fallback_ambiguous_rejected():
    forecast = _forecast_row(join_key_preferred=None, join_key_secondary=None)
    actual_one = _actual_row()
    actual_two = _actual_row(signal_timestamp="2026-05-28 20:15:00+00:00")
    actual_one["actual_join_key_preferred"] = None
    actual_one["actual_join_key_secondary"] = None
    actual_two["actual_join_key_preferred"] = None
    actual_two["actual_join_key_secondary"] = None

    result = build_forecast_actual_join_rows([forecast], [actual_one, actual_two])

    assert result["join_rows"] == []
    assert result["unmatched_forecasts"][0]["join_status"] == "ambiguous"
    assert "fallback" in result["unmatched_forecasts"][0]["join_warning"]


def test_no_future_bars_classified_not_yet_mature():
    row = build_joined_calibration_row(
        _forecast_row(),
        _actual_row(outcome="NEITHER", future_bars_available=0, neither_reason="no_future_bars_available"),
        join_method="preferred",
    )

    assert row["scoreable"] is False
    assert row["eligibility_status"] == "not_yet_mature"
    assert row["scoreable_reason"] == "no_future_bars_available"


def test_horizon_mismatch_classified_not_scoreable():
    row = build_joined_calibration_row(
        _forecast_row(mc_horizon_bars=50),
        _actual_row(horizon_bars=20),
        join_method="preferred",
    )

    assert row["scoreable"] is False
    assert row["horizon_match"] is False
    assert row["eligibility_status"] == "horizon_mismatch"


def test_partial_future_window_not_scoreable():
    row = build_joined_calibration_row(
        _forecast_row(),
        _actual_row(future_bars_available=5, horizon_bars=20),
        join_method="preferred",
    )

    assert row["scoreable"] is False
    assert row["eligibility_status"] == "partial_future_window"


def test_full_horizon_tp_first_eligible():
    row = build_joined_calibration_row(_forecast_row(), _actual_row(outcome="TP_FIRST"), join_method="preferred")

    assert row["scoreable"] is True
    assert row["eligibility_status"] == "eligible"
    assert row["actual_tp_event"] == 1


def test_full_horizon_sl_first_eligible():
    row = build_joined_calibration_row(
        _forecast_row(),
        _actual_row(outcome="SL_FIRST", realized_R=-1.0),
        join_method="preferred",
    )

    assert row["scoreable"] is True
    assert row["actual_sl_event"] == 1


def test_full_horizon_neither_eligible():
    row = build_joined_calibration_row(
        _forecast_row(),
        _actual_row(outcome="NEITHER", realized_R=0.2),
        join_method="preferred",
    )

    assert row["scoreable"] is True
    assert row["actual_neither_event"] == 1


def test_ambiguous_not_scoreable():
    row = build_joined_calibration_row(_forecast_row(), _actual_row(outcome="AMBIGUOUS"), join_method="preferred")

    assert row["scoreable"] is False
    assert row["eligibility_status"] == "ambiguous"


def test_invalid_not_scoreable():
    row = build_joined_calibration_row(
        _forecast_row(),
        _actual_row(outcome="INVALID", backtest_success=False, outcome_error="bad row"),
        join_method="preferred",
    )

    assert row["scoreable"] is False
    assert row["eligibility_status"] == "invalid"


def test_brier_score_calculation():
    row = build_joined_calibration_row(
        _forecast_row(forecast_tp_probability=0.8),
        _actual_row(outcome="TP_FIRST"),
        join_method="preferred",
    )

    result = summarize_forecast_calibration_rows([row])

    assert result["summary"]["brier_score_tp"] == pytest.approx(0.04)


def test_no_scoreable_rows_returns_none_metrics():
    row = build_joined_calibration_row(
        _forecast_row(),
        _actual_row(outcome="NEITHER", future_bars_available=0, neither_reason="no_future_bars_available"),
        join_method="preferred",
    )

    result = summarize_forecast_calibration_rows([row])

    assert result["summary"]["scoreable_count"] == 0
    assert result["summary"]["brier_score_tp"] is None
    assert result["summary"]["brier_score_sl"] is None
    assert result["summary"]["brier_score_neither"] is None


def test_grouped_summary_by_default_columns():
    ionq = build_joined_calibration_row(_forecast_row(ticker="IONQ"), _actual_row(ticker="IONQ"), join_method="preferred")
    aaau = build_joined_calibration_row(
        _forecast_row(
            ticker="AAAU",
            timeframe="30m",
            source_csv="AAAU_30m_wyckoff_annotated.csv",
            candidate_snapshot_file="AAAU_30m_backtest_candidates.csv",
            join_key_preferred="AAAU|30m|AAAU_30m_backtest_candidates.csv",
            join_key_secondary="AAAU|30m|AAAU_30m_wyckoff_annotated.csv|303",
            signal_row_index=303,
        ),
        _actual_row(
            ticker="AAAU",
            timeframe="30m",
            source_csv="AAAU_30m_wyckoff_annotated.csv",
            candidate_snapshot_file="AAAU_30m_backtest_candidates.csv",
            signal_row_index=303,
        ),
        join_method="preferred",
    )

    result = summarize_forecast_calibration_rows([ionq, aaau])

    assert len(result["grouped_summary_rows"]) == 2
    assert {row["ticker"] for row in result["grouped_summary_rows"]} == {"IONQ", "AAAU"}


def test_folder_summary_discovers_mc_json_and_result_csv_only(tmp_path):
    mc_path = tmp_path / "20260529_075920_mc_summary.json"
    mc_path.write_text(json.dumps(_mc_payload()), encoding="utf-8")
    csv_path = tmp_path / "IONQ_15m_backtest_results_20260529_075921.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(_actual_raw().keys()))
        writer.writeheader()
        writer.writerow(_actual_raw())
    (tmp_path / "ignore.txt").write_text("ignore", encoding="utf-8")
    (tmp_path / "other.json").write_text("{}", encoding="utf-8")

    result = summarize_monte_carlo_calibration_folder(tmp_path)

    assert result["success"] is True
    assert result["forecast_file_count"] == 1
    assert result["actual_file_count"] == 1
    assert len(result["join_rows"]) == 1
    assert result["summary"]["joined_count"] == 1


def test_join_and_summary_do_not_mutate_input_rows():
    forecast = _forecast_row()
    actual = _actual_row()
    original_forecast = deepcopy(forecast)
    original_actual = deepcopy(actual)

    result = build_forecast_actual_join_rows([forecast], [actual])
    summarize_forecast_calibration_rows(result["join_rows"])

    assert forecast == original_forecast
    assert actual == original_actual
