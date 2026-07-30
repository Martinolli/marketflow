from __future__ import annotations

import os
from pathlib import Path

import pytest

from marketflow.marketflow_strategy import (
    SOURCE_REASON_DATASET_IDENTITY_AMBIGUOUS,
    SOURCE_REASON_DATASET_NOT_FOUND,
    SOURCE_REASON_INVALID_REQUEST,
    SOURCE_REASON_INVALID_SOURCE_ROOT,
    SOURCE_STATUS_EXACT_MATCH,
    StrategyConfig,
    _select_strategy_source_csv,
    rank_long_candidates,
    resolve_strategy_source_identity,
)


def _touch(path: Path) -> Path:
    rows = ["timestamp,open,high,low,close,tr_low,tr_high,wyckoff_phase,wyckoff_confirmed_event"]
    for index in range(25):
        close = 100 + index
        rows.append(
            f"2026-01-{index + 1:02d},{close - 1},{close + 2},{close - 2},{close},"
            f"{close - 5},{close + 12},D,SOS"
        )
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def _selected_name(tmp_path: Path, ticker: str = "AAPL", tf: str = "1d") -> str | None:
    selected = _select_strategy_source_csv(str(tmp_path), ticker, tf)
    return Path(selected).name if selected else None


def test_canonical_annotated_preferred_over_pv_eigen(tmp_path):
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated.csv")
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated_pv_eigen.csv")

    assert _selected_name(tmp_path) == "AAPL_1d_wyckoff_annotated.csv"


def test_raw_csv_selected_for_exact_identity_when_canonical_is_different_timeframe(tmp_path):
    _touch(tmp_path / "AAPL_1d.csv")
    _touch(tmp_path / "AAPL_4h_wyckoff_annotated.csv")

    assert _selected_name(tmp_path) == "AAPL_1d.csv"


def test_generated_candidate_and_result_csvs_ignored(tmp_path):
    _touch(tmp_path / "AAPL_1d_backtest_candidates_20260528.csv")
    _touch(tmp_path / "AAPL_1d_backtest_results_20260528.csv")
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated.csv")

    assert _selected_name(tmp_path) == "AAPL_1d_wyckoff_annotated.csv"


def test_generated_walk_forward_csvs_are_ignored_as_strategy_sources(tmp_path):
    _touch(tmp_path / "AAPL_1d_fast_test_walk_forward_cases_20260729_120000.csv")
    _touch(tmp_path / "AAPL_1d_fast_test_walk_forward_results_20260729_120000.csv")
    _touch(tmp_path / "AAPL_1d_fast_test_walk_forward_summary_20260729_120000.csv")
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated.csv")

    assert _selected_name(tmp_path) == "AAPL_1d_wyckoff_annotated.csv"


def test_generated_walk_forward_csvs_are_not_selected_when_source_is_absent(tmp_path):
    _touch(tmp_path / "AAPL_1d_fast_test_walk_forward_cases_20260729_120000.csv")

    assert _selected_name(tmp_path) is None


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


def test_exact_ticker_match_does_not_cross_similar_prefixes(tmp_path):
    _touch(tmp_path / "AAPL_1d_wyckoff_annotated.csv")
    _touch(tmp_path / "MSFT_1d_wyckoff_annotated.csv")

    assert _selected_name(tmp_path, ticker="AAPL") == "AAPL_1d_wyckoff_annotated.csv"


def test_wrong_ticker_same_timeframe_is_not_selected(tmp_path):
    _touch(tmp_path / "BBB_4h_wyckoff_annotated.csv")

    resolution = resolve_strategy_source_identity(str(tmp_path), "AAA", "4h")

    assert resolution.success is False
    assert resolution.reason == SOURCE_REASON_DATASET_NOT_FOUND
    assert _selected_name(tmp_path, ticker="AAA", tf="4h") is None


def test_matching_ticker_wrong_timeframe_is_not_selected(tmp_path):
    _touch(tmp_path / "AAA_1h_wyckoff_annotated.csv")

    resolution = resolve_strategy_source_identity(str(tmp_path), "AAA", "4h")

    assert resolution.success is False
    assert resolution.reason == SOURCE_REASON_DATASET_NOT_FOUND


def test_exact_timeframe_tokens_do_not_substring_match(tmp_path):
    _touch(tmp_path / "AAA_1h_wyckoff_annotated.csv")
    _touch(tmp_path / "AAA_1w_wyckoff_annotated.csv")

    assert _selected_name(tmp_path, ticker="AAA", tf="4h") is None
    assert _selected_name(tmp_path, ticker="AAA", tf="1d") is None


def test_similar_ticker_names_do_not_cross_match(tmp_path):
    for ticker in ("A", "AA", "AAA", "AI", "AT"):
        _touch(tmp_path / f"{ticker}_4h_wyckoff_annotated.csv")

    assert _selected_name(tmp_path, ticker="AA", tf="4h") == "AA_4h_wyckoff_annotated.csv"
    assert _selected_name(tmp_path, ticker="AI", tf="4h") == "AI_4h_wyckoff_annotated.csv"


def test_ambiguous_duplicate_identity_is_not_selected(tmp_path):
    _touch(tmp_path / "AAA_4h.csv")
    _touch(tmp_path / "AAA_4h_source.csv")

    resolution = resolve_strategy_source_identity(str(tmp_path), "AAA", "4h")

    assert resolution.success is False
    assert resolution.reason == SOURCE_REASON_DATASET_IDENTITY_AMBIGUOUS
    assert _selected_name(tmp_path, ticker="AAA", tf="4h") is None


