"""Offline frozen exchange-calendar models for Contract v2.1."""

from __future__ import annotations

import hashlib
import importlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from importlib import metadata
from typing import Any
from zoneinfo import ZoneInfo

from marketflow.research import acquisition_contract_v2 as contract_v2
from marketflow.research import acquisition_contract_v2_1 as contract_v21


CALENDAR_SCHEMA_VERSION = "marketflow.frozen_calendar.v2_1"
CALENDAR_GENERATION_CODE_VERSION = "marketflow.historical_data.frozen_calendar.v1"
REQUIRED_EXCHANGE_CALENDARS_VERSION = "4.13.2"
SOURCE_TIMEZONE = "America/New_York"
CANONICAL_TIMEZONE = "UTC"

NORMAL_FULL_SESSION = "NORMAL_FULL_SESSION"
EARLY_CLOSE_SESSION = "EARLY_CLOSE_SESSION"
FULL_MARKET_CLOSED = "FULL_MARKET_CLOSED"
CALENDAR_SOURCE_UNRESOLVED = "CALENDAR_SOURCE_UNRESOLVED"
CALENDAR_CONFLICT = "CALENDAR_CONFLICT"

CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE = "CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE"
CALENDAR_READY_FOR_FREEZE_REVIEW = "CALENDAR_READY_FOR_FREEZE_REVIEW"
CALENDAR_INVALID = "CALENDAR_INVALID"
CALENDAR_IMPLEMENTATION_VERSION_MISMATCH = "CALENDAR_IMPLEMENTATION_VERSION_MISMATCH"

SUPPORTED_CALENDAR_TOKENS = {"XNYS", "XNAS", "XASE"}
EXPECTED_RESOLVED_BY_TOKEN = {"XNYS": "XNYS", "XNAS": "XNYS", "XASE": "XNYS"}


class CalendarGenerationError(ValueError):
    """Raised when an offline frozen calendar cannot be generated safely."""


def _tzdata_version() -> str:
    try:
        return metadata.version("tzdata")
    except metadata.PackageNotFoundError:
        return "SYSTEM_ZONEINFO"


