"""Offline exchange-calendar evidence candidate helpers."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from marketflow.historical_data import frozen_calendar
from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import identity_segment_freeze_service as identity_candidate
from marketflow.services import identity_segment_operator_freeze_service as identity_freeze


ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE = "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE"
SCHEMA_VERSION_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_V1 = "exchange_calendar_evidence_candidate_v1"
EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW = "EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW"

EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST = "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
CALENDAR_EVIDENCE_CANDIDATE_ONLY = "CALENDAR_EVIDENCE_CANDIDATE_ONLY"
CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN = identity_candidate.CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN
REQUESTED_CALENDAR = "XNAS"
RESOLVED_CALENDAR = "XNYS"
CALENDAR_ALIAS = "XNAS_USES_XNYS_SCHEDULE"
CALENDAR_SOURCE_LIBRARY = "exchange_calendars"
CALENDAR_SOURCE_AUTHORITY = "LOCAL_EXCHANGE_CALENDARS_XNYS_ALIAS_CANDIDATE"
SOURCE_BAR_INTERVAL_MINUTES = 15
RTH_HALF_SESSION_195M_BARS_PER_FULL_SESSION = 2
POSITION_SWING_FULL_SESSION_1D_BARS_PER_FULL_SESSION = 1

REMAINING_ROADMAP_AFTER_CALENDAR_CANDIDATE = [
    "Operator review package for exchange-calendar evidence.",
    "Digest-bound operator freeze ceremony for exchange-calendar evidence.",
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


class ExchangeCalendarEvidenceError(ValueError):
    """Raised when calendar evidence candidate validation fails."""


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise ExchangeCalendarEvidenceError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ExchangeCalendarEvidenceError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ExchangeCalendarEvidenceError(f"{field_name} must be true")


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _calendar_candidate() -> frozen_calendar.FrozenCalendar:
    request = frozen_calendar.default_calendar_request(
        requested_primary_listing_mic=REQUESTED_CALENDAR,
        requested_calendar_token=REQUESTED_CALENDAR,
        official_exchange_evidence_identity="OPERATOR_SUPPLIED_OFFICIAL_EXCHANGE_EVIDENCE_PENDING_FREEZE",
        official_exchange_evidence_digest="OFFICIAL_EVIDENCE_DIGEST_PENDING",
    )
    return frozen_calendar.generate_frozen_calendar(request)


def build_exchange_calendar_schedule_rows_v1() -> list[dict[str, Any]]:
    """Build deterministic open-session schedule rows for the fixed XNAS/XNYS range."""
    calendar = _calendar_candidate()
    rows: list[dict[str, Any]] = []
    for session in calendar.sessions:
        if session.session_classification == frozen_calendar.FULL_MARKET_CLOSED:
            continue
        if session.market_open_utc is None or session.market_close_utc is None:
            raise ExchangeCalendarEvidenceError("open session is missing market timestamps")
        session_minutes = int((_parse_utc(session.market_close_utc) - _parse_utc(session.market_open_utc)).total_seconds() // 60)
        rows.append(
            {
                "session_date": session.session_date,
                "market_open_utc": session.market_open_utc,
                "market_close_utc": session.market_close_utc,
                "market_open_local": session.market_open_local,
                "market_close_local": session.market_close_local,
                "session_minutes": session_minutes,
                "is_full_session": session.session_classification == frozen_calendar.NORMAL_FULL_SESSION,
                "is_half_session": session.session_classification == frozen_calendar.EARLY_CLOSE_SESSION,
            }
        )
    return rows


def schedule_semantic_digest(schedule_rows: list[dict[str, Any]] | None = None) -> str:
    """Return the deterministic digest for the fixed calendar schedule evidence."""
    rows = deepcopy(schedule_rows) if schedule_rows is not None else build_exchange_calendar_schedule_rows_v1()
    payload = {
        "schema_version": "exchange_calendar_schedule_rows_v1",
        "requested_calendar": REQUESTED_CALENDAR,
        "resolved_calendar": RESOLVED_CALENDAR,
        "calendar_alias": CALENDAR_ALIAS,
        "range_start": identity_candidate.FIXED_ACQUISITION_START,
        "range_end": identity_candidate.FIXED_ACQUISITION_END,
        "rows": rows,
    }
    return semantic_digest(payload)


def _schedule_coverage(schedule_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not schedule_rows:
        raise ExchangeCalendarEvidenceError("schedule evidence must include open sessions")
    full_session_count = sum(1 for row in schedule_rows if row["is_full_session"] is True)
    half_session_count = sum(1 for row in schedule_rows if row["is_half_session"] is True)
    return {
        "range_start": identity_candidate.FIXED_ACQUISITION_START,
        "range_end": identity_candidate.FIXED_ACQUISITION_END,
        "session_count": len(schedule_rows),
        "full_session_count": full_session_count,
        "half_session_count": half_session_count,
        "special_close_count": half_session_count,
        "special_open_count": 0,
        "first_session": schedule_rows[0]["session_date"],
        "last_session": schedule_rows[-1]["session_date"],
        "schedule_semantic_digest": schedule_semantic_digest(schedule_rows),
    }


def _identity_segment_binding() -> dict[str, Any]:
    segment = identity_candidate.SEGMENT
    return {
        "identity_segment_artifact_kind": identity_freeze.ARTIFACT_KIND_IDENTITY_SEGMENT_FROZEN,
        "identity_segment_freeze_status": identity_freeze.IDENTITY_SEGMENT_FROZEN,
        "identity_segment_frozen": True,
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "ticker": segment["ticker"],
        "composite_figi": segment["composite_figi"],
        "share_class_figi": segment["share_class_figi"],
        "primary_mic": segment["primary_mic"],
        "security_type": segment["security_type"],
        "segment_start": segment["segment_start"],
        "segment_end": segment["segment_end"],
    }


def _calendar_binding(calendar_version: str) -> dict[str, Any]:
    return {
        "requested_calendar": REQUESTED_CALENDAR,
        "resolved_calendar": RESOLVED_CALENDAR,
        "calendar_alias": CALENDAR_ALIAS,
        "calendar_timezone": frozen_calendar.SOURCE_TIMEZONE,
        "canonical_storage_timezone": frozen_calendar.CANONICAL_TIMEZONE,
        "calendar_source_library": CALENDAR_SOURCE_LIBRARY,
        "calendar_source_library_version": calendar_version,
        "calendar_source_authority": CALENDAR_SOURCE_AUTHORITY,
        "calendar_authority_status": CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN,
    }


def _rth_bar_derivation_rules() -> dict[str, Any]:
    return {
        "source_bar_interval_minutes": SOURCE_BAR_INTERVAL_MINUTES,
        "source_timestamps_are_aggregate_window_starts": True,
        "rth_half_session_195m_bars_per_full_session": RTH_HALF_SESSION_195M_BARS_PER_FULL_SESSION,
        "position_swing_full_session_1d_bars_per_full_session": POSITION_SWING_FULL_SESSION_1D_BARS_PER_FULL_SESSION,
        "canonical_storage_timezone": frozen_calendar.CANONICAL_TIMEZONE,
    }


def _accepted_monthly_cross_check() -> dict[str, Any]:
    return deepcopy(identity_candidate.MONTHLY_SOURCE_EVIDENCE)


def _authority_boundary() -> dict[str, Any]:
    return {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": identity_candidate.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": identity_candidate.PROFITABILITY_NOT_ACCEPTED,
    }


def _guardrails() -> dict[str, Any]:
    return {
        "binding_mode": CALENDAR_EVIDENCE_CANDIDATE_ONLY,
        "provider_requests_made": False,
        "calendar_freeze_created": False,
        "acquisition_generation_created": False,
        "canonical_dataset_created": False,
        "registry_approval_created": False,
    }


def _candidate_digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("calendar_evidence_candidate_semantic_digest", None)
    payload.pop("calendar_evidence_candidate_payload_digest", None)
    return payload


def calendar_evidence_candidate_semantic_digest(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the calendar candidate."""
    return semantic_digest(_candidate_digest_payload(candidate))