def test_canonical_and_raw_duplicate_identity_is_ambiguous(tmp_path):
    _touch(tmp_path / "AAA_4h.csv")
    _touch(tmp_path / "AAA_4h_wyckoff_annotated.csv")

    resolution = resolve_strategy_source_identity(str(tmp_path), "AAA", "4h")

    assert resolution.success is False
    assert resolution.reason == SOURCE_REASON_DATASET_IDENTITY_AMBIGUOUS
    assert _selected_name(tmp_path, ticker="AAA", tf="4h") is None


def test_successful_resolution_returns_validated_identity(tmp_path):
    _touch(tmp_path / "brk.b_4H_wyckoff_annotated.csv")

    resolution = resolve_strategy_source_identity(str(tmp_path), "BRK.B", "4h")

    assert resolution.success is True
    assert resolution.status == SOURCE_STATUS_EXACT_MATCH
    assert resolution.identity is not None
    assert resolution.identity.ticker == "BRK.B"
    assert resolution.identity.timeframe == "4h"
    assert resolution.source is not None
    assert resolution.source.name == "brk.b_4H_wyckoff_annotated.csv"


def test_invalid_ticker_and_timeframe_requests_fail_closed(tmp_path):
    _touch(tmp_path / "AAA_4h_wyckoff_annotated.csv")

    assert resolve_strategy_source_identity(str(tmp_path), "", "4h").reason == SOURCE_REASON_INVALID_REQUEST
    assert resolve_strategy_source_identity(str(tmp_path), " AAA", "4h").reason == SOURCE_REASON_INVALID_REQUEST
    assert resolve_strategy_source_identity(str(tmp_path), "AA/A", "4h").reason == SOURCE_REASON_INVALID_REQUEST
    assert resolve_strategy_source_identity(str(tmp_path), "AAA", " 4h").reason == SOURCE_REASON_INVALID_REQUEST
    assert resolve_strategy_source_identity(str(tmp_path), "AAA", "9h").reason == SOURCE_REASON_INVALID_REQUEST


def test_source_root_and_regular_file_enforcement(tmp_path):
    file_root = _touch(tmp_path / "not_a_directory.csv")
    directory_candidate = tmp_path / "AAA_4h_wyckoff_annotated.csv"
    directory_candidate.mkdir()

    assert resolve_strategy_source_identity(str(file_root), "AAA", "4h").reason == SOURCE_REASON_INVALID_SOURCE_ROOT
    assert _selected_name(tmp_path, ticker="AAA", tf="4h") is None


def test_symlink_escape_is_not_selected(tmp_path):
    outside = _touch(tmp_path / "outside.csv")
    root = tmp_path / "root"
    root.mkdir()
    link = root / "AAA_4h_wyckoff_annotated.csv"
    try:
        os.symlink(outside, link)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")

    assert _selected_name(root, ticker="AAA", tf="4h") is None


def test_ranked_candidate_labels_come_from_validated_source_identity(tmp_path):
    report_root = tmp_path / "reports"
    ticker_dir = report_root / "batch_20260729_010203" / "AAA"
    ticker_dir.mkdir(parents=True)
    _touch(ticker_dir / "aaa_4H_wyckoff_annotated.csv")

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260729_010203",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(),
    )

    assert len(results) == 1
    result = results[0]
    assert result["ticker"] == "AAA"
    assert result["tf"] == "4h"
    assert result["csv"] == "batch_20260729_010203/AAA/aaa_4H_wyckoff_annotated.csv"
    assert result["source_csv_name"] == "aaa_4H_wyckoff_annotated.csv"
    assert result["source_status"] == SOURCE_STATUS_EXACT_MATCH
    assert not Path(result["csv"]).is_absolute()


def test_batch_missing_wrong_ticker_and_ambiguous_candidates_are_skipped_independently(tmp_path):
    report_root = tmp_path / "reports"
    batch = report_root / "batch_20260729_010203"
    good = batch / "GOOD"
    missing = batch / "MISS"
    wrong = batch / "AAA"
    ambiguous = batch / "AMB"
    for directory in (good, missing, wrong, ambiguous):
        directory.mkdir(parents=True)

    _touch(good / "GOOD_4h_wyckoff_annotated.csv")
    _touch(wrong / "BBB_4h_wyckoff_annotated.csv")
    _touch(ambiguous / "AMB_4h.csv")
    _touch(ambiguous / "AMB_4h_source.csv")

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260729_010203",
        tickers=["GOOD", "MISS", "AAA", "AMB"],
        tf="4h",
        cfg=StrategyConfig(),
    )

    assert [result["ticker"] for result in results] == ["GOOD"]
    failure_keys = {"MISS", "AAA", "AMB"}
    for result in results:
        assert result["ticker"] not in failure_keys
    assert {"score", "sl", "tp", "rr"}.issubset(results[0])


def test_rank_long_candidates_rejects_escaping_date_glob(tmp_path):
    report_root = tmp_path / "reports"
    outside = tmp_path / "outside" / "AAA"
    outside.mkdir(parents=True)
    _touch(outside / "AAA_4h_wyckoff_annotated.csv")

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="../outside",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(),
    )

    assert results == []


def test_latest_batch_namespace_ignores_batch_csv_summary_folders(tmp_path):
    report_root = tmp_path / "reports"
    valid = report_root / "batch_20260729_010203" / "AAA"
    summary = report_root / "batch_csv_99999999_999999" / "AAA"
    valid.mkdir(parents=True)
    summary.mkdir(parents=True)
    _touch(valid / "AAA_4h_wyckoff_annotated.csv")
    _touch(summary / "AAA_4h_wyckoff_annotated.csv")

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="*",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(),
        use_batch_namespace="latest",
    )

    assert len(results) == 1
    assert results[0]["csv"].startswith("batch_20260729_010203/")
