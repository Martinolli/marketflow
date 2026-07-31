from __future__ import annotations

import ast
import json
from pathlib import Path

import pandas as pd
import pytest

from marketflow.marketflow_strategy import (
    COMPONENT_EVENT,
    COMPONENT_PHASE,
    COMPONENT_PNF,
    COMPONENT_POP,
    COMPONENT_TREND,
    EVIDENCE_AVAILABLE,
    EVIDENCE_DISABLED_BY_CONFIGURATION,
    EVIDENCE_INVALID,
    EVIDENCE_NOT_AVAILABLE,
    SCORE_COMPLETE,
    SCORE_INCOMPLETE,
    SCORE_INVALID,
    StrategyConfig,
    _phase_score,
    _resolve_evidence_components,
    _score_from_evidence,
    rank_long_candidates,
)
from marketflow.services.backtest_candidate_artifact_service import (
    BACKTEST_CANDIDATE_COLUMNS,
    candidate_snapshot_row,
)
from marketflow.services.backtest_candidate_service import (
    LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE,
    build_candidate_snapshot_from_strategy_candidate,
    normalize_candidate_snapshot,
)
from marketflow.services.strategy_service import STRATEGY_COLUMNS
from marketflow.services.walk_forward_validation_artifact_service import CASE_COLUMNS
from marketflow.services.walk_forward_validation_service import build_walk_forward_candidate_from_row


def _rows(*, count: int = 25, pnf_score: object | None = None) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index in range(count):
        row: dict[str, object] = {
            "timestamp": f"2026-01-{index + 1:02d}",
            "open": 100.0,
            "high": 102.0,
            "low": 98.0,
            "close": 100.0,
            "tr_low": 95.0,
            "tr_high": 112.0,
            "wyckoff_phase": "D",
            "wyckoff_confirmed_event": "SOS",
            "wyckoff_confirmed_event_occurrence": index == count - 1,
        }
        if pnf_score is not None:
            row["pnf_score"] = pnf_score
        rows.append(row)
    return rows


def _write_strategy_csv(
    report_root: Path,
    *,
    ticker: str = "AAA",
    tf: str = "1d",
    pnf_score: object | None = None,
) -> Path:
    ticker_dir = report_root / "batch_20260730_010203" / ticker
    ticker_dir.mkdir(parents=True)
    csv_path = ticker_dir / f"{ticker}_{tf}_wyckoff_annotated.csv"
    pd.DataFrame(_rows(pnf_score=pnf_score)).to_csv(csv_path, index=False)
    return csv_path


def _write_mc_summary(source_csv: Path, *, pop: object | None, tf: str = "1d") -> Path:
    path = source_csv.parent / f"{source_csv.stem}_{tf}_mc_summary.json"
    metrics = {} if pop is None else {"pop_tp_first": pop}
    ticker = source_csv.name.split("_", 1)[0]
    path.write_text(
        json.dumps(
            {
                "tf": tf,
                "ticker": ticker,
                "csv": source_csv.name,
                "workflow_type": "CANONICAL_STRATEGY_DECISION_SUPPORT",
                "metrics_from_now": metrics,
            }
        ),
        encoding="utf-8",
    )
    return path


def _rank(report_root: Path, cfg: StrategyConfig) -> list[dict]:
    return rank_long_candidates(
        str(report_root),
        "batch_20260730_010203",
        ["AAA"],
        "1d",
        cfg,
    )


def test_reproduces_old_missing_monte_carlo_placeholder_risk(tmp_path: Path):
    _write_strategy_csv(tmp_path)

    candidate = _rank(tmp_path, StrategyConfig(use_mc=True, use_pnf=False))[0]

    assert candidate["score_status"] == SCORE_INCOMPLETE
    assert candidate["score"] is None
    assert candidate["composite_score"] is None
    assert candidate["pop"] is None
    assert candidate["pop_evidence_status"] == EVIDENCE_NOT_AVAILABLE
    assert COMPONENT_POP in candidate["missing_components"]


