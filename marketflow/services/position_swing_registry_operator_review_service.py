"""Offline operator-review package for POSITION_SWING registry approval candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import position_swing_canonical_dataset_service as position
from marketflow.services import position_swing_registry_approval_service as registry


ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE = (
    "POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_V1 = (
    "position_swing_registry_approval_candidate_review_v1"
)
POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY = (
    "POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY"
)
POSITION_SWING_REGISTRY_CANDIDATE_STATUS_BINDING = "POSITION_SWING_REGISTRY_CANDIDATE_STATUS_BINDING"
POSITION_SWING_REGISTRY_CANDIDATE_OBJECT_BINDING = "POSITION_SWING_REGISTRY_CANDIDATE_OBJECT_BINDING"

EXPECTED_POSITION_SWING_REGISTRY_CANDIDATE_DIGEST = (
    "3987efa860732c113a1f5037ef0ccca9b261f10b7602b52b6866bf7f4a8a3511"
)
EXPECTED_CANDIDATE_CHECKLIST_TOTAL = 40
EXPECTED_CANDIDATE_CHECKLIST_PASSED = 40
EXPECTED_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_CANDIDATE_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

REQUIRED_CHECK_IDS = [
    "registry_candidate_kind_matches",
    "registry_candidate_status_ready_for_review",
    "registry_candidate_digest_matches",
    "proposed_registry_key_matches",
    "registry_scope_research_dataset",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "registry_activation_false",
    "candidate_checklist_zero_blockers",
    "position_swing_canonical_dataset_frozen_true",
    "position_swing_frozen_digest_matches",
    "dataset_rows_digest_matches",
    "dataset_manifest_digest_matches",
    "dataset_profile_position_swing",
    "dataset_bar_rule_rth_full_session_1d",
    "position_swing_bar_count_994",
    "special_session_policy_preserved",
    "cross_check_2025_01_passed",
    "cross_check_2025_01_position_swing_bars_20",
    "authority_digests_match",
    "swing_registry_approval_digest_bound",
    "dividend_implication_preserved",
    "position_swing_registry_approval_created_false",
    "position_swing_registry_eligibility_false",
    "position_swing_registry_activation_false",
    "registry_eligibility_false",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "runtime_use_not_authorized_boundary",
    "strategy_use_not_authorized_boundary",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "provider_requests_made_in_review_false",
    "no_position_swing_registry_approved_artifact_created",
]

REMAINING_ROADMAP = [
    "Digest-bound POSITION_SWING registry approval ceremony.",
    "Normal runtime migration planning.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
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

FORBIDDEN_TRUE_FIELDS = frozenset(
    {
        "position_swing_registry_approval_created",
        "position_swing_registry_eligibility",
        "position_swing_registry_activation",
        "registry_eligibility",
        "canonical_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
        "provider_requests_made_in_review",
        "software_registry_approval_authorized",
        "runtime_migration_authorized",
    }
)


class PositionSwingRegistryOperatorReviewError(ValueError):
    """Raised when a POSITION_SWING registry review package violates guardrails."""


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise PositionSwingRegistryOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PositionSwingRegistryOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PositionSwingRegistryOperatorReviewError(f"{field_name} must be true")


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


def _authority_digests() -> dict[str, Any]:
    return {
        "identity_frozen_digest": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "calendar_frozen_digest": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_digest": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_frozen_digest": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_frozen_digest": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_generation_frozen_digest": registry.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
        "swing_canonical_dataset_frozen_digest": registry.EXPECTED_SWING_CANONICAL_DATASET_FROZEN_DIGEST,
        "swing_registry_approval_digest": registry.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
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
        "swing_registry_activation": True,
        "position_swing_canonical_dataset_frozen": True,
        "position_swing_registry_approval_created": False,
        "position_swing_registry_eligibility": False,
        "position_swing_registry_activation": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "registry_activation": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "runtime_use": registry.NOT_AUTHORIZED,
        "strategy_use": registry.NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def _candidate_evidence_from_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    validation = registry.validate_position_swing_registry_approval_candidate_v1(candidate)
    return {
        "reviewed_registry_candidate_kind": candidate["artifact_kind"],
        "reviewed_registry_candidate_status": candidate["candidate_status"],
        "reviewed_registry_candidate_digest": validation[
            "position_swing_registry_approval_candidate_semantic_digest"
        ],
        "reviewed_proposed_registry_key": candidate["proposed_registry_key"],
        "reviewed_registry_scope": candidate["proposed_registry_scope"],
        "reviewed_runtime_use": candidate["proposed_runtime_use"],
        "reviewed_strategy_use": candidate["proposed_strategy_use"],
        "reviewed_registry_activation": candidate["proposed_registry_activation"],
        "reviewed_candidate_checklist_total": validation["total_checks"],
        "reviewed_candidate_checklist_passed": validation["passed_checks"],
        "reviewed_candidate_checklist_failed": validation["failed_checks"],
        "reviewed_candidate_blocker_count": validation["blocker_count"],
        "position_swing_canonical_dataset_frozen": candidate["position_swing_canonical_dataset_frozen"],
        "position_swing_canonical_dataset_frozen_digest": candidate[
            "position_swing_canonical_dataset_frozen_digest"
        ],
        "position_swing_review_package_digest": candidate["position_swing_review_package_digest"],
        "position_swing_candidate_digest": candidate["position_swing_candidate_digest"],
        "dataset_rows_digest": candidate["dataset_rows_digest"],
        "dataset_manifest_digest": candidate["dataset_manifest_digest"],
        "source_rows_digest": candidate["source_rows_digest"],
        "materialization_receipt_digest": candidate["materialization_receipt_digest"],
        "dataset_profile": candidate["dataset_profile"],
        "dataset_bar_rule": candidate["dataset_bar_rule"],
        "position_swing_bar_count": candidate["position_swing_bar_count"],
        "source_rth_rows_consumed": candidate["source_rth_rows_consumed"],
        "source_rth_rows_excluded": candidate["source_rth_rows_excluded"],
        "full_sessions_used": candidate["full_sessions_used"],
        "special_session_policy": candidate["special_session_policy"],
        "special_sessions_excluded": candidate["special_sessions_excluded"],
        "special_session_rows_excluded": candidate["special_session_rows_excluded"],
        "cross_check_2025_01_status": candidate["cross_check_2025_01_status"],
        "cross_check_2025_01_position_swing_bars": candidate["cross_check_2025_01_position_swing_bars"],
        "in_range_dividends_found": candidate["in_range_dividends_found"],
        "in_range_dividend_count": candidate["in_range_dividend_count"],
        "in_range_dividend_implication": candidate["in_range_dividend_implication"],
        "source_adjusted_data_used": candidate["source_adjusted_data_used"],
        **_authority_digests(),
        **_fixed_segment(),
    }


def _recorded_candidate_evidence() -> dict[str, Any]:
    return _candidate_evidence_from_candidate(registry.build_position_swing_registry_approval_candidate_v1())


def _package_context() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_V1,
        "review_status": POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY,
        "operator_decision_required": True,
        "operator_decision": None,
        "position_swing_registry_approval_created": False,
        "position_swing_registry_eligibility": False,
        "position_swing_registry_activation": False,
        "registry_eligibility": False,
        "canonical_eligibility": False,
        "strategy_runtime_migration": False,
        "runtime_use": registry.NOT_AUTHORIZED,
        "strategy_use": registry.NOT_AUTHORIZED,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "operator_approved_by": None,
        "operator_approval_timestamp": None,
        "operator_approval_digest": None,
        "operator_signature": None,
        "approval_status": None,
        "registry_activation": False,
        "software_registry_approval_authorized": False,
        "runtime_migration_authorized": False,
    }


def _authority_digest_actuals(package: dict[str, Any]) -> dict[str, Any]:
    return {field: package.get(field) for field in _authority_digests()}


def _build_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    expected_authority = _authority_digests()
    return [
        _check(
            "registry_candidate_kind_matches",
            registry.ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE,
            package.get("reviewed_registry_candidate_kind"),
        ),
        _check(
            "registry_candidate_status_ready_for_review",
            registry.POSITION_SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW,
            package.get("reviewed_registry_candidate_status"),
        ),
        _check(
            "registry_candidate_digest_matches",
            EXPECTED_POSITION_SWING_REGISTRY_CANDIDATE_DIGEST,
            package.get("reviewed_registry_candidate_digest"),
        ),
        _check("proposed_registry_key_matches", registry.PROPOSED_REGISTRY_KEY, package.get("reviewed_proposed_registry_key")),
        _check("registry_scope_research_dataset", registry.PROPOSED_REGISTRY_SCOPE, package.get("reviewed_registry_scope")),
        _check("runtime_use_not_authorized", registry.NOT_AUTHORIZED, package.get("reviewed_runtime_use")),
        _check("strategy_use_not_authorized", registry.NOT_AUTHORIZED, package.get("reviewed_strategy_use")),
        _check("registry_activation_false", False, package.get("reviewed_registry_activation")),
        _check(
            "candidate_checklist_zero_blockers",
            {
                "total": EXPECTED_CANDIDATE_CHECKLIST_TOTAL,
                "passed": EXPECTED_CANDIDATE_CHECKLIST_PASSED,
                "failed": EXPECTED_CANDIDATE_CHECKLIST_FAILED,
                "blockers": EXPECTED_CANDIDATE_BLOCKER_COUNT,
            },
            {
                "total": package.get("reviewed_candidate_checklist_total"),
                "passed": package.get("reviewed_candidate_checklist_passed"),
                "failed": package.get("reviewed_candidate_checklist_failed"),
                "blockers": package.get("reviewed_candidate_blocker_count"),
            },
        ),
        _check("position_swing_canonical_dataset_frozen_true", True, package.get("position_swing_canonical_dataset_frozen")),
        _check(
            "position_swing_frozen_digest_matches",
            registry.EXPECTED_POSITION_SWING_FROZEN_DIGEST,
            package.get("position_swing_canonical_dataset_frozen_digest"),
        ),
        _check("dataset_rows_digest_matches", registry.EXPECTED_DATASET_ROWS_DIGEST, package.get("dataset_rows_digest")),
        _check(
            "dataset_manifest_digest_matches",
            registry.EXPECTED_DATASET_MANIFEST_DIGEST,
            package.get("dataset_manifest_digest"),
        ),
        _check("dataset_profile_position_swing", position.DATASET_PROFILE_POSITION_SWING, package.get("dataset_profile")),
        _check(
            "dataset_bar_rule_rth_full_session_1d",
            position.DATASET_BAR_RULE_RTH_FULL_SESSION_1D,
            package.get("dataset_bar_rule"),
        ),
        _check("position_swing_bar_count_994", registry.EXPECTED_POSITION_SWING_BAR_COUNT, package.get("position_swing_bar_count")),
        _check("special_session_policy_preserved", registry.EXPECTED_SPECIAL_SESSION_POLICY, package.get("special_session_policy")),
        _check("cross_check_2025_01_passed", registry.EXPECTED_CROSS_CHECK_STATUS, package.get("cross_check_2025_01_status")),
        _check(
            "cross_check_2025_01_position_swing_bars_20",
            registry.EXPECTED_CROSS_CHECK_POSITION_SWING_BARS,
            package.get("cross_check_2025_01_position_swing_bars"),
        ),
        _check("authority_digests_match", expected_authority, _authority_digest_actuals(package)),
        _check(
            "swing_registry_approval_digest_bound",
            registry.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
            package.get("swing_registry_approval_digest"),
        ),
        _check(
            "dividend_implication_preserved",
            {
                "in_range_dividends_found": True,
                "in_range_dividend_count": 16,
                "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
                "source_adjusted_data_used": True,
            },
            {
                "in_range_dividends_found": package.get("in_range_dividends_found"),
                "in_range_dividend_count": package.get("in_range_dividend_count"),
                "in_range_dividend_implication": package.get("in_range_dividend_implication"),
                "source_adjusted_data_used": package.get("source_adjusted_data_used"),
            },
        ),
        _check(
            "position_swing_registry_approval_created_false",
            False,
            package.get("position_swing_registry_approval_created"),
        ),
        _check(
            "position_swing_registry_eligibility_false",
            False,
            package.get("position_swing_registry_eligibility"),
        ),
        _check(
            "position_swing_registry_activation_false",
            False,
            package.get("position_swing_registry_activation"),
        ),
        _check("registry_eligibility_false", False, package.get("registry_eligibility")),
        _check("strategy_runtime_migration_false", False, package.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, package.get("automatic_stitching")),
        _check("runtime_use_not_authorized_boundary", registry.NOT_AUTHORIZED, package.get("runtime_use")),
        _check("strategy_use_not_authorized_boundary", registry.NOT_AUTHORIZED, package.get("strategy_use")),
        _check(
            "predictive_usefulness_not_accepted",
            acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            package.get("predictive_usefulness"),
            severity=INFO,
        ),
        _check(
            "profitability_not_accepted",
            acquisition.PROFITABILITY_NOT_ACCEPTED,
            package.get("profitability"),
            severity=INFO,
        ),
        _check("provider_requests_made_in_review_false", False, package.get("provider_requests_made_in_review")),
        _check(
            "no_position_swing_registry_approved_artifact_created",
            {
                "artifact_kind_is_not_position_swing_registry_approved": True,
                "review_status_is_not_position_swing_registry_approved": True,
                "approval_status_is_null": True,
            },
            {
                "artifact_kind_is_not_position_swing_registry_approved": (
                    package.get("artifact_kind") != "POSITION_SWING_REGISTRY_APPROVED"
                ),
                "review_status_is_not_position_swing_registry_approved": (
                    package.get("review_status") != "POSITION_SWING_REGISTRY_APPROVED"
                ),
                "approval_status_is_null": package.get("approval_status") is None,
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
        "ready_for_operator_registry_assessment": failed == 0,
        "operator_decision_required_before_registry_approval": True,
        "software_registry_approval_authorized": False,
        "runtime_migration_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("position_swing_registry_review_package_semantic_digest", None)
    return payload


def position_swing_registry_review_package_semantic_digest_v1(review_package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a POSITION_SWING registry review package."""
    return semantic_digest(_digest_payload(review_package))


