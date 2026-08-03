"""Offline source-authority support for Massive.com Ticker Events audits."""

from __future__ import annotations

import getpass
import json
import os
import shutil
import stat
import sys
import tempfile
import uuid
from dataclasses import asdict, dataclass, is_dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

import httpx

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.historical_data.massive_transport import (
    CONNECT_TIMEOUT_SECONDS,
    MASSIVE_REST_HOST,
    MASSIVE_REST_SCHEME,
    MASSIVE_USER_AGENT,
    MassiveTransportError,
    POOL_TIMEOUT_SECONDS,
    ProviderApiKey,
    READ_TIMEOUT_SECONDS,
    WRITE_TIMEOUT_SECONDS,
)
import marketflow.source_authority.instrument_identity as identity


TICKER_EVENT_AUDIT_SPECIFICATION_SCHEMA_VERSION = "marketflow.ticker_event_audit_specification.v1"
TICKER_EVENT_AUDIT_ARTIFACT_MANIFEST_SCHEMA_VERSION = "marketflow.ticker_event_audit_artifact_manifest.v1"
PROVIDER_TICKER_EVENT_AUDIT_CANDIDATE_NONCANONICAL = "PROVIDER_TICKER_EVENT_AUDIT_CANDIDATE_NONCANONICAL"
TICKER_EVENTS_EXPERIMENTAL_VX = "TICKER_EVENTS_EXPERIMENTAL_VX"
ENDPOINT_STABILITY_EXPERIMENTAL = "EXPERIMENTAL"
QUERY_IDENTIFIER_TYPE = "COMPOSITE_FIGI"
QUERY_IDENTIFIER = "BBG000B9XRY4"
TICKER_CONTEXT = "AAPL"
SHARE_CLASS_FIGI_CONTEXT = "BBG001S5N8V8"
PRIMARY_EXCHANGE_CONTEXT = "XNAS"
SECURITY_TYPE_CONTEXT = "CS"
START_DATE = "2022-01-01"
END_DATE = "2025-12-31"
EVENT_TYPE_TICKER_CHANGE = "ticker_change"
SOURCE_IDENTITY_RUN_ID = "ident-509de6e2eb5e4a1db785e034bcfaf045"
SOURCE_CONTINUITY_ARTIFACT_ID = "ident-art-8607986a2341423182614a41c6236ed9"
SOURCE_CONTINUITY_STATUS = identity.IDENTITY_CONTINUITY_SUPPORTED
SOURCE_START_SNAPSHOT_DIGEST = "75a3fb5cccda09c05001129ec7161ad479457a714a5903828c67c5cfeb965928"
SOURCE_END_SNAPSHOT_DIGEST = "5e80a556b6172d8ca8985177f8c17e05183322fb5981ba92def57d4698aa4f50"
TICKER_EVENTS_PATH = f"/vX/reference/tickers/{QUERY_IDENTIFIER}/events"
TICKER_EVENTS_QUERY = (("types", EVENT_TYPE_TICKER_CHANGE),)
TICKER_EVENT_RUNTIME_ROOT = Path(".marketflow") / "source_authority" / "ticker_events" / "runs"
CONFIRMATION_PREFIX = "RUN MARKETFLOW TICKER EVENT AUDIT "

TICKER_EVENTS_RAW_RESPONSE = "TICKER_EVENTS_RAW_RESPONSE"
TICKER_EVENT_TIMELINE = "TICKER_EVENT_TIMELINE"
TICKER_EVENT_AUDIT_CANDIDATE = "TICKER_EVENT_AUDIT_CANDIDATE"
TICKER_EVENT_AUDIT_RECEIPT = "TICKER_EVENT_AUDIT_RECEIPT"

NO_TICKER_CHANGE_EVENTS_RETURNED = "NO_TICKER_CHANGE_EVENTS_RETURNED"
TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE = "TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE"
TICKER_EVENT_CHANGE_REQUIRES_SEGMENT_REVIEW = "TICKER_EVENT_CHANGE_REQUIRES_SEGMENT_REVIEW"
TICKER_EVENT_EVIDENCE_INCOMPLETE = "TICKER_EVENT_EVIDENCE_INCOMPLETE"
TICKER_EVENT_EVIDENCE_CONFLICT = "TICKER_EVENT_EVIDENCE_CONFLICT"
TICKER_EVENT_ENDPOINT_UNAVAILABLE = "TICKER_EVENT_ENDPOINT_UNAVAILABLE"
IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE = "IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE"
IDENTITY_CONTINUITY_REQUIRES_TICKER_EVENT_SEGMENT_REVIEW = "IDENTITY_CONTINUITY_REQUIRES_TICKER_EVENT_SEGMENT_REVIEW"
IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_INCOMPLETE = "IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_INCOMPLETE"

TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_READY = "TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_READY"
TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_FAILED = "TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_FAILED"
TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED = "TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED"
TICKER_EVENT_AUDIT_TRANSPORT_FAILED = "TICKER_EVENT_AUDIT_TRANSPORT_FAILED"
TICKER_EVENT_AUDIT_RESPONSE_REJECTED = "TICKER_EVENT_AUDIT_RESPONSE_REJECTED"
TICKER_EVENT_AUDIT_READY_NONCANONICAL = "TICKER_EVENT_AUDIT_READY_NONCANONICAL"
TICKER_EVENT_AUDIT_UNEXPECTED_FAILURE = "TICKER_EVENT_AUDIT_UNEXPECTED_FAILURE"
TICKER_EVENT_AUDIT_REPOSITORY_ROOT_UNRESOLVED = "TICKER_EVENT_AUDIT_REPOSITORY_ROOT_UNRESOLVED"
TICKER_EVENT_AUDIT_RUNTIME_ROOT_INVALID = "TICKER_EVENT_AUDIT_RUNTIME_ROOT_INVALID"
TICKER_EVENT_AUDIT_ARTIFACT_WRITER_UNREADY = "TICKER_EVENT_AUDIT_ARTIFACT_WRITER_UNREADY"
TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID = "TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID"
TICKER_EVENT_AUDIT_SOURCE_DEPENDENCY_INVALID = "TICKER_EVENT_AUDIT_SOURCE_DEPENDENCY_INVALID"

PROVIDER_STATUS_OK = "OK"
BEFORE_CONTRACT_RANGE = "BEFORE_CONTRACT_RANGE"
WITHIN_CONTRACT_RANGE = "WITHIN_CONTRACT_RANGE"
AFTER_CONTRACT_RANGE = "AFTER_CONTRACT_RANGE"
PAYLOAD_MEDIA_TYPE_CANONICAL_JSON = identity.PAYLOAD_MEDIA_TYPE_CANONICAL_JSON
PAYLOAD_MEDIA_TYPE_PROVIDER_RAW_BYTES = identity.PAYLOAD_MEDIA_TYPE_PROVIDER_RAW_BYTES

TOP_LEVEL_FIELDS = frozenset({"request_id", "results", "status"})
RESULT_FIELDS = frozenset({"events", "name"})
EVENT_FIELDS = frozenset({"date", "type", "ticker_change"})
TICKER_CHANGE_FIELDS = frozenset({"ticker"})
MANIFEST_FIELDS = frozenset(
    {
        "schema_version",
        "artifact_id",
        "run_id",
        "artifact_type",
        "stage",
        "created_at_utc",
        "ticker_event_audit_specification_digest",
        "provider",
        "identifier_type",
        "query_identifier",
        "source_identity_run_id",
        "source_continuity_artifact_id",
        "source_continuity_semantic_digest",
        "payload_ref",
        "payload_sha256",
        "payload_byte_size",
        "payload_media_type",
        "semantic_payload_digest",
        "input_artifact_ids",
        "input_manifest_refs",
        "lineage_artifact_ids",
        "external_source_artifact_ids",
    }
)
STAGE_BY_TYPE = {
    TICKER_EVENTS_RAW_RESPONSE: "ticker_events_raw_response",
    TICKER_EVENT_TIMELINE: "ticker_event_timeline",
    TICKER_EVENT_AUDIT_CANDIDATE: "ticker_event_audit_candidate",
    TICKER_EVENT_AUDIT_RECEIPT: "ticker_event_audit_receipt",
}
STAGE_DIRECTORY = {
    "ticker_events_raw_response": "raw_response",
    "ticker_event_timeline": "timeline",
    "ticker_event_audit_candidate": "audit",
    "ticker_event_audit_receipt": "receipt",
}


class TickerEventAuditError(ValueError):
    """Raised when ticker-event audit evidence fails closed."""


