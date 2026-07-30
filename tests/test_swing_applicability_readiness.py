from __future__ import annotations

import ast
import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest

from marketflow.research import applicability_readiness as readiness


def _write_dataset(
    path: Path,
    rows: int = 300,
    *,
    timeframe_minutes: int = 1440,
    duplicate_timestamp: bool = False,
    invalid_geometry: bool = False,
    include_volume: bool = True,
    include_annotations: bool = True,
) -> Path:
    start = datetime(2025, 1, 1, 9, 30)
    records = []
    for index in range(rows):
        timestamp = start + timedelta(minutes=index * timeframe_minutes)
        if duplicate_timestamp and index == rows - 1:
            timestamp = start
        close = 100.0 + index * 0.1
        high = close + 1.0
        low = close - 1.0
        if invalid_geometry and index == rows - 1:
            high = low - 1.0
        row = {
            "timestamp": timestamp.isoformat(),
            "open": close - 0.2,
            "high": high,
            "low": low,
            "close": close,
        }
        if include_volume:
            row["volume"] = 1000 + index
        if include_annotations:
            row.update(
                {
                    "wyckoff_phase": "D",
                    "wyckoff_confirmed_event": "SOS" if index == rows - 1 else "",
                    "wyckoff_confirmed_event_occurrence": index == rows - 1,
                    "tr_low": close - 3.0,
                    "tr_high": close + 5.0,
                }
            )
        records.append(row)
    pd.DataFrame(records).to_csv(path, index=False)
    return path


def test_manifest_identity_safe_paths_and_unknown_adjustment(tmp_path: Path) -> None:
    path = _write_dataset(tmp_path / "AAPL_1d_wyckoff_annotated.csv")

    manifest = readiness.build_dataset_manifest(tmp_path, [tmp_path])

    assert manifest["status"] == "valid"
    assert manifest["dataset_count"] == 1
    row = manifest["datasets"][0]
    assert row["ticker"] == "AAPL"
    assert row["timeframe"] == "1d"
    assert row["relative_path"] == path.name
    assert not Path(row["relative_path"]).is_absolute()
    assert row["corporate_action_adjustment_status"] == readiness.ADJUSTMENT_STATUS_UNKNOWN
    assert manifest["contains_performance"] is False
    assert manifest["contains_candidate_results"] is False


