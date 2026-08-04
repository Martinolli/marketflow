"""Offline operator-review package for identity segment candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import identity_segment_freeze_service as freeze


ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE = "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE"
SCHEMA_VERSION_IDENTITY_SEGMENT_CANDIDATE_REVIEW_V1 = "identity_segment_candidate_review_v1"
IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY = "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY"
EXPECTED_CANDIDATE_SEMANTIC_DIGEST = "263902ddc149728d095a4f8bc941c92a82c2d4360e0a038d231e0eac6c70dc57"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
HIGH = "HIGH"
INFO = "INFO"

REMAINING_REQUIRED_TASKS = [
    "Digest-bound operator freeze ceremony.",
    "Official/operator-frozen exchange-calendar evidence.",
    "Split-event audit.",
    "Dividend-event audit.",
    "Full 2022-2025 acquisition generation.",
    "Acquisition-generation freeze.",
    "SWING canonical dataset and registry approval.",
    "POSITION_SWING canonical dataset and registry approval.",
    "Normal runtime migration.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
]

REQUIRED_CHECK_IDS = [
    "candidate_kind_is_identity_segment_candidate",
    "candidate_status_ready_for_operator_review",
    "candidate_digest_matches_expected",
    "segment_ticker_matches",
    "segment_composite_figi_matches",
    "segment_share_class_figi_matches",
    "segment_primary_mic_matches",
    "segment_security_type_matches",
    "segment_start_matches",
    "segment_end_matches",
    "contract_digest_matches",
    "identity_run_id_matches",
    "identity_continuity_artifact_id_matches",
    "identity_snapshot_digests_match",
    "identity_artifact_inventory_count_matches",
    "ticker_events_audit_run_id_matches",
    "ticker_events_artifact_ids_match",
    "ticker_events_raw_digest_matches",
    "ticker_events_timeline_digest_matches",
    "ticker_events_in_range_count_zero",
    "ticker_events_change_before_contract_range",
    "ticker_events_endpoint_marked_experimental",
    "automatic_stitching_false",
    "identity_segment_frozen_false",
    "calendar_operator_frozen_false",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "acquisition_generation_freeze_false",
    "strategy_runtime_migration_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "provider_requests_made_false",
    "reference_only_binding_confirmed",
]

FORBIDDEN_FREEZE_FIELDS = frozenset(
    {
        "operator_approved_by",
        "operator_freeze_timestamp",
        "operator_freeze_digest",
        "operator_signature",
    }
)


class IdentitySegmentOperatorReviewError(ValueError):
    """Raised when an operator-review package violates review boundaries."""


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
        "message": message or ("accepted candidate evidence matches" if status == PASS else "candidate evidence mismatch"),
    }


def _event_before_contract_range(candidate: dict[str, Any]) -> str | None:
    events = candidate.get("ticker_events_evidence_binding", {}).get("events")
    if not isinstance(events, list) or len(events) != 1 or not isinstance(events[0], dict):
        return None
    event = events[0]
    if event.get("event_date") == "2003-09-10" and event.get("range_classification") == freeze.BEFORE_CONTRACT_RANGE:
        return freeze.BEFORE_CONTRACT_RANGE
    return str(event.get("range_classification"))


def _build_checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    segment = candidate.get("segment", {})
    identity = candidate.get("identity_evidence_binding", {})
    ticker_events = candidate.get("ticker_events_evidence_binding", {})
    authority = candidate.get("authority_boundary", {})
    guardrails = candidate.get("lineage_guardrails", {})
    candidate_artifact_ids = {
        "raw_response_artifact_id": ticker_events.get("raw_response_artifact_id"),
        "timeline_artifact_id": ticker_events.get("timeline_artifact_id"),
        "audit_artifact_id": ticker_events.get("audit_artifact_id"),
        "receipt_artifact_id": ticker_events.get("receipt_artifact_id"),
    }
    expected_artifact_ids = {
        "raw_response_artifact_id": freeze.TICKER_EVENTS_RAW_RESPONSE_ARTIFACT_ID,
        "timeline_artifact_id": freeze.TICKER_EVENTS_TIMELINE_ARTIFACT_ID,
        "audit_artifact_id": freeze.TICKER_EVENTS_AUDIT_ARTIFACT_ID,
        "receipt_artifact_id": freeze.TICKER_EVENTS_RECEIPT_ARTIFACT_ID,
    }
    return [
        _check("candidate_kind_is_identity_segment_candidate", freeze.ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE, candidate.get("artifact_kind")),
        _check("candidate_status_ready_for_operator_review", freeze.IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW, candidate.get("candidate_status")),
        _check("candidate_digest_matches_expected", EXPECTED_CANDIDATE_SEMANTIC_DIGEST, candidate.get("candidate_semantic_digest")),
        _check("segment_ticker_matches", freeze.SEGMENT["ticker"], segment.get("ticker")),
        _check("segment_composite_figi_matches", freeze.SEGMENT["composite_figi"], segment.get("composite_figi")),
        _check("segment_share_class_figi_matches", freeze.SEGMENT["share_class_figi"], segment.get("share_class_figi")),
        _check("segment_primary_mic_matches", freeze.SEGMENT["primary_mic"], segment.get("primary_mic")),
        _check("segment_security_type_matches", freeze.SEGMENT["security_type"], segment.get("security_type")),
        _check("segment_start_matches", freeze.SEGMENT["segment_start"], segment.get("segment_start")),
        _check("segment_end_matches", freeze.SEGMENT["segment_end"], segment.get("segment_end")),
        _check("contract_digest_matches", freeze.ACQUISITION_CONTRACT_V2_1_DIGEST, segment.get("acquisition_contract_digest")),
        _check("identity_run_id_matches", freeze.IDENTITY_RUN_ID, identity.get("identity_run_id")),
        _check("identity_continuity_artifact_id_matches", freeze.CONTINUITY_ARTIFACT_ID, identity.get("continuity_artifact_id")),
        _check(
            "identity_snapshot_digests_match",
            {
                "start_snapshot_semantic_digest": freeze.START_SNAPSHOT_SEMANTIC_DIGEST,
                "end_snapshot_semantic_digest": freeze.END_SNAPSHOT_SEMANTIC_DIGEST,
            },
            {
                "start_snapshot_semantic_digest": identity.get("start_snapshot_semantic_digest"),
                "end_snapshot_semantic_digest": identity.get("end_snapshot_semantic_digest"),
            },
        ),
        _check("identity_artifact_inventory_count_matches", 6, identity.get("total_manifests")),
        _check("ticker_events_audit_run_id_matches", freeze.TICKER_EVENTS_AUDIT_RUN_ID, ticker_events.get("ticker_events_audit_run_id")),
        _check("ticker_events_artifact_ids_match", expected_artifact_ids, candidate_artifact_ids),
        _check("ticker_events_raw_digest_matches", freeze.TICKER_EVENTS_RAW_RESPONSE_SEMANTIC_PAYLOAD_DIGEST, ticker_events.get("raw_response_semantic_payload_digest")),
        _check("ticker_events_timeline_digest_matches", freeze.TICKER_EVENTS_TIMELINE_SEMANTIC_DIGEST, ticker_events.get("timeline_semantic_digest")),
        _check("ticker_events_in_range_count_zero", 0, ticker_events.get("in_range_events")),
        _check("ticker_events_change_before_contract_range", freeze.BEFORE_CONTRACT_RANGE, _event_before_contract_range(candidate), severity=HIGH),
        _check("ticker_events_endpoint_marked_experimental", freeze.tkev.ENDPOINT_STABILITY_EXPERIMENTAL, ticker_events.get("endpoint_stability"), severity=INFO),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("identity_segment_frozen_false", False, candidate.get("identity_segment_frozen")),
        _check("calendar_operator_frozen_false", False, authority.get("calendar_operator_frozen")),
        _check("canonical_eligibility_false", False, authority.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, authority.get("registry_eligibility")),
        _check("acquisition_generation_freeze_false", False, authority.get("acquisition_generation_freeze")),
        _check("strategy_runtime_migration_false", False, authority.get("strategy_runtime_migration")),
        _check("predictive_usefulness_not_accepted", freeze.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, authority.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", freeze.PROFITABILITY_NOT_ACCEPTED, authority.get("profitability"), severity=INFO),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check(
            "reference_only_binding_confirmed",
            {"binding_mode": freeze.REFERENCE_ONLY, "raw_source_evidence_copied": False, "raw_source_evidence_rewritten": False},
            {
                "binding_mode": guardrails.get("binding_mode"),
                "raw_source_evidence_copied": guardrails.get("raw_source_evidence_copied"),
                "raw_source_evidence_rewritten": guardrails.get("raw_source_evidence_rewritten"),
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
        "ready_for_freeze_ceremony": False,
        "operator_decision_required_before_freeze": True,
        "software_freeze_authorized": False,
    }


def _package_digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("review_package_semantic_digest", None)
    payload.pop("review_package_payload_digest", None)
    return payload


def review_package_semantic_digest(review_package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the review package itself."""
    return semantic_digest(_package_digest_payload(review_package))


