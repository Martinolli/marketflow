from __future__ import annotations

import ast
import json
import subprocess
import sys
from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from marketflow.historical_data import analytical_segments as segments
from marketflow.historical_data import frozen_calendar as fc
from marketflow.historical_data import rth_bar_engine as rth
from marketflow.research import acquisition_contract_v2 as acv2
from marketflow.research import acquisition_contract_v2_1 as acv21
from marketflow.research import fixed_date_acquisition_contract as fdac


REPO_ROOT = Path(__file__).resolve().parents[1]
V1_DIGEST = "29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e"
V2_DIGEST = "59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0"
V21_DIGEST = "538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6"


def _session(session_date: str, classification: str = fc.NORMAL_FULL_SESSION) -> fc.FrozenCalendarSession:
    if classification == fc.FULL_MARKET_CLOSED:
        return fc.FrozenCalendarSession(session_date, classification, None, None, None, None)
    open_utc = datetime.fromisoformat(f"{session_date}T14:30:00+00:00")
    close_hour = "21:00:00" if classification == fc.NORMAL_FULL_SESSION else "18:00:00"
    close_utc = datetime.fromisoformat(f"{session_date}T{close_hour}+00:00")
    return fc.FrozenCalendarSession(
        session_date=session_date,
        session_classification=classification,
        market_open_utc=open_utc.isoformat().replace("+00:00", "Z"),
        market_close_utc=close_utc.isoformat().replace("+00:00", "Z"),
        market_open_local="2024-01-02T09:30:00-05:00",
        market_close_local="2024-01-02T16:00:00-05:00",
    )


def _calendar(*sessions: fc.FrozenCalendarSession) -> fc.FrozenCalendar:
    payload = {"sessions": sessions, "contract": V21_DIGEST}
    return fc.FrozenCalendar(
        schema_version=fc.CALENDAR_SCHEMA_VERSION,
        contract_v2_1_digest=V21_DIGEST,
        requested_primary_listing_mic="XNAS",
        requested_calendar_token="XNAS",
        resolved_calendar="XNYS",
        calendar_alias_relationship="XNAS_USES_XNYS_SCHEDULE",
        exchange_calendars_version="4.13.2",
        tzdata_version="2025.2",
        fixed_start_date=sessions[0].session_date,
        fixed_end_date=sessions[-1].session_date,
        source_timezone="America/New_York",
        canonical_timezone="UTC",
        official_exchange_evidence_identity="TEST_OFFICIAL_EVIDENCE",
        official_exchange_evidence_digest="TEST_DIGEST",
        status=fc.CALENDAR_READY_FOR_FREEZE_REVIEW,
        sessions=sessions,
        semantic_digest=fc.semantic_digest(payload),
    )


def _bar(start: datetime, offset: int = 0, volume: str = "10") -> rth.SourceBar:
    base = Decimal("100") + Decimal(offset)
    return rth.SourceBar.build(
        window_start_utc=start,
        window_end_utc=start + timedelta(minutes=15),
        open=str(base),
        high=str(base + Decimal("2")),
        low=str(base - Decimal("1")),
        close=str(base + Decimal("0.5")),
        volume=volume,
    )


def _rth_bars(session: fc.FrozenCalendarSession) -> tuple[rth.SourceBar, ...]:
    return tuple(_bar(start, index) for index, start in enumerate(rth.expected_source_windows(session)))


def test_calendar_generation_uses_exact_package_pin_and_is_deterministic():
    request = fc.default_calendar_request(requested_primary_listing_mic="XNAS", requested_calendar_token="XNAS")
    calendar_one = fc.generate_frozen_calendar(request)
    calendar_two = fc.generate_frozen_calendar(request)

    assert request.exchange_calendars_version == "4.13.2"
    assert calendar_one.semantic_digest == calendar_two.semantic_digest
    assert calendar_one.requested_primary_listing_mic == "XNAS"
    assert calendar_one.requested_calendar_token == "XNAS"
    assert calendar_one.resolved_calendar == "XNYS"
    assert calendar_one.calendar_alias_relationship == "XNAS_USES_XNYS_SCHEDULE"
    assert calendar_one.status == fc.CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE
    assert len(calendar_one.normal_sessions()) > 900
    assert len(calendar_one.early_close_sessions()) > 0


