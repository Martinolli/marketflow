"""Acquisition generation candidate contracts for fixed AAPL 2022-2025 bars."""

from __future__ import annotations

import json
import os
import csv
from copy import deepcopy
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Mapping
from zoneinfo import ZoneInfo

from marketflow.historical_data import provider_response
from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_provider_adapter_service as acquisition_adapter
from marketflow.services import dividend_event_operator_freeze_service as dividend_freeze
from marketflow.services import exchange_calendar_evidence_service as calendar_service


ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE = "ACQUISITION_GENERATION_CANDIDATE"
ARTIFACT_KIND_ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE = "ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE"
ARTIFACT_KIND_ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE = "ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE"
ARTIFACT_KIND_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS = "ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS"
ARTIFACT_KIND_ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN = "ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN"
SCHEMA_VERSION_ACQUISITION_GENERATION_CANDIDATE_V1 = "acquisition_generation_candidate_v1"
SCHEMA_VERSION_ACQUISITION_MONTHLY_LIVE_SMOKE_V1 = "acquisition_monthly_live_smoke_candidate_v1"
SCHEMA_VERSION_ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_V1 = "acquisition_monthly_reconciliation_triage_v1"
SCHEMA_VERSION_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS_V1 = "acquisition_per_session_reconciliation_diagnostics_v1"
SCHEMA_VERSION_ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_V1 = "acquisition_targeted_session_diagnostic_rerun_v1"
ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW = "ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW"
ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION = "ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION"
ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE = "ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE"
ACQUISITION_GENERATION_2025_01_CROSS_CHECK_MISMATCH = "ACQUISITION_GENERATION_2025_01_CROSS_CHECK_MISMATCH"
ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_READY = "ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_READY"
ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_BLOCKS_ACQUISITION_REVIEW = (
    "ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_BLOCKS_ACQUISITION_REVIEW"
)
ACQUISITION_PER_SESSION_DIAGNOSTICS_COMPLETE = "ACQUISITION_PER_SESSION_DIAGNOSTICS_COMPLETE"
ACQUISITION_PER_SESSION_DIAGNOSTICS_BLOCKED_MISSING_ROW_LEVEL_DATA = (
    "ACQUISITION_PER_SESSION_DIAGNOSTICS_BLOCKED_MISSING_ROW_LEVEL_DATA"
)
ACQUISITION_PER_SESSION_DIAGNOSTICS_REQUIRES_OPERATOR_REVIEW = (
    "ACQUISITION_PER_SESSION_DIAGNOSTICS_REQUIRES_OPERATOR_REVIEW"
)
ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_COMPLETE = "ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_COMPLETE"
ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_INCOMPLETE = "ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_INCOMPLETE"
ACQUISITION_OPERATOR_REVIEW_READY_AFTER_TRIAGE = "READY_AFTER_TRIAGE"
ACQUISITION_OPERATOR_REVIEW_BLOCKED_PENDING_RECONCILIATION_EXPLANATION = (
    "BLOCKED_PENDING_RECONCILIATION_EXPLANATION"
)
LIVE_TARGETED_SESSION_DIAGNOSTICS_BLOCKED_MISSING_API_KEY = "LIVE_TARGETED_SESSION_DIAGNOSTICS_BLOCKED_MISSING_API_KEY"
LIVE_TARGETED_SESSION_DIAGNOSTICS_BLOCKED_GATE_NOT_ENABLED = "LIVE_TARGETED_SESSION_DIAGNOSTICS_BLOCKED_GATE_NOT_ENABLED"
ACQUISITION_GENERATION_FROZEN = "ACQUISITION_GENERATION_FROZEN"
ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW = "ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW"
ACQUISITION_MONTHLY_LIVE_SMOKE_RECONCILIATION_MISMATCH = "ACQUISITION_MONTHLY_LIVE_SMOKE_RECONCILIATION_MISMATCH"
LIVE_ACQUISITION_GENERATION_BLOCKED_MISSING_API_KEY = "LIVE_ACQUISITION_GENERATION_BLOCKED_MISSING_API_KEY"
LIVE_ACQUISITION_GENERATION_BLOCKED_GATE_NOT_ENABLED = "LIVE_ACQUISITION_GENERATION_BLOCKED_GATE_NOT_ENABLED"
LIVE_ACQUISITION_SMOKE_BLOCKED_MISSING_API_KEY = "LIVE_ACQUISITION_SMOKE_BLOCKED_MISSING_API_KEY"
LIVE_ACQUISITION_SMOKE_BLOCKED_GATE_NOT_ENABLED = "LIVE_ACQUISITION_SMOKE_BLOCKED_GATE_NOT_ENABLED"
LIVE_ACQUISITION_SMOKE_PROVIDER_ERROR = "LIVE_ACQUISITION_SMOKE_PROVIDER_ERROR"
MARKETFLOW_ENABLE_LIVE_ACQUISITION_GENERATION = "MARKETFLOW_ENABLE_LIVE_ACQUISITION_GENERATION"

PROVIDER_NAME_MASSIVE = "Massive.com"
PROVIDER_ENDPOINT_MASSIVE_CUSTOM_BARS = "/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}"
PROVIDER_ENDPOINT_STABILITY_MASSIVE_AGGS_V2 = "CURRENT_STOCKS_V2_AGGS_RANGE"
PROVIDER_REQUEST_MODE_FAKE_TRANSPORT = "FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION"
PROVIDER_REQUEST_MODE_LIVE = "LIVE_PROVIDER_REQUEST"
CHUNKING_STRATEGY_MONTHLY = "MONTHLY"

RTH = "RTH"
EXTENDED_HOURS = "EXTENDED_HOURS"
OUT_OF_CALENDAR_RANGE = "OUT_OF_CALENDAR_RANGE"
UNKNOWN = "UNKNOWN"
RTH_SOURCE_ROWS_RECONCILED = "RTH_SOURCE_ROWS_RECONCILED"
RTH_SOURCE_ROWS_NOT_RECONCILED = "RTH_SOURCE_ROWS_NOT_RECONCILED"
ISSUE_CATEGORY_RECONCILED = "RECONCILED"
ISSUE_CATEGORY_RTH_ROW_COUNT_MISMATCH = "RTH_ROW_COUNT_MISMATCH"
ISSUE_CATEGORY_MISSING_PROVIDER_ROWS = "MISSING_PROVIDER_ROWS"
ISSUE_CATEGORY_EXTRA_PROVIDER_ROWS = "EXTRA_PROVIDER_ROWS"
ISSUE_CATEGORY_INSUFFICIENT_DETAIL = "INSUFFICIENT_DETAIL"
ISSUE_CATEGORY_MISSING_RTH_BARS = "MISSING_RTH_BARS"
ISSUE_CATEGORY_EXTRA_RTH_BARS = "EXTRA_RTH_BARS"
ISSUE_CATEGORY_INSUFFICIENT_ROW_LEVEL_DETAIL = "INSUFFICIENT_ROW_LEVEL_DETAIL"
ISSUE_CATEGORY_CALENDAR_SESSION_DURATION_REVIEW_REQUIRED = "CALENDAR_SESSION_DURATION_REVIEW_REQUIRED"
ISSUE_CATEGORY_UNKNOWN = "UNKNOWN"
SEVERITY_INFO = "INFO"
SEVERITY_HIGH = "HIGH"
SEVERITY_BLOCKER = "BLOCKER"

EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST = dividend_freeze.dividend.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST
EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST = dividend_freeze.dividend.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST
EXPECTED_SCHEDULE_SEMANTIC_DIGEST = dividend_freeze.dividend.EXPECTED_SCHEDULE_SEMANTIC_DIGEST
EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST = dividend_freeze.dividend.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST
EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST = "0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141"
EXPECTED_ACQUISITION_CONTRACT_DIGEST = dividend_freeze.dividend.EXPECTED_ACQUISITION_CONTRACT_DIGEST
EXPECTED_FULL_LIVE_ACQUISITION_CANDIDATE_DIGEST = "5b1f7507c4549b0cd590737e37571cd0ff18f5710c5bfb853bd04aeec6b3f1cb"
EXPECTED_FULL_LIVE_MONTHLY_RECONCILIATION_DIGEST = "d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4"
EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION = dividend_freeze.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION
PREDICTIVE_USEFULNESS_NOT_ACCEPTED = dividend_freeze.dividend.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = dividend_freeze.dividend.PROFITABILITY_NOT_ACCEPTED

FIXED_IDENTITY_SEGMENT = deepcopy(dividend_freeze.dividend.FIXED_IDENTITY_SEGMENT)
FIXED_ACQUISITION_CONTRACT = deepcopy(dividend_freeze.dividend.FIXED_ACQUISITION_CONTRACT)
ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK = {
    "ticker": "AAPL",
    "month": "2025-01",
    "normalized_source_rows": 1277,
    "extended_hours_rows": 757,
    "expected_rth_rows": 520,
    "validated_rth_rows": 520,
    "rth_reconciliation": RTH_SOURCE_ROWS_RECONCILED,
    "full_ordinary_sessions": 20,
    "incomplete_ordinary_sessions": 0,
    "swing_rth_half_session_195m_bars": 40,
    "position_swing_rth_full_session_1d_bars": 20,
    "requested_calendar": "XNAS",
    "resolved_calendar": "XNYS",
    "calendar_alias": "XNAS_USES_XNYS_SCHEDULE",
}

REMAINING_ROADMAP_AFTER_ACQUISITION_GENERATION_CANDIDATE = [
    "Full live acquisition smoke/generation.",
    "Acquisition generation operator review package.",
    "Acquisition generation freeze.",
    "SWING canonical dataset candidate.",
    "POSITION_SWING canonical dataset candidate.",
]

DEFAULT_PER_SESSION_DIAGNOSTIC_TARGET_MONTHS = [
    "2022-11",
    "2023-07",
    "2023-11",
    "2024-07",
    "2024-11",
    "2024-12",
    "2025-07",
    "2025-11",
    "2025-12",
]

PER_SESSION_RECONCILIATION_CSV_COLUMNS = [
    "session_date",
    "month",
    "session_type",
    "expected_15m_bars",
    "observed_15m_bars",
    "rth_row_delta",
    "missing_count",
    "extra_count",
    "first_observed_rth_timestamp_utc",
    "last_observed_rth_timestamp_utc",
    "provider_chunk_id",
    "provider_chunk_month",
    "issue_category",
    "issue_severity",
    "notes",
]

TARGETED_SESSION_DIAGNOSTIC_CSV_COLUMNS = [
    "month",
    "session_date",
    "calendar_open_local",
    "calendar_close_local",
    "calendar_open_utc",
    "calendar_close_utc",
    "session_minutes",
    "is_full_session",
    "is_special_close",
    "is_holiday_adjacent",
    "expected_rth_rows",
    "observed_rth_rows",
    "rth_row_delta",
    "first_observed_rth_timestamp_utc",
    "last_observed_rth_timestamp_utc",
    "missing_rth_bar_count",
    "extra_rth_bar_count",
    "issue_category",
    "issue_severity",
    "diagnostic_reason",
    "requires_provider_recheck",
    "requires_calendar_logic_review",
    "requires_timezone_review",
    "requires_algorithm_review",
]


class AcquisitionGenerationError(ValueError):
    """Raised when acquisition generation candidate data violates its contract."""


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise AcquisitionGenerationError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise AcquisitionGenerationError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise AcquisitionGenerationError(f"{field_name} must be true")


def _date_range_months(start_date: str, end_date: str) -> list[str]:
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    cursor = date(start.year, start.month, 1)
    months: list[str] = []
    while cursor <= end:
        months.append(f"{cursor.year:04d}-{cursor.month:02d}")
        year = cursor.year + (1 if cursor.month == 12 else 0)
        month = 1 if cursor.month == 12 else cursor.month + 1
        cursor = date(year, month, 1)
    return months


def _month_bounds(month_key: str, *, range_start: str, range_end: str) -> tuple[str, str]:
    year_text, month_text = month_key.split("-", 1)
    year = int(year_text)
    month = int(month_text)
    month_start = date(year, month, 1)
    next_month = date(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1)
    month_end = next_month - timedelta(days=1)
    return max(month_start, date.fromisoformat(range_start)).isoformat(), min(month_end, date.fromisoformat(range_end)).isoformat()


