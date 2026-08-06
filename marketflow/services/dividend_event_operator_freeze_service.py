"""Offline operator freeze ceremony for dividend-event audit evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import dividend_event_audit_service as dividend
from marketflow.services import dividend_event_operator_review_service as review


ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_FROZEN = "DIVIDEND_EVENT_AUDIT_FROZEN"
SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_OPERATOR_FREEZE_V1 = "dividend_event_audit_operator_freeze_v1"
DIVIDEND_EVENT_AUDIT_FROZEN = "DIVIDEND_EVENT_AUDIT_FROZEN"
OPERATOR_DECISION_APPROVE_DIVIDEND_EVENT_AUDIT_FREEZE = "APPROVE_DIVIDEND_EVENT_AUDIT_FREEZE"
OPERATOR_ATTESTATION_VERSION_V1 = "dividend_event_operator_attestation_v1"
REQUIRED_DIVIDEND_EVENT_OPERATOR_ATTESTATION_PHRASE = (
    "FREEZE DIVIDEND EVENT AUDIT AAPL BBG000B9XRY4 BBG001S5N8V8 XNAS CS "
    "2022-01-01 2025-12-31 16_REPORTED_IN_RANGE_DIVIDENDS"
)

EXPECTED_DIVIDEND_REVIEW_PACKAGE_SEMANTIC_DIGEST = "5cfa4b8f86658b84df932afbf8278d431f18a1082014b3df3ad8c15af2d55742"
EXPECTED_LIVE_DIVIDEND_CANDIDATE_DIGEST = review.EXPECTED_LIVE_CANDIDATE_SEMANTIC_DIGEST
EXPECTED_LIVE_RAW_RESPONSE_DIGEST = review.EXPECTED_LIVE_RAW_RESPONSE_DIGEST
EXPECTED_LIVE_TIMELINE_DIGEST = review.EXPECTED_LIVE_TIMELINE_DIGEST
EXPECTED_LIVE_RECEIPT_DIGEST = review.EXPECTED_LIVE_RECEIPT_DIGEST
EXPECTED_AUDIT_STATUS = review.EXPECTED_AUDIT_STATUS
EXPECTED_IN_RANGE_DIVIDEND_COUNT = 16
EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION = review.IN_RANGE_DIVIDEND_IMPLICATION

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OPERATOR_BOUNDARY_CONFIRMATION_FIELDS = [
    "operator_confirms_no_provider_requests_in_freeze",
    "operator_confirms_no_canonical_approval",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_acquisition_generation_freeze",
    "operator_confirms_no_strategy_runtime_migration",
]

REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_FREEZE = [
    "Full 2022-2025 acquisition generation.",
    "Acquisition-generation freeze.",
    "SWING canonical dataset and registry approval.",
    "POSITION_SWING canonical dataset and registry approval.",
    "Normal runtime migration.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
]

REQUIRED_FREEZE_CHECK_IDS = [
    "dividend_review_package_digest_matches_expected",
    "dividend_review_package_has_zero_blockers",
    "live_dividend_candidate_digest_matches_expected",
    "raw_response_digest_matches_expected",
    "timeline_digest_matches_expected",
    "receipt_digest_matches_expected",
    "provider_request_mode_live",
    "provider_response_status_ok",
    "provider_raw_row_count_sixteen",
    "event_count_total_sixteen",
    "event_count_pre_range_zero",
    "event_count_in_range_sixteen",
    "event_count_post_range_zero",
    "event_count_unknown_zero",
    "audit_status_found_in_range_dividend",
    "in_range_dividend_implication_preserved",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_dividend_review_digest_confirmation_matches",
    "operator_live_candidate_digest_confirmation_matches",
    "operator_raw_digest_confirmation_matches",
    "operator_timeline_digest_confirmation_matches",
    "operator_receipt_digest_confirmation_matches",
    "operator_confirms_in_range_dividend_count",
    "operator_confirms_in_range_dividend_implication",
    "operator_identity_digest_confirmation_matches",
    "operator_calendar_digest_confirmation_matches",
    "operator_schedule_digest_confirmation_matches",
    "operator_split_event_digest_confirmation_matches",
    "operator_confirms_no_provider_requests_in_freeze",
    "operator_confirms_no_canonical_approval",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_acquisition_generation_freeze",
    "operator_confirms_no_strategy_runtime_migration",
    "identity_segment_frozen_true",
    "calendar_operator_frozen_true",
    "split_event_audit_frozen_true",
    "dividend_event_audit_frozen_true",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "acquisition_generation_freeze_false",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "segment_fields_match",
    "contract_digest_matches",
    "authority_digests_match",
]


class DividendEventOperatorFreezeError(ValueError):
    """Raised when a dividend-event operator freeze ceremony violates guardrails."""


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
        "message": message or ("dividend-event freeze evidence matches" if status == PASS else "dividend-event freeze evidence mismatch"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise DividendEventOperatorFreezeError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise DividendEventOperatorFreezeError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise DividendEventOperatorFreezeError(f"{field_name} must be true")


def _source_dividend_review_package(dividend_review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(dividend_review_package)
        if dividend_review_package is not None
        else review.build_dividend_event_audit_candidate_review_package_v1()
    )
    try:
        validation = review.validate_dividend_event_audit_candidate_review_package_v1(source_review)
    except review.DividendEventOperatorReviewError as exc:
        raise DividendEventOperatorFreezeError(f"source dividend review package invalid: {exc}") from exc
    _expect(
        validation["dividend_event_review_package_semantic_digest"],
        EXPECTED_DIVIDEND_REVIEW_PACKAGE_SEMANTIC_DIGEST,
        "source dividend review package semantic digest",
    )
    _expect(validation["blocker_count"], 0, "source dividend review blocker count")
    _expect(validation["failed_checks"], 0, "source dividend review failed check count")
    return source_review


def build_dividend_event_operator_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_dividend_review_package_digest: str,
    operator_confirms_live_dividend_candidate_digest: str,
    operator_confirms_raw_response_digest: str,
    operator_confirms_timeline_digest: str,
    operator_confirms_receipt_digest: str,
    operator_confirms_identity_frozen_digest: str,
    operator_confirms_calendar_frozen_digest: str,
    operator_confirms_schedule_digest: str,
    operator_confirms_split_event_frozen_digest: str,
    operator_confirms_in_range_dividend_count: int,
    operator_confirms_in_range_dividend_implication: bool,
    operator_confirms_no_provider_requests_in_freeze: bool,
    operator_confirms_no_canonical_approval: bool,
    operator_confirms_no_registry_approval: bool,
    operator_confirms_no_acquisition_generation_freeze: bool,
    operator_confirms_no_strategy_runtime_migration: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_DIVIDEND_EVENT_AUDIT_FREEZE,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for dividend-event audit freeze."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_dividend_review_package_digest": operator_confirms_dividend_review_package_digest,
        "operator_confirms_live_dividend_candidate_digest": operator_confirms_live_dividend_candidate_digest,
        "operator_confirms_raw_response_digest": operator_confirms_raw_response_digest,
        "operator_confirms_timeline_digest": operator_confirms_timeline_digest,
        "operator_confirms_receipt_digest": operator_confirms_receipt_digest,
        "operator_confirms_identity_frozen_digest": operator_confirms_identity_frozen_digest,
        "operator_confirms_calendar_frozen_digest": operator_confirms_calendar_frozen_digest,
        "operator_confirms_schedule_digest": operator_confirms_schedule_digest,
        "operator_confirms_split_event_frozen_digest": operator_confirms_split_event_frozen_digest,
        "operator_confirms_in_range_dividend_count": operator_confirms_in_range_dividend_count,
        "operator_confirms_in_range_dividend_implication": operator_confirms_in_range_dividend_implication,
        "operator_confirms_no_provider_requests_in_freeze": operator_confirms_no_provider_requests_in_freeze,
        "operator_confirms_no_canonical_approval": operator_confirms_no_canonical_approval,
        "operator_confirms_no_registry_approval": operator_confirms_no_registry_approval,
        "operator_confirms_no_acquisition_generation_freeze": operator_confirms_no_acquisition_generation_freeze,
        "operator_confirms_no_strategy_runtime_migration": operator_confirms_no_strategy_runtime_migration,
    }


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_DIVIDEND_EVENT_AUDIT_FREEZE, None),
            _check("operator_attestation_phrase_matches", REQUIRED_DIVIDEND_EVENT_OPERATOR_ATTESTATION_PHRASE, None),
            _check("operator_dividend_review_digest_confirmation_matches", EXPECTED_DIVIDEND_REVIEW_PACKAGE_SEMANTIC_DIGEST, None),
            _check("operator_live_candidate_digest_confirmation_matches", EXPECTED_LIVE_DIVIDEND_CANDIDATE_DIGEST, None),
            _check("operator_raw_digest_confirmation_matches", EXPECTED_LIVE_RAW_RESPONSE_DIGEST, None),
            _check("operator_timeline_digest_confirmation_matches", EXPECTED_LIVE_TIMELINE_DIGEST, None),
            _check("operator_receipt_digest_confirmation_matches", EXPECTED_LIVE_RECEIPT_DIGEST, None),
            _check("operator_confirms_in_range_dividend_count", EXPECTED_IN_RANGE_DIVIDEND_COUNT, None),
            _check("operator_confirms_in_range_dividend_implication", True, None),
            _check("operator_identity_digest_confirmation_matches", dividend.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, None),
            _check("operator_calendar_digest_confirmation_matches", dividend.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, None),
            _check("operator_schedule_digest_confirmation_matches", dividend.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, None),
            _check("operator_split_event_digest_confirmation_matches", dividend.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, None),
            *[_check(field, True, None) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_DIVIDEND_EVENT_AUDIT_FREEZE, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_DIVIDEND_EVENT_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check(
            "operator_dividend_review_digest_confirmation_matches",
            EXPECTED_DIVIDEND_REVIEW_PACKAGE_SEMANTIC_DIGEST,
            attestation.get("operator_confirms_dividend_review_package_digest"),
        ),
        _check(
            "operator_live_candidate_digest_confirmation_matches",
            EXPECTED_LIVE_DIVIDEND_CANDIDATE_DIGEST,
            attestation.get("operator_confirms_live_dividend_candidate_digest"),
        ),
        _check("operator_raw_digest_confirmation_matches", EXPECTED_LIVE_RAW_RESPONSE_DIGEST, attestation.get("operator_confirms_raw_response_digest")),
        _check("operator_timeline_digest_confirmation_matches", EXPECTED_LIVE_TIMELINE_DIGEST, attestation.get("operator_confirms_timeline_digest")),
        _check("operator_receipt_digest_confirmation_matches", EXPECTED_LIVE_RECEIPT_DIGEST, attestation.get("operator_confirms_receipt_digest")),
        _check("operator_confirms_in_range_dividend_count", EXPECTED_IN_RANGE_DIVIDEND_COUNT, attestation.get("operator_confirms_in_range_dividend_count")),
        _check("operator_confirms_in_range_dividend_implication", True, attestation.get("operator_confirms_in_range_dividend_implication")),
        _check(
            "operator_identity_digest_confirmation_matches",
            dividend.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
            attestation.get("operator_confirms_identity_frozen_digest"),
        ),
        _check(
            "operator_calendar_digest_confirmation_matches",
            dividend.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
            attestation.get("operator_confirms_calendar_frozen_digest"),
        ),
        _check("operator_schedule_digest_confirmation_matches", dividend.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, attestation.get("operator_confirms_schedule_digest")),
        _check(
            "operator_split_event_digest_confirmation_matches",
            dividend.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
            attestation.get("operator_confirms_split_event_frozen_digest"),
        ),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise DividendEventOperatorFreezeError("operator_attestation must be a JSON object")
    for field in ("operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise DividendEventOperatorFreezeError(f"{field} must be a non-empty string")
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise DividendEventOperatorFreezeError(f"operator attestation failed: {failed[0]['check_id']}")
    return deepcopy(attestation)


def _authority_boundary() -> dict[str, Any]:
    return {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": dividend.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": dividend.PROFITABILITY_NOT_ACCEPTED,
    }


def _guardrails() -> dict[str, Any]:
    return {
        "binding_mode": "DIVIDEND_EVENT_AUDIT_FROZEN_REFERENCE_ONLY",
        "provider_requests_made_in_freeze": False,
        "dividend_event_audit_frozen": True,
        "acquisition_generation_created": False,
        "canonical_dataset_created": False,
        "registry_approval_created": False,
        "strategy_runtime_migration": False,
        "software_auto_approval": False,
    }


def _source_live_evidence_from_review(source_review: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_live_dividend_candidate_digest": source_review["reviewed_candidate_semantic_digest"],
        "source_live_provider_request_mode": source_review["reviewed_provider_request_mode"],
        "source_live_provider_response_status": source_review["reviewed_provider_response_status"],
        "source_live_raw_row_count": source_review["reviewed_provider_raw_row_count"],
        "source_live_audit_status": source_review["reviewed_audit_status"],
        "source_live_raw_response_digest": source_review["reviewed_raw_response_digest"],
        "source_live_timeline_digest": source_review["reviewed_timeline_digest"],
        "source_live_receipt_digest": source_review["reviewed_receipt_digest"],
    }


def _count_value(frozen_artifact: dict[str, Any], field: str) -> Any:
    if field in frozen_artifact:
        return frozen_artifact.get(field)
    counts = frozen_artifact.get("event_counts", {})
    return counts.get(field) if isinstance(counts, dict) else None


def _build_freeze_checklist(frozen_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = frozen_artifact.get("operator_attestation")
    segment = frozen_artifact.get("identity_segment", {})
    return [
        _check("dividend_review_package_digest_matches_expected", EXPECTED_DIVIDEND_REVIEW_PACKAGE_SEMANTIC_DIGEST, frozen_artifact.get("source_dividend_review_package_semantic_digest")),
        _check("dividend_review_package_has_zero_blockers", 0, frozen_artifact.get("source_dividend_review_blocker_count")),
        _check("live_dividend_candidate_digest_matches_expected", EXPECTED_LIVE_DIVIDEND_CANDIDATE_DIGEST, frozen_artifact.get("source_live_dividend_candidate_digest")),
        _check("raw_response_digest_matches_expected", EXPECTED_LIVE_RAW_RESPONSE_DIGEST, frozen_artifact.get("source_live_raw_response_digest")),
        _check("timeline_digest_matches_expected", EXPECTED_LIVE_TIMELINE_DIGEST, frozen_artifact.get("source_live_timeline_digest")),
        _check("receipt_digest_matches_expected", EXPECTED_LIVE_RECEIPT_DIGEST, frozen_artifact.get("source_live_receipt_digest")),
        _check("provider_request_mode_live", dividend.LIVE_PROVIDER_REQUEST, frozen_artifact.get("source_live_provider_request_mode")),
        _check("provider_response_status_ok", review.EXPECTED_PROVIDER_RESPONSE_STATUS, frozen_artifact.get("source_live_provider_response_status")),
        _check("provider_raw_row_count_sixteen", 16, frozen_artifact.get("source_live_raw_row_count")),
        _check("event_count_total_sixteen", 16, _count_value(frozen_artifact, "dividend_event_count_total")),
        _check("event_count_pre_range_zero", 0, _count_value(frozen_artifact, "dividend_event_count_pre_range")),
        _check("event_count_in_range_sixteen", 16, _count_value(frozen_artifact, "dividend_event_count_in_range")),
        _check("event_count_post_range_zero", 0, _count_value(frozen_artifact, "dividend_event_count_post_range")),
        _check("event_count_unknown_zero", 0, _count_value(frozen_artifact, "dividend_event_count_unknown")),
        _check("audit_status_found_in_range_dividend", EXPECTED_AUDIT_STATUS, frozen_artifact.get("source_live_audit_status")),
        _check("in_range_dividend_implication_preserved", EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, frozen_artifact.get("in_range_dividend_implication")),
        *_attestation_checks(attestation if isinstance(attestation, dict) else None),
        _check("identity_segment_frozen_true", True, frozen_artifact.get("identity_segment_frozen")),
        _check("calendar_operator_frozen_true", True, frozen_artifact.get("calendar_operator_frozen")),
        _check("split_event_audit_frozen_true", True, frozen_artifact.get("split_event_audit_frozen")),
        _check("dividend_event_audit_frozen_true", True, frozen_artifact.get("dividend_event_audit_frozen")),
        _check("canonical_eligibility_false", False, frozen_artifact.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, frozen_artifact.get("registry_eligibility")),
        _check("acquisition_generation_freeze_false", False, frozen_artifact.get("acquisition_generation_freeze")),
        _check("strategy_runtime_migration_false", False, frozen_artifact.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, frozen_artifact.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", dividend.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, frozen_artifact.get("predictive_usefulness")),
        _check("profitability_not_accepted", dividend.PROFITABILITY_NOT_ACCEPTED, frozen_artifact.get("profitability")),
        _check("segment_fields_match", dividend.FIXED_IDENTITY_SEGMENT, segment),
        _check("contract_digest_matches", dividend.EXPECTED_ACQUISITION_CONTRACT_DIGEST, frozen_artifact.get("acquisition_contract_digest")),
        _check(
            "authority_digests_match",
            {
                "identity_segment_frozen_digest": dividend.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
                "exchange_calendar_frozen_digest": dividend.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
                "schedule_semantic_digest": dividend.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
                "split_event_audit_frozen_digest": dividend.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
                "previous_scaffold_candidate_digest": dividend.PREVIOUS_DIVIDEND_EVENT_AUDIT_SCAFFOLD_DIGEST,
            },
            {
                "identity_segment_frozen_digest": frozen_artifact.get("identity_segment_frozen_digest"),
                "exchange_calendar_frozen_digest": frozen_artifact.get("exchange_calendar_frozen_digest"),
                "schedule_semantic_digest": frozen_artifact.get("schedule_semantic_digest"),
                "split_event_audit_frozen_digest": frozen_artifact.get("split_event_audit_frozen_digest"),
                "previous_scaffold_candidate_digest": frozen_artifact.get("previous_scaffold_candidate_digest"),
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
        "dividend_event_audit_freeze_authorized_by_operator": failed == 0,
        "software_auto_approval": False,
    }


def _frozen_digest_payload(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(frozen_artifact)
    payload.pop("dividend_event_audit_frozen_semantic_digest", None)
    payload.pop("frozen_payload_digest", None)
    return payload


def dividend_event_audit_frozen_semantic_digest(frozen_artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for frozen dividend-event audit evidence."""
    return semantic_digest(_frozen_digest_payload(frozen_artifact))


