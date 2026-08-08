from __future__ import annotations

import csv
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import dataset_file_availability_verification_service as verification


def _package(search_root: str | Path | None = None) -> dict:
    return verification.build_dataset_file_availability_verification_package_v1(search_root=search_root)


def _entry(package: dict, profile: str) -> dict:
    return next(item for item in package["verification_entries"] if item["dataset_profile"] == profile)


def _row(profile: str, rule: str) -> dict:
    return {
        "ticker": "AAPL",
        "dataset_profile": profile,
        "dataset_bar_rule": rule,
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


def _manifest(profile: str, rule: str, rows_digest: str) -> dict:
    schema = (
        "swing_canonical_dataset_manifest_v1"
        if profile == "SWING"
        else "position_swing_canonical_dataset_manifest_v1"
    )
    artifact_kind = (
        "SWING_CANONICAL_DATASET_MANIFEST"
        if profile == "SWING"
        else "POSITION_SWING_CANONICAL_DATASET_MANIFEST"
    )
    manifest = {
        "artifact_kind": artifact_kind,
        "schema_version": schema,
        "dataset_profile": profile,
        "dataset_bar_rule": rule,
        "row_count": 1,
        "dataset_rows_digest": rows_digest,
        "source_normalized_source_rows_digest": "0" * 64,
        "canonical_dataset_frozen": False,
    }
    digest_fn = (
        verification.discovery.swing_dataset.dataset_manifest_digest_v1
        if profile == "SWING"
        else verification.discovery.position_dataset.dataset_manifest_digest_v1
    )
    manifest["dataset_manifest_digest"] = digest_fn(manifest)
    return manifest


def _write_dataset(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(manifest))


def _write_valid_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for definition in verification.discovery._registry_definitions():
        profile = definition["dataset_profile"]
        rows = [_row(profile, definition["dataset_bar_rule"])]
        digest_fn = (
            verification.discovery.swing_dataset.dataset_rows_digest_v1
            if profile == "SWING"
            else verification.discovery.position_dataset.dataset_rows_digest_v1
        )
        rows_digest = digest_fn(rows)
        manifest = _manifest(profile, definition["dataset_bar_rule"], rows_digest)
        if profile == "SWING":
            monkeypatch.setattr(verification.discovery.swing_registry, "EXPECTED_DATASET_ROWS_DIGEST", rows_digest)
            monkeypatch.setattr(
                verification.discovery.swing_registry,
                "EXPECTED_DATASET_MANIFEST_DIGEST",
                manifest["dataset_manifest_digest"],
            )
        else:
            monkeypatch.setattr(verification.discovery.position_registry, "EXPECTED_DATASET_ROWS_DIGEST", rows_digest)
            monkeypatch.setattr(
                verification.discovery.position_registry,
                "EXPECTED_DATASET_MANIFEST_DIGEST",
                manifest["dataset_manifest_digest"],
            )
        _write_dataset(tmp_path / definition["expected_dataset_path"], rows)
        _write_manifest(tmp_path / definition["expected_manifest_path"], manifest)
        result[profile] = {
            "rows_digest": rows_digest,
            "manifest_digest": manifest["dataset_manifest_digest"],
        }
    return result


def test_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(verification.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made"] is False


def test_artifact_kind_is_dataset_file_availability_verification_package():
    assert (
        _package()["artifact_kind"]
        == verification.ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE
    )


def test_package_status_ready_when_fixture_files_exist_and_digests_match(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_valid_fixture(tmp_path, monkeypatch)

    assert (
        _package(tmp_path)["package_status"]
        == verification.DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW
    )


def test_package_status_blocked_when_dataset_file_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_valid_fixture(tmp_path, monkeypatch)
    (tmp_path / verification.discovery.SWING_EXPECTED_DATASET_PATH).unlink()

    package = _package(tmp_path)

    assert package["package_status"] == verification.DATASET_FILE_AVAILABILITY_VERIFICATION_BLOCKED
    assert _entry(package, "SWING")["file_availability_status"] == verification.MISSING_DATASET_FILE


def test_package_status_blocked_when_manifest_file_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_valid_fixture(tmp_path, monkeypatch)
    (tmp_path / verification.discovery.SWING_EXPECTED_MANIFEST_PATH).unlink()

    package = _package(tmp_path)

    assert package["package_status"] == verification.DATASET_FILE_AVAILABILITY_VERIFICATION_BLOCKED
    assert _entry(package, "SWING")["file_availability_status"] == verification.MISSING_MANIFEST_FILE


def test_package_status_blocked_when_dataset_digest_mismatches(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_valid_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(verification.discovery.swing_registry, "EXPECTED_DATASET_ROWS_DIGEST", "0" * 64)

    package = _package(tmp_path)

    assert package["package_status"] == verification.DATASET_FILE_AVAILABILITY_VERIFICATION_BLOCKED
    assert _entry(package, "SWING")["file_availability_status"] == verification.DATASET_DIGEST_MISMATCH


def test_package_status_blocked_when_manifest_digest_mismatches(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_valid_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(verification.discovery.swing_registry, "EXPECTED_DATASET_MANIFEST_DIGEST", "0" * 64)

    package = _package(tmp_path)

    assert package["package_status"] == verification.DATASET_FILE_AVAILABILITY_VERIFICATION_BLOCKED
    assert _entry(package, "SWING")["file_availability_status"] == verification.MANIFEST_DIGEST_MISMATCH


def test_verification_entry_count_is_two():
    assert _package()["verification_summary"]["verification_entry_count"] == 2


def test_swing_verification_entry_exists():
    assert _entry(_package(), "SWING")["registry_key"] == verification.discovery.swing_registry.PROPOSED_REGISTRY_KEY


def test_position_swing_verification_entry_exists():
    assert (
        _entry(_package(), "POSITION_SWING")["registry_key"]
        == verification.discovery.position_registry.PROPOSED_REGISTRY_KEY
    )


def test_dataset_file_sha256_is_computed():
    assert _entry(_package(), "SWING")["dataset_file_sha256"]


def test_manifest_file_sha256_is_computed():
    assert _entry(_package(), "SWING")["manifest_file_sha256"]


def test_runtime_use_remains_not_authorized():
    assert _package()["runtime_use"] == verification.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _package()["strategy_use"] == verification.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _package()["paper_trading"] == verification.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _package()["broker_execution"] == verification.NOT_AUTHORIZED


def test_runtime_migration_approved_remains_false():
    assert _package()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _package()["runtime_migration_active"] is False


def test_strategy_runtime_migration_remains_false():
    assert _package()["strategy_runtime_migration"] is False


def test_automatic_stitching_remains_false():
    assert _package()["automatic_stitching"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    package = _package()

    assert package["predictive_usefulness"] == verification.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert package["profitability"] == verification.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _package()["verification_checklist"]] == verification.REQUIRED_CHECK_IDS


def test_all_checks_pass_for_valid_available_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_valid_fixture(tmp_path, monkeypatch)

    assert {item["status"] for item in _package(tmp_path)["verification_checklist"]} == {verification.PASS}


def test_checklist_includes_blockers_for_missing_or_mismatched_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_valid_fixture(tmp_path, monkeypatch)
    (tmp_path / verification.discovery.SWING_EXPECTED_DATASET_PATH).unlink()

    failed = [item for item in _package(tmp_path)["verification_checklist"] if item["status"] == verification.FAIL]

    assert failed
    assert {item["severity"] for item in failed} == {verification.BLOCKER}


def test_package_digest_is_deterministic():
    first = _package()
    second = _package()

    assert first["dataset_file_availability_verification_package_digest"] == second[
        "dataset_file_availability_verification_package_digest"
    ]
    assert (
        first["dataset_file_availability_verification_package_digest"]
        == verification.dataset_file_availability_verification_package_digest_v1(first)
    )


def test_validator_accepts_valid_package():
    validation = verification.validate_dataset_file_availability_verification_package_v1(_package())

    assert validation["status"] == "DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_VALID"
    assert validation["runtime_migration_approved"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("provider_requests_made", True, "provider_requests_made"),
        ("file_system_verification_performed", False, "file_system_verification_performed"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
    ],
)
def test_validator_rejects_forbidden_boundary_mutations(field: str, value, match: str):
    package = _package()
    package[field] = value

    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match=match):
        verification.validate_dataset_file_availability_verification_package_v1(package)


def test_validator_rejects_predictive_and_profitability_accepted():
    for field in ("predictive_usefulness", "profitability"):
        package = _package()
        package[field] = "accepted"

        with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match=field):
            verification.validate_dataset_file_availability_verification_package_v1(package)


def test_validator_rejects_ready_status_with_missing_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_valid_fixture(tmp_path, monkeypatch)
    (tmp_path / verification.discovery.SWING_EXPECTED_DATASET_PATH).unlink()
    package = _package(tmp_path)
    package["package_status"] = verification.DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW

    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match="package_status"):
        verification.validate_dataset_file_availability_verification_package_v1(package)


def test_validator_rejects_ready_status_with_digest_mismatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _write_valid_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(verification.discovery.swing_registry, "EXPECTED_DATASET_ROWS_DIGEST", "0" * 64)
    package = _package(tmp_path)
    package["package_status"] = verification.DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW

    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match="package_status"):
        verification.validate_dataset_file_availability_verification_package_v1(package)


def test_validator_rejects_wrong_artifact_kind():
    package = _package()
    package["artifact_kind"] = "WRONG"

    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match="artifact_kind"):
        verification.validate_dataset_file_availability_verification_package_v1(package)


