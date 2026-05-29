from __future__ import annotations

import csv
import json

from marketflow.services.artifact_service import list_report_artifacts
from marketflow.services.monte_carlo_calibration_artifact_service import (
    MONTE_CARLO_CALIBRATION_SUMMARY_KIND,
    build_monte_carlo_calibration_summary_filename,
    build_monte_carlo_calibration_summary_markdown,
    summarize_folder_to_monte_carlo_calibration_markdown,
    write_monte_carlo_calibration_summary_markdown,
)


def _calibration_result(**overrides):
    result = {
        "success": True,
        "report_dir": "reports/2026-05-29/IONQ",
        "forecast_file_count": 1,
        "actual_file_count": 1,
        "forecast_rows": [
            {
                "forecast_path": "reports/2026-05-29/IONQ/20260529_120000_mc_summary.json",
                "forecast_file": "20260529_120000_mc_summary.json",
            }
        ],
        "actual_rows": [
            {
                "actual_ticker": "IONQ",
                "actual_timeframe": "15m",
                "actual_candidate_snapshot_file": "IONQ_15m_backtest_candidates_20260529_115900.csv",
            }
        ],
        "join_rows": [
            {
                "forecast_file": "20260529_120000_mc_summary.json",
                "ticker": "IONQ",
                "timeframe": "15m",
                "model": "bootstrap",
                "mc_horizon_bars": 20,
                "actual_horizon_bars": 20,
                "actual_outcome": "TP_FIRST",
                "future_bars_available": 20,
                "join_method": "preferred",
                "eligibility_status": "eligible",
                "scoreable": True,
                "scoreable_reason": None,
            }
        ],
        "unmatched_forecasts": [],
        "unmatched_outcomes": [],
        "summary": {
            "sample_count": 1,
            "joined_count": 1,
            "scoreable_count": 1,
            "not_scoreable_count": 0,
            "eligible_count": 1,
            "not_yet_mature_count": 0,
            "horizon_mismatch_count": 0,
            "partial_future_window_count": 0,
            "invalid_count": 0,
            "ambiguous_count": 0,
            "tp_actual_rate": 1.0,
            "sl_actual_rate": 0.0,
            "neither_actual_rate": 0.0,
            "mean_forecast_tp_probability": 0.8,
            "mean_forecast_sl_probability": 0.15,
            "mean_forecast_neither_probability": 0.05,
            "brier_score_tp": 0.04,
            "brier_score_sl": 0.0225,
            "brier_score_neither": 0.0025,
            "small_sample_warning": "small_sample",
        },
        "summary_rows": [],
        "grouped_summary_rows": [
            {
                "ticker": "IONQ",
                "timeframe": "15m",
                "model": "bootstrap",
                "mc_horizon_bars": 20,
                "scoreable_count": 1,
            }
        ],
        "warnings": [],
        "errors": [],
    }
    result["summary_rows"] = [result["summary"]]
    result.update(overrides)
    return result


def _mc_payload():
    return {
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
        },
        "calibration": {"model_used": "bootstrap"},
        "join_metadata": {
            "metadata_version": "mc_join_metadata_v1",
            "ticker": "IONQ",
            "timeframe": "15m",
            "source_csv": "IONQ_15m_wyckoff_annotated.csv",
            "candidate_snapshot_file": "IONQ_15m_backtest_candidates_20260529_115900.csv",
            "signal_row_index": 831,
            "entry": 40.0,
            "stop_loss": 38.0,
            "take_profit": 42.0,
            "join_key_preferred": "IONQ|15m|IONQ_15m_backtest_candidates_20260529_115900.csv",
            "join_key_secondary": "IONQ|15m|IONQ_15m_wyckoff_annotated.csv|831",
        },
    }


