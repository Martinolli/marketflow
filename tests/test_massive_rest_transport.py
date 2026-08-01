from __future__ import annotations

import ast
import dataclasses
import gzip
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import httpx
import pytest

from marketflow.historical_data import massive_transport as mt
from marketflow.historical_data import monthly_acquisition as monthly
from marketflow.historical_data.fake_transport import OUTCOME_HTTP_RESPONSE, OUTCOME_HTTP_STATUS, OUTCOME_NO_RESPONSE


REPO_ROOT = Path(__file__).resolve().parents[1]


def _month_request() -> monthly.MonthChunkRequest:
    return monthly.build_month_chunk_request(
        canonical_ticker="FAKEFLOW",
        month_key="2024-01",
        effective_start_date="2024-01-01",
        effective_end_date="2024-01-01",
    )


def _page_request(request: monthly.MonthChunkRequest, page_ordinal: int = 1, continuation: str | None = None):
    predecessor = "page-predecessor" if page_ordinal > 1 else None
    logical = monthly.build_logical_page_request(
        request,
        page_ordinal=page_ordinal,
        predecessor_accepted_page_identity=predecessor,
        sanitized_continuation_identity=continuation,
    )
    return logical, monthly.fake_transport_request(request, logical)


def _body(*, ticker: str = "FAKEFLOW", next_url: str | None = None, t: int = 1704105000000) -> bytes:
    next_part = f',"next_url":"{next_url}"' if next_url else ""
    return (
        '{"adjusted":true,"queryCount":1,"results":[{"c":100,"h":101,"l":99,"n":1,'
        '"o":100,"t":'
        + str(t)
        + ',"v":1000}],"resultsCount":1,"status":"OK","ticker":"'
        + ticker
        + '"'
        + next_part
        + "}"
    ).encode("utf-8")


def _transport(handler, request: monthly.MonthChunkRequest | None = None) -> mt.MassiveRestTransport:
    return mt.MassiveRestTransport(
        month_request=request or _month_request(),
        api_key=mt.ProviderApiKey("fictional-test-key"),
        http_transport=httpx.MockTransport(handler),
    )


def test_httpx_is_source_declared_and_no_dependency_change_needed():
    requirements = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")

    assert "httpx==0.28.1" in requirements


@pytest.mark.parametrize("bad_key", ["", " ", " key", "key ", "abc\rdef", "abc\ndef", "abc\x00def"])
def test_provider_api_key_rejects_empty_whitespace_and_header_injection(bad_key: str):
    with pytest.raises(mt.MassiveTransportError):
        mt.ProviderApiKey(bad_key)


def test_provider_api_key_is_redacted_and_only_header_injects_secret():
    key = mt.ProviderApiKey("fictional-secret")

    assert str(key) == "<redacted>"
    assert repr(key) == "ProviderApiKey(<redacted>)"
    assert "fictional-secret" not in repr(key)
    assert dataclasses.is_dataclass(key) is False
    assert key.authorization_header() == "Bearer fictional-secret"


def test_prepared_request_repr_redacts_authorization_header():
    month_request = _month_request()
    _, protocol_request = _page_request(month_request)
    prepared = _transport(lambda request: httpx.Response(200), month_request).prepare_request(protocol_request)

    assert "fictional-test-key" not in repr(prepared)
    assert "<redacted>" in repr(prepared)
    assert prepared.headers["Authorization"] == "<redacted>"


