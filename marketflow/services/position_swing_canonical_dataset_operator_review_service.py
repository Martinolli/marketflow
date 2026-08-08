"""Offline operator-review package for POSITION_SWING canonical dataset candidates."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import position_swing_canonical_dataset_service as position


ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE = (
    "POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_V1 = (
    "position_swing_canonical_dataset_candidate_review_v1"
)
POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY = (
    "POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY"
)
POSITION_SWING_CANONICAL_DATASET_CANDIDATE_STATUS_BINDING = (
    "POSITION_SWING_CANONICAL_DATASET_CANDIDATE_STATUS_BINDING"
)
POSITION_SWING_CANONICAL_DATASET_CANDIDATE_OBJECT_BINDING = (
    "POSITION_SWING_CANONICAL_DATASET_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_POSITION_SWING_CANDIDATE_DIGEST = (
    "ed16a41304a4d3838f495124a9d491e834eba0dd4a1ff8009e456963ecc2c916"
)
EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST = (
    "163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3"
)
EXPECTED_POSITION_SWING_DATASET_MANIFEST_DIGEST = (
    "720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba"
)
EXPECTED_SOURCE_ROWS_DIGEST = position.EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST
EXPECTED_MATERIALIZATION_RECEIPT_DIGEST = position.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST
EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST = position.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST
EXPECTED_POSITION_SWING_BAR_COUNT = 994
EXPECTED_SOURCE_RTH_ROWS_CONSUMED = 25844
EXPECTED_SOURCE_RTH_ROWS_EXCLUDED = 126
EXPECTED_FULL_SESSIONS_USED = 994
EXPECTED_SPECIAL_SESSIONS_EXCLUDED = 9
EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED = 126
EXPECTED_CROSS_CHECK_MONTH = "2025-01"
EXPECTED_CROSS_CHECK_STATUS = "PASSED"
EXPECTED_CROSS_CHECK_POSITION_SWING_BARS = 20

DEFAULT_POSITION_SWING_REVIEW_PACKAGE_OUTPUT_DIR = Path("docs") / "status"
DEFAULT_POSITION_SWING_DATASET_PATH = (
    position.DEFAULT_POSITION_SWING_CANDIDATE_OUTPUT_ROOT
    / "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv"
)
DEFAULT_POSITION_SWING_MANIFEST_PATH = (
    position.DEFAULT_POSITION_SWING_CANDIDATE_OUTPUT_ROOT
    / "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_manifest.json"
)
DEFAULT_POSITION_SWING_CANDIDATE_PATH = (
    position.DEFAULT_POSITION_SWING_CANDIDATE_OUTPUT_ROOT
    / "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_candidate.json"
)

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
HIGH = "HIGH"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "candidate_kind_is_position_swing_canonical_dataset_candidate",
    "candidate_status_ready_for_operator_review",
    "candidate_digest_matches",
    "dataset_profile_matches_position_swing",
    "dataset_bar_rule_matches_rth_full_session_1d",
    "dataset_rows_digest_matches",
    "dataset_manifest_digest_matches",
    "source_rows_digest_matches",
    "materialization_receipt_digest_matches",
    "acquisition_frozen_digest_matches",
    "identity_frozen_digest_matches",
    "calendar_frozen_digest_matches",
    "schedule_digest_matches",
    "split_event_frozen_digest_matches",
    "dividend_event_frozen_digest_matches",
    "position_swing_bar_count_994",
    "source_rth_rows_consumed_25844",
    "source_rth_rows_excluded_126",
    "full_sessions_used_994",
    "special_sessions_excluded_9",
    "special_session_rows_excluded_126",
    "special_session_policy_full_ordinary_only",
    "special_sessions_recorded_in_exclusion_inventory",
    "cross_check_2025_01_passed",
    "cross_check_2025_01_position_swing_bars_20",
    "dividend_implication_preserved",
    "position_swing_canonical_dataset_frozen_false",
    "position_swing_registry_approval_created_false",
    "position_swing_registry_eligibility_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "provider_requests_made_in_review_false",
    "no_position_swing_canonical_dataset_frozen_artifact_created",
    "no_position_swing_registry_approval_created",
]

REMAINING_ROADMAP = [
    "Digest-bound POSITION_SWING canonical dataset operator freeze ceremony.",
    "POSITION_SWING registry approval candidate.",
    "POSITION_SWING registry operator review package.",
    "POSITION_SWING registry approval ceremony.",
    "Normal runtime migration planning.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
]

FORBIDDEN_FREEZE_FIELDS = frozenset(
    {
        "operator_approved_by",
        "operator_freeze_timestamp",
        "operator_freeze_digest",
        "operator_signature",
    }
)


class PositionSwingCanonicalDatasetOperatorReviewError(ValueError):
    """Raised when a POSITION_SWING review package violates authority boundaries."""


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise PositionSwingCanonicalDatasetOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PositionSwingCanonicalDatasetOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PositionSwingCanonicalDatasetOperatorReviewError(f"{field_name} must be true")


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


def _fixed_segment() -> dict[str, Any]:
    segment = acquisition.FIXED_IDENTITY_SEGMENT
    return {
        "ticker": segment["ticker"],
        "composite_figi": segment["composite_figi"],
        "share_class_figi": segment["share_class_figi"],
        "primary_mic": segment["primary_mic"],
        "security_type": segment["security_type"],
        "segment_start": segment["segment_start"],
        "segment_end": segment["segment_end"],
    }


def _authority_bindings() -> dict[str, Any]:
    return {
        "identity_frozen_digest": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "calendar_frozen_digest": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_digest": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_frozen_digest": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_frozen_digest": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_generation_frozen_digest": EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
        "materialization_receipt_digest": EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        "normalized_source_rows_digest": EXPECTED_SOURCE_ROWS_DIGEST,
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        "source_adjusted_data_used": True,
        "fixed_segment": _fixed_segment(),
    }


def _authority_boundary() -> dict[str, Any]:
    return {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "acquisition_generation_freeze": True,
        "swing_canonical_dataset_frozen": True,
        "swing_registry_approval_created": True,
        "swing_registry_eligibility": True,
        "position_swing_canonical_dataset_frozen": False,
        "position_swing_registry_approval_created": False,
        "position_swing_registry_eligibility": False,
        "strategy_runtime_migration": False,
        "runtime_use": position.NOT_AUTHORIZED,
        "strategy_use": position.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def _recorded_candidate_evidence() -> dict[str, Any]:
    return {
        "reviewed_candidate_kind": position.ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE,
        "reviewed_candidate_status": position.POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW,
        "reviewed_candidate_digest": EXPECTED_POSITION_SWING_CANDIDATE_DIGEST,
        "reviewed_dataset_profile": position.DATASET_PROFILE_POSITION_SWING,
        "reviewed_dataset_bar_rule": position.DATASET_BAR_RULE_RTH_FULL_SESSION_1D,
        "reviewed_dataset_rows_digest": EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST,
        "reviewed_dataset_manifest_digest": EXPECTED_POSITION_SWING_DATASET_MANIFEST_DIGEST,
        "reviewed_source_rows_digest": EXPECTED_SOURCE_ROWS_DIGEST,
        "reviewed_materialization_receipt_digest": EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        "reviewed_acquisition_generation_frozen_digest": EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
        "position_swing_bar_count": EXPECTED_POSITION_SWING_BAR_COUNT,
        "source_rth_rows_consumed": EXPECTED_SOURCE_RTH_ROWS_CONSUMED,
        "source_rth_rows_excluded": EXPECTED_SOURCE_RTH_ROWS_EXCLUDED,
        "full_sessions_used": EXPECTED_FULL_SESSIONS_USED,
        "special_sessions_excluded": EXPECTED_SPECIAL_SESSIONS_EXCLUDED,
        "special_session_rows_excluded": EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED,
        "cross_check_month": EXPECTED_CROSS_CHECK_MONTH,
        "cross_check_status": EXPECTED_CROSS_CHECK_STATUS,
        "cross_check_position_swing_bars": EXPECTED_CROSS_CHECK_POSITION_SWING_BARS,
        "special_session_policy": "FULL_ORDINARY_SESSIONS_ONLY",
        "special_sessions_excluded_from_position_swing_bars": True,
        "special_sessions_recorded_in_exclusion_inventory": True,
        "special_session_exclusion_count": EXPECTED_SPECIAL_SESSIONS_EXCLUDED,
    }


def _candidate_evidence_from_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    try:
        validation = position.validate_position_swing_canonical_dataset_candidate_v1(candidate)
    except position.PositionSwingCanonicalDatasetError as exc:
        raise PositionSwingCanonicalDatasetOperatorReviewError(f"source POSITION_SWING candidate invalid: {exc}") from exc
    cross_check = candidate.get("2025_01_position_swing_cross_check") if isinstance(candidate, dict) else {}
    if not isinstance(cross_check, dict):
        cross_check = {}
    policy = candidate.get("special_session_policy") if isinstance(candidate, dict) else {}
    if not isinstance(policy, dict):
        policy = {}
    return {
        "reviewed_candidate_kind": candidate.get("artifact_kind"),
        "reviewed_candidate_status": candidate.get("candidate_status"),
        "reviewed_candidate_digest": validation["position_swing_candidate_semantic_digest"],
        "reviewed_dataset_profile": candidate.get("dataset_profile"),
        "reviewed_dataset_bar_rule": candidate.get("dataset_bar_rule"),
        "reviewed_dataset_rows_digest": candidate.get("dataset_rows_digest"),
        "reviewed_dataset_manifest_digest": candidate.get("dataset_manifest_digest"),
        "reviewed_source_rows_digest": candidate.get("normalized_source_rows_digest"),
        "reviewed_materialization_receipt_digest": candidate.get("materialization_receipt_digest"),
        "reviewed_acquisition_generation_frozen_digest": candidate.get("acquisition_generation_frozen_digest"),
        "position_swing_bar_count": candidate.get("position_swing_bar_count"),
        "source_rth_rows_consumed": candidate.get("source_rth_rows_consumed"),
        "source_rth_rows_excluded": candidate.get("source_rth_rows_excluded"),
        "full_sessions_used": candidate.get("full_sessions_used"),
        "special_sessions_excluded": candidate.get("special_sessions_excluded"),
        "special_session_rows_excluded": candidate.get("special_session_rows_excluded"),
        "cross_check_month": EXPECTED_CROSS_CHECK_MONTH,
        "cross_check_status": cross_check.get("cross_check_status"),
        "cross_check_position_swing_bars": cross_check.get("actual_position_swing_bars"),
        "special_session_policy": "FULL_ORDINARY_SESSIONS_ONLY"
        if policy.get("full_ordinary_sessions_only_for_RTH_FULL_SESSION_1D") is True
        else None,
        "special_sessions_excluded_from_position_swing_bars": policy.get(
            "special_sessions_excluded_from_position_swing_bars"
        ),
        "special_sessions_recorded_in_exclusion_inventory": policy.get(
            "special_sessions_recorded_in_exclusion_inventory"
        ),
        "special_session_exclusion_count": candidate.get("special_session_exclusion_count"),
    }


def _normalized_dataset_csv_row(row: dict[str, str]) -> dict[str, Any]:
    normalized: dict[str, Any] = dict(row)
    for field in ("source_row_count", "transactions"):
        value = normalized.get(field)
        if isinstance(value, str) and value:
            normalized[field] = int(value)
    return normalized


def _local_artifact_binding(
    *,
    dataset_path: Path = DEFAULT_POSITION_SWING_DATASET_PATH,
    manifest_path: Path = DEFAULT_POSITION_SWING_MANIFEST_PATH,
    candidate_path: Path = DEFAULT_POSITION_SWING_CANDIDATE_PATH,
) -> dict[str, Any]:
    manifest_available = manifest_path.exists()
    dataset_available = dataset_path.exists()
    candidate_available = candidate_path.exists()
    manifest_payload: dict[str, Any] | None = None
    manifest_digest: str | None = None
    dataset_rows: list[dict[str, Any]] | None = None
    dataset_row_count: int | None = None
    computed_dataset_rows_digest: str | None = None
    candidate_file_verified = False
    if manifest_available:
        loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise PositionSwingCanonicalDatasetOperatorReviewError("local POSITION_SWING manifest must be an object")
        manifest_payload = loaded
        manifest_digest = position.dataset_manifest_digest_v1(loaded)
    if dataset_available:
        with dataset_path.open("r", encoding="utf-8", newline="") as handle:
            dataset_rows = [_normalized_dataset_csv_row(row) for row in csv.DictReader(handle)]
        dataset_row_count = len(dataset_rows)
        computed_dataset_rows_digest = position.dataset_rows_digest_v1(dataset_rows)
    if candidate_available:
        loaded_candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        if not isinstance(loaded_candidate, dict):
            raise PositionSwingCanonicalDatasetOperatorReviewError("local POSITION_SWING candidate must be an object")
        try:
            validation = position.validate_position_swing_canonical_dataset_candidate_v1(loaded_candidate)
        except position.PositionSwingCanonicalDatasetError:
            candidate_file_verified = False
        else:
            candidate_file_verified = validation["position_swing_candidate_semantic_digest"] == EXPECTED_POSITION_SWING_CANDIDATE_DIGEST
    return {
        "candidate_path": str(candidate_path),
        "candidate_file_available": candidate_available,
        "candidate_file_verified": candidate_file_verified,
        "dataset_path": str(dataset_path),
        "dataset_file_available": dataset_available,
        "dataset_file_verified": bool(
            dataset_row_count == EXPECTED_POSITION_SWING_BAR_COUNT
            and computed_dataset_rows_digest == EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST
        ),
        "manifest_path": str(manifest_path),
        "manifest_file_available": manifest_available,
        "manifest_file_verified": bool(
            manifest_payload is not None
            and manifest_digest == EXPECTED_POSITION_SWING_DATASET_MANIFEST_DIGEST
            and manifest_payload.get("dataset_manifest_digest") == EXPECTED_POSITION_SWING_DATASET_MANIFEST_DIGEST
            and manifest_payload.get("dataset_rows_digest") == EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST
        ),
        "dataset_row_count": dataset_row_count,
        "computed_dataset_rows_digest": computed_dataset_rows_digest,
        "manifest_dataset_rows_digest": manifest_payload.get("dataset_rows_digest") if manifest_payload else None,
        "manifest_dataset_manifest_digest": manifest_payload.get("dataset_manifest_digest") if manifest_payload else None,
        "computed_manifest_digest": manifest_digest,
        "binding_mode_if_files_missing": POSITION_SWING_CANONICAL_DATASET_CANDIDATE_STATUS_BINDING,
    }


def _package_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE,
        "review_status": POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY,
        "operator_decision_required": True,
        "operator_decision": None,
        "canonical_dataset_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "position_swing_canonical_dataset_frozen": False,
        "position_swing_registry_approval_created": False,
        "position_swing_registry_eligibility": False,
        "strategy_runtime_migration": False,
        "runtime_use": position.NOT_AUTHORIZED,
        "strategy_use": position.NOT_AUTHORIZED,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "automatic_stitching": False,
        "software_freeze_authorized": False,
        "registry_approval_authorized": False,
        "runtime_migration_authorized": False,
        "position_swing_canonical_dataset_frozen_artifact_created": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "operator_approved_by": None,
        "operator_freeze_timestamp": None,
        "operator_freeze_digest": None,
        "operator_signature": None,
        "freeze_status": None,
    }


def _build_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = package["reviewed_position_swing_candidate_evidence"]
    bindings = package["authority_bindings"]
    boundary = package["authority_boundary"]
    return [
        _check("candidate_kind_is_position_swing_canonical_dataset_candidate", position.ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE, evidence["reviewed_candidate_kind"]),
        _check("candidate_status_ready_for_operator_review", position.POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW, evidence["reviewed_candidate_status"]),
        _check("candidate_digest_matches", EXPECTED_POSITION_SWING_CANDIDATE_DIGEST, evidence["reviewed_candidate_digest"]),
        _check("dataset_profile_matches_position_swing", position.DATASET_PROFILE_POSITION_SWING, evidence["reviewed_dataset_profile"]),
        _check("dataset_bar_rule_matches_rth_full_session_1d", position.DATASET_BAR_RULE_RTH_FULL_SESSION_1D, evidence["reviewed_dataset_bar_rule"]),
        _check("dataset_rows_digest_matches", EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST, evidence["reviewed_dataset_rows_digest"]),
        _check("dataset_manifest_digest_matches", EXPECTED_POSITION_SWING_DATASET_MANIFEST_DIGEST, evidence["reviewed_dataset_manifest_digest"]),
        _check("source_rows_digest_matches", EXPECTED_SOURCE_ROWS_DIGEST, evidence["reviewed_source_rows_digest"]),
        _check("materialization_receipt_digest_matches", EXPECTED_MATERIALIZATION_RECEIPT_DIGEST, evidence["reviewed_materialization_receipt_digest"]),
        _check("acquisition_frozen_digest_matches", EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST, evidence["reviewed_acquisition_generation_frozen_digest"]),
        _check("identity_frozen_digest_matches", acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, bindings["identity_frozen_digest"]),
        _check("calendar_frozen_digest_matches", acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, bindings["calendar_frozen_digest"]),
        _check("schedule_digest_matches", acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, bindings["schedule_digest"]),
        _check("split_event_frozen_digest_matches", acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, bindings["split_event_frozen_digest"]),
        _check("dividend_event_frozen_digest_matches", acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST, bindings["dividend_event_frozen_digest"]),
        _check("position_swing_bar_count_994", EXPECTED_POSITION_SWING_BAR_COUNT, evidence["position_swing_bar_count"]),
        _check("source_rth_rows_consumed_25844", EXPECTED_SOURCE_RTH_ROWS_CONSUMED, evidence["source_rth_rows_consumed"]),
        _check("source_rth_rows_excluded_126", EXPECTED_SOURCE_RTH_ROWS_EXCLUDED, evidence["source_rth_rows_excluded"]),
        _check("full_sessions_used_994", EXPECTED_FULL_SESSIONS_USED, evidence["full_sessions_used"]),
        _check("special_sessions_excluded_9", EXPECTED_SPECIAL_SESSIONS_EXCLUDED, evidence["special_sessions_excluded"]),
        _check("special_session_rows_excluded_126", EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED, evidence["special_session_rows_excluded"]),
        _check("special_session_policy_full_ordinary_only", "FULL_ORDINARY_SESSIONS_ONLY", evidence["special_session_policy"]),
        _check("special_sessions_recorded_in_exclusion_inventory", True, evidence["special_sessions_recorded_in_exclusion_inventory"]),
        _check("cross_check_2025_01_passed", EXPECTED_CROSS_CHECK_STATUS, evidence["cross_check_status"]),
        _check("cross_check_2025_01_position_swing_bars_20", EXPECTED_CROSS_CHECK_POSITION_SWING_BARS, evidence["cross_check_position_swing_bars"]),
        _check("dividend_implication_preserved", acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, bindings["in_range_dividend_implication"]),
        _check("position_swing_canonical_dataset_frozen_false", False, boundary["position_swing_canonical_dataset_frozen"]),
        _check("position_swing_registry_approval_created_false", False, boundary["position_swing_registry_approval_created"]),
        _check("position_swing_registry_eligibility_false", False, boundary["position_swing_registry_eligibility"]),
        _check("strategy_runtime_migration_false", False, boundary["strategy_runtime_migration"]),
        _check("runtime_use_not_authorized", position.NOT_AUTHORIZED, boundary["runtime_use"]),
        _check("strategy_use_not_authorized", position.NOT_AUTHORIZED, boundary["strategy_use"]),
        _check("automatic_stitching_false", False, boundary["automatic_stitching"]),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, boundary["predictive_usefulness"], severity=INFO),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, boundary["profitability"], severity=INFO),
        _check("provider_requests_made_in_review_false", False, package["provider_requests_made_in_review"]),
        _check(
            "no_position_swing_canonical_dataset_frozen_artifact_created",
            {"artifact_kind_is_not_frozen": True, "review_status_is_not_frozen": True, "freeze_status_is_null": True},
            {
                "artifact_kind_is_not_frozen": package.get("artifact_kind") != "POSITION_SWING_CANONICAL_DATASET_FROZEN",
                "review_status_is_not_frozen": package.get("review_status") != "POSITION_SWING_CANONICAL_DATASET_FROZEN",
                "freeze_status_is_null": package.get("freeze_status") is None,
            },
        ),
        _check("no_position_swing_registry_approval_created", False, boundary["position_swing_registry_approval_created"], severity=HIGH),
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
        "operator_decision_required_before_freeze": True,
        "software_freeze_authorized": False,
        "registry_approval_authorized": False,
        "runtime_migration_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("position_swing_canonical_dataset_review_package_semantic_digest", None)
    return payload


def position_swing_canonical_dataset_review_package_semantic_digest_v1(review_package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the POSITION_SWING review package."""
    return semantic_digest(_digest_payload(review_package))


