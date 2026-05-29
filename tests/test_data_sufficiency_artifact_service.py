from __future__ import annotations

from datetime import datetime, timedelta

from marketflow.services.artifact_service import list_report_artifacts
from marketflow.services.data_sufficiency_artifact_service import (
    DATA_SUFFICIENCY_SUMMARY_KIND,
    build_data_sufficiency_summary_filename,
    build_data_sufficiency_summary_markdown,
    summarize_folder_to_data_sufficiency_markdown,
    write_data_sufficiency_summary_markdown,
)


def _write_csv(path, rows: int) -> None:
    start = datetime(2026, 1, 1, 9, 30)
    lines = ["timestamp,open,high,low,close"]
    for index in range(rows):
        timestamp = (start + timedelta(minutes=index)).isoformat()
        lines.append(f"{timestamp},{100 + index},{101 + index},{99 + index},{100.5 + index}")
    path.write_text("\n".join(lines), encoding="utf-8")


def _sufficiency_result(**overrides):
    rows = [
        {
            "ticker": "IONQ",
            "timeframe": "15m",
            "source_csv_name": "IONQ_15m_wyckoff_annotated.csv",
            "rows_available": 300,
            "first_timestamp": "2026-01-01 09:30:00",
            "last_timestamp": "2026-01-04 10:00:00",
            "configured_period": "20d",
            "eigen_window": 80,
            "monte_carlo_horizon": 60,
            "backtest_horizon": 60,
            "minimum_rows_required": 240,
            "future_bars_available": None,
            "bars_remaining_to_maturity": None,
            "data_sufficiency_status": "sufficient",
            "eigen_sufficiency_status": "sufficient",
            "monte_carlo_sufficiency_status": "sufficient",
            "backtest_sufficiency_status": "sufficient",
            "calibration_sufficiency_status": "sufficient",
            "noise_warning": "strong_noise_caution",
            "provider_limit_warning": None,
            "notes": ["micro_timeframe_noise_caution"],
        },
        {
            "ticker": "IONQ",
            "timeframe": "1w",
            "source_csv_name": "IONQ_1w_wyckoff_annotated.csv",
            "rows_available": 105,
            "configured_period": "2y",
            "eigen_window": 80,
            "monte_carlo_horizon": 60,
            "backtest_horizon": 60,
            "minimum_rows_required": 240,
            "data_sufficiency_status": "limited",
            "calibration_sufficiency_status": "limited",
            "noise_warning": None,
            "provider_limit_warning": "possible_provider_limit",
        },
        {
            "ticker": "IONQ",
            "timeframe": "1mo",
            "source_csv_name": "IONQ_1mo_wyckoff_annotated.csv",
            "rows_available": 30,
            "configured_period": "5y",
            "minimum_rows_required": 240,
            "data_sufficiency_status": "insufficient",
            "calibration_sufficiency_status": "insufficient",
            "noise_warning": None,
            "provider_limit_warning": None,
        },
    ]
    result = {
        "success": True,
        "report_dir": "reports/2026-05-29/IONQ",
        "csv_file_count": len(rows),
        "rows": rows,
        "summary": {
            "csv_file_count": len(rows),
            "sufficient_count": 1,
            "limited_count": 1,
            "insufficient_count": 1,
            "provider_limited_count": 1,
            "not_yet_mature_count": 0,
            "unknown_count": 0,
            "noise_warning_count": 1,
            "provider_limit_warning_count": 1,
            "minimum_rows_required_max": 240,
            "rows_available_min": 30,
            "rows_available_max": 300,
        },
        "warnings": [],
        "errors": [],
    }
    result.update(overrides)
    return result


def test_filename_with_ticker_timeframe():
    filename = build_data_sufficiency_summary_filename(
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )

    assert filename == "IONQ_15m_data_sufficiency_summary_20260529_120000.md"


def test_filename_with_ticker_only():
    filename = build_data_sufficiency_summary_filename(ticker="IONQ", timestamp="20260529_120000")

    assert filename == "IONQ_data_sufficiency_summary_20260529_120000.md"