def build_position_swing_registry_approval_candidate_review_package_v1(
    registry_candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline, digest-bound review package without registry approval."""
    binding_mode = POSITION_SWING_REGISTRY_CANDIDATE_STATUS_BINDING
    evidence = _recorded_candidate_evidence()
    if registry_candidate is not None:
        binding_mode = POSITION_SWING_REGISTRY_CANDIDATE_OBJECT_BINDING
        evidence = _candidate_evidence_from_candidate(registry_candidate)
    package = {
        **_package_context(),
        "binding_mode": binding_mode,
        **evidence,
        "authority_boundary": _authority_boundary(),
        "remaining_roadmap": list(REMAINING_ROADMAP),
    }
    checklist = _build_checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist)
    package["position_swing_registry_review_package_semantic_digest"] = (
        position_swing_registry_review_package_semantic_digest_v1(package)
    )
    validate_position_swing_registry_approval_candidate_review_package_v1(package)
    return package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "POSITION_SWING_REGISTRY_APPROVED",
            "REGISTRY_ELIGIBLE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise PositionSwingRegistryOperatorReviewError(f"{current_path} must not emit {value}")
        if key in FORBIDDEN_APPROVAL_FIELDS and value is not None:
            raise PositionSwingRegistryOperatorReviewError(f"{current_path} must be null")
        if key in FORBIDDEN_TRUE_FIELDS and value is True:
            raise PositionSwingRegistryOperatorReviewError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "reviewed_runtime_use", "reviewed_strategy_use"}:
            if value == "AUTHORIZED":
                raise PositionSwingRegistryOperatorReviewError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PositionSwingRegistryOperatorReviewError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_position_swing_registry_approval_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate a POSITION_SWING registry review package without granting registry authority."""
    if not isinstance(review_package, dict):
        raise PositionSwingRegistryOperatorReviewError(
            "POSITION_SWING registry review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("binding_mode") not in {
        POSITION_SWING_REGISTRY_CANDIDATE_STATUS_BINDING,
        POSITION_SWING_REGISTRY_CANDIDATE_OBJECT_BINDING,
    }:
        raise PositionSwingRegistryOperatorReviewError("binding_mode mismatch")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    _expect_true(review_package.get("created_offline"), "created_offline")
    for field in FORBIDDEN_TRUE_FIELDS:
        _expect_false(review_package.get(field), field)
    for field in FORBIDDEN_APPROVAL_FIELDS:
        _expect(review_package.get(field), None, field)
    _expect_false(review_package.get("registry_activation"), "registry_activation")
    _expect(review_package.get("runtime_use"), registry.NOT_AUTHORIZED, "runtime_use")
    _expect(review_package.get("strategy_use"), registry.NOT_AUTHORIZED, "strategy_use")
    _expect(
        review_package.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "reviewed_registry_candidate_kind": registry.ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE,
        "reviewed_registry_candidate_status": registry.POSITION_SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW,
        "reviewed_registry_candidate_digest": EXPECTED_POSITION_SWING_REGISTRY_CANDIDATE_DIGEST,
        "reviewed_proposed_registry_key": registry.PROPOSED_REGISTRY_KEY,
        "reviewed_registry_scope": registry.PROPOSED_REGISTRY_SCOPE,
        "reviewed_runtime_use": registry.NOT_AUTHORIZED,
        "reviewed_strategy_use": registry.NOT_AUTHORIZED,
        "reviewed_registry_activation": False,
        "reviewed_candidate_checklist_total": EXPECTED_CANDIDATE_CHECKLIST_TOTAL,
        "reviewed_candidate_checklist_passed": EXPECTED_CANDIDATE_CHECKLIST_PASSED,
        "reviewed_candidate_checklist_failed": EXPECTED_CANDIDATE_CHECKLIST_FAILED,
        "reviewed_candidate_blocker_count": EXPECTED_CANDIDATE_BLOCKER_COUNT,
        "position_swing_canonical_dataset_frozen_digest": registry.EXPECTED_POSITION_SWING_FROZEN_DIGEST,
        "position_swing_review_package_digest": registry.EXPECTED_POSITION_SWING_REVIEW_PACKAGE_DIGEST,
        "position_swing_candidate_digest": registry.EXPECTED_POSITION_SWING_CANDIDATE_DIGEST,
        "dataset_rows_digest": registry.EXPECTED_DATASET_ROWS_DIGEST,
        "dataset_manifest_digest": registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "source_rows_digest": registry.EXPECTED_SOURCE_ROWS_DIGEST,
        "materialization_receipt_digest": registry.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        "dataset_profile": position.DATASET_PROFILE_POSITION_SWING,
        "dataset_bar_rule": position.DATASET_BAR_RULE_RTH_FULL_SESSION_1D,
        "position_swing_bar_count": registry.EXPECTED_POSITION_SWING_BAR_COUNT,
        "source_rth_rows_consumed": registry.EXPECTED_SOURCE_RTH_ROWS_CONSUMED,
        "source_rth_rows_excluded": registry.EXPECTED_SOURCE_RTH_ROWS_EXCLUDED,
        "full_sessions_used": registry.EXPECTED_FULL_SESSIONS_USED,
        "special_session_policy": registry.EXPECTED_SPECIAL_SESSION_POLICY,
        "special_sessions_excluded": registry.EXPECTED_SPECIAL_SESSIONS_EXCLUDED,
        "special_session_rows_excluded": registry.EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED,
        "cross_check_2025_01_status": registry.EXPECTED_CROSS_CHECK_STATUS,
        "cross_check_2025_01_position_swing_bars": registry.EXPECTED_CROSS_CHECK_POSITION_SWING_BARS,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        "ticker": "AAPL",
        "composite_figi": "BBG000B9XRY4",
        "share_class_figi": "BBG001S5N8V8",
        "primary_mic": "XNAS",
        "security_type": "CS",
        "segment_start": "2022-01-01",
        "segment_end": "2025-12-31",
        **_authority_digests(),
    }.items():
        _expect(review_package.get(field), expected, field)
    _expect_true(
        review_package.get("position_swing_canonical_dataset_frozen"),
        "position_swing_canonical_dataset_frozen",
    )
    _expect_true(review_package.get("in_range_dividends_found"), "in_range_dividends_found")
    _expect_true(review_package.get("source_adjusted_data_used"), "source_adjusted_data_used")
    _expect(review_package.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    _expect(review_package.get("remaining_roadmap"), REMAINING_ROADMAP, "remaining_roadmap")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PositionSwingRegistryOperatorReviewError("review_checklist must be a list")
    check_ids = [item.get("check_id") for item in checklist if isinstance(item, dict)]
    _expect(check_ids, REQUIRED_CHECK_IDS, "review_checklist check IDs")
    _expect(checklist, _build_checklist(review_package), "review_checklist")
    failed = [item for item in checklist if item.get("status") != PASS]
    if failed:
        raise PositionSwingRegistryOperatorReviewError(
            f"POSITION_SWING registry review package contains failed check: {failed[0]['check_id']}"
        )
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    summary = review_package["review_summary"]
    _expect_true(
        summary.get("ready_for_operator_registry_assessment"),
        "ready_for_operator_registry_assessment",
    )
    _expect_true(
        summary.get("operator_decision_required_before_registry_approval"),
        "operator_decision_required_before_registry_approval",
    )
    _expect_false(summary.get("software_registry_approval_authorized"), "software_registry_approval_authorized")
    _expect_false(summary.get("runtime_migration_authorized"), "runtime_migration_authorized")
    digest = review_package.get("position_swing_registry_review_package_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PositionSwingRegistryOperatorReviewError(
            "position_swing_registry_review_package_semantic_digest missing"
        )
    _expect(
        digest,
        position_swing_registry_review_package_semantic_digest_v1(review_package),
        "position_swing_registry_review_package_semantic_digest",
    )
    return {
        "status": "POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "review_package_digest": digest,
        "reviewed_registry_candidate_digest": review_package["reviewed_registry_candidate_digest"],
        "reviewed_proposed_registry_key": review_package["reviewed_proposed_registry_key"],
        "reviewed_registry_scope": review_package["reviewed_registry_scope"],
        "runtime_use": registry.NOT_AUTHORIZED,
        "strategy_use": registry.NOT_AUTHORIZED,
        "position_swing_canonical_dataset_frozen_digest": registry.EXPECTED_POSITION_SWING_FROZEN_DIGEST,
        "dataset_rows_digest": registry.EXPECTED_DATASET_ROWS_DIGEST,
        "dataset_manifest_digest": registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "ready_for_operator_registry_assessment": summary["ready_for_operator_registry_assessment"],
        "provider_requests_made_in_review": False,
        "position_swing_registry_approval_created": False,
        "position_swing_registry_eligibility": False,
        "position_swing_registry_activation": False,
        "registry_eligibility": False,
        "canonical_eligibility": False,
        "strategy_runtime_migration": False,
    }


def build_position_swing_registry_approval_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized POSITION_SWING registry review package status document."""
    validation = validate_position_swing_registry_approval_candidate_review_package_v1(review_package)
    summary = review_package["review_summary"]
    failed = [item for item in review_package["review_checklist"] if item["status"] != PASS]
    boundary = review_package["authority_boundary"]
    lines = [
        "# MarketFlow POSITION_SWING Registry Operator Review Package Status",
        "",
        "## Title",
        "- POSITION_SWING Registry Operator Review Package v1.",
        "",
        "## Reviewed Registry Candidate",
        f"- Review package artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Binding mode: `{review_package['binding_mode']}`",
        f"- Reviewed candidate kind: `{review_package['reviewed_registry_candidate_kind']}`",
        f"- Reviewed candidate status: `{review_package['reviewed_registry_candidate_status']}`",
        f"- Reviewed candidate digest: `{review_package['reviewed_registry_candidate_digest']}`",
        "",
        "## Proposed Registry Entry",
        f"- Proposed registry key: `{review_package['reviewed_proposed_registry_key']}`",
        f"- Registry scope: `{review_package['reviewed_registry_scope']}`",
        f"- Runtime use: `{review_package['reviewed_runtime_use']}`",
        f"- Strategy use: `{review_package['reviewed_strategy_use']}`",
        f"- Registry activation: `{review_package['reviewed_registry_activation']}`",
        "",
        "## Frozen POSITION_SWING Dataset Evidence",
        f"- POSITION_SWING frozen digest: `{review_package['position_swing_canonical_dataset_frozen_digest']}`",
        f"- POSITION_SWING review package digest: `{review_package['position_swing_review_package_digest']}`",
        f"- POSITION_SWING candidate digest: `{review_package['position_swing_candidate_digest']}`",
        f"- Dataset rows digest: `{review_package['dataset_rows_digest']}`",
        f"- Dataset manifest digest: `{review_package['dataset_manifest_digest']}`",
        f"- Source rows digest: `{review_package['source_rows_digest']}`",
        f"- Materialization receipt digest: `{review_package['materialization_receipt_digest']}`",
        "",
        "## Dataset Summary",
        f"- Dataset profile: `{review_package['dataset_profile']}`",
        f"- Dataset bar rule: `{review_package['dataset_bar_rule']}`",
        f"- POSITION_SWING bar count: `{review_package['position_swing_bar_count']}`",
        f"- Source RTH rows consumed: `{review_package['source_rth_rows_consumed']}`",
        f"- Source RTH rows excluded: `{review_package['source_rth_rows_excluded']}`",
        f"- Full sessions used: `{review_package['full_sessions_used']}`",
        f"- Special-session policy: `{review_package['special_session_policy']}`",
        f"- Special sessions excluded: `{review_package['special_sessions_excluded']}`",
        f"- Special-session rows excluded: `{review_package['special_session_rows_excluded']}`",
        f"- 2025-01 cross-check: `{review_package['cross_check_2025_01_status']}` / `{review_package['cross_check_2025_01_position_swing_bars']}` bars",
        "",
        "## Registry Boundary",
        f"- POSITION_SWING registry approval created: `{review_package['position_swing_registry_approval_created']}`",
        f"- POSITION_SWING registry eligibility: `{review_package['position_swing_registry_eligibility']}`",
        f"- POSITION_SWING registry activation: `{review_package['position_swing_registry_activation']}`",
        f"- Registry eligibility: `{review_package['registry_eligibility']}`",
        f"- Canonical eligibility: `{review_package['canonical_eligibility']}`",
        f"- Registry activation: `{review_package['registry_activation']}`",
        f"- Runtime use: `{review_package['runtime_use']}`",
        f"- Strategy use: `{review_package['strategy_use']}`",
        f"- Strategy runtime migration: `{review_package['strategy_runtime_migration']}`",
        f"- Predictive usefulness: `{review_package['predictive_usefulness']}`",
        f"- Profitability: `{review_package['profitability']}`",
        "",
        "## Authority Bindings",
        f"- Identity frozen digest: `{review_package['identity_frozen_digest']}`",
        f"- Calendar frozen digest: `{review_package['calendar_frozen_digest']}`",
        f"- Schedule digest: `{review_package['schedule_digest']}`",
        f"- Split-event audit frozen digest: `{review_package['split_event_frozen_digest']}`",
        f"- Dividend-event audit frozen digest: `{review_package['dividend_event_frozen_digest']}`",
        f"- Acquisition generation frozen digest: `{review_package['acquisition_generation_frozen_digest']}`",
        f"- SWING canonical dataset frozen digest: `{review_package['swing_canonical_dataset_frozen_digest']}`",
        f"- SWING registry approval digest: `{review_package['swing_registry_approval_digest']}`",
        f"- In-range dividend implication: `{review_package['in_range_dividend_implication']}`",
        "",
        "## Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        f"- Ready for operator registry assessment: `{summary['ready_for_operator_registry_assessment']}`",
        f"- Software registry approval authorized: `{summary['software_registry_approval_authorized']}`",
        f"- Runtime migration authorized: `{summary['runtime_migration_authorized']}`",
        "",
        "## Failed Checks",
    ]
    if failed:
        lines.extend(f"- `{item['check_id']}`: {item['message']}" for item in failed)
    else:
        lines.append("- None.")
    lines.extend(["", "## Authority Boundary"])
    lines.extend(f"- {key}: `{value}`" for key, value in boundary.items())
    lines.extend(["", "## Remaining Required Tasks"])
    lines.extend(f"{index}. {task}" for index, task in enumerate(review_package["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made in review: `False`",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No acquisition rows or POSITION_SWING bars were regenerated.",
            "- No `POSITION_SWING_REGISTRY_APPROVED` artifact or status is created.",
            "- No `REGISTRY_ELIGIBLE` or `STRATEGY_RUNTIME_MIGRATION` artifact or status is created.",
            "- No POSITION_SWING registry approval, registry eligibility, registry activation, or runtime migration occurred.",
            "- Runtime and Strategy use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "- Operator decision remains required before any future POSITION_SWING registry approval ceremony.",
            "",
            "## Review Package Digest",
            f"- Review package digest: `{validation['review_package_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_position_swing_registry_approval_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    registry_candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the POSITION_SWING registry review package JSON artifact without overwriting output."""
    review_package = build_position_swing_registry_approval_candidate_review_package_v1(registry_candidate)
    validation = validate_position_swing_registry_approval_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or (
        "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_registry_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PositionSwingRegistryOperatorReviewError(
            "POSITION_SWING registry review package filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PositionSwingRegistryOperatorReviewError("POSITION_SWING registry review package output already exists")
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
