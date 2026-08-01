from __future__ import annotations

import ast
import json
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from marketflow.historical_data import artifacts
from marketflow.historical_data import frozen_calendar as fc
from marketflow.historical_data import pipeline
from marketflow.historical_data import rth_bar_engine as rth
from marketflow.research import acquisition_contract_v2 as acv2
from marketflow.research import acquisition_contract_v2_1 as acv21
from marketflow.research import fixed_date_acquisition_contract as fdac


REPO_ROOT = Path(__file__).resolve().parents[1]
V1_DIGEST = "29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e"
V2_DIGEST = "59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0"
V21_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"


def _ids() -> callable:
    values = iter(
        [
            "calendar-a",
            "source-a",
            "dividends-a",
            "swing-a",
            "swing-segments-a",
            "position-a",
            "position-segments-a",
            "receipt-a",
        ]
    )
    return lambda: next(values)


def _fixture():
    return pipeline.synthetic_self_check_fixture()


def _commit_roots(tmp_path: Path):
    calendar, source_bars, dividends = _fixture()
    run = artifacts.create_historical_run(run_root=tmp_path, run_id="run-a", created_at_utc="2026-08-01T00:00:00Z")
    calendar_result = artifacts.commit_calendar_candidate_artifact(
        calendar=calendar,
        run_root=tmp_path,
        run_id=run.run_id,
        artifact_id="calendar-a",
        created_at_utc="2026-08-01T00:00:00Z",
    )
    source_result = artifacts.commit_normalized_15m_artifact(
        source_bars=source_bars,
        run_root=tmp_path,
        run_id=run.run_id,
        artifact_id="source-a",
        created_at_utc="2026-08-01T00:00:00Z",
    )
    dividend_result = artifacts.commit_dividend_event_set_artifact(
        events=dividends,
        run_root=tmp_path,
        run_id=run.run_id,
        artifact_id="dividends-a",
        created_at_utc="2026-08-01T00:00:00Z",
    )
    return run, calendar_result, source_result, dividend_result


def _manifest_ref(result: dict, run_root: Path) -> str:
    return artifacts.manifest_ref_from_result(result, run_root=run_root)


def test_historical_run_identity_is_opaque_utc_and_no_replace(tmp_path: Path):
    run = artifacts.create_historical_run(run_root=tmp_path, run_id="run-a", created_at_utc="2026-08-01T00:00:00Z")

    assert run.run_id == "run-a"
    assert run.created_at_utc == "2026-08-01T00:00:00Z"
    assert run.run_ref == "run-a"
    with pytest.raises(artifacts.HistoricalArtifactError, match="already exists"):
        artifacts.create_historical_run(run_root=tmp_path, run_id="run-a")
    with pytest.raises(artifacts.HistoricalArtifactError, match="path-safe"):
        artifacts.create_historical_run(run_root=tmp_path, run_id="../bad")
    with pytest.raises(artifacts.HistoricalArtifactError, match="timezone-aware UTC"):
        artifacts.create_historical_run(run_root=tmp_path, run_id="run-b", created_at_utc="2026-08-01T00:00:00")


def test_manifest_schema_exact_and_safe_relative_refs(tmp_path: Path):
    _, calendar_result, _, _ = _commit_roots(tmp_path)
    manifest = artifacts.load_historical_manifest(_manifest_ref(calendar_result, tmp_path), run_root=tmp_path)

    assert manifest["schema_version"] == artifacts.HISTORICAL_MANIFEST_SCHEMA_VERSION
    assert set(manifest) == artifacts.MANIFEST_FIELDS
    assert not Path(manifest["payload_ref"]).is_absolute()
    extra = dict(manifest)
    extra["account_id"] = "forbidden"
    with pytest.raises(artifacts.HistoricalArtifactError, match="schema exactly"):
        artifacts.validate_historical_manifest(extra, run_root=tmp_path)
    missing = dict(manifest)
    del missing["processing_engine_version"]
    with pytest.raises(artifacts.HistoricalArtifactError, match="schema exactly"):
        artifacts.validate_historical_manifest(missing, run_root=tmp_path)
    for bad_ref in (
        "../outside.json",
        "run-a\\calendar\\calendar-a.json",
        "C:/outside.json",
        "//server/share/file.json",
        "run-a/calendar/calendar-a.json:stream",
        "CON",
    ):
        changed = dict(manifest)
        changed["payload_ref"] = bad_ref
        with pytest.raises(artifacts.HistoricalArtifactError, match="safe relative path"):
            artifacts.validate_historical_manifest(changed, run_root=tmp_path)