def test_reproduces_old_missing_point_and_figure_placeholder_risk(tmp_path: Path):
    _write_strategy_csv(tmp_path)

    candidate = _rank(tmp_path, StrategyConfig(use_mc=False, use_pnf=True))[0]

    assert candidate["score_status"] == SCORE_INCOMPLETE
    assert candidate["score"] is None
    assert candidate["pnf_score"] is None
    assert candidate["pnf_evidence_status"] == EVIDENCE_NOT_AVAILABLE
    assert COMPONENT_PNF in candidate["missing_components"]


def test_disabled_components_are_not_valid_neutral_scores(tmp_path: Path):
    _write_strategy_csv(tmp_path)

    candidate = _rank(tmp_path, StrategyConfig(use_mc=False, use_pnf=False))[0]

    assert candidate["score_status"] == SCORE_COMPLETE
    assert candidate["pop"] is None
    assert candidate["pnf_score"] is None
    assert candidate["pop_evidence_status"] == EVIDENCE_DISABLED_BY_CONFIGURATION
    assert candidate["pnf_evidence_status"] == EVIDENCE_DISABLED_BY_CONFIGURATION
    assert set(candidate["disabled_components"]) == {COMPONENT_POP, COMPONENT_PNF}
    assert candidate["active_evidence_profile"] == "phase,event,trend"
    assert candidate["active_weight_total"] == pytest.approx(4.0)
    assert candidate["score"] == pytest.approx(93.75)
    assert candidate["score_profile_calibration"] == "SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED"
    assert candidate["rank_eligible"] is False


def test_valid_neutral_monte_carlo_pop_remains_available(tmp_path: Path):
    source_csv = _write_strategy_csv(tmp_path)
    _write_mc_summary(source_csv, pop=0.5)

    candidate = _rank(tmp_path, StrategyConfig(use_mc=True, use_pnf=False))[0]

    assert candidate["score_status"] == SCORE_COMPLETE
    assert candidate["pop"] == pytest.approx(0.5)
    assert candidate["pop_evidence_status"] == EVIDENCE_AVAILABLE
    assert candidate["pop_evidence_provenance"] == "MONTE_CARLO_POP"
    assert candidate["score"] == pytest.approx(76.92307692307693)


def test_valid_non_neutral_monte_carlo_pop_scores_without_formula_change(tmp_path: Path):
    source_csv = _write_strategy_csv(tmp_path)
    _write_mc_summary(source_csv, pop=0.8)

    candidate = _rank(tmp_path, StrategyConfig(use_mc=True, use_pnf=False))[0]

    assert candidate["score_status"] == SCORE_COMPLETE
    assert candidate["pop"] == pytest.approx(0.8)
    assert candidate["score"] == pytest.approx(((2.0 * 1.0) + 1.0 + (2.5 * 0.8) + 0.75) / 6.5 * 100.0)


def test_invalid_monte_carlo_pop_is_not_neutral(tmp_path: Path):
    source_csv = _write_strategy_csv(tmp_path)
    _write_mc_summary(source_csv, pop=1.5)

    candidate = _rank(tmp_path, StrategyConfig(use_mc=True, use_pnf=False))[0]

    assert candidate["score_status"] == SCORE_INCOMPLETE
    assert candidate["score"] is None
    assert candidate["pop"] is None
    assert candidate["pop_evidence_status"] == EVIDENCE_INVALID
    assert COMPONENT_POP in candidate["invalid_components"]


def test_malformed_monte_carlo_pop_is_invalid_not_unavailable(tmp_path: Path):
    source_csv = _write_strategy_csv(tmp_path)
    _write_mc_summary(source_csv, pop="bad")

    candidate = _rank(tmp_path, StrategyConfig(use_mc=True, use_pnf=False))[0]

    assert candidate["score_status"] == SCORE_INCOMPLETE
    assert candidate["pop"] is None
    assert candidate["pop_evidence_status"] == EVIDENCE_INVALID
    assert COMPONENT_POP in candidate["invalid_components"]


def test_valid_neutral_point_and_figure_score_remains_available(tmp_path: Path):
    _write_strategy_csv(tmp_path, pnf_score=0.5)

    candidate = _rank(tmp_path, StrategyConfig(use_mc=False, use_pnf=True))[0]

    assert candidate["score_status"] == SCORE_COMPLETE
    assert candidate["pnf_score"] == pytest.approx(0.5)
    assert candidate["pnf_evidence_status"] == EVIDENCE_AVAILABLE
    assert candidate["pnf_evidence_provenance"] == "PNF_SCORE_COLUMN"
    assert candidate["score"] == pytest.approx(85.0)