class TickerEventAuditRunError(TickerEventAuditError):
    """Raised after a live audit attempt with sanitized observable counts."""

    def __init__(
        self,
        message: str,
        *,
        provider_request_count: int,
        runtime_artifact_written: bool,
    ) -> None:
        super().__init__(message)
        self.provider_request_count = provider_request_count
        self.runtime_artifact_written = runtime_artifact_written


@dataclass(frozen=True, slots=True)
class TickerEventAuditSpecification:
    schema_version: str
    classification: str
    provider: str
    endpoint_family: str
    endpoint_stability: str
    query_identifier_type: str
    query_identifier: str
    ticker_context: str
    share_class_figi_context: str
    start_date: str
    end_date: str
    event_types: tuple[str, ...]
    source_identity_run_id: str
    source_continuity_artifact_id: str
    source_continuity_status: str
    canonical_eligibility: bool
    registry_eligibility: bool
    identity_freeze_eligibility: bool
    strategy_enabled: bool


@dataclass(frozen=True, slots=True)
class PreparedTickerEventsRequest:
    method: str
    url: str
    headers: Mapping[str, str]
    sanitized_path: str
    query: tuple[tuple[str, str], ...]

    def __repr__(self) -> str:
        safe_headers = {key: ("<redacted>" if key.lower() == "authorization" else value) for key, value in self.headers.items()}
        return f"PreparedTickerEventsRequest(method={self.method!r}, path={self.sanitized_path!r}, headers={safe_headers!r})"


@dataclass(frozen=True, slots=True)
class SourceIdentityBinding:
    source_identity_run_id: str
    source_continuity_artifact_id: str
    source_continuity_status: str
    source_continuity_semantic_digest: str
    start_snapshot_artifact_id: str
    end_snapshot_artifact_id: str
    start_snapshot_semantic_digest: str
    end_snapshot_semantic_digest: str
    ticker: str
    composite_figi: str
    share_class_figi: str
    primary_exchange: str
    security_type: str


@dataclass(frozen=True, slots=True)
class TickerEvent:
    date: str
    type: str
    ticker: str
    range_classification: str


@dataclass(frozen=True, slots=True)
class TickerEventTimeline:
    schema_version: str
    specification_digest: str
    query_identifier_type: str
    query_identifier: str
    source_identity_run_id: str
    source_continuity_artifact_id: str
    source_continuity_semantic_digest: str
    endpoint_stability: str
    provider_status: str
    event_count: int
    pre_range_event_count: int
    in_range_event_count: int
    post_range_event_count: int
    empty_events_status: str | None
    events: tuple[TickerEvent, ...]
    timeline_semantic_digest: str


@dataclass(frozen=True, slots=True)
class TickerEventAuditEvidence:
    schema_version: str
    source_identity_run_id: str
    source_continuity_artifact_id: str
    source_continuity_status: str
    source_continuity_semantic_digest: str
    start_snapshot_semantic_digest: str
    end_snapshot_semantic_digest: str
    contract_start_date: str
    contract_end_date: str
    audit_status: str
    combined_identity_candidate_status: str
    fixed_findings: tuple[str, ...]
    event_count: int
    pre_range_event_count: int
    in_range_event_count: int
    post_range_event_count: int
    endpoint_stability: str
    canonical_eligibility: bool
    registry_eligibility: bool
    identity_freeze_eligibility: bool
    strategy_enabled: bool
    audit_semantic_digest: str


@dataclass(frozen=True, slots=True)
class TickerEventRunContext:
    run_id: str
    run_root: Path
    run_dir: Path
    created_at_utc: str


def default_ticker_event_audit_specification() -> TickerEventAuditSpecification:
    return TickerEventAuditSpecification(
        schema_version=TICKER_EVENT_AUDIT_SPECIFICATION_SCHEMA_VERSION,
        classification=PROVIDER_TICKER_EVENT_AUDIT_CANDIDATE_NONCANONICAL,
        provider="MASSIVE.COM",
        endpoint_family=TICKER_EVENTS_EXPERIMENTAL_VX,
        endpoint_stability=ENDPOINT_STABILITY_EXPERIMENTAL,
        query_identifier_type=QUERY_IDENTIFIER_TYPE,
        query_identifier=QUERY_IDENTIFIER,
        ticker_context=TICKER_CONTEXT,
        share_class_figi_context=SHARE_CLASS_FIGI_CONTEXT,
        start_date=START_DATE,
        end_date=END_DATE,
        event_types=(EVENT_TYPE_TICKER_CHANGE,),
        source_identity_run_id=SOURCE_IDENTITY_RUN_ID,
        source_continuity_artifact_id=SOURCE_CONTINUITY_ARTIFACT_ID,
        source_continuity_status=SOURCE_CONTINUITY_STATUS,
        canonical_eligibility=False,
        registry_eligibility=False,
        identity_freeze_eligibility=False,
        strategy_enabled=False,
    )


def ticker_event_audit_specification_digest() -> str:
    return _digest(default_ticker_event_audit_specification())


