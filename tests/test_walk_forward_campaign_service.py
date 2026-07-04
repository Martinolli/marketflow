from pathlib import Path

import pandas as pd
import pytest

from marketflow.services.artifact_service import list_report_artifacts
from marketflow.services.walk_forward_campaign_service import (
    WALK_FORWARD_CAMPAIGN_REPORT_MD_KIND,
    WALK_FORWARD_CAMPAIGN_RESULTS_CSV_KIND,
    WALK_FORWARD_CAMPAIGN_SUMMARY_CSV_KIND,
    build_walk_forward_campaign_grouped_summary,
    build_walk_forward_campaign_report_markdown,
    build_walk_forward_campaign_report_filename,
    build_walk_forward_campaign_results_filename,
    build_walk_forward_campaign_summary_filename,
    discover_walk_forward_campaign_files,
    load_walk_forward_results_csvs,
    load_walk_forward_summary_csvs,
    normalize_walk_forward_result_rows,
    write_walk_forward_campaign_artifacts,
)


def _write_csv(path: Path, rows: list[dict]) -> Path:
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def _result_rows() -> list[dict]:
    return [
        {"ticker": "IONQ", "timeframe": "1h", "profile_name": "intraday_tactical", "wyckoff_event": "SPRING_WEAK", "outcome": "TP_FIRST", "realized_R": 2.0, "bars_to_hit": 3, "same_bar_hit": True},
        {"ticker": "IONQ", "timeframe": "1h", "profile_name": "intraday_tactical", "wyckoff_event": "SPRING_WEAK", "outcome": "SL_FIRST", "realized_R": -1.0, "bars_to_hit": 5, "same_bar_hit": False},
        {"ticker": "IONQ", "timeframe": "1h", "profile_name": "intraday_tactical", "wyckoff_event": "SPRING_WEAK", "outcome": "NEITHER", "realized_R": 0.0, "bars_to_hit": None, "same_bar_hit": False},
        {"ticker": "IONQ", "timeframe": "1h", "profile_name": "intraday_tactical", "wyckoff_event": "SPRING_WEAK", "outcome": "INVALID", "realized_R": None},
        {"ticker": "IONQ", "timeframe": "1h", "profile_name": "intraday_tactical", "wyckoff_event": "SPRING_WEAK", "outcome": "AMBIGUOUS", "realized_R": None},
    ]


def test_filename_builders_use_safe_ticker_and_fallback() -> None:
    stamp = "20260704_120000"
    assert build_walk_forward_campaign_results_filename(ticker="IONQ / test", timestamp=stamp) == (
        "IONQ___test_walk_forward_campaign_results_20260704_120000.csv"
    )
    assert build_walk_forward_campaign_summary_filename(timestamp=stamp) == (
        "marketflow_walk_forward_campaign_summary_20260704_120000.csv"
    )
    assert build_walk_forward_campaign_report_filename(timestamp=stamp) == (
        "marketflow_walk_forward_campaign_report_20260704_120000.md"
    )


