"""Offline historical-data artifact pipeline orchestration."""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Callable

from marketflow.historical_data import artifacts
from marketflow.historical_data import frozen_calendar as calendar_engine
from marketflow.historical_data import rth_bar_engine as rth


def run_offline_historical_pipeline(
    *,
    calendar: calendar_engine.FrozenCalendar,
    source_bars: tuple[rth.SourceBar, ...],
    dividend_events: tuple[artifacts.DividendEventRecord, ...],
    run_root: str | Path,
    run_id: str | None = None,
    run_id_factory: Callable[[], str] | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> dict[str, object]:
    """Write one synthetic offline historical-data run and return a receipt."""
    run = artifacts.create_historical_run(
        run_root=run_root,
        run_id=run_id,
        run_id_factory=run_id_factory,
        created_at_utc=created_at_utc,
    )
    committed: list[dict[str, object]] = []
    findings: list[str] = []

    try:
        calendar_result = artifacts.commit_calendar_candidate_artifact(
            calendar=calendar,
            run_root=run_root,
            run_id=run.run_id,
            artifact_id_factory=artifact_id_factory,
            created_at_utc=created_at_utc,
        )
        committed.append(calendar_result["receipt"])
        calendar_ref = artifacts.manifest_ref_from_result(calendar_result, run_root=run_root)
    except artifacts.HistoricalArtifactError:
        return _blocked_receipt(run, "CALENDAR_ARTIFACT_BLOCKED", findings + ["CALENDAR_ARTIFACT_BLOCKED"], committed)

    try:
        source_result = artifacts.commit_normalized_15m_artifact(
            source_bars=source_bars,
            run_root=run_root,
            run_id=run.run_id,
            artifact_id_factory=artifact_id_factory,
            created_at_utc=created_at_utc,
        )
        committed.append(source_result["receipt"])
        source_ref = artifacts.manifest_ref_from_result(source_result, run_root=run_root)
    except artifacts.HistoricalArtifactError:
        return _blocked_receipt(run, "NORMALIZED_SOURCE_BLOCKED", findings + ["NORMALIZED_SOURCE_BLOCKED"], committed)

    try:
        dividend_result = artifacts.commit_dividend_event_set_artifact(
            events=dividend_events,
            run_root=run_root,
            run_id=run.run_id,
            artifact_id_factory=artifact_id_factory,
            created_at_utc=created_at_utc,
        )
        committed.append(dividend_result["receipt"])
        dividend_ref = artifacts.manifest_ref_from_result(dividend_result, run_root=run_root)
    except artifacts.HistoricalArtifactError:
        return _blocked_receipt(run, "DIVIDEND_EVENT_SET_BLOCKED", findings + ["DIVIDEND_EVENT_SET_BLOCKED"], committed)

    profile_statuses: dict[str, str] = {}
    segment_statuses: dict[str, str] = {}
    derivation_refs: list[str] = []
    for profile in (rth.PROFILE_SWING, rth.PROFILE_POSITION_SWING):
        try:
            derived_result = artifacts.commit_derived_profile_artifact(
                calendar_manifest_ref=calendar_ref,
                source_manifest_ref=source_ref,
                profile=profile,
                run_root=run_root,
                artifact_id_factory=artifact_id_factory,
                created_at_utc=created_at_utc,
            )
            committed.append(derived_result["receipt"])
            derived_ref = artifacts.manifest_ref_from_result(derived_result, run_root=run_root)
            derivation_refs.append(derived_ref)
            derived_payload = artifacts.load_historical_payload(derived_result["manifest"], run_root=run_root)
            profile_statuses[profile] = str(derived_payload["derivation_status"])
            if derived_payload["derivation_status"] == rth.DERIVATION_COMPLETE:
                segment_result = artifacts.commit_segment_map_artifact(
                    derived_manifest_ref=derived_ref,
                    dividend_manifest_ref=dividend_ref,
                    calendar_manifest_ref=calendar_ref,
                    run_root=run_root,
                    artifact_id_factory=artifact_id_factory,
                    created_at_utc=created_at_utc,
                )
                committed.append(segment_result["receipt"])
                segment_payload = artifacts.load_historical_payload(segment_result["manifest"], run_root=run_root)
                segment_statuses[profile] = "SEGMENT_MAP_WRITTEN" if segment_payload["bar_assignment_count"] >= 0 else "SEGMENT_MAP_INVALID"
            else:
                segment_statuses[profile] = "SEGMENT_MAP_SKIPPED_DERIVATION_BLOCKED"
        except artifacts.HistoricalArtifactError:
            profile_statuses[profile] = "DERIVATION_ARTIFACT_BLOCKED"
            segment_statuses[profile] = "SEGMENT_MAP_SKIPPED_DERIVATION_BLOCKED"
            findings.append(f"{profile}:DERIVATION_ARTIFACT_BLOCKED")

    complete_profiles = [profile for profile, status in profile_statuses.items() if status == rth.DERIVATION_COMPLETE]
    if len(complete_profiles) == 2 and not findings:
        status = artifacts.PIPELINE_COMPLETED
    elif complete_profiles:
        status = artifacts.PIPELINE_PARTIAL
    else:
        status = artifacts.PIPELINE_BLOCKED

    receipt_payload = {
        "pipeline_status": status,
        "run_id": run.run_id,
        "calendar_status": calendar.status,
        "normalized_source_status": "NORMALIZED_SOURCE_WRITTEN",
        "swing_derivation_status": profile_statuses.get(rth.PROFILE_SWING, "DERIVATION_NOT_RUN"),
        "position_swing_derivation_status": profile_statuses.get(rth.PROFILE_POSITION_SWING, "DERIVATION_NOT_RUN"),
        "segment_map_statuses": segment_statuses,
        "artifact_receipts": committed,
        "fixed_findings": findings,
        "synthetic_only": True,
        "provider_execution_enabled": False,
        "runtime_migration_performed": False,
    }
    receipt_inputs = (calendar_ref, source_ref, dividend_ref, *tuple(derivation_refs))
    try:
        receipt_result = artifacts.commit_pipeline_receipt_artifact(
            run_root=run_root,
            run_id=run.run_id,
            receipt_payload=receipt_payload,
            input_manifest_refs=receipt_inputs,
            artifact_id_factory=artifact_id_factory,
            created_at_utc=created_at_utc,
        )
        committed.append(receipt_result["receipt"])
        receipt_payload["pipeline_receipt_artifact"] = receipt_result["receipt"]
        receipt_payload["artifact_receipts"] = committed
    except artifacts.HistoricalArtifactError:
        receipt_payload["pipeline_status"] = artifacts.PIPELINE_PARTIAL if complete_profiles else artifacts.PIPELINE_BLOCKED
        receipt_payload["fixed_findings"] = findings + ["PIPELINE_RECEIPT_ARTIFACT_BLOCKED"]
    return receipt_payload


def _blocked_receipt(
    run: artifacts.HistoricalRunContext,
    status: str,
    findings: list[str],
    committed: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "pipeline_status": artifacts.PIPELINE_BLOCKED,
        "run_id": run.run_id,
        "calendar_status": status if status.startswith("CALENDAR") else "CALENDAR_STATUS_UNAVAILABLE",
        "normalized_source_status": status if status.startswith("NORMALIZED") else "NORMALIZED_SOURCE_NOT_WRITTEN",
        "swing_derivation_status": "DERIVATION_NOT_RUN",
        "position_swing_derivation_status": "DERIVATION_NOT_RUN",
        "segment_map_statuses": {},
        "artifact_receipts": committed,
        "fixed_findings": findings,
        "synthetic_only": True,
        "provider_execution_enabled": False,
        "runtime_migration_performed": False,
    }


def synthetic_self_check_fixture() -> tuple[calendar_engine.FrozenCalendar, tuple[rth.SourceBar, ...], tuple[artifacts.DividendEventRecord, ...]]:
    """Return deterministic synthetic calendar/source/dividend inputs."""
    day1 = _session("2024-01-02")
    early = _session("2024-01-03", calendar_engine.EARLY_CLOSE_SESSION)
    day2 = _session("2024-01-04")
    sessions = (day1, early, day2)
    calendar_payload = {"sessions": [asdict(session) for session in sessions], "contract": _contract_digest()}
    calendar = calendar_engine.FrozenCalendar(
        schema_version=calendar_engine.CALENDAR_SCHEMA_VERSION,
        contract_v2_1_digest=_contract_digest(),
        requested_primary_listing_mic="XNAS",
        requested_calendar_token="XNAS",
        resolved_calendar="XNYS",
        calendar_alias_relationship="XNAS_USES_XNYS_SCHEDULE",
        exchange_calendars_version=calendar_engine.REQUIRED_EXCHANGE_CALENDARS_VERSION,
        tzdata_version="SYSTEM_ZONEINFO",
        fixed_start_date="2024-01-02",
        fixed_end_date="2024-01-04",
        source_timezone=calendar_engine.SOURCE_TIMEZONE,
        canonical_timezone=calendar_engine.CANONICAL_TIMEZONE,
        official_exchange_evidence_identity="SYNTHETIC_OFFLINE_FIXTURE_OFFICIAL_EVIDENCE",
        official_exchange_evidence_digest="SYNTHETIC_OFFLINE_FIXTURE_DIGEST",
        status=calendar_engine.CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE,
        sessions=sessions,
        semantic_digest=calendar_engine.semantic_digest(calendar_payload),
    )
    source_bars = _rth_bars(day1) + (_bar(datetime(2024, 1, 2, 13, 0, tzinfo=UTC), -10),) + _rth_bars(day2)
    source_bars = tuple(sorted(source_bars, key=lambda item: item.window_start_utc))
    dividends = (artifacts.DividendEventRecord(event_id="DIV-A", ex_dividend_date="2024-01-03"),)
    return calendar, source_bars, dividends


def _contract_digest() -> str:
    from marketflow.research import acquisition_contract_v2_1 as contract_v21

    return contract_v21.contract_digest(contract_v21.default_contract())


def _session(session_date: str, classification: str = calendar_engine.NORMAL_FULL_SESSION) -> calendar_engine.FrozenCalendarSession:
    if classification == calendar_engine.FULL_MARKET_CLOSED:
        return calendar_engine.FrozenCalendarSession(session_date, classification, None, None, None, None)
    open_utc = datetime.fromisoformat(f"{session_date}T14:30:00+00:00")
    close_hour = "21:00:00" if classification == calendar_engine.NORMAL_FULL_SESSION else "18:00:00"
    close_utc = datetime.fromisoformat(f"{session_date}T{close_hour}+00:00")
    return calendar_engine.FrozenCalendarSession(
        session_date=session_date,
        session_classification=classification,
        market_open_utc=open_utc.isoformat().replace("+00:00", "Z"),
        market_close_utc=close_utc.isoformat().replace("+00:00", "Z"),
        market_open_local=f"{session_date}T09:30:00-05:00",
        market_close_local=f"{session_date}T16:00:00-05:00",
    )


def _bar(start: datetime, offset: int = 0) -> rth.SourceBar:
    base = Decimal("100") + Decimal(offset)
    return rth.SourceBar.build(
        window_start_utc=start,
        window_end_utc=start + timedelta(minutes=15),
        open=str(base),
        high=str(base + Decimal("2")),
        low=str(base - Decimal("1")),
        close=str(base + Decimal("0.5")),
        volume="10",
    )


def _rth_bars(session: calendar_engine.FrozenCalendarSession) -> tuple[rth.SourceBar, ...]:
    return tuple(_bar(start, index) for index, start in enumerate(rth.expected_source_windows(session)))
