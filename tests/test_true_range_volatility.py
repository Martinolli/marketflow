from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from marketflow.marketflow_strategy import (
    RR_BELOW_MINIMUM,
    RR_GATE_PASSED,
    TARGET_PROVENANCE_WYCKOFF_TR_HIGH,
    StrategyConfig,
    _atr,
    _resolve_long_trade_levels,
    rank_long_candidates,
)
from marketflow.services.backtest_candidate_service import build_candidate_snapshot_from_strategy_candidate


def _rows(
    *,
    count: int = 14,
    close: float = 100.0,
    high: float = 101.0,
    low: float = 99.0,
    tr_low: float | None = 90.0,
    tr_high: float | None = 130.0,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index in range(count):
        row: dict[str, object] = {
            "timestamp": f"2026-03-{index + 1:02d}",
            "open": close,
            "high": high,
            "low": low,
            "close": close,
            "volume": 1000,
            "wyckoff_phase": "D",
            "wyckoff_confirmed_event": "SOS",
        }
        if tr_low is not None:
            row["tr_low"] = tr_low
        if tr_high is not None:
            row["tr_high"] = tr_high
        rows.append(row)
    return rows


def _write_strategy_csv(path: Path, rows: list[dict[str, object]]) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


def test_atr_uses_first_bar_high_low_when_previous_close_is_absent():
    frame = pd.DataFrame([{"high": 101.0, "low": 99.0, "close": 100.0}])

    assert _atr(frame, n=14) == pytest.approx(2.0)


def test_atr_uses_true_range_for_gap_up_and_gap_down():
    frame = pd.DataFrame(
        [
            {"high": 101.0, "low": 99.0, "close": 100.0},
            {"high": 105.0, "low": 104.0, "close": 104.5},
            {"high": 96.0, "low": 95.0, "close": 95.5},
            {"high": 98.5, "low": 95.5, "close": 97.0},
        ]
    )

    assert _atr(frame, n=4) == pytest.approx((2.0 + 5.0 + 9.5 + 3.0) / 4)


def test_atr_preserves_simple_rolling_window_and_warmup_tail_mean():
    frame = pd.DataFrame(
        [
            {"high": 101.0, "low": 99.0, "close": 100.0},
            {"high": 102.0, "low": 100.0, "close": 101.0},
            {"high": 110.0, "low": 109.0, "close": 109.5},
            {"high": 111.0, "low": 109.0, "close": 110.0},
        ]
    )

    assert _atr(frame.iloc[:2], n=3) == pytest.approx(2.0)
    assert _atr(frame, n=3) == pytest.approx((9.0 + 2.0 + 2.0) / 3)


def test_true_range_volatility_is_prefix_invariant():
    prefix = pd.DataFrame(
        [
            {"high": 101.0, "low": 99.0, "close": 100.0},
            {"high": 105.0, "low": 104.0, "close": 104.5},
        ]
    )
    with_future = pd.concat(
        [
            prefix,
            pd.DataFrame([{"high": 250.0, "low": 20.0, "close": 100.0}]),
        ],
        ignore_index=True,
    )

    assert _atr(prefix, n=2) == _atr(with_future.iloc[:2], n=2)


def test_trade_level_volatility_uses_decision_prefix_not_future_rows():
    rows = _rows(close=100.0, high=101.0, low=99.0, tr_low=90.0, tr_high=130.0, count=14)
    prefix = pd.DataFrame(rows)
    with_future_gap = pd.concat(
        [
            prefix,
            pd.DataFrame(
                [
                    {
                        "timestamp": "2026-03-15",
                        "open": 250.0,
                        "high": 260.0,
                        "low": 240.0,
                        "close": 250.0,
                        "volume": 1000,
                        "wyckoff_phase": "D",
                        "wyckoff_confirmed_event": "SOS",
                        "tr_low": 50.0,
                        "tr_high": 300.0,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

    original = _resolve_long_trade_levels(prefix, StrategyConfig(min_rr=1.0), decision_row_index=13)
    with_future = _resolve_long_trade_levels(with_future_gap, StrategyConfig(min_rr=1.0), decision_row_index=13)

    assert original.stop_loss == with_future.stop_loss
    assert original.rr == with_future.rr
    assert original.volatility.value == with_future.volatility.value


def test_invalid_ohlc_volatility_fails_closed_without_actionable_rr():
    invalid = pd.DataFrame(_rows()).astype(object)
    invalid.loc[13, "high"] = 98.0
    invalid.loc[13, "low"] = 99.0

    resolution = _resolve_long_trade_levels(invalid, StrategyConfig(min_rr=1.0))

    assert resolution.eligible is False
    assert resolution.stop_loss is None
    assert resolution.rr is None
    assert resolution.reason == "VOLATILITY_INVALID"
    assert resolution.volatility.status == "VOLATILITY_INVALID"

    bad_window = _resolve_long_trade_levels(
        pd.DataFrame(_rows()),
        StrategyConfig(min_rr=1.0, atr_len=0),
    )
    assert bad_window.eligible is False
    assert bad_window.volatility.status == "VOLATILITY_INVALID"

    duplicate_close = pd.DataFrame(_rows())
    duplicate_close.insert(len(duplicate_close.columns), "close", 100.0, allow_duplicates=True)
    duplicate_resolution = _resolve_long_trade_levels(duplicate_close, StrategyConfig(min_rr=1.0))
    assert duplicate_resolution.eligible is False
    assert duplicate_resolution.reason == "VOLATILITY_SOURCE_UNSAFE"
    assert duplicate_resolution.volatility.status == "VOLATILITY_SOURCE_UNSAFE"


def test_non_finite_ohlc_and_missing_previous_close_fail_closed():
    non_finite_high = pd.DataFrame(_rows()).astype(object)
    non_finite_high.loc[13, "high"] = float("inf")
    missing_previous_close = pd.DataFrame(_rows()).astype(object)
    missing_previous_close.loc[12, "close"] = None

    for frame in (non_finite_high, missing_previous_close):
        resolution = _resolve_long_trade_levels(frame, StrategyConfig(min_rr=1.0))
        assert resolution.eligible is False
        assert resolution.stop_loss is None
        assert resolution.rr is None
        assert resolution.reason == "VOLATILITY_INVALID"
        assert resolution.volatility.status == "VOLATILITY_INVALID"


def test_timestamp_chronology_must_be_unique_and_monotonic_when_present():
    unsorted = pd.DataFrame(_rows()).astype(object)
    unsorted.loc[12, "timestamp"] = "2026-03-20"
    unsorted.loc[13, "timestamp"] = "2026-03-19"
    duplicate = pd.DataFrame(_rows()).astype(object)
    duplicate.loc[13, "timestamp"] = duplicate.loc[12, "timestamp"]

    for frame in (unsorted, duplicate):
        resolution = _resolve_long_trade_levels(frame, StrategyConfig(min_rr=1.0))
        assert resolution.eligible is False
        assert resolution.stop_loss is None
        assert resolution.rr is None
        assert resolution.reason == "VOLATILITY_SOURCE_UNSAFE"
        assert resolution.volatility.status == "VOLATILITY_SOURCE_UNSAFE"


def test_missing_high_low_malformed_numeric_and_zero_range_fail_closed():
    for column in ("high", "low"):
        frame = pd.DataFrame(_rows()).drop(columns=[column])
        resolution = _resolve_long_trade_levels(frame, StrategyConfig(min_rr=1.0))
        assert resolution.eligible is False
        assert resolution.stop_loss is None
        assert resolution.reason == "VOLATILITY_NOT_AVAILABLE"
        assert resolution.volatility.status == "VOLATILITY_NOT_AVAILABLE"

    malformed = pd.DataFrame(_rows()).astype(object)
    malformed.loc[13, "low"] = "not-a-number"
    malformed_resolution = _resolve_long_trade_levels(malformed, StrategyConfig(min_rr=1.0))
    assert malformed_resolution.eligible is False
    assert malformed_resolution.reason == "VOLATILITY_INVALID"
    assert malformed_resolution.volatility.status == "VOLATILITY_INVALID"

    flat = pd.DataFrame(_rows(close=100.0, high=100.0, low=100.0, tr_low=90.0, tr_high=130.0))
    flat_resolution = _resolve_long_trade_levels(flat, StrategyConfig(min_rr=1.0))
    assert flat_resolution.eligible is False
    assert flat_resolution.stop_loss is None
    assert flat_resolution.rr is None
    assert flat_resolution.reason == "VOLATILITY_INVALID"
    assert flat_resolution.volatility.status == "VOLATILITY_INVALID"


def test_gap_aware_volatility_widens_stop_without_changing_target_or_threshold_semantics():
    rows = _rows(close=100.0, high=101.0, low=99.0, tr_low=90.0, tr_high=130.0)
    rows[-1].update({"open": 110.0, "high": 111.0, "low": 110.0, "close": 110.0})
    frame = pd.DataFrame(rows)

    loose_gate = _resolve_long_trade_levels(frame, StrategyConfig(min_rr=1.0))
    strict_gate = _resolve_long_trade_levels(frame, StrategyConfig(min_rr=4.0))

    expected_atr = ((13 * 2.0) + 11.0) / 14
    expected_stop = 110.0 - (2.0 * expected_atr)
    assert loose_gate.stop_loss == pytest.approx(expected_stop)
    assert loose_gate.target.target_price == strict_gate.target.target_price == 130.0
    assert loose_gate.target.provenance == strict_gate.target.provenance == TARGET_PROVENANCE_WYCKOFF_TR_HIGH
    assert loose_gate.rr == strict_gate.rr
    assert loose_gate.rr_status == RR_GATE_PASSED
    assert strict_gate.rr_status == RR_BELOW_MINIMUM
    assert loose_gate.volatility.status == "VOLATILITY_RESOLVED"
    assert loose_gate.volatility.provenance == "TRUE_RANGE_SIMPLE_ROLLING"


def test_ranked_candidate_and_backtest_snapshot_carry_volatility_diagnostics(tmp_path):
    report_root = tmp_path / "reports"
    source_dir = report_root / "batch_20260730_010203" / "GAP"
    source_dir.mkdir(parents=True)
    rows = _rows(close=100.0, high=101.0, low=99.0, tr_low=90.0, tr_high=130.0)
    rows[-1].update({"open": 110.0, "high": 111.0, "low": 110.0, "close": 110.0})
    _write_strategy_csv(source_dir / "GAP_4h_wyckoff_annotated.csv", rows)

    candidates = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260730_010203",
        tickers=["GAP"],
        tf="4h",
        cfg=StrategyConfig(min_rr=1.0),
    )

    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate["volatility_status"] == "VOLATILITY_RESOLVED"
    assert candidate["volatility_provenance"] == "TRUE_RANGE_SIMPLE_ROLLING"
    assert candidate["volatility_window"] == 14
    snapshot = build_candidate_snapshot_from_strategy_candidate(candidate)["snapshot"]
    assert snapshot["volatility_status"] == "VOLATILITY_RESOLVED"
    assert snapshot["volatility_provenance"] == "TRUE_RANGE_SIMPLE_ROLLING"