def test_atomic_commit_complete_no_overwrite_and_corruption_failures(tmp_path: Path):
    _, calendar_result, _, _ = _commit_roots(tmp_path)
    manifest = calendar_result["manifest"]
    payload_path = calendar_result["payload_path"]
    manifest_path = calendar_result["manifest_path"]

    assert payload_path.exists()
    assert manifest_path.exists()
    assert artifacts.load_historical_manifest(_manifest_ref(calendar_result, tmp_path), run_root=tmp_path)["payload_sha256"] == artifacts.sha256_file(payload_path)
    with pytest.raises(artifacts.HistoricalArtifactError, match="already exists"):
        artifacts.commit_calendar_candidate_artifact(
            calendar=_fixture()[0],
            run_root=tmp_path,
            run_id="run-a",
            artifact_id="calendar-a",
        )

    (tmp_path / "run-a" / "calendar" / ".tmp-leftover.payload.tmp").write_text("{}", encoding="utf-8")
    artifacts.validate_historical_manifest_chain(manifest, run_root=tmp_path)
    payload_path.write_text("changed", encoding="utf-8")
    with pytest.raises(artifacts.HistoricalArtifactError, match="size mismatch|digest mismatch"):
        artifacts.validate_historical_manifest(manifest, run_root=tmp_path)


def test_payload_only_and_manifest_only_are_not_valid_artifacts(tmp_path: Path):
    artifacts.create_historical_run(run_root=tmp_path, run_id="run-a")
    payload_only = tmp_path / "run-a" / "calendar" / "orphan.json"
    payload_only.parent.mkdir(parents=True, exist_ok=True)
    payload_only.write_text("{}", encoding="utf-8")
    with pytest.raises(artifacts.HistoricalArtifactError, match="manifest is missing"):
        artifacts.load_historical_manifest("run-a/calendar/orphan.json.manifest.json", run_root=tmp_path)

    _, calendar_result, _, _ = _commit_roots(tmp_path / "complete")
    manifest = dict(calendar_result["manifest"])
    manifest["payload_ref"] = "run-a/calendar/missing.json"
    manifest_path = tmp_path / "run-a" / "calendar" / "missing.json.manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
    with pytest.raises(artifacts.HistoricalArtifactError, match="missing|regular file"):
        artifacts.load_historical_manifest("run-a/calendar/missing.json.manifest.json", run_root=tmp_path)


def test_calendar_candidate_payload_is_deterministic_and_not_frozen(tmp_path: Path):
    calendar = _fixture()[0]
    artifacts.create_historical_run(run_root=tmp_path, run_id="run-a")
    first = artifacts.commit_calendar_candidate_artifact(calendar=calendar, run_root=tmp_path, run_id="run-a", artifact_id="calendar-a")

    payload = artifacts.load_historical_payload(first["manifest"], run_root=tmp_path)
    assert payload["artifact_type"] == artifacts.ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE
    assert payload["requested_primary_listing_mic"] == "XNAS"
    assert payload["requested_calendar_token"] == "XNAS"
    assert payload["resolved_calendar"] == "XNYS"
    assert payload["calendar_status"] == fc.CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE
    assert "FROZEN" not in payload["artifact_type"]
    assert first["manifest"]["semantic_payload_digest"] == artifacts.semantic_digest(payload)


def test_normalized_source_artifact_serializes_exact_start_stamped_decimal_rows(tmp_path: Path):
    _, _, source_result, _ = _commit_roots(tmp_path)
    payload = artifacts.load_historical_payload(source_result["manifest"], run_root=tmp_path)

    assert payload["artifact_type"] == artifacts.ARTIFACT_TYPE_NORMALIZED_15M_OHLCV
    assert payload["provenance_classification"] == artifacts.SYNTHETIC_OFFLINE_FIXTURE
    assert payload["source_timestamp_semantic"] == rth.SOURCE_TIMESTAMP_SEMANTIC
    assert payload["records"][0]["window_start_utc"].endswith("Z")
    assert payload["records"][0]["window_end_utc"].endswith("Z")
    assert isinstance(payload["records"][0]["open"], str)
    assert payload["records"] == sorted(payload["records"], key=lambda item: item["window_start_utc"])
    with pytest.raises(artifacts.HistoricalArtifactError, match="chronological"):
        artifacts.normalized_source_payload(tuple(reversed(_fixture()[1])))
    with pytest.raises(artifacts.HistoricalArtifactError, match="synthetic"):
        artifacts.commit_normalized_15m_artifact(
            source_bars=_fixture()[1],
            run_root=tmp_path,
            run_id="run-a",
            provenance_classification="PROVIDER_ACQUIRED",
            artifact_id="source-provider",
        )


