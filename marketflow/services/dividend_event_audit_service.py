"""Dividend-event audit candidate contracts."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import split_event_audit_service as split


ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE = "DIVIDEND_EVENT_AUDIT_CANDIDATE"
SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_CANDIDATE_V1 = "dividend_event_audit_candidate_v1"
DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE = "DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"
DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND = "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND"
DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION = "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION"
DIVIDEND_EVENT_OPERATOR_REVIEW_PACKAGE = "DIVIDEND_EVENT_OPERATOR_REVIEW_PACKAGE"
DIVIDEND_EVENT_LIVE_PROVIDER_COLLECTION_DISABLED = "DIVIDEND_EVENT_LIVE_PROVIDER_COLLECTION_DISABLED"
DIVIDEND_EVENT_LIVE_PROVIDER_API_KEY_MISSING = "DIVIDEND_EVENT_LIVE_PROVIDER_API_KEY_MISSING"
MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT = "MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT"

PROVIDER_EVIDENCE_STATUS_NOT_BOUND = "NOT_BOUND"
PROVIDER_EVIDENCE_STATUS_BOUND = "BOUND"
PROVIDER_NAME_MASSIVE = "MASSIVE.COM"
PROVIDER_ENDPOINT_MASSIVE_DIVIDENDS = "/stocks/v1/dividends"
PROVIDER_ENDPOINT_STABILITY_MASSIVE_STOCKS_V1 = "CURRENT_STOCKS_V1_DIVIDENDS"
PROVIDER_QUERY_LIMITATION_TICKER_ONLY = "PROVIDER_ENDPOINT_QUERIES_TICKER_AND_RETAINS_COMPOSITE_FIGI_BINDING"
LIVE_PROVIDER_REQUEST = "LIVE_PROVIDER_REQUEST"
PROVIDER_RESPONSE_INJECTION = "PROVIDER_RESPONSE_INJECTION"
PREDICTIVE_USEFULNESS_NOT_ACCEPTED = "not accepted"
PROFITABILITY_NOT_ACCEPTED = "not accepted"
SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT = "SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT"
DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND = "DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND"
DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND = "DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND"
DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE = "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE"
PRE_RANGE = "PRE_RANGE"
IN_RANGE = "IN_RANGE"
POST_RANGE = "POST_RANGE"
UNKNOWN = "UNKNOWN"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST = split.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST
EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST = split.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST
EXPECTED_SCHEDULE_SEMANTIC_DIGEST = split.EXPECTED_SCHEDULE_SEMANTIC_DIGEST
EXPECTED_ACQUISITION_CONTRACT_DIGEST = split.EXPECTED_ACQUISITION_CONTRACT_DIGEST
EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST = "9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae"
EXPECTED_SPLIT_EVENT_AUDIT_STATUS = SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT
PREVIOUS_DIVIDEND_EVENT_AUDIT_SCAFFOLD_DIGEST = "9f50358696a79496bc14f7c526553072f3026b5df28c1d94e65da4c88791a4c0"

DIVIDEND_EVENT_COUNT_FIELDS = [
    "dividend_event_count_total",
    "dividend_event_count_pre_range",
    "dividend_event_count_in_range",
    "dividend_event_count_post_range",
    "dividend_event_count_unknown",
]

PROVIDER_ARTIFACT_FIELDS = [
    "provider_endpoint",
    "provider_query_identifier",
    "raw_response_artifact_id",
    "raw_response_semantic_digest",
    "event_timeline_artifact_id",
    "event_timeline_semantic_digest",
    "audit_receipt_artifact_id",
]

EXPECTED_DIVIDEND_EVENT_FIELDS = [
    "ex_dividend_date",
    "declaration_date",
    "record_date",
    "pay_date",
    "cash_amount",
    "split_adjusted_cash_amount",
    "historical_adjustment_factor",
    "currency",
    "frequency",
    "distribution_type",
    "dividend_type_if_available",
    "ticker",
    "composite_figi_if_available",
    "raw_event_index",
    "raw_event_digest",
    "event_position",
]

TIMELINE_EVENT_FIELDS = set(EXPECTED_DIVIDEND_EVENT_FIELDS)
VALID_EVENT_POSITIONS = [PRE_RANGE, IN_RANGE, POST_RANGE, UNKNOWN]
VALID_EVENT_POSITION_SET = set(VALID_EVENT_POSITIONS)
VALID_PROVIDER_BOUND_AUDIT_STATUSES = {
    DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND,
    DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND,
    DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE,
}

PROVIDER_EVIDENCE_FIELDS = {
    "provider_name",
    "provider_endpoint",
    "provider_endpoint_stability",
    "provider_query_identifier",
    "provider_query_ticker",
    "provider_query_composite_figi",
    "provider_query_start",
    "provider_query_end",
    "provider_request_timestamp_utc",
    "provider_response_artifact_id",
    "provider_raw_response_digest",
    "provider_raw_response_row_count",
    "provider_response_status",
    "provider_response_page_count",
    "provider_request_mode",
    "provider_response_injected",
    "provider_requests_made",
}

REQUIRED_CHECK_IDS = [
    "identity_segment_frozen_digest_bound",
    "calendar_frozen_digest_bound",
    "schedule_digest_bound",
    "split_event_audit_frozen_digest_bound",
    "split_event_audit_status_bound",
    "contract_digest_bound",
    "segment_fields_bound",
    "created_offline_true",
    "provider_requests_made_false",
    "provider_evidence_required_true",
    "provider_evidence_not_bound",
    "dividend_event_audit_not_complete",
    "dividend_event_audit_not_frozen",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "acquisition_generation_freeze_false",
    "strategy_runtime_migration_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
]

FIXED_IDENTITY_SEGMENT = deepcopy(split.FIXED_IDENTITY_SEGMENT)
FIXED_ACQUISITION_CONTRACT = deepcopy(split.FIXED_ACQUISITION_CONTRACT)

FIXED_AUTHORITY_BINDINGS = {
    "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
    "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
    "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
    "split_event_audit_frozen_digest": EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
    "split_event_audit_status": EXPECTED_SPLIT_EVENT_AUDIT_STATUS,
    "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
}

REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_AUDIT_SCAFFOLD = [
    "Dividend-event provider evidence collection.",
    "Dividend-event audit candidate with bound provider evidence.",
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

REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_PROVIDER_EVIDENCE = [
    "Dividend-event live evidence smoke.",
    "Dividend-event operator review package.",
    "Dividend-event operator freeze ceremony.",
    "Full 2022-2025 acquisition generation.",
]


class DividendEventAuditError(ValueError):
    """Raised when a dividend-event audit candidate violates guardrails."""


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
        "message": message or ("dividend-event scaffold evidence matches" if status == PASS else "dividend-event scaffold evidence mismatch"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise DividendEventAuditError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise DividendEventAuditError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise DividendEventAuditError(f"{field_name} must be true")


def _source_evidence_status() -> dict[str, Any]:
    return {
        "provider_evidence_required": True,
        "provider_evidence_status": PROVIDER_EVIDENCE_STATUS_NOT_BOUND,
        "provider_request_performed_in_this_task": False,
        "provider_endpoint": None,
        "provider_query_identifier": None,
        "raw_response_artifact_id": None,
        "raw_response_semantic_digest": None,
        "event_timeline_artifact_id": None,
        "event_timeline_semantic_digest": None,
        "audit_receipt_artifact_id": None,
    }


def _dividend_event_audit_outline() -> dict[str, Any]:
    return {
        "dividend_event_count_total": None,
        "dividend_event_count_pre_range": None,
        "dividend_event_count_in_range": None,
        "dividend_event_count_post_range": None,
        "dividend_event_count_unknown": None,
        "dividend_events": [],
        "audit_status": None,
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
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
    }


def _guardrails() -> dict[str, Any]:
    return {
        "binding_mode": "DIVIDEND_EVENT_AUDIT_SCAFFOLD_ONLY",
        "provider_requests_made": False,
        "provider_evidence_bound": False,
        "dividend_event_audit_complete": False,
        "dividend_event_audit_frozen": False,
        "raw_source_evidence_copied": False,
        "raw_source_evidence_rewritten": False,
        "acquisition_generation_created": False,
        "canonical_dataset_created": False,
        "registry_approval_created": False,
        "software_auto_approval": False,
    }


def _provider_bound_guardrails(*, provider_requests_made: bool, provider_response_injected: bool) -> dict[str, Any]:
    return {
        "binding_mode": DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "provider_requests_made": provider_requests_made,
        "provider_response_injected": provider_response_injected,
        "provider_evidence_bound": True,
        "dividend_event_audit_complete": True,
        "dividend_event_audit_frozen": False,
        "raw_source_evidence_copied": False,
        "raw_source_evidence_rewritten": False,
        "acquisition_generation_created": False,
        "canonical_dataset_created": False,
        "registry_approval_created": False,
        "software_auto_approval": False,
    }


def _build_checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    source_status = candidate.get("source_evidence_status", {})
    return [
        _check("identity_segment_frozen_digest_bound", EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, candidate.get("identity_segment_frozen_digest")),
        _check("calendar_frozen_digest_bound", EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, candidate.get("exchange_calendar_frozen_digest")),
        _check("schedule_digest_bound", EXPECTED_SCHEDULE_SEMANTIC_DIGEST, candidate.get("schedule_semantic_digest")),
        _check("split_event_audit_frozen_digest_bound", EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, candidate.get("split_event_audit_frozen_digest")),
        _check("split_event_audit_status_bound", EXPECTED_SPLIT_EVENT_AUDIT_STATUS, candidate.get("split_event_audit_status")),
        _check("contract_digest_bound", EXPECTED_ACQUISITION_CONTRACT_DIGEST, candidate.get("acquisition_contract_digest")),
        _check("segment_fields_bound", FIXED_IDENTITY_SEGMENT, candidate.get("identity_segment")),
        _check("created_offline_true", True, candidate.get("created_offline")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("provider_evidence_required_true", True, source_status.get("provider_evidence_required") if isinstance(source_status, dict) else None),
        _check("provider_evidence_not_bound", _source_evidence_status(), source_status),
        _check("dividend_event_audit_not_complete", False, candidate.get("dividend_event_audit_complete")),
        _check("dividend_event_audit_not_frozen", False, candidate.get("dividend_event_audit_frozen")),
        _check("canonical_eligibility_false", False, candidate.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, candidate.get("registry_eligibility")),
        _check("acquisition_generation_freeze_false", False, candidate.get("acquisition_generation_freeze")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("predictive_usefulness_not_accepted", PREDICTIVE_USEFULNESS_NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("profitability_not_accepted", PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
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
        "ready_for_provider_evidence_collection": failed == 0,
        "dividend_event_audit_complete": False,
        "dividend_event_audit_frozen": False,
        "software_auto_approval": False,
    }


def _candidate_digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("dividend_event_audit_candidate_semantic_digest", None)
    payload.pop("dividend_event_audit_candidate_payload_digest", None)
    return payload


def dividend_event_audit_candidate_semantic_digest(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a dividend-event audit candidate."""
    return semantic_digest(_candidate_digest_payload(candidate))


