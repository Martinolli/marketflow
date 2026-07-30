from __future__ import annotations

from pathlib import Path

import pandas as pd

from marketflow.services.artifact_service import list_report_artifacts
from marketflow.services.walk_forward_validation_artifact_service import (
    WALK_FORWARD_CASES_CSV_KIND,
    WALK_FORWARD_RESULTS_CSV_KIND,
    WALK_FORWARD_SUMMARY_CSV_KIND,
    WALK_FORWARD_VALIDATION_SUMMARY_KIND,
    build_walk_forward_cases_filename,
    build_walk_forward_results_filename,
    build_walk_forward_summary_filename,
    build_walk_forward_validation_summary_filename,
    build_walk_forward_validation_summary_markdown,
    summarize_csv_to_walk_forward_validation_artifacts,
    summarize_csv_to_walk_forward_validation_markdown,
    write_walk_forward_cases_csv,
    write_walk_forward_results_csv,
    write_walk_forward_summary_csv,
    write_walk_forward_validation_csv_artifacts,
    write_walk_forward_validation_summary_markdown,
)


def _minimal_result() -> dict:
    return {
        "success": True,
        "build_result": {
            "csv_path": "IONQ_30m_wyckoff_annotated.csv",
            "source_csv_name": "IONQ_30m_wyckoff_annotated.csv",
            "ticker": "IONQ",
            "timeframe": "30m",
            "profile_name": "intraday_tactical",
            "walk_forward_run_id": "run-1",
            "row_count": 320,
            "minimum_lookback_rows": 240,
            "horizon_bars": 60,
            "require_mature_future": True,
            "case_count": 1,
            "event_filters": ["SPRING_WEAK"],
            "cases": [
                {
                    "ticker": "IONQ",
                    "timeframe": "30m",
                    "profile_name": "intraday_tactical",
                    "signal_row_index": 240,
                    "signal_timestamp": "2026-01-01 10:00:00",
                    "entry": 10.0,
                    "stop_loss": 9.5,
                    "take_profit": 10.75,
                    "risk_reward": 1.5,
                    "target_status": "TARGET_RESOLVED",
                    "target_provenance": "WYCKOFF_TR_HIGH",
                    "target_structural_level_kind": "resistance",
                    "rr_status": "RR_GATE_PASSED",
                    "strategy_score": 72.0,
                    "wyckoff_phase": "C",
                    "wyckoff_event": "SPRING_WEAK",
                    "trend": "up",
                    "direction": "long",
                    "lookback_rows_available": 241,
                    "future_bars_available": 79,
                    "lookback_end_index": 240,
                    "future_window_start_index": 241,
                    "future_window_end_index": 300,
                    "snapshot_success": True,
                    "wyckoff_event_source": "wyckoff_confirmed_event",
                    "wyckoff_phase_source": "wyckoff_phase",
                    "trend_source": "trend",
                    "walk_forward_run_id": "run-1",
                    "walk_forward_case_id": "case-1",
                }
            ],
        },
        "evaluation_result": {
            "success": True,
            "profile_name": "intraday_tactical",
            "horizon_bars": 60,
            "evaluated_count": 1,
            "result_rows": [
                {
                    "ticker": "IONQ",
                    "timeframe": "30m",
                    "profile_name": "intraday_tactical",
                    "signal_row_index": 240,
                    "signal_timestamp": "2026-01-01 10:00:00",
                    "entry": 10.0,
                    "stop_loss": 9.5,
                    "take_profit": 10.75,
                    "outcome": "TP_FIRST",
                    "future_bars_available": 60,
                    "horizon_bars": 60,
                    "bars_to_hit": 1,
                    "realized_R": 1.5,
                    "same_bar_hit": False,
                    "neither_reason": "",
                    "backtest_success": True,
                    "wyckoff_phase": "C",
                    "wyckoff_event": "SPRING_WEAK",
                    "trend": "up",
                }
            ],
        },
        "summary": {
            "success": True,
            "sample_count": 1,
            "scoreable_count": 1,
            "tp_first_count": 1,
            "sl_first_count": 0,
            "neither_count": 0,
            "invalid_count": 0,
            "ambiguous_count": 0,
            "not_mature_count": 0,
            "mean_realized_R": 1.5,
            "median_realized_R": 1.5,
            "win_rate": 1.0,
            "loss_rate": 0.0,
            "neither_rate": 0.0,
        },
        "warnings": [],
        "errors": [],
    }


