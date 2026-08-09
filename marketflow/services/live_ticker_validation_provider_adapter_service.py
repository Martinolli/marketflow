"""Sanitized Massive.com ticker validation provider adapter."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any, Callable, Mapping
from urllib.parse import quote

import httpx

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.historical_data.massive_transport import (
    CONNECT_TIMEOUT_SECONDS,
    MASSIVE_REST_HOST,
    MASSIVE_REST_SCHEME,
    MASSIVE_USER_AGENT,
    POOL_TIMEOUT_SECONDS,
    READ_TIMEOUT_SECONDS,
    WRITE_TIMEOUT_SECONDS,
    ProviderApiKey,
)


LIVE_TICKER_VALIDATION_GATE_ENV = "MARKETFLOW_ENABLE_LIVE_TICKER_VALIDATION"
MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE = "/v3/reference/tickers/{ticker}"
MASSIVE_TICKER_DETAILS_ENDPOINT_STABILITY = "CURRENT_V3_REFERENCE_TICKER_DETAILS"
PROVIDER_NAME = "Massive.com"
LIVE_PROVIDER_REQUEST = "LIVE_PROVIDER_REQUEST"
INJECTED_PROVIDER_RESPONSE = "INJECTED_PROVIDER_RESPONSE"
RAW_RESPONSE_SCHEMA_VERSION = "massive_ticker_details_sanitized_response_v1"
SELECTED_ENDPOINT_MODE = "Massive.com reference ticker details"


class LiveTickerValidationProviderAdapterError(ValueError):
    """Raised when ticker validation provider evidence cannot be collected safely."""


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _live_gate_enabled() -> bool:
    return os.environ.get(LIVE_TICKER_VALIDATION_GATE_ENV) == "1"


def _validate_ticker(value: str) -> str:
    if type(value) is not str or not value or len(value) > 32:
        raise LiveTickerValidationProviderAdapterError("ticker must be bounded non-empty text")
    safe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-"
    if not all(char in safe for char in value):
        raise LiveTickerValidationProviderAdapterError("ticker contains unsupported characters")
    return value.upper()


def _endpoint(ticker: str) -> str:
    return MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE.format(ticker=quote(_validate_ticker(ticker), safe="._-"))


def _public_headers() -> dict[str, str]:
    return {
        "Authorization": "<redacted>",
        "Accept": "application/json",
        "Accept-Encoding": "identity",
        "User-Agent": MASSIVE_USER_AGENT,
    }


def _private_headers(api_key: ProviderApiKey) -> dict[str, str]:
    return {
        "Authorization": api_key.authorization_header(),
        "Accept": "application/json",
        "Accept-Encoding": "identity",
        "User-Agent": MASSIVE_USER_AGENT,
    }


def build_massive_ticker_details_request_v1(
    *,
    ticker: str,
    api_key: str | None = None,
    request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Build sanitized Massive ticker-details request metadata without retaining secrets."""
    api_key_supplied = api_key is not None
    del api_key
    validated_ticker = _validate_ticker(ticker)
    endpoint = _endpoint(validated_ticker)
    url = f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{endpoint}"
    return {
        "provider_name": PROVIDER_NAME,
        "provider_endpoint": endpoint,
        "provider_endpoint_stability": MASSIVE_TICKER_DETAILS_ENDPOINT_STABILITY,
        "provider_endpoint_mode": SELECTED_ENDPOINT_MODE,
        "provider_query_identifier": validated_ticker,
        "provider_query_ticker": validated_ticker,
        "provider_request_timestamp_utc": request_timestamp_utc or _utc_now(),
        "provider_request_mode": LIVE_PROVIDER_REQUEST,
        "method": "GET",
        "url": url,
        "sanitized_url": url,
        "headers": _public_headers(),
        "query_parameters": [],
        "api_key_supplied": api_key_supplied,
        "api_key_stored": False,
        "api_key_printed": False,
    }


def _load_json_bytes(body: bytes) -> dict[str, Any]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LiveTickerValidationProviderAdapterError("ticker provider response must be UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise LiveTickerValidationProviderAdapterError("ticker provider response must be a JSON object")
    return _deterministic_json_value(payload)


def _payload_from_transport_result(result: Any) -> dict[str, Any]:
    if isinstance(result, bytes):
        return _load_json_bytes(result)
    if isinstance(result, Mapping):
        return _deterministic_json_value(dict(result))
    raise LiveTickerValidationProviderAdapterError("ticker provider transport returned unsupported payload")


def _deterministic_json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _deterministic_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_deterministic_json_value(item) for item in value]
    if isinstance(value, tuple):
        return [_deterministic_json_value(item) for item in value]
    if isinstance(value, float):
        return format(value, ".15g")
    return value


