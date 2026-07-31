from __future__ import annotations

import json
import subprocess
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from marketflow.fixed_profile_orchestrator import (
    ALL_PROFILES_BLOCKED,
    CANDIDATE_INCOMPLETE,
    DATASET_IDENTITY_AMBIGUOUS,
    DATASET_INVALID,
    DATASET_NOT_FOUND,
    INSUFFICIENT_HISTORY,
    MONTE_CARLO_NOT_AUTHORIZED,
    NormalTickerError,
    OUTCOME_EVALUATION_NOT_AUTHORIZED,
    PROFILE_ANALYSIS_FAILED,
    PROFILE_READY_FOR_ANALYSIS,
    SOURCE_STATUS_EXACT_MATCH,
    normalize_normal_ticker,
    resolve_local_profile_source,
    run_fixed_profile_orchestrator,
    validate_profile_dataset,
)
from marketflow.marketflow_data_parameters import (
    FIXED_PROFILE_VERSION,
    FixedAnalysisProfile,
    fixed_analysis_profiles,
    fixed_profile_contract_payload,
    fixed_profile_digest,
    get_fixed_analysis_profile,
)
from marketflow.operational_artifacts import DEFAULT_RUN_ROOT, load_manifest, stable_digest


def _id_factory(*values: str):
    iterator = iter(values)
    return lambda: next(iterator)