def test_initial_request_uses_fixed_https_host_path_query_headers_and_no_api_key_url():
    month_request = _month_request()
    observed: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        observed["method"] = request.method
        observed["url"] = str(request.url)
        observed["host"] = request.url.host or ""
        observed["scheme"] = request.url.scheme
        observed["path"] = request.url.path
        observed["authorization"] = request.headers.get("Authorization", "")
        observed["accept"] = request.headers.get("Accept", "")
        observed["accept_encoding"] = request.headers.get("Accept-Encoding", "")
        observed["user_agent"] = request.headers.get("User-Agent", "")
        observed["cookie"] = request.headers.get("Cookie", "")
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body())

    transport = _transport(handler, month_request)
    _, protocol_request = _page_request(month_request)

    outcome = transport.send(protocol_request)
    transport.close()

    assert outcome.outcome_type == OUTCOME_HTTP_RESPONSE
    assert observed["method"] == "GET"
    assert observed["scheme"] == "https"
    assert observed["host"] == mt.MASSIVE_REST_HOST
    assert observed["path"] == "/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01"
    assert "adjusted=true" in observed["url"]
    assert "sort=asc" in observed["url"]
    assert "limit=50000" in observed["url"]
    assert "apiKey" not in observed["url"] and "api_key" not in observed["url"]
    assert observed["authorization"] == "Bearer fictional-test-key"
    assert observed["accept"] == "application/json"
    assert observed["accept_encoding"] == "identity"
    assert observed["user_agent"] == mt.MASSIVE_USER_AGENT
    assert observed["cookie"] == ""


def test_ticker_path_escape_is_rejected_before_http_call():
    month_request = monthly.build_month_chunk_request(
        canonical_ticker="FAKE/FLOW",
        month_key="2024-01",
        effective_start_date="2024-01-01",
        effective_end_date="2024-01-01",
    )
    _, protocol_request = _page_request(month_request)
    transport = _transport(lambda request: httpx.Response(500), month_request)

    outcome = transport.send(protocol_request)

    assert outcome.outcome_type == OUTCOME_NO_RESPONSE
    assert outcome.headers["failure_category"] == mt.INVALID_REQUEST
    assert transport.call_count == 0


@pytest.mark.parametrize(
    "replacement",
    [
        {"multiplier": 1},
        {"timespan": "day"},
        {"adjusted": False},
        {"sort": "desc"},
        {"limit": 10},
    ],
)
def test_request_contract_overrides_are_rejected_before_http_call(replacement: dict[str, object]):
    month_request = replace(_month_request(), **replacement)
    _, protocol_request = _page_request(month_request)
    transport = _transport(lambda request: httpx.Response(500), month_request)

    outcome = transport.send(protocol_request)

    assert outcome.outcome_type == OUTCOME_NO_RESPONSE
    assert outcome.headers["failure_category"] == mt.INVALID_REQUEST
    assert transport.call_count == 0


def test_valid_continuation_reconstructs_same_endpoint_and_digest():
    month_request = _month_request()
    raw_next_url = (
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/"
        "2024-01-01/2024-01-01?cursor=opaque&adjusted=true&sort=asc&limit=50000"
    )
    continuation = mt.validate_massive_continuation(raw_next_url, month_request=month_request)
    logical, protocol_request = _page_request(month_request, page_ordinal=2, continuation=continuation.sanitized_continuation_identity)

    assert logical.sanitized_continuation_identity == continuation.sanitized_continuation_identity
    assert continuation.cursor_digest
    assert "opaque" not in continuation.sanitized_continuation_identity
    prepared = _transport(lambda request: httpx.Response(200), month_request).prepare_request(protocol_request, raw_next_url=raw_next_url)
    assert prepared.url.endswith("adjusted=true&sort=asc&limit=50000&cursor=opaque")
    assert "cursor_digest=" in prepared.sanitized_url
    assert "opaque" not in prepared.sanitized_url
    assert "opaque" not in repr(prepared)
    assert "apiKey" not in prepared.url