def build_identity_segment_candidate_review_package_v1(candidate: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a digest-bound offline operator-review package for the candidate."""
    reviewed_candidate = deepcopy(candidate) if candidate is not None else freeze.build_identity_segment_candidate_v1()
    checklist = _build_checklist(reviewed_candidate)
    package: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_IDENTITY_SEGMENT_CANDIDATE_REVIEW_V1,
        "review_status": IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY,
        "operator_decision_required": True,
        "operator_decision": None,
        "identity_segment_frozen": False,
        "created_offline": True,
        "provider_requests_made": False,
        "automatic_stitching": False,
        "reviewed_candidate_kind": reviewed_candidate.get("artifact_kind"),
        "reviewed_candidate_status": reviewed_candidate.get("candidate_status"),
        "reviewed_candidate_semantic_digest": reviewed_candidate.get("candidate_semantic_digest"),
        "candidate_binding": {
            "segment": deepcopy(reviewed_candidate.get("segment")),
            "identity_evidence_binding": deepcopy(reviewed_candidate.get("identity_evidence_binding")),
            "ticker_events_evidence_binding": deepcopy(reviewed_candidate.get("ticker_events_evidence_binding")),
            "authority_boundary": deepcopy(reviewed_candidate.get("authority_boundary")),
            "lineage_guardrails": deepcopy(reviewed_candidate.get("lineage_guardrails")),
        },
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
    package["review_package_semantic_digest"] = review_package_semantic_digest(package)
    return package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key in {"artifact_kind", "review_status", "reviewed_candidate_kind", "reviewed_candidate_status", "candidate_status", "freeze_status"} and value == freeze.IDENTITY_SEGMENT_FROZEN:
            raise IdentitySegmentOperatorReviewError(f"{current_path} must not emit IDENTITY_SEGMENT_FROZEN")
        if key in FORBIDDEN_FREEZE_FIELDS and value is not None:
            raise IdentitySegmentOperatorReviewError(f"{current_path} must be null")
        if key == "freeze_status" and value is not None:
            raise IdentitySegmentOperatorReviewError(f"{current_path} must be null")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise IdentitySegmentOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise IdentitySegmentOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise IdentitySegmentOperatorReviewError(f"{field_name} must be true")


def validate_identity_segment_candidate_review_package_v1(review_package: dict[str, Any]) -> dict[str, Any]:
    """Validate the operator-review package and fail closed on any failed check."""
    if not isinstance(review_package, dict):
        raise IdentitySegmentOperatorReviewError("review package must be a JSON object")
    _reject_forbidden_values(review_package)
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_IDENTITY_SEGMENT_CANDIDATE_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY, "review_status")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    _expect_false(review_package.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(review_package.get("created_offline"), "created_offline")
    _expect_false(review_package.get("provider_requests_made"), "provider_requests_made")
    _expect_false(review_package.get("automatic_stitching"), "automatic_stitching")
    _expect(review_package.get("reviewed_candidate_kind"), freeze.ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE, "reviewed_candidate_kind")
    _expect(review_package.get("reviewed_candidate_status"), freeze.IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW, "reviewed_candidate_status")
    _expect(review_package.get("reviewed_candidate_semantic_digest"), EXPECTED_CANDIDATE_SEMANTIC_DIGEST, "reviewed_candidate_semantic_digest")

    binding = review_package.get("candidate_binding")
    if not isinstance(binding, dict):
        raise IdentitySegmentOperatorReviewError("candidate_binding must be a JSON object")
    _expect(binding.get("segment"), freeze.SEGMENT, "candidate_binding.segment")
    _expect(binding.get("identity_evidence_binding"), freeze.IDENTITY_EVIDENCE_BINDING, "candidate_binding.identity_evidence_binding")
    _expect(binding.get("ticker_events_evidence_binding"), freeze.TICKER_EVENTS_EVIDENCE_BINDING, "candidate_binding.ticker_events_evidence_binding")
    _expect(binding.get("authority_boundary"), freeze.AUTHORITY_BOUNDARY, "candidate_binding.authority_boundary")
    _expect(binding.get("lineage_guardrails"), freeze.LINEAGE_GUARDRAILS, "candidate_binding.lineage_guardrails")

    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise IdentitySegmentOperatorReviewError("review_checklist must be a list")
    check_ids = [item.get("check_id") for item in checklist if isinstance(item, dict)]
    _expect(check_ids, REQUIRED_CHECK_IDS, "review_checklist check IDs")
    failed = [item for item in checklist if item.get("status") != PASS]
    if failed:
        raise IdentitySegmentOperatorReviewError("review package contains failed checks")

    expected_summary = _summary(checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    summary = review_package["review_summary"]
    _expect_true(summary.get("ready_for_operator_assessment"), "ready_for_operator_assessment")
    _expect_true(summary.get("operator_decision_required_before_freeze"), "operator_decision_required_before_freeze")
    _expect_false(summary.get("software_freeze_authorized"), "software_freeze_authorized")
    _expect_false(summary.get("ready_for_freeze_ceremony"), "ready_for_freeze_ceremony")
    _expect(review_package.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")

    controls = review_package.get("operator_freeze_controls")
    if not isinstance(controls, dict):
        raise IdentitySegmentOperatorReviewError("operator_freeze_controls must be a JSON object")
    for field in ("operator_approved_by", "operator_freeze_timestamp", "operator_freeze_digest", "operator_signature", "freeze_status"):
        _expect(controls.get(field), None, f"operator_freeze_controls.{field}")

    digest = review_package_semantic_digest(review_package)
    _expect(review_package.get("review_package_semantic_digest"), digest, "review_package_semantic_digest")
    return {
        "status": "IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE,
        "review_status": IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY,
        "reviewed_candidate_semantic_digest": EXPECTED_CANDIDATE_SEMANTIC_DIGEST,
        "review_package_semantic_digest": digest,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "provider_requests_made": False,
        "identity_segment_frozen": False,
        "software_freeze_authorized": False,
    }


def write_identity_segment_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the review package JSON artifact without overwriting existing output."""
    review_package = build_identity_segment_candidate_review_package_v1(candidate)
    validation = validate_identity_segment_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_identity_segment_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise IdentitySegmentOperatorReviewError("review package filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise IdentitySegmentOperatorReviewError("identity segment review package output already exists")
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "review_package_payload_digest": sha256_bytes(payload),
    }


def build_identity_segment_candidate_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Build a compact Markdown view of a validated review package."""
    validation = validate_identity_segment_candidate_review_package_v1(review_package)
    binding = review_package["candidate_binding"]
    segment = binding["segment"]
    identity = binding["identity_evidence_binding"]
    ticker_events = binding["ticker_events_evidence_binding"]
    authority = binding["authority_boundary"]
    failed_checks = [item for item in review_package["review_checklist"] if item["status"] != PASS]
    lines = [
        "# Identity Segment Candidate Review Package v1",
        "",
        "## Reviewed Candidate",
        f"- Artifact kind: `{review_package['reviewed_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_candidate_status']}`",
        f"- Candidate semantic digest: `{review_package['reviewed_candidate_semantic_digest']}`",
        f"- Review package semantic digest: `{validation['review_package_semantic_digest']}`",
        "",
        "## Segment",
        f"- Ticker: `{segment['ticker']}`",
        f"- Composite FIGI: `{segment['composite_figi']}`",
        f"- Share Class FIGI: `{segment['share_class_figi']}`",
        f"- Primary MIC: `{segment['primary_mic']}`",
        f"- Security type: `{segment['security_type']}`",
        f"- Range: `{segment['segment_start']}` through `{segment['segment_end']}`",
        "",
        "## Evidence Bound",
        f"- Identity run: `{identity['identity_run_id']}`",
        f"- Continuity artifact: `{identity['continuity_artifact_id']}`",
        f"- Ticker Events audit run: `{ticker_events['ticker_events_audit_run_id']}`",
        f"- Ticker Events status: `{ticker_events['ticker_events_audit_status']}`",
        f"- Endpoint stability: `{ticker_events['endpoint_stability']}`",
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
            f"- identity_segment_frozen: `{authority['identity_segment_frozen']}`",
            f"- calendar_operator_frozen: `{authority['calendar_operator_frozen']}`",
            f"- canonical_eligibility: `{authority['canonical_eligibility']}`",
            f"- registry_eligibility: `{authority['registry_eligibility']}`",
            f"- acquisition_generation_freeze: `{authority['acquisition_generation_freeze']}`",
            f"- strategy_runtime_migration: `{authority['strategy_runtime_migration']}`",
            f"- automatic_stitching: `{authority['automatic_stitching']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(REMAINING_REQUIRED_TASKS, start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider requests were made.",
            "- No `IDENTITY_SEGMENT_FROZEN` artifact or status is created.",
            "- Operator decision remains required before any future freeze ceremony.",
        ]
    )
    return "\n".join(lines) + "\n"