def test_fallback_filename():
    filename = build_data_sufficiency_summary_filename(timestamp="20260529_120000")

    assert filename == "marketflow_data_sufficiency_summary_20260529_120000.md"


def test_unsafe_filename_parts_are_sanitized():
    filename = build_data_sufficiency_summary_filename(
        ticker="AA/PL Inc",
        timeframe="15 m",
        timestamp="20260529_120000",
    )

    assert "/" not in filename
    assert " " not in filename
    assert filename == "AA_PL_Inc_15_m_data_sufficiency_summary_20260529_120000.md"


def test_markdown_contains_required_sections():
    markdown = build_data_sufficiency_summary_markdown(_sufficiency_result())

    assert "# MarketFlow Data Horizon / Parameter Sufficiency Summary" in markdown
    assert "## Metadata" in markdown
    assert "## Summary" in markdown
    assert "## CSV Sufficiency Rows" in markdown
    assert "## Status Review" in markdown
    assert "## Guardrails" in markdown


def test_markdown_includes_status_rows():
    markdown = build_data_sufficiency_summary_markdown(_sufficiency_result())

    assert "sufficient" in markdown
    assert "limited" in markdown
    assert "insufficient" in markdown


def test_markdown_includes_warning_review():
    markdown = build_data_sufficiency_summary_markdown(_sufficiency_result())

    assert "strong_noise_caution" in markdown
    assert "possible_provider_limit" in markdown


def test_empty_warnings_errors_show_none():
    markdown = build_data_sufficiency_summary_markdown(_sufficiency_result(warnings=[], errors=[]))

    assert "## Errors\n\n_None._" in markdown
    assert "## Warnings\n\n_None._" in markdown


def test_warnings_errors_render_bullet_lists():
    markdown = build_data_sufficiency_summary_markdown(
        _sufficiency_result(warnings=["small sample"], errors=["bad input"])
    )

    assert "## Errors\n\n- bad input" in markdown
    assert "## Warnings\n\n- small sample" in markdown


def test_write_markdown_file_success(tmp_path):
    result = write_data_sufficiency_summary_markdown(
        _sufficiency_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )

    assert result["success"] is True
    assert result["kind"] == DATA_SUFFICIENCY_SUMMARY_KIND
    path = tmp_path / result["filename"]
    assert path.exists()
    assert "# MarketFlow Data Horizon / Parameter Sufficiency Summary" in path.read_text(encoding="utf-8")


def test_collision_suffix(tmp_path):
    first = write_data_sufficiency_summary_markdown(
        _sufficiency_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )
    second = write_data_sufficiency_summary_markdown(
        _sufficiency_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )

    assert first["filename"] == "IONQ_15m_data_sufficiency_summary_20260529_120000.md"
    assert second["filename"] == "IONQ_15m_data_sufficiency_summary_20260529_120000_2.md"


def test_folder_convenience_writer(tmp_path):
    csv_path = tmp_path / "IONQ_15m_wyckoff_annotated.csv"
    _write_csv(csv_path, 300)

    result = summarize_folder_to_data_sufficiency_markdown(
        tmp_path,
        parameter_context={"eigen_window": 80, "monte_carlo_horizon": 60, "backtest_horizon": 60},
        ticker="IONQ",
        timeframe="15m",
        timestamp="20260529_120000",
    )

    assert result["success"] is True
    assert (tmp_path / result["filename"]).exists()
    assert result["sufficiency_result"]["rows"]
    assert "_data_sufficiency_summary" in result["filename"]


def test_artifact_classification(tmp_path):
    path = tmp_path / "IONQ_15m_data_sufficiency_summary_20260529_120000.md"
    path.write_text("# Summary", encoding="utf-8")

    artifacts = list_report_artifacts(str(tmp_path))
    artifact = next(row for row in artifacts if row["name"] == path.name)

    assert artifact["kind"] == "data_sufficiency_summary_md"
    assert artifact["previewable"] is True
    assert artifact["downloadable"] is True
