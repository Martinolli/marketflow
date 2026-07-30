from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from marketflow.marketflow_strategy import (
    RR_BELOW_MINIMUM,
    RR_GATE_PASSED,
    TARGET_INVALID,
    TARGET_NOT_AVAILABLE,
    TARGET_RESOLVED,
    TARGET_SOURCE_AMBIGUOUS,
    TARGET_PROVENANCE_WYCKOFF_TR_HIGH,
    StrategyConfig,
    _derive_sl_tp_long,
    _resolve_long_target,
    _resolve_long_trade_levels,
    _rr,
    rank_long_candidates,
)
from marketflow.marketflow_wyckoff_confirmation_adapter import ConfirmCfg, WyckoffConfirmationAdapter


def _rows(
    *,
    close: float = 100.0,
    tr_low: float | None = 95.0,
    tr_high: float | None = 112.0,
    count: int = 25,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index in range(count):
        row: dict[str, object] = {
            "timestamp": f"2026-01-{(index % 28) + 1:02d}",
            "open": close - 1,
            "high": close + 2,
            "low": close - 2,
            "close": close,
            "wyckoff_phase": "D",
            "wyckoff_confirmed_event": "SOS",
            "wyckoff_confirmed_event_occurrence": index == 0,
        }
        if tr_low is not None:
            row["tr_low"] = tr_low
        if tr_high is not None:
            row["tr_high"] = tr_high
        rows.append(row)
    return rows


def _frame(
    *,
    close: float = 100.0,
    tr_low: float | None = 95.0,
    tr_high: float | None = 112.0,
    count: int = 25,
) -> pd.DataFrame:
    return pd.DataFrame(_rows(close=close, tr_low=tr_low, tr_high=tr_high, count=count))


def _write_csv(path: Path, rows: list[dict[str, object]]) -> Path:
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def test_reproduces_baseline_circular_target_behavior_before_correction():
    entry = 100.0
    stop = 95.0

    target_rr_2 = entry + 2.0 * (entry - stop)
    target_rr_3 = entry + 3.0 * (entry - stop)

    assert target_rr_2 == 110.0
    assert target_rr_3 == 115.0
    assert target_rr_2 != target_rr_3


def test_corrected_target_behavior_is_not_circular():
    frame = _frame(close=100.0, tr_high=112.0)

    _, target_rr_2, rr_2 = _derive_sl_tp_long(frame, StrategyConfig(min_rr=2.0))
    _, target_rr_3, rr_3 = _derive_sl_tp_long(frame, StrategyConfig(min_rr=3.0))

    assert target_rr_2 == target_rr_3
    assert rr_2 == pytest.approx((target_rr_2 - 100.0) / 5.0)
    assert rr_3 == pytest.approx((target_rr_3 - 100.0) / 5.0)


def test_target_is_independent_of_minimum_rr_values():
    frame = _frame(close=100.0, tr_high=112.0)

    targets = [_derive_sl_tp_long(frame, StrategyConfig(min_rr=value))[1] for value in (1.0, 2.0, 3.0)]

    assert targets == [112.0, 112.0, 112.0]


def test_rr_gate_changes_eligibility_without_changing_target():
    frame = _frame(close=100.0, tr_high=112.0)

    passed = _resolve_long_trade_levels(frame, StrategyConfig(min_rr=2.0))
    failed = _resolve_long_trade_levels(frame, StrategyConfig(min_rr=3.0))

    assert passed.target.target_price == failed.target.target_price == 112.0
    assert passed.rr == failed.rr == pytest.approx(2.4)
    assert passed.rr_status == RR_GATE_PASSED
    assert failed.rr_status == RR_BELOW_MINIMUM


def test_target_resolution_validates_long_target_inputs():
    assert _resolve_long_target(_frame(tr_high=101.0), entry=100.0).status == TARGET_RESOLVED
    assert _resolve_long_target(_frame(tr_high=100.0), entry=100.0).status == TARGET_INVALID
    assert _resolve_long_target(_frame(tr_high=99.0), entry=100.0).status == TARGET_INVALID
    assert _resolve_long_target(_frame(tr_high=None), entry=100.0).status == TARGET_NOT_AVAILABLE
    assert _resolve_long_target(_frame(tr_high=float("nan")), entry=100.0).status == TARGET_INVALID
    assert _resolve_long_target(_frame(tr_high=float("inf")), entry=100.0).status == TARGET_INVALID


def test_ambiguous_duplicate_tr_high_sources_fail_closed():
    frame = _frame(tr_high=None)
    frame.insert(len(frame.columns), "tr_high", 112.0)
    frame.insert(len(frame.columns), "tr_high", 115.0, allow_duplicates=True)

    resolution = _resolve_long_target(frame, entry=100.0)

    assert resolution.status == TARGET_SOURCE_AMBIGUOUS
    assert resolution.target_price is None


def test_risk_reward_validation_rejects_invalid_values():
    assert _rr(100.0, 95.0, 110.0) == pytest.approx(2.0)
    assert _rr(100.0, 100.0, 110.0) is None
    assert _rr(100.0, 101.0, 110.0) is None
    assert _rr(100.0, 95.0, 100.0) is None
    assert _rr(100.0, 95.0, 99.0) is None
    assert _rr(float("nan"), 95.0, 110.0) is None


def test_invalid_minimum_rr_fails_closed():
    for value in (0.0, -1.0, float("nan"), float("inf")):
        resolution = _resolve_long_trade_levels(_frame(), StrategyConfig(min_rr=value))
        assert resolution.eligible is False
        assert resolution.rr is None


def test_malformed_numeric_level_inputs_fail_closed():
    malformed_close = _frame().astype(object)
    malformed_close.loc[24, "close"] = "bad"
    malformed_ohlc = _frame().astype(object)
    malformed_ohlc.loc[24, "high"] = "bad"
    malformed_tr_low = _frame().astype(object)
    malformed_tr_low.loc[24, "tr_low"] = "bad"

    for frame in (malformed_close, malformed_ohlc, malformed_tr_low):
        resolution = _resolve_long_trade_levels(frame, StrategyConfig(min_rr=1.0))
        assert resolution.eligible is False
        assert resolution.rr is None


def test_no_rounding_induced_false_pass():
    frame = _frame(close=100.0, tr_high=109.999999)

    resolution = _resolve_long_trade_levels(frame, StrategyConfig(min_rr=2.0))

    assert round(resolution.rr or 0.0, 2) == 2.0
    assert resolution.eligible is False
    assert resolution.rr_status == RR_BELOW_MINIMUM


def test_target_resolution_does_not_use_future_rows():
    frame = _frame(close=100.0, tr_high=112.0, count=30)
    decision = _resolve_long_target(frame, entry=100.0, decision_row_index=20)
    with_future = pd.concat(
        [
            frame,
            pd.DataFrame(
                [
                    {
                        "timestamp": "2026-02-01",
                        "open": 100,
                        "high": 999,
                        "low": 99,
                        "close": 100,
                        "tr_high": 999,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

    after_future = _resolve_long_target(with_future, entry=100.0, decision_row_index=20)

    assert decision.target_price == after_future.target_price == 112.0


def test_wyckoff_tr_high_columns_are_point_in_time_target_sources():
    rows: list[dict[str, object]] = []
    for index in range(8):
        rows.append(
            {
                "open": 100.0,
                "high": 101.0,
                "low": 99.0,
                "close": 99.4 if index == 5 else 100.0,
                "volume": 1000.0,
                "wyckoff_event": "SPRING" if index == 5 else "",
            }
        )
    annotated = pd.DataFrame(rows)

    adapter = WyckoffConfirmationAdapter(ConfirmCfg(pass_threshold=0.0))
    enriched, _ = adapter.score_annotated(annotated)
    with_future_extremes, future_events = adapter.score_annotated(
        pd.concat(
            [
                annotated,
                pd.DataFrame(
                    [
                        {
                            "open": 100.0,
                            "high": 150.0,
                            "low": 50.0,
                            "close": 100.0,
                            "volume": 1000.0,
                            "wyckoff_event": "",
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )
    )

    assert pd.isna(enriched.loc[0, "tr_low"])
    assert pd.isna(enriched.loc[0, "tr_high"])
    assert enriched.loc[5, "tr_high"] == 101.0
    assert enriched.loc[5, "tr_low"] == 99.0
    assert with_future_extremes.loc[5, "tr_high"] == enriched.loc[5, "tr_high"]
    assert with_future_extremes.loc[5, "tr_low"] == enriched.loc[5, "tr_low"]
    assert with_future_extremes.loc[8, "tr_high"] > enriched.loc[5, "tr_high"]
    assert with_future_extremes.loc[8, "tr_low"] < enriched.loc[5, "tr_low"]
    assert enriched.loc[5, "wyckoff_confirmed_event"] == with_future_extremes.loc[5, "wyckoff_confirmed_event"]
    if enriched.loc[5, "wyckoff_confirmed_event"]:
        event = next(item for item in future_events if item["price"] == pytest.approx(99.4))
        assert event["tr_high"] == enriched.loc[5, "tr_high"]
        assert event["tr_low"] == enriched.loc[5, "tr_low"]


def test_rank_long_candidates_uses_structural_target_not_minimum_rr(tmp_path):
    report_root = tmp_path / "reports"
    source_dir = report_root / "batch_20260729_010203" / "AAA"
    source_dir.mkdir(parents=True)
    _write_csv(source_dir / "AAA_4h_wyckoff_annotated.csv", _rows(close=100.0, tr_high=112.0))

    min_2 = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260729_010203",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(min_rr=2.0),
    )
    min_3 = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260729_010203",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(min_rr=3.0),
    )

    assert len(min_2) == 1
    assert min_2[0]["tp"] == 112.0
    assert min_2[0]["rr"] == pytest.approx(2.4)
    assert min_2[0]["target_status"] == TARGET_RESOLVED
    assert min_2[0]["target_provenance"] == TARGET_PROVENANCE_WYCKOFF_TR_HIGH
    assert min_3 == []


def test_rank_long_candidates_skips_missing_invalid_and_ambiguous_targets(tmp_path):
    report_root = tmp_path / "reports"
    batch = report_root / "batch_20260729_010203"
    valid = batch / "VALID"
    missing = batch / "MISS"
    invalid = batch / "BAD"
    ambiguous = batch / "AMB"
    for directory in (valid, missing, invalid, ambiguous):
        directory.mkdir(parents=True)

    valid_rows = _rows(close=100.0, tr_high=112.0)
    for row in valid_rows:
        row["pnf_score"] = 0.5
    _write_csv(valid / "VALID_4h_wyckoff_annotated.csv", valid_rows)
    (valid / "VALID_4h_mc_summary.json").write_text(
        json.dumps({"tf": "4h", "metrics_from_now": {"pop_tp_first": 0.5}}),
        encoding="utf-8",
    )
    _write_csv(missing / "MISS_4h_wyckoff_annotated.csv", _rows(close=100.0, tr_high=None))
    _write_csv(invalid / "BAD_4h_wyckoff_annotated.csv", _rows(close=100.0, tr_high=99.0))
    ambiguous_frame = _frame(close=100.0, tr_high=None)
    ambiguous_frame.insert(len(ambiguous_frame.columns), "tr_high", 112.0)
    ambiguous_frame.insert(len(ambiguous_frame.columns), "tr_high", 115.0, allow_duplicates=True)
    ambiguous_frame.to_csv(ambiguous / "AMB_4h_wyckoff_annotated.csv", index=False)

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260729_010203",
        tickers=["VALID", "MISS", "BAD", "AMB"],
        tf="4h",
            cfg=StrategyConfig(min_rr=2.0, max_event_age_bars=24, use_mc=True, use_pnf=True),
    )

    assert [result["ticker"] for result in results] == ["VALID"]
    assert results[0]["score"] == pytest.approx(73.33333333333333)
    assert results[0]["score_status"] == "SCORE_COMPLETE"
    assert results[0]["event_status"] == "EVENT_CURRENT"