def test_valid_non_neutral_point_and_figure_score_scores(tmp_path: Path):
    _write_strategy_csv(tmp_path, pnf_score=0.8)

    candidate = _rank(tmp_path, StrategyConfig(use_mc=False, use_pnf=True))[0]

    assert candidate["score_status"] == SCORE_COMPLETE
    assert candidate["pnf_score"] == pytest.approx(0.8)
    assert candidate["score"] == pytest.approx(((2.0 * 1.0) + 1.0 + 0.8 + 0.75) / 5.0 * 100.0)


def test_invalid_point_and_figure_score_is_not_neutral(tmp_path: Path):
    _write_strategy_csv(tmp_path, pnf_score="bad")

    candidate = _rank(tmp_path, StrategyConfig(use_mc=False, use_pnf=True))[0]

    assert candidate["score_status"] == SCORE_INCOMPLETE
    assert candidate["score"] is None
    assert candidate["pnf_score"] is None
    assert candidate["pnf_evidence_status"] == EVIDENCE_INVALID
    assert COMPONENT_PNF in candidate["invalid_components"]


def test_phase_event_and_trend_components_remain_semantic_evidence():
    frame = pd.DataFrame(_rows())
    components = _resolve_evidence_components(frame, StrategyConfig(use_mc=False, use_pnf=False), pop=None)
    by_component = {component.component: component for component in components}

    assert by_component[COMPONENT_PHASE].status == EVIDENCE_AVAILABLE
    assert by_component[COMPONENT_PHASE].score == pytest.approx(_phase_score("D"))
    assert by_component[COMPONENT_EVENT].status == EVIDENCE_AVAILABLE
    assert by_component[COMPONENT_EVENT].score == pytest.approx(1.0)
    assert by_component[COMPONENT_TREND].status == EVIDENCE_AVAILABLE
    assert by_component[COMPONENT_TREND].score == pytest.approx(0.75)


def test_event_semantic_zero_remains_available():
    frame = pd.DataFrame(_rows())
    frame.loc[len(frame) - 1, "wyckoff_confirmed_event"] = "UT_WEAK"
    components = _resolve_evidence_components(frame, StrategyConfig(), pop=None)
    event = {component.component: component for component in components}[COMPONENT_EVENT]

    assert event.status == EVIDENCE_AVAILABLE
    assert event.score == pytest.approx(0.0)


def test_stale_event_evidence_is_not_available_complete_score_input():
    frame = pd.DataFrame(_rows())
    frame["wyckoff_confirmed_event_occurrence"] = [index == 0 for index in range(len(frame))]
    components = _resolve_evidence_components(
        frame,
        StrategyConfig(max_event_age_bars=1),
        pop=None,
    )
    event = {component.component: component for component in components}[COMPONENT_EVENT]
    resolution = _score_from_evidence(components)

    assert event.status == EVIDENCE_NOT_AVAILABLE
    assert event.score is None
    assert event.reason == "EVENT_STALE"
    assert resolution.status == SCORE_INCOMPLETE
    assert COMPONENT_EVENT in resolution.missing_components


def test_unconfigured_old_event_evidence_is_not_available_complete_score_input():
    frame = pd.DataFrame(_rows())
    frame["wyckoff_confirmed_event_occurrence"] = [index == 0 for index in range(len(frame))]
    components = _resolve_evidence_components(frame, StrategyConfig(), pop=None)
    event = {component.component: component for component in components}[COMPONENT_EVENT]

    assert event.status == EVIDENCE_NOT_AVAILABLE
    assert event.score is None
    assert event.reason == "EVENT_RECENCY_POLICY_NOT_CONFIGURED"
    assert _score_from_evidence(components).status == SCORE_INCOMPLETE


