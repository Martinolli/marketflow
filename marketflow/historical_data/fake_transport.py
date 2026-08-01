"""Deterministic fake transport for offline monthly acquisition tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


OUTCOME_HTTP_RESPONSE = "HTTP_RESPONSE"
OUTCOME_HTTP_STATUS = "HTTP_STATUS"
OUTCOME_TRANSPORT_TIMEOUT = "TRANSPORT_TIMEOUT"
OUTCOME_CONNECTION_RESET = "CONNECTION_RESET"
OUTCOME_CRASH_AFTER_BODY = "CRASH_AFTER_BODY"
OUTCOME_NO_RESPONSE = "NO_RESPONSE"

_VALID_OUTCOMES = frozenset(
    {
        OUTCOME_HTTP_RESPONSE,
        OUTCOME_HTTP_STATUS,
        OUTCOME_TRANSPORT_TIMEOUT,
        OUTCOME_CONNECTION_RESET,
        OUTCOME_CRASH_AFTER_BODY,
        OUTCOME_NO_RESPONSE,
    }
)


class FakeTransportError(ValueError):
    """Raised when the deterministic fake transport script is violated."""


@dataclass(frozen=True, slots=True)
class FakeTransportRequest:
    """A logical fake-provider request identity with no real URL or credential data."""

    logical_page_request_id: str
    request_semantic_digest: str
    page_ordinal: int
    month_key: str
    sanitized_continuation_identity: str | None


@dataclass(frozen=True, slots=True)
class ScriptedOutcome:
    outcome_type: str
    http_status: int | None = None
    body: bytes | None = None
    headers: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if self.outcome_type not in _VALID_OUTCOMES:
            raise FakeTransportError("unknown fake transport outcome")
        if self.outcome_type in {OUTCOME_HTTP_RESPONSE, OUTCOME_HTTP_STATUS, OUTCOME_CRASH_AFTER_BODY}:
            if type(self.http_status) is not int:
                raise FakeTransportError("HTTP fake outcomes require integer status")
        if self.outcome_type in {OUTCOME_HTTP_RESPONSE, OUTCOME_CRASH_AFTER_BODY} and self.body is None:
            raise FakeTransportError("complete-body fake outcomes require bytes")
        if self.body is not None and type(self.body) is not bytes:
            raise FakeTransportError("fake response body must be bytes")


@dataclass(frozen=True, slots=True)
class ScriptedExchange:
    expected_request: FakeTransportRequest
    outcome: ScriptedOutcome


class ScriptedFakeTransport:
    """Consume a strict sequence of fake request/outcome pairs."""

    def __init__(self, script: tuple[ScriptedExchange, ...] | list[ScriptedExchange]) -> None:
        self._script = tuple(script)
        self._cursor = 0

    def send(self, request: FakeTransportRequest) -> ScriptedOutcome:
        if self._cursor >= len(self._script):
            raise FakeTransportError("unexpected fake transport request")
        exchange = self._script[self._cursor]
        if request != exchange.expected_request:
            raise FakeTransportError("fake transport request identity mismatch")
        self._cursor += 1
        return exchange.outcome

    def assert_consumed(self) -> None:
        if self._cursor != len(self._script):
            raise FakeTransportError("unconsumed fake transport response")


def http_response(status: int, body: bytes, *, headers: Mapping[str, str] | None = None) -> ScriptedOutcome:
    return ScriptedOutcome(OUTCOME_HTTP_RESPONSE, http_status=status, body=body, headers=headers or {})


def http_status(status: int, *, headers: Mapping[str, str] | None = None) -> ScriptedOutcome:
    return ScriptedOutcome(OUTCOME_HTTP_STATUS, http_status=status, headers=headers or {})


def timeout() -> ScriptedOutcome:
    return ScriptedOutcome(OUTCOME_TRANSPORT_TIMEOUT)


def connection_reset() -> ScriptedOutcome:
    return ScriptedOutcome(OUTCOME_CONNECTION_RESET)


def crash_after_body(status: int, body: bytes, *, headers: Mapping[str, str] | None = None) -> ScriptedOutcome:
    return ScriptedOutcome(OUTCOME_CRASH_AFTER_BODY, http_status=status, body=body, headers=headers or {})


def no_response() -> ScriptedOutcome:
    return ScriptedOutcome(OUTCOME_NO_RESPONSE)