def test_dividend_event_artifact_is_explicit_offline_evidence(tmp_path: Path):
    _, _, _, dividend_result = _commit_roots(tmp_path)
    payload = artifacts.load_historical_payload(dividend_result["manifest"], run_root=tmp_path)

    assert payload["artifact_type"] == artifacts.ARTIFACT_TYPE_DIVIDEND_EVENT_SET
    assert payload["evidence_classification"] == artifacts.SYNTHETIC_OFFLINE_FIXTURE
    assert payload["event_set_semantic_digest"] == artifacts.semantic_digest(payload["events"])
    with pytest.raises(artifacts.HistoricalArtifactError, match="unique"):
        artifacts.dividend_event_set_payload(
            (
                artifacts.DividendEventRecord("DIV-A", "2024-01-03"),
                artifacts.DividendEventRecord("DIV-A", "2024-01-04"),
            )
        )


def test_derived_profile_artifacts_use_exact_multi_input_lineage_and_engine_digests(tmp_path: Path):
    _, calendar_result, source_result, _ = _commit_roots(tmp_path)
    swing = artifacts.commit_derived_profile_artifact(
        calendar_manifest_ref=_manifest_ref(calendar_result, tmp_path),
        source_manifest_ref=_manifest_ref(source_result, tmp_path),
        profile=rth.PROFILE_SWING,
        run_root=tmp_path,
        artifact_id="swing-a",
    )
    position = artifacts.commit_derived_profile_artifact(
        calendar_manifest_ref=_manifest_ref(calendar_result, tmp_path),
        source_manifest_ref=_manifest_ref(source_result, tmp_path),
        profile=rth.PROFILE_POSITION_SWING,
        run_root=tmp_path,
        artifact_id="position-a",
    )

    swing_payload = artifacts.load_historical_payload(swing["manifest"], run_root=tmp_path)
    position_payload = artifacts.load_historical_payload(position["manifest"], run_root=tmp_path)
    assert swing["manifest"]["primary_parent_artifact_id"] == "source-a"
    assert swing["manifest"]["input_artifact_ids"] == ["calendar-a"]
    assert swing_payload["profile"] == rth.PROFILE_SWING
    assert swing_payload["canonical_bar_type"] == rth.RTH_HALF_SESSION_195M
    assert swing_payload["produced_bar_count"] == 4
    assert swing_payload["extended_hours_exclusion_count"] == 1
    assert swing_payload["early_close_exclusion_count"] == 1
    assert position_payload["canonical_bar_type"] == rth.RTH_FULL_SESSION_1D
    assert position_payload["produced_bar_count"] == 2
    artifacts.validate_historical_manifest_chain(swing["manifest"], run_root=tmp_path)
    artifacts.validate_historical_manifest_chain(position["manifest"], run_root=tmp_path)


def test_wrong_run_duplicate_input_and_self_parent_lineage_are_rejected(tmp_path: Path):
    _, calendar_result, source_result, _ = _commit_roots(tmp_path)
    artifacts.create_historical_run(run_root=tmp_path, run_id="run-b")
    other = artifacts.commit_normalized_15m_artifact(
        source_bars=_fixture()[1],
        run_root=tmp_path,
        run_id="run-b",
        artifact_id="source-b",
    )

    with pytest.raises(artifacts.HistoricalArtifactError, match="cross-run"):
        artifacts.commit_derived_profile_artifact(
            calendar_manifest_ref=_manifest_ref(calendar_result, tmp_path),
            source_manifest_ref=_manifest_ref(other, tmp_path),
            profile=rth.PROFILE_SWING,
            run_root=tmp_path,
        )
    manifest = dict(source_result["manifest"])
    manifest["input_artifact_ids"] = ["calendar-a", "calendar-a"]
    manifest["input_manifest_refs"] = [_manifest_ref(calendar_result, tmp_path), _manifest_ref(calendar_result, tmp_path)]
    with pytest.raises(artifacts.HistoricalArtifactError, match="duplicate input"):
        artifacts.validate_historical_manifest(manifest, run_root=tmp_path)
    manifest = dict(source_result["manifest"])
    manifest["primary_parent_artifact_id"] = "source-a"
    with pytest.raises(artifacts.HistoricalArtifactError, match="own parent"):
        artifacts.validate_historical_manifest(manifest, run_root=tmp_path)


