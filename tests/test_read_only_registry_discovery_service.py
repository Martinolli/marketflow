from __future__ import annotations

import csv
from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import read_only_registry_discovery_service as discovery


def _candidate(search_root: str | Path | None = None) -> dict:
    return discovery.build_read_only_registry_discovery_candidate_v1(search_root=search_root)


def _entry(candidate: dict, profile: str) -> dict:
    return next(item for item in candidate["registry_entries"] if item["dataset_profile"] == profile)


def _write_dataset(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(manifest))


def _swing_fixture_rows() -> list[dict]:
    return [
        {
            "ticker": "AAPL",
            "dataset_profile": "SWING",
            "dataset_bar_rule": "RTH_HALF_SESSION_195M",
            "session_date": "2022-01-03",
            "session_type": "FULL_ORDINARY_SESSION",
            "bar_number_in_session": 1,
            "bar_start_utc": "2022-01-03T14:30:00Z",
            "bar_end_utc": "2022-01-03T17:45:00Z",
            "bar_start_local": "2022-01-03T09:30:00-05:00",
            "bar_end_local": "2022-01-03T12:45:00-05:00",
            "open": "100",
            "high": "101",
            "low": "99",
            "close": "100.5",
            "volume": "1000",
            "transactions": 12,
            "vwap": None,
            "source_row_count": 13,
            "source_first_timestamp_utc": "2022-01-03T14:30:00Z",
            "source_last_timestamp_utc": "2022-01-03T17:30:00Z",
            "source_session_date": "2022-01-03",
            "source_timeframe": "15m",
        }
    ]


def _swing_fixture_manifest(rows_digest: str) -> dict:
    manifest = {
        "artifact_kind": "SWING_CANONICAL_DATASET_MANIFEST",
        "schema_version": "swing_canonical_dataset_manifest_v1",
        "dataset_profile": "SWING",
        "dataset_bar_rule": "RTH_HALF_SESSION_195M",
        "row_count": 1,
        "dataset_rows_digest": rows_digest,
        "source_normalized_source_rows_digest": "0" * 64,
        "canonical_dataset_frozen": False,
    }
    manifest["dataset_manifest_digest"] = discovery.swing_dataset.dataset_manifest_digest_v1(manifest)
    return manifest


def _write_matching_swing_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[str, str]:
    rows = _swing_fixture_rows()
    rows_digest = discovery.swing_dataset.dataset_rows_digest_v1(rows)
    manifest = _swing_fixture_manifest(rows_digest)
    monkeypatch.setattr(discovery.swing_registry, "EXPECTED_DATASET_ROWS_DIGEST", rows_digest)
    monkeypatch.setattr(
        discovery.swing_registry,
        "EXPECTED_DATASET_MANIFEST_DIGEST",
        manifest["dataset_manifest_digest"],
    )
    _write_dataset(tmp_path / discovery.SWING_EXPECTED_DATASET_PATH, rows)
    _write_manifest(tmp_path / discovery.SWING_EXPECTED_MANIFEST_PATH, manifest)
    return rows_digest, manifest["dataset_manifest_digest"]


