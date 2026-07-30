from __future__ import annotations

from pathlib import Path

import pandas as pd

from marketflow.marketflow_strategy import (
    EVENT_CURRENT,
    EVENT_INVALID,
    EVENT_NOT_AVAILABLE,
    EVENT_PROVENANCE_WYCKOFF_CONFIRMED_EVENT,
    EVENT_RECENCY_POLICY_NOT_CONFIGURED,
    EVENT_SOURCE_UNSAFE,
    EVENT_STALE,
    SOURCE_STATUS_EXACT_MATCH,
    StrategyConfig,
    _event_score,
    _event_score_for_resolution,
    _extract_context,
    _resolve_wyckoff_event,
    rank_long_candidates,
)
from marketflow.services.backtest_candidate_service import normalize_candidate_snapshot
from marketflow.services.backtest_candidate_service import build_candidate_snapshot_from_strategy_candidate
from marketflow.services.walk_forward_validation_service import (
    build_walk_forward_candidate_from_row,
    build_walk_forward_cases_from_csv,
)


def _frame(events: list[object], *, duplicate_timestamp: bool = False) -> pd.DataFrame:
    rows = []
    for index, event in enumerate(events):
        timestamp = pd.Timestamp("2026-01-01") + pd.Timedelta(days=index)
        if duplicate_timestamp and index == len(events) - 1:
            timestamp = pd.Timestamp("2026-01-01")
        close = 100 + index
        rows.append(
            {
                "timestamp": timestamp,
                "open": close - 1,
                "high": close + 2,
                "low": close - 2,
                "close": close,
                "tr_high": close + 10,
                "tr_low": close - 5,
                "wyckoff_phase": "D",
                "wyckoff_confirmed_event": event,
            }
        )
    return pd.DataFrame(rows)


def _frame_with_occurrence_markers(events: list[object], markers: list[object]) -> pd.DataFrame:
    frame = _frame(events)
    frame["wyckoff_confirmed_event_occurrence"] = markers
    return frame


def test_old_missing_tail_event_without_policy_is_not_score_eligible():
    frame = _frame([pd.NA, pd.NA, "SPRING_WEAK", *([pd.NA] * 27)])

    context = _extract_context(frame, StrategyConfig())

    assert context["event"] == "SPRING_WEAK"
    assert context["event_occurrence_row_index"] == 2
    assert context["event_decision_row_index"] == 29
    assert context["event_age_bars"] == 27
    assert context["event_status"] == EVENT_RECENCY_POLICY_NOT_CONFIGURED
    assert context["event_scoring_eligible"] is False
    assert _event_score(context["event"]) == 1.0
    assert _event_score_for_resolution(context["event_resolution"]) == 0.0


def test_event_age_zero_is_current_without_policy():
    resolution = _resolve_wyckoff_event(_frame([pd.NA, "SOS"]), None)

    assert resolution.status == EVENT_CURRENT
    assert resolution.event == "SOS"
    assert resolution.event_age_bars == 0
    assert resolution.provenance == EVENT_PROVENANCE_WYCKOFF_CONFIRMED_EVENT
    assert resolution.scoring_eligible is True
    assert _event_score_for_resolution(resolution) == 1.0


def test_configured_policy_boundary_and_stale_status():
    frame = _frame(["SPRING_WEAK", pd.NA, pd.NA, pd.NA])

    assert _resolve_wyckoff_event(_frame(["SPRING_WEAK"]), 0).status == EVENT_CURRENT
    assert _resolve_wyckoff_event(_frame(["SPRING_WEAK", pd.NA]), 0).status == EVENT_STALE
    assert _resolve_wyckoff_event(frame, 3).status == EVENT_CURRENT
    stale = _resolve_wyckoff_event(frame, 2)

    assert stale.status == EVENT_STALE
    assert stale.event_age_bars == 3
    assert stale.scoring_eligible is False
    assert _event_score_for_resolution(stale) == 0.0


def test_invalid_event_age_policy_values_are_rejected():
    frame = _frame(["SPRING_WEAK"])

    for invalid in (-1, True, 1.5, float("nan"), float("inf"), "2"):
        resolution = _resolve_wyckoff_event(frame, invalid)  # type: ignore[arg-type]
        assert resolution.status == EVENT_INVALID
        assert resolution.scoring_eligible is False
        assert _event_score_for_resolution(resolution) == 0.0


