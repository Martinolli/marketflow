"""Offline operator-review package for dividend-event audit candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import dividend_event_audit_service as dividend


ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE = "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_V1 = "dividend_event_audit_candidate_review_v1"
DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY = "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
DIVIDEND_EVENT_AUDIT_FROZEN = "DIVIDEND_EVENT_AUDIT_FROZEN"
LIVE_PROVIDER_EVIDENCE_STATUS_BINDING = "LIVE_PROVIDER_EVIDENCE_STATUS_BINDING"

EXPECTED_LIVE_CANDIDATE_SEMANTIC_DIGEST = "19a6275675c14e4ab06c9785828c60bd6a27274507fcddc60dced2ce82662d50"
EXPECTED_LIVE_RAW_RESPONSE_DIGEST = "3b60a63bf0103c1f6b735efd6b086626605c7e717f45d0299965e8988dee396f"
EXPECTED_LIVE_TIMELINE_DIGEST = "e5d13b1e203b3106855571299f147d0221d92ebcbed019e4b50e6f8e908c0659"
EXPECTED_LIVE_RECEIPT_DIGEST = "e8bb85d0ceefbe5f1bad411e333142e7957cca09572d0f7be64612eba4bef9e5"
EXPECTED_PROVIDER_RESPONSE_STATUS = "OK"
EXPECTED_PROVIDER_RESPONSE_PAGE_COUNT = 1
EXPECTED_PROVIDER_RAW_ROW_COUNT = 16
EXPECTED_AUDIT_STATUS = dividend.DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
HIGH = "HIGH"
INFO = "INFO"

EVENT_COUNT_FIELDS = [
    "dividend_event_count_total",
    "dividend_event_count_pre_range",
    "dividend_event_count_in_range",
    "dividend_event_count_post_range",
    "dividend_event_count_unknown",
]

EXPECTED_EVENT_COUNTS = {
    "dividend_event_count_total": 16,
    "dividend_event_count_pre_range": 0,
    "dividend_event_count_in_range": 16,
    "dividend_event_count_post_range": 0,
    "dividend_event_count_unknown": 0,
}

IN_RANGE_DIVIDEND_IMPLICATION = "ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY"

REMAINING_REQUIRED_TASKS = [
    "Digest-bound dividend-event operator freeze ceremony.",
    "Full 2022-2025 acquisition generation.",
    "Acquisition-generation freeze.",
    "SWING canonical dataset and registry approval.",
    "POSITION_SWING canonical dataset and registry approval.",
    "Normal runtime migration.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
]

REQUIRED_CHECK_IDS = [
    "candidate_kind_is_dividend_event_audit_candidate",
    "candidate_status_provider_evidence_bound",
    "candidate_digest_matches_recorded_live_evidence",
    "provider_request_mode_is_live",
    "provider_response_status_ok",
    "provider_raw_row_count_sixteen",
    "raw_response_digest_matches",
    "timeline_digest_matches",
    "receipt_digest_matches",
    "audit_status_found_in_range_dividend",
    "event_count_total_sixteen",
    "event_count_pre_range_zero",
    "event_count_in_range_sixteen",
    "event_count_post_range_zero",
    "event_count_unknown_zero",
    "identity_frozen_digest_matches",
    "calendar_frozen_digest_matches",
    "schedule_digest_matches",
    "split_event_frozen_digest_matches",
    "dividend_scaffold_digest_matches",
    "segment_ticker_matches",
    "segment_composite_figi_matches",
    "segment_share_class_figi_matches",
    "segment_primary_mic_matches",
    "segment_security_type_matches",
    "segment_start_matches",
    "segment_end_matches",
    "contract_digest_matches",
    "dividend_event_audit_frozen_false",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "acquisition_generation_freeze_false",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "provider_requests_made_in_review_false",
    "no_api_key_stored",
    "no_dividend_audit_frozen_artifact_created",
]

FORBIDDEN_FREEZE_FIELDS = frozenset(
    {
        "operator_approved_by",
        "operator_freeze_timestamp",
        "operator_freeze_digest",
        "operator_signature",
    }
)


class DividendEventOperatorReviewError(ValueError):
    """Raised when a dividend-event operator review package violates boundaries."""


def _status(expected: Any, actual: Any) -> str:
    return PASS if actual == expected else FAIL


def _check(check_id: str, expected: Any, actual: Any, *, severity: str = BLOCKER, message: str | None = None) -> dict[str, Any]:
    status = _status(expected, actual)
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": message or ("dividend-event live evidence matches" if status == PASS else "dividend-event live evidence mismatch"),
    }


def _authority_boundary() -> dict[str, Any]:
    return {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": dividend.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": dividend.PROFITABILITY_NOT_ACCEPTED,
    }


def _expected_live_evidence_binding() -> dict[str, Any]:
    return {
        "binding_mode": LIVE_PROVIDER_EVIDENCE_STATUS_BINDING,
        "raw_provider_payload_present": False,
        "reviewed_candidate_kind": dividend.ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE,
        "reviewed_candidate_status": dividend.DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "reviewed_candidate_semantic_digest": EXPECTED_LIVE_CANDIDATE_SEMANTIC_DIGEST,
        "reviewed_provider_request_mode": dividend.LIVE_PROVIDER_REQUEST,
        "reviewed_provider_endpoint": dividend.PROVIDER_ENDPOINT_MASSIVE_DIVIDENDS,
        "reviewed_provider_response_status": EXPECTED_PROVIDER_RESPONSE_STATUS,
        "reviewed_provider_response_page_count": EXPECTED_PROVIDER_RESPONSE_PAGE_COUNT,
        "reviewed_provider_raw_row_count": EXPECTED_PROVIDER_RAW_ROW_COUNT,
        "reviewed_raw_response_digest": EXPECTED_LIVE_RAW_RESPONSE_DIGEST,
        "reviewed_timeline_digest": EXPECTED_LIVE_TIMELINE_DIGEST,
        "reviewed_receipt_digest": EXPECTED_LIVE_RECEIPT_DIGEST,
        "reviewed_audit_status": EXPECTED_AUDIT_STATUS,
        "event_counts": deepcopy(EXPECTED_EVENT_COUNTS),
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": IN_RANGE_DIVIDEND_IMPLICATION,
        "identity_segment_frozen_digest": dividend.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": dividend.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": dividend.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": dividend.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "previous_scaffold_candidate_digest": dividend.PREVIOUS_DIVIDEND_EVENT_AUDIT_SCAFFOLD_DIGEST,
        "identity_segment": deepcopy(dividend.FIXED_IDENTITY_SEGMENT),
        "authority_bindings": deepcopy(dividend.FIXED_AUTHORITY_BINDINGS),
        "acquisition_contract": deepcopy(dividend.FIXED_ACQUISITION_CONTRACT),
        "authority_boundary": _authority_boundary(),
    }


def _binding_from_candidate(candidate: dict[str, Any] | None) -> dict[str, Any]:
    if candidate is None:
        return _expected_live_evidence_binding()
    reviewed = deepcopy(candidate)
    if reviewed.get("binding_mode") == LIVE_PROVIDER_EVIDENCE_STATUS_BINDING:
        return reviewed
    dividend.validate_dividend_event_audit_candidate_v1(reviewed)
    provider = reviewed.get("provider_evidence", {})
    outline = reviewed.get("dividend_event_audit_outline", {})
    return {
        "binding_mode": "LIVE_PROVIDER_CANDIDATE_BINDING",
        "raw_provider_payload_present": False,
        "reviewed_candidate_kind": reviewed.get("artifact_kind"),
        "reviewed_candidate_status": reviewed.get("candidate_status"),
        "reviewed_candidate_semantic_digest": reviewed.get("dividend_event_audit_candidate_semantic_digest"),
        "reviewed_provider_request_mode": reviewed.get("provider_request_mode"),
        "reviewed_provider_endpoint": provider.get("provider_endpoint") if isinstance(provider, dict) else None,
        "reviewed_provider_response_status": provider.get("provider_response_status") if isinstance(provider, dict) else None,
        "reviewed_provider_response_page_count": provider.get("provider_response_page_count") if isinstance(provider, dict) else None,
        "reviewed_provider_raw_row_count": provider.get("provider_raw_response_row_count") if isinstance(provider, dict) else None,
        "reviewed_raw_response_digest": reviewed.get("dividend_event_provider_raw_response_digest"),
        "reviewed_timeline_digest": reviewed.get("dividend_event_timeline_semantic_digest"),
        "reviewed_receipt_digest": reviewed.get("dividend_event_audit_receipt_digest"),
        "reviewed_audit_status": outline.get("audit_status") if isinstance(outline, dict) else None,
        "event_counts": {field: outline.get(field) for field in EVENT_COUNT_FIELDS} if isinstance(outline, dict) else {},
        "in_range_dividends_found": (outline.get("dividend_event_count_in_range", 0) > 0) if isinstance(outline, dict) else None,
        "in_range_dividend_count": outline.get("dividend_event_count_in_range") if isinstance(outline, dict) else None,
        "in_range_dividend_implication": IN_RANGE_DIVIDEND_IMPLICATION,
        "identity_segment_frozen_digest": reviewed.get("identity_segment_frozen_digest"),
        "exchange_calendar_frozen_digest": reviewed.get("exchange_calendar_frozen_digest"),
        "schedule_semantic_digest": reviewed.get("schedule_semantic_digest"),
        "split_event_audit_frozen_digest": reviewed.get("split_event_audit_frozen_digest"),
        "previous_scaffold_candidate_digest": reviewed.get("previous_scaffold_candidate_digest"),
        "identity_segment": deepcopy(reviewed.get("identity_segment")),
        "authority_bindings": deepcopy(reviewed.get("authority_bindings")),
        "acquisition_contract": deepcopy(reviewed.get("acquisition_contract")),
        "authority_boundary": deepcopy(reviewed.get("authority_boundary")),
    }


def _contains_secret_marker(value: Any) -> bool:
    rendered = repr(value).lower()
    forbidden = ("api_key", "apikey", "authorization", "bearer ", "polygon_api_key", "massive_api_key")
    return any(marker in rendered for marker in forbidden)


def _build_checklist(binding: dict[str, Any], package_context: dict[str, Any]) -> list[dict[str, Any]]:
    segment = binding.get("identity_segment", {})
    acquisition = binding.get("acquisition_contract", {})
    boundary = binding.get("authority_boundary", {})
    event_counts = binding.get("event_counts", {})
    return [
        _check("candidate_kind_is_dividend_event_audit_candidate", dividend.ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE, binding.get("reviewed_candidate_kind")),
        _check("candidate_status_provider_evidence_bound", dividend.DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND, binding.get("reviewed_candidate_status")),
        _check("candidate_digest_matches_recorded_live_evidence", EXPECTED_LIVE_CANDIDATE_SEMANTIC_DIGEST, binding.get("reviewed_candidate_semantic_digest")),
        _check("provider_request_mode_is_live", dividend.LIVE_PROVIDER_REQUEST, binding.get("reviewed_provider_request_mode")),
        _check("provider_response_status_ok", EXPECTED_PROVIDER_RESPONSE_STATUS, binding.get("reviewed_provider_response_status")),
        _check("provider_raw_row_count_sixteen", EXPECTED_PROVIDER_RAW_ROW_COUNT, binding.get("reviewed_provider_raw_row_count")),
        _check("raw_response_digest_matches", EXPECTED_LIVE_RAW_RESPONSE_DIGEST, binding.get("reviewed_raw_response_digest")),
        _check("timeline_digest_matches", EXPECTED_LIVE_TIMELINE_DIGEST, binding.get("reviewed_timeline_digest")),
        _check("receipt_digest_matches", EXPECTED_LIVE_RECEIPT_DIGEST, binding.get("reviewed_receipt_digest")),
        _check("audit_status_found_in_range_dividend", EXPECTED_AUDIT_STATUS, binding.get("reviewed_audit_status")),
        _check("event_count_total_sixteen", 16, event_counts.get("dividend_event_count_total") if isinstance(event_counts, dict) else None),
        _check("event_count_pre_range_zero", 0, event_counts.get("dividend_event_count_pre_range") if isinstance(event_counts, dict) else None),
        _check("event_count_in_range_sixteen", 16, event_counts.get("dividend_event_count_in_range") if isinstance(event_counts, dict) else None),
        _check("event_count_post_range_zero", 0, event_counts.get("dividend_event_count_post_range") if isinstance(event_counts, dict) else None),
        _check("event_count_unknown_zero", 0, event_counts.get("dividend_event_count_unknown") if isinstance(event_counts, dict) else None),
        _check("identity_frozen_digest_matches", dividend.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, binding.get("identity_segment_frozen_digest")),
        _check("calendar_frozen_digest_matches", dividend.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, binding.get("exchange_calendar_frozen_digest")),
        _check("schedule_digest_matches", dividend.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, binding.get("schedule_semantic_digest")),
        _check("split_event_frozen_digest_matches", dividend.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, binding.get("split_event_audit_frozen_digest")),
        _check("dividend_scaffold_digest_matches", dividend.PREVIOUS_DIVIDEND_EVENT_AUDIT_SCAFFOLD_DIGEST, binding.get("previous_scaffold_candidate_digest")),
        _check("segment_ticker_matches", dividend.FIXED_IDENTITY_SEGMENT["ticker"], segment.get("ticker") if isinstance(segment, dict) else None),
        _check("segment_composite_figi_matches", dividend.FIXED_IDENTITY_SEGMENT["composite_figi"], segment.get("composite_figi") if isinstance(segment, dict) else None),
        _check("segment_share_class_figi_matches", dividend.FIXED_IDENTITY_SEGMENT["share_class_figi"], segment.get("share_class_figi") if isinstance(segment, dict) else None),
        _check("segment_primary_mic_matches", dividend.FIXED_IDENTITY_SEGMENT["primary_mic"], segment.get("primary_mic") if isinstance(segment, dict) else None),
        _check("segment_security_type_matches", dividend.FIXED_IDENTITY_SEGMENT["security_type"], segment.get("security_type") if isinstance(segment, dict) else None),
        _check("segment_start_matches", dividend.FIXED_IDENTITY_SEGMENT["segment_start"], segment.get("segment_start") if isinstance(segment, dict) else None),
        _check("segment_end_matches", dividend.FIXED_IDENTITY_SEGMENT["segment_end"], segment.get("segment_end") if isinstance(segment, dict) else None),
        _check("contract_digest_matches", dividend.EXPECTED_ACQUISITION_CONTRACT_DIGEST, acquisition.get("contract_digest") if isinstance(acquisition, dict) else None),
        _check("dividend_event_audit_frozen_false", False, package_context.get("dividend_event_audit_frozen")),
        _check("canonical_eligibility_false", False, package_context.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, package_context.get("registry_eligibility")),
        _check("acquisition_generation_freeze_false", False, package_context.get("acquisition_generation_freeze")),
        _check("strategy_runtime_migration_false", False, package_context.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, package_context.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", dividend.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, package_context.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", dividend.PROFITABILITY_NOT_ACCEPTED, package_context.get("profitability"), severity=INFO),
        _check("provider_requests_made_in_review_false", False, package_context.get("provider_requests_made_in_review")),
        _check("no_api_key_stored", False, _contains_secret_marker({"binding": binding, "package_context": package_context}), severity=HIGH),
        _check(
            "no_dividend_audit_frozen_artifact_created",
            {"artifact_kind_is_not_frozen": True, "review_status_is_not_frozen": True, "freeze_status_is_null": True},
            {
                "artifact_kind_is_not_frozen": package_context.get("artifact_kind") != DIVIDEND_EVENT_AUDIT_FROZEN,
                "review_status_is_not_frozen": package_context.get("review_status") != DIVIDEND_EVENT_AUDIT_FROZEN,
                "freeze_status_is_null": package_context.get("freeze_status") is None,
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
        "operator_decision_required_before_freeze": True,
        "software_freeze_authorized": False,
    }


def _package_digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("dividend_event_review_package_semantic_digest", None)
    payload.pop("dividend_event_review_package_payload_digest", None)
    return payload


def dividend_event_review_package_semantic_digest(review_package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the dividend-event review package."""
    return semantic_digest(_package_digest_payload(review_package))


