"""Offline ex-dividend analytical segment tagging."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from marketflow.historical_data.frozen_calendar import EARLY_CLOSE_SESSION, FULL_MARKET_CLOSED, FrozenCalendar, semantic_digest
from marketflow.historical_data.rth_bar_engine import DerivedBar


DATASET_START = "DATASET_START"
EX_DIVIDEND_CONTINUITY_RESET = "EX_DIVIDEND_CONTINUITY_RESET"
ANALYTICAL_SEGMENT_WARMUP = "ANALYTICAL_SEGMENT_WARMUP"


@dataclass(frozen=True, slots=True)
class ExDividendEvidence:
    ex_dividend_date: str
    event_ids: tuple[str, ...]
    dividend_event_set_digest: str

    def validate(self) -> None:
        if not self.ex_dividend_date or len(self.ex_dividend_date) != 10:
            raise ValueError("ex-dividend date must be an ISO date")
        if not self.event_ids:
            raise ValueError("ex-dividend evidence must include event IDs")
        if len(set(self.event_ids)) != len(self.event_ids):
            raise ValueError("event IDs must be unique")
        if not self.dividend_event_set_digest:
            raise ValueError("dividend event-set digest is required")


@dataclass(frozen=True, slots=True)
class AnalyticalSegment:
    analysis_segment_id: str
    profile: str
    source_dataset_digest: str
    dividend_event_set_digest: str
    segment_start_session_date: str
    first_canonical_bar_timestamp_utc: str
    start_reason: str
    trigger_event_ids: tuple[str, ...]
    readiness_status: str
    deterministic_segment_digest: str


@dataclass(frozen=True, slots=True)
class SegmentedBar:
    bar: DerivedBar
    analysis_segment_id: str
    readiness_status: str


def _event_map(events: Iterable[ExDividendEvidence]) -> dict[str, ExDividendEvidence]:
    merged: dict[str, list[str]] = {}
    digest_by_date: dict[str, str] = {}
    for event in events:
        event.validate()
        merged.setdefault(event.ex_dividend_date, []).extend(event.event_ids)
        digest_by_date.setdefault(event.ex_dividend_date, event.dividend_event_set_digest)
    return {
        event_date: ExDividendEvidence(event_date, tuple(sorted(set(event_ids))), digest_by_date[event_date])
        for event_date, event_ids in merged.items()
    }


def assign_analytical_segments(
    bars: tuple[DerivedBar, ...],
    *,
    calendar: FrozenCalendar,
    dividend_events: tuple[ExDividendEvidence, ...],
    source_dataset_digest: str,
    profile: str,
) -> tuple[tuple[AnalyticalSegment, ...], tuple[SegmentedBar, ...]]:
    """Assign deterministic ex-dividend analytical segments to derived bars."""
    if not bars:
        return (), ()
    events_by_date = _event_map(dividend_events)
    event_dates = sorted(events_by_date)
    next_event_index = 0
    pending_event: ExDividendEvidence | None = None
    current_segment: AnalyticalSegment | None = None
    segments: list[AnalyticalSegment] = []
    segmented: list[SegmentedBar] = []
    for bar in sorted(bars, key=lambda item: (item.session_date, item.timestamp_utc)):
        while next_event_index < len(event_dates) and event_dates[next_event_index] <= bar.session_date:
            pending_event = _merge_pending(pending_event, events_by_date[event_dates[next_event_index]])
            next_event_index += 1
        if current_segment is None:
            current_segment = _new_segment(
                profile=profile,
                source_dataset_digest=source_dataset_digest,
                event_digest="DATASET_START",
                bar=bar,
                reason=DATASET_START,
                event_ids=(),
            )
            segments.append(current_segment)
        if pending_event is not None and bar.session_date >= pending_event.ex_dividend_date:
            current_segment = _new_segment(
                profile=profile,
                source_dataset_digest=source_dataset_digest,
                event_digest=pending_event.dividend_event_set_digest,
                bar=bar,
                reason=EX_DIVIDEND_CONTINUITY_RESET,
                event_ids=pending_event.event_ids,
            )
            segments.append(current_segment)
            pending_event = None
        segmented.append(SegmentedBar(bar, current_segment.analysis_segment_id, ANALYTICAL_SEGMENT_WARMUP))
    return tuple(segments), tuple(segmented)


def _merge_pending(existing: ExDividendEvidence | None, new: ExDividendEvidence) -> ExDividendEvidence:
    if existing is None:
        return new
    return ExDividendEvidence(
        ex_dividend_date=min(existing.ex_dividend_date, new.ex_dividend_date),
        event_ids=tuple(sorted(set(existing.event_ids + new.event_ids))),
        dividend_event_set_digest=semantic_digest(
            {
                "digests": sorted((existing.dividend_event_set_digest, new.dividend_event_set_digest)),
                "event_ids": sorted(set(existing.event_ids + new.event_ids)),
            }
        ),
    )


def _new_segment(
    *,
    profile: str,
    source_dataset_digest: str,
    event_digest: str,
    bar: DerivedBar,
    reason: str,
    event_ids: tuple[str, ...],
) -> AnalyticalSegment:
    payload = {
        "profile": profile,
        "source_dataset_digest": source_dataset_digest,
        "dividend_event_set_digest": event_digest,
        "segment_start_session_date": bar.session_date,
        "first_canonical_bar_timestamp_utc": bar.timestamp_utc.isoformat().replace("+00:00", "Z"),
        "start_reason": reason,
        "trigger_event_ids": event_ids,
    }
    digest = semantic_digest(payload)
    return AnalyticalSegment(
        analysis_segment_id=f"SEGMENT-{digest[:16]}",
        profile=profile,
        source_dataset_digest=source_dataset_digest,
        dividend_event_set_digest=event_digest,
        segment_start_session_date=bar.session_date,
        first_canonical_bar_timestamp_utc=bar.timestamp_utc.isoformat().replace("+00:00", "Z"),
        start_reason=reason,
        trigger_event_ids=event_ids,
        readiness_status=ANALYTICAL_SEGMENT_WARMUP,
        deterministic_segment_digest=digest,
    )


def current_segment_prefix(segmented_bars: tuple[SegmentedBar, ...], decision_row: int) -> tuple[DerivedBar, ...]:
    """Return only current-segment bars through decision row T."""
    if decision_row < 0 or decision_row >= len(segmented_bars):
        raise IndexError("decision row out of range")
    current_segment = segmented_bars[decision_row].analysis_segment_id
    prefix = segmented_bars[: decision_row + 1]
    return tuple(item.bar for item in prefix if item.analysis_segment_id == current_segment)