def test_incomplete_source_writes_blocked_derived_artifact_without_repair(tmp_path: Path):
    calendar, source_bars, _ = _fixture()
    incomplete = tuple(bar for index, bar in enumerate(source_bars) if index != 25)
    run = artifacts.create_historical_run(run_root=tmp_path, run_id="run-a")
    calendar_result = artifacts.commit_calendar_candidate_artifact(calendar=calendar, run_root=tmp_path, run_id=run.run_id, artifact_id="calendar-a")
    source_result = artifacts.commit_normalized_15m_artifact(source_bars=incomplete, run_root=tmp_path, run_id=run.run_id, artifact_id="source-a")

    derived = artifacts.commit_derived_profile_artifact(
        calendar_manifest_ref=_manifest_ref(calendar_result, tmp_path),
        source_manifest_ref=_manifest_ref(source_result, tmp_path),
        profile=rth.PROFILE_POSITION_SWING,
        run_root=tmp_path,
        artifact_id="position-a",
    )
    payload = artifacts.load_historical_payload(derived["manifest"], run_root=tmp_path)
    assert payload["derivation_status"] == rth.DERIVATION_BLOCKED
    assert payload["invalid_or_incomplete_session_count"] == 1
    assert payload["produced_bar_count"] == 1
    assert any("SESSION_SOURCE_INCOMPLETE" in finding for finding in payload["findings"])


def test_segment_map_uses_derived_profile_and_dividend_event_inputs(tmp_path: Path):
    _, calendar_result, source_result, dividend_result = _commit_roots(tmp_path)
    swing = artifacts.commit_derived_profile_artifact(
        calendar_manifest_ref=_manifest_ref(calendar_result, tmp_path),
        source_manifest_ref=_manifest_ref(source_result, tmp_path),
        profile=rth.PROFILE_SWING,
        run_root=tmp_path,
        artifact_id="swing-a",
    )
    segment = artifacts.commit_segment_map_artifact(
        derived_manifest_ref=_manifest_ref(swing, tmp_path),
        dividend_manifest_ref=_manifest_ref(dividend_result, tmp_path),
        calendar_manifest_ref=_manifest_ref(calendar_result, tmp_path),
        run_root=tmp_path,
        artifact_id="segments-a",
    )

    payload = artifacts.load_historical_payload(segment["manifest"], run_root=tmp_path)
    assert segment["manifest"]["primary_parent_artifact_id"] == "swing-a"
    assert segment["manifest"]["input_artifact_ids"] == ["dividends-a"]
    assert payload["profile"] == rth.PROFILE_SWING
    assert [item["start_reason"] for item in payload["segments"]] == [
        "DATASET_START",
        "EX_DIVIDEND_CONTINUITY_RESET",
    ]
    assert payload["segments"][1]["segment_start_session_date"] == "2024-01-04"
    assert payload["bar_assignment_count"] == 4
    artifacts.validate_historical_manifest_chain(segment["manifest"], run_root=tmp_path)


def test_segment_map_rejects_cross_profile_manifest_tampering(tmp_path: Path):
    _, calendar_result, source_result, dividend_result = _commit_roots(tmp_path)
    swing = artifacts.commit_derived_profile_artifact(
        calendar_manifest_ref=_manifest_ref(calendar_result, tmp_path),
        source_manifest_ref=_manifest_ref(source_result, tmp_path),
        profile=rth.PROFILE_SWING,
        run_root=tmp_path,
        artifact_id="swing-a",
    )
    manifest_path = swing["manifest_path"]
    tampered = dict(swing["manifest"])
    tampered["profile_id"] = rth.PROFILE_POSITION_SWING
    manifest_path.write_text(json.dumps(tampered, sort_keys=True), encoding="utf-8")

    with pytest.raises(artifacts.HistoricalArtifactError, match="profile mismatch"):
        artifacts.commit_segment_map_artifact(
            derived_manifest_ref=_manifest_ref(swing, tmp_path),
            dividend_manifest_ref=_manifest_ref(dividend_result, tmp_path),
            calendar_manifest_ref=_manifest_ref(calendar_result, tmp_path),
            run_root=tmp_path,
        )


