"""Offline scaffold contract for split-event audit evidence candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes


ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE = "SPLIT_EVENT_AUDIT_CANDIDATE"
SCHEMA_VERSION_SPLIT_EVENT_AUDIT_CANDIDATE_V1 = "split_event_audit_candidate_v1"
SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE = "SPLIT_EVENT_AUDIT_REQUIRES_PROVIDER_EVIDENCE"
SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION = "SPLIT_EVENT_AUDIT_PROVIDER_EVIDENCE_COLLECTION"

EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST = "25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6"
EXPECTED_SCHEDULE_SEMANTIC_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
EXPECTED_ACQUISITION_CONTRACT_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"

PROVIDER_EVIDENCE_STATUS_NOT_BOUND = "NOT_BOUND"
PREDICTIVE_USEFULNESS_NOT_ACCEPTED = "not accepted"
PROFITABILITY_NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EVENT_COUNT_FIELDS = [
    "split_event_count_total",
    "split_event_count_pre_range",
    "split_event_count_in_range",
    "split_event_count_post_range",
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


def validate_split_event_audit_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate the split-event audit scaffold and fail closed on premature evidence claims."""
    if not isinstance(candidate, dict):
        raise SplitEventAuditError("split-event audit candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_SPLIT_EVENT_AUDIT_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_SPLIT_EVENT_AUDIT_CANDIDATE_V1, "schema_version")
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
