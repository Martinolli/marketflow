"""Offline operator-review package for dataset file availability verification."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dataset_file_availability_verification_service as verification


ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE = (
    "DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE"
)
SCHEMA_VERSION_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_V1 = (
    "dataset_file_availability_verification_review_v1"
)
DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_READY = (
    "DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_READY"
)
DATASET_FILE_AVAILABILITY_VERIFICATION_STATUS_BINDING = (
    "DATASET_FILE_AVAILABILITY_VERIFICATION_STATUS_BINDING"
)
DATASET_FILE_AVAILABILITY_VERIFICATION_OBJECT_BINDING = (
    "DATASET_FILE_AVAILABILITY_VERIFICATION_OBJECT_BINDING"
)

EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST = (
    "8ba7db3aa50eb858f7eebb10eb6ee1a554a97b43a789c93460ff276cadc96751"
)
EXPECTED_VERIFICATION_CHECKLIST_TOTAL = len(verification.REQUIRED_CHECK_IDS)
EXPECTED_VERIFICATION_CHECKLIST_PASSED = len(verification.REQUIRED_CHECK_IDS)
EXPECTED_VERIFICATION_CHECKLIST_FAILED = 0
EXPECTED_VERIFICATION_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "verification_package_kind_matches",
    "verification_package_status_ready_for_review",
    "verification_package_digest_matches",
    "verification_package_checklist_zero_blockers",
    "verification_entry_count_two",
    "dataset_files_available_count_two",
    "manifest_files_available_count_two",
    "dataset_digests_verified_count_two",
    "manifest_digests_verified_count_two",
    "missing_file_count_zero",
    "digest_mismatch_count_zero",
    "swing_dataset_available_and_verified",
    "swing_manifest_available_and_verified",
    "position_swing_dataset_available_and_verified",
    "position_swing_manifest_available_and_verified",
    "read_only_discovery_candidate_digest_bound",
    "read_only_discovery_review_package_digest_bound",
    "runtime_plan_digest_bound",
    "runtime_review_package_digest_bound",
    "ready_for_research_campaign_planning_true",
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


class DatasetFileAvailabilityVerificationOperatorReviewError(ValueError):
    """Raised when a dataset availability review package violates guardrails."""


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
        raise DatasetFileAvailabilityVerificationOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise DatasetFileAvailabilityVerificationOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise DatasetFileAvailabilityVerificationOperatorReviewError(f"{field_name} must be true")


def _review_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_V1,
        "review_status": DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_READY,
        "operator_decision_required": True,
        "operator_decision": None,
        "operator_approved_by": None,
        "operator_approval_timestamp": None,
        "operator_approval_digest": None,
        "operator_signature": None,
        "approval_status": None,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": verification.NOT_AUTHORIZED,
        "strategy_use": verification.NOT_AUTHORIZED,
        "paper_trading": verification.NOT_AUTHORIZED,
        "broker_execution": verification.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _status_for_dataset_entry(entry: dict[str, Any]) -> str:
    if entry.get("dataset_file_exists") is True and entry.get("dataset_rows_digest_match") is True:
        return verification.AVAILABLE_AND_DIGEST_VERIFIED
    return entry.get("file_availability_status")


def _status_for_manifest_entry(entry: dict[str, Any]) -> str:
    if entry.get("manifest_file_exists") is True and entry.get("dataset_manifest_digest_match") is True:
        return verification.AVAILABLE_AND_DIGEST_VERIFIED
    return entry.get("file_availability_status")


def _file_entry_from_verification_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "registry_key": entry["registry_key"],
        "dataset_profile": entry["dataset_profile"],
        "dataset_bar_rule": entry["dataset_bar_rule"],
        "dataset_path": entry["dataset_path"],
        "manifest_path": entry["manifest_path"],
        "registry_approval_digest": entry["registry_approval_digest"],
        "dataset_rows_digest": entry["dataset_rows_digest_expected"],
        "dataset_manifest_digest": entry["dataset_manifest_digest_expected"],
        "dataset_file_status": _status_for_dataset_entry(entry),
        "manifest_file_status": _status_for_manifest_entry(entry),
        "dataset_rows_digest_match": entry["dataset_rows_digest_match"],
        "dataset_manifest_digest_match": entry["dataset_manifest_digest_match"],
        "dataset_file_sha256": entry.get("dataset_file_sha256"),
        "manifest_file_sha256": entry.get("manifest_file_sha256"),
        "runtime_use": verification.NOT_AUTHORIZED,
        "strategy_use": verification.NOT_AUTHORIZED,
    }


def _recorded_file_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for definition in verification.discovery._registry_definitions():
        entries.append(
            {
                "registry_key": definition["registry_key"],
                "dataset_profile": definition["dataset_profile"],
                "dataset_bar_rule": definition["dataset_bar_rule"],
                "dataset_path": definition["expected_dataset_path"],
                "manifest_path": definition["expected_manifest_path"],
                "registry_approval_digest": definition["registry_approval_digest"],
                "dataset_rows_digest": definition["dataset_rows_digest"],
                "dataset_manifest_digest": definition["dataset_manifest_digest"],
                "dataset_file_status": verification.AVAILABLE_AND_DIGEST_VERIFIED,
                "manifest_file_status": verification.AVAILABLE_AND_DIGEST_VERIFIED,
                "dataset_rows_digest_match": True,
                "dataset_manifest_digest_match": True,
                "runtime_use": verification.NOT_AUTHORIZED,
                "strategy_use": verification.NOT_AUTHORIZED,
            }
        )
    return entries


def _verification_evidence_from_package(verification_package: dict[str, Any]) -> dict[str, Any]:
    try:
        validation = verification.validate_dataset_file_availability_verification_package_v1(
            verification_package
        )
    except verification.DatasetFileAvailabilityVerificationError as exc:
        raise DatasetFileAvailabilityVerificationOperatorReviewError(
            f"source dataset file availability verification package invalid: {exc}"
        ) from exc
    summary = verification_package["verification_summary"]
    return {
        "reviewed_verification_package_kind": verification_package["artifact_kind"],
        "reviewed_verification_package_status": verification_package["package_status"],
        "reviewed_verification_package_digest": validation[
            "dataset_file_availability_verification_package_digest"
        ],
        "reviewed_verification_checklist_total": validation["total_checks"],
        "reviewed_verification_checklist_passed": validation["passed_checks"],
        "reviewed_verification_checklist_failed": validation["failed_checks"],
        "reviewed_verification_blocker_count": validation["blocker_count"],
        "verification_entry_count": summary["verification_entry_count"],
        "dataset_files_available_count": summary["dataset_files_available_count"],
        "manifest_files_available_count": summary["manifest_files_available_count"],
        "dataset_digests_verified_count": summary["dataset_digests_verified_count"],
        "manifest_digests_verified_count": summary["manifest_digests_verified_count"],
        "missing_file_count": summary["missing_file_count"],
        "digest_mismatch_count": summary["digest_mismatch_count"],
        "ready_for_research_campaign_planning": summary["ready_for_research_campaign_planning"],
        "read_only_discovery_candidate_digest": verification_package[
            "read_only_discovery_candidate_digest"
        ],
        "read_only_discovery_review_package_digest": verification_package[
            "read_only_discovery_review_package_digest"
        ],
        "runtime_migration_plan_digest": verification.discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "runtime_migration_review_package_digest": (
            verification.discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
        ),
        "verification_entries": [
            _file_entry_from_verification_entry(entry)
            for entry in verification_package["verification_entries"]
        ],
    }


def _recorded_verification_evidence() -> dict[str, Any]:
    return {
        "reviewed_verification_package_kind": (
            verification.ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE
        ),
        "reviewed_verification_package_status": (
            verification.DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_verification_package_digest": (
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST
        ),
        "reviewed_verification_checklist_total": EXPECTED_VERIFICATION_CHECKLIST_TOTAL,
        "reviewed_verification_checklist_passed": EXPECTED_VERIFICATION_CHECKLIST_PASSED,
        "reviewed_verification_checklist_failed": EXPECTED_VERIFICATION_CHECKLIST_FAILED,
        "reviewed_verification_blocker_count": EXPECTED_VERIFICATION_BLOCKER_COUNT,
        "verification_entry_count": 2,
        "dataset_files_available_count": 2,
        "manifest_files_available_count": 2,
        "dataset_digests_verified_count": 2,
        "manifest_digests_verified_count": 2,
        "missing_file_count": 0,
        "digest_mismatch_count": 0,
        "ready_for_research_campaign_planning": True,
        "read_only_discovery_candidate_digest": verification.EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST,
        "read_only_discovery_review_package_digest": (
            verification.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
        ),
        "runtime_migration_plan_digest": verification.discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
        "runtime_migration_review_package_digest": (
            verification.discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
        ),
        "verification_entries": _recorded_file_entries(),
    }


def _entry_by_profile(review_package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        entry.get("dataset_profile"): entry
        for entry in review_package.get("verification_entries") or []
        if isinstance(entry, dict)
    }


def _build_checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    by_profile = _entry_by_profile(review_package)
    swing_entry = by_profile.get("SWING") or {}
    position_entry = by_profile.get("POSITION_SWING") or {}
    return [
        _check(
            "verification_package_kind_matches",
            verification.ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE,
            review_package.get("reviewed_verification_package_kind"),
        ),
        _check(
            "verification_package_status_ready_for_review",
            verification.DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW,
            review_package.get("reviewed_verification_package_status"),
        ),
        _check(
            "verification_package_digest_matches",
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST,
            review_package.get("reviewed_verification_package_digest"),
        ),
        _check(
            "verification_package_checklist_zero_blockers",
            {
                "total": EXPECTED_VERIFICATION_CHECKLIST_TOTAL,
                "passed": EXPECTED_VERIFICATION_CHECKLIST_PASSED,
                "failed": EXPECTED_VERIFICATION_CHECKLIST_FAILED,
                "blockers": EXPECTED_VERIFICATION_BLOCKER_COUNT,
            },
            {
                "total": review_package.get("reviewed_verification_checklist_total"),
                "passed": review_package.get("reviewed_verification_checklist_passed"),
                "failed": review_package.get("reviewed_verification_checklist_failed"),
                "blockers": review_package.get("reviewed_verification_blocker_count"),
            },
        ),
        _check("verification_entry_count_two", 2, review_package.get("verification_entry_count")),
        _check("dataset_files_available_count_two", 2, review_package.get("dataset_files_available_count")),
        _check("manifest_files_available_count_two", 2, review_package.get("manifest_files_available_count")),
        _check("dataset_digests_verified_count_two", 2, review_package.get("dataset_digests_verified_count")),
        _check("manifest_digests_verified_count_two", 2, review_package.get("manifest_digests_verified_count")),
        _check("missing_file_count_zero", 0, review_package.get("missing_file_count")),
        _check("digest_mismatch_count_zero", 0, review_package.get("digest_mismatch_count")),
        _check(
            "swing_dataset_available_and_verified",
            verification.AVAILABLE_AND_DIGEST_VERIFIED,
            swing_entry.get("dataset_file_status"),
        ),
        _check(
            "swing_manifest_available_and_verified",
            verification.AVAILABLE_AND_DIGEST_VERIFIED,
            swing_entry.get("manifest_file_status"),
        ),
        _check(
            "position_swing_dataset_available_and_verified",
            verification.AVAILABLE_AND_DIGEST_VERIFIED,
            position_entry.get("dataset_file_status"),
        ),
        _check(
            "position_swing_manifest_available_and_verified",
            verification.AVAILABLE_AND_DIGEST_VERIFIED,
            position_entry.get("manifest_file_status"),
        ),
        _check(
            "read_only_discovery_candidate_digest_bound",
            verification.EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST,
            review_package.get("read_only_discovery_candidate_digest"),
        ),
        _check(
            "read_only_discovery_review_package_digest_bound",
            verification.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST,
            review_package.get("read_only_discovery_review_package_digest"),
        ),
        _check(
            "runtime_plan_digest_bound",
            verification.discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST,
            review_package.get("runtime_migration_plan_digest"),
        ),
        _check(
            "runtime_review_package_digest_bound",
            verification.discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST,
            review_package.get("runtime_migration_review_package_digest"),
        ),
        _check(
            "ready_for_research_campaign_planning_true",
            True,
            review_package.get("ready_for_research_campaign_planning"),
        ),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", verification.NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", verification.NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", verification.NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", verification.NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check(
            "predictive_usefulness_not_accepted",
            acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            review_package.get("predictive_usefulness"),
            severity=INFO,
        ),
        _check(
            "profitability_not_accepted",
            acquisition.PROFITABILITY_NOT_ACCEPTED,
            review_package.get("profitability"),
            severity=INFO,
        ),
        _check(
            "provider_requests_made_in_review_false",
            False,
            review_package.get("provider_requests_made_in_review"),
        ),
        _check(
            "no_runtime_activation_artifact_created",
            {
                "artifact_kind_is_review_package": True,
                "review_status_is_review_ready": True,
                "approval_status_is_null": True,
                "runtime_migration_approved_is_false": True,
                "runtime_migration_active_is_false": True,
            },
            {
                "artifact_kind_is_review_package": review_package.get("artifact_kind")
                == ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE,
                "review_status_is_review_ready": review_package.get("review_status")
                == DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_READY,
                "approval_status_is_null": review_package.get("approval_status") is None,
                "runtime_migration_approved_is_false": review_package.get("runtime_migration_approved") is False,
                "runtime_migration_active_is_false": review_package.get("runtime_migration_active") is False,
            },
        ),
    ]


def _summary(checklist: list[dict[str, Any]], review_package: dict[str, Any]) -> dict[str, Any]:
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
        "ready_for_research_campaign_planning": review_package.get(
            "ready_for_research_campaign_planning"
        )
        is True,
        "operator_decision_required_before_next_gate": True,
        "software_runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("dataset_file_availability_verification_review_package_digest", None)
    return payload


def dataset_file_availability_verification_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for a dataset availability review package."""
    return semantic_digest(_digest_payload(review_package))


