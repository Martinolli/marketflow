"""Massive.com live custom-bars adapter for acquisition smoke checks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes


PROVIDER_NAME = "Massive.com"
MASSIVE_REST_SCHEME = "https"
MASSIVE_REST_HOST = "api.massive.com"
MASSIVE_CUSTOM_BARS_ENDPOINT = "/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}"
MASSIVE_CUSTOM_BARS_ENDPOINT_STABILITY = "CURRENT_STOCKS_V2_AGGS_RANGE"
MASSIVE_USER_AGENT = "MarketFlow-Massive-Acquisition-Smoke/1"
LIVE_PROVIDER_REQUEST = "LIVE_PROVIDER_REQUEST"
FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION = "FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION"
ACQUISITION_RAW_RESPONSE_SCHEMA_VERSION = "massive_custom_bars_monthly_raw_response_v1"
ACQUISITION_SMOKE_LIMIT = 50000
MAXIMUM_RESPONSE_BODY_BYTES = 67_108_864


class AcquisitionProviderAdapterError(ValueError):
    """Raised when custom-bars provider evidence cannot be collected safely."""


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _validate_api_key(value: str) -> str:
    if type(value) is not str or not value.strip() or value != value.strip():
        raise AcquisitionProviderAdapterError("provider API key must be non-empty without surrounding whitespace")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise AcquisitionProviderAdapterError("provider API key contains prohibited control characters")
    return value


def _validate_ticker(value: str) -> str:
    if type(value) is not str or not value or len(value) > 32:
        raise AcquisitionProviderAdapterError("ticker must be bounded non-empty text")
    safe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-"
    if not all(char in safe for char in value):
        raise AcquisitionProviderAdapterError("ticker contains unsupported characters")
    return value.upper()


def _validate_iso_date(value: str, field_name: str) -> str:
    if type(value) is not str:
        raise AcquisitionProviderAdapterError(f"{field_name} must be an ISO date")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise AcquisitionProviderAdapterError(f"{field_name} must be an ISO date") from exc


def _validate_fixed_contract(*, multiplier: int, timespan: str, adjusted: bool, sort: str, limit: int) -> None:
    if multiplier != 15:
        raise AcquisitionProviderAdapterError("custom-bars multiplier must remain fixed at 15")
    if timespan != "minute":
        raise AcquisitionProviderAdapterError("custom-bars timespan must remain fixed at minute")
    if adjusted is not True:
        raise AcquisitionProviderAdapterError("custom-bars adjusted flag must remain true")
    if sort != "asc":
        raise AcquisitionProviderAdapterError("custom-bars sort must remain asc")
    if limit != ACQUISITION_SMOKE_LIMIT:
        raise AcquisitionProviderAdapterError("custom-bars limit must remain fixed at 50000")


def _query_string(pairs: tuple[tuple[str, str], ...]) -> str:
    forbidden = {"apikey", "api_key", "token", "access_token", "authorization", "auth", "key"}
    for key, value in pairs:
        if key.lower() in forbidden:
            raise AcquisitionProviderAdapterError("credential-like query parameter is prohibited")
        if any(char in value for char in ("\r", "\n", "\x00")):
            raise AcquisitionProviderAdapterError("query parameter contains prohibited control characters")
    return urlencode(pairs, quote_via=quote, safe="._-")


def _public_headers() -> dict[str, str]:
    return {
        "Authorization": "<redacted>",
        "Accept": "application/json",
        "Accept-Encoding": "identity",
        "User-Agent": MASSIVE_USER_AGENT,
    }


def _private_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Accept-Encoding": "identity",
        "User-Agent": MASSIVE_USER_AGENT,
    }


def build_massive_custom_bars_live_request_v1(
    *,
    ticker: str,
    start_date: str,
    end_date: str,
    api_key: str | None = None,
    multiplier: int = 15,
    timespan: str = "minute",
    adjusted: bool = True,
    sort: str = "asc",
    limit: int = ACQUISITION_SMOKE_LIMIT,
    request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Build sanitized live custom-bars request metadata without storing credentials."""
    del api_key
    ticker_text = _validate_ticker(ticker)
    start = _validate_iso_date(start_date, "start_date")
    end = _validate_iso_date(end_date, "end_date")
    if start > end:
        raise AcquisitionProviderAdapterError("start_date must be <= end_date")
    _validate_fixed_contract(multiplier=multiplier, timespan=timespan, adjusted=adjusted, sort=sort, limit=int(limit))
    path = (
        "/v2/aggs/ticker/"
        f"{quote(ticker_text, safe='._-')}/range/{multiplier}/{timespan}/{start}/{end}"
    )
    query = (("adjusted", "true"), ("sort", sort), ("limit", str(int(limit))))
    url = f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{path}?{_query_string(query)}"
    request = {
        "provider_name": PROVIDER_NAME,
        "provider_endpoint": MASSIVE_CUSTOM_BARS_ENDPOINT,
        "provider_endpoint_path": path,
        "provider_endpoint_stability": MASSIVE_CUSTOM_BARS_ENDPOINT_STABILITY,
        "provider_query_identifier": ticker_text,
        "provider_query_ticker": ticker_text,
        "provider_query_start": start,
        "provider_query_end": end,
        "provider_request_timestamp_utc": request_timestamp_utc or _utc_now(),
        "provider_multiplier": int(multiplier),
        "provider_timespan": timespan,
        "provider_adjusted": adjusted,
        "provider_sort": sort,
        "provider_limit": int(limit),
        "provider_request_mode": LIVE_PROVIDER_REQUEST,
        "method": "GET",
        "url": url,
        "sanitized_url": url,
        "headers": _public_headers(),
        "query_parameters": list(query),
        "api_key_stored": False,
    }
    request["request_semantic_digest"] = semantic_digest({key: value for key, value in request.items() if key != "request_semantic_digest"})
    return request