def test_validator_rejects_verification_entry_count_not_two():
    package = _package()
    package["verification_entries"] = package["verification_entries"][:1]

    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match="verification entry count"):
        verification.validate_dataset_file_availability_verification_package_v1(package)


def test_validator_rejects_missing_swing_verification_entry():
    package = _package()
    position_entry = _entry(package, "POSITION_SWING")
    package["verification_entries"] = [position_entry, dict(position_entry)]

    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match="missing SWING"):
        verification.validate_dataset_file_availability_verification_package_v1(package)


def test_validator_rejects_missing_position_swing_verification_entry():
    package = _package()
    swing_entry = _entry(package, "SWING")
    package["verification_entries"] = [swing_entry, dict(swing_entry)]

    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match="missing POSITION_SWING"):
        verification.validate_dataset_file_availability_verification_package_v1(package)


def test_validator_rejects_missing_read_only_discovery_review_digest():
    package = _package()
    package["read_only_discovery_review_package_digest"] = None

    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match="read_only_discovery_review_package_digest"):
        verification.validate_dataset_file_availability_verification_package_v1(package)


def test_validator_rejects_missing_package_digest():
    package = _package()
    package.pop("dataset_file_availability_verification_package_digest")

    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match="dataset_file_availability_verification_package_digest"):
        verification.validate_dataset_file_availability_verification_package_v1(package)