def build_exchange_calendar_evidence_candidate_v1() -> dict[str, Any]:
    """Build the fixed offline exchange-calendar evidence candidate."""
    version = frozen_calendar.require_exchange_calendar_pin()
    calendar = _calendar_candidate()
    if calendar.resolved_calendar != RESOLVED_CALENDAR or calendar.calendar_alias_relationship != CALENDAR_ALIAS:
        raise ExchangeCalendarEvidenceError("calendar alias resolution mismatch")
    schedule_rows = build_exchange_calendar_schedule_rows_v1()
    coverage = _schedule_coverage(schedule_rows)
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE,
        "schema_version": SCHEMA_VERSION_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_V1,
        "candidate_status": EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "operator_review_required": True,
        "operator_freeze_required": True,
        "calendar_operator_frozen": False,
        "created_offline": True,
        "provider_requests_made": False,
        "identity_segment_frozen": True,
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "acquisition_contract": {
            "contract": identity_candidate.CORE_ACQUISITION_CONTRACT_V2_1,
            "contract_digest": identity_candidate.ACQUISITION_CONTRACT_V2_1_DIGEST,
            "fixed_acquisition_range": {
                "start": identity_candidate.FIXED_ACQUISITION_START,
                "end": identity_candidate.FIXED_ACQUISITION_END,
            },
            "source": {
                "provider": "Massive.com Custom Bars",
                "interval": "15-minute",
                "adjustment": "Adjusted",
                "sort": "Ascending",
                "source_timestamp_semantic": "aggregate-window starts",
                "source_timezone": frozen_calendar.SOURCE_TIMEZONE,
                "canonical_storage_timezone": frozen_calendar.CANONICAL_TIMEZONE,
            },
        },
        "identity_segment_binding": _identity_segment_binding(),
        "calendar_binding": _calendar_binding(version),
        "schedule_coverage": coverage,
        "rth_bar_derivation_rules": _rth_bar_derivation_rules(),
        "accepted_monthly_cross_check": _accepted_monthly_cross_check(),
        "authority_boundary": _authority_boundary(),
        "guardrails": _guardrails(),
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_CALENDAR_CANDIDATE),
    }
    candidate["schedule_semantic_digest"] = coverage["schedule_semantic_digest"]
    candidate["calendar_evidence_candidate_semantic_digest"] = calendar_evidence_candidate_semantic_digest(candidate)
    validate_exchange_calendar_evidence_candidate_v1(candidate)
    return candidate