def _write_csv(
    path: Path,
    rows: int,
    *,
    timeframe: str = "1d",
    invalid_last: bool = False,
    duplicate_last: bool = False,
    bad_volume_last: bool = False,
) -> Path:
    start = "2026-01-01"
    delta = "4h" if timeframe == "4h" else "1D"
    timestamps = [str(item) for item in __import__("pandas").date_range(start=start, periods=rows, freq=delta)]
    if duplicate_last and rows > 1:
        timestamps[-1] = timestamps[-2]
    lines = [
        "timestamp,open,high,low,close,volume,tr_low,tr_high,wyckoff_phase,wyckoff_confirmed_event,wyckoff_confirmed_event_occurrence,pnf_score"
    ]
    for index in range(rows):
        close = 100 + index
        high = close + 2
        low = close - 2
        if invalid_last and index == rows - 1:
            high = close - 3
            low = close + 3
        event = "SOS" if index == rows - 1 else ""
        occurrence = "True" if index == rows - 1 else "False"
        volume = -1 if bad_volume_last and index == rows - 1 else 1000 + index
        lines.append(
            f"{timestamps[index]},{close - 1},{high},{low},{close},"
            f"{volume},{close - 5},{close + 12},D,{event},{occurrence},0.8"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_fixed_profile_contract_values_digest_and_immutability():
    swing, position = fixed_analysis_profiles()

    assert swing.profile_version == FIXED_PROFILE_VERSION
    assert swing.profile_id == "SWING"
    assert swing.candidate_timeframe == "4h"
    assert swing.minimum_valid_rows == 390
    assert swing.intended_holding_concept == "SEVERAL_TRADING_DAYS"
    assert swing.higher_timeframe_context == "NOT_IMPLEMENTED"
    assert swing.automatic_monte_carlo is False
    assert swing.automatic_outcome_evaluation is False

    assert position.profile_id == "POSITION_SWING"
    assert position.candidate_timeframe == "1d"
    assert position.minimum_valid_rows == 560
    assert position.intended_holding_concept == "SEVERAL_DAYS_TO_WEEKS"

    assert fixed_profile_digest(swing) == fixed_profile_digest(get_fixed_analysis_profile("SWING"))
    changed_payload = fixed_profile_contract_payload(swing)
    changed_payload["minimum_valid_rows"] = 391
    assert stable_digest(changed_payload) != fixed_profile_digest(swing)
    reordered_payload = {
        "automatic_outcome_evaluation": swing.automatic_outcome_evaluation,
        "automatic_monte_carlo": swing.automatic_monte_carlo,
        "higher_timeframe_context": swing.higher_timeframe_context,
        "intended_holding_concept": swing.intended_holding_concept,
        "minimum_valid_rows": swing.minimum_valid_rows,
        "candidate_timeframe": swing.candidate_timeframe,
        "profile_id": swing.profile_id,
        "profile_version": swing.profile_version,
    }
    assert stable_digest(reordered_payload) == fixed_profile_digest(swing)
    with pytest.raises(FrozenInstanceError):
        swing.minimum_valid_rows = 1
    with pytest.raises(TypeError):
        FixedAnalysisProfile(
            profile_version=FIXED_PROFILE_VERSION,
            profile_id="CUSTOM",
            candidate_timeframe="1h",
            minimum_valid_rows=1,
            intended_holding_concept="CUSTOM",
            higher_timeframe_context="NOT_IMPLEMENTED",
            automatic_monte_carlo=False,
            automatic_outcome_evaluation=False,
        )
    with pytest.raises(ValueError):
        get_fixed_analysis_profile("CUSTOM")


def test_fixed_profiles_do_not_depend_on_legacy_primary_timeframe_order():
    swing = get_fixed_analysis_profile("SWING")
    position = get_fixed_analysis_profile("POSITION_SWING")

    assert swing.candidate_timeframe == "4h"
    assert position.candidate_timeframe == "1d"


@pytest.mark.parametrize(
    "value",
    ["AAA", "brk.b", "MS-FT", "A1"],
)
def test_normal_ticker_input_accepts_one_supported_symbol(value: str):
    assert normalize_normal_ticker(value) == value.upper()


@pytest.mark.parametrize(
    "value",
    ["", " AAA", "AAA ", "AA/A", "AA\\A", "AAA,MSFT", "AAA:4h", "AAA_4h", "AAA.csv", "AA\x01A", "AA$A"],
)
def test_normal_ticker_input_rejects_non_ticker_values(value: str):
    with pytest.raises(NormalTickerError):
        normalize_normal_ticker(value)


def test_source_resolution_exact_missing_duplicate_wrong_and_similar(tmp_path: Path):
    swing = get_fixed_analysis_profile("SWING")
    source_root = tmp_path / "reports"
    _write_csv(source_root / "run" / "AAA" / "AAA_4h_wyckoff_annotated.csv", 390, timeframe="4h")
    _write_csv(source_root / "run" / "AA" / "AA_4h_wyckoff_annotated.csv", 390, timeframe="4h")
    _write_csv(source_root / "run" / "AAA" / "AAA_1d_wyckoff_annotated.csv", 560, timeframe="1d")

    resolution = resolve_local_profile_source(ticker="AAA", profile=swing, source_root=source_root)
    assert resolution["status"] == SOURCE_STATUS_EXACT_MATCH
    assert resolution["source"].name == "AAA_4h_wyckoff_annotated.csv"

    assert resolve_local_profile_source(ticker="BBB", profile=swing, source_root=source_root)["status"] == DATASET_NOT_FOUND
    _write_csv(source_root / "other" / "AAA" / "AAA_4h_wyckoff_annotated.csv", 390, timeframe="4h")
    assert resolve_local_profile_source(ticker="AAA", profile=swing, source_root=source_root)["status"] == DATASET_IDENTITY_AMBIGUOUS


def test_source_resolution_requires_canonical_annotated_source(tmp_path: Path):
    swing = get_fixed_analysis_profile("SWING")
    source_root = tmp_path / "reports"
    _write_csv(source_root / "run" / "AAA" / "AAA_4h.csv", 390, timeframe="4h")

    assert resolve_local_profile_source(ticker="AAA", profile=swing, source_root=source_root)["status"] == DATASET_NOT_FOUND


def test_daily_duplicate_identity_blocks_position_profile_independently(tmp_path: Path):
    position = get_fixed_analysis_profile("POSITION_SWING")
    source_root = tmp_path / "reports"
    _write_csv(source_root / "run" / "AAA" / "AAA_1d_wyckoff_annotated.csv", 560, timeframe="1d")
    _write_csv(source_root / "other" / "AAA" / "AAA_1d_wyckoff_annotated.csv", 560, timeframe="1d")

    assert resolve_local_profile_source(ticker="AAA", profile=position, source_root=source_root)["status"] == DATASET_IDENTITY_AMBIGUOUS


def test_source_resolution_skips_path_escape_symlink(tmp_path: Path):
    swing = get_fixed_analysis_profile("SWING")
    source_root = tmp_path / "reports"
    source_root.mkdir()
    outside = _write_csv(tmp_path / "AAA_4h_wyckoff_annotated.csv", 390, timeframe="4h")
    link = source_root / "AAA_4h_wyckoff_annotated.csv"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")

    assert resolve_local_profile_source(ticker="AAA", profile=swing, source_root=source_root)["status"] == DATASET_NOT_FOUND


def test_row_gates_exact_boundaries_invalid_rows_and_invalid_chronology(tmp_path: Path):
    swing = get_fixed_analysis_profile("SWING")
    position = get_fixed_analysis_profile("POSITION_SWING")
    exact_swing = _write_csv(tmp_path / "AAA_4h_wyckoff_annotated.csv", 390, timeframe="4h")
    short_swing = _write_csv(tmp_path / "BBB_4h_wyckoff_annotated.csv", 389, timeframe="4h")
    exact_position = _write_csv(tmp_path / "AAA_1d_wyckoff_annotated.csv", 560, timeframe="1d")
    short_position = _write_csv(tmp_path / "BBB_1d_wyckoff_annotated.csv", 559, timeframe="1d")
    invalid_row = _write_csv(tmp_path / "CCC_4h_wyckoff_annotated.csv", 390, timeframe="4h", invalid_last=True)
    duplicate_timestamp = _write_csv(tmp_path / "DDD_4h_wyckoff_annotated.csv", 390, timeframe="4h", duplicate_last=True)
    invalid_volume = _write_csv(tmp_path / "EEE_4h_wyckoff_annotated.csv", 390, timeframe="4h", bad_volume_last=True)

    assert validate_profile_dataset(csv_path=exact_swing, source_root=tmp_path, profile=swing)["status"] == "PROFILE_READY_FOR_ANALYSIS"
    assert validate_profile_dataset(csv_path=short_swing, source_root=tmp_path, profile=swing)["status"] == INSUFFICIENT_HISTORY
    assert validate_profile_dataset(csv_path=exact_position, source_root=tmp_path, profile=position)["status"] == "PROFILE_READY_FOR_ANALYSIS"
    assert validate_profile_dataset(csv_path=short_position, source_root=tmp_path, profile=position)["status"] == INSUFFICIENT_HISTORY
    invalid_result = validate_profile_dataset(csv_path=invalid_row, source_root=tmp_path, profile=swing)
    assert invalid_result["actual_valid_rows"] == 389
    assert invalid_result["status"] == INSUFFICIENT_HISTORY
    volume_result = validate_profile_dataset(csv_path=invalid_volume, source_root=tmp_path, profile=swing)
    assert volume_result["actual_valid_rows"] == 389
    assert volume_result["status"] == INSUFFICIENT_HISTORY
    assert validate_profile_dataset(csv_path=duplicate_timestamp, source_root=tmp_path, profile=swing)["status"] == DATASET_INVALID


def _complete_candidate(request):
    return {
        "candidate_build_success": True,
        "candidate_build_status": "valid",
        "rank_eligible": True,
        "ticker": request.source_identity.ticker,
        "timeframe": request.source_identity.timeframe,
        "entry": 100.0,
        "stop_loss": 95.0,
        "take_profit": 112.0,
        "source_csv": request.source_identity.source.name,
        "source_status": "EXACT_MATCH",
    }


def test_orchestrator_reports_all_completed_when_both_candidates_are_eligible(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import marketflow.marketflow_strategy as strategy

    source_root = tmp_path / "reports"
    run_root = tmp_path / "runs"
    _write_csv(source_root / "batch_20260731_010203" / "AAA" / "AAA_4h_wyckoff_annotated.csv", 390, timeframe="4h")
    _write_csv(source_root / "batch_20260731_010203" / "AAA" / "AAA_1d_wyckoff_annotated.csv", 560, timeframe="1d")
    monkeypatch.setattr(strategy, "build_candidate_from_prefix", _complete_candidate)

    receipt = run_fixed_profile_orchestrator(
        "AAA",
        source_root=source_root,
        run_root=run_root,
        run_id_factory=_id_factory("run-swing", "run-position"),
        artifact_id_factory=_id_factory("analysis-swing", "candidate-swing", "analysis-position", "candidate-position"),
    )

    assert receipt["status"] == "ALL_PROFILES_COMPLETED"
    results = {item["profile_id"]: item for item in receipt["profile_results"]}
    assert results["SWING"]["candidate_status"] == "CANDIDATE_COMPLETE"
    assert results["POSITION_SWING"]["candidate_status"] == "CANDIDATE_COMPLETE"
    assert len(results["SWING"]["artifacts"]) == 2
    assert len(results["POSITION_SWING"]["artifacts"]) == 2


def test_orchestrator_reports_partial_completion_when_one_candidate_is_eligible(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import marketflow.marketflow_strategy as strategy

    source_root = tmp_path / "reports"
    run_root = tmp_path / "runs"
    _write_csv(source_root / "batch_20260731_010203" / "AAA" / "AAA_4h_wyckoff_annotated.csv", 390, timeframe="4h")
    monkeypatch.setattr(strategy, "build_candidate_from_prefix", _complete_candidate)

    receipt = run_fixed_profile_orchestrator(
        "AAA",
        source_root=source_root,
        run_root=run_root,
        run_id_factory=_id_factory("run-swing"),
        artifact_id_factory=_id_factory("analysis-swing", "candidate-swing"),
    )

    results = {item["profile_id"]: item for item in receipt["profile_results"]}
    assert receipt["status"] == "PARTIAL_PROFILE_COMPLETION"
    assert results["SWING"]["candidate_status"] == "CANDIDATE_COMPLETE"
    assert results["POSITION_SWING"]["status"] == DATASET_NOT_FOUND


def test_orchestrator_builds_independent_ready_profile_lineage_without_blending(tmp_path: Path):
    source_root = tmp_path / "reports"
    run_root = tmp_path / "runs"
    _write_csv(source_root / "batch_20260731_010203" / "AAA" / "AAA_4h_wyckoff_annotated.csv", 390, timeframe="4h")
    _write_csv(source_root / "batch_20260731_010203" / "AAA" / "AAA_1d_wyckoff_annotated.csv", 560, timeframe="1d")

    receipt = run_fixed_profile_orchestrator(
        "AAA",
        source_root=source_root,
        run_root=run_root,
        run_id_factory=_id_factory("run-swing", "run-position"),
        artifact_id_factory=_id_factory("analysis-swing", "candidate-swing", "analysis-position", "candidate-position"),
    )

    assert receipt["status"] == ALL_PROFILES_BLOCKED
    assert "score" not in receipt
    assert "recommendation" not in receipt
    results = {item["profile_id"]: item for item in receipt["profile_results"]}
    assert results["SWING"]["readiness_status"] == PROFILE_READY_FOR_ANALYSIS
    assert results["POSITION_SWING"]["readiness_status"] == PROFILE_READY_FOR_ANALYSIS
    assert results["SWING"]["candidate_status"] == CANDIDATE_INCOMPLETE
    assert results["POSITION_SWING"]["candidate_status"] == CANDIDATE_INCOMPLETE
    assert results["SWING"]["candidate_reason"] == "SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED"
    assert results["SWING"]["score_status"] == "SCORE_COMPLETE"
    assert results["SWING"]["score_profile_calibration"] == "SCORE_PROFILE_CALIBRATION_NOT_ESTABLISHED"
    assert results["SWING"]["active_evidence_profile"] == "phase,event,trend"
    assert results["SWING"]["disabled_components"] == ["pnf", "pop"]
    assert results["SWING"]["missing_components"] == []
    assert results["SWING"]["invalid_components"] == []
    assert results["SWING"]["run_id"] != results["POSITION_SWING"]["run_id"]
    assert results["SWING"]["candidate_digest"] is None
    assert results["POSITION_SWING"]["candidate_digest"] is None
    for result in results.values():
        assert result["monte_carlo_status"] == MONTE_CARLO_NOT_AUTHORIZED
        assert result["outcome_evaluation_status"] == OUTCOME_EVALUATION_NOT_AUTHORIZED
        assert len(result["artifacts"]) == 1
        for artifact in result["artifacts"]:
            assert not Path(artifact["manifest_ref"]).is_absolute()
            assert not Path(artifact["payload_ref"]).is_absolute()
    swing_analysis = load_manifest(results["SWING"]["artifacts"][0]["manifest_ref"], run_root=run_root)
    position_analysis = load_manifest(results["POSITION_SWING"]["artifacts"][0]["manifest_ref"], run_root=run_root)
    assert swing_analysis["analysis_profile"] == "SWING"
    assert position_analysis["analysis_profile"] == "POSITION_SWING"


def test_orchestrator_profiles_block_independently(tmp_path: Path):
    source_root = tmp_path / "reports"
    run_root = tmp_path / "runs"
    _write_csv(source_root / "batch_20260731_010203" / "AAA" / "AAA_4h_wyckoff_annotated.csv", 390, timeframe="4h")

    receipt = run_fixed_profile_orchestrator(
        "AAA",
        source_root=source_root,
        run_root=run_root,
        run_id_factory=_id_factory("run-swing"),
        artifact_id_factory=_id_factory("analysis-swing", "candidate-swing"),
    )

    results = {item["profile_id"]: item for item in receipt["profile_results"]}
    assert receipt["status"] == ALL_PROFILES_BLOCKED
    assert results["SWING"]["readiness_status"] == PROFILE_READY_FOR_ANALYSIS
    assert results["SWING"]["candidate_status"] == CANDIDATE_INCOMPLETE
    assert len(results["SWING"]["artifacts"]) == 1
    assert results["POSITION_SWING"]["status"] == DATASET_NOT_FOUND


def test_profile_failure_after_run_preserves_partial_receipt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import marketflow.marketflow_strategy as strategy

    source_root = tmp_path / "reports"
    run_root = tmp_path / "runs"
    _write_csv(source_root / "batch_20260731_010203" / "AAA" / "AAA_4h_wyckoff_annotated.csv", 390, timeframe="4h")
    monkeypatch.setattr(strategy, "build_candidate_from_prefix", lambda request: (_ for _ in ()).throw(RuntimeError("synthetic builder failure")))

    receipt = run_fixed_profile_orchestrator(
        "AAA",
        source_root=source_root,
        run_root=run_root,
        run_id_factory=_id_factory("run-swing"),
        artifact_id_factory=_id_factory("analysis-swing", "unused-candidate"),
    )

    results = {item["profile_id"]: item for item in receipt["profile_results"]}
    assert results["SWING"]["status"] == PROFILE_ANALYSIS_FAILED
    assert results["SWING"]["candidate_status"] == "CANDIDATE_NOT_AVAILABLE"
    assert results["SWING"]["run_id"] == "run-swing"
    assert [artifact["artifact_id"] for artifact in results["SWING"]["artifacts"]] == ["analysis-swing"]
    assert results["POSITION_SWING"]["status"] == DATASET_NOT_FOUND


def test_orchestrator_all_profiles_blocked_without_lineage(tmp_path: Path):
    receipt = run_fixed_profile_orchestrator("AAA", source_root=tmp_path / "missing", run_root=tmp_path / "runs")

    assert receipt["status"] == ALL_PROFILES_BLOCKED
    assert all(not result["artifacts"] for result in receipt["profile_results"])


def test_normal_cli_rejects_semantic_options_and_malformed_ticker():
    repo = Path(__file__).resolve().parents[1]
    python = repo / "env" / "Scripts" / "python.exe"

    forbidden = subprocess.run(
        [str(python), "-m", "marketflow", "normal", "AAA", "--timeframe", "4h"],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert forbidden.returncode != 0
    assert "unrecognized arguments" in forbidden.stderr

    display_flag = subprocess.run(
        [str(python), "-m", "marketflow", "normal", "AAA", "--json"],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert display_flag.returncode != 0
    assert "unrecognized arguments" in display_flag.stderr

    malformed = subprocess.run(
        [str(python), "-m", "marketflow", "normal", "AAA,MSFT"],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert malformed.returncode == 2
    payload = json.loads(malformed.stdout)
    assert payload["status"] == "ORCHESTRATOR_INVALID"


def test_normal_cli_runs_without_streamlit_import_for_blocked_local_data():
    repo = Path(__file__).resolve().parents[1]
    python = repo / "env" / "Scripts" / "python.exe"
    result = subprocess.run(
        [str(python), "-m", "marketflow", "normal", "ZZZUNLIKELY"],
        cwd=repo,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["status"] in {ALL_PROFILES_BLOCKED, "PARTIAL_PROFILE_COMPLETION", "ALL_PROFILES_COMPLETED"}
    assert "streamlit" not in result.stderr.lower()
    assert str(repo) not in result.stdout
    assert str(DEFAULT_RUN_ROOT) not in result.stdout


def test_blocked_normal_cli_does_not_import_advanced_or_provider_modules():
    repo = Path(__file__).resolve().parents[1]
    python = repo / "env" / "Scripts" / "python.exe"
    script = (
        "import json,sys;"
        "from marketflow.__main__ import main;"
        "sys.argv=['marketflow','normal','ZZZUNLIKELY'];"
        "rc=main();"
        "advanced=['marketflow.marketflow_strategy','marketflow.marketflow_facade','marketflow.marketflow_data_provider','streamlit'];"
        "print('__MODULES__'+json.dumps({'rc':rc,'loaded':[name for name in advanced if name in sys.modules]}, sort_keys=True))"
    )
    result = subprocess.run(
        [str(python), "-c", script],
        cwd=repo,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0
    marker_line = [line for line in result.stdout.splitlines() if line.startswith("__MODULES__")][-1]
    payload = json.loads(marker_line.removeprefix("__MODULES__"))
    assert payload == {"loaded": [], "rc": 0}
