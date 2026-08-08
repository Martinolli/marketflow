"""Offline read-only discovery for approved research registry datasets."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import position_swing_canonical_dataset_service as position_dataset
from marketflow.services import position_swing_registry_approval_service as position_registry
from marketflow.services import runtime_migration_operator_review_service as runtime_review
from marketflow.services import runtime_migration_planning_service as runtime_planning
from marketflow.services import swing_canonical_dataset_service as swing_dataset
from marketflow.services import swing_registry_approval_service as swing_registry


ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE = "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE"
SCHEMA_VERSION_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_V1 = "read_only_registry_discovery_candidate_v1"
READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW = "READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW"
READ_ONLY_REGISTRY_DISCOVERY_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION = (
    "READ_ONLY_REGISTRY_DISCOVERY_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION"
)

AVAILABLE_DIGEST_VERIFIED = "AVAILABLE_DIGEST_VERIFIED"
AVAILABLE_UNVERIFIED = "AVAILABLE_UNVERIFIED"
AVAILABLE_DIGEST_MISMATCH = "AVAILABLE_DIGEST_MISMATCH"
MISSING_LOCAL_DATASET_FILE = "MISSING_LOCAL_DATASET_FILE"
MISSING_LOCAL_MANIFEST_FILE = "MISSING_LOCAL_MANIFEST_FILE"
DISCOVERED_DIGEST_VERIFIED = "DISCOVERED_DIGEST_VERIFIED"
DISCOVERED_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION = (
    "DISCOVERED_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION"
)

EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST = runtime_review.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST
EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST = (
    "1d856db1e388e48948155739810baa5f140e2bec5318c80c3f4381d4d759d2e4"
)
NOT_AUTHORIZED = runtime_planning.NOT_AUTHORIZED

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

SWING_EXPECTED_DATASET_PATH = (
    ".marketflow/canonical_candidates/AAPL/SWING/"
    "AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv"
)
SWING_EXPECTED_MANIFEST_PATH = (
    ".marketflow/canonical_candidates/AAPL/SWING/"
    "AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025_manifest.json"
)
POSITION_SWING_EXPECTED_DATASET_PATH = (
    ".marketflow/canonical_candidates/AAPL/POSITION_SWING/"
    "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv"
)
POSITION_SWING_EXPECTED_MANIFEST_PATH = (
    ".marketflow/canonical_candidates/AAPL/POSITION_SWING/"
    "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_manifest.json"
)

REQUIRED_CHECK_IDS = [
    "runtime_plan_digest_bound",
    "runtime_review_package_digest_bound",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "swing_registry_entry_discovered",
    "position_swing_registry_entry_discovered",
    "registry_entry_count_two",
    "registry_scope_research_dataset_only",
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
    "read_only_discovery_true",
    "no_runtime_default_change",
]

REMAINING_REQUIRED_TASKS = [
    "Read-only registry discovery operator review package.",
    "Dataset file availability verification.",
    "Research-only applicability campaign plan.",
]


class ReadOnlyRegistryDiscoveryError(ValueError):
    """Raised when a read-only registry discovery candidate violates guardrails."""


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
        raise ReadOnlyRegistryDiscoveryError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ReadOnlyRegistryDiscoveryError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ReadOnlyRegistryDiscoveryError(f"{field_name} must be true")


def _candidate_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE,
        "schema_version": SCHEMA_VERSION_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_V1,
        "created_offline": True,
        "provider_requests_made": False,
        "read_only_discovery": True,
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
        "runtime_migration_plan_digest": EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "runtime_migration_review_package_digest": EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
    }


def _registry_definitions() -> list[dict[str, Any]]:
    return [
        {
            "registry_key": swing_registry.PROPOSED_REGISTRY_KEY,
            "dataset_profile": swing_dataset.DATASET_PROFILE_SWING,
            "dataset_bar_rule": swing_dataset.DATASET_BAR_RULE_RTH_HALF_SESSION_195M,
            "ticker": "AAPL",
            "range_start": "2022-01-01",
            "range_end": "2025-12-31",
            "registry_scope": swing_registry.PROPOSED_REGISTRY_SCOPE,
            "registry_approval_digest": runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
            "dataset_rows_digest": swing_registry.EXPECTED_DATASET_ROWS_DIGEST,
            "dataset_manifest_digest": swing_registry.EXPECTED_DATASET_MANIFEST_DIGEST,
            "expected_dataset_path": SWING_EXPECTED_DATASET_PATH,
            "expected_manifest_path": SWING_EXPECTED_MANIFEST_PATH,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
        },
        {
            "registry_key": position_registry.PROPOSED_REGISTRY_KEY,
            "dataset_profile": position_dataset.DATASET_PROFILE_POSITION_SWING,
            "dataset_bar_rule": position_dataset.DATASET_BAR_RULE_RTH_FULL_SESSION_1D,
            "ticker": "AAPL",
            "range_start": "2022-01-01",
            "range_end": "2025-12-31",
            "registry_scope": position_registry.PROPOSED_REGISTRY_SCOPE,
            "registry_approval_digest": runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
            "dataset_rows_digest": position_registry.EXPECTED_DATASET_ROWS_DIGEST,
            "dataset_manifest_digest": position_registry.EXPECTED_DATASET_MANIFEST_DIGEST,
            "expected_dataset_path": POSITION_SWING_EXPECTED_DATASET_PATH,
            "expected_manifest_path": POSITION_SWING_EXPECTED_MANIFEST_PATH,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
        },
    ]


def _resolve_search_root(search_root: str | Path | None) -> Path:
    return Path("." if search_root is None else search_root)


def _read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    integer_fields = {"bar_number_in_session", "transactions", "source_row_count"}
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized_row: dict[str, Any] = {}
        for key, value in row.items():
            if value == "":
                normalized_row[key] = None
            elif key in integer_fields:
                normalized_row[key] = int(value)
            else:
                normalized_row[key] = value
        normalized.append(normalized_row)
    return normalized


def _read_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if not isinstance(manifest, dict):
        raise ReadOnlyRegistryDiscoveryError("dataset manifest must be a JSON object")
    return manifest


def _dataset_digest_for_entry(entry: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    if entry["dataset_profile"] == "SWING":
        return swing_dataset.dataset_rows_digest_v1(rows)
    if entry["dataset_profile"] == "POSITION_SWING":
        return position_dataset.dataset_rows_digest_v1(rows)
    raise ReadOnlyRegistryDiscoveryError("unsupported dataset profile")


def _manifest_digest_for_entry(entry: dict[str, Any], manifest: dict[str, Any]) -> str:
    if entry["dataset_profile"] == "SWING":
        return swing_dataset.dataset_manifest_digest_v1(manifest)
    if entry["dataset_profile"] == "POSITION_SWING":
        return position_dataset.dataset_manifest_digest_v1(manifest)
    raise ReadOnlyRegistryDiscoveryError("unsupported dataset profile")


def _availability(entry: dict[str, Any], *, search_root: Path) -> dict[str, Any]:
    dataset_path = search_root / entry["expected_dataset_path"]
    manifest_path = search_root / entry["expected_manifest_path"]
    dataset_exists = dataset_path.exists() and dataset_path.is_file()
    manifest_exists = manifest_path.exists() and manifest_path.is_file()

    dataset_status = MISSING_LOCAL_DATASET_FILE
    manifest_status = MISSING_LOCAL_MANIFEST_FILE
    dataset_digest_verified: bool | None = None
    manifest_digest_verified: bool | None = None
    actual_dataset_rows_digest = None
    actual_dataset_manifest_digest = None

    if dataset_exists:
        rows = _read_csv_rows(dataset_path)
        actual_dataset_rows_digest = _dataset_digest_for_entry(entry, rows)
        dataset_digest_verified = actual_dataset_rows_digest == entry["dataset_rows_digest"]
        dataset_status = AVAILABLE_DIGEST_VERIFIED if dataset_digest_verified else AVAILABLE_DIGEST_MISMATCH

    if manifest_exists:
        manifest = _read_manifest(manifest_path)
        actual_dataset_manifest_digest = _manifest_digest_for_entry(entry, manifest)
        manifest_digest_verified = actual_dataset_manifest_digest == entry["dataset_manifest_digest"]
        manifest_status = AVAILABLE_DIGEST_VERIFIED if manifest_digest_verified else AVAILABLE_DIGEST_MISMATCH

    if dataset_exists and dataset_digest_verified is None:
        dataset_status = AVAILABLE_UNVERIFIED
    if manifest_exists and manifest_digest_verified is None:
        manifest_status = AVAILABLE_UNVERIFIED

    entry_discovery_status = (
        DISCOVERED_DIGEST_VERIFIED
        if dataset_digest_verified is True and manifest_digest_verified is True
        else DISCOVERED_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION
    )
    return {
        "dataset_file_status": dataset_status,
        "manifest_file_status": manifest_status,
        "dataset_digest_verified": dataset_digest_verified,
        "manifest_digest_verified": manifest_digest_verified,
        "actual_dataset_rows_digest": actual_dataset_rows_digest,
        "actual_dataset_manifest_digest": actual_dataset_manifest_digest,
        "entry_discovery_status": entry_discovery_status,
    }


def discover_research_registry_entries_v1(
    *,
    search_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Discover the two approved research registry entries without changing runtime defaults."""
    root = _resolve_search_root(search_root)
    entries: list[dict[str, Any]] = []
    for definition in _registry_definitions():
        entry = deepcopy(definition)
        entry.update(_availability(entry, search_root=root))
        entries.append(entry)
    return entries