def test_calendar_package_mismatch_and_unsupported_token_fail_closed(monkeypatch):
    original_version = fc.metadata.version

    def fake_version(package: str) -> str:
        if package == "exchange_calendars":
            return "0.0"
        return original_version(package)

    monkeypatch.setattr(fc.metadata, "version", fake_version)
    with pytest.raises(fc.CalendarGenerationError, match=fc.CALENDAR_IMPLEMENTATION_VERSION_MISMATCH):
        fc.default_calendar_request()

    monkeypatch.setattr(fc.metadata, "version", original_version)
    request = fc.default_calendar_request(requested_calendar_token="UNSUPPORTED")
    with pytest.raises(fc.CalendarGenerationError, match=fc.CALENDAR_SOURCE_UNRESOLVED):
        fc.generate_frozen_calendar(request)


def test_calendar_classifies_normal_early_close_closed_and_dst():
    calendar = fc.generate_frozen_calendar(fc.default_calendar_request())
    sessions = calendar.session_by_date()

    assert sessions["2024-01-02"].session_classification == fc.NORMAL_FULL_SESSION
    assert sessions["2024-01-02"].market_open_utc == "2024-01-02T14:30:00Z"
    assert sessions["2024-07-01"].market_open_utc == "2024-07-01T13:30:00Z"
    assert sessions["2024-11-29"].session_classification == fc.EARLY_CLOSE_SESSION
    assert sessions["2024-01-01"].session_classification == fc.FULL_MARKET_CLOSED
    assert sessions["2024-01-01"].market_open_utc is None


def test_source_bar_validation_decimal_timestamp_and_compatibility_semantic():
    start = datetime(2024, 1, 2, 14, 30, tzinfo=UTC)
    bar = _bar(start, volume="12.500")

    assert bar.window_end_utc == start + timedelta(minutes=15)
    assert bar.timestamp_utc == bar.window_start_utc
    assert bar.volume == Decimal("12.500")
    assert bar.semantic_payload()["volume"] == "12.5"

    bad_values = [
        {"open": 1.2},
        {"high": "NaN"},
        {"high": "99", "low": "100"},
        {"volume": "-1"},
        {"window_start_utc": datetime(2024, 1, 2, 14, 30)},
        {"window_start_utc": datetime(2024, 1, 2, 18, 30, tzinfo=timezone(timedelta(hours=4)))},
        {"window_end_utc": start + timedelta(minutes=30)},
        {"window_start_utc": datetime(2024, 1, 2, 14, 37, tzinfo=UTC)},
    ]
    for overrides in bad_values:
        kwargs = {
            "window_start_utc": start,
            "window_end_utc": start + timedelta(minutes=15),
            "open": "100",
            "high": "101",
            "low": "99",
            "close": "100",
            "volume": "1",
        }
        kwargs.update(overrides)
        with pytest.raises(rth.BarValidationError):
            rth.SourceBar.build(**kwargs)


def test_session_validation_complete_missing_duplicate_extra_extended_and_closed_conflict():
    session = _session("2024-01-02")
    calendar = _calendar(session, _session("2024-01-03", fc.FULL_MARKET_CLOSED))
    bars = _rth_bars(session)

    complete = rth.validate_session_sources(calendar, session, bars)
    assert complete.outcome == rth.SESSION_COMPLETE
    assert len(complete.accepted_source_bars) == 26

    assert rth.validate_session_sources(calendar, session, bars[1:]).outcome == rth.SESSION_SOURCE_INCOMPLETE
    assert rth.validate_session_sources(calendar, session, bars[:10] + bars[11:]).outcome == rth.SESSION_SOURCE_INCOMPLETE
    assert rth.validate_session_sources(calendar, session, bars[:-1]).outcome == rth.SESSION_SOURCE_INCOMPLETE
    assert rth.validate_session_sources(calendar, session, (bars[0],) + bars).outcome == rth.SESSION_SOURCE_DUPLICATE_SLOT

    extended = (_bar(datetime(2024, 1, 2, 13, 0, tzinfo=UTC), -10),) + bars
    result = rth.validate_session_sources(calendar, session, extended)
    assert result.outcome == rth.SESSION_COMPLETE
    assert result.extended_hours_exclusion_count == 1

    closed = calendar.sessions[1]
    assert rth.validate_session_sources(calendar, closed, (_bar(datetime(2024, 1, 3, 14, 30, tzinfo=UTC)),)).outcome == rth.CALENDAR_DATA_CONFLICT


