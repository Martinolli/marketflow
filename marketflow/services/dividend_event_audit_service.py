"""Dividend-event audit candidate scaffold contracts."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import split_event_audit_service as split


ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE = "DIVIDEND_EVENT_AUDIT_CANDIDATE"
SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_CANDIDATE_V1 = "dividend_event_audit_candidate_v1"
DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE = "DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"
DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION = "DIVIDEND_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION"
PROVIDER_EVIDENCE_STATUS_NOT_BOUND = "NOT_BOUND"
PREDICTIVE_USEFULNESS_NOT_ACCEPTED = "not accepted"
PROFITABILITY_NOT_ACCEPTED = "not accepted"
SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT = "SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT"

EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST = split.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST
EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST = split.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST
EXPECTED_SCHEDULE_SEMANTIC_DIGEST = split.EXPECTED_SCHEDULE_SEMANTIC_DIGEST
EXPECTED_ACQUISITION_CONTRACT_DIGEST = split.EXPECTED_ACQUISITION_CONTRACT_DIGEST
EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST = "9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae"
EXPECTED_SPLIT_EVENT_AUDIT_STATUS = SPLIT_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_SPLIT

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

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
    "payable_date",
    "cash_amount",
    "currency",
    "frequency",
    "dividend_type",
    "ticker",
    "composite_figi_if_available",
    "raw_event_index",
    "raw_event_digest",
    "event_position",
]

VALID_EVENT_POSITIONS = ["PRE_RANGE", "IN_RANGE", "POST_RANGE", "UNKNOWN"]

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


class DividendEventAuditError(ValueError):
    """Raised when a dividend-event audit candidate violates scaffold guardrails."""


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
    """Return the deterministic semantic digest for a dividend-event audit candidate scaffold."""
    return semantic_digest(_candidate_digest_payload(candidate))


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


def _validate_authority_boundary(candidate: dict[str, Any]) -> None:
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


def _validate_digest(candidate: dict[str, Any]) -> str:
    digest = candidate.get("dividend_event_audit_candidate_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise DividendEventAuditError("dividend_event_audit_candidate_semantic_digest missing")
    expected = dividend_event_audit_candidate_semantic_digest(candidate)
    _expect(digest, expected, "dividend_event_audit_candidate_semantic_digest")
    return digest


def validate_dividend_event_audit_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate the offline dividend-event audit scaffold and return a receipt."""
    if not isinstance(candidate, dict):
        raise DividendEventAuditError("candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_DIVIDEND_EVENT_AUDIT_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_DIVIDEND_EVENT_AUDIT_CANDIDATE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), DIVIDEND_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE, "candidate_status")
    _expect_true(candidate.get("created_offline"), "created_offline")
    _expect_false(candidate.get("provider_requests_made"), "provider_requests_made")
    _expect_false(candidate.get("dividend_events_provider_evidence_bound"), "dividend_events_provider_evidence_bound")
    _expect_false(candidate.get("dividend_event_audit_complete"), "dividend_event_audit_complete")
    _expect_false(candidate.get("dividend_event_audit_frozen"), "dividend_event_audit_frozen")
    _expect_true(candidate.get("operator_review_required"), "operator_review_required")
    _expect_true(candidate.get("operator_freeze_required"), "operator_freeze_required")
    _validate_authority_boundary(candidate)
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
    """Build a sanitized Markdown summary for the offline dividend scaffold."""
    payload = deepcopy(candidate) if candidate is not None else build_dividend_event_audit_candidate_v1()
    validation = validate_dividend_event_audit_candidate_v1(payload)
    summary = payload["scaffold_summary"]
    lines = [
        "# Dividend-Event Audit Candidate v1",
        "",
        "## Scaffold Candidate",
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
        "No provider requests were made.",
        "No dividend-event provider evidence is bound.",
        "Dividend event counts, raw response artifacts, timeline artifacts, and receipts remain unpopulated.",
        "",
        "## Scaffold Checklist Summary",
        "",
        f"- total checks: `{summary['total_checks']}`",
        f"- passed checks: `{summary['passed_checks']}`",
        f"- failed checks: `{summary['failed_checks']}`",
        f"- blocker count: `{summary['blocker_count']}`",
        "",
        "## Authority Boundary",
        "",
    ]
    for key, value in payload["authority_boundary"].items():
        rendered = str(value).lower() if isinstance(value, bool) else value
        lines.append(f"- {key}: `{rendered}`")
    lines.extend(
        [
            "",
            "## Expected Future Normalized Fields",
            "",
            *[f"- `{field}`" for field in EXPECTED_DIVIDEND_EVENT_FIELDS],
            "",
            "## Remaining Roadmap",
            "",
            *[f"- {item}" for item in payload["remaining_roadmap"]],
            "",
            "## Guardrails",
            "",
            "No dividend audit completion or freeze is claimed.",
            "No canonical eligibility, registry eligibility, acquisition-generation freeze, strategy runtime migration, predictive acceptance, or profitability acceptance is claimed.",
            "",
        ]
    )
    return "\n".join(lines)