def _summary(entries: list[dict[str, Any]], checklist: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    available_dataset_file_count = sum(
        1 for entry in entries if entry.get("dataset_file_status") != MISSING_LOCAL_DATASET_FILE
    )
    available_manifest_file_count = sum(
        1 for entry in entries if entry.get("manifest_file_status") != MISSING_LOCAL_MANIFEST_FILE
    )
    verified_dataset_digest_count = sum(1 for entry in entries if entry.get("dataset_digest_verified") is True)
    verified_manifest_digest_count = sum(1 for entry in entries if entry.get("manifest_digest_verified") is True)
    missing_file_count = sum(
        1
        for entry in entries
        for field in ("dataset_file_status", "manifest_file_status")
        if entry.get(field) in {MISSING_LOCAL_DATASET_FILE, MISSING_LOCAL_MANIFEST_FILE}
    )
    total = len(checklist or [])
    passed = sum(1 for item in checklist or [] if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(1 for item in checklist or [] if item.get("status") == FAIL and item.get("severity") == BLOCKER)
    return {
        "registry_entry_count": len(entries),
        "available_dataset_file_count": available_dataset_file_count,
        "available_manifest_file_count": available_manifest_file_count,
        "verified_dataset_digest_count": verified_dataset_digest_count,
        "verified_manifest_digest_count": verified_manifest_digest_count,
        "missing_file_count": missing_file_count,
        "ready_for_dataset_availability_verification": missing_file_count > 0
        or verified_dataset_digest_count != len(entries)
        or verified_manifest_digest_count != len(entries),
        "ready_for_runtime_migration": False,
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_review": failed == 0,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _candidate_status(entries: list[dict[str, Any]]) -> str:
    if all(
        entry.get("dataset_digest_verified") is True and entry.get("manifest_digest_verified") is True
        for entry in entries
    ):
        return READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW
    return READ_ONLY_REGISTRY_DISCOVERY_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION


def _build_checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("registry_entries") or []
    entry_by_profile = {
        entry.get("dataset_profile"): entry for entry in entries if isinstance(entry, dict)
    }
    swing_entry = entry_by_profile.get("SWING") or {}
    position_entry = entry_by_profile.get("POSITION_SWING") or {}
    scopes = [entry.get("registry_scope") for entry in entries if isinstance(entry, dict)]
    runtime_uses = [entry.get("runtime_use") for entry in entries if isinstance(entry, dict)]
    strategy_uses = [entry.get("strategy_use") for entry in entries if isinstance(entry, dict)]
    return [
        _check("runtime_plan_digest_bound", EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST, candidate.get("runtime_migration_plan_digest")),
        _check(
            "runtime_review_package_digest_bound",
            EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
            candidate.get("runtime_migration_review_package_digest"),
        ),
        _check(
            "swing_registry_approval_digest_bound",
            runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
            swing_entry.get("registry_approval_digest"),
        ),
        _check(
            "position_swing_registry_approval_digest_bound",
            runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
            position_entry.get("registry_approval_digest"),
        ),
        _check("swing_registry_entry_discovered", True, bool(swing_entry)),
        _check("position_swing_registry_entry_discovered", True, bool(position_entry)),
        _check("registry_entry_count_two", 2, len(entries)),
        _check("registry_scope_research_dataset_only", ["RESEARCH_DATASET", "RESEARCH_DATASET"], scopes),
        _check("runtime_use_not_authorized", [NOT_AUTHORIZED, NOT_AUTHORIZED], runtime_uses),
        _check("strategy_use_not_authorized", [NOT_AUTHORIZED, NOT_AUTHORIZED], strategy_uses),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, candidate.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check(
            "predictive_usefulness_not_accepted",
            acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            candidate.get("predictive_usefulness"),
            severity=INFO,
        ),
        _check(
            "profitability_not_accepted",
            acquisition.PROFITABILITY_NOT_ACCEPTED,
            candidate.get("profitability"),
            severity=INFO,
        ),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("read_only_discovery_true", True, candidate.get("read_only_discovery")),
        _check(
            "no_runtime_default_change",
            {
                "runtime_use": NOT_AUTHORIZED,
                "strategy_use": NOT_AUTHORIZED,
                "runtime_migration_approved": False,
                "runtime_migration_active": False,
            },
            {
                "runtime_use": candidate.get("runtime_use"),
                "strategy_use": candidate.get("strategy_use"),
                "runtime_migration_approved": candidate.get("runtime_migration_approved"),
                "runtime_migration_active": candidate.get("runtime_migration_active"),
            },
        ),
    ]


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("read_only_registry_discovery_candidate_digest", None)
    return payload


def read_only_registry_discovery_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a discovery candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_read_only_registry_discovery_candidate_v1(
    *,
    search_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build a read-only candidate describing approved research registry dataset availability."""
    entries = discover_research_registry_entries_v1(search_root=search_root)
    candidate = {
        **_candidate_context(),
        "candidate_status": _candidate_status(entries),
        "registry_entries": entries,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _build_checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(entries, checklist)
    candidate["read_only_registry_discovery_candidate_digest"] = (
        read_only_registry_discovery_candidate_digest_v1(candidate)
    )
    validate_read_only_registry_discovery_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise ReadOnlyRegistryDiscoveryError(f"{current_path} must not emit {value}")
        if key in {
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
        } and value is True:
            raise ReadOnlyRegistryDiscoveryError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise ReadOnlyRegistryDiscoveryError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ReadOnlyRegistryDiscoveryError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_read_only_registry_discovery_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate a read-only registry discovery candidate without granting runtime authority."""
    if not isinstance(candidate, dict):
        raise ReadOnlyRegistryDiscoveryError("read-only registry discovery candidate must be a JSON object")
    _reject_forbidden_values(candidate)
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_V1, "schema_version")
    if candidate.get("candidate_status") not in {
        READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW,
        READ_ONLY_REGISTRY_DISCOVERY_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION,
    }:
        raise ReadOnlyRegistryDiscoveryError("candidate_status mismatch")
    for field in ("created_offline", "read_only_discovery", "operator_review_required"):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    _expect(
        candidate.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(candidate.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(candidate.get("runtime_migration_plan_digest"), EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST, "runtime_migration_plan_digest")
    _expect(
        candidate.get("runtime_migration_review_package_digest"),
        EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
        "runtime_migration_review_package_digest",
    )
    entries = candidate.get("registry_entries")
    if not isinstance(entries, list) or len(entries) != 2:
        raise ReadOnlyRegistryDiscoveryError("registry entry count must be 2")
    expected_by_profile = {entry["dataset_profile"]: entry for entry in _registry_definitions()}
    found_profiles = {entry.get("dataset_profile") for entry in entries if isinstance(entry, dict)}
    if "SWING" not in found_profiles:
        raise ReadOnlyRegistryDiscoveryError("missing SWING registry entry")
    if "POSITION_SWING" not in found_profiles:
        raise ReadOnlyRegistryDiscoveryError("missing POSITION_SWING registry entry")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ReadOnlyRegistryDiscoveryError("registry entry must be a JSON object")
        profile = entry.get("dataset_profile")
        expected = expected_by_profile.get(profile)
        if expected is None:
            raise ReadOnlyRegistryDiscoveryError("unexpected registry entry")
        for field in (
            "registry_key",
            "dataset_profile",
            "dataset_bar_rule",
            "ticker",
            "range_start",
            "range_end",
            "registry_scope",
            "registry_approval_digest",
            "dataset_rows_digest",
            "dataset_manifest_digest",
            "expected_dataset_path",
            "expected_manifest_path",
            "runtime_use",
            "strategy_use",
        ):
            _expect(entry.get(field), expected[field], field)
        if entry.get("registry_scope") != "RESEARCH_DATASET":
            raise ReadOnlyRegistryDiscoveryError("registry_scope must be RESEARCH_DATASET")
        for status_field, allowed in {
            "dataset_file_status": {AVAILABLE_DIGEST_VERIFIED, AVAILABLE_UNVERIFIED, AVAILABLE_DIGEST_MISMATCH, MISSING_LOCAL_DATASET_FILE},
            "manifest_file_status": {AVAILABLE_DIGEST_VERIFIED, AVAILABLE_UNVERIFIED, AVAILABLE_DIGEST_MISMATCH, MISSING_LOCAL_MANIFEST_FILE},
            "entry_discovery_status": {
                DISCOVERED_DIGEST_VERIFIED,
                DISCOVERED_REQUIRES_DATASET_FILE_AVAILABILITY_VERIFICATION,
            },
        }.items():
            if entry.get(status_field) not in allowed:
                raise ReadOnlyRegistryDiscoveryError(f"{status_field} mismatch")
        for field in ("dataset_digest_verified", "manifest_digest_verified"):
            if entry.get(field) not in {True, False, None}:
                raise ReadOnlyRegistryDiscoveryError(f"{field} mismatch")
    expected_status = _candidate_status(entries)
    _expect(candidate.get("candidate_status"), expected_status, "candidate_status")
    _expect(candidate.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise ReadOnlyRegistryDiscoveryError("candidate_checklist must be a list")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check IDs",
    )
    expected_checklist = _build_checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise ReadOnlyRegistryDiscoveryError(f"discovery checklist contains failed check: {failed[0]['check_id']}")
    _expect(checklist, expected_checklist, "candidate_checklist")
    summary = _summary(entries, checklist)
    _expect(candidate.get("candidate_summary"), summary, "candidate_summary")
    _expect_false(summary.get("ready_for_runtime_migration"), "ready_for_runtime_migration")
    _expect_false(summary.get("runtime_migration_authorized"), "runtime_migration_authorized")
    _expect_false(summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    digest = candidate.get("read_only_registry_discovery_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ReadOnlyRegistryDiscoveryError("read_only_registry_discovery_candidate_digest missing")
    _expect(
        digest,
        read_only_registry_discovery_candidate_digest_v1(candidate),
        "read_only_registry_discovery_candidate_digest",
    )
    return {
        "status": "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "read_only_registry_discovery_candidate_digest": digest,
        "runtime_migration_plan_digest": EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "runtime_migration_review_package_digest": EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
        "registry_entry_count": summary["registry_entry_count"],
        "available_dataset_file_count": summary["available_dataset_file_count"],
        "available_manifest_file_count": summary["available_manifest_file_count"],
        "verified_dataset_digest_count": summary["verified_dataset_digest_count"],
        "verified_manifest_digest_count": summary["verified_manifest_digest_count"],
        "missing_file_count": summary["missing_file_count"],
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
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


def build_read_only_registry_discovery_candidate_markdown_v1(candidate: dict[str, Any]) -> str:
    """Render a sanitized read-only registry discovery candidate status document."""
    validation = validate_read_only_registry_discovery_candidate_v1(candidate)
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Read-Only Registry Discovery Status",
        "",
        "## Title",
        "- Read-Only Registry Discovery Candidate v1.",
        "",
        "## Purpose",
        "- Discover approved research registry entries without changing runtime defaults.",
        "- This candidate does not approve or activate runtime migration.",
        "",
        "## Discovered Research Registry Entries",
    ]
    for entry in candidate["registry_entries"]:
        lines.extend(
            [
                f"- `{entry['registry_key']}`",
                f"  - Dataset profile: `{entry['dataset_profile']}`",
                f"  - Dataset bar rule: `{entry['dataset_bar_rule']}`",
                f"  - Registry scope: `{entry['registry_scope']}`",
                f"  - Runtime use: `{entry['runtime_use']}`",
                f"  - Strategy use: `{entry['strategy_use']}`",
            ]
        )
    lines.extend(["", "## Local Dataset File Availability"])
    for entry in candidate["registry_entries"]:
        lines.extend(
            [
                f"- `{entry['dataset_profile']}` dataset file: `{entry['dataset_file_status']}`",
                f"- `{entry['dataset_profile']}` manifest file: `{entry['manifest_file_status']}`",
                f"- `{entry['dataset_profile']}` dataset digest verified: `{entry['dataset_digest_verified']}`",
                f"- `{entry['dataset_profile']}` manifest digest verified: `{entry['manifest_digest_verified']}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{candidate['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{candidate['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{candidate['strategy_runtime_migration']}`",
            f"- runtime_use: `{candidate['runtime_use']}`",
            f"- strategy_use: `{candidate['strategy_use']}`",
            f"- paper_trading: `{candidate['paper_trading']}`",
            f"- broker_execution: `{candidate['broker_execution']}`",
            f"- automatic_stitching: `{candidate['automatic_stitching']}`",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            f"- profitability: `{candidate['profitability']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Ready for runtime migration: `{summary['ready_for_runtime_migration']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(candidate["remaining_required_tasks"], start=1))
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
            "## Candidate Digest",
            f"- Candidate digest: `{validation['read_only_registry_discovery_candidate_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_read_only_registry_discovery_candidate_v1(
    output_dir: str | Path,
    *,
    search_root: str | Path | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write a read-only registry discovery candidate JSON artifact without overwriting output."""
    candidate = build_read_only_registry_discovery_candidate_v1(search_root=search_root)
    validation = validate_read_only_registry_discovery_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "read_only_registry_discovery_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ReadOnlyRegistryDiscoveryError("read-only registry discovery filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise ReadOnlyRegistryDiscoveryError("read-only registry discovery output already exists")
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
