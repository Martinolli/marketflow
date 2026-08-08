"""Offline dataset file availability verification for approved research datasets."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes, sha256_file
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import read_only_registry_discovery_operator_review_service as discovery_review
from marketflow.services import read_only_registry_discovery_service as discovery


ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE = (
    "DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE"
)
SCHEMA_VERSION_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_V1 = (
    "dataset_file_availability_verification_package_v1"
)
DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW = (
    "DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW"
)
DATASET_FILE_AVAILABILITY_VERIFICATION_BLOCKED = "DATASET_FILE_AVAILABILITY_VERIFICATION_BLOCKED"

AVAILABLE_AND_DIGEST_VERIFIED = "AVAILABLE_AND_DIGEST_VERIFIED"
MISSING_DATASET_FILE = "MISSING_DATASET_FILE"
MISSING_MANIFEST_FILE = "MISSING_MANIFEST_FILE"
DATASET_DIGEST_MISMATCH = "DATASET_DIGEST_MISMATCH"
MANIFEST_DIGEST_MISMATCH = "MANIFEST_DIGEST_MISMATCH"
VERIFICATION_BLOCKED = "VERIFICATION_BLOCKED"

EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST = (
    discovery_review.EXPECTED_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_DIGEST
)
EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST = (
    "299eb78d52e598e690db501b10ea88390ff6848a217640022e56251c41584021"
)
NOT_AUTHORIZED = discovery.NOT_AUTHORIZED

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "read_only_discovery_candidate_digest_bound",
    "read_only_discovery_review_package_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "verification_entry_count_two",
    "swing_dataset_file_exists",
    "swing_manifest_file_exists",
    "position_swing_dataset_file_exists",
    "position_swing_manifest_file_exists",
    "swing_dataset_digest_matches",
    "swing_manifest_digest_matches",
    "position_swing_dataset_digest_matches",
    "position_swing_manifest_digest_matches",
    "missing_file_count_zero",
    "digest_mismatch_count_zero",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "provider_requests_made_false",
]

REMAINING_REQUIRED_TASKS = [
    "Dataset file availability verification operator review package.",
    "Research-only applicability campaign plan.",
    "Research-only applicability campaign execution.",
]


class DatasetFileAvailabilityVerificationError(ValueError):
    """Raised when a dataset file availability package violates guardrails."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
    message: str | None = None,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": message or (f"{check_id} passed" if status == PASS else f"{check_id} failed"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise DatasetFileAvailabilityVerificationError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise DatasetFileAvailabilityVerificationError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise DatasetFileAvailabilityVerificationError(f"{field_name} must be true")


def _package_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE,
        "schema_version": SCHEMA_VERSION_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_V1,
        "created_offline": True,
        "provider_requests_made": False,
        "file_system_verification_performed": True,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "operator_review_required": True,
        "read_only_discovery_candidate_digest": EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST,
        "read_only_discovery_review_package_digest": EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST,
    }


def _resolve_search_root(search_root: str | Path | None) -> Path:
    return Path("." if search_root is None else search_root)


def _file_status(
    *,
    dataset_exists: bool,
    manifest_exists: bool,
    dataset_digest_match: bool | None,
    manifest_digest_match: bool | None,
) -> str:
    if not dataset_exists:
        return MISSING_DATASET_FILE
    if not manifest_exists:
        return MISSING_MANIFEST_FILE
    if dataset_digest_match is not True:
        return DATASET_DIGEST_MISMATCH
    if manifest_digest_match is not True:
        return MANIFEST_DIGEST_MISMATCH
    return AVAILABLE_AND_DIGEST_VERIFIED


