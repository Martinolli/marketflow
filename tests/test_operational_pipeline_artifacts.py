from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path

import pytest

from marketflow.marketflow_strategy import StrategyConfig, rank_long_candidates
from marketflow.operational_artifacts import (
    ArtifactContractError,
    SCENARIO_ORIGIN_MANUAL,
    STAGE_BATCH_ANALYSIS,
    STAGE_MONTE_CARLO,
    STAGE_STRATEGY_RANKING,
    WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
    WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
    assert_monte_carlo_geometry_matches_candidate,
    build_artifact_identity,
    build_workflow_a_manual_scenario_request,
    build_workflow_b_monte_carlo_request,
    run_specific_output_path,
    select_exact_artifact,
    stable_digest,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def _strategy_csv(path: Path, *, close: float = 100.0) -> Path:
    rows = ["timestamp,open,high,low,close,tr_low,tr_high,wyckoff_phase,wyckoff_confirmed_event,pnf_score"]
    for index in range(25):
        value = close + index
        rows.append(
            f"2026-01-{index + 1:02d},{value - 1},{value + 2},{value - 2},{value},"
            f"{value - 5},{value + 12},D,SOS,0.7"
        )
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def _candidate() -> dict:
    return {
        "candidate_build_success": True,
        "candidate_build_status": "valid",
        "ticker": "AAA",
        "tf": "4h",
        "timeframe": "4h",
        "entry": 101.25,
        "sl": 97.5,
        "stop_loss": 97.5,
        "tp": 112.0,
        "take_profit": 112.0,
        "source_csv": "batch_20260731_010203/AAA/AAA_4h_wyckoff_annotated.csv",
        "source_status": "EXACT_MATCH",
        "rank_eligible": True,
    }


def test_exact_artifact_parent_selection_and_rejections():
    artifact = build_artifact_identity(
        artifact_id="mc-1",
        run_id="run-1",
        stage=STAGE_MONTE_CARLO,
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile="SWING",
        timeframe="4h",
        source_dataset_identity="AAA_4h_wyckoff_annotated.csv",
        parent_artifact_id="strategy-1",
    )

    selected = select_exact_artifact(
        [{"artifact_identity": artifact}],
        artifact_id="mc-1",
        parent_artifact_id="strategy-1",
        ticker="AAA",
        timeframe="4h",
        run_id="run-1",
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        stage=STAGE_MONTE_CARLO,
    )

    assert selected["artifact_identity"]["artifact_id"] == "mc-1"
    with pytest.raises(ArtifactContractError, match="No exact artifact match"):
        select_exact_artifact([{"artifact_identity": artifact}], artifact_id="mc-1", ticker="BBB")
    with pytest.raises(ArtifactContractError, match="No exact artifact match"):
        select_exact_artifact([{"artifact_identity": artifact}], artifact_id="mc-1", timeframe="1d")
    with pytest.raises(ArtifactContractError, match="No exact artifact match"):
        select_exact_artifact([{"artifact_identity": artifact}], artifact_id="mc-1", run_id="run-2")
    with pytest.raises(ArtifactContractError, match="Ambiguous artifact match"):
        select_exact_artifact([{"artifact_identity": artifact}, {"artifact_identity": artifact}], artifact_id="mc-1")


def test_artifact_identity_rejects_unsafe_or_unknown_metadata(tmp_path: Path):
    required_kwargs = {
        "artifact_id": "artifact-1",
        "run_id": "run-1",
        "stage": STAGE_MONTE_CARLO,
        "workflow_type": WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        "ticker": "AAA",
        "analysis_profile": "SWING",
        "timeframe": "4h",
        "source_dataset_identity": "AAA_4h_wyckoff_annotated.csv",
    }
    for required_field in ("artifact_id", "run_id", "ticker", "timeframe", "source_dataset_identity"):
        missing_kwargs = dict(required_kwargs)
        missing_kwargs[required_field] = None
        with pytest.raises(ArtifactContractError, match=required_field):
            build_artifact_identity(**missing_kwargs)

    with pytest.raises(ArtifactContractError, match="Unsupported stage"):
        build_artifact_identity(
            artifact_id="bad-stage",
            run_id="run-1",
            stage="free_form_stage",
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            ticker="AAA",
            analysis_profile="SWING",
            timeframe="4h",
            source_dataset_identity="AAA_4h_wyckoff_annotated.csv",
        )
    with pytest.raises(ArtifactContractError, match="own parent"):
        build_artifact_identity(
            artifact_id="self",
            run_id="run-1",
            stage=STAGE_MONTE_CARLO,
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            ticker="AAA",
            analysis_profile="SWING",
            timeframe="4h",
            source_dataset_identity="AAA_4h_wyckoff_annotated.csv",
            parent_artifact_id="self",
        )
    with pytest.raises(ArtifactContractError, match="safe relative"):
        build_artifact_identity(
            artifact_id="unsafe-ref",
            run_id="run-1",
            stage=STAGE_MONTE_CARLO,
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            ticker="AAA",
            analysis_profile="SWING",
            timeframe="4h",
            source_dataset_identity="AAA_4h_wyckoff_annotated.csv",
            artifact_path="../escape.json",
        )
    with pytest.raises(ArtifactContractError, match="artifact_root"):
        build_artifact_identity(
            artifact_id="outside-root",
            run_id="run-1",
            stage=STAGE_MONTE_CARLO,
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            ticker="AAA",
            analysis_profile="SWING",
            timeframe="4h",
            source_dataset_identity="AAA_4h_wyckoff_annotated.csv",
            artifact_path=tmp_path.parent / "outside.json",
            artifact_root=tmp_path,
        )


def test_parent_cycle_fails_closed():
    first = build_artifact_identity(
        artifact_id="a",
        run_id="run-1",
        stage=STAGE_MONTE_CARLO,
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile="SWING",
        timeframe="4h",
        source_dataset_identity="AAA_4h_wyckoff_annotated.csv",
        parent_artifact_id="b",
    )
    second = build_artifact_identity(
        artifact_id="b",
        run_id="run-1",
        stage=STAGE_STRATEGY_RANKING,
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile="SWING",
        timeframe="4h",
        source_dataset_identity="AAA_4h_wyckoff_annotated.csv",
        parent_artifact_id="a",
    )

    with pytest.raises(ArtifactContractError, match="parent cycle"):
        select_exact_artifact(
            [{"artifact_identity": first}, {"artifact_identity": second}],
            artifact_id="a",
        )


def test_workflow_a_manual_scenario_labeling():
    parent = build_artifact_identity(
        artifact_id="analysis-1",
        run_id="run-a",
        stage=STAGE_BATCH_ANALYSIS,
        workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        ticker="AAA",
        analysis_profile="MANUAL",
        timeframe="4h",
        source_dataset_identity="AAA_4h_wyckoff_annotated.csv",
    )

    request = build_workflow_a_manual_scenario_request(
        parent_analysis_artifact={"artifact_identity": parent},
        scenario={"entry": 101.0, "stop_loss": 98.0, "take_profit": 112.0, "horizon_bars": 20},
        run_id="run-a",
    )

    assert request["workflow_type"] == WORKFLOW_MANUAL_SCENARIO_ANALYSIS
    assert request["scenario_origin"] == SCENARIO_ORIGIN_MANUAL
    assert request["candidate_source"] is None
    assert request["artifact_identity"]["parent_artifact_id"] == "analysis-1"


def test_workflow_b_canonical_candidate_labeling_and_geometry():
    candidate = _candidate()

    request = build_workflow_b_monte_carlo_request(
        candidate=candidate,
        strategy_artifact_id="strategy-1",
        run_id="run-b",
        horizon_bars=40,
    )

    assert request["workflow_type"] == WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT
    assert request["entry"] == candidate["entry"]
    assert request["sl"] == candidate["stop_loss"]
    assert request["tp"] == candidate["take_profit"]
    assert request["artifact_identity"]["stage"] == STAGE_MONTE_CARLO
    assert request["artifact_identity"]["parent_artifact_id"] == "strategy-1"
    assert request["artifact_identity"]["candidate_core_digest"] == stable_digest(
        {
            "candidate_build_status": "valid",
            "entry": 101.25,
            "source_csv": candidate["source_csv"],
            "source_status": "EXACT_MATCH",
            "stop_loss": 97.5,
            "take_profit": 112.0,
            "ticker": "AAA",
            "timeframe": "4h",
        }
    )
    assert_monte_carlo_geometry_matches_candidate(candidate, request)


def test_workflow_b_rejects_incomplete_candidate_and_geometry_mutation():
    candidate = _candidate()
    candidate["candidate_build_success"] = False

    with pytest.raises(ArtifactContractError, match="not actionable"):
        build_workflow_b_monte_carlo_request(
            candidate=candidate,
            strategy_artifact_id="strategy-1",
            run_id="run-b",
            horizon_bars=40,
        )

    candidate = _candidate()
    candidate["rank_eligible"] = False
    with pytest.raises(ArtifactContractError, match="not actionable"):
        build_workflow_b_monte_carlo_request(
            candidate=candidate,
            strategy_artifact_id="strategy-1",
            run_id="run-b",
            horizon_bars=40,
        )

    candidate = _candidate()
    request = build_workflow_b_monte_carlo_request(
        candidate=candidate,
        strategy_artifact_id="strategy-1",
        run_id="run-b",
        horizon_bars=40,
    )
    request["entry"] = 102.0
    with pytest.raises(ArtifactContractError, match="entry"):
        assert_monte_carlo_geometry_matches_candidate(candidate, request)

    request = build_workflow_b_monte_carlo_request(
        candidate=candidate,
        strategy_artifact_id="strategy-1",
        run_id="run-b",
        horizon_bars=40,
    )
    request["sl"] = 96.0
    with pytest.raises(ArtifactContractError, match="stop_loss"):
        assert_monte_carlo_geometry_matches_candidate(candidate, request)

    request = build_workflow_b_monte_carlo_request(
        candidate=candidate,
        strategy_artifact_id="strategy-1",
        run_id="run-b",
        horizon_bars=40,
    )
    request["tp"] = 120.0
    with pytest.raises(ArtifactContractError, match="take_profit"):
        assert_monte_carlo_geometry_matches_candidate(candidate, request)

    request = build_workflow_b_monte_carlo_request(
        candidate=candidate,
        strategy_artifact_id="strategy-1",
        run_id="run-b",
        horizon_bars=40,
    )
    request["ticker"] = "BBB"
    with pytest.raises(ArtifactContractError, match="ticker"):
        assert_monte_carlo_geometry_matches_candidate(candidate, request)

    request = build_workflow_b_monte_carlo_request(
        candidate=candidate,
        strategy_artifact_id="strategy-1",
        run_id="run-b",
        horizon_bars=40,
    )
    request["timeframe"] = "1d"
    with pytest.raises(ArtifactContractError, match="timeframe"):
        assert_monte_carlo_geometry_matches_candidate(candidate, request)

    request = build_workflow_b_monte_carlo_request(
        candidate=candidate,
        strategy_artifact_id="strategy-1",
        run_id="run-b",
        horizon_bars=40,
    )
    request["artifact_identity"]["candidate_core_digest"] = "wrong"
    with pytest.raises(ArtifactContractError, match="candidate_core_digest"):
        assert_monte_carlo_geometry_matches_candidate(candidate, request)


def test_strategy_mc_selection_has_no_latest_or_ambiguous_fallback(tmp_path: Path):
    report_root = tmp_path / "reports"
    ticker_dir = report_root / "batch_20260731_010203" / "AAA"
    ticker_dir.mkdir(parents=True)
    _strategy_csv(ticker_dir / "AAA_4h_wyckoff_annotated.csv")
    (ticker_dir / "older_4h_mc_summary.json").write_text(
        json.dumps(
            {
                "tf": "4h",
                "ticker": "AAA",
                "csv": "AAA_4h_wyckoff_annotated.csv",
                "workflow_type": WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
                "metrics_from_now": {"pop_tp_first": 0.6},
            }
        ),
        encoding="utf-8",
    )
    (ticker_dir / "newer_4h_mc_summary.json").write_text(
        json.dumps(
            {
                "tf": "4h",
                "ticker": "AAA",
                "csv": "AAA_4h_wyckoff_annotated.csv",
                "workflow_type": WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
                "metrics_from_now": {"pop_tp_first": 0.7},
            }
        ),
        encoding="utf-8",
    )

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260731_010203",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(use_mc=True, use_pnf=True),
    )

    assert len(results) == 1
    assert results[0]["pop"] is None
    assert results[0]["mc_matched_by"] == "ambiguous_timeframe"


