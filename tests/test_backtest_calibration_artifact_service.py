from __future__ import annotations

import pandas as pd

from marketflow.services.artifact_service import list_report_artifacts
from marketflow.services.backtest_calibration_artifact_service import (
    BACKTEST_CALIBRATION_SUMMARY_KIND,
    build_backtest_calibration_summary_filename,
    build_backtest_calibration_summary_markdown,
    summarize_folder_to_backtest_calibration_markdown,
    write_backtest_calibration_summary_markdown,
)


def _calibration_result(**overrides):
    result = {
        "success": True,
        "report_dir": "reports/AAPL",
        "source_result_files": ["reports/AAPL/AAPL_1d_backtest_results_20260528.csv"],
        "file_count": 1,
        "count": 1,
        "summary": {
            "count": 1,
            "valid_count": 1,
            "invalid_count": 0,
            "neither_count": 1,
            "small_sample_warning": "small_sample",
        },
        "summary_rows": [
            {
                "count": 1,
                "valid_count": 1,
                "invalid_count": 0,
                "neither_count": 1,
                "small_sample_warning": "small_sample",
            }
        ],
        "grouped_summary_rows": [
            {
                "ticker": "AAPL",
                "timeframe": "1d",
                "horizon_bars": 20,
                "tie_break_policy": "conservative",
                "group_key": "AAPL|1d|20|conservative",
                "count": 1,
            }
        ],
        "invalid_reason_rows": [],
        "warnings": [],
        "errors": [],
    }
    result.update(overrides)
    return result


def _result_row(**overrides):
    row = {
        "ticker": "AAPL",
        "timeframe": "1d",
        "outcome": "NEITHER",
        "realized_R": 0.0,
        "bars_to_hit": "",
        "planned_rr": 1.5,
        "tie_break_policy": "conservative",
        "horizon_bars": 20,
        "backtest_success": True,
    }
    row.update(overrides)
    return row


def test_filename_with_ticker_timeframe():
    filename = build_backtest_calibration_summary_filename(
        ticker="AAPL",
        timeframe="1d",
        timestamp="20260528_120000",
    )

    assert filename == "AAPL_1d_backtest_calibration_summary_20260528_120000.md"


def test_fallback_filename():
    filename = build_backtest_calibration_summary_filename(timestamp="20260528_120000")

    assert filename == "marketflow_backtest_calibration_summary_20260528_120000.md"


def test_unsafe_filename_parts_are_sanitized():
    filename = build_backtest_calibration_summary_filename(
        ticker="AA/PL Inc",
        timeframe="1 d",
        timestamp="20260528_120000",
    )

    assert "/" not in filename
    assert " " not in filename
    assert filename == "AA_PL_Inc_1_d_backtest_calibration_summary_20260528_120000.md"


def test_markdown_contains_required_sections():
    markdown = build_backtest_calibration_summary_markdown(_calibration_result())

    assert "# MarketFlow Backtest Calibration Summary" in markdown
    assert "## Metadata" in markdown
    assert "## Global Summary" in markdown
    assert "## Grouped Summary" in markdown
    assert "## Invalid Row Review" in markdown
    assert "## Guardrails" in markdown


def test_markdown_includes_source_result_files():
    markdown = build_backtest_calibration_summary_markdown(
        _calibration_result(source_result_files=["one.csv", "two.csv"])
    )

    assert "one.csv" in markdown
    assert "two.csv" in markdown


def test_empty_warnings_errors_show_none():
    markdown = build_backtest_calibration_summary_markdown(_calibration_result(warnings=[], errors=[]))

    assert "## Warnings\n\n_None._" in markdown
    assert "## Errors\n\n_None._" in markdown


def test_warnings_errors_render_bullet_lists():
    markdown = build_backtest_calibration_summary_markdown(
        _calibration_result(warnings=["small sample"], errors=["read failed"])
    )

    assert "- small sample" in markdown
    assert "- read failed" in markdown


def test_write_markdown_file_success(tmp_path):
    result = write_backtest_calibration_summary_markdown(
        _calibration_result(),
        tmp_path,
        ticker="AAPL",
        timeframe="1d",
        timestamp="20260528_120000",
    )

    assert result["success"] is True
    assert result["kind"] == BACKTEST_CALIBRATION_SUMMARY_KIND
    path = tmp_path / result["filename"]
    assert path.exists()
    assert "# MarketFlow Backtest Calibration Summary" in path.read_text(encoding="utf-8")


def test_collision_suffix(tmp_path):
    first = write_backtest_calibration_summary_markdown(
        _calibration_result(),
        tmp_path,
        ticker="AAPL",
        timeframe="1d",
        timestamp="20260528_120000",
    )
    second = write_backtest_calibration_summary_markdown(
        _calibration_result(),
        tmp_path,
        ticker="AAPL",
        timeframe="1d",
        timestamp="20260528_120000",
    )

    assert first["filename"] == "AAPL_1d_backtest_calibration_summary_20260528_120000.md"
    assert second["filename"] == "AAPL_1d_backtest_calibration_summary_20260528_120000_2.md"


def test_folder_convenience_writer(tmp_path):
    pd.DataFrame([_result_row()]).to_csv(
        tmp_path / "AAPL_1d_backtest_results_20260528.csv",
        index=False,
    )

    result = summarize_folder_to_backtest_calibration_markdown(
        tmp_path,
        ticker="AAPL",
        timeframe="1d",
        timestamp="20260528_120000",
    )

    assert result["success"] is True
    assert result["calibration_result"]["count"] == 1
    assert result["write_result"]["success"] is True
    assert (tmp_path / result["filename"]).exists()


def test_artifact_classification_for_calibration_summary(tmp_path):
    path = tmp_path / "AAPL_1d_backtest_calibration_summary_20260528_120000.md"
    path.write_text("# Summary", encoding="utf-8")

    artifacts = list_report_artifacts(str(tmp_path))
    artifact = next(item for item in artifacts if item["name"] == path.name)

    assert artifact["kind"] == BACKTEST_CALIBRATION_SUMMARY_KIND
    assert artifact["previewable"] is True
    assert artifact["downloadable"] is True