def test_forged_page_protocol_state_fails_closed_before_http_call():
    month_request = _month_request()
    first_logical = monthly.LogicalPageRequest(
        logical_page_request_id="forged-first",
        month_request_digest=month_request.request_semantic_digest,
        page_ordinal=1,
        predecessor_accepted_page_identity=None,
        sanitized_continuation_identity="cont-forged",
    )
    second_logical = monthly.LogicalPageRequest(
        logical_page_request_id="forged-second",
        month_request_digest=month_request.request_semantic_digest,
        page_ordinal=2,
        predecessor_accepted_page_identity=None,
        sanitized_continuation_identity=None,
    )
    transport = _transport(lambda request: httpx.Response(500), month_request)

    first_outcome = transport.send(monthly.fake_transport_request(month_request, first_logical))
    second_outcome = transport.send(monthly.fake_transport_request(month_request, second_logical))

    assert first_outcome.outcome_type == OUTCOME_NO_RESPONSE
    assert first_outcome.headers["failure_category"] == mt.INVALID_REQUEST
    assert second_outcome.outcome_type == OUTCOME_NO_RESPONSE
    assert second_outcome.headers["failure_category"] == mt.INVALID_REQUEST
    assert transport.call_count == 0


@pytest.mark.parametrize(
    "raw_url",
    [
        "http://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x",
        "https://api.polygon.io/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x",
        "https://user@api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x",
        "https://api.massive.com:8443/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x#frag",
        "https://api.massive.com/v2/aggs/ticker/OTHER/range/15/minute/2024-01-01/2024-01-01?cursor=x",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/1/day/2024-01-01/2024-01-01?cursor=x",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-02/2024-01-01?cursor=x",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x&adjusted=false",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x&sort=desc",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x&limit=10",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x&apiKey=secret",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=opaque%26apiKey%3Dsecret",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=opaque%26account_id%3Dacct",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x&account_id=acct",
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x&extra=1",
    ],
)
def test_invalid_continuations_are_rejected(raw_url: str):
    with pytest.raises(mt.MassiveTransportError):
        mt.validate_massive_continuation(raw_url, month_request=_month_request())


def test_response_exact_body_bytes_and_selected_headers_only():
    raw = b'{"z":2, "a":1}\n'

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Content-Length": str(len(raw)),
                "Retry-After": "5",
                "Set-Cookie": "secret-cookie",
                "Authorization": "secret",
            },
            content=raw,
        )

    transport = _transport(handler)
    _, protocol_request = _page_request(_month_request())
    outcome = transport.send(protocol_request)

    assert outcome.outcome_type == OUTCOME_HTTP_RESPONSE
    assert outcome.body == raw
    assert outcome.headers["Content-Type"] == "application/json; charset=utf-8"
    assert outcome.headers["Content-Length"] == str(len(raw))
    assert outcome.headers["Retry-After"] == "5"
    assert "Set-Cookie" not in outcome.headers
    assert "Authorization" not in outcome.headers


def test_success_body_with_invalid_next_url_returns_exact_body_for_parser_boundary():
    raw = _body(next_url="https://api.polygon.io/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=x")
    transport = _transport(lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=raw))
    _, protocol_request = _page_request(_month_request())

    outcome = transport.send(protocol_request)

    assert outcome.outcome_type == OUTCOME_HTTP_RESPONSE
    assert outcome.body == raw


@pytest.mark.parametrize("content_type", [None, "text/html", "text/plain", "application/xml", "multipart/form-data"])
def test_success_response_rejects_missing_or_non_json_content_type(content_type: str | None):
    headers = {} if content_type is None else {"Content-Type": content_type}
    transport = _transport(lambda request: httpx.Response(200, headers=headers, content=b"{}"))
    _, protocol_request = _page_request(_month_request())

    outcome = transport.send(protocol_request)

    assert outcome.outcome_type == OUTCOME_HTTP_STATUS
    assert outcome.headers["failure_category"] == mt.RESPONSE_SCHEMA_INVALID


def test_unsupported_content_encoding_is_rejected_before_acceptance():
    transport = _transport(
        lambda request: httpx.Response(
            200,
            headers={"Content-Type": "application/json", "Content-Encoding": "gzip"},
            content=gzip.compress(b"abc"),
        )
    )
    _, protocol_request = _page_request(_month_request())

    outcome = transport.send(protocol_request)

    assert outcome.outcome_type == OUTCOME_HTTP_STATUS
    assert outcome.headers["failure_category"] == mt.UNSUPPORTED_CONTENT_ENCODING


