"""Acquisition generation candidate contracts for fixed AAPL 2022-2025 bars."""

from __future__ import annotations

import json
import os
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
SCHEMA_VERSION_ACQUISITION_GENERATION_CANDIDATE_V1 = "acquisition_generation_candidate_v1"
SCHEMA_VERSION_ACQUISITION_MONTHLY_LIVE_SMOKE_V1 = "acquisition_monthly_live_smoke_candidate_v1"
ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW = "ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW"
ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION = "ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION"
ACQUISITION_GENERATION_FROZEN = "ACQUISITION_GENERATION_FROZEN"
ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW = "ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW"
ACQUISITION_MONTHLY_LIVE_SMOKE_RECONCILIATION_MISMATCH = "ACQUISITION_MONTHLY_LIVE_SMOKE_RECONCILIATION_MISMATCH"
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

EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST = dividend_freeze.dividend.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST
EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST = dividend_freeze.dividend.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST
EXPECTED_SCHEDULE_SEMANTIC_DIGEST = dividend_freeze.dividend.EXPECTED_SCHEDULE_SEMANTIC_DIGEST
EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST = dividend_freeze.dividend.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST
EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST = "0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141"
EXPECTED_ACQUISITION_CONTRACT_DIGEST = dividend_freeze.dividend.EXPECTED_ACQUISITION_CONTRACT_DIGEST
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
        "provider_raw_response_digest": candidate.get("provider_raw_response_digest"),
        "normalized_source_rows_digest": candidate.get("normalized_source_rows_digest"),
        "monthly_reconciliation_digest": candidate.get("monthly_reconciliation_digest"),
        "chunk_manifest_digest": candidate.get("provider_chunk_manifest_digest"),
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
        chunk_records.append(
            {
                "chunk_id": chunk["chunk_id"],
                "month": month,
                "provider_response_status": result["provider_response_status"],
                "provider_response_row_count": result["provider_response_row_count"],
                "provider_raw_response_digest": result["provider_raw_response_digest"],
                "provider_projection_digest": result["provider_projection_digest"],
                "request_semantic_digest": chunk["request_semantic_digest"],
            }
        )
        normalized_rows.extend(result["normalized_rows"])
    normalized_rows.sort(key=lambda row: (row["timestamp_utc"], row["source_chunk_id"], row["source_row_index"]))
    for index, row in enumerate(normalized_rows):
        row["source_row_index"] = index
    return chunk_records, normalized_rows


def build_acquisition_generation_candidate_v1(
    *,
    provider_responses: list[dict[str, Any]] | None = None,
    provider_request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Build a candidate-only acquisition generation artifact."""
    chunks = build_acquisition_month_chunks_v1()
    generated = provider_responses is not None
    provider_records: list[dict[str, Any]] = []
    normalized_rows: list[dict[str, Any]] = []
    monthly_reconciliation: list[dict[str, Any]] = []
    classified_rows: list[dict[str, Any]] = []
    if generated:
        provider_records, normalized_rows = _provider_records_from_responses(provider_responses or [], chunks=chunks)
        classified_rows = classify_normalized_source_rows_v1(normalized_rows)
        monthly_reconciliation = build_monthly_reconciliation_v1(classified_rows, chunks=chunks)
    rth_count = sum(1 for row in classified_rows if row.get("session_classification") == RTH)
    extended_count = sum(1 for row in classified_rows if row.get("session_classification") == EXTENDED_HOURS)
    out_count = sum(1 for row in classified_rows if row.get("session_classification") == OUT_OF_CALENDAR_RANGE)
    unknown_count = sum(1 for row in classified_rows if row.get("session_classification") == UNKNOWN)
    failed_chunks = 0
    provider_raw_digest = semantic_digest(provider_records) if generated else None
    normalized_digest = normalized_source_rows_digest_v1(normalized_rows) if generated else None
    monthly_digest = monthly_reconciliation_digest_v1(monthly_reconciliation) if generated else None
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_CANDIDATE_V1,
        "candidate_status": ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW if generated else ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION,
        "created_offline": True,
        "provider_requests_made": False,
        "provider_response_injected": generated,
        "acquisition_generation_complete": generated and len(provider_records) == len(chunks) and failed_chunks == 0,
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
        "provider_request_mode": PROVIDER_REQUEST_MODE_FAKE_TRANSPORT if generated else None,
        "provider_request_timestamp_utc": provider_request_timestamp_utc,
        "provider_chunk_count": len(provider_records),
        "provider_failed_chunk_count": failed_chunks,
        "provider_raw_response_digest": provider_raw_digest,
        "provider_chunk_manifest_digest": chunk_manifest_digest_v1(chunks),
        "chunking_strategy": CHUNKING_STRATEGY_MONTHLY,
        "chunk_count_expected": len(chunks),
        "chunk_count_completed": len(provider_records),
        "failed_chunk_count": failed_chunks,
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


def _validate_january_2025_cross_check(candidate: dict[str, Any]) -> None:
    months = candidate.get("monthly_reconciliation")
    if not months:
        return
    january = next((item for item in months if item.get("month") == "2025-01"), None)
    if january is None:
        return
    _expect(january.get("normalized_source_rows"), 1277, "2025-01.normalized_source_rows")
    _expect(january.get("extended_hours_rows"), 757, "2025-01.extended_hours_rows")
    _expect(january.get("expected_rth_rows"), 520, "2025-01.expected_rth_rows")
    _expect(january.get("validated_rth_rows"), 520, "2025-01.validated_rth_rows")
    _expect(january.get("full_ordinary_sessions"), 20, "2025-01.full_ordinary_sessions")
    _expect(january.get("incomplete_ordinary_sessions"), 0, "2025-01.incomplete_ordinary_sessions")
    _expect(january.get("swing_rth_half_session_195m_bars"), 40, "2025-01.swing_rth_half_session_195m_bars")
    _expect(january.get("position_swing_rth_full_session_1d_bars"), 20, "2025-01.position_swing_rth_full_session_1d_bars")
    _expect(january.get("rth_reconciliation_status"), RTH_SOURCE_ROWS_RECONCILED, "2025-01.rth_reconciliation_status")


def validate_acquisition_generation_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate an acquisition generation candidate artifact."""
    if not isinstance(candidate, dict):
        raise AcquisitionGenerationError("acquisition generation candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_ACQUISITION_GENERATION_CANDIDATE_V1, "schema_version")
    if candidate.get("candidate_status") not in {
        ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW,
        ACQUISITION_GENERATION_REQUIRES_LIVE_PROVIDER_EXECUTION,
    }:
        raise AcquisitionGenerationError("candidate_status mismatch")
    if candidate.get("freeze_status") == ACQUISITION_GENERATION_FROZEN:
        raise AcquisitionGenerationError("freeze_status must not be ACQUISITION_GENERATION_FROZEN")
    _expect_true(candidate.get("created_offline"), "created_offline")
    _expect_false(candidate.get("provider_requests_made"), "provider_requests_made")
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
        "provider_requests_made": False,
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
