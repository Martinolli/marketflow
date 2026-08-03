"""Offline source-authority evidence for point-in-time instrument identity."""

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
    POOL_TIMEOUT_SECONDS,
    ProviderApiKey,
    READ_TIMEOUT_SECONDS,
    WRITE_TIMEOUT_SECONDS,
)


IDENTITY_SPECIFICATION_SCHEMA_VERSION = "marketflow.instrument_identity_specification.v1"
IDENTITY_ARTIFACT_MANIFEST_SCHEMA_VERSION = "marketflow.instrument_identity_artifact_manifest.v1"
PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL = "PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL"
TICKER_OVERVIEW_V3 = "TICKER_OVERVIEW_V3"
TICKER_OVERVIEW_RAW_RESPONSE = "TICKER_OVERVIEW_RAW_RESPONSE"
TICKER_OVERVIEW_SNAPSHOT = "TICKER_OVERVIEW_SNAPSHOT"
IDENTITY_CONTINUITY_CANDIDATE = "IDENTITY_CONTINUITY_CANDIDATE"
INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT = "INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT"
IDENTITY_RUNTIME_ROOT = Path(".marketflow") / "source_authority" / "identity" / "runs"
TICKER = "AAPL"
START_SNAPSHOT_DATE = "2022-01-01"
END_SNAPSHOT_DATE = "2025-12-31"
EXPECTED_MARKET = "stocks"
EXPECTED_LOCALE = "us"
EXPECTED_CURRENCY = "usd"
TICKER_OVERVIEW_PATH = f"/v3/reference/tickers/{TICKER}"
TICKER_EVENT_AUDIT_NOT_IMPLEMENTED = "TICKER_EVENT_AUDIT_NOT_IMPLEMENTED"
IDENTITY_CONTINUITY_SUPPORTED = "IDENTITY_CONTINUITY_SUPPORTED"
IDENTITY_CHANGE_REQUIRES_SEGMENT_REVIEW = "IDENTITY_CHANGE_REQUIRES_SEGMENT_REVIEW"
IDENTITY_EVIDENCE_INCOMPLETE = "IDENTITY_EVIDENCE_INCOMPLETE"
IDENTITY_EVIDENCE_CONFLICT = "IDENTITY_EVIDENCE_CONFLICT"
IDENTITY_SNAPSHOT_COMPLETE = "IDENTITY_SNAPSHOT_COMPLETE"
IDENTITY_SNAPSHOT_INCOMPLETE = "IDENTITY_SNAPSHOT_INCOMPLETE"
PRESENT = "PRESENT"
NOT_RETURNED = "NOT_RETURNED"
PROVIDER_STATUS_OK = "OK"
SANITIZATION = "SANITIZED_PUBLIC_IDENTITY_ONLY"
PAYLOAD_MEDIA_TYPE_CANONICAL_JSON = "application/vnd.marketflow.canonical+json"
PAYLOAD_MEDIA_TYPE_PROVIDER_RAW_BYTES = "application/vnd.marketflow.provider-raw+octet-stream"
CONFIRMATION_PREFIX = "RUN MARKETFLOW INSTRUMENT IDENTITY "
WINDOWS_REPARSE_POINT_ATTRIBUTE = 0x400
INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED = "INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED"
INSTRUMENT_IDENTITY_RUNTIME_ROOT_INVALID = "INSTRUMENT_IDENTITY_RUNTIME_ROOT_INVALID"
INSTRUMENT_IDENTITY_ARTIFACT_WRITER_UNREADY = "INSTRUMENT_IDENTITY_ARTIFACT_WRITER_UNREADY"
INSTRUMENT_IDENTITY_SOURCE_DEPENDENCY_INVALID = "INSTRUMENT_IDENTITY_SOURCE_DEPENDENCY_INVALID"
INSTRUMENT_IDENTITY_LOCAL_PREFLIGHT_FAILED = "INSTRUMENT_IDENTITY_LOCAL_PREFLIGHT_FAILED"
INSTRUMENT_IDENTITY_LOCAL_PREFLIGHT_READY = "INSTRUMENT_IDENTITY_LOCAL_PREFLIGHT_READY"
INSTRUMENT_IDENTITY_UNEXPECTED_FAILURE = "INSTRUMENT_IDENTITY_UNEXPECTED_FAILURE"
REPOSITORY_EVIDENCE_REFS = (
    "AGENTS.md",
    "requirements.txt",
    "marketflow/source_authority/instrument_identity.py",
    "config/fixed_date_acquisition_contract_v2_1.toml",
)

TOP_LEVEL_FIELDS = frozenset({"request_id", "status", "results", "count"})
RESULT_FIELDS = frozenset(
    {
        "active",
        "address",
        "branding",
        "cik",
        "composite_figi",
        "currency_name",
        "delisted_utc",
        "description",
        "homepage_url",
        "list_date",
        "locale",
        "market",
        "market_cap",
        "name",
        "phone_number",
        "primary_exchange",
        "round_lot",
        "share_class_figi",
        "share_class_shares_outstanding",
        "sic_code",
        "sic_description",
        "ticker",
        "ticker_root",
        "ticker_suffix",
        "total_employees",
        "type",
        "weighted_shares_outstanding",
    }
)
CRITICAL_FIELDS = (
    "ticker",
    "active",
    "market",
    "locale",
    "currency_name",
    "primary_exchange",
    "composite_figi",
    "share_class_figi",
    "type",
)
CONTINUITY_CRITICAL_FIELDS = (
    "ticker",
    "market",
    "locale",
    "currency_name",
    "primary_exchange",
    "composite_figi",
    "share_class_figi",
    "type",
)
CONTINUITY_SUPPORTING_FIELDS = ("cik", "active", "list_date", "delisted_utc")
MANIFEST_FIELDS = frozenset(
    {
        "schema_version",
        "artifact_id",
        "run_id",
        "artifact_type",
        "stage",
        "created_at_utc",
        "identity_specification_digest",
        "provider",
        "ticker",
        "as_of_date",
        "payload_ref",
        "payload_sha256",
        "payload_byte_size",
        "payload_media_type",
        "semantic_payload_digest",
        "input_artifact_ids",
        "input_manifest_refs",
        "lineage_artifact_ids",
    }
)
STAGE_BY_TYPE = {
    TICKER_OVERVIEW_RAW_RESPONSE: "ticker_overview_raw_response",
    TICKER_OVERVIEW_SNAPSHOT: "ticker_overview_snapshot",
    IDENTITY_CONTINUITY_CANDIDATE: "identity_continuity_candidate",
    INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT: "instrument_identity_receipt",
}
STAGE_DIRECTORY = {
    "ticker_overview_raw_response": "raw_response",
    "ticker_overview_snapshot": "snapshots",
    "identity_continuity_candidate": "continuity",
    "instrument_identity_receipt": "receipt",
}


class InstrumentIdentityError(ValueError):
    """Raised when instrument identity evidence fails closed."""


@dataclass(frozen=True, slots=True)
class InstrumentIdentitySpecification:
    schema_version: str
    classification: str
    provider: str
    endpoint_family: str
    ticker: str
    start_snapshot_date: str
    end_snapshot_date: str
    expected_market: str
    expected_locale: str
    expected_currency: str
    canonical_eligibility: bool
    registry_eligibility: bool
    generation_freeze_eligibility: bool
    strategy_enabled: bool


