"""Deterministic RTH source-window validation and aggregation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any
from zoneinfo import ZoneInfo

from marketflow.historical_data.frozen_calendar import (
    EARLY_CLOSE_SESSION,
    FULL_MARKET_CLOSED,
    NORMAL_FULL_SESSION,
    FrozenCalendar,
    FrozenCalendarSession,
    semantic_digest,
)
from marketflow.research import acquisition_contract_v2 as contract_v2
from marketflow.research import acquisition_contract_v2_1 as contract_v21


SOURCE_INTERVAL = timedelta(minutes=15)
SOURCE_TIMEZONE = "America/New_York"
SOURCE_TIMESTAMP_SEMANTIC = "START_OF_AGGREGATE_WINDOW"
RUNTIME_MIGRATION_PENDING = "LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION"
PROFILE_SWING = "SWING"
PROFILE_POSITION_SWING = "POSITION_SWING"
SWING_CONTRACT_VERSION = "SWING_RTH_HALF_SESSION_V1"
POSITION_CONTRACT_VERSION = "POSITION_SWING_RTH_FULL_SESSION_V1"
RTH_HALF_SESSION_195M = "RTH_HALF_SESSION_195M"
RTH_FULL_SESSION_1D = "RTH_FULL_SESSION_1D"

SESSION_COMPLETE = "SESSION_COMPLETE"
EARLY_CLOSE_SESSION_EXCLUDED = "EARLY_CLOSE_SESSION_EXCLUDED"
FULL_MARKET_CLOSED_OUTCOME = "FULL_MARKET_CLOSED"
SESSION_SOURCE_MISSING = "SESSION_SOURCE_MISSING"
SESSION_SOURCE_INCOMPLETE = "SESSION_SOURCE_INCOMPLETE"
SESSION_SOURCE_DUPLICATE_SLOT = "SESSION_SOURCE_DUPLICATE_SLOT"
SESSION_SOURCE_EXTRA_SLOT = "SESSION_SOURCE_EXTRA_SLOT"
SESSION_SOURCE_INVALID = "SESSION_SOURCE_INVALID"
CALENDAR_DATA_CONFLICT = "CALENDAR_DATA_CONFLICT"
DERIVATION_BLOCKED = "DERIVATION_BLOCKED"
DERIVATION_COMPLETE = "DERIVATION_COMPLETE"


class BarValidationError(ValueError):
    """Raised when source bars or derivation inputs are invalid."""


def _utc_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise BarValidationError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise BarValidationError(f"{field_name} must be timezone-aware")
    if value.utcoffset() != timedelta(0):
        raise BarValidationError(f"{field_name} must be UTC")
    return value.astimezone(UTC)


def _decimal(value: str | int | Decimal, field_name: str) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise BarValidationError(f"{field_name} must not be a binary float or boolean")
    try:
        parsed = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise BarValidationError(f"{field_name} must be a finite Decimal") from exc
    if parsed.is_nan() or parsed.is_infinite():
        raise BarValidationError(f"{field_name} must be finite")
    return parsed


def _decimal_text(value: Decimal) -> str:
    if value == 0:
        return "0"
    normalized = value.normalize()
    if normalized == normalized.to_integral():
        return format(normalized.quantize(Decimal(1)), "f")
    return format(normalized, "f")


def _utc_iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class SourceBar:
    window_start_utc: datetime
    window_end_utc: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal

    @classmethod
    def build(
        cls,
        *,
        window_start_utc: datetime,
        window_end_utc: datetime,
        open: str | int | Decimal,
        high: str | int | Decimal,
        low: str | int | Decimal,
        close: str | int | Decimal,
        volume: str | int | Decimal,
    ) -> "SourceBar":
        bar = cls(
            window_start_utc=_utc_datetime(window_start_utc, "window_start_utc"),
            window_end_utc=_utc_datetime(window_end_utc, "window_end_utc"),
            open=_decimal(open, "open"),
            high=_decimal(high, "high"),
            low=_decimal(low, "low"),
            close=_decimal(close, "close"),
            volume=_decimal(volume, "volume"),
        )
        bar.validate()
        return bar

    @property
    def timestamp_utc(self) -> datetime:
        """Compatibility metadata: timestamp_utc is explicitly WINDOW_START."""
        return self.window_start_utc

    def validate(self) -> None:
        if self.window_end_utc - self.window_start_utc != SOURCE_INTERVAL:
            raise BarValidationError("source window must be exactly 15 minutes")
        if self.window_start_utc.second or self.window_start_utc.microsecond:
            raise BarValidationError("source start must align to a minute")
        if self.window_start_utc.minute % 15 != 0:
            raise BarValidationError("source start must align to the 15-minute UTC grid")
        local_start = self.window_start_utc.astimezone(ZoneInfo(SOURCE_TIMEZONE))
        if local_start.second or local_start.microsecond or local_start.minute % 15 != 0:
            raise BarValidationError("source start must align to the 15-minute local grid")
        if self.high < self.low:
            raise BarValidationError("high must be greater than or equal to low")
        if self.volume < 0:
            raise BarValidationError("volume must be nonnegative")

    def semantic_payload(self) -> dict[str, str]:
        return {
            "window_start_utc": _utc_iso(self.window_start_utc),
            "window_end_utc": _utc_iso(self.window_end_utc),
            "open": _decimal_text(self.open),
            "high": _decimal_text(self.high),
            "low": _decimal_text(self.low),
            "close": _decimal_text(self.close),
            "volume": _decimal_text(self.volume),
        }


@dataclass(frozen=True, slots=True)
class DerivedBar:
    profile_id: str
    profile_contract_version: str
    canonical_bar_type: str
    session_date: str
    timestamp_utc: datetime
    local_source_window_start: str
    local_source_window_end: str
    source_bar_count: int
    source_timestamp_set_digest: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    frozen_calendar_digest: str
    contract_v2_1_digest: str
    deterministic_bar_digest: str

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "profile_contract_version": self.profile_contract_version,
            "canonical_bar_type": self.canonical_bar_type,
            "session_date": self.session_date,
            "timestamp_utc": _utc_iso(self.timestamp_utc),
            "local_source_window_start": self.local_source_window_start,
            "local_source_window_end": self.local_source_window_end,
            "source_bar_count": self.source_bar_count,
            "source_timestamp_set_digest": self.source_timestamp_set_digest,
            "open": _decimal_text(self.open),
            "high": _decimal_text(self.high),
            "low": _decimal_text(self.low),
            "close": _decimal_text(self.close),
            "volume": _decimal_text(self.volume),
            "frozen_calendar_digest": self.frozen_calendar_digest,
            "contract_v2_1_digest": self.contract_v2_1_digest,
        }


@dataclass(frozen=True, slots=True)
class SessionDerivation:
    session_date: str
    outcome: str
    accepted_source_bars: tuple[SourceBar, ...]
    extended_hours_exclusion_count: int
    finding: str


@dataclass(frozen=True, slots=True)
class DerivedDatasetResult:
    contract_v2_1_digest: str
    frozen_calendar_digest: str
    profile: str
    status: str
    accepted_full_session_count: int
    early_close_exclusion_count: int
    extended_hours_exclusion_count: int
    invalid_or_incomplete_session_count: int
    produced_bar_count: int
    findings: tuple[str, ...]
    bars: tuple[DerivedBar, ...]
    dataset_semantic_digest: str

    def public_receipt(self) -> dict[str, Any]:
        return {
            "contract_v2_1_digest": self.contract_v2_1_digest,
            "frozen_calendar_digest": self.frozen_calendar_digest,
            "profile": self.profile,
            "status": self.status,
            "accepted_full_session_count": self.accepted_full_session_count,
            "early_close_exclusion_count": self.early_close_exclusion_count,
            "extended_hours_exclusion_count": self.extended_hours_exclusion_count,
            "invalid_or_incomplete_session_count": self.invalid_or_incomplete_session_count,
            "produced_bar_count": self.produced_bar_count,
            "findings": list(self.findings),
            "dataset_semantic_digest": self.dataset_semantic_digest,
        }


def expected_source_windows(session: FrozenCalendarSession) -> tuple[datetime, ...]:
    if session.session_classification != NORMAL_FULL_SESSION or session.market_open_utc is None:
        return ()
    start = datetime.fromisoformat(session.market_open_utc.replace("Z", "+00:00")).astimezone(UTC)
    return tuple(start + index * SOURCE_INTERVAL for index in range(26))


def _local_hhmm(value: datetime) -> str:
    return value.astimezone(ZoneInfo(SOURCE_TIMEZONE)).strftime("%H:%M")


def _validate_source_order(source_bars: tuple[SourceBar, ...]) -> str | None:
    starts = [bar.window_start_utc for bar in source_bars]
    if starts != sorted(starts):
        return SESSION_SOURCE_INVALID
    if len(starts) != len(set(starts)):
        return SESSION_SOURCE_DUPLICATE_SLOT
    return None


def validate_session_sources(
    calendar: FrozenCalendar,
    session: FrozenCalendarSession,
    source_bars: tuple[SourceBar, ...],
) -> SessionDerivation:
    """Validate source bars for one session and exclude extended-hours bars."""
    order_error = _validate_source_order(source_bars)
    if order_error:
        return SessionDerivation(session.session_date, order_error, (), 0, order_error)
    if session.session_classification == EARLY_CLOSE_SESSION:
        return SessionDerivation(session.session_date, EARLY_CLOSE_SESSION_EXCLUDED, (), 0, EARLY_CLOSE_SESSION_EXCLUDED)
    if session.session_classification == FULL_MARKET_CLOSED:
        if source_bars:
            return SessionDerivation(session.session_date, CALENDAR_DATA_CONFLICT, (), 0, CALENDAR_DATA_CONFLICT)
        return SessionDerivation(session.session_date, FULL_MARKET_CLOSED_OUTCOME, (), 0, FULL_MARKET_CLOSED_OUTCOME)
    if session.session_classification != NORMAL_FULL_SESSION:
        return SessionDerivation(session.session_date, CALENDAR_DATA_CONFLICT, (), 0, CALENDAR_DATA_CONFLICT)

    expected = expected_source_windows(session)
    expected_set = set(expected)
    rth_bars = tuple(bar for bar in source_bars if bar.window_start_utc in expected_set)
    extended_count = len(source_bars) - len(rth_bars)
    starts = tuple(bar.window_start_utc for bar in rth_bars)
    if not source_bars:
        return SessionDerivation(session.session_date, SESSION_SOURCE_MISSING, (), extended_count, SESSION_SOURCE_MISSING)
    if len(starts) != len(set(starts)):
        return SessionDerivation(session.session_date, SESSION_SOURCE_DUPLICATE_SLOT, (), extended_count, SESSION_SOURCE_DUPLICATE_SLOT)
    if any(
        bar.window_start_utc not in expected_set
        and time(9, 30) <= bar.window_start_utc.astimezone(ZoneInfo(SOURCE_TIMEZONE)).time().replace(tzinfo=None) < time(16, 0)
        for bar in source_bars
    ):
        return SessionDerivation(session.session_date, SESSION_SOURCE_EXTRA_SLOT, (), extended_count, SESSION_SOURCE_EXTRA_SLOT)
    if set(starts) != expected_set:
        return SessionDerivation(session.session_date, SESSION_SOURCE_INCOMPLETE, (), extended_count, SESSION_SOURCE_INCOMPLETE)
    return SessionDerivation(session.session_date, SESSION_COMPLETE, rth_bars, extended_count, SESSION_COMPLETE)


def _aggregate(
    bars: tuple[SourceBar, ...],
    *,
    profile_id: str,
    profile_contract_version: str,
    canonical_bar_type: str,
    session_date: str,
    timestamp_utc: datetime,
    local_start: str,
    local_end: str,
    frozen_calendar_digest: str,
    contract_v2_1_digest: str,
) -> DerivedBar:
    open_value = bars[0].open
    high_value = max(bar.high for bar in bars)
    low_value = min(bar.low for bar in bars)
    close_value = bars[-1].close
    volume_value = sum((bar.volume for bar in bars), Decimal("0"))
    timestamp_digest = semantic_digest([_utc_iso(bar.window_start_utc) for bar in bars])
    payload = {
        "profile_id": profile_id,
        "profile_contract_version": profile_contract_version,
        "canonical_bar_type": canonical_bar_type,
        "session_date": session_date,
        "timestamp_utc": _utc_iso(timestamp_utc),
        "local_source_window_start": local_start,
        "local_source_window_end": local_end,
        "source_bar_count": len(bars),
        "source_timestamp_set_digest": timestamp_digest,
        "open": _decimal_text(open_value),
        "high": _decimal_text(high_value),
        "low": _decimal_text(low_value),
        "close": _decimal_text(close_value),
        "volume": _decimal_text(volume_value),
        "frozen_calendar_digest": frozen_calendar_digest,
        "contract_v2_1_digest": contract_v2_1_digest,
    }
    return DerivedBar(
        profile_id=profile_id,
        profile_contract_version=profile_contract_version,
        canonical_bar_type=canonical_bar_type,
        session_date=session_date,
        timestamp_utc=timestamp_utc,
        local_source_window_start=local_start,
        local_source_window_end=local_end,
        source_bar_count=len(bars),
        source_timestamp_set_digest=timestamp_digest,
        open=open_value,
        high=high_value,
        low=low_value,
        close=close_value,
        volume=volume_value,
        frozen_calendar_digest=frozen_calendar_digest,
        contract_v2_1_digest=contract_v2_1_digest,
        deterministic_bar_digest=semantic_digest(payload),
    )


def _bars_by_session(calendar: FrozenCalendar, bars: tuple[SourceBar, ...]) -> dict[str, tuple[SourceBar, ...]]:
    by_date: dict[str, list[SourceBar]] = {session.session_date: [] for session in calendar.sessions}
    source_tz = ZoneInfo(SOURCE_TIMEZONE)
    known_dates = set(by_date)
    for bar in bars:
        local_date = bar.window_start_utc.astimezone(source_tz).date().isoformat()
        if local_date in known_dates:
            by_date[local_date].append(bar)
    return {key: tuple(value) for key, value in by_date.items()}


def _contract_digest() -> str:
    contract = contract_v21.default_contract()
    contract_v21.verify_base_contract_digest(contract)
    if contract_v21.contract_digest(contract) != "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6":
        raise BarValidationError("Contract v2.1 digest changed")
    return contract_v21.contract_digest(contract)


def derive_profile_bars(calendar: FrozenCalendar, source_bars: tuple[SourceBar, ...], profile: str) -> DerivedDatasetResult:
    """Derive deterministic SWING or POSITION_SWING bars from source windows."""
    base = contract_v2.default_contract()
    if base.runtime_profile_migration_status != RUNTIME_MIGRATION_PENDING:
        raise BarValidationError("runtime migration status changed")
    contract_digest = _contract_digest()
    source_tuple = tuple(source_bars)
    order_error = _validate_source_order(source_tuple)
    if order_error:
        return _blocked_result(calendar, contract_digest, profile, (order_error,))
    by_session = _bars_by_session(calendar, source_tuple)
    derived: list[DerivedBar] = []
    findings: list[str] = []
    accepted = 0
    early = 0
    extended = 0
    invalid = 0
    for session in calendar.sessions:
        session_bars = by_session.get(session.session_date, ())
        validation = validate_session_sources(calendar, session, session_bars)
        extended += validation.extended_hours_exclusion_count
        if validation.outcome == SESSION_COMPLETE:
            accepted += 1
            expected = expected_source_windows(session)
            rth_bars = tuple(sorted(validation.accepted_source_bars, key=lambda item: item.window_start_utc))
            if tuple(bar.window_start_utc for bar in rth_bars) != expected:
                invalid += 1
                findings.append(f"{session.session_date}:{SESSION_SOURCE_INVALID}")
                continue
            source_tz = ZoneInfo(SOURCE_TIMEZONE)
            if profile == PROFILE_SWING:
                morning = rth_bars[:13]
                afternoon = rth_bars[13:]
                derived.append(
                    _aggregate(
                        morning,
                        profile_id=PROFILE_SWING,
                        profile_contract_version=SWING_CONTRACT_VERSION,
                        canonical_bar_type=RTH_HALF_SESSION_195M,
                        session_date=session.session_date,
                        timestamp_utc=morning[-1].window_end_utc,
                        local_start=_local_hhmm(morning[0].window_start_utc),
                        local_end=_local_hhmm(morning[-1].window_end_utc),
                        frozen_calendar_digest=calendar.semantic_digest,
                        contract_v2_1_digest=contract_digest,
                    )
                )
                derived.append(
                    _aggregate(
                        afternoon,
                        profile_id=PROFILE_SWING,
                        profile_contract_version=SWING_CONTRACT_VERSION,
                        canonical_bar_type=RTH_HALF_SESSION_195M,
                        session_date=session.session_date,
                        timestamp_utc=afternoon[-1].window_end_utc,
                        local_start=_local_hhmm(afternoon[0].window_start_utc),
                        local_end=_local_hhmm(afternoon[-1].window_end_utc),
                        frozen_calendar_digest=calendar.semantic_digest,
                        contract_v2_1_digest=contract_digest,
                    )
                )
            elif profile == PROFILE_POSITION_SWING:
                derived.append(
                    _aggregate(
                        rth_bars,
                        profile_id=PROFILE_POSITION_SWING,
                        profile_contract_version=POSITION_CONTRACT_VERSION,
                        canonical_bar_type=RTH_FULL_SESSION_1D,
                        session_date=session.session_date,
                        timestamp_utc=datetime.combine(date.fromisoformat(session.session_date), time(16, 0), tzinfo=source_tz).astimezone(UTC),
                        local_start=_local_hhmm(rth_bars[0].window_start_utc),
                        local_end=_local_hhmm(rth_bars[-1].window_end_utc),
                        frozen_calendar_digest=calendar.semantic_digest,
                        contract_v2_1_digest=contract_digest,
                    )
                )
            else:
                raise BarValidationError("unknown profile")
        elif validation.outcome == EARLY_CLOSE_SESSION_EXCLUDED:
            early += 1
            findings.append(f"{session.session_date}:{EARLY_CLOSE_SESSION_EXCLUDED}")
        elif validation.outcome in {FULL_MARKET_CLOSED_OUTCOME}:
            continue
        else:
            invalid += 1
            findings.append(f"{session.session_date}:{validation.finding}")
    status = DERIVATION_COMPLETE if invalid == 0 else DERIVATION_BLOCKED
    payload = {
        "contract_v2_1_digest": contract_digest,
        "frozen_calendar_digest": calendar.semantic_digest,
        "profile": profile,
        "status": status,
        "accepted_full_session_count": accepted,
        "early_close_exclusion_count": early,
        "extended_hours_exclusion_count": extended,
        "invalid_or_incomplete_session_count": invalid,
        "produced_bar_count": len(derived),
        "findings": findings,
        "bar_digests": [bar.deterministic_bar_digest for bar in derived],
    }
    return DerivedDatasetResult(
        contract_v2_1_digest=contract_digest,
        frozen_calendar_digest=calendar.semantic_digest,
        profile=profile,
        status=status,
        accepted_full_session_count=accepted,
        early_close_exclusion_count=early,
        extended_hours_exclusion_count=extended,
        invalid_or_incomplete_session_count=invalid,
        produced_bar_count=len(derived),
        findings=tuple(findings),
        bars=tuple(derived),
        dataset_semantic_digest=semantic_digest(payload),
    )


def _blocked_result(calendar: FrozenCalendar, contract_digest: str, profile: str, findings: tuple[str, ...]) -> DerivedDatasetResult:
    payload = {
        "contract_v2_1_digest": contract_digest,
        "frozen_calendar_digest": calendar.semantic_digest,
        "profile": profile,
        "status": DERIVATION_BLOCKED,
        "findings": findings,
    }
    return DerivedDatasetResult(
        contract_v2_1_digest=contract_digest,
        frozen_calendar_digest=calendar.semantic_digest,
        profile=profile,
        status=DERIVATION_BLOCKED,
        accepted_full_session_count=0,
        early_close_exclusion_count=0,
        extended_hours_exclusion_count=0,
        invalid_or_incomplete_session_count=1,
        produced_bar_count=0,
        findings=findings,
        bars=(),
        dataset_semantic_digest=semantic_digest(payload),
    )