def test_segment_map_rejects_wrong_calendar_context(tmp_path: Path):
    _, calendar_result, source_result, dividend_result = _commit_roots(tmp_path)
    other_calendar = _fixture()[0]
    other_result = artifacts.commit_calendar_candidate_artifact(
        calendar=fc.FrozenCalendar(
            schema_version=other_calendar.schema_version,
            contract_v2_1_digest=other_calendar.contract_v2_1_digest,
            requested_primary_listing_mic=other_calendar.requested_primary_listing_mic,
            requested_calendar_token=other_calendar.requested_calendar_token,
            resolved_calendar=other_calendar.resolved_calendar,
            calendar_alias_relationship=other_calendar.calendar_alias_relationship,
            exchange_calendars_version=other_calendar.exchange_calendars_version,
            tzdata_version=other_calendar.tzdata_version,
            fixed_start_date=other_calendar.fixed_start_date,
            fixed_end_date=other_calendar.fixed_end_date,
            source_timezone=other_calendar.source_timezone,
            canonical_timezone=other_calendar.canonical_timezone,
            official_exchange_evidence_identity="DIFFERENT_SYNTHETIC_EVIDENCE",
            official_exchange_evidence_digest="DIFFERENT_SYNTHETIC_DIGEST",
            status=other_calendar.status,
            sessions=other_calendar.sessions,
            semantic_digest=fc.semantic_digest({"different": "calendar"}),
        ),
        run_root=tmp_path,
        run_id="run-a",
        artifact_id="calendar-b",
    )
    swing = artifacts.commit_derived_profile_artifact(
        calendar_manifest_ref=_manifest_ref(calendar_result, tmp_path),
        source_manifest_ref=_manifest_ref(source_result, tmp_path),
        profile=rth.PROFILE_SWING,
        run_root=tmp_path,
        artifact_id="swing-a",
    )

    with pytest.raises(artifacts.HistoricalArtifactError, match="calendar artifact mismatch"):
        artifacts.commit_segment_map_artifact(
            derived_manifest_ref=_manifest_ref(swing, tmp_path),
            dividend_manifest_ref=_manifest_ref(dividend_result, tmp_path),
            calendar_manifest_ref=_manifest_ref(other_result, tmp_path),
            run_root=tmp_path,
        )


def test_pipeline_completes_and_writes_sanitized_receipt(tmp_path: Path):
    receipt = pipeline.run_offline_historical_pipeline(
        calendar=_fixture()[0],
        source_bars=_fixture()[1],
        dividend_events=_fixture()[2],
        run_root=tmp_path,
        run_id="run-a",
        artifact_id_factory=_ids(),
        created_at_utc="2026-08-01T00:00:00Z",
    )

    assert receipt["pipeline_status"] == artifacts.PIPELINE_COMPLETED
    assert receipt["swing_derivation_status"] == rth.DERIVATION_COMPLETE
    assert receipt["position_swing_derivation_status"] == rth.DERIVATION_COMPLETE
    assert receipt["segment_map_statuses"][rth.PROFILE_SWING] == "SEGMENT_MAP_WRITTEN"
    assert len(receipt["artifact_receipts"]) == 8
    rendered = json.dumps(receipt, sort_keys=True)
    assert "open" not in rendered
    assert str(tmp_path) not in rendered


def test_pipeline_partial_profile_failure_does_not_rollback_valid_profile(tmp_path: Path, monkeypatch):
    original = artifacts.commit_derived_profile_artifact

    def fail_position(**kwargs):
        if kwargs["profile"] == rth.PROFILE_POSITION_SWING:
            raise artifacts.HistoricalArtifactError("forced position failure")
        return original(**kwargs)

    monkeypatch.setattr(artifacts, "commit_derived_profile_artifact", fail_position)
    receipt = pipeline.run_offline_historical_pipeline(
        calendar=_fixture()[0],
        source_bars=_fixture()[1],
        dividend_events=_fixture()[2],
        run_root=tmp_path,
        run_id="run-a",
        artifact_id_factory=_ids(),
    )

    assert receipt["pipeline_status"] == artifacts.PIPELINE_PARTIAL
    assert receipt["swing_derivation_status"] == rth.DERIVATION_COMPLETE
    assert receipt["position_swing_derivation_status"] == "DERIVATION_ARTIFACT_BLOCKED"
    assert receipt["fixed_findings"] == ["POSITION_SWING:DERIVATION_ARTIFACT_BLOCKED"]
    assert "forced position failure" not in json.dumps(receipt, sort_keys=True)