@dataclass(frozen=True, slots=True)
class PreparedTickerOverviewRequest:
    method: str
    url: str
    headers: Mapping[str, str]
    sanitized_url: str
    as_of_date: str


@dataclass(frozen=True, slots=True)
class IdentitySnapshot:
    schema_version: str
    as_of_date: str
    ticker: str | None
    active: bool | None
    market: str | None
    locale: str | None
    currency_name: str | None
    primary_exchange: str | None
    composite_figi: str | None
    share_class_figi: str | None
    type: str | None
    cik_status: str
    cik: str | None
    list_date_status: str
    list_date: str | None
    delisted_utc_status: str
    delisted_utc: str | None
    provider_status: str
    snapshot_status: str
    fixed_findings: tuple[str, ...]
    identity_projection_digest: str


@dataclass(frozen=True, slots=True)
class ContinuityEvidence:
    schema_version: str
    start_as_of_date: str
    end_as_of_date: str
    continuity_status: str
    ticker_event_audit_status: str
    critical_field_status: str
    supporting_field_status: str
    fixed_findings: tuple[str, ...]
    start_identity_projection_digest: str | None
    end_identity_projection_digest: str | None
    continuity_digest: str
    canonical_eligibility: bool
    registry_eligibility: bool
    generation_freeze_eligibility: bool
    strategy_enabled: bool


@dataclass(frozen=True, slots=True)
class IdentityRunContext:
    run_id: str
    run_root: Path
    run_dir: Path
    created_at_utc: str


def default_identity_specification() -> InstrumentIdentitySpecification:
    return InstrumentIdentitySpecification(
        schema_version=IDENTITY_SPECIFICATION_SCHEMA_VERSION,
        classification=PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL,
        provider="MASSIVE.COM",
        endpoint_family=TICKER_OVERVIEW_V3,
        ticker=TICKER,
        start_snapshot_date=START_SNAPSHOT_DATE,
        end_snapshot_date=END_SNAPSHOT_DATE,
        expected_market=EXPECTED_MARKET,
        expected_locale=EXPECTED_LOCALE,
        expected_currency=EXPECTED_CURRENCY,
        canonical_eligibility=False,
        registry_eligibility=False,
        generation_freeze_eligibility=False,
        strategy_enabled=False,
    )


