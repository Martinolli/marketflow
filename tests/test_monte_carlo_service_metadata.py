from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from marketflow.services.monte_carlo_service import (
    build_monte_carlo_join_metadata,
    enrich_latest_monte_carlo_summary_json,
    run_monte_carlo_for_csv,
)


def test_build_metadata_from_candidate_snapshot():
    snapshot = {
        "ticker": "AAPL",
        "timeframe": "1d",
        "source_csv": r"C:\reports\AAPL_1d_wyckoff_annotated.csv",
        "source_report_dir": r"C:\reports",
        "signal_row_index": 123,
        "signal_timestamp": "2026-05-28",
        "entry": 310.85,
        "stop_loss": 300.69,
        "take_profit": 326.08,
        "risk_reward": 1.5,
        "strategy_score": 60,
        "wyckoff_phase": "D",
        "wyckoff_event": "UT_WEAK",
        "trend": "up",
        "candidate_source": "strategy_ranking",
        "source_strategy_rank": 1,
        "validation_status": "valid",
        "snapshot_success": True,
    }

    metadata = build_monte_carlo_join_metadata(
        csv_path=snapshot["source_csv"],
        candidate_snapshot=snapshot,
        candidate_snapshot_file="AAPL_1d_backtest_candidates_20260528.csv",
    )

    assert metadata["metadata_version"] == "mc_join_metadata_v1"
    assert metadata["ticker"] == "AAPL"
    assert metadata["timeframe"] == "1d"
    assert metadata["source_csv"] == "AAPL_1d_wyckoff_annotated.csv"
    assert metadata["signal_row_index"] == 123
    assert metadata["signal_timestamp"] == "2026-05-28"
    assert metadata["candidate_validation_status"] == "valid"
    assert metadata["candidate_snapshot_success"] is True
    assert metadata["join_key_preferred"] == "AAPL|1d|AAPL_1d_backtest_candidates_20260528.csv"
    assert metadata["join_key_secondary"] == "AAPL|1d|AAPL_1d_wyckoff_annotated.csv|123"


def test_build_metadata_from_trade_plan_fallback():
    trade_plan = {
        "ticker": "AI",
        "csv": "AI_1d_wyckoff_annotated.csv",
        "tf": "1d",
        "entry": 9.1,
        "stop_loss": 8.6,
        "take_profit": 10.0,
        "source": "strategy_ranking",
    }

    metadata = build_monte_carlo_join_metadata(trade_plan=trade_plan)

    assert metadata["ticker"] == "AI"
    assert metadata["timeframe"] == "1d"
    assert metadata["source_csv"] == "AI_1d_wyckoff_annotated.csv"
    assert metadata["entry"] == 9.1
    assert metadata["stop_loss"] == 8.6
    assert metadata["take_profit"] == 10.0
    assert metadata["signal_row_index"] is None
    assert metadata["join_key_preferred"] is None


def test_infer_ticker_and_timeframe_from_csv_path():
    metadata = build_monte_carlo_join_metadata(
        csv_path=Path("AAPL_1d_wyckoff_annotated.csv"),
    )

    assert metadata["ticker"] == "AAPL"
    assert metadata["timeframe"] == "1d"
    assert metadata["source_csv"] == "AAPL_1d_wyckoff_annotated.csv"


def test_build_metadata_does_not_mutate_inputs():
    trade_plan = {"ticker": "AAPL", "csv": "AAPL_1d_wyckoff_annotated.csv", "tf": "1d"}
    snapshot = {"ticker": "AAPL", "source_csv": "AAPL_1d_wyckoff_annotated.csv"}
    original_trade_plan = deepcopy(trade_plan)
    original_snapshot = deepcopy(snapshot)

    build_monte_carlo_join_metadata(trade_plan=trade_plan, candidate_snapshot=snapshot)

    assert trade_plan == original_trade_plan
    assert snapshot == original_snapshot


