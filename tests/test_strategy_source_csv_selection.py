from __future__ import annotations

from pathlib import Path

from marketflow.marketflow_strategy import _select_strategy_source_csv


def _touch(path: Path) -> Path:
    path.write_text("timestamp,open,high,low,close\n2026-01-01,1,2,1,1.5\n", encoding="utf-8")
    return path


def _selected_name(tmp_path: Path, ticker: str = "AAPL", tf: str = "1d") -> str | None:
    selected = _select_strategy_source_csv(str(tmp_path), ticker, tf)
    return Path(selected).name if selected else None


def test_canonical_annotated_preferred_over_pv_eigen(tmp_path):
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated.csv")
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated_pv_eigen.csv")

    assert _selected_name(tmp_path) == "AAPL_1d_wyckoff_annotated.csv"


def test_canonical_annotated_preferred_over_raw_csv(tmp_path):
    _touch(tmp_path / "AAPL_1d.csv")
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated.csv")

    assert _selected_name(tmp_path) == "AAPL_1d_wyckoff_annotated.csv"


def test_generated_candidate_and_result_csvs_ignored(tmp_path):
    _touch(tmp_path / "AAPL_1d_backtest_candidates_20260528.csv")
    _touch(tmp_path / "AAPL_1d_backtest_results_20260528.csv")
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated.csv")

    assert _selected_name(tmp_path) == "AAPL_1d_wyckoff_annotated.csv"


def test_raw_csv_fallback_when_no_annotated_exists(tmp_path):
    _touch(tmp_path / "AAPL_1d.csv")

    assert _selected_name(tmp_path) == "AAPL_1d.csv"


def test_generated_only_csvs_are_not_selected(tmp_path):
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated_pv_eigen.csv")
    _touch(tmp_path / "AAPL_1d_backtest_results_20260528.csv")

    assert _selected_name(tmp_path) is None


def test_timeframe_token_match_selects_requested_timeframe(tmp_path):
    _touch(tmp_path / "AAPL_1h_wyckoff_annotated.csv")
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated.csv")

    assert _selected_name(tmp_path, tf="1d") == "AAPL_1d_wyckoff_annotated.csv"


def test_ticker_prefix_preference(tmp_path):
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated.csv")
    _touch(tmp_path / "MSFT_1d_wyckoff_annotated.csv")

    assert _selected_name(tmp_path, ticker="AAPL") == "AAPL_1d_wyckoff_annotated.csv"