def test_duplicate_dataset_identity_fails_manifest_closed(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _write_dataset(first / "AAPL_1d_wyckoff_annotated.csv")
    _write_dataset(second / "AAPL_1d_wyckoff_annotated.csv")

    manifest = readiness.build_dataset_manifest(tmp_path, [first, second])

    assert manifest["status"] == "ineligible"
    assert manifest["errors"] == ["DUPLICATE_DATASET_IDENTITY"]
    assert manifest["duplicate_identities"] == [{"ticker": "AAPL", "timeframe": "1d", "count": 2}]


def test_ambiguous_dataset_identity_fails_closed(tmp_path: Path) -> None:
    path = _write_dataset(tmp_path / "AAPL_1d_4h_wyckoff_annotated.csv", rows=400, timeframe_minutes=240)

    manifest = readiness.build_dataset_manifest(tmp_path, [tmp_path])

    assert manifest["dataset_count"] == 1
    row = manifest["datasets"][0]
    assert row["relative_path"] == path.name
    assert row["status"] == "ineligible"
    assert "DATASET_IDENTITY_AMBIGUOUS" in row["errors"]


def test_manifest_bytes_and_digest_are_deterministic(tmp_path: Path) -> None:
    _write_dataset(tmp_path / "MSFT_4h_wyckoff_annotated.csv", timeframe_minutes=240)

    first = readiness.build_dataset_manifest(tmp_path, [tmp_path])
    second = readiness.build_dataset_manifest(tmp_path, [tmp_path])

    assert readiness.canonical_json_bytes(first) == readiness.canonical_json_bytes(second)
    assert first["manifest_digest"] == second["manifest_digest"]


def test_chronology_ohlcv_and_annotation_checks(tmp_path: Path) -> None:
    path = _write_dataset(
        tmp_path / "MSFT_4h_wyckoff_annotated.csv",
        timeframe_minutes=240,
        duplicate_timestamp=True,
        invalid_geometry=True,
    )

    row = readiness.inspect_dataset(path, tmp_path)

    assert row.duplicate_timestamp_count == 1
    assert row.non_monotonic_timestamp_count >= 1
    assert row.invalid_high_low_geometry_count == 1
    assert row.volume_available is True
    assert row.wyckoff_annotations_available is True
    assert row.tr_levels_available is True
    assert row.confirmed_event_occurrence_markers_available is True
    assert row.status == "ineligible"


def test_valid_ohlcv_row_count_requires_volume(tmp_path: Path) -> None:
    path = _write_dataset(tmp_path / "MSFT_4h_wyckoff_annotated.csv", include_volume=False)

    row = readiness.inspect_dataset(path, tmp_path)

    assert row.volume_available is False
    assert row.missing_or_invalid_volume_count == row.total_row_count
    assert row.valid_ohlcv_row_count == 0
    assert "VOLUME_COLUMN_MISSING" in row.errors
    assert "MISSING_OR_INVALID_VOLUME_ROWS" in row.warnings
    assert row.status == "ineligible"


def test_timestamp_range_uses_min_and_max_not_physical_row_order(tmp_path: Path) -> None:
    path = _write_dataset(tmp_path / "MSFT_4h_wyckoff_annotated.csv", rows=3, timeframe_minutes=240)
    frame = pd.read_csv(path)
    frame = frame.iloc[[1, 0, 2]]
    frame.to_csv(path, index=False)

    row = readiness.inspect_dataset(path, tmp_path)

    assert row.earliest_timestamp == pd.Timestamp("2025-01-01T09:30:00").isoformat()
    assert row.latest_timestamp == pd.Timestamp("2025-01-01T17:30:00").isoformat()
    assert row.non_monotonic_timestamp_count == 1
    assert row.status == "ineligible"


def test_profile_feasibility_uses_coverage_only(tmp_path: Path) -> None:
    for ticker in ("AAPL", "IONQ", "MSFT"):
        _write_dataset(tmp_path / f"{ticker}_4h_wyckoff_annotated.csv", rows=400, timeframe_minutes=240)
        _write_dataset(tmp_path / f"{ticker}_1d_wyckoff_annotated.csv", rows=600)
    manifest = readiness.build_dataset_manifest(tmp_path, [tmp_path])

    swing = readiness.assess_profile_feasibility(manifest, "SWING")
    position = readiness.assess_profile_feasibility(manifest, "POSITION_SWING")

    assert swing["status"] == "READY_FOR_PROTOCOL_FREEZE"
    assert position["status"] == "READY_FOR_PROTOCOL_FREEZE"
    assert swing["required_valid_ohlcv_rows"] == 390
    assert position["required_valid_ohlcv_rows"] == 560
    assert swing["unique_eligible_identity_count"] == 3
    assert position["unique_eligible_identity_count"] == 3
    assert "performance" not in json.dumps(swing).lower()


def test_profile_feasibility_blocks_duplicate_identity(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _write_dataset(first / "AAPL_4h_wyckoff_annotated.csv", rows=400, timeframe_minutes=240)
    _write_dataset(second / "AAPL_4h_wyckoff_annotated.csv", rows=400, timeframe_minutes=240)
    manifest = readiness.build_dataset_manifest(tmp_path, [first, second])

    result = readiness.assess_profile_feasibility(manifest, "SWING")

    assert result["status"] == "BLOCKED"
    assert "DUPLICATE_DATASET_IDENTITY" in result["blockers"]


def test_profile_feasibility_uses_valid_ohlcv_rows_not_total_rows(tmp_path: Path) -> None:
    path = _write_dataset(tmp_path / "AAPL_4h_wyckoff_annotated.csv", rows=400, timeframe_minutes=240)
    frame = pd.read_csv(path)
    frame.loc[50:, "close"] = float("nan")
    frame.to_csv(path, index=False)
    manifest = readiness.build_dataset_manifest(tmp_path, [tmp_path])

    result = readiness.assess_profile_feasibility(manifest, "SWING")

    assert manifest["datasets"][0]["total_row_count"] == 400
    assert manifest["datasets"][0]["valid_ohlcv_row_count"] == 50
    assert result["status"] == "BLOCKED"
    assert "INSUFFICIENT_ROWS_FOR_MULTIPLE_SEQUENTIAL_SPLITS" in result["blockers"]


def test_scan_root_outside_repository_fails_before_traversal(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}_outside"
    outside.mkdir()

    with pytest.raises(ValueError, match="scan root must stay inside repository root"):
        readiness.discover_canonical_datasets(tmp_path, [outside])


def test_manifest_output_must_stay_under_ignored_research_artifacts(tmp_path: Path) -> None:
    manifest = {"schema_version": "x", "datasets": []}

    with pytest.raises(ValueError, match="manifest output must be under .marketflow/research"):
        readiness.write_manifest(manifest, tmp_path / "docs" / "manifest.json", tmp_path)

    outside = tmp_path.parent / f"{tmp_path.name}_outside_manifest.json"
    with pytest.raises(ValueError, match="manifest output must stay inside repository root"):
        readiness.write_manifest(manifest, outside, tmp_path)


def test_universe_partition_is_deterministic_and_not_performance_based() -> None:
    partition = readiness.deterministic_universe_partition(["MSFT", "AAPL", "IONQ", "AAPL", "LOAR"])

    assert partition == {
        "development": ["AAPL", "MSFT"],
        "validation": ["IONQ"],
        "locked_holdout": ["LOAR"],
    }


def test_temporal_split_chronology_and_embargo() -> None:
    split = readiness.propose_temporal_splits("2020-01-01", "2025-01-01", embargo_bars=20)

    assert split["development"]["start"] < split["development"]["end"]
    assert split["development"]["end"] == split["validation"]["start"]
    assert split["validation"]["end"] == split["locked_holdout"]["start"]
    assert split["embargo_bars"] == 20
    assert "outcome horizon" in split["purge_rule"]


def test_protocol_serialization_digest_changes_on_one_field(tmp_path: Path) -> None:
    _write_dataset(tmp_path / "AAPL_1d_wyckoff_annotated.csv", rows=600)
    manifest = readiness.build_dataset_manifest(tmp_path, [tmp_path])
    protocol = readiness.build_protocol_model(manifest)
    changed = json.loads(json.dumps(protocol))
    changed["profile_definitions"]["POSITION_SWING"]["primary_horizon_bars"] = 25

    assert protocol["status"] == readiness.PROTOCOL_STATUS_PROPOSED_WITH_BLOCKERS
    assert readiness.sha256_digest({key: value for key, value in changed.items() if key != "protocol_digest"}) != protocol["protocol_digest"]


def test_trial_ledger_append_only_rules() -> None:
    first = readiness.build_trial_ledger_example()["trials"][0]
    second = {**first, "trial_id": "TRIAL-YYYYMMDD-002"}
    existing = [first]

    assert readiness.validate_trial_ledger_append_only(existing, [first, second])["success"] is True
    assert readiness.validate_trial_ledger_append_only(existing, [])["success"] is False
    assert readiness.validate_trial_ledger_append_only(existing, [{**first, "status": "edited"}])["success"] is False
    assert readiness.validate_trial_ledger_append_only(existing, [first, {**second, "trial_id": first["trial_id"]}])["success"] is False
    malformed = dict(second)
    malformed.pop("strategy_config_digest")
    assert readiness.validate_trial_ledger_append_only(existing, [first, malformed])["success"] is False
    nested_absolute = {**second, "trial_id": "TRIAL-YYYYMMDD-003", "cost_assumptions": {"source": str(Path.cwd())}}
    assert readiness.validate_trial_ledger_append_only(existing, [first, nested_absolute])["success"] is False


def test_readiness_cli_writes_ignored_manifest_without_absolute_paths(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_dataset(tmp_path / "AAPL_1d_wyckoff_annotated.csv", rows=600)
    output = tmp_path / ".marketflow" / "research" / "manifest.json"

    exit_code = readiness.main(["--repo-root", str(tmp_path), "--scan-root", str(tmp_path), "--manifest-output", str(output)])
    printed = json.loads(capsys.readouterr().out)
    manifest = json.loads(output.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert printed["no_performance_inspected"] is True
    assert output.exists()
    assert not Path(manifest["datasets"][0]["relative_path"]).is_absolute()


def test_no_forbidden_runtime_imports_or_calls() -> None:
    source = Path("marketflow/research/applicability_readiness.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_names = {
        "evaluate_candidate_outcome",
        "evaluate_candidate_outcome_from_csv",
        "evaluate_candidate_snapshot_rows",
        "build_and_evaluate_walk_forward_cases_from_csv",
        "summarize_walk_forward_validation",
        "build_walk_forward_campaign_grouped_summary",
        "rank_long_candidates",
        "build_candidate_from_prefix",
    }
    imported_modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    called_attributes = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }

    assert "marketflow.backtesting.outcome_engine" not in imported_modules
    assert "marketflow.backtesting.outcome_engine" not in imported_from
    assert "marketflow.services.walk_forward_campaign_service" not in imported_modules
    assert "marketflow.services.walk_forward_campaign_service" not in imported_from
    assert forbidden_names.isdisjoint(called_names)
    assert forbidden_names.isdisjoint(called_attributes)