def _verify_entry(definition: dict[str, Any], *, search_root: Path) -> dict[str, Any]:
    dataset_path = search_root / definition["expected_dataset_path"]
    manifest_path = search_root / definition["expected_manifest_path"]
    dataset_exists = dataset_path.exists() and dataset_path.is_file()
    manifest_exists = manifest_path.exists() and manifest_path.is_file()

    dataset_rows_digest_actual = None
    dataset_manifest_digest_actual = None
    dataset_rows_digest_match: bool | None = None
    dataset_manifest_digest_match: bool | None = None
    dataset_file_sha256 = None
    manifest_file_sha256 = None
    dataset_file_size_bytes = None
    manifest_file_size_bytes = None

    if dataset_exists:
        rows = discovery._read_csv_rows(dataset_path)
        dataset_rows_digest_actual = discovery._dataset_digest_for_entry(definition, rows)
        dataset_rows_digest_match = dataset_rows_digest_actual == definition["dataset_rows_digest"]
        dataset_file_sha256 = sha256_file(dataset_path)
        dataset_file_size_bytes = dataset_path.stat().st_size

    if manifest_exists:
        manifest = discovery._read_manifest(manifest_path)
        dataset_manifest_digest_actual = discovery._manifest_digest_for_entry(definition, manifest)
        dataset_manifest_digest_match = dataset_manifest_digest_actual == definition["dataset_manifest_digest"]
        manifest_file_sha256 = sha256_file(manifest_path)
        manifest_file_size_bytes = manifest_path.stat().st_size

    file_availability_status = _file_status(
        dataset_exists=dataset_exists,
        manifest_exists=manifest_exists,
        dataset_digest_match=dataset_rows_digest_match,
        manifest_digest_match=dataset_manifest_digest_match,
    )
    return {
        "registry_key": definition["registry_key"],
        "dataset_profile": definition["dataset_profile"],
        "dataset_bar_rule": definition["dataset_bar_rule"],
        "dataset_path": definition["expected_dataset_path"],
        "manifest_path": definition["expected_manifest_path"],
        "registry_approval_digest": definition["registry_approval_digest"],
        "dataset_file_exists": dataset_exists,
        "manifest_file_exists": manifest_exists,
        "dataset_rows_digest_expected": definition["dataset_rows_digest"],
        "dataset_rows_digest_actual": dataset_rows_digest_actual,
        "dataset_rows_digest_match": dataset_rows_digest_match,
        "dataset_manifest_digest_expected": definition["dataset_manifest_digest"],
        "dataset_manifest_digest_actual": dataset_manifest_digest_actual,
        "dataset_manifest_digest_match": dataset_manifest_digest_match,
        "dataset_file_sha256": dataset_file_sha256,
        "manifest_file_sha256": manifest_file_sha256,
        "dataset_file_size_bytes": dataset_file_size_bytes,
        "manifest_file_size_bytes": manifest_file_size_bytes,
        "file_availability_status": file_availability_status,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
    }