def _http_transport(request_metadata: Mapping[str, Any], *, api_key: ProviderApiKey) -> dict[str, Any]:
    if not _live_gate_enabled():
        raise LiveTickerValidationProviderAdapterError(
            "live ticker validation gate is required for live provider transport"
        )
    with httpx.Client(
        timeout=httpx.Timeout(
            connect=CONNECT_TIMEOUT_SECONDS,
            read=READ_TIMEOUT_SECONDS,
            write=WRITE_TIMEOUT_SECONDS,
            pool=POOL_TIMEOUT_SECONDS,
        ),
        follow_redirects=False,
        trust_env=False,
        verify=True,
    ) as client:
        response = client.request(str(request_metadata["method"]), str(request_metadata["url"]), headers=_private_headers(api_key))
    if response.status_code in {401, 403}:
        raise LiveTickerValidationProviderAdapterError("ticker provider authentication failed")
    if response.status_code != 200:
        raise LiveTickerValidationProviderAdapterError("ticker provider returned non-success status")
    content_type = response.headers.get("Content-Type")
    if content_type is not None and content_type.split(";", 1)[0].strip().lower() != "application/json":
        raise LiveTickerValidationProviderAdapterError("ticker provider response content-type mismatch")
    return _load_json_bytes(response.content)


def _result_object(payload: Mapping[str, Any]) -> dict[str, Any]:
    result = payload.get("results")
    if not isinstance(result, Mapping):
        raise LiveTickerValidationProviderAdapterError("ticker provider result must be an object")
    return _deterministic_json_value(dict(result))


def _text_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _bool_or_none(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def _sanitized_details(result: Mapping[str, Any]) -> dict[str, Any]:
    fields = {
        "ticker": _text_or_none(result.get("ticker")),
        "name": _text_or_none(result.get("name")),
        "market": _text_or_none(result.get("market")),
        "locale": _text_or_none(result.get("locale")),
        "primary_exchange": _text_or_none(result.get("primary_exchange")),
        "type": _text_or_none(result.get("type")),
        "active": _bool_or_none(result.get("active")),
        "currency_name": _text_or_none(result.get("currency_name")),
        "cik": _text_or_none(result.get("cik")),
        "composite_figi": _text_or_none(result.get("composite_figi")),
        "share_class_figi": _text_or_none(result.get("share_class_figi")),
        "last_updated_utc": _text_or_none(result.get("last_updated_utc")),
        "delisted_utc": _text_or_none(result.get("delisted_utc")),
    }
    return {key: value for key, value in fields.items() if value is not None}


def fetch_massive_ticker_details_v1(
    *,
    ticker: str,
    api_key: str,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Fetch ticker details and return sanitized evidence only."""
    key = ProviderApiKey(api_key)
    request = build_massive_ticker_details_request_v1(
        ticker=ticker,
        api_key=api_key,
        request_timestamp_utc=request_timestamp_utc,
    )
    payload = _payload_from_transport_result(
        transport(request) if transport is not None else _http_transport(request, api_key=key)
    )
    result = _result_object(payload)
    response_status = payload.get("status")
    sanitized = {
        "schema_version": RAW_RESPONSE_SCHEMA_VERSION,
        "provider_name": PROVIDER_NAME,
        "provider_endpoint": request["provider_endpoint"],
        "provider_endpoint_stability": MASSIVE_TICKER_DETAILS_ENDPOINT_STABILITY,
        "provider_endpoint_mode": SELECTED_ENDPOINT_MODE,
        "provider_request_mode": INJECTED_PROVIDER_RESPONSE if transport is not None else LIVE_PROVIDER_REQUEST,
        "provider_query_identifier": request["provider_query_identifier"],
        "provider_query_ticker": request["provider_query_ticker"],
        "provider_request_timestamp_utc": request["provider_request_timestamp_utc"],
        "provider_requests_made": True,
        "provider_response_injected": transport is not None,
        "provider_response_status": response_status if isinstance(response_status, str) else "UNKNOWN",
        "request": {key: value for key, value in request.items() if key not in {"url"}},
        "sanitized_response": _sanitized_details(result),
        "raw_response_stored": False,
        "raw_payload_committed": False,
        "api_key_stored_or_printed": False,
    }
    return sanitized | {"provider_response_digest": semantic_digest(sanitized)}