def instrument_identity_specification_digest() -> str:
    return semantic_digest(default_identity_specification())


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
            raise InstrumentIdentityError("timestamp must be timezone-aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, Decimal):
        raise InstrumentIdentityError("binary-float authority fields are prohibited")
    return value


def _digest(value: Any) -> str:
    return semantic_digest(_canonical(value))


def _load_json(body: bytes) -> Any:
    if type(body) is not bytes or not body:
        raise InstrumentIdentityError("provider response body must be non-empty bytes")

    def reject_constant(value: str) -> None:
        raise InstrumentIdentityError(f"provider JSON constant is rejected: {value}")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise InstrumentIdentityError("provider JSON object contains duplicate keys")
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
        raise InstrumentIdentityError("provider response body must be UTF-8 JSON") from exc
    except json.JSONDecodeError as exc:
        raise InstrumentIdentityError("provider response body must be valid JSON") from exc


def _require_text(value: Any, field_name: str) -> str:
    if type(value) is not str or not value:
        raise InstrumentIdentityError(f"{field_name} must be non-empty text")
    if any(ord(char) < 32 for char in value):
        raise InstrumentIdentityError(f"{field_name} contains control characters")
    return value


def _require_bool(value: Any, field_name: str) -> bool:
    if type(value) is not bool:
        raise InstrumentIdentityError(f"{field_name} must be boolean")
    return value


def _require_optional_text(value: Any, field_name: str) -> tuple[str, str | None]:
    if value is None:
        return NOT_RETURNED, None
    return PRESENT, _require_text(value, field_name)


def _validate_iso_date(value: str, field_name: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise InstrumentIdentityError(f"{field_name} must be an ISO calendar date") from exc


def _validate_provider_timestamp_or_date(value: str, field_name: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        pass
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InstrumentIdentityError(f"{field_name} must be a supported provider date or timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise InstrumentIdentityError(f"{field_name} must be timezone-aware when timestamp")
    return parsed.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _validate_mic(value: str) -> str:
    text = _require_text(value, "primary_exchange")
    if len(text) != 4 or not text.isascii() or not text.isupper() or not text.isalpha():
        raise InstrumentIdentityError("primary_exchange must be a MIC")
    return text


def _validate_figi(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    if len(text) != 12 or not text.isascii() or not text.isalnum() or not text.isupper() or text.isdigit():
        raise InstrumentIdentityError(f"{field_name} must be a bounded FIGI")
    return text


def _validate_cik(value: str | None) -> str | None:
    if value is None:
        return None
    text = _require_text(value, "cik")
    if not text.isdigit() or not 1 <= len(text) <= 10:
        raise InstrumentIdentityError("cik must be 1-10 digits when present")
    return text


def _validate_security_type(value: str) -> str:
    text = _require_text(value, "type")
    if not text.isascii() or not text.isupper() or not 1 <= len(text) <= 12 or not all(char.isalnum() or char in {"_", "."} for char in text):
        raise InstrumentIdentityError("type must be a bounded provider security type")
    return text


def _validated_incomplete_projection_values(results: Mapping[str, Any], spec: InstrumentIdentitySpecification) -> dict[str, Any]:
    values: dict[str, Any] = {}
    if "ticker" in results and results["ticker"] is not None:
        values["ticker"] = _require_text(results["ticker"], "ticker")
        if values["ticker"] != spec.ticker:
            raise InstrumentIdentityError("ticker mismatch")
    else:
        values["ticker"] = None
    if "active" in results and results["active"] is not None:
        values["active"] = _require_bool(results["active"], "active")
    else:
        values["active"] = None
    for field_name, expected in (
        ("market", spec.expected_market),
        ("locale", spec.expected_locale),
        ("currency_name", spec.expected_currency),
    ):
        if field_name in results and results[field_name] is not None:
            values[field_name] = _require_text(results[field_name], field_name)
            if values[field_name] != expected:
                raise InstrumentIdentityError("market/locale/currency mismatch")
        else:
            values[field_name] = None
    values["primary_exchange"] = _validate_mic(results["primary_exchange"]) if results.get("primary_exchange") is not None else None
    values["composite_figi"] = _validate_figi(results["composite_figi"], "composite_figi") if results.get("composite_figi") is not None else None
    values["share_class_figi"] = _validate_figi(results["share_class_figi"], "share_class_figi") if results.get("share_class_figi") is not None else None
    values["type"] = _validate_security_type(results["type"]) if results.get("type") is not None else None
    values["cik_status"], cik_value = _require_optional_text(results.get("cik"), "cik")
    values["cik"] = _validate_cik(cik_value)
    values["list_date_status"], list_date_raw = _require_optional_text(results.get("list_date"), "list_date")
    values["list_date"] = _validate_iso_date(list_date_raw, "list_date") if list_date_raw is not None else None
    values["delisted_utc_status"], delisted_raw = _require_optional_text(results.get("delisted_utc"), "delisted_utc")
    values["delisted_utc"] = _validate_provider_timestamp_or_date(delisted_raw, "delisted_utc") if delisted_raw is not None else None
    return values


def _projection_payload(snapshot: IdentitySnapshot) -> dict[str, Any]:
    payload = asdict(snapshot)
    payload.pop("identity_projection_digest")
    return payload


def parse_ticker_overview_response(body: bytes, *, as_of_date: str, spec: InstrumentIdentitySpecification | None = None) -> IdentitySnapshot:
    actual = spec or default_identity_specification()
    as_of = _validate_iso_date(as_of_date, "as_of_date")
    payload = _load_json(body)
    if not isinstance(payload, dict):
        raise InstrumentIdentityError("provider response top level must be an object")
    extra_top = set(payload) - TOP_LEVEL_FIELDS
    if extra_top:
        raise InstrumentIdentityError("provider response contains unexpected top-level field")
    status = _require_text(payload.get("status"), "status")
    if status != PROVIDER_STATUS_OK:
        raise InstrumentIdentityError("provider status is not accepted")
    results = payload.get("results")
    if not isinstance(results, dict):
        raise InstrumentIdentityError("results must be one object")
    if "count" in payload:
        if type(payload["count"]) is not int or payload["count"] < 0:
            raise InstrumentIdentityError("count must be a nonnegative exact integer")
        if payload["count"] != 1:
            raise InstrumentIdentityError("count must equal one")
    extra_results = set(results) - RESULT_FIELDS
    if extra_results:
        raise InstrumentIdentityError("ticker overview result contains unexpected field")
    missing = [field for field in CRITICAL_FIELDS if field not in results or results[field] is None]
    if missing:
        incomplete_values = _validated_incomplete_projection_values(results, actual)
        projection = IdentitySnapshot(
            schema_version="marketflow.instrument_identity_snapshot.v1",
            as_of_date=as_of,
            ticker=incomplete_values["ticker"],
            active=incomplete_values["active"],
            market=incomplete_values["market"],
            locale=incomplete_values["locale"],
            currency_name=incomplete_values["currency_name"],
            primary_exchange=incomplete_values["primary_exchange"],
            composite_figi=incomplete_values["composite_figi"],
            share_class_figi=incomplete_values["share_class_figi"],
            type=incomplete_values["type"],
            cik_status=incomplete_values["cik_status"],
            cik=incomplete_values["cik"],
            list_date_status=incomplete_values["list_date_status"],
            list_date=incomplete_values["list_date"],
            delisted_utc_status=incomplete_values["delisted_utc_status"],
            delisted_utc=incomplete_values["delisted_utc"],
            provider_status=status,
            snapshot_status=IDENTITY_SNAPSHOT_INCOMPLETE,
            fixed_findings=("MISSING_CRITICAL_IDENTITY_FIELD",),
            identity_projection_digest="",
        )
        return _with_snapshot_digest(projection)
    ticker = _require_text(results["ticker"], "ticker")
    if ticker != actual.ticker:
        raise InstrumentIdentityError("ticker mismatch")
    active = _require_bool(results["active"], "active")
    market = _require_text(results["market"], "market")
    locale = _require_text(results["locale"], "locale")
    currency_name = _require_text(results["currency_name"], "currency_name")
    if market != actual.expected_market or locale != actual.expected_locale or currency_name != actual.expected_currency:
        raise InstrumentIdentityError("market/locale/currency mismatch")
    primary_exchange = _validate_mic(results["primary_exchange"])
    composite_figi = _validate_figi(results["composite_figi"], "composite_figi")
    share_class_figi = _validate_figi(results["share_class_figi"], "share_class_figi")
    security_type = _validate_security_type(results["type"])
    cik_status, cik_value = _require_optional_text(results.get("cik"), "cik")
    cik = _validate_cik(cik_value)
    list_date_status, list_date_raw = _require_optional_text(results.get("list_date"), "list_date")
    list_date = _validate_iso_date(list_date_raw, "list_date") if list_date_raw is not None else None
    delisted_status, delisted_raw = _require_optional_text(results.get("delisted_utc"), "delisted_utc")
    delisted = _validate_provider_timestamp_or_date(delisted_raw, "delisted_utc") if delisted_raw is not None else None
    snapshot = IdentitySnapshot(
        schema_version="marketflow.instrument_identity_snapshot.v1",
        as_of_date=as_of,
        ticker=ticker,
        active=active,
        market=market,
        locale=locale,
        currency_name=currency_name,
        primary_exchange=primary_exchange,
        composite_figi=composite_figi,
        share_class_figi=share_class_figi,
        type=security_type,
        cik_status=cik_status,
        cik=cik,
        list_date_status=list_date_status,
        list_date=list_date,
        delisted_utc_status=delisted_status,
        delisted_utc=delisted,
        provider_status=status,
        snapshot_status=IDENTITY_SNAPSHOT_COMPLETE,
        fixed_findings=(),
        identity_projection_digest="",
    )
    return _with_snapshot_digest(snapshot)


def _with_snapshot_digest(snapshot: IdentitySnapshot) -> IdentitySnapshot:
    digest = _digest(_projection_payload(snapshot))
    return IdentitySnapshot(**(_projection_payload(snapshot) | {"identity_projection_digest": digest}))


def prepare_ticker_overview_request(as_of_date: str, api_key: ProviderApiKey) -> PreparedTickerOverviewRequest:
    as_of = _validate_iso_date(as_of_date, "as_of_date")
    if as_of not in {START_SNAPSHOT_DATE, END_SNAPSHOT_DATE}:
        raise InstrumentIdentityError("snapshot date is not part of the fixed specification")
    query = f"date={as_of}"
    url = f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{TICKER_OVERVIEW_PATH}?{query}"
    return PreparedTickerOverviewRequest(
        method="GET",
        url=url,
        headers={
            "Authorization": api_key.authorization_header(),
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "User-Agent": MASSIVE_USER_AGENT,
        },
        sanitized_url=f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{TICKER_OVERVIEW_PATH}?date={as_of}",
        as_of_date=as_of,
    )


class TickerOverviewTransport:
    """Two-point-in-time Massive Ticker Overview transport boundary."""

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

    @property
    def client(self) -> httpx.Client:
        return self._client

    def close(self) -> None:
        self._client.close()

    def prepare_request(self, as_of_date: str) -> PreparedTickerOverviewRequest:
        public = prepare_ticker_overview_request(as_of_date, self._api_key)
        return PreparedTickerOverviewRequest(
            method=public.method,
            url=public.url,
            headers=public.headers | {"Authorization": "<redacted>"},
            sanitized_url=public.sanitized_url,
            as_of_date=public.as_of_date,
        )

    def send(self, as_of_date: str) -> bytes:
        prepared = prepare_ticker_overview_request(as_of_date, self._api_key)
        self._call_count += 1
        self._client.cookies.clear()
        response = self._client.request(prepared.method, prepared.url, headers=prepared.headers)
        self._client.cookies.clear()
        if response.status_code != 200:
            raise InstrumentIdentityError("ticker overview HTTP status is not accepted")
        content_type = response.headers.get("Content-Type")
        if content_type is None or content_type.split(";", 1)[0].strip().lower() != "application/json":
            raise InstrumentIdentityError("ticker overview response must be JSON")
        return response.content


def compare_identity_snapshots(start: IdentitySnapshot | None, end: IdentitySnapshot | None) -> ContinuityEvidence:
    if start is None or end is None:
        return _continuity(IDENTITY_EVIDENCE_INCOMPLETE, start, end, ("MISSING_SNAPSHOT_EVIDENCE",))
    if start.snapshot_status != IDENTITY_SNAPSHOT_COMPLETE or end.snapshot_status != IDENTITY_SNAPSHOT_COMPLETE:
        return _continuity(IDENTITY_EVIDENCE_INCOMPLETE, start, end, ("IDENTITY_SNAPSHOT_INCOMPLETE",))
    findings: list[str] = []
    for field in CONTINUITY_CRITICAL_FIELDS:
        if getattr(start, field) != getattr(end, field):
            findings.append(f"CRITICAL_{field.upper()}_CHANGED")
    if start.active is False or end.active is False:
        findings.append("INACTIVE_SNAPSHOT_CONFLICT")
    if start.delisted_utc is not None or end.delisted_utc is not None:
        findings.append("DELISTED_SNAPSHOT_CONFLICT")
    for field in ("cik", "list_date"):
        left = getattr(start, field)
        right = getattr(end, field)
        if left is not None and right is not None and left != right:
            findings.append(f"SUPPORTING_{field.upper()}_CONFLICT")
    if any(item.startswith("CRITICAL_") for item in findings):
        return _continuity(IDENTITY_CHANGE_REQUIRES_SEGMENT_REVIEW, start, end, tuple(findings))
    if findings:
        return _continuity(IDENTITY_EVIDENCE_CONFLICT, start, end, tuple(findings))
    return _continuity(IDENTITY_CONTINUITY_SUPPORTED, start, end, ())


def _continuity(status: str, start: IdentitySnapshot | None, end: IdentitySnapshot | None, findings: tuple[str, ...]) -> ContinuityEvidence:
    payload = {
        "schema_version": "marketflow.instrument_identity_continuity_candidate.v1",
        "start_as_of_date": start.as_of_date if start else START_SNAPSHOT_DATE,
        "end_as_of_date": end.as_of_date if end else END_SNAPSHOT_DATE,
        "continuity_status": status,
        "ticker_event_audit_status": TICKER_EVENT_AUDIT_NOT_IMPLEMENTED,
        "critical_field_status": "CRITICAL_FIELDS_MATCH" if status == IDENTITY_CONTINUITY_SUPPORTED else "CRITICAL_FIELD_REVIEW_REQUIRED",
        "supporting_field_status": "SUPPORTING_FIELDS_NONCONFLICTING" if not findings else "SUPPORTING_FIELDS_REVIEW_REQUIRED",
        "fixed_findings": list(findings),
        "start_identity_projection_digest": start.identity_projection_digest if start else None,
        "end_identity_projection_digest": end.identity_projection_digest if end else None,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "generation_freeze_eligibility": False,
        "strategy_enabled": False,
    }
    return ContinuityEvidence(
        schema_version=str(payload["schema_version"]),
        start_as_of_date=str(payload["start_as_of_date"]),
        end_as_of_date=str(payload["end_as_of_date"]),
        continuity_status=status,
        ticker_event_audit_status=TICKER_EVENT_AUDIT_NOT_IMPLEMENTED,
        critical_field_status=str(payload["critical_field_status"]),
        supporting_field_status=str(payload["supporting_field_status"]),
        fixed_findings=findings,
        start_identity_projection_digest=payload["start_identity_projection_digest"],
        end_identity_projection_digest=payload["end_identity_projection_digest"],
        continuity_digest=_digest(payload),
        canonical_eligibility=False,
        registry_eligibility=False,
        generation_freeze_eligibility=False,
        strategy_enabled=False,
    )


def _repository_root() -> Path:
    try:
        module_path = Path(__file__).resolve(strict=True)
        root = module_path.parents[2].resolve(strict=True)
    except (IndexError, OSError):
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED) from None
    return _validate_repository_root(root, module_path=module_path)


def _validate_repository_root(root: str | Path, *, module_path: str | Path | None = None) -> Path:
    root_path = Path(root)
    try:
        _reject_reparse(root_path.lstat())
    except InstrumentIdentityError:
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED) from None
    except OSError:
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED) from None
    try:
        candidate = root_path.resolve(strict=True)
    except OSError:
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED) from None
    if not candidate.is_dir():
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED)
    _reject_reparse_components(candidate)
    resolved_module = Path(module_path).resolve(strict=True) if module_path is not None else Path(__file__).resolve(strict=True)
    try:
        resolved_module.relative_to(candidate)
    except ValueError:
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED) from None
    expected_module = candidate / "marketflow" / "source_authority" / "instrument_identity.py"
    try:
        if not expected_module.samefile(resolved_module):
            raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED)
    except OSError:
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED) from None
    for ref in REPOSITORY_EVIDENCE_REFS:
        evidence = candidate / ref
        try:
            _reject_reparse_components(evidence)
            evidence_resolved = evidence.resolve(strict=True)
            evidence_resolved.relative_to(candidate)
        except (InstrumentIdentityError, OSError, ValueError):
            raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED) from None
        _reject_reparse_components(evidence_resolved)
        metadata = evidence.lstat()
        _reject_reparse(metadata)
        if not stat.S_ISREG(metadata.st_mode):
            raise InstrumentIdentityError(INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED)
    return candidate