def test_missing_blank_and_unsafe_event_sources_are_diagnosed():
    assert _resolve_wyckoff_event(_frame([pd.NA, ""]), None).status == EVENT_NOT_AVAILABLE
    assert _resolve_wyckoff_event(_frame(["SPRING_WEAK"], duplicate_timestamp=True), None).status == EVENT_CURRENT
    assert _resolve_wyckoff_event(_frame(["SPRING_WEAK", "SOS"], duplicate_timestamp=True), None).status == EVENT_SOURCE_UNSAFE


def test_forward_filled_labels_do_not_create_fresh_occurrences():
    frame = _frame_with_occurrence_markers(
        [pd.NA, "SPRING_WEAK", "SPRING_WEAK", "SPRING_WEAK"],
        [False, True, False, False],
    )

    resolution = _resolve_wyckoff_event(frame, None)

    assert resolution.event == "SPRING_WEAK"
    assert resolution.occurrence_row_index == 1
    assert resolution.event_age_bars == 2
    assert resolution.status == EVENT_RECENCY_POLICY_NOT_CONFIGURED


def test_second_identical_explicit_event_after_blank_is_new_occurrence():
    frame = _frame(["SPRING_WEAK", pd.NA, pd.NA, "SPRING_WEAK"])

    resolution = _resolve_wyckoff_event(frame, 5)

    assert resolution.event == "SPRING_WEAK"
    assert resolution.occurrence_row_index == 3
    assert resolution.event_age_bars == 0
    assert resolution.superseded_event_count == 1
    assert resolution.status == EVENT_CURRENT


def test_consecutive_identical_markerless_confirmed_events_fail_closed_as_ambiguous():
    frame = _frame(["SOS", "SOS"])

    resolution = _resolve_wyckoff_event(frame, 5)

    assert resolution.status == EVENT_SOURCE_UNSAFE
    assert resolution.scoring_eligible is False


def test_consecutive_identical_marker_confirmed_events_are_distinct_occurrences():
    frame = _frame_with_occurrence_markers(["SOS", "SOS"], [True, True])

    resolution = _resolve_wyckoff_event(frame, 5)

    assert resolution.event == "SOS"
    assert resolution.occurrence_row_index == 1
    assert resolution.event_age_bars == 0
    assert resolution.superseded_event_count == 1
    assert resolution.status == EVENT_CURRENT


def test_malformed_occurrence_marker_fails_closed():
    frame = _frame_with_occurrence_markers(["SOS"], ["definitely"])

    resolution = _resolve_wyckoff_event(frame, 5)

    assert resolution.status == EVENT_SOURCE_UNSAFE
    assert resolution.scoring_eligible is False


def test_latest_event_supersedes_older_bullish_event_without_backward_reuse():
    frame = _frame(["SPRING_WEAK", pd.NA, "UT_WEAK", pd.NA])

    resolution = _resolve_wyckoff_event(frame, 5)

    assert resolution.event == "UT_WEAK"
    assert resolution.occurrence_row_index == 2
    assert resolution.superseded_event_count == 1
    assert resolution.status == EVENT_CURRENT
    assert _event_score_for_resolution(resolution) == 0.0


def test_later_scoring_event_supersedes_older_non_scoring_event():
    frame = _frame(["UT_WEAK", pd.NA, "SOS", pd.NA])

    resolution = _resolve_wyckoff_event(frame, 5)

    assert resolution.event == "SOS"
    assert resolution.occurrence_row_index == 2
    assert resolution.superseded_event_count == 1
    assert _event_score_for_resolution(resolution) == 1.0


def test_future_event_does_not_change_historical_decision_row_resolution():
    frame = _frame(["SPRING_WEAK", pd.NA, pd.NA, "SOS"])

    historical = _resolve_wyckoff_event(frame, 10, decision_row_index=2)

    assert historical.event == "SPRING_WEAK"
    assert historical.event_age_bars == 2
    assert historical.occurrence_row_index == 0


def test_future_non_scoring_event_does_not_change_historical_resolution():
    frame = _frame(["SOS", pd.NA, pd.NA, "UT_WEAK"])

    historical = _resolve_wyckoff_event(frame, 10, decision_row_index=2)

    assert historical.event == "SOS"
    assert historical.event_age_bars == 2
    assert historical.occurrence_row_index == 0
    assert _event_score_for_resolution(historical) == 1.0