def test_discovery_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(discovery.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_artifact_kind_is_read_only_registry_discovery_candidate():
    assert _candidate()["artifact_kind"] == discovery.ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE


def test_candidate_status_is_ready_or_requires_availability_verification(tmp_path: Path):
    ready = _candidate()
    missing = _candidate(tmp_path)

    assert ready["candidate_status"] in {
        discovery.READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW,
        discovery.READ_ONLY_REGISTRY_DISCOVERY_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION,
    }
    assert missing["candidate_status"] == discovery.READ_ONLY_REGISTRY_DISCOVERY_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION


def test_swing_registry_entry_is_discovered():
    entry = _entry(_candidate(), "SWING")

    assert entry["registry_key"] == discovery.swing_registry.PROPOSED_REGISTRY_KEY


def test_position_swing_registry_entry_is_discovered():
    entry = _entry(_candidate(), "POSITION_SWING")

    assert entry["registry_key"] == discovery.position_registry.PROPOSED_REGISTRY_KEY


def test_registry_entry_count_is_two():
    assert _candidate()["candidate_summary"]["registry_entry_count"] == 2


def test_registry_scopes_are_research_dataset():
    assert {entry["registry_scope"] for entry in _candidate()["registry_entries"]} == {"RESEARCH_DATASET"}


def test_runtime_use_remains_not_authorized():
    candidate = _candidate()

    assert candidate["runtime_use"] == discovery.NOT_AUTHORIZED
    assert {entry["runtime_use"] for entry in candidate["registry_entries"]} == {discovery.NOT_AUTHORIZED}


def test_strategy_use_remains_not_authorized():
    candidate = _candidate()

    assert candidate["strategy_use"] == discovery.NOT_AUTHORIZED
    assert {entry["strategy_use"] for entry in candidate["registry_entries"]} == {discovery.NOT_AUTHORIZED}


def test_paper_trading_remains_not_authorized():
    assert _candidate()["paper_trading"] == discovery.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _candidate()["broker_execution"] == discovery.NOT_AUTHORIZED


def test_runtime_migration_approved_remains_false():
    assert _candidate()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _candidate()["runtime_migration_active"] is False


def test_strategy_runtime_migration_remains_false():
    assert _candidate()["strategy_runtime_migration"] is False


def test_automatic_stitching_remains_false():
    assert _candidate()["automatic_stitching"] is False


def test_predictive_usefulness_remains_not_accepted():
    assert _candidate()["predictive_usefulness"] == discovery.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED


def test_profitability_remains_not_accepted():
    assert _candidate()["profitability"] == discovery.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_missing_dataset_file_is_reported_without_fabrication(tmp_path: Path):
    candidate = _candidate(tmp_path)

    assert candidate["candidate_status"] == discovery.READ_ONLY_REGISTRY_DISCOVERY_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION
    assert {entry["dataset_file_status"] for entry in candidate["registry_entries"]} == {
        discovery.MISSING_LOCAL_DATASET_FILE
    }
    assert {entry["dataset_digest_verified"] for entry in candidate["registry_entries"]} == {None}


def test_existing_dataset_and_manifest_files_report_available(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_matching_swing_fixture(tmp_path, monkeypatch)

    entry = _entry(_candidate(tmp_path), "SWING")

    assert entry["dataset_file_status"] == discovery.AVAILABLE_DIGEST_VERIFIED
    assert entry["manifest_file_status"] == discovery.AVAILABLE_DIGEST_VERIFIED


def test_digest_verification_passes_for_fixture_file_when_expected_digest_matches(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    rows_digest, manifest_digest = _write_matching_swing_fixture(tmp_path, monkeypatch)

    entry = _entry(_candidate(tmp_path), "SWING")

    assert entry["dataset_digest_verified"] is True
    assert entry["manifest_digest_verified"] is True
    assert entry["actual_dataset_rows_digest"] == rows_digest
    assert entry["actual_dataset_manifest_digest"] == manifest_digest


def test_digest_mismatch_is_reported_without_approving_runtime_use(tmp_path: Path):
    rows = _swing_fixture_rows()
    rows[0]["close"] = "999"
    manifest = _swing_fixture_manifest(discovery.swing_registry.EXPECTED_DATASET_ROWS_DIGEST)
    _write_dataset(tmp_path / discovery.SWING_EXPECTED_DATASET_PATH, rows)
    _write_manifest(tmp_path / discovery.SWING_EXPECTED_MANIFEST_PATH, manifest)

    candidate = _candidate(tmp_path)
    entry = _entry(candidate, "SWING")

    assert entry["dataset_file_status"] == discovery.AVAILABLE_DIGEST_MISMATCH
    assert entry["dataset_digest_verified"] is False
    assert candidate["runtime_use"] == discovery.NOT_AUTHORIZED
    assert candidate["runtime_migration_approved"] is False


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _candidate()["candidate_checklist"]] == discovery.REQUIRED_CHECK_IDS


def test_all_boundary_checks_pass_for_accepted_discovery_candidate():
    assert {item["status"] for item in _candidate()["candidate_checklist"]} == {discovery.PASS}


def test_candidate_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["read_only_registry_discovery_candidate_digest"] == second[
        "read_only_registry_discovery_candidate_digest"
    ]
    assert first["read_only_registry_discovery_candidate_digest"] == discovery.read_only_registry_discovery_candidate_digest_v1(first)


def test_validator_accepts_valid_candidate():
    validation = discovery.validate_read_only_registry_discovery_candidate_v1(_candidate())

    assert validation["status"] == "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_VALID"
    assert validation["registry_entry_count"] == 2
    assert validation["runtime_migration_approved"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("provider_requests_made", True, "provider_requests_made"),
        ("read_only_discovery", False, "read_only_discovery"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("automatic_stitching", True, "automatic_stitching"),
    ],
)
def test_validator_rejects_forbidden_boundary_mutations(field: str, value, match: str):
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match=match):
        discovery.validate_read_only_registry_discovery_candidate_v1(candidate)


def test_validator_rejects_predictive_and_profitability_accepted():
    for field in ("predictive_usefulness", "profitability"):
        candidate = _candidate()
        candidate[field] = "accepted"

        with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match=field):
            discovery.validate_read_only_registry_discovery_candidate_v1(candidate)


