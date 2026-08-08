"""Offline POSITION_SWING registry approval ceremony helpers."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import position_swing_canonical_dataset_service as position
from marketflow.services import position_swing_registry_approval_service as registry
from marketflow.services import position_swing_registry_operator_review_service as review


ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVED = "POSITION_SWING_REGISTRY_APPROVED"
SCHEMA_VERSION_POSITION_SWING_REGISTRY_APPROVAL_V1 = "position_swing_registry_approval_v1"
POSITION_SWING_REGISTRY_APPROVED = "POSITION_SWING_REGISTRY_APPROVED"
OPERATOR_DECISION_APPROVE_POSITION_SWING_REGISTRY_ENTRY = "APPROVE_POSITION_SWING_REGISTRY_ENTRY"
OPERATOR_ATTESTATION_VERSION_V1 = "position_swing_registry_approval_operator_attestation_v1"
REQUIRED_POSITION_SWING_REGISTRY_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE POSITION_SWING REGISTRY ENTRY AAPL POSITION_SWING RTH_FULL_SESSION_1D "
    "2022-01-01 2025-12-31 RESEARCH_DATASET NOT_RUNTIME_AUTHORIZED"
)

EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST = (
    "db8dc9c15d9ed5a1edd2756fc5e5d1a5cfe157eac0e2ac36dbb2cc0faefe233e"
)
EXPECTED_REGISTRY_CANDIDATE_DIGEST = review.EXPECTED_POSITION_SWING_REGISTRY_CANDIDATE_DIGEST
EXPECTED_REGISTRY_REVIEW_CHECKLIST_TOTAL = len(review.REQUIRED_CHECK_IDS)
EXPECTED_REGISTRY_REVIEW_CHECKLIST_PASSED = len(review.REQUIRED_CHECK_IDS)
EXPECTED_REGISTRY_REVIEW_CHECKLIST_FAILED = 0
EXPECTED_REGISTRY_REVIEW_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

OPERATOR_BOUNDARY_CONFIRMATION_FIELDS = [
    "operator_confirms_registry_scope_research_dataset",
    "operator_confirms_runtime_use_not_authorized",
    "operator_confirms_strategy_use_not_authorized",
    "operator_confirms_no_strategy_runtime_migration",
    "operator_confirms_no_predictive_usefulness",
    "operator_confirms_no_profitability_acceptance",
]

REMAINING_ROADMAP_AFTER_POSITION_SWING_REGISTRY_APPROVAL = [
    "Normal runtime migration planning.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
]

REQUIRED_APPROVAL_CHECK_IDS = [
    "registry_review_package_digest_matches_expected",
    "registry_review_package_has_zero_blockers",
    "registry_candidate_digest_matches_expected",
    "registry_key_matches_expected",
    "registry_scope_research_dataset",
    "position_swing_canonical_dataset_frozen_true",
    "position_swing_frozen_digest_matches_expected",
    "dataset_rows_digest_matches_expected",
    "dataset_manifest_digest_matches_expected",
    "dataset_profile_position_swing",
    "dataset_bar_rule_rth_full_session_1d",
    "position_swing_bar_count_994",
    "cross_check_2025_01_passed",
    "special_session_policy_preserved",
    "dividend_implication_preserved",
    "swing_registry_approval_digest_bound",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_review_digest_confirmation_matches",
    "operator_candidate_digest_confirmation_matches",
    "operator_registry_key_confirmation_matches",
    "operator_position_swing_frozen_digest_confirmation_matches",
    "operator_dataset_rows_digest_confirmation_matches",
    "operator_dataset_manifest_digest_confirmation_matches",
    "operator_registry_scope_confirmation_research_dataset",
    "operator_runtime_use_not_authorized_confirmation",
    "operator_strategy_use_not_authorized_confirmation",
    "operator_no_strategy_runtime_migration_confirmation",
    "operator_no_predictive_usefulness_confirmation",
    "operator_no_profitability_acceptance_confirmation",
    "operator_authority_digest_confirmations_match",
    "position_swing_registry_approval_created_true",
    "position_swing_registry_eligibility_true",
    "position_swing_registry_activation_true",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
]


class PositionSwingRegistryApprovalCeremonyError(ValueError):
    """Raised when a POSITION_SWING registry approval ceremony violates guardrails."""


def _check(check_id: str, expected: Any, actual: Any, *, severity: str = BLOCKER) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": f"{check_id} passed" if status == PASS else f"{check_id} failed",
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise PositionSwingRegistryApprovalCeremonyError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PositionSwingRegistryApprovalCeremonyError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PositionSwingRegistryApprovalCeremonyError(f"{field_name} must be true")


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


def _expected_operator_authority_confirmations() -> dict[str, Any]:
    return {
        "identity": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "calendar": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition": registry.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
        "swing": registry.EXPECTED_SWING_CANONICAL_DATASET_FROZEN_DIGEST,
        "swing_registry": registry.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
    }


def _operator_authority_confirmations(attestation: dict[str, Any]) -> dict[str, Any]:
    return {
        "identity": attestation.get("operator_confirms_identity_frozen_digest"),
        "calendar": attestation.get("operator_confirms_calendar_frozen_digest"),
        "schedule": attestation.get("operator_confirms_schedule_digest"),
        "split": attestation.get("operator_confirms_split_event_frozen_digest"),
        "dividend": attestation.get("operator_confirms_dividend_event_frozen_digest"),
        "acquisition": attestation.get("operator_confirms_acquisition_generation_frozen_digest"),
        "swing": attestation.get("operator_confirms_swing_frozen_digest"),
        "swing_registry": attestation.get("operator_confirms_swing_registry_approval_digest"),
    }


def _source_review_package(registry_review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(registry_review_package)
        if registry_review_package is not None
        else review.build_position_swing_registry_approval_candidate_review_package_v1()
    )
    try:
        validation = review.validate_position_swing_registry_approval_candidate_review_package_v1(source_review)
    except review.PositionSwingRegistryOperatorReviewError as exc:
        raise PositionSwingRegistryApprovalCeremonyError(f"source registry review package invalid: {exc}") from exc
    _expect(validation["review_package_digest"], EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST, "source registry review package digest")
    _expect(validation["failed_checks"], 0, "source registry review failed check count")
    _expect(validation["blocker_count"], 0, "source registry review blocker count")
    return source_review


def build_position_swing_registry_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_registry_review_package_digest: str,
    operator_confirms_registry_candidate_digest: str,
    operator_confirms_registry_key: str,
    operator_confirms_position_swing_frozen_digest: str,
    operator_confirms_dataset_rows_digest: str,
    operator_confirms_dataset_manifest_digest: str,
    operator_confirms_identity_frozen_digest: str,
    operator_confirms_calendar_frozen_digest: str,
    operator_confirms_schedule_digest: str,
    operator_confirms_split_event_frozen_digest: str,
    operator_confirms_dividend_event_frozen_digest: str,
    operator_confirms_acquisition_generation_frozen_digest: str,
    operator_confirms_swing_frozen_digest: str,
    operator_confirms_swing_registry_approval_digest: str,
    operator_confirms_registry_scope_research_dataset: bool,
    operator_confirms_runtime_use_not_authorized: bool,
    operator_confirms_strategy_use_not_authorized: bool,
    operator_confirms_no_strategy_runtime_migration: bool,
    operator_confirms_no_predictive_usefulness: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_POSITION_SWING_REGISTRY_ENTRY,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for POSITION_SWING registry approval."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_registry_review_package_digest": operator_confirms_registry_review_package_digest,
        "operator_confirms_registry_candidate_digest": operator_confirms_registry_candidate_digest,
        "operator_confirms_registry_key": operator_confirms_registry_key,
        "operator_confirms_position_swing_frozen_digest": operator_confirms_position_swing_frozen_digest,
        "operator_confirms_dataset_rows_digest": operator_confirms_dataset_rows_digest,
        "operator_confirms_dataset_manifest_digest": operator_confirms_dataset_manifest_digest,
        "operator_confirms_identity_frozen_digest": operator_confirms_identity_frozen_digest,
        "operator_confirms_calendar_frozen_digest": operator_confirms_calendar_frozen_digest,
        "operator_confirms_schedule_digest": operator_confirms_schedule_digest,
        "operator_confirms_split_event_frozen_digest": operator_confirms_split_event_frozen_digest,
        "operator_confirms_dividend_event_frozen_digest": operator_confirms_dividend_event_frozen_digest,
        "operator_confirms_acquisition_generation_frozen_digest": operator_confirms_acquisition_generation_frozen_digest,
        "operator_confirms_swing_frozen_digest": operator_confirms_swing_frozen_digest,
        "operator_confirms_swing_registry_approval_digest": operator_confirms_swing_registry_approval_digest,
        "operator_confirms_registry_scope_research_dataset": operator_confirms_registry_scope_research_dataset,
        "operator_confirms_runtime_use_not_authorized": operator_confirms_runtime_use_not_authorized,
        "operator_confirms_strategy_use_not_authorized": operator_confirms_strategy_use_not_authorized,
        "operator_confirms_no_strategy_runtime_migration": operator_confirms_no_strategy_runtime_migration,
        "operator_confirms_no_predictive_usefulness": operator_confirms_no_predictive_usefulness,
        "operator_confirms_no_profitability_acceptance": operator_confirms_no_profitability_acceptance,
    }


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_POSITION_SWING_REGISTRY_ENTRY, None),
            _check("operator_attestation_phrase_matches", REQUIRED_POSITION_SWING_REGISTRY_APPROVAL_ATTESTATION_PHRASE, None),
            _check("operator_review_digest_confirmation_matches", EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_candidate_digest_confirmation_matches", EXPECTED_REGISTRY_CANDIDATE_DIGEST, None),
            _check("operator_registry_key_confirmation_matches", registry.PROPOSED_REGISTRY_KEY, None),
            _check("operator_position_swing_frozen_digest_confirmation_matches", registry.EXPECTED_POSITION_SWING_FROZEN_DIGEST, None),
            _check("operator_dataset_rows_digest_confirmation_matches", registry.EXPECTED_DATASET_ROWS_DIGEST, None),
            _check("operator_dataset_manifest_digest_confirmation_matches", registry.EXPECTED_DATASET_MANIFEST_DIGEST, None),
            _check("operator_registry_scope_confirmation_research_dataset", True, None),
            _check("operator_runtime_use_not_authorized_confirmation", True, None),
            _check("operator_strategy_use_not_authorized_confirmation", True, None),
            _check("operator_no_strategy_runtime_migration_confirmation", True, None),
            _check("operator_no_predictive_usefulness_confirmation", True, None),
            _check("operator_no_profitability_acceptance_confirmation", True, None),
            _check("operator_authority_digest_confirmations_match", _expected_operator_authority_confirmations(), None),
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_POSITION_SWING_REGISTRY_ENTRY, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_POSITION_SWING_REGISTRY_APPROVAL_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check("operator_review_digest_confirmation_matches", EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_registry_review_package_digest")),
        _check("operator_candidate_digest_confirmation_matches", EXPECTED_REGISTRY_CANDIDATE_DIGEST, attestation.get("operator_confirms_registry_candidate_digest")),
        _check("operator_registry_key_confirmation_matches", registry.PROPOSED_REGISTRY_KEY, attestation.get("operator_confirms_registry_key")),
        _check("operator_position_swing_frozen_digest_confirmation_matches", registry.EXPECTED_POSITION_SWING_FROZEN_DIGEST, attestation.get("operator_confirms_position_swing_frozen_digest")),
        _check("operator_dataset_rows_digest_confirmation_matches", registry.EXPECTED_DATASET_ROWS_DIGEST, attestation.get("operator_confirms_dataset_rows_digest")),
        _check("operator_dataset_manifest_digest_confirmation_matches", registry.EXPECTED_DATASET_MANIFEST_DIGEST, attestation.get("operator_confirms_dataset_manifest_digest")),
        _check("operator_registry_scope_confirmation_research_dataset", True, attestation.get("operator_confirms_registry_scope_research_dataset")),
        _check("operator_runtime_use_not_authorized_confirmation", True, attestation.get("operator_confirms_runtime_use_not_authorized")),
        _check("operator_strategy_use_not_authorized_confirmation", True, attestation.get("operator_confirms_strategy_use_not_authorized")),
        _check("operator_no_strategy_runtime_migration_confirmation", True, attestation.get("operator_confirms_no_strategy_runtime_migration")),
        _check("operator_no_predictive_usefulness_confirmation", True, attestation.get("operator_confirms_no_predictive_usefulness")),
        _check("operator_no_profitability_acceptance_confirmation", True, attestation.get("operator_confirms_no_profitability_acceptance")),
        _check("operator_authority_digest_confirmations_match", _expected_operator_authority_confirmations(), _operator_authority_confirmations(attestation)),
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise PositionSwingRegistryApprovalCeremonyError("operator_attestation must be a JSON object")
    for field in ("operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise PositionSwingRegistryApprovalCeremonyError(f"{field} must be a non-empty string")
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise PositionSwingRegistryApprovalCeremonyError(f"operator attestation failed: {failed[0]['check_id']}")
    return deepcopy(attestation)


def _review_evidence(source_review: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_registry_review_package_kind": source_review["artifact_kind"],
        "source_registry_review_status": source_review["review_status"],
        "source_registry_review_package_digest": source_review[
            "position_swing_registry_review_package_semantic_digest"
        ],
        "source_registry_review_checklist_total": source_review["review_summary"]["total_checks"],
        "source_registry_review_checklist_passed": source_review["review_summary"]["passed_checks"],
        "source_registry_review_checklist_failed": source_review["review_summary"]["failed_checks"],
        "source_registry_review_blocker_count": source_review["review_summary"]["blocker_count"],
        "source_registry_candidate_kind": source_review["reviewed_registry_candidate_kind"],
        "source_registry_candidate_status": source_review["reviewed_registry_candidate_status"],
        "source_registry_candidate_digest": source_review["reviewed_registry_candidate_digest"],
        "proposed_registry_key": source_review["reviewed_proposed_registry_key"],
        "registry_key": source_review["reviewed_proposed_registry_key"],
        "registry_scope": source_review["reviewed_registry_scope"],
        "position_swing_canonical_dataset_frozen": source_review["position_swing_canonical_dataset_frozen"],
        "position_swing_canonical_dataset_frozen_digest": source_review[
            "position_swing_canonical_dataset_frozen_digest"
        ],
        "position_swing_review_package_digest": source_review["position_swing_review_package_digest"],
        "position_swing_candidate_digest": source_review["position_swing_candidate_digest"],
        "dataset_rows_digest": source_review["dataset_rows_digest"],
        "dataset_manifest_digest": source_review["dataset_manifest_digest"],
        "source_rows_digest": source_review["source_rows_digest"],
        "materialization_receipt_digest": source_review["materialization_receipt_digest"],
        "dataset_profile": source_review["dataset_profile"],
        "dataset_bar_rule": source_review["dataset_bar_rule"],
        "position_swing_bar_count": source_review["position_swing_bar_count"],
        "source_rth_rows_consumed": source_review["source_rth_rows_consumed"],
        "source_rth_rows_excluded": source_review["source_rth_rows_excluded"],
        "full_sessions_used": source_review["full_sessions_used"],
        "special_session_policy": source_review["special_session_policy"],
        "special_sessions_excluded": source_review["special_sessions_excluded"],
        "special_session_rows_excluded": source_review["special_session_rows_excluded"],
        "cross_check_2025_01_status": source_review["cross_check_2025_01_status"],
        "cross_check_2025_01_position_swing_bars": source_review["cross_check_2025_01_position_swing_bars"],
        "in_range_dividends_found": source_review["in_range_dividends_found"],
        "in_range_dividend_count": source_review["in_range_dividend_count"],
        "in_range_dividend_implication": source_review["in_range_dividend_implication"],
        "source_adjusted_data_used": source_review["source_adjusted_data_used"],
        **_authority_digests(),
        **_fixed_segment(),
    }


def _approval_checklist(approved: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("registry_review_package_digest_matches_expected", EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST, approved.get("source_registry_review_package_digest")),
        _check("registry_review_package_has_zero_blockers", EXPECTED_REGISTRY_REVIEW_BLOCKER_COUNT, approved.get("source_registry_review_blocker_count")),
        _check("registry_candidate_digest_matches_expected", EXPECTED_REGISTRY_CANDIDATE_DIGEST, approved.get("source_registry_candidate_digest")),
        _check("registry_key_matches_expected", registry.PROPOSED_REGISTRY_KEY, approved.get("registry_key")),
        _check("registry_scope_research_dataset", registry.PROPOSED_REGISTRY_SCOPE, approved.get("registry_scope")),
        _check("position_swing_canonical_dataset_frozen_true", True, approved.get("position_swing_canonical_dataset_frozen")),
        _check("position_swing_frozen_digest_matches_expected", registry.EXPECTED_POSITION_SWING_FROZEN_DIGEST, approved.get("position_swing_canonical_dataset_frozen_digest")),
        _check("dataset_rows_digest_matches_expected", registry.EXPECTED_DATASET_ROWS_DIGEST, approved.get("dataset_rows_digest")),
        _check("dataset_manifest_digest_matches_expected", registry.EXPECTED_DATASET_MANIFEST_DIGEST, approved.get("dataset_manifest_digest")),
        _check("dataset_profile_position_swing", position.DATASET_PROFILE_POSITION_SWING, approved.get("dataset_profile")),
        _check("dataset_bar_rule_rth_full_session_1d", position.DATASET_BAR_RULE_RTH_FULL_SESSION_1D, approved.get("dataset_bar_rule")),
        _check("position_swing_bar_count_994", registry.EXPECTED_POSITION_SWING_BAR_COUNT, approved.get("position_swing_bar_count")),
        _check("cross_check_2025_01_passed", registry.EXPECTED_CROSS_CHECK_STATUS, approved.get("cross_check_2025_01_status")),
        _check("special_session_policy_preserved", registry.EXPECTED_SPECIAL_SESSION_POLICY, approved.get("special_session_policy")),
        _check("dividend_implication_preserved", acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, approved.get("in_range_dividend_implication")),
        _check("swing_registry_approval_digest_bound", registry.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST, approved.get("swing_registry_approval_digest")),
        *_attestation_checks(approved.get("operator_attestation") if isinstance(approved.get("operator_attestation"), dict) else None),
        _check("position_swing_registry_approval_created_true", True, approved.get("position_swing_registry_approval_created")),
        _check("position_swing_registry_eligibility_true", True, approved.get("position_swing_registry_eligibility")),
        _check("position_swing_registry_activation_true", True, approved.get("position_swing_registry_activation")),
        _check("runtime_use_not_authorized", registry.NOT_AUTHORIZED, approved.get("runtime_use")),
        _check("strategy_use_not_authorized", registry.NOT_AUTHORIZED, approved.get("strategy_use")),
        _check("strategy_runtime_migration_false", False, approved.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, approved.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, approved.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, approved.get("profitability"), severity=INFO),
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
        "position_swing_registry_approval_authorized_by_operator": failed == 0,
        "software_runtime_migration_authorized": False,
        "software_strategy_use_authorized": False,
    }


def _digest_payload(approved_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approved_artifact)
    payload.pop("position_swing_registry_approved_semantic_digest", None)
    return payload


def position_swing_registry_approved_semantic_digest_v1(approved_artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a POSITION_SWING registry approval artifact."""
    return semantic_digest(_digest_payload(approved_artifact))