def _actual_row():
    return {
        "ticker": "IONQ",
        "timeframe": "15m",
        "source_csv": "IONQ_15m_wyckoff_annotated.csv",
        "candidate_snapshot_file": "IONQ_15m_backtest_candidates_20260529_115900.csv",
        "signal_row_index": 831,
        "entry": 40.0,
        "stop_loss": 38.0,
        "take_profit": 42.0,
        "outcome": "TP_FIRST",
        "realized_R": 1.5,
        "bars_to_hit": 4,
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


def test_filename_with_ticker_timeframe():
    filename = build_monte_carlo_calibration_summary_filename(
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )

    assert filename == "IONQ_15m_monte_carlo_calibration_summary_20260529_120000.md"


def test_fallback_filename():
    filename = build_monte_carlo_calibration_summary_filename(timestamp="20260529_120000")

    assert filename == "marketflow_monte_carlo_calibration_summary_20260529_120000.md"


def test_unsafe_filename_parts_are_sanitized():
    filename = build_monte_carlo_calibration_summary_filename(
        ticker="AA/PL Inc",
        timeframe="15 m",
        timestamp="20260529_120000",
    )

    assert "/" not in filename
    assert " " not in filename
    assert filename == "AA_PL_Inc_15_m_monte_carlo_calibration_summary_20260529_120000.md"


def test_markdown_contains_required_sections():
    markdown = build_monte_carlo_calibration_summary_markdown(_calibration_result())

    assert "# MarketFlow Monte Carlo Forecast Calibration Summary" in markdown
    assert "## Metadata" in markdown
    assert "## Calibration Summary" in markdown
    assert "## Grouped Summary" in markdown
    assert "## Join Rows" in markdown
    assert "## Guardrails" in markdown


def test_markdown_includes_forecast_and_actual_files():
    markdown = build_monte_carlo_calibration_summary_markdown(_calibration_result())

    assert "20260529_120000_mc_summary.json" in markdown
    assert "IONQ_15m_backtest_candidates_20260529_115900.csv" in markdown


def test_empty_warnings_errors_show_none():
    markdown = build_monte_carlo_calibration_summary_markdown(_calibration_result(warnings=[], errors=[]))

    assert "## Warnings\n\n_None._" in markdown
    assert "## Errors\n\n_None._" in markdown


def test_warnings_errors_render_bullet_lists():
    markdown = build_monte_carlo_calibration_summary_markdown(
        _calibration_result(warnings=["small sample"], errors=["bad input"])
    )

    assert "## Warnings\n\n- small sample" in markdown
    assert "## Errors\n\n- bad input" in markdown


def test_write_markdown_file_success(tmp_path):
    result = write_monte_carlo_calibration_summary_markdown(
        _calibration_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )

    assert result["success"] is True
    assert result["kind"] == MONTE_CARLO_CALIBRATION_SUMMARY_KIND
    path = tmp_path / result["filename"]
    assert path.exists()
    assert "# MarketFlow Monte Carlo Forecast Calibration Summary" in path.read_text(encoding="utf-8")


def test_collision_suffix(tmp_path):
    first = write_monte_carlo_calibration_summary_markdown(
        _calibration_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )
    second = write_monte_carlo_calibration_summary_markdown(
        _calibration_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )

    assert first["filename"] == "IONQ_15m_monte_carlo_calibration_summary_20260529_120000.md"
    assert second["filename"] == "IONQ_15m_monte_carlo_calibration_summary_20260529_120000_2.md"


def test_folder_convenience_writer(tmp_path):
    mc_path = tmp_path / "20260529_120000_mc_summary.json"
    mc_path.write_text(json.dumps(_mc_payload()), encoding="utf-8")
    result_path = tmp_path / "IONQ_15m_backtest_results_20260529_120010.csv"
    actual = _actual_row()
    with result_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(actual.keys()))
        writer.writeheader()
        writer.writerow(actual)

    result = summarize_folder_to_monte_carlo_calibration_markdown(
        tmp_path,
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )

    assert result["success"] is True
    assert (tmp_path / result["filename"]).exists()
    assert result["calibration_result"]["join_rows"]
    assert result["calibration_result"]["summary_rows"]


def test_artifact_classification(tmp_path):
    path = tmp_path / "IONQ_15m_monte_carlo_calibration_summary_20260529_120000.md"
    path.write_text("# Summary", encoding="utf-8")

    artifacts = list_report_artifacts(str(tmp_path))
    artifact = next(row for row in artifacts if row["name"] == path.name)

    assert artifact["kind"] == "monte_carlo_calibration_summary_md"
    assert artifact["previewable"] is True
    assert artifact["downloadable"] is True