def test_missing_event_evidence_is_not_available_complete_score_input():
    frame = pd.DataFrame(_rows())
    frame["wyckoff_confirmed_event"] = pd.NA
    frame["wyckoff_confirmed_event_occurrence"] = False
    components = _resolve_evidence_components(frame, StrategyConfig(), pop=None)
    event = {component.component: component for component in components}[COMPONENT_EVENT]

    assert event.status == EVIDENCE_NOT_AVAILABLE
    assert event.score is None
    assert event.reason == "EVENT_NOT_AVAILABLE"
    assert _score_from_evidence(components).status == SCORE_INCOMPLETE


def test_composite_complete_matches_previous_genuine_evidence_formula():
    frame = pd.DataFrame(_rows(pnf_score=0.8))
    components = _resolve_evidence_components(frame, StrategyConfig(use_mc=True, use_pnf=True), pop=0.7)

    resolution = _score_from_evidence(components)

    assert resolution.status == SCORE_COMPLETE
    assert resolution.composite_score == pytest.approx(
        ((2.0 * 1.0) + 1.0 + (1.0 * 0.8) + (2.5 * 0.7) + (1.0 * 0.75)) / 7.5 * 100.0
    )


def test_missing_active_component_does_not_renormalize_to_complete_score():
    frame = pd.DataFrame(_rows())
    components = _resolve_evidence_components(frame, StrategyConfig(use_mc=True, use_pnf=False), pop=None)

    resolution = _score_from_evidence(components)

    assert resolution.status == SCORE_INCOMPLETE
    assert resolution.composite_score is None
    assert resolution.available_weight_total == pytest.approx(4.0)
    assert resolution.active_weight_total == pytest.approx(6.5)
    assert COMPONENT_POP in resolution.missing_components


def test_zero_active_weight_profile_is_invalid():
    frame = pd.DataFrame(_rows())
    cfg = StrategyConfig(use_mc=False, use_pnf=False, weights={COMPONENT_PHASE: 0, COMPONENT_EVENT: 0, COMPONENT_TREND: 0, COMPONENT_PNF: 1, COMPONENT_POP: 1})

    resolution = _score_from_evidence(_resolve_evidence_components(frame, cfg, pop=None))

    assert resolution.status == SCORE_INVALID
    assert resolution.composite_score is None


def test_missing_active_component_with_zero_weight_is_still_incomplete():
    frame = pd.DataFrame(_rows())
    cfg = StrategyConfig(use_mc=True, use_pnf=False, weights={COMPONENT_PHASE: 2, COMPONENT_EVENT: 1, COMPONENT_TREND: 1, COMPONENT_POP: 0, COMPONENT_PNF: 1})

    resolution = _score_from_evidence(_resolve_evidence_components(frame, cfg, pop=None))

    assert resolution.status == SCORE_INCOMPLETE
    assert COMPONENT_POP in resolution.missing_components


def test_missing_configured_weight_for_active_component_is_invalid():
    frame = pd.DataFrame(_rows())
    cfg = StrategyConfig(use_mc=True, use_pnf=False, weights={COMPONENT_PHASE: 2, COMPONENT_EVENT: 1, COMPONENT_TREND: 1, COMPONENT_PNF: 1})

    resolution = _score_from_evidence(_resolve_evidence_components(frame, cfg, pop=0.7))

    assert resolution.status == SCORE_INCOMPLETE
    assert COMPONENT_POP in resolution.invalid_components


def test_batch_complete_and_incomplete_candidates_are_not_compared(tmp_path: Path):
    complete_csv = _write_strategy_csv(tmp_path, ticker="AAA", pnf_score=0.8)
    _write_mc_summary(complete_csv, pop=0.6)
    _write_strategy_csv(tmp_path, ticker="BBB", pnf_score=0.8)

    results = rank_long_candidates(
        str(tmp_path),
        "batch_20260730_010203",
        ["AAA", "BBB"],
        "1d",
        StrategyConfig(use_mc=True, use_pnf=True),
    )

    assert [row["ticker"] for row in results] == ["AAA", "BBB"]
    assert results[0]["score_status"] == SCORE_COMPLETE
    assert results[0]["rank_eligible"] is True
    assert results[1]["score_status"] == SCORE_INCOMPLETE
    assert results[1]["rank_eligible"] is False
    assert results[1]["score"] is None