def _safe_ref_to_path(root: str | Path, ref: str) -> Path:
    text = str(ref)
    parts = Path(text).parts
    if (
        not text
        or text.startswith(("/", "\\", "~"))
        or text.startswith("//")
        or text.startswith("\\\\")
        or "\\" in text
        or ":" in text
        or "\x00" in text
        or Path(text).is_absolute()
        or ".." in parts
        or any(part in {"", ".", ".."} for part in parts)
    ):
        raise InstrumentIdentityError("artifact reference must be a safe relative path")
    return Path(root) / Path(text)


def _safe_relative_path(path: str | Path, root: str | Path) -> str:
    root_path = Path(root).resolve(strict=True)
    candidate = Path(path).resolve(strict=False)
    try:
        relative = candidate.relative_to(root_path)
    except ValueError:
        raise InstrumentIdentityError("artifact path must stay within run root") from None
    return _safe_ref_to_path(".", relative.as_posix()).as_posix()


def _reject_reparse(metadata: Any) -> None:
    if stat.S_ISLNK(metadata.st_mode):
        raise InstrumentIdentityError("source-authority path must not be a symlink")
    if getattr(metadata, "st_file_attributes", 0) & WINDOWS_REPARSE_POINT_ATTRIBUTE:
        raise InstrumentIdentityError("source-authority path must not be a reparse point")


def _reject_reparse_components(path: Path) -> None:
    current = Path(path.anchor) if path.is_absolute() else Path()
    parts = path.parts[1:] if path.is_absolute() else path.parts
    for part in parts:
        current = current / part
        _reject_reparse(current.lstat())


def _reject_existing_reparse_components(path: Path) -> None:
    current = Path(path.anchor) if path.is_absolute() else Path()
    parts = path.parts[1:] if path.is_absolute() else path.parts
    for part in parts:
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            break
        _reject_reparse(metadata)