def test_early_close_session_is_excluded_entirely():
    early = _session("2024-01-02", fc.EARLY_CLOSE_SESSION)
    calendar = _calendar(early)
    bars = tuple(_bar(datetime(2024, 1, 2, 14, 30, tzinfo=UTC) + i * timedelta(minutes=15), i) for i in range(13))

    result = rth.derive_profile_bars(calendar, bars, rth.PROFILE_SWING)

    assert result.early_close_exclusion_count == 1
    assert result.produced_bar_count == 0
    assert result.status == rth.DERIVATION_COMPLETE


def test_swing_aggregation_uses_exact_13_13_source_windows_and_decimal_sums():
    session = _session("2024-01-02")
    calendar = _calendar(session)
    result = rth.derive_profile_bars(calendar, _rth_bars(session), rth.PROFILE_SWING)

    assert result.status == rth.DERIVATION_COMPLETE
    assert result.accepted_full_session_count == 1
    assert result.produced_bar_count == 2
    morning, afternoon = result.bars
    assert morning.canonical_bar_type == rth.RTH_HALF_SESSION_195M
    assert morning.source_bar_count == 13
    assert afternoon.source_bar_count == 13
    assert morning.local_source_window_start == "09:30"
    assert morning.local_source_window_end == "12:45"
    assert afternoon.local_source_window_start == "12:45"
    assert afternoon.local_source_window_end == "16:00"
    assert morning.timestamp_utc == datetime(2024, 1, 2, 17, 45, tzinfo=UTC)
    assert afternoon.timestamp_utc == datetime(2024, 1, 2, 21, 0, tzinfo=UTC)
    assert morning.open == Decimal("100")
    assert morning.high == Decimal("114")
    assert morning.low == Decimal("99")
    assert morning.close == Decimal("112.5")
    assert morning.volume == Decimal("130")
    assert "open" not in result.public_receipt()


def test_position_swing_aggregation_uses_exact_26_source_windows():
    session = _session("2024-01-02")
    result = rth.derive_profile_bars(_calendar(session), _rth_bars(session), rth.PROFILE_POSITION_SWING)

    assert result.status == rth.DERIVATION_COMPLETE
    assert result.produced_bar_count == 1
    daily = result.bars[0]
    assert daily.canonical_bar_type == rth.RTH_FULL_SESSION_1D
    assert daily.source_bar_count == 26
    assert daily.local_source_window_start == "09:30"
    assert daily.local_source_window_end == "16:00"
    assert daily.timestamp_utc == datetime(2024, 1, 2, 21, 0, tzinfo=UTC)
    assert daily.open == Decimal("100")
    assert daily.high == Decimal("127")
    assert daily.low == Decimal("99")
    assert daily.close == Decimal("125.5")
    assert daily.volume == Decimal("260")


def test_incomplete_normal_session_blocks_complete_dataset_claim():
    session = _session("2024-01-02")
    result = rth.derive_profile_bars(_calendar(session), _rth_bars(session)[:-1], rth.PROFILE_POSITION_SWING)

    assert result.status == rth.DERIVATION_BLOCKED
    assert result.invalid_or_incomplete_session_count == 1
    assert result.produced_bar_count == 0
    assert "SESSION_SOURCE_INCOMPLETE" in result.findings[0]


def test_segment_assignment_normal_early_close_multiple_event_and_prefix_invariance():
    day1 = _session("2024-01-02")
    early = _session("2024-01-03", fc.EARLY_CLOSE_SESSION)
    day2 = _session("2024-01-04")
    calendar = _calendar(day1, early, day2)
    bars = rth.derive_profile_bars(calendar, _rth_bars(day1) + _rth_bars(day2), rth.PROFILE_SWING).bars
    events = (
        segments.ExDividendEvidence("2024-01-03", ("DIV-A", "DIV-B"), "EVENT-DIGEST-A"),
    )

    analytical, segmented = segments.assign_analytical_segments(
        bars,
        calendar=calendar,
        dividend_events=events,
        source_dataset_digest="DATASET-DIGEST",
        profile=rth.PROFILE_SWING,
    )

    assert analytical[0].start_reason == segments.DATASET_START
    assert analytical[1].start_reason == segments.EX_DIVIDEND_CONTINUITY_RESET
    assert analytical[1].segment_start_session_date == "2024-01-04"
    assert analytical[1].trigger_event_ids == ("DIV-A", "DIV-B")
    assert segmented[0].analysis_segment_id != segmented[-1].analysis_segment_id
    assert segments.current_segment_prefix(segmented, 2) == (bars[2],)
    with_future = bars + (bars[-1],)
    again = segments.assign_analytical_segments(
        with_future,
        calendar=calendar,
        dividend_events=events + (segments.ExDividendEvidence("2024-12-01", ("FUTURE",), "FUTURE-DIGEST"),),
        source_dataset_digest="DATASET-DIGEST",
        profile=rth.PROFILE_SWING,
    )[1]
    assert again[0].analysis_segment_id == segmented[0].analysis_segment_id
    assert again[2].analysis_segment_id == segmented[2].analysis_segment_id


