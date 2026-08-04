"""Offline operator-review package for exchange-calendar evidence candidates."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import exchange_calendar_evidence_service as calendar


ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE = "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE"
SCHEMA_VERSION_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_V1 = "exchange_calendar_evidence_candidate_review_v1"
EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY = "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY"
EXCHANGE_CALENDAR_FROZEN = "EXCHANGE_CALENDAR_FROZEN"

EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST = "867aa02ad9c9c737eda3d8398eda4e4aad3181cd4bc5505600ccf9647b0d60ee"
EXPECTED_SCHEDULE_SEMANTIC_DIGEST = "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
HIGH = "HIGH"
INFO = "INFO"

REMAINING_REQUIRED_TASKS = [
    "Digest-bound calendar operator freeze ceremony.",
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
    "candidate_kind_is_exchange_calendar_evidence_candidate",
    "candidate_status_ready_for_operator_review",
    "calendar_candidate_digest_matches_expected",
    "schedule_semantic_digest_matches_expected",
    "identity_segment_frozen_digest_matches",
    "identity_segment_is_frozen",
    "segment_ticker_matches",
    "segment_composite_figi_matches",
    "segment_share_class_figi_matches",
    "segment_primary_mic_matches",
    "segment_security_type_matches",
    "segment_start_matches",
    "segment_end_matches",
    "contract_digest_matches",
    "requested_calendar_matches",
    "resolved_calendar_matches",
    "calendar_alias_matches",
    "calendar_timezone_matches",
    "canonical_storage_timezone_matches",
    "calendar_source_library_matches",
    "calendar_source_library_version_matches",
    "calendar_authority_status_not_operator_frozen",
    "calendar_operator_frozen_false",
    "schedule_digest_present",
    "schedule_stats_internally_consistent",
    "monthly_2025_01_expected_rth_rows_match",
    "monthly_2025_01_validated_rth_rows_match",
    "monthly_2025_01_full_sessions_match",
    "monthly_2025_01_incomplete_sessions_match",
    "monthly_2025_01_swing_bars_match",
    "monthly_2025_01_position_swing_bars_match",
    "provider_requests_made_false",
    "automatic_stitching_false",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "acquisition_generation_freeze_false",
    "strategy_runtime_migration_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "no_exchange_calendar_frozen_artifact_created",
]

FORBIDDEN_FREEZE_FIELDS = frozenset(
    {
        "operator_approved_by",
        "operator_freeze_timestamp",
        "operator_freeze_digest",
        "operator_signature",
    }
)


class ExchangeCalendarOperatorReviewError(ValueError):
    """Raised when a calendar review package violates review boundaries."""


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
        "message": message or ("calendar candidate evidence matches" if status == PASS else "calendar candidate evidence mismatch"),
    }


def _schedule_stats_consistent(coverage: dict[str, Any]) -> dict[str, Any]:
    try:
        session_count = int(coverage.get("session_count"))
        full_session_count = int(coverage.get("full_session_count"))
        half_session_count = int(coverage.get("half_session_count"))
    except (TypeError, ValueError):
        return {"session_count_gte_full_session_count": False, "first_session_lte_last_session": False, "half_session_count_nonnegative": False}
    return {
        "session_count_gte_full_session_count": session_count >= full_session_count,
        "first_session_lte_last_session": str(coverage.get("first_session", "")) <= str(coverage.get("last_session", "")),
        "half_session_count_nonnegative": half_session_count >= 0,
    }


def _build_checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    identity = candidate.get("identity_segment_binding", {})
    acquisition = candidate.get("acquisition_contract", {})
    calendar_binding = candidate.get("calendar_binding", {})
    coverage = candidate.get("schedule_coverage", {})
    monthly = candidate.get("accepted_monthly_cross_check", {})
    authority = candidate.get("authority_boundary", {})
    return [
        _check(
            "candidate_kind_is_exchange_calendar_evidence_candidate",
            calendar.ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE,
            candidate.get("artifact_kind"),
        ),
        _check(
            "candidate_status_ready_for_operator_review",
            calendar.EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
            candidate.get("candidate_status"),
        ),
        _check(
            "calendar_candidate_digest_matches_expected",
            EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST,
            candidate.get("calendar_evidence_candidate_semantic_digest"),
        ),
        _check("schedule_semantic_digest_matches_expected", EXPECTED_SCHEDULE_SEMANTIC_DIGEST, candidate.get("schedule_semantic_digest")),
        _check(
            "identity_segment_frozen_digest_matches",
            calendar.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
            candidate.get("identity_segment_frozen_digest"),
        ),
        _check("identity_segment_is_frozen", True, candidate.get("identity_segment_frozen")),
        _check("segment_ticker_matches", "AAPL", identity.get("ticker")),
        _check("segment_composite_figi_matches", "BBG000B9XRY4", identity.get("composite_figi")),
        _check("segment_share_class_figi_matches", "BBG001S5N8V8", identity.get("share_class_figi")),
        _check("segment_primary_mic_matches", "XNAS", identity.get("primary_mic")),
        _check("segment_security_type_matches", "CS", identity.get("security_type")),
        _check("segment_start_matches", "2022-01-01", identity.get("segment_start")),
        _check("segment_end_matches", "2025-12-31", identity.get("segment_end")),
        _check("contract_digest_matches", calendar.identity_candidate.ACQUISITION_CONTRACT_V2_1_DIGEST, acquisition.get("contract_digest")),
        _check("requested_calendar_matches", calendar.REQUESTED_CALENDAR, calendar_binding.get("requested_calendar")),
        _check("resolved_calendar_matches", calendar.RESOLVED_CALENDAR, calendar_binding.get("resolved_calendar")),
        _check("calendar_alias_matches", calendar.CALENDAR_ALIAS, calendar_binding.get("calendar_alias")),
        _check("calendar_timezone_matches", "America/New_York", calendar_binding.get("calendar_timezone")),
        _check("canonical_storage_timezone_matches", "UTC", calendar_binding.get("canonical_storage_timezone")),
        _check("calendar_source_library_matches", calendar.CALENDAR_SOURCE_LIBRARY, calendar_binding.get("calendar_source_library")),
        _check("calendar_source_library_version_matches", "4.13.2", calendar_binding.get("calendar_source_library_version")),
        _check(
            "calendar_authority_status_not_operator_frozen",
            calendar.CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN,
            calendar_binding.get("calendar_authority_status"),
            severity=INFO,
        ),
        _check("calendar_operator_frozen_false", False, candidate.get("calendar_operator_frozen")),
        _check("schedule_digest_present", True, isinstance(candidate.get("schedule_semantic_digest"), str) and bool(candidate.get("schedule_semantic_digest"))),
        _check(
            "schedule_stats_internally_consistent",
            {
                "session_count_gte_full_session_count": True,
                "first_session_lte_last_session": True,
                "half_session_count_nonnegative": True,
            },
            _schedule_stats_consistent(coverage) if isinstance(coverage, dict) else {},
            severity=HIGH,
        ),
        _check("monthly_2025_01_expected_rth_rows_match", 520, monthly.get("expected_rth_rows")),
        _check("monthly_2025_01_validated_rth_rows_match", 520, monthly.get("validated_rth_rows")),
        _check("monthly_2025_01_full_sessions_match", 20, monthly.get("full_ordinary_sessions")),
        _check("monthly_2025_01_incomplete_sessions_match", 0, monthly.get("incomplete_ordinary_sessions")),
        _check("monthly_2025_01_swing_bars_match", 40, monthly.get("swing_rth_half_session_195m_bars")),
        _check("monthly_2025_01_position_swing_bars_match", 20, monthly.get("position_swing_rth_full_session_1d_bars")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("automatic_stitching_false", False, authority.get("automatic_stitching")),
        _check("canonical_eligibility_false", False, authority.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, authority.get("registry_eligibility")),
        _check("acquisition_generation_freeze_false", False, authority.get("acquisition_generation_freeze")),
        _check("strategy_runtime_migration_false", False, authority.get("strategy_runtime_migration")),
        _check("predictive_usefulness_not_accepted", "not accepted", authority.get("predictive_usefulness"), severity=INFO),
        _check("profitability_not_accepted", "not accepted", authority.get("profitability"), severity=INFO),
        _check(
            "no_exchange_calendar_frozen_artifact_created",
            {"artifact_kind_is_not_frozen": True, "candidate_status_is_not_frozen": True, "calendar_freeze_created": False},
            {
                "artifact_kind_is_not_frozen": candidate.get("artifact_kind") != EXCHANGE_CALENDAR_FROZEN,
                "candidate_status_is_not_frozen": candidate.get("candidate_status") != EXCHANGE_CALENDAR_FROZEN,
                "calendar_freeze_created": candidate.get("guardrails", {}).get("calendar_freeze_created"),
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
    payload.pop("calendar_review_package_semantic_digest", None)
    payload.pop("calendar_review_package_payload_digest", None)
    return payload


def calendar_review_package_semantic_digest(review_package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the calendar review package."""
    return semantic_digest(_package_digest_payload(review_package))