def test_enrich_existing_mc_summary_json(tmp_path):
    csv_path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    csv_path.write_text("timestamp,open,high,low,close\n2026-01-01,1,1,1,1\n", encoding="utf-8")
    summary_path = tmp_path / "20260528_120000_mc_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "params": {"model": "bootstrap"},
                "metrics_from_now": {"pop_tp_first": 0.5},
            }
        ),
        encoding="utf-8",
    )
    metadata = build_monte_carlo_join_metadata(
        csv_path=csv_path,
        timeframe="1d",
        candidate_snapshot={"ticker": "AAPL", "source_csv": str(csv_path), "signal_row_index": 4},
        candidate_snapshot_file="AAPL_1d_backtest_candidates.csv",
    )

    result = enrich_latest_monte_carlo_summary_json(csv_path, metadata)

    assert result["success"] is True
    enriched = json.loads(summary_path.read_text(encoding="utf-8"))
    assert enriched["params"] == {"model": "bootstrap"}
    assert enriched["metrics_from_now"] == {"pop_tp_first": 0.5}
    assert enriched["join_metadata"]["metadata_version"] == "mc_join_metadata_v1"
    assert enriched["join_metadata"]["signal_row_index"] == 4
    assert enriched["candidate_snapshot_file"] == "AAPL_1d_backtest_candidates.csv"


def test_enrich_no_summary_json_returns_warning(tmp_path):
    csv_path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    csv_path.write_text("timestamp,open,high,low,close\n2026-01-01,1,1,1,1\n", encoding="utf-8")

    result = enrich_latest_monte_carlo_summary_json(csv_path, {"ticker": "AAPL"})

    assert result["success"] is False
    assert result["warnings"]
    assert result["errors"] == []


def test_run_service_return_includes_join_metadata_and_enrichment(tmp_path, monkeypatch):
    csv_path = tmp_path / "AAPL_1d_wyckoff_annotated.csv"
    csv_path.write_text("timestamp,open,high,low,close\n2026-01-01,1,1,1,1\n", encoding="utf-8")

    class FakeSimulator:
        def __init__(self, model_type: str):
            self.model_type = model_type

        def simulate_trade_for_csv(self, **kwargs):
            summary_path = Path(kwargs["csv_path"]).parent / "20260528_120000_mc_summary.json"
            payload = {
                "csv": Path(kwargs["csv_path"]).name,
                "tf": kwargs["tf"],
                "params": {
                    "tp": kwargs["tp"],
                    "sl": kwargs["sl"],
                    "entry": kwargs["entry"],
                    "horizon_bars": kwargs["horizon_bars"],
                    "model": kwargs["model"],
                },
                "metrics_from_now": {"pop_tp_first": 0.5},
                "actual_outcome": {"outcome": "neither", "bars_to_hit": None},
                "calibration": {"model_used": kwargs["model"]},
            }
            summary_path.write_text(json.dumps(payload), encoding="utf-8")
            return payload

    monkeypatch.setattr(
        "marketflow.services.monte_carlo_service._load_simulator_class",
        lambda model: FakeSimulator,
    )

    result = run_monte_carlo_for_csv(
        str(csv_path),
        entry=100,
        stop_loss=95,
        take_profit=110,
        timeframe="1d",
        model="bootstrap",
        paths=1000,
        horizon=20,
        trade_plan={"ticker": "AAPL", "csv": str(csv_path), "tf": "1d"},
        candidate_snapshot={"ticker": "AAPL", "source_csv": str(csv_path), "signal_row_index": 9},
        candidate_snapshot_file="AAPL_1d_backtest_candidates.csv",
        save_plots=False,
    )

    assert result["success"] is True
    assert result["join_metadata"]["metadata_version"] == "mc_join_metadata_v1"
    assert result["join_metadata"]["signal_row_index"] == 9
    assert result["summary_enrichment"]["success"] is True
    assert result["candidate_snapshot_file"] == "AAPL_1d_backtest_candidates.csv"
    summary_path = tmp_path / "20260528_120000_mc_summary.json"
    enriched = json.loads(summary_path.read_text(encoding="utf-8"))
    assert enriched["join_metadata"]["join_key_secondary"] == "AAPL|1d|AAPL_1d_wyckoff_annotated.csv|9"
