from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from marketflow.marketflow_strategy import (
    CandidateBuildRequest,
    CandidateEvidenceInputs,
    SOURCE_STATUS_EXACT_MATCH,
    StrategyConfig,
    StrategyDatasetIdentity,
    build_candidate_from_prefix,
    rank_long_candidates,
)
from marketflow.services.backtest_candidate_service import build_candidate_snapshot_from_strategy_candidate
from marketflow.services.walk_forward_validation_service import build_walk_forward_candidate_from_row


CORE_FIELDS = (
    "ticker",
    "timeframe",
    "source_status",
    "signal_row_index",
    "signal_timestamp",
    "entry",
    "stop_loss",
    "take_profit",
    "risk_reward",
    "target_status",
    "target_provenance",
    "target_structural_level_kind",
    "rr_status",
    "volatility_status",
    "volatility_provenance",
    "volatility_window",
    "volatility_value",
    "strategy_score",
    "composite_score",
    "score_status",
    "active_evidence_profile",
    "missing_components",
    "disabled_components",
    "invalid_components",
    "rank_eligible",
    "wyckoff_phase",
    "wyckoff_event",
    "event_status",
    "event_provenance",
    "event_age_bars",
    "event_occurrence_row_index",
    "event_decision_row_index",
    "trend",
    "phase_evidence_status",
    "phase_evidence_score",
    "event_evidence_status",
    "event_evidence_score",
    "pnf_evidence_status",
    "pnf_evidence_score",
    "pop_evidence_status",
    "pop_evidence_score",
    "trend_evidence_status",
    "trend_evidence_score",
)


def _frame(count: int = 25) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for index in range(count):
        close = 100.0 + index * 0.25
        rows.append(
            {
                "timestamp": (pd.Timestamp("2026-01-01") + pd.Timedelta(days=index)).isoformat(),
                "open": close - 0.1,
                "high": close + 1.0,
                "low": close - 1.0,
                "close": close,
                "tr_low": close - 4.0,
                "tr_high": close + 6.0,
                "wyckoff_phase": "D",
                "wyckoff_confirmed_event": "SOS" if index == count - 1 else pd.NA,
                "wyckoff_confirmed_event_occurrence": index == count - 1,
                "pnf_score": 0.8,
            }
        )
    return pd.DataFrame(rows)


def _write_strategy_report(tmp_path: Path, frame: pd.DataFrame) -> Path:
    ticker_dir = tmp_path / "batch_20260730_010203" / "AAA"
    ticker_dir.mkdir(parents=True)
    csv_path = ticker_dir / "AAA_1d_wyckoff_annotated.csv"
    frame.to_csv(csv_path, index=False)
    mc_path = ticker_dir / "AAA_1d_wyckoff_annotated_1d_mc_summary.json"
    mc_path.write_text(
        json.dumps({"tf": "1d", "metrics_from_now": {"pop_tp_first": 0.7}}),
        encoding="utf-8",
    )
    return csv_path


def _projection(candidate: dict[str, Any]) -> dict[str, Any]:
    projection = {field: candidate.get(field) for field in CORE_FIELDS}
    source_csv_name = candidate.get("source_csv_name")
    if source_csv_name is None and candidate.get("source_csv") is not None:
        source_csv_name = Path(str(candidate.get("source_csv"))).name
    projection["source_csv_name"] = source_csv_name
    return projection


def test_current_backtest_walk_forward_share_candidate_core(tmp_path: Path):
    frame = _frame()
    csv_path = _write_strategy_report(tmp_path, frame)
    cfg = StrategyConfig(use_mc=True, use_pnf=True, max_event_age_bars=3)
    evidence = CandidateEvidenceInputs(pop=0.7)
    identity = StrategyDatasetIdentity(
        ticker="AAA",
        timeframe="1d",
        source=csv_path,
        source_kind="canonical",
        status=SOURCE_STATUS_EXACT_MATCH,
    )

    direct = build_candidate_from_prefix(
        CandidateBuildRequest(
            source_identity=identity,
            data_prefix=frame,
            config=cfg,
            evidence=evidence,
            report_root=tmp_path,
            source_status=SOURCE_STATUS_EXACT_MATCH,
            candidate_source="direct_test",
        )
    )
    current = rank_long_candidates(
        report_root=str(tmp_path),
        date_glob="batch_20260730_010203",
        tickers=["AAA"],
        tf="1d",
        cfg=cfg,
    )[0]
    backtest_input = dict(current)
    backtest_input.pop("source_report_dir", None)
    backtest_input.update(
        {
            "csv": str(csv_path),
            "source_csv": str(csv_path),
        }
    )
    backtest = build_candidate_snapshot_from_strategy_candidate(
        backtest_input,
        strategy_config=cfg,
        evidence_inputs=evidence,
    )["snapshot"]
    walk_forward = build_walk_forward_candidate_from_row(
        frame.iloc[-1],
        csv_path=csv_path,
        signal_row_index=len(frame) - 1,
        total_rows=len(frame),
        profile_name="alignment",
        profile_context={"success": True, "horizon_bars": 1},
        ticker="AAA",
        timeframe="1d",
        timestamp_column="timestamp",
        decision_frame=frame,
        strategy_config=cfg,
        evidence_inputs=evidence,
    )

    expected = _projection(direct)
    assert _projection(current) == expected
    assert _projection(backtest) == expected
    assert _projection(walk_forward) == expected