def build_exchange_calendar_evidence_candidate_review_package_v1(candidate: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a digest-bound offline operator-review package for a calendar candidate."""
    reviewed_candidate = deepcopy(candidate) if candidate is not None else calendar.build_exchange_calendar_evidence_candidate_v1()
    checklist = _build_checklist(reviewed_candidate)
    package: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_V1,
        "review_status": EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY,
        "operator_decision_required": True,
        "operator_decision": None,
        "calendar_operator_frozen": False,
        "created_offline": True,
        "provider_requests_made": False,
        "automatic_stitching": False,
        "reviewed_candidate_kind": reviewed_candidate.get("artifact_kind"),
        "reviewed_candidate_status": reviewed_candidate.get("candidate_status"),
        "reviewed_calendar_candidate_semantic_digest": reviewed_candidate.get("calendar_evidence_candidate_semantic_digest"),
        "reviewed_schedule_semantic_digest": reviewed_candidate.get("schedule_semantic_digest"),
        "candidate_binding": {
            "identity_segment_binding": deepcopy(reviewed_candidate.get("identity_segment_binding")),
            "calendar_binding": deepcopy(reviewed_candidate.get("calendar_binding")),
            "acquisition_contract": deepcopy(reviewed_candidate.get("acquisition_contract")),
            "schedule_coverage": deepcopy(reviewed_candidate.get("schedule_coverage")),
            "accepted_monthly_cross_check": deepcopy(reviewed_candidate.get("accepted_monthly_cross_check")),
            "authority_boundary": deepcopy(reviewed_candidate.get("authority_boundary")),
            "guardrails": deepcopy(reviewed_candidate.get("guardrails")),
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
    package["calendar_review_package_semantic_digest"] = calendar_review_package_semantic_digest(package)
    return package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key in {"artifact_kind", "review_status", "reviewed_candidate_kind", "reviewed_candidate_status", "candidate_status", "freeze_status"}:
            if value == EXCHANGE_CALENDAR_FROZEN:
                raise ExchangeCalendarOperatorReviewError(f"{current_path} must not emit EXCHANGE_CALENDAR_FROZEN")
        if key in FORBIDDEN_FREEZE_FIELDS and value is not None:
            raise ExchangeCalendarOperatorReviewError(f"{current_path} must be null")
        if key == "freeze_status" and value is not None:
            raise ExchangeCalendarOperatorReviewError(f"{current_path} must be null")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise ExchangeCalendarOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ExchangeCalendarOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ExchangeCalendarOperatorReviewError(f"{field_name} must be true")


def validate_exchange_calendar_evidence_candidate_review_package_v1(review_package: dict[str, Any]) -> dict[str, Any]:
    """Validate the calendar operator-review package and fail closed on failed checks."""
    if not isinstance(review_package, dict):
        raise ExchangeCalendarOperatorReviewError("calendar review package must be a JSON object")
    _reject_forbidden_values(review_package)
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY, "review_status")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    _expect_false(review_package.get("calendar_operator_frozen"), "calendar_operator_frozen")
    _expect_true(review_package.get("created_offline"), "created_offline")
    _expect_false(review_package.get("provider_requests_made"), "provider_requests_made")
    _expect_false(review_package.get("automatic_stitching"), "automatic_stitching")
    _expect(
        review_package.get("reviewed_candidate_kind"),
        calendar.ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE,
        "reviewed_candidate_kind",
    )
    _expect(
        review_package.get("reviewed_candidate_status"),
        calendar.EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "reviewed_candidate_status",
    )
    _expect(
        review_package.get("reviewed_calendar_candidate_semantic_digest"),
        EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST,
        "reviewed_calendar_candidate_semantic_digest",
    )
    _expect(review_package.get("reviewed_schedule_semantic_digest"), EXPECTED_SCHEDULE_SEMANTIC_DIGEST, "reviewed_schedule_semantic_digest")

    binding = review_package.get("candidate_binding")
    if not isinstance(binding, dict):
        raise ExchangeCalendarOperatorReviewError("candidate_binding must be a JSON object")
    expected_candidate = calendar.build_exchange_calendar_evidence_candidate_v1()
    _expect(binding.get("identity_segment_binding"), expected_candidate["identity_segment_binding"], "candidate_binding.identity_segment_binding")
    _expect(binding.get("calendar_binding"), expected_candidate["calendar_binding"], "candidate_binding.calendar_binding")
    _expect(binding.get("acquisition_contract"), expected_candidate["acquisition_contract"], "candidate_binding.acquisition_contract")
    _expect(binding.get("schedule_coverage"), expected_candidate["schedule_coverage"], "candidate_binding.schedule_coverage")
    _expect(binding.get("accepted_monthly_cross_check"), expected_candidate["accepted_monthly_cross_check"], "candidate_binding.accepted_monthly_cross_check")
    _expect(binding.get("authority_boundary"), expected_candidate["authority_boundary"], "candidate_binding.authority_boundary")
    _expect(binding.get("guardrails"), expected_candidate["guardrails"], "candidate_binding.guardrails")

    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ExchangeCalendarOperatorReviewError("review_checklist must be a list")
    check_ids = [item.get("check_id") for item in checklist if isinstance(item, dict)]
    _expect(check_ids, REQUIRED_CHECK_IDS, "review_checklist check IDs")
    candidate_from_binding = {
        "artifact_kind": review_package.get("reviewed_candidate_kind"),
        "candidate_status": review_package.get("reviewed_candidate_status"),
        "calendar_evidence_candidate_semantic_digest": review_package.get("reviewed_calendar_candidate_semantic_digest"),
        "schedule_semantic_digest": review_package.get("reviewed_schedule_semantic_digest"),
        "identity_segment_frozen": binding["identity_segment_binding"].get("identity_segment_frozen"),
        "identity_segment_frozen_digest": binding["identity_segment_binding"].get("identity_segment_frozen_digest"),
        "identity_segment_binding": binding["identity_segment_binding"],
        "calendar_operator_frozen": review_package.get("calendar_operator_frozen"),
        "provider_requests_made": review_package.get("provider_requests_made"),
        "acquisition_contract": binding["acquisition_contract"],
        "calendar_binding": binding["calendar_binding"],
        "schedule_coverage": binding["schedule_coverage"],
        "accepted_monthly_cross_check": binding["accepted_monthly_cross_check"],
        "authority_boundary": binding["authority_boundary"],
        "guardrails": binding["guardrails"],
    }
    _expect(checklist, _build_checklist(candidate_from_binding), "review_checklist")
    failed = [item for item in checklist if item.get("status") != PASS]
    if failed:
        raise ExchangeCalendarOperatorReviewError("calendar review package contains failed checks")

    expected_summary = _summary(checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    summary = review_package["review_summary"]
    _expect_true(summary.get("ready_for_operator_assessment"), "ready_for_operator_assessment")
    _expect_true(summary.get("operator_decision_required_before_freeze"), "operator_decision_required_before_freeze")
    _expect_false(summary.get("software_freeze_authorized"), "software_freeze_authorized")
    _expect(review_package.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")

    controls = review_package.get("operator_freeze_controls")
    if not isinstance(controls, dict):
        raise ExchangeCalendarOperatorReviewError("operator_freeze_controls must be a JSON object")
    for field in ("operator_approved_by", "operator_freeze_timestamp", "operator_freeze_digest", "operator_signature", "freeze_status"):
        _expect(controls.get(field), None, f"operator_freeze_controls.{field}")

    digest = calendar_review_package_semantic_digest(review_package)
    _expect(review_package.get("calendar_review_package_semantic_digest"), digest, "calendar_review_package_semantic_digest")
    return {
        "status": "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE,
        "review_status": EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_READY,
        "reviewed_calendar_candidate_semantic_digest": EXPECTED_CALENDAR_CANDIDATE_SEMANTIC_DIGEST,
        "reviewed_schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "calendar_review_package_semantic_digest": digest,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "provider_requests_made": False,
        "calendar_operator_frozen": False,
        "software_freeze_authorized": False,
    }


def write_exchange_calendar_evidence_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the calendar review package JSON artifact without overwriting output."""
    review_package = build_exchange_calendar_evidence_candidate_review_package_v1(candidate)
    validation = validate_exchange_calendar_evidence_candidate_review_package_v1(review_package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_exchange_calendar_evidence_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ExchangeCalendarOperatorReviewError("calendar review package filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise ExchangeCalendarOperatorReviewError("exchange calendar review package output already exists")
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "calendar_review_package_payload_digest": sha256_bytes(payload),
    }


def build_exchange_calendar_evidence_candidate_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Build a compact Markdown view of a validated calendar review package."""
    validation = validate_exchange_calendar_evidence_candidate_review_package_v1(review_package)
    binding = review_package["candidate_binding"]
    identity = binding["identity_segment_binding"]
    calendar_binding = binding["calendar_binding"]
    coverage = binding["schedule_coverage"]
    monthly = binding["accepted_monthly_cross_check"]
    authority = binding["authority_boundary"]
    failed_checks = [item for item in review_package["review_checklist"] if item["status"] != PASS]
    lines = [
        "# Exchange Calendar Evidence Candidate Review Package v1",
        "",
        "## Reviewed Calendar Candidate",
        f"- Artifact kind: `{review_package['reviewed_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_candidate_status']}`",
        f"- Calendar candidate digest: `{review_package['reviewed_calendar_candidate_semantic_digest']}`",
        f"- Review package digest: `{validation['calendar_review_package_semantic_digest']}`",
        "",
        "## Frozen Identity Segment Binding",
        f"- Ticker: `{identity['ticker']}`",
        f"- Composite FIGI: `{identity['composite_figi']}`",
        f"- Share Class FIGI: `{identity['share_class_figi']}`",
        f"- Primary MIC: `{identity['primary_mic']}`",
        f"- Security type: `{identity['security_type']}`",
        f"- Range: `{identity['segment_start']}` through `{identity['segment_end']}`",
        f"- Frozen identity digest: `{identity['identity_segment_frozen_digest']}`",
        "",
        "## Calendar Binding",
        f"- Requested calendar: `{calendar_binding['requested_calendar']}`",
        f"- Resolved calendar: `{calendar_binding['resolved_calendar']}`",
        f"- Alias: `{calendar_binding['calendar_alias']}`",
        f"- Source library: `{calendar_binding['calendar_source_library']}` `{calendar_binding['calendar_source_library_version']}`",
        "",
        "## Schedule Evidence",
        f"- Schedule digest: `{review_package['reviewed_schedule_semantic_digest']}`",
        f"- Sessions: `{coverage['session_count']}`",
        f"- Full sessions: `{coverage['full_session_count']}`",
        f"- Half sessions: `{coverage['half_session_count']}`",
        "",
        "## 2025-01 Monthly Cross-Check",
        f"- Expected RTH rows: `{monthly['expected_rth_rows']}`",
        f"- Validated RTH rows: `{monthly['validated_rth_rows']}`",
        f"- Full ordinary sessions: `{monthly['full_ordinary_sessions']}`",
        f"- Incomplete ordinary sessions: `{monthly['incomplete_ordinary_sessions']}`",
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
            "- No `EXCHANGE_CALENDAR_FROZEN` artifact or status is created.",
            "- Operator decision remains required before any future calendar freeze ceremony.",
        ]
    )
    return "\n".join(lines) + "\n"
