from __future__ import annotations

from pathlib import Path

from marketflow.services import strategy_service


def _touch(path: Path) -> Path:
    rows = ["timestamp,open,high,low,close,wyckoff_phase,wyckoff_confirmed_event"]
    for index in range(25):
        close = 100 + index
        rows.append(f"2026-01-{index + 1:02d},{close - 1},{close + 2},{close - 2},{close},D,SOS")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def test_rank_latest_candidates_rejects_surrounding_ticker_whitespace(monkeypatch, tmp_path):
    monkeypatch.setattr(strategy_service, "get_report_root", lambda: str(tmp_path))

    result = strategy_service.rank_latest_candidates([" AAA"], "4h")

    assert result["success"] is False
    assert result["error_type"] == "ValueError"
    assert "surrounding whitespace" in result["error"]
    assert result["results"] == []


def test_rank_latest_candidates_rejects_surrounding_timeframe_whitespace(monkeypatch, tmp_path):
    monkeypatch.setattr(strategy_service, "get_report_root", lambda: str(tmp_path))

    result = strategy_service.rank_latest_candidates(["AAA"], " 4h")

    assert result["success"] is False
    assert result["error_type"] == "ValueError"
    assert "surrounding whitespace" in result["error"]
    assert result["results"] == []


def test_inspect_strategy_inputs_reports_strict_source_status_not_timeframe_only_match(tmp_path):
    ticker_dir = tmp_path / "batch_20260729_010203" / "AAA"
    ticker_dir.mkdir(parents=True)
    _touch(ticker_dir / "BBB_4h_wyckoff_annotated.csv")

    result = strategy_service.inspect_strategy_inputs(
        report_root=str(tmp_path),
        tickers=["AAA"],
        timeframe="4h",
        min_rr=1.5,
        max_sl_atr=2.0,
        prefer_phases=("C", "D", "E"),
        use_mc=False,
    )

    check = result["ticker_checks"]["AAA"]
    assert "matching_timeframe_csvs" not in check
    assert check["source_status"] == "DATASET_NOT_FOUND"
    assert check["source_reason"] == "DATASET_NOT_FOUND"
    assert check["source_csv_name"] is None