def _canonicalize(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: _canonicalize(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _canonicalize(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_canonicalize(item) for item in value]
    if isinstance(value, datetime):
        return _utc_iso(value)
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return format(value, "f")
    return value


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize deterministic semantic JSON."""
    return json.dumps(
        _canonicalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def semantic_digest(value: Any) -> str:
    """Return deterministic SHA-256 digest for semantic payloads."""
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _utc_iso(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise CalendarGenerationError("timestamp must be timezone-aware")
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _ensure_utc_datetime(value: Any, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise CalendarGenerationError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise CalendarGenerationError(f"{field_name} must be timezone-aware")
    return value.astimezone(UTC)


def exchange_calendars_version() -> str:
    """Return installed exchange_calendars version without importing providers."""
    return metadata.version("exchange_calendars")


def require_exchange_calendar_pin() -> str:
    """Fail closed unless the exact accepted calendar package is installed."""
    version = exchange_calendars_version()
    if version != REQUIRED_EXCHANGE_CALENDARS_VERSION:
        raise CalendarGenerationError(CALENDAR_IMPLEMENTATION_VERSION_MISMATCH)
    return version


@dataclass(frozen=True, slots=True)
class FrozenCalendarRequest:
    schema_version: str
    contract_v2_1_digest: str
    requested_primary_listing_mic: str
    requested_calendar_token: str
    fixed_start_date: str
    fixed_end_date: str
    source_timezone: str
    canonical_timezone: str
    exchange_calendars_version: str
    tzdata_version: str
    official_exchange_evidence_identity: str
    official_exchange_evidence_digest: str
    calendar_generation_code_version: str = CALENDAR_GENERATION_CODE_VERSION

    def validate(self) -> None:
        if self.schema_version != CALENDAR_SCHEMA_VERSION:
            raise CalendarGenerationError("unsupported frozen calendar request schema")
        if self.contract_v2_1_digest != contract_v21.contract_digest(contract_v21.default_contract()):
            raise CalendarGenerationError("unexpected Contract v2.1 digest")
        if self.source_timezone != SOURCE_TIMEZONE:
            raise CalendarGenerationError("source timezone differs from Contract v2.1")
        if self.canonical_timezone != CANONICAL_TIMEZONE:
            raise CalendarGenerationError("canonical timezone differs from Contract v2.1")
        if self.exchange_calendars_version != REQUIRED_EXCHANGE_CALENDARS_VERSION:
            raise CalendarGenerationError(CALENDAR_IMPLEMENTATION_VERSION_MISMATCH)
        if self.requested_calendar_token not in SUPPORTED_CALENDAR_TOKENS:
            raise CalendarGenerationError(CALENDAR_SOURCE_UNRESOLVED)
        base_v2 = contract_v2.default_contract()
        if self.fixed_start_date != base_v2.fixed_range_policy.start_date:
            raise CalendarGenerationError("fixed start date differs from Contract v2")
        if self.fixed_end_date != base_v2.fixed_range_policy.end_date:
            raise CalendarGenerationError("fixed end date differs from Contract v2")


@dataclass(frozen=True, slots=True)
class FrozenCalendarSession:
    session_date: str
    session_classification: str
    market_open_utc: str | None
    market_close_utc: str | None
    market_open_local: str | None
    market_close_local: str | None


@dataclass(frozen=True, slots=True)
class FrozenCalendar:
    schema_version: str
    contract_v2_1_digest: str
    requested_primary_listing_mic: str
    requested_calendar_token: str
    resolved_calendar: str
    calendar_alias_relationship: str
    exchange_calendars_version: str
    tzdata_version: str
    fixed_start_date: str
    fixed_end_date: str
    source_timezone: str
    canonical_timezone: str
    official_exchange_evidence_identity: str
    official_exchange_evidence_digest: str
    status: str
    sessions: tuple[FrozenCalendarSession, ...]
    semantic_digest: str

    def session_by_date(self) -> dict[str, FrozenCalendarSession]:
        return {session.session_date: session for session in self.sessions}

    def normal_sessions(self) -> tuple[FrozenCalendarSession, ...]:
        return tuple(session for session in self.sessions if session.session_classification == NORMAL_FULL_SESSION)

    def early_close_sessions(self) -> tuple[FrozenCalendarSession, ...]:
        return tuple(session for session in self.sessions if session.session_classification == EARLY_CLOSE_SESSION)


def default_calendar_request(
    *,
    requested_primary_listing_mic: str = "XNYS",
    requested_calendar_token: str = "XNYS",
    official_exchange_evidence_identity: str = "OPERATOR_SUPPLIED_OFFICIAL_EXCHANGE_EVIDENCE_PENDING_FREEZE",
    official_exchange_evidence_digest: str = "OFFICIAL_EVIDENCE_DIGEST_PENDING",
) -> FrozenCalendarRequest:
    """Build the default non-ticker frozen calendar request."""
    version = require_exchange_calendar_pin()
    base = contract_v2.default_contract()
    contract = contract_v21.default_contract()
    contract_v21.verify_base_contract_digest(contract)
    return FrozenCalendarRequest(
        schema_version=CALENDAR_SCHEMA_VERSION,
        contract_v2_1_digest=contract_v21.contract_digest(contract),
        requested_primary_listing_mic=requested_primary_listing_mic,
        requested_calendar_token=requested_calendar_token,
        fixed_start_date=base.fixed_range_policy.start_date,
        fixed_end_date=base.fixed_range_policy.end_date,
        source_timezone=SOURCE_TIMEZONE,
        canonical_timezone=CANONICAL_TIMEZONE,
        exchange_calendars_version=version,
        tzdata_version=_tzdata_version(),
        official_exchange_evidence_identity=official_exchange_evidence_identity,
        official_exchange_evidence_digest=official_exchange_evidence_digest,
    )


def _date_range(start: date, end: date) -> tuple[date, ...]:
    days = []
    cursor = start
    while cursor <= end:
        days.append(cursor)
        cursor += timedelta(days=1)
    return tuple(days)


def generate_frozen_calendar(request: FrozenCalendarRequest) -> FrozenCalendar:
    """Generate a deterministic exchange-aware calendar preview."""
    request.validate()
    version = require_exchange_calendar_pin()
    if version != request.exchange_calendars_version:
        raise CalendarGenerationError(CALENDAR_IMPLEMENTATION_VERSION_MISMATCH)
    expected_resolved = EXPECTED_RESOLVED_BY_TOKEN.get(request.requested_calendar_token)
    if expected_resolved is None:
        raise CalendarGenerationError(CALENDAR_SOURCE_UNRESOLVED)

    exchange_calendars = importlib.import_module("exchange_calendars")
    try:
        calendar = exchange_calendars.get_calendar(request.requested_calendar_token)
    except Exception as exc:  # package-specific unsupported-token errors vary.
        raise CalendarGenerationError(CALENDAR_SOURCE_UNRESOLVED) from exc
    resolved_name = str(getattr(calendar, "name", ""))
    if resolved_name != expected_resolved:
        raise CalendarGenerationError(CALENDAR_CONFLICT)
    if str(getattr(calendar, "tz", "")) != request.source_timezone:
        raise CalendarGenerationError(CALENDAR_CONFLICT)

    schedule = calendar.schedule.loc[request.fixed_start_date : request.fixed_end_date]
    start = date.fromisoformat(request.fixed_start_date)
    end = date.fromisoformat(request.fixed_end_date)
    source_tz = ZoneInfo(request.source_timezone)
    schedule_by_date = {item.date().isoformat(): row for item, row in schedule.iterrows()}
    sessions = []
    for session_day in _date_range(start, end):
        key = session_day.isoformat()
        if key not in schedule_by_date:
            sessions.append(FrozenCalendarSession(key, FULL_MARKET_CLOSED, None, None, None, None))
            continue
        row = schedule_by_date[key]
        market_open = _ensure_utc_datetime(row["open"].to_pydatetime(), "market_open")
        market_close = _ensure_utc_datetime(row["close"].to_pydatetime(), "market_close")
        local_open = market_open.astimezone(source_tz)
        local_close = market_close.astimezone(source_tz)
        classification = (
            NORMAL_FULL_SESSION
            if local_open.time().replace(tzinfo=None) == time(9, 30)
            and local_close.time().replace(tzinfo=None) == time(16, 0)
            else EARLY_CLOSE_SESSION
        )
        sessions.append(
            FrozenCalendarSession(
                session_date=key,
                session_classification=classification,
                market_open_utc=_utc_iso(market_open),
                market_close_utc=_utc_iso(market_close),
                market_open_local=local_open.isoformat(),
                market_close_local=local_close.isoformat(),
            )
        )

    alias = (
        "IDENTICAL"
        if request.requested_calendar_token == resolved_name
        else f"{request.requested_calendar_token}_USES_{resolved_name}_SCHEDULE"
    )
    status = (
        CALENDAR_READY_FOR_FREEZE_REVIEW
        if request.official_exchange_evidence_digest != "OFFICIAL_EVIDENCE_DIGEST_PENDING"
        else CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE
    )
    payload = {
        "schema_version": CALENDAR_SCHEMA_VERSION,
        "contract_v2_1_digest": request.contract_v2_1_digest,
        "requested_primary_listing_mic": request.requested_primary_listing_mic,
        "requested_calendar_token": request.requested_calendar_token,
        "resolved_calendar": resolved_name,
        "calendar_alias_relationship": alias,
        "exchange_calendars_version": request.exchange_calendars_version,
        "tzdata_version": request.tzdata_version,
        "fixed_start_date": request.fixed_start_date,
        "fixed_end_date": request.fixed_end_date,
        "source_timezone": request.source_timezone,
        "canonical_timezone": request.canonical_timezone,
        "official_exchange_evidence_identity": request.official_exchange_evidence_identity,
        "official_exchange_evidence_digest": request.official_exchange_evidence_digest,
        "status": status,
        "sessions": sessions,
    }
    digest = semantic_digest(payload)
    return FrozenCalendar(
        schema_version=CALENDAR_SCHEMA_VERSION,
        contract_v2_1_digest=request.contract_v2_1_digest,
        requested_primary_listing_mic=request.requested_primary_listing_mic,
        requested_calendar_token=request.requested_calendar_token,
        resolved_calendar=resolved_name,
        calendar_alias_relationship=alias,
        exchange_calendars_version=request.exchange_calendars_version,
        tzdata_version=request.tzdata_version,
        fixed_start_date=request.fixed_start_date,
        fixed_end_date=request.fixed_end_date,
        source_timezone=request.source_timezone,
        canonical_timezone=request.canonical_timezone,
        official_exchange_evidence_identity=request.official_exchange_evidence_identity,
        official_exchange_evidence_digest=request.official_exchange_evidence_digest,
        status=status,
        sessions=tuple(sessions),
        semantic_digest=digest,
    )