def test_pipeline_blocks_on_invalid_normalized_source_without_derivation(tmp_path: Path):
    calendar, source_bars, dividends = _fixture()
    receipt = pipeline.run_offline_historical_pipeline(
        calendar=calendar,
        source_bars=tuple(reversed(source_bars)),
        dividend_events=dividends,
        run_root=tmp_path,
        run_id="run-a",
        artifact_id_factory=_ids(),
    )

    assert receipt["pipeline_status"] == artifacts.PIPELINE_BLOCKED
    assert receipt["normalized_source_status"] == "NORMALIZED_SOURCE_BLOCKED"
    assert receipt["swing_derivation_status"] == "DERIVATION_NOT_RUN"
    assert len(receipt["artifact_receipts"]) == 1
    assert receipt["fixed_findings"] == ["NORMALIZED_SOURCE_BLOCKED"]


def test_dry_cli_pipeline_self_check_is_sanitized_and_rejects_ticker_args():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--pipeline-self-check"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["status"] == "HISTORICAL_DATA_ARTIFACT_LINEAGE_SYNTHETIC_SELF_CHECK"
    assert receipt["pipeline_status"] == artifacts.PIPELINE_COMPLETED
    assert receipt["synthetic_only"] is True
    assert receipt["provider_execution_enabled"] is False
    assert "ticker" not in result.stdout.lower()
    blocked = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--pipeline-self-check", "--ticker", "AAPL"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert blocked.returncode != 0


def test_contract_digests_operational_lineage_and_runtime_boundaries_remain_unchanged():
    assert fdac.contract_digest(fdac.load_contract_toml(REPO_ROOT / "config" / "fixed_date_acquisition_contract.example.toml")) == V1_DIGEST
    assert acv2.contract_digest(acv2.default_contract()) == V2_DIGEST
    assert acv21.contract_digest(acv21.default_contract()) == V21_DIGEST
    assert artifacts.HISTORICAL_MANIFEST_SCHEMA_VERSION != "marketflow.artifact_manifest.v1"
    assert rth.RUNTIME_MIGRATION_PENDING == "LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION"


def test_historical_artifact_source_assurance_boundaries():
    package_files = [
        REPO_ROOT / "marketflow" / "historical_data" / "__init__.py",
        REPO_ROOT / "marketflow" / "historical_data" / "__main__.py",
        REPO_ROOT / "marketflow" / "historical_data" / "artifacts.py",
        REPO_ROOT / "marketflow" / "historical_data" / "pipeline.py",
    ]
    forbidden_modules = {
        "polygon",
        "requests",
        "httpx",
        "socket",
        "urllib",
        "yfinance",
        "openai",
        "streamlit",
        "marketflow.marketflow_data_provider",
        "marketflow.marketflow_polygon_tools",
        "marketflow.marketflow_strategy",
        "marketflow.services.monte_carlo_service",
        "marketflow.services.backtest_result_service",
        "marketflow.services.walk_forward_validation_service",
        "marketflow.backtesting.outcome_engine",
    }
    combined = ""
    for path in package_files:
        source = path.read_text(encoding="utf-8")
        combined += source
        tree = ast.parse(source)
        imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
        attrs = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        names = {node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
        assert forbidden_modules.isdisjoint(imported)
        assert forbidden_modules.isdisjoint(imported_from)
        assert "getenv" not in attrs
        assert "environ" not in attrs
        assert {"download", "request", "post", "put", "delete", "connect"}.isdisjoint(attrs)
        assert {"rank_long_candidates", "build_candidate_from_prefix", "evaluate_candidate_outcome"}.isdisjoint(names)
    assert "os.replace" not in combined
    assert "glob(" not in combined
    assert "provider_native_4h" not in combined
    assert "provider_native_1d" not in combined
    assert "SYNTHETIC_OFFLINE_FIXTURE" in combined
    assert "marketflow.historical_data_artifact_manifest.v1" in combined
