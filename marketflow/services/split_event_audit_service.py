"""Split-event audit evidence candidate contracts."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes


ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE = "SPLIT_EVENT_AUDIT_CANDIDATE"
SCHEMA_VERSION_SPLIT_EVENT_AUDIT_CANDIDATE_V1 = "split_event_audit_candidate_v1"
SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE = "SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"
SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND = "SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND"
SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION = "SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION"
SPLIT_EVENT_OPERATOR_REVIEW_PACKAGE = "SPLIT_EVENT_OPERATOR_REVIEW_PACKAGE"

EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST = "25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6"
EXPECTED_SCHEDULE_SEMANTIC_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
EXPECTED_ACQUISITION_CONTRACT_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"
PREVIOUS_SPLIT_EVENT_AUDIT_SCAFFOLD_DIGEST = "6874936bcbc10db46f5ad084b1ada6fa1658502994a1a935472507452d09d33d"

PROVIDER_EVIDENCE_STATUS_NOT_BOUND = "NOT_BOUND"
PROVIDER_EVIDENCE_STATUS_BOUND = "BOUND"
PROVIDER_NAME_MASSIVE = "MASSIVE.COM"
PROVIDER_ENDPOINT_STABILITY_ADAPTER_REQUIRED = "SPLIT_ENDPOINT_ADAPTER_REQUIRED_NOT_LIVE_VERIFIED"
PROVIDER_ENDPOINT_LIMITATION = "NO_SAFE_EXISTING_SPLIT_EVENT_PROVIDER_ENDPOINT_ADAPTER_IN_REPOSITORY"
PREDICTIVE_USEFULNESS_NOT_ACCEPTED = "not accepted"
PROFITABILITY_NOT_ACCEPTED = "not accepted"
SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT = "SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT"
SPLIT_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_SPLIT = "SPLIT_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_SPLIT"
SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE = "SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE"
PRE_RANGE = "PRE_RANGE"
IN_RANGE = "IN_RANGE"
POST_RANGE = "POST_RANGE"
UNKNOWN = "UNKNOWN"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EVENT_COUNT_FIELDS = [
    "split_event_count_total",
    "split_event_count_pre_range",
    "split_event_count_in_range",
    "split_event_count_post_range",
]

PROVIDER_EVENT_COUNT_FIELDS = [
    "split_event_count_total",
    "split_event_count_pre_range",
    "split_event_count_in_range",
    "split_event_count_post_range",
    "split_event_count_unknown",
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

REQUIRED_CHECK_IDS = [
    "identity_segment_frozen_digest_bound",
    "calendar_frozen_digest_bound",
    "schedule_digest_bound",
    "contract_digest_bound",
    "segment_fields_bound",
    "created_offline_true",
    "provider_requests_made_false",
    "provider_evidence_required_true",
    "provider_evidence_not_bound",
    "split_event_counts_not_populated",
    "split_events_empty",
    "split_event_audit_not_complete",
    "split_event_audit_not_frozen",
    "dividend_event_audit_not_frozen",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "acquisition_generation_freeze_false",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
]

FIXED_IDENTITY_SEGMENT = {
    "ticker": "AAPL",
    "composite_figi": "BBG000B9XRY4",
    "share_class_figi": "BBG001S5N8V8",
    "primary_mic": "XNAS",
    "security_type": "CS",
    "segment_start": "2022-01-01",
    "segment_end": "2025-12-31",
}

FIXED_ACQUISITION_CONTRACT = {
    "contract": "CORE ACQUISITION CONTRACT v2.1",
    "contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
    "range_start": "2022-01-01",
    "range_end": "2025-12-31",
    "source": "Massive.com Custom Bars",
    "bar_interval": "15-minute",
    "adjusted": True,
    "ascending": True,
    "source_timestamps_are_aggregate_window_starts": True,
    "source_timezone": "America/New_York",
    "canonical_storage_timezone": "UTC",
}

FIXED_AUTHORITY_BINDINGS = {
    "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
    "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
    "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
    "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
}

REMAINING_ROADMAP_AFTER_SPLIT_EVENT_AUDIT_SCAFFOLD = [
    "Split-event provider evidence collection.",
    "Split-event audit candidate with bound provider evidence.",
    "Split-event operator review package.",
    "Split-event operator freeze ceremony.",
    "Dividend-event audit chain.",
]

REMAINING_ROADMAP_AFTER_SPLIT_EVENT_PROVIDER_EVIDENCE = [
    "Split-event operator review package.",
    "Split-event operator freeze ceremony.",
    "Dividend-event audit candidate.",
]

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
}

TIMELINE_EVENT_FIELDS = {
    "execution_date",
    "declaration_date",
    "record_date",
    "payable_date",
    "split_from",
    "split_to",
    "split_ratio",
    "ticker",
    "composite_figi_if_available",
    "raw_event_index",
    "raw_event_digest",
    "event_position",
}

VALID_EVENT_POSITIONS = {PRE_RANGE, IN_RANGE, POST_RANGE, UNKNOWN}
VALID_PROVIDER_BOUND_AUDIT_STATUSES = {
    SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT,
    SPLIT_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_SPLIT,
    SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE,
}


class SplitEventAuditError(ValueError):
    """Raised when a split-event audit candidate violates scaffold guardrails."""


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
        "message": message or ("split-event scaffold evidence matches" if status == PASS else "split-event scaffold evidence mismatch"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise SplitEventAuditError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise SplitEventAuditError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise SplitEventAuditError(f"{field_name} must be true")


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


def _split_event_audit_outline() -> dict[str, Any]:
    return {
        "split_event_count_total": None,
        "split_event_count_pre_range": None,
        "split_event_count_in_range": None,
        "split_event_count_post_range": None,
        "split_events": [],
        "audit_status": None,
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
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
    }


def _guardrails() -> dict[str, Any]:
    return {
        "binding_mode": "SPLIT_EVENT_AUDIT_SCAFFOLD_ONLY",
        "provider_requests_made": False,
        "provider_evidence_bound": False,
        "split_event_audit_complete": False,
        "split_event_audit_frozen": False,
        "raw_source_evidence_copied": False,
        "raw_source_evidence_rewritten": False,
        "acquisition_generation_created": False,
        "canonical_dataset_created": False,
        "registry_approval_created": False,
        "software_auto_approval": False,
    }


def _provider_bound_guardrails(*, provider_requests_made: bool, provider_response_injected: bool) -> dict[str, Any]:
    return {
        "binding_mode": SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "provider_requests_made": provider_requests_made,
        "provider_response_injected": provider_response_injected,
        "provider_evidence_bound": True,
        "split_event_audit_complete": True,
        "split_event_audit_frozen": False,
        "raw_source_evidence_copied": False,
        "raw_source_evidence_rewritten": False,
        "acquisition_generation_created": False,
        "canonical_dataset_created": False,
        "registry_approval_created": False,
        "software_auto_approval": False,
    }


def _build_checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    authority = candidate.get("authority_boundary", {})
    source_status = candidate.get("source_evidence_status", {})
    outline = candidate.get("split_event_audit_outline", {})
    return [
        _check("identity_segment_frozen_digest_bound", EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, candidate.get("identity_segment_frozen_digest")),
        _check("calendar_frozen_digest_bound", EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, candidate.get("exchange_calendar_frozen_digest")),
        _check("schedule_digest_bound", EXPECTED_SCHEDULE_SEMANTIC_DIGEST, candidate.get("schedule_semantic_digest")),
        _check("contract_digest_bound", EXPECTED_ACQUISITION_CONTRACT_DIGEST, candidate.get("acquisition_contract_digest")),
        _check("segment_fields_bound", FIXED_IDENTITY_SEGMENT, candidate.get("identity_segment")),
        _check("created_offline_true", True, candidate.get("created_offline")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("provider_evidence_required_true", True, source_status.get("provider_evidence_required") if isinstance(source_status, dict) else None),
        _check("provider_evidence_not_bound", _source_evidence_status(), source_status),
        _check(
            "split_event_counts_not_populated",
            {field: None for field in EVENT_COUNT_FIELDS},
            {field: outline.get(field) for field in EVENT_COUNT_FIELDS} if isinstance(outline, dict) else {},
        ),
        _check("split_events_empty", [], outline.get("split_events") if isinstance(outline, dict) else None),
        _check("split_event_audit_not_complete", False, candidate.get("split_event_audit_complete")),
        _check("split_event_audit_not_frozen", False, candidate.get("split_event_audit_frozen")),
        _check("dividend_event_audit_not_frozen", False, authority.get("dividend_event_audit_frozen") if isinstance(authority, dict) else None),
        _check("canonical_eligibility_false", False, candidate.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, candidate.get("registry_eligibility")),
        _check("acquisition_generation_freeze_false", False, candidate.get("acquisition_generation_freeze")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
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
        "split_event_audit_complete": False,
        "split_event_audit_frozen": False,
        "software_auto_approval": False,
    }


def _candidate_digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("split_event_audit_candidate_semantic_digest", None)
    payload.pop("split_event_audit_candidate_payload_digest", None)
    return payload


def split_event_audit_candidate_semantic_digest(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a split-event audit candidate scaffold."""
    return semantic_digest(_candidate_digest_payload(candidate))


