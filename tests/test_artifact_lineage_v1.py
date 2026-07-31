from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import pandas as pd
import pytest

from marketflow.operational_artifacts import (
    ARTIFACT_TYPE_ANNOTATED_PLOT,
    ARTIFACT_TYPE_ANNOTATED_DATASET,
    ARTIFACT_TYPE_MONTE_CARLO_SUMMARY,
    ArtifactContractError,
    PAYLOAD_TYPE_JSON,
    PROFILE_MANUAL_SCENARIO,
    PROFILE_SWING,
    STAGE_BATCH_ANALYSIS_V1,
    STAGE_PLOT_V1,
    STAGE_STRATEGY_CANDIDATE_V1,
    WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
    WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
    annotated_dataset_artifact,
    build_artifact_manifest,
    commit_artifact_payload,
    commit_candidate_core_artifact,
    commit_manual_scenario_artifact,
    commit_monte_carlo_summary_artifact,
    commit_plot_artifact,
    create_run_context,
    candidate_core,
    load_manifest,
    manual_scenario_contract,
    sha256_bytes,
    stable_digest,
    validate_manifest,
)


def _csv(path: Path) -> Path:
    path.write_text(
        "timestamp,open,high,low,close,volume,tr_low,tr_high,wyckoff_phase,wyckoff_confirmed_event,wyckoff_confirmed_event_occurrence\n"
        "2026-01-01,100,102,98,100,1000,95,112,D,SOS,True\n",
        encoding="utf-8",
    )
    return path


def _cli_csv(path: Path) -> Path:
    rows = []
    start = pd.Timestamp("2026-01-01")
    for index in range(60):
        rows.append(
            {
                "timestamp": (start + pd.Timedelta(days=index)).date().isoformat(),
                "open": 100 + index,
                "high": 102 + index,
                "low": 98 + index,
                "close": 100 + index,
                "volume": 1000 + index,
                "tr_low": 95 + index,
                "tr_high": 112 + index,
                "wyckoff_phase": "D",
                "wyckoff_confirmed_event": "SOS" if index == 59 else "",
                "wyckoff_confirmed_event_occurrence": index == 59,
                "pnf_score": 0.8,
            }
        )
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def _candidate(source_name: str = "AAA_4h.csv") -> dict:
    return {
        "candidate_build_success": True,
        "candidate_build_status": "valid",
        "rank_eligible": True,
        "ticker": "AAA",
        "timeframe": "4h",
        "entry": 100.0,
        "stop_loss": 95.0,
        "take_profit": 112.0,
        "source_csv": source_name,
        "source_status": "EXACT_MATCH",
    }


def _receipt(stdout: str) -> dict:
    start = stdout.find("{")
    assert start >= 0
    return json.loads(stdout[start:])


def test_run_identity_is_opaque_unique_and_collision_checked(tmp_path: Path):
    first = create_run_context(run_root=tmp_path, run_id_factory=lambda: "run-a")

    assert first["run_id"] == "run-a"
    assert first["run_ref"] == "run-a"
    with pytest.raises(ArtifactContractError, match="already exists"):
        create_run_context(run_root=tmp_path, run_id="run-a")
    with pytest.raises(ArtifactContractError, match="path-safe"):
        create_run_context(run_root=tmp_path, run_id="../bad")