def build_position_swing_registry_approved_v1(
    *,
    registry_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build an offline POSITION_SWING registry-approved artifact for the research dataset entry."""
    source_review = _source_review_package(registry_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    approved = {
        "artifact_kind": ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVED,
        "schema_version": SCHEMA_VERSION_POSITION_SWING_REGISTRY_APPROVAL_V1,
        "approval_status": POSITION_SWING_REGISTRY_APPROVED,
        "position_swing_registry_approval_created": True,
        "position_swing_registry_eligibility": True,
        "position_swing_registry_activation": True,
        "runtime_use": registry.NOT_AUTHORIZED,
        "strategy_use": registry.NOT_AUTHORIZED,
        "strategy_runtime_migration": False,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "operator_attestation": attestation,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_POSITION_SWING_REGISTRY_APPROVAL),
        **_review_evidence(source_review),
    }
    checklist = _approval_checklist(approved)
    approved["approval_checklist"] = checklist
    approved["approval_summary"] = _summary(checklist)
    approved["position_swing_registry_approved_semantic_digest"] = (
        position_swing_registry_approved_semantic_digest_v1(approved)
    )
    validate_position_swing_registry_approved_v1(approved)
    return approved


def validate_position_swing_registry_approved_v1(approved_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate POSITION_SWING registry approval while preserving runtime and strategy guardrails."""
    if not isinstance(approved_artifact, dict):
        raise PositionSwingRegistryApprovalCeremonyError("approved artifact must be a JSON object")
    _expect(approved_artifact.get("artifact_kind"), ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVED, "artifact_kind")
    _expect(approved_artifact.get("schema_version"), SCHEMA_VERSION_POSITION_SWING_REGISTRY_APPROVAL_V1, "schema_version")
    _expect(approved_artifact.get("approval_status"), POSITION_SWING_REGISTRY_APPROVED, "approval_status")
    for field in (
        "position_swing_registry_approval_created",
        "position_swing_registry_eligibility",
        "position_swing_registry_activation",
        "created_offline",
        "position_swing_canonical_dataset_frozen",
        "in_range_dividends_found",
        "source_adjusted_data_used",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "strategy_runtime_migration",
        "provider_requests_made_in_approval",
        "automatic_stitching",
    ):
        _expect_false(approved_artifact.get(field), field)
    _expect(approved_artifact.get("runtime_use"), registry.NOT_AUTHORIZED, "runtime_use")
    _expect(approved_artifact.get("strategy_use"), registry.NOT_AUTHORIZED, "strategy_use")
    _expect(approved_artifact.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(approved_artifact.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "source_registry_review_package_kind": review.ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE,
        "source_registry_review_status": review.POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY,
        "source_registry_review_package_digest": EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST,
        "source_registry_review_checklist_total": EXPECTED_REGISTRY_REVIEW_CHECKLIST_TOTAL,
        "source_registry_review_checklist_passed": EXPECTED_REGISTRY_REVIEW_CHECKLIST_PASSED,
        "source_registry_review_checklist_failed": EXPECTED_REGISTRY_REVIEW_CHECKLIST_FAILED,
        "source_registry_review_blocker_count": EXPECTED_REGISTRY_REVIEW_BLOCKER_COUNT,
        "source_registry_candidate_kind": registry.ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE,
        "source_registry_candidate_status": registry.POSITION_SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW,
        "source_registry_candidate_digest": EXPECTED_REGISTRY_CANDIDATE_DIGEST,
        "proposed_registry_key": registry.PROPOSED_REGISTRY_KEY,
        "registry_key": registry.PROPOSED_REGISTRY_KEY,
        "registry_scope": registry.PROPOSED_REGISTRY_SCOPE,
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
        _expect(approved_artifact.get(field), expected, field)
    _validated_operator_attestation(approved_artifact.get("operator_attestation"))
    _expect(
        approved_artifact.get("remaining_roadmap"),
        REMAINING_ROADMAP_AFTER_POSITION_SWING_REGISTRY_APPROVAL,
        "remaining_roadmap",
    )
    checklist = _approval_checklist(approved_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_APPROVAL_CHECK_IDS, "approval_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise PositionSwingRegistryApprovalCeremonyError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(approved_artifact.get("approval_checklist"), checklist, "approval_checklist")
    summary = _summary(checklist)
    _expect(approved_artifact.get("approval_summary"), summary, "approval_summary")
    _expect_true(
        summary.get("position_swing_registry_approval_authorized_by_operator"),
        "position_swing_registry_approval_authorized_by_operator",
    )
    _expect_false(summary.get("software_runtime_migration_authorized"), "software_runtime_migration_authorized")
    _expect_false(summary.get("software_strategy_use_authorized"), "software_strategy_use_authorized")
    digest = approved_artifact.get("position_swing_registry_approved_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PositionSwingRegistryApprovalCeremonyError("position_swing_registry_approved_semantic_digest missing")
    _expect(
        digest,
        position_swing_registry_approved_semantic_digest_v1(approved_artifact),
        "position_swing_registry_approved_semantic_digest",
    )
    return {
        "status": "POSITION_SWING_REGISTRY_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "position_swing_registry_approved_semantic_digest": digest,
        "registry_key": registry.PROPOSED_REGISTRY_KEY,
        "registry_scope": registry.PROPOSED_REGISTRY_SCOPE,
        "source_registry_review_package_digest": EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST,
        "source_registry_candidate_digest": EXPECTED_REGISTRY_CANDIDATE_DIGEST,
        "position_swing_canonical_dataset_frozen_digest": registry.EXPECTED_POSITION_SWING_FROZEN_DIGEST,
        "dataset_rows_digest": registry.EXPECTED_DATASET_ROWS_DIGEST,
        "dataset_manifest_digest": registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "position_swing_registry_approval_created": True,
        "position_swing_registry_eligibility": True,
        "position_swing_registry_activation": True,
        "runtime_use": registry.NOT_AUTHORIZED,
        "strategy_use": registry.NOT_AUTHORIZED,
        "strategy_runtime_migration": False,
        "provider_requests_made_in_approval": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_position_swing_registry_approved_markdown_v1(approved_artifact: dict[str, Any]) -> str:
    """Render a sanitized POSITION_SWING registry approval status document."""
    validation = validate_position_swing_registry_approved_v1(approved_artifact)
    attestation = approved_artifact["operator_attestation"]
    summary = approved_artifact["approval_summary"]
    lines = [
        "# MarketFlow POSITION_SWING Registry Approval Status",
        "",
        "## Title",
        "- POSITION_SWING Registry Approval Ceremony v1.",
        "",
        "## Approved Registry Entry",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Registry key: `{approved_artifact['registry_key']}`",
        f"- Registry scope: `{approved_artifact['registry_scope']}`",
        f"- POSITION_SWING registry approval created: `{approved_artifact['position_swing_registry_approval_created']}`",
        f"- POSITION_SWING registry eligibility: `{approved_artifact['position_swing_registry_eligibility']}`",
        f"- POSITION_SWING registry activation: `{approved_artifact['position_swing_registry_activation']}`",
        f"- Approval digest: `{validation['position_swing_registry_approved_semantic_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        "",
        "## Source Registry Review Package",
        f"- Review package kind: `{approved_artifact['source_registry_review_package_kind']}`",
        f"- Review status: `{approved_artifact['source_registry_review_status']}`",
        f"- Review package digest: `{approved_artifact['source_registry_review_package_digest']}`",
        f"- Registry candidate digest: `{approved_artifact['source_registry_candidate_digest']}`",
        f"- Review checks: `{approved_artifact['source_registry_review_checklist_passed']}` passed of `{approved_artifact['source_registry_review_checklist_total']}`",
        f"- Review blockers: `{approved_artifact['source_registry_review_blocker_count']}`",
        "",
        "## Frozen POSITION_SWING Dataset Evidence",
        f"- POSITION_SWING frozen digest: `{approved_artifact['position_swing_canonical_dataset_frozen_digest']}`",
        f"- Dataset rows digest: `{approved_artifact['dataset_rows_digest']}`",
        f"- Dataset manifest digest: `{approved_artifact['dataset_manifest_digest']}`",
        f"- Dataset profile: `{approved_artifact['dataset_profile']}`",
        f"- Dataset bar rule: `{approved_artifact['dataset_bar_rule']}`",
        f"- POSITION_SWING bar count: `{approved_artifact['position_swing_bar_count']}`",
        "",
        "## Registry Scope",
        f"- Ticker: `{approved_artifact['ticker']}`",
        f"- Composite FIGI: `{approved_artifact['composite_figi']}`",
        f"- Share class FIGI: `{approved_artifact['share_class_figi']}`",
        f"- Primary MIC: `{approved_artifact['primary_mic']}`",
        f"- Security type: `{approved_artifact['security_type']}`",
        f"- Segment: `{approved_artifact['segment_start']}` through `{approved_artifact['segment_end']}`",
        "",
        "## Runtime Boundary",
        f"- Runtime use: `{approved_artifact['runtime_use']}`",
        f"- Strategy use: `{approved_artifact['strategy_use']}`",
        f"- Strategy runtime migration: `{approved_artifact['strategy_runtime_migration']}`",
        f"- Automatic stitching: `{approved_artifact['automatic_stitching']}`",
        f"- Predictive usefulness: `{approved_artifact['predictive_usefulness']}`",
        f"- Profitability: `{approved_artifact['profitability']}`",
        "",
        "## Authority Bindings",
        f"- Identity frozen digest: `{approved_artifact['identity_frozen_digest']}`",
        f"- Calendar frozen digest: `{approved_artifact['calendar_frozen_digest']}`",
        f"- Schedule digest: `{approved_artifact['schedule_digest']}`",
        f"- Split-event audit frozen digest: `{approved_artifact['split_event_frozen_digest']}`",
        f"- Dividend-event audit frozen digest: `{approved_artifact['dividend_event_frozen_digest']}`",
        f"- Acquisition generation frozen digest: `{approved_artifact['acquisition_generation_frozen_digest']}`",
        f"- SWING canonical dataset frozen digest: `{approved_artifact['swing_canonical_dataset_frozen_digest']}`",
        f"- SWING registry approval digest: `{approved_artifact['swing_registry_approval_digest']}`",
        "",
        "## Approval Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        f"- Registry approval authorized by operator: `{summary['position_swing_registry_approval_authorized_by_operator']}`",
        f"- Runtime migration authorized: `{summary['software_runtime_migration_authorized']}`",
        f"- Strategy use authorized: `{summary['software_strategy_use_authorized']}`",
        "",
        "## Remaining Roadmap",
    ]
    lines.extend(f"{index}. {task}" for index, task in enumerate(approved_artifact["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made in approval: `False`",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No acquisition rows or POSITION_SWING bars were regenerated.",
            "- No Strategy runtime migration occurred.",
            "- Runtime use and strategy use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
        ]
    )
    return "\n".join(lines)


def write_position_swing_registry_approved_v1(
    output_dir: str | Path,
    *,
    registry_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the POSITION_SWING registry approval JSON artifact without overwriting output."""
    approved = build_position_swing_registry_approved_v1(
        registry_review_package=registry_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_position_swing_registry_approved_v1(approved)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_registry_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PositionSwingRegistryApprovalCeremonyError(
            "POSITION_SWING registry approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PositionSwingRegistryApprovalCeremonyError("POSITION_SWING registry approval output already exists")
    payload = canonical_json_bytes(approved)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
