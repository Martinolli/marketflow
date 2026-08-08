"""Offline operator freeze ceremony for SWING canonical dataset evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import swing_canonical_dataset_operator_review_service as review
from marketflow.services import swing_canonical_dataset_service as swing


ARTIFACT_KIND_SWING_CANONICAL_DATASET_FROZEN = "SWING_CANONICAL_DATASET_FROZEN"
SCHEMA_VERSION_SWING_CANONICAL_DATASET_OPERATOR_FREEZE_V1 = "swing_canonical_dataset_operator_freeze_v1"
SWING_CANONICAL_DATASET_FROZEN = "SWING_CANONICAL_DATASET_FROZEN"
OPERATOR_DECISION_APPROVE_SWING_CANONICAL_DATASET_FREEZE = "APPROVE_SWING_CANONICAL_DATASET_FREEZE"
OPERATOR_ATTESTATION_VERSION_V1 = "swing_canonical_dataset_operator_attestation_v1"
REQUIRED_SWING_CANONICAL_DATASET_OPERATOR_ATTESTATION_PHRASE = (
    "FREEZE SWING CANONICAL DATASET AAPL BBG000B9XRY4 BBG001S5N8V8 XNAS CS "
    "2022-01-01 2025-12-31 RTH_HALF_SESSION_195M 1988_BARS"
)

EXPECTED_SWING_REVIEW_PACKAGE_DIGEST = "1fe4efabfef575956cd4578da5ae060655e420062bf40b24b83cd0d4643bf98d"
EXPECTED_SWING_CANDIDATE_DIGEST = review.EXPECTED_REVIEWED_CANDIDATE_DIGEST
EXPECTED_DATASET_ROWS_DIGEST = review.EXPECTED_REVIEWED_DATASET_ROWS_DIGEST
EXPECTED_DATASET_MANIFEST_DIGEST = review.EXPECTED_REVIEWED_DATASET_MANIFEST_DIGEST
EXPECTED_SOURCE_ROWS_DIGEST = review.EXPECTED_SOURCE_ROWS_DIGEST
EXPECTED_MATERIALIZATION_RECEIPT_DIGEST = review.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST
EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST = review.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST
EXPECTED_SWING_BAR_COUNT = review.EXPECTED_SWING_BAR_COUNT
EXPECTED_SOURCE_RTH_ROWS_CONSUMED = review.EXPECTED_SOURCE_RTH_ROWS_CONSUMED
EXPECTED_SOURCE_RTH_ROWS_EXCLUDED = review.EXPECTED_SOURCE_RTH_ROWS_EXCLUDED
EXPECTED_FULL_SESSIONS_USED = review.EXPECTED_FULL_SESSIONS_USED
EXPECTED_SPECIAL_SESSIONS_EXCLUDED = review.EXPECTED_SPECIAL_SESSIONS_EXCLUDED
EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED = review.EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED
EXPECTED_CROSS_CHECK_STATUS = review.EXPECTED_CROSS_CHECK_STATUS
EXPECTED_CROSS_CHECK_SWING_BARS = review.EXPECTED_CROSS_CHECK_SWING_BARS
EXPECTED_SPECIAL_SESSION_POLICY = "FULL_ORDINARY_SESSIONS_ONLY"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OPERATOR_BOUNDARY_CONFIRMATION_FIELDS = [
    "operator_confirms_no_provider_requests_in_freeze",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_strategy_runtime_migration",
    "operator_confirms_no_predictive_usefulness",
    "operator_confirms_no_profitability_acceptance",
]

REMAINING_ROADMAP_AFTER_SWING_CANONICAL_DATASET_FREEZE = [
    "SWING registry approval.",
    "POSITION_SWING canonical dataset candidate.",
    "POSITION_SWING canonical dataset operator review.",
    "POSITION_SWING canonical dataset freeze.",
    "POSITION_SWING registry approval.",
    "Normal runtime migration.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
]

REQUIRED_FREEZE_CHECK_IDS = [
    "swing_review_package_digest_matches_expected",
    "swing_review_package_has_zero_blockers",
    "swing_candidate_digest_matches_expected",
    "dataset_rows_digest_matches_expected",
    "dataset_manifest_digest_matches_expected",
    "source_rows_digest_matches_expected",
    "materialization_receipt_digest_matches_expected",
    "acquisition_generation_frozen_digest_matches_expected",
    "identity_frozen_digest_matches_expected",
    "calendar_frozen_digest_matches_expected",
    "schedule_digest_matches_expected",
    "split_event_frozen_digest_matches_expected",
    "dividend_event_frozen_digest_matches_expected",
    "dataset_profile_swing",
    "dataset_bar_rule_rth_half_session_195m",
    "swing_bar_count_1988",
    "source_rth_rows_consumed_25844",
    "source_rth_rows_excluded_126",
    "full_sessions_used_994",
    "special_sessions_excluded_9",
    "special_session_rows_excluded_126",
    "cross_check_2025_01_passed",
    "cross_check_2025_01_swing_bars_40",
    "special_session_policy_preserved",
    "dividend_implication_preserved",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_review_digest_confirmation_matches",
    "operator_candidate_digest_confirmation_matches",
    "operator_dataset_rows_digest_confirmation_matches",
    "operator_dataset_manifest_digest_confirmation_matches",
    "operator_source_rows_digest_confirmation_matches",
    "operator_materialization_receipt_confirmation_matches",
    "operator_acquisition_digest_confirmation_matches",
    "operator_authority_digest_confirmations_match",
    "operator_confirms_swing_bar_count",
    "operator_confirms_2025_01_cross_check",
    "operator_confirms_special_session_policy",
    "operator_confirms_dividend_implication",
    "operator_confirms_no_provider_requests_in_freeze",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_strategy_runtime_migration",
    "operator_confirms_no_predictive_usefulness",
    "operator_confirms_no_profitability_acceptance",
    "swing_canonical_dataset_frozen_true",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "no_registry_approval_present",
]


class SwingCanonicalDatasetOperatorFreezeError(ValueError):
    """Raised when SWING dataset freeze ceremony data violates guardrails."""


def _check(check_id: str, expected: Any, actual: Any, *, message: str | None = None) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": message
        or ("SWING canonical dataset freeze evidence matches" if status == PASS else "SWING canonical dataset freeze evidence mismatch"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise SwingCanonicalDatasetOperatorFreezeError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise SwingCanonicalDatasetOperatorFreezeError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise SwingCanonicalDatasetOperatorFreezeError(f"{field_name} must be true")


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


def _source_review_package(swing_review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(swing_review_package)
        if swing_review_package is not None
        else review.build_swing_canonical_dataset_candidate_review_package_v1()
    )
    try:
        validation = review.validate_swing_canonical_dataset_candidate_review_package_v1(source_review)
    except review.SwingCanonicalDatasetOperatorReviewError as exc:
        raise SwingCanonicalDatasetOperatorFreezeError(f"source SWING review package invalid: {exc}") from exc
    _expect(validation["review_package_digest"], EXPECTED_SWING_REVIEW_PACKAGE_DIGEST, "source SWING review package semantic digest")
    _expect(validation["failed_checks"], 0, "source SWING review failed check count")
    _expect(validation["blocker_count"], 0, "source SWING review blocker count")
    return source_review


def build_swing_canonical_dataset_operator_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_swing_review_package_digest: str,
    operator_confirms_swing_candidate_digest: str,
    operator_confirms_dataset_rows_digest: str,
    operator_confirms_dataset_manifest_digest: str,
    operator_confirms_source_rows_digest: str,
    operator_confirms_materialization_receipt_digest: str,
    operator_confirms_acquisition_generation_frozen_digest: str,
    operator_confirms_identity_frozen_digest: str,
    operator_confirms_calendar_frozen_digest: str,
    operator_confirms_schedule_digest: str,
    operator_confirms_split_event_frozen_digest: str,
    operator_confirms_dividend_event_frozen_digest: str,
    operator_confirms_swing_bar_count: int,
    operator_confirms_2025_01_cross_check_passed: bool,
    operator_confirms_special_session_policy: bool,
    operator_confirms_dividend_implication: bool,
    operator_confirms_no_provider_requests_in_freeze: bool = True,
    operator_confirms_no_registry_approval: bool = True,
    operator_confirms_no_strategy_runtime_migration: bool = True,
    operator_confirms_no_predictive_usefulness: bool = True,
    operator_confirms_no_profitability_acceptance: bool = True,
    operator_decision: str = OPERATOR_DECISION_APPROVE_SWING_CANONICAL_DATASET_FREEZE,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for SWING dataset freeze."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_swing_review_package_digest": operator_confirms_swing_review_package_digest,
        "operator_confirms_swing_candidate_digest": operator_confirms_swing_candidate_digest,
        "operator_confirms_dataset_rows_digest": operator_confirms_dataset_rows_digest,
        "operator_confirms_dataset_manifest_digest": operator_confirms_dataset_manifest_digest,
        "operator_confirms_source_rows_digest": operator_confirms_source_rows_digest,
        "operator_confirms_materialization_receipt_digest": operator_confirms_materialization_receipt_digest,
        "operator_confirms_acquisition_generation_frozen_digest": operator_confirms_acquisition_generation_frozen_digest,
        "operator_confirms_identity_frozen_digest": operator_confirms_identity_frozen_digest,
        "operator_confirms_calendar_frozen_digest": operator_confirms_calendar_frozen_digest,
        "operator_confirms_schedule_digest": operator_confirms_schedule_digest,
        "operator_confirms_split_event_frozen_digest": operator_confirms_split_event_frozen_digest,
        "operator_confirms_dividend_event_frozen_digest": operator_confirms_dividend_event_frozen_digest,
        "operator_confirms_swing_bar_count": operator_confirms_swing_bar_count,
        "operator_confirms_2025_01_cross_check_passed": operator_confirms_2025_01_cross_check_passed,
        "operator_confirms_special_session_policy": operator_confirms_special_session_policy,
        "operator_confirms_dividend_implication": operator_confirms_dividend_implication,
        "operator_confirms_no_provider_requests_in_freeze": operator_confirms_no_provider_requests_in_freeze,
        "operator_confirms_no_registry_approval": operator_confirms_no_registry_approval,
        "operator_confirms_no_strategy_runtime_migration": operator_confirms_no_strategy_runtime_migration,
        "operator_confirms_no_predictive_usefulness": operator_confirms_no_predictive_usefulness,
        "operator_confirms_no_profitability_acceptance": operator_confirms_no_profitability_acceptance,
    }


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_SWING_CANONICAL_DATASET_FREEZE, None),
            _check("operator_attestation_phrase_matches", REQUIRED_SWING_CANONICAL_DATASET_OPERATOR_ATTESTATION_PHRASE, None),
            _check("operator_review_digest_confirmation_matches", EXPECTED_SWING_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_candidate_digest_confirmation_matches", EXPECTED_SWING_CANDIDATE_DIGEST, None),
            _check("operator_dataset_rows_digest_confirmation_matches", EXPECTED_DATASET_ROWS_DIGEST, None),
            _check("operator_dataset_manifest_digest_confirmation_matches", EXPECTED_DATASET_MANIFEST_DIGEST, None),
            _check("operator_source_rows_digest_confirmation_matches", EXPECTED_SOURCE_ROWS_DIGEST, None),
            _check("operator_materialization_receipt_confirmation_matches", EXPECTED_MATERIALIZATION_RECEIPT_DIGEST, None),
            _check("operator_acquisition_digest_confirmation_matches", EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST, None),
            _check("operator_authority_digest_confirmations_match", _expected_operator_authority_confirmations(), None),
            _check("operator_confirms_swing_bar_count", EXPECTED_SWING_BAR_COUNT, None),
            _check("operator_confirms_2025_01_cross_check", True, None),
            _check("operator_confirms_special_session_policy", True, None),
            _check("operator_confirms_dividend_implication", True, None),
            *[_check(field, True, None) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_SWING_CANONICAL_DATASET_FREEZE, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_SWING_CANONICAL_DATASET_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check("operator_review_digest_confirmation_matches", EXPECTED_SWING_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_swing_review_package_digest")),
        _check("operator_candidate_digest_confirmation_matches", EXPECTED_SWING_CANDIDATE_DIGEST, attestation.get("operator_confirms_swing_candidate_digest")),
        _check("operator_dataset_rows_digest_confirmation_matches", EXPECTED_DATASET_ROWS_DIGEST, attestation.get("operator_confirms_dataset_rows_digest")),
        _check("operator_dataset_manifest_digest_confirmation_matches", EXPECTED_DATASET_MANIFEST_DIGEST, attestation.get("operator_confirms_dataset_manifest_digest")),
        _check("operator_source_rows_digest_confirmation_matches", EXPECTED_SOURCE_ROWS_DIGEST, attestation.get("operator_confirms_source_rows_digest")),
        _check(
            "operator_materialization_receipt_confirmation_matches",
            EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
            attestation.get("operator_confirms_materialization_receipt_digest"),
        ),
        _check(
            "operator_acquisition_digest_confirmation_matches",
            EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
            attestation.get("operator_confirms_acquisition_generation_frozen_digest"),
        ),
        _check("operator_authority_digest_confirmations_match", _expected_operator_authority_confirmations(), _operator_authority_confirmations(attestation)),
        _check("operator_confirms_swing_bar_count", EXPECTED_SWING_BAR_COUNT, attestation.get("operator_confirms_swing_bar_count")),
        _check("operator_confirms_2025_01_cross_check", True, attestation.get("operator_confirms_2025_01_cross_check_passed")),
        _check("operator_confirms_special_session_policy", True, attestation.get("operator_confirms_special_session_policy")),
        _check("operator_confirms_dividend_implication", True, attestation.get("operator_confirms_dividend_implication")),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
    ]


def _expected_operator_authority_confirmations() -> dict[str, str]:
    return {
        "identity": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "calendar": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
    }


def _operator_authority_confirmations(attestation: dict[str, Any]) -> dict[str, Any]:
    return {
        "identity": attestation.get("operator_confirms_identity_frozen_digest"),
        "calendar": attestation.get("operator_confirms_calendar_frozen_digest"),
        "schedule": attestation.get("operator_confirms_schedule_digest"),
        "split": attestation.get("operator_confirms_split_event_frozen_digest"),
        "dividend": attestation.get("operator_confirms_dividend_event_frozen_digest"),
    }


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise SwingCanonicalDatasetOperatorFreezeError("operator_attestation must be a JSON object")
    for field in ("operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise SwingCanonicalDatasetOperatorFreezeError(f"{field} must be a non-empty string")
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise SwingCanonicalDatasetOperatorFreezeError(f"operator attestation failed: {failed[0]['check_id']}")
    return deepcopy(attestation)


def _review_evidence(source_review: dict[str, Any]) -> dict[str, Any]:
    evidence = source_review["reviewed_swing_candidate_evidence"]
    return {
        "source_swing_review_package_kind": source_review["artifact_kind"],
        "source_swing_review_status": source_review["review_status"],
        "source_swing_review_package_semantic_digest": source_review["swing_canonical_dataset_review_package_semantic_digest"],
        "source_swing_review_checklist_total": source_review["review_summary"]["total_checks"],
        "source_swing_review_checklist_passed": source_review["review_summary"]["passed_checks"],
        "source_swing_review_checklist_failed": source_review["review_summary"]["failed_checks"],
        "source_swing_review_blocker_count": source_review["review_summary"]["blocker_count"],
        "source_swing_candidate_digest": evidence["reviewed_candidate_digest"],
        "source_dataset_rows_digest": evidence["reviewed_dataset_rows_digest"],
        "source_dataset_manifest_digest": evidence["reviewed_dataset_manifest_digest"],
        "source_normalized_rows_digest": evidence["reviewed_source_rows_digest"],
        "source_materialization_receipt_digest": evidence["reviewed_materialization_receipt_digest"],
        "source_acquisition_generation_frozen_digest": evidence["reviewed_acquisition_generation_frozen_digest"],
        "swing_bar_count": evidence["swing_bar_count"],
        "source_rth_rows_consumed": evidence["source_rth_rows_consumed"],
        "source_rth_rows_excluded": evidence["source_rth_rows_excluded"],
        "full_sessions_used": evidence["full_sessions_used"],
        "special_session_policy": evidence["special_session_policy"],
        "special_sessions_excluded": evidence["special_sessions_excluded"],
        "special_session_rows_excluded": evidence["special_session_rows_excluded"],
        "cross_check_2025_01_status": evidence["cross_check_status"],
        "cross_check_2025_01_swing_bars": evidence["cross_check_swing_bars"],
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        "source_adjusted_data_used": True,
    }


def _freeze_checklist(frozen: dict[str, Any]) -> list[dict[str, Any]]:
    bindings = frozen.get("authority_bindings", {})
    return [
        _check("swing_review_package_digest_matches_expected", EXPECTED_SWING_REVIEW_PACKAGE_DIGEST, frozen.get("source_swing_review_package_semantic_digest")),
        _check("swing_review_package_has_zero_blockers", 0, frozen.get("source_swing_review_blocker_count")),
        _check("swing_candidate_digest_matches_expected", EXPECTED_SWING_CANDIDATE_DIGEST, frozen.get("source_swing_candidate_digest")),
        _check("dataset_rows_digest_matches_expected", EXPECTED_DATASET_ROWS_DIGEST, frozen.get("source_dataset_rows_digest")),
        _check("dataset_manifest_digest_matches_expected", EXPECTED_DATASET_MANIFEST_DIGEST, frozen.get("source_dataset_manifest_digest")),
        _check("source_rows_digest_matches_expected", EXPECTED_SOURCE_ROWS_DIGEST, frozen.get("source_normalized_rows_digest")),
        _check("materialization_receipt_digest_matches_expected", EXPECTED_MATERIALIZATION_RECEIPT_DIGEST, frozen.get("source_materialization_receipt_digest")),
        _check("acquisition_generation_frozen_digest_matches_expected", EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST, frozen.get("source_acquisition_generation_frozen_digest")),
        _check("identity_frozen_digest_matches_expected", acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, bindings.get("identity_frozen_digest")),
        _check("calendar_frozen_digest_matches_expected", acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, bindings.get("calendar_frozen_digest")),
        _check("schedule_digest_matches_expected", acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, bindings.get("schedule_digest")),
        _check("split_event_frozen_digest_matches_expected", acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, bindings.get("split_event_frozen_digest")),
        _check("dividend_event_frozen_digest_matches_expected", acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST, bindings.get("dividend_event_frozen_digest")),
        _check("dataset_profile_swing", swing.DATASET_PROFILE_SWING, frozen.get("dataset_profile")),
        _check("dataset_bar_rule_rth_half_session_195m", swing.DATASET_BAR_RULE_RTH_HALF_SESSION_195M, frozen.get("dataset_bar_rule")),
        _check("swing_bar_count_1988", EXPECTED_SWING_BAR_COUNT, frozen.get("swing_bar_count")),
        _check("source_rth_rows_consumed_25844", EXPECTED_SOURCE_RTH_ROWS_CONSUMED, frozen.get("source_rth_rows_consumed")),
        _check("source_rth_rows_excluded_126", EXPECTED_SOURCE_RTH_ROWS_EXCLUDED, frozen.get("source_rth_rows_excluded")),
        _check("full_sessions_used_994", EXPECTED_FULL_SESSIONS_USED, frozen.get("full_sessions_used")),
        _check("special_sessions_excluded_9", EXPECTED_SPECIAL_SESSIONS_EXCLUDED, frozen.get("special_sessions_excluded")),
        _check("special_session_rows_excluded_126", EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED, frozen.get("special_session_rows_excluded")),
        _check("cross_check_2025_01_passed", EXPECTED_CROSS_CHECK_STATUS, frozen.get("cross_check_2025_01_status")),
        _check("cross_check_2025_01_swing_bars_40", EXPECTED_CROSS_CHECK_SWING_BARS, frozen.get("cross_check_2025_01_swing_bars")),
        _check("special_session_policy_preserved", EXPECTED_SPECIAL_SESSION_POLICY, frozen.get("special_session_policy")),
        _check("dividend_implication_preserved", acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, frozen.get("in_range_dividend_implication")),
        *_attestation_checks(frozen.get("operator_attestation") if isinstance(frozen.get("operator_attestation"), dict) else None),
        _check("swing_canonical_dataset_frozen_true", True, frozen.get("swing_canonical_dataset_frozen")),
        _check("canonical_eligibility_false", False, frozen.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, frozen.get("registry_eligibility")),
        _check("strategy_runtime_migration_false", False, frozen.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, frozen.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, frozen.get("predictive_usefulness")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, frozen.get("profitability")),
        _check("no_registry_approval_present", False, frozen.get("registry_approval_created", False)),
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
        "swing_canonical_dataset_freeze_authorized_by_operator": failed == 0,
        "software_auto_approval": False,
        "registry_approval_authorized": False,
        "runtime_migration_authorized": False,
    }


def _digest_payload(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(frozen_artifact)
    payload.pop("swing_canonical_dataset_frozen_semantic_digest", None)
    return payload


def swing_canonical_dataset_frozen_semantic_digest_v1(frozen_artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for frozen SWING dataset evidence."""
    return semantic_digest(_digest_payload(frozen_artifact))