def build_dividend_event_audit_frozen_v1(
    *,
    dividend_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build the offline dividend-event audit frozen artifact after operator attestation."""
    source_review = _source_dividend_review_package(dividend_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    live = _source_live_evidence_from_review(source_review)
    counts = deepcopy(source_review["event_counts"])
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_FROZEN,
        "schema_version": SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_OPERATOR_FREEZE_V1,
        "freeze_status": DIVIDEND_EVENT_AUDIT_FROZEN,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "created_offline": True,
        "provider_requests_made_in_freeze": False,
        "automatic_stitching": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "predictive_usefulness": dividend.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": dividend.PROFITABILITY_NOT_ACCEPTED,
        "source_dividend_review_package_kind": source_review["artifact_kind"],
        "source_dividend_review_status": source_review["review_status"],
        "source_dividend_review_package_semantic_digest": source_review["dividend_event_review_package_semantic_digest"],
        "source_dividend_review_checklist_total": source_review["review_summary"]["total_checks"],
        "source_dividend_review_checklist_passed": source_review["review_summary"]["passed_checks"],
        "source_dividend_review_checklist_failed": source_review["review_summary"]["failed_checks"],
        "source_dividend_review_blocker_count": source_review["review_summary"]["blocker_count"],
        **live,
        "event_counts": counts,
        **counts,
        "in_range_dividends_found": source_review["in_range_dividends_found"],
        "in_range_dividend_count": source_review["in_range_dividend_count"],
        "in_range_dividend_implication": source_review["in_range_dividend_implication"],
        "identity_segment_frozen_digest": dividend.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": dividend.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": dividend.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": dividend.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "previous_scaffold_candidate_digest": dividend.PREVIOUS_DIVIDEND_EVENT_AUDIT_SCAFFOLD_DIGEST,
        "identity_segment": deepcopy(dividend.FIXED_IDENTITY_SEGMENT),
        "authority_bindings": deepcopy(dividend.FIXED_AUTHORITY_BINDINGS),
        "acquisition_contract_digest": dividend.EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "acquisition_contract": deepcopy(dividend.FIXED_ACQUISITION_CONTRACT),
        "operator_attestation": attestation,
        "authority_boundary": _authority_boundary(),
        "guardrails": _guardrails(),
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_FREEZE),
    }
    checklist = _build_freeze_checklist(artifact)
    artifact["freeze_checklist"] = checklist
    artifact["freeze_summary"] = _summary(checklist)
    artifact["dividend_event_audit_frozen_semantic_digest"] = dividend_event_audit_frozen_semantic_digest(artifact)
    validate_dividend_event_audit_frozen_v1(artifact)
    return artifact


def validate_dividend_event_audit_frozen_v1(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate frozen dividend-event audit evidence and return a receipt."""
    if not isinstance(frozen_artifact, dict):
        raise DividendEventOperatorFreezeError("dividend-event frozen artifact must be a JSON object")
    _expect(frozen_artifact.get("artifact_kind"), ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_FROZEN, "artifact_kind")
    _expect(frozen_artifact.get("schema_version"), SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_OPERATOR_FREEZE_V1, "schema_version")
    _expect(frozen_artifact.get("freeze_status"), DIVIDEND_EVENT_AUDIT_FROZEN, "freeze_status")
    _expect_true(frozen_artifact.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(frozen_artifact.get("calendar_operator_frozen"), "calendar_operator_frozen")
    _expect_true(frozen_artifact.get("split_event_audit_frozen"), "split_event_audit_frozen")
    _expect_true(frozen_artifact.get("dividend_event_audit_frozen"), "dividend_event_audit_frozen")
    _expect_true(frozen_artifact.get("created_offline"), "created_offline")
    _expect_false(frozen_artifact.get("provider_requests_made_in_freeze"), "provider_requests_made_in_freeze")
    for field in ("canonical_eligibility", "registry_eligibility", "acquisition_generation_freeze", "strategy_runtime_migration", "automatic_stitching"):
        _expect_false(frozen_artifact.get(field), field)
    _expect(frozen_artifact.get("predictive_usefulness"), dividend.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(frozen_artifact.get("profitability"), dividend.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(
        frozen_artifact.get("source_dividend_review_package_kind"),
        review.ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE,
        "source_dividend_review_package_kind",
    )
    _expect(
        frozen_artifact.get("source_dividend_review_status"),
        review.DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY,
        "source_dividend_review_status",
    )
    _expect(
        frozen_artifact.get("source_dividend_review_package_semantic_digest"),
        EXPECTED_DIVIDEND_REVIEW_PACKAGE_SEMANTIC_DIGEST,
        "source_dividend_review_package_semantic_digest",
    )
    _expect(frozen_artifact.get("source_dividend_review_checklist_total"), len(review.REQUIRED_CHECK_IDS), "source_dividend_review_checklist_total")
    _expect(frozen_artifact.get("source_dividend_review_checklist_passed"), len(review.REQUIRED_CHECK_IDS), "source_dividend_review_checklist_passed")
    _expect(frozen_artifact.get("source_dividend_review_checklist_failed"), 0, "source_dividend_review_checklist_failed")
    _expect(frozen_artifact.get("source_dividend_review_blocker_count"), 0, "source_dividend_review_blocker_count")
    _expect(frozen_artifact.get("source_live_dividend_candidate_digest"), EXPECTED_LIVE_DIVIDEND_CANDIDATE_DIGEST, "source_live_dividend_candidate_digest")
    _expect(frozen_artifact.get("source_live_provider_request_mode"), dividend.LIVE_PROVIDER_REQUEST, "source_live_provider_request_mode")
    _expect(frozen_artifact.get("source_live_provider_response_status"), review.EXPECTED_PROVIDER_RESPONSE_STATUS, "source_live_provider_response_status")
    _expect(frozen_artifact.get("source_live_raw_row_count"), 16, "source_live_raw_row_count")
    _expect(frozen_artifact.get("source_live_audit_status"), EXPECTED_AUDIT_STATUS, "source_live_audit_status")
    _expect(frozen_artifact.get("source_live_raw_response_digest"), EXPECTED_LIVE_RAW_RESPONSE_DIGEST, "source_live_raw_response_digest")
    _expect(frozen_artifact.get("source_live_timeline_digest"), EXPECTED_LIVE_TIMELINE_DIGEST, "source_live_timeline_digest")
    _expect(frozen_artifact.get("source_live_receipt_digest"), EXPECTED_LIVE_RECEIPT_DIGEST, "source_live_receipt_digest")
    _expect(frozen_artifact.get("event_counts"), review.EXPECTED_EVENT_COUNTS, "event_counts")
    for field, expected in review.EXPECTED_EVENT_COUNTS.items():
        _expect(frozen_artifact.get(field), expected, field)
    _expect_true(frozen_artifact.get("in_range_dividends_found"), "in_range_dividends_found")
    _expect(frozen_artifact.get("in_range_dividend_count"), 16, "in_range_dividend_count")
    _expect(frozen_artifact.get("in_range_dividend_implication"), EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, "in_range_dividend_implication")
    _expect(frozen_artifact.get("identity_segment_frozen_digest"), dividend.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, "identity_segment_frozen_digest")
    _expect(frozen_artifact.get("exchange_calendar_frozen_digest"), dividend.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, "exchange_calendar_frozen_digest")
    _expect(frozen_artifact.get("schedule_semantic_digest"), dividend.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, "schedule_semantic_digest")
    _expect(frozen_artifact.get("split_event_audit_frozen_digest"), dividend.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, "split_event_audit_frozen_digest")
    _expect(frozen_artifact.get("previous_scaffold_candidate_digest"), dividend.PREVIOUS_DIVIDEND_EVENT_AUDIT_SCAFFOLD_DIGEST, "previous_scaffold_candidate_digest")
    _expect(frozen_artifact.get("identity_segment"), dividend.FIXED_IDENTITY_SEGMENT, "identity_segment")
    _expect(frozen_artifact.get("authority_bindings"), dividend.FIXED_AUTHORITY_BINDINGS, "authority_bindings")
    _expect(frozen_artifact.get("acquisition_contract_digest"), dividend.EXPECTED_ACQUISITION_CONTRACT_DIGEST, "acquisition_contract_digest")
    _expect(frozen_artifact.get("acquisition_contract"), dividend.FIXED_ACQUISITION_CONTRACT, "acquisition_contract")
    _expect(frozen_artifact.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    _expect(frozen_artifact.get("guardrails"), _guardrails(), "guardrails")
    _validated_operator_attestation(frozen_artifact.get("operator_attestation"))

    checklist = _build_freeze_checklist(frozen_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_FREEZE_CHECK_IDS, "freeze_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise DividendEventOperatorFreezeError(f"freeze checklist contains failed check: {failed[0]['check_id']}")
    _expect(frozen_artifact.get("freeze_checklist"), checklist, "freeze_checklist")
    summary = _summary(checklist)
    _expect(frozen_artifact.get("freeze_summary"), summary, "freeze_summary")
    _expect_true(summary.get("dividend_event_audit_freeze_authorized_by_operator"), "dividend_event_audit_freeze_authorized_by_operator")
    _expect_false(summary.get("software_auto_approval"), "software_auto_approval")
    _expect(frozen_artifact.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_FREEZE, "remaining_roadmap")

    digest = dividend_event_audit_frozen_semantic_digest(frozen_artifact)
    _expect(
        frozen_artifact.get("dividend_event_audit_frozen_semantic_digest"),
        digest,
        "dividend_event_audit_frozen_semantic_digest",
    )
    return {
        "status": "DIVIDEND_EVENT_AUDIT_FROZEN_VALID",
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_FROZEN,
        "freeze_status": DIVIDEND_EVENT_AUDIT_FROZEN,
        "source_dividend_review_package_semantic_digest": EXPECTED_DIVIDEND_REVIEW_PACKAGE_SEMANTIC_DIGEST,
        "source_live_dividend_candidate_digest": EXPECTED_LIVE_DIVIDEND_CANDIDATE_DIGEST,
        "source_live_raw_response_digest": EXPECTED_LIVE_RAW_RESPONSE_DIGEST,
        "source_live_timeline_digest": EXPECTED_LIVE_TIMELINE_DIGEST,
        "source_live_receipt_digest": EXPECTED_LIVE_RECEIPT_DIGEST,
        "dividend_event_audit_frozen_semantic_digest": digest,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "dividend_event_audit_freeze_authorized_by_operator": True,
        "software_auto_approval": False,
        "provider_requests_made_in_freeze": False,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        **review.EXPECTED_EVENT_COUNTS,
        "audit_status": EXPECTED_AUDIT_STATUS,
    }


def write_dividend_event_audit_frozen_v1(
    output_dir: str | Path,
    *,
    dividend_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the dividend-event audit frozen JSON artifact without overwriting output."""
    frozen = build_dividend_event_audit_frozen_v1(
        dividend_review_package=dividend_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_dividend_event_audit_frozen_v1(frozen)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_dividend_event_audit_frozen_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise DividendEventOperatorFreezeError("dividend-event frozen artifact filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise DividendEventOperatorFreezeError("dividend-event frozen output already exists")
    payload = canonical_json_bytes(frozen)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "frozen_payload_digest": sha256_bytes(payload),
    }


def build_dividend_event_audit_frozen_markdown_v1(frozen_artifact: dict[str, Any]) -> str:
    """Build a compact Markdown view of validated frozen dividend-event audit evidence."""
    validation = validate_dividend_event_audit_frozen_v1(frozen_artifact)
    attestation = frozen_artifact["operator_attestation"]
    segment = frozen_artifact["identity_segment"]
    counts = frozen_artifact["event_counts"]
    authority = frozen_artifact["authority_boundary"]
    lines = [
        "# Dividend-Event Audit Frozen v1",
        "",
        "## Frozen Dividend-Event Audit",
        f"- Artifact kind: `{frozen_artifact['artifact_kind']}`",
        f"- Freeze status: `{frozen_artifact['freeze_status']}`",
        f"- Frozen artifact digest: `{validation['dividend_event_audit_frozen_semantic_digest']}`",
        f"- Dividend event audit frozen: `{frozen_artifact['dividend_event_audit_frozen']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        f"- Attestation phrase: `{attestation['operator_attestation_phrase']}`",
        "",
        "## Source Dividend Review Package",
        f"- Artifact kind: `{frozen_artifact['source_dividend_review_package_kind']}`",
        f"- Review status: `{frozen_artifact['source_dividend_review_status']}`",
        f"- Review package digest: `{frozen_artifact['source_dividend_review_package_semantic_digest']}`",
        f"- Review checks: `{frozen_artifact['source_dividend_review_checklist_passed']}` passed of `{frozen_artifact['source_dividend_review_checklist_total']}`",
        f"- Review blockers: `{frozen_artifact['source_dividend_review_blocker_count']}`",
        "",
        "## Live Provider Evidence",
        f"- Live dividend candidate digest: `{frozen_artifact['source_live_dividend_candidate_digest']}`",
        f"- Provider request mode: `{frozen_artifact['source_live_provider_request_mode']}`",
        f"- Provider response status: `{frozen_artifact['source_live_provider_response_status']}`",
        f"- Raw row count: `{frozen_artifact['source_live_raw_row_count']}`",
        f"- Raw response digest: `{frozen_artifact['source_live_raw_response_digest']}`",
        f"- Timeline digest: `{frozen_artifact['source_live_timeline_digest']}`",
        f"- Receipt digest: `{frozen_artifact['source_live_receipt_digest']}`",
        f"- Audit status: `{frozen_artifact['source_live_audit_status']}`",
        "",
        "## Frozen Identity / Calendar / Split Bindings",
        f"- Ticker: `{segment['ticker']}`",
        f"- Composite FIGI: `{segment['composite_figi']}`",
        f"- Share Class FIGI: `{segment['share_class_figi']}`",
        f"- Primary MIC: `{segment['primary_mic']}`",
        f"- Security type: `{segment['security_type']}`",
        f"- Range: `{segment['segment_start']}` through `{segment['segment_end']}`",
        f"- Identity frozen digest: `{frozen_artifact['identity_segment_frozen_digest']}`",
        f"- Calendar frozen digest: `{frozen_artifact['exchange_calendar_frozen_digest']}`",
        f"- Schedule digest: `{frozen_artifact['schedule_semantic_digest']}`",
        f"- Split-event frozen digest: `{frozen_artifact['split_event_audit_frozen_digest']}`",
        "",
        "## Event Counts",
        f"- Total: `{counts['dividend_event_count_total']}`",
        f"- Pre-range: `{counts['dividend_event_count_pre_range']}`",
        f"- In-range: `{counts['dividend_event_count_in_range']}`",
        f"- Post-range: `{counts['dividend_event_count_post_range']}`",
        f"- Unknown: `{counts['dividend_event_count_unknown']}`",
        "",
        "## In-Range Dividend Interpretation",
        f"- In-range dividends found: `{frozen_artifact['in_range_dividends_found']}`",
        f"- In-range dividend count: `{frozen_artifact['in_range_dividend_count']}`",
        f"- Implication: `{frozen_artifact['in_range_dividend_implication']}`",
        "- This is not canonical approval and not acquisition-generation approval.",
        "",
        "## Freeze Checklist Summary",
        f"- Total checks: `{validation['total_checks']}`",
        f"- Passed checks: `{validation['passed_checks']}`",
        f"- Failed checks: `{validation['failed_checks']}`",
        f"- Blockers: `{validation['blocker_count']}`",
        f"- Software auto approval: `{frozen_artifact['freeze_summary']['software_auto_approval']}`",
        "",
        "## Authority Boundary",
        f"- identity_segment_frozen: `{authority['identity_segment_frozen']}`",
        f"- calendar_operator_frozen: `{authority['calendar_operator_frozen']}`",
        f"- split_event_audit_frozen: `{authority['split_event_audit_frozen']}`",
        f"- dividend_event_audit_frozen: `{authority['dividend_event_audit_frozen']}`",
        f"- canonical_eligibility: `{authority['canonical_eligibility']}`",
        f"- registry_eligibility: `{authority['registry_eligibility']}`",
        f"- acquisition_generation_freeze: `{authority['acquisition_generation_freeze']}`",
        f"- strategy_runtime_migration: `{authority['strategy_runtime_migration']}`",
        f"- automatic_stitching: `{authority['automatic_stitching']}`",
        f"- predictive_usefulness: `{authority['predictive_usefulness']}`",
        f"- profitability: `{authority['profitability']}`",
        "",
        "## Remaining Roadmap",
    ]
    lines.extend(f"{index}. {task}" for index, task in enumerate(REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_FREEZE, start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider requests were made during freeze.",
            "- No dividend evidence was refreshed.",
            "- No acquisition bars are generated or frozen.",
            "- No canonical or registry eligibility is approved.",
            "- No Strategy, runtime, broker, or execution behavior is changed.",
            "- Predictive usefulness and profitability remain not accepted.",
        ]
    )
    return "\n".join(lines) + "\n"