def _request_digest_payload(request: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(request)
    payload.pop("request_semantic_digest", None)
    return payload


def build_massive_custom_bars_request_v1(
    *,
    ticker: str,
    start_date: str,
    end_date: str,
    multiplier: int = 15,
    timespan: str = "minute",
    adjusted: bool = True,
    sort: str = "asc",
    limit: int = 50000,
    api_key: str | None = None,
) -> dict[str, Any]:
    """Build sanitized Massive custom-bars request metadata without storing API keys."""
    ticker_text = ticker.strip().upper()
    if ticker_text != FIXED_IDENTITY_SEGMENT["ticker"]:
        raise AcquisitionGenerationError("ticker must match fixed identity segment")
    if start_date > end_date:
        raise AcquisitionGenerationError("start_date must be <= end_date")
    if multiplier != 15 or timespan != "minute" or adjusted is not True or sort != "asc":
        raise AcquisitionGenerationError("provider request must match fixed acquisition contract")
    if int(limit) <= 0:
        raise AcquisitionGenerationError("limit must be positive")
    endpoint_path = f"/v2/aggs/ticker/{ticker_text}/range/{multiplier}/{timespan}/{start_date}/{end_date}"
    request = {
        "provider_name": PROVIDER_NAME_MASSIVE,
        "provider_endpoint": PROVIDER_ENDPOINT_MASSIVE_CUSTOM_BARS,
        "provider_endpoint_path": endpoint_path,
        "provider_endpoint_stability": PROVIDER_ENDPOINT_STABILITY_MASSIVE_AGGS_V2,
        "provider_query_identifier": ticker_text,
        "provider_query_ticker": ticker_text,
        "provider_query_composite_figi": FIXED_IDENTITY_SEGMENT["composite_figi"],
        "provider_query_start": start_date,
        "provider_query_end": end_date,
        "provider_multiplier": int(multiplier),
        "provider_timespan": timespan,
        "provider_adjusted": adjusted,
        "provider_sort": sort,
        "provider_limit": int(limit),
        "provider_request_mode": PROVIDER_REQUEST_MODE_LIVE if api_key else PROVIDER_REQUEST_MODE_FAKE_TRANSPORT,
        "api_key_supplied": bool(api_key),
        "api_key_stored": False,
        "request_url_without_credentials": f"https://api.massive.com{endpoint_path}?adjusted=true&sort=asc&limit={int(limit)}",
    }
    request["request_semantic_digest"] = semantic_digest(_request_digest_payload(request))
    return request


def build_acquisition_month_chunks_v1(
    *,
    start_date: str = "2022-01-01",
    end_date: str = "2025-12-31",
    ticker: str = "AAPL",
    limit: int = 50000,
) -> list[dict[str, Any]]:
    """Build deterministic monthly custom-bars chunk metadata for the fixed range."""
    chunks: list[dict[str, Any]] = []
    for index, month_key in enumerate(_date_range_months(start_date, end_date), start=1):
        chunk_start, chunk_end = _month_bounds(month_key, range_start=start_date, range_end=end_date)
        request = build_massive_custom_bars_request_v1(
            ticker=ticker,
            start_date=chunk_start,
            end_date=chunk_end,
            limit=limit,
        )
        chunk = {
            "chunk_id": f"AAPL-{month_key}",
            "chunk_ordinal": index,
            "month": month_key,
            "effective_start_date": chunk_start,
            "effective_end_date": chunk_end,
            "request": request,
            "request_semantic_digest": request["request_semantic_digest"],
        }
        chunks.append(chunk)
    return chunks


def chunk_manifest_digest_v1(chunks: list[dict[str, Any]]) -> str:
    return semantic_digest(chunks)


def _body_bytes(provider_response_data: Mapping[str, Any] | bytes) -> bytes:
    if isinstance(provider_response_data, bytes):
        return provider_response_data
    if isinstance(provider_response_data, Mapping):
        return canonical_json_bytes(dict(provider_response_data))
    raise AcquisitionGenerationError("provider response must be bytes or a mapping")


def fetch_massive_custom_bars_v1(
    *,
    ticker: str,
    start_date: str,
    end_date: str,
    api_key: str,
    multiplier: int = 15,
    timespan: str = "minute",
    adjusted: bool = True,
    sort: str = "asc",
    limit: int = 50000,
    transport: Callable[[dict[str, Any]], Mapping[str, Any] | bytes] | None = None,
) -> dict[str, Any]:
    """Execute a custom-bars request through an injected transport and parse the response."""
    if not api_key:
        raise AcquisitionGenerationError("api_key is required for acquisition generation fetch")
    request = build_massive_custom_bars_request_v1(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        multiplier=multiplier,
        timespan=timespan,
        adjusted=adjusted,
        sort=sort,
        limit=limit,
        api_key=api_key,
    )
    if transport is None:
        raise AcquisitionGenerationError("live acquisition transport is not configured")
    response_data = transport(request)
    body = _body_bytes(response_data)
    raw_digest = sha256_bytes(body)
    parsed = provider_response.parse_provider_response(
        body,
        body_sha256=raw_digest,
        context=provider_response.ResponseRequestContext(
            canonical_ticker=ticker.strip().upper(),
            month_key=start_date[:7],
            effective_start_date=start_date,
            effective_end_date=end_date,
            adjusted=adjusted,
            sort=sort,
            limit=limit,
            month_request_digest=request["request_semantic_digest"],
        ),
    )
    return {
        "request": request,
        "provider_response_status": parsed.status,
        "provider_response_row_count": len(parsed.rows),
        "provider_raw_response_digest": raw_digest,
        "provider_projection_digest": parsed.semantic_projection_digest,
        "parsed_rows": parsed.rows,
    }


def _decode_payload(provider_response_data: Mapping[str, Any] | bytes) -> dict[str, Any]:
    body = _body_bytes(provider_response_data)
    try:
        payload = json.loads(body.decode("utf-8"), parse_float=Decimal, parse_int=int)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AcquisitionGenerationError("provider response must be UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise AcquisitionGenerationError("provider response must decode to a JSON object")
    return payload


def _decimal_text(value: Decimal | int | None) -> str | None:
    if value is None:
        return None
    decimal = value if isinstance(value, Decimal) else Decimal(value)
    if decimal == 0:
        return "0"
    text = format(decimal.normalize(), "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _raw_rows_by_timestamp(payload: dict[str, Any]) -> dict[int, dict[str, Any]]:
    rows = payload.get("results")
    if not isinstance(rows, list):
        return {}
    by_timestamp: dict[int, dict[str, Any]] = {}
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("t"), int):
            by_timestamp[int(row["t"])] = row
    return by_timestamp


def normalize_provider_response_rows_v1(
    *,
    chunk: dict[str, Any],
    provider_response_data: Mapping[str, Any] | bytes,
) -> dict[str, Any]:
    """Normalize one provider response page into deterministic source rows."""
    body = _body_bytes(provider_response_data)
    raw_digest = sha256_bytes(body)
    request = chunk["request"]
    parsed = provider_response.parse_provider_response(
        body,
        body_sha256=raw_digest,
        context=provider_response.ResponseRequestContext(
            canonical_ticker=request["provider_query_ticker"],
            month_key=chunk["month"],
            effective_start_date=chunk["effective_start_date"],
            effective_end_date=chunk["effective_end_date"],
            adjusted=request["provider_adjusted"],
            sort=request["provider_sort"],
            limit=request["provider_limit"],
            month_request_digest=request["request_semantic_digest"],
        ),
    )
    raw_rows = _raw_rows_by_timestamp(_decode_payload(provider_response_data))
    normalized: list[dict[str, Any]] = []
    for index, row in enumerate(parsed.rows):
        raw = raw_rows.get(row.provider_timestamp, {})
        normalized_row = {
            "ticker": parsed.ticker,
            "timestamp_utc": row.window_start_utc,
            "timestamp_source": row.provider_timestamp,
            "timestamp_source_timezone": FIXED_ACQUISITION_CONTRACT["source_timezone"],
            "open": _decimal_text(row.open),
            "high": _decimal_text(row.high),
            "low": _decimal_text(row.low),
            "close": _decimal_text(row.close),
            "volume": _decimal_text(row.volume),
            "vwap": _decimal_text(row.vwap),
            "transactions": row.transaction_count,
            "otc": raw.get("otc") if "otc" in raw else None,
            "adjusted": parsed.adjusted,
            "source_interval_minutes": 15,
            "source_row_index": index,
            "source_chunk_id": chunk["chunk_id"],
            "source_month": chunk["month"],
            "raw_row_digest": semantic_digest(raw),
        }
        normalized.append(normalized_row)
    return {
        "chunk_id": chunk["chunk_id"],
        "month": chunk["month"],
        "provider_response_status": parsed.status,
        "provider_response_row_count": len(normalized),
        "provider_raw_response_digest": raw_digest,
        "provider_projection_digest": parsed.semantic_projection_digest,
        "normalized_rows": normalized,
    }


def normalized_source_rows_digest_v1(rows: list[dict[str, Any]]) -> str:
    return semantic_digest(rows)


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _local_date(value: str) -> str:
    return _parse_utc(value).astimezone(ZoneInfo(FIXED_ACQUISITION_CONTRACT["source_timezone"])).date().isoformat()


def classify_normalized_source_rows_v1(
    rows: list[dict[str, Any]],
    *,
    schedule_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Classify normalized source rows against the frozen regular-session schedule."""
    schedule = schedule_rows if schedule_rows is not None else calendar_service.build_exchange_calendar_schedule_rows_v1()
    by_date = {row["session_date"]: row for row in schedule}
    classified: list[dict[str, Any]] = []
    for row in rows:
        item = deepcopy(row)
        timestamp = row.get("timestamp_utc")
        if not isinstance(timestamp, str):
            item["session_classification"] = UNKNOWN
            classified.append(item)
            continue
        session_date = _local_date(timestamp)
        schedule_row = by_date.get(session_date)
        item["session_date"] = session_date
        if schedule_row is None:
            item["session_classification"] = OUT_OF_CALENDAR_RANGE
        else:
            market_open = _parse_utc(schedule_row["market_open_utc"])
            market_close = _parse_utc(schedule_row["market_close_utc"])
            row_time = _parse_utc(timestamp)
            item["session_classification"] = RTH if market_open <= row_time < market_close else EXTENDED_HOURS
        classified.append(item)
    return classified


def _rows_for_month(rows: list[dict[str, Any]], month: str) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("source_month") == month or str(row.get("session_date", ""))[:7] == month]


def build_monthly_reconciliation_v1(
    rows: list[dict[str, Any]],
    *,
    chunks: list[dict[str, Any]] | None = None,
    schedule_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build deterministic monthly RTH/extended-hours reconciliation summaries."""
    chunk_list = chunks if chunks is not None else build_acquisition_month_chunks_v1()
    schedule = schedule_rows if schedule_rows is not None else calendar_service.build_exchange_calendar_schedule_rows_v1()
    classified = classify_normalized_source_rows_v1(rows, schedule_rows=schedule)
    by_schedule_month: dict[str, list[dict[str, Any]]] = {}
    for schedule_row in schedule:
        by_schedule_month.setdefault(schedule_row["session_date"][:7], []).append(schedule_row)
    summaries: list[dict[str, Any]] = []
    for chunk in chunk_list:
        month = chunk["month"]
        month_rows = _rows_for_month(classified, month)
        rth_rows = [row for row in month_rows if row.get("session_classification") == RTH]
        extended_rows = [row for row in month_rows if row.get("session_classification") == EXTENDED_HOURS]
        out_rows = [row for row in month_rows if row.get("session_classification") == OUT_OF_CALENDAR_RANGE]
        unknown_rows = [row for row in month_rows if row.get("session_classification") == UNKNOWN]
        full_sessions = [row for row in by_schedule_month.get(month, []) if row.get("is_full_session") is True]
        counts_by_session: dict[str, int] = {}
        for row in rth_rows:
            counts_by_session[str(row["session_date"])] = counts_by_session.get(str(row["session_date"]), 0) + 1
        incomplete = sum(1 for session in full_sessions if counts_by_session.get(session["session_date"], 0) != 26)
        complete = len(full_sessions) - incomplete
        expected_rth = len(full_sessions) * 26
        status = RTH_SOURCE_ROWS_RECONCILED if len(rth_rows) == expected_rth and incomplete == 0 else RTH_SOURCE_ROWS_NOT_RECONCILED
        errors = [] if status == RTH_SOURCE_ROWS_RECONCILED else ["RTH_SOURCE_ROWS_NOT_RECONCILED"]
        summaries.append(
            {
                "month": month,
                "normalized_source_rows": len(month_rows),
                "rth_rows": len(rth_rows),
                "extended_hours_rows": len(extended_rows),
                "out_of_calendar_range_rows": len(out_rows),
                "unknown_session_rows": len(unknown_rows),
                "expected_rth_rows": expected_rth,
                "validated_rth_rows": len(rth_rows),
                "rth_reconciliation_status": status,
                "full_ordinary_sessions": len(full_sessions),
                "incomplete_ordinary_sessions": incomplete,
                "swing_rth_half_session_195m_bars": complete * 2,
                "position_swing_rth_full_session_1d_bars": complete,
                "warnings": [],
                "errors": errors,
            }
        )
    return summaries


def monthly_reconciliation_digest_v1(monthly_reconciliation: list[dict[str, Any]]) -> str:
    return semantic_digest(monthly_reconciliation)


def _authority_boundary() -> dict[str, Any]:
    return {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
    }


def _authority_bindings() -> dict[str, Any]:
    return {
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_audit_frozen_digest": EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
    }


def _receipt_digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "provider_request_mode": candidate.get("provider_request_mode"),
        "provider_requests_made": candidate.get("provider_requests_made"),
        "provider_response_injected": candidate.get("provider_response_injected"),
        "provider_raw_response_digest": candidate.get("provider_raw_response_digest"),
        "normalized_source_rows_digest": candidate.get("normalized_source_rows_digest"),
        "monthly_reconciliation_digest": candidate.get("monthly_reconciliation_digest"),
        "chunk_manifest_digest": candidate.get("provider_chunk_manifest_digest"),
        "chunk_count_completed": candidate.get("chunk_count_completed"),
        "failed_chunk_count": candidate.get("failed_chunk_count"),
        "normalized_source_row_count": candidate.get("normalized_source_row_count"),
        "rth_row_count": candidate.get("rth_row_count"),
        "extended_hours_row_count": candidate.get("extended_hours_row_count"),
    }


def _candidate_digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("acquisition_generation_candidate_semantic_digest", None)
    payload.pop("acquisition_generation_candidate_payload_digest", None)
    return payload


def acquisition_generation_candidate_semantic_digest(candidate: dict[str, Any]) -> str:
    return semantic_digest(_candidate_digest_payload(candidate))


def _monthly_smoke_digest_payload(smoke: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(smoke)
    payload.pop("acquisition_smoke_receipt_digest", None)
    payload.pop("acquisition_monthly_smoke_candidate_digest", None)
    return payload


def acquisition_monthly_smoke_candidate_digest_v1(smoke: dict[str, Any]) -> str:
    return semantic_digest(_monthly_smoke_digest_payload(smoke))


def _smoke_receipt_payload(smoke: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": smoke["artifact_kind"],
        "candidate_status": smoke["candidate_status"],
        "provider_request_mode": smoke.get("provider_request_mode"),
        "provider_response_status": smoke.get("provider_response_status"),
        "provider_raw_response_digest": smoke.get("provider_raw_response_digest"),
        "normalized_source_rows_digest": smoke.get("normalized_source_rows_digest"),
        "monthly_reconciliation_digest": smoke.get("monthly_reconciliation_digest"),
        "normalized_source_row_count": smoke.get("normalized_source_row_count"),
        "rth_row_count": smoke.get("rth_row_count"),
        "extended_hours_row_count": smoke.get("extended_hours_row_count"),
        "rth_reconciliation_status": smoke.get("rth_reconciliation_status"),
        "accepted_2025_01_cross_check_passed": smoke.get("accepted_2025_01_cross_check_passed"),
    }


def _month_chunk_for_smoke(*, ticker: str, month: str) -> dict[str, Any]:
    if ticker.strip().upper() != FIXED_IDENTITY_SEGMENT["ticker"]:
        raise AcquisitionGenerationError("ticker must match fixed identity segment")
    if month != ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK["month"]:
        raise AcquisitionGenerationError("monthly live smoke is fixed to 2025-01")
    start_date, end_date = _month_bounds(month, range_start=f"{month}-01", range_end=f"{month}-31")
    request = build_massive_custom_bars_request_v1(ticker=ticker, start_date=start_date, end_date=end_date)
    return {
        "chunk_id": f"{ticker.strip().upper()}-{month}",
        "chunk_ordinal": 1,
        "month": month,
        "effective_start_date": start_date,
        "effective_end_date": end_date,
        "request": request,
        "request_semantic_digest": request["request_semantic_digest"],
    }


def _blocked_monthly_smoke(
    *,
    status: str,
    ticker: str,
    month: str,
    request_timestamp_utc: str | None,
) -> dict[str, Any]:
    smoke = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE,
        "schema_version": SCHEMA_VERSION_ACQUISITION_MONTHLY_LIVE_SMOKE_V1,
        "candidate_status": status,
        "ticker": ticker.strip().upper(),
        "month": month,
        "range_start": f"{month}-01",
        "range_end": f"{month}-31",
        "created_offline": True,
        "provider_requests_made": False,
        "provider_response_injected": False,
        "provider_request_mode": None,
        "provider_request_timestamp_utc": request_timestamp_utc,
        "provider_response_status": None,
        "provider_raw_row_count": None,
        "provider_raw_response_digest": None,
        "provider_raw_body_sha256": None,
        "normalized_source_row_count": None,
        "rth_row_count": None,
        "extended_hours_row_count": None,
        "expected_rth_rows": ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK["expected_rth_rows"],
        "validated_rth_rows": None,
        "rth_reconciliation_status": None,
        "full_ordinary_sessions": None,
        "incomplete_ordinary_sessions": None,
        "swing_rth_half_session_195m_bars": None,
        "position_swing_rth_full_session_1d_bars": None,
        "normalized_source_rows_digest": None,
        "monthly_reconciliation_digest": None,
        "accepted_2025_01_cross_check": deepcopy(ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK),
        "accepted_2025_01_cross_check_passed": False,
        "normalized_source_rows": [],
        "monthly_reconciliation": [],
        "request_metadata": None,
        "identity_segment": deepcopy(FIXED_IDENTITY_SEGMENT),
        "acquisition_contract": deepcopy(FIXED_ACQUISITION_CONTRACT),
        "authority_bindings": _authority_bindings(),
        "authority_boundary": _authority_boundary(),
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_audit_frozen_digest": EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "api_key_stored": False,
        "raw_provider_payload_stored": False,
        "generated_bars_stored": False,
        "next_required_task": "Full 2022-2025 live acquisition generation candidate, after operator review of monthly smoke.",
    }
    smoke["acquisition_smoke_receipt_digest"] = semantic_digest(_smoke_receipt_payload(smoke))
    smoke["acquisition_monthly_smoke_candidate_digest"] = acquisition_monthly_smoke_candidate_digest_v1(smoke)
    return smoke


def _api_key_from_environment() -> str | None:
    return os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")


def _january_cross_check_passed(summary: dict[str, Any]) -> bool:
    expected = ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK
    return (
        summary.get("month") == expected["month"]
        and summary.get("normalized_source_rows") == expected["normalized_source_rows"]
        and summary.get("extended_hours_rows") == expected["extended_hours_rows"]
        and summary.get("expected_rth_rows") == expected["expected_rth_rows"]
        and summary.get("validated_rth_rows") == expected["validated_rth_rows"]
        and summary.get("rth_reconciliation_status") == expected["rth_reconciliation"]
        and summary.get("full_ordinary_sessions") == expected["full_ordinary_sessions"]
        and summary.get("incomplete_ordinary_sessions") == expected["incomplete_ordinary_sessions"]
        and summary.get("swing_rth_half_session_195m_bars") == expected["swing_rth_half_session_195m_bars"]
        and summary.get("position_swing_rth_full_session_1d_bars") == expected["position_swing_rth_full_session_1d_bars"]
    )


def build_acquisition_generation_monthly_live_smoke_v1(
    *,
    ticker: str = "AAPL",
    month: str = "2025-01",
    api_key: str | None = None,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Build one-month custom-bars smoke evidence without promoting acquisition authority."""
    ticker_text = ticker.strip().upper()
    timestamp = request_timestamp_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if transport is None and os.environ.get(MARKETFLOW_ENABLE_LIVE_ACQUISITION_GENERATION) != "1":
        return _blocked_monthly_smoke(
            status=LIVE_ACQUISITION_SMOKE_BLOCKED_GATE_NOT_ENABLED,
            ticker=ticker_text,
            month=month,
            request_timestamp_utc=timestamp,
        )
    key = api_key or _api_key_from_environment()
    if not key:
        return _blocked_monthly_smoke(
            status=LIVE_ACQUISITION_SMOKE_BLOCKED_MISSING_API_KEY,
            ticker=ticker_text,
            month=month,
            request_timestamp_utc=timestamp,
        )
    chunk = _month_chunk_for_smoke(ticker=ticker_text, month=month)
    try:
        raw = acquisition_adapter.fetch_massive_custom_bars_live_v1(
            ticker=ticker_text,
            start_date=chunk["effective_start_date"],
            end_date=chunk["effective_end_date"],
            api_key=key,
            transport=transport,
            request_timestamp_utc=timestamp,
        )
        normalized = normalize_provider_response_rows_v1(chunk=chunk, provider_response_data=raw["provider_response_body"])
        normalized_rows = normalized["normalized_rows"]
        classified_rows = classify_normalized_source_rows_v1(normalized_rows)
        monthly_reconciliation = build_monthly_reconciliation_v1(classified_rows, chunks=[chunk])
        january_summary = monthly_reconciliation[0]
        cross_check_passed = _january_cross_check_passed(january_summary)
        candidate_status = (
            ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW
            if cross_check_passed
            else ACQUISITION_MONTHLY_LIVE_SMOKE_RECONCILIATION_MISMATCH
        )
        normalized_digest = normalized_source_rows_digest_v1(normalized_rows)
        monthly_digest = monthly_reconciliation_digest_v1(monthly_reconciliation)
        smoke = {
            "artifact_kind": ARTIFACT_KIND_ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE,
            "schema_version": SCHEMA_VERSION_ACQUISITION_MONTHLY_LIVE_SMOKE_V1,
            "candidate_status": candidate_status,
            "ticker": ticker_text,
            "month": month,
            "range_start": chunk["effective_start_date"],
            "range_end": chunk["effective_end_date"],
            "created_offline": transport is not None,
            "provider_requests_made": raw["provider_requests_made"],
            "provider_response_injected": raw["provider_response_injected"],
            "provider_request_mode": raw["provider_request_mode"],
            "provider_request_timestamp_utc": timestamp,
            "provider_response_status": raw["provider_response_status"],
            "provider_raw_row_count": raw["provider_raw_response_row_count"],
            "provider_raw_response_digest": raw["provider_raw_response_digest"],
            "provider_raw_body_sha256": raw["provider_raw_body_sha256"],
            "normalized_source_row_count": len(normalized_rows),
            "rth_row_count": january_summary["rth_rows"],
            "extended_hours_row_count": january_summary["extended_hours_rows"],
            "expected_rth_rows": january_summary["expected_rth_rows"],
            "validated_rth_rows": january_summary["validated_rth_rows"],
            "rth_reconciliation_status": january_summary["rth_reconciliation_status"],
            "full_ordinary_sessions": january_summary["full_ordinary_sessions"],
            "incomplete_ordinary_sessions": january_summary["incomplete_ordinary_sessions"],
            "swing_rth_half_session_195m_bars": january_summary["swing_rth_half_session_195m_bars"],
            "position_swing_rth_full_session_1d_bars": january_summary["position_swing_rth_full_session_1d_bars"],
            "normalized_source_rows_digest": normalized_digest,
            "monthly_reconciliation_digest": monthly_digest,
            "accepted_2025_01_cross_check": deepcopy(ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK),
            "accepted_2025_01_cross_check_passed": cross_check_passed,
            "normalized_source_rows": normalized_rows,
            "monthly_reconciliation": monthly_reconciliation,
            "request_metadata": raw["request"],
            "identity_segment": deepcopy(FIXED_IDENTITY_SEGMENT),
            "acquisition_contract": deepcopy(FIXED_ACQUISITION_CONTRACT),
            "authority_bindings": _authority_bindings(),
            "authority_boundary": _authority_boundary(),
            "identity_segment_frozen": True,
            "calendar_operator_frozen": True,
            "split_event_audit_frozen": True,
            "dividend_event_audit_frozen": True,
            "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
            "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
            "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
            "split_event_audit_frozen_digest": EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
            "dividend_event_audit_frozen_digest": EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
            "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
            "in_range_dividends_found": True,
            "in_range_dividend_count": 16,
            "in_range_dividend_implication": EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
            "acquisition_generation_freeze": False,
            "canonical_eligibility": False,
            "registry_eligibility": False,
            "strategy_runtime_migration": False,
            "automatic_stitching": False,
            "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            "profitability": PROFITABILITY_NOT_ACCEPTED,
            "api_key_stored": False,
            "raw_provider_payload_stored": False,
            "generated_bars_stored": False,
            "next_required_task": "Full 2022-2025 live acquisition generation candidate, after operator review of monthly smoke.",
        }
    except Exception as exc:
        smoke = _blocked_monthly_smoke(
            status=LIVE_ACQUISITION_SMOKE_PROVIDER_ERROR,
            ticker=ticker_text,
            month=month,
            request_timestamp_utc=timestamp,
        )
        smoke["provider_response_status"] = type(exc).__name__
    smoke["acquisition_smoke_receipt_digest"] = semantic_digest(_smoke_receipt_payload(smoke))
    smoke["acquisition_monthly_smoke_candidate_digest"] = acquisition_monthly_smoke_candidate_digest_v1(smoke)
    return smoke


def _provider_records_from_responses(
    provider_responses: list[dict[str, Any]],
    *,
    chunks: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    chunks_by_month = {chunk["month"]: chunk for chunk in chunks}
    chunk_records: list[dict[str, Any]] = []
    normalized_rows: list[dict[str, Any]] = []
    for item in provider_responses:
        month = str(item["month"])
        chunk = chunks_by_month[month]
        result = normalize_provider_response_rows_v1(chunk=chunk, provider_response_data=item["response"])
        chunk_normalized_rows = result["normalized_rows"]
        raw_metadata = item.get("raw_metadata") if isinstance(item.get("raw_metadata"), Mapping) else {}
        request_metadata = raw_metadata.get("request") if isinstance(raw_metadata.get("request"), Mapping) else None
        chunk_records.append(
            {
                "chunk_id": chunk["chunk_id"],
                "month": month,
                "from": chunk["effective_start_date"],
                "to": chunk["effective_end_date"],
                "provider_response_status": result["provider_response_status"],
                "raw_row_count": result["provider_response_row_count"],
                "normalized_row_count": len(chunk_normalized_rows),
                "rth_row_count": None,
                "extended_hours_row_count": None,
                "out_of_calendar_range_row_count": None,
                "unknown_session_row_count": None,
                "provider_response_row_count": result["provider_response_row_count"],
                "raw_response_digest": result["provider_raw_response_digest"],
                "provider_raw_response_digest": result["provider_raw_response_digest"],
                "provider_raw_body_sha256": raw_metadata.get("provider_raw_body_sha256"),
                "provider_raw_metadata_digest": raw_metadata.get("provider_raw_response_digest"),
                "normalized_rows_digest": normalized_source_rows_digest_v1(chunk_normalized_rows),
                "monthly_reconciliation_digest": None,
                "provider_projection_digest": result["provider_projection_digest"],
                "request_semantic_digest": chunk["request_semantic_digest"],
                "request_metadata": deepcopy(request_metadata),
                "warnings": [],
                "errors": [],
            }
        )
        normalized_rows.extend(chunk_normalized_rows)
    normalized_rows.sort(key=lambda row: (row["timestamp_utc"], row["source_chunk_id"], row["source_row_index"]))
    for index, row in enumerate(normalized_rows):
        row["source_row_index"] = index
    return chunk_records, normalized_rows


def _merge_reconciliation_into_provider_records(
    provider_records: list[dict[str, Any]],
    monthly_reconciliation: list[dict[str, Any]],
) -> None:
    by_month = {item["month"]: item for item in monthly_reconciliation}
    for record in provider_records:
        summary = by_month.get(record["month"])
        if not summary:
            continue
        record["rth_row_count"] = summary["rth_rows"]
        record["extended_hours_row_count"] = summary["extended_hours_rows"]
        record["out_of_calendar_range_row_count"] = summary["out_of_calendar_range_rows"]
        record["unknown_session_row_count"] = summary["unknown_session_rows"]
        record["monthly_reconciliation_digest"] = semantic_digest(summary)
        record["warnings"] = list(summary["warnings"])
        record["errors"] = list(summary["errors"])


def _january_2025_summary(monthly_reconciliation: list[dict[str, Any]]) -> dict[str, Any] | None:
    return next((item for item in monthly_reconciliation if item.get("month") == "2025-01"), None)


def _candidate_status_for_generation(
    *,
    generated: bool,
    completed_chunks: int,
    expected_chunks: int,
    failed_chunks: int,
    january_cross_check_passed: bool,
) -> str:
    if not generated:
        return ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION
    if failed_chunks or completed_chunks != expected_chunks:
        return ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE
    if not january_cross_check_passed:
        return ACQUISITION_GENERATION_2025_01_CROSS_CHECK_MISMATCH
    return ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW


def build_acquisition_generation_candidate_v1(
    *,
    provider_responses: list[dict[str, Any]] | None = None,
    provider_request_timestamp_utc: str | None = None,
    failed_chunk_records: list[dict[str, Any]] | None = None,
    provider_request_mode: str | None = None,
    provider_requests_made: bool = False,
    provider_response_injected: bool | None = None,
    created_offline: bool | None = None,
) -> dict[str, Any]:
    """Build a candidate-only acquisition generation artifact."""
    chunks = build_acquisition_month_chunks_v1()
    generated = provider_responses is not None
    failed_records = [deepcopy(item) for item in (failed_chunk_records or [])]
    if provider_response_injected is None:
        provider_response_injected = generated and not provider_requests_made
    if created_offline is None:
        created_offline = not provider_requests_made
    if provider_request_mode is None:
        provider_request_mode = PROVIDER_REQUEST_MODE_FAKE_TRANSPORT if generated else None
    provider_records: list[dict[str, Any]] = []
    normalized_rows: list[dict[str, Any]] = []
    monthly_reconciliation: list[dict[str, Any]] = []
    classified_rows: list[dict[str, Any]] = []
    if generated:
        provider_records, normalized_rows = _provider_records_from_responses(provider_responses or [], chunks=chunks)
        classified_rows = classify_normalized_source_rows_v1(normalized_rows)
        monthly_reconciliation = build_monthly_reconciliation_v1(classified_rows, chunks=chunks)
        _merge_reconciliation_into_provider_records(provider_records, monthly_reconciliation)
    rth_count = sum(1 for row in classified_rows if row.get("session_classification") == RTH)
    extended_count = sum(1 for row in classified_rows if row.get("session_classification") == EXTENDED_HOURS)
    out_count = sum(1 for row in classified_rows if row.get("session_classification") == OUT_OF_CALENDAR_RANGE)
    unknown_count = sum(1 for row in classified_rows if row.get("session_classification") == UNKNOWN)
    failed_chunks = len(failed_records)
    january_summary = _january_2025_summary(monthly_reconciliation)
    january_cross_check_passed = _january_cross_check_passed(january_summary) if january_summary else not generated
    acquisition_generation_complete = (
        generated and len(provider_records) == len(chunks) and failed_chunks == 0 and january_cross_check_passed
    )
    candidate_status = _candidate_status_for_generation(
        generated=generated,
        completed_chunks=len(provider_records),
        expected_chunks=len(chunks),
        failed_chunks=failed_chunks,
        january_cross_check_passed=january_cross_check_passed,
    )
    provider_raw_digest = semantic_digest({"completed": provider_records, "failed": failed_records}) if generated or failed_records else None
    normalized_digest = normalized_source_rows_digest_v1(normalized_rows) if generated else None
    monthly_digest = monthly_reconciliation_digest_v1(monthly_reconciliation) if generated else None
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_CANDIDATE_V1,
        "candidate_status": candidate_status,
        "created_offline": created_offline,
        "provider_requests_made": provider_requests_made,
        "provider_response_injected": provider_response_injected,
        "acquisition_generation_complete": acquisition_generation_complete,
        "acquisition_generation_freeze": False,
        "operator_review_required": True,
        "operator_freeze_required": True,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "identity_segment_frozen_digest": EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_audit_frozen_digest": EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_contract_digest": EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "identity_segment": deepcopy(FIXED_IDENTITY_SEGMENT),
        "acquisition_contract": deepcopy(FIXED_ACQUISITION_CONTRACT),
        "authority_bindings": _authority_bindings(),
        "authority_boundary": _authority_boundary(),
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        "provider_name": PROVIDER_NAME_MASSIVE,
        "provider_endpoint": PROVIDER_ENDPOINT_MASSIVE_CUSTOM_BARS,
        "provider_endpoint_stability": PROVIDER_ENDPOINT_STABILITY_MASSIVE_AGGS_V2,
        "provider_query_identifier": FIXED_IDENTITY_SEGMENT["ticker"],
        "provider_request_mode": provider_request_mode,
        "provider_request_timestamp_utc": provider_request_timestamp_utc,
        "provider_chunk_count": len(provider_records),
        "provider_failed_chunk_count": failed_chunks,
        "provider_raw_response_digest": provider_raw_digest,
        "provider_chunk_manifest_digest": chunk_manifest_digest_v1(chunks),
        "chunking_strategy": CHUNKING_STRATEGY_MONTHLY,
        "chunk_count_expected": len(chunks),
        "chunk_count_completed": len(provider_records),
        "failed_chunk_count": failed_chunks,
        "failed_chunks": failed_records,
        "chunk_manifest_digest": chunk_manifest_digest_v1(chunks),
        "chunk_manifest": chunks,
        "provider_chunk_records": provider_records,
        "normalized_source_row_count": len(normalized_rows),
        "rth_row_count": rth_count,
        "extended_hours_row_count": extended_count,
        "out_of_calendar_range_row_count": out_count,
        "unknown_session_row_count": unknown_count,
        "normalized_source_rows_digest": normalized_digest,
        "monthly_reconciliation_digest": monthly_digest,
        "monthly_reconciliation": monthly_reconciliation,
        "accepted_monthly_source_cross_check": deepcopy(ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK),
        "normalized_source_rows": normalized_rows,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_ACQUISITION_GENERATION_CANDIDATE),
    }
    candidate["acquisition_generation_receipt_digest"] = semantic_digest(_receipt_digest_payload(candidate)) if generated else None
    candidate["acquisition_generation_candidate_semantic_digest"] = acquisition_generation_candidate_semantic_digest(candidate)
    validate_acquisition_generation_candidate_v1(candidate)
    return candidate


def _failed_chunk_record(chunk: dict[str, Any], exc: Exception) -> dict[str, Any]:
    return {
        "chunk_id": chunk["chunk_id"],
        "month": chunk["month"],
        "from": chunk["effective_start_date"],
        "to": chunk["effective_end_date"],
        "provider_response_status": type(exc).__name__,
        "raw_row_count": None,
        "normalized_row_count": 0,
        "rth_row_count": None,
        "extended_hours_row_count": None,
        "out_of_calendar_range_row_count": None,
        "unknown_session_row_count": None,
        "raw_response_digest": None,
        "provider_raw_response_digest": None,
        "normalized_rows_digest": None,
        "monthly_reconciliation_digest": None,
        "request_semantic_digest": chunk["request_semantic_digest"],
        "warnings": [],
        "errors": ["PROVIDER_CHUNK_FAILED"],
    }


def build_acquisition_generation_live_candidate_v1(
    *,
    ticker: str = "AAPL",
    api_key: str | None = None,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    provider_request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Run the gated 48-month provider-backed acquisition candidate generation."""
    ticker_text = ticker.strip().upper()
    timestamp = provider_request_timestamp_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if transport is None and os.environ.get(MARKETFLOW_ENABLE_LIVE_ACQUISITION_GENERATION) != "1":
        raise AcquisitionGenerationError(LIVE_ACQUISITION_GENERATION_BLOCKED_GATE_NOT_ENABLED)
    key = api_key or _api_key_from_environment()
    if not key:
        raise AcquisitionGenerationError(LIVE_ACQUISITION_GENERATION_BLOCKED_MISSING_API_KEY)

    provider_responses: list[dict[str, Any]] = []
    failed_records: list[dict[str, Any]] = []
    chunks = build_acquisition_month_chunks_v1(ticker=ticker_text)
    for chunk in chunks:
        try:
            raw = acquisition_adapter.fetch_massive_custom_bars_live_v1(
                ticker=ticker_text,
                start_date=chunk["effective_start_date"],
                end_date=chunk["effective_end_date"],
                api_key=key,
                transport=transport,
                request_timestamp_utc=timestamp,
            )
        except Exception as exc:
            failed_records.append(_failed_chunk_record(chunk, exc))
            continue
        raw_metadata = {field: value for field, value in raw.items() if field != "provider_response_body"}
        provider_responses.append(
            {
                "month": chunk["month"],
                "response": raw["provider_response_body"],
                "raw_metadata": raw_metadata,
            }
        )

    return build_acquisition_generation_candidate_v1(
        provider_responses=provider_responses,
        failed_chunk_records=failed_records,
        provider_request_timestamp_utc=timestamp,
        provider_request_mode=PROVIDER_REQUEST_MODE_LIVE if transport is None else PROVIDER_REQUEST_MODE_FAKE_TRANSPORT,
        provider_requests_made=transport is None,
        provider_response_injected=transport is not None,
        created_offline=transport is not None,
    )


def _validate_january_2025_cross_check(candidate: dict[str, Any]) -> None:
    months = candidate.get("monthly_reconciliation")
    if not months:
        return
    january = next((item for item in months if item.get("month") == "2025-01"), None)
    if january is None:
        return
    checks = {
        "2025-01.normalized_source_rows": (january.get("normalized_source_rows"), 1277),
        "2025-01.extended_hours_rows": (january.get("extended_hours_rows"), 757),
        "2025-01.expected_rth_rows": (january.get("expected_rth_rows"), 520),
        "2025-01.validated_rth_rows": (january.get("validated_rth_rows"), 520),
        "2025-01.full_ordinary_sessions": (january.get("full_ordinary_sessions"), 20),
        "2025-01.incomplete_ordinary_sessions": (january.get("incomplete_ordinary_sessions"), 0),
        "2025-01.swing_rth_half_session_195m_bars": (january.get("swing_rth_half_session_195m_bars"), 40),
        "2025-01.position_swing_rth_full_session_1d_bars": (january.get("position_swing_rth_full_session_1d_bars"), 20),
        "2025-01.rth_reconciliation_status": (january.get("rth_reconciliation_status"), RTH_SOURCE_ROWS_RECONCILED),
    }
    mismatches = [field for field, (actual, expected) in checks.items() if actual != expected]
    if mismatches and candidate.get("candidate_status") not in {
        ACQUISITION_GENERATION_2025_01_CROSS_CHECK_MISMATCH,
        ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE,
    }:
        raise AcquisitionGenerationError(f"{mismatches[0]} mismatch")


def validate_acquisition_generation_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate an acquisition generation candidate artifact."""
    if not isinstance(candidate, dict):
        raise AcquisitionGenerationError("acquisition generation candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_ACQUISITION_GENERATION_CANDIDATE_V1, "schema_version")
    if candidate.get("candidate_status") not in {
        ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW,
        ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION,
        ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE,
        ACQUISITION_GENERATION_2025_01_CROSS_CHECK_MISMATCH,
    }:
        raise AcquisitionGenerationError("candidate_status mismatch")
    if candidate.get("freeze_status") == ACQUISITION_GENERATION_FROZEN:
        raise AcquisitionGenerationError("freeze_status must not be ACQUISITION_GENERATION_FROZEN")
    if type(candidate.get("created_offline")) is not bool:
        raise AcquisitionGenerationError("created_offline must be boolean")
    if type(candidate.get("provider_requests_made")) is not bool:
        raise AcquisitionGenerationError("provider_requests_made must be boolean")
    if type(candidate.get("provider_response_injected")) is not bool:
        raise AcquisitionGenerationError("provider_response_injected must be boolean")
    provider_mode = candidate.get("provider_request_mode")
    if provider_mode == PROVIDER_REQUEST_MODE_LIVE:
        _expect_true(candidate.get("provider_requests_made"), "provider_requests_made")
        _expect_false(candidate.get("provider_response_injected"), "provider_response_injected")
    elif provider_mode == PROVIDER_REQUEST_MODE_FAKE_TRANSPORT:
        _expect_false(candidate.get("provider_requests_made"), "provider_requests_made")
        _expect_true(candidate.get("provider_response_injected"), "provider_response_injected")
    elif provider_mode is None:
        _expect_false(candidate.get("provider_requests_made"), "provider_requests_made")
        _expect_false(candidate.get("provider_response_injected"), "provider_response_injected")
    else:
        raise AcquisitionGenerationError("provider_request_mode mismatch")
    _expect_false(candidate.get("acquisition_generation_freeze"), "acquisition_generation_freeze")
    for field in ("canonical_eligibility", "registry_eligibility", "strategy_runtime_migration", "automatic_stitching"):
        _expect_false(candidate.get(field), field)
    _expect(candidate.get("predictive_usefulness"), PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field in ("identity_segment_frozen", "calendar_operator_frozen", "split_event_audit_frozen", "dividend_event_audit_frozen"):
        _expect_true(candidate.get(field), field)
    _expect(candidate.get("identity_segment_frozen_digest"), EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, "identity_segment_frozen_digest")
    _expect(candidate.get("exchange_calendar_frozen_digest"), EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, "exchange_calendar_frozen_digest")
    _expect(candidate.get("schedule_semantic_digest"), EXPECTED_SCHEDULE_SEMANTIC_DIGEST, "schedule_semantic_digest")
    _expect(candidate.get("split_event_audit_frozen_digest"), EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, "split_event_audit_frozen_digest")
    _expect(candidate.get("dividend_event_audit_frozen_digest"), EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST, "dividend_event_audit_frozen_digest")
    _expect(candidate.get("acquisition_contract_digest"), EXPECTED_ACQUISITION_CONTRACT_DIGEST, "acquisition_contract_digest")
    _expect(candidate.get("identity_segment"), FIXED_IDENTITY_SEGMENT, "identity_segment")
    _expect(candidate.get("acquisition_contract"), FIXED_ACQUISITION_CONTRACT, "acquisition_contract")
    _expect(candidate.get("authority_bindings"), _authority_bindings(), "authority_bindings")
    _expect(candidate.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    _expect_true(candidate.get("in_range_dividends_found"), "in_range_dividends_found")
    _expect(candidate.get("in_range_dividend_count"), 16, "in_range_dividend_count")
    _expect(candidate.get("in_range_dividend_implication"), EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, "in_range_dividend_implication")
    _expect(candidate.get("chunking_strategy"), CHUNKING_STRATEGY_MONTHLY, "chunking_strategy")
    _expect(candidate.get("chunk_count_expected"), 48, "chunk_count_expected")
    if candidate.get("chunk_count_completed") != candidate.get("provider_chunk_count"):
        raise AcquisitionGenerationError("chunk count inconsistent")
    if candidate.get("failed_chunk_count") != candidate.get("provider_failed_chunk_count"):
        raise AcquisitionGenerationError("failed chunk count inconsistent")
    if candidate.get("acquisition_generation_complete") is True:
        _expect(candidate.get("candidate_status"), ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW, "candidate_status")
        _expect(candidate.get("chunk_count_completed"), 48, "chunk_count_completed")
        _expect(candidate.get("failed_chunk_count"), 0, "failed_chunk_count")
        for field in ("provider_raw_response_digest", "normalized_source_rows_digest", "monthly_reconciliation_digest", "acquisition_generation_receipt_digest"):
            value = candidate.get(field)
            if not isinstance(value, str) or len(value) != 64:
                raise AcquisitionGenerationError(f"{field} missing")
    if candidate.get("failed_chunk_count", 0) > 0 and candidate.get("acquisition_generation_complete") is True:
        raise AcquisitionGenerationError("failed chunks cannot be complete")
    if candidate.get("candidate_status") == ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW:
        _expect_true(candidate.get("acquisition_generation_complete"), "acquisition_generation_complete")
    if candidate.get("candidate_status") == ACQUISITION_GENERATION_PROVIDER_CHUNKS_INCOMPLETE:
        _expect_false(candidate.get("acquisition_generation_complete"), "acquisition_generation_complete")
    if candidate.get("candidate_status") == ACQUISITION_GENERATION_2025_01_CROSS_CHECK_MISMATCH:
        _expect_false(candidate.get("acquisition_generation_complete"), "acquisition_generation_complete")
    _validate_january_2025_cross_check(candidate)
    _expect(candidate.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_ACQUISITION_GENERATION_CANDIDATE, "remaining_roadmap")
    digest = candidate.get("acquisition_generation_candidate_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AcquisitionGenerationError("acquisition_generation_candidate_semantic_digest missing")
    _expect(digest, acquisition_generation_candidate_semantic_digest(candidate), "acquisition_generation_candidate_semantic_digest")
    return {
        "status": "ACQUISITION_GENERATION_CANDIDATE_VALID",
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE,
        "candidate_status": candidate["candidate_status"],
        "acquisition_generation_candidate_semantic_digest": digest,
        "provider_raw_response_digest": candidate.get("provider_raw_response_digest"),
        "normalized_source_rows_digest": candidate.get("normalized_source_rows_digest"),
        "monthly_reconciliation_digest": candidate.get("monthly_reconciliation_digest"),
        "acquisition_generation_receipt_digest": candidate.get("acquisition_generation_receipt_digest"),
        "chunking_strategy": CHUNKING_STRATEGY_MONTHLY,
        "chunk_count_expected": 48,
        "chunk_count_completed": candidate.get("chunk_count_completed"),
        "failed_chunk_count": candidate.get("failed_chunk_count"),
        "normalized_source_row_count": candidate.get("normalized_source_row_count"),
        "rth_row_count": candidate.get("rth_row_count"),
        "extended_hours_row_count": candidate.get("extended_hours_row_count"),
        "provider_requests_made": candidate.get("provider_requests_made"),
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
    }


def _expect_hex_digest(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise AcquisitionGenerationError(f"{field_name} missing")


def validate_acquisition_generation_monthly_live_smoke_v1(smoke: dict[str, Any]) -> dict[str, Any]:
    """Validate an acquisition monthly smoke candidate and reject premature authority claims."""
    if not isinstance(smoke, dict):
        raise AcquisitionGenerationError("acquisition monthly smoke must be a JSON object")
    _expect(smoke.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE, "artifact_kind")
    _expect(smoke.get("schema_version"), SCHEMA_VERSION_ACQUISITION_MONTHLY_LIVE_SMOKE_V1, "schema_version")
    if smoke.get("candidate_status") not in {
        ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW,
        LIVE_ACQUISITION_SMOKE_BLOCKED_MISSING_API_KEY,
        LIVE_ACQUISITION_SMOKE_BLOCKED_GATE_NOT_ENABLED,
        LIVE_ACQUISITION_SMOKE_PROVIDER_ERROR,
    }:
        raise AcquisitionGenerationError("candidate_status mismatch")
    _expect(smoke.get("ticker"), ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK["ticker"], "ticker")
    _expect(smoke.get("month"), ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK["month"], "month")
    _expect_false(smoke.get("acquisition_generation_freeze"), "acquisition_generation_freeze")
    for field in ("canonical_eligibility", "registry_eligibility", "strategy_runtime_migration", "automatic_stitching"):
        _expect_false(smoke.get(field), field)
    _expect(smoke.get("predictive_usefulness"), PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(smoke.get("profitability"), PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field in ("identity_segment_frozen", "calendar_operator_frozen", "split_event_audit_frozen", "dividend_event_audit_frozen"):
        _expect_true(smoke.get(field), field)
    _expect(smoke.get("identity_segment_frozen_digest"), EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, "identity_segment_frozen_digest")
    _expect(smoke.get("exchange_calendar_frozen_digest"), EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, "exchange_calendar_frozen_digest")
    _expect(smoke.get("schedule_semantic_digest"), EXPECTED_SCHEDULE_SEMANTIC_DIGEST, "schedule_semantic_digest")
    _expect(smoke.get("split_event_audit_frozen_digest"), EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, "split_event_audit_frozen_digest")
    _expect(smoke.get("dividend_event_audit_frozen_digest"), EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST, "dividend_event_audit_frozen_digest")
    _expect(smoke.get("acquisition_contract_digest"), EXPECTED_ACQUISITION_CONTRACT_DIGEST, "acquisition_contract_digest")
    _expect(smoke.get("identity_segment"), FIXED_IDENTITY_SEGMENT, "identity_segment")
    _expect(smoke.get("acquisition_contract"), FIXED_ACQUISITION_CONTRACT, "acquisition_contract")
    _expect(smoke.get("authority_bindings"), _authority_bindings(), "authority_bindings")
    _expect(smoke.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    _expect_true(smoke.get("in_range_dividends_found"), "in_range_dividends_found")
    _expect(smoke.get("in_range_dividend_count"), 16, "in_range_dividend_count")
    _expect(smoke.get("in_range_dividend_implication"), EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, "in_range_dividend_implication")
    _expect_false(smoke.get("api_key_stored"), "api_key_stored")
    _expect_false(smoke.get("raw_provider_payload_stored"), "raw_provider_payload_stored")
    _expect_false(smoke.get("generated_bars_stored"), "generated_bars_stored")
    if smoke.get("candidate_status") == ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW:
        _expect_true(smoke.get("accepted_2025_01_cross_check_passed"), "accepted_2025_01_cross_check_passed")
        _expect(smoke.get("normalized_source_row_count"), 1277, "normalized_source_row_count")
        _expect(smoke.get("extended_hours_row_count"), 757, "extended_hours_row_count")
        _expect(smoke.get("expected_rth_rows"), 520, "expected_rth_rows")
        _expect(smoke.get("validated_rth_rows"), 520, "validated_rth_rows")
        _expect(smoke.get("rth_row_count"), 520, "rth_row_count")
        _expect(smoke.get("rth_reconciliation_status"), RTH_SOURCE_ROWS_RECONCILED, "rth_reconciliation_status")
        _expect(smoke.get("full_ordinary_sessions"), 20, "full_ordinary_sessions")
        _expect(smoke.get("incomplete_ordinary_sessions"), 0, "incomplete_ordinary_sessions")
        _expect(smoke.get("swing_rth_half_session_195m_bars"), 40, "swing_rth_half_session_195m_bars")
        _expect(smoke.get("position_swing_rth_full_session_1d_bars"), 20, "position_swing_rth_full_session_1d_bars")
        for field in (
            "provider_raw_response_digest",
            "normalized_source_rows_digest",
            "monthly_reconciliation_digest",
            "acquisition_smoke_receipt_digest",
            "acquisition_monthly_smoke_candidate_digest",
        ):
            _expect_hex_digest(smoke.get(field), field)
        _expect(
            smoke["normalized_source_rows_digest"],
            normalized_source_rows_digest_v1(smoke.get("normalized_source_rows") or []),
            "normalized_source_rows_digest",
        )
        _expect(
            smoke["monthly_reconciliation_digest"],
            monthly_reconciliation_digest_v1(smoke.get("monthly_reconciliation") or []),
            "monthly_reconciliation_digest",
        )
    if smoke.get("accepted_2025_01_cross_check_passed") is False and smoke.get("provider_raw_response_digest"):
        raise AcquisitionGenerationError("accepted_2025_01_cross_check_passed must be true for provider-bound smoke")
    _expect(
        smoke.get("acquisition_smoke_receipt_digest"),
        semantic_digest(_smoke_receipt_payload(smoke)),
        "acquisition_smoke_receipt_digest",
    )
    _expect(
        smoke.get("acquisition_monthly_smoke_candidate_digest"),
        acquisition_monthly_smoke_candidate_digest_v1(smoke),
        "acquisition_monthly_smoke_candidate_digest",
    )
    return {
        "status": "ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE_VALID",
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE,
        "candidate_status": smoke["candidate_status"],
        "provider_request_mode": smoke.get("provider_request_mode"),
        "provider_response_status": smoke.get("provider_response_status"),
        "provider_raw_row_count": smoke.get("provider_raw_row_count"),
        "normalized_source_row_count": smoke.get("normalized_source_row_count"),
        "rth_row_count": smoke.get("rth_row_count"),
        "extended_hours_row_count": smoke.get("extended_hours_row_count"),
        "expected_rth_rows": smoke.get("expected_rth_rows"),
        "rth_reconciliation_status": smoke.get("rth_reconciliation_status"),
        "full_ordinary_sessions": smoke.get("full_ordinary_sessions"),
        "incomplete_ordinary_sessions": smoke.get("incomplete_ordinary_sessions"),
        "provider_raw_response_digest": smoke.get("provider_raw_response_digest"),
        "normalized_source_rows_digest": smoke.get("normalized_source_rows_digest"),
        "monthly_reconciliation_digest": smoke.get("monthly_reconciliation_digest"),
        "acquisition_smoke_receipt_digest": smoke.get("acquisition_smoke_receipt_digest"),
        "acquisition_monthly_smoke_candidate_digest": smoke.get("acquisition_monthly_smoke_candidate_digest"),
        "accepted_2025_01_cross_check_passed": smoke.get("accepted_2025_01_cross_check_passed"),
        "api_key_stored": False,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
    }


def _monthly_reconciliation_status_summary(candidate: dict[str, Any]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for item in candidate.get("monthly_reconciliation") or []:
        status = str(item.get("rth_reconciliation_status"))
        summary[status] = summary.get(status, 0) + 1
    return dict(sorted(summary.items()))


def _january_2025_cross_check_result(candidate: dict[str, Any]) -> str:
    summary = _january_2025_summary(candidate.get("monthly_reconciliation") or [])
    if summary is None:
        return "NOT_PRESENT"
    return "PASSED" if _january_cross_check_passed(summary) else "FAILED"


def build_acquisition_generation_live_status_markdown_v1(candidate: dict[str, Any]) -> str:
    """Render a sanitized full acquisition generation status document."""
    validate_acquisition_generation_candidate_v1(candidate)
    endpoint = PROVIDER_ENDPOINT_MASSIVE_CUSTOM_BARS
    boundary = candidate["authority_boundary"]
    bindings = candidate["authority_bindings"]
    status_summary = _monthly_reconciliation_status_summary(candidate)
    cross_check = _january_2025_cross_check_result(candidate)
    lines = [
        "# MarketFlow Acquisition Live Generation 2022-2025 Status",
        "",
        "## Scope",
        f"- Artifact kind: `{candidate['artifact_kind']}`",
        f"- Candidate status: `{candidate['candidate_status']}`",
        f"- Endpoint used: `{endpoint}`",
        f"- Request mode: `{candidate.get('provider_request_mode')}`",
        f"- Ticker: `{candidate['provider_query_identifier']}`",
        "- Range: `2022-01-01` through `2025-12-31`",
        "- Interval: `15-minute`",
        "- Adjusted: `true`",
        "- Sort: `asc`",
        "- Chunking: `MONTHLY`",
        "- Source timestamps: `aggregate-window starts`",
        "- Source timezone: `America/New_York`",
        "- Canonical storage timezone: `UTC`",
        "",
        "## Chunk Results",
        f"- Expected chunk count: `{candidate['chunk_count_expected']}`",
        f"- Completed chunk count: `{candidate['chunk_count_completed']}`",
        f"- Failed chunk count: `{candidate['failed_chunk_count']}`",
        f"- Total provider raw rows: `{sum(record.get('raw_row_count') or 0 for record in candidate.get('provider_chunk_records') or [])}`",
        f"- Total normalized source rows: `{candidate.get('normalized_source_row_count')}`",
        f"- Total RTH rows: `{candidate.get('rth_row_count')}`",
        f"- Total extended-hours rows: `{candidate.get('extended_hours_row_count')}`",
        f"- Total out-of-calendar/unknown rows: `{(candidate.get('out_of_calendar_range_row_count') or 0) + (candidate.get('unknown_session_row_count') or 0)}`",
        f"- Monthly reconciliation status summary: `{json.dumps(status_summary, sort_keys=True, separators=(',', ':'))}`",
        f"- 2025-01 cross-check result: `{cross_check}`",
        "",
        "## Chunk Manifest",
        "| chunk_id | month | from | to | status | raw_rows | normalized_rows | rth_rows | extended_hours_rows | out_or_unknown_rows | raw_response_digest | normalized_rows_digest | monthly_reconciliation_digest | warnings | errors |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for record in candidate.get("provider_chunk_records") or []:
        out_or_unknown = (record.get("out_of_calendar_range_row_count") or 0) + (record.get("unknown_session_row_count") or 0)
        warnings = ",".join(record.get("warnings") or [])
        errors = ",".join(record.get("errors") or [])
        lines.append(
            "| "
            f"{record.get('chunk_id')} | "
            f"{record.get('month')} | "
            f"{record.get('from')} | "
            f"{record.get('to')} | "
            f"{record.get('provider_response_status')} | "
            f"{record.get('raw_row_count')} | "
            f"{record.get('normalized_row_count')} | "
            f"{record.get('rth_row_count')} | "
            f"{record.get('extended_hours_row_count')} | "
            f"{out_or_unknown} | "
            f"{record.get('raw_response_digest')} | "
            f"{record.get('normalized_rows_digest')} | "
            f"{record.get('monthly_reconciliation_digest')} | "
            f"{warnings} | "
            f"{errors} |"
        )
    lines.extend(
        [
            "",
        "## Digests",
        f"- Chunk manifest digest: `{candidate.get('chunk_manifest_digest')}`",
        f"- Provider raw response digest: `{candidate.get('provider_raw_response_digest')}`",
        f"- Normalized source rows digest: `{candidate.get('normalized_source_rows_digest')}`",
        f"- Monthly reconciliation digest: `{candidate.get('monthly_reconciliation_digest')}`",
        f"- Acquisition generation receipt digest: `{candidate.get('acquisition_generation_receipt_digest')}`",
        f"- Acquisition generation candidate digest: `{candidate.get('acquisition_generation_candidate_semantic_digest')}`",
        "",
        "## Authority Bindings",
        f"- Identity frozen digest: `{bindings['identity_segment_frozen_digest']}`",
        f"- Calendar frozen digest: `{bindings['exchange_calendar_frozen_digest']}`",
        f"- Schedule digest: `{bindings['schedule_semantic_digest']}`",
        f"- Split-event audit frozen digest: `{bindings['split_event_audit_frozen_digest']}`",
        f"- Dividend-event audit frozen digest: `{bindings['dividend_event_audit_frozen_digest']}`",
        f"- Acquisition contract digest: `{bindings['acquisition_contract_digest']}`",
        "",
        "## Dividend Implication",
        f"- In-range dividends found: `{candidate['in_range_dividends_found']}`",
        f"- In-range dividend count: `{candidate['in_range_dividend_count']}`",
        f"- Implication: `{candidate['in_range_dividend_implication']}`",
        "",
        "## Authority Boundary",
        f"- identity_segment_frozen: `{boundary['identity_segment_frozen']}`",
        f"- calendar_operator_frozen: `{boundary['calendar_operator_frozen']}`",
        f"- split_event_audit_frozen: `{boundary['split_event_audit_frozen']}`",
        f"- dividend_event_audit_frozen: `{boundary['dividend_event_audit_frozen']}`",
        f"- acquisition_generation_freeze: `{boundary['acquisition_generation_freeze']}`",
        f"- canonical_eligibility: `{boundary['canonical_eligibility']}`",
        f"- registry_eligibility: `{boundary['registry_eligibility']}`",
        f"- strategy_runtime_migration: `{boundary['strategy_runtime_migration']}`",
        f"- automatic_stitching: `{boundary['automatic_stitching']}`",
        f"- predictive_usefulness: `{boundary['predictive_usefulness']}`",
        f"- profitability: `{boundary['profitability']}`",
        "",
        "## Safety Confirmations",
        "- API key stored: `False`",
        "- Raw provider payload stored in this document: `False`",
        "- Full generated bars stored in this document: `False`",
        "- No acquisition-generation freeze was created.",
        "- No canonical, registry, runtime, predictive, or profitability approval occurred.",
        "",
        "## Next Task Recommendation",
        "- Build an operator review package for the acquisition generation candidate before any freeze ceremony.",
        "",
        ]
    )
    return "\n".join(lines)


def write_acquisition_generation_live_status_v1(path: str | Path, *, candidate: dict[str, Any]) -> dict[str, Any]:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = build_acquisition_generation_live_status_markdown_v1(candidate)
    output_path.write_text(text, encoding="utf-8")
    return {
        "path": str(output_path),
        "filename": output_path.name,
        "status_document_digest": sha256_bytes(text.encode("utf-8")),
    }


def _int_or_none(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if type(value) is int:
        return value
    if type(value) is str and value.strip().lstrip("-").isdigit():
        return int(value.strip())
    return None


def _calendar_expectation_for_month(month: str) -> dict[str, int]:
    schedule = calendar_service.build_exchange_calendar_schedule_rows_v1()
    full_sessions = [row for row in schedule if row["session_date"].startswith(month) and row.get("is_full_session") is True]
    expected_rth_rows = len(full_sessions) * 26
    return {
        "expected_rth_rows": expected_rth_rows,
        "full_ordinary_sessions": len(full_sessions),
        "swing_rth_half_session_195m_bars": len(full_sessions) * 2,
        "position_swing_rth_full_session_1d_bars": len(full_sessions),
    }


def _is_reconciled_status(status: Any) -> bool:
    return status == RTH_SOURCE_ROWS_RECONCILED


def _row_status(row: Mapping[str, Any]) -> str:
    status = row.get("reconciliation_status") or row.get("rth_reconciliation_status")
    if isinstance(status, str):
        return status
    errors = row.get("errors")
    if isinstance(errors, list) and RTH_SOURCE_ROWS_NOT_RECONCILED in errors:
        return RTH_SOURCE_ROWS_NOT_RECONCILED
    if isinstance(errors, str) and RTH_SOURCE_ROWS_NOT_RECONCILED in errors:
        return RTH_SOURCE_ROWS_NOT_RECONCILED
    return RTH_SOURCE_ROWS_RECONCILED


def _row_number(row: Mapping[str, Any], *names: str) -> int | None:
    for name in names:
        value = _int_or_none(row.get(name))
        if value is not None:
            return value
    return None


def _triage_digest_payload(triage: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(triage)
    payload.pop("triage_semantic_digest", None)
    return payload


def acquisition_monthly_reconciliation_triage_semantic_digest_v1(triage: dict[str, Any]) -> str:
    return semantic_digest(_triage_digest_payload(triage))


def classify_monthly_reconciliation_issue_v1(monthly_row: dict[str, Any]) -> dict[str, Any]:
    """Classify one monthly reconciliation row without inferring a root cause."""
    if not isinstance(monthly_row, dict):
        raise AcquisitionGenerationError("monthly reconciliation row must be a JSON object")
    month = monthly_row.get("month")
    if type(month) is not str or len(month) != 7:
        raise AcquisitionGenerationError("month must be YYYY-MM")
    status = _row_status(monthly_row)
    normalized_rows = _row_number(monthly_row, "normalized_source_rows", "normalized_row_count")
    rth_rows = _row_number(monthly_row, "rth_rows", "rth_row_count")
    extended_rows = _row_number(monthly_row, "extended_hours_rows", "extended_hours_row_count")
    expected_rth = _row_number(monthly_row, "expected_rth_rows")
    validated_rth = _row_number(monthly_row, "validated_rth_rows", "rth_rows", "rth_row_count")
    full_sessions = _row_number(monthly_row, "full_ordinary_sessions")
    incomplete_sessions = _row_number(monthly_row, "incomplete_ordinary_sessions")
    swing_bars = _row_number(monthly_row, "swing_rth_half_session_195m_bars")
    position_bars = _row_number(monthly_row, "position_swing_rth_full_session_1d_bars")
    delta = None if expected_rth is None or validated_rth is None else validated_rth - expected_rth
    detail_level = monthly_row.get("detail_level")

    if _is_reconciled_status(status):
        issue_category = ISSUE_CATEGORY_RECONCILED
        issue_severity = SEVERITY_INFO
        triage_reason = "Monthly RTH row count reconciles against the available calendar expectation."
        requires_operator_review = False
        requires_provider_recheck = False
        requires_calendar_logic_review = False
        requires_algorithm_review = False
    elif month == "2025-01":
        issue_category = ISSUE_CATEGORY_RTH_ROW_COUNT_MISMATCH
        issue_severity = SEVERITY_BLOCKER
        triage_reason = "Accepted 2025-01 cross-check is not reconciled; acquisition review is blocked."
        requires_operator_review = True
        requires_provider_recheck = True
        requires_calendar_logic_review = True
        requires_algorithm_review = True
    elif detail_level == "STATUS_DOC_CHUNK_MANIFEST_ONLY" or incomplete_sessions is None:
        issue_category = ISSUE_CATEGORY_INSUFFICIENT_DETAIL
        issue_severity = SEVERITY_HIGH
        triage_reason = "The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification."
        requires_operator_review = True
        requires_provider_recheck = True
        requires_calendar_logic_review = True
        requires_algorithm_review = True
    elif delta is not None and delta < 0:
        issue_category = ISSUE_CATEGORY_MISSING_PROVIDER_ROWS
        issue_severity = SEVERITY_HIGH
        triage_reason = "Validated RTH rows are below expected RTH rows; per-session evidence is required before assigning a root cause."
        requires_operator_review = True
        requires_provider_recheck = True
        requires_calendar_logic_review = True
        requires_algorithm_review = True
    elif delta is not None and delta > 0:
        issue_category = ISSUE_CATEGORY_EXTRA_PROVIDER_ROWS
        issue_severity = SEVERITY_HIGH
        triage_reason = "Validated RTH rows are above expected RTH rows; calendar and classification logic need review."
        requires_operator_review = True
        requires_provider_recheck = True
        requires_calendar_logic_review = True
        requires_algorithm_review = True
    else:
        issue_category = ISSUE_CATEGORY_RTH_ROW_COUNT_MISMATCH if delta == 0 else ISSUE_CATEGORY_UNKNOWN
        issue_severity = SEVERITY_HIGH
        triage_reason = "Monthly RTH reconciliation did not pass and available detail is insufficient for a narrower classification."
        requires_operator_review = True
        requires_provider_recheck = True
        requires_calendar_logic_review = True
        requires_algorithm_review = True

    return {
        "month": month,
        "reconciliation_status": status,
        "normalized_source_rows": normalized_rows,
        "rth_rows": rth_rows,
        "extended_hours_rows": extended_rows,
        "expected_rth_rows": expected_rth,
        "validated_rth_rows": validated_rth,
        "rth_row_delta": delta,
        "full_ordinary_sessions": full_sessions,
        "incomplete_ordinary_sessions": incomplete_sessions,
        "swing_rth_half_session_195m_bars": swing_bars,
        "position_swing_rth_full_session_1d_bars": position_bars,
        "issue_category": issue_category,
        "issue_severity": issue_severity,
        "triage_reason": triage_reason,
        "requires_operator_review": requires_operator_review,
        "requires_provider_recheck": requires_provider_recheck,
        "requires_calendar_logic_review": requires_calendar_logic_review,
        "requires_algorithm_review": requires_algorithm_review,
    }


def _count_by(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        key = str(row.get(field))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def _january_cross_check_status_from_triage_rows(rows: list[dict[str, Any]]) -> str:
    january = next((row for row in rows if row.get("month") == "2025-01"), None)
    if january is None:
        return "NOT_PRESENT"
    if january.get("issue_severity") == SEVERITY_BLOCKER:
        return "FAILED"
    if january.get("reconciliation_status") == RTH_SOURCE_ROWS_RECONCILED:
        return "PASSED"
    return "FAILED"


def build_acquisition_monthly_reconciliation_triage_v1(
    monthly_rows: list[dict[str, Any]],
    *,
    source_acquisition_candidate_digest: str = EXPECTED_FULL_LIVE_ACQUISITION_CANDIDATE_DIGEST,
    source_monthly_reconciliation_digest: str = EXPECTED_FULL_LIVE_MONTHLY_RECONCILIATION_DIGEST,
) -> dict[str, Any]:
    """Build a conservative monthly reconciliation triage artifact."""
    if not isinstance(monthly_rows, list):
        raise AcquisitionGenerationError("monthly_rows must be a list")
    triage_rows = [classify_monthly_reconciliation_issue_v1(row) for row in monthly_rows]
    triage_rows.sort(key=lambda row: row["month"])
    total_months = len(triage_rows)
    reconciled_months = sum(1 for row in triage_rows if row["reconciliation_status"] == RTH_SOURCE_ROWS_RECONCILED)
    not_reconciled_months = total_months - reconciled_months
    blocker_count = sum(1 for row in triage_rows if row["issue_severity"] == SEVERITY_BLOCKER)
    high_count = sum(1 for row in triage_rows if row["issue_severity"] == SEVERITY_HIGH)
    ready_for_acquisition_review = not_reconciled_months == 0 and blocker_count == 0
    triage = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE,
        "schema_version": SCHEMA_VERSION_ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_V1,
        "triage_status": (
            ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_READY
            if ready_for_acquisition_review
            else ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_BLOCKS_ACQUISITION_REVIEW
        ),
        "source_acquisition_candidate_digest": source_acquisition_candidate_digest,
        "source_monthly_reconciliation_digest": source_monthly_reconciliation_digest,
        "total_months": total_months,
        "reconciled_months": reconciled_months,
        "not_reconciled_months": not_reconciled_months,
        "blocker_count": blocker_count,
        "high_count": high_count,
        "issue_category_summary": _count_by(triage_rows, "issue_category"),
        "issue_severity_summary": _count_by(triage_rows, "issue_severity"),
        "non_reconciled_months": [row["month"] for row in triage_rows if row["reconciliation_status"] != RTH_SOURCE_ROWS_RECONCILED],
        "accepted_2025_01_cross_check_status": _january_cross_check_status_from_triage_rows(triage_rows),
        "ready_for_acquisition_review": ready_for_acquisition_review,
        "operator_review_required": not ready_for_acquisition_review,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "triage_rows": triage_rows,
        "authority_boundary": _authority_boundary(),
    }
    triage["triage_semantic_digest"] = acquisition_monthly_reconciliation_triage_semantic_digest_v1(triage)
    validate_acquisition_monthly_reconciliation_triage_v1(triage)
    return triage


def validate_acquisition_monthly_reconciliation_triage_v1(triage: dict[str, Any]) -> dict[str, Any]:
    """Validate monthly reconciliation triage and reject premature authority claims."""
    if not isinstance(triage, dict):
        raise AcquisitionGenerationError("triage must be a JSON object")
    _expect(triage.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE, "artifact_kind")
    _expect(triage.get("schema_version"), SCHEMA_VERSION_ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_V1, "schema_version")
    if triage.get("triage_status") not in {
        ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_READY,
        ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_BLOCKS_ACQUISITION_REVIEW,
    }:
        raise AcquisitionGenerationError("triage_status mismatch")
    _expect(
        triage.get("source_acquisition_candidate_digest"),
        EXPECTED_FULL_LIVE_ACQUISITION_CANDIDATE_DIGEST,
        "source_acquisition_candidate_digest",
    )
    _expect(
        triage.get("source_monthly_reconciliation_digest"),
        EXPECTED_FULL_LIVE_MONTHLY_RECONCILIATION_DIGEST,
        "source_monthly_reconciliation_digest",
    )
    for field in ("acquisition_generation_freeze", "canonical_eligibility", "registry_eligibility", "strategy_runtime_migration", "automatic_stitching"):
        _expect_false(triage.get(field), field)
    rows = triage.get("triage_rows")
    if not isinstance(rows, list):
        raise AcquisitionGenerationError("triage_rows must be a list")
    _expect(triage.get("total_months"), len(rows), "total_months")
    reconciled = sum(1 for row in rows if row.get("reconciliation_status") == RTH_SOURCE_ROWS_RECONCILED)
    _expect(triage.get("reconciled_months"), reconciled, "reconciled_months")
    _expect(triage.get("not_reconciled_months"), len(rows) - reconciled, "not_reconciled_months")
    _expect(triage.get("blocker_count"), sum(1 for row in rows if row.get("issue_severity") == SEVERITY_BLOCKER), "blocker_count")
    _expect(triage.get("high_count"), sum(1 for row in rows if row.get("issue_severity") == SEVERITY_HIGH), "high_count")
    if triage.get("not_reconciled_months", 0) > 0:
        _expect_false(triage.get("ready_for_acquisition_review"), "ready_for_acquisition_review")
    digest = triage.get("triage_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AcquisitionGenerationError("triage_semantic_digest missing")
    _expect(digest, acquisition_monthly_reconciliation_triage_semantic_digest_v1(triage), "triage_semantic_digest")
    return {
        "status": "ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_VALID",
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE,
        "triage_status": triage["triage_status"],
        "total_months": triage["total_months"],
        "reconciled_months": triage["reconciled_months"],
        "not_reconciled_months": triage["not_reconciled_months"],
        "ready_for_acquisition_review": triage["ready_for_acquisition_review"],
        "triage_semantic_digest": digest,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
    }


def _per_session_diagnostics_payload(diagnostics: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(diagnostics)
    payload.pop("per_session_diagnostics_semantic_digest", None)
    return payload


def acquisition_per_session_reconciliation_diagnostics_semantic_digest_v1(diagnostics: dict[str, Any]) -> str:
    return semantic_digest(_per_session_diagnostics_payload(diagnostics))


def _normalize_target_months(target_months: list[str] | tuple[str, ...] | None) -> list[str]:
    months = list(target_months) if target_months is not None else list(DEFAULT_PER_SESSION_DIAGNOSTIC_TARGET_MONTHS)
    for month in months:
        if type(month) is not str or len(month) != 7 or month[4] != "-":
            raise AcquisitionGenerationError("target_months must contain YYYY-MM strings")
    return sorted(months)


def _session_rows_for_months(
    target_months: list[str],
    *,
    schedule_rows: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    schedule = schedule_rows if schedule_rows is not None else calendar_service.build_exchange_calendar_schedule_rows_v1()
    target_set = set(target_months)
    return [row for row in schedule if row["session_date"][:7] in target_set]


def _is_holiday_adjacent(session_date: str, open_session_dates: set[str]) -> bool:
    current = date.fromisoformat(session_date)
    for offset in (-1, 1):
        adjacent = current + timedelta(days=offset)
        if adjacent.weekday() < 5 and adjacent.isoformat() not in open_session_dates:
            return True
    return False


def _timestamp_utc_or_none(row: Mapping[str, Any]) -> datetime | None:
    value = row.get("timestamp_utc")
    if not isinstance(value, str):
        return None
    try:
        return _parse_utc(value)
    except ValueError:
        return None


def _iso_utc(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def classify_session_reconciliation_issue_v1(session_row: dict[str, Any]) -> dict[str, Any]:
    """Classify one session diagnostic row without assigning unverifiable root cause."""
    if not isinstance(session_row, dict):
        raise AcquisitionGenerationError("session reconciliation row must be a JSON object")
    month = session_row.get("month")
    if type(month) is not str or len(month) != 7:
        raise AcquisitionGenerationError("month must be YYYY-MM")
    expected = _int_or_none(session_row.get("expected_15m_bars"))
    observed = _int_or_none(session_row.get("observed_15m_bars"))
    if observed is None:
        raise AcquisitionGenerationError("observed_15m_bars is required")
    if expected is None:
        delta = None
        issue_category = ISSUE_CATEGORY_CALENDAR_SESSION_DURATION_REVIEW_REQUIRED
        issue_severity = SEVERITY_HIGH
        notes = "Calendar session duration is not divisible by the 15-minute source interval."
        requires_provider_recheck = False
        requires_calendar_logic_review = True
        requires_timezone_review = True
        requires_algorithm_review = True
    else:
        delta = observed - expected
        if delta == 0:
            issue_category = ISSUE_CATEGORY_RECONCILED
            issue_severity = SEVERITY_INFO
            notes = "Session RTH row count reconciles against the calendar open-close window."
            requires_provider_recheck = False
            requires_calendar_logic_review = False
            requires_timezone_review = False
            requires_algorithm_review = False
        elif delta < 0:
            issue_category = ISSUE_CATEGORY_MISSING_RTH_BARS
            issue_severity = SEVERITY_BLOCKER if month == "2025-01" else SEVERITY_HIGH
            notes = "Observed RTH bars are below the calendar-derived session expectation."
            requires_provider_recheck = True
            requires_calendar_logic_review = False
            requires_timezone_review = True
            requires_algorithm_review = True
        else:
            issue_category = ISSUE_CATEGORY_EXTRA_RTH_BARS
            issue_severity = SEVERITY_BLOCKER if month == "2025-01" else SEVERITY_HIGH
            notes = "Observed RTH bars exceed the calendar-derived session expectation."
            requires_provider_recheck = True
            requires_calendar_logic_review = True
            requires_timezone_review = True
            requires_algorithm_review = True

    result = deepcopy(session_row)
    result.update(
        {
            "rth_row_delta": delta,
            "missing_count": abs(delta) if delta is not None and delta < 0 else 0,
            "extra_count": delta if delta is not None and delta > 0 else 0,
            "missing_rth_bar_count": abs(delta) if delta is not None and delta < 0 else 0,
            "extra_rth_bar_count": delta if delta is not None and delta > 0 else 0,
            "issue_category": issue_category,
            "issue_severity": issue_severity,
            "requires_operator_review": issue_severity != SEVERITY_INFO,
            "requires_provider_recheck": requires_provider_recheck,
            "requires_calendar_logic_review": requires_calendar_logic_review,
            "requires_timezone_review": requires_timezone_review,
            "requires_algorithm_review": requires_algorithm_review,
            "notes": notes,
            "diagnostic_reason": notes,
        }
    )
    return result


def build_per_session_reconciliation_rows_v1(
    normalized_rows: list[dict[str, Any]],
    *,
    target_months: list[str] | tuple[str, ...] | None = None,
    schedule_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build session-level RTH reconciliation diagnostics from normalized source rows."""
    if not isinstance(normalized_rows, list):
        raise AcquisitionGenerationError("normalized_rows must be a list")
    months = _normalize_target_months(target_months)
    schedule = _session_rows_for_months(months, schedule_rows=schedule_rows)
    open_session_dates = {row["session_date"] for row in schedule_rows} if schedule_rows is not None else {
        row["session_date"] for row in calendar_service.build_exchange_calendar_schedule_rows_v1()
    }
    timestamped_rows: list[tuple[datetime, dict[str, Any]]] = []
    for row in normalized_rows:
        if not isinstance(row, dict):
            raise AcquisitionGenerationError("normalized_rows must contain JSON objects")
        timestamp = _timestamp_utc_or_none(row)
        if timestamp is not None:
            timestamped_rows.append((timestamp, row))

    diagnostics: list[dict[str, Any]] = []
    for session in schedule:
        open_utc = _parse_utc(session["market_open_utc"])
        close_utc = _parse_utc(session["market_close_utc"])
        session_rows = [(timestamp, row) for timestamp, row in timestamped_rows if open_utc <= timestamp < close_utc]
        session_rows.sort(key=lambda item: item[0])
        observed = len(session_rows)
        session_minutes = _int_or_none(session.get("session_minutes"))
        expected = None if session_minutes is None or session_minutes % 15 != 0 else session_minutes // 15
        chunk_ids = sorted({str(row.get("source_chunk_id")) for _, row in session_rows if row.get("source_chunk_id")})
        source_months = sorted({str(row.get("source_month")) for _, row in session_rows if row.get("source_month")})
        session_type = "FULL" if session.get("is_full_session") is True else "HALF" if session.get("is_half_session") is True else "SPECIAL"
        base = {
            "session_date": session["session_date"],
            "month": session["session_date"][:7],
            "session_type": session_type,
            "calendar_open_local": session.get("market_open_local"),
            "calendar_close_local": session.get("market_close_local"),
            "calendar_open_utc": session["market_open_utc"],
            "calendar_close_utc": session["market_close_utc"],
            "market_open_utc": session["market_open_utc"],
            "market_close_utc": session["market_close_utc"],
            "session_minutes": session_minutes,
            "is_full_session": session.get("is_full_session") is True,
            "is_special_close": session.get("is_half_session") is True,
            "is_holiday_adjacent": _is_holiday_adjacent(session["session_date"], open_session_dates),
            "expected_15m_bars": expected,
            "expected_rth_rows": expected,
            "observed_15m_bars": observed,
            "observed_rth_rows": observed,
            "first_observed_rth_timestamp_utc": _iso_utc(session_rows[0][0]) if session_rows else None,
            "last_observed_rth_timestamp_utc": _iso_utc(session_rows[-1][0]) if session_rows else None,
            "provider_chunk_id": ",".join(chunk_ids) if chunk_ids else f"AAPL-{session['session_date'][:7]}",
            "provider_chunk_month": ",".join(source_months) if source_months else session["session_date"][:7],
        }
        diagnostics.append(classify_session_reconciliation_issue_v1(base))
    diagnostics.sort(key=lambda row: row["session_date"])
    return diagnostics


def _per_session_status_from_rows(rows: list[dict[str, Any]]) -> str:
    if any(row.get("issue_severity") == SEVERITY_BLOCKER for row in rows):
        return ACQUISITION_PER_SESSION_DIAGNOSTICS_REQUIRES_OPERATOR_REVIEW
    if any(row.get("issue_severity") == SEVERITY_HIGH for row in rows):
        return ACQUISITION_PER_SESSION_DIAGNOSTICS_REQUIRES_OPERATOR_REVIEW
    return ACQUISITION_PER_SESSION_DIAGNOSTICS_COMPLETE


def _january_cross_check_status_from_session_rows(rows: list[dict[str, Any]], target_months: list[str]) -> str:
    january = [row for row in rows if row.get("month") == "2025-01"]
    if not january:
        return "PASSED_FROM_MONTHLY_TRIAGE" if "2025-01" not in target_months else "NOT_PRESENT"
    if any(row.get("issue_severity") == SEVERITY_BLOCKER for row in january):
        return "FAILED"
    if all(row.get("issue_category") == ISSUE_CATEGORY_RECONCILED for row in january):
        return "PASSED"
    return "FAILED"


def _blocked_per_session_diagnostics(
    *,
    target_months: list[str],
    source_acquisition_candidate_digest: str,
    source_monthly_reconciliation_digest: str,
) -> dict[str, Any]:
    diagnostics = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS,
        "schema_version": SCHEMA_VERSION_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS_V1,
        "diagnostics_status": ACQUISITION_PER_SESSION_DIAGNOSTICS_BLOCKED_MISSING_ROW_LEVEL_DATA,
        "source_acquisition_candidate_digest": source_acquisition_candidate_digest,
        "source_monthly_reconciliation_digest": source_monthly_reconciliation_digest,
        "target_months": target_months,
        "target_month_count": len(target_months),
        "row_level_source_available": False,
        "session_diagnostics_available": False,
        "blocked_reason": "ROW_LEVEL_NORMALIZED_SOURCE_DATA_NOT_AVAILABLE",
        "instrumentation_added_for_future_generation_runs": True,
        "total_sessions_evaluated": 0,
        "reconciled_sessions": 0,
        "non_reconciled_sessions": 0,
        "missing_bar_sessions": 0,
        "extra_bar_sessions": 0,
        "calendar_duration_review_sessions": 0,
        "blocker_count": 0,
        "high_count": 0,
        "issue_category_summary": {},
        "issue_severity_summary": {},
        "session_diagnostics": [],
        "accepted_2025_01_cross_check_status": "PASSED_FROM_MONTHLY_TRIAGE",
        "ready_for_acquisition_review": False,
        "operator_review_required": True,
        "provider_requests_made": False,
        "provider_refresh_performed": False,
        "full_rerun_performed": False,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "authority_boundary": _authority_boundary(),
        "next_required_task": "Run a separately gated generation that emits row-level per-session reconciliation diagnostics.",
    }
    diagnostics["per_session_diagnostics_semantic_digest"] = acquisition_per_session_reconciliation_diagnostics_semantic_digest_v1(
        diagnostics
    )
    return diagnostics


def build_acquisition_per_session_reconciliation_diagnostics_v1(
    normalized_rows: list[dict[str, Any]] | None = None,
    *,
    target_months: list[str] | tuple[str, ...] | None = None,
    schedule_rows: list[dict[str, Any]] | None = None,
    source_acquisition_candidate_digest: str = EXPECTED_FULL_LIVE_ACQUISITION_CANDIDATE_DIGEST,
    source_monthly_reconciliation_digest: str = EXPECTED_FULL_LIVE_MONTHLY_RECONCILIATION_DIGEST,
) -> dict[str, Any]:
    """Build per-session reconciliation diagnostics, or a blocked artifact when rows are unavailable."""
    months = _normalize_target_months(target_months)
    if normalized_rows is None:
        diagnostics = _blocked_per_session_diagnostics(
            target_months=months,
            source_acquisition_candidate_digest=source_acquisition_candidate_digest,
            source_monthly_reconciliation_digest=source_monthly_reconciliation_digest,
        )
        validate_acquisition_per_session_reconciliation_diagnostics_v1(diagnostics)
        return diagnostics

    session_rows = build_per_session_reconciliation_rows_v1(
        normalized_rows,
        target_months=months,
        schedule_rows=schedule_rows,
    )
    status = _per_session_status_from_rows(session_rows)
    total_sessions = len(session_rows)
    non_reconciled = [row for row in session_rows if row["issue_category"] != ISSUE_CATEGORY_RECONCILED]
    ready_for_review = status == ACQUISITION_PER_SESSION_DIAGNOSTICS_COMPLETE
    diagnostics = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS,
        "schema_version": SCHEMA_VERSION_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS_V1,
        "diagnostics_status": status,
        "source_acquisition_candidate_digest": source_acquisition_candidate_digest,
        "source_monthly_reconciliation_digest": source_monthly_reconciliation_digest,
        "target_months": months,
        "target_month_count": len(months),
        "row_level_source_available": True,
        "session_diagnostics_available": True,
        "blocked_reason": None,
        "instrumentation_added_for_future_generation_runs": True,
        "total_sessions_evaluated": total_sessions,
        "reconciled_sessions": total_sessions - len(non_reconciled),
        "non_reconciled_sessions": len(non_reconciled),
        "missing_bar_sessions": sum(1 for row in session_rows if row["issue_category"] == ISSUE_CATEGORY_MISSING_RTH_BARS),
        "extra_bar_sessions": sum(1 for row in session_rows if row["issue_category"] == ISSUE_CATEGORY_EXTRA_RTH_BARS),
        "calendar_duration_review_sessions": sum(
            1 for row in session_rows if row["issue_category"] == ISSUE_CATEGORY_CALENDAR_SESSION_DURATION_REVIEW_REQUIRED
        ),
        "blocker_count": sum(1 for row in session_rows if row["issue_severity"] == SEVERITY_BLOCKER),
        "high_count": sum(1 for row in session_rows if row["issue_severity"] == SEVERITY_HIGH),
        "issue_category_summary": _count_by(session_rows, "issue_category"),
        "issue_severity_summary": _count_by(session_rows, "issue_severity"),
        "session_diagnostics": session_rows,
        "accepted_2025_01_cross_check_status": _january_cross_check_status_from_session_rows(session_rows, months),
        "ready_for_acquisition_review": ready_for_review,
        "operator_review_required": not ready_for_review,
        "provider_requests_made": False,
        "provider_refresh_performed": False,
        "full_rerun_performed": False,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "authority_boundary": _authority_boundary(),
        "next_required_task": "Operator review of unreconciled per-session diagnostics before any acquisition freeze.",
    }
    diagnostics["per_session_diagnostics_semantic_digest"] = acquisition_per_session_reconciliation_diagnostics_semantic_digest_v1(
        diagnostics
    )
    validate_acquisition_per_session_reconciliation_diagnostics_v1(diagnostics)
    return diagnostics


def validate_acquisition_per_session_reconciliation_diagnostics_v1(diagnostics: dict[str, Any]) -> dict[str, Any]:
    """Validate per-session diagnostics and reject premature authority claims."""
    if not isinstance(diagnostics, dict):
        raise AcquisitionGenerationError("per-session diagnostics must be a JSON object")
    _expect(diagnostics.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS, "artifact_kind")
    _expect(
        diagnostics.get("schema_version"),
        SCHEMA_VERSION_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS_V1,
        "schema_version",
    )
    if diagnostics.get("diagnostics_status") not in {
        ACQUISITION_PER_SESSION_DIAGNOSTICS_COMPLETE,
        ACQUISITION_PER_SESSION_DIAGNOSTICS_BLOCKED_MISSING_ROW_LEVEL_DATA,
        ACQUISITION_PER_SESSION_DIAGNOSTICS_REQUIRES_OPERATOR_REVIEW,
    }:
        raise AcquisitionGenerationError("diagnostics_status mismatch")
    _expect(
        diagnostics.get("source_acquisition_candidate_digest"),
        EXPECTED_FULL_LIVE_ACQUISITION_CANDIDATE_DIGEST,
        "source_acquisition_candidate_digest",
    )
    _expect(
        diagnostics.get("source_monthly_reconciliation_digest"),
        EXPECTED_FULL_LIVE_MONTHLY_RECONCILIATION_DIGEST,
        "source_monthly_reconciliation_digest",
    )
    for field in (
        "provider_requests_made",
        "provider_refresh_performed",
        "full_rerun_performed",
        "acquisition_generation_freeze",
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(diagnostics.get(field), field)
    _expect(diagnostics.get("predictive_usefulness"), PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(diagnostics.get("profitability"), PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(diagnostics.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    target_months = diagnostics.get("target_months")
    if not isinstance(target_months, list):
        raise AcquisitionGenerationError("target_months must be a list")
    _expect(diagnostics.get("target_month_count"), len(target_months), "target_month_count")
    rows = diagnostics.get("session_diagnostics")
    if not isinstance(rows, list):
        raise AcquisitionGenerationError("session_diagnostics must be a list")
    _expect(diagnostics.get("total_sessions_evaluated"), len(rows), "total_sessions_evaluated")
    reconciled = sum(1 for row in rows if row.get("issue_category") == ISSUE_CATEGORY_RECONCILED)
    _expect(diagnostics.get("reconciled_sessions"), reconciled, "reconciled_sessions")
    _expect(diagnostics.get("non_reconciled_sessions"), len(rows) - reconciled, "non_reconciled_sessions")
    _expect(diagnostics.get("blocker_count"), sum(1 for row in rows if row.get("issue_severity") == SEVERITY_BLOCKER), "blocker_count")
    _expect(diagnostics.get("high_count"), sum(1 for row in rows if row.get("issue_severity") == SEVERITY_HIGH), "high_count")
    if diagnostics.get("diagnostics_status") == ACQUISITION_PER_SESSION_DIAGNOSTICS_BLOCKED_MISSING_ROW_LEVEL_DATA:
        _expect_false(diagnostics.get("row_level_source_available"), "row_level_source_available")
        _expect_false(diagnostics.get("session_diagnostics_available"), "session_diagnostics_available")
        _expect(diagnostics.get("blocked_reason"), "ROW_LEVEL_NORMALIZED_SOURCE_DATA_NOT_AVAILABLE", "blocked_reason")
        _expect_false(diagnostics.get("ready_for_acquisition_review"), "ready_for_acquisition_review")
        _expect_true(diagnostics.get("operator_review_required"), "operator_review_required")
    elif diagnostics.get("diagnostics_status") == ACQUISITION_PER_SESSION_DIAGNOSTICS_COMPLETE:
        _expect_true(diagnostics.get("row_level_source_available"), "row_level_source_available")
        _expect_true(diagnostics.get("session_diagnostics_available"), "session_diagnostics_available")
        _expect_true(diagnostics.get("ready_for_acquisition_review"), "ready_for_acquisition_review")
    elif diagnostics.get("non_reconciled_sessions", 0) > 0 or diagnostics.get("blocker_count", 0) > 0:
        _expect_false(diagnostics.get("ready_for_acquisition_review"), "ready_for_acquisition_review")
        _expect_true(diagnostics.get("operator_review_required"), "operator_review_required")
    digest = diagnostics.get("per_session_diagnostics_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AcquisitionGenerationError("per_session_diagnostics_semantic_digest missing")
    _expect(
        digest,
        acquisition_per_session_reconciliation_diagnostics_semantic_digest_v1(diagnostics),
        "per_session_diagnostics_semantic_digest",
    )
    return {
        "status": "ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS_VALID",
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS,
        "diagnostics_status": diagnostics["diagnostics_status"],
        "target_month_count": diagnostics["target_month_count"],
        "total_sessions_evaluated": diagnostics["total_sessions_evaluated"],
        "non_reconciled_sessions": diagnostics["non_reconciled_sessions"],
        "ready_for_acquisition_review": diagnostics["ready_for_acquisition_review"],
        "per_session_diagnostics_semantic_digest": digest,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
    }


def write_per_session_reconciliation_csv_v1(path: str | Path, session_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Write compact session diagnostics without raw OHLCV/provider payload fields."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PER_SESSION_RECONCILIATION_CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in session_rows:
            writer.writerow(row)
    data = output_path.read_bytes()
    return {
        "path": str(output_path),
        "filename": output_path.name,
        "row_count": len(session_rows),
        "csv_sha256": sha256_bytes(data),
    }


def build_acquisition_per_session_reconciliation_diagnostics_markdown_v1(diagnostics: dict[str, Any]) -> str:
    """Render a sanitized per-session reconciliation diagnostics status document."""
    validate_acquisition_per_session_reconciliation_diagnostics_v1(diagnostics)
    boundary = diagnostics["authority_boundary"]
    lines = [
        "# MarketFlow Acquisition Per-Session Reconciliation Diagnostics Status",
        "",
        "## Scope",
        f"- Artifact kind: `{diagnostics['artifact_kind']}`",
        f"- Diagnostics status: `{diagnostics['diagnostics_status']}`",
        f"- Source acquisition candidate digest: `{diagnostics['source_acquisition_candidate_digest']}`",
        f"- Source monthly reconciliation digest: `{diagnostics['source_monthly_reconciliation_digest']}`",
        f"- Target month count: `{diagnostics['target_month_count']}`",
        f"- Target months: `{', '.join(diagnostics['target_months'])}`",
        f"- Row-level source available: `{diagnostics['row_level_source_available']}`",
        f"- Session diagnostics available: `{diagnostics['session_diagnostics_available']}`",
        f"- Blocked reason: `{diagnostics['blocked_reason']}`",
        f"- Instrumentation added for future generation runs: `{diagnostics['instrumentation_added_for_future_generation_runs']}`",
        f"- 2025-01 cross-check status: `{diagnostics['accepted_2025_01_cross_check_status']}`",
        f"- Acquisition operator review: `{'ALLOWED' if diagnostics['ready_for_acquisition_review'] else 'BLOCKED'}`",
        "",
        "## Session Summary",
        f"- Total sessions evaluated: `{diagnostics['total_sessions_evaluated']}`",
        f"- Reconciled sessions: `{diagnostics['reconciled_sessions']}`",
        f"- Non-reconciled sessions: `{diagnostics['non_reconciled_sessions']}`",
        f"- Missing-bar sessions: `{diagnostics['missing_bar_sessions']}`",
        f"- Extra-bar sessions: `{diagnostics['extra_bar_sessions']}`",
        f"- Calendar-duration review sessions: `{diagnostics['calendar_duration_review_sessions']}`",
        f"- Blocker count: `{diagnostics['blocker_count']}`",
        f"- High count: `{diagnostics['high_count']}`",
        f"- Issue category summary: `{json.dumps(diagnostics['issue_category_summary'], sort_keys=True, separators=(',', ':'))}`",
        f"- Issue severity summary: `{json.dumps(diagnostics['issue_severity_summary'], sort_keys=True, separators=(',', ':'))}`",
    ]
    if diagnostics["session_diagnostics"]:
        lines.extend(
            [
                "",
                "## Session Diagnostics",
                "| session_date | month | session_type | expected_15m_bars | observed_15m_bars | delta | missing | extra | first_observed_rth_timestamp_utc | last_observed_rth_timestamp_utc | provider_chunk_id | provider_chunk_month | category | severity | notes |",
                "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in diagnostics["session_diagnostics"]:
            lines.append(
                "| "
                f"{row['session_date']} | "
                f"{row['month']} | "
                f"{row['session_type']} | "
                f"{row['expected_15m_bars']} | "
                f"{row['observed_15m_bars']} | "
                f"{row['rth_row_delta']} | "
                f"{row['missing_count']} | "
                f"{row['extra_count']} | "
                f"{row['first_observed_rth_timestamp_utc']} | "
                f"{row['last_observed_rth_timestamp_utc']} | "
                f"{row['provider_chunk_id']} | "
                f"{row['provider_chunk_month']} | "
                f"{row['issue_category']} | "
                f"{row['issue_severity']} | "
                f"{row['notes']} |"
            )
    else:
        lines.extend(
            [
                "",
                "## Blocked Detail",
                "- Row-level normalized source artifacts for the target months were not available in the local ignored runtime artifacts.",
                "- No per-session rows were fabricated from monthly totals.",
                "- Acquisition review remains blocked until row-level per-session diagnostics can be generated and reviewed.",
            ]
        )
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- identity_segment_frozen: `{boundary['identity_segment_frozen']}`",
            f"- calendar_operator_frozen: `{boundary['calendar_operator_frozen']}`",
            f"- split_event_audit_frozen: `{boundary['split_event_audit_frozen']}`",
            f"- dividend_event_audit_frozen: `{boundary['dividend_event_audit_frozen']}`",
            f"- acquisition_generation_freeze: `{boundary['acquisition_generation_freeze']}`",
            f"- canonical_eligibility: `{boundary['canonical_eligibility']}`",
            f"- registry_eligibility: `{boundary['registry_eligibility']}`",
            f"- strategy_runtime_migration: `{boundary['strategy_runtime_migration']}`",
            f"- automatic_stitching: `{boundary['automatic_stitching']}`",
            f"- predictive_usefulness: `{boundary['predictive_usefulness']}`",
            f"- profitability: `{boundary['profitability']}`",
            "",
            "## Non-Goals",
            "- No provider refresh was performed.",
            "- No full acquisition generation rerun was performed.",
            "- No API key, raw provider payload, generated bars, personal, broker, or tax data is included.",
            "- No acquisition-generation freeze was created.",
            "- No canonical, registry, runtime, predictive, or profitability approval occurred.",
            "",
            "## Next Task Recommendation",
            f"- {diagnostics['next_required_task']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_acquisition_per_session_reconciliation_diagnostics_status_v1(
    path: str | Path,
    *,
    diagnostics: dict[str, Any],
) -> dict[str, Any]:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = build_acquisition_per_session_reconciliation_diagnostics_markdown_v1(diagnostics)
    output_path.write_text(text, encoding="utf-8")
    return {
        "path": str(output_path),
        "filename": output_path.name,
        "status_document_digest": sha256_bytes(text.encode("utf-8")),
    }


def _normalize_targeted_session_months(target_months: list[str] | tuple[str, ...] | None) -> list[str]:
    months = _normalize_target_months(target_months)
    expected = list(DEFAULT_PER_SESSION_DIAGNOSTIC_TARGET_MONTHS)
    if months != expected:
        raise AcquisitionGenerationError("targeted session diagnostic rerun must use exactly the 9 non-reconciled target months")
    return months


def build_targeted_acquisition_month_chunks_v1(
    *,
    target_months: list[str] | tuple[str, ...] | None = None,
    ticker: str = "AAPL",
) -> list[dict[str, Any]]:
    """Build deterministic monthly request metadata for the 9 target diagnostic months."""
    months = _normalize_targeted_session_months(target_months)
    chunks = [chunk for chunk in build_acquisition_month_chunks_v1(ticker=ticker) if chunk["month"] in set(months)]
    chunks.sort(key=lambda chunk: chunk["month"])
    if [chunk["month"] for chunk in chunks] != months:
        raise AcquisitionGenerationError("targeted session diagnostic chunk list mismatch")
    return chunks


def targeted_session_diagnostics_digest_v1(session_rows: list[dict[str, Any]]) -> str:
    return semantic_digest(session_rows)


def _targeted_diagnostic_receipt_payload(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": result["artifact_kind"],
        "rerun_status": result["rerun_status"],
        "acquisition_operator_review_status": result["acquisition_operator_review_status"],
        "provider_request_mode": result.get("provider_request_mode"),
        "provider_requests_made": result.get("provider_requests_made"),
        "target_months": result.get("target_months"),
        "target_chunk_count_expected": result.get("target_chunk_count_expected"),
        "target_chunk_count_completed": result.get("target_chunk_count_completed"),
        "target_failed_chunk_count": result.get("target_failed_chunk_count"),
        "all_9_monthly_mismatches_explained": result.get("all_9_monthly_mismatches_explained"),
        "targeted_chunk_manifest_digest": result.get("targeted_chunk_manifest_digest"),
        "targeted_provider_raw_response_digest": result.get("targeted_provider_raw_response_digest"),
        "targeted_normalized_rows_digest": result.get("targeted_normalized_rows_digest"),
        "targeted_monthly_reconciliation_digest": result.get("targeted_monthly_reconciliation_digest"),
        "per_session_diagnostics_digest": result.get("per_session_diagnostics_digest"),
    }


def targeted_diagnostic_receipt_digest_v1(result: dict[str, Any]) -> str:
    return semantic_digest(_targeted_diagnostic_receipt_payload(result))


def _targeted_result_digest_payload(result: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(result)
    payload.pop("targeted_diagnostic_receipt_digest", None)
    payload.pop("targeted_session_diagnostic_rerun_semantic_digest", None)
    return payload


def targeted_session_diagnostic_rerun_semantic_digest_v1(result: dict[str, Any]) -> str:
    return semantic_digest(_targeted_result_digest_payload(result))


def _targeted_provider_records_from_responses(
    provider_responses: list[dict[str, Any]],
    *,
    chunks: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    provider_records, normalized_rows = _provider_records_from_responses(provider_responses, chunks=chunks)
    classified_rows = classify_normalized_source_rows_v1(normalized_rows)
    monthly_reconciliation = build_monthly_reconciliation_v1(classified_rows, chunks=chunks)
    _merge_reconciliation_into_provider_records(provider_records, monthly_reconciliation)
    return provider_records, normalized_rows


def _session_rows_by_month(session_rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in session_rows:
        grouped.setdefault(row["month"], []).append(row)
    return grouped


def _month_explanation_rows(
    monthly_reconciliation: list[dict[str, Any]],
    session_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sessions_by_month = _session_rows_by_month(session_rows)
    explanation_rows: list[dict[str, Any]] = []
    for month in monthly_reconciliation:
        month_key = month["month"]
        sessions = sessions_by_month.get(month_key, [])
        expected_all_sessions = sum(int(row["expected_rth_rows"]) for row in sessions if row.get("expected_rth_rows") is not None)
        observed_all_sessions = sum(int(row["observed_rth_rows"]) for row in sessions)
        non_reconciled_sessions = [row for row in sessions if row.get("issue_category") != ISSUE_CATEGORY_RECONCILED]
        legacy_delta = month.get("validated_rth_rows") - month.get("expected_rth_rows")
        special_session_expected_rows = sum(
            int(row["expected_rth_rows"])
            for row in sessions
            if row.get("is_special_close") is True and row.get("expected_rth_rows") is not None
        )
        explained = (
            len(non_reconciled_sessions) == 0
            and observed_all_sessions == expected_all_sessions
            and legacy_delta == special_session_expected_rows
        )
        if month.get("rth_reconciliation_status") == RTH_SOURCE_ROWS_RECONCILED and len(non_reconciled_sessions) == 0:
            explanation_status = "RECONCILED"
            explained = True
        elif explained:
            explanation_status = "EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION"
        else:
            explanation_status = "UNEXPLAINED"
        explanation_rows.append(
            {
                "month": month_key,
                "monthly_reconciliation_status": month.get("rth_reconciliation_status"),
                "legacy_expected_rth_rows": month.get("expected_rth_rows"),
                "validated_rth_rows": month.get("validated_rth_rows"),
                "legacy_rth_row_delta": legacy_delta,
                "session_expected_rth_rows": expected_all_sessions,
                "session_observed_rth_rows": observed_all_sessions,
                "special_session_expected_rth_rows": special_session_expected_rows,
                "non_reconciled_session_count": len(non_reconciled_sessions),
                "targeted_reconciliation_explanation_status": explanation_status,
                "monthly_mismatch_explained": explained,
            }
        )
    return explanation_rows


def _sanitize_targeted_chunk_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "chunk_id": record["chunk_id"],
        "month": record["month"],
        "from": record["from"],
        "to": record["to"],
        "provider_response_status": record["provider_response_status"],
        "raw_row_count": record["raw_row_count"],
        "normalized_row_count": record["normalized_row_count"],
        "rth_row_count": record["rth_row_count"],
        "extended_hours_row_count": record["extended_hours_row_count"],
        "raw_response_digest": record["raw_response_digest"],
        "normalized_rows_digest": record["normalized_rows_digest"],
        "monthly_reconciliation_digest": record["monthly_reconciliation_digest"],
        "warnings": list(record.get("warnings", [])),
        "errors": list(record.get("errors", [])),
    }


def build_acquisition_targeted_session_diagnostic_rerun_v1(
    *,
    api_key: str | None = None,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    provider_request_timestamp_utc: str | None = None,
    target_months: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Run the gated 9-month provider diagnostic and return only sanitized diagnostic metadata."""
    months = _normalize_targeted_session_months(target_months)
    timestamp = provider_request_timestamp_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if transport is None and os.environ.get(MARKETFLOW_ENABLE_LIVE_ACQUISITION_GENERATION) != "1":
        raise AcquisitionGenerationError(LIVE_TARGETED_SESSION_DIAGNOSTICS_BLOCKED_GATE_NOT_ENABLED)
    key = api_key or _api_key_from_environment()
    if not key:
        raise AcquisitionGenerationError(LIVE_TARGETED_SESSION_DIAGNOSTICS_BLOCKED_MISSING_API_KEY)
    chunks = build_targeted_acquisition_month_chunks_v1(target_months=months)
    provider_responses: list[dict[str, Any]] = []
    failed_records: list[dict[str, Any]] = []
    for chunk in chunks:
        try:
            raw = acquisition_adapter.fetch_massive_custom_bars_live_v1(
                ticker=FIXED_IDENTITY_SEGMENT["ticker"],
                start_date=chunk["effective_start_date"],
                end_date=chunk["effective_end_date"],
                api_key=key,
                transport=transport,
                request_timestamp_utc=timestamp,
            )
        except Exception as exc:
            failed_records.append(_failed_chunk_record(chunk, exc))
            continue
        provider_responses.append(
            {
                "month": chunk["month"],
                "response": raw["provider_response_body"],
                "raw_metadata": {field: value for field, value in raw.items() if field != "provider_response_body"},
            }
        )

    provider_records, normalized_rows = _targeted_provider_records_from_responses(provider_responses, chunks=chunks)
    classified_rows = classify_normalized_source_rows_v1(normalized_rows)
    monthly_reconciliation = build_monthly_reconciliation_v1(classified_rows, chunks=chunks)
    session_rows = build_per_session_reconciliation_rows_v1(normalized_rows, target_months=months)
    month_explanations = _month_explanation_rows(monthly_reconciliation, session_rows)
    completed = len(provider_records)
    failed = len(failed_records)
    all_explained = completed == len(chunks) and failed == 0 and all(row["monthly_mismatch_explained"] for row in month_explanations)
    blocker_count = sum(1 for row in session_rows if row.get("issue_severity") == SEVERITY_BLOCKER)
    high_count = sum(1 for row in session_rows if row.get("issue_severity") == SEVERITY_HIGH)
    unresolved_sessions = [row for row in session_rows if row.get("issue_category") != ISSUE_CATEGORY_RECONCILED]
    review_status = (
        ACQUISITION_OPERATOR_REVIEW_READY_AFTER_TRIAGE
        if all_explained and blocker_count == 0
        else ACQUISITION_OPERATOR_REVIEW_BLOCKED_PENDING_RECONCILIATION_EXPLANATION
    )
    result = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN,
        "schema_version": SCHEMA_VERSION_ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_V1,
        "rerun_status": (
            ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_COMPLETE
            if completed == len(chunks) and failed == 0
            else ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_INCOMPLETE
        ),
        "acquisition_operator_review_status": review_status,
        "target_months": months,
        "target_month_count": len(months),
        "provider_name": PROVIDER_NAME_MASSIVE,
        "provider_endpoint": PROVIDER_ENDPOINT_MASSIVE_CUSTOM_BARS,
        "provider_request_mode": PROVIDER_REQUEST_MODE_LIVE if transport is None else PROVIDER_REQUEST_MODE_FAKE_TRANSPORT,
        "provider_request_timestamp_utc": timestamp,
        "provider_requests_made": transport is None,
        "provider_response_injected": transport is not None,
        "target_chunk_count_expected": len(chunks),
        "target_chunk_count_completed": completed,
        "target_failed_chunk_count": failed,
        "failed_chunks": failed_records,
        "targeted_chunk_manifest": chunks,
        "targeted_chunk_records": [_sanitize_targeted_chunk_record(record) for record in provider_records],
        "targeted_monthly_reconciliation": monthly_reconciliation,
        "targeted_month_explanations": month_explanations,
        "targeted_per_session_diagnostics": session_rows,
        "non_reconciled_sessions": [
            {
                "month": row["month"],
                "session_date": row["session_date"],
                "issue_category": row["issue_category"],
                "issue_severity": row["issue_severity"],
                "rth_row_delta": row["rth_row_delta"],
            }
            for row in unresolved_sessions
        ],
        "all_9_monthly_mismatches_explained": all_explained,
        "issue_category_summary": _count_by(session_rows, "issue_category"),
        "issue_severity_summary": _count_by(session_rows, "issue_severity"),
        "blocker_count": blocker_count,
        "high_count": high_count,
        "api_key_stored": False,
        "raw_provider_payload_stored": False,
        "generated_bars_stored": False,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "authority_boundary": _authority_boundary(),
        "targeted_chunk_manifest_digest": chunk_manifest_digest_v1(chunks),
        "targeted_provider_raw_response_digest": semantic_digest(
            {"completed": [_sanitize_targeted_chunk_record(record) for record in provider_records], "failed": failed_records}
        ),
        "targeted_normalized_rows_digest": normalized_source_rows_digest_v1(normalized_rows) if provider_responses else None,
        "targeted_monthly_reconciliation_digest": monthly_reconciliation_digest_v1(monthly_reconciliation) if provider_responses else None,
        "per_session_diagnostics_digest": targeted_session_diagnostics_digest_v1(session_rows),
        "next_required_task": (
            "Acquisition operator review may proceed after human review of targeted triage evidence."
            if review_status == ACQUISITION_OPERATOR_REVIEW_READY_AFTER_TRIAGE
            else "Resolve unexplained per-session diagnostics before acquisition operator review."
        ),
    }
    result["targeted_diagnostic_receipt_digest"] = targeted_diagnostic_receipt_digest_v1(result)
    result["targeted_session_diagnostic_rerun_semantic_digest"] = targeted_session_diagnostic_rerun_semantic_digest_v1(result)
    validate_acquisition_targeted_session_diagnostic_rerun_v1(result)
    return result


def validate_acquisition_targeted_session_diagnostic_rerun_v1(result: dict[str, Any]) -> dict[str, Any]:
    """Validate targeted session diagnostics and reject authority escalation."""
    if not isinstance(result, dict):
        raise AcquisitionGenerationError("targeted session diagnostic rerun must be a JSON object")
    _expect(result.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN, "artifact_kind")
    _expect(result.get("schema_version"), SCHEMA_VERSION_ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_V1, "schema_version")
    _expect(result.get("target_months"), list(DEFAULT_PER_SESSION_DIAGNOSTIC_TARGET_MONTHS), "target_months")
    _expect(result.get("target_month_count"), 9, "target_month_count")
    _expect(result.get("target_chunk_count_expected"), 9, "target_chunk_count_expected")
    if result.get("rerun_status") not in {
        ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_COMPLETE,
        ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_INCOMPLETE,
    }:
        raise AcquisitionGenerationError("rerun_status mismatch")
    if result.get("acquisition_operator_review_status") not in {
        ACQUISITION_OPERATOR_REVIEW_READY_AFTER_TRIAGE,
        ACQUISITION_OPERATOR_REVIEW_BLOCKED_PENDING_RECONCILIATION_EXPLANATION,
    }:
        raise AcquisitionGenerationError("acquisition_operator_review_status mismatch")
    for field in (
        "api_key_stored",
        "raw_provider_payload_stored",
        "generated_bars_stored",
        "acquisition_generation_freeze",
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(result.get(field), field)
    _expect(result.get("predictive_usefulness"), PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(result.get("profitability"), PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(result.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    chunks = result.get("targeted_chunk_records")
    sessions = result.get("targeted_per_session_diagnostics")
    monthly = result.get("targeted_monthly_reconciliation")
    if not isinstance(chunks, list) or not isinstance(sessions, list) or not isinstance(monthly, list):
        raise AcquisitionGenerationError("targeted diagnostics lists missing")
    observed_months = {row["month"] for row in chunks}
    if not observed_months.issubset(set(DEFAULT_PER_SESSION_DIAGNOSTIC_TARGET_MONTHS)):
        raise AcquisitionGenerationError("targeted chunks include non-target month")
    for row in sessions:
        forbidden = {"open", "high", "low", "close", "volume", "vwap", "transactions", "raw_row_digest"}
        if forbidden.intersection(row):
            raise AcquisitionGenerationError("targeted session diagnostics contain raw bar fields")
    if result.get("all_9_monthly_mismatches_explained") is True and result.get("blocker_count") == 0:
        _expect(
            result.get("acquisition_operator_review_status"),
            ACQUISITION_OPERATOR_REVIEW_READY_AFTER_TRIAGE,
            "acquisition_operator_review_status",
        )
    if result.get("all_9_monthly_mismatches_explained") is not True:
        _expect(
            result.get("acquisition_operator_review_status"),
            ACQUISITION_OPERATOR_REVIEW_BLOCKED_PENDING_RECONCILIATION_EXPLANATION,
            "acquisition_operator_review_status",
        )
    _expect(result.get("targeted_diagnostic_receipt_digest"), targeted_diagnostic_receipt_digest_v1(result), "targeted_diagnostic_receipt_digest")
    _expect(
        result.get("targeted_session_diagnostic_rerun_semantic_digest"),
        targeted_session_diagnostic_rerun_semantic_digest_v1(result),
        "targeted_session_diagnostic_rerun_semantic_digest",
    )
    return {
        "status": "ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_VALID",
        "rerun_status": result["rerun_status"],
        "acquisition_operator_review_status": result["acquisition_operator_review_status"],
        "target_chunk_count_expected": result["target_chunk_count_expected"],
        "target_chunk_count_completed": result["target_chunk_count_completed"],
        "target_failed_chunk_count": result["target_failed_chunk_count"],
        "all_9_monthly_mismatches_explained": result["all_9_monthly_mismatches_explained"],
        "targeted_diagnostic_receipt_digest": result["targeted_diagnostic_receipt_digest"],
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
    }


def write_targeted_session_diagnostics_csv_v1(path: str | Path, session_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Write compact targeted session diagnostics without OHLCV or raw payload fields."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TARGETED_SESSION_DIAGNOSTIC_CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in session_rows:
            writer.writerow(row)
    data = output_path.read_bytes()
    return {
        "path": str(output_path),
        "filename": output_path.name,
        "row_count": len(session_rows),
        "csv_sha256": sha256_bytes(data),
    }


def build_acquisition_targeted_session_diagnostic_rerun_markdown_v1(result: dict[str, Any]) -> str:
    """Render a sanitized targeted session diagnostic rerun status document."""
    validate_acquisition_targeted_session_diagnostic_rerun_v1(result)
    boundary = result["authority_boundary"]
    lines = [
        "# MarketFlow Acquisition Targeted Session Diagnostic Rerun Status",
        "",
        "## Scope",
        f"- Artifact kind: `{result['artifact_kind']}`",
        f"- Rerun status: `{result['rerun_status']}`",
        f"- Acquisition operator review status: `{result['acquisition_operator_review_status']}`",
        f"- Target months: `{', '.join(result['target_months'])}`",
        f"- Endpoint used: `{result['provider_endpoint']}`",
        f"- Request mode: `{result['provider_request_mode']}`",
        f"- Expected target chunks: `{result['target_chunk_count_expected']}`",
        f"- Completed target chunks: `{result['target_chunk_count_completed']}`",
        f"- Failed target chunks: `{result['target_failed_chunk_count']}`",
        f"- All 9 monthly mismatches explained: `{result['all_9_monthly_mismatches_explained']}`",
        "",
        "## Per-Month Results",
        "| month | provider_status | raw_rows | normalized_rows | rth_rows | extended_hours_rows | monthly_status | legacy_delta | session_expected | session_observed | explanation |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |",
    ]
    records_by_month = {record["month"]: record for record in result["targeted_chunk_records"]}
    explanation_by_month = {row["month"]: row for row in result["targeted_month_explanations"]}
    for month in result["target_months"]:
        record = records_by_month.get(month, {})
        explanation = explanation_by_month.get(month, {})
        lines.append(
            "| "
            f"{month} | "
            f"{record.get('provider_response_status')} | "
            f"{record.get('raw_row_count')} | "
            f"{record.get('normalized_row_count')} | "
            f"{record.get('rth_row_count')} | "
            f"{record.get('extended_hours_row_count')} | "
            f"{explanation.get('monthly_reconciliation_status')} | "
            f"{explanation.get('legacy_rth_row_delta')} | "
            f"{explanation.get('session_expected_rth_rows')} | "
            f"{explanation.get('session_observed_rth_rows')} | "
            f"{explanation.get('targeted_reconciliation_explanation_status')} |"
        )
    lines.extend(
        [
            "",
            "## Session Diagnostics",
            f"- Issue category summary: `{json.dumps(result['issue_category_summary'], sort_keys=True, separators=(',', ':'))}`",
            f"- Issue severity summary: `{json.dumps(result['issue_severity_summary'], sort_keys=True, separators=(',', ':'))}`",
            f"- Non-reconciled session count: `{len(result['non_reconciled_sessions'])}`",
        ]
    )
    if result["non_reconciled_sessions"]:
        lines.extend(
            [
                "",
                "## Non-Reconciled Sessions",
                "| month | session_date | category | severity | rth_delta |",
                "| --- | --- | --- | --- | ---: |",
            ]
        )
        for row in result["non_reconciled_sessions"]:
            lines.append(
                f"| {row['month']} | {row['session_date']} | {row['issue_category']} | {row['issue_severity']} | {row['rth_row_delta']} |"
            )
    else:
        lines.extend(["", "## Non-Reconciled Sessions", "- None identified in compact per-session diagnostics."])
    lines.extend(
        [
            "",
            "## Digests",
            f"- Targeted chunk manifest digest: `{result['targeted_chunk_manifest_digest']}`",
            f"- Targeted provider raw response digest: `{result['targeted_provider_raw_response_digest']}`",
            f"- Targeted normalized rows digest: `{result['targeted_normalized_rows_digest']}`",
            f"- Targeted monthly reconciliation digest: `{result['targeted_monthly_reconciliation_digest']}`",
            f"- Per-session diagnostics digest: `{result['per_session_diagnostics_digest']}`",
            f"- Targeted diagnostic receipt digest: `{result['targeted_diagnostic_receipt_digest']}`",
            "",
            "## Authority Boundary",
            f"- identity_segment_frozen: `{boundary['identity_segment_frozen']}`",
            f"- calendar_operator_frozen: `{boundary['calendar_operator_frozen']}`",
            f"- split_event_audit_frozen: `{boundary['split_event_audit_frozen']}`",
            f"- dividend_event_audit_frozen: `{boundary['dividend_event_audit_frozen']}`",
            f"- acquisition_generation_freeze: `{boundary['acquisition_generation_freeze']}`",
            f"- canonical_eligibility: `{boundary['canonical_eligibility']}`",
            f"- registry_eligibility: `{boundary['registry_eligibility']}`",
            f"- strategy_runtime_migration: `{boundary['strategy_runtime_migration']}`",
            f"- automatic_stitching: `{boundary['automatic_stitching']}`",
            f"- predictive_usefulness: `{boundary['predictive_usefulness']}`",
            f"- profitability: `{boundary['profitability']}`",
            "",
            "## Safeguards",
            f"- API key stored: `{result['api_key_stored']}`",
            f"- Raw provider payload stored: `{result['raw_provider_payload_stored']}`",
            f"- Generated bars stored: `{result['generated_bars_stored']}`",
            "- No acquisition-generation freeze was created.",
            "- No canonical, registry, runtime, predictive, or profitability approval occurred.",
            "- No full 48-month acquisition rerun was performed.",
            "",
            "## Next Task Recommendation",
            f"- {result['next_required_task']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_acquisition_targeted_session_diagnostic_rerun_status_v1(
    path: str | Path,
    *,
    result: dict[str, Any],
) -> dict[str, Any]:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = build_acquisition_targeted_session_diagnostic_rerun_markdown_v1(result)
    output_path.write_text(text, encoding="utf-8")
    return {
        "path": str(output_path),
        "filename": output_path.name,
        "status_document_digest": sha256_bytes(text.encode("utf-8")),
    }


def _parse_markdown_table_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def parse_acquisition_live_status_chunk_manifest_v1(status_markdown: str) -> list[dict[str, Any]]:
    """Parse the sanitized live-generation chunk manifest table from Markdown."""
    rows: list[dict[str, Any]] = []
    in_table = False
    headers: list[str] = []
    for line in status_markdown.splitlines():
        if line.startswith("| chunk_id | month |"):
            headers = _parse_markdown_table_row(line)
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("| ---"):
            continue
        if not line.startswith("| "):
            break
        values = _parse_markdown_table_row(line)
        if len(values) != len(headers):
            raise AcquisitionGenerationError("chunk manifest table row does not match header")
        record = dict(zip(headers, values, strict=True))
        month = record["month"]
        calendar = _calendar_expectation_for_month(month)
        rth_rows = _int_or_none(record["rth_rows"])
        errors = [item for item in record["errors"].split(",") if item] if record["errors"] else []
        status = RTH_SOURCE_ROWS_NOT_RECONCILED if RTH_SOURCE_ROWS_NOT_RECONCILED in errors else RTH_SOURCE_ROWS_RECONCILED
        rows.append(
            {
                "month": month,
                "reconciliation_status": status,
                "normalized_source_rows": _int_or_none(record["normalized_rows"]),
                "rth_rows": rth_rows,
                "extended_hours_rows": _int_or_none(record["extended_hours_rows"]),
                "expected_rth_rows": calendar["expected_rth_rows"],
                "validated_rth_rows": rth_rows,
                "full_ordinary_sessions": calendar["full_ordinary_sessions"],
                "incomplete_ordinary_sessions": None,
                "swing_rth_half_session_195m_bars": calendar["swing_rth_half_session_195m_bars"],
                "position_swing_rth_full_session_1d_bars": calendar["position_swing_rth_full_session_1d_bars"],
                "detail_level": "STATUS_DOC_CHUNK_MANIFEST_ONLY",
                "source_chunk_id": record["chunk_id"],
                "warnings": [item for item in record["warnings"].split(",") if item] if record["warnings"] else [],
                "errors": errors,
            }
        )
    if not rows:
        raise AcquisitionGenerationError("chunk manifest table not found")
    return rows


def build_acquisition_monthly_reconciliation_triage_markdown_v1(triage: dict[str, Any]) -> str:
    """Render a sanitized monthly reconciliation triage status document."""
    validate_acquisition_monthly_reconciliation_triage_v1(triage)
    boundary = triage["authority_boundary"]
    lines = [
        "# MarketFlow Acquisition Monthly Reconciliation Triage Status",
        "",
        "## Scope",
        f"- Artifact kind: `{triage['artifact_kind']}`",
        f"- Triage status: `{triage['triage_status']}`",
        f"- Source acquisition candidate digest: `{triage['source_acquisition_candidate_digest']}`",
        f"- Source monthly reconciliation digest: `{triage['source_monthly_reconciliation_digest']}`",
        f"- Total months: `{triage['total_months']}`",
        f"- Reconciled months: `{triage['reconciled_months']}`",
        f"- Non-reconciled months: `{triage['not_reconciled_months']}`",
        f"- Non-reconciled month list: `{', '.join(triage['non_reconciled_months'])}`",
        f"- Issue category summary: `{json.dumps(triage['issue_category_summary'], sort_keys=True, separators=(',', ':'))}`",
        f"- Issue severity summary: `{json.dumps(triage['issue_severity_summary'], sort_keys=True, separators=(',', ':'))}`",
        f"- 2025-01 cross-check status: `{triage['accepted_2025_01_cross_check_status']}`",
        f"- Acquisition operator review: `{'ALLOWED' if triage['ready_for_acquisition_review'] else 'BLOCKED'}`",
        "",
        "## Triage Table",
        "| month | status | normalized_rows | rth_rows | extended_hours_rows | expected_rth_rows | validated_rth_rows | rth_delta | full_sessions | incomplete_sessions | swing_bars | position_bars | category | severity | operator_review | provider_recheck | calendar_review | algorithm_review | reason |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in triage["triage_rows"]:
        lines.append(
            "| "
            f"{row['month']} | "
            f"{row['reconciliation_status']} | "
            f"{row['normalized_source_rows']} | "
            f"{row['rth_rows']} | "
            f"{row['extended_hours_rows']} | "
            f"{row['expected_rth_rows']} | "
            f"{row['validated_rth_rows']} | "
            f"{row['rth_row_delta']} | "
            f"{row['full_ordinary_sessions']} | "
            f"{row['incomplete_ordinary_sessions']} | "
            f"{row['swing_rth_half_session_195m_bars']} | "
            f"{row['position_swing_rth_full_session_1d_bars']} | "
            f"{row['issue_category']} | "
            f"{row['issue_severity']} | "
            f"{row['requires_operator_review']} | "
            f"{row['requires_provider_recheck']} | "
            f"{row['requires_calendar_logic_review']} | "
            f"{row['requires_algorithm_review']} | "
            f"{row['triage_reason']} |"
        )
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- identity_segment_frozen: `{boundary['identity_segment_frozen']}`",
            f"- calendar_operator_frozen: `{boundary['calendar_operator_frozen']}`",
            f"- split_event_audit_frozen: `{boundary['split_event_audit_frozen']}`",
            f"- dividend_event_audit_frozen: `{boundary['dividend_event_audit_frozen']}`",
            f"- acquisition_generation_freeze: `{boundary['acquisition_generation_freeze']}`",
            f"- canonical_eligibility: `{boundary['canonical_eligibility']}`",
            f"- registry_eligibility: `{boundary['registry_eligibility']}`",
            f"- strategy_runtime_migration: `{boundary['strategy_runtime_migration']}`",
            f"- automatic_stitching: `{boundary['automatic_stitching']}`",
            f"- predictive_usefulness: `{boundary['predictive_usefulness']}`",
            f"- profitability: `{boundary['profitability']}`",
            "",
            "## Non-Goals",
            "- No provider refresh was performed.",
            "- No API key, raw provider payload, generated bars, personal, broker, or tax data is included.",
            "- No acquisition-generation freeze was created.",
            "- No canonical, registry, runtime, predictive, or profitability approval occurred.",
            "",
            "## Next Task Recommendation",
            "- Build a per-session reconciliation diagnostic from ignored local runtime artifacts or a separately gated rerun before acquisition operator review.",
            "",
        ]
    )
    return "\n".join(lines)


def write_acquisition_monthly_reconciliation_triage_status_v1(path: str | Path, *, triage: dict[str, Any]) -> dict[str, Any]:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = build_acquisition_monthly_reconciliation_triage_markdown_v1(triage)
    output_path.write_text(text, encoding="utf-8")
    return {
        "path": str(output_path),
        "filename": output_path.name,
        "status_document_digest": sha256_bytes(text.encode("utf-8")),
    }


def build_acquisition_generation_monthly_live_smoke_markdown_v1(smoke: dict[str, Any]) -> str:
    """Render a sanitized monthly smoke status document without raw bars or credentials."""
    endpoint = PROVIDER_ENDPOINT_MASSIVE_CUSTOM_BARS
    request = smoke.get("request_metadata") if isinstance(smoke.get("request_metadata"), dict) else {}
    boundary = smoke["authority_boundary"]
    bindings = smoke["authority_bindings"]
    lines = [
        "# MarketFlow Acquisition Live Provider Smoke 2025-01 Status",
        "",
        "## Scope",
        f"- Artifact kind: `{smoke['artifact_kind']}`",
        f"- Candidate status: `{smoke['candidate_status']}`",
        f"- Ticker: `{smoke['ticker']}`",
        f"- Month: `{smoke['month']}`",
        f"- Range: `{smoke['range_start']}` through `{smoke['range_end']}`",
        f"- Endpoint used: `{endpoint}`",
        f"- Endpoint path: `{request.get('provider_endpoint_path')}`",
        f"- Request mode: `{smoke.get('provider_request_mode')}`",
        f"- Provider response status: `{smoke.get('provider_response_status')}`",
        "",
        "## Reconciliation",
        f"- Raw row count: `{smoke.get('provider_raw_row_count')}`",
        f"- Normalized source row count: `{smoke.get('normalized_source_row_count')}`",
        f"- RTH row count: `{smoke.get('rth_row_count')}`",
        f"- Extended-hours row count: `{smoke.get('extended_hours_row_count')}`",
        f"- Expected RTH row count: `{smoke.get('expected_rth_rows')}`",
        f"- RTH reconciliation status: `{smoke.get('rth_reconciliation_status')}`",
        f"- Full ordinary sessions: `{smoke.get('full_ordinary_sessions')}`",
        f"- Incomplete ordinary sessions: `{smoke.get('incomplete_ordinary_sessions')}`",
        f"- SWING half-session 195m bars: `{smoke.get('swing_rth_half_session_195m_bars')}`",
        f"- POSITION_SWING full-session 1d bars: `{smoke.get('position_swing_rth_full_session_1d_bars')}`",
        f"- Accepted 2025-01 cross-check passed: `{smoke.get('accepted_2025_01_cross_check_passed')}`",
        "",
        "## Digests",
        f"- Provider raw response digest: `{smoke.get('provider_raw_response_digest')}`",
        f"- Provider raw body sha256: `{smoke.get('provider_raw_body_sha256')}`",
        f"- Normalized rows digest: `{smoke.get('normalized_source_rows_digest')}`",
        f"- Monthly reconciliation digest: `{smoke.get('monthly_reconciliation_digest')}`",
        f"- Acquisition smoke receipt digest: `{smoke.get('acquisition_smoke_receipt_digest')}`",
        f"- Acquisition monthly smoke candidate digest: `{smoke.get('acquisition_monthly_smoke_candidate_digest')}`",
        "",
        "## Authority Bindings",
        f"- Identity frozen digest: `{bindings['identity_segment_frozen_digest']}`",
        f"- Calendar frozen digest: `{bindings['exchange_calendar_frozen_digest']}`",
        f"- Schedule digest: `{bindings['schedule_semantic_digest']}`",
        f"- Split-event audit frozen digest: `{bindings['split_event_audit_frozen_digest']}`",
        f"- Dividend-event audit frozen digest: `{bindings['dividend_event_audit_frozen_digest']}`",
        f"- Acquisition contract digest: `{bindings['acquisition_contract_digest']}`",
        "",
        "## Dividend Implication",
        f"- In-range dividends found: `{smoke['in_range_dividends_found']}`",
        f"- In-range dividend count: `{smoke['in_range_dividend_count']}`",
        f"- Implication: `{smoke['in_range_dividend_implication']}`",
        "",
        "## Authority Boundary",
        f"- acquisition_generation_freeze: `{boundary['acquisition_generation_freeze']}`",
        f"- canonical_eligibility: `{boundary['canonical_eligibility']}`",
        f"- registry_eligibility: `{boundary['registry_eligibility']}`",
        f"- strategy_runtime_migration: `{boundary['strategy_runtime_migration']}`",
        f"- automatic_stitching: `{boundary['automatic_stitching']}`",
        f"- predictive_usefulness: `{boundary['predictive_usefulness']}`",
        f"- profitability: `{boundary['profitability']}`",
        "",
        "## Safety Confirmations",
        f"- API key stored: `{smoke['api_key_stored']}`",
        f"- Raw provider payload stored in this document: `{False}`",
        f"- Full generated bars stored in this document: `{False}`",
        "- No acquisition-generation freeze was created.",
        "- No canonical, registry, runtime, predictive, or profitability approval occurred.",
        "",
        "## Next Task Recommendation",
        f"- {smoke['next_required_task']}",
        "",
    ]
    return "\n".join(lines)


def write_acquisition_generation_monthly_live_smoke_status_v1(path: str | Path, *, smoke: dict[str, Any]) -> dict[str, Any]:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = build_acquisition_generation_monthly_live_smoke_markdown_v1(smoke)
    output_path.write_text(text, encoding="utf-8")
    return {
        "path": str(output_path),
        "filename": output_path.name,
        "status_document_digest": sha256_bytes(text.encode("utf-8")),
    }


def write_acquisition_generation_candidate_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    provider_responses: list[dict[str, Any]] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write acquisition generation candidate JSON without overwriting output."""
    payload = deepcopy(candidate) if candidate is not None else build_acquisition_generation_candidate_v1(provider_responses=provider_responses)
    validation = validate_acquisition_generation_candidate_v1(payload)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_2022-01-01_2025-12-31_acquisition_generation_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AcquisitionGenerationError("acquisition generation candidate filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise AcquisitionGenerationError("acquisition generation candidate output already exists")
    data = canonical_json_bytes(payload)
    with path.open("xb") as handle:
        handle.write(data)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(data),
        "acquisition_generation_candidate_payload_digest": sha256_bytes(data),
    }