def test_discovery_finds_inputs_and_excludes_campaign_outputs(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    summary = nested / "IONQ_1h_intraday_tactical_walk_forward_summary_20260704_100000.csv"
    results = nested / "IONQ_1h_intraday_tactical_walk_forward_results_20260704_100000.csv"
    _write_csv(summary, [{"sample_count": 2}])
    _write_csv(results, [{"outcome": "TP_FIRST"}])
    _write_csv(tmp_path / "IONQ_walk_forward_campaign_summary_20260704_110000.csv", [{"sample_count": 2}])
    _write_csv(tmp_path / "IONQ_walk_forward_campaign_results_20260704_110000.csv", [{"outcome": "TP_FIRST"}])

    discovered = discover_walk_forward_campaign_files(tmp_path)

    assert discovered["success"] is True
    assert discovered["summary_csv_paths"] == [str(summary)]
    assert discovered["results_csv_paths"] == [str(results)]
    assert discovered["summary_count"] == discovered["results_count"] == 1


def test_discovery_empty_folder_returns_controlled_warning(tmp_path: Path) -> None:
    discovered = discover_walk_forward_campaign_files(tmp_path)

    assert discovered["success"] is False
    assert discovered["errors"] == []
    assert "No walk-forward" in discovered["warnings"][0]


def test_summary_loader_combines_files_and_adds_source_metadata(tmp_path: Path) -> None:
    first = _write_csv(tmp_path / "A_walk_forward_summary_1.csv", [{"ticker": "A", "sample_count": 1}])
    second = _write_csv(tmp_path / "B_walk_forward_summary_2.csv", [{"ticker": "B", "extra": "ok"}])

    loaded = load_walk_forward_summary_csvs([first, second])

    assert loaded["success"] is True
    assert loaded["file_count"] == loaded["row_count"] == 2
    assert set(loaded["dataframe"]["source_file"]) == {first.name, second.name}
    assert "extra" in loaded["dataframe"].columns


def test_results_loader_combines_metadata_and_coerces_numeric_fields(tmp_path: Path) -> None:
    first = _write_csv(
        tmp_path / "A_1h_p_walk_forward_results_1.csv",
        [{"realized_R": "2.5", "future_bars_available": "20", "outcome": "TP_FIRST"}],
    )
    second = _write_csv(
        tmp_path / "B_1h_p_walk_forward_results_2.csv",
        [{"realized_R": "not-a-number", "horizon_bars": "10", "bars_to_hit": "3"}],
    )

    loaded = load_walk_forward_results_csvs([first, second])

    assert loaded["file_count"] == loaded["row_count"] == 2
    assert loaded["dataframe"].loc[0, "realized_R"] == pytest.approx(2.5)
    assert pd.isna(loaded["dataframe"].loc[1, "realized_R"])
    assert loaded["dataframe"].loc[1, "bars_to_hit"] == 3
    assert all(loaded["dataframe"]["source_path"].str.contains(str(tmp_path), regex=False))


def test_normalizer_infers_filename_context_when_fields_are_missing() -> None:
    frame = pd.DataFrame(
        [
            {
                "ticker": "",
                "timeframe": None,
                "profile_name": " ",
                "outcome": "TP_FIRST",
                "source_file": "IONQ_1h_intraday_tactical_walk_forward_results_20260704_095631.csv",
                "source_path": "/reports/file.csv",
            }
        ]
    )

    normalized = normalize_walk_forward_result_rows(frame)

    assert normalized.loc[0, "ticker"] == "IONQ"
    assert normalized.loc[0, "timeframe"] == "1h"
    assert normalized.loc[0, "profile_name"] == "intraday_tactical"
    assert list(normalized.columns)[-2:] == ["source_file", "source_path"]


def test_grouped_summary_computes_requested_metrics() -> None:
    frame = pd.DataFrame(_result_rows())
    frame["source_file"] = ["one.csv", "one.csv", "two.csv", "two.csv", "two.csv"]

    result = build_walk_forward_campaign_grouped_summary(frame)
    row = result["rows"][0]

    assert result["success"] is True
    assert row["sample_count"] == 5
    assert row["scoreable_count"] == 3
    assert row["tp_first_count"] == row["sl_first_count"] == row["neither_count"] == 1
    assert row["invalid_count"] == row["ambiguous_count"] == 1
    assert row["win_rate"] == row["loss_rate"] == pytest.approx(1 / 3)
    assert row["mean_realized_R"] == pytest.approx(1 / 3)
    assert row["median_realized_R"] == 0
    assert row["min_realized_R"] == -1
    assert row["max_realized_R"] == 2
    assert row["same_bar_hit_count"] == 1
    assert row["mean_bars_to_hit"] == 4
    assert row["source_file_count"] == 2


def test_blank_event_group_is_named_no_confirmed_event() -> None:
    frame = pd.DataFrame([{"ticker": "IONQ", "timeframe": "30m", "profile_name": "p", "wyckoff_event": "", "outcome": "NEITHER"}])

    result = build_walk_forward_campaign_grouped_summary(frame)

    assert result["rows"][0]["wyckoff_event"] == "NO_CONFIRMED_EVENT"


def test_campaign_markdown_contains_required_sections_and_guardrails() -> None:
    grouped = build_walk_forward_campaign_grouped_summary(pd.DataFrame(_result_rows()))
    markdown = build_walk_forward_campaign_report_markdown(
        grouped_summary_rows=grouped["rows"],
        summary_rows=[{"source_path": "/reports/summary.csv"}],
        result_rows=[{"source_path": "/reports/results.csv"}],
        metadata={"ticker": "IONQ"},
    )

    for heading in (
        "# MarketFlow Walk-Forward Campaign Report",
        "## Metadata",
        "## Input Files",
        "## Campaign Summary by Timeframe/Event",
        "## Best Groups by Mean R",
        "## Weakest Groups by Mean R",
        "## Outcome Distribution",
        "## Notes / Limitations",
        "## Guardrails",
    ):
        assert heading in markdown
    assert "Candidate quality remains separate from workflow validity." in markdown


def test_write_campaign_artifacts_creates_all_outputs_collision_safely(tmp_path: Path) -> None:
    _write_csv(
        tmp_path / "IONQ_1h_intraday_tactical_walk_forward_summary_20260704_100000.csv",
        [{"ticker": "IONQ", "sample_count": 5}],
    )
    _write_csv(
        tmp_path / "IONQ_1h_intraday_tactical_walk_forward_results_20260704_100000.csv",
        _result_rows(),
    )

    first = write_walk_forward_campaign_artifacts(
        root_dir=tmp_path, ticker="IONQ", timestamp="20260704_120000"
    )
    second = write_walk_forward_campaign_artifacts(
        root_dir=tmp_path, ticker="IONQ", timestamp="20260704_120000"
    )

    assert first["success"] is True
    assert len(first["artifacts"]) == 3
    assert {artifact["kind"] for artifact in first["artifacts"]} == {
        WALK_FORWARD_CAMPAIGN_RESULTS_CSV_KIND,
        WALK_FORWARD_CAMPAIGN_SUMMARY_CSV_KIND,
        WALK_FORWARD_CAMPAIGN_REPORT_MD_KIND,
    }
    assert all(Path(artifact["path"]).exists() for artifact in first["artifacts"])
    assert second["success"] is True
    assert all("_2." in artifact["filename"] for artifact in second["artifacts"])
    assert second["discovery_result"]["results_count"] == 1


def test_artifact_classification_recognizes_campaign_outputs(tmp_path: Path) -> None:
    (tmp_path / "IONQ_walk_forward_campaign_results_1.csv").write_text("outcome\nTP_FIRST\n", encoding="utf-8")
    (tmp_path / "IONQ_walk_forward_campaign_summary_1.csv").write_text("sample_count\n1\n", encoding="utf-8")
    (tmp_path / "IONQ_walk_forward_campaign_report_1.md").write_text("# Report\n", encoding="utf-8")

    kinds = {artifact["kind"] for artifact in list_report_artifacts(str(tmp_path))}

    assert WALK_FORWARD_CAMPAIGN_RESULTS_CSV_KIND in kinds
    assert WALK_FORWARD_CAMPAIGN_SUMMARY_CSV_KIND in kinds
    assert WALK_FORWARD_CAMPAIGN_REPORT_MD_KIND in kinds