def verify_research_dataset_files_v1(
    *,
    search_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Verify local research dataset files without fetching or regenerating data."""
    root = _resolve_search_root(search_root)
    return [_verify_entry(definition, search_root=root) for definition in discovery._registry_definitions()]


def _summary(entries: list[dict[str, Any]], checklist: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    dataset_files_available_count = sum(1 for entry in entries if entry.get("dataset_file_exists") is True)
    manifest_files_available_count = sum(1 for entry in entries if entry.get("manifest_file_exists") is True)
    dataset_digests_verified_count = sum(1 for entry in entries if entry.get("dataset_rows_digest_match") is True)
    manifest_digests_verified_count = sum(1 for entry in entries if entry.get("dataset_manifest_digest_match") is True)
    missing_file_count = sum(
        1
        for entry in entries
        for field in ("dataset_file_exists", "manifest_file_exists")
        if entry.get(field) is not True
    )
    digest_mismatch_count = sum(
        1
        for entry in entries
        for field in ("dataset_rows_digest_match", "dataset_manifest_digest_match")
        if entry.get(field) is False
    )
    total = len(checklist or [])
    passed = sum(1 for item in checklist or [] if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(1 for item in checklist or [] if item.get("status") == FAIL and item.get("severity") == BLOCKER)
    ready_for_research_campaign_planning = (
        len(entries) == 2
        and dataset_files_available_count == 2
        and manifest_files_available_count == 2
        and dataset_digests_verified_count == 2
        and manifest_digests_verified_count == 2
        and missing_file_count == 0
        and digest_mismatch_count == 0
    )
    return {
        "verification_entry_count": len(entries),
        "dataset_files_available_count": dataset_files_available_count,
        "manifest_files_available_count": manifest_files_available_count,
        "dataset_digests_verified_count": dataset_digests_verified_count,
        "manifest_digests_verified_count": manifest_digests_verified_count,
        "missing_file_count": missing_file_count,
        "digest_mismatch_count": digest_mismatch_count,
        "ready_for_research_campaign_planning": ready_for_research_campaign_planning,
        "ready_for_runtime_migration": False,
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_review": failed == 0,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _package_status(entries: list[dict[str, Any]]) -> str:
    summary = _summary(entries)
    if summary["ready_for_research_campaign_planning"]:
        return DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW
    return DATASET_FILE_AVAILABILITY_VERIFICATION_BLOCKED


def _entry_by_profile(package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        entry.get("dataset_profile"): entry
        for entry in package.get("verification_entries") or []
        if isinstance(entry, dict)
    }


def _build_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    by_profile = _entry_by_profile(package)
    swing_entry = by_profile.get("SWING") or {}
    position_entry = by_profile.get("POSITION_SWING") or {}
    summary = _summary(package.get("verification_entries") or [])
    return [
        _check("read_only_discovery_candidate_digest_bound", EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST, package.get("read_only_discovery_candidate_digest")),
        _check("read_only_discovery_review_package_digest_bound", EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST, package.get("read_only_discovery_review_package_digest")),
        _check("swing_registry_approval_digest_bound", discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, swing_entry.get("registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, position_entry.get("registry_approval_digest")),
        _check("verification_entry_count_two", 2, summary["verification_entry_count"]),
        _check("swing_dataset_file_exists", True, swing_entry.get("dataset_file_exists")),
        _check("swing_manifest_file_exists", True, swing_entry.get("manifest_file_exists")),
        _check("position_swing_dataset_file_exists", True, position_entry.get("dataset_file_exists")),
        _check("position_swing_manifest_file_exists", True, position_entry.get("manifest_file_exists")),
        _check("swing_dataset_digest_matches", True, swing_entry.get("dataset_rows_digest_match")),
        _check("swing_manifest_digest_matches", True, swing_entry.get("dataset_manifest_digest_match")),
        _check("position_swing_dataset_digest_matches", True, position_entry.get("dataset_rows_digest_match")),
        _check("position_swing_manifest_digest_matches", True, position_entry.get("dataset_manifest_digest_match")),
        _check("missing_file_count_zero", 0, summary["missing_file_count"]),
        _check("digest_mismatch_count_zero", 0, summary["digest_mismatch_count"]),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        _check("runtime_migration_approved_false", False, package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, package.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, package.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, package.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, package.get("profitability"), severity=INFO),
        _check("provider_requests_made_false", False, package.get("provider_requests_made")),
    ]


def _digest_payload(package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(package)
    payload.pop("dataset_file_availability_verification_package_digest", None)
    return payload


def dataset_file_availability_verification_package_digest_v1(package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a dataset availability package."""
    return semantic_digest(_digest_payload(package))


def build_dataset_file_availability_verification_package_v1(
    *,
    search_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build an offline verification package for local research dataset files."""
    entries = verify_research_dataset_files_v1(search_root=search_root)
    package = {
        **_package_context(),
        "package_status": _package_status(entries),
        "verification_entries": entries,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _build_checklist(package)
    package["verification_checklist"] = checklist
    package["verification_summary"] = _summary(entries, checklist)
    package["dataset_file_availability_verification_package_digest"] = (
        dataset_file_availability_verification_package_digest_v1(package)
    )
    validate_dataset_file_availability_verification_package_v1(package)
    return package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise DatasetFileAvailabilityVerificationError(f"{current_path} must not emit {value}")
        if key in {
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
        } and value is True:
            raise DatasetFileAvailabilityVerificationError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise DatasetFileAvailabilityVerificationError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise DatasetFileAvailabilityVerificationError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_entries(package: dict[str, Any]) -> None:
    entries = package.get("verification_entries")
    if not isinstance(entries, list) or len(entries) != 2:
        raise DatasetFileAvailabilityVerificationError("verification entry count must be 2")
    by_profile = _entry_by_profile(package)
    if "SWING" not in by_profile:
        raise DatasetFileAvailabilityVerificationError("missing SWING verification entry")
    if "POSITION_SWING" not in by_profile:
        raise DatasetFileAvailabilityVerificationError("missing POSITION_SWING verification entry")
    expected_by_profile = {entry["dataset_profile"]: entry for entry in discovery._registry_definitions()}
    allowed_statuses = {
        AVAILABLE_AND_DIGEST_VERIFIED,
        MISSING_DATASET_FILE,
        MISSING_MANIFEST_FILE,
        DATASET_DIGEST_MISMATCH,
        MANIFEST_DIGEST_MISMATCH,
        VERIFICATION_BLOCKED,
    }
    for profile, expected in expected_by_profile.items():
        entry = by_profile[profile]
        for field, expected_value in {
            "registry_key": expected["registry_key"],
            "dataset_profile": expected["dataset_profile"],
            "dataset_bar_rule": expected["dataset_bar_rule"],
            "dataset_path": expected["expected_dataset_path"],
            "manifest_path": expected["expected_manifest_path"],
            "registry_approval_digest": expected["registry_approval_digest"],
            "dataset_rows_digest_expected": expected["dataset_rows_digest"],
            "dataset_manifest_digest_expected": expected["dataset_manifest_digest"],
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
        }.items():
            _expect(entry.get(field), expected_value, field)
        if entry.get("file_availability_status") not in allowed_statuses:
            raise DatasetFileAvailabilityVerificationError("file_availability_status mismatch")
        for field in ("dataset_file_exists", "manifest_file_exists", "dataset_rows_digest_match", "dataset_manifest_digest_match"):
            if entry.get(field) not in {True, False, None}:
                raise DatasetFileAvailabilityVerificationError(f"{field} mismatch")
        if entry.get("dataset_file_exists") is not True:
            _expect(entry.get("dataset_rows_digest_actual"), None, "dataset_rows_digest_actual")
            _expect(entry.get("dataset_file_sha256"), None, "dataset_file_sha256")
            _expect(entry.get("dataset_file_size_bytes"), None, "dataset_file_size_bytes")
        if entry.get("manifest_file_exists") is not True:
            _expect(entry.get("dataset_manifest_digest_actual"), None, "dataset_manifest_digest_actual")
            _expect(entry.get("manifest_file_sha256"), None, "manifest_file_sha256")
            _expect(entry.get("manifest_file_size_bytes"), None, "manifest_file_size_bytes")
        if entry.get("dataset_file_exists") is True and not isinstance(entry.get("dataset_file_sha256"), str):
            raise DatasetFileAvailabilityVerificationError("dataset_file_sha256 missing")
        if entry.get("manifest_file_exists") is True and not isinstance(entry.get("manifest_file_sha256"), str):
            raise DatasetFileAvailabilityVerificationError("manifest_file_sha256 missing")


def validate_dataset_file_availability_verification_package_v1(package: dict[str, Any]) -> dict[str, Any]:
    """Validate a dataset availability package without granting runtime authority."""
    if not isinstance(package, dict):
        raise DatasetFileAvailabilityVerificationError("dataset file availability package must be a JSON object")
    _reject_forbidden_values(package)
    _expect(package.get("artifact_kind"), ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE, "artifact_kind")
    _expect(package.get("schema_version"), SCHEMA_VERSION_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_V1, "schema_version")
    if package.get("package_status") not in {
        DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW,
        DATASET_FILE_AVAILABILITY_VERIFICATION_BLOCKED,
    }:
        raise DatasetFileAvailabilityVerificationError("package_status mismatch")
    for field in ("created_offline", "file_system_verification_performed", "operator_review_required"):
        _expect_true(package.get(field), field)
    for field in (
        "provider_requests_made",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(package.get(field), NOT_AUTHORIZED, field)
    _expect(package.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(
        package.get("read_only_discovery_candidate_digest"),
        EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST,
        "read_only_discovery_candidate_digest",
    )
    _expect(
        package.get("read_only_discovery_review_package_digest"),
        EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST,
        "read_only_discovery_review_package_digest",
    )
    _validate_entries(package)
    summary = _summary(package["verification_entries"], package.get("verification_checklist") or [])
    expected_status = (
        DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW
        if summary["ready_for_research_campaign_planning"]
        else DATASET_FILE_AVAILABILITY_VERIFICATION_BLOCKED
    )
    _expect(package.get("package_status"), expected_status, "package_status")
    if package.get("package_status") == DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW:
        _expect(summary["missing_file_count"], 0, "missing_file_count")
        _expect(summary["digest_mismatch_count"], 0, "digest_mismatch_count")
    checklist = package.get("verification_checklist")
    if not isinstance(checklist, list):
        raise DatasetFileAvailabilityVerificationError("verification_checklist must be a list")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "verification_checklist check IDs",
    )
    expected_checklist = _build_checklist(package)
    _expect(checklist, expected_checklist, "verification_checklist")
    expected_summary = _summary(package["verification_entries"], checklist)
    _expect(package.get("verification_summary"), expected_summary, "verification_summary")
    _expect_false(expected_summary.get("ready_for_runtime_migration"), "ready_for_runtime_migration")
    _expect_false(expected_summary.get("runtime_migration_authorized"), "runtime_migration_authorized")
    _expect_false(expected_summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    digest = package.get("dataset_file_availability_verification_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise DatasetFileAvailabilityVerificationError("dataset_file_availability_verification_package_digest missing")
    _expect(
        digest,
        dataset_file_availability_verification_package_digest_v1(package),
        "dataset_file_availability_verification_package_digest",
    )
    return {
        "status": "DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_VALID",
        "artifact_kind": package["artifact_kind"],
        "package_status": package["package_status"],
        "dataset_file_availability_verification_package_digest": digest,
        "verification_entry_count": expected_summary["verification_entry_count"],
        "dataset_files_available_count": expected_summary["dataset_files_available_count"],
        "manifest_files_available_count": expected_summary["manifest_files_available_count"],
        "dataset_digests_verified_count": expected_summary["dataset_digests_verified_count"],
        "manifest_digests_verified_count": expected_summary["manifest_digests_verified_count"],
        "missing_file_count": expected_summary["missing_file_count"],
        "digest_mismatch_count": expected_summary["digest_mismatch_count"],
        "ready_for_research_campaign_planning": expected_summary["ready_for_research_campaign_planning"],
        "total_checks": expected_summary["total_checks"],
        "passed_checks": expected_summary["passed_checks"],
        "failed_checks": expected_summary["failed_checks"],
        "blocker_count": expected_summary["blocker_count"],
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_dataset_file_availability_verification_markdown_v1(package: dict[str, Any]) -> str:
    """Render a sanitized dataset file availability verification status document."""
    validation = validate_dataset_file_availability_verification_package_v1(package)
    summary = package["verification_summary"]
    lines = [
        "# MarketFlow Dataset File Availability Verification Status",
        "",
        "## Title",
        "- Dataset File Availability Verification Package v1.",
        "",
        "## Purpose",
        "- Verify local research dataset and manifest files without changing runtime defaults.",
        "- This package does not approve or activate runtime migration.",
        "",
        "## Verified Dataset Files",
    ]
    for entry in package["verification_entries"]:
        lines.extend(
            [
                f"- `{entry['registry_key']}`",
                f"  - Dataset path: `{entry['dataset_path']}`",
                f"  - Manifest path: `{entry['manifest_path']}`",
                f"  - File status: `{entry['file_availability_status']}`",
            ]
        )
    lines.extend(["", "## Digest Verification"])
    for entry in package["verification_entries"]:
        lines.extend(
            [
                f"- `{entry['dataset_profile']}` dataset digest match: `{entry['dataset_rows_digest_match']}`",
                f"- `{entry['dataset_profile']}` manifest digest match: `{entry['dataset_manifest_digest_match']}`",
                f"- `{entry['dataset_profile']}` dataset file SHA-256: `{entry['dataset_file_sha256']}`",
                f"- `{entry['dataset_profile']}` manifest file SHA-256: `{entry['manifest_file_sha256']}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Availability Summary",
            f"- Dataset files available: `{summary['dataset_files_available_count']}`",
            f"- Manifest files available: `{summary['manifest_files_available_count']}`",
            f"- Dataset digests verified: `{summary['dataset_digests_verified_count']}`",
            f"- Manifest digests verified: `{summary['manifest_digests_verified_count']}`",
            f"- Missing files: `{summary['missing_file_count']}`",
            f"- Digest mismatches: `{summary['digest_mismatch_count']}`",
            f"- Ready for research campaign planning: `{summary['ready_for_research_campaign_planning']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{package['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{package['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{package['strategy_runtime_migration']}`",
            f"- runtime_use: `{package['runtime_use']}`",
            f"- strategy_use: `{package['strategy_use']}`",
            f"- paper_trading: `{package['paper_trading']}`",
            f"- broker_execution: `{package['broker_execution']}`",
            f"- automatic_stitching: `{package['automatic_stitching']}`",
            f"- predictive_usefulness: `{package['predictive_usefulness']}`",
            f"- profitability: `{package['profitability']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(package["remaining_required_tasks"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made: `False`",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No acquisition rows, SWING bars, or POSITION_SWING bars were regenerated.",
            "- No runtime default source was changed.",
            "- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
            "## Package Digest",
            f"- Package digest: `{validation['dataset_file_availability_verification_package_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_dataset_file_availability_verification_package_v1(
    output_dir: str | Path,
    *,
    search_root: str | Path | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the dataset availability package JSON artifact without overwriting output."""
    package = build_dataset_file_availability_verification_package_v1(search_root=search_root)
    validation = validate_dataset_file_availability_verification_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "dataset_file_availability_verification_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise DatasetFileAvailabilityVerificationError(
            "dataset file availability verification filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise DatasetFileAvailabilityVerificationError(
            "dataset file availability verification output already exists"
        )
    payload = canonical_json_bytes(package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