def test_walk_forward_candidate_core_uses_decision_prefix_not_future_rows(tmp_path: Path):
    frame = _frame()
    csv_path = _write_strategy_report(tmp_path, frame)
    cfg = StrategyConfig(use_mc=True, use_pnf=True, max_event_age_bars=3)
    evidence = CandidateEvidenceInputs(pop=0.7)
    prefix = frame.iloc[:20].copy()
    prefix.loc[prefix.index[-1], "wyckoff_confirmed_event"] = "SOS"
    prefix.loc[prefix.index[-1], "wyckoff_confirmed_event_occurrence"] = True
    extended = pd.concat([prefix, frame.iloc[20:].copy()], ignore_index=True)
    extended.loc[20:, "close"] = 1000.0
    extended.loc[20:, "tr_high"] = 2000.0
    extended.loc[20:, "pnf_score"] = 0.1

    first = build_walk_forward_candidate_from_row(
        prefix.iloc[-1],
        csv_path=csv_path,
        signal_row_index=len(prefix) - 1,
        total_rows=len(extended),
        profile_name="alignment",
        profile_context={"success": True, "horizon_bars": 1},
        ticker="AAA",
        timeframe="1d",
        timestamp_column="timestamp",
        decision_frame=prefix,
        strategy_config=cfg,
        evidence_inputs=evidence,
    )
    with_future = build_walk_forward_candidate_from_row(
        extended.iloc[len(prefix) - 1],
        csv_path=csv_path,
        signal_row_index=len(prefix) - 1,
        total_rows=len(extended),
        profile_name="alignment",
        profile_context={"success": True, "horizon_bars": 1},
        ticker="AAA",
        timeframe="1d",
        timestamp_column="timestamp",
        decision_frame=extended,
        strategy_config=cfg,
        evidence_inputs=evidence,
    )

    assert _projection(with_future) == _projection(first)


@pytest.mark.parametrize("signal_row_index", [None, True, -1, 1.5, "1", 25])
def test_walk_forward_candidate_rejects_invalid_signal_row_index(tmp_path: Path, signal_row_index: Any):
    frame = _frame()
    csv_path = _write_strategy_report(tmp_path, frame)

    case = build_walk_forward_candidate_from_row(
        frame.iloc[-1],
        csv_path=csv_path,
        signal_row_index=signal_row_index,
        total_rows=len(frame),
        profile_name="alignment",
        profile_context={"success": True, "horizon_bars": 1},
        ticker="AAA",
        timeframe="1d",
        timestamp_column="timestamp",
        decision_frame=frame,
        strategy_config=StrategyConfig(use_mc=True, use_pnf=True, max_event_age_bars=3),
        evidence_inputs=CandidateEvidenceInputs(pop=0.7),
    )

    assert case["snapshot_success"] is False
    assert case["candidate_validation_errors"] == ["INVALID_SIGNAL_ROW_INDEX"]
    assert case["entry"] is None
    assert case["take_profit"] is None


def test_walk_forward_candidate_rejects_signal_timestamp_mismatch(tmp_path: Path):
    frame = _frame()
    csv_path = _write_strategy_report(tmp_path, frame)
    row = frame.iloc[-1].copy()
    row["timestamp"] = "2026-02-01"

    case = build_walk_forward_candidate_from_row(
        row,
        csv_path=csv_path,
        signal_row_index=len(frame) - 1,
        total_rows=len(frame),
        profile_name="alignment",
        profile_context={"success": True, "horizon_bars": 1},
        ticker="AAA",
        timeframe="1d",
        timestamp_column="timestamp",
        decision_frame=frame,
        strategy_config=StrategyConfig(use_mc=True, use_pnf=True, max_event_age_bars=3),
        evidence_inputs=CandidateEvidenceInputs(pop=0.7),
    )

    assert case["snapshot_success"] is False
    assert case["candidate_validation_errors"] == ["SIGNAL_TIMESTAMP_MISMATCH"]