def _validated_runtime_root(run_root: str | Path, *, repository_root: Path | None = None) -> Path:
    root = Path(run_root)
    text = str(root)
    if not text or "\x00" in text or ".." in root.parts:
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_RUNTIME_ROOT_INVALID)
    root_abs = root if root.is_absolute() else root.resolve(strict=False)
    _reject_existing_reparse_components(root_abs)
    resolved = root_abs.resolve(strict=False)
    _reject_existing_reparse_components(resolved)
    if root_abs.exists() and not root_abs.is_dir():
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_RUNTIME_ROOT_INVALID)
    if repository_root is not None:
        repo_root = repository_root.resolve(strict=True)
        try:
            resolved.relative_to(repo_root)
        except ValueError:
            raise InstrumentIdentityError(INSTRUMENT_IDENTITY_RUNTIME_ROOT_INVALID) from None
    return resolved


def _identity_runtime_root(*, repository_root: Path | None = None) -> Path:
    repo_root = repository_root.resolve(strict=True) if repository_root is not None else _repository_root()
    return _validated_runtime_root(repo_root / IDENTITY_RUNTIME_ROOT, repository_root=repo_root)


def _validate_artifact_writer_readiness(runtime_root: Path, repository_root: Path) -> None:
    current = runtime_root
    while not current.exists():
        parent = current.parent
        if parent == current:
            raise InstrumentIdentityError(INSTRUMENT_IDENTITY_ARTIFACT_WRITER_UNREADY)
        current = parent
    if not current.resolve(strict=True).is_dir():
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_ARTIFACT_WRITER_UNREADY)
    try:
        current.resolve(strict=True).relative_to(repository_root.resolve(strict=True))
    except ValueError:
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_RUNTIME_ROOT_INVALID) from None
    if not os.access(current, os.W_OK):
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_ARTIFACT_WRITER_UNREADY)


def _validate_source_defined_dependencies() -> None:
    if not callable(getattr(httpx, "Client", None)):
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_SOURCE_DEPENDENCY_INVALID)
    if not callable(ProviderApiKey):
        raise InstrumentIdentityError(INSTRUMENT_IDENTITY_SOURCE_DEPENDENCY_INVALID)


def _local_preflight() -> dict[str, Any]:
    repository_root = _repository_root()
    runtime_root = _identity_runtime_root(repository_root=repository_root)
    _validate_artifact_writer_readiness(runtime_root, repository_root)
    _validate_source_defined_dependencies()
    return {
        "status": INSTRUMENT_IDENTITY_LOCAL_PREFLIGHT_READY,
        "repository_root_status": "INSTRUMENT_IDENTITY_REPOSITORY_ROOT_RESOLVED",
        "runtime_root_status": "INSTRUMENT_IDENTITY_RUNTIME_ROOT_READY",
        "runtime_root_ref": IDENTITY_RUNTIME_ROOT.as_posix(),
        "path_containment_status": "INSTRUMENT_IDENTITY_RUNTIME_ROOT_CONTAINED",
        "artifact_writer_status": "INSTRUMENT_IDENTITY_ARTIFACT_WRITER_READY",
        "source_dependency_status": "INSTRUMENT_IDENTITY_SOURCE_DEPENDENCIES_READY",
        "credential_required": False,
        "writes_artifacts": False,
    }


def _validate_regular_file(path: Path, root: Path) -> None:
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except FileNotFoundError:
        raise InstrumentIdentityError("artifact file is missing") from None
    except ValueError:
        raise InstrumentIdentityError("artifact file must stay within run root") from None
    _reject_reparse_components(path)
    metadata = path.lstat()
    _reject_reparse(metadata)
    if not stat.S_ISREG(metadata.st_mode):
        raise InstrumentIdentityError("artifact path must be a regular file")


