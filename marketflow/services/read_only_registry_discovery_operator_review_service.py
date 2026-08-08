"""Offline operator-review package for read-only registry discovery candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import read_only_registry_discovery_service as discovery


ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE = (
    "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_V1 = (
    "read_only_registry_discovery_candidate_review_v1"
)
READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_READY = (
    "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_READY"
)
READ_ONLY_REGISTRY_DISCOVERY_STATUS_BINDING = "READ_ONLY_REGISTRY_DISCOVERY_STATUS_BINDING"
READ_ONLY_REGISTRY_DISCOVERY_OBJECT_BINDING = "READ_ONLY_REGISTRY_DISCOVERY_OBJECT_BINDING"

EXPECTED_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_DIGEST = (
    "b2c46f880b3764e31d159f4c344004dbb104a3a1129e97499aafc0a7b6ef8bc1"
)
EXPECTED_DISCOVERY_CHECKLIST_TOTAL = len(discovery.REQUIRED_CHECK_IDS)
EXPECTED_DISCOVERY_CHECKLIST_PASSED = len(discovery.REQUIRED_CHECK_IDS)
EXPECTED_DISCOVERY_CHECKLIST_FAILED = 0
EXPECTED_DISCOVERY_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "discovery_candidate_kind_matches",
    "discovery_candidate_status_ready_for_review",
    "discovery_candidate_digest_matches",
    "discovery_candidate_checklist_zero_blockers",
    "registry_entry_count_two",
    "available_dataset_file_count_two",
    "available_manifest_file_count_two",
    "verified_dataset_digest_count_two",
    "verified_manifest_digest_count_two",
    "missing_file_count_zero",
    "swing_registry_entry_verified",
    "position_swing_registry_entry_verified",
    "swing_registry_approval_digest_bound",
    "position_swing_registry_approval_digest_bound",
    "swing_dataset_digest_verified",
    "position_swing_dataset_digest_verified",
    "swing_manifest_digest_verified",
    "position_swing_manifest_digest_verified",
    "runtime_plan_digest_bound",
    "runtime_review_package_digest_bound",
    "read_only_discovery_true",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "provider_requests_made_in_review_false",
    "no_runtime_activation_artifact_created",
]

REMAINING_REQUIRED_TASKS = [
    "Dataset file availability verification package.",
    "Research-only applicability campaign plan.",
    "Research-only applicability campaign execution.",
    "Predictive usefulness review.",
    "Profitability review.",
    "Separate runtime migration approval ceremony, if ever authorized.",
]

FORBIDDEN_APPROVAL_FIELDS = frozenset(
    {
        "operator_approved_by",
        "operator_approval_timestamp",
        "operator_approval_digest",
        "operator_signature",
        "approval_status",
    }
)


class ReadOnlyRegistryDiscoveryOperatorReviewError(ValueError):
    """Raised when a read-only discovery review package violates guardrails."""


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
        raise ReadOnlyRegistryDiscoveryOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ReadOnlyRegistryDiscoveryOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ReadOnlyRegistryDiscoveryOperatorReviewError(f"{field_name} must be true")


def _review_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_V1,
        "review_status": READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_READY,
        "operator_decision_required": True,
        "operator_decision": None,
        "operator_approved_by": None,
        "operator_approval_timestamp": None,
        "operator_approval_digest": None,
        "operator_signature": None,
        "approval_status": None,
        "read_only_discovery": True,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": discovery.NOT_AUTHORIZED,
        "strategy_use": discovery.NOT_AUTHORIZED,
        "paper_trading": discovery.NOT_AUTHORIZED,
        "broker_execution": discovery.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _entry_with_verified_availability(entry: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(entry)
    result.update(
        {
            "dataset_file_status": discovery.AVAILABLE_DIGEST_VERIFIED,
            "manifest_file_status": discovery.AVAILABLE_DIGEST_VERIFIED,
            "dataset_digest_verified": True,
            "manifest_digest_verified": True,
            "actual_dataset_rows_digest": entry["dataset_rows_digest"],
            "actual_dataset_manifest_digest": entry["dataset_manifest_digest"],
            "entry_discovery_status": discovery.DISCOVERED_DIGEST_VERIFIED,
        }
    )
    return result


def _recorded_registry_entries() -> list[dict[str, Any]]:
    return [_entry_with_verified_availability(entry) for entry in discovery._registry_definitions()]


def _discovery_evidence_from_candidate(discovery_candidate: dict[str, Any]) -> dict[str, Any]:
    try:
        validation = discovery.validate_read_only_registry_discovery_candidate_v1(discovery_candidate)
    except discovery.ReadOnlyRegistryDiscoveryError as exc:
        raise ReadOnlyRegistryDiscoveryOperatorReviewError(
            f"source read-only registry discovery candidate invalid: {exc}"
        ) from exc
    return {
        "reviewed_discovery_candidate_kind": discovery_candidate["artifact_kind"],
        "reviewed_discovery_candidate_status": discovery_candidate["candidate_status"],
        "reviewed_discovery_candidate_digest": validation["read_only_registry_discovery_candidate_digest"],
        "reviewed_discovery_checklist_total": validation["total_checks"],
        "reviewed_discovery_checklist_passed": validation["passed_checks"],
        "reviewed_discovery_checklist_failed": validation["failed_checks"],
        "reviewed_discovery_blocker_count": validation["blocker_count"],
        "registry_entry_count": validation["registry_entry_count"],
        "available_dataset_file_count": validation["available_dataset_file_count"],
        "available_manifest_file_count": validation["available_manifest_file_count"],
        "verified_dataset_digest_count": validation["verified_dataset_digest_count"],
        "verified_manifest_digest_count": validation["verified_manifest_digest_count"],
        "missing_file_count": validation["missing_file_count"],
        "runtime_migration_plan_digest": validation["runtime_migration_plan_digest"],
        "runtime_migration_review_package_digest": validation["runtime_migration_review_package_digest"],
        "registry_entries": deepcopy(discovery_candidate["registry_entries"]),
    }


def _recorded_discovery_evidence() -> dict[str, Any]:
    return {
        "reviewed_discovery_candidate_kind": discovery.ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE,
        "reviewed_discovery_candidate_status": discovery.READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW,
        "reviewed_discovery_candidate_digest": EXPECTED_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_DIGEST,
        "reviewed_discovery_checklist_total": EXPECTED_DISCOVERY_CHECKLIST_TOTAL,
        "reviewed_discovery_checklist_passed": EXPECTED_DISCOVERY_CHECKLIST_PASSED,
        "reviewed_discovery_checklist_failed": EXPECTED_DISCOVERY_CHECKLIST_FAILED,
        "reviewed_discovery_blocker_count": EXPECTED_DISCOVERY_BLOCKER_COUNT,
        "registry_entry_count": 2,
        "available_dataset_file_count": 2,
        "available_manifest_file_count": 2,
        "verified_dataset_digest_count": 2,
        "verified_manifest_digest_count": 2,
        "missing_file_count": 0,
        "runtime_migration_plan_digest": discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "runtime_migration_review_package_digest": discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
        "registry_entries": _recorded_registry_entries(),
    }


def _entry_by_profile(review_package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        entry.get("dataset_profile"): entry
        for entry in review_package.get("registry_entries") or []
        if isinstance(entry, dict)
    }


def _build_checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("registry_entries") or []
    entry_by_profile = _entry_by_profile(review_package)
    swing_entry = entry_by_profile.get("SWING") or {}
    position_entry = entry_by_profile.get("POSITION_SWING") or {}
    return [
        _check("discovery_candidate_kind_matches", discovery.ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE, review_package.get("reviewed_discovery_candidate_kind")),
        _check("discovery_candidate_status_ready_for_review", discovery.READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_discovery_candidate_status")),
        _check("discovery_candidate_digest_matches", EXPECTED_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_DIGEST, review_package.get("reviewed_discovery_candidate_digest")),
        _check(
            "discovery_candidate_checklist_zero_blockers",
            {
                "total": EXPECTED_DISCOVERY_CHECKLIST_TOTAL,
                "passed": EXPECTED_DISCOVERY_CHECKLIST_PASSED,
                "failed": EXPECTED_DISCOVERY_CHECKLIST_FAILED,
                "blockers": EXPECTED_DISCOVERY_BLOCKER_COUNT,
            },
            {
                "total": review_package.get("reviewed_discovery_checklist_total"),
                "passed": review_package.get("reviewed_discovery_checklist_passed"),
                "failed": review_package.get("reviewed_discovery_checklist_failed"),
                "blockers": review_package.get("reviewed_discovery_blocker_count"),
            },
        ),
        _check("registry_entry_count_two", 2, review_package.get("registry_entry_count")),
        _check("available_dataset_file_count_two", 2, review_package.get("available_dataset_file_count")),
        _check("available_manifest_file_count_two", 2, review_package.get("available_manifest_file_count")),
        _check("verified_dataset_digest_count_two", 2, review_package.get("verified_dataset_digest_count")),
        _check("verified_manifest_digest_count_two", 2, review_package.get("verified_manifest_digest_count")),
        _check("missing_file_count_zero", 0, review_package.get("missing_file_count")),
        _check("swing_registry_entry_verified", discovery.AVAILABLE_DIGEST_VERIFIED, swing_entry.get("dataset_file_status")),
        _check("position_swing_registry_entry_verified", discovery.AVAILABLE_DIGEST_VERIFIED, position_entry.get("dataset_file_status")),
        _check("swing_registry_approval_digest_bound", discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, swing_entry.get("registry_approval_digest")),
        _check("position_swing_registry_approval_digest_bound", discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST, position_entry.get("registry_approval_digest")),
        _check("swing_dataset_digest_verified", True, swing_entry.get("dataset_digest_verified")),
        _check("position_swing_dataset_digest_verified", True, position_entry.get("dataset_digest_verified")),
        _check("swing_manifest_digest_verified", True, swing_entry.get("manifest_digest_verified")),
        _check("position_swing_manifest_digest_verified", True, position_entry.get("manifest_digest_verified")),
        _check("runtime_plan_digest_bound", discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST, review_package.get("runtime_migration_plan_digest")),
        _check("runtime_review_package_digest_bound", discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST, review_package.get("runtime_migration_review_package_digest")),
        _check("read_only_discovery_true", True, review_package.get("read_only_discovery")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", discovery.NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", discovery.NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", discovery.NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", discovery.NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, review_package.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, review_package.get("profitability"), severity=INFO),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check(
            "no_runtime_activation_artifact_created",
            {
                "artifact_kind_is_review_package": True,
                "review_status_is_ready": True,
                "approval_status_is_null": True,
                "runtime_migration_approved_is_false": True,
                "runtime_migration_active_is_false": True,
            },
            {
                "artifact_kind_is_review_package": review_package.get("artifact_kind")
                == ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE,
                "review_status_is_ready": review_package.get("review_status")
                == READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_READY,
                "approval_status_is_null": review_package.get("approval_status") is None,
                "runtime_migration_approved_is_false": review_package.get("runtime_migration_approved") is False,
                "runtime_migration_active_is_false": review_package.get("runtime_migration_active") is False,
            },
        ),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item["status"] == PASS)
    failed = total - passed
    blocker_count = sum(1 for item in checklist if item["status"] == FAIL and item["severity"] == BLOCKER)
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_assessment": failed == 0,
        "operator_decision_required_before_next_gate": True,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("read_only_registry_discovery_review_package_digest", None)
    return payload


def read_only_registry_discovery_review_package_digest_v1(review_package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a discovery review package."""
    return semantic_digest(_digest_payload(review_package))