def _decode_injected_provider_response(provider_response_data: Mapping[str, Any] | bytes) -> dict[str, Any]:
    if isinstance(provider_response_data, bytes):
        try:
            payload = json.loads(provider_response_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SplitEventAuditError("provider response injection must be UTF-8 JSON") from exc
    elif isinstance(provider_response_data, Mapping):
        payload = deepcopy(dict(provider_response_data))
    else:
        raise SplitEventAuditError("provider response injection must be a mapping or JSON bytes")
    if not isinstance(payload, dict):
        raise SplitEventAuditError("provider response injection must decode to a JSON object")
    return payload


def _first_present(mapping: Mapping[str, Any], field_names: tuple[str, ...]) -> Any:
    for field_name in field_names:
        if field_name in mapping:
            return mapping[field_name]
    return None


def _extract_split_event_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    candidates: list[Any] = []
    if "results" in payload:
        candidates.append(payload["results"])
        if isinstance(payload["results"], Mapping):
            candidates.extend(payload["results"].get(name) for name in ("events", "splits"))
    candidates.extend(payload.get(name) for name in ("events", "splits"))
    for candidate in candidates:
        if isinstance(candidate, list):
            if not all(isinstance(item, dict) for item in candidate):
                raise SplitEventAuditError("split event provider rows must be JSON objects")
            return [deepcopy(item) for item in candidate]
    raise SplitEventAuditError("provider response injection must include a split event array")


def _optional_iso_date(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    if type(value) is not str:
        raise SplitEventAuditError(f"{field_name} must be an ISO date or null")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise SplitEventAuditError(f"{field_name} must be an ISO date or null") from exc


def _event_position(execution_date: str | None) -> str:
    if execution_date is None:
        return UNKNOWN
    event_date = date.fromisoformat(execution_date)
    range_start = date.fromisoformat(FIXED_IDENTITY_SEGMENT["segment_start"])
    range_end = date.fromisoformat(FIXED_IDENTITY_SEGMENT["segment_end"])
    if event_date < range_start:
        return PRE_RANGE
    if event_date > range_end:
        return POST_RANGE
    return IN_RANGE


def _normalize_split_ratio(split_from: Any, split_to: Any, supplied_ratio: Any) -> Any:
    if supplied_ratio is not None:
        return supplied_ratio
    if type(split_from) in {int, str} and type(split_to) in {int, str} and str(split_from) and str(split_to):
        return f"{split_to}:{split_from}"
    return None


def _normalize_split_event(row: Mapping[str, Any], raw_event_index: int) -> dict[str, Any]:
    execution_date = _optional_iso_date(
        _first_present(row, ("execution_date", "executionDate", "ex_date", "exDate", "date")),
        "execution_date",
    )
    declaration_date = _optional_iso_date(_first_present(row, ("declaration_date", "declarationDate")), "declaration_date")
    record_date = _optional_iso_date(_first_present(row, ("record_date", "recordDate")), "record_date")
    payable_date = _optional_iso_date(_first_present(row, ("payable_date", "payableDate", "payment_date", "paymentDate")), "payable_date")
    split_from = _first_present(row, ("split_from", "splitFrom", "from_factor", "fromFactor", "from"))
    split_to = _first_present(row, ("split_to", "splitTo", "to_factor", "toFactor", "to"))
    event = {
        "execution_date": execution_date,
        "declaration_date": declaration_date,
        "record_date": record_date,
        "payable_date": payable_date,
        "split_from": split_from,
        "split_to": split_to,
        "split_ratio": _normalize_split_ratio(split_from, split_to, _first_present(row, ("split_ratio", "splitRatio", "ratio"))),
        "ticker": _first_present(row, ("ticker", "symbol")),
        "composite_figi_if_available": _first_present(row, ("composite_figi", "compositeFigi", "composite_figi_if_available")),
        "raw_event_index": raw_event_index,
        "raw_event_digest": semantic_digest(row),
        "event_position": _event_position(execution_date),
    }
    _expect(set(event), TIMELINE_EVENT_FIELDS, "split event fields")
    return event


def _build_split_event_timeline(raw_events: list[dict[str, Any]]) -> dict[str, Any]:
    events = [_normalize_split_event(row, index) for index, row in enumerate(raw_events)]
    ordered = sorted(
        events,
        key=lambda item: (
            item["execution_date"] or "",
            item["event_position"],
            item["raw_event_digest"],
            item["raw_event_index"],
        ),
    )
    counts = {
        "split_event_count_total": len(ordered),
        "split_event_count_pre_range": sum(1 for item in ordered if item["event_position"] == PRE_RANGE),
        "split_event_count_in_range": sum(1 for item in ordered if item["event_position"] == IN_RANGE),
        "split_event_count_post_range": sum(1 for item in ordered if item["event_position"] == POST_RANGE),
        "split_event_count_unknown": sum(1 for item in ordered if item["event_position"] == UNKNOWN),
    }
    base = {
        "schema_version": "split_event_timeline_v1",
        "identity_segment": deepcopy(FIXED_IDENTITY_SEGMENT),
        "authority_bindings": deepcopy(FIXED_AUTHORITY_BINDINGS),
        "events": ordered,
        **counts,
    }
    return base | {"split_event_timeline_semantic_digest": semantic_digest(base)}


def _audit_status_from_counts(counts: Mapping[str, int]) -> str:
    if counts["split_event_count_unknown"] > 0:
        return SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_INCOMPLETE
    if counts["split_event_count_in_range"] > 0:
        return SPLIT_EVENT_AUDIT_FOUND_REPORTED_IN_RANGE_SPLIT
    return SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT


def _artifact_id(prefix: str, digest: str) -> str:
    return f"split-art-{prefix}-{digest[:24]}"


def _provider_bound_source_evidence_status(provider_evidence: Mapping[str, Any], timeline: Mapping[str, Any], receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "provider_evidence_required": True,
        "provider_evidence_status": PROVIDER_EVIDENCE_STATUS_BOUND,
        "provider_request_performed_in_this_task": False,
        "provider_response_injected": True,
        "provider_endpoint": provider_evidence["provider_endpoint"],
        "provider_query_identifier": provider_evidence["provider_query_identifier"],
        "raw_response_artifact_id": provider_evidence["provider_response_artifact_id"],
        "raw_response_semantic_digest": provider_evidence["provider_raw_response_digest"],
        "event_timeline_artifact_id": timeline["event_timeline_artifact_id"],
        "event_timeline_semantic_digest": timeline["split_event_timeline_semantic_digest"],
        "audit_receipt_artifact_id": receipt["audit_receipt_artifact_id"],
    }


def build_split_event_audit_provider_bound_candidate_v1(
    provider_response_data: Mapping[str, Any] | bytes,
    *,
    provider_name: str = PROVIDER_NAME_MASSIVE,
    provider_endpoint: str | None = None,
    provider_endpoint_stability: str = PROVIDER_ENDPOINT_STABILITY_ADAPTER_REQUIRED,
    provider_query_identifier: str = FIXED_IDENTITY_SEGMENT["ticker"],
    provider_request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Build a split-event audit candidate from injected provider response data.

    This path intentionally performs no live provider request. It binds supplied
    provider response data for deterministic validation while leaving endpoint
    adapter work explicit.
    """
    raw_response = _decode_injected_provider_response(provider_response_data)
    raw_events = _extract_split_event_rows(raw_response)
    raw_digest = semantic_digest(raw_response)
    raw_artifact_id = _artifact_id("raw-response", raw_digest)
    timeline = _build_split_event_timeline(raw_events)
    timeline["event_timeline_artifact_id"] = _artifact_id("timeline", timeline["split_event_timeline_semantic_digest"])
    counts = {field: int(timeline[field]) for field in PROVIDER_EVENT_COUNT_FIELDS}
    audit_status = _audit_status_from_counts(counts)
    provider_evidence = {
        "provider_name": provider_name,
        "provider_endpoint": provider_endpoint,
        "provider_endpoint_stability": provider_endpoint_stability,
        "provider_query_identifier": provider_query_identifier,
        "provider_query_ticker": FIXED_IDENTITY_SEGMENT["ticker"],
        "provider_query_composite_figi": FIXED_IDENTITY_SEGMENT["composite_figi"],
        "provider_query_start": FIXED_IDENTITY_SEGMENT["segment_start"],
        "provider_query_end": FIXED_IDENTITY_SEGMENT["segment_end"],
        "provider_request_timestamp_utc": provider_request_timestamp_utc,
        "provider_response_artifact_id": raw_artifact_id,
        "provider_raw_response_digest": raw_digest,
        "provider_raw_response_row_count": len(raw_events),
        "provider_response_status": raw_response.get("status") if isinstance(raw_response.get("status"), str) else None,
        "provider_endpoint_limitation": PROVIDER_ENDPOINT_LIMITATION if provider_endpoint is None else None,
    }
    receipt_base = {
        "schema_version": "split_event_audit_receipt_v1",
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE,
        "candidate_status": SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "previous_scaffold_digest": PREVIOUS_SPLIT_EVENT_AUDIT_SCAFFOLD_DIGEST,
        "provider_requests_made": False,
        "provider_response_injected": True,
        "split_events_provider_evidence_bound": True,
        "split_event_audit_complete": True,
        "split_event_audit_frozen": False,
        "provider_evidence": provider_evidence,
        "split_event_provider_raw_response_digest": raw_digest,
        "split_event_timeline_semantic_digest": timeline["split_event_timeline_semantic_digest"],
        "audit_status": audit_status,
        **counts,
    }
    receipt_digest = semantic_digest(receipt_base)
    receipt = receipt_base | {
        "audit_receipt_artifact_id": _artifact_id("receipt", receipt_digest),
        "split_event_audit_receipt_digest": receipt_digest,
    }
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE,
        "schema_version": SCHEMA_VERSION_SPLIT_EVENT_AUDIT_CANDIDATE_V1,
        "candidate_status": SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "created_offline": False,
        "provider_requests_made": False,
        "provider_response_injected": True,
        "split_events_provider_evidence_bound": True,
        "split_event_audit_complete": True,
        "split_event_audit_frozen": False,
        "operator_review_required": True,
        "operator_freeze_required": True,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
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
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "previous_scaffold_candidate_digest": PREVIOUS_SPLIT_EVENT_AUDIT_SCAFFOLD_DIGEST,
        "identity_segment": deepcopy(FIXED_IDENTITY_SEGMENT),
        "authority_bindings": deepcopy(FIXED_AUTHORITY_BINDINGS),
        "acquisition_contract": deepcopy(FIXED_ACQUISITION_CONTRACT),
        "provider_evidence": provider_evidence,
        "source_evidence_status": _provider_bound_source_evidence_status(provider_evidence, timeline, receipt),
        "split_event_timeline": timeline,
        "split_event_audit_outline": {
            **counts,
            "split_events": deepcopy(timeline["events"]),
            "audit_status": audit_status,
        },
        "split_event_audit_receipt": receipt,
        "raw_response_artifact_id": raw_artifact_id,
        "event_timeline_artifact_id": timeline["event_timeline_artifact_id"],
        "audit_receipt_artifact_id": receipt["audit_receipt_artifact_id"],
        "split_event_provider_raw_response_digest": raw_digest,
        "split_event_timeline_semantic_digest": timeline["split_event_timeline_semantic_digest"],
        "split_event_audit_receipt_digest": receipt_digest,
        "authority_boundary": _authority_boundary(),
        "guardrails": _provider_bound_guardrails(provider_requests_made=False, provider_response_injected=True),
        "next_required_task": SPLIT_EVENT_OPERATOR_REVIEW_PACKAGE,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_SPLIT_EVENT_PROVIDER_EVIDENCE),
    }
    candidate["split_event_audit_candidate_semantic_digest"] = split_event_audit_candidate_semantic_digest(candidate)
    validate_split_event_audit_candidate_v1(candidate)
    return candidate


def build_split_event_audit_candidate_v1() -> dict[str, Any]:
    """Build the offline split-event audit scaffold without binding provider evidence."""
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE,
        "schema_version": SCHEMA_VERSION_SPLIT_EVENT_AUDIT_CANDIDATE_V1,
        "candidate_status": SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE,
        "created_offline": True,
        "provider_requests_made": False,
        "split_events_provider_evidence_bound": False,
        "split_event_audit_complete": False,
        "split_event_audit_frozen": False,
        "operator_review_required": True,
        "operator_freeze_required": True,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
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
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "identity_segment": deepcopy(FIXED_IDENTITY_SEGMENT),
        "authority_bindings": deepcopy(FIXED_AUTHORITY_BINDINGS),
        "acquisition_contract": deepcopy(FIXED_ACQUISITION_CONTRACT),
        "source_evidence_status": _source_evidence_status(),
        "split_event_audit_outline": _split_event_audit_outline(),
        "authority_boundary": _authority_boundary(),
        "guardrails": _guardrails(),
        "next_required_task": SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_SPLIT_EVENT_AUDIT_SCAFFOLD),
    }
    checklist = _build_checklist(candidate)
    candidate["scaffold_checklist"] = checklist
    candidate["scaffold_summary"] = _summary(checklist)
    candidate["split_event_audit_candidate_semantic_digest"] = split_event_audit_candidate_semantic_digest(candidate)
    validate_split_event_audit_candidate_v1(candidate)
    return candidate


def _validate_source_evidence_status(status: Any) -> None:
    if not isinstance(status, dict):
        raise SplitEventAuditError("source_evidence_status must be a JSON object")
    _expect(status, _source_evidence_status(), "source_evidence_status")
    _expect_true(status.get("provider_evidence_required"), "source_evidence_status.provider_evidence_required")
    _expect(status.get("provider_evidence_status"), PROVIDER_EVIDENCE_STATUS_NOT_BOUND, "source_evidence_status.provider_evidence_status")
    _expect_false(status.get("provider_request_performed_in_this_task"), "source_evidence_status.provider_request_performed_in_this_task")
    for field in PROVIDER_ARTIFACT_FIELDS:
        _expect(status.get(field), None, f"source_evidence_status.{field}")


def _validate_split_event_outline(outline: Any) -> None:
    if not isinstance(outline, dict):
        raise SplitEventAuditError("split_event_audit_outline must be a JSON object")
    for field in EVENT_COUNT_FIELDS:
        _expect(outline.get(field), None, f"split_event_audit_outline.{field}")
    _expect(outline.get("split_events"), [], "split_event_audit_outline.split_events")
    _expect(outline.get("audit_status"), None, "split_event_audit_outline.audit_status")


def _validate_provider_bound_source_evidence_status(status: Any) -> None:
    if not isinstance(status, dict):
        raise SplitEventAuditError("source_evidence_status must be a JSON object")
    _expect_true(status.get("provider_evidence_required"), "source_evidence_status.provider_evidence_required")
    _expect(status.get("provider_evidence_status"), PROVIDER_EVIDENCE_STATUS_BOUND, "source_evidence_status.provider_evidence_status")
    _expect_false(status.get("provider_request_performed_in_this_task"), "source_evidence_status.provider_request_performed_in_this_task")
    _expect_true(status.get("provider_response_injected"), "source_evidence_status.provider_response_injected")
    for field in (
        "raw_response_artifact_id",
        "raw_response_semantic_digest",
        "event_timeline_artifact_id",
        "event_timeline_semantic_digest",
        "audit_receipt_artifact_id",
    ):
        value = status.get(field)
        if not isinstance(value, str) or not value:
            raise SplitEventAuditError(f"source_evidence_status.{field} missing")


def _expect_hex_digest(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise SplitEventAuditError(f"{field_name} missing")
    return value


def _expect_nonnegative_int(value: Any, field_name: str) -> int:
    if type(value) is not int or value < 0:
        raise SplitEventAuditError(f"{field_name} must be a nonnegative integer")
    return value


def _validate_common_authority_boundary(candidate: dict[str, Any]) -> None:
    _expect_true(candidate.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(candidate.get("calendar_operator_frozen"), "calendar_operator_frozen")
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
    _expect(candidate.get("acquisition_contract_digest"), EXPECTED_ACQUISITION_CONTRACT_DIGEST, "acquisition_contract_digest")
    _expect(candidate.get("identity_segment"), FIXED_IDENTITY_SEGMENT, "identity_segment")
    _expect(candidate.get("authority_bindings"), FIXED_AUTHORITY_BINDINGS, "authority_bindings")
    _expect(candidate.get("acquisition_contract"), FIXED_ACQUISITION_CONTRACT, "acquisition_contract")
    _expect(candidate.get("authority_boundary"), _authority_boundary(), "authority_boundary")


def _validate_provider_bound_counts(outline: Mapping[str, Any]) -> dict[str, int]:
    counts = {field: _expect_nonnegative_int(outline.get(field), f"split_event_audit_outline.{field}") for field in PROVIDER_EVENT_COUNT_FIELDS}
    total = (
        counts["split_event_count_pre_range"]
        + counts["split_event_count_in_range"]
        + counts["split_event_count_post_range"]
        + counts["split_event_count_unknown"]
    )
    if counts["split_event_count_total"] != total:
        raise SplitEventAuditError("split event count totals inconsistent")
    return counts


def _validate_provider_bound_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    _expect_false(candidate.get("provider_requests_made"), "provider_requests_made")
    _expect_true(candidate.get("provider_response_injected"), "provider_response_injected")
    _expect_true(candidate.get("split_events_provider_evidence_bound"), "split_events_provider_evidence_bound")
    _expect_true(candidate.get("split_event_audit_complete"), "split_event_audit_complete")
    _expect_false(candidate.get("split_event_audit_frozen"), "split_event_audit_frozen")
    _expect_true(candidate.get("operator_review_required"), "operator_review_required")
    _expect_true(candidate.get("operator_freeze_required"), "operator_freeze_required")
    _validate_common_authority_boundary(candidate)
    _expect(candidate.get("previous_scaffold_candidate_digest"), PREVIOUS_SPLIT_EVENT_AUDIT_SCAFFOLD_DIGEST, "previous_scaffold_candidate_digest")

    provider_evidence = candidate.get("provider_evidence")
    if not isinstance(provider_evidence, dict):
        raise SplitEventAuditError("provider_evidence must be a JSON object")
    if not PROVIDER_EVIDENCE_FIELDS.issubset(provider_evidence):
        raise SplitEventAuditError("provider_evidence fields missing")
    _expect(provider_evidence.get("provider_name"), PROVIDER_NAME_MASSIVE, "provider_evidence.provider_name")
    _expect(provider_evidence.get("provider_query_ticker"), FIXED_IDENTITY_SEGMENT["ticker"], "provider_evidence.provider_query_ticker")
    _expect(provider_evidence.get("provider_query_composite_figi"), FIXED_IDENTITY_SEGMENT["composite_figi"], "provider_evidence.provider_query_composite_figi")
    _expect(provider_evidence.get("provider_query_start"), FIXED_IDENTITY_SEGMENT["segment_start"], "provider_evidence.provider_query_start")
    _expect(provider_evidence.get("provider_query_end"), FIXED_IDENTITY_SEGMENT["segment_end"], "provider_evidence.provider_query_end")
    raw_digest = _expect_hex_digest(provider_evidence.get("provider_raw_response_digest"), "provider_evidence.provider_raw_response_digest")
    _expect_nonnegative_int(provider_evidence.get("provider_raw_response_row_count"), "provider_evidence.provider_raw_response_row_count")

    _validate_provider_bound_source_evidence_status(candidate.get("source_evidence_status"))
    source_status = candidate["source_evidence_status"]
    _expect(source_status.get("raw_response_artifact_id"), provider_evidence.get("provider_response_artifact_id"), "source_evidence_status.raw_response_artifact_id")
    _expect(source_status.get("raw_response_semantic_digest"), raw_digest, "source_evidence_status.raw_response_semantic_digest")

    timeline = candidate.get("split_event_timeline")
    if not isinstance(timeline, dict):
        raise SplitEventAuditError("split_event_timeline must be a JSON object")
    timeline_digest = _expect_hex_digest(timeline.get("split_event_timeline_semantic_digest"), "split_event_timeline_semantic_digest")
    timeline_payload = dict(timeline)
    timeline_payload.pop("split_event_timeline_semantic_digest", None)
    timeline_payload.pop("event_timeline_artifact_id", None)
    _expect(timeline_digest, semantic_digest(timeline_payload), "split_event_timeline_semantic_digest")
    _expect_hex_digest(candidate.get("split_event_timeline_semantic_digest"), "split_event_timeline_semantic_digest")
    _expect(candidate.get("split_event_timeline_semantic_digest"), timeline_digest, "split_event_timeline_semantic_digest")

    outline = candidate.get("split_event_audit_outline")
    if not isinstance(outline, dict):
        raise SplitEventAuditError("split_event_audit_outline must be a JSON object")
    counts = _validate_provider_bound_counts(outline)
    events = outline.get("split_events")
    timeline_events = timeline.get("events")
    if not isinstance(events, list) or events != timeline_events:
        raise SplitEventAuditError("split_event_audit_outline.split_events mismatch")
    if counts["split_event_count_total"] != len(events):
        raise SplitEventAuditError("split event count totals inconsistent")
    for event in events:
        if not isinstance(event, dict) or set(event) != TIMELINE_EVENT_FIELDS:
            raise SplitEventAuditError("split event timeline event fields mismatch")
        if event["event_position"] not in VALID_EVENT_POSITIONS:
            raise SplitEventAuditError("split event position mismatch")
        _expect_hex_digest(event.get("raw_event_digest"), "split_event.raw_event_digest")
    observed_counts = {
        "split_event_count_total": len(events),
        "split_event_count_pre_range": sum(1 for item in events if item["event_position"] == PRE_RANGE),
        "split_event_count_in_range": sum(1 for item in events if item["event_position"] == IN_RANGE),
        "split_event_count_post_range": sum(1 for item in events if item["event_position"] == POST_RANGE),
        "split_event_count_unknown": sum(1 for item in events if item["event_position"] == UNKNOWN),
    }
    _expect(counts, observed_counts, "split event counts")
    audit_status = outline.get("audit_status")
    if audit_status not in VALID_PROVIDER_BOUND_AUDIT_STATUSES:
        raise SplitEventAuditError("audit_status missing")
    _expect(audit_status, _audit_status_from_counts(counts), "audit_status")

    _expect(candidate.get("raw_response_artifact_id"), provider_evidence.get("provider_response_artifact_id"), "raw_response_artifact_id")
    _expect(candidate.get("event_timeline_artifact_id"), timeline.get("event_timeline_artifact_id"), "event_timeline_artifact_id")
    _expect(candidate.get("audit_receipt_artifact_id"), candidate.get("split_event_audit_receipt", {}).get("audit_receipt_artifact_id"), "audit_receipt_artifact_id")
    _expect(candidate.get("split_event_provider_raw_response_digest"), raw_digest, "split_event_provider_raw_response_digest")
    _expect_hex_digest(candidate.get("split_event_audit_receipt_digest"), "split_event_audit_receipt_digest")
    receipt = candidate.get("split_event_audit_receipt")
    if not isinstance(receipt, dict):
        raise SplitEventAuditError("split_event_audit_receipt must be a JSON object")
    receipt_payload = dict(receipt)
    receipt_payload.pop("audit_receipt_artifact_id", None)
    receipt_payload.pop("split_event_audit_receipt_digest", None)
    _expect(candidate["split_event_audit_receipt_digest"], semantic_digest(receipt_payload), "split_event_audit_receipt_digest")
    _expect(receipt.get("audit_status"), audit_status, "split_event_audit_receipt.audit_status")

    _expect(candidate.get("guardrails"), _provider_bound_guardrails(provider_requests_made=False, provider_response_injected=True), "guardrails")
    _expect(candidate.get("next_required_task"), SPLIT_EVENT_OPERATOR_REVIEW_PACKAGE, "next_required_task")
    _expect(candidate.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_SPLIT_EVENT_PROVIDER_EVIDENCE, "remaining_roadmap")

    digest = candidate.get("split_event_audit_candidate_semantic_digest")
    _expect_hex_digest(digest, "split_event_audit_candidate_semantic_digest")
    recomputed = split_event_audit_candidate_semantic_digest(candidate)
    _expect(digest, recomputed, "split_event_audit_candidate_semantic_digest")
    return {
        "status": "SPLIT_EVENT_AUDIT_CANDIDATE_VALID",
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE,
        "candidate_status": SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND,
        "split_event_audit_candidate_semantic_digest": recomputed,
        "split_event_provider_raw_response_digest": raw_digest,
        "split_event_timeline_semantic_digest": timeline_digest,
        "split_event_audit_receipt_digest": candidate["split_event_audit_receipt_digest"],
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "provider_requests_made": False,
        "provider_response_injected": True,
        "provider_evidence_status": PROVIDER_EVIDENCE_STATUS_BOUND,
        "split_events_provider_evidence_bound": True,
        "split_event_audit_complete": True,
        "split_event_audit_frozen": False,
        "audit_status": audit_status,
        **counts,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
    }


def validate_split_event_audit_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate split-event audit candidates and fail closed on premature authority claims."""
    if not isinstance(candidate, dict):
        raise SplitEventAuditError("split-event audit candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_SPLIT_EVENT_AUDIT_CANDIDATE_V1, "schema_version")
    if candidate.get("candidate_status") == SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_BOUND:
        return _validate_provider_bound_candidate_v1(candidate)
    _expect(candidate.get("candidate_status"), SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE, "candidate_status")
    _expect_true(candidate.get("created_offline"), "created_offline")
    _expect_false(candidate.get("provider_requests_made"), "provider_requests_made")
    _expect_false(candidate.get("split_events_provider_evidence_bound"), "split_events_provider_evidence_bound")
    _expect_false(candidate.get("split_event_audit_complete"), "split_event_audit_complete")
    _expect_false(candidate.get("split_event_audit_frozen"), "split_event_audit_frozen")
    _expect_true(candidate.get("operator_review_required"), "operator_review_required")
    _expect_true(candidate.get("operator_freeze_required"), "operator_freeze_required")
    _expect_true(candidate.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(candidate.get("calendar_operator_frozen"), "calendar_operator_frozen")
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
    _expect(candidate.get("acquisition_contract_digest"), EXPECTED_ACQUISITION_CONTRACT_DIGEST, "acquisition_contract_digest")
    _expect(candidate.get("identity_segment"), FIXED_IDENTITY_SEGMENT, "identity_segment")
    _expect(candidate.get("authority_bindings"), FIXED_AUTHORITY_BINDINGS, "authority_bindings")
    _expect(candidate.get("acquisition_contract"), FIXED_ACQUISITION_CONTRACT, "acquisition_contract")
    _validate_source_evidence_status(candidate.get("source_evidence_status"))
    _validate_split_event_outline(candidate.get("split_event_audit_outline"))
    _expect(candidate.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    _expect(candidate.get("guardrails"), _guardrails(), "guardrails")
    _expect(candidate.get("next_required_task"), SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION, "next_required_task")
    _expect(candidate.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_SPLIT_EVENT_AUDIT_SCAFFOLD, "remaining_roadmap")

    checklist = _build_checklist(candidate)
    _expect([item["check_id"] for item in checklist], REQUIRED_CHECK_IDS, "scaffold_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise SplitEventAuditError(f"scaffold checklist contains failed check: {failed[0]['check_id']}")
    _expect(candidate.get("scaffold_checklist"), checklist, "scaffold_checklist")
    summary = _summary(checklist)
    _expect(candidate.get("scaffold_summary"), summary, "scaffold_summary")
    _expect_true(summary.get("ready_for_provider_evidence_collection"), "ready_for_provider_evidence_collection")
    _expect_false(summary.get("split_event_audit_complete"), "scaffold_summary.split_event_audit_complete")
    _expect_false(summary.get("split_event_audit_frozen"), "scaffold_summary.split_event_audit_frozen")
    _expect_false(summary.get("software_auto_approval"), "scaffold_summary.software_auto_approval")

    digest = candidate.get("split_event_audit_candidate_semantic_digest")
    if not isinstance(digest, str) or not digest:
        raise SplitEventAuditError("split_event_audit_candidate_semantic_digest missing")
    recomputed = split_event_audit_candidate_semantic_digest(candidate)
    _expect(digest, recomputed, "split_event_audit_candidate_semantic_digest")
    return {
        "status": "SPLIT_EVENT_AUDIT_CANDIDATE_VALID",
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE,
        "candidate_status": SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE,
        "split_event_audit_candidate_semantic_digest": recomputed,
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "provider_requests_made": False,
        "provider_evidence_required": True,
        "provider_evidence_status": PROVIDER_EVIDENCE_STATUS_NOT_BOUND,
        "split_events_provider_evidence_bound": False,
        "split_event_audit_complete": False,
        "split_event_audit_frozen": False,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
    }


def write_split_event_audit_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the split-event audit scaffold JSON artifact without overwriting output."""
    candidate = build_split_event_audit_candidate_v1()
    validation = validate_split_event_audit_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_split_event_audit_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise SplitEventAuditError("split-event audit candidate filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise SplitEventAuditError("split-event audit candidate output already exists")
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "split_event_audit_candidate_payload_digest": sha256_bytes(payload),
    }


def build_split_event_audit_candidate_markdown_v1(candidate: dict[str, Any]) -> str:
    """Build a compact Markdown view of a validated split-event audit scaffold."""
    validation = validate_split_event_audit_candidate_v1(candidate)
    segment = candidate["identity_segment"]
    source_status = candidate["source_evidence_status"]
    boundary = candidate["authority_boundary"]
    lines = [
        "# Split-Event Audit Candidate v1",
        "",
        "## Scaffold Candidate",
        f"- Artifact kind: `{candidate['artifact_kind']}`",
        f"- Candidate status: `{candidate['candidate_status']}`",
        f"- Candidate digest: `{validation['split_event_audit_candidate_semantic_digest']}`",
        f"- Ticker: `{segment['ticker']}`",
        f"- Composite FIGI: `{segment['composite_figi']}`",
        f"- Share Class FIGI: `{segment['share_class_figi']}`",
        f"- Primary MIC: `{segment['primary_mic']}`",
        f"- Security type: `{segment['security_type']}`",
        f"- Range: `{segment['segment_start']}` through `{segment['segment_end']}`",
        "",
        "## Frozen Authority Bindings",
        f"- Identity frozen digest: `{candidate['identity_segment_frozen_digest']}`",
        f"- Calendar frozen digest: `{candidate['exchange_calendar_frozen_digest']}`",
        f"- Schedule digest: `{candidate['schedule_semantic_digest']}`",
        f"- Acquisition contract digest: `{candidate['acquisition_contract_digest']}`",
        "",
        "## Provider Evidence",
        f"- Provider evidence required: `{source_status['provider_evidence_required']}`",
        f"- Provider evidence status: `{source_status['provider_evidence_status']}`",
        f"- Provider request performed in this task: `{source_status['provider_request_performed_in_this_task']}`",
        f"- Split event audit complete: `{candidate['split_event_audit_complete']}`",
        f"- Split event audit frozen: `{candidate['split_event_audit_frozen']}`",
        "",
        "## Scaffold Checklist Summary",
        f"- Total checks: `{validation['total_checks']}`",
        f"- Passed checks: `{validation['passed_checks']}`",
        f"- Failed checks: `{validation['failed_checks']}`",
        f"- Blockers: `{validation['blocker_count']}`",
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
        "## Remaining Roadmap",
    ]
    lines.extend(f"{index}. {task}" for index, task in enumerate(REMAINING_ROADMAP_AFTER_SPLIT_EVENT_AUDIT_SCAFFOLD, start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider requests were made.",
            "- No split-event provider evidence is bound.",
            "- No split audit completion or freeze is claimed.",
            "- No acquisition bars are generated or frozen.",
            "- No canonical or registry eligibility is approved.",
            "- No Strategy, runtime, broker, or execution behavior is changed.",
            "- Predictive usefulness and profitability remain not accepted.",
        ]
    )
    return "\n".join(lines) + "\n"