def build_dataset_file_availability_verification_review_package_v1(
    verification_package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline operator review package for dataset file availability."""
    binding_mode = DATASET_FILE_AVAILABILITY_VERIFICATION_STATUS_BINDING
    evidence = _recorded_verification_evidence()
    if verification_package is not None:
        binding_mode = DATASET_FILE_AVAILABILITY_VERIFICATION_OBJECT_BINDING
        evidence = _verification_evidence_from_package(verification_package)
    review_package = {
        **_review_context(),
        "binding_mode": binding_mode,
        **evidence,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }
    checklist = _build_checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist, review_package)
    review_package["dataset_file_availability_verification_review_package_digest"] = (
        dataset_file_availability_verification_review_package_digest_v1(review_package)
    )
    validate_dataset_file_availability_verification_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise DatasetFileAvailabilityVerificationOperatorReviewError(
                f"{current_path} must not emit {value}"
            )
        if key in FORBIDDEN_APPROVAL_FIELDS and value is not None:
            raise DatasetFileAvailabilityVerificationOperatorReviewError(f"{current_path} must be null")
        if key in {
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
        } and value is True:
            raise DatasetFileAvailabilityVerificationOperatorReviewError(f"{current_path} must be false")
        if key in {
            "runtime_use",
            "strategy_use",
            "paper_trading",
            "broker_execution",
        } and value == "AUTHORIZED":
            raise DatasetFileAvailabilityVerificationOperatorReviewError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise DatasetFileAvailabilityVerificationOperatorReviewError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_verification_entries(review_package: dict[str, Any]) -> None:
    entries = review_package.get("verification_entries")
    if not isinstance(entries, list) or len(entries) != 2:
        raise DatasetFileAvailabilityVerificationOperatorReviewError(
            "verification entry count must be 2"
        )
    by_profile = _entry_by_profile(review_package)
    if "SWING" not in by_profile:
        raise DatasetFileAvailabilityVerificationOperatorReviewError("missing SWING verification entry")
    if "POSITION_SWING" not in by_profile:
        raise DatasetFileAvailabilityVerificationOperatorReviewError(
            "missing POSITION_SWING verification entry"
        )
    expected_by_profile = {
        entry["dataset_profile"]: entry for entry in verification.discovery._registry_definitions()
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
            "dataset_rows_digest": expected["dataset_rows_digest"],
            "dataset_manifest_digest": expected["dataset_manifest_digest"],
            "dataset_file_status": verification.AVAILABLE_AND_DIGEST_VERIFIED,
            "manifest_file_status": verification.AVAILABLE_AND_DIGEST_VERIFIED,
            "dataset_rows_digest_match": True,
            "dataset_manifest_digest_match": True,
            "runtime_use": verification.NOT_AUTHORIZED,
            "strategy_use": verification.NOT_AUTHORIZED,
        }.items():
            _expect(entry.get(field), expected_value, field)


def validate_dataset_file_availability_verification_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate a dataset availability review package without granting runtime authority."""
    if not isinstance(review_package, dict):
        raise DatasetFileAvailabilityVerificationOperatorReviewError(
            "dataset file availability verification review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("binding_mode") not in {
        DATASET_FILE_AVAILABILITY_VERIFICATION_STATUS_BINDING,
        DATASET_FILE_AVAILABILITY_VERIFICATION_OBJECT_BINDING,
    }:
        raise DatasetFileAvailabilityVerificationOperatorReviewError("binding_mode mismatch")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in FORBIDDEN_APPROVAL_FIELDS:
        _expect(review_package.get(field), None, field)
    _expect_true(review_package.get("created_offline"), "created_offline")
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
        _expect(review_package.get(field), verification.NOT_AUTHORIZED, field)
    _expect(
        review_package.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "reviewed_verification_package_kind": (
            verification.ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE
        ),
        "reviewed_verification_package_status": (
            verification.DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_verification_package_digest": (
            EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST
        ),
        "reviewed_verification_checklist_total": EXPECTED_VERIFICATION_CHECKLIST_TOTAL,
        "reviewed_verification_checklist_passed": EXPECTED_VERIFICATION_CHECKLIST_PASSED,
        "reviewed_verification_checklist_failed": EXPECTED_VERIFICATION_CHECKLIST_FAILED,
        "reviewed_verification_blocker_count": EXPECTED_VERIFICATION_BLOCKER_COUNT,
        "verification_entry_count": 2,
        "dataset_files_available_count": 2,
        "manifest_files_available_count": 2,
        "dataset_digests_verified_count": 2,
        "manifest_digests_verified_count": 2,
        "missing_file_count": 0,
        "digest_mismatch_count": 0,
        "ready_for_research_campaign_planning": True,
        "read_only_discovery_candidate_digest": (
            verification.EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST
        ),
        "read_only_discovery_review_package_digest": (
            verification.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
        ),
        "runtime_migration_plan_digest": (
            verification.discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST
        ),
        "runtime_migration_review_package_digest": (
            verification.discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
        ),
    }.items():
        _expect(review_package.get(field), expected, field)
    _validate_verification_entries(review_package)
    _expect(review_package.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise DatasetFileAvailabilityVerificationOperatorReviewError("review_checklist must be a list")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _build_checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise DatasetFileAvailabilityVerificationOperatorReviewError(
            f"dataset file availability verification review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    summary = _summary(checklist, review_package)
    _expect(review_package.get("review_summary"), summary, "review_summary")
    _expect_true(summary.get("ready_for_operator_assessment"), "ready_for_operator_assessment")
    _expect_true(
        summary.get("ready_for_research_campaign_planning"),
        "ready_for_research_campaign_planning",
    )
    _expect_true(
        summary.get("operator_decision_required_before_next_gate"),
        "operator_decision_required_before_next_gate",
    )
    _expect_false(summary.get("software_runtime_migration_authorized"), "software_runtime_migration_authorized")
    _expect_false(summary.get("software_runtime_activation_authorized"), "software_runtime_activation_authorized")
    digest = review_package.get("dataset_file_availability_verification_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise DatasetFileAvailabilityVerificationOperatorReviewError(
            "dataset_file_availability_verification_review_package_digest missing"
        )
    _expect(
        digest,
        dataset_file_availability_verification_review_package_digest_v1(review_package),
        "dataset_file_availability_verification_review_package_digest",
    )
    return {
        "status": "DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "dataset_file_availability_verification_review_package_digest": digest,
        "reviewed_verification_package_digest": EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST,
        "verification_entry_count": 2,
        "dataset_files_available_count": 2,
        "manifest_files_available_count": 2,
        "dataset_digests_verified_count": 2,
        "manifest_digests_verified_count": 2,
        "missing_file_count": 0,
        "digest_mismatch_count": 0,
        "ready_for_research_campaign_planning": True,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": verification.NOT_AUTHORIZED,
        "strategy_use": verification.NOT_AUTHORIZED,
        "paper_trading": verification.NOT_AUTHORIZED,
        "broker_execution": verification.NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_dataset_file_availability_verification_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized dataset availability verification review status document."""
    validation = validate_dataset_file_availability_verification_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Dataset File Availability Verification Operator Review Package Status",
        "",
        "## Title",
        "- Dataset File Availability Verification Operator Review Package v1.",
        "",
        "## Reviewed Dataset File Availability Verification",
        f"- Review package artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Binding mode: `{review_package['binding_mode']}`",
        f"- Reviewed verification package kind: `{review_package['reviewed_verification_package_kind']}`",
        f"- Reviewed verification package status: `{review_package['reviewed_verification_package_status']}`",
        f"- Reviewed verification package digest: `{review_package['reviewed_verification_package_digest']}`",
        "",
        "## Verified Files",
    ]
    for entry in review_package["verification_entries"]:
        lines.extend(
            [
                f"- `{entry['registry_key']}`",
                f"  - Dataset path: `{entry['dataset_path']}`",
                f"  - Manifest path: `{entry['manifest_path']}`",
                f"  - Dataset file status: `{entry['dataset_file_status']}`",
                f"  - Manifest file status: `{entry['manifest_file_status']}`",
            ]
        )
    lines.extend(["", "## Digest Verification Summary"])
    for entry in review_package["verification_entries"]:
        lines.extend(
            [
                f"- `{entry['dataset_profile']}` dataset rows digest: `{entry['dataset_rows_digest']}`",
                f"- `{entry['dataset_profile']}` dataset manifest digest: `{entry['dataset_manifest_digest']}`",
            ]
        )
    lines.extend(
        [
            f"- Dataset digests verified: `{review_package['dataset_digests_verified_count']}`",
            f"- Manifest digests verified: `{review_package['manifest_digests_verified_count']}`",
            f"- Missing files: `{review_package['missing_file_count']}`",
            f"- Digest mismatches: `{review_package['digest_mismatch_count']}`",
            f"- Ready for research campaign planning: `{review_package['ready_for_research_campaign_planning']}`",
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
            f"- Review package digest: `{validation['dataset_file_availability_verification_review_package_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_dataset_file_availability_verification_review_package_v1(
    output_dir: str | Path,
    *,
    verification_package: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the dataset availability verification review package without overwriting output."""
    review_package = build_dataset_file_availability_verification_review_package_v1(
        verification_package
    )
    validation = validate_dataset_file_availability_verification_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "dataset_file_availability_verification_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise DatasetFileAvailabilityVerificationOperatorReviewError(
            "dataset file availability verification review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise DatasetFileAvailabilityVerificationOperatorReviewError(
            "dataset file availability verification review output already exists"
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