def _validate_identity_binding(candidate: dict[str, Any]) -> None:
    expected = _identity_segment_binding()
    _expect(candidate.get("identity_segment_frozen"), True, "identity_segment_frozen")
    _expect(candidate.get("identity_segment_frozen_digest"), EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, "identity_segment_frozen_digest")
    _expect(candidate.get("identity_segment_binding"), expected, "identity_segment_binding")


def _validate_monthly_cross_check(candidate: dict[str, Any]) -> None:
    _expect(candidate.get("accepted_monthly_cross_check"), _accepted_monthly_cross_check(), "accepted_monthly_cross_check")


def validate_exchange_calendar_evidence_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate the exchange-calendar evidence candidate and return a receipt."""
    if not isinstance(candidate, dict):
        raise ExchangeCalendarEvidenceError("calendar evidence candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    _expect_true(candidate.get("operator_review_required"), "operator_review_required")
    _expect_true(candidate.get("operator_freeze_required"), "operator_freeze_required")
    _expect_false(candidate.get("calendar_operator_frozen"), "calendar_operator_frozen")
    _expect_true(candidate.get("created_offline"), "created_offline")
    _expect_false(candidate.get("provider_requests_made"), "provider_requests_made")
    _validate_identity_binding(candidate)

    acquisition = candidate.get("acquisition_contract", {})
    _expect(acquisition.get("contract"), identity_candidate.CORE_ACQUISITION_CONTRACT_V2_1, "acquisition_contract.contract")
    _expect(acquisition.get("contract_digest"), identity_candidate.ACQUISITION_CONTRACT_V2_1_DIGEST, "acquisition_contract.contract_digest")
    _expect(
        acquisition.get("fixed_acquisition_range"),
        {"start": identity_candidate.FIXED_ACQUISITION_START, "end": identity_candidate.FIXED_ACQUISITION_END},
        "acquisition_contract.fixed_acquisition_range",
    )
    version = frozen_calendar.require_exchange_calendar_pin()
    _expect(candidate.get("calendar_binding"), _calendar_binding(version), "calendar_binding")
    coverage = candidate.get("schedule_coverage")
    if not isinstance(coverage, dict):
        raise ExchangeCalendarEvidenceError("schedule_coverage must be a JSON object")
    for field in ("range_start", "range_end", "session_count", "full_session_count", "half_session_count", "first_session", "last_session"):
        if field not in coverage:
            raise ExchangeCalendarEvidenceError(f"schedule_coverage.{field} missing")
    digest = coverage.get("schedule_semantic_digest")
    if not isinstance(digest, str) or not digest:
        raise ExchangeCalendarEvidenceError("schedule_semantic_digest missing")
    _expect(candidate.get("schedule_semantic_digest"), digest, "schedule_semantic_digest")
    _expect(coverage.get("range_start"), identity_candidate.FIXED_ACQUISITION_START, "schedule_coverage.range_start")
    _expect(coverage.get("range_end"), identity_candidate.FIXED_ACQUISITION_END, "schedule_coverage.range_end")
    if int(coverage["session_count"]) < int(coverage["full_session_count"]):
        raise ExchangeCalendarEvidenceError("session_count must be >= full_session_count")
    if str(coverage["first_session"]) > str(coverage["last_session"]):
        raise ExchangeCalendarEvidenceError("first_session must be <= last_session")
    if int(coverage["half_session_count"]) < 0:
        raise ExchangeCalendarEvidenceError("half_session_count must be nonnegative")
    _expect(candidate.get("rth_bar_derivation_rules"), _rth_bar_derivation_rules(), "rth_bar_derivation_rules")
    _validate_monthly_cross_check(candidate)

    authority = candidate.get("authority_boundary")
    _expect(authority, _authority_boundary(), "authority_boundary")
    guardrails = candidate.get("guardrails")
    _expect(guardrails, _guardrails(), "guardrails")
    _expect(candidate.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_CALENDAR_CANDIDATE, "remaining_roadmap")

    candidate_digest = candidate_evidence_digest = candidate.get("calendar_evidence_candidate_semantic_digest")
    if not isinstance(candidate_digest, str) or not candidate_digest:
        raise ExchangeCalendarEvidenceError("calendar_evidence_candidate_semantic_digest missing")
    recomputed = calendar_evidence_candidate_semantic_digest(candidate)
    _expect(candidate_evidence_digest, recomputed, "calendar_evidence_candidate_semantic_digest")
    return {
        "status": "EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE_VALID",
        "artifact_kind": ARTIFACT_KIND_EXCHANGE_CALENDAR_EVIDENCE_CANDIDATE,
        "candidate_status": EXCHANGE_CALENDAR_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "calendar_evidence_candidate_semantic_digest": recomputed,
        "schedule_semantic_digest": digest,
        "requested_calendar": REQUESTED_CALENDAR,
        "resolved_calendar": RESOLVED_CALENDAR,
        "calendar_alias": CALENDAR_ALIAS,
        "calendar_source_library": CALENDAR_SOURCE_LIBRARY,
        "calendar_source_library_version": version,
        "session_count": coverage["session_count"],
        "full_session_count": coverage["full_session_count"],
        "half_session_count": coverage["half_session_count"],
        "provider_requests_made": False,
        "calendar_operator_frozen": False,
        "identity_segment_frozen": True,
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_freeze": False,
        "strategy_runtime_migration": False,
    }


def write_exchange_calendar_evidence_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the exchange-calendar evidence candidate without overwriting output."""
    candidate = build_exchange_calendar_evidence_candidate_v1()
    validation = validate_exchange_calendar_evidence_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_exchange_calendar_evidence_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ExchangeCalendarEvidenceError("calendar evidence filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise ExchangeCalendarEvidenceError("exchange calendar evidence candidate output already exists")
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "calendar_evidence_candidate_payload_digest": sha256_bytes(payload),
    }