def _decode_provider_response(provider_response_data: Mapping[str, Any] | bytes) -> dict[str, Any]:
    if isinstance(provider_response_data, bytes):
        try:
            payload = json.loads(provider_response_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DividendEventAuditError("provider response injection must be UTF-8 JSON") from exc
    elif isinstance(provider_response_data, Mapping):
        payload = deepcopy(dict(provider_response_data))
    else:
        raise DividendEventAuditError("provider response injection must be a mapping or JSON bytes")
    if not isinstance(payload, dict):
        raise DividendEventAuditError("provider response injection must decode to a JSON object")
    return _deterministic_json_value(payload)


def _deterministic_json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _deterministic_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_deterministic_json_value(item) for item in value]
    if isinstance(value, tuple):
        return [_deterministic_json_value(item) for item in value]
    if isinstance(value, float):
        return format(value, ".15g")
    return value


def _first_present(mapping: Mapping[str, Any], field_names: tuple[str, ...]) -> Any:
    for field_name in field_names:
        if field_name in mapping:
            return mapping[field_name]
    return None


def _extract_dividend_event_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    candidates: list[Any] = []
    if "results" in payload:
        candidates.append(payload["results"])
        if isinstance(payload["results"], Mapping):
            candidates.extend(payload["results"].get(name) for name in ("events", "dividends"))
    candidates.extend(payload.get(name) for name in ("events", "dividends"))
    for candidate in candidates:
        if isinstance(candidate, list):
            if not all(isinstance(item, dict) for item in candidate):
                raise DividendEventAuditError("dividend event provider rows must be JSON objects")
            return [deepcopy(item) for item in candidate]
    raise DividendEventAuditError("provider response must include a dividend event array")