def test_strategy_mc_selection_rejects_wrong_ticker_and_workflow_metadata(tmp_path: Path):
    report_root = tmp_path / "reports"
    ticker_dir = report_root / "batch_20260731_010203" / "AAA"
    ticker_dir.mkdir(parents=True)
    _strategy_csv(ticker_dir / "AAA_4h_wyckoff_annotated.csv")
    (ticker_dir / "wrong_ticker_4h_mc_summary.json").write_text(
        json.dumps({"tf": "4h", "ticker": "BBB", "metrics_from_now": {"pop_tp_first": 0.6}}),
        encoding="utf-8",
    )
    (ticker_dir / "manual_4h_mc_summary.json").write_text(
        json.dumps(
            {
                "tf": "4h",
                "ticker": "AAA",
                "workflow_type": WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
                "metrics_from_now": {"pop_tp_first": 0.7},
            }
        ),
        encoding="utf-8",
    )

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260731_010203",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(use_mc=True, use_pnf=True),
    )

    assert len(results) == 1
    assert results[0]["pop"] is None
    assert results[0]["mc_matched_by"] == "none"


def test_strategy_mc_selection_rejects_missing_identity_metadata(tmp_path: Path):
    report_root = tmp_path / "reports"
    ticker_dir = report_root / "batch_20260731_010203" / "AAA"
    ticker_dir.mkdir(parents=True)
    _strategy_csv(ticker_dir / "AAA_4h_wyckoff_annotated.csv")
    (ticker_dir / "identity_missing_4h_mc_summary.json").write_text(
        json.dumps({"tf": "4h", "metrics_from_now": {"pop_tp_first": 0.6}}),
        encoding="utf-8",
    )

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260731_010203",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(use_mc=True, use_pnf=True),
    )

    assert len(results) == 1
    assert results[0]["pop"] is None
    assert results[0]["mc_matched_by"] == "none"