def test_backtest_snapshot_and_artifact_preserve_score_diagnostics():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score": None,
            "score_status": SCORE_INCOMPLETE,
            "active_evidence_profile": "phase,event,pop,trend",
            "missing_components": [COMPONENT_POP],
        }
    )

    assert snapshot["strategy_score"] is None
    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["missing_components"] == [COMPONENT_POP]
    row = candidate_snapshot_row({"snapshot": snapshot, "validation": {"status": "valid"}})
    assert "score_status" in BACKTEST_CANDIDATE_COLUMNS
    assert row["score_status"] == SCORE_INCOMPLETE


def test_legacy_pop_neutral_without_status_is_not_available_evidence():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "pop": 0.5,
        }
    )

    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["score_reason"] == LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE
    assert snapshot["pop_evidence_status"] == EVIDENCE_NOT_AVAILABLE
    assert snapshot["pop_evidence_score"] is None
    assert snapshot["pop_evidence_scoring_eligible"] is False
    assert snapshot["rank_eligible"] is False


def test_legacy_pnf_neutral_without_status_is_not_available_evidence():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "pnf_score": 0.5,
        }
    )

    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["pnf_evidence_status"] == EVIDENCE_NOT_AVAILABLE
    assert snapshot["pnf_score"] is None
    assert snapshot["pnf_evidence_score"] is None
    assert snapshot["pnf_evidence_scoring_eligible"] is False


def test_legacy_composite_without_component_statuses_is_non_actionable():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score": 73.33333333333333,
            "composite_score": 73.33333333333333,
        }
    )

    assert snapshot["strategy_score"] == pytest.approx(73.33333333333333)
    assert snapshot["composite_score"] is None
    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["missing_components"] == [
        COMPONENT_PHASE,
        COMPONENT_EVENT,
        COMPONENT_PNF,
        COMPONENT_POP,
        COMPONENT_TREND,
    ]
    assert snapshot["rank_eligible"] is False


def test_existing_explicit_safe_diagnostics_are_not_overwritten():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score": 73.33333333333333,
            "composite_score": 73.33333333333333,
            "score_status": SCORE_COMPLETE,
            "active_evidence_profile": "phase,event,pnf,pop,trend",
            "active_weight_total": 7.5,
            "rank_eligible": True,
            "phase_evidence_status": EVIDENCE_AVAILABLE,
            "phase_evidence_score": 1.0,
            "phase_evidence_active_weight": 2.0,
            "phase_evidence_provenance": "WYCKOFF_PHASE",
            "phase_evidence_scoring_eligible": True,
            "event_evidence_status": EVIDENCE_AVAILABLE,
            "event_evidence_score": 1.0,
            "event_evidence_active_weight": 1.0,
            "event_evidence_provenance": "WYCKOFF_EVENT_RESOLUTION",
            "event_evidence_scoring_eligible": True,
            "pnf_evidence_status": EVIDENCE_AVAILABLE,
            "pnf_evidence_score": 0.8,
            "pnf_evidence_active_weight": 1.0,
            "pnf_evidence_provenance": "PNF_SCORE_COLUMN",
            "pnf_evidence_scoring_eligible": True,
            "pop_evidence_status": EVIDENCE_AVAILABLE,
            "pop_evidence_score": 0.5,
            "pop_evidence_active_weight": 2.5,
            "pop_evidence_provenance": "MONTE_CARLO_POP",
            "pop_evidence_scoring_eligible": True,
            "trend_evidence_status": EVIDENCE_AVAILABLE,
            "trend_evidence_score": 0.75,
            "trend_evidence_active_weight": 1.0,
            "trend_evidence_provenance": "TREND_CLOSE_ROLLING_MEAN",
            "trend_evidence_scoring_eligible": True,
        }
    )

    assert snapshot["score_status"] == SCORE_COMPLETE
    assert snapshot["composite_score"] == pytest.approx(73.33333333333333)
    assert snapshot["pop_evidence_status"] == EVIDENCE_AVAILABLE
    assert snapshot["pop_evidence_score"] == pytest.approx(0.5)
    assert snapshot["rank_eligible"] is True