def _optional_iso_date(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    if type(value) is not str:
        raise DividendEventAuditError(f"{field_name} must be an ISO date or null")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        return None


def _event_position(ex_dividend_date: str | None) -> str:
    if ex_dividend_date is None:
        return UNKNOWN
    event_date = date.fromisoformat(ex_dividend_date)
    range_start = date.fromisoformat(FIXED_IDENTITY_SEGMENT["segment_start"])
    range_end = date.fromisoformat(FIXED_IDENTITY_SEGMENT["segment_end"])
    if event_date < range_start:
        return PRE_RANGE
    if event_date > range_end:
        return POST_RANGE
    return IN_RANGE


def _normalize_dividend_event(row: Mapping[str, Any], raw_event_index: int) -> dict[str, Any]:
    ex_dividend_date = _optional_iso_date(
        _first_present(row, ("ex_dividend_date", "exDividendDate", "ex_date", "exDate", "date")),
        "ex_dividend_date",
    )
    event = {
        "ex_dividend_date": ex_dividend_date,
        "declaration_date": _optional_iso_date(_first_present(row, ("declaration_date", "declarationDate")), "declaration_date"),
        "record_date": _optional_iso_date(_first_present(row, ("record_date", "recordDate")), "record_date"),
        "pay_date": _optional_iso_date(_first_present(row, ("pay_date", "payDate", "payment_date", "paymentDate", "payable_date")), "pay_date"),
        "cash_amount": _first_present(row, ("cash_amount", "cashAmount", "amount")),
        "split_adjusted_cash_amount": _first_present(row, ("split_adjusted_cash_amount", "splitAdjustedCashAmount")),
        "historical_adjustment_factor": _first_present(row, ("historical_adjustment_factor", "historicalAdjustmentFactor")),
        "currency": _first_present(row, ("currency",)),
        "frequency": _first_present(row, ("frequency",)),
        "distribution_type": _first_present(row, ("distribution_type", "distributionType")),
        "dividend_type_if_available": _first_present(row, ("dividend_type_if_available", "dividend_type", "dividendType")),
        "ticker": _first_present(row, ("ticker", "symbol")),
        "composite_figi_if_available": _first_present(row, ("composite_figi", "compositeFigi", "composite_figi_if_available")),
        "raw_event_index": raw_event_index,
        "raw_event_digest": semantic_digest(row),
        "event_position": _event_position(ex_dividend_date),
    }
    _expect(set(event), TIMELINE_EVENT_FIELDS, "dividend event fields")
    return event


def _build_dividend_event_timeline(raw_events: list[dict[str, Any]]) -> dict[str, Any]:
    events = [_normalize_dividend_event(row, index) for index, row in enumerate(raw_events)]
    ordered = sorted(
        events,
        key=lambda item: (
            item["ex_dividend_date"] or "",
            item["event_position"],
            item["raw_event_digest"],
            item["raw_event_index"],
        ),
    )
    counts = {
        "dividend_event_count_total": len(ordered),
        "dividend_event_count_pre_range": sum(1 for item in ordered if item["event_position"] == PRE_RANGE),
        "dividend_event_count_in_range": sum(1 for item in ordered if item["event_position"] == IN_RANGE),
        "dividend_event_count_post_range": sum(1 for item in ordered if item["event_position"] == POST_RANGE),
        "dividend_event_count_unknown": sum(1 for item in ordered if item["event_position"] == UNKNOWN),
    }
    base = {
        "schema_version": "dividend_event_timeline_v1",
        "identity_segment": deepcopy(FIXED_IDENTITY_SEGMENT),
        "authority_bindings": deepcopy(FIXED_AUTHORITY_BINDINGS),
        "events": ordered,
        **counts,
    }
    return base | {"dividend_event_timeline_semantic_digest": semantic_digest(base)}


def _audit_status_from_counts(counts: Mapping[str, int]) -> str:
    if counts["dividend_event_count_unknown"] > 0:
        return DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE
    if counts["dividend_event_count_in_range"] > 0:
        return DIVIDEND_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_DIVIDEND
    return DIVIDEND_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_DIVIDEND


def _artifact_id(prefix: str, digest: str) -> str:
    return f"div-art-{prefix}-{digest[:24]}"


def _provider_bound_source_evidence_status(
    provider_evidence: Mapping[str, Any],
    timeline: Mapping[str, Any],
    receipt: Mapping[str, Any],
    *,
    provider_requests_made: bool,
    provider_response_injected: bool,
) -> dict[str, Any]:
    return {
        "provider_evidence_required": True,
        "provider_evidence_status": PROVIDER_EVIDENCE_STATUS_BOUND,
        "provider_request_performed_in_this_task": provider_requests_made,
        "provider_response_injected": provider_response_injected,
        "provider_request_mode": provider_evidence["provider_request_mode"],
        "provider_endpoint": provider_evidence["provider_endpoint"],
        "provider_query_identifier": provider_evidence["provider_query_identifier"],
        "raw_response_artifact_id": provider_evidence["provider_response_artifact_id"],
        "raw_response_semantic_digest": provider_evidence["provider_raw_response_digest"],
        "event_timeline_artifact_id": timeline["event_timeline_artifact_id"],
        "event_timeline_semantic_digest": timeline["dividend_event_timeline_semantic_digest"],
        "audit_receipt_artifact_id": receipt["audit_receipt_artifact_id"],
    }


def _provider_evidence_from_raw(
    raw_response: Mapping[str, Any],
    *,
    raw_artifact_id: str,
    raw_digest: str,
    raw_event_count: int,
    provider_requests_made: bool,
    provider_response_injected: bool,
    provider_request_mode: str,
    provider_request_timestamp_utc: str | None,
) -> dict[str, Any]:
    evidence = {
        "provider_name": PROVIDER_NAME_MASSIVE,
        "provider_endpoint": raw_response.get("provider_endpoint") or PROVIDER_ENDPOINT_MASSIVE_DIVIDENDS,
        "provider_endpoint_stability": raw_response.get("provider_endpoint_stability") or PROVIDER_ENDPOINT_STABILITY_MASSIVE_STOCKS_V1,
        "provider_query_identifier": raw_response.get("provider_query_identifier") or FIXED_IDENTITY_SEGMENT["ticker"],
        "provider_query_ticker": FIXED_IDENTITY_SEGMENT["ticker"],
        "provider_query_composite_figi": FIXED_IDENTITY_SEGMENT["composite_figi"],
        "provider_query_start": FIXED_IDENTITY_SEGMENT["segment_start"],
        "provider_query_end": FIXED_IDENTITY_SEGMENT["segment_end"],
        "provider_request_timestamp_utc": raw_response.get("provider_request_timestamp_utc") or provider_request_timestamp_utc,
        "provider_response_artifact_id": raw_artifact_id,
        "provider_raw_response_digest": raw_digest,
        "provider_raw_response_row_count": raw_response.get("provider_raw_response_row_count", raw_event_count),
        "provider_response_status": raw_response.get("provider_response_status") or (raw_response.get("status") if isinstance(raw_response.get("status"), str) else None),
        "provider_response_page_count": raw_response.get("provider_response_page_count", 1),
        "provider_request_mode": provider_request_mode,
        "provider_response_injected": provider_response_injected,
        "provider_requests_made": provider_requests_made,
        "provider_query_limitation": PROVIDER_QUERY_LIMITATION_TICKER_ONLY,
    }
    if "request" in raw_response and isinstance(raw_response["request"], Mapping):
        evidence["provider_request_metadata"] = deepcopy(dict(raw_response["request"]))
    return evidence


def _build_provider_bound_candidate(
    raw_response: Mapping[str, Any],
    *,
    provider_requests_made: bool,
    provider_response_injected: bool,
    provider_request_mode: str,
    provider_request_timestamp_utc: str | None,
    include_raw_response: bool,
) -> dict[str, Any]:
    raw_response_payload = _deterministic_json_value(deepcopy(dict(raw_response)))
    raw_events = _extract_dividend_event_rows(raw_response_payload)
    raw_digest = raw_response_payload.get("provider_raw_response_digest")
    if not isinstance(raw_digest, str):
        raw_digest = semantic_digest(raw_response_payload)
    raw_artifact_id = _artifact_id("raw-response", raw_digest)
    timeline = _build_dividend_event_timeline(raw_events)
    timeline["event_timeline_artifact_id"] = _artifact_id("timeline", timeline["dividend_event_timeline_semantic_digest"])
    counts = {field: int(timeline[field]) for field in DIVIDEND_EVENT_COUNT_FIELDS}
    audit_status = _audit_status_from_counts(counts)
    provider_evidence = _provider_evidence_from_raw(
        raw_response_payload,
        raw_artifact_id=raw_artifact_id,
        raw_digest=raw_digest,
        raw_event_count=len(raw_events),
        provider_requests_made=provider_requests_made,
        provider_response_injected=provider_response_injected,
        provider_request_mode=provider_request_mode,
        provider_request_timestamp_utc=provider_request_timestamp_utc,
    )
    receipt_base = {
        "schema_version": "dividend_event_audit_receipt_v1",
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE,
        "candidate_status": DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "previous_scaffold_digest": PREVIOUS_DIVIDEND_EVENT_AUDIT_SCAFFOLD_DIGEST,
        "provider_requests_made": provider_requests_made,
        "provider_response_injected": provider_response_injected,
        "provider_request_mode": provider_request_mode,
        "dividend_events_provider_evidence_bound": True,
        "dividend_event_audit_complete": True,
        "dividend_event_audit_frozen": False,
        "provider_evidence": provider_evidence,
        "dividend_event_provider_raw_response_digest": raw_digest,
        "dividend_event_timeline_semantic_digest": timeline["dividend_event_timeline_semantic_digest"],
        "audit_status": audit_status,
        **counts,
    }
    receipt_digest = semantic_digest(receipt_base)
    receipt = receipt_base | {
        "audit_receipt_artifact_id": _artifact_id("receipt", receipt_digest),
        "dividend_event_audit_receipt_digest": receipt_digest,
    }
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE,
        "schema_version": SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_CANDIDATE_V1,
        "candidate_status": DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "created_offline": False,
        "provider_requests_made": provider_requests_made,
        "provider_response_injected": provider_response_injected,
        "provider_request_mode": provider_request_mode,
        "dividend_events_provider_evidence_bound": True,
        "dividend_event_audit_complete": True,
        "dividend_event_audit_frozen": False,
        "operator_review_required": True,
        "operator_freeze_required": True,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "split_event_audit_status": EXPECTED_SPLIT_EVENT_AUDIT_STATUS,
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "previous_scaffold_candidate_digest": PREVIOUS_DIVIDEND_EVENT_AUDIT_SCAFFOLD_DIGEST,
        "identity_segment": deepcopy(FIXED_IDENTITY_SEGMENT),
        "authority_bindings": deepcopy(FIXED_AUTHORITY_BINDINGS),
        "acquisition_contract": deepcopy(FIXED_ACQUISITION_CONTRACT),
        "provider_evidence": provider_evidence,
        "source_evidence_status": _provider_bound_source_evidence_status(
            provider_evidence,
            timeline,
            receipt,
            provider_requests_made=provider_requests_made,
            provider_response_injected=provider_response_injected,
        ),
        "dividend_event_timeline": timeline,
        "dividend_event_audit_outline": {
            **counts,
            "dividend_events": deepcopy(timeline["events"]),
            "audit_status": audit_status,
        },
        "dividend_event_audit_receipt": receipt,
        "raw_response_artifact_id": raw_artifact_id,
        "event_timeline_artifact_id": timeline["event_timeline_artifact_id"],
        "audit_receipt_artifact_id": receipt["audit_receipt_artifact_id"],
        "dividend_event_provider_raw_response_digest": raw_digest,
        "dividend_event_timeline_semantic_digest": timeline["dividend_event_timeline_semantic_digest"],
        "dividend_event_audit_receipt_digest": receipt_digest,
        "authority_boundary": _authority_boundary(),
        "guardrails": _provider_bound_guardrails(provider_requests_made=provider_requests_made, provider_response_injected=provider_response_injected),
        "next_required_task": DIVIDEND_EVENT_OPERATOR_REVIEW_PACKAGE,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_PROVIDER_EVIDENCE),
    }
    if include_raw_response:
        candidate["provider_raw_response"] = raw_response_payload
    candidate["dividend_event_audit_candidate_semantic_digest"] = dividend_event_audit_candidate_semantic_digest(candidate)
    validate_dividend_event_audit_candidate_v1(candidate)
    return candidate