def test_walk_forward_candidate_normalizes_ohlc_aliases_before_canonical_build(tmp_path: Path):
    frame = _frame().rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "wyckoff_phase": "phase",
        }
    )
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    frame.to_csv(csv_path, index=False)

    case = build_walk_forward_candidate_from_row(
        frame.iloc[-1],
        csv_path=csv_path,
        signal_row_index=len(frame) - 1,
        total_rows=len(frame),
        profile_name="alignment",
        profile_context={"success": True, "horizon_bars": 1},
        ticker="AAA",
        timeframe="1d",
        timestamp_column="timestamp",
        ohlc_columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"},
        phase_column="phase",
        event_column="wyckoff_confirmed_event",
        decision_frame=frame,
        strategy_config=StrategyConfig(use_mc=True, use_pnf=True, max_event_age_bars=3),
        evidence_inputs=CandidateEvidenceInputs(pop=0.7),
    )

    assert case["snapshot_success"] is True
    assert case["entry"] == frame["Close"].iloc[-1]
    assert case["target_status"] == "TARGET_RESOLVED"
    assert case["score_status"] == "SCORE_COMPLETE"


def test_walk_forward_candidate_rejects_conflicting_alias_values(tmp_path: Path):
    frame = _frame()
    frame["Close"] = frame["close"] + 10.0
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    frame.to_csv(csv_path, index=False)

    case = build_walk_forward_candidate_from_row(
        frame.iloc[-1],
        csv_path=csv_path,
        signal_row_index=len(frame) - 1,
        total_rows=len(frame),
        profile_name="alignment",
        profile_context={"success": True, "horizon_bars": 1},
        ticker="AAA",
        timeframe="1d",
        timestamp_column="timestamp",
        ohlc_columns={"open": "open", "high": "high", "low": "low", "close": "Close"},
        event_column="wyckoff_confirmed_event",
        decision_frame=frame,
        strategy_config=StrategyConfig(use_mc=True, use_pnf=True, max_event_age_bars=3),
        evidence_inputs=CandidateEvidenceInputs(pop=0.7),
    )

    assert case["snapshot_success"] is False
    assert case["candidate_validation_errors"] == ["ALIAS_CONFLICT"]


def test_canonical_rejection_is_non_actionable_across_wrappers(tmp_path: Path):
    frame = _frame()
    csv_path = _write_strategy_report(tmp_path, frame)
    cfg = StrategyConfig(use_mc=True, use_pnf=True, max_event_age_bars=3, min_pop=0.8, min_pop_backup=0.8)
    evidence = CandidateEvidenceInputs(pop=0.1)
    identity = StrategyDatasetIdentity(
        ticker="AAA",
        timeframe="1d",
        source=csv_path,
        source_kind="canonical",
        status=SOURCE_STATUS_EXACT_MATCH,
    )

    direct = build_candidate_from_prefix(
        CandidateBuildRequest(
            source_identity=identity,
            data_prefix=frame,
            config=cfg,
            evidence=evidence,
            report_root=tmp_path,
            source_status=SOURCE_STATUS_EXACT_MATCH,
            candidate_source="direct_test",
        )
    )
    current = rank_long_candidates(
        report_root=str(tmp_path),
        date_glob="batch_20260730_010203",
        tickers=["AAA"],
        tf="1d",
        cfg=cfg,
    )
    backtest = build_candidate_snapshot_from_strategy_candidate(
        {
            "ticker": "AAA",
            "timeframe": "1d",
            "csv": str(csv_path),
            "source_csv": str(csv_path),
            "signal_row_index": len(frame) - 1,
            "source_status": SOURCE_STATUS_EXACT_MATCH,
            "entry": frame["close"].iloc[-1],
            "stop_loss": frame["tr_low"].iloc[-1],
            "take_profit": frame["tr_high"].iloc[-1],
            "risk_reward": 2.0,
        },
        strategy_config=cfg,
        evidence_inputs=evidence,
    )
    walk_forward = build_walk_forward_candidate_from_row(
        frame.iloc[-1],
        csv_path=csv_path,
        signal_row_index=len(frame) - 1,
        total_rows=len(frame),
        profile_name="alignment",
        profile_context={"success": True, "horizon_bars": 1},
        ticker="AAA",
        timeframe="1d",
        timestamp_column="timestamp",
        decision_frame=frame,
        strategy_config=cfg,
        evidence_inputs=evidence,
    )

    assert direct["candidate_build_success"] is False
    assert direct["candidate_build_reason"] == "POP_BELOW_MINIMUM"
    assert direct["rank_eligible"] is False
    assert current == []
    assert backtest["success"] is False
    assert backtest["snapshot"]["rank_eligible"] is False
    assert backtest["snapshot"]["target_status"] == "POP_BELOW_MINIMUM"
    assert walk_forward["snapshot_success"] is False
    assert walk_forward["candidate_validation_errors"] == ["POP_BELOW_MINIMUM"]
    assert walk_forward["rank_eligible"] is False


