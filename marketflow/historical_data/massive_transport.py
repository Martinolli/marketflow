"""Massive.com REST transport boundary for MarketFlow monthly acquisition."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Mapping

import httpx

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.historical_data.fake_transport import (
    OUTCOME_CONNECTION_RESET,
    OUTCOME_HTTP_RESPONSE,
    OUTCOME_HTTP_STATUS,
    OUTCOME_NO_RESPONSE,
    OUTCOME_TRANSPORT_TIMEOUT,
    FakeTransportRequest,
    ScriptedOutcome,
)
from marketflow.historical_data.monthly_acquisition import MonthChunkRequest


PROVIDER_BUSINESS_IDENTITY = "MASSIVE.COM"
MASSIVE_REST_HOST = "api.massive.com"
MASSIVE_REST_SCHEME = "https"
MASSIVE_CUSTOM_BARS_PATH_TEMPLATE = "/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
MASSIVE_USER_AGENT = "MarketFlow-Massive-Rest-Transport/1"

MASSIVE_MULTIPLIER = 15
MASSIVE_TIMESPAN = "minute"
MASSIVE_ADJUSTED = True
MASSIVE_SORT = "asc"
MASSIVE_LIMIT = 50000

CONNECT_TIMEOUT_SECONDS = 10
READ_TIMEOUT_SECONDS = 30
WRITE_TIMEOUT_SECONDS = 10
POOL_TIMEOUT_SECONDS = 10
MAXIMUM_RESPONSE_BODY_BYTES = 67_108_864

CONTENT_TYPE = "Content-Type"
CONTENT_LENGTH = "Content-Length"
CONTENT_ENCODING = "Content-Encoding"
RETRY_AFTER = "Retry-After"

HTTP_REDIRECT_REJECTED = "HTTP_REDIRECT_REJECTED"
TLS_VALIDATION_FAILURE = "TLS_VALIDATION_FAILURE"
INVALID_REQUEST = "INVALID_REQUEST"
RESPONSE_BODY_LIMIT_EXCEEDED = "RESPONSE_BODY_LIMIT_EXCEEDED"
RESPONSE_SCHEMA_INVALID = "RESPONSE_SCHEMA_INVALID"
UNSUPPORTED_CONTENT_ENCODING = "UNSUPPORTED_CONTENT_ENCODING"
AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"
AUTHORIZATION_FAILURE = "AUTHORIZATION_FAILURE"
HTTP_STATUS_NON_SUCCESS = "HTTP_STATUS_NON_SUCCESS"

_ALLOWED_CONTINUATION_QUERY_KEYS = frozenset({"cursor", "adjusted", "sort", "limit"})
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
_RETAINED_RESPONSE_HEADERS = (CONTENT_TYPE, CONTENT_LENGTH, CONTENT_ENCODING, RETRY_AFTER, "X-Request-ID", "X-Correlation-ID")
_AUTH_RESPONSE_FAILURES = frozenset({AUTHENTICATION_FAILURE, AUTHORIZATION_FAILURE})


class MassiveTransportError(ValueError):
    """Raised when the Massive REST transport boundary is configured unsafely."""


class ProviderApiKey:
    """Narrow secret wrapper; public representations are always redacted."""

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        if type(value) is not str or not value.strip() or value != value.strip():
            raise MassiveTransportError("provider API key must be non-empty without surrounding whitespace")
        if any(ord(char) < 32 or ord(char) == 127 for char in value):
            raise MassiveTransportError("provider API key contains prohibited control characters")
        object.__setattr__(self, "_value", value)

    def __repr__(self) -> str:
        return "ProviderApiKey(<redacted>)"

    def __str__(self) -> str:
        return "<redacted>"

    def authorization_header(self) -> str:
        return f"Bearer {self._value}"


@dataclass(frozen=True, slots=True)
class SanitizedContinuation:
    sanitized_continuation_identity: str
    cursor_digest: str
    query_params: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True, repr=False)
class MassivePreparedRequest:
    method: str
    url: str
    headers: Mapping[str, str] = field(compare=False)
    sanitized_url: str
    logical_page_request_id: str
    page_ordinal: int
    sanitized_continuation_identity: str | None

    def __repr__(self) -> str:
        safe_headers = {key: ("<redacted>" if key.lower() == "authorization" else value) for key, value in self.headers.items()}
        return (
            "MassivePreparedRequest("
            f"method={self.method!r}, url={self.sanitized_url!r}, headers={safe_headers!r}, "
            f"logical_page_request_id={self.logical_page_request_id!r}, page_ordinal={self.page_ordinal!r}, "
            f"sanitized_continuation_identity={self.sanitized_continuation_identity!r})"
        )


def _quote_path_segment(value: str, field_name: str) -> str:
    if type(value) is not str or not value:
        raise MassiveTransportError(f"{field_name} must be non-empty text")
    if any(char in value for char in ("/", "\\", "\x00", "?", "#", "%")):
        raise MassiveTransportError(f"{field_name} contains unsupported path characters")
    safe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-"
    if not all(char in safe for char in value):
        raise MassiveTransportError(f"{field_name} contains unsupported path characters")
    return value


def _request_query(month_request: MonthChunkRequest, cursor: str | None = None) -> tuple[tuple[str, str], ...]:
    pairs = (
        ("adjusted", str(month_request.adjusted).lower()),
        ("sort", month_request.sort),
        ("limit", str(month_request.limit)),
    )
    if cursor is None:
        return pairs
    return (*pairs, ("cursor", cursor))


def _query_string(pairs: tuple[tuple[str, str], ...]) -> str:
    safe_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._~-"
    for key, value in pairs:
        if key.lower() in _FORBIDDEN_QUERY_KEYS:
            raise MassiveTransportError("credential-like query parameter is prohibited")
        if any(char in value for char in ("\r", "\n", "\x00")):
            raise MassiveTransportError("query parameter contains prohibited control characters")
    encoded: list[str] = []
    for key, value in pairs:
        if not all(char in safe_chars for char in key):
            raise MassiveTransportError("query key contains unsupported characters")
        quoted = "".join(char if char in safe_chars else f"%{ord(char):02X}" for char in value)
        encoded.append(f"{key}={quoted}")
    return "&".join(encoded)


def _custom_bars_path(month_request: MonthChunkRequest) -> str:
    _validate_fixed_month_request_contract(month_request)
    ticker = _quote_path_segment(month_request.canonical_ticker, "canonical_ticker")
    return MASSIVE_CUSTOM_BARS_PATH_TEMPLATE.format(
        ticker=ticker,
        multiplier=month_request.multiplier,
        timespan=month_request.timespan,
        from_date=month_request.effective_start_date,
        to_date=month_request.effective_end_date,
    )


def _validate_fixed_month_request_contract(month_request: MonthChunkRequest) -> None:
    if month_request.multiplier != MASSIVE_MULTIPLIER:
        raise MassiveTransportError("month request multiplier must remain fixed at 15")
    if month_request.timespan != MASSIVE_TIMESPAN:
        raise MassiveTransportError("month request timespan must remain fixed at minute")
    if month_request.adjusted is not MASSIVE_ADJUSTED:
        raise MassiveTransportError("month request adjusted flag must remain true")
    if month_request.sort != MASSIVE_SORT:
        raise MassiveTransportError("month request sort must remain asc")
    if month_request.limit != MASSIVE_LIMIT:
        raise MassiveTransportError("month request limit must remain fixed at 50000")


def _headers(api_key: ProviderApiKey) -> dict[str, str]:
    return {
        "Authorization": api_key.authorization_header(),
        "Accept": "application/json",
        "Accept-Encoding": "identity",
        "User-Agent": MASSIVE_USER_AGENT,
    }


def _public_headers() -> dict[str, str]:
    return {
        "Authorization": "<redacted>",
        "Accept": "application/json",
        "Accept-Encoding": "identity",
        "User-Agent": MASSIVE_USER_AGENT,
    }


def _sanitize_headers(headers: httpx.Headers) -> dict[str, str]:
    retained: dict[str, str] = {}
    for key in _RETAINED_RESPONSE_HEADERS:
        values = headers.get_list(key)
        if len(values) > 1:
            retained[key] = "DUPLICATE_HEADER_REJECTED"
        elif values:
            value = values[0]
            if len(value) <= 256 and not any(char in value for char in ("\r", "\n", "\x00")):
                retained[key] = value
    return retained


def _content_type_is_json(value: str | None) -> bool:
    if value is None:
        return False
    parts = [part.strip() for part in value.split(";")]
    if not parts or parts[0].lower() != "application/json":
        return False
    for parameter in parts[1:]:
        if not parameter:
            continue
        key, separator, val = parameter.partition("=")
        if separator != "=" or key.strip().lower() != "charset":
            return False
        if val.strip().strip('"').lower() not in {"utf-8", "utf8"}:
            return False
    return True


def _failure_category_for_status(status_code: int) -> str:
    if status_code in {408, 429, 500, 502, 503, 504}:
        return f"HTTP_{status_code}"
    if status_code == 401:
        return AUTHENTICATION_FAILURE
    if status_code == 403:
        return AUTHORIZATION_FAILURE
    if 300 <= status_code <= 399:
        return HTTP_REDIRECT_REJECTED
    if status_code >= 400:
        return HTTP_STATUS_NON_SUCCESS
    return RESPONSE_SCHEMA_INVALID


def _is_tls_validation_error(exc: BaseException) -> bool:
    current: BaseException | None = exc
    while current is not None:
        text = f"{type(current).__name__} {current}".lower()
        if any(marker in text for marker in ("ssl", "tls", "certificate", "cert_verify", "cert verify")):
            return True
        current = current.__cause__
    return False


def _outcome_status_for_failure(category: str) -> str:
    if category == "TRANSPORT_TIMEOUT":
        return OUTCOME_TRANSPORT_TIMEOUT
    if category == "CONNECTION_RESET":
        return OUTCOME_CONNECTION_RESET
    if category.startswith("HTTP_") or category in _AUTH_RESPONSE_FAILURES:
        return OUTCOME_HTTP_STATUS
    return OUTCOME_NO_RESPONSE


def _continuation_identity(month_request: MonthChunkRequest, cursor: str) -> str:
    return "cont-" + semantic_digest(
        {
            "cursor": cursor,
            "month_key": month_request.month_key,
            "month_request_digest": month_request.request_semantic_digest,
            "ticker": month_request.canonical_ticker,
        }
    )[:24]


def validate_massive_continuation(raw_next_url: str, *, month_request: MonthChunkRequest) -> SanitizedContinuation:
    try:
        url = httpx.URL(raw_next_url)
    except Exception as exc:
        raise MassiveTransportError("continuation URL is malformed") from exc
    if url.scheme != MASSIVE_REST_SCHEME:
        raise MassiveTransportError("continuation URL scheme mismatch")
    if url.host != MASSIVE_REST_HOST:
        raise MassiveTransportError("continuation URL host mismatch")
    if url.userinfo:
        raise MassiveTransportError("continuation URL userinfo is prohibited")
    if url.port not in (None, 443):
        raise MassiveTransportError("continuation URL port mismatch")
    if url.fragment:
        raise MassiveTransportError("continuation URL fragment is prohibited")
    expected_path = _custom_bars_path(month_request)
    if url.path != expected_path:
        raise MassiveTransportError("continuation URL path does not match request")
    params = tuple((str(key), str(value)) for key, value in url.params.multi_items())
    seen: set[str] = set()
    parsed: dict[str, str] = {}
    for key, value in params:
        lower = key.lower()
        if lower in _FORBIDDEN_QUERY_KEYS:
            raise MassiveTransportError("continuation URL contains credential-like parameter")
        if lower not in _ALLOWED_CONTINUATION_QUERY_KEYS:
            raise MassiveTransportError("continuation URL contains unsupported query parameter")
        if lower in seen:
            raise MassiveTransportError("continuation URL contains duplicate query parameter")
        seen.add(lower)
        parsed[lower] = value
    cursor = parsed.get("cursor")
    if not cursor:
        raise MassiveTransportError("continuation URL must include opaque cursor")
    cursor_lower = cursor.lower()
    if any(char in cursor for char in ("&", "=", "?", "#")) or any(key in cursor_lower for key in _FORBIDDEN_QUERY_KEYS):
        raise MassiveTransportError("continuation cursor contains prohibited query-like material")
    if parsed.get("adjusted", str(month_request.adjusted).lower()) != str(month_request.adjusted).lower():
        raise MassiveTransportError("continuation adjusted parameter mismatch")
    if parsed.get("sort", month_request.sort) != month_request.sort:
        raise MassiveTransportError("continuation sort parameter mismatch")
    if parsed.get("limit", str(month_request.limit)) != str(month_request.limit):
        raise MassiveTransportError("continuation limit parameter mismatch")
    digest = hashlib.sha256(cursor.encode("utf-8")).hexdigest()
    return SanitizedContinuation(
        sanitized_continuation_identity=_continuation_identity(month_request, cursor),
        cursor_digest=digest,
        query_params=_request_query(month_request, cursor),
    )


def _sanitized_query_string(
    pairs: tuple[tuple[str, str], ...],
    *,
    continuation: SanitizedContinuation | None,
) -> str:
    safe_pairs: list[tuple[str, str]] = []
    for key, value in pairs:
        if key == "cursor" and continuation is not None:
            safe_pairs.append(("cursor_digest", continuation.cursor_digest))
        else:
            safe_pairs.append((key, value))
    return _query_string(tuple(safe_pairs))


class MassiveRestTransport:
    """One-round-trip Massive REST transport compatible with monthly acquisition."""

    def __init__(
        self,
        *,
        month_request: MonthChunkRequest,
        api_key: ProviderApiKey,
        http_transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._month_request = month_request
        self._api_key = api_key
        self._client = httpx.Client(
            timeout=httpx.Timeout(
                connect=CONNECT_TIMEOUT_SECONDS,
                read=READ_TIMEOUT_SECONDS,
                write=WRITE_TIMEOUT_SECONDS,
                pool=POOL_TIMEOUT_SECONDS,
            ),
            follow_redirects=False,
            trust_env=False,
            verify=True,
            transport=http_transport,
        )
        self._call_count = 0

    @property
    def call_count(self) -> int:
        return self._call_count

    def close(self) -> None:
        self._client.close()

    def prepare_request(self, request: FakeTransportRequest, raw_next_url: str | None = None) -> MassivePreparedRequest:
        self._validate_protocol_request(request)
        path = _custom_bars_path(self._month_request)
        continuation: SanitizedContinuation | None = None
        query = _request_query(self._month_request)
        if raw_next_url is not None:
            continuation = validate_massive_continuation(raw_next_url, month_request=self._month_request)
            if continuation.sanitized_continuation_identity != request.sanitized_continuation_identity:
                raise MassiveTransportError("continuation identity mismatch")
            query = continuation.query_params
        elif request.sanitized_continuation_identity is not None:
            raise MassiveTransportError("continuation request requires raw provider evidence for reconstruction")
        url = f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{path}?{_query_string(query)}"
        sanitized_url = f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{path}?{_sanitized_query_string(query, continuation=continuation)}"
        return MassivePreparedRequest(
            method="GET",
            url=url,
            headers=_public_headers(),
            sanitized_url=sanitized_url,
            logical_page_request_id=request.logical_page_request_id,
            page_ordinal=request.page_ordinal,
            sanitized_continuation_identity=request.sanitized_continuation_identity,
        )

    def send(self, request: FakeTransportRequest, raw_next_url: str | None = None) -> ScriptedOutcome:
        try:
            prepared = self.prepare_request(request, raw_next_url=raw_next_url)
            self._call_count += 1
            self._client.cookies.clear()
            with self._client.stream(prepared.method, prepared.url, headers=_headers(self._api_key)) as response:
                outcome = self._outcome_from_response(response)
            self._client.cookies.clear()
            return outcome
        except httpx.TimeoutException:
            return ScriptedOutcome(OUTCOME_TRANSPORT_TIMEOUT)
        except httpx.ConnectError as exc:
            if _is_tls_validation_error(exc):
                return ScriptedOutcome(OUTCOME_NO_RESPONSE, headers={"failure_category": TLS_VALIDATION_FAILURE})
            return ScriptedOutcome(OUTCOME_CONNECTION_RESET)
        except (httpx.NetworkError, httpx.RemoteProtocolError):
            return ScriptedOutcome(OUTCOME_CONNECTION_RESET)
        except httpx.DecodingError:
            return ScriptedOutcome(OUTCOME_NO_RESPONSE, headers={"failure_category": UNSUPPORTED_CONTENT_ENCODING})
        except httpx.TransportError:
            return ScriptedOutcome(OUTCOME_NO_RESPONSE, headers={"failure_category": TLS_VALIDATION_FAILURE})
        except MassiveTransportError:
            return ScriptedOutcome(OUTCOME_NO_RESPONSE, headers={"failure_category": INVALID_REQUEST})

    def _validate_protocol_request(self, request: FakeTransportRequest) -> None:
        if request.request_semantic_digest != self._month_request.request_semantic_digest:
            raise MassiveTransportError("request semantic digest mismatch")
        if request.month_key != self._month_request.month_key:
            raise MassiveTransportError("request month mismatch")
        if request.page_ordinal < 1:
            raise MassiveTransportError("page ordinal must be positive")
        if request.page_ordinal == 1 and request.sanitized_continuation_identity is not None:
            raise MassiveTransportError("first page must not include continuation identity")
        if request.page_ordinal > 1 and request.sanitized_continuation_identity is None:
            raise MassiveTransportError("continuation page must include continuation identity")

    def _outcome_from_response(self, response: httpx.Response) -> ScriptedOutcome:
        headers = _sanitize_headers(response.headers)
        encoding = response.headers.get(CONTENT_ENCODING)
        if encoding and encoding.lower() != "identity":
            headers["failure_category"] = UNSUPPORTED_CONTENT_ENCODING
            return ScriptedOutcome(OUTCOME_HTTP_STATUS, http_status=response.status_code, headers=headers)
        if 300 <= response.status_code <= 399:
            headers["failure_category"] = HTTP_REDIRECT_REJECTED
            return ScriptedOutcome(OUTCOME_HTTP_STATUS, http_status=response.status_code, headers=headers)
        content_length = response.headers.get(CONTENT_LENGTH)
        if content_length is not None:
            try:
                if int(content_length) > MAXIMUM_RESPONSE_BODY_BYTES:
                    headers["failure_category"] = RESPONSE_BODY_LIMIT_EXCEEDED
                    return ScriptedOutcome(OUTCOME_HTTP_STATUS, http_status=response.status_code, headers=headers)
            except ValueError:
                headers["failure_category"] = RESPONSE_SCHEMA_INVALID
                return ScriptedOutcome(OUTCOME_HTTP_STATUS, http_status=response.status_code, headers=headers)
        if response.is_stream_consumed:
            content = response.content
        else:
            chunks: list[bytes] = []
            total = 0
            for chunk in response.iter_raw():
                total += len(chunk)
                if total > MAXIMUM_RESPONSE_BODY_BYTES:
                    headers["failure_category"] = RESPONSE_BODY_LIMIT_EXCEEDED
                    return ScriptedOutcome(OUTCOME_HTTP_STATUS, http_status=response.status_code, headers=headers)
                chunks.append(chunk)
            content = b"".join(chunks)
        if len(content) > MAXIMUM_RESPONSE_BODY_BYTES:
            headers["failure_category"] = RESPONSE_BODY_LIMIT_EXCEEDED
            return ScriptedOutcome(OUTCOME_HTTP_STATUS, http_status=response.status_code, headers=headers)
        if response.status_code == 200:
            if not _content_type_is_json(response.headers.get(CONTENT_TYPE)):
                headers["failure_category"] = RESPONSE_SCHEMA_INVALID
                return ScriptedOutcome(OUTCOME_HTTP_STATUS, http_status=response.status_code, headers=headers)
            return ScriptedOutcome(OUTCOME_HTTP_RESPONSE, http_status=200, body=content, headers=headers)
        headers["failure_category"] = _failure_category_for_status(response.status_code)
        return ScriptedOutcome(
            _outcome_status_for_failure(str(headers["failure_category"])),
            http_status=response.status_code,
            body=content if content else None,
            headers=headers,
        )


def massive_transport_self_check() -> dict[str, object]:
    body = b'{"adjusted":true,"queryCount":1,"results":[{"c":100,"h":101,"l":99,"n":1,"o":100,"t":1704105000000,"v":1000}],"resultsCount":1,"status":"OK","ticker":"FAKEFLOW"}'
    observed: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        observed["authorization"] = request.headers.get("Authorization", "")
        observed["url"] = str(request.url)
        observed["accept_encoding"] = request.headers.get("Accept-Encoding", "")
        return httpx.Response(200, headers={CONTENT_TYPE: "application/json"}, content=body)

    from marketflow.historical_data.monthly_acquisition import build_logical_page_request, build_month_chunk_request, fake_transport_request

    month_request = build_month_chunk_request(
        canonical_ticker="FAKEFLOW",
        month_key="2024-01",
        effective_start_date="2024-01-01",
        effective_end_date="2024-01-01",
    )
    logical_page = build_logical_page_request(month_request, page_ordinal=1)
    transport = MassiveRestTransport(
        month_request=month_request,
        api_key=ProviderApiKey("fictional-self-check-key"),
        http_transport=httpx.MockTransport(handler),
    )
    outcome = transport.send(fake_transport_request(month_request, logical_page))
    transport.close()
    next_url = (
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/"
        "2024-01-01/2024-01-01?cursor=selfcheck&adjusted=true&sort=asc&limit=50000"
    )
    continuation = validate_massive_continuation(next_url, month_request=month_request)
    return {
        "status": "MASSIVE_REST_TRANSPORT_SELF_CHECK",
        "provider_business_identity": PROVIDER_BUSINESS_IDENTITY,
        "fixed_host": MASSIVE_REST_HOST,
        "fixed_scheme": MASSIVE_REST_SCHEME,
        "http_status": outcome.http_status,
        "transport_status": outcome.outcome_type,
        "body_byte_count": len(outcome.body or b""),
        "exact_body_bytes_returned": outcome.body == body,
        "authorization_header_present": observed.get("authorization", "").startswith("Bearer "),
        "url_contains_api_key": "apikey" in observed.get("url", "").lower() or "api_key" in observed.get("url", "").lower(),
        "accept_encoding": observed.get("accept_encoding"),
        "continuation_identity": continuation.sanitized_continuation_identity,
        "cursor_digest": continuation.cursor_digest,
        "provider_execution_enabled": False,
        "real_provider_call_performed": False,
        "credential_source": "FICTIONAL_EXPLICIT_INJECTION",
    }