def _canonical(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _canonical(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise TickerEventAuditError("timestamp must be timezone-aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, Decimal):
        raise TickerEventAuditError("binary-float authority fields are prohibited")
    return value


def _digest(value: Any) -> str:
    return semantic_digest(_canonical(value))


def _load_json(body: bytes) -> Any:
    if type(body) is not bytes or not body:
        raise TickerEventAuditError("provider response body must be non-empty bytes")

    def reject_constant(value: str) -> None:
        raise TickerEventAuditError(f"provider JSON constant is rejected: {value}")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise TickerEventAuditError("provider JSON object contains duplicate keys")
            result[key] = value
        return result

    try:
        return json.loads(
            body.decode("utf-8"),
            parse_float=Decimal,
            parse_int=int,
            parse_constant=reject_constant,
            object_pairs_hook=reject_duplicates,
        )
    except UnicodeDecodeError as exc:
        raise TickerEventAuditError("provider response body must be UTF-8 JSON") from exc
    except json.JSONDecodeError as exc:
        raise TickerEventAuditError("provider response body must be valid JSON") from exc


def _require_text(value: Any, field_name: str) -> str:
    if type(value) is not str or not value:
        raise TickerEventAuditError(f"{field_name} must be non-empty text")
    if any(ord(char) < 32 for char in value):
        raise TickerEventAuditError(f"{field_name} contains control characters")
    return value


def _validate_iso_date(value: str, field_name: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise TickerEventAuditError(f"{field_name} must be an ISO calendar date") from exc


def _validate_ticker(value: Any) -> str:
    text = _require_text(value, "ticker")
    safe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-"
    if len(text) > 32 or not all(char in safe for char in text):
        raise TickerEventAuditError("ticker must be a bounded provider ticker")
    return text


def _range_classification(value: str) -> str:
    event_date = date.fromisoformat(value)
    if event_date < date.fromisoformat(START_DATE):
        return BEFORE_CONTRACT_RANGE
    if event_date > date.fromisoformat(END_DATE):
        return AFTER_CONTRACT_RANGE
    return WITHIN_CONTRACT_RANGE


def parse_ticker_events_response(body: bytes, *, source_binding: SourceIdentityBinding | None = None) -> TickerEventTimeline:
    binding = source_binding or validate_accepted_source_identity_evidence()
    payload = _load_json(body)
    if not isinstance(payload, dict):
        raise TickerEventAuditError("Ticker Events response must be a JSON object")
    unknown = set(payload) - TOP_LEVEL_FIELDS
    if unknown:
        raise TickerEventAuditError("Ticker Events response has unknown top-level fields")
    status = _require_text(payload.get("status"), "status")
    if status != PROVIDER_STATUS_OK:
        raise TickerEventAuditError("Ticker Events response status mismatch")
    results = payload.get("results")
    if not isinstance(results, dict):
        raise TickerEventAuditError("Ticker Events results must be an object")
    unknown_results = set(results) - RESULT_FIELDS
    if unknown_results:
        raise TickerEventAuditError("Ticker Events results has unknown fields")
    if "events" not in results:
        raise TickerEventAuditError(TICKER_EVENT_EVIDENCE_INCOMPLETE)
    raw_events = results["events"]
    if not isinstance(raw_events, list):
        raise TickerEventAuditError("Ticker Events events must be an array")

    events: list[TickerEvent] = []
    by_date_type: dict[tuple[str, str], str] = {}
    seen_exact: set[tuple[str, str, str]] = set()
    for item in raw_events:
        if not isinstance(item, dict):
            raise TickerEventAuditError("Ticker Events event must be an object")
        unknown_event = set(item) - EVENT_FIELDS
        if unknown_event:
            raise TickerEventAuditError("Ticker Events event has unknown fields")
        event_type = _require_text(item.get("type"), "type")
        if event_type != EVENT_TYPE_TICKER_CHANGE:
            raise TickerEventAuditError("Ticker Events event type mismatch")
        event_date = _validate_iso_date(_require_text(item.get("date"), "date"), "date")
        ticker_change = item.get("ticker_change")
        if not isinstance(ticker_change, dict):
            raise TickerEventAuditError("ticker_change must be an object")
        unknown_change = set(ticker_change) - TICKER_CHANGE_FIELDS
        if unknown_change:
            raise TickerEventAuditError("ticker_change has unknown fields")
        ticker = _validate_ticker(ticker_change.get("ticker"))
        exact_key = (event_date, event_type, ticker)
        date_type_key = (event_date, event_type)
        if exact_key in seen_exact:
            raise TickerEventAuditError("duplicate identical Ticker Events event")
        if date_type_key in by_date_type and by_date_type[date_type_key] != ticker:
            raise TickerEventAuditError("conflicting duplicate Ticker Events event")
        seen_exact.add(exact_key)
        by_date_type[date_type_key] = ticker
        events.append(TickerEvent(event_date, event_type, ticker, _range_classification(event_date)))

    ordered = tuple(sorted(events, key=lambda event: (event.date, event.type, event.ticker)))
    pre = sum(1 for event in ordered if event.range_classification == BEFORE_CONTRACT_RANGE)
    in_range = sum(1 for event in ordered if event.range_classification == WITHIN_CONTRACT_RANGE)
    post = sum(1 for event in ordered if event.range_classification == AFTER_CONTRACT_RANGE)
    base = {
        "schema_version": "marketflow.ticker_event_timeline.v1",
        "specification_digest": ticker_event_audit_specification_digest(),
        "query_identifier_type": QUERY_IDENTIFIER_TYPE,
        "query_identifier": QUERY_IDENTIFIER,
        "source_identity_run_id": binding.source_identity_run_id,
        "source_continuity_artifact_id": binding.source_continuity_artifact_id,
        "source_continuity_semantic_digest": binding.source_continuity_semantic_digest,
        "endpoint_stability": ENDPOINT_STABILITY_EXPERIMENTAL,
        "provider_status": status,
        "event_count": len(ordered),
        "pre_range_event_count": pre,
        "in_range_event_count": in_range,
        "post_range_event_count": post,
        "empty_events_status": NO_TICKER_CHANGE_EVENTS_RETURNED if not ordered else None,
        "events": [asdict(event) for event in ordered],
    }
    return TickerEventTimeline(
        schema_version=str(base["schema_version"]),
        specification_digest=str(base["specification_digest"]),
        query_identifier_type=QUERY_IDENTIFIER_TYPE,
        query_identifier=QUERY_IDENTIFIER,
        source_identity_run_id=binding.source_identity_run_id,
        source_continuity_artifact_id=binding.source_continuity_artifact_id,
        source_continuity_semantic_digest=binding.source_continuity_semantic_digest,
        endpoint_stability=ENDPOINT_STABILITY_EXPERIMENTAL,
        provider_status=status,
        event_count=len(ordered),
        pre_range_event_count=pre,
        in_range_event_count=in_range,
        post_range_event_count=post,
        empty_events_status=NO_TICKER_CHANGE_EVENTS_RETURNED if not ordered else None,
        events=ordered,
        timeline_semantic_digest=_digest(base),
    )


def _event_payload_without_digest(timeline: TickerEventTimeline) -> dict[str, Any]:
    payload = asdict(timeline)
    payload.pop("timeline_semantic_digest")
    return payload


def build_supporting_audit(timeline: TickerEventTimeline, source_binding: SourceIdentityBinding) -> TickerEventAuditEvidence:
    findings: tuple[str, ...]
    if timeline.in_range_event_count:
        status = TICKER_EVENT_CHANGE_REQUIRES_SEGMENT_REVIEW
        combined = IDENTITY_CONTINUITY_REQUIRES_TICKER_EVENT_SEGMENT_REVIEW
        findings = ("TICKER_CHANGE_EVENT_WITHIN_CONTRACT_RANGE",)
    else:
        status = TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE
        combined = IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE
        findings = (NO_TICKER_CHANGE_EVENTS_RETURNED,) if timeline.event_count == 0 else ("NO_REPORTED_IN_RANGE_TICKER_CHANGE",)
    payload = {
        "schema_version": "marketflow.ticker_event_audit_candidate.v1",
        "source_identity_run_id": source_binding.source_identity_run_id,
        "source_continuity_artifact_id": source_binding.source_continuity_artifact_id,
        "source_continuity_status": source_binding.source_continuity_status,
        "source_continuity_semantic_digest": source_binding.source_continuity_semantic_digest,
        "start_snapshot_semantic_digest": source_binding.start_snapshot_semantic_digest,
        "end_snapshot_semantic_digest": source_binding.end_snapshot_semantic_digest,
        "contract_start_date": START_DATE,
        "contract_end_date": END_DATE,
        "audit_status": status,
        "combined_identity_candidate_status": combined,
        "fixed_findings": list(findings),
        "event_count": timeline.event_count,
        "pre_range_event_count": timeline.pre_range_event_count,
        "in_range_event_count": timeline.in_range_event_count,
        "post_range_event_count": timeline.post_range_event_count,
        "endpoint_stability": ENDPOINT_STABILITY_EXPERIMENTAL,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "identity_freeze_eligibility": False,
        "strategy_enabled": False,
    }
    return TickerEventAuditEvidence(
        schema_version=str(payload["schema_version"]),
        source_identity_run_id=source_binding.source_identity_run_id,
        source_continuity_artifact_id=source_binding.source_continuity_artifact_id,
        source_continuity_status=source_binding.source_continuity_status,
        source_continuity_semantic_digest=source_binding.source_continuity_semantic_digest,
        start_snapshot_semantic_digest=source_binding.start_snapshot_semantic_digest,
        end_snapshot_semantic_digest=source_binding.end_snapshot_semantic_digest,
        contract_start_date=START_DATE,
        contract_end_date=END_DATE,
        audit_status=status,
        combined_identity_candidate_status=combined,
        fixed_findings=findings,
        event_count=timeline.event_count,
        pre_range_event_count=timeline.pre_range_event_count,
        in_range_event_count=timeline.in_range_event_count,
        post_range_event_count=timeline.post_range_event_count,
        endpoint_stability=ENDPOINT_STABILITY_EXPERIMENTAL,
        canonical_eligibility=False,
        registry_eligibility=False,
        identity_freeze_eligibility=False,
        strategy_enabled=False,
        audit_semantic_digest=_digest(payload),
    )


def _audit_payload_without_digest(audit: TickerEventAuditEvidence) -> dict[str, Any]:
    payload = asdict(audit)
    payload.pop("audit_semantic_digest")
    return payload


def _query_string(pairs: tuple[tuple[str, str], ...]) -> str:
    for key, value in pairs:
        if key.lower() in {"apikey", "api_key", "token", "access_token", "authorization", "auth", "key"}:
            raise TickerEventAuditError("credential-like query parameter is prohibited")
        if any(char in value for char in ("\r", "\n", "\x00")):
            raise TickerEventAuditError("query parameter contains prohibited control characters")
    return "&".join(f"{key}={value}" for key, value in pairs)


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


class TickerEventsTransport:
    """One-round-trip Massive.com Ticker Events transport."""

    def __init__(self, *, api_key: ProviderApiKey, http_transport: httpx.BaseTransport | None = None) -> None:
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

    def prepare_request(self) -> PreparedTickerEventsRequest:
        if TICKER_EVENTS_PATH != f"/vX/reference/tickers/{QUERY_IDENTIFIER}/events":
            raise TickerEventAuditError("Ticker Events path/identifier mismatch")
        query = _query_string(TICKER_EVENTS_QUERY)
        url = f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{TICKER_EVENTS_PATH}?{query}"
        return PreparedTickerEventsRequest("GET", url, _public_headers(), TICKER_EVENTS_PATH, TICKER_EVENTS_QUERY)

    def send(self) -> bytes:
        request = self.prepare_request()
        self._call_count += 1
        try:
            self._client.cookies.clear()
            response = self._client.request(request.method, request.url, headers=_headers(self._api_key))
            self._client.cookies.clear()
        except httpx.TimeoutException as exc:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_TRANSPORT_FAILED) from exc
        except (httpx.NetworkError, httpx.RemoteProtocolError, httpx.TransportError) as exc:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_TRANSPORT_FAILED) from exc
        if response.status_code in {401, 403}:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED)
        if response.status_code != 200:
            raise TickerEventAuditError(TICKER_EVENT_ENDPOINT_UNAVAILABLE)
        content_type = response.headers.get("Content-Type")
        if content_type is not None and content_type.split(";", 1)[0].strip().lower() != "application/json":
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_RESPONSE_REJECTED)
        return response.content