def test_partial_legacy_complete_diagnostics_fail_closed():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score": 73.33333333333333,
            "composite_score": 73.33333333333333,
            "score_status": SCORE_COMPLETE,
            "pop_evidence_status": EVIDENCE_AVAILABLE,
            "pop_evidence_score": 0.5,
            "rank_eligible": True,
        }
    )

    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["score_reason"] == LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE
    assert snapshot["composite_score"] is None
    assert snapshot["pop_evidence_status"] == EVIDENCE_NOT_AVAILABLE
    assert snapshot["rank_eligible"] is False


def test_status_only_complete_legacy_diagnostics_fail_closed():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score": 73.33333333333333,
            "composite_score": 73.33333333333333,
            "score_status": SCORE_COMPLETE,
            "active_evidence_profile": "phase,event,pnf,pop,trend",
            "active_weight_total": 7.5,
            "phase_evidence_status": EVIDENCE_AVAILABLE,
            "event_evidence_status": EVIDENCE_AVAILABLE,
            "pnf_evidence_status": EVIDENCE_AVAILABLE,
            "pop_evidence_status": EVIDENCE_AVAILABLE,
            "trend_evidence_status": EVIDENCE_AVAILABLE,
        }
    )

    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["composite_score"] is None
    assert snapshot["rank_eligible"] is False


def test_complete_status_without_legacy_numeric_score_still_requires_evidence_details():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score_status": SCORE_COMPLETE,
            "rank_eligible": True,
        }
    )

    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["score_reason"] == LEGACY_EVIDENCE_STATUS_NOT_AVAILABLE
    assert snapshot["rank_eligible"] is False


def test_non_complete_legacy_diagnostics_are_never_rank_eligible():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score_status": SCORE_INCOMPLETE,
            "rank_eligible": True,
            "composite_score": 73.33333333333333,
            "pop_evidence_status": EVIDENCE_DISABLED_BY_CONFIGURATION,
            "pop_evidence_score": 0.5,
            "pop_evidence_scoring_eligible": True,
        }
    )

    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["rank_eligible"] is False
    assert snapshot["composite_score"] is None
    assert snapshot["pop_evidence_score"] is None
    assert snapshot["pop_evidence_scoring_eligible"] is False


def test_complete_disabled_profile_diagnostics_are_preserved_as_uncalibrated():
    snapshot = normalize_candidate_snapshot(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": "AAA_1d_wyckoff_annotated.csv",
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score": 91.66666666666666,
            "composite_score": 91.66666666666666,
            "score_status": SCORE_COMPLETE,
            "active_evidence_profile": "phase,event,trend",
            "active_weight_total": 4.0,
            "rank_eligible": False,
            "score_profile_calibration": "SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED",
            "phase_evidence_status": EVIDENCE_AVAILABLE,
            "phase_evidence_score": 1.0,
            "phase_evidence_active_weight": 2.0,
            "phase_evidence_provenance": "WYCKOFF_PHASE",
            "phase_evidence_scoring_eligible": True,
            "event_evidence_status": EVIDENCE_AVAILABLE,
            "event_evidence_score": 1.0,
            "event_evidence_active_weight": 1.0,
            "event_evidence_provenance": "WYCKOFF_EVENT_RESOLUTION",
            "event_evidence_scoring_eligible": True,
            "trend_evidence_status": EVIDENCE_AVAILABLE,
            "trend_evidence_score": 0.75,
            "trend_evidence_active_weight": 1.0,
            "trend_evidence_provenance": "TREND_CLOSE_ROLLING_MEAN",
            "trend_evidence_scoring_eligible": True,
            "pnf_evidence_status": EVIDENCE_DISABLED_BY_CONFIGURATION,
            "pnf_evidence_scoring_eligible": False,
            "pop_evidence_status": EVIDENCE_DISABLED_BY_CONFIGURATION,
            "pop_evidence_scoring_eligible": False,
        }
    )

    assert snapshot["score_status"] == SCORE_COMPLETE
    assert snapshot["composite_score"] == pytest.approx(91.66666666666666)
    assert snapshot["score_profile_calibration"] == "SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED"
    assert snapshot["rank_eligible"] is False
    assert snapshot["pnf_evidence_status"] == EVIDENCE_DISABLED_BY_CONFIGURATION
    assert snapshot["pop_evidence_status"] == EVIDENCE_DISABLED_BY_CONFIGURATION