def test_canonical_malformed_prefix_without_close_fails_closed(tmp_path: Path):
    frame = _frame().drop(columns=["close"])
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    frame.to_csv(csv_path, index=False)
    identity = StrategyDatasetIdentity(
        ticker="AAA",
        timeframe="1d",
        source=csv_path,
        source_kind="canonical",
        status=SOURCE_STATUS_EXACT_MATCH,
    )

    candidate = build_candidate_from_prefix(
        CandidateBuildRequest(
            source_identity=identity,
            data_prefix=frame,
            config=StrategyConfig(use_mc=True, use_pnf=True, max_event_age_bars=3),
            evidence=CandidateEvidenceInputs(pop=0.7),
            source_status=SOURCE_STATUS_EXACT_MATCH,
            candidate_source="direct_test",
        )
    )

    assert candidate["candidate_build_success"] is False
    assert candidate["candidate_build_status"] == "invalid"
    assert candidate["rank_eligible"] is False
    assert candidate["entry"] is None


def test_backtest_exact_source_invalid_prefix_fails_closed(tmp_path: Path):
    csv_path = tmp_path / "AAA_1d_wyckoff_annotated.csv"
    pd.DataFrame(
        [
            {
                "timestamp": "2026-01-01",
                "open": 100,
                "high": 101,
                "low": 99,
                "close": 100,
                "wyckoff_phase": "D",
                "wyckoff_confirmed_event": "SOS",
            }
        ]
    ).to_csv(csv_path, index=False)

    result = build_candidate_snapshot_from_strategy_candidate(
        {
            "ticker": "AAA",
            "tf": "1d",
            "csv": str(csv_path),
            "close": 100,
            "sl": 95,
            "tp": 110,
            "rr": 2.0,
            "signal_row_index": 0,
            "source_status": SOURCE_STATUS_EXACT_MATCH,
        }
    )

    assert result["success"] is False
    assert result["snapshot"]["take_profit"] is None
    assert result["snapshot"]["target_status"] == "TARGET_NOT_AVAILABLE"


def test_wrappers_delegate_candidate_core_to_canonical_builder():
    strategy_source = Path("marketflow/marketflow_strategy.py").read_text(encoding="utf-8")
    walk_forward_source = Path("marketflow/services/walk_forward_validation_service.py").read_text(encoding="utf-8")
    backtest_source = Path("marketflow/services/backtest_candidate_service.py").read_text(encoding="utf-8")

    strategy_functions = {
        node.name: ast.unparse(node)
        for node in ast.parse(strategy_source).body
        if isinstance(node, ast.FunctionDef)
    }
    walk_forward_functions = {
        node.name: ast.unparse(node)
        for node in ast.parse(walk_forward_source).body
        if isinstance(node, ast.FunctionDef)
    }
    backtest_functions = {
        node.name: ast.unparse(node)
        for node in ast.parse(backtest_source).body
        if isinstance(node, ast.FunctionDef)
    }

    assert "build_candidate_from_prefix" in strategy_functions["rank_long_candidates"]
    assert "build_candidate_from_prefix" in walk_forward_functions["build_walk_forward_candidate_from_row"]
    assert "build_candidate_from_prefix" in backtest_functions["_canonical_snapshot_from_source_prefix"]
    assert "strategy_config" in walk_forward_functions["build_walk_forward_cases_from_csv"]
    assert "effective_strategy_config" in walk_forward_functions["build_walk_forward_cases_from_csv"]
    assert "_resolve_long_target" not in walk_forward_functions["build_walk_forward_candidate_from_row"]
    assert "_rr(" not in walk_forward_functions["build_walk_forward_candidate_from_row"]