def build_dividend_event_audit_provider_bound_candidate_v1(
    provider_response_data: Mapping[str, Any] | bytes,
    *,
    provider_request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Build a provider-bound dividend candidate from injected response data."""
    raw_response = _decode_provider_response(provider_response_data)
    return _build_provider_bound_candidate(
        raw_response,
        provider_requests_made=False,
        provider_response_injected=True,
        provider_request_mode=PROVIDER_RESPONSE_INJECTION,
        provider_request_timestamp_utc=provider_request_timestamp_utc,
        include_raw_response=False,
    )


def _api_key_from_environment() -> str | None:
    return os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")


def build_dividend_event_audit_candidate_from_live_provider_v1(
    *,
    api_key: str | None = None,
    transport: Any | None = None,
    request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Build a provider-bound dividend candidate from an explicitly gated live request."""
    if os.environ.get(MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT) != "1":
        return {
            "status": DIVIDEND_EVENT_LIVE_PROVIDER_COLLECTION_DISABLED,
            "provider_requests_made": False,
            "provider_response_injected": False,
            "required_environment_variable": MARKETFLOW_ENABLE_LIVE_DIVIDEND_AUDIT,
            "dividend_event_audit_frozen": False,
        }
    resolved_api_key = api_key or _api_key_from_environment()
    if resolved_api_key is None:
        return {
            "status": DIVIDEND_EVENT_LIVE_PROVIDER_API_KEY_MISSING,
            "provider_requests_made": False,
            "provider_response_injected": False,
            "accepted_environment_variables": ["MASSIVE_API_KEY", "POLYGON_API_KEY"],
            "dividend_event_audit_frozen": False,
        }
    from marketflow.services.dividend_event_provider_adapter_service import fetch_massive_dividend_events_v1

    raw_response = fetch_massive_dividend_events_v1(
        ticker=FIXED_IDENTITY_SEGMENT["ticker"],
        start_date=FIXED_IDENTITY_SEGMENT["segment_start"],
        end_date=FIXED_IDENTITY_SEGMENT["segment_end"],
        api_key=resolved_api_key,
        transport=transport,
        request_timestamp_utc=request_timestamp_utc,
    )
    return _build_provider_bound_candidate(
        raw_response,
        provider_requests_made=True,
        provider_response_injected=False,
        provider_request_mode=LIVE_PROVIDER_REQUEST,
        provider_request_timestamp_utc=request_timestamp_utc,
        include_raw_response=True,
    )


def build_dividend_event_audit_candidate_v1() -> dict[str, Any]:
    """Build the offline dividend-event audit scaffold without binding provider evidence."""
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE,
        "schema_version": SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_CANDIDATE_V1,
        "candidate_status": DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE,
        "created_offline": True,
        "provider_requests_made": False,
        "dividend_events_provider_evidence_bound": False,
        "dividend_event_audit_complete": False,
        "dividend_event_audit_frozen": False,
        "operator_review_required": True,
        "operator_freeze_required": True,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "split_event_audit_status": EXPECTED_SPLIT_EVENT_AUDIT_STATUS,
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "identity_segment": deepcopy(FIXED_IDENTITY_SEGMENT),
        "authority_bindings": deepcopy(FIXED_AUTHORITY_BINDINGS),
        "acquisition_contract": deepcopy(FIXED_ACQUISITION_CONTRACT),
        "source_evidence_status": _source_evidence_status(),
        "dividend_event_audit_outline": _dividend_event_audit_outline(),
        "expected_future_normalized_dividend_event_fields": list(EXPECTED_DIVIDEND_EVENT_FIELDS),
        "valid_event_positions": list(VALID_EVENT_POSITIONS),
        "authority_boundary": _authority_boundary(),
        "guardrails": _guardrails(),
        "next_required_task": DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_AUDIT_SCAFFOLD),
    }
    checklist = _build_checklist(candidate)
    candidate["scaffold_checklist"] = checklist
    candidate["scaffold_summary"] = _summary(checklist)
    candidate["dividend_event_audit_candidate_semantic_digest"] = dividend_event_audit_candidate_semantic_digest(candidate)
    validate_dividend_event_audit_candidate_v1(candidate)
    return candidate


