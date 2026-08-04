"""Offline operator freeze ceremony for exchange-calendar evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import exchange_calendar_evidence_service as calendar
from marketflow.services import exchange_calendar_operator_review_service as review


ARTIFACT_KIND_EXCHANGE_CALENDAR_FROZEN = "EXCHANGE_CALENDAR_FROZEN"
SCHEMA_VERSION_EXCHANGE_CALENDAR_OPERATOR_FREEZE_V1 = "exchange_calendar_operator_freeze_v1"
EXCHANGE_CALENDAR_FROZEN = "EXCHANGE_CALENDAR_FROZEN"
OPERATOR_DECISION_APPROVE_EXCHANGE_CALENDAR_FREEZE = "APPROVE_EXCHANGE_CALENDAR_FREEZE"
OPERATOR_ATTESTATION_VERSION_V1 = "exchange_calendar_operator_attestation_v1"
REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "FREEZE EXCHANGE CALENDAR AAPL XNAS XNYS XNAS_USES_XNYS_SCHEDULE 2022-01-01 2025-12-31"
)
REQUIRED_EXCHANGE_CALENDAR_OPERATOR_ATTESTATION_PHRASE = REQUIRED_OPERATOR_ATTESTATION_PHRASE

EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST = review.EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST
EXPECTED_CALENDAR_REVIEW_PACKAGE_SEMANTIC_DIGEST = (
    "5e7e528068cd161e06a7a3cf6b30c40909023f23eb6b64661abb063363a690cb"
)
EXPECTED_SCHEDULE_SEMANTIC_DIGEST = review.EXPECTED_SCHEDULE_SEMANTIC_DIGEST
EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST = calendar.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CALENDAR_AUTHORITY_OPERATOR_FROZEN = "OPERATOR_FROZEN"
EXCHANGE_CALENDAR_FROZEN_REFERENCE_ONLY = "EXCHANGE_CALENDAR_FROZEN_REFERENCE_ONLY"

OPERATOR_BOUNDARY_CONFIRMATION_FIELDS = [
    "operator_confirms_no_provider_requests",
    "operator_confirms_no_canonical_approval",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_acquisition_generation_freeze",
    "operator_confirms_no_strategy_runtime_migration",
]

REMAINING_ROADMAP_AFTER_EXCHANGE_CALENDAR_FREEZE = [
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
    "calendar_candidate_digest_matches_expected",
    "calendar_review_package_digest_matches_expected",
    "calendar_review_package_has_zero_blockers",
    "schedule_digest_matches_expected",
    "identity_segment_frozen_digest_matches_expected",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_calendar_candidate_digest_confirmation_matches",
    "operator_calendar_review_digest_confirmation_matches",
    "operator_schedule_digest_confirmation_matches",
    "operator_identity_frozen_digest_confirmation_matches",
    "operator_confirms_no_provider_requests",
    "operator_confirms_no_canonical_approval",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_acquisition_generation_freeze",
    "operator_confirms_no_strategy_runtime_migration",
    "identity_segment_is_frozen",
    "calendar_operator_frozen_true",
    "calendar_binding_matches",
    "calendar_alias_matches",
    "calendar_source_library_matches",
    "calendar_source_library_version_matches",
    "monthly_2025_01_cross_check_matches",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "acquisition_generation_freeze_false",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
]


class ExchangeCalendarOperatorFreezeError(ValueError):
    """Raised when a calendar freeze ceremony violates freeze guardrails."""


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
        "message": message or ("calendar freeze evidence matches" if status == PASS else "calendar freeze evidence mismatch"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise ExchangeCalendarOperatorFreezeError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ExchangeCalendarOperatorFreezeError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ExchangeCalendarOperatorFreezeError(f"{field_name} must be true")


def _source_calendar_candidate(candidate: dict[str, Any] | None) -> dict[str, Any]:
    source_candidate = deepcopy(candidate) if candidate is not None else calendar.build_exchange_calendar_evidence_candidate_v1()
    try:
        validation = calendar.validate_exchange_calendar_evidence_candidate_v1(source_candidate)
    except calendar.ExchangeCalendarEvidenceError as exc:
        raise ExchangeCalendarOperatorFreezeError(f"source calendar candidate invalid: {exc}") from exc
    _expect(
        validation["calendar_evidence_candidate_semantic_digest"],
        EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST,
        "source calendar candidate semantic digest",
    )
    _expect(validation["schedule_semantic_digest"], EXPECTED_SCHEDULE_SEMANTIC_DIGEST, "source schedule semantic digest")
    return source_candidate


def _source_calendar_review_package(
    candidate: dict[str, Any],
    review_package: dict[str, Any] | None,
) -> dict[str, Any]:
    source_review = (
        deepcopy(review_package)
        if review_package is not None
        else review.build_exchange_calendar_evidence_candidate_review_package_v1(candidate)
    )
    try:
        validation = review.validate_exchange_calendar_evidence_candidate_review_package_v1(source_review)
    except review.ExchangeCalendarOperatorReviewError as exc:
        raise ExchangeCalendarOperatorFreezeError(f"source calendar review package invalid: {exc}") from exc
    _expect(
        validation["calendar_review_package_semantic_digest"],
        EXPECTED_CALENDAR_REVIEW_PACKAGE_SEMANTIC_DIGEST,
        "source calendar review package semantic digest",
    )
    _expect(validation["blocker_count"], 0, "source calendar review blocker count")
    _expect(validation["failed_checks"], 0, "source calendar review failed check count")
    _expect(
        source_review.get("reviewed_calendar_candidate_semantic_digest"),
        candidate.get("calendar_evidence_candidate_semantic_digest"),
        "reviewed calendar candidate semantic digest",
    )
    return source_review


def build_exchange_calendar_operator_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_calendar_candidate_digest: str,
    operator_confirms_calendar_review_package_digest: str,
    operator_confirms_schedule_digest: str,
    operator_confirms_identity_segment_frozen_digest: str,
    operator_confirms_no_provider_requests: bool,
    operator_confirms_no_canonical_approval: bool,
    operator_confirms_no_registry_approval: bool,
    operator_confirms_no_acquisition_generation_freeze: bool,
    operator_confirms_no_strategy_runtime_migration: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_EXCHANGE_CALENDAR_FREEZE,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for the exchange-calendar freeze ceremony."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_calendar_candidate_digest": operator_confirms_calendar_candidate_digest,
        "operator_confirms_calendar_review_package_digest": operator_confirms_calendar_review_package_digest,
        "operator_confirms_schedule_digest": operator_confirms_schedule_digest,
        "operator_confirms_identity_segment_frozen_digest": operator_confirms_identity_segment_frozen_digest,
        "operator_confirms_no_provider_requests": operator_confirms_no_provider_requests,
        "operator_confirms_no_canonical_approval": operator_confirms_no_canonical_approval,
        "operator_confirms_no_registry_approval": operator_confirms_no_registry_approval,
        "operator_confirms_no_acquisition_generation_freeze": operator_confirms_no_acquisition_generation_freeze,
        "operator_confirms_no_strategy_runtime_migration": operator_confirms_no_strategy_runtime_migration,
    }


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_EXCHANGE_CALENDAR_FREEZE, None),
            _check("operator_attestation_phrase_matches", REQUIRED_OPERATOR_ATTESTATION_PHRASE, None),
            _check("operator_calendar_candidate_digest_confirmation_matches", EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST, None),
            _check("operator_calendar_review_digest_confirmation_matches", EXPECTED_CALENDAR_REVIEW_PACKAGE_SEMANTIC_DIGEST, None),
            _check("operator_schedule_digest_confirmation_matches", EXPECTED_SCHEDULE_SEMANTIC_DIGEST, None),
            _check("operator_identity_frozen_digest_confirmation_matches", EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, None),
            *[_check(field, True, None) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_EXCHANGE_CALENDAR_FREEZE, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check(
            "operator_calendar_candidate_digest_confirmation_matches",
            EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST,
            attestation.get("operator_confirms_calendar_candidate_digest"),
        ),
        _check(
            "operator_calendar_review_digest_confirmation_matches",
            EXPECTED_CALENDAR_REVIEW_PACKAGE_SEMANTIC_DIGEST,
            attestation.get("operator_confirms_calendar_review_package_digest"),
        ),
        _check("operator_schedule_digest_confirmation_matches", EXPECTED_SCHEDULE_SEMANTIC_DIGEST, attestation.get("operator_confirms_schedule_digest")),
        _check(
            "operator_identity_frozen_digest_confirmation_matches",
            EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
            attestation.get("operator_confirms_identity_segment_frozen_digest"),
        ),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_BOUNDARY_CONFIRMATION_FIELDS],
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise ExchangeCalendarOperatorFreezeError("operator_attestation must be a JSON object")
    for field in ("operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ExchangeCalendarOperatorFreezeError(f"{field} must be a non-empty string")
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise ExchangeCalendarOperatorFreezeError(f"operator attestation failed: {failed[0]['check_id']}")
    return deepcopy(attestation)


def _frozen_calendar_binding(source_binding: dict[str, Any], schedule_digest: str) -> dict[str, Any]:
    binding = deepcopy(source_binding)
    binding["calendar_authority_status"] = CALENDAR_AUTHORITY_OPERATOR_FROZEN
    binding["calendar_operator_frozen"] = True
    binding["schedule_semantic_digest"] = schedule_digest
    return binding


def _authority_boundary() -> dict[str, Any]:
    return {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
    }


def _guardrails() -> dict[str, Any]:
    return {
        "binding_mode": EXCHANGE_CALENDAR_FROZEN_REFERENCE_ONLY,
        "provider_requests_made": False,
        "calendar_freeze_created": True,
        "acquisition_generation_created": False,
        "canonical_dataset_created": False,
        "registry_approval_created": False,
        "software_auto_approval": False,
    }


def _expected_frozen_calendar_binding() -> dict[str, Any]:
    candidate = calendar.build_exchange_calendar_evidence_candidate_v1()
    return _frozen_calendar_binding(candidate["calendar_binding"], EXPECTED_SCHEDULE_SEMANTIC_DIGEST)


def _build_freeze_checklist(frozen_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = frozen_artifact.get("operator_attestation")
    calendar_binding = frozen_artifact.get("frozen_calendar_binding", {})
    monthly = frozen_artifact.get("accepted_monthly_cross_check", {})
    return [
        _check(
            "calendar_candidate_digest_matches_expected",
            EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST,
            frozen_artifact.get("source_calendar_candidate_semantic_digest"),
        ),
        _check(
            "calendar_review_package_digest_matches_expected",
            EXPECTED_CALENDAR_REVIEW_PACKAGE_SEMANTIC_DIGEST,
            frozen_artifact.get("source_calendar_review_package_semantic_digest"),
        ),
        _check("calendar_review_package_has_zero_blockers", 0, frozen_artifact.get("source_calendar_review_blocker_count")),
        _check("schedule_digest_matches_expected", EXPECTED_SCHEDULE_SEMANTIC_DIGEST, frozen_artifact.get("schedule_semantic_digest")),
        _check(
            "identity_segment_frozen_digest_matches_expected",
            EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
            frozen_artifact.get("source_identity_segment_frozen_digest"),
        ),
        *_attestation_checks(attestation if isinstance(attestation, dict) else None),
        _check("identity_segment_is_frozen", True, frozen_artifact.get("identity_segment_frozen")),
        _check("calendar_operator_frozen_true", True, frozen_artifact.get("calendar_operator_frozen")),
        _check("calendar_binding_matches", _expected_frozen_calendar_binding(), calendar_binding),
        _check("calendar_alias_matches", calendar.CALENDAR_ALIAS, calendar_binding.get("calendar_alias") if isinstance(calendar_binding, dict) else None),
        _check(
            "calendar_source_library_matches",
            calendar.CALENDAR_SOURCE_LIBRARY,
            calendar_binding.get("calendar_source_library") if isinstance(calendar_binding, dict) else None,
        ),
        _check(
            "calendar_source_library_version_matches",
            "4.13.2",
            calendar_binding.get("calendar_source_library_version") if isinstance(calendar_binding, dict) else None,
        ),
        _check("monthly_2025_01_cross_check_matches", calendar.identity_candidate.MONTHLY_SOURCE_EVIDENCE, monthly),
        _check("canonical_eligibility_false", False, frozen_artifact.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, frozen_artifact.get("registry_eligibility")),
        _check("acquisition_generation_freeze_false", False, frozen_artifact.get("acquisition_generation_freeze")),
        _check("strategy_runtime_migration_false", False, frozen_artifact.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, frozen_artifact.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", "not accepted", frozen_artifact.get("predictive_usefulness")),
        _check("profitability_not_accepted", "not accepted", frozen_artifact.get("profitability")),
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
        "exchange_calendar_freeze_authorized_by_operator": failed == 0,
        "software_auto_approval": False,
    }


def _frozen_digest_payload(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(frozen_artifact)
    payload.pop("exchange_calendar_frozen_semantic_digest", None)
    payload.pop("frozen_payload_digest", None)
    return payload


def exchange_calendar_frozen_semantic_digest(frozen_artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for frozen exchange-calendar evidence."""
    return semantic_digest(_frozen_digest_payload(frozen_artifact))