def test_strategy_mc_selection_rejects_filename_only_timeframe(tmp_path: Path):
    report_root = tmp_path / "reports"
    ticker_dir = report_root / "batch_20260731_010203" / "AAA"
    ticker_dir.mkdir(parents=True)
    _strategy_csv(ticker_dir / "AAA_4h_wyckoff_annotated.csv")
    (ticker_dir / "filename_only_4h_mc_summary.json").write_text(
        json.dumps(
            {
                "ticker": "AAA",
                "csv": "AAA_4h_wyckoff_annotated.csv",
                "workflow_type": WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
                "metrics_from_now": {"pop_tp_first": 0.6},
            }
        ),
        encoding="utf-8",
    )

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260731_010203",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(use_mc=True, use_pnf=True),
    )

    assert len(results) == 1
    assert results[0]["pop"] is None
    assert results[0]["mc_matched_by"] == "none"


def test_strategy_wrong_batch_run_is_not_selected_by_recursive_fallback(tmp_path: Path):
    report_root = tmp_path / "reports"
    ticker_dir = report_root / "batch_20260731_010203" / "AAA"
    ticker_dir.mkdir(parents=True)
    _strategy_csv(ticker_dir / "AAA_4h_wyckoff_annotated.csv")

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260731_999999",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(),
    )

    assert results == []