def test_atomic_manifest_commit_payload_digest_and_no_overwrite(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-a")
    result = commit_artifact_payload(
        payload=b'{"ok":true}\n',
        run_root=tmp_path,
        run_id="run-a",
        stage=STAGE_BATCH_ANALYSIS_V1,
        artifact_type=ARTIFACT_TYPE_ANNOTATED_DATASET,
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile=PROFILE_SWING,
        timeframe="4h",
        source_dataset_identity="AAA_4h.csv",
        source_dataset_digest="d" * 64,
        payload_type=PAYLOAD_TYPE_JSON,
        payload_extension=".json",
        artifact_id="artifact-a",
    )

    manifest = load_manifest(result["receipt"]["manifest_ref"], run_root=tmp_path)
    assert manifest["payload_sha256"] == sha256_bytes(b'{"ok":true}\n')
    assert manifest["payload_byte_size"] == len(b'{"ok":true}\n')
    assert result["payload_path"].exists()
    assert result["manifest_path"].exists()
    with pytest.raises(ArtifactContractError, match="already exists"):
        commit_artifact_payload(
            payload=b"{}",
            run_root=tmp_path,
            run_id="run-a",
            stage=STAGE_BATCH_ANALYSIS_V1,
            artifact_type=ARTIFACT_TYPE_ANNOTATED_DATASET,
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            ticker="AAA",
            analysis_profile=PROFILE_SWING,
            timeframe="4h",
            source_dataset_identity="AAA_4h.csv",
            source_dataset_digest="d" * 64,
            payload_type=PAYLOAD_TYPE_JSON,
            payload_extension=".json",
            artifact_id="artifact-a",
        )
    with pytest.raises(ArtifactContractError, match="already exists"):
        commit_artifact_payload(
            payload=b"{}",
            run_root=tmp_path,
            run_id="run-a",
            stage=STAGE_STRATEGY_CANDIDATE_V1,
            artifact_type="CANDIDATE_CORE",
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            ticker="AAA",
            analysis_profile=PROFILE_SWING,
            timeframe="4h",
            source_dataset_identity="AAA_4h.csv",
            source_dataset_digest="d" * 64,
            payload_type=PAYLOAD_TYPE_JSON,
            payload_extension=".json",
            artifact_id="artifact-a",
        )


def test_incomplete_and_corrupt_artifacts_fail_closed(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-a")
    result = commit_artifact_payload(
        payload=b"payload",
        run_root=tmp_path,
        run_id="run-a",
        stage=STAGE_BATCH_ANALYSIS_V1,
        artifact_type=ARTIFACT_TYPE_ANNOTATED_DATASET,
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile=PROFILE_SWING,
        timeframe="4h",
        source_dataset_identity="AAA_4h.csv",
        source_dataset_digest="d" * 64,
        payload_type=PAYLOAD_TYPE_JSON,
        payload_extension=".json",
        artifact_id="artifact-a",
    )

    result["payload_path"].write_text("changed", encoding="utf-8")
    with pytest.raises(ArtifactContractError, match="digest mismatch"):
        validate_manifest(result["manifest"], run_root=tmp_path)

    payload_only = tmp_path / "run-a" / "plot" / "orphan.json"
    payload_only.parent.mkdir(parents=True, exist_ok=True)
    payload_only.write_text("{}", encoding="utf-8")
    with pytest.raises(FileNotFoundError):
        load_manifest(payload_only.with_suffix(".json.manifest.json"), run_root=tmp_path)

    misplaced = tmp_path / "run-a" / "monte_carlo" / result["manifest_path"].name
    misplaced.parent.mkdir(parents=True, exist_ok=True)
    misplaced.write_text(result["manifest_path"].read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ArtifactContractError, match="Manifest path does not match"):
        load_manifest(misplaced, run_root=tmp_path)


def test_manifest_rejects_stage_type_mismatch_and_naive_timestamp(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-a")
    result = commit_artifact_payload(
        payload=b"{}",
        run_root=tmp_path,
        run_id="run-a",
        stage=STAGE_BATCH_ANALYSIS_V1,
        artifact_type=ARTIFACT_TYPE_ANNOTATED_DATASET,
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile=PROFILE_SWING,
        timeframe="4h",
        source_dataset_identity="AAA_4h.csv",
        source_dataset_digest="d" * 64,
        payload_type=PAYLOAD_TYPE_JSON,
        payload_extension=".json",
        artifact_id="artifact-a",
    )
    bad_type = dict(result["manifest"])
    bad_type["artifact_type"] = ARTIFACT_TYPE_MONTE_CARLO_SUMMARY
    with pytest.raises(ArtifactContractError, match="type does not match stage"):
        validate_manifest(bad_type, run_root=tmp_path)

    bad_time = dict(result["manifest"])
    bad_time["created_at"] = "2026-07-31T12:00:00"
    with pytest.raises(ArtifactContractError, match="timezone-aware UTC"):
        validate_manifest(bad_time, run_root=tmp_path)

    bad_source = dict(result["manifest"])
    bad_source["source_ref"] = "../outside.csv"
    with pytest.raises(ArtifactContractError, match="safe relative path"):
        validate_manifest(bad_source, run_root=tmp_path)

    extra_field = dict(result["manifest"])
    extra_field["account_id"] = "forbidden"
    with pytest.raises(ArtifactContractError, match="schema exactly"):
        validate_manifest(extra_field, run_root=tmp_path)

    missing_field = dict(result["manifest"])
    del missing_field["code_commit"]
    with pytest.raises(ArtifactContractError, match="schema exactly"):
        validate_manifest(missing_field, run_root=tmp_path)

    for ref in (
        "run-a/plot/artifact-a.json:stream",
        "run-a\\plot\\artifact-a.json",
        "C:run-a/plot/artifact-a.json",
        "CON",
    ):
        bad_ref = dict(result["manifest"])
        bad_ref["payload_ref"] = ref
        with pytest.raises(ArtifactContractError, match="safe relative path"):
            validate_manifest(bad_ref, run_root=tmp_path)


def test_non_finite_geometry_fails_closed(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-a")
    analysis = annotated_dataset_artifact(
        csv_path=_csv(tmp_path / "AAA_4h.csv"),
        run_root=tmp_path,
        run_id="run-a",
        workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        ticker="AAA",
        analysis_profile=PROFILE_MANUAL_SCENARIO,
        timeframe="4h",
        artifact_id="analysis-a",
    )["manifest"]

    with pytest.raises(ArtifactContractError, match="finite numeric geometry"):
        commit_manual_scenario_artifact(
            analysis_manifest=analysis,
            entry=math.nan,
            stop_loss=95.0,
            take_profit=112.0,
            horizon_bars=20,
            run_root=tmp_path,
        )


def test_workflow_a_manual_lineage_and_digest(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-a")
    source = _csv(tmp_path / "AAA_4h.csv")
    analysis = annotated_dataset_artifact(
        csv_path=source,
        run_root=tmp_path,
        run_id="run-a",
        workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        ticker="AAA",
        analysis_profile=PROFILE_MANUAL_SCENARIO,
        timeframe="4h",
        artifact_id="analysis-a",
    )["manifest"]
    scenario = commit_manual_scenario_artifact(
        analysis_manifest=analysis,
        entry=100.0,
        stop_loss=95.0,
        take_profit=112.0,
        horizon_bars=20,
        run_root=tmp_path,
        artifact_id="scenario-a",
    )["manifest"]
    mc = commit_monte_carlo_summary_artifact(
        parent_manifest=scenario,
        summary={"csv": "AAA_4h.csv", "tf": "4h", "params": {"entry": 100.0, "sl": 95.0, "tp": 112.0, "horizon_bars": 20}},
        workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        run_root=tmp_path,
        artifact_id="mc-a",
    )["manifest"]
    plot = commit_plot_artifact(
        analysis_manifest=analysis,
        monte_carlo_manifest=mc,
        html_payload="<html></html>",
        workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        run_root=tmp_path,
        artifact_id="plot-a",
    )["manifest"]

    expected = manual_scenario_contract(
        analysis_manifest=analysis,
        entry=100.0,
        stop_loss=95.0,
        take_profit=112.0,
        horizon_bars=20,
    )
    assert scenario["manual_scenario_digest"] == expected["manual_scenario_digest"]
    assert scenario["candidate_core_digest"] is None
    assert analysis["artifact_id"] in mc["lineage_artifact_ids"]
    assert plot["input_artifact_ids"] == ["analysis-a", "mc-a"]


def test_monte_carlo_summary_geometry_mismatch_fails_closed(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-a")
    analysis = annotated_dataset_artifact(
        csv_path=_csv(tmp_path / "AAA_4h.csv"),
        run_root=tmp_path,
        run_id="run-a",
        workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        ticker="AAA",
        analysis_profile=PROFILE_MANUAL_SCENARIO,
        timeframe="4h",
        artifact_id="analysis-a",
    )["manifest"]
    scenario = commit_manual_scenario_artifact(
        analysis_manifest=analysis,
        entry=100.0,
        stop_loss=95.0,
        take_profit=112.0,
        horizon_bars=20,
        run_root=tmp_path,
        artifact_id="scenario-a",
    )["manifest"]
    with pytest.raises(ArtifactContractError, match="entry mismatch"):
        commit_monte_carlo_summary_artifact(
            parent_manifest=scenario,
            summary={"csv": "AAA_4h.csv", "tf": "4h", "params": {"entry": 101.0, "sl": 95.0, "tp": 112.0, "horizon_bars": 20}},
            workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
            run_root=tmp_path,
        )


def test_workflow_b_candidate_mc_plot_lineage(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-b")
    source = _csv(tmp_path / "AAA_4h.csv")
    analysis = annotated_dataset_artifact(
        csv_path=source,
        run_root=tmp_path,
        run_id="run-b",
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile=PROFILE_SWING,
        timeframe="4h",
        artifact_id="analysis-b",
    )["manifest"]
    candidate = commit_candidate_core_artifact(
        analysis_manifest=analysis,
        candidate=_candidate(),
        strategy_config_digest=stable_digest({"min_rr": 1.5}),
        run_root=tmp_path,
        artifact_id="candidate-b",
    )["manifest"]
    candidate_payload = json.loads((tmp_path / candidate["payload_ref"]).read_text(encoding="utf-8"))
    assert candidate_payload["candidate_core"] == candidate_core(_candidate())
    assert "rank_eligible" not in candidate_payload["candidate_core"]
    mc = commit_monte_carlo_summary_artifact(
        parent_manifest=candidate,
        summary={"csv": "AAA_4h.csv", "tf": "4h", "params": {"entry": 100.0, "sl": 95.0, "tp": 112.0}},
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        run_root=tmp_path,
        artifact_id="mc-b",
    )["manifest"]
    plot = commit_plot_artifact(
        analysis_manifest=analysis,
        monte_carlo_manifest=mc,
        html_payload="<html></html>",
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        run_root=tmp_path,
        artifact_id="plot-b",
    )["manifest"]

    assert candidate["candidate_core_digest"] == stable_digest(candidate_core(_candidate()))
    assert candidate["strategy_config_digest"] == stable_digest({"min_rr": 1.5})
    assert analysis["artifact_id"] in mc["lineage_artifact_ids"]
    assert plot["parent_artifact_id"] == "mc-b"


def test_invalid_lineage_mixing_and_duplicate_inputs_rejected(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-a")
    source = _csv(tmp_path / "AAA_4h.csv")
    manual_analysis = annotated_dataset_artifact(
        csv_path=source,
        run_root=tmp_path,
        run_id="run-a",
        workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        ticker="AAA",
        analysis_profile=PROFILE_MANUAL_SCENARIO,
        timeframe="4h",
        artifact_id="analysis-a",
    )["manifest"]

    with pytest.raises(ArtifactContractError, match="canonical workflow"):
        commit_candidate_core_artifact(
            analysis_manifest=manual_analysis,
            candidate=_candidate(),
            strategy_config_digest=stable_digest({"min_rr": 1.5}),
            run_root=tmp_path,
        )

    with pytest.raises(ArtifactContractError, match="Duplicate input"):
        commit_artifact_payload(
            payload=b"{}",
            run_root=tmp_path,
            run_id="run-a",
            stage=STAGE_PLOT_V1,
            artifact_type=ARTIFACT_TYPE_ANNOTATED_PLOT,
            workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
            ticker="AAA",
            analysis_profile=PROFILE_MANUAL_SCENARIO,
            timeframe="4h",
            source_dataset_identity=manual_analysis["source_dataset_identity"],
            source_dataset_digest=manual_analysis["source_dataset_digest"],
            payload_type=PAYLOAD_TYPE_JSON,
            payload_extension=".json",
            input_manifests=[manual_analysis, manual_analysis],
        )


def test_forged_plot_lineage_is_rejected(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-a")
    analysis = annotated_dataset_artifact(
        csv_path=_csv(tmp_path / "AAA_4h.csv"),
        run_root=tmp_path,
        run_id="run-a",
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile=PROFILE_SWING,
        timeframe="4h",
        artifact_id="analysis-a",
    )["manifest"]
    payload_path = tmp_path / "run-a" / "monte_carlo" / "forged.json"
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    payload = b'{"workflow_type":"CANONICAL_STRATEGY_DECISION_SUPPORT"}\n'
    payload_path.write_bytes(payload)
    forged = build_artifact_manifest(
        artifact_id="forged-mc",
        run_id="run-a",
        stage="MONTE_CARLO",
        artifact_type="MONTE_CARLO_SUMMARY",
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile=PROFILE_SWING,
        timeframe="4h",
        source_dataset_identity=analysis["source_dataset_identity"],
        source_dataset_digest=analysis["source_dataset_digest"],
        source_ref=analysis["payload_ref"],
        payload_ref="run-a/monte_carlo/forged.json",
        payload_sha256=sha256_bytes(payload),
        payload_byte_size=len(payload),
        payload_type=PAYLOAD_TYPE_JSON,
        lineage_artifact_ids=["analysis-a"],
    )
    (tmp_path / "run-a" / "monte_carlo" / "forged.json.manifest.json").write_text(
        json.dumps(forged, sort_keys=True),
        encoding="utf-8",
    )

    validate_manifest(forged, run_root=tmp_path)
    with pytest.raises(ArtifactContractError, match="requires a parent"):
        commit_plot_artifact(
            analysis_manifest=analysis,
            monte_carlo_manifest=forged,
            html_payload="<html></html>",
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            run_root=tmp_path,
        )


def test_plot_rejects_wrong_run_and_wrong_profile(tmp_path: Path):
    create_run_context(run_root=tmp_path, run_id="run-a")
    create_run_context(run_root=tmp_path, run_id="run-b")
    analysis_a = annotated_dataset_artifact(
        csv_path=_csv(tmp_path / "AAA_4h.csv"),
        run_root=tmp_path,
        run_id="run-a",
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile=PROFILE_SWING,
        timeframe="4h",
        artifact_id="analysis-a",
    )["manifest"]
    analysis_b = annotated_dataset_artifact(
        csv_path=_csv(tmp_path / "AAA_4h_b.csv"),
        run_root=tmp_path,
        run_id="run-b",
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile=PROFILE_SWING,
        timeframe="4h",
        artifact_id="analysis-b",
    )["manifest"]
    candidate = commit_candidate_core_artifact(
        analysis_manifest=analysis_a,
        candidate=_candidate(),
        strategy_config_digest=stable_digest({"min_rr": 1.5}),
        run_root=tmp_path,
        artifact_id="candidate-a",
    )["manifest"]
    mc = commit_monte_carlo_summary_artifact(
        parent_manifest=candidate,
        summary={"csv": "AAA_4h.csv", "tf": "4h", "params": {"entry": 100.0, "sl": 95.0, "tp": 112.0}},
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        run_root=tmp_path,
        artifact_id="mc-a",
    )["manifest"]
    with pytest.raises(ArtifactContractError, match="same run"):
        commit_plot_artifact(
            analysis_manifest=analysis_b,
            monte_carlo_manifest=mc,
            html_payload="<html></html>",
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            run_root=tmp_path,
        )
    wrong_profile = dict(analysis_a)
    wrong_profile["analysis_profile"] = PROFILE_MANUAL_SCENARIO
    with pytest.raises(ArtifactContractError, match="profile"):
        commit_plot_artifact(
            analysis_manifest=wrong_profile,
            monte_carlo_manifest=mc,
            html_payload="<html></html>",
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            run_root=tmp_path,
        )


def test_canonical_cli_receipts_and_no_geometry_override(tmp_path: Path):
    repo = Path(__file__).resolve().parents[1]
    python = repo / "env" / "Scripts" / "python.exe"
    run_root = tmp_path / "runs"
    create_run_context(run_root=run_root, run_id="run-cli")
    analysis = annotated_dataset_artifact(
        csv_path=_cli_csv(tmp_path / "AAA_4h.csv"),
        run_root=run_root,
        run_id="run-cli",
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker="AAA",
        analysis_profile=PROFILE_SWING,
        timeframe="4h",
        artifact_id="analysis-cli",
    )["receipt"]
    strategy = subprocess.run(
        [
            str(python),
            "marketflow/marketflow_strategy.py",
            "--lineage-mode",
            "canonical",
            "--lineage-run-root",
            str(run_root),
            "--lineage-analysis-manifest",
            analysis["manifest_ref"],
            "--max-event-age-bars",
            "3",
            "--use-mc",
            "--use-pnf",
            "--lineage-pop",
            "0.7",
        ],
        cwd=repo,
        check=True,
        text=True,
        capture_output=True,
    )
    candidate_receipt = _receipt(strategy.stdout)
    assert candidate_receipt["artifact_type"] == "CANDIDATE_CORE"

    blocked = subprocess.run(
        [
            str(python),
            "marketflow/marketflow_monte_carlo_trade.py",
            "--lineage-mode",
            "canonical",
            "--lineage-run-root",
            str(run_root),
            "--lineage-candidate-manifest",
            candidate_receipt["manifest_ref"],
            "--entry",
            "1",
        ],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert blocked.returncode != 0
    assert "accepts no geometry overrides" in blocked.stderr

    mc = subprocess.run(
        [
            str(python),
            "marketflow/marketflow_monte_carlo_trade.py",
            "--lineage-mode",
            "canonical",
            "--lineage-run-root",
            str(run_root),
            "--lineage-candidate-manifest",
            candidate_receipt["manifest_ref"],
            "--model",
            "bootstrap",
            "--paths",
            "10",
            "--horizon",
            "2",
            "--no-plots",
        ],
        cwd=repo,
        check=True,
        text=True,
        capture_output=True,
    )
    mc_receipt = _receipt(mc.stdout)
    assert mc_receipt["artifact_type"] == "MONTE_CARLO_SUMMARY"

    plot = subprocess.run(
        [
            str(python),
            "scripts/plot_annotated_features.py",
            "--lineage-mode",
            "canonical",
            "--lineage-run-root",
            str(run_root),
            "--lineage-analysis-manifest",
            analysis["manifest_ref"],
            "--lineage-mc-manifest",
            mc_receipt["manifest_ref"],
        ],
        cwd=repo,
        check=True,
        text=True,
        capture_output=True,
    )
    plot_receipt = _receipt(plot.stdout)
    assert plot_receipt["artifact_type"] == "ANNOTATED_PLOT"
    plot_manifest = load_manifest(plot_receipt["manifest_ref"], run_root=run_root)
    plot_payload = (run_root / plot_manifest["payload_ref"]).read_text(encoding="utf-8")
    assert "MC input" in plot_payload


def test_source_assurance_lineage_writer_boundaries():
    source = Path("marketflow/operational_artifacts.py").read_text(encoding="utf-8")
    mc_source = Path("marketflow/marketflow_monte_carlo_trade.py").read_text(encoding="utf-8")
    plot_source = Path("scripts/plot_annotated_features.py").read_text(encoding="utf-8")
    batch_source = Path("scripts/marketflow_batch_analysis.py").read_text(encoding="utf-8")

    assert "os.replace" not in source
    assert "commit_artifact_payload" in source
    assert "validate_manifest_chain" in source
    assert "canonical lineage mode accepts no geometry overrides" in mc_source
    assert "--lineage-candidate-manifest" in mc_source
    assert "--lineage-analysis-manifest" in plot_source
    assert "except ArtifactContractError" in batch_source
    assert "find_latest" not in source