def test_body_limit_accepts_exact_limit_and_rejects_over_limit(monkeypatch):
    monkeypatch.setattr(mt, "MAXIMUM_RESPONSE_BODY_BYTES", 8)
    month_request = _month_request()
    _, protocol_request = _page_request(month_request)
    exact = _transport(lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=b"12345678"), month_request)
    over = _transport(lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=b"123456789"), month_request)

    assert exact.send(protocol_request).outcome_type == OUTCOME_HTTP_RESPONSE
    over_outcome = over.send(protocol_request)
    assert over_outcome.outcome_type == OUTCOME_HTTP_STATUS
    assert over_outcome.headers["failure_category"] == mt.RESPONSE_BODY_LIMIT_EXCEEDED
    assert mt.MAXIMUM_RESPONSE_BODY_BYTES == 8


def test_content_length_over_limit_rejects_without_reading(monkeypatch):
    class FailingStream(httpx.SyncByteStream):
        def __iter__(self):
            raise AssertionError("body stream should not be read")

    monkeypatch.setattr(mt, "MAXIMUM_RESPONSE_BODY_BYTES", 8)
    transport = _transport(
        lambda request: httpx.Response(
            200,
            headers={"Content-Type": "application/json", "Content-Length": "9"},
            stream=FailingStream(),
        )
    )
    _, protocol_request = _page_request(_month_request())

    outcome = transport.send(protocol_request)

    assert outcome.outcome_type == OUTCOME_HTTP_STATUS
    assert outcome.headers["failure_category"] == mt.RESPONSE_BODY_LIMIT_EXCEEDED


@pytest.mark.parametrize(
    ("status_code", "failure"),
    [
        (408, "HTTP_408"),
        (429, "HTTP_429"),
        (500, "HTTP_500"),
        (502, "HTTP_502"),
        (503, "HTTP_503"),
        (504, "HTTP_504"),
        (401, mt.AUTHENTICATION_FAILURE),
        (403, mt.AUTHORIZATION_FAILURE),
        (302, mt.HTTP_REDIRECT_REJECTED),
    ],
)
def test_status_mapping_preserves_retryable_and_nonretryable_categories(status_code: int, failure: str):
    headers = {"Content-Type": "application/json", "Retry-After": "10"}
    transport = _transport(lambda request: httpx.Response(status_code, headers=headers, content=b"{}"))
    _, protocol_request = _page_request(_month_request())

    outcome = transport.send(protocol_request)

    assert outcome.http_status == status_code
    assert outcome.outcome_type == OUTCOME_HTTP_STATUS
    assert outcome.headers["failure_category"] == failure


@pytest.mark.parametrize(
    "exception",
    [
        httpx.ConnectTimeout("timeout"),
        httpx.ReadTimeout("timeout"),
        httpx.WriteTimeout("timeout"),
        httpx.PoolTimeout("timeout"),
    ],
)
def test_timeout_exceptions_map_to_transport_timeout_without_raw_text(exception: Exception):
    def handler(request: httpx.Request) -> httpx.Response:
        raise exception

    transport = _transport(handler)
    _, protocol_request = _page_request(_month_request())

    outcome = transport.send(protocol_request)

    assert outcome.outcome_type == "TRANSPORT_TIMEOUT"
    assert "timeout" not in json.dumps(outcome.headers or {}, sort_keys=True).lower()


def test_connection_reset_and_tls_failure_map_to_fixed_categories():
    ssl_error = OSError("SSL certificate verify failed")

    def reset_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("raw reset detail")

    def tls_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connect failed") from ssl_error

    _, protocol_request = _page_request(_month_request())
    reset = _transport(reset_handler).send(protocol_request)
    tls = _transport(tls_handler).send(protocol_request)

    assert reset.outcome_type == "CONNECTION_RESET"
    assert tls.outcome_type == OUTCOME_NO_RESPONSE
    assert tls.headers["failure_category"] == mt.TLS_VALIDATION_FAILURE
    assert "raw" not in json.dumps(tls.headers, sort_keys=True).lower()