def build_swing_canonical_dataset_frozen_v1(
    *,
    swing_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build an offline SWING canonical dataset frozen artifact."""
    source_review = _source_review_package(swing_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    frozen = {
        "artifact_kind": ARTIFACT_KIND_SWING_CANONICAL_DATASET_FROZEN,
        "schema_version": SCHEMA_VERSION_SWING_CANONICAL_DATASET_OPERATOR_FREEZE_V1,
        "freeze_status": SWING_CANONICAL_DATASET_FROZEN,
        "dataset_profile": swing.DATASET_PROFILE_SWING,
        "dataset_bar_rule": swing.DATASET_BAR_RULE_RTH_HALF_SESSION_195M,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "acquisition_generation_freeze": True,
        "swing_canonical_dataset_frozen": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "created_offline": True,
        "provider_requests_made_in_freeze": False,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "registry_approval_created": False,
        "operator_attestation": attestation,
        "authority_bindings": _authority_bindings(),
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_SWING_CANONICAL_DATASET_FREEZE),
        **_review_evidence(source_review),
    }
    checklist = _freeze_checklist(frozen)
    frozen["freeze_checklist"] = checklist
    frozen["freeze_summary"] = _summary(checklist)
    frozen["swing_canonical_dataset_frozen_semantic_digest"] = swing_canonical_dataset_frozen_semantic_digest_v1(frozen)
    validate_swing_canonical_dataset_frozen_v1(frozen)
    return frozen


def validate_swing_canonical_dataset_frozen_v1(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate frozen SWING canonical dataset evidence and guardrails."""
    if not isinstance(frozen_artifact, dict):
        raise SwingCanonicalDatasetOperatorFreezeError("frozen artifact must be a JSON object")
    _expect(frozen_artifact.get("artifact_kind"), ARTIFACT_KIND_SWING_CANONICAL_DATASET_FROZEN, "artifact_kind")
    _expect(frozen_artifact.get("schema_version"), SCHEMA_VERSION_SWING_CANONICAL_DATASET_OPERATOR_FREEZE_V1, "schema_version")
    _expect(frozen_artifact.get("freeze_status"), SWING_CANONICAL_DATASET_FROZEN, "freeze_status")
    for field in (
        "identity_segment_frozen",
        "calendar_operator_frozen",
        "split_event_audit_frozen",
        "dividend_event_audit_frozen",
        "acquisition_generation_freeze",
        "swing_canonical_dataset_frozen",
        "created_offline",
    ):
        _expect_true(frozen_artifact.get(field), field)
    for field in (
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
        "provider_requests_made_in_freeze",
        "registry_approval_created",
    ):
        _expect_false(frozen_artifact.get(field, False), field)
    _expect(frozen_artifact.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(frozen_artifact.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(frozen_artifact.get("source_swing_review_package_kind"), review.ARTIFACT_KIND_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE, "source_swing_review_package_kind")
    _expect(frozen_artifact.get("source_swing_review_status"), review.SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY, "source_swing_review_status")
    _expect(frozen_artifact.get("source_swing_review_package_semantic_digest"), EXPECTED_SWING_REVIEW_PACKAGE_DIGEST, "source_swing_review_package_semantic_digest")
    _expect(frozen_artifact.get("source_swing_review_checklist_total"), len(review.REQUIRED_CHECK_IDS), "source_swing_review_checklist_total")
    _expect(frozen_artifact.get("source_swing_review_checklist_passed"), len(review.REQUIRED_CHECK_IDS), "source_swing_review_checklist_passed")
    _expect(frozen_artifact.get("source_swing_review_checklist_failed"), 0, "source_swing_review_checklist_failed")
    _expect(frozen_artifact.get("source_swing_review_blocker_count"), 0, "source_swing_review_blocker_count")
    for field, expected in {
        "source_swing_candidate_digest": EXPECTED_SWING_CANDIDATE_DIGEST,
        "source_dataset_rows_digest": EXPECTED_DATASET_ROWS_DIGEST,
        "source_dataset_manifest_digest": EXPECTED_DATASET_MANIFEST_DIGEST,
        "source_normalized_rows_digest": EXPECTED_SOURCE_ROWS_DIGEST,
        "source_materialization_receipt_digest": EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        "source_acquisition_generation_frozen_digest": EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
        "dataset_profile": swing.DATASET_PROFILE_SWING,
        "dataset_bar_rule": swing.DATASET_BAR_RULE_RTH_HALF_SESSION_195M,
        "swing_bar_count": EXPECTED_SWING_BAR_COUNT,
        "source_rth_rows_consumed": EXPECTED_SOURCE_RTH_ROWS_CONSUMED,
        "source_rth_rows_excluded": EXPECTED_SOURCE_RTH_ROWS_EXCLUDED,
        "full_sessions_used": EXPECTED_FULL_SESSIONS_USED,
        "special_session_policy": EXPECTED_SPECIAL_SESSION_POLICY,
        "special_sessions_excluded": EXPECTED_SPECIAL_SESSIONS_EXCLUDED,
        "special_session_rows_excluded": EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED,
        "cross_check_2025_01_status": EXPECTED_CROSS_CHECK_STATUS,
        "cross_check_2025_01_swing_bars": EXPECTED_CROSS_CHECK_SWING_BARS,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
    }.items():
        _expect(frozen_artifact.get(field), expected, field)
    _expect_true(frozen_artifact.get("in_range_dividends_found"), "in_range_dividends_found")
    _expect_true(frozen_artifact.get("source_adjusted_data_used"), "source_adjusted_data_used")
    _expect(frozen_artifact.get("authority_bindings"), _authority_bindings(), "authority_bindings")
    _validated_operator_attestation(frozen_artifact.get("operator_attestation"))
    _expect(frozen_artifact.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_SWING_CANONICAL_DATASET_FREEZE, "remaining_roadmap")
    checklist = _freeze_checklist(frozen_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_FREEZE_CHECK_IDS, "freeze_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise SwingCanonicalDatasetOperatorFreezeError(f"freeze checklist contains failed check: {failed[0]['check_id']}")
    _expect(frozen_artifact.get("freeze_checklist"), checklist, "freeze_checklist")
    summary = _summary(checklist)
    _expect(frozen_artifact.get("freeze_summary"), summary, "freeze_summary")
    _expect_true(summary.get("swing_canonical_dataset_freeze_authorized_by_operator"), "swing_canonical_dataset_freeze_authorized_by_operator")
    _expect_false(summary.get("software_auto_approval"), "software_auto_approval")
    _expect_false(summary.get("registry_approval_authorized"), "registry_approval_authorized")
    _expect_false(summary.get("runtime_migration_authorized"), "runtime_migration_authorized")
    digest = frozen_artifact.get("swing_canonical_dataset_frozen_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise SwingCanonicalDatasetOperatorFreezeError("swing_canonical_dataset_frozen_semantic_digest missing")
    _expect(digest, swing_canonical_dataset_frozen_semantic_digest_v1(frozen_artifact), "swing_canonical_dataset_frozen_semantic_digest")
    return {
        "status": "SWING_CANONICAL_DATASET_FROZEN_VALID",
        "artifact_kind": frozen_artifact["artifact_kind"],
        "freeze_status": frozen_artifact["freeze_status"],
        "swing_canonical_dataset_frozen_semantic_digest": digest,
        "source_swing_review_package_semantic_digest": EXPECTED_SWING_REVIEW_PACKAGE_DIGEST,
        "source_swing_candidate_digest": EXPECTED_SWING_CANDIDATE_DIGEST,
        "source_dataset_rows_digest": EXPECTED_DATASET_ROWS_DIGEST,
        "source_dataset_manifest_digest": EXPECTED_DATASET_MANIFEST_DIGEST,
        "source_normalized_rows_digest": EXPECTED_SOURCE_ROWS_DIGEST,
        "source_materialization_receipt_digest": EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        "swing_bar_count": EXPECTED_SWING_BAR_COUNT,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "swing_canonical_dataset_frozen": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "provider_requests_made_in_freeze": False,
    }


def build_swing_canonical_dataset_frozen_markdown_v1(frozen_artifact: dict[str, Any]) -> str:
    """Render a sanitized SWING canonical dataset frozen status document."""
    validation = validate_swing_canonical_dataset_frozen_v1(frozen_artifact)
    attestation = frozen_artifact["operator_attestation"]
    bindings = frozen_artifact["authority_bindings"]
    summary = frozen_artifact["freeze_summary"]
    lines = [
        "# MarketFlow SWING Canonical Dataset Operator Freeze Status",
        "",
        "## Frozen SWING Canonical Dataset",
        f"- Artifact kind: `{frozen_artifact['artifact_kind']}`",
        f"- Freeze status: `{frozen_artifact['freeze_status']}`",
        f"- Frozen semantic digest: `{validation['swing_canonical_dataset_frozen_semantic_digest']}`",
        f"- Dataset profile: `{frozen_artifact['dataset_profile']}`",
        f"- Dataset bar rule: `{frozen_artifact['dataset_bar_rule']}`",
        f"- SWING canonical dataset frozen: `{frozen_artifact['swing_canonical_dataset_frozen']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        "",
        "## Source SWING Review Package",
        f"- Review package kind: `{frozen_artifact['source_swing_review_package_kind']}`",
        f"- Review status: `{frozen_artifact['source_swing_review_status']}`",
        f"- Review package digest: `{frozen_artifact['source_swing_review_package_semantic_digest']}`",
        f"- Review checks: `{frozen_artifact['source_swing_review_checklist_passed']}` passed of `{frozen_artifact['source_swing_review_checklist_total']}`",
        f"- Review blockers: `{frozen_artifact['source_swing_review_blocker_count']}`",
        "",
        "## Dataset Evidence",
        f"- SWING candidate digest: `{frozen_artifact['source_swing_candidate_digest']}`",
        f"- Dataset rows digest: `{frozen_artifact['source_dataset_rows_digest']}`",
        f"- Dataset manifest digest: `{frozen_artifact['source_dataset_manifest_digest']}`",
        f"- Source normalized rows digest: `{frozen_artifact['source_normalized_rows_digest']}`",
        f"- Materialization receipt digest: `{frozen_artifact['source_materialization_receipt_digest']}`",
        f"- SWING bar count: `{frozen_artifact['swing_bar_count']}`",
        f"- Source RTH rows consumed: `{frozen_artifact['source_rth_rows_consumed']}`",
        f"- Source RTH rows excluded: `{frozen_artifact['source_rth_rows_excluded']}`",
        "",
        "## 2025-01 Cross-Check",
        f"- Cross-check status: `{frozen_artifact['cross_check_2025_01_status']}`",
        f"- Cross-check SWING bars: `{frozen_artifact['cross_check_2025_01_swing_bars']}`",
        "",
        "## Special-Session Policy",
        f"- Policy: `{frozen_artifact['special_session_policy']}`",
        f"- Full sessions used: `{frozen_artifact['full_sessions_used']}`",
        f"- Special sessions excluded: `{frozen_artifact['special_sessions_excluded']}`",
        f"- Special session rows excluded: `{frozen_artifact['special_session_rows_excluded']}`",
        "",
        "## Frozen Authority Bindings",
        f"- Identity frozen digest: `{bindings['identity_frozen_digest']}`",
        f"- Calendar frozen digest: `{bindings['calendar_frozen_digest']}`",
        f"- Schedule digest: `{bindings['schedule_digest']}`",
        f"- Split-event audit frozen digest: `{bindings['split_event_frozen_digest']}`",
        f"- Dividend-event audit frozen digest: `{bindings['dividend_event_frozen_digest']}`",
        f"- Acquisition generation frozen digest: `{bindings['acquisition_generation_frozen_digest']}`",
        "",
        "## Dividend Adjustment Implication",
        f"- In-range dividends found: `{frozen_artifact['in_range_dividends_found']}`",
        f"- In-range dividend count: `{frozen_artifact['in_range_dividend_count']}`",
        f"- Implication: `{frozen_artifact['in_range_dividend_implication']}`",
        f"- Source adjusted data used: `{frozen_artifact['source_adjusted_data_used']}`",
        "",
        "## Freeze Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        f"- Freeze authorized by operator: `{summary['swing_canonical_dataset_freeze_authorized_by_operator']}`",
        f"- Software auto approval: `{summary['software_auto_approval']}`",
        f"- Registry approval authorized: `{summary['registry_approval_authorized']}`",
        f"- Runtime migration authorized: `{summary['runtime_migration_authorized']}`",
        "",
        "## Authority Boundary",
        f"- identity_segment_frozen: `{frozen_artifact['identity_segment_frozen']}`",
        f"- calendar_operator_frozen: `{frozen_artifact['calendar_operator_frozen']}`",
        f"- split_event_audit_frozen: `{frozen_artifact['split_event_audit_frozen']}`",
        f"- dividend_event_audit_frozen: `{frozen_artifact['dividend_event_audit_frozen']}`",
        f"- acquisition_generation_freeze: `{frozen_artifact['acquisition_generation_freeze']}`",
        f"- swing_canonical_dataset_frozen: `{frozen_artifact['swing_canonical_dataset_frozen']}`",
        f"- canonical_eligibility: `{frozen_artifact['canonical_eligibility']}`",
        f"- registry_eligibility: `{frozen_artifact['registry_eligibility']}`",
        f"- strategy_runtime_migration: `{frozen_artifact['strategy_runtime_migration']}`",
        f"- automatic_stitching: `{frozen_artifact['automatic_stitching']}`",
        f"- predictive_usefulness: `{frozen_artifact['predictive_usefulness']}`",
        f"- profitability: `{frozen_artifact['profitability']}`",
        "",
        "## Remaining Roadmap",
    ]
    lines.extend(f"{index}. {task}" for index, task in enumerate(frozen_artifact["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made in freeze: `False`",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No acquisition bars or SWING bars were regenerated.",
            "- No registry approval or Strategy runtime migration occurred.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
        ]
    )
    return "\n".join(lines)


def write_swing_canonical_dataset_frozen_v1(
    output_dir: str | Path,
    *,
    swing_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the SWING canonical dataset frozen JSON artifact without overwriting output."""
    frozen = build_swing_canonical_dataset_frozen_v1(
        swing_review_package=swing_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_swing_canonical_dataset_frozen_v1(frozen)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025_frozen_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise SwingCanonicalDatasetOperatorFreezeError("SWING canonical dataset frozen filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise SwingCanonicalDatasetOperatorFreezeError("SWING canonical dataset frozen output already exists")
    payload = canonical_json_bytes(frozen)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "frozen_payload_digest": sha256_bytes(payload),
    }