def _payload_to_bytes(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, Mapping):
        return canonical_json_bytes(dict(payload))
    raise AcquisitionProviderAdapterError("custom-bars provider transport returned unsupported payload")


def _decode_json(body: bytes) -> dict[str, Any]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AcquisitionProviderAdapterError("custom-bars provider response must be UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise AcquisitionProviderAdapterError("custom-bars provider response must be a JSON object")
    return payload


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
            raise AcquisitionProviderAdapterError("custom-bars provider authentication failed") from None
        raise AcquisitionProviderAdapterError("custom-bars provider returned non-success status") from None
    except URLError as exc:
        raise AcquisitionProviderAdapterError("custom-bars provider transport failed") from exc
    if status != 200:
        raise AcquisitionProviderAdapterError("custom-bars provider returned non-success status")
    if len(body) > MAXIMUM_RESPONSE_BODY_BYTES:
        raise AcquisitionProviderAdapterError("custom-bars provider response body limit exceeded")
    if content_type is not None and content_type.split(";", 1)[0].strip().lower() != "application/json":
        raise AcquisitionProviderAdapterError("custom-bars provider response content-type mismatch")
    return body


def fetch_massive_custom_bars_live_v1(
    *,
    ticker: str,
    start_date: str,
    end_date: str,
    api_key: str,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Fetch one custom-bars month and return sanitized raw evidence plus private body bytes."""
    key = _validate_api_key(api_key)
    request = build_massive_custom_bars_live_request_v1(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        api_key=key,
        request_timestamp_utc=request_timestamp_utc,
    )
    body = _payload_to_bytes(transport(request) if transport is not None else _http_transport(request, api_key=key))
    payload = _decode_json(body)
    rows = payload.get("results")
    if rows is None:
        rows = []
    if not isinstance(rows, list) or not all(isinstance(item, dict) for item in rows):
        raise AcquisitionProviderAdapterError("custom-bars provider results must be an array of objects")
    response_status = payload.get("status")
    raw_response = {
        "schema_version": ACQUISITION_RAW_RESPONSE_SCHEMA_VERSION,
        "provider_name": PROVIDER_NAME,
        "provider_endpoint": MASSIVE_CUSTOM_BARS_ENDPOINT,
        "provider_endpoint_path": request["provider_endpoint_path"],
        "provider_endpoint_stability": MASSIVE_CUSTOM_BARS_ENDPOINT_STABILITY,
        "provider_request_mode": LIVE_PROVIDER_REQUEST if transport is None else FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION,
        "provider_query_identifier": request["provider_query_identifier"],
        "provider_query_ticker": request["provider_query_ticker"],
        "provider_query_start": request["provider_query_start"],
        "provider_query_end": request["provider_query_end"],
        "provider_request_timestamp_utc": request["provider_request_timestamp_utc"],
        "provider_requests_made": transport is None,
        "provider_response_injected": transport is not None,
        "provider_response_status": response_status if isinstance(response_status, str) else "UNKNOWN",
        "provider_raw_response_row_count": len(rows),
        "provider_raw_body_sha256": sha256_bytes(body),
        "request": {key: value for key, value in request.items() if key != "url"},
    }
    raw_response["provider_raw_response_digest"] = semantic_digest(raw_response)
    return raw_response | {"provider_response_body": body}