def build_read_only_registry_discovery_candidate_review_package_v1(
    discovery_candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for read-only registry discovery."""
    binding_mode = READ_ONLY_REGISTRY_DISCOVERY_STATUS_BINDING
    evidence = _recorded_discovery_evidence()
    if discovery_candidate is not None:
        binding_mode = READ_ONLY_REGISTRY_DISCOVERY_OBJECT_BINDING
        evidence = _discovery_evidence_from_candidate(discovery_candidate)
    review_package = {
        **_review_context(),
        "binding_mode": binding_mode,
        **evidence,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _build_checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package["read_only_registry_discovery_review_package_digest"] = (
        read_only_registry_discovery_review_package_digest_v1(review_package)
    )
    validate_read_only_registry_discovery_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise ReadOnlyRegistryDiscoveryOperatorReviewError(f"{current_path} must not emit {value}")
        if key in FORBIDDEN_APPROVAL_FIELDS and value is not None:
            raise ReadOnlyRegistryDiscoveryOperatorReviewError(f"{current_path} must be null")
        if key in {
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
        } and value is True:
            raise ReadOnlyRegistryDiscoveryOperatorReviewError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise ReadOnlyRegistryDiscoveryOperatorReviewError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ReadOnlyRegistryDiscoveryOperatorReviewError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_registry_entries(review_package: dict[str, Any]) -> None:
    entries = review_package.get("registry_entries")
    if not isinstance(entries, list) or len(entries) != 2:
        raise ReadOnlyRegistryDiscoveryOperatorReviewError("registry entry count must be 2")
    by_profile = _entry_by_profile(review_package)
    if "SWING" not in by_profile:
        raise ReadOnlyRegistryDiscoveryOperatorReviewError("missing SWING registry entry")
    if "POSITION_SWING" not in by_profile:
        raise ReadOnlyRegistryDiscoveryOperatorReviewError("missing POSITION_SWING registry entry")
    expected_by_profile = {
        entry["dataset_profile"]: _entry_with_verified_availability(entry)
        for entry in discovery._registry_definitions()
    }
    for profile, expected in expected_by_profile.items():
        entry = by_profile[profile]
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
            "dataset_file_status",
            "manifest_file_status",
            "dataset_digest_verified",
            "manifest_digest_verified",
            "actual_dataset_rows_digest",
            "actual_dataset_manifest_digest",
            "entry_discovery_status",
            "runtime_use",
            "strategy_use",
        ):
            _expect(entry.get(field), expected[field], field)


def validate_read_only_registry_discovery_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate a discovery review package without granting runtime authority."""
    if not isinstance(review_package, dict):
        raise ReadOnlyRegistryDiscoveryOperatorReviewError("read-only discovery review package must be a JSON object")
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("binding_mode") not in {
        READ_ONLY_REGISTRY_DISCOVERY_STATUS_BINDING,
        READ_ONLY_REGISTRY_DISCOVERY_OBJECT_BINDING,
    }:
        raise ReadOnlyRegistryDiscoveryOperatorReviewError("binding_mode mismatch")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in FORBIDDEN_APPROVAL_FIELDS:
        _expect(review_package.get(field), None, field)
    _expect_true(review_package.get("created_offline"), "created_offline")
    _expect_true(review_package.get("read_only_discovery"), "read_only_discovery")
    for field in (
        "provider_requests_made_in_review",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "software_runtime_migration_authorized",
        "software_runtime_activation_authorized",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), discovery.NOT_AUTHORIZED, field)
    _expect(
        review_package.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "reviewed_discovery_candidate_kind": discovery.ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE,
        "reviewed_discovery_candidate_status": discovery.READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW,
        "reviewed_discovery_candidate_digest": EXPECTED_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_DIGEST,
        "reviewed_discovery_checklist_total": EXPECTED_DISCOVERY_CHECKLIST_TOTAL,
        "reviewed_discovery_checklist_passed": EXPECTED_DISCOVERY_CHECKLIST_PASSED,
        "reviewed_discovery_checklist_failed": EXPECTED_DISCOVERY_CHECKLIST_FAILED,
        "reviewed_discovery_blocker_count": EXPECTED_DISCOVERY_BLOCKER_COUNT,
        "registry_entry_count": 2,
        "available_dataset_file_count": 2,
        "available_manifest_file_count": 2,
        "verified_dataset_digest_count": 2,
        "verified_manifest_digest_count": 2,
        "missing_file_count": 0,
        "runtime_migration_plan_digest": discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "runtime_migration_review_package_digest": discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
    }.items():
        _expect(review_package.get(field), expected, field)
    _validate_registry_entries(review_package)
    _expect(review_package.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ReadOnlyRegistryDiscoveryOperatorReviewError("review_checklist must be a list")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _build_checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise ReadOnlyRegistryDiscoveryOperatorReviewError(
            f"read-only discovery review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    summary = _summary(checklist)
    _expect(review_package.get("review_summary"), summary, "review_summary")
    _expect_true(summary.get("ready_for_operator_assessment"), "ready_for_operator_assessment")
    _expect_true(
        summary.get("operator_decision_required_before_next_gate"),
        "operator_decision_required_before_next_gate",
    )
    _expect_false(summary.get("software_runtime_migration_authorized"), "software_runtime_migration_authorized")
    _expect_false(summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    digest = review_package.get("read_only_registry_discovery_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ReadOnlyRegistryDiscoveryOperatorReviewError(
            "read_only_registry_discovery_review_package_digest missing"
        )
    _expect(
        digest,
        read_only_registry_discovery_review_package_digest_v1(review_package),
        "read_only_registry_discovery_review_package_digest",
    )
    return {
        "status": "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "read_only_registry_discovery_review_package_digest": digest,
        "reviewed_discovery_candidate_digest": EXPECTED_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_DIGEST,
        "registry_entry_count": 2,
        "available_dataset_file_count": 2,
        "available_manifest_file_count": 2,
        "verified_dataset_digest_count": 2,
        "verified_manifest_digest_count": 2,
        "missing_file_count": 0,
        "runtime_migration_plan_digest": discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "runtime_migration_review_package_digest": discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": discovery.NOT_AUTHORIZED,
        "strategy_use": discovery.NOT_AUTHORIZED,
        "paper_trading": discovery.NOT_AUTHORIZED,
        "broker_execution": discovery.NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_read_only_registry_discovery_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized read-only registry discovery review package status document."""
    validation = validate_read_only_registry_discovery_candidate_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Read-Only Registry Discovery Operator Review Package Status",
        "",
        "## Title",
        "- Read-Only Registry Discovery Operator Review Package v1.",
        "",
        "## Reviewed Read-Only Discovery Candidate",
        f"- Review package artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Binding mode: `{review_package['binding_mode']}`",
        f"- Reviewed discovery candidate kind: `{review_package['reviewed_discovery_candidate_kind']}`",
        f"- Reviewed discovery candidate status: `{review_package['reviewed_discovery_candidate_status']}`",
        f"- Reviewed discovery candidate digest: `{review_package['reviewed_discovery_candidate_digest']}`",
        "",
        "## Discovered Registry Entries",
    ]
    for entry in review_package["registry_entries"]:
        lines.extend(
            [
                f"- `{entry['registry_key']}`",
                f"  - Registry scope: `{entry['registry_scope']}`",
                f"  - Registry approval digest: `{entry['registry_approval_digest']}`",
                f"  - Runtime use: `{entry['runtime_use']}`",
                f"  - Strategy use: `{entry['strategy_use']}`",
            ]
        )
    lines.extend(["", "## Dataset File Availability"])
    for entry in review_package["registry_entries"]:
        lines.extend(
            [
                f"- `{entry['dataset_profile']}` dataset file status: `{entry['dataset_file_status']}`",
                f"- `{entry['dataset_profile']}` manifest file status: `{entry['manifest_file_status']}`",
            ]
        )
    lines.extend(["", "## Digest Verification"])
    for entry in review_package["registry_entries"]:
        lines.extend(
            [
                f"- `{entry['dataset_profile']}` dataset digest verified: `{entry['dataset_digest_verified']}`",
                f"- `{entry['dataset_profile']}` manifest digest verified: `{entry['manifest_digest_verified']}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{review_package['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{review_package['strategy_runtime_migration']}`",
            f"- runtime_use: `{review_package['runtime_use']}`",
            f"- strategy_use: `{review_package['strategy_use']}`",
            f"- paper_trading: `{review_package['paper_trading']}`",
            f"- broker_execution: `{review_package['broker_execution']}`",
            f"- automatic_stitching: `{review_package['automatic_stitching']}`",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- profitability: `{review_package['profitability']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Runtime migration authorized: `{summary['software_runtime_migration_authorized']}`",
            f"- Runtime activation authorized: `{summary['software_runtime_activation_authorized']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(review_package["remaining_required_tasks"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made in review: `False`",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No acquisition rows, SWING bars, or POSITION_SWING bars were regenerated.",
            "- No runtime default source was changed.",
            "- No `RUNTIME_MIGRATION_APPROVED`, `RUNTIME_MIGRATION_ACTIVE`, or `STRATEGY_RUNTIME_MIGRATION` artifact or status is created.",
            "- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
            "## Review Package Digest",
            f"- Review package digest: `{validation['read_only_registry_discovery_review_package_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_read_only_registry_discovery_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    discovery_candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the read-only discovery review package JSON artifact without overwriting output."""
    review_package = build_read_only_registry_discovery_candidate_review_package_v1(discovery_candidate)
    validation = validate_read_only_registry_discovery_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "read_only_registry_discovery_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ReadOnlyRegistryDiscoveryOperatorReviewError(
            "read-only registry discovery review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ReadOnlyRegistryDiscoveryOperatorReviewError(
            "read-only registry discovery review output already exists"
        )
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
