"""Offline operator freeze ceremony for acquisition generation evidence."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_operator_review_service as review
from marketflow.services import acquisition_generation_service as acquisition


ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN = "ACQUISITION_GENERATION_FROZEN"
SCHEMA_VERSION_ACQUISITION_GENERATION_OPERATOR_FREEZE_V1 = "acquisition_generation_operator_freeze_v1"
ACQUISITION_GENERATION_FROZEN = "ACQUISITION_GENERATION_FROZEN"
OPERATOR_DECISION_APPROVE_ACQUISITION_GENERATION_FREEZE = "APPROVE_ACQUISITION_GENERATION_FREEZE"
OPERATOR_ATTESTATION_VERSION_V1 = "acquisition_generation_operator_attestation_v1"
REQUIRED_ACQUISITION_GENERATION_OPERATOR_ATTESTATION_PHRASE = (
    "FREEZE ACQUISITION GENERATION AAPL BBG000B9XRY4 BBG001S5N8V8 XNAS CS "
    "2022-01-01 2025-12-31 48_CHUNKS_63804_ROWS_READY_AFTER_TRIAGE"
)

EXPECTED_ACQUISITION_REVIEW_PACKAGE_DIGEST = "70dcc5a06ed368399cf367e3c12199d3e3f329d6a2990ab0cb9cb3c3436924a3"
EXPECTED_ACQUISITION_CANDIDATE_DIGEST = acquisition.EXPECTED_FULL_LIVE_ACQUISITION_CANDIDATE_DIGEST
EXPECTED_CHUNK_MANIFEST_DIGEST = review.EXPECTED_REVIEWED_CHUNK_MANIFEST_DIGEST
EXPECTED_PROVIDER_RAW_RESPONSE_DIGEST = review.EXPECTED_REVIEWED_PROVIDER_RAW_RESPONSE_DIGEST
EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST = review.EXPECTED_REVIEWED_NORMALIZED_SOURCE_ROWS_DIGEST
EXPECTED_MONTHLY_RECONCILIATION_DIGEST = acquisition.EXPECTED_FULL_LIVE_MONTHLY_RECONCILIATION_DIGEST
EXPECTED_ACQUISITION_RECEIPT_DIGEST = review.EXPECTED_REVIEWED_ACQUISITION_RECEIPT_DIGEST
EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST = review.EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST
EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST = review.EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OPERATOR_BOUNDARY_CONFIRMATION_FIELDS = [
    "operator_confirms_no_provider_requests_in_freeze",
    "operator_confirms_no_canonical_approval",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_strategy_runtime_migration",
]

REMAINING_ROADMAP_AFTER_ACQUISITION_GENERATION_FREEZE = [
    "SWING canonical dataset candidate.",
    "SWING canonical dataset operator review/freeze.",
    "SWING registry approval.",
    "POSITION_SWING canonical dataset candidate.",
    "POSITION_SWING canonical dataset operator review/freeze.",
    "POSITION_SWING registry approval.",
    "Normal runtime migration.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
]


class AcquisitionGenerationOperatorFreezeError(ValueError):
    """Raised when acquisition generation freeze ceremony data violates guardrails."""


def _status(expected: Any, actual: Any) -> str:
    return PASS if actual == expected else FAIL


def _check(check_id: str, expected: Any, actual: Any, *, message: str | None = None) -> dict[str, Any]:
    status = _status(expected, actual)
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": message
        or ("acquisition generation freeze evidence matches" if status == PASS else "acquisition generation freeze evidence mismatch"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise AcquisitionGenerationOperatorFreezeError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise AcquisitionGenerationOperatorFreezeError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise AcquisitionGenerationOperatorFreezeError(f"{field_name} must be true")


def _source_review_package(acquisition_review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(acquisition_review_package)
        if acquisition_review_package is not None
        else review.build_acquisition_generation_candidate_review_package_v1()
    )
    try:
        validation = review.validate_acquisition_generation_candidate_review_package_v1(source_review)
    except review.AcquisitionGenerationOperatorReviewError as exc:
        raise AcquisitionGenerationOperatorFreezeError(f"source acquisition review package invalid: {exc}") from exc
    _expect(
        validation["review_package_digest"],
        EXPECTED_ACQUISITION_REVIEW_PACKAGE_DIGEST,
        "source acquisition review package semantic digest",
    )
    _expect(validation["blocker_count"], 0, "source acquisition review blocker count")
    _expect(validation["failed_checks"], 0, "source acquisition review failed check count")
    return source_review


def build_acquisition_generation_operator_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_acquisition_review_package_digest: str,
    operator_confirms_acquisition_candidate_digest: str,
    operator_confirms_chunk_manifest_digest: str,
    operator_confirms_provider_raw_response_digest: str,
    operator_confirms_normalized_source_rows_digest: str,
    operator_confirms_monthly_reconciliation_digest: str,
    operator_confirms_acquisition_receipt_digest: str,
    operator_confirms_targeted_diagnostic_receipt_digest: str,
    operator_confirms_per_session_diagnostics_digest: str,
    operator_confirms_identity_frozen_digest: str,
    operator_confirms_calendar_frozen_digest: str,
    operator_confirms_schedule_digest: str,
    operator_confirms_split_event_frozen_digest: str,
    operator_confirms_dividend_event_frozen_digest: str,
    operator_confirms_2025_01_cross_check_passed: bool,
    operator_confirms_all_monthly_mismatches_explained: bool,
    operator_confirms_dividend_implication: bool,
    operator_confirms_no_provider_requests_in_freeze: bool = True,
    operator_confirms_no_canonical_approval: bool = True,
    operator_confirms_no_registry_approval: bool = True,
    operator_confirms_no_strategy_runtime_migration: bool = True,
    operator_decision: str = OPERATOR_DECISION_APPROVE_ACQUISITION_GENERATION_FREEZE,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for acquisition generation freeze."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_acquisition_review_package_digest": operator_confirms_acquisition_review_package_digest,
        "operator_confirms_acquisition_candidate_digest": operator_confirms_acquisition_candidate_digest,
        "operator_confirms_chunk_manifest_digest": operator_confirms_chunk_manifest_digest,
        "operator_confirms_provider_raw_response_digest": operator_confirms_provider_raw_response_digest,
        "operator_confirms_normalized_source_rows_digest": operator_confirms_normalized_source_rows_digest,
        "operator_confirms_monthly_reconciliation_digest": operator_confirms_monthly_reconciliation_digest,
        "operator_confirms_acquisition_receipt_digest": operator_confirms_acquisition_receipt_digest,
        "operator_confirms_targeted_diagnostic_receipt_digest": operator_confirms_targeted_diagnostic_receipt_digest,
        "operator_confirms_per_session_diagnostics_digest": operator_confirms_per_session_diagnostics_digest,
        "operator_confirms_identity_frozen_digest": operator_confirms_identity_frozen_digest,
        "operator_confirms_calendar_frozen_digest": operator_confirms_calendar_frozen_digest,
        "operator_confirms_schedule_digest": operator_confirms_schedule_digest,
        "operator_confirms_split_event_frozen_digest": operator_confirms_split_event_frozen_digest,
        "operator_confirms_dividend_event_frozen_digest": operator_confirms_dividend_event_frozen_digest,
        "operator_confirms_2025_01_cross_check_passed": operator_confirms_2025_01_cross_check_passed,
        "operator_confirms_all_monthly_mismatches_explained": operator_confirms_all_monthly_mismatches_explained,
        "operator_confirms_dividend_implication": operator_confirms_dividend_implication,
        "operator_confirms_no_provider_requests_in_freeze": operator_confirms_no_provider_requests_in_freeze,
        "operator_confirms_no_canonical_approval": operator_confirms_no_canonical_approval,
        "operator_confirms_no_registry_approval": operator_confirms_no_registry_approval,
        "operator_confirms_no_strategy_runtime_migration": operator_confirms_no_strategy_runtime_migration,
    }


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_ACQUISITION_GENERATION_FREEZE, None),
            _check("operator_attestation_phrase_matches", REQUIRED_ACQUISITION_GENERATION_OPERATOR_ATTESTATION_PHRASE, None),
            _check("operator_review_digest_confirmation_matches", EXPECTED_ACQUISITION_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_candidate_digest_confirmation_matches", EXPECTED_ACQUISITION_CANDIDATE_DIGEST, None),
            _check("operator_chunk_manifest_digest_confirmation_matches", EXPECTED_CHUNK_MANIFEST_DIGEST, None),
            _check("operator_raw_digest_confirmation_matches", EXPECTED_PROVIDER_RAW_RESPONSE_DIGEST, None),
            _check("operator_normalized_digest_confirmation_matches", EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST, None),
            _check("operator_monthly_digest_confirmation_matches", EXPECTED_MONTHLY_RECONCILIATION_DIGEST, None),
            _check("operator_receipt_digest_confirmation_matches", EXPECTED_ACQUISITION_RECEIPT_DIGEST, None),
            _check("operator_targeted_receipt_digest_confirmation_matches", EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST, None),
            _check("operator_per_session_digest_confirmation_matches", EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST, None),
            _check("operator_confirms_2025_01_cross_check", True, None),
            _check("operator_confirms_all_mismatches_explained", True, None),
            _check("operator_confirms_dividend_implication", True, None),
            _check("operator_identity_digest_confirmation_matches", acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, None),
            _check("operator_calendar_digest_confirmation_matches", acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, None),
            _check("operator_schedule_digest_confirmation_matches", acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, None),
            _check("operator_split_digest_confirmation_matches", acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, None),
            _check("operator_dividend_digest_confirmation_matches", acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST, None),
            *[_check(field, True, None) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_ACQUISITION_GENERATION_FREEZE, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_ACQUISITION_GENERATION_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check("operator_review_digest_confirmation_matches", EXPECTED_ACQUISITION_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_acquisition_review_package_digest")),
        _check("operator_candidate_digest_confirmation_matches", EXPECTED_ACQUISITION_CANDIDATE_DIGEST, attestation.get("operator_confirms_acquisition_candidate_digest")),
        _check("operator_chunk_manifest_digest_confirmation_matches", EXPECTED_CHUNK_MANIFEST_DIGEST, attestation.get("operator_confirms_chunk_manifest_digest")),
        _check("operator_raw_digest_confirmation_matches", EXPECTED_PROVIDER_RAW_RESPONSE_DIGEST, attestation.get("operator_confirms_provider_raw_response_digest")),
        _check("operator_normalized_digest_confirmation_matches", EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST, attestation.get("operator_confirms_normalized_source_rows_digest")),
        _check("operator_monthly_digest_confirmation_matches", EXPECTED_MONTHLY_RECONCILIATION_DIGEST, attestation.get("operator_confirms_monthly_reconciliation_digest")),
        _check("operator_receipt_digest_confirmation_matches", EXPECTED_ACQUISITION_RECEIPT_DIGEST, attestation.get("operator_confirms_acquisition_receipt_digest")),
        _check("operator_targeted_receipt_digest_confirmation_matches", EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST, attestation.get("operator_confirms_targeted_diagnostic_receipt_digest")),
        _check("operator_per_session_digest_confirmation_matches", EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST, attestation.get("operator_confirms_per_session_diagnostics_digest")),
        _check("operator_confirms_2025_01_cross_check", True, attestation.get("operator_confirms_2025_01_cross_check_passed")),
        _check("operator_confirms_all_mismatches_explained", True, attestation.get("operator_confirms_all_monthly_mismatches_explained")),
        _check("operator_confirms_dividend_implication", True, attestation.get("operator_confirms_dividend_implication")),
        _check("operator_identity_digest_confirmation_matches", acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, attestation.get("operator_confirms_identity_frozen_digest")),
        _check("operator_calendar_digest_confirmation_matches", acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, attestation.get("operator_confirms_calendar_frozen_digest")),
        _check("operator_schedule_digest_confirmation_matches", acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, attestation.get("operator_confirms_schedule_digest")),
        _check("operator_split_digest_confirmation_matches", acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, attestation.get("operator_confirms_split_event_frozen_digest")),
        _check("operator_dividend_digest_confirmation_matches", acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST, attestation.get("operator_confirms_dividend_event_frozen_digest")),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise AcquisitionGenerationOperatorFreezeError("operator_attestation must be a JSON object")
    for field in ("operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise AcquisitionGenerationOperatorFreezeError(f"{field} is required")
    failures = [check for check in _attestation_checks(attestation) if check["status"] != PASS]
    if failures:
        raise AcquisitionGenerationOperatorFreezeError(f"{failures[0]['check_id']} failed")
    return deepcopy(attestation)


def _review_evidence(source_review: dict[str, Any]) -> dict[str, Any]:
    evidence = source_review["reviewed_acquisition_evidence"]
    targeted = source_review["targeted_diagnostic_evidence"]
    return {
        "source_acquisition_review_package_kind": source_review["artifact_kind"],
        "source_acquisition_review_status": source_review["review_status"],
        "source_acquisition_review_package_semantic_digest": source_review["acquisition_generation_review_package_semantic_digest"],
        "source_acquisition_review_checklist_total": source_review["review_summary"]["total_checks"],
        "source_acquisition_review_checklist_passed": source_review["review_summary"]["passed_checks"],
        "source_acquisition_review_checklist_failed": source_review["review_summary"]["failed_checks"],
        "source_acquisition_review_blocker_count": source_review["review_summary"]["blocker_count"],
        "source_acquisition_candidate_digest": evidence["reviewed_acquisition_candidate_digest"],
        "source_chunk_manifest_digest": evidence["reviewed_chunk_manifest_digest"],
        "source_provider_raw_response_digest": evidence["reviewed_provider_raw_response_digest"],
        "source_normalized_source_rows_digest": evidence["reviewed_normalized_source_rows_digest"],
        "source_monthly_reconciliation_digest": evidence["reviewed_monthly_reconciliation_digest"],
        "source_acquisition_receipt_digest": evidence["reviewed_acquisition_receipt_digest"],
        "expected_chunk_count": evidence["expected_chunk_count"],
        "completed_chunk_count": evidence["completed_chunk_count"],
        "failed_chunk_count": evidence["failed_chunk_count"],
        "total_raw_rows": evidence["total_raw_rows"],
        "total_normalized_source_rows": evidence["total_normalized_source_rows"],
        "total_rth_rows": evidence["total_rth_rows"],
        "total_extended_hours_rows": evidence["total_extended_hours_rows"],
        "out_of_calendar_or_unknown_rows": evidence["out_of_calendar_or_unknown_rows"],
        "monthly_reconciled_count": evidence["monthly_reconciled_count"],
        "monthly_not_reconciled_count": evidence["monthly_not_reconciled_count"],
        "accepted_2025_01_cross_check": deepcopy(evidence["accepted_2025_01_cross_check"]),
        "targeted_diagnostic_status": targeted["targeted_diagnostic_status"],
        "targeted_month_count": targeted["targeted_month_count"],
        "targeted_completed_chunks": targeted["targeted_completed_chunks"],
        "targeted_failed_chunks": targeted["targeted_failed_chunks"],
        "all_monthly_mismatches_explained": targeted["all_monthly_mismatches_explained"],
        "mismatch_explanation": targeted["mismatch_explanation"],
        "per_session_issue_summary": deepcopy(targeted["per_session_issue_summary"]),
        "per_session_severity_summary": deepcopy(targeted["per_session_severity_summary"]),
        "targeted_chunk_manifest_digest": targeted["targeted_chunk_manifest_digest"],
        "targeted_provider_raw_response_digest": targeted["targeted_provider_raw_response_digest"],
        "targeted_normalized_rows_digest": targeted["targeted_normalized_rows_digest"],
        "targeted_monthly_reconciliation_digest": targeted["targeted_monthly_reconciliation_digest"],
        "per_session_diagnostics_digest": targeted["per_session_diagnostics_digest"],
        "targeted_diagnostic_receipt_digest": targeted["targeted_diagnostic_receipt_digest"],
    }


def _authority_bindings() -> dict[str, Any]:
    segment = acquisition.FIXED_IDENTITY_SEGMENT
    return {
        "identity_segment_frozen_digest": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_audit_frozen_digest": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_contract_digest": acquisition.EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        "fixed_segment": {
            "ticker": segment["ticker"],
            "composite_figi": segment["composite_figi"],
            "share_class_figi": segment["share_class_figi"],
            "primary_mic": segment["primary_mic"],
            "security_type": segment["security_type"],
            "segment_start": segment["segment_start"],
            "segment_end": segment["segment_end"],
        },
    }


def _freeze_checklist(frozen: dict[str, Any]) -> list[dict[str, Any]]:
    bindings = frozen["authority_bindings"]
    segment = bindings["fixed_segment"]
    return [
        _check("acquisition_review_package_digest_matches_expected", EXPECTED_ACQUISITION_REVIEW_PACKAGE_DIGEST, frozen["source_acquisition_review_package_semantic_digest"]),
        _check("acquisition_review_package_has_zero_blockers", 0, frozen["source_acquisition_review_blocker_count"]),
        _check("acquisition_candidate_digest_matches_expected", EXPECTED_ACQUISITION_CANDIDATE_DIGEST, frozen["source_acquisition_candidate_digest"]),
        _check("chunk_manifest_digest_matches_expected", EXPECTED_CHUNK_MANIFEST_DIGEST, frozen["source_chunk_manifest_digest"]),
        _check("provider_raw_response_digest_matches_expected", EXPECTED_PROVIDER_RAW_RESPONSE_DIGEST, frozen["source_provider_raw_response_digest"]),
        _check("normalized_source_rows_digest_matches_expected", EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST, frozen["source_normalized_source_rows_digest"]),
        _check("monthly_reconciliation_digest_matches_expected", EXPECTED_MONTHLY_RECONCILIATION_DIGEST, frozen["source_monthly_reconciliation_digest"]),
        _check("acquisition_receipt_digest_matches_expected", EXPECTED_ACQUISITION_RECEIPT_DIGEST, frozen["source_acquisition_receipt_digest"]),
        _check("expected_chunk_count_48", 48, frozen["expected_chunk_count"]),
        _check("completed_chunk_count_48", 48, frozen["completed_chunk_count"]),
        _check("failed_chunk_count_zero", 0, frozen["failed_chunk_count"]),
        _check("total_raw_rows_match", 63804, frozen["total_raw_rows"]),
        _check("total_normalized_rows_match", 63804, frozen["total_normalized_source_rows"]),
        _check("total_rth_rows_match", 25970, frozen["total_rth_rows"]),
        _check("total_extended_hours_rows_match", 37834, frozen["total_extended_hours_rows"]),
        _check("out_of_calendar_unknown_rows_zero", 0, frozen["out_of_calendar_or_unknown_rows"]),
        _check("cross_check_2025_01_passed", "PASSED", frozen["accepted_2025_01_cross_check"].get("cross_check_status")),
        _check("targeted_diagnostics_ready_after_triage", acquisition.ACQUISITION_OPERATOR_REVIEW_READY_AFTER_TRIAGE, frozen["targeted_diagnostic_status"]),
        _check("all_monthly_mismatches_explained", True, frozen["all_monthly_mismatches_explained"]),
        _check("per_session_issue_summary_reconciled", {"RECONCILED": 188}, frozen["per_session_issue_summary"]),
        _check("per_session_severity_summary_info", {"INFO": 188}, frozen["per_session_severity_summary"]),
        _check("targeted_diagnostic_receipt_digest_matches", EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST, frozen["targeted_diagnostic_receipt_digest"]),
        _check("per_session_diagnostics_digest_matches", EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST, frozen["per_session_diagnostics_digest"]),
        _check("dividend_implication_preserved", acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, bindings["in_range_dividend_implication"]),
        *_attestation_checks(frozen.get("operator_attestation")),
        _check("identity_segment_frozen_true", True, frozen["identity_segment_frozen"]),
        _check("calendar_operator_frozen_true", True, frozen["calendar_operator_frozen"]),
        _check("split_event_audit_frozen_true", True, frozen["split_event_audit_frozen"]),
        _check("dividend_event_audit_frozen_true", True, frozen["dividend_event_audit_frozen"]),
        _check("acquisition_generation_freeze_true", True, frozen["acquisition_generation_freeze"]),
        _check("canonical_eligibility_false", False, frozen["canonical_eligibility"]),
        _check("registry_eligibility_false", False, frozen["registry_eligibility"]),
        _check("strategy_runtime_migration_false", False, frozen["strategy_runtime_migration"]),
        _check("automatic_stitching_false", False, frozen["automatic_stitching"]),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, frozen["predictive_usefulness"]),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, frozen["profitability"]),
        _check("provider_requests_made_in_freeze_false", False, frozen["provider_requests_made_in_freeze"]),
        _check("segment_fields_match", {
            "ticker": "AAPL",
            "composite_figi": "BBG000B9XRY4",
            "share_class_figi": "BBG001S5N8V8",
            "primary_mic": "XNAS",
            "security_type": "CS",
            "segment_start": "2022-01-01",
            "segment_end": "2025-12-31",
        }, segment),
        _check("contract_digest_matches", acquisition.EXPECTED_ACQUISITION_CONTRACT_DIGEST, bindings["acquisition_contract_digest"]),
        _check("authority_digests_match", {
            "identity": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
            "calendar": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
            "schedule": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
            "split": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
            "dividend": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        }, {
            "identity": bindings["identity_segment_frozen_digest"],
            "calendar": bindings["exchange_calendar_frozen_digest"],
            "schedule": bindings["schedule_semantic_digest"],
            "split": bindings["split_event_audit_frozen_digest"],
            "dividend": bindings["dividend_event_audit_frozen_digest"],
        }),
    ]


def _digest_payload(frozen: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(frozen)
    payload.pop("acquisition_generation_frozen_semantic_digest", None)
    return payload


def acquisition_generation_frozen_semantic_digest_v1(frozen_artifact: dict[str, Any]) -> str:
    return semantic_digest(_digest_payload(frozen_artifact))


def build_acquisition_generation_frozen_v1(
    *,
    acquisition_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build an offline acquisition generation frozen artifact."""
    source_review = _source_review_package(acquisition_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    frozen = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_OPERATOR_FREEZE_V1,
        "freeze_status": ACQUISITION_GENERATION_FROZEN,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "acquisition_generation_freeze": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "created_offline": True,
        "provider_requests_made_in_freeze": False,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "operator_attestation": attestation,
        "authority_bindings": _authority_bindings(),
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_ACQUISITION_GENERATION_FREEZE),
        **_review_evidence(source_review),
    }
    checklist = _freeze_checklist(frozen)
    failed = [check for check in checklist if check["status"] != PASS]
    frozen["freeze_checklist"] = checklist
    frozen["freeze_summary"] = {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(1 for check in failed if check["severity"] == BLOCKER),
        "acquisition_generation_freeze_authorized_by_operator": not failed,
        "software_auto_approval": False,
    }
    frozen["acquisition_generation_frozen_semantic_digest"] = acquisition_generation_frozen_semantic_digest_v1(frozen)
    validate_acquisition_generation_frozen_v1(frozen)
    return frozen


