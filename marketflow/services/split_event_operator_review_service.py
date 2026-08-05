"""Offline operator-review package for split-event audit candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import split_event_audit_service as split


ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE = "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE"
SCHEMA_VERSION_SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_V1 = "split_event_audit_candidate_review_v1"
SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY = "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY"
SPLIT_EVENT_AUDIT_FROZEN = "SPLIT_EVENT_AUDIT_FROZEN"
LIVE_PROVIDER_EVIDENCE_STATUS_BINDING = "LIVE_PROVIDER_EVIDENCE_STATUS_BINDING"

EXPECTED_LIVE_CANDIDATE_SEMANTIC_DIGEST = "92c0a4b4350be4731501fae3300f528bf5f42e5140f01e587ff9c87014c1f66b"
EXPECTED_LIVE_RAW_RESPONSE_DIGEST = "e8db3f18ca3b441a4ae6436d22f48a5481fe5ab0554c092b7cba4010178974bf"
EXPECTED_LIVE_TIMELINE_DIGEST = "e73556f686e19eef149a95141718bb6c5ab2f53f4df9e5e3f9520f7c050c5076"
EXPECTED_LIVE_RECEIPT_DIGEST = "dd09dd19fe091816310ec4896ba1d63579f5e794d2efc4de7a897e9c5b117d91"
EXPECTED_PROVIDER_RESPONSE_STATUS = "OK"
EXPECTED_PROVIDER_RESPONSE_PAGE_COUNT = 1
EXPECTED_PROVIDER_RAW_ROW_COUNT = 0
EXPECTED_AUDIT_STATUS = split.SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
HIGH = "HIGH"
INFO = "INFO"

EVENT_COUNT_FIELDS = [
    "split_event_count_total",
    "split_event_count_pre_range",
    "split_event_count_in_range",
    "split_event_count_post_range",
    "split_event_count_unknown",
]

EXPECTED_EVENT_COUNTS = {
    "split_event_count_total": 0,
    "split_event_count_pre_range": 0,
    "split_event_count_in_range": 0,
    "split_event_count_post_range": 0,
    "split_event_count_unknown": 0,
}

REMAINING_REQUIRED_TASKS = [
    "Digest-bound split-event operator freeze ceremony.",
    "Dividend-event audit candidate.",
    "Dividend-event provider evidence collection.",
    "Dividend-event operator review package.",
    "Dividend-event operator freeze ceremony.",
    "Full 2022-2025 acquisition generation.",
    "Acquisition-generation freeze.",
    "SWING canonical dataset and registry approval.",
    "POSITION_SWING canonical dataset and registry approval.",
    "Normal runtime migration.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
]

REQUIRED_CHECK_IDS = [
    "candidate_kind_is_split_event_audit_candidate",
    "candidate_status_provider_evidence_bound",
    "candidate_digest_matches_recorded_live_evidence",
    "provider_request_mode_is_live",
    "provider_response_status_ok",
    "provider_raw_row_count_zero",
    "raw_response_digest_matches",
    "timeline_digest_matches",
    "receipt_digest_matches",
    "audit_status_supports_no_in_range_split",
    "event_count_total_zero",
    "event_count_pre_range_zero",
    "event_count_in_range_zero",
    "event_count_post_range_zero",
    "event_count_unknown_zero",
    "identity_frozen_digest_matches",
    "calendar_frozen_digest_matches",
    "schedule_digest_matches",
    "scaffold_digest_matches",
    "segment_ticker_matches",
    "segment_composite_figi_matches",
    "segment_share_class_figi_matches",
    "segment_primary_mic_matches",
    "segment_security_type_matches",
    "segment_start_matches",
    "segment_end_matches",
    "contract_digest_matches",
    "split_event_audit_frozen_false",
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
    "no_split_audit_frozen_artifact_created",
]

FORBIDDEN_FREEZE_FIELDS = frozenset(
    {
        "operator_approved_by",
        "operator_freeze_timestamp",
        "operator_freeze_digest",
        "operator_signature",
    }
)


class SplitEventOperatorReviewError(ValueError):
    """Raised when a split-event operator review package violates boundaries."""


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
        "message": message or ("split-event live evidence matches" if status == PASS else "split-event live evidence mismatch"),
    }


def _authority_boundary() -> dict[str, Any]:
    return {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": False,
        "dividend_event_audit_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": split.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": split.PROFITABILITY_NOT_ACCEPTED,
    }


def _expected_live_evidence_binding() -> dict[str, Any]:
    return {
        "binding_mode": LIVE_PROVIDER_EVIDENCE_STATUS_BINDING,
        "raw_provider_payload_present": False,
        "reviewed_candidate_kind": split.ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE,
        "reviewed_candidate_status": split.SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "reviewed_candidate_semantic_digest": EXPECTED_LIVE_CANDIDATE_SEMANTIC_DIGEST,
        "reviewed_provider_request_mode": split.LIVE_PROVIDER_REQUEST,
        "reviewed_provider_endpoint": "/stocks/v1/splits",
        "reviewed_provider_response_status": EXPECTED_PROVIDER_RESPONSE_STATUS,
        "reviewed_provider_response_page_count": EXPECTED_PROVIDER_RESPONSE_PAGE_COUNT,
        "reviewed_provider_raw_row_count": EXPECTED_PROVIDER_RAW_ROW_COUNT,
        "reviewed_raw_response_digest": EXPECTED_LIVE_RAW_RESPONSE_DIGEST,
        "reviewed_timeline_digest": EXPECTED_LIVE_TIMELINE_DIGEST,
        "reviewed_receipt_digest": EXPECTED_LIVE_RECEIPT_DIGEST,
        "reviewed_audit_status": EXPECTED_AUDIT_STATUS,
        "event_counts": deepcopy(EXPECTED_EVENT_COUNTS),
        "identity_segment_frozen_digest": split.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": split.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": split.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "previous_scaffold_candidate_digest": split.PREVIOUS_SPLIT_EVENT_AUDIT_SCAFFOLD_DIGEST,
        "identity_segment": deepcopy(split.FIXED_IDENTITY_SEGMENT),
        "authority_bindings": deepcopy(split.FIXED_AUTHORITY_BINDINGS),
        "acquisition_contract": deepcopy(split.FIXED_ACQUISITION_CONTRACT),
        "authority_boundary": _authority_boundary(),
    }


def _binding_from_candidate(candidate: dict[str, Any] | None) -> dict[str, Any]:
    if candidate is None:
        return _expected_live_evidence_binding()
    reviewed = deepcopy(candidate)
    if reviewed.get("binding_mode") == LIVE_PROVIDER_EVIDENCE_STATUS_BINDING:
        return reviewed
    provider = reviewed.get("provider_evidence", {})
    outline = reviewed.get("split_event_audit_outline", {})
    return {
        "binding_mode": "LIVE_PROVIDER_CANDIDATE_BINDING",
        "raw_provider_payload_present": isinstance(reviewed.get("provider_raw_response"), dict),
        "reviewed_candidate_kind": reviewed.get("artifact_kind"),
        "reviewed_candidate_status": reviewed.get("candidate_status"),
        "reviewed_candidate_semantic_digest": reviewed.get("split_event_audit_candidate_semantic_digest"),
        "reviewed_provider_request_mode": reviewed.get("provider_request_mode"),
        "reviewed_provider_endpoint": provider.get("provider_endpoint") if isinstance(provider, dict) else None,
        "reviewed_provider_response_status": provider.get("provider_response_status") if isinstance(provider, dict) else None,
        "reviewed_provider_response_page_count": provider.get("provider_response_page_count") if isinstance(provider, dict) else None,
        "reviewed_provider_raw_row_count": provider.get("provider_raw_response_row_count") if isinstance(provider, dict) else None,
        "reviewed_raw_response_digest": reviewed.get("split_event_provider_raw_response_digest"),
        "reviewed_timeline_digest": reviewed.get("split_event_timeline_semantic_digest"),
        "reviewed_receipt_digest": reviewed.get("split_event_audit_receipt_digest"),
        "reviewed_audit_status": outline.get("audit_status") if isinstance(outline, dict) else None,
        "event_counts": {field: outline.get(field) for field in EVENT_COUNT_FIELDS} if isinstance(outline, dict) else {},
        "identity_segment_frozen_digest": reviewed.get("identity_segment_frozen_digest"),
        "exchange_calendar_frozen_digest": reviewed.get("exchange_calendar_frozen_digest"),
        "schedule_semantic_digest": reviewed.get("schedule_semantic_digest"),
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
        _check("candidate_kind_is_split_event_audit_candidate", split.ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE, binding.get("reviewed_candidate_kind")),
        _check("candidate_status_provider_evidence_bound", split.SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND, binding.get("reviewed_candidate_status")),
        _check("candidate_digest_matches_recorded_live_evidence", EXPECTED_LIVE_CANDIDATE_SEMANTIC_DIGEST, binding.get("reviewed_candidate_semantic_digest")),
        _check("provider_request_mode_is_live", split.LIVE_PROVIDER_REQUEST, binding.get("reviewed_provider_request_mode")),
        _check("provider_response_status_ok", EXPECTED_PROVIDER_RESPONSE_STATUS, binding.get("reviewed_provider_response_status")),
        _check("provider_raw_row_count_zero", EXPECTED_PROVIDER_RAW_ROW_COUNT, binding.get("reviewed_provider_raw_row_count")),
        _check("raw_response_digest_matches", EXPECTED_LIVE_RAW_RESPONSE_DIGEST, binding.get("reviewed_raw_response_digest")),
        _check("timeline_digest_matches", EXPECTED_LIVE_TIMELINE_DIGEST, binding.get("reviewed_timeline_digest")),
        _check("receipt_digest_matches", EXPECTED_LIVE_RECEIPT_DIGEST, binding.get("reviewed_receipt_digest")),
        _check("audit_status_supports_no_in_range_split", EXPECTED_AUDIT_STATUS, binding.get("reviewed_audit_status")),
        _check("event_count_total_zero", 0, event_counts.get("split_event_count_total") if isinstance(event_counts, dict) else None),
        _check("event_count_pre_range_zero", 0, event_counts.get("split_event_count_pre_range") if isinstance(event_counts, dict) else None),
        _check("event_count_in_range_zero", 0, event_counts.get("split_event_count_in_range") if isinstance(event_counts, dict) else None),
        _check("event_count_post_range_zero", 0, event_counts.get("split_event_count_post_range") if isinstance(event_counts, dict) else None),
        _check("event_count_unknown_zero", 0, event_counts.get("split_event_count_unknown") if isinstance(event_counts, dict) else None),
        _check("identity_frozen_digest_matches", split.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, binding.get("identity_segment_frozen_digest")),
        _check("calendar_frozen_digest_matches", split.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, binding.get("exchange_calendar_frozen_digest")),
        _check("schedule_digest_matches", split.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, binding.get("schedule_semantic_digest")),
        _check("scaffold_digest_matches", split.PREVIOUS_SPLIT_EVENT_AUDIT_SCAFFOLD_DIGEST, binding.get("previous_scaffold_candidate_digest")),
        _check("segment_ticker_matches", split.FIXED_IDENTITY_SEGMENT["ticker"], segment.get("ticker") if isinstance(segment, dict) else None),
        _check("segment_composite_figi_matches", split.FIXED_IDENTITY_SEGMENT["composite_figi"], segment.get("composite_figi") if isinstance(segment, dict) else None),
        _check("segment_share_class_figi_matches", split.FIXED_IDENTITY_SEGMENT["share_class_figi"], segment.get("share_class_figi") if isinstance(segment, dict) else None),
        _check("segment_primary_mic_matches", split.FIXED_IDENTITY_SEGMENT["primary_mic"], segment.get("primary_mic") if isinstance(segment, dict) else None),
        _check("segment_security_type_matches", split.FIXED_IDENTITY_SEGMENT["security_type"], segment.get("security_type") if isinstance(segment, dict) else None),
        _check("segment_start_matches", split.FIXED_IDENTITY_SEGMENT["segment_start"], segment.get("segment_start") if isinstance(segment, dict) else None),
        _check("segment_end_matches", split.FIXED_IDENTITY_SEGMENT["segment_end"], segment.get("segment_end") if isinstance(segment, dict) else None),
        _check("contract_digest_matches", split.EXPECTED_ACQUISITION_CONTRACT_DIGEST, acquisition.get("contract_digest") if isinstance(acquisition, dict) else None),
        _check("split_event_audit_frozen_false", False, package_context.get("split_event_audit_frozen")),
        _check("dividend_event_audit_frozen_false", False, boundary.get("dividend_event_audit_frozen") if isinstance(boundary, dict) else None),
        _check("canonical_eligibility_false", False, package_context.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, package_context.get("registry_eligibility")),
        _check("acquisition_generation_freeze_false", False, package_context.get("acquisition_generation_freeze")),
        _check("strategy_runtime_migration_false", False, package_context.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, package_context.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", split.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, package_context.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", split.PROFITABILITY_NOT_ACCEPTED, package_context.get("profitability"), severity=INFO),
        _check("provider_requests_made_in_review_false", False, package_context.get("provider_requests_made_in_review")),
        _check("no_api_key_stored", False, _contains_secret_marker({"binding": binding, "package_context": package_context}), severity=HIGH),
        _check(
            "no_split_audit_frozen_artifact_created",
            {"artifact_kind_is_not_frozen": True, "review_status_is_not_frozen": True, "freeze_status_is_null": True},
            {
                "artifact_kind_is_not_frozen": package_context.get("artifact_kind") != SPLIT_EVENT_AUDIT_FROZEN,
                "review_status_is_not_frozen": package_context.get("review_status") != SPLIT_EVENT_AUDIT_FROZEN,
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
    payload.pop("split_event_review_package_semantic_digest", None)
    payload.pop("split_event_review_package_payload_digest", None)
    return payload


def split_event_review_package_semantic_digest(review_package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the split-event review package."""
    return semantic_digest(_package_digest_payload(review_package))


