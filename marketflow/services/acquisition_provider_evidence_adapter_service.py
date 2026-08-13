"""Sanitized Massive.com daily-bars adapter for acquisition evidence execution."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
import json
import os
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes


PROVIDER_NAME = "Massive.com"
MASSIVE_REST_SCHEME = "https"
MASSIVE_REST_HOST = "api.massive.com"
MASSIVE_DAILY_BARS_ENDPOINT = "/v2/aggs/ticker/{stocksTicker}/range/1/day/{from}/{to}"
MASSIVE_DAILY_BARS_ENDPOINT_STABILITY = "CURRENT_STOCKS_V2_AGGS_RANGE_DAILY"
MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE = (
    "MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE"
)
LIVE_PROVIDER_REQUEST = "LIVE_PROVIDER_REQUEST"
FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION = "FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION"
DAILY_BARS_LIMIT = 50_000
MAXIMUM_RESPONSE_BODY_BYTES = 67_108_864
USER_AGENT = "MarketFlow-Acquisition-Provider-Evidence/1"


class AcquisitionProviderEvidenceAdapterError(ValueError):
    """Raised when daily-bars evidence cannot be collected safely."""


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _validate_api_key(value: str) -> str:
    if type(value) is not str or not value.strip() or value != value.strip():
        raise AcquisitionProviderEvidenceAdapterError(
            "provider API key must be non-empty without surrounding whitespace"
        )
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise AcquisitionProviderEvidenceAdapterError("provider API key contains prohibited control characters")
    return value


def _validate_ticker(value: str) -> str:
    if type(value) is not str or not value or len(value) > 32:
        raise AcquisitionProviderEvidenceAdapterError("ticker must be bounded non-empty text")
    if not all(char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-" for char in value):
        raise AcquisitionProviderEvidenceAdapterError("ticker contains unsupported characters")
    return value.upper()


def _validate_iso_date(value: str, field_name: str) -> str:
    if type(value) is not str:
        raise AcquisitionProviderEvidenceAdapterError(f"{field_name} must be an ISO date")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise AcquisitionProviderEvidenceAdapterError(f"{field_name} must be an ISO date") from exc


def _public_headers() -> dict[str, str]:
    return {
        "Authorization": "<redacted>",
        "Accept": "application/json",
        "Accept-Encoding": "identity",
        "User-Agent": USER_AGENT,
    }


def _private_headers(api_key: str) -> dict[str, str]:
    return _public_headers() | {"Authorization": f"Bearer {api_key}"}


def build_massive_daily_bars_request_v1(
    *,
    ticker: str,
    start_date: str,
    end_date: str,
    request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Build credential-free request metadata for the approved daily-bars endpoint."""
    ticker_text = _validate_ticker(ticker)
    start = _validate_iso_date(start_date, "start_date")
    end = _validate_iso_date(end_date, "end_date")
    if start > end:
        raise AcquisitionProviderEvidenceAdapterError("start_date must be <= end_date")
    path = f"/v2/aggs/ticker/{quote(ticker_text, safe='._-')}/range/1/day/{start}/{end}"
    query = (("adjusted", "true"), ("sort", "asc"), ("limit", str(DAILY_BARS_LIMIT)))
    url = f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{path}?{urlencode(query)}"
    request = {
        "provider_name": PROVIDER_NAME,
        "provider_endpoint": MASSIVE_DAILY_BARS_ENDPOINT,
        "provider_endpoint_path": path,
        "provider_endpoint_stability": MASSIVE_DAILY_BARS_ENDPOINT_STABILITY,
        "provider_query_ticker": ticker_text,
        "provider_query_start": start,
        "provider_query_end": end,
        "provider_request_timestamp_utc": request_timestamp_utc or _utc_now(),
        "provider_multiplier": 1,
        "provider_timespan": "day",
        "provider_adjusted": True,
        "provider_sort": "asc",
        "provider_limit": DAILY_BARS_LIMIT,
        "method": "GET",
        "url": url,
        "sanitized_url": url,
        "headers": _public_headers(),
        "query_parameters": list(query),
        "api_key_stored": False,
    }
    request["request_semantic_digest"] = semantic_digest(
        {key: value for key, value in request.items() if key != "request_semantic_digest"}
    )
    return request


def _payload_to_bytes(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, Mapping):
        return canonical_json_bytes(dict(payload))
    raise AcquisitionProviderEvidenceAdapterError("daily-bars transport returned unsupported payload")