def test_rank_long_candidates_preserves_candidate_without_unconfigured_event_credit(tmp_path: Path):
    ticker_dir = tmp_path / "batch_20260730_010203" / "AAA"
    ticker_dir.mkdir(parents=True)
    csv_path = ticker_dir / "AAA_1d_wyckoff_annotated.csv"
    _frame(["SPRING_WEAK", *([pd.NA] * 24)]).to_csv(csv_path, index=False)

    result = rank_long_candidates(
        str(tmp_path),
        "batch_20260730_010203",
        ["AAA"],
        "1d",
        StrategyConfig(max_event_age_bars=None),
    )

    assert len(result) == 1
    candidate = result[0]
    assert candidate["event"] == "SPRING_WEAK"
    assert candidate["event_status"] == EVENT_RECENCY_POLICY_NOT_CONFIGURED
    assert candidate["event_scoring_eligible"] is False
    assert candidate["event_age_bars"] == 24
    assert candidate["rr_status"] == "RR_GATE_PASSED"


def test_backtest_snapshot_preserves_event_recency_diagnostics():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100,
            "sl": 95,
            "tp": 110,
            "phase": "D",
            "event": "SPRING_WEAK",
            "event_status": EVENT_STALE,
            "event_age_bars": 12,
            "event_max_age_bars": 5,
            "event_scoring_eligible": False,
            "event_occurrence_row_index": 3,
            "event_decision_row_index": 15,
            "event_reason": EVENT_STALE,
            "signal_row_index": 15,
        }
    )

    assert snapshot["event_status"] == EVENT_STALE
    assert snapshot["event_age_bars"] == 12
    assert snapshot["event_max_age_bars"] == 5
    assert snapshot["event_scoring_eligible"] is False
    assert snapshot["event_occurrence_row_index"] == 3
    assert snapshot["event_decision_row_index"] == 15
    assert snapshot["event_reason"] == EVENT_STALE


def test_backtest_candidate_build_resolves_missing_event_diagnostics_from_source(tmp_path: Path):
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    _frame(["SPRING_WEAK", *([pd.NA] * 9)]).to_csv(csv_path, index=False)

    result = build_candidate_snapshot_from_strategy_candidate(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": str(csv_path),
            "close": 109,
            "sl": 104,
            "tp": 119,
            "phase": "D",
            "signal_row_index": 9,
            "source_status": SOURCE_STATUS_EXACT_MATCH,
        },
        max_event_age_bars=3,
    )

    snapshot = result["snapshot"]
    assert snapshot["event_status"] == EVENT_STALE
    assert snapshot["event_age_bars"] == 9
    assert snapshot["event_max_age_bars"] == 3
    assert snapshot["event_resolution_source"] == "wyckoff_confirmed_event"
    assert snapshot["wyckoff_event"] == "SPRING_WEAK"


def test_backtest_candidate_enrichment_ignores_post_signal_confirmed_events(tmp_path: Path):
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    _frame(["SPRING_WEAK", *([pd.NA] * 8), "SOS"]).to_csv(csv_path, index=False)

    result = build_candidate_snapshot_from_strategy_candidate(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": str(csv_path),
            "close": 108,
            "sl": 103,
            "tp": 118,
            "phase": "D",
            "signal_row_index": 8,
            "source_status": SOURCE_STATUS_EXACT_MATCH,
        },
        max_event_age_bars=20,
    )

    snapshot = result["snapshot"]
    assert snapshot["wyckoff_event"] == "SPRING_WEAK"
    assert snapshot["event_occurrence_row_index"] == 0
    assert snapshot["event_decision_row_index"] == 8
    assert snapshot["event_age_bars"] == 8


def test_backtest_candidate_enrichment_ignores_post_signal_repeated_identical_event(tmp_path: Path):
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    _frame(["SPRING_WEAK", *([pd.NA] * 8), "SPRING_WEAK"]).to_csv(csv_path, index=False)

    result = build_candidate_snapshot_from_strategy_candidate(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": str(csv_path),
            "close": 108,
            "sl": 103,
            "tp": 118,
            "phase": "D",
            "signal_row_index": 8,
            "source_status": SOURCE_STATUS_EXACT_MATCH,
        },
        max_event_age_bars=20,
    )

    snapshot = result["snapshot"]
    assert snapshot["wyckoff_event"] == "SPRING_WEAK"
    assert snapshot["event_occurrence_row_index"] == 0
    assert snapshot["event_decision_row_index"] == 8
    assert snapshot["event_age_bars"] == 8