def _safe_ref_to_path(root: str | Path, ref: str) -> Path:
    try:
        return identity._safe_ref_to_path(root, ref)
    except identity.InstrumentIdentityError as exc:
        raise TickerEventAuditError(str(exc)) from exc


def _safe_relative_path(path: str | Path, root: str | Path) -> str:
    try:
        return identity._safe_relative_path(path, root)
    except identity.InstrumentIdentityError as exc:
        raise TickerEventAuditError(str(exc)) from exc


def _validate_regular_file(path: Path, root: Path) -> None:
    try:
        identity._validate_regular_file(path, root)
    except identity.InstrumentIdentityError as exc:
        raise TickerEventAuditError(str(exc)) from exc


def _validated_runtime_root(run_root: str | Path, *, repository_root: Path | None = None) -> Path:
    try:
        return identity._validated_runtime_root(run_root, repository_root=repository_root)
    except identity.InstrumentIdentityError as exc:
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_RUNTIME_ROOT_INVALID) from exc


def _repository_root() -> Path:
    try:
        return identity._repository_root()
    except identity.InstrumentIdentityError as exc:
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_REPOSITORY_ROOT_UNRESOLVED) from exc


def _ticker_event_runtime_root(*, repository_root: Path | None = None) -> Path:
    repo_root = repository_root.resolve(strict=True) if repository_root is not None else _repository_root()
    return _validated_runtime_root(repo_root / TICKER_EVENT_RUNTIME_ROOT, repository_root=repo_root)


def _validate_artifact_writer_readiness(runtime_root: Path, repository_root: Path) -> None:
    try:
        identity._validate_artifact_writer_readiness(runtime_root, repository_root)
    except identity.InstrumentIdentityError as exc:
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_ARTIFACT_WRITER_UNREADY) from exc


def _validate_source_defined_dependencies() -> None:
    if not callable(getattr(httpx, "Client", None)) or not callable(ProviderApiKey):
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_DEPENDENCY_INVALID)


def _opaque(value: str, field_name: str) -> str:
    try:
        return identity._opaque(value, field_name)
    except identity.InstrumentIdentityError as exc:
        raise TickerEventAuditError(str(exc)) from exc


def _created_at_utc(value: str | None = None) -> str:
    try:
        return identity._created_at_utc(value)
    except identity.InstrumentIdentityError as exc:
        raise TickerEventAuditError(str(exc)) from exc


def _identity_payload_ref_for_manifest(manifest: Mapping[str, Any], refs_by_id: Mapping[str, str], root: Path) -> str:
    artifact_id = str(manifest["artifact_id"])
    try:
        return refs_by_id[artifact_id]
    except KeyError as exc:
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID) from exc


def _validate_identity_input_refs(
    manifest: Mapping[str, Any],
    *,
    root: Path,
    expected_ids: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    input_ids = list(manifest["input_artifact_ids"])
    input_refs = list(manifest["input_manifest_refs"])
    if expected_ids is not None and input_ids != list(expected_ids):
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
    if len(input_ids) != len(input_refs):
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
    loaded: list[dict[str, Any]] = []
    for expected_id, ref in zip(input_ids, input_refs):
        input_manifest = identity.load_identity_manifest(str(ref), run_root=root)
        if input_manifest["artifact_id"] != expected_id:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        loaded.append(input_manifest)
    return loaded


def _validate_false_identity_flags(payload: Mapping[str, Any]) -> None:
    for key in ("canonical_eligibility", "registry_eligibility", "generation_freeze_eligibility", "strategy_enabled"):
        if payload.get(key) is not False:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)


def _validate_continuity_payload_digest(payload: Mapping[str, Any]) -> None:
    expected = payload.get("continuity_digest")
    if type(expected) is not str or len(expected) != 64:
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
    base = dict(payload)
    base.pop("continuity_digest", None)
    base.pop("artifact_payload_schema", None)
    if identity._digest(base) != expected:
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)


def validate_accepted_source_identity_evidence(*, identity_run_root: str | Path | None = None) -> SourceIdentityBinding:
    try:
        root = Path(identity_run_root) if identity_run_root is not None else identity._identity_runtime_root()
        run_dir = identity._safe_ref_to_path(root, SOURCE_IDENTITY_RUN_ID)
        if not run_dir.is_dir():
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        manifest_refs = [path.relative_to(root).as_posix() for path in sorted(run_dir.rglob("*.manifest.json"))]
        manifests = [identity.load_identity_manifest(ref, run_root=root) for ref in manifest_refs]
        counts: dict[str, int] = {}
        manifest_by_id: dict[str, dict[str, Any]] = {}
        manifest_ref_by_id: dict[str, str] = {}
        for manifest_ref, manifest in zip(manifest_refs, manifests):
            identity.validate_identity_manifest(manifest, run_root=root)
            if manifest["run_id"] != SOURCE_IDENTITY_RUN_ID:
                raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
            counts[manifest["artifact_type"]] = counts.get(manifest["artifact_type"], 0) + 1
            if manifest["artifact_id"] in manifest_by_id:
                raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
            manifest_by_id[manifest["artifact_id"]] = manifest
            manifest_ref_by_id[manifest["artifact_id"]] = manifest_ref
        expected_counts = {
            identity.TICKER_OVERVIEW_RAW_RESPONSE: 2,
            identity.TICKER_OVERVIEW_SNAPSHOT: 2,
            identity.IDENTITY_CONTINUITY_CANDIDATE: 1,
            identity.INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT: 1,
        }
        if len(manifests) != 6 or counts != expected_counts:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        continuity_manifest = manifest_by_id.get(SOURCE_CONTINUITY_ARTIFACT_ID)
        if continuity_manifest is None or continuity_manifest["artifact_type"] != identity.IDENTITY_CONTINUITY_CANDIDATE:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        continuity_ref = _identity_payload_ref_for_manifest(continuity_manifest, manifest_ref_by_id, root)
        continuity_payload = identity.load_identity_payload(continuity_ref, run_root=root)
        if continuity_payload["schema_version"] != "marketflow.instrument_identity_continuity_candidate.v1":
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        if continuity_payload["continuity_status"] != SOURCE_CONTINUITY_STATUS:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        if continuity_payload["ticker_event_audit_status"] != identity.TICKER_EVENT_AUDIT_NOT_IMPLEMENTED:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        if continuity_payload["critical_field_status"] != "CRITICAL_FIELDS_MATCH":
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        if continuity_payload["start_identity_projection_digest"] != SOURCE_START_SNAPSHOT_DIGEST:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        if continuity_payload["end_identity_projection_digest"] != SOURCE_END_SNAPSHOT_DIGEST:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        _validate_false_identity_flags(continuity_payload)
        _validate_continuity_payload_digest(continuity_payload)

        snapshot_payloads: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for manifest_ref, manifest in zip(manifest_refs, manifests):
            if manifest["artifact_type"] == identity.TICKER_OVERVIEW_SNAPSHOT:
                snapshot_payloads.append((manifest, identity.load_identity_payload(manifest_ref, run_root=root)))
                raw_inputs = _validate_identity_input_refs(manifest, root=root)
                if len(raw_inputs) != 1 or raw_inputs[0]["artifact_type"] != identity.TICKER_OVERVIEW_RAW_RESPONSE:
                    raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        if len(snapshot_payloads) != 2:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        snapshots = {payload["as_of_date"]: (manifest, payload) for manifest, payload in snapshot_payloads}
        start_manifest, start_payload = snapshots[START_DATE]
        end_manifest, end_payload = snapshots[END_DATE]
        for payload, expected_digest in ((start_payload, SOURCE_START_SNAPSHOT_DIGEST), (end_payload, SOURCE_END_SNAPSHOT_DIGEST)):
            if payload["identity_projection_digest"] != expected_digest:
                raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
            if payload["ticker"] != TICKER_CONTEXT or payload["composite_figi"] != QUERY_IDENTIFIER:
                raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
            if payload["share_class_figi"] != SHARE_CLASS_FIGI_CONTEXT:
                raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
            if payload["primary_exchange"] != PRIMARY_EXCHANGE_CONTEXT or payload["type"] != SECURITY_TYPE_CONTEXT:
                raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        continuity_inputs = _validate_identity_input_refs(
            continuity_manifest,
            root=root,
            expected_ids=(start_manifest["artifact_id"], end_manifest["artifact_id"]),
        )
        if [item["artifact_type"] for item in continuity_inputs] != [identity.TICKER_OVERVIEW_SNAPSHOT, identity.TICKER_OVERVIEW_SNAPSHOT]:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        receipt_manifests = [manifest for manifest in manifests if manifest["artifact_type"] == identity.INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT]
        receipt_manifest = receipt_manifests[0]
        receipt_inputs = _validate_identity_input_refs(receipt_manifest, root=root, expected_ids=(SOURCE_CONTINUITY_ARTIFACT_ID,))
        if len(receipt_inputs) != 1 or receipt_inputs[0]["artifact_type"] != identity.IDENTITY_CONTINUITY_CANDIDATE:
            raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        receipt_ref = _identity_payload_ref_for_manifest(receipt_manifest, manifest_ref_by_id, root)
        receipt_payload = identity.load_identity_payload(receipt_ref, run_root=root)
        expected_receipt = {
            "status": "INSTRUMENT_IDENTITY_EVIDENCE_READY",
            "classification": identity.PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL,
            "run_id": SOURCE_IDENTITY_RUN_ID,
            "ticker": TICKER_CONTEXT,
            "start_snapshot_date": START_DATE,
            "end_snapshot_date": END_DATE,
            "start_snapshot_artifact_id": start_manifest["artifact_id"],
            "end_snapshot_artifact_id": end_manifest["artifact_id"],
            "continuity_status": SOURCE_CONTINUITY_STATUS,
            "start_snapshot_semantic_digest": SOURCE_START_SNAPSHOT_DIGEST,
            "end_snapshot_semantic_digest": SOURCE_END_SNAPSHOT_DIGEST,
            "ticker_event_audit_status": identity.TICKER_EVENT_AUDIT_NOT_IMPLEMENTED,
        }
        for key, expected in expected_receipt.items():
            if receipt_payload.get(key) != expected:
                raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID)
        _validate_false_identity_flags(receipt_payload)
        return SourceIdentityBinding(
            source_identity_run_id=SOURCE_IDENTITY_RUN_ID,
            source_continuity_artifact_id=SOURCE_CONTINUITY_ARTIFACT_ID,
            source_continuity_status=SOURCE_CONTINUITY_STATUS,
            source_continuity_semantic_digest=continuity_manifest["semantic_payload_digest"],
            start_snapshot_artifact_id=start_manifest["artifact_id"],
            end_snapshot_artifact_id=end_manifest["artifact_id"],
            start_snapshot_semantic_digest=SOURCE_START_SNAPSHOT_DIGEST,
            end_snapshot_semantic_digest=SOURCE_END_SNAPSHOT_DIGEST,
            ticker=TICKER_CONTEXT,
            composite_figi=QUERY_IDENTIFIER,
            share_class_figi=SHARE_CLASS_FIGI_CONTEXT,
            primary_exchange=PRIMARY_EXCHANGE_CONTEXT,
            security_type=SECURITY_TYPE_CONTEXT,
        )
    except (identity.InstrumentIdentityError, KeyError, IndexError) as exc:
        raise TickerEventAuditError(TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID) from exc