def build_exchange_calendar_frozen_v1(
    *,
    calendar_candidate: dict[str, Any] | None = None,
    calendar_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build the offline exchange-calendar frozen artifact after operator attestation."""
    source_candidate = _source_calendar_candidate(calendar_candidate)
    source_review = _source_calendar_review_package(source_candidate, calendar_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    frozen_calendar_binding = _frozen_calendar_binding(source_candidate["calendar_binding"], source_candidate["schedule_semantic_digest"])
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_EXCHANGE_CALENDAR_FROZEN,
        "schema_version": SCHEMA_VERSION_EXCHANGE_CALENDAR_OPERATOR_FREEZE_V1,
        "freeze_status": EXCHANGE_CALENDAR_FROZEN,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "created_offline": True,
        "provider_requests_made": False,
        "automatic_stitching": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "source_calendar_candidate_kind": source_candidate["artifact_kind"],
        "source_calendar_candidate_status": source_candidate["candidate_status"],
        "source_calendar_candidate_semantic_digest": source_candidate["calendar_evidence_candidate_semantic_digest"],
        "source_calendar_review_package_kind": source_review["artifact_kind"],
        "source_calendar_review_status": source_review["review_status"],
        "source_calendar_review_package_semantic_digest": source_review["calendar_review_package_semantic_digest"],
        "source_calendar_review_checklist_total": source_review["review_summary"]["total_checks"],
        "source_calendar_review_checklist_passed": source_review["review_summary"]["passed_checks"],
        "source_calendar_review_checklist_failed": source_review["review_summary"]["failed_checks"],
        "source_calendar_review_blocker_count": source_review["review_summary"]["blocker_count"],
        "source_identity_segment_frozen_digest": source_candidate["identity_segment_frozen_digest"],
        "schedule_semantic_digest": source_candidate["schedule_semantic_digest"],
        "operator_attestation": attestation,
        "frozen_identity_segment_binding": deepcopy(source_candidate["identity_segment_binding"]),
        "acquisition_contract_digest": source_candidate["acquisition_contract"]["contract_digest"],
        "acquisition_contract": deepcopy(source_candidate["acquisition_contract"]),
        "frozen_calendar_binding": frozen_calendar_binding,
        "schedule_coverage": deepcopy(source_candidate["schedule_coverage"]),
        "accepted_monthly_cross_check": deepcopy(source_candidate["accepted_monthly_cross_check"]),
        "authority_boundary": _authority_boundary(),
        "guardrails": _guardrails(),
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_EXCHANGE_CALENDAR_FREEZE),
    }
    checklist = _build_freeze_checklist(artifact)
    artifact["freeze_checklist"] = checklist
    artifact["freeze_summary"] = _summary(checklist)
    artifact["exchange_calendar_frozen_semantic_digest"] = exchange_calendar_frozen_semantic_digest(artifact)
    validate_exchange_calendar_frozen_v1(artifact)
    return artifact


def validate_exchange_calendar_frozen_v1(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate the frozen exchange-calendar evidence artifact and return a receipt."""
    if not isinstance(frozen_artifact, dict):
        raise ExchangeCalendarOperatorFreezeError("calendar frozen artifact must be a JSON object")
    _expect(frozen_artifact.get("artifact_kind"), ARTIFACT_KIND_EXCHANGE_CALENDAR_FROZEN, "artifact_kind")
    _expect(frozen_artifact.get("schema_version"), SCHEMA_VERSION_EXCHANGE_CALENDAR_OPERATOR_FREEZE_V1, "schema_version")
    _expect(frozen_artifact.get("freeze_status"), EXCHANGE_CALENDAR_FROZEN, "freeze_status")
    _expect_true(frozen_artifact.get("identity_segment_frozen"), "identity_segment_frozen")
    _expect_true(frozen_artifact.get("calendar_operator_frozen"), "calendar_operator_frozen")
    _expect_true(frozen_artifact.get("created_offline"), "created_offline")
    _expect_false(frozen_artifact.get("provider_requests_made"), "provider_requests_made")
    _expect_false(frozen_artifact.get("automatic_stitching"), "automatic_stitching")
    for field in ("canonical_eligibility", "registry_eligibility", "acquisition_generation_freeze", "strategy_runtime_migration"):
        _expect_false(frozen_artifact.get(field), field)
    _expect(frozen_artifact.get("predictive_usefulness"), "not accepted", "predictive_usefulness")
    _expect(frozen_artifact.get("profitability"), "not accepted", "profitability")
    _expect(
        frozen_artifact.get("source_calendar_candidate_kind"),
        calendar.ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE,
        "source_calendar_candidate_kind",
    )
    _expect(
        frozen_artifact.get("source_calendar_candidate_status"),
        calendar.EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "source_calendar_candidate_status",
    )
    _expect(
        frozen_artifact.get("source_calendar_candidate_semantic_digest"),
        EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST,
        "source_calendar_candidate_semantic_digest",
    )
    _expect(
        frozen_artifact.get("source_calendar_review_package_kind"),
        review.ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE,
        "source_calendar_review_package_kind",
    )
    _expect(
        frozen_artifact.get("source_calendar_review_status"),
        review.EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY,
        "source_calendar_review_status",
    )
    _expect(
        frozen_artifact.get("source_calendar_review_package_semantic_digest"),
        EXPECTED_CALENDAR_REVIEW_PACKAGE_SEMANTIC_DIGEST,
        "source_calendar_review_package_semantic_digest",
    )
    _expect(frozen_artifact.get("source_calendar_review_checklist_total"), len(review.REQUIRED_CHECK_IDS), "source_calendar_review_checklist_total")
    _expect(frozen_artifact.get("source_calendar_review_checklist_passed"), len(review.REQUIRED_CHECK_IDS), "source_calendar_review_checklist_passed")
    _expect(frozen_artifact.get("source_calendar_review_checklist_failed"), 0, "source_calendar_review_checklist_failed")
    _expect(frozen_artifact.get("source_calendar_review_blocker_count"), 0, "source_calendar_review_blocker_count")
    _expect(frozen_artifact.get("source_identity_segment_frozen_digest"), EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, "source_identity_segment_frozen_digest")
    _expect(frozen_artifact.get("schedule_semantic_digest"), EXPECTED_SCHEDULE_SEMANTIC_DIGEST, "schedule_semantic_digest")
    _validated_operator_attestation(frozen_artifact.get("operator_attestation"))
    expected_candidate = calendar.build_exchange_calendar_evidence_candidate_v1()
    _expect(
        frozen_artifact.get("frozen_identity_segment_binding"),
        expected_candidate["identity_segment_binding"],
        "frozen_identity_segment_binding",
    )
    _expect(
        frozen_artifact.get("acquisition_contract_digest"),
        expected_candidate["acquisition_contract"]["contract_digest"],
        "acquisition_contract_digest",
    )
    _expect(frozen_artifact.get("acquisition_contract"), expected_candidate["acquisition_contract"], "acquisition_contract")
    _expect(frozen_artifact.get("frozen_calendar_binding"), _expected_frozen_calendar_binding(), "frozen_calendar_binding")
    _expect(frozen_artifact.get("schedule_coverage"), expected_candidate["schedule_coverage"], "schedule_coverage")
    _expect(frozen_artifact.get("accepted_monthly_cross_check"), expected_candidate["accepted_monthly_cross_check"], "accepted_monthly_cross_check")
    _expect(frozen_artifact.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    _expect(frozen_artifact.get("guardrails"), _guardrails(), "guardrails")

    checklist = _build_freeze_checklist(frozen_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_FREEZE_CHECK_IDS, "freeze_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise ExchangeCalendarOperatorFreezeError(f"freeze checklist contains failed check: {failed[0]['check_id']}")
    _expect(frozen_artifact.get("freeze_checklist"), checklist, "freeze_checklist")
    summary = _summary(checklist)
    _expect(frozen_artifact.get("freeze_summary"), summary, "freeze_summary")
    _expect_true(summary.get("exchange_calendar_freeze_authorized_by_operator"), "exchange_calendar_freeze_authorized_by_operator")
    _expect_false(summary.get("software_auto_approval"), "software_auto_approval")
    _expect(frozen_artifact.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_EXCHANGE_CALENDAR_FREEZE, "remaining_roadmap")

    digest = exchange_calendar_frozen_semantic_digest(frozen_artifact)
    _expect(
        frozen_artifact.get("exchange_calendar_frozen_semantic_digest"),
        digest,
        "exchange_calendar_frozen_semantic_digest",
    )
    return {
        "status": "EXCHANGE_CALENDAR_FROZEN_VALID",
        "artifact_kind": ARTIFACT_KIND_EXCHANGE_CALENDAR_FROZEN,
        "freeze_status": EXCHANGE_CALENDAR_FROZEN,
        "source_calendar_candidate_semantic_digest": EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST,
        "source_calendar_review_package_semantic_digest": EXPECTED_CALENDAR_REVIEW_PACKAGE_SEMANTIC_DIGEST,
        "source_identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "exchange_calendar_frozen_semantic_digest": digest,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "exchange_calendar_freeze_authorized_by_operator": True,
        "software_auto_approval": False,
        "provider_requests_made": False,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
    }


def write_exchange_calendar_frozen_v1(
    output_dir: str | Path,
    *,
    calendar_candidate: dict[str, Any] | None = None,
    calendar_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the frozen exchange-calendar JSON artifact without overwriting output."""
    frozen = build_exchange_calendar_frozen_v1(
        calendar_candidate=calendar_candidate,
        calendar_review_package=calendar_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_exchange_calendar_frozen_v1(frozen)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_exchange_calendar_frozen_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ExchangeCalendarOperatorFreezeError("exchange calendar frozen artifact filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise ExchangeCalendarOperatorFreezeError("exchange calendar frozen output already exists")
    payload = canonical_json_bytes(frozen)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "frozen_payload_digest": sha256_bytes(payload),
    }


def build_exchange_calendar_frozen_markdown_v1(frozen_artifact: dict[str, Any]) -> str:
    """Build a compact Markdown view of validated frozen exchange-calendar evidence."""
    validation = validate_exchange_calendar_frozen_v1(frozen_artifact)
    attestation = frozen_artifact["operator_attestation"]
    identity = frozen_artifact["frozen_identity_segment_binding"]
    binding = frozen_artifact["frozen_calendar_binding"]
    coverage = frozen_artifact["schedule_coverage"]
    authority = frozen_artifact["authority_boundary"]
    lines = [
        "# Exchange Calendar Frozen v1",
        "",
        "## Frozen Calendar Evidence",
        f"- Ticker: `{identity['ticker']}`",
        f"- Requested calendar: `{binding['requested_calendar']}`",
        f"- Resolved calendar: `{binding['resolved_calendar']}`",
        f"- Calendar alias: `{binding['calendar_alias']}`",
        f"- Calendar authority status: `{binding['calendar_authority_status']}`",
        f"- Frozen artifact digest: `{validation['exchange_calendar_frozen_semantic_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        f"- Attestation phrase: `{attestation['operator_attestation_phrase']}`",
        "",
        "## Source Candidate",
        f"- Artifact kind: `{frozen_artifact['source_calendar_candidate_kind']}`",
        f"- Candidate status: `{frozen_artifact['source_calendar_candidate_status']}`",
        f"- Calendar candidate digest: `{frozen_artifact['source_calendar_candidate_semantic_digest']}`",
        f"- Schedule digest: `{frozen_artifact['schedule_semantic_digest']}`",
        "",
        "## Source Review Package",
        f"- Artifact kind: `{frozen_artifact['source_calendar_review_package_kind']}`",
        f"- Review status: `{frozen_artifact['source_calendar_review_status']}`",
        f"- Review package digest: `{frozen_artifact['source_calendar_review_package_semantic_digest']}`",
        f"- Review checks: `{validation['passed_checks']}` passed of `{validation['total_checks']}`",
        f"- Blockers: `{validation['blocker_count']}`",
        "",
        "## Schedule Coverage",
        f"- Range: `{coverage['range_start']}` through `{coverage['range_end']}`",
        f"- Open sessions: `{coverage['session_count']}`",
        f"- Full sessions: `{coverage['full_session_count']}`",
        f"- Half sessions: `{coverage['half_session_count']}`",
        f"- First session: `{coverage['first_session']}`",
        f"- Last session: `{coverage['last_session']}`",
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
    lines.extend(f"{index}. {task}" for index, task in enumerate(REMAINING_ROADMAP_AFTER_EXCHANGE_CALENDAR_FREEZE, start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider requests were made.",
            "- No split or dividend event evidence is refreshed.",
            "- No acquisition bars are generated or frozen.",
            "- No canonical or registry eligibility is approved.",
            "- No Strategy, runtime, broker, or execution behavior is changed.",
            "- Predictive usefulness and profitability remain not accepted.",
        ]
    )
    return "\n".join(lines) + "\n"