def test_dry_cli_is_sanitized_offline_and_rejects_ticker_args():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["status"] == "HISTORICAL_DATA_ENGINE_READY_FOR_OFFLINE_SYNTHETIC_USE"
    assert receipt["contract_v2_1_digest"] == V21_DIGEST
    assert receipt["acquisition_enabled"] is False
    assert receipt["provider_execution_enabled"] is False
    assert "ticker" not in result.stdout.lower()
    rejected = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--ticker", "AAPL"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert rejected.returncode != 0


def test_contract_digests_and_prior_runtime_integrity_remain_unchanged():
    from marketflow.marketflow_data_parameters import fixed_analysis_profiles
    from marketflow.operational_artifacts import ARTIFACT_TYPE_ANNOTATED_DATASET
    from marketflow.research.data_readiness_remediation import FIXED_PROFILE_REQUIREMENTS

    assert fdac.contract_digest(fdac.load_contract_toml(REPO_ROOT / "config" / "fixed_date_acquisition_contract.example.toml")) == V1_DIGEST
    assert acv2.contract_digest(acv2.default_contract()) == V2_DIGEST
    assert acv21.contract_digest(acv21.default_contract()) == V21_DIGEST
    profiles = {profile.profile_id: profile for profile in fixed_analysis_profiles()}
    assert profiles["SWING"].candidate_timeframe == "4h"
    assert profiles["POSITION_SWING"].candidate_timeframe == "1d"
    assert ARTIFACT_TYPE_ANNOTATED_DATASET == "ANNOTATED_DATASET"
    assert FIXED_PROFILE_REQUIREMENTS["SWING"] == {"timeframe": "4h", "required_rows": 390}


def test_historical_data_source_assurance_boundaries():
    package_files = [
        REPO_ROOT / "marketflow" / "historical_data" / "__init__.py",
        REPO_ROOT / "marketflow" / "historical_data" / "frozen_calendar.py",
        REPO_ROOT / "marketflow" / "historical_data" / "rth_bar_engine.py",
        REPO_ROOT / "marketflow" / "historical_data" / "analytical_segments.py",
        REPO_ROOT / "marketflow" / "historical_data" / "__main__.py",
    ]
    forbidden_modules = {
        "polygon",
        "requests",
        "httpx",
        "socket",
        "urllib",
        "yfinance",
        "openai",
        "streamlit",
        "marketflow.marketflow_data_provider",
        "marketflow.marketflow_polygon_tools",
        "marketflow.marketflow_strategy",
        "marketflow.services.monte_carlo_service",
        "marketflow.services.backtest_result_service",
        "marketflow.services.walk_forward_validation_service",
        "marketflow.backtesting.outcome_engine",
    }
    combined = ""
    for path in package_files:
        source = path.read_text(encoding="utf-8")
        combined += source
        tree = ast.parse(source)
        imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
        attrs = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        assert forbidden_modules.isdisjoint(imported)
        assert forbidden_modules.isdisjoint(imported_from)
        assert "getenv" not in attrs
        assert "environ" not in attrs
        assert {"download", "request", "post", "put", "delete", "connect"}.isdisjoint(attrs)
    assert "REQUIRED_EXCHANGE_CALENDARS_VERSION = \"4.13.2\"" in combined
    assert "CALENDAR_IMPLEMENTATION_VERSION_MISMATCH" in combined
    assert "START_OF_AGGREGATE_WINDOW" in combined
    assert "timestamp_snapping" not in combined
    assert "provider_native_4h" not in combined
    assert "provider_native_1d" not in combined
    assert "LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION" in combined
    assert "exchange_calendars==4.13.2" in (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")