def test_validator_rejects_missing_swing_registry_entry():
    candidate = _candidate()
    position_entry = deepcopy(_entry(candidate, "POSITION_SWING"))
    candidate["registry_entries"] = [position_entry, deepcopy(position_entry)]

    with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match="missing SWING"):
        discovery.validate_read_only_registry_discovery_candidate_v1(candidate)


def test_validator_rejects_missing_position_swing_registry_entry():
    candidate = _candidate()
    swing_entry = deepcopy(_entry(candidate, "SWING"))
    candidate["registry_entries"] = [swing_entry, deepcopy(swing_entry)]

    with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match="missing POSITION_SWING"):
        discovery.validate_read_only_registry_discovery_candidate_v1(candidate)


def test_validator_rejects_wrong_artifact_kind():
    candidate = _candidate()
    candidate["artifact_kind"] = "WRONG"

    with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match="artifact_kind"):
        discovery.validate_read_only_registry_discovery_candidate_v1(candidate)


def test_validator_rejects_registry_scope_not_research_dataset():
    candidate = _candidate()
    candidate["registry_entries"] = deepcopy(candidate["registry_entries"])
    candidate["registry_entries"][0]["registry_scope"] = "RUNTIME_DATASET"

    with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match="registry_scope"):
        discovery.validate_read_only_registry_discovery_candidate_v1(candidate)


def test_validator_rejects_missing_runtime_migration_plan_digest():
    candidate = _candidate()
    candidate["runtime_migration_plan_digest"] = None

    with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match="runtime_migration_plan_digest"):
        discovery.validate_read_only_registry_discovery_candidate_v1(candidate)


def test_validator_rejects_missing_runtime_review_package_digest():
    candidate = _candidate()
    candidate["runtime_migration_review_package_digest"] = None

    with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match="runtime_migration_review_package_digest"):
        discovery.validate_read_only_registry_discovery_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("read_only_registry_discovery_candidate_digest")

    with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match="read_only_registry_discovery_candidate_digest"):
        discovery.validate_read_only_registry_discovery_candidate_v1(candidate)


def test_markdown_writer_includes_required_sections():
    markdown = discovery.build_read_only_registry_discovery_candidate_markdown_v1(_candidate())

    for section in (
        "## Title",
        "## Purpose",
        "## Discovered Research Registry Entries",
        "## Local Dataset File Availability",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown
    assert "Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`." in markdown


def test_write_discovery_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = discovery.write_read_only_registry_discovery_candidate_v1(tmp_path, search_root=tmp_path)

    assert result["artifact_kind"] == discovery.ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE
    assert result["payload_sha256"]
    with pytest.raises(discovery.ReadOnlyRegistryDiscoveryError, match="already exists"):
        discovery.write_read_only_registry_discovery_candidate_v1(tmp_path, search_root=tmp_path)


def test_read_only_registry_discovery_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE
        == "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE"
    )
    assert (
        services.READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW
        == "READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW"
    )
    assert (
        services.READ_ONLY_REGISTRY_DISCOVERY_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION
        == "READ_ONLY_REGISTRY_DISCOVERY_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION"
    )
    assert services.build_read_only_registry_discovery_candidate_v1 is discovery.build_read_only_registry_discovery_candidate_v1
    assert services.discover_research_registry_entries_v1 is discovery.discover_research_registry_entries_v1
    assert services.validate_read_only_registry_discovery_candidate_v1 is discovery.validate_read_only_registry_discovery_candidate_v1
    assert services.write_read_only_registry_discovery_candidate_v1 is discovery.write_read_only_registry_discovery_candidate_v1
    assert (
        services.build_read_only_registry_discovery_candidate_markdown_v1
        is discovery.build_read_only_registry_discovery_candidate_markdown_v1
    )