def _synthetic_source_binding() -> SourceIdentityBinding:
    return SourceIdentityBinding(
        source_identity_run_id=SOURCE_IDENTITY_RUN_ID,
        source_continuity_artifact_id=SOURCE_CONTINUITY_ARTIFACT_ID,
        source_continuity_status=SOURCE_CONTINUITY_STATUS,
        source_continuity_semantic_digest="0" * 64,
        start_snapshot_artifact_id="ident-art-start-snapshot",
        end_snapshot_artifact_id="ident-art-end-snapshot",
        start_snapshot_semantic_digest=SOURCE_START_SNAPSHOT_DIGEST,
        end_snapshot_semantic_digest=SOURCE_END_SNAPSHOT_DIGEST,
        ticker=TICKER_CONTEXT,
        composite_figi=QUERY_IDENTIFIER,
        share_class_figi=SHARE_CLASS_FIGI_CONTEXT,
        primary_exchange=PRIMARY_EXCHANGE_CONTEXT,
        security_type=SECURITY_TYPE_CONTEXT,
    )


def create_ticker_event_run(
    *,
    run_root: str | Path | None = None,
    run_id: str | None = None,
    run_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> TickerEventRunContext:
    root = _validated_runtime_root(run_root) if run_root is not None else _ticker_event_runtime_root()
    root.mkdir(parents=True, exist_ok=True)
    identity._reject_reparse_components(root.resolve(strict=True))
    run_id_text = _opaque(run_id or (run_id_factory() if run_id_factory else f"tkev-{uuid.uuid4().hex}"), "run_id")
    run_dir = root / run_id_text
    try:
        run_dir.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        raise TickerEventAuditError("ticker-event run directory already exists") from None
    return TickerEventRunContext(run_id_text, root, run_dir, _created_at_utc(created_at_utc))


def _write_temp_bytes(directory: Path, payload: bytes, suffix: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".tmp-", suffix=suffix, dir=str(directory))
    with os.fdopen(fd, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    return Path(temp_name)


def _install_without_replace(temp_path: Path, final_path: Path) -> None:
    if final_path.exists():
        raise TickerEventAuditError("ticker-event artifact already exists")
    try:
        os.link(temp_path, final_path)
    except OSError:
        with final_path.open("xb") as final_handle, temp_path.open("rb") as temp_handle:
            shutil.copyfileobj(temp_handle, final_handle)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def _artifact_payload(value: TickerEventTimeline | TickerEventAuditEvidence | dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, TickerEventTimeline):
        return _event_payload_without_digest(value) | {"timeline_semantic_digest": value.timeline_semantic_digest}
    if isinstance(value, TickerEventAuditEvidence):
        return _audit_payload_without_digest(value) | {"audit_semantic_digest": value.audit_semantic_digest}
    return _canonical(value)


def _artifact_bytes_and_metadata(payload: TickerEventTimeline | TickerEventAuditEvidence | dict[str, Any] | bytes, artifact_type: str) -> tuple[bytes, str, str]:
    if isinstance(payload, bytes):
        if artifact_type != TICKER_EVENTS_RAW_RESPONSE:
            raise TickerEventAuditError("raw bytes are only valid for Ticker Events raw response artifacts")
        digest = sha256_bytes(payload)
        return payload, digest, PAYLOAD_MEDIA_TYPE_PROVIDER_RAW_BYTES
    if artifact_type == TICKER_EVENTS_RAW_RESPONSE:
        raise TickerEventAuditError("Ticker Events raw response artifacts require raw bytes")
    payload_data = _artifact_payload(payload)
    return canonical_json_bytes(payload_data), semantic_digest(payload_data), PAYLOAD_MEDIA_TYPE_CANONICAL_JSON


def _lineage_ids(input_manifests: Iterable[dict[str, Any]]) -> list[str]:
    ids: list[str] = []
    for manifest in input_manifests:
        artifact_id = str(manifest["artifact_id"])
        if artifact_id not in ids:
            ids.append(artifact_id)
        for item in manifest.get("lineage_artifact_ids") or []:
            if str(item) not in ids:
                ids.append(str(item))
    return ids


def commit_ticker_event_artifact(
    *,
    payload: TickerEventTimeline | TickerEventAuditEvidence | dict[str, Any] | bytes,
    artifact_type: str,
    context: TickerEventRunContext,
    source_binding: SourceIdentityBinding,
    artifact_id: str | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    input_manifests: tuple[dict[str, Any], ...] = (),
    input_manifest_refs: tuple[str, ...] = (),
) -> dict[str, Any]:
    if artifact_type not in STAGE_BY_TYPE:
        raise TickerEventAuditError("unsupported ticker-event artifact type")
    artifact_id_text = _opaque(artifact_id or (artifact_id_factory() if artifact_id_factory else f"tkev-art-{uuid.uuid4().hex}"), "artifact_id")
    stage = STAGE_BY_TYPE[artifact_type]
    stage_dir = context.run_dir / STAGE_DIRECTORY[stage]
    payload_suffix = ".bin" if artifact_type == TICKER_EVENTS_RAW_RESPONSE else ".json"
    payload_path = stage_dir / f"{artifact_id_text}{payload_suffix}"
    manifest_path = stage_dir / f"{artifact_id_text}{payload_suffix}.manifest.json"
    if payload_path.exists() or manifest_path.exists():
        raise TickerEventAuditError("artifact output already exists")
    payload_bytes, semantic_payload_digest, media_type = _artifact_bytes_and_metadata(payload, artifact_type)
    input_ids = [str(item["artifact_id"]) for item in input_manifests]
    if len(input_ids) != len(set(input_ids)) or len(input_ids) != len(input_manifest_refs):
        raise TickerEventAuditError("input manifests must reconcile")
    manifest = {
        "schema_version": TICKER_EVENT_AUDIT_ARTIFACT_MANIFEST_SCHEMA_VERSION,
        "artifact_id": artifact_id_text,
        "run_id": context.run_id,
        "artifact_type": artifact_type,
        "stage": stage,
        "created_at_utc": context.created_at_utc,
        "ticker_event_audit_specification_digest": ticker_event_audit_specification_digest(),
        "provider": "MASSIVE.COM",
        "identifier_type": QUERY_IDENTIFIER_TYPE,
        "query_identifier": QUERY_IDENTIFIER,
        "source_identity_run_id": source_binding.source_identity_run_id,
        "source_continuity_artifact_id": source_binding.source_continuity_artifact_id,
        "source_continuity_semantic_digest": source_binding.source_continuity_semantic_digest,
        "payload_ref": _safe_relative_path(payload_path, context.run_root),
        "payload_sha256": sha256_bytes(payload_bytes),
        "payload_byte_size": len(payload_bytes),
        "payload_media_type": media_type,
        "semantic_payload_digest": semantic_payload_digest,
        "input_artifact_ids": input_ids,
        "input_manifest_refs": list(input_manifest_refs),
        "lineage_artifact_ids": _lineage_ids(input_manifests),
        "external_source_artifact_ids": [source_binding.source_continuity_artifact_id],
    }
    validate_ticker_event_manifest_shape_without_payload(manifest)
    temp_payload = _write_temp_bytes(stage_dir, payload_bytes, ".payload.tmp")
    try:
        _install_without_replace(temp_payload, payload_path)
        temp_manifest = _write_temp_bytes(stage_dir, canonical_json_bytes(manifest), ".manifest.tmp")
        _install_without_replace(temp_manifest, manifest_path)
    except Exception:
        if payload_path.exists() and not manifest_path.exists():
            try:
                payload_path.unlink()
            except OSError:
                pass
        raise
    saved = load_ticker_event_manifest(_safe_relative_path(manifest_path, context.run_root), run_root=context.run_root)
    return {
        "manifest": saved,
        "manifest_ref": _safe_relative_path(manifest_path, context.run_root),
        "payload_ref": saved["payload_ref"],
        "manifest_path": manifest_path,
        "payload_path": payload_path,
    }


def _manifest_path_from_payload_ref(root: Path, payload_ref: str) -> Path:
    payload_path = _safe_ref_to_path(root, payload_ref)
    return payload_path.with_suffix(payload_path.suffix + ".manifest.json")


def _hex_digest(value: Any, field_name: str) -> str:
    if type(value) is not str or len(value) != 64 or not all(char in "0123456789abcdef" for char in value):
        raise TickerEventAuditError(f"ticker-event manifest {field_name} invalid")
    return value


def _manifest_text_list(manifest: Mapping[str, Any], key: str, *, refs: bool = False) -> list[str]:
    value = manifest[key]
    if not isinstance(value, list):
        raise TickerEventAuditError("ticker-event manifest lineage fields must be lists")
    items: list[str] = []
    for item in value:
        if type(item) is not str:
            raise TickerEventAuditError("ticker-event manifest lineage entries must be text")
        if refs:
            _safe_ref_to_path(".", item)
        else:
            _opaque(item, key[:-1] if key.endswith("s") else key)
        if item in items:
            raise TickerEventAuditError("ticker-event manifest lineage entries must be unique")
        items.append(item)
    return items


def validate_ticker_event_manifest_shape_without_payload(manifest: dict[str, Any]) -> None:
    if set(manifest) != MANIFEST_FIELDS:
        raise TickerEventAuditError("ticker-event manifest fields must match schema exactly")
    if manifest["schema_version"] != TICKER_EVENT_AUDIT_ARTIFACT_MANIFEST_SCHEMA_VERSION:
        raise TickerEventAuditError("unsupported ticker-event manifest schema")
    if manifest["artifact_type"] not in STAGE_BY_TYPE or manifest["stage"] != STAGE_BY_TYPE[manifest["artifact_type"]]:
        raise TickerEventAuditError("ticker-event artifact type/stage mismatch")
    _opaque(str(manifest["artifact_id"]), "artifact_id")
    _opaque(str(manifest["run_id"]), "run_id")
    if manifest["ticker_event_audit_specification_digest"] != ticker_event_audit_specification_digest():
        raise TickerEventAuditError("ticker-event specification digest mismatch")
    if manifest["provider"] != "MASSIVE.COM" or manifest["identifier_type"] != QUERY_IDENTIFIER_TYPE or manifest["query_identifier"] != QUERY_IDENTIFIER:
        raise TickerEventAuditError("ticker-event manifest provider/identifier mismatch")
    if manifest["source_identity_run_id"] != SOURCE_IDENTITY_RUN_ID or manifest["source_continuity_artifact_id"] != SOURCE_CONTINUITY_ARTIFACT_ID:
        raise TickerEventAuditError("ticker-event manifest source identity mismatch")
    _hex_digest(manifest["source_continuity_semantic_digest"], "source continuity semantic digest")
    if type(manifest["payload_ref"]) is not str:
        raise TickerEventAuditError("ticker-event manifest payload ref must be text")
    _safe_ref_to_path(".", manifest["payload_ref"])
    _hex_digest(manifest["payload_sha256"], "payload byte digest")
    _hex_digest(manifest["semantic_payload_digest"], "semantic payload digest")
    if type(manifest["payload_byte_size"]) is not int or manifest["payload_byte_size"] < 0:
        raise TickerEventAuditError("ticker-event manifest payload size invalid")
    expected_media_type = PAYLOAD_MEDIA_TYPE_PROVIDER_RAW_BYTES if manifest["artifact_type"] == TICKER_EVENTS_RAW_RESPONSE else PAYLOAD_MEDIA_TYPE_CANONICAL_JSON
    if manifest["payload_media_type"] != expected_media_type:
        raise TickerEventAuditError("ticker-event manifest media type invalid")
    input_ids = _manifest_text_list(manifest, "input_artifact_ids")
    input_refs = _manifest_text_list(manifest, "input_manifest_refs", refs=True)
    _manifest_text_list(manifest, "lineage_artifact_ids")
    external_ids = _manifest_text_list(manifest, "external_source_artifact_ids")
    if len(input_ids) != len(input_refs):
        raise TickerEventAuditError("ticker-event manifest inputs must reconcile")
    if external_ids != [SOURCE_CONTINUITY_ARTIFACT_ID]:
        raise TickerEventAuditError("ticker-event manifest external source lineage invalid")


def load_ticker_event_manifest(manifest_ref: str | Path, *, run_root: str | Path) -> dict[str, Any]:
    root = Path(run_root)
    path = _safe_ref_to_path(root, str(manifest_ref))
    _validate_regular_file(path, root)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TickerEventAuditError("ticker-event manifest must be a JSON object")
    validate_ticker_event_manifest_shape_without_payload(data)
    if path.resolve(strict=True) != _manifest_path_from_payload_ref(root, str(data["payload_ref"])).resolve(strict=True):
        raise TickerEventAuditError("ticker-event manifest path does not match payload reference")
    validate_ticker_event_manifest(data, run_root=root)
    return data


def validate_ticker_event_manifest(manifest: dict[str, Any], *, run_root: str | Path) -> None:
    validate_ticker_event_manifest_shape_without_payload(manifest)
    root = Path(run_root)
    input_manifests: list[dict[str, Any]] = []
    for expected_id, ref in zip(manifest["input_artifact_ids"], manifest["input_manifest_refs"]):
        input_manifest = load_ticker_event_manifest(ref, run_root=root)
        if input_manifest["artifact_id"] != expected_id:
            raise TickerEventAuditError("ticker-event manifest input reference mismatch")
        input_manifests.append(input_manifest)
    if manifest["lineage_artifact_ids"] != _lineage_ids(input_manifests):
        raise TickerEventAuditError("ticker-event manifest lineage mismatch")
    payload_path = _safe_ref_to_path(root, str(manifest["payload_ref"]))
    _validate_regular_file(payload_path, root)
    payload_bytes = payload_path.read_bytes()
    if len(payload_bytes) != manifest["payload_byte_size"]:
        raise TickerEventAuditError("ticker-event payload size mismatch")
    if sha256_bytes(payload_bytes) != manifest["payload_sha256"]:
        raise TickerEventAuditError("ticker-event payload byte digest mismatch")
    if manifest["artifact_type"] == TICKER_EVENTS_RAW_RESPONSE:
        semantic_payload_digest = sha256_bytes(payload_bytes)
    else:
        semantic_payload_digest = semantic_digest(json.loads(payload_bytes.decode("utf-8")))
    if semantic_payload_digest != manifest["semantic_payload_digest"]:
        raise TickerEventAuditError("ticker-event payload semantic digest mismatch")


def load_ticker_event_payload(manifest_ref: str | Path, *, run_root: str | Path) -> dict[str, Any]:
    manifest = load_ticker_event_manifest(manifest_ref, run_root=run_root)
    if manifest["artifact_type"] == TICKER_EVENTS_RAW_RESPONSE:
        raise TickerEventAuditError("raw Ticker Events artifacts must be loaded as bytes")
    payload_path = _safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    _validate_regular_file(payload_path, Path(run_root))
    return json.loads(payload_path.read_text(encoding="utf-8"))


def load_ticker_event_raw_bytes(manifest_ref: str | Path, *, run_root: str | Path) -> bytes:
    manifest = load_ticker_event_manifest(manifest_ref, run_root=run_root)
    if manifest["artifact_type"] != TICKER_EVENTS_RAW_RESPONSE:
        raise TickerEventAuditError("ticker-event artifact is not a raw response")
    payload_path = _safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    _validate_regular_file(payload_path, Path(run_root))
    return payload_path.read_bytes()


def sanitized_receipt(
    *,
    context: TickerEventRunContext,
    source_binding: SourceIdentityBinding,
    raw_manifest: dict[str, Any],
    timeline_manifest: dict[str, Any],
    audit_manifest: dict[str, Any],
    timeline: TickerEventTimeline,
    audit: TickerEventAuditEvidence,
) -> dict[str, Any]:
    return {
        "status": TICKER_EVENT_AUDIT_READY_NONCANONICAL,
        "audit_run_id": context.run_id,
        "specification_digest": ticker_event_audit_specification_digest(),
        "provider": "MASSIVE.COM",
        "identifier_type": QUERY_IDENTIFIER_TYPE,
        "composite_figi": QUERY_IDENTIFIER,
        "ticker_context": TICKER_CONTEXT,
        "contract_start_date": START_DATE,
        "contract_end_date": END_DATE,
        "source_identity_run_id": source_binding.source_identity_run_id,
        "source_continuity_artifact_id": source_binding.source_continuity_artifact_id,
        "source_continuity_semantic_digest": source_binding.source_continuity_semantic_digest,
        "raw_response_artifact_id": raw_manifest["artifact_id"],
        "raw_response_artifact_digest": raw_manifest["payload_sha256"],
        "timeline_artifact_id": timeline_manifest["artifact_id"],
        "timeline_artifact_digest": timeline.timeline_semantic_digest,
        "audit_artifact_id": audit_manifest["artifact_id"],
        "event_count": timeline.event_count,
        "pre_range_event_count": timeline.pre_range_event_count,
        "in_range_event_count": timeline.in_range_event_count,
        "post_range_event_count": timeline.post_range_event_count,
        "events": [asdict(event) for event in timeline.events],
        "audit_status": audit.audit_status,
        "combined_identity_candidate_status": audit.combined_identity_candidate_status,
        "fixed_findings": list(audit.fixed_findings),
        "endpoint_stability": ENDPOINT_STABILITY_EXPERIMENTAL,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "identity_freeze_eligibility": False,
        "strategy_enabled": False,
    }


def ticker_event_audit_plan() -> dict[str, Any]:
    spec = default_ticker_event_audit_specification()
    return {
        "status": "TICKER_EVENT_AUDIT_PLAN_READY",
        "schema_version": spec.schema_version,
        "classification": spec.classification,
        "provider": spec.provider,
        "endpoint_family": spec.endpoint_family,
        "endpoint_stability": spec.endpoint_stability,
        "query_identifier_type": spec.query_identifier_type,
        "query_identifier": spec.query_identifier,
        "ticker_context": spec.ticker_context,
        "start_date": spec.start_date,
        "end_date": spec.end_date,
        "event_types": list(spec.event_types),
        "specification_digest": ticker_event_audit_specification_digest(),
        "source_identity_run_id": spec.source_identity_run_id,
        "source_continuity_artifact_id": spec.source_continuity_artifact_id,
        "live_audit_occurred": False,
        "automatic_stitching": False,
        "writes_artifacts": False,
        "credential_required": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "identity_freeze_eligibility": False,
        "strategy_enabled": False,
    }


def _fixture_response(events: list[dict[str, Any]] | None = None, *, include_events: bool = True, status: str = PROVIDER_STATUS_OK) -> bytes:
    results: dict[str, Any] = {"name": "not public evidence"}
    if include_events:
        results["events"] = events or []
    return canonical_json_bytes({"status": status, "request_id": "mock-request-not-public", "results": results})


def _run_ticker_event_audit(
    confirmation: str,
    *,
    api_key: ProviderApiKey,
    http_transport: httpx.BaseTransport | None = None,
    run_root: str | Path | None = None,
    run_id_factory: Callable[[], str] | None = None,
    source_binding: SourceIdentityBinding | None = None,
    _transport_factory: Callable[..., TickerEventsTransport] = TickerEventsTransport,
) -> dict[str, Any]:
    if confirmation != _confirmation_phrase():
        return {
            "status": "TICKER_EVENT_AUDIT_BLOCKED",
            "finding": "TICKER_EVENT_AUDIT_CONFIRMATION_REJECTED",
            "specification_digest": ticker_event_audit_specification_digest(),
        }
    binding = source_binding or validate_accepted_source_identity_evidence()
    context = create_ticker_event_run(run_root=run_root, run_id_factory=run_id_factory)
    transport = _transport_factory(api_key=api_key, http_transport=http_transport)
    try:
        try:
            body = transport.send()
        except TickerEventAuditError as exc:
            raise TickerEventAuditRunError(
                str(exc),
                provider_request_count=transport.call_count,
                runtime_artifact_written=False,
            ) from exc
    finally:
        transport.close()
    raw_written = False
    try:
        raw = commit_ticker_event_artifact(payload=body, artifact_type=TICKER_EVENTS_RAW_RESPONSE, context=context, source_binding=binding)
        raw_written = True
        timeline = parse_ticker_events_response(load_ticker_event_raw_bytes(raw["manifest_ref"], run_root=context.run_root), source_binding=binding)
        timeline_artifact = commit_ticker_event_artifact(
            payload=timeline,
            artifact_type=TICKER_EVENT_TIMELINE,
            context=context,
            source_binding=binding,
            input_manifests=(raw["manifest"],),
            input_manifest_refs=(raw["manifest_ref"],),
        )
        audit = build_supporting_audit(timeline, binding)
        audit_artifact = commit_ticker_event_artifact(
            payload=audit,
            artifact_type=TICKER_EVENT_AUDIT_CANDIDATE,
            context=context,
            source_binding=binding,
            input_manifests=(raw["manifest"], timeline_artifact["manifest"]),
            input_manifest_refs=(raw["manifest_ref"], timeline_artifact["manifest_ref"]),
        )
        receipt = sanitized_receipt(
            context=context,
            source_binding=binding,
            raw_manifest=raw["manifest"],
            timeline_manifest=timeline_artifact["manifest"],
            audit_manifest=audit_artifact["manifest"],
            timeline=timeline,
            audit=audit,
        )
        receipt_artifact = commit_ticker_event_artifact(
            payload=receipt,
            artifact_type=TICKER_EVENT_AUDIT_RECEIPT,
            context=context,
            source_binding=binding,
            input_manifests=(audit_artifact["manifest"],),
            input_manifest_refs=(audit_artifact["manifest_ref"],),
        )
    except TickerEventAuditError as exc:
        raise TickerEventAuditRunError(
            str(exc),
            provider_request_count=transport.call_count,
            runtime_artifact_written=raw_written,
        ) from exc
    return receipt | {
        "receipt_artifact_id": receipt_artifact["manifest"]["artifact_id"],
        "provider_request_count": transport.call_count,
    }


def ticker_event_audit_self_check() -> dict[str, Any]:
    receipts: list[dict[str, Any]] = []
    cases = [
        ("no_events", _fixture_response([])),
        ("pre_range_event", _fixture_response([{"date": "2021-12-31", "type": EVENT_TYPE_TICKER_CHANGE, "ticker_change": {"ticker": "OLD"}}])),
        ("in_range_event", _fixture_response([{"date": "2023-06-01", "type": EVENT_TYPE_TICKER_CHANGE, "ticker_change": {"ticker": "AAPL1"}}])),
        ("post_range_event", _fixture_response([{"date": "2026-01-01", "type": EVENT_TYPE_TICKER_CHANGE, "ticker_change": {"ticker": "AAPL2"}}])),
    ]
    binding = _synthetic_source_binding()
    with tempfile.TemporaryDirectory() as tmp:
        for index, (name, body) in enumerate(cases, start=1):
            observed: list[str] = []

            def handler(request: httpx.Request, body: bytes = body) -> httpx.Response:
                observed.append(str(request.url))
                return httpx.Response(200, headers={"Content-Type": "application/json"}, content=body)

            receipt = _run_ticker_event_audit(
                _confirmation_phrase(),
                api_key=ProviderApiKey("fictional-self-check-key"),
                http_transport=httpx.MockTransport(handler),
                run_root=Path(tmp),
                run_id_factory=lambda name=name: f"tkev-self-check-{name}",
                source_binding=binding,
            )
            receipts.append({"case": name, "observed_request_count": len(observed), "audit_status": receipt["audit_status"], "combined_identity_candidate_status": receipt["combined_identity_candidate_status"]})
        incomplete_status = None
        try:
            parse_ticker_events_response(_fixture_response(include_events=False), source_binding=binding)
        except TickerEventAuditError as exc:
            incomplete_status = str(exc)
    return {
        "self_check_status": "TICKER_EVENT_AUDIT_SELF_CHECK_COMPLETE",
        "mock_transport_only": True,
        "persistent_artifacts_written": False,
        "endpoint_stability": ENDPOINT_STABILITY_EXPERIMENTAL,
        "cases": receipts,
        "incomplete_response_status": incomplete_status,
    }


def _local_preflight() -> dict[str, Any]:
    repository_root = _repository_root()
    validate_accepted_source_identity_evidence()
    runtime_root = _ticker_event_runtime_root(repository_root=repository_root)
    _validate_artifact_writer_readiness(runtime_root, repository_root)
    _validate_source_defined_dependencies()
    return {
        "status": TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_READY,
        "repository_root_status": "TICKER_EVENT_AUDIT_REPOSITORY_ROOT_RESOLVED",
        "source_identity_status": "TICKER_EVENT_AUDIT_SOURCE_IDENTITY_VALIDATED",
        "runtime_root_status": "TICKER_EVENT_AUDIT_RUNTIME_ROOT_READY",
        "runtime_root_ref": TICKER_EVENT_RUNTIME_ROOT.as_posix(),
        "artifact_writer_status": "TICKER_EVENT_AUDIT_ARTIFACT_WRITER_READY",
        "credential_required": False,
        "writes_artifacts": False,
    }


def _confirmation_phrase() -> str:
    return CONFIRMATION_PREFIX + ticker_event_audit_specification_digest()[:12]


def ticker_event_audit_confirmation_phrase() -> str:
    return _confirmation_phrase()


def _failure_receipt(
    status: str,
    *,
    failure_category: str,
    credential_prompted: bool,
    provider_request_count: int = 0,
    runtime_artifact_written: bool = False,
) -> dict[str, Any]:
    return {
        "status": status,
        "failure_category": failure_category,
        "credential_prompted": credential_prompted,
        "provider_request_count": provider_request_count,
        "runtime_artifact_written": runtime_artifact_written,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "identity_freeze_eligibility": False,
        "strategy_enabled": False,
        "endpoint_stability": ENDPOINT_STABILITY_EXPERIMENTAL,
    }


def _expected_failure_category(exc: TickerEventAuditError) -> str:
    text = str(exc)
    fixed = {
        TICKER_EVENT_AUDIT_REPOSITORY_ROOT_UNRESOLVED,
        TICKER_EVENT_AUDIT_RUNTIME_ROOT_INVALID,
        TICKER_EVENT_AUDIT_ARTIFACT_WRITER_UNREADY,
        TICKER_EVENT_AUDIT_SOURCE_IDENTITY_INVALID,
        TICKER_EVENT_AUDIT_SOURCE_DEPENDENCY_INVALID,
        TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED,
        TICKER_EVENT_AUDIT_TRANSPORT_FAILED,
        TICKER_EVENT_AUDIT_RESPONSE_REJECTED,
        TICKER_EVENT_ENDPOINT_UNAVAILABLE,
        TICKER_EVENT_EVIDENCE_INCOMPLETE,
    }
    return text if text in fixed else "TICKER_EVENT_AUDIT_EXPECTED_FAILURE"


def live_command(
    getpass_fn: Callable[[str], str] = getpass.getpass,
    *,
    _provider_key_factory: Callable[[str], ProviderApiKey] = ProviderApiKey,
    _http_transport: httpx.BaseTransport | None = None,
    _run_id_factory: Callable[[], str] | None = None,
    _transport_factory: Callable[..., TickerEventsTransport] = TickerEventsTransport,
    _preflight: Callable[[], Mapping[str, Any]] = _local_preflight,
) -> int:
    if not sys.stdin.isatty():
        print(json.dumps({"status": "TICKER_EVENT_AUDIT_BLOCKED", "finding": "TTY_REQUIRED"}, sort_keys=True, indent=2))
        return 2
    print(json.dumps(ticker_event_audit_plan(), sort_keys=True, indent=2))
    print(f"Required confirmation phrase: {_confirmation_phrase()}")
    confirmation = input("Type confirmation phrase: ")
    if confirmation != _confirmation_phrase():
        print(json.dumps({"status": "TICKER_EVENT_AUDIT_BLOCKED", "finding": "TICKER_EVENT_AUDIT_CONFIRMATION_REJECTED"}, sort_keys=True, indent=2))
        return 2
    try:
        _preflight()
    except TickerEventAuditError as exc:
        print(json.dumps(_failure_receipt(TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_FAILED, failure_category=_expected_failure_category(exc), credential_prompted=False), sort_keys=True, indent=2))
        return 2
    except Exception:
        print(json.dumps(_failure_receipt(TICKER_EVENT_AUDIT_LOCAL_PREFLIGHT_FAILED, failure_category=TICKER_EVENT_AUDIT_UNEXPECTED_FAILURE, credential_prompted=False), sort_keys=True, indent=2))
        return 2
    try:
        secret = getpass_fn("Massive.com API key: ")
        api_key = _provider_key_factory(secret)
    except MassiveTransportError:
        print(json.dumps(_failure_receipt(TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED, failure_category=TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED, credential_prompted=True), sort_keys=True, indent=2))
        return 2
    except Exception:
        print(json.dumps(_failure_receipt(TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED, failure_category=TICKER_EVENT_AUDIT_UNEXPECTED_FAILURE, credential_prompted=True), sort_keys=True, indent=2))
        return 2
    try:
        receipt = _run_ticker_event_audit(
            confirmation,
            api_key=api_key,
            http_transport=_http_transport,
            run_id_factory=_run_id_factory,
            _transport_factory=_transport_factory,
        )
    except TickerEventAuditRunError as exc:
        category = _expected_failure_category(exc)
        status = (
            TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED
            if category == TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED
            else TICKER_EVENT_AUDIT_TRANSPORT_FAILED
            if category in {TICKER_EVENT_AUDIT_TRANSPORT_FAILED, TICKER_EVENT_ENDPOINT_UNAVAILABLE}
            else TICKER_EVENT_AUDIT_RESPONSE_REJECTED
        )
        print(
            json.dumps(
                _failure_receipt(
                    status,
                    failure_category=category,
                    credential_prompted=True,
                    provider_request_count=exc.provider_request_count,
                    runtime_artifact_written=exc.runtime_artifact_written,
                ),
                sort_keys=True,
                indent=2,
            )
        )
        return 2
    except TickerEventAuditError as exc:
        category = _expected_failure_category(exc)
        status = (
            TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED
            if category == TICKER_EVENT_AUDIT_AUTHENTICATION_FAILED
            else TICKER_EVENT_AUDIT_TRANSPORT_FAILED
            if category == TICKER_EVENT_AUDIT_TRANSPORT_FAILED
            else TICKER_EVENT_AUDIT_RESPONSE_REJECTED
        )
        print(json.dumps(_failure_receipt(status, failure_category=category, credential_prompted=True), sort_keys=True, indent=2))
        return 2
    except Exception:
        print(json.dumps(_failure_receipt(TICKER_EVENT_AUDIT_RESPONSE_REJECTED, failure_category=TICKER_EVENT_AUDIT_UNEXPECTED_FAILURE, credential_prompted=True), sort_keys=True, indent=2))
        return 2
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0