def build_dividend_event_audit_candidate_review_package_v1(candidate: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a digest-bound offline operator-review package for dividend-event evidence."""
    binding = _binding_from_candidate(candidate)
    package_context = {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE,
        "review_status": DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY,
        "freeze_status": None,
        "dividend_event_audit_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": dividend.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": dividend.PROFITABILITY_NOT_ACCEPTED,
        "provider_requests_made_in_review": False,
    }
    checklist = _build_checklist(binding, package_context)
    package: dict[str, Any] = {
        **package_context,
        "schema_version": SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_V1,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "reviewed_candidate_kind": binding.get("reviewed_candidate_kind"),
        "reviewed_candidate_status": binding.get("reviewed_candidate_status"),
        "reviewed_candidate_semantic_digest": binding.get("reviewed_candidate_semantic_digest"),
        "reviewed_provider_request_mode": binding.get("reviewed_provider_request_mode"),
        "reviewed_provider_response_status": binding.get("reviewed_provider_response_status"),
        "reviewed_provider_response_page_count": binding.get("reviewed_provider_response_page_count"),
        "reviewed_provider_raw_row_count": binding.get("reviewed_provider_raw_row_count"),
        "reviewed_raw_response_digest": binding.get("reviewed_raw_response_digest"),
        "reviewed_timeline_digest": binding.get("reviewed_timeline_digest"),
        "reviewed_receipt_digest": binding.get("reviewed_receipt_digest"),
        "reviewed_audit_status": binding.get("reviewed_audit_status"),
        "event_counts": deepcopy(binding.get("event_counts")),
        "in_range_dividends_found": binding.get("in_range_dividends_found"),
        "in_range_dividend_count": binding.get("in_range_dividend_count"),
        "in_range_dividend_implication": binding.get("in_range_dividend_implication"),
        "live_evidence_binding": binding,
        "authority_boundary": _authority_boundary(),
        "review_checklist": checklist,
        "review_summary": _summary(checklist),
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
        "operator_freeze_controls": {
            "operator_approved_by": None,
            "operator_freeze_timestamp": None,
            "operator_freeze_digest": None,
            "operator_signature": None,
            "freeze_status": None,
        },
    }
    package["dividend_event_review_package_semantic_digest"] = dividend_event_review_package_semantic_digest(package)
    return package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key in {"artifact_kind", "review_status", "reviewed_candidate_kind", "reviewed_candidate_status", "candidate_status", "freeze_status"}:
            if value == DIVIDEND_EVENT_AUDIT_FROZEN:
                raise DividendEventOperatorReviewError(f"{current_path} must not emit DIVIDEND_EVENT_AUDIT_FROZEN")
        if key in FORBIDDEN_FREEZE_FIELDS and value is not None:
            raise DividendEventOperatorReviewError(f"{current_path} must be null")
        if key == "freeze_status" and value is not None:
            raise DividendEventOperatorReviewError(f"{current_path} must be null")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise DividendEventOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise DividendEventOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise DividendEventOperatorReviewError(f"{field_name} must be true")


def validate_dividend_event_audit_candidate_review_package_v1(review_package: dict[str, Any]) -> dict[str, Any]:
    """Validate a dividend-event review package and fail closed on failed checks."""
    if not isinstance(review_package, dict):
        raise DividendEventOperatorReviewError("dividend-event review package must be a JSON object")
    _reject_forbidden_values(review_package)
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY, "review_status")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    _expect_true(review_package.get("created_offline"), "created_offline")
    _expect_false(review_package.get("provider_requests_made_in_review"), "provider_requests_made_in_review")
    _expect_false(review_package.get("dividend_event_audit_frozen"), "dividend_event_audit_frozen")
    _expect_true(review_package.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(review_package.get("calendar_operator_frozen"), "calendar_operator_frozen")
    _expect_true(review_package.get("split_event_audit_frozen"), "split_event_audit_frozen")
    for field in ("canonical_eligibility", "registry_eligibility", "acquisition_generation_freeze", "strategy_runtime_migration", "automatic_stitching"):
        _expect_false(review_package.get(field), field)
    _expect(review_package.get("predictive_usefulness"), dividend.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), dividend.PROFITABILITY_NOT_ACCEPTED, "profitability")

    binding = review_package.get("live_evidence_binding")
    if not isinstance(binding, dict):
        raise DividendEventOperatorReviewError("live_evidence_binding must be a JSON object")
    _expect(binding.get("binding_mode"), LIVE_PROVIDER_EVIDENCE_STATUS_BINDING, "live_evidence_binding.binding_mode")
    _expect(binding.get("raw_provider_payload_present"), False, "live_evidence_binding.raw_provider_payload_present")
    _expect(binding, _expected_live_evidence_binding(), "live_evidence_binding")

    for field in (
        "reviewed_candidate_kind",
        "reviewed_candidate_status",
        "reviewed_candidate_semantic_digest",
        "reviewed_provider_request_mode",
        "reviewed_provider_response_status",
        "reviewed_provider_response_page_count",
        "reviewed_provider_raw_row_count",
        "reviewed_raw_response_digest",
        "reviewed_timeline_digest",
        "reviewed_receipt_digest",
        "reviewed_audit_status",
        "in_range_dividends_found",
        "in_range_dividend_count",
        "in_range_dividend_implication",
    ):
        _expect(review_package.get(field), binding.get(field), field)
    _expect(review_package.get("event_counts"), EXPECTED_EVENT_COUNTS, "event_counts")
    _expect(review_package.get("in_range_dividends_found"), True, "in_range_dividends_found")
    _expect(review_package.get("in_range_dividend_count"), 16, "in_range_dividend_count")
    _expect(review_package.get("in_range_dividend_implication"), IN_RANGE_DIVIDEND_IMPLICATION, "in_range_dividend_implication")
    _expect(review_package.get("authority_boundary"), _authority_boundary(), "authority_boundary")

    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise DividendEventOperatorReviewError("review_checklist must be a list")
    check_ids = [item.get("check_id") for item in checklist if isinstance(item, dict)]
    _expect(check_ids, REQUIRED_CHECK_IDS, "review_checklist check IDs")
    package_context = {
        "artifact_kind": review_package.get("artifact_kind"),
        "review_status": review_package.get("review_status"),
        "freeze_status": review_package.get("freeze_status"),
        "dividend_event_audit_frozen": review_package.get("dividend_event_audit_frozen"),
        "canonical_eligibility": review_package.get("canonical_eligibility"),
        "registry_eligibility": review_package.get("registry_eligibility"),
        "acquisition_generation_freeze": review_package.get("acquisition_generation_freeze"),
        "strategy_runtime_migration": review_package.get("strategy_runtime_migration"),
        "automatic_stitching": review_package.get("automatic_stitching"),
        "predictive_usefulness": review_package.get("predictive_usefulness"),
        "profitability": review_package.get("profitability"),
        "provider_requests_made_in_review": review_package.get("provider_requests_made_in_review"),
    }
    _expect(checklist, _build_checklist(binding, package_context), "review_checklist")
    failed = [item for item in checklist if item.get("status") != PASS]
    if failed:
        raise DividendEventOperatorReviewError("dividend-event review package contains failed checks")

    expected_summary = _summary(checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    summary = review_package["review_summary"]
    _expect_true(summary.get("ready_for_operator_assessment"), "ready_for_operator_assessment")
    _expect_true(summary.get("operator_decision_required_before_freeze"), "operator_decision_required_before_freeze")
    _expect_false(summary.get("software_freeze_authorized"), "software_freeze_authorized")
    _expect(review_package.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")

    controls = review_package.get("operator_freeze_controls")
    if not isinstance(controls, dict):
        raise DividendEventOperatorReviewError("operator_freeze_controls must be a JSON object")
    for field in ("operator_approved_by", "operator_freeze_timestamp", "operator_freeze_digest", "operator_signature", "freeze_status"):
        _expect(controls.get(field), None, f"operator_freeze_controls.{field}")

    digest = dividend_event_review_package_semantic_digest(review_package)
    _expect(review_package.get("dividend_event_review_package_semantic_digest"), digest, "dividend_event_review_package_semantic_digest")
    return {
        "status": "DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE,
        "review_status": DIVIDEND_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY,
        "reviewed_candidate_semantic_digest": EXPECTED_LIVE_CANDIDATE_SEMANTIC_DIGEST,
        "reviewed_raw_response_digest": EXPECTED_LIVE_RAW_RESPONSE_DIGEST,
        "reviewed_timeline_digest": EXPECTED_LIVE_TIMELINE_DIGEST,
        "reviewed_receipt_digest": EXPECTED_LIVE_RECEIPT_DIGEST,
        "dividend_event_review_package_semantic_digest": digest,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "provider_requests_made_in_review": False,
        "dividend_event_audit_frozen": False,
        "software_freeze_authorized": False,
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": IN_RANGE_DIVIDEND_IMPLICATION,
        **EXPECTED_EVENT_COUNTS,
        "audit_status": EXPECTED_AUDIT_STATUS,
    }


def write_dividend_event_audit_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the dividend-event review package JSON artifact without overwriting output."""
    review_package = build_dividend_event_audit_candidate_review_package_v1(candidate)
    validation = validate_dividend_event_audit_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_dividend_event_audit_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise DividendEventOperatorReviewError("dividend-event review package filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise DividendEventOperatorReviewError("dividend-event review package output already exists")
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "dividend_event_review_package_payload_digest": sha256_bytes(payload),
    }


def build_dividend_event_audit_candidate_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Build a compact Markdown view of a validated dividend-event review package."""
    validation = validate_dividend_event_audit_candidate_review_package_v1(review_package)
    binding = review_package["live_evidence_binding"]
    segment = binding["identity_segment"]
    boundary = review_package["authority_boundary"]
    counts = review_package["event_counts"]
    failed_checks = [item for item in review_package["review_checklist"] if item["status"] != PASS]
    lines = [
        "# Dividend-Event Audit Candidate Review Package v1",
        "",
        "## Reviewed Dividend-Event Candidate",
        f"- Artifact kind: `{review_package['reviewed_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_candidate_status']}`",
        f"- Candidate semantic digest: `{review_package['reviewed_candidate_semantic_digest']}`",
        f"- Review package digest: `{validation['dividend_event_review_package_semantic_digest']}`",
        f"- Binding mode: `{binding['binding_mode']}`",
        "",
        "## Live Provider Evidence Summary",
        f"- Provider request mode: `{review_package['reviewed_provider_request_mode']}`",
        f"- Provider response status: `{review_package['reviewed_provider_response_status']}`",
        f"- Provider response page count: `{review_package['reviewed_provider_response_page_count']}`",
        f"- Provider raw row count: `{review_package['reviewed_provider_raw_row_count']}`",
        f"- Raw response digest: `{review_package['reviewed_raw_response_digest']}`",
        f"- Timeline digest: `{review_package['reviewed_timeline_digest']}`",
        f"- Receipt digest: `{review_package['reviewed_receipt_digest']}`",
        f"- Audit status: `{review_package['reviewed_audit_status']}`",
        "",
        "## In-Range Dividend Implication",
        f"- In-range dividends found: `{review_package['in_range_dividends_found']}`",
        f"- In-range dividend count: `{review_package['in_range_dividend_count']}`",
        f"- Implication: `{review_package['in_range_dividend_implication']}`",
        "- The observed in-range dividends are not a review-package blocker.",
        "",
        "## Frozen Identity / Calendar / Split Bindings",
        f"- Ticker: `{segment['ticker']}`",
        f"- Composite FIGI: `{segment['composite_figi']}`",
        f"- Share Class FIGI: `{segment['share_class_figi']}`",
        f"- Primary MIC: `{segment['primary_mic']}`",
        f"- Security type: `{segment['security_type']}`",
        f"- Range: `{segment['segment_start']}` through `{segment['segment_end']}`",
        f"- Identity frozen digest: `{binding['identity_segment_frozen_digest']}`",
        f"- Calendar frozen digest: `{binding['exchange_calendar_frozen_digest']}`",
        f"- Schedule digest: `{binding['schedule_semantic_digest']}`",
        f"- Split-event frozen digest: `{binding['split_event_audit_frozen_digest']}`",
        "",
        "## Event Counts",
        f"- Total: `{counts['dividend_event_count_total']}`",
        f"- Pre-range: `{counts['dividend_event_count_pre_range']}`",
        f"- In-range: `{counts['dividend_event_count_in_range']}`",
        f"- Post-range: `{counts['dividend_event_count_post_range']}`",
        f"- Unknown: `{counts['dividend_event_count_unknown']}`",
        "",
        "## Checklist Summary",
        f"- Total checks: `{validation['total_checks']}`",
        f"- Passed checks: `{validation['passed_checks']}`",
        f"- Failed checks: `{validation['failed_checks']}`",
        f"- Blockers: `{validation['blocker_count']}`",
        "",
        "## Failed Checks",
    ]
    if failed_checks:
        lines.extend(f"- `{item['check_id']}`: {item['message']}" for item in failed_checks)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- identity_segment_frozen: `{boundary['identity_segment_frozen']}`",
            f"- calendar_operator_frozen: `{boundary['calendar_operator_frozen']}`",
            f"- split_event_audit_frozen: `{boundary['split_event_audit_frozen']}`",
            f"- dividend_event_audit_frozen: `{boundary['dividend_event_audit_frozen']}`",
            f"- canonical_eligibility: `{boundary['canonical_eligibility']}`",
            f"- registry_eligibility: `{boundary['registry_eligibility']}`",
            f"- acquisition_generation_freeze: `{boundary['acquisition_generation_freeze']}`",
            f"- strategy_runtime_migration: `{boundary['strategy_runtime_migration']}`",
            f"- automatic_stitching: `{boundary['automatic_stitching']}`",
            f"- predictive_usefulness: `{boundary['predictive_usefulness']}`",
            f"- profitability: `{boundary['profitability']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(REMAINING_REQUIRED_TASKS, start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider requests were made during review.",
            "- No `DIVIDEND_EVENT_AUDIT_FROZEN` artifact or status is created.",
            "- `dividend_event_audit_frozen` remains `false`.",
            "- Operator decision remains required before any future dividend-event freeze ceremony.",
            "- No canonical, registry, acquisition-generation, Strategy, runtime, broker, or execution approval is created.",
            "- Predictive usefulness and profitability remain not accepted.",
        ]
    )
    return "\n".join(lines) + "\n"