def build_split_event_audit_candidate_review_package_v1(candidate: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a digest-bound offline operator-review package for split-event evidence."""
    binding = _binding_from_candidate(candidate)
    package_context = {
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE,
        "review_status": SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY,
        "freeze_status": None,
        "split_event_audit_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": split.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": split.PROFITABILITY_NOT_ACCEPTED,
        "provider_requests_made_in_review": False,
    }
    checklist = _build_checklist(binding, package_context)
    package: dict[str, Any] = {
        **package_context,
        "schema_version": SCHEMA_VERSION_SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_V1,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "dividend_event_audit_frozen": False,
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
    package["split_event_review_package_semantic_digest"] = split_event_review_package_semantic_digest(package)
    return package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key in {"artifact_kind", "review_status", "reviewed_candidate_kind", "reviewed_candidate_status", "candidate_status", "freeze_status"}:
            if value == SPLIT_EVENT_AUDIT_FROZEN:
                raise SplitEventOperatorReviewError(f"{current_path} must not emit SPLIT_EVENT_AUDIT_FROZEN")
        if key in FORBIDDEN_FREEZE_FIELDS and value is not None:
            raise SplitEventOperatorReviewError(f"{current_path} must be null")
        if key == "freeze_status" and value is not None:
            raise SplitEventOperatorReviewError(f"{current_path} must be null")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise SplitEventOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise SplitEventOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise SplitEventOperatorReviewError(f"{field_name} must be true")


def validate_split_event_audit_candidate_review_package_v1(review_package: dict[str, Any]) -> dict[str, Any]:
    """Validate a split-event review package and fail closed on failed checks."""
    if not isinstance(review_package, dict):
        raise SplitEventOperatorReviewError("split-event review package must be a JSON object")
    _reject_forbidden_values(review_package)
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY, "review_status")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    _expect_true(review_package.get("created_offline"), "created_offline")
    _expect_false(review_package.get("provider_requests_made_in_review"), "provider_requests_made_in_review")
    _expect_false(review_package.get("split_event_audit_frozen"), "split_event_audit_frozen")
    _expect_false(review_package.get("dividend_event_audit_frozen"), "dividend_event_audit_frozen")
    _expect_true(review_package.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(review_package.get("calendar_operator_frozen"), "calendar_operator_frozen")
    for field in ("canonical_eligibility", "registry_eligibility", "acquisition_generation_freeze", "strategy_runtime_migration", "automatic_stitching"):
        _expect_false(review_package.get(field), field)
    _expect(review_package.get("predictive_usefulness"), split.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), split.PROFITABILITY_NOT_ACCEPTED, "profitability")

    binding = review_package.get("live_evidence_binding")
    if not isinstance(binding, dict):
        raise SplitEventOperatorReviewError("live_evidence_binding must be a JSON object")
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
    ):
        _expect(review_package.get(field), binding.get(field), field)
    _expect(review_package.get("event_counts"), EXPECTED_EVENT_COUNTS, "event_counts")
    _expect(review_package.get("authority_boundary"), _authority_boundary(), "authority_boundary")

    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise SplitEventOperatorReviewError("review_checklist must be a list")
    check_ids = [item.get("check_id") for item in checklist if isinstance(item, dict)]
    _expect(check_ids, REQUIRED_CHECK_IDS, "review_checklist check IDs")
    package_context = {
        "artifact_kind": review_package.get("artifact_kind"),
        "review_status": review_package.get("review_status"),
        "freeze_status": review_package.get("freeze_status"),
        "split_event_audit_frozen": review_package.get("split_event_audit_frozen"),
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
        raise SplitEventOperatorReviewError("split-event review package contains failed checks")

    expected_summary = _summary(checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    summary = review_package["review_summary"]
    _expect_true(summary.get("ready_for_operator_assessment"), "ready_for_operator_assessment")
    _expect_true(summary.get("operator_decision_required_before_freeze"), "operator_decision_required_before_freeze")
    _expect_false(summary.get("software_freeze_authorized"), "software_freeze_authorized")
    _expect(review_package.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")

    controls = review_package.get("operator_freeze_controls")
    if not isinstance(controls, dict):
        raise SplitEventOperatorReviewError("operator_freeze_controls must be a JSON object")
    for field in ("operator_approved_by", "operator_freeze_timestamp", "operator_freeze_digest", "operator_signature", "freeze_status"):
        _expect(controls.get(field), None, f"operator_freeze_controls.{field}")

    digest = split_event_review_package_semantic_digest(review_package)
    _expect(review_package.get("split_event_review_package_semantic_digest"), digest, "split_event_review_package_semantic_digest")
    return {
        "status": "SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE,
        "review_status": SPLIT_EVENT_AUDIT_CANDIDATE_REVIEW_PACKAGE_READY,
        "reviewed_candidate_semantic_digest": EXPECTED_LIVE_CANDIDATE_SEMANTIC_DIGEST,
        "reviewed_raw_response_digest": EXPECTED_LIVE_RAW_RESPONSE_DIGEST,
        "reviewed_timeline_digest": EXPECTED_LIVE_TIMELINE_DIGEST,
        "reviewed_receipt_digest": EXPECTED_LIVE_RECEIPT_DIGEST,
        "split_event_review_package_semantic_digest": digest,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "provider_requests_made_in_review": False,
        "split_event_audit_frozen": False,
        "software_freeze_authorized": False,
        **EXPECTED_EVENT_COUNTS,
        "audit_status": EXPECTED_AUDIT_STATUS,
    }


def write_split_event_audit_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the split-event review package JSON artifact without overwriting output."""
    review_package = build_split_event_audit_candidate_review_package_v1(candidate)
    validation = validate_split_event_audit_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_split_event_audit_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise SplitEventOperatorReviewError("split-event review package filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise SplitEventOperatorReviewError("split-event review package output already exists")
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "split_event_review_package_payload_digest": sha256_bytes(payload),
    }


def build_split_event_audit_candidate_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Build a compact Markdown view of a validated split-event review package."""
    validation = validate_split_event_audit_candidate_review_package_v1(review_package)
    binding = review_package["live_evidence_binding"]
    segment = binding["identity_segment"]
    boundary = review_package["authority_boundary"]
    counts = review_package["event_counts"]
    failed_checks = [item for item in review_package["review_checklist"] if item["status"] != PASS]
    lines = [
        "# Split-Event Audit Candidate Review Package v1",
        "",
        "## Reviewed Split-Event Candidate",
        f"- Artifact kind: `{review_package['reviewed_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_candidate_status']}`",
        f"- Candidate semantic digest: `{review_package['reviewed_candidate_semantic_digest']}`",
        f"- Review package digest: `{validation['split_event_review_package_semantic_digest']}`",
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
        "## Frozen Identity / Calendar Bindings",
        f"- Ticker: `{segment['ticker']}`",
        f"- Composite FIGI: `{segment['composite_figi']}`",
        f"- Share Class FIGI: `{segment['share_class_figi']}`",
        f"- Primary MIC: `{segment['primary_mic']}`",
        f"- Security type: `{segment['security_type']}`",
        f"- Range: `{segment['segment_start']}` through `{segment['segment_end']}`",
        f"- Identity frozen digest: `{binding['identity_segment_frozen_digest']}`",
        f"- Calendar frozen digest: `{binding['exchange_calendar_frozen_digest']}`",
        f"- Schedule digest: `{binding['schedule_semantic_digest']}`",
        "",
        "## Event Counts",
        f"- Total: `{counts['split_event_count_total']}`",
        f"- Pre-range: `{counts['split_event_count_pre_range']}`",
        f"- In-range: `{counts['split_event_count_in_range']}`",
        f"- Post-range: `{counts['split_event_count_post_range']}`",
        f"- Unknown: `{counts['split_event_count_unknown']}`",
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
            "- No `SPLIT_EVENT_AUDIT_FROZEN` artifact or status is created.",
            "- `split_event_audit_frozen` remains `false`.",
            "- Operator decision remains required before any future split-event freeze ceremony.",
            "- No canonical, registry, acquisition-generation, Strategy, runtime, broker, or execution approval is created.",
            "- Predictive usefulness and profitability remain not accepted.",
        ]
    )
    return "\n".join(lines) + "\n"