def build_exchange_calendar_evidence_candidate_markdown_v1(candidate: dict[str, Any]) -> str:
    """Build a compact Markdown view of a validated calendar evidence candidate."""
    validation = validate_exchange_calendar_evidence_candidate_v1(candidate)
    binding = candidate["identity_segment_binding"]
    calendar = candidate["calendar_binding"]
    coverage = candidate["schedule_coverage"]
    monthly = candidate["accepted_monthly_cross_check"]
    authority = candidate["authority_boundary"]
    lines = [
        "# Exchange Calendar Evidence Candidate v1",
        "",
        "## Purpose",
        "- Candidate-only calendar evidence for the frozen AAPL identity segment.",
        "",
        "## Frozen Identity Segment",
        f"- Ticker: `{binding['ticker']}`",
        f"- Composite FIGI: `{binding['composite_figi']}`",
        f"- Share Class FIGI: `{binding['share_class_figi']}`",
        f"- Primary MIC: `{binding['primary_mic']}`",
        f"- Security type: `{binding['security_type']}`",
        f"- Range: `{binding['segment_start']}` through `{binding['segment_end']}`",
        f"- Frozen identity digest: `{binding['identity_segment_frozen_digest']}`",
        "",
        "## Calendar Alias",
        f"- Requested calendar: `{calendar['requested_calendar']}`",
        f"- Resolved calendar: `{calendar['resolved_calendar']}`",
        f"- Alias: `{calendar['calendar_alias']}`",
        f"- Source library: `{calendar['calendar_source_library']}` `{calendar['calendar_source_library_version']}`",
        "",
        "## Schedule Coverage",
        f"- Schedule digest: `{validation['schedule_semantic_digest']}`",
        f"- Sessions: `{coverage['session_count']}`",
        f"- Full sessions: `{coverage['full_session_count']}`",
        f"- Half sessions: `{coverage['half_session_count']}`",
        f"- First session: `{coverage['first_session']}`",
        f"- Last session: `{coverage['last_session']}`",
        "",
        "## Monthly Cross-Check",
        f"- Month: `{monthly['month']}`",
        f"- Normalized source rows: `{monthly['normalized_source_rows']}`",
        f"- Extended-hours rows: `{monthly['extended_hours_rows']}`",
        f"- Expected RTH rows: `{monthly['expected_rth_rows']}`",
        f"- Validated RTH rows: `{monthly['validated_rth_rows']}`",
        f"- Full ordinary sessions: `{monthly['full_ordinary_sessions']}`",
        f"- Incomplete ordinary sessions: `{monthly['incomplete_ordinary_sessions']}`",
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
        "## Non-Goals",
        "- No provider requests were made.",
        "- No `EXCHANGE_CALENDAR_FROZEN` artifact or status is created.",
        "- No acquisition generation, canonical dataset, registry approval, runtime migration, broker, or execution behavior is changed.",
        "",
        "## Next Steps",
    ]
    lines.extend(f"{index}. {task}" for index, task in enumerate(REMAINING_ROADMAP_AFTER_CALENDAR_CANDIDATE, start=1))
    return "\n".join(lines) + "\n"
