"""Massive.com live split-event provider adapter."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any, Callable, Mapping
from urllib.parse import parse_qsl, quote, urlencode, urlparse

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


MASSIVE_SPLIT_EVENTS_ENDPOINT = "/stocks/v1/splits"
MASSIVE_SPLIT_EVENTS_ENDPOINT_STABILITY = "CURRENT_STOCKS_V1_SPLITS"
LIVE_PROVIDER_REQUEST = "LIVE_PROVIDER_REQUEST"
SPLIT_EVENT_LIMIT = 5000
SPLIT_EVENT_SORT = "execution_date.asc"
MAX_SPLIT_EVENT_PAGES = 10
PROVIDER_NAME = "Massive.com"
RAW_RESPONSE_SCHEMA_VERSION = "massive_split_events_raw_response_v1"
_FORBIDDEN_QUERY_KEYS = frozenset(
    {
        "apikey",
        "api_key",
        "token",
        "access_token",
        "authorization",
        "auth",
        "key",
        "user",
        "username",
        "account",
        "account_id",
    }
)
_CONTINUATION_ALLOWED_QUERY_KEYS = frozenset(
    {
        "cursor",
        "ticker",
        "execution_date.gte",
        "execution_date.lte",
        "sort",
        "limit",
    }
)


class SplitEventProviderAdapterError(ValueError):
    """Raised when live split-event provider evidence cannot be collected safely."""


def _validate_ticker(value: str) -> str:
    if type(value) is not str or not value or len(value) > 32:
        raise SplitEventProviderAdapterError("ticker must be bounded non-empty text")
    safe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-"
    if not all(char in safe for char in value):
        raise SplitEventProviderAdapterError("ticker contains unsupported characters")
    return value


def _validate_iso_date(value: str, field_name: str) -> str:
    if type(value) is not str:
        raise SplitEventProviderAdapterError(f"{field_name} must be an ISO date")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise SplitEventProviderAdapterError(f"{field_name} must be an ISO date") from exc


def _query_string(pairs: tuple[tuple[str, str], ...]) -> str:
    for key, value in pairs:
        if key.lower() in _FORBIDDEN_QUERY_KEYS:
            raise SplitEventProviderAdapterError("credential-like query parameter is prohibited")
        if any(char in value for char in ("\r", "\n", "\x00")):
            raise SplitEventProviderAdapterError("query parameter contains prohibited control characters")
    return urlencode(pairs, quote_via=quote, safe="._-")


def _request_query(*, ticker: str, start_date: str, end_date: str, cursor: str | None = None) -> tuple[tuple[str, str], ...]:
    query = (
        ("ticker", _validate_ticker(ticker)),
        ("execution_date.gte", _validate_iso_date(start_date, "start_date")),
        ("execution_date.lte", _validate_iso_date(end_date, "end_date")),
        ("sort", SPLIT_EVENT_SORT),
        ("limit", str(SPLIT_EVENT_LIMIT)),
    )
    if cursor is None:
        return query
    return (*query, ("cursor", cursor))


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


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_massive_split_events_request_v1(
    *,
    ticker: str,
    start_date: str,
    end_date: str,
    api_key: str | None = None,
    request_timestamp_utc: str | None = None,
    cursor: str | None = None,
) -> dict[str, Any]:
    """Build sanitized Massive split-events request metadata."""
    del api_key
    query = _request_query(ticker=ticker, start_date=start_date, end_date=end_date, cursor=cursor)
    query_text = _query_string(query)
    endpoint = MASSIVE_SPLIT_EVENTS_ENDPOINT
    url = f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{endpoint}?{query_text}"
    return {
        "provider_name": PROVIDER_NAME,
        "provider_endpoint": endpoint,
        "provider_endpoint_stability": MASSIVE_SPLIT_EVENTS_ENDPOINT_STABILITY,
        "provider_query_identifier": ticker,
        "provider_query_ticker": ticker,
        "provider_query_start": start_date,
        "provider_query_end": end_date,
        "provider_request_timestamp_utc": request_timestamp_utc or _utc_now(),
        "provider_request_mode": LIVE_PROVIDER_REQUEST,
        "method": "GET",
        "url": url,
        "sanitized_url": url,
        "headers": _public_headers(),
        "query_parameters": list(query),
    }


def _load_json_bytes(body: bytes) -> dict[str, Any]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SplitEventProviderAdapterError("split provider response must be UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise SplitEventProviderAdapterError("split provider response must be a JSON object")
    return payload


def _payload_from_transport_result(result: Any) -> dict[str, Any]:
    if isinstance(result, bytes):
        return _load_json_bytes(result)
    if isinstance(result, Mapping):
        return dict(result)
    raise SplitEventProviderAdapterError("split provider transport returned unsupported payload")


def _validate_next_url(raw_next_url: Any, *, ticker: str, start_date: str, end_date: str) -> tuple[str, str]:
    if type(raw_next_url) is not str or not raw_next_url:
        raise SplitEventProviderAdapterError("next_url must be non-empty text")
    parsed = urlparse(raw_next_url)
    if parsed.scheme != MASSIVE_REST_SCHEME or parsed.hostname != MASSIVE_REST_HOST:
        raise SplitEventProviderAdapterError("next_url host or scheme mismatch")
    if parsed.username or parsed.password or parsed.fragment or parsed.path != MASSIVE_SPLIT_EVENTS_ENDPOINT:
        raise SplitEventProviderAdapterError("next_url structure mismatch")
    if parsed.port not in (None, 443):
        raise SplitEventProviderAdapterError("next_url port mismatch")
    pairs = tuple((key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=False))
    seen: set[str] = set()
    params: dict[str, str] = {}
    for key, value in pairs:
        lower = key.lower()
        if lower in _FORBIDDEN_QUERY_KEYS:
            raise SplitEventProviderAdapterError("next_url contains credential-like parameter")
        if key not in _CONTINUATION_ALLOWED_QUERY_KEYS:
            raise SplitEventProviderAdapterError("next_url contains unsupported parameter")
        if key in seen:
            raise SplitEventProviderAdapterError("next_url contains duplicate parameter")
        seen.add(key)
        params[key] = value
    cursor = params.get("cursor")
    if not cursor:
        raise SplitEventProviderAdapterError("next_url must include cursor")
    if params.get("ticker", ticker) != ticker:
        raise SplitEventProviderAdapterError("next_url ticker mismatch")
    if params.get("execution_date.gte", start_date) != start_date:
        raise SplitEventProviderAdapterError("next_url start-date mismatch")
    if params.get("execution_date.lte", end_date) != end_date:
        raise SplitEventProviderAdapterError("next_url end-date mismatch")
    if params.get("sort", SPLIT_EVENT_SORT) != SPLIT_EVENT_SORT:
        raise SplitEventProviderAdapterError("next_url sort mismatch")
    if params.get("limit", str(SPLIT_EVENT_LIMIT)) != str(SPLIT_EVENT_LIMIT):
        raise SplitEventProviderAdapterError("next_url limit mismatch")
    sanitized_query = _request_query(ticker=ticker, start_date=start_date, end_date=end_date, cursor="cursor-" + semantic_digest({"cursor": cursor})[:24])
    sanitized_url = f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{MASSIVE_SPLIT_EVENTS_ENDPOINT}?{_query_string(sanitized_query)}"
    return cursor, sanitized_url


def _http_transport(request_metadata: Mapping[str, Any], *, api_key: ProviderApiKey) -> dict[str, Any]:
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
        raise SplitEventProviderAdapterError("split provider authentication failed")
    if response.status_code != 200:
        raise SplitEventProviderAdapterError("split provider returned non-success status")
    content_type = response.headers.get("Content-Type")
    if content_type is not None and content_type.split(";", 1)[0].strip().lower() != "application/json":
        raise SplitEventProviderAdapterError("split provider response content-type mismatch")
    return _load_json_bytes(response.content)


def fetch_massive_split_events_v1(
    *,
    ticker: str,
    start_date: str,
    end_date: str,
    api_key: str,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    request_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Fetch live Massive split events and return sanitized deterministic raw evidence."""
    key = ProviderApiKey(api_key)
    request_timestamp = request_timestamp_utc or _utc_now()
    pages: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    cursor: str | None = None
    sanitized_continuation_url: str | None = None
    response_status = "UNKNOWN"
    for page_index in range(1, MAX_SPLIT_EVENT_PAGES + 1):
        request = build_massive_split_events_request_v1(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            request_timestamp_utc=request_timestamp,
            cursor=cursor,
        )
        if sanitized_continuation_url is not None:
            request["sanitized_url"] = sanitized_continuation_url
        payload = _payload_from_transport_result(transport(request) if transport is not None else _http_transport(request, api_key=key))
        status = payload.get("status")
        response_status = status if isinstance(status, str) else "UNKNOWN"
        page_results = payload.get("results")
        if not isinstance(page_results, list):
            raise SplitEventProviderAdapterError("split provider results must be an array")
        if not all(isinstance(item, dict) for item in page_results):
            raise SplitEventProviderAdapterError("split provider result rows must be objects")
        results.extend(dict(item) for item in page_results)
        pages.append(
            {
                "page_index": page_index,
                "sanitized_url": request["sanitized_url"],
                "provider_response_status": response_status,
                "result_count": len(page_results),
                "payload": payload,
            }
        )
        next_url = payload.get("next_url")
        if next_url is None:
            break
        cursor, sanitized_continuation_url = _validate_next_url(next_url, ticker=ticker, start_date=start_date, end_date=end_date)
    else:
        raise SplitEventProviderAdapterError("split provider pagination exceeded safe page limit")
    raw_response = {
        "schema_version": RAW_RESPONSE_SCHEMA_VERSION,
        "provider_name": PROVIDER_NAME,
        "provider_endpoint": MASSIVE_SPLIT_EVENTS_ENDPOINT,
        "provider_endpoint_stability": MASSIVE_SPLIT_EVENTS_ENDPOINT_STABILITY,
        "provider_request_mode": LIVE_PROVIDER_REQUEST,
        "provider_query_identifier": ticker,
        "provider_query_ticker": ticker,
        "provider_query_start": start_date,
        "provider_query_end": end_date,
        "provider_request_timestamp_utc": request_timestamp,
        "provider_requests_made": True,
        "provider_response_injected": False,
        "provider_response_page_count": len(pages),
        "provider_raw_response_row_count": len(results),
        "provider_response_status": response_status,
        "request_metadata": {
            key: pages[0]["payload"].get(key)
            for key in ()
        },
        "request": {
            key: value
            for key, value in build_massive_split_events_request_v1(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                request_timestamp_utc=request_timestamp,
            ).items()
            if key not in {"url"}
        },
        "pages": pages,
        "results": results,
    }
    return raw_response | {"provider_raw_response_digest": semantic_digest(raw_response)}