def _http_transport(request_metadata: Mapping[str, Any], *, api_key: str) -> bytes:
    request = Request(
        str(request_metadata["url"]),
        headers=_private_headers(api_key),
        method=str(request_metadata["method"]),
    )
    try:
        with urlopen(request, timeout=40) as response:
            status = int(response.status)
            content_type = response.headers.get("Content-Type")
            body = response.read(MAXIMUM_RESPONSE_BODY_BYTES + 1)
    except HTTPError as exc:
        if exc.code in {401, 403}:
            raise AcquisitionProviderEvidenceAdapterError("daily-bars provider authentication failed") from None
        raise AcquisitionProviderEvidenceAdapterError("daily-bars provider returned non-success status") from None
    except URLError as exc:
        raise AcquisitionProviderEvidenceAdapterError("daily-bars provider transport failed") from exc
    if status != 200:
        raise AcquisitionProviderEvidenceAdapterError("daily-bars provider returned non-success status")
    if len(body) > MAXIMUM_RESPONSE_BODY_BYTES:
        raise AcquisitionProviderEvidenceAdapterError("daily-bars provider response body limit exceeded")
    if content_type is not None and content_type.split(";", 1)[0].strip().lower() != "application/json":
        raise AcquisitionProviderEvidenceAdapterError("daily-bars provider response content-type mismatch")
    return body


def _deterministic_number(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal, str)):
        raise AcquisitionProviderEvidenceAdapterError(f"provider {field_name} must be numeric")
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise AcquisitionProviderEvidenceAdapterError(f"provider {field_name} must be numeric") from exc
    if not number.is_finite():
        raise AcquisitionProviderEvidenceAdapterError(f"provider {field_name} must be finite")
    normalized = format(number.normalize(), "f")
    return "0" if normalized in {"-0", ""} else normalized


def _sanitize_bar(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    return {
        "bar_index": index,
        "timestamp": _deterministic_number(row.get("t"), "timestamp"),
        "open": _deterministic_number(row.get("o"), "open"),
        "high": _deterministic_number(row.get("h"), "high"),
        "low": _deterministic_number(row.get("l"), "low"),
        "close": _deterministic_number(row.get("c"), "close"),
        "volume": _deterministic_number(row.get("v"), "volume"),
        "transaction_count": _deterministic_number(row.get("n"), "transaction_count"),
        "volume_weighted_average_price": _deterministic_number(row.get("vw"), "vw"),
    }


def fetch_massive_daily_bars_evidence_v1(
    *,
    ticker: str,
    start_date: str,
    end_date: str,
    api_key: str,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Fetch daily bars and return only sanitized evidence and digests."""
    key = _validate_api_key(api_key)
    if transport is None and os.environ.get(MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE) != "1":
        raise AcquisitionProviderEvidenceAdapterError("live acquisition provider evidence gate is not enabled")
    request = build_massive_daily_bars_request_v1(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        request_timestamp_utc=request_timestamp_utc,
    )
    transport_result = transport(request) if transport is not None else _http_transport(request, api_key=key)
    body: bytes | None
    if isinstance(transport_result, Mapping):
        payload = dict(transport_result)
        body = None
    else:
        body = _payload_to_bytes(transport_result)
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AcquisitionProviderEvidenceAdapterError("daily-bars response must be UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise AcquisitionProviderEvidenceAdapterError("daily-bars response must be a JSON object")
    raw_rows = payload.get("results") or []
    if not isinstance(raw_rows, list) or not all(isinstance(row, Mapping) for row in raw_rows):
        raise AcquisitionProviderEvidenceAdapterError("daily-bars results must be an array of objects")
    sanitized_rows = [_sanitize_bar(row, index) for index, row in enumerate(raw_rows)]
    sanitized_request = {key: value for key, value in request.items() if key != "url"}
    result = {
        "provider_name": PROVIDER_NAME,
        "provider_endpoint": MASSIVE_DAILY_BARS_ENDPOINT,
        "provider_endpoint_path": request["provider_endpoint_path"],
        "provider_endpoint_stability": MASSIVE_DAILY_BARS_ENDPOINT_STABILITY,
        "provider_request_mode": (
            LIVE_PROVIDER_REQUEST if transport is None else FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION
        ),
        "provider_response_status": payload.get("status") if isinstance(payload.get("status"), str) else "UNKNOWN",
        "provider_request_metadata": sanitized_request,
        "provider_raw_body_sha256": (
            sha256_bytes(body)
            if body is not None
            else semantic_digest(
                {
                    "provider_response_status": payload.get("status"),
                    "sanitized_rows": sanitized_rows,
                }
            )
        ),
        "provider_raw_response_row_count": len(raw_rows),
        "sanitized_rows": sanitized_rows,
        "raw_response_stored": False,
        "raw_payload_exposed": False,
        "api_key_stored_or_printed": False,
    }
    result["provider_response_digest"] = semantic_digest(
        {key: value for key, value in result.items() if key != "provider_response_digest"}
    )
    return result