def _created_at_utc(value: str | None = None) -> str:
    if value is None:
        return datetime.now(UTC).isoformat().replace("+00:00", "Z")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        raise InstrumentIdentityError("created_at_utc must be timezone-aware UTC")
    return parsed.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _opaque(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    if any(char in text for char in ("/", "\\", "..", "*", "?", "[", "]", ":")) or text.rstrip(" .") != text:
        raise InstrumentIdentityError(f"{field_name} must be opaque")
    return text


def create_identity_run(
    *,
    run_root: str | Path | None = None,
    run_id: str | None = None,
    run_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> IdentityRunContext:
    root = _validated_runtime_root(run_root) if run_root is not None else _identity_runtime_root()
    root.mkdir(parents=True, exist_ok=True)
    _reject_reparse_components(root.resolve(strict=True))
    run_id_text = _opaque(run_id or (run_id_factory() if run_id_factory else f"ident-{uuid.uuid4().hex}"), "run_id")
    run_dir = root / run_id_text
    try:
        run_dir.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        raise InstrumentIdentityError("identity run directory already exists") from None
    return IdentityRunContext(run_id_text, root, run_dir, _created_at_utc(created_at_utc))


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
        raise InstrumentIdentityError("artifact output already exists")
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


def _artifact_payload(value: IdentitySnapshot | ContinuityEvidence | dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, IdentitySnapshot):
        return asdict(value) | {"artifact_payload_schema": "marketflow.instrument_identity_snapshot_payload.v1"}
    if isinstance(value, ContinuityEvidence):
        return asdict(value) | {"artifact_payload_schema": "marketflow.instrument_identity_continuity_payload.v1"}
    return dict(value)


def _artifact_payload_bytes_and_metadata(
    payload: IdentitySnapshot | ContinuityEvidence | dict[str, Any] | bytes,
    artifact_type: str,
) -> tuple[bytes, str, str]:
    if isinstance(payload, bytes):
        if artifact_type != TICKER_OVERVIEW_RAW_RESPONSE:
            raise InstrumentIdentityError("raw bytes are only valid for Ticker Overview response artifacts")
        digest = sha256_bytes(payload)
        return payload, digest, PAYLOAD_MEDIA_TYPE_PROVIDER_RAW_BYTES
    if artifact_type == TICKER_OVERVIEW_RAW_RESPONSE:
        raise InstrumentIdentityError("Ticker Overview raw response artifacts require raw bytes")
    payload_data = _artifact_payload(payload)
    return canonical_json_bytes(payload_data), semantic_digest(payload_data), PAYLOAD_MEDIA_TYPE_CANONICAL_JSON


def _manifest_path_from_payload_ref(root: Path, payload_ref: str) -> Path:
    payload_path = _safe_ref_to_path(root, payload_ref)
    return payload_path.with_suffix(payload_path.suffix + ".manifest.json")


def commit_identity_artifact(
    *,
    payload: IdentitySnapshot | ContinuityEvidence | dict[str, Any] | bytes,
    artifact_type: str,
    context: IdentityRunContext,
    artifact_id: str | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    as_of_date: str | None = None,
    input_manifests: tuple[dict[str, Any], ...] = (),
    input_manifest_refs: tuple[str, ...] = (),
) -> dict[str, Any]:
    if artifact_type not in STAGE_BY_TYPE:
        raise InstrumentIdentityError("unsupported identity artifact type")
    artifact_id_text = _opaque(artifact_id or (artifact_id_factory() if artifact_id_factory else f"ident-art-{uuid.uuid4().hex}"), "artifact_id")
    stage = STAGE_BY_TYPE[artifact_type]
    stage_dir = context.run_dir / STAGE_DIRECTORY[stage]
    payload_suffix = ".bin" if artifact_type == TICKER_OVERVIEW_RAW_RESPONSE else ".json"
    payload_path = stage_dir / f"{artifact_id_text}{payload_suffix}"
    manifest_path = stage_dir / f"{artifact_id_text}{payload_suffix}.manifest.json"
    if payload_path.exists() or manifest_path.exists():
        raise InstrumentIdentityError("artifact output already exists")
    payload_bytes, semantic_payload_digest, media_type = _artifact_payload_bytes_and_metadata(payload, artifact_type)
    payload_ref = _safe_relative_path(payload_path, context.run_root)
    input_ids = [str(item["artifact_id"]) for item in input_manifests]
    if len(input_ids) != len(set(input_ids)) or len(input_ids) != len(input_manifest_refs):
        raise InstrumentIdentityError("input manifests must reconcile")
    manifest = {
        "schema_version": IDENTITY_ARTIFACT_MANIFEST_SCHEMA_VERSION,
        "artifact_id": artifact_id_text,
        "run_id": context.run_id,
        "artifact_type": artifact_type,
        "stage": stage,
        "created_at_utc": context.created_at_utc,
        "identity_specification_digest": instrument_identity_specification_digest(),
        "provider": "MASSIVE.COM",
        "ticker": TICKER,
        "as_of_date": as_of_date,
        "payload_ref": payload_ref,
        "payload_sha256": sha256_bytes(payload_bytes),
        "payload_byte_size": len(payload_bytes),
        "payload_media_type": media_type,
        "semantic_payload_digest": semantic_payload_digest,
        "input_artifact_ids": input_ids,
        "input_manifest_refs": list(input_manifest_refs),
        "lineage_artifact_ids": _lineage_ids(input_manifests),
    }
    validate_identity_manifest_shape_without_payload(manifest)
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
    saved = load_identity_manifest(_safe_relative_path(manifest_path, context.run_root), run_root=context.run_root)
    return {
        "manifest": saved,
        "manifest_ref": _safe_relative_path(manifest_path, context.run_root),
        "payload_ref": saved["payload_ref"],
        "manifest_path": manifest_path,
        "payload_path": payload_path,
    }


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


def validate_identity_manifest_shape_without_payload(manifest: dict[str, Any]) -> None:
    if set(manifest) != MANIFEST_FIELDS:
        raise InstrumentIdentityError("identity manifest fields must match schema exactly")
    if manifest["schema_version"] != IDENTITY_ARTIFACT_MANIFEST_SCHEMA_VERSION:
        raise InstrumentIdentityError("unsupported identity manifest schema")
    if manifest["artifact_type"] not in STAGE_BY_TYPE or manifest["stage"] != STAGE_BY_TYPE[manifest["artifact_type"]]:
        raise InstrumentIdentityError("identity artifact type/stage mismatch")
    _opaque(str(manifest["artifact_id"]), "artifact_id")
    _opaque(str(manifest["run_id"]), "run_id")
    if manifest["identity_specification_digest"] != instrument_identity_specification_digest():
        raise InstrumentIdentityError("identity specification digest mismatch")
    if manifest["provider"] != "MASSIVE.COM" or manifest["ticker"] != TICKER:
        raise InstrumentIdentityError("identity manifest provider/ticker mismatch")
    if manifest["as_of_date"] is not None:
        _validate_iso_date(str(manifest["as_of_date"]), "as_of_date")
    _safe_ref_to_path(".", str(manifest["payload_ref"]))
    if len(str(manifest["payload_sha256"])) != 64 or len(str(manifest["semantic_payload_digest"])) != 64:
        raise InstrumentIdentityError("identity manifest digest invalid")
    if type(manifest["payload_byte_size"]) is not int or manifest["payload_byte_size"] < 0:
        raise InstrumentIdentityError("identity manifest payload size invalid")
    expected_media_type = (
        PAYLOAD_MEDIA_TYPE_PROVIDER_RAW_BYTES
        if manifest["artifact_type"] == TICKER_OVERVIEW_RAW_RESPONSE
        else PAYLOAD_MEDIA_TYPE_CANONICAL_JSON
    )
    if manifest["payload_media_type"] != expected_media_type:
        raise InstrumentIdentityError("identity manifest media type invalid")
    if not isinstance(manifest["input_artifact_ids"], list) or not isinstance(manifest["input_manifest_refs"], list):
        raise InstrumentIdentityError("identity manifest inputs must be lists")
    if len(manifest["input_artifact_ids"]) != len(manifest["input_manifest_refs"]):
        raise InstrumentIdentityError("identity manifest inputs must reconcile")
    for artifact_id in manifest["input_artifact_ids"]:
        if type(artifact_id) is not str:
            raise InstrumentIdentityError("identity manifest input artifact IDs must be text")
        _opaque(artifact_id, "input_artifact_id")
    for ref in manifest["input_manifest_refs"]:
        if type(ref) is not str:
            raise InstrumentIdentityError("identity manifest input refs must be text")
        _safe_ref_to_path(".", str(ref))
    if not isinstance(manifest["lineage_artifact_ids"], list):
        raise InstrumentIdentityError("identity manifest lineage IDs must be a list")
    for artifact_id in manifest["lineage_artifact_ids"]:
        if type(artifact_id) is not str:
            raise InstrumentIdentityError("identity manifest lineage artifact IDs must be text")
        _opaque(artifact_id, "lineage_artifact_id")


def load_identity_manifest(manifest_ref: str | Path, *, run_root: str | Path) -> dict[str, Any]:
    root = Path(run_root)
    path = _safe_ref_to_path(root, str(manifest_ref))
    _validate_regular_file(path, root)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise InstrumentIdentityError("identity manifest must be a JSON object")
    validate_identity_manifest_shape_without_payload(data)
    expected = _manifest_path_from_payload_ref(root, str(data["payload_ref"]))
    if path.resolve(strict=True) != expected.resolve(strict=True):
        raise InstrumentIdentityError("identity manifest path does not match payload reference")
    validate_identity_manifest(data, run_root=root)
    return data


def validate_identity_manifest(manifest: dict[str, Any], *, run_root: str | Path) -> None:
    validate_identity_manifest_shape_without_payload(manifest)
    root = Path(run_root)
    payload_path = _safe_ref_to_path(root, str(manifest["payload_ref"]))
    _validate_regular_file(payload_path, root)
    payload_bytes = payload_path.read_bytes()
    if len(payload_bytes) != manifest["payload_byte_size"]:
        raise InstrumentIdentityError("identity payload size mismatch")
    if sha256_bytes(payload_bytes) != manifest["payload_sha256"]:
        raise InstrumentIdentityError("identity payload byte digest mismatch")
    if manifest["artifact_type"] == TICKER_OVERVIEW_RAW_RESPONSE:
        semantic_payload_digest = sha256_bytes(payload_bytes)
    else:
        payload = json.loads(payload_bytes.decode("utf-8"))
        semantic_payload_digest = semantic_digest(payload)
    if semantic_payload_digest != manifest["semantic_payload_digest"]:
        raise InstrumentIdentityError("identity payload semantic digest mismatch")


def load_identity_payload(manifest_ref: str | Path, *, run_root: str | Path) -> dict[str, Any]:
    manifest = load_identity_manifest(manifest_ref, run_root=run_root)
    if manifest["artifact_type"] == TICKER_OVERVIEW_RAW_RESPONSE:
        raise InstrumentIdentityError("raw identity response artifacts must be loaded as bytes")
    payload_path = _safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    _validate_regular_file(payload_path, Path(run_root))
    return json.loads(payload_path.read_text(encoding="utf-8"))


def load_identity_raw_bytes(manifest_ref: str | Path, *, run_root: str | Path) -> bytes:
    manifest = load_identity_manifest(manifest_ref, run_root=run_root)
    if manifest["artifact_type"] != TICKER_OVERVIEW_RAW_RESPONSE:
        raise InstrumentIdentityError("identity artifact is not a raw response")
    payload_path = _safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    _validate_regular_file(payload_path, Path(run_root))
    return payload_path.read_bytes()


def sanitized_receipt(
    *,
    run_id: str,
    start_snapshot: IdentitySnapshot,
    end_snapshot: IdentitySnapshot,
    continuity: ContinuityEvidence,
    start_manifest: dict[str, Any] | None = None,
    end_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "status": "INSTRUMENT_IDENTITY_EVIDENCE_READY",
        "classification": PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL,
        "run_id": run_id,
        "identity_specification_digest": instrument_identity_specification_digest(),
        "provider": "MASSIVE.COM",
        "ticker": TICKER,
        "start_snapshot_date": START_SNAPSHOT_DATE,
        "end_snapshot_date": END_SNAPSHOT_DATE,
        "start_snapshot_artifact_id": start_manifest["artifact_id"] if start_manifest else None,
        "end_snapshot_artifact_id": end_manifest["artifact_id"] if end_manifest else None,
        "start_snapshot_semantic_digest": start_snapshot.identity_projection_digest,
        "end_snapshot_semantic_digest": end_snapshot.identity_projection_digest,
        "start_active": start_snapshot.active,
        "end_active": end_snapshot.active,
        "market": start_snapshot.market,
        "locale": start_snapshot.locale,
        "currency_name": start_snapshot.currency_name,
        "primary_exchange": start_snapshot.primary_exchange,
        "composite_figi": start_snapshot.composite_figi,
        "share_class_figi": start_snapshot.share_class_figi,
        "type": start_snapshot.type,
        "start_cik_status": start_snapshot.cik_status,
        "end_cik_status": end_snapshot.cik_status,
        "start_list_date_status": start_snapshot.list_date_status,
        "end_list_date_status": end_snapshot.list_date_status,
        "start_delisted_utc_status": start_snapshot.delisted_utc_status,
        "end_delisted_utc_status": end_snapshot.delisted_utc_status,
        "continuity_status": continuity.continuity_status,
        "ticker_event_audit_status": continuity.ticker_event_audit_status,
        "fixed_findings": list(continuity.fixed_findings),
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "generation_freeze_eligibility": False,
        "strategy_enabled": False,
        "sanitization": SANITIZATION,
    }


def instrument_identity_plan() -> dict[str, Any]:
    spec = default_identity_specification()
    return {
        "status": "INSTRUMENT_IDENTITY_PLAN_READY",
        "schema_version": spec.schema_version,
        "classification": spec.classification,
        "provider": spec.provider,
        "endpoint_family": spec.endpoint_family,
        "ticker": spec.ticker,
        "start_snapshot_date": spec.start_snapshot_date,
        "end_snapshot_date": spec.end_snapshot_date,
        "identity_specification_digest": instrument_identity_specification_digest(),
        "provider_verified_identity": False,
        "ticker_event_audit_status": TICKER_EVENT_AUDIT_NOT_IMPLEMENTED,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "generation_freeze_eligibility": False,
        "strategy_enabled": False,
        "writes_artifacts": False,
        "credential_required": False,
    }


def _fixture_response(*, composite_figi: str = "BBG000B9XRY4", share_class_figi: str = "BBG001S5N8V8", primary_exchange: str = "XNAS", active: bool = True, cik: str = "320193") -> bytes:
    return canonical_json_bytes(
        {
            "status": "OK",
            "request_id": "mock-request-not-public",
            "count": 1,
            "results": {
                "ticker": "AAPL",
                "active": active,
                "market": "stocks",
                "locale": "us",
                "currency_name": "usd",
                "primary_exchange": primary_exchange,
                "composite_figi": composite_figi,
                "share_class_figi": share_class_figi,
                "type": "CS",
                "cik": cik,
                "list_date": "1980-12-12",
                "delisted_utc": None,
                "name": "Apple Inc.",
            },
        }
    )


def instrument_identity_self_check() -> dict[str, Any]:
    observed: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        observed.append(str(request.url))
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=_fixture_response())

    transport = TickerOverviewTransport(api_key=ProviderApiKey("fictional-self-check-key"), http_transport=httpx.MockTransport(handler))
    with tempfile.TemporaryDirectory() as tmp:
        start_body = transport.send(START_SNAPSHOT_DATE)
        end_body = transport.send(END_SNAPSHOT_DATE)
        transport.close()
        context = create_identity_run(run_root=Path(tmp), run_id="ident-self-check", created_at_utc="2026-01-01T00:00:00Z")
        start_raw = commit_identity_artifact(payload=start_body, artifact_type=TICKER_OVERVIEW_RAW_RESPONSE, context=context, artifact_id="ident-art-start-raw", as_of_date=START_SNAPSHOT_DATE)
        end_raw = commit_identity_artifact(payload=end_body, artifact_type=TICKER_OVERVIEW_RAW_RESPONSE, context=context, artifact_id="ident-art-end-raw", as_of_date=END_SNAPSHOT_DATE)
        start = parse_ticker_overview_response(load_identity_raw_bytes(start_raw["manifest_ref"], run_root=context.run_root), as_of_date=START_SNAPSHOT_DATE)
        end = parse_ticker_overview_response(load_identity_raw_bytes(end_raw["manifest_ref"], run_root=context.run_root), as_of_date=END_SNAPSHOT_DATE)
        continuity = compare_identity_snapshots(start, end)
        changed = compare_identity_snapshots(
            start,
            parse_ticker_overview_response(_fixture_response(share_class_figi="BBG001S5N8W9"), as_of_date=END_SNAPSHOT_DATE),
        )
        start_artifact = commit_identity_artifact(
            payload=start,
            artifact_type=TICKER_OVERVIEW_SNAPSHOT,
            context=context,
            artifact_id="ident-art-start",
            as_of_date=START_SNAPSHOT_DATE,
            input_manifests=(start_raw["manifest"],),
            input_manifest_refs=(start_raw["manifest_ref"],),
        )
        end_artifact = commit_identity_artifact(
            payload=end,
            artifact_type=TICKER_OVERVIEW_SNAPSHOT,
            context=context,
            artifact_id="ident-art-end",
            as_of_date=END_SNAPSHOT_DATE,
            input_manifests=(end_raw["manifest"],),
            input_manifest_refs=(end_raw["manifest_ref"],),
        )
        receipt = sanitized_receipt(
            run_id=context.run_id,
            start_snapshot=start,
            end_snapshot=end,
            continuity=continuity,
            start_manifest=start_artifact["manifest"],
            end_manifest=end_artifact["manifest"],
        )
    return receipt | {
        "self_check_status": "INSTRUMENT_IDENTITY_SELF_CHECK_COMPLETE",
        "mock_transport_only": True,
        "persistent_artifacts_written": False,
        "observed_request_count": len(observed),
        "changed_identity_status": changed.continuity_status,
    }


def _confirmation_phrase() -> str:
    return CONFIRMATION_PREFIX + instrument_identity_specification_digest()[:12]


def diagnostic_confirmation_phrase() -> str:
    return _confirmation_phrase()


def _run_instrument_identity_evidence(
    confirmation: str,
    *,
    api_key: ProviderApiKey,
    http_transport: httpx.BaseTransport | None = None,
    run_root: str | Path | None = None,
    run_id_factory: Callable[[], str] | None = None,
    _transport_factory: Callable[..., TickerOverviewTransport] = TickerOverviewTransport,
) -> dict[str, Any]:
    if confirmation != _confirmation_phrase():
        return {
            "status": "INSTRUMENT_IDENTITY_EVIDENCE_BLOCKED",
            "finding": "IDENTITY_CONFIRMATION_REJECTED",
            "identity_specification_digest": instrument_identity_specification_digest(),
        }
    context = create_identity_run(run_root=run_root, run_id_factory=run_id_factory)
    transport = _transport_factory(api_key=api_key, http_transport=http_transport)
    try:
        start_body = transport.send(START_SNAPSHOT_DATE)
        end_body = transport.send(END_SNAPSHOT_DATE)
    finally:
        transport.close()
    start_raw = commit_identity_artifact(payload=start_body, artifact_type=TICKER_OVERVIEW_RAW_RESPONSE, context=context, as_of_date=START_SNAPSHOT_DATE)
    end_raw = commit_identity_artifact(payload=end_body, artifact_type=TICKER_OVERVIEW_RAW_RESPONSE, context=context, as_of_date=END_SNAPSHOT_DATE)
    start = parse_ticker_overview_response(load_identity_raw_bytes(start_raw["manifest_ref"], run_root=context.run_root), as_of_date=START_SNAPSHOT_DATE)
    end = parse_ticker_overview_response(load_identity_raw_bytes(end_raw["manifest_ref"], run_root=context.run_root), as_of_date=END_SNAPSHOT_DATE)
    continuity = compare_identity_snapshots(start, end)
    start_artifact = commit_identity_artifact(
        payload=start,
        artifact_type=TICKER_OVERVIEW_SNAPSHOT,
        context=context,
        as_of_date=START_SNAPSHOT_DATE,
        input_manifests=(start_raw["manifest"],),
        input_manifest_refs=(start_raw["manifest_ref"],),
    )
    end_artifact = commit_identity_artifact(
        payload=end,
        artifact_type=TICKER_OVERVIEW_SNAPSHOT,
        context=context,
        as_of_date=END_SNAPSHOT_DATE,
        input_manifests=(end_raw["manifest"],),
        input_manifest_refs=(end_raw["manifest_ref"],),
    )
    continuity_artifact = commit_identity_artifact(
        payload=continuity,
        artifact_type=IDENTITY_CONTINUITY_CANDIDATE,
        context=context,
        input_manifests=(start_artifact["manifest"], end_artifact["manifest"]),
        input_manifest_refs=(start_artifact["manifest_ref"], end_artifact["manifest_ref"]),
    )
    receipt = sanitized_receipt(
        run_id=context.run_id,
        start_snapshot=start,
        end_snapshot=end,
        continuity=continuity,
        start_manifest=start_artifact["manifest"],
        end_manifest=end_artifact["manifest"],
    )
    receipt_artifact = commit_identity_artifact(
        payload=receipt,
        artifact_type=INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT,
        context=context,
        input_manifests=(continuity_artifact["manifest"],),
        input_manifest_refs=(continuity_artifact["manifest_ref"],),
    )
    return receipt | {
        "receipt_artifact_id": receipt_artifact["manifest"]["artifact_id"],
        "provider_request_count": transport.call_count,
    }


def _local_preflight_failure_receipt(failure_category: str) -> dict[str, Any]:
    return {
        "status": INSTRUMENT_IDENTITY_LOCAL_PREFLIGHT_FAILED,
        "failure_category": failure_category,
        "credential_prompted": False,
        "provider_request_count": 0,
        "runtime_artifact_written": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
    }


def _unexpected_failure_receipt(*, credential_prompted: bool) -> dict[str, Any]:
    return {
        "status": "INSTRUMENT_IDENTITY_EVIDENCE_FAILED",
        "failure_category": INSTRUMENT_IDENTITY_UNEXPECTED_FAILURE,
        "credential_prompted": credential_prompted,
        "canonical_eligibility": False,
        "registry_eligibility": False,
    }


def _expected_failure_category(exc: InstrumentIdentityError) -> str:
    text = str(exc)
    fixed_categories = {
        INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED,
        INSTRUMENT_IDENTITY_RUNTIME_ROOT_INVALID,
        INSTRUMENT_IDENTITY_ARTIFACT_WRITER_UNREADY,
        INSTRUMENT_IDENTITY_SOURCE_DEPENDENCY_INVALID,
    }
    return text if text in fixed_categories else "INSTRUMENT_IDENTITY_EXPECTED_FAILURE"


def live_command(
    getpass_fn: Callable[[str], str] = getpass.getpass,
    *,
    _provider_key_factory: Callable[[str], ProviderApiKey] = ProviderApiKey,
    _http_transport: httpx.BaseTransport | None = None,
    _run_id_factory: Callable[[], str] | None = None,
    _transport_factory: Callable[..., TickerOverviewTransport] = TickerOverviewTransport,
    _preflight: Callable[[], Mapping[str, Any]] = _local_preflight,
) -> int:
    if not sys.stdin.isatty():
        print(json.dumps({"status": "INSTRUMENT_IDENTITY_EVIDENCE_BLOCKED", "finding": "TTY_REQUIRED"}, sort_keys=True, indent=2))
        return 2
    print(json.dumps(instrument_identity_plan(), sort_keys=True, indent=2))
    print(f"Required confirmation phrase: {_confirmation_phrase()}")
    confirmation = input("Type confirmation phrase: ")
    if confirmation != _confirmation_phrase():
        print(json.dumps({"status": "INSTRUMENT_IDENTITY_EVIDENCE_BLOCKED", "finding": "IDENTITY_CONFIRMATION_REJECTED"}, sort_keys=True, indent=2))
        return 2
    try:
        _preflight()
    except InstrumentIdentityError as exc:
        print(json.dumps(_local_preflight_failure_receipt(_expected_failure_category(exc)), sort_keys=True, indent=2))
        return 2
    except Exception:
        print(json.dumps(_unexpected_failure_receipt(credential_prompted=False), sort_keys=True, indent=2))
        return 2
    secret = getpass_fn("Massive.com API key: ")
    try:
        receipt = _run_instrument_identity_evidence(
            confirmation,
            api_key=_provider_key_factory(secret),
            http_transport=_http_transport,
            run_id_factory=_run_id_factory,
            _transport_factory=_transport_factory,
        )
    except InstrumentIdentityError as exc:
        print(
            json.dumps(
                {
                    "status": "INSTRUMENT_IDENTITY_EVIDENCE_FAILED",
                    "failure_category": _expected_failure_category(exc),
                    "credential_prompted": True,
                    "canonical_eligibility": False,
                    "registry_eligibility": False,
                },
                sort_keys=True,
                indent=2,
            )
        )
        return 2
    except Exception:
        print(json.dumps(_unexpected_failure_receipt(credential_prompted=True), sort_keys=True, indent=2))
        return 2
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0