def test_legacy_unavailable_event_enrichment_stays_incomplete(tmp_path: Path):
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    pd.DataFrame(_rows(count=2)).drop(columns=["wyckoff_confirmed_event"]).to_csv(csv_path, index=False)

    result = build_candidate_snapshot_from_strategy_candidate(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": str(csv_path),
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score": 73.33333333333333,
            "signal_row_index": 1,
            "source_status": "EXACT_MATCH",
        },
        max_event_age_bars=5,
    )

    snapshot = result["snapshot"]
    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["event_status"] == "EVENT_NOT_AVAILABLE"
    assert snapshot["event_evidence_status"] == EVIDENCE_NOT_AVAILABLE
    assert snapshot["rank_eligible"] is False


def test_future_event_after_legacy_decision_row_does_not_create_complete_evidence(tmp_path: Path):
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    frame = pd.DataFrame(_rows(count=4))
    frame.loc[:2, "wyckoff_confirmed_event"] = pd.NA
    frame.loc[:2, "wyckoff_confirmed_event_occurrence"] = False
    frame.loc[3, "wyckoff_confirmed_event"] = "SOS"
    frame.loc[3, "wyckoff_confirmed_event_occurrence"] = True
    frame.to_csv(csv_path, index=False)

    result = build_candidate_snapshot_from_strategy_candidate(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": str(csv_path),
            "close": 100.0,
            "sl": 95.0,
            "tp": 112.0,
            "rr": 2.4,
            "score": 73.33333333333333,
            "signal_row_index": 2,
            "source_status": "EXACT_MATCH",
        },
        max_event_age_bars=5,
    )

    snapshot = result["snapshot"]
    assert snapshot["score_status"] == SCORE_INCOMPLETE
    assert snapshot["event_status"] == "EVENT_NOT_AVAILABLE"
    assert snapshot["event_occurrence_row_index"] is None
    assert snapshot["event_decision_row_index"] == 2
    assert snapshot["rank_eligible"] is False


def test_walk_forward_case_rebuilds_score_diagnostics_from_candidate_builder(tmp_path: Path):
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    pd.DataFrame(_rows()).to_csv(csv_path, index=False)
    row = pd.Series(
        {
            "timestamp": "2026-01-25",
            "open": 100,
            "high": 102,
            "low": 98,
            "close": 100,
            "tr_high": 112,
            "wyckoff_phase": "D",
            "wyckoff_confirmed_event": "SOS",
            "score_status": SCORE_INCOMPLETE,
            "missing_components": [COMPONENT_POP],
        }
    )

    case = build_walk_forward_candidate_from_row(
        row,
        csv_path=csv_path,
        signal_row_index=24,
        total_rows=30,
        profile_name="evidence",
        profile_context={},
        ticker="AAA",
        timeframe="1d",
        decision_frame=pd.DataFrame(_rows()),
    )

    assert case["score_status"] == SCORE_COMPLETE
    assert case["missing_components"] == []
    assert case["active_evidence_profile"] == "phase,event,trend"
    assert "score_status" in CASE_COLUMNS


def test_strategy_service_columns_expose_score_diagnostics():
    for column in (
        "score_status",
        "active_evidence_profile",
        "configured_weight_total",
        "active_weight_total",
        "available_weight_total",
        "evidence_coverage",
        "missing_components",
        "disabled_components",
        "invalid_components",
        "phase_evidence_status",
        "event_evidence_status",
        "pnf_evidence_status",
        "pop_evidence_status",
        "trend_evidence_status",
    ):
        assert column in STRATEGY_COLUMNS


def test_no_missing_evidence_placeholder_source_patterns():
    source = Path("marketflow/marketflow_strategy.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {
        node.name: ast.unparse(node)
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    ranker = functions["rank_long_candidates"]

    assert "pop if pop is not None else 0.5" not in ranker
    assert "_pnf_score_neutral()" not in ranker
    assert "EVIDENCE_DISABLED_BY_CONFIGURATION" in source
    assert "SCORE_INCOMPLETE" in source
