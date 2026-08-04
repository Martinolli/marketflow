"""Offline operator freeze ceremony for identity segment candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import identity_segment_freeze_service as freeze
from marketflow.services import identity_segment_operator_review_service as review


ARTIFACT_KIND_IDENTITY_SEGMENT_FROZEN = "IDENTITY_SEGMENT_FROZEN"
SCHEMA_VERSION_IDENTITY_SEGMENT_OPERATOR_FREEZE_V1 = "identity_segment_operator_freeze_v1"
IDENTITY_SEGMENT_FROZEN = "IDENTITY_SEGMENT_FROZEN"
OPERATOR_DECISION_APPROVE_IDENTITY_SEGMENT_FREEZE = "APPROVE_IDENTITY_SEGMENT_FREEZE"
OPERATOR_ATTESTATION_VERSION_V1 = "identity_segment_operator_attestation_v1"
REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "FREEZE IDENTITY SEGMENT AAPL BBG000B9XRY4 BBG001S5N8V8 XNAS CS 2022-01-01 2025-12-31"
)

EXPECTED_CANDIDATE_SEMANTIC_DIGEST = review.EXPECTED_CANDIDATE_SEMANTIC_DIGEST
EXPECTED_REVIEW_PACKAGE_SEMANTIC_DIGEST = "c39ad88e25554de67a52a3383c53a1df2bcac257b89b3d087be68b22bbcc17bd"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OPERATOR_BOUNDARY_CONFIRMATION_FIELDS = [
    "operator_confirms_no_provider_requests",
    "operator_confirms_no_calendar_freeze",
    "operator_confirms_no_canonical_approval",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_acquisition_generation_freeze",
]

REMAINING_ROADMAP_AFTER_IDENTITY_SEGMENT_FREEZE = [
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

REQUIRED_FREEZE_CHECK_IDS = [
    "candidate_digest_matches_expected",
    "review_package_digest_matches_expected",
    "review_package_has_zero_blockers",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_candidate_digest_confirmation_matches",
    "operator_review_digest_confirmation_matches",
    "operator_confirms_no_provider_requests",
    "operator_confirms_no_calendar_freeze",
    "operator_confirms_no_canonical_approval",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_acquisition_generation_freeze",
    "identity_segment_fields_match",
    "contract_digest_matches",
    "identity_evidence_bindings_match",
    "ticker_events_evidence_bindings_match",
    "ticker_events_in_range_count_zero",
    "automatic_stitching_false",
    "calendar_operator_frozen_false",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "acquisition_generation_freeze_false",
    "strategy_runtime_migration_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
]


class IdentitySegmentOperatorFreezeError(ValueError):
    """Raised when an operator freeze ceremony violates freeze guardrails."""


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
        "message": message or ("freeze evidence matches" if status == PASS else "freeze evidence mismatch"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise IdentitySegmentOperatorFreezeError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise IdentitySegmentOperatorFreezeError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise IdentitySegmentOperatorFreezeError(f"{field_name} must be true")


def _source_candidate(candidate: dict[str, Any] | None) -> dict[str, Any]:
    source_candidate = deepcopy(candidate) if candidate is not None else freeze.build_identity_segment_candidate_v1()
    try:
        validation = freeze.validate_identity_segment_candidate_v1(source_candidate)
    except freeze.IdentitySegmentFreezeError as exc:
        raise IdentitySegmentOperatorFreezeError(f"source candidate invalid: {exc}") from exc
    _expect(validation["candidate_semantic_digest"], EXPECTED_CANDIDATE_SEMANTIC_DIGEST, "source candidate semantic digest")
    return source_candidate


def _source_review_package(
    candidate: dict[str, Any],
    review_package: dict[str, Any] | None,
) -> dict[str, Any]:
    source_review = (
        deepcopy(review_package)
        if review_package is not None
        else review.build_identity_segment_candidate_review_package_v1(candidate)
    )
    try:
        validation = review.validate_identity_segment_candidate_review_package_v1(source_review)
    except review.IdentitySegmentOperatorReviewError as exc:
        raise IdentitySegmentOperatorFreezeError(f"source review package invalid: {exc}") from exc
    _expect(validation["review_package_semantic_digest"], EXPECTED_REVIEW_PACKAGE_SEMANTIC_DIGEST, "source review package semantic digest")
    _expect(validation["blocker_count"], 0, "source review blocker count")
    _expect(validation["failed_checks"], 0, "source review failed check count")
    _expect(source_review.get("reviewed_candidate_semantic_digest"), candidate.get("candidate_semantic_digest"), "reviewed candidate semantic digest")
    return source_review


def build_identity_segment_operator_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_review_package_digest: str,
    operator_confirms_no_provider_requests: bool,
    operator_confirms_no_calendar_freeze: bool,
    operator_confirms_no_canonical_approval: bool,
    operator_confirms_no_registry_approval: bool,
    operator_confirms_no_acquisition_generation_freeze: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_IDENTITY_SEGMENT_FREEZE,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for the identity freeze ceremony."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_candidate_digest": operator_confirms_candidate_digest,
        "operator_confirms_review_package_digest": operator_confirms_review_package_digest,
        "operator_confirms_no_provider_requests": operator_confirms_no_provider_requests,
        "operator_confirms_no_calendar_freeze": operator_confirms_no_calendar_freeze,
        "operator_confirms_no_canonical_approval": operator_confirms_no_canonical_approval,
        "operator_confirms_no_registry_approval": operator_confirms_no_registry_approval,
        "operator_confirms_no_acquisition_generation_freeze": operator_confirms_no_acquisition_generation_freeze,
    }


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_IDENTITY_SEGMENT_FREEZE, None),
            _check("operator_attestation_phrase_matches", REQUIRED_OPERATOR_ATTESTATION_PHRASE, None),
            _check("operator_candidate_digest_confirmation_matches", EXPECTED_CANDIDATE_SEMANTIC_DIGEST, None),
            _check("operator_review_digest_confirmation_matches", EXPECTED_REVIEW_PACKAGE_SEMANTIC_DIGEST, None),
            *[_check(field, True, None) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_IDENTITY_SEGMENT_FREEZE, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check(
            "operator_candidate_digest_confirmation_matches",
            EXPECTED_CANDIDATE_SEMANTIC_DIGEST,
            attestation.get("operator_confirms_candidate_digest"),
        ),
        _check(
            "operator_review_digest_confirmation_matches",
            EXPECTED_REVIEW_PACKAGE_SEMANTIC_DIGEST,
            attestation.get("operator_confirms_review_package_digest"),
        ),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
    ]


def _build_freeze_checklist(frozen_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = frozen_artifact.get("operator_attestation")
    segment = frozen_artifact.get("frozen_identity_segment")
    identity = frozen_artifact.get("identity_evidence_binding")
    identity_summary = frozen_artifact.get("identity_evidence")
    ticker_events = frozen_artifact.get("ticker_events_evidence_binding")
    ticker_events_summary = frozen_artifact.get("ticker_events_evidence")
    authority = frozen_artifact.get("authority_boundary", {})
    expected_identity_summary = {
        "identity_run_id": freeze.IDENTITY_RUN_ID,
        "continuity_artifact_id": freeze.CONTINUITY_ARTIFACT_ID,
        "start_snapshot_semantic_digest": freeze.START_SNAPSHOT_SEMANTIC_DIGEST,
        "end_snapshot_semantic_digest": freeze.END_SNAPSHOT_SEMANTIC_DIGEST,
        "continuity_status": freeze.ident.IDENTITY_CONTINUITY_SUPPORTED,
        "artifact_inventory_total": 6,
    }
    expected_ticker_events_summary = {
        "ticker_events_audit_run_id": freeze.TICKER_EVENTS_AUDIT_RUN_ID,
        "raw_response_artifact_id": freeze.TICKER_EVENTS_RAW_RESPONSE_ARTIFACT_ID,
        "raw_response_semantic_payload_digest": freeze.TICKER_EVENTS_RAW_RESPONSE_SEMANTIC_PAYLOAD_DIGEST,
        "timeline_artifact_id": freeze.TICKER_EVENTS_TIMELINE_ARTIFACT_ID,
        "timeline_semantic_digest": freeze.TICKER_EVENTS_TIMELINE_SEMANTIC_DIGEST,
        "audit_artifact_id": freeze.TICKER_EVENTS_AUDIT_ARTIFACT_ID,
        "receipt_artifact_id": freeze.TICKER_EVENTS_RECEIPT_ARTIFACT_ID,
        "endpoint": freeze.tkev.TICKER_EVENTS_EXPERIMENTAL_VX,
        "endpoint_stability": freeze.tkev.ENDPOINT_STABILITY_EXPERIMENTAL,
        "pre_range_events": 1,
        "in_range_events": 0,
        "post_range_events": 0,
        "ticker_events_audit_status": freeze.tkev.TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE,
    }
    return [
        _check("candidate_digest_matches_expected", EXPECTED_CANDIDATE_SEMANTIC_DIGEST, frozen_artifact.get("source_candidate_semantic_digest")),
        _check("review_package_digest_matches_expected", EXPECTED_REVIEW_PACKAGE_SEMANTIC_DIGEST, frozen_artifact.get("source_review_package_semantic_digest")),
        _check("review_package_has_zero_blockers", 0, frozen_artifact.get("source_review_blocker_count")),
        *_attestation_checks(attestation if isinstance(attestation, dict) else None),
        _check("identity_segment_fields_match", freeze.SEGMENT, segment),
        _check(
            "contract_digest_matches",
            freeze.ACQUISITION_CONTRACT_V2_1_DIGEST,
            frozen_artifact.get("acquisition_contract_digest"),
        ),
        _check(
            "identity_evidence_bindings_match",
            {"binding": freeze.IDENTITY_EVIDENCE_BINDING, "summary": expected_identity_summary},
            {"binding": identity, "summary": identity_summary},
        ),
        _check(
            "ticker_events_evidence_bindings_match",
            {"binding": freeze.TICKER_EVENTS_EVIDENCE_BINDING, "summary": expected_ticker_events_summary},
            {"binding": ticker_events, "summary": ticker_events_summary},
        ),
        _check(
            "ticker_events_in_range_count_zero",
            0,
            ticker_events.get("in_range_events") if isinstance(ticker_events, dict) else None,
        ),
        _check("automatic_stitching_false", False, frozen_artifact.get("automatic_stitching")),
        _check("calendar_operator_frozen_false", False, authority.get("calendar_operator_frozen")),
        _check("canonical_eligibility_false", False, authority.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, authority.get("registry_eligibility")),
        _check("acquisition_generation_freeze_false", False, authority.get("acquisition_generation_freeze")),
        _check("strategy_runtime_migration_false", False, authority.get("strategy_runtime_migration")),
        _check("predictive_usefulness_not_accepted", freeze.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, authority.get("predictive_usefulness")),
        _check("profitability_not_accepted", freeze.PROFITABILITY_NOT_ACCEPTED, authority.get("profitability")),
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
        "identity_segment_freeze_authorized_by_operator": failed == 0,
        "software_auto_approval": False,
    }


def _frozen_digest_payload(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(frozen_artifact)
    payload.pop("identity_segment_frozen_semantic_digest", None)
    payload.pop("frozen_payload_digest", None)
    return payload


def identity_segment_frozen_semantic_digest(frozen_artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a frozen identity segment."""
    return semantic_digest(_frozen_digest_payload(frozen_artifact))


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise IdentitySegmentOperatorFreezeError("operator_attestation must be a JSON object")
    for field in ("operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise IdentitySegmentOperatorFreezeError(f"{field} must be a non-empty string")
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise IdentitySegmentOperatorFreezeError(f"operator attestation failed: {failed[0]['check_id']}")
    return deepcopy(attestation)


def _identity_evidence_summary(identity: dict[str, Any]) -> dict[str, Any]:
    return {
        "identity_run_id": identity["identity_run_id"],
        "continuity_artifact_id": identity["continuity_artifact_id"],
        "start_snapshot_semantic_digest": identity["start_snapshot_semantic_digest"],
        "end_snapshot_semantic_digest": identity["end_snapshot_semantic_digest"],
        "continuity_status": identity["continuity_status"],
        "artifact_inventory_total": identity["total_manifests"],
    }


def _ticker_events_evidence_summary(ticker_events: dict[str, Any]) -> dict[str, Any]:
    return {
        "ticker_events_audit_run_id": ticker_events["ticker_events_audit_run_id"],
        "raw_response_artifact_id": ticker_events["raw_response_artifact_id"],
        "raw_response_semantic_payload_digest": ticker_events["raw_response_semantic_payload_digest"],
        "timeline_artifact_id": ticker_events["timeline_artifact_id"],
        "timeline_semantic_digest": ticker_events["timeline_semantic_digest"],
        "audit_artifact_id": ticker_events["audit_artifact_id"],
        "receipt_artifact_id": ticker_events["receipt_artifact_id"],
        "endpoint": ticker_events["endpoint"],
        "endpoint_stability": ticker_events["endpoint_stability"],
        "pre_range_events": ticker_events["pre_range_events"],
        "in_range_events": ticker_events["in_range_events"],
        "post_range_events": ticker_events["post_range_events"],
        "ticker_events_audit_status": ticker_events["ticker_events_audit_status"],
    }


def build_identity_segment_frozen_v1(
    *,
    candidate: dict[str, Any] | None = None,
    review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build the offline identity segment frozen artifact after operator attestation."""
    source_candidate = _source_candidate(candidate)
    source_review = _source_review_package(source_candidate, review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    authority_boundary = deepcopy(source_candidate["authority_boundary"])
    authority_boundary["identity_segment_frozen"] = True
    identity_binding = deepcopy(source_candidate["identity_evidence_binding"])
    ticker_events_binding = deepcopy(source_candidate["ticker_events_evidence_binding"])
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_IDENTITY_SEGMENT_FROZEN,
        "schema_version": SCHEMA_VERSION_IDENTITY_SEGMENT_OPERATOR_FREEZE_V1,
        "freeze_status": IDENTITY_SEGMENT_FROZEN,
        "identity_segment_frozen": True,
        "created_offline": True,
        "provider_requests_made": False,
        "automatic_stitching": False,
        "calendar_operator_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "predictive_usefulness": freeze.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": freeze.PROFITABILITY_NOT_ACCEPTED,
        "source_candidate_kind": source_candidate["artifact_kind"],
        "source_candidate_status": source_candidate["candidate_status"],
        "source_candidate_semantic_digest": source_candidate["candidate_semantic_digest"],
        "source_review_package_kind": source_review["artifact_kind"],
        "source_review_status": source_review["review_status"],
        "source_review_package_semantic_digest": source_review["review_package_semantic_digest"],
        "source_review_checklist_total": source_review["review_summary"]["total_checks"],
        "source_review_checklist_passed": source_review["review_summary"]["passed_checks"],
        "source_review_checklist_failed": source_review["review_summary"]["failed_checks"],
        "source_review_blocker_count": source_review["review_summary"]["blocker_count"],
        "operator_attestation": attestation,
        "frozen_identity_segment": deepcopy(source_candidate["segment"]),
        "acquisition_contract_digest": freeze.ACQUISITION_CONTRACT_V2_1_DIGEST,
        "identity_evidence_binding": identity_binding,
        "identity_evidence": _identity_evidence_summary(identity_binding),
        "ticker_events_evidence_binding": ticker_events_binding,
        "ticker_events_evidence": _ticker_events_evidence_summary(ticker_events_binding),
        "monthly_source_evidence": deepcopy(source_candidate["monthly_source_evidence"]),
        "authority_boundary": authority_boundary,
        "lineage_guardrails": {
            "binding_mode": freeze.REFERENCE_ONLY,
            "raw_source_evidence_copied": False,
            "raw_source_evidence_rewritten": False,
            "provider_requests_made": False,
            "operator_attested": True,
            "software_auto_approval": False,
        },
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_IDENTITY_SEGMENT_FREEZE),
    }
    checklist = _build_freeze_checklist(artifact)
    artifact["freeze_checklist"] = checklist
    artifact["freeze_summary"] = _summary(checklist)
    artifact["identity_segment_frozen_semantic_digest"] = identity_segment_frozen_semantic_digest(artifact)
    validate_identity_segment_frozen_v1(artifact)
    return artifact


def validate_identity_segment_frozen_v1(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate the frozen identity segment artifact and return a receipt."""
    if not isinstance(frozen_artifact, dict):
        raise IdentitySegmentOperatorFreezeError("frozen artifact must be a JSON object")
    _expect(frozen_artifact.get("artifact_kind"), ARTIFACT_KIND_IDENTITY_SEGMENT_FROZEN, "artifact_kind")
    _expect(frozen_artifact.get("schema_version"), SCHEMA_VERSION_IDENTITY_SEGMENT_OPERATOR_FREEZE_V1, "schema_version")
    _expect(frozen_artifact.get("freeze_status"), IDENTITY_SEGMENT_FROZEN, "freeze_status")
    _expect_true(frozen_artifact.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(frozen_artifact.get("created_offline"), "created_offline")
    _expect_false(frozen_artifact.get("provider_requests_made"), "provider_requests_made")
    _expect_false(frozen_artifact.get("automatic_stitching"), "automatic_stitching")
    for field in (
        "calendar_operator_frozen",
        "canonical_eligibility",
        "registry_eligibility",
        "acquisition_generation_freeze",
        "strategy_runtime_migration",
    ):
        _expect_false(frozen_artifact.get(field), field)
    _expect(frozen_artifact.get("predictive_usefulness"), freeze.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(frozen_artifact.get("profitability"), freeze.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(frozen_artifact.get("source_candidate_kind"), freeze.ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE, "source_candidate_kind")
    _expect(
        frozen_artifact.get("source_candidate_status"),
        freeze.IDENTITY_SEGMENT_READY_FOR_OPERATOR_FREEZE_REVIEW,
        "source_candidate_status",
    )
    _expect(frozen_artifact.get("source_candidate_semantic_digest"), EXPECTED_CANDIDATE_SEMANTIC_DIGEST, "source_candidate_semantic_digest")
    _expect(
        frozen_artifact.get("source_review_package_kind"),
        review.ARTIFACT_KIND_IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE,
        "source_review_package_kind",
    )
    _expect(frozen_artifact.get("source_review_status"), review.IDENTITY_SEGMENT_CANDIDATE_REVIEW_PACKAGE_READY, "source_review_status")
    _expect(
        frozen_artifact.get("source_review_package_semantic_digest"),
        EXPECTED_REVIEW_PACKAGE_SEMANTIC_DIGEST,
        "source_review_package_semantic_digest",
    )
    _expect(frozen_artifact.get("source_review_checklist_total"), len(review.REQUIRED_CHECK_IDS), "source_review_checklist_total")
    _expect(frozen_artifact.get("source_review_checklist_passed"), len(review.REQUIRED_CHECK_IDS), "source_review_checklist_passed")
    _expect(frozen_artifact.get("source_review_checklist_failed"), 0, "source_review_checklist_failed")
    _expect(frozen_artifact.get("source_review_blocker_count"), 0, "source_review_blocker_count")
    _validated_operator_attestation(frozen_artifact.get("operator_attestation"))

    checklist = _build_freeze_checklist(frozen_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_FREEZE_CHECK_IDS, "freeze_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise IdentitySegmentOperatorFreezeError(f"freeze checklist contains failed check: {failed[0]['check_id']}")
    _expect(frozen_artifact.get("freeze_checklist"), checklist, "freeze_checklist")
    summary = _summary(checklist)
    _expect(frozen_artifact.get("freeze_summary"), summary, "freeze_summary")
    _expect_true(summary.get("identity_segment_freeze_authorized_by_operator"), "identity_segment_freeze_authorized_by_operator")
    _expect_false(summary.get("software_auto_approval"), "software_auto_approval")
    _expect(frozen_artifact.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_IDENTITY_SEGMENT_FREEZE, "remaining_roadmap")

    digest = identity_segment_frozen_semantic_digest(frozen_artifact)
    _expect(
        frozen_artifact.get("identity_segment_frozen_semantic_digest"),
        digest,
        "identity_segment_frozen_semantic_digest",
    )
    return {
        "status": "IDENTITY_SEGMENT_FROZEN_VALID",
        "artifact_kind": ARTIFACT_KIND_IDENTITY_SEGMENT_FROZEN,
        "freeze_status": IDENTITY_SEGMENT_FROZEN,
        "source_candidate_semantic_digest": EXPECTED_CANDIDATE_SEMANTIC_DIGEST,
        "source_review_package_semantic_digest": EXPECTED_REVIEW_PACKAGE_SEMANTIC_DIGEST,
        "identity_segment_frozen_semantic_digest": digest,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "identity_segment_freeze_authorized_by_operator": True,
        "software_auto_approval": False,
        "provider_requests_made": False,
        "calendar_operator_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
    }


def write_identity_segment_frozen_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the frozen identity segment JSON artifact without overwriting output."""
    frozen = build_identity_segment_frozen_v1(
        candidate=candidate,
        review_package=review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_identity_segment_frozen_v1(frozen)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_identity_segment_frozen_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise IdentitySegmentOperatorFreezeError("frozen artifact filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise IdentitySegmentOperatorFreezeError("identity segment frozen output already exists")
    payload = canonical_json_bytes(frozen)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "frozen_payload_digest": sha256_bytes(payload),
    }


def build_identity_segment_frozen_markdown_v1(frozen_artifact: dict[str, Any]) -> str:
    """Build a compact Markdown view of a validated frozen identity segment."""
    validation = validate_identity_segment_frozen_v1(frozen_artifact)
    segment = frozen_artifact["frozen_identity_segment"]
    attestation = frozen_artifact["operator_attestation"]
    identity = frozen_artifact["identity_evidence_binding"]
    ticker_events = frozen_artifact["ticker_events_evidence_binding"]
    authority = frozen_artifact["authority_boundary"]
    lines = [
        "# Identity Segment Frozen v1",
        "",
        "## Frozen Identity Segment",
        f"- Ticker: `{segment['ticker']}`",
        f"- Composite FIGI: `{segment['composite_figi']}`",
        f"- Share Class FIGI: `{segment['share_class_figi']}`",
        f"- Primary MIC: `{segment['primary_mic']}`",
        f"- Security type: `{segment['security_type']}`",
        f"- Range: `{segment['segment_start']}` through `{segment['segment_end']}`",
        f"- Frozen artifact digest: `{validation['identity_segment_frozen_semantic_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        f"- Attestation phrase: `{attestation['operator_attestation_phrase']}`",
        "",
        "## Source Candidate",
        f"- Artifact kind: `{frozen_artifact['source_candidate_kind']}`",
        f"- Candidate status: `{frozen_artifact['source_candidate_status']}`",
        f"- Candidate semantic digest: `{frozen_artifact['source_candidate_semantic_digest']}`",
        "",
        "## Source Review Package",
        f"- Artifact kind: `{frozen_artifact['source_review_package_kind']}`",
        f"- Review status: `{frozen_artifact['source_review_status']}`",
        f"- Review package semantic digest: `{frozen_artifact['source_review_package_semantic_digest']}`",
        f"- Review checks: `{validation['passed_checks']}` passed of `{validation['total_checks']}`",
        f"- Blockers: `{validation['blocker_count']}`",
        "",
        "## Evidence Bound",
        f"- Identity run: `{identity['identity_run_id']}`",
        f"- Continuity artifact: `{identity['continuity_artifact_id']}`",
        f"- Ticker Events audit run: `{ticker_events['ticker_events_audit_run_id']}`",
        f"- Ticker Events status: `{ticker_events['ticker_events_audit_status']}`",
        f"- Ticker Events in-range events: `{ticker_events['in_range_events']}`",
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
    lines.extend(f"{index}. {task}" for index, task in enumerate(REMAINING_ROADMAP_AFTER_IDENTITY_SEGMENT_FREEZE, start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider requests were made.",
            "- No calendar evidence is frozen.",
            "- No canonical or registry eligibility is approved.",
            "- No acquisition generation freeze, runtime migration, broker, or execution behavior is changed.",
            "- Predictive usefulness and profitability remain not accepted.",
        ]
    )
    return "\n".join(lines) + "\n"