def _validate_source_evidence_status(status: Any) -> None:
    if not isinstance(status, dict):
        raise DividendEventAuditError("source_evidence_status must be a JSON object")
    _expect(status, _source_evidence_status(), "source_evidence_status")
    _expect_true(status.get("provider_evidence_required"), "source_evidence_status.provider_evidence_required")
    _expect(status.get("provider_evidence_status"), PROVIDER_EVIDENCE_STATUS_NOT_BOUND, "source_evidence_status.provider_evidence_status")
    _expect_false(status.get("provider_request_performed_in_this_task"), "source_evidence_status.provider_request_performed_in_this_task")
    for field in PROVIDER_ARTIFACT_FIELDS:
        _expect(status.get(field), None, f"source_evidence_status.{field}")


def _validate_dividend_event_outline(outline: Any) -> None:
    if not isinstance(outline, dict):
        raise DividendEventAuditError("dividend_event_audit_outline must be a JSON object")
    for field in DIVIDEND_EVENT_COUNT_FIELDS:
        _expect(outline.get(field), None, f"dividend_event_audit_outline.{field}")
    _expect(outline.get("dividend_events"), [], "dividend_event_audit_outline.dividend_events")
    _expect(outline.get("audit_status"), None, "dividend_event_audit_outline.audit_status")