def test_strategy_ambiguous_ticker_directories_fail_closed(tmp_path: Path):
    report_root = tmp_path / "reports"
    for batch_name in ("batch_20260731_010203", "batch_20260731_010204"):
        ticker_dir = report_root / batch_name / "AAA"
        ticker_dir.mkdir(parents=True)
        _strategy_csv(ticker_dir / "AAA_4h_wyckoff_annotated.csv")

    results = rank_long_candidates(
        report_root=str(report_root),
        date_glob="batch_20260731_*",
        tickers=["AAA"],
        tf="4h",
        cfg=StrategyConfig(),
    )

    assert results == []


def test_plot_consumes_explicit_mc_identity_without_scanning(tmp_path: Path):
    script = REPO_ROOT / "scripts" / "plot_annotated_features.py"
    spec = importlib.util.spec_from_file_location("plot_annotated_features_for_test", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    csv_path = tmp_path / "AAA_4h_wyckoff_annotated.csv"
    csv_path.write_text("timestamp,open,high,low,close\n2026-01-01,1,2,1,1.5\n", encoding="utf-8")
    mc_path = tmp_path / "20260731_010203_mc_summary.json"
    mc_path.write_text(
        json.dumps({"csv": "AAA_4h_wyckoff_annotated.csv", "metrics_from_now": {"pop_tp_first": 0.55}}),
        encoding="utf-8",
    )

    data = module._load_explicit_mc_for(str(csv_path), str(mc_path))

    assert data["csv"] == "AAA_4h_wyckoff_annotated.csv"
    with pytest.raises(ValueError, match="does not match"):
        module._load_explicit_mc_for(str(tmp_path / "BBB_4h_wyckoff_annotated.csv"), str(mc_path))
    directory_named_like_summary = tmp_path / "directory_mc_summary.json"
    directory_named_like_summary.mkdir()
    with pytest.raises(ValueError, match="regular file"):
        module._load_explicit_mc_for(str(csv_path), str(directory_named_like_summary))
    other_run = tmp_path / "other_run"
    other_run.mkdir()
    other_mc_path = other_run / "20260731_010204_mc_summary.json"
    other_mc_path.write_text(
        json.dumps({"csv": "AAA_4h_wyckoff_annotated.csv", "metrics_from_now": {"pop_tp_first": 0.55}}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="same report directory"):
        module._load_explicit_mc_for(str(csv_path), str(other_mc_path))


def test_candidate_digest_is_deterministic_and_excludes_future_outcome():
    candidate = _candidate()
    request = build_workflow_b_monte_carlo_request(
        candidate=candidate,
        strategy_artifact_id="strategy-1",
        run_id="run-b",
        horizon_bars=40,
        strategy_config_digest=stable_digest({"min_rr": 1.5, "max_sl_atr": 2.0}),
    )
    candidate_with_future = dict(candidate)
    candidate_with_future["actual_outcome"] = "tp_first"
    second = build_workflow_b_monte_carlo_request(
        candidate=candidate_with_future,
        strategy_artifact_id="strategy-1",
        run_id="run-b",
        horizon_bars=40,
        strategy_config_digest=stable_digest({"min_rr": 1.5, "max_sl_atr": 2.0}),
    )

    assert request["artifact_identity"]["candidate_core_digest"] == second["artifact_identity"]["candidate_core_digest"]
    assert request["artifact_identity"]["strategy_config_digest"] == second["artifact_identity"]["strategy_config_digest"]


def test_report_collision_prevention_and_run_specific_outputs(tmp_path: Path):
    output = run_specific_output_path(tmp_path, "run-1_mc_summary.json")
    assert output == tmp_path / "run-1_mc_summary.json"
    output.write_text("{}", encoding="utf-8")

    with pytest.raises(ArtifactContractError, match="already exists"):
        run_specific_output_path(tmp_path, "run-1_mc_summary.json")
    with pytest.raises(ArtifactContractError, match="safe relative"):
        run_specific_output_path(tmp_path, "../other.json")


def test_operational_source_assurance_boundaries():
    strategy_source = (REPO_ROOT / "marketflow" / "marketflow_strategy.py").read_text(encoding="utf-8")
    plot_source = (REPO_ROOT / "scripts" / "plot_annotated_features.py").read_text(encoding="utf-8")
    contract_source = (REPO_ROOT / "marketflow" / "operational_artifacts.py").read_text(encoding="utf-8")
    contract_functions = {
        node.name: ast.unparse(node)
        for node in ast.parse(contract_source).body
        if isinstance(node, ast.FunctionDef)
    }

    assert "fallback_latest" not in strategy_source
    assert "os.path.getmtime" not in strategy_source
    assert "_load_latest_mc_for" not in plot_source
    assert "os.path.getmtime" not in plot_source
    assert "build_workflow_b_monte_carlo_request" in contract_source
    assert "candidate.get('entry')" in contract_functions["candidate_core"]
    assert "candidate.get('stop_loss')" in contract_functions["candidate_core"]
    assert "candidate.get('take_profit')" in contract_functions["candidate_core"]
    assert WORKFLOW_MANUAL_SCENARIO_ANALYSIS in contract_source
    assert WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT in contract_source


def test_core_modules_do_not_import_streamlit_or_llm_into_strategy_contracts():
    checked = [
        REPO_ROOT / "marketflow" / "marketflow_strategy.py",
        REPO_ROOT / "marketflow" / "marketflow_monte_carlo_trade.py",
        REPO_ROOT / "marketflow" / "operational_artifacts.py",
    ]
    forbidden_imports = {"streamlit", "openai", "marketflow.marketflow_llm_interface"}

    for path in checked:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imports.update(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        assert forbidden_imports.isdisjoint(imports)