def test_backtest_candidate_enrichment_without_confirmed_source_fails_closed(tmp_path: Path):
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    frame = _frame([pd.NA, pd.NA]).drop(columns=["wyckoff_confirmed_event"])
    frame["wyckoff_event"] = ["SPRING", pd.NA]
    frame.to_csv(csv_path, index=False)

    result = build_candidate_snapshot_from_strategy_candidate(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": str(csv_path),
            "close": 101,
            "sl": 96,
            "tp": 111,
            "phase": "D",
            "signal_row_index": 1,
            "source_status": SOURCE_STATUS_EXACT_MATCH,
        },
        max_event_age_bars=5,
    )

    snapshot = result["snapshot"]
    assert snapshot["event_status"] == EVENT_NOT_AVAILABLE
    assert snapshot["event_provenance"] is None
    assert snapshot["event_scoring_eligible"] is False
    assert snapshot["event_resolution_source"] is None


def test_backtest_candidate_enrichment_requires_exact_source_identity(tmp_path: Path):
    csv_path = tmp_path / "BBB_1d_wyckoff_annotated.csv"
    _frame(["SOS", pd.NA]).to_csv(csv_path, index=False)

    result = build_candidate_snapshot_from_strategy_candidate(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": str(csv_path),
            "close": 101,
            "sl": 96,
            "tp": 111,
            "phase": "D",
            "signal_row_index": 1,
        },
        max_event_age_bars=5,
    )

    snapshot = result["snapshot"]
    assert snapshot["event_status"] == EVENT_SOURCE_UNSAFE
    assert snapshot["event_provenance"] is None
    assert snapshot["event_scoring_eligible"] is False
    assert snapshot["wyckoff_event"] is None


def test_walk_forward_candidate_resolves_event_from_decision_prefix():
    frame = _frame(["SPRING_WEAK", pd.NA, pd.NA, "SOS"])
    row = frame.iloc[2]

    candidate = build_walk_forward_candidate_from_row(
        row,
        csv_path="AAA_1d_wyckoff_annotated.csv",
        signal_row_index=2,
        total_rows=len(frame),
        profile_name="daily_swing",
        profile_context={"success": True, "horizon_bars": 1},
        event_column="wyckoff_confirmed_event",
        decision_frame=frame.iloc[:3],
        max_event_age_bars=5,
    )

    assert candidate["wyckoff_event"] == "SPRING_WEAK"
    assert candidate["event_status"] == EVENT_CURRENT
    assert candidate["event_age_bars"] == 2
    assert candidate["event_occurrence_row_index"] == 0
    assert candidate["event_decision_row_index"] == 2


def test_walk_forward_case_builder_passes_configured_event_recency_policy(tmp_path: Path):
    path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    _frame(["SPRING_WEAK", *([pd.NA] * 129)]).to_csv(path, index=False)

    result = build_walk_forward_cases_from_csv(
        path,
        profile_name="fast_test",
        min_signal_row=125,
        max_signal_row=125,
        require_mature_future=False,
        include_invalid_cases=True,
        max_event_age_bars=3,
    )

    assert result["success"] is True
    assert result["max_event_age_bars"] == 3
    case = result["cases"][0]
    assert case["wyckoff_event"] == "SPRING_WEAK"
    assert case["event_resolution_source"] == "wyckoff_confirmed_event"
    assert case["event_age_bars"] == 125
    assert case["event_max_age_bars"] == 3
    assert case["event_status"] == EVENT_STALE
    assert case["event_scoring_eligible"] is False


def test_walk_forward_raw_event_fallback_does_not_claim_confirmed_provenance():
    frame = _frame([pd.NA, pd.NA]).drop(columns=["wyckoff_confirmed_event"])
    frame["wyckoff_event"] = ["SPRING", pd.NA]
    row = frame.iloc[1]

    candidate = build_walk_forward_candidate_from_row(
        row,
        csv_path="AAA_1d_wyckoff_annotated.csv",
        signal_row_index=1,
        total_rows=len(frame),
        profile_name="daily_swing",
        profile_context={"success": True, "horizon_bars": 1},
        event_column="wyckoff_event",
        decision_frame=frame.iloc[:2],
        max_event_age_bars=5,
    )

    assert candidate["wyckoff_event"] is None
    assert candidate["wyckoff_event_source"] == "wyckoff_event"
    assert candidate["event_resolution_source"] is None
    assert candidate["event_status"] == EVENT_NOT_AVAILABLE
    assert candidate["event_provenance"] is None