def validate_acquisition_generation_frozen_v1(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate the acquisition generation frozen artifact and downstream guardrails."""
    if not isinstance(frozen_artifact, dict):
        raise AcquisitionGenerationOperatorFreezeError("frozen artifact must be a JSON object")
    _expect(frozen_artifact.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN, "artifact_kind")
    _expect(frozen_artifact.get("schema_version"), SCHEMA_VERSION_ACQUISITION_GENERATION_OPERATOR_FREEZE_V1, "schema_version")
    _expect(frozen_artifact.get("freeze_status"), ACQUISITION_GENERATION_FROZEN, "freeze_status")
    for field in ("identity_segment_frozen", "calendar_operator_frozen", "split_event_audit_frozen", "dividend_event_audit_frozen", "acquisition_generation_freeze", "created_offline"):
        _expect_true(frozen_artifact.get(field), field)
    for field in ("canonical_eligibility", "registry_eligibility", "strategy_runtime_migration", "automatic_stitching", "provider_requests_made_in_freeze"):
        _expect_false(frozen_artifact.get(field), field)
    _expect(frozen_artifact.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(frozen_artifact.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(frozen_artifact.get("source_acquisition_review_package_kind"), review.ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE, "source_acquisition_review_package_kind")
    _expect(frozen_artifact.get("source_acquisition_review_status"), review.ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY, "source_acquisition_review_status")
    _expect(frozen_artifact.get("source_acquisition_review_package_semantic_digest"), EXPECTED_ACQUISITION_REVIEW_PACKAGE_DIGEST, "source_acquisition_review_package_semantic_digest")
    _expect(frozen_artifact.get("source_acquisition_review_checklist_total"), 52, "source_acquisition_review_checklist_total")
    _expect(frozen_artifact.get("source_acquisition_review_checklist_passed"), 52, "source_acquisition_review_checklist_passed")
    _expect(frozen_artifact.get("source_acquisition_review_checklist_failed"), 0, "source_acquisition_review_checklist_failed")
    _expect(frozen_artifact.get("source_acquisition_review_blocker_count"), 0, "source_acquisition_review_blocker_count")
    for field, expected in {
        "source_acquisition_candidate_digest": EXPECTED_ACQUISITION_CANDIDATE_DIGEST,
        "source_chunk_manifest_digest": EXPECTED_CHUNK_MANIFEST_DIGEST,
        "source_provider_raw_response_digest": EXPECTED_PROVIDER_RAW_RESPONSE_DIGEST,
        "source_normalized_source_rows_digest": EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST,
        "source_monthly_reconciliation_digest": EXPECTED_MONTHLY_RECONCILIATION_DIGEST,
        "source_acquisition_receipt_digest": EXPECTED_ACQUISITION_RECEIPT_DIGEST,
        "targeted_diagnostic_receipt_digest": EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST,
        "per_session_diagnostics_digest": EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST,
    }.items():
        _expect(frozen_artifact.get(field), expected, field)
    for field, expected in {
        "expected_chunk_count": 48,
        "completed_chunk_count": 48,
        "failed_chunk_count": 0,
        "total_raw_rows": 63804,
        "total_normalized_source_rows": 63804,
        "total_rth_rows": 25970,
        "total_extended_hours_rows": 37834,
        "out_of_calendar_or_unknown_rows": 0,
    }.items():
        _expect(frozen_artifact.get(field), expected, field)
    _expect(frozen_artifact.get("accepted_2025_01_cross_check", {}).get("cross_check_status"), "PASSED", "accepted_2025_01_cross_check")
    _expect_true(frozen_artifact.get("all_monthly_mismatches_explained"), "all_monthly_mismatches_explained")
    _expect(frozen_artifact.get("mismatch_explanation"), review.MISMATCH_EXPLANATION_SPECIAL_SESSION_EXPECTATION, "mismatch_explanation")
    _expect(frozen_artifact.get("per_session_issue_summary"), {"RECONCILED": 188}, "per_session_issue_summary")
    _expect(frozen_artifact.get("per_session_severity_summary"), {"INFO": 188}, "per_session_severity_summary")
    _expect(frozen_artifact.get("authority_bindings"), _authority_bindings(), "authority_bindings")
    _expect(frozen_artifact.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_ACQUISITION_GENERATION_FREEZE, "remaining_roadmap")
    if not isinstance(frozen_artifact.get("operator_attestation"), dict):
        raise AcquisitionGenerationOperatorFreezeError("operator_attestation missing")
    _validated_operator_attestation(frozen_artifact["operator_attestation"])
    checklist = frozen_artifact.get("freeze_checklist")
    if not isinstance(checklist, list):
        raise AcquisitionGenerationOperatorFreezeError("freeze_checklist must be a list")
    _expect(checklist, _freeze_checklist(frozen_artifact), "freeze_checklist")
    failed = [check for check in checklist if check["status"] != PASS]
    _expect(
        frozen_artifact.get("freeze_summary"),
        {
            "total_checks": len(checklist),
            "passed_checks": len(checklist) - len(failed),
            "failed_checks": len(failed),
            "blocker_count": sum(1 for check in failed if check["severity"] == BLOCKER),
            "acquisition_generation_freeze_authorized_by_operator": not failed,
            "software_auto_approval": False,
        },
        "freeze_summary",
    )
    digest = frozen_artifact.get("acquisition_generation_frozen_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AcquisitionGenerationOperatorFreezeError("acquisition_generation_frozen_semantic_digest missing")
    _expect(digest, acquisition_generation_frozen_semantic_digest_v1(frozen_artifact), "acquisition_generation_frozen_semantic_digest")
    return {
        "status": "ACQUISITION_GENERATION_FROZEN_VALID",
        "artifact_kind": frozen_artifact["artifact_kind"],
        "freeze_status": frozen_artifact["freeze_status"],
        "acquisition_generation_frozen_semantic_digest": digest,
        "total_checks": frozen_artifact["freeze_summary"]["total_checks"],
        "failed_checks": frozen_artifact["freeze_summary"]["failed_checks"],
        "blocker_count": frozen_artifact["freeze_summary"]["blocker_count"],
        "acquisition_generation_freeze": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
    }


def build_acquisition_generation_frozen_markdown_v1(frozen_artifact: dict[str, Any]) -> str:
    """Render a sanitized acquisition generation frozen status document."""
    validate_acquisition_generation_frozen_v1(frozen_artifact)
    bindings = frozen_artifact["authority_bindings"]
    summary = frozen_artifact["freeze_summary"]
    lines = [
        "# MarketFlow Acquisition Generation Operator Freeze Status",
        "",
        "## Frozen Acquisition Generation",
        f"- Artifact kind: `{frozen_artifact['artifact_kind']}`",
        f"- Freeze status: `{frozen_artifact['freeze_status']}`",
        f"- Acquisition generation freeze: `{frozen_artifact['acquisition_generation_freeze']}`",
        f"- Frozen semantic digest: `{frozen_artifact['acquisition_generation_frozen_semantic_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{frozen_artifact['operator_attestation']['operator_reference']}`",
        f"- Operator decision: `{frozen_artifact['operator_attestation']['operator_decision']}`",
        f"- Attestation version: `{frozen_artifact['operator_attestation']['operator_attestation_version']}`",
        f"- Attestation timestamp UTC: `{frozen_artifact['operator_attestation']['operator_attestation_timestamp_utc']}`",
        "",
        "## Source Acquisition Review Package",
        f"- Review package digest: `{frozen_artifact['source_acquisition_review_package_semantic_digest']}`",
        f"- Review status: `{frozen_artifact['source_acquisition_review_status']}`",
        f"- Review blockers: `{frozen_artifact['source_acquisition_review_blocker_count']}`",
        "",
        "## Full Generation Evidence",
        f"- Acquisition candidate digest: `{frozen_artifact['source_acquisition_candidate_digest']}`",
        f"- Chunk manifest digest: `{frozen_artifact['source_chunk_manifest_digest']}`",
        f"- Provider raw response digest: `{frozen_artifact['source_provider_raw_response_digest']}`",
        f"- Normalized rows digest: `{frozen_artifact['source_normalized_source_rows_digest']}`",
        f"- Monthly reconciliation digest: `{frozen_artifact['source_monthly_reconciliation_digest']}`",
        f"- Acquisition receipt digest: `{frozen_artifact['source_acquisition_receipt_digest']}`",
        f"- Chunks: `{frozen_artifact['expected_chunk_count']} / {frozen_artifact['completed_chunk_count']} / {frozen_artifact['failed_chunk_count']}`",
        f"- Rows: `{frozen_artifact['total_raw_rows']} raw / {frozen_artifact['total_normalized_source_rows']} normalized / {frozen_artifact['total_rth_rows']} RTH / {frozen_artifact['total_extended_hours_rows']} extended-hours / {frozen_artifact['out_of_calendar_or_unknown_rows']} out-or-unknown`",
        "",
        "## 2025-01 Cross-Check",
        f"- Cross-check status: `{frozen_artifact['accepted_2025_01_cross_check']['cross_check_status']}`",
        "",
        "## Targeted Per-Session Triage",
        f"- Targeted diagnostic status: `{frozen_artifact['targeted_diagnostic_status']}`",
        f"- All monthly mismatches explained: `{frozen_artifact['all_monthly_mismatches_explained']}`",
        f"- Per-session diagnostics digest: `{frozen_artifact['per_session_diagnostics_digest']}`",
        f"- Targeted diagnostic receipt digest: `{frozen_artifact['targeted_diagnostic_receipt_digest']}`",
        "",
        "## Frozen Authority Bindings",
        f"- Identity frozen digest: `{bindings['identity_segment_frozen_digest']}`",
        f"- Calendar frozen digest: `{bindings['exchange_calendar_frozen_digest']}`",
        f"- Schedule digest: `{bindings['schedule_semantic_digest']}`",
        f"- Split-event audit frozen digest: `{bindings['split_event_audit_frozen_digest']}`",
        f"- Dividend-event audit frozen digest: `{bindings['dividend_event_audit_frozen_digest']}`",
        f"- Acquisition contract digest: `{bindings['acquisition_contract_digest']}`",
        "",
        "## Dividend Adjustment Implication",
        f"- In-range dividends found: `{bindings['in_range_dividends_found']}`",
        f"- In-range dividend count: `{bindings['in_range_dividend_count']}`",
        f"- Implication: `{bindings['in_range_dividend_implication']}`",
        "",
        "## Freeze Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        f"- Software auto approval: `{summary['software_auto_approval']}`",
        "",
        "## Authority Boundary",
        f"- identity_segment_frozen: `{frozen_artifact['identity_segment_frozen']}`",
        f"- calendar_operator_frozen: `{frozen_artifact['calendar_operator_frozen']}`",
        f"- split_event_audit_frozen: `{frozen_artifact['split_event_audit_frozen']}`",
        f"- dividend_event_audit_frozen: `{frozen_artifact['dividend_event_audit_frozen']}`",
        f"- acquisition_generation_freeze: `{frozen_artifact['acquisition_generation_freeze']}`",
        f"- canonical_eligibility: `{frozen_artifact['canonical_eligibility']}`",
        f"- registry_eligibility: `{frozen_artifact['registry_eligibility']}`",
        f"- strategy_runtime_migration: `{frozen_artifact['strategy_runtime_migration']}`",
        f"- automatic_stitching: `{frozen_artifact['automatic_stitching']}`",
        f"- predictive_usefulness: `{frozen_artifact['predictive_usefulness']}`",
        f"- profitability: `{frozen_artifact['profitability']}`",
        "",
        "## Remaining Roadmap",
    ]
    lines.extend(f"{index}. {item}" for index, item in enumerate(frozen_artifact["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made in freeze: `False`",
            "- No canonical, registry, runtime, predictive, or profitability approval occurred.",
            "- No provider data was fetched and no acquisition bars were regenerated.",
            "",
        ]
    )
    return "\n".join(lines)


def write_acquisition_generation_frozen_v1(
    output_dir: str | Path,
    *,
    acquisition_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Write the acquisition generation frozen JSON and Markdown artifacts."""
    frozen = build_acquisition_generation_frozen_v1(
        acquisition_review_package=acquisition_review_package,
        operator_attestation=operator_attestation,
    )
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / "acquisition_generation_frozen_v1.json"
    markdown_path = output_path / "MARKETFLOW_ACQUISITION_GENERATION_OPERATOR_FREEZE_STATUS.md"
    json_text = json.dumps(frozen, sort_keys=True, indent=2)
    markdown_text = build_acquisition_generation_frozen_markdown_v1(frozen)
    json_path.write_text(json_text + "\n", encoding="utf-8")
    markdown_path.write_text(markdown_text, encoding="utf-8")
    return {
        "frozen_artifact": frozen,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "json_sha256": sha256_bytes((json_text + "\n").encode("utf-8")),
        "markdown_sha256": sha256_bytes(markdown_text.encode("utf-8")),
        "acquisition_generation_frozen_semantic_digest": frozen["acquisition_generation_frozen_semantic_digest"],
    }