def _rows(count: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index in range(count):
        close = 100.0 + index * 0.1
        rows.append(
            {
                "timestamp": (
                    pd.Timestamp("2026-01-01 10:00:00") + pd.Timedelta(minutes=index)
                ).isoformat(sep=" "),
                "open": close - 0.2,
                "high": close + 2.0,
                "low": close - 1.0,
                "close": close,
                "tr_low": close - 1.0,
                "tr_high": close + 2.0,
                "wyckoff_phase": "C",
                "wyckoff_event": "SPRING_WEAK",
                "trend": "up",
            }
        )
    return rows


def test_filename_with_ticker_timeframe_profile():
    filename = build_walk_forward_validation_summary_filename(
        ticker="IONQ",
        timeframe="30m",
        profile_name="intraday_tactical",
        timestamp="20260603_120000",
    )

    assert filename == "IONQ_30m_intraday_tactical_walk_forward_validation_summary_20260603_120000.md"


def test_fallback_filename():
    filename = build_walk_forward_validation_summary_filename(timestamp="20260603_120000")

    assert filename == "marketflow_walk_forward_validation_summary_20260603_120000.md"


def test_csv_filename_builders_with_ticker_timeframe_profile():
    kwargs = {
        "ticker": "IONQ",
        "timeframe": "30m",
        "profile_name": "intraday_tactical",
        "timestamp": "20260603_120000",
    }

    assert build_walk_forward_cases_filename(**kwargs) == (
        "IONQ_30m_intraday_tactical_walk_forward_cases_20260603_120000.csv"
    )
    assert build_walk_forward_results_filename(**kwargs) == (
        "IONQ_30m_intraday_tactical_walk_forward_results_20260603_120000.csv"
    )
    assert build_walk_forward_summary_filename(**kwargs) == (
        "IONQ_30m_intraday_tactical_walk_forward_summary_20260603_120000.csv"
    )


def test_csv_filename_builders_fallback():
    assert build_walk_forward_cases_filename(timestamp="20260603_120000") == (
        "marketflow_walk_forward_cases_20260603_120000.csv"
    )
    assert build_walk_forward_results_filename(timestamp="20260603_120000") == (
        "marketflow_walk_forward_results_20260603_120000.csv"
    )
    assert build_walk_forward_summary_filename(timestamp="20260603_120000") == (
        "marketflow_walk_forward_summary_20260603_120000.csv"
    )


def test_unsafe_filename_parts_sanitized():
    filename = build_walk_forward_validation_summary_filename(
        ticker="IO/NQ",
        timeframe="30m",
        profile_name="intraday tactical",
        timestamp="20260603_120000",
    )

    assert "/" not in filename
    assert " " not in filename
    assert "IO_NQ_30m_intraday_tactical" in filename


def test_markdown_contains_required_sections():
    markdown = build_walk_forward_validation_summary_markdown(_minimal_result())

    assert "# MarketFlow Historical Walk-Forward Validation Summary" in markdown
    assert "## Metadata" in markdown
    assert "## Summary" in markdown
    assert "## Walk-Forward Cases" in markdown
    assert "## Deterministic Outcome Rows" in markdown
    assert "## Outcome Review" in markdown
    assert "## No-Leakage Review" in markdown
    assert "## Guardrails" in markdown


def test_markdown_includes_summary_metrics():
    markdown = build_walk_forward_validation_summary_markdown(_minimal_result())

    assert "scoreable_count" in markdown
    assert "tp_first_count" in markdown
    assert "| 1 | 1 | 1 | 0 | 0 |" in markdown


def test_markdown_includes_cases_and_result_rows():
    markdown = build_walk_forward_validation_summary_markdown(_minimal_result())

    assert "signal_row_index" in markdown
    assert "target_status" in markdown
    assert "TARGET_RESOLVED" in markdown
    assert "240" in markdown
    assert "TP_FIRST" in markdown


def test_empty_warnings_and_errors_show_none():
    markdown = build_walk_forward_validation_summary_markdown(_minimal_result())

    assert "## Warnings\n\n_None._" in markdown
    assert "## Errors\n\n_None._" in markdown


def test_warnings_and_errors_render_bullets():
    result = _minimal_result()
    result["warnings"] = ["small sample"]
    result["errors"] = ["example error"]

    markdown = build_walk_forward_validation_summary_markdown(result)

    assert "- small sample" in markdown
    assert "- example error" in markdown


def test_write_markdown_file_success(tmp_path):
    result = write_walk_forward_validation_summary_markdown(
        _minimal_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="30m",
        profile_name="intraday_tactical",
        timestamp="20260603_120000",
    )

    assert result["success"] is True
    assert Path(result["path"]).exists()
    assert result["kind"] == WALK_FORWARD_VALIDATION_SUMMARY_KIND


def test_write_cases_csv_creates_file_and_kind(tmp_path):
    result = write_walk_forward_cases_csv(
        _minimal_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="30m",
        profile_name="intraday_tactical",
        timestamp="20260603_120000",
    )

    rows = pd.read_csv(result["path"])

    assert result["success"] is True
    assert Path(result["path"]).exists()
    assert result["kind"] == WALK_FORWARD_CASES_CSV_KIND
    assert result["row_count"] == 1
    assert rows.loc[0, "wyckoff_event_source"] == "wyckoff_confirmed_event"
    assert rows.loc[0, "walk_forward_case_id"] == "case-1"
    assert rows.loc[0, "target_status"] == "TARGET_RESOLVED"
    assert rows.loc[0, "target_provenance"] == "WYCKOFF_TR_HIGH"
    assert rows.loc[0, "rr_status"] == "RR_GATE_PASSED"


def test_write_results_csv_creates_file_and_kind(tmp_path):
    result = write_walk_forward_results_csv(
        _minimal_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="30m",
        profile_name="intraday_tactical",
        timestamp="20260603_120000",
    )

    rows = pd.read_csv(result["path"])

    assert result["success"] is True
    assert Path(result["path"]).exists()
    assert result["kind"] == WALK_FORWARD_RESULTS_CSV_KIND
    assert result["row_count"] == 1
    assert rows.loc[0, "outcome"] == "TP_FIRST"
    assert rows.loc[0, "walk_forward_case_id"] == "case-1"


def test_write_summary_csv_creates_file_and_kind(tmp_path):
    result = write_walk_forward_summary_csv(
        _minimal_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="30m",
        profile_name="intraday_tactical",
        timestamp="20260603_120000",
    )

    rows = pd.read_csv(result["path"])

    assert result["success"] is True
    assert Path(result["path"]).exists()
    assert result["kind"] == WALK_FORWARD_SUMMARY_CSV_KIND
    assert result["row_count"] == 1
    assert rows.loc[0, "scoreable_count"] == 1
    assert rows.loc[0, "case_count"] == 1


def test_combined_csv_artifacts_writer_writes_selected_files(tmp_path):
    result = write_walk_forward_validation_csv_artifacts(
        _minimal_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="30m",
        profile_name="intraday_tactical",
        timestamp="20260603_120000",
        include_cases=True,
        include_results=False,
        include_summary=True,
    )

    kinds = {artifact["kind"] for artifact in result["artifacts"]}

    assert result["success"] is True
    assert kinds == {WALK_FORWARD_CASES_CSV_KIND, WALK_FORWARD_SUMMARY_CSV_KIND}
    assert result["results_result"] is None


def test_header_only_cases_and_results_csv_when_no_rows(tmp_path):
    empty_result = {
        "success": False,
        "build_result": {
            "ticker": "IONQ",
            "timeframe": "30m",
            "profile_name": "intraday_tactical",
            "cases": [],
            "case_count": 0,
            "event_filters": ["DOES_NOT_EXIST"],
        },
        "evaluation_result": {"result_rows": [], "evaluated_count": 0},
        "summary": {},
        "warnings": ["No walk-forward cases were built."],
        "errors": [],
    }

    cases_result = write_walk_forward_cases_csv(empty_result, tmp_path, timestamp="20260603_120000")
    results_result = write_walk_forward_results_csv(empty_result, tmp_path, timestamp="20260603_120000")

    cases_rows = pd.read_csv(cases_result["path"])
    results_rows = pd.read_csv(results_result["path"])

    assert cases_result["success"] is True
    assert results_result["success"] is True
    assert cases_result["row_count"] == 0
    assert results_result["row_count"] == 0
    assert cases_rows.empty
    assert results_rows.empty
    assert "No walk-forward cases were available." in cases_result["warnings"]
    assert "No walk-forward result rows were available." in results_result["warnings"]


def test_collision_suffix(tmp_path):
    first = write_walk_forward_validation_summary_markdown(
        _minimal_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="30m",
        profile_name="intraday_tactical",
        timestamp="20260603_120000",
    )
    second = write_walk_forward_validation_summary_markdown(
        _minimal_result(),
        tmp_path,
        ticker="IONQ",
        timeframe="30m",
        profile_name="intraday_tactical",
        timestamp="20260603_120000",
    )

    assert first["filename"].endswith(".md")
    assert second["filename"].endswith("_2.md")


def test_convenience_csv_writer(tmp_path):
    csv_path = tmp_path / "IONQ_30m_wyckoff_annotated.csv"
    pd.DataFrame(_rows(320)).to_csv(csv_path, index=False)

    result = summarize_csv_to_walk_forward_validation_markdown(
        csv_path,
        profile_name="fast_test",
        step=20,
        max_cases=3,
        timestamp="20260603_120000",
    )

    assert result["success"] is True
    assert Path(result["path"]).exists()
    assert result["walk_forward_result"]["build_result"]["case_count"] > 0
    assert result["write_result"]["kind"] == WALK_FORWARD_VALIDATION_SUMMARY_KIND


def test_artifact_classification(tmp_path):
    path = tmp_path / "IONQ_30m_intraday_tactical_walk_forward_validation_summary_20260603_120000.md"
    path.write_text("# Summary", encoding="utf-8")

    items = list_report_artifacts(tmp_path)
    item = next(item for item in items if item["name"] == path.name)

    assert item["kind"] == WALK_FORWARD_VALIDATION_SUMMARY_KIND
    assert item["previewable"] is True
    assert item["downloadable"] is True


def test_csv_artifact_classification(tmp_path):
    paths = [
        tmp_path / "IONQ_30m_intraday_tactical_walk_forward_cases_20260603_120000.csv",
        tmp_path / "IONQ_30m_intraday_tactical_walk_forward_results_20260603_120000.csv",
        tmp_path / "IONQ_30m_intraday_tactical_walk_forward_summary_20260603_120000.csv",
    ]
    for path in paths:
        path.write_text("a\n", encoding="utf-8")

    items = list_report_artifacts(tmp_path)
    kinds = {item["name"]: item["kind"] for item in items}

    assert kinds[paths[0].name] == WALK_FORWARD_CASES_CSV_KIND
    assert kinds[paths[1].name] == WALK_FORWARD_RESULTS_CSV_KIND
    assert kinds[paths[2].name] == WALK_FORWARD_SUMMARY_CSV_KIND


def test_convenience_full_artifact_writer_creates_markdown_and_csv(tmp_path):
    csv_path = tmp_path / "IONQ_30m_wyckoff_annotated.csv"
    pd.DataFrame(_rows(320)).to_csv(csv_path, index=False)

    result = summarize_csv_to_walk_forward_validation_artifacts(
        csv_path,
        profile_name="fast_test",
        step=20,
        max_cases=3,
        timestamp="20260603_120000",
        save_markdown=True,
        save_cases_csv=True,
        save_results_csv=True,
        save_summary_csv=True,
    )
    kinds = {artifact["kind"] for artifact in result["artifacts"]}

    assert result["success"] is True
    assert {
        WALK_FORWARD_VALIDATION_SUMMARY_KIND,
        WALK_FORWARD_CASES_CSV_KIND,
        WALK_FORWARD_RESULTS_CSV_KIND,
        WALK_FORWARD_SUMMARY_CSV_KIND,
    }.issubset(kinds)
    assert all(Path(artifact["path"]).exists() for artifact in result["artifacts"])
    assert result["csv_result"]["summary_result"]["row_count"] == 1


def test_markdown_truncates_long_cases_and_results():
    result = _minimal_result()
    result["build_result"]["cases"] = result["build_result"]["cases"] * 3
    result["evaluation_result"]["result_rows"] = result["evaluation_result"]["result_rows"] * 3

    markdown = build_walk_forward_validation_summary_markdown(result, max_case_rows=1, max_result_rows=1)

    assert "_Showing 1 of 3 rows._" in markdown