def test_markdown_writer_includes_required_sections():
    markdown = verification.build_dataset_file_availability_verification_markdown_v1(_package())

    for section in (
        "## Title",
        "## Purpose",
        "## Verified Dataset Files",
        "## Digest Verification",
        "## Availability Summary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown
    assert "Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`." in markdown


def test_write_package_writes_json_without_overwrite(tmp_path: Path):
    result = verification.write_dataset_file_availability_verification_package_v1(tmp_path, search_root=tmp_path)

    assert result["artifact_kind"] == verification.ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE
    assert result["payload_sha256"]
    with pytest.raises(verification.DatasetFileAvailabilityVerificationError, match="already exists"):
        verification.write_dataset_file_availability_verification_package_v1(tmp_path, search_root=tmp_path)


def test_dataset_file_availability_verification_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE
        == "DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE"
    )
    assert (
        services.DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW
        == "DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW"
    )
    assert services.build_dataset_file_availability_verification_package_v1 is verification.build_dataset_file_availability_verification_package_v1
    assert services.verify_research_dataset_files_v1 is verification.verify_research_dataset_files_v1
    assert services.validate_dataset_file_availability_verification_package_v1 is verification.validate_dataset_file_availability_verification_package_v1
    assert services.write_dataset_file_availability_verification_package_v1 is verification.write_dataset_file_availability_verification_package_v1
    assert services.build_dataset_file_availability_verification_markdown_v1 is verification.build_dataset_file_availability_verification_markdown_v1