def test_cookie_persistence_is_disabled_between_calls():
    seen_cookies: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_cookies.append(request.headers.get("Cookie", ""))
        return httpx.Response(500, headers={"Set-Cookie": "session=secret", "Content-Type": "application/json"}, content=b"{}")

    month_request = _month_request()
    transport = _transport(handler, month_request)
    _, protocol_request = _page_request(month_request)

    transport.send(protocol_request)
    transport.send(protocol_request)

    assert seen_cookies == ["", ""]


def test_transport_has_fixed_http_security_configuration():
    transport = _transport(lambda request: httpx.Response(200, headers={"Content-Type": "application/json"}, content=b"{}"))

    assert transport._client.follow_redirects is False
    assert transport._client.trust_env is False
    assert transport._client.timeout.connect == mt.CONNECT_TIMEOUT_SECONDS
    assert transport._client.timeout.read == mt.READ_TIMEOUT_SECONDS
    assert transport._client.timeout.write == mt.WRITE_TIMEOUT_SECONDS
    assert transport._client.timeout.pool == mt.POOL_TIMEOUT_SECONDS


def test_monthly_executor_accepts_massive_transport_and_executor_owns_retry(tmp_path: Path):
    month_request = _month_request()
    responses = iter(
        [
            httpx.Response(500, headers={"Content-Type": "application/json"}, content=b'{"status":"ERROR"}'),
            httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body()),
        ]
    )
    transport = _transport(lambda request: next(responses), month_request)

    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=month_request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-massive-retry",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["recorded_retry_delays_seconds"] == [2]
    assert transport.call_count == 2


def test_monthly_executor_accepts_massive_transport_for_two_page_chain(tmp_path: Path):
    month_request = _month_request()
    next_url = (
        "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/"
        "2024-01-01/2024-01-01?cursor=next&adjusted=true&sort=asc&limit=50000"
    )
    seen_urls: list[str] = []
    responses = iter(
        [
            httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body(next_url=next_url)),
            httpx.Response(200, headers={"Content-Type": "application/json"}, content=_body(t=1704105900000)),
        ]
    )

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return next(responses)

    transport = _transport(handler, month_request)
    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=month_request,
        transport=transport,
        run_root=tmp_path,
        run_id="run-massive-two-page",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
    )

    assert receipt["status"] == monthly.MONTH_ACQUISITION_COMPLETED
    assert receipt["page_count"] == 2
    assert len(seen_urls) == 2
    assert "cursor=next" in seen_urls[1]
    assert "apiKey" not in seen_urls[0] + seen_urls[1]
    assert transport.call_count == 2


def test_massive_transport_self_check_cli_is_sanitized_and_rejects_operational_args():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-transport-self-check"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["status"] == "MASSIVE_REST_TRANSPORT_SELF_CHECK"
    assert receipt["fixed_host"] == mt.MASSIVE_REST_HOST
    assert receipt["authorization_header_present"] is True
    assert receipt["url_contains_api_key"] is False
    assert receipt["exact_body_bytes_returned"] is True
    assert "fictional-self-check-key" not in result.stdout
    blocked = subprocess.run(
        [sys.executable, "-m", "marketflow.historical_data", "--massive-transport-self-check", "--api-key", "x"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert blocked.returncode != 0


def test_massive_transport_source_assurance_boundaries():
    path = REPO_ROOT / "marketflow" / "historical_data" / "massive_transport.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    attrs = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}

    assert {"polygon", "requests", "yfinance", "socket", "urllib", "openai", "streamlit"}.isdisjoint(imported)
    assert {"polygon", "requests", "yfinance", "socket", "urllib", "openai", "streamlit"}.isdisjoint(imported_from)
    assert "getenv" not in attrs
    assert "environ" not in attrs
    assert "verify=False" not in source
    assert "follow_redirects=True" not in source
    assert "trust_env=True" not in source
    assert "?apiKey" not in source
    assert "api.polygon.io" not in source
    assert "_record_continuation_evidence" not in source
    assert "json.loads(content" not in source