def _validate_common_authority_boundary(candidate: dict[str, Any]) -> None:
    _expect_true(candidate.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(candidate.get("calendar_operator_frozen"), "calendar_operator_frozen")
    _expect_true(candidate.get("split_event_audit_frozen"), "split_event_audit_frozen")
    for field in (
        "canonical_eligibility",
        "registry_eligibility",
        "acquisition_generation_freeze",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(candidate.get(field), field)
    _expect(candidate.get("predictive_usefulness"), PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(candidate.get("identity_segment_frozen_digest"), EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, "identity_segment_frozen_digest")
    _expect(candidate.get("exchange_calendar_frozen_digest"), EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, "exchange_calendar_frozen_digest")
    _expect(candidate.get("schedule_semantic_digest"), EXPECTED_SCHEDULE_SEMANTIC_DIGEST, "schedule_semantic_digest")
    _expect(candidate.get("split_event_audit_frozen_digest"), EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, "split_event_audit_frozen_digest")
    _expect(candidate.get("split_event_audit_status"), EXPECTED_SPLIT_EVENT_AUDIT_STATUS, "split_event_audit_status")
    _expect(candidate.get("acquisition_contract_digest"), EXPECTED_ACQUISITION_CONTRACT_DIGEST, "acquisition_contract_digest")
    _expect(candidate.get("identity_segment"), FIXED_IDENTITY_SEGMENT, "identity_segment")
    _expect(candidate.get("authority_bindings"), FIXED_AUTHORITY_BINDINGS, "authority_bindings")
    _expect(candidate.get("acquisition_contract"), FIXED_ACQUISITION_CONTRACT, "acquisition_contract")
    _expect(candidate.get("authority_boundary"), _authority_boundary(), "authority_boundary")


def _expect_hex_digest(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise DividendEventAuditError(f"{field_name} missing")
    return value


def _expect_nonnegative_int(value: Any, field_name: str) -> int:
    if type(value) is not int or value < 0:
        raise DividendEventAuditError(f"{field_name} must be a nonnegative integer")
    return value


def _validate_provider_bound_source_evidence_status(
    status: Any,
    *,
    provider_requests_made: bool,
    provider_response_injected: bool,
    provider_request_mode: str,
) -> None:
    if not isinstance(status, dict):
        raise DividendEventAuditError("source_evidence_status must be a JSON object")
    _expect_true(status.get("provider_evidence_required"), "source_evidence_status.provider_evidence_required")
    _expect(status.get("provider_evidence_status"), PROVIDER_EVIDENCE_STATUS_BOUND, "source_evidence_status.provider_evidence_status")
    _expect(status.get("provider_request_performed_in_this_task"), provider_requests_made, "source_evidence_status.provider_request_performed_in_this_task")
    _expect(status.get("provider_response_injected"), provider_response_injected, "source_evidence_status.provider_response_injected")
    _expect(status.get("provider_request_mode"), provider_request_mode, "source_evidence_status.provider_request_mode")
    for field in (
        "provider_endpoint",
        "provider_query_identifier",
        "raw_response_artifact_id",
        "raw_response_semantic_digest",
        "event_timeline_artifact_id",
        "event_timeline_semantic_digest",
        "audit_receipt_artifact_id",
    ):
        value = status.get(field)
        if not isinstance(value, str) or not value:
            raise DividendEventAuditError(f"source_evidence_status.{field} missing")


def _validate_provider_bound_counts(outline: Mapping[str, Any]) -> dict[str, int]:
    counts = {field: _expect_nonnegative_int(outline.get(field), f"dividend_event_audit_outline.{field}") for field in DIVIDEND_EVENT_COUNT_FIELDS}
    total = (
        counts["dividend_event_count_pre_range"]
        + counts["dividend_event_count_in_range"]
        + counts["dividend_event_count_post_range"]
        + counts["dividend_event_count_unknown"]
    )
    if counts["dividend_event_count_total"] != total:
        raise DividendEventAuditError("dividend event count totals inconsistent")
    return counts


def _validate_provider_bound_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    _expect_false(candidate.get("created_offline"), "created_offline")
    provider_requests_made = candidate.get("provider_requests_made")
    provider_response_injected = candidate.get("provider_response_injected")
    provider_request_mode = candidate.get("provider_request_mode")
    if provider_requests_made is True:
        _expect_false(provider_response_injected, "provider_response_injected")
        _expect(provider_request_mode, LIVE_PROVIDER_REQUEST, "provider_request_mode")
    elif provider_requests_made is False:
        _expect_true(provider_response_injected, "provider_response_injected")
        _expect(provider_request_mode, PROVIDER_RESPONSE_INJECTION, "provider_request_mode")
    else:
        raise DividendEventAuditError("provider_requests_made must be boolean")
    _expect_true(candidate.get("dividend_events_provider_evidence_bound"), "dividend_events_provider_evidence_bound")
    _expect_true(candidate.get("dividend_event_audit_complete"), "dividend_event_audit_complete")
    _expect_false(candidate.get("dividend_event_audit_frozen"), "dividend_event_audit_frozen")
    _expect_true(candidate.get("operator_review_required"), "operator_review_required")
    _expect_true(candidate.get("operator_freeze_required"), "operator_freeze_required")
    _validate_common_authority_boundary(candidate)
    _expect(candidate.get("previous_scaffold_candidate_digest"), PREVIOUS_DIVIDEND_EVENT_AUDIT_SCAFFOLD_DIGEST, "previous_scaffold_candidate_digest")

    provider_evidence = candidate.get("provider_evidence")
    if not isinstance(provider_evidence, dict):
        raise DividendEventAuditError("provider_evidence must be a JSON object")
    if not PROVIDER_EVIDENCE_FIELDS.issubset(provider_evidence):
        raise DividendEventAuditError("provider_evidence fields missing")
    _expect(provider_evidence.get("provider_name"), PROVIDER_NAME_MASSIVE, "provider_evidence.provider_name")
    _expect(provider_evidence.get("provider_endpoint"), PROVIDER_ENDPOINT_MASSIVE_DIVIDENDS, "provider_evidence.provider_endpoint")
    _expect(provider_evidence.get("provider_endpoint_stability"), PROVIDER_ENDPOINT_STABILITY_MASSIVE_STOCKS_V1, "provider_evidence.provider_endpoint_stability")
    _expect(provider_evidence.get("provider_query_identifier"), FIXED_IDENTITY_SEGMENT["ticker"], "provider_evidence.provider_query_identifier")
    _expect(provider_evidence.get("provider_query_ticker"), FIXED_IDENTITY_SEGMENT["ticker"], "provider_evidence.provider_query_ticker")
    _expect(provider_evidence.get("provider_query_composite_figi"), FIXED_IDENTITY_SEGMENT["composite_figi"], "provider_evidence.provider_query_composite_figi")
    _expect(provider_evidence.get("provider_query_start"), FIXED_IDENTITY_SEGMENT["segment_start"], "provider_evidence.provider_query_start")
    _expect(provider_evidence.get("provider_query_end"), FIXED_IDENTITY_SEGMENT["segment_end"], "provider_evidence.provider_query_end")
    _expect(provider_evidence.get("provider_request_mode"), provider_request_mode, "provider_evidence.provider_request_mode")
    _expect(provider_evidence.get("provider_response_injected"), provider_response_injected, "provider_evidence.provider_response_injected")
    _expect(provider_evidence.get("provider_requests_made"), provider_requests_made, "provider_evidence.provider_requests_made")
    if provider_requests_made is True and not provider_evidence.get("provider_request_timestamp_utc"):
        raise DividendEventAuditError("provider_evidence.provider_request_timestamp_utc missing")
    raw_digest = _expect_hex_digest(provider_evidence.get("provider_raw_response_digest"), "provider_evidence.provider_raw_response_digest")
    _expect_nonnegative_int(provider_evidence.get("provider_raw_response_row_count"), "provider_evidence.provider_raw_response_row_count")
    _expect_nonnegative_int(provider_evidence.get("provider_response_page_count"), "provider_evidence.provider_response_page_count")

    _validate_provider_bound_source_evidence_status(
        candidate.get("source_evidence_status"),
        provider_requests_made=provider_requests_made,
        provider_response_injected=provider_response_injected,
        provider_request_mode=provider_request_mode,
    )
    source_status = candidate["source_evidence_status"]
    _expect(source_status.get("raw_response_artifact_id"), provider_evidence.get("provider_response_artifact_id"), "source_evidence_status.raw_response_artifact_id")
    _expect(source_status.get("raw_response_semantic_digest"), raw_digest, "source_evidence_status.raw_response_semantic_digest")

    timeline = candidate.get("dividend_event_timeline")
    if not isinstance(timeline, dict):
        raise DividendEventAuditError("dividend_event_timeline must be a JSON object")
    timeline_digest = _expect_hex_digest(timeline.get("dividend_event_timeline_semantic_digest"), "dividend_event_timeline_semantic_digest")
    timeline_payload = dict(timeline)
    timeline_payload.pop("dividend_event_timeline_semantic_digest", None)
    timeline_payload.pop("event_timeline_artifact_id", None)
    _expect(timeline_digest, semantic_digest(timeline_payload), "dividend_event_timeline_semantic_digest")
    _expect(candidate.get("dividend_event_timeline_semantic_digest"), timeline_digest, "dividend_event_timeline_semantic_digest")

    outline = candidate.get("dividend_event_audit_outline")
    if not isinstance(outline, dict):
        raise DividendEventAuditError("dividend_event_audit_outline must be a JSON object")
    counts = _validate_provider_bound_counts(outline)
    events = outline.get("dividend_events")
    timeline_events = timeline.get("events")
    if not isinstance(events, list) or events != timeline_events:
        raise DividendEventAuditError("dividend_event_audit_outline.dividend_events mismatch")
    if counts["dividend_event_count_total"] != len(events):
        raise DividendEventAuditError("dividend event count totals inconsistent")
    for event in events:
        if not isinstance(event, dict) or set(event) != TIMELINE_EVENT_FIELDS:
            raise DividendEventAuditError("dividend event timeline event fields mismatch")
        if event["event_position"] not in VALID_EVENT_POSITION_SET:
            raise DividendEventAuditError("dividend event position mismatch")
        _expect_hex_digest(event.get("raw_event_digest"), "dividend_event.raw_event_digest")
    observed_counts = {
        "dividend_event_count_total": len(events),
        "dividend_event_count_pre_range": sum(1 for item in events if item["event_position"] == PRE_RANGE),
        "dividend_event_count_in_range": sum(1 for item in events if item["event_position"] == IN_RANGE),
        "dividend_event_count_post_range": sum(1 for item in events if item["event_position"] == POST_RANGE),
        "dividend_event_count_unknown": sum(1 for item in events if item["event_position"] == UNKNOWN),
    }
    _expect(counts, observed_counts, "dividend event counts")
    audit_status = outline.get("audit_status")
    if audit_status not in VALID_PROVIDER_BOUND_AUDIT_STATUSES:
        raise DividendEventAuditError("audit_status missing")
    _expect(audit_status, _audit_status_from_counts(counts), "audit_status")

    _expect(candidate.get("raw_response_artifact_id"), provider_evidence.get("provider_response_artifact_id"), "raw_response_artifact_id")
    _expect(candidate.get("event_timeline_artifact_id"), timeline.get("event_timeline_artifact_id"), "event_timeline_artifact_id")
    _expect(candidate.get("audit_receipt_artifact_id"), candidate.get("dividend_event_audit_receipt", {}).get("audit_receipt_artifact_id"), "audit_receipt_artifact_id")
    _expect(candidate.get("dividend_event_provider_raw_response_digest"), raw_digest, "dividend_event_provider_raw_response_digest")
    receipt = candidate.get("dividend_event_audit_receipt")
    if not isinstance(receipt, dict):
        raise DividendEventAuditError("dividend_event_audit_receipt must be a JSON object")
    receipt_digest = _expect_hex_digest(candidate.get("dividend_event_audit_receipt_digest"), "dividend_event_audit_receipt_digest")
    receipt_payload = dict(receipt)
    receipt_payload.pop("audit_receipt_artifact_id", None)
    receipt_payload.pop("dividend_event_audit_receipt_digest", None)
    _expect(receipt_digest, semantic_digest(receipt_payload), "dividend_event_audit_receipt_digest")
    _expect(receipt.get("audit_status"), audit_status, "dividend_event_audit_receipt.audit_status")

    if provider_requests_made is True:
        raw_response = candidate.get("provider_raw_response")
        if not isinstance(raw_response, dict):
            raise DividendEventAuditError("provider_raw_response must be a JSON object")
        _expect_true(raw_response.get("provider_requests_made"), "provider_raw_response.provider_requests_made")
        _expect_false(raw_response.get("provider_response_injected"), "provider_raw_response.provider_response_injected")
        _expect(raw_response.get("provider_request_mode"), LIVE_PROVIDER_REQUEST, "provider_raw_response.provider_request_mode")
        _expect(raw_response.get("provider_raw_response_digest"), raw_digest, "provider_raw_response.provider_raw_response_digest")
    _expect(candidate.get("guardrails"), _provider_bound_guardrails(provider_requests_made=provider_requests_made, provider_response_injected=provider_response_injected), "guardrails")
    _expect(candidate.get("next_required_task"), DIVIDEND_EVENT_OPERATOR_REVIEW_PACKAGE, "next_required_task")
    _expect(candidate.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_PROVIDER_EVIDENCE, "remaining_roadmap")

    digest = candidate.get("dividend_event_audit_candidate_semantic_digest")
    _expect_hex_digest(digest, "dividend_event_audit_candidate_semantic_digest")
    recomputed = dividend_event_audit_candidate_semantic_digest(candidate)
    _expect(digest, recomputed, "dividend_event_audit_candidate_semantic_digest")
    return {
        "status": "DIVIDEND_EVENT_AUDIT_CANDIDATE_VALID",
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE,
        "candidate_status": DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "dividend_event_audit_candidate_semantic_digest": recomputed,
        "dividend_event_provider_raw_response_digest": raw_digest,
        "dividend_event_timeline_semantic_digest": timeline_digest,
        "dividend_event_audit_receipt_digest": receipt_digest,
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "provider_requests_made": provider_requests_made,
        "provider_response_injected": provider_response_injected,
        "provider_request_mode": provider_request_mode,
        "provider_evidence_status": PROVIDER_EVIDENCE_STATUS_BOUND,
        "dividend_events_provider_evidence_bound": True,
        "dividend_event_audit_complete": True,
        "dividend_event_audit_frozen": False,
        "audit_status": audit_status,
        **counts,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
    }


def _validate_digest(candidate: dict[str, Any]) -> str:
    digest = candidate.get("dividend_event_audit_candidate_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise DividendEventAuditError("dividend_event_audit_candidate_semantic_digest missing")
    expected = dividend_event_audit_candidate_semantic_digest(candidate)
    _expect(digest, expected, "dividend_event_audit_candidate_semantic_digest")
    return digest


def validate_dividend_event_audit_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate dividend-event audit candidates and fail closed on premature authority claims."""
    if not isinstance(candidate, dict):
        raise DividendEventAuditError("candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_CANDIDATE_V1, "schema_version")
    if candidate.get("candidate_status") == DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND:
        return _validate_provider_bound_candidate_v1(candidate)
    _expect(candidate.get("candidate_status"), DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE, "candidate_status")
    _expect_true(candidate.get("created_offline"), "created_offline")
    _expect_false(candidate.get("provider_requests_made"), "provider_requests_made")
    _expect_false(candidate.get("dividend_events_provider_evidence_bound"), "dividend_events_provider_evidence_bound")
    _expect_false(candidate.get("dividend_event_audit_complete"), "dividend_event_audit_complete")
    _expect_false(candidate.get("dividend_event_audit_frozen"), "dividend_event_audit_frozen")
    _expect_true(candidate.get("operator_review_required"), "operator_review_required")
    _expect_true(candidate.get("operator_freeze_required"), "operator_freeze_required")
    _validate_common_authority_boundary(candidate)
    _validate_source_evidence_status(candidate.get("source_evidence_status"))
    _validate_dividend_event_outline(candidate.get("dividend_event_audit_outline"))
    _expect(candidate.get("expected_future_normalized_dividend_event_fields"), EXPECTED_DIVIDEND_EVENT_FIELDS, "expected_future_normalized_dividend_event_fields")
    _expect(candidate.get("valid_event_positions"), VALID_EVENT_POSITIONS, "valid_event_positions")
    _expect(candidate.get("guardrails"), _guardrails(), "guardrails")
    _expect(candidate.get("next_required_task"), DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION, "next_required_task")
    _expect(candidate.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_DIVIDEND_EVENT_AUDIT_SCAFFOLD, "remaining_roadmap")
    checklist = candidate.get("scaffold_checklist")
    if not isinstance(checklist, list):
        raise DividendEventAuditError("scaffold_checklist must be a list")
    _expect([item.get("check_id") for item in checklist if isinstance(item, dict)], REQUIRED_CHECK_IDS, "scaffold_checklist check ids")
    _expect(checklist, _build_checklist(candidate), "scaffold_checklist")
    _expect(candidate.get("scaffold_summary"), _summary(checklist), "scaffold_summary")
    digest = _validate_digest(candidate)
    return {
        "status": "DIVIDEND_EVENT_AUDIT_CANDIDATE_VALID",
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE,
        "candidate_status": DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE,
        "dividend_event_audit_candidate_semantic_digest": digest,
        "provider_requests_made": False,
        "dividend_events_provider_evidence_bound": False,
        "dividend_event_audit_complete": False,
        "dividend_event_audit_frozen": False,
        "ready_for_provider_evidence_collection": candidate["scaffold_summary"]["ready_for_provider_evidence_collection"],
        "total_checks": candidate["scaffold_summary"]["total_checks"],
        "passed_checks": candidate["scaffold_summary"]["passed_checks"],
        "failed_checks": candidate["scaffold_summary"]["failed_checks"],
        "blocker_count": candidate["scaffold_summary"]["blocker_count"],
    }


def write_dividend_event_audit_candidate_v1(output_dir: str | Path) -> dict[str, Any]:
    """Write the offline dividend-event audit scaffold JSON without overwriting."""
    candidate = build_dividend_event_audit_candidate_v1()
    output_path = Path(output_dir) / "dividend_event_audit_candidate_v1.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        raise DividendEventAuditError(f"dividend-event audit candidate already exists: {output_path}")
    payload = canonical_json_bytes(candidate)
    output_path.write_bytes(payload)
    return {
        "path": str(output_path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "dividend_event_audit_candidate_semantic_digest": candidate["dividend_event_audit_candidate_semantic_digest"],
        "dividend_event_audit_candidate_payload_digest": sha256_bytes(payload),
        "provider_requests_made": False,
        "dividend_event_audit_frozen": False,
    }


def build_dividend_event_audit_candidate_markdown_v1(candidate: dict[str, Any] | None = None) -> str:
    """Build a sanitized Markdown summary for a dividend candidate."""
    payload = deepcopy(candidate) if candidate is not None else build_dividend_event_audit_candidate_v1()
    validation = validate_dividend_event_audit_candidate_v1(payload)
    boundary = payload["authority_boundary"]
    source_status = payload["source_evidence_status"]
    lines = [
        "# Dividend-Event Audit Candidate v1",
        "",
        "## Candidate",
        "",
        f"- artifact kind: `{payload['artifact_kind']}`",
        f"- schema version: `{payload['schema_version']}`",
        f"- candidate status: `{payload['candidate_status']}`",
        f"- candidate semantic digest: `{validation['dividend_event_audit_candidate_semantic_digest']}`",
        f"- created offline: `{str(payload['created_offline']).lower()}`",
        f"- provider requests made: `{str(payload['provider_requests_made']).lower()}`",
        f"- dividend_event_audit_frozen: `{str(payload['dividend_event_audit_frozen']).lower()}`",
        "",
        "## Frozen Authority Bindings",
        "",
        f"- identity frozen digest: `{payload['identity_segment_frozen_digest']}`",
        f"- calendar frozen digest: `{payload['exchange_calendar_frozen_digest']}`",
        f"- schedule digest: `{payload['schedule_semantic_digest']}`",
        f"- split event audit frozen digest: `{payload['split_event_audit_frozen_digest']}`",
        f"- split event audit status: `{payload['split_event_audit_status']}`",
        f"- acquisition contract digest: `{payload['acquisition_contract_digest']}`",
        "",
        "## Provider Evidence",
        "",
        f"- provider evidence status: `{source_status['provider_evidence_status']}`",
        f"- provider request performed in this task: `{str(source_status['provider_request_performed_in_this_task']).lower()}`",
    ]
    if payload["candidate_status"] == DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND:
        outline = payload["dividend_event_audit_outline"]
        lines.extend(
            [
                f"- provider request mode: `{payload['provider_request_mode']}`",
                f"- raw response digest: `{payload['dividend_event_provider_raw_response_digest']}`",
                f"- timeline digest: `{payload['dividend_event_timeline_semantic_digest']}`",
                f"- receipt digest: `{payload['dividend_event_audit_receipt_digest']}`",
                f"- audit status: `{outline['audit_status']}`",
            ]
        )
    else:
        lines.extend(
            [
                "No provider requests were made.",
                "No dividend-event provider evidence is bound.",
                "Dividend event counts, raw response artifacts, timeline artifacts, and receipts remain unpopulated.",
            ]
        )
    lines.extend(["", "## Authority Boundary", ""])
    for key, value in boundary.items():
        rendered = str(value).lower() if isinstance(value, bool) else value
        lines.append(f"- {key}: `{rendered}`")
    lines.extend(
        [
            "",
            "## Expected Normalized Fields",
            "",
            *[f"- `{field}`" for field in EXPECTED_DIVIDEND_EVENT_FIELDS],
            "",
            "## Remaining Roadmap",
            "",
            *[f"- {item}" for item in payload["remaining_roadmap"]],
            "",
            "## Guardrails",
            "",
            "No dividend audit freeze is claimed.",
            "No canonical eligibility, registry eligibility, acquisition-generation freeze, strategy runtime migration, predictive acceptance, or profitability acceptance is claimed.",
            "",
        ]
    )
    return "\n".join(lines)