def build_position_swing_canonical_dataset_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline, digest-bound operator review package for POSITION_SWING."""
    binding_mode = POSITION_SWING_CANONICAL_DATASET_CANDIDATE_STATUS_BINDING
    evidence = _recorded_candidate_evidence()
    if candidate is not None:
        binding_mode = POSITION_SWING_CANONICAL_DATASET_CANDIDATE_OBJECT_BINDING
        evidence = _candidate_evidence_from_candidate(candidate)
    package = {
        **_package_context(),
        "schema_version": SCHEMA_VERSION_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_V1,
        "binding_mode": binding_mode,
        "reviewed_position_swing_candidate_evidence": evidence,
        "local_artifact_binding": _local_artifact_binding(),
        "authority_bindings": _authority_bindings(),
        "authority_boundary": _authority_boundary(),
        "remaining_roadmap": list(REMAINING_ROADMAP),
    }
    checklist = _build_checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist)
    package["position_swing_canonical_dataset_review_package_semantic_digest"] = (
        position_swing_canonical_dataset_review_package_semantic_digest_v1(package)
    )
    validate_position_swing_canonical_dataset_candidate_review_package_v1(package)
    return package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key in {"registry_approval_created", "position_swing_registry_approval_created"} and value is not False:
            raise PositionSwingCanonicalDatasetOperatorReviewError(f"{current_path} must be false")
        if key == "position_swing_registry_eligibility" and value is not False:
            raise PositionSwingCanonicalDatasetOperatorReviewError(f"{current_path} must be false")
        if key in {"artifact_kind", "review_status", "candidate_status", "freeze_status"}:
            if value == "POSITION_SWING_CANONICAL_DATASET_FROZEN":
                raise PositionSwingCanonicalDatasetOperatorReviewError(
                    f"{current_path} must not emit POSITION_SWING_CANONICAL_DATASET_FROZEN"
                )
        if value == "POSITION_SWING_REGISTRY_APPROVED":
            raise PositionSwingCanonicalDatasetOperatorReviewError(
                f"{current_path} must not emit POSITION_SWING_REGISTRY_APPROVED"
            )
        if key in FORBIDDEN_FREEZE_FIELDS and value is not None:
            raise PositionSwingCanonicalDatasetOperatorReviewError(f"{current_path} must be null")
        if key == "freeze_status" and value is not None:
            raise PositionSwingCanonicalDatasetOperatorReviewError(f"{current_path} must be null")
        if key in {"runtime_use", "strategy_use"} and value == "AUTHORIZED":
            raise PositionSwingCanonicalDatasetOperatorReviewError(f"{current_path} must not be AUTHORIZED")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_position_swing_canonical_dataset_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate a POSITION_SWING review package without granting freeze or registry authority."""
    if not isinstance(review_package, dict):
        raise PositionSwingCanonicalDatasetOperatorReviewError("POSITION_SWING review package must be a JSON object")
    _reject_forbidden_values(review_package)
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY, "review_status")
    if review_package.get("binding_mode") not in {
        POSITION_SWING_CANONICAL_DATASET_CANDIDATE_STATUS_BINDING,
        POSITION_SWING_CANONICAL_DATASET_CANDIDATE_OBJECT_BINDING,
    }:
        raise PositionSwingCanonicalDatasetOperatorReviewError("binding_mode mismatch")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    _expect_true(review_package.get("created_offline"), "created_offline")
    for field in (
        "canonical_dataset_frozen",
        "canonical_eligibility",
        "registry_eligibility",
        "position_swing_canonical_dataset_frozen",
        "position_swing_registry_approval_created",
        "position_swing_registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
        "provider_requests_made_in_review",
        "software_freeze_authorized",
        "registry_approval_authorized",
        "runtime_migration_authorized",
        "position_swing_canonical_dataset_frozen_artifact_created",
    ):
        _expect_false(review_package.get(field), field)
    _expect(review_package.get("runtime_use"), position.NOT_AUTHORIZED, "runtime_use")
    _expect(review_package.get("strategy_use"), position.NOT_AUTHORIZED, "strategy_use")
    _expect(review_package.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field in FORBIDDEN_FREEZE_FIELDS:
        _expect(review_package.get(field), None, field)
    _expect(review_package.get("freeze_status"), None, "freeze_status")

    evidence = review_package.get("reviewed_position_swing_candidate_evidence")
    if not isinstance(evidence, dict):
        raise PositionSwingCanonicalDatasetOperatorReviewError("reviewed_position_swing_candidate_evidence must be an object")
    expected_evidence = _recorded_candidate_evidence()
    for field, expected in expected_evidence.items():
        _expect(evidence.get(field), expected, f"reviewed_position_swing_candidate_evidence.{field}")

    _expect(review_package.get("authority_bindings"), _authority_bindings(), "authority_bindings")
    _expect(review_package.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    _expect(review_package.get("remaining_roadmap"), REMAINING_ROADMAP, "remaining_roadmap")

    local_binding = review_package.get("local_artifact_binding")
    if not isinstance(local_binding, dict):
        raise PositionSwingCanonicalDatasetOperatorReviewError("local_artifact_binding must be an object")
    if local_binding.get("manifest_file_available") is True:
        _expect_true(local_binding.get("manifest_file_verified"), "manifest_file_verified")
    if local_binding.get("dataset_file_available") is True:
        _expect_true(local_binding.get("dataset_file_verified"), "dataset_file_verified")
    if local_binding.get("candidate_file_available") is True:
        _expect_true(local_binding.get("candidate_file_verified"), "candidate_file_verified")

    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PositionSwingCanonicalDatasetOperatorReviewError("review_checklist must be a list")
    check_ids = [item.get("check_id") for item in checklist if isinstance(item, dict)]
    _expect(check_ids, REQUIRED_CHECK_IDS, "review_checklist check IDs")
    _expect(checklist, _build_checklist(review_package), "review_checklist")
    failed = [item for item in checklist if item.get("status") != PASS]
    if failed:
        raise PositionSwingCanonicalDatasetOperatorReviewError("POSITION_SWING review package contains failed checks")
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    summary = review_package["review_summary"]
    _expect_true(summary.get("ready_for_operator_assessment"), "ready_for_operator_assessment")
    _expect_true(summary.get("operator_decision_required_before_freeze"), "operator_decision_required_before_freeze")
    _expect_false(summary.get("software_freeze_authorized"), "software_freeze_authorized")
    _expect_false(summary.get("registry_approval_authorized"), "registry_approval_authorized")
    _expect_false(summary.get("runtime_migration_authorized"), "runtime_migration_authorized")

    digest = review_package.get("position_swing_canonical_dataset_review_package_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PositionSwingCanonicalDatasetOperatorReviewError("position_swing_canonical_dataset_review_package_semantic_digest missing")
    _expect(
        digest,
        position_swing_canonical_dataset_review_package_semantic_digest_v1(review_package),
        "position_swing_canonical_dataset_review_package_semantic_digest",
    )
    return {
        "status": "POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "review_package_digest": digest,
        "reviewed_candidate_digest": evidence["reviewed_candidate_digest"],
        "dataset_rows_digest": evidence["reviewed_dataset_rows_digest"],
        "dataset_manifest_digest": evidence["reviewed_dataset_manifest_digest"],
        "source_rows_digest": evidence["reviewed_source_rows_digest"],
        "materialization_receipt_digest": evidence["reviewed_materialization_receipt_digest"],
        "position_swing_bar_count": evidence["position_swing_bar_count"],
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "ready_for_operator_assessment": summary["ready_for_operator_assessment"],
        "provider_requests_made_in_review": False,
        "position_swing_canonical_dataset_frozen": False,
        "position_swing_registry_approval_created": False,
        "position_swing_registry_eligibility": False,
        "strategy_runtime_migration": False,
        "runtime_use": position.NOT_AUTHORIZED,
        "strategy_use": position.NOT_AUTHORIZED,
    }


def build_position_swing_canonical_dataset_candidate_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Render a sanitized POSITION_SWING canonical dataset review package status document."""
    validation = validate_position_swing_canonical_dataset_candidate_review_package_v1(review_package)
    evidence = review_package["reviewed_position_swing_candidate_evidence"]
    bindings = review_package["authority_bindings"]
    boundary = review_package["authority_boundary"]
    summary = review_package["review_summary"]
    failed = [item for item in review_package["review_checklist"] if item["status"] != PASS]
    lines = [
        "# MarketFlow POSITION_SWING Canonical Dataset Operator Review Package Status",
        "",
        "## Title",
        "- POSITION_SWING Canonical Dataset Operator Review Package v1.",
        "",
        "## Reviewed POSITION_SWING Candidate",
        f"- Review package artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Binding mode: `{review_package['binding_mode']}`",
        f"- Reviewed candidate kind: `{evidence['reviewed_candidate_kind']}`",
        f"- Reviewed candidate status: `{evidence['reviewed_candidate_status']}`",
        f"- POSITION_SWING candidate digest: `{evidence['reviewed_candidate_digest']}`",
        f"- Dataset profile: `{evidence['reviewed_dataset_profile']}`",
        f"- Dataset bar rule: `{evidence['reviewed_dataset_bar_rule']}`",
        f"- Dataset rows digest: `{evidence['reviewed_dataset_rows_digest']}`",
        f"- Dataset manifest digest: `{evidence['reviewed_dataset_manifest_digest']}`",
        "",
        "## Dataset Summary",
        f"- POSITION_SWING bar count: `{evidence['position_swing_bar_count']}`",
        f"- Source RTH rows consumed: `{evidence['source_rth_rows_consumed']}`",
        f"- Source RTH rows excluded: `{evidence['source_rth_rows_excluded']}`",
        f"- Full sessions used: `{evidence['full_sessions_used']}`",
        f"- Special sessions excluded: `{evidence['special_sessions_excluded']}`",
        f"- Special session rows excluded: `{evidence['special_session_rows_excluded']}`",
        "",
        "## 2025-01 Cross-Check",
        f"- Cross-check month: `{evidence['cross_check_month']}`",
        f"- Cross-check status: `{evidence['cross_check_status']}`",
        f"- Cross-check POSITION_SWING bars: `{evidence['cross_check_position_swing_bars']}`",
        "",
        "## Special-Session Policy",
        f"- Policy: `{evidence['special_session_policy']}`",
        f"- Special sessions excluded from POSITION_SWING bars: `{evidence['special_sessions_excluded_from_position_swing_bars']}`",
        f"- Special sessions recorded in exclusion inventory: `{evidence['special_sessions_recorded_in_exclusion_inventory']}`",
        f"- Special-session exclusion count: `{evidence['special_session_exclusion_count']}`",
        "",
        "## Frozen Authority Bindings",
        f"- Identity frozen digest: `{bindings['identity_frozen_digest']}`",
        f"- Calendar frozen digest: `{bindings['calendar_frozen_digest']}`",
        f"- Schedule digest: `{bindings['schedule_digest']}`",
        f"- Split-event audit frozen digest: `{bindings['split_event_frozen_digest']}`",
        f"- Dividend-event audit frozen digest: `{bindings['dividend_event_frozen_digest']}`",
        f"- Acquisition generation frozen digest: `{bindings['acquisition_generation_frozen_digest']}`",
        f"- Materialization receipt digest: `{bindings['materialization_receipt_digest']}`",
        f"- Normalized source rows digest: `{bindings['normalized_source_rows_digest']}`",
        "",
        "## Dividend Adjustment Implication",
        f"- In-range dividends found: `{bindings['in_range_dividends_found']}`",
        f"- In-range dividend count: `{bindings['in_range_dividend_count']}`",
        f"- Implication: `{bindings['in_range_dividend_implication']}`",
        f"- Source adjusted data used: `{bindings['source_adjusted_data_used']}`",
        "",
        "## Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        f"- Ready for operator assessment: `{summary['ready_for_operator_assessment']}`",
        f"- Software freeze authorized: `{summary['software_freeze_authorized']}`",
        "",
        "## Failed Checks",
    ]
    if failed:
        lines.extend(f"- `{item['check_id']}`: {item['message']}" for item in failed)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Authority Boundary",
        ]
    )
    lines.extend(f"- {key}: `{value}`" for key, value in boundary.items())
    lines.extend(
        [
            "",
            "## Remaining Roadmap",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(review_package["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made in review: `False`",
            "- No `POSITION_SWING_CANONICAL_DATASET_FROZEN` artifact or status is created.",
            "- No POSITION_SWING canonical dataset freeze, registry approval, runtime migration, predictive acceptance, or profitability acceptance occurred.",
            "- Operator decision remains required before any future POSITION_SWING canonical dataset freeze ceremony.",
            "",
            "## Review Package Digest",
            f"- Review package digest: `{validation['review_package_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_position_swing_canonical_dataset_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the POSITION_SWING review package JSON artifact without overwriting output."""
    review_package = build_position_swing_canonical_dataset_candidate_review_package_v1(candidate)
    validation = validate_position_swing_canonical_dataset_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PositionSwingCanonicalDatasetOperatorReviewError("POSITION_SWING review package filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise PositionSwingCanonicalDatasetOperatorReviewError("POSITION_SWING review package output already exists")
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
