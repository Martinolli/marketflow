"""Offline fake-transport monthly acquisition executor."""

from __future__ import annotations

import calendar
import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo

from marketflow.historical_data import artifacts
from marketflow.historical_data.fake_transport import (
    OUTCOME_CONNECTION_RESET,
    OUTCOME_CRASH_AFTER_BODY,
    OUTCOME_HTTP_RESPONSE,
    OUTCOME_NO_RESPONSE,
    OUTCOME_TRANSPORT_TIMEOUT,
    FakeTransportError,
    FakeTransportRequest,
    ScriptedExchange,
    ScriptedFakeTransport,
    crash_after_body,
    http_response,
)
from marketflow.historical_data.provider_response import (
    AggregateRow,
    ParsedProviderResponse,
    ProviderResponseError,
    ResponseRequestContext,
    SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE as PROVIDER_SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE,
    TRANSACTION_COUNT_ABSENT,
    TRANSACTION_COUNT_PRESENT,
    TIMESTAMP_ORDER as PROVIDER_TIMESTAMP_ORDER,
    TIMESTAMP_RANGE_INVALID as PROVIDER_TIMESTAMP_RANGE_INVALID,
    VWAP_ABSENT,
    VWAP_PRESENT,
    parse_provider_response,
)
from marketflow.research import acquisition_contract_v2 as contract_v2
from marketflow.research import acquisition_contract_v2_1 as contract_v21


MONTHLY_ACQUISITION_MANIFEST_SCHEMA_VERSION = "marketflow.monthly_acquisition_artifact_manifest.v1"
MONTHLY_ACQUISITION_ENGINE_VERSION = "marketflow.historical_data.monthly_acquisition.v1"
FAKE_FIXTURE_PROVENANCE = "SCRIPTED_FAKE_TRANSPORT_FIXTURE"

ARTIFACT_MONTH_CHUNK_REQUEST_CONTRACT = "MONTH_CHUNK_REQUEST_CONTRACT"
ARTIFACT_REQUEST_ATTEMPT_RECORD = "REQUEST_ATTEMPT_RECORD"
ARTIFACT_RAW_PROVIDER_PAGE = "RAW_PROVIDER_PAGE"
ARTIFACT_MONTH_CHUNK_COMPLETENESS_MANIFEST = "MONTH_CHUNK_COMPLETENESS_MANIFEST"
ARTIFACT_MONTH_NORMALIZED_15M_OHLCV = "MONTH_NORMALIZED_15M_OHLCV"
ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS = "MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS"
ARTIFACT_MONTH_ACQUISITION_RECEIPT = "MONTH_ACQUISITION_RECEIPT"

MONTH_ACQUISITION_COMPLETED = "MONTH_ACQUISITION_COMPLETED"
MONTH_ACQUISITION_BLOCKED = "MONTH_ACQUISITION_BLOCKED"
MONTH_ACQUISITION_RETRY_EXHAUSTED = "MONTH_ACQUISITION_RETRY_EXHAUSTED"
MONTH_ACQUISITION_RESPONSE_VARIANCE = "MONTH_ACQUISITION_RESPONSE_VARIANCE"
MONTH_ACQUISITION_PAGINATION_INVALID = "MONTH_ACQUISITION_PAGINATION_INVALID"
MONTH_ACQUISITION_AUTHENTICATION_FAILED = "MONTH_ACQUISITION_AUTHENTICATION_FAILED"
MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED = "MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED"
MONTH_ACQUISITION_INVALID = "MONTH_ACQUISITION_INVALID"

ATTEMPT_ACCEPTED = "REQUEST_ATTEMPT_ACCEPTED"
ATTEMPT_RETRY_SCHEDULED = "REQUEST_ATTEMPT_RETRY_SCHEDULED"
ATTEMPT_RETRY_EXHAUSTED = "REQUEST_ATTEMPT_RETRY_EXHAUSTED"
ATTEMPT_REJECTED_NON_RETRYABLE = "REQUEST_ATTEMPT_REJECTED_NON_RETRYABLE"
ATTEMPT_VALID_NOT_ACCEPTED = "REQUEST_ATTEMPT_VALID_NOT_ACCEPTED"

SEMANTICALLY_EQUIVALENT_RETRIES = "SEMANTICALLY_EQUIVALENT_RETRIES"
PROVIDER_RESPONSE_VARIANCE = "PROVIDER_RESPONSE_VARIANCE"
ONE_VALID_ATTEMPT_PER_PAGE = "ONE_VALID_ATTEMPT_PER_PAGE"
SEMANTIC_RETRY_NOT_APPLICABLE = "SEMANTIC_RETRY_NOT_APPLICABLE"
PAGINATION_CHAIN_VALID = "PAGINATION_CHAIN_VALID"
PAGINATION_CHAIN_INVALID = "PAGINATION_CHAIN_INVALID"
PAGINATION_NOT_STARTED = "PAGINATION_NOT_STARTED"
RETRY_AFTER_POLICY_VIOLATION = "RETRY_AFTER_POLICY_VIOLATION"
RANGE_COVERAGE_COMPLETE = "RANGE_COVERAGE_COMPLETE"
RANGE_COVERAGE_INCOMPLETE = "RANGE_COVERAGE_INCOMPLETE"
AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"
AUTHORIZATION_FAILURE = "AUTHORIZATION_FAILURE"
RESPONSE_SCHEMA_INVALID = "RESPONSE_SCHEMA_INVALID"
SCHEMA_FAILURE = "SCHEMA_FAILURE"
TIMESTAMP_ORDER = PROVIDER_TIMESTAMP_ORDER
TIMESTAMP_RANGE_INVALID = PROVIDER_TIMESTAMP_RANGE_INVALID
SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE = PROVIDER_SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE

MAXIMUM_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = (2, 5)
RETRY_JITTER = False
RETRYABLE_CATEGORIES = frozenset(
    {
        "TRANSPORT_TIMEOUT",
        "CONNECTION_RESET",
        "HTTP_408",
        "HTTP_429",
        "HTTP_500",
        "HTTP_502",
        "HTTP_503",
        "HTTP_504",
    }
)
RETRYABLE_HTTP_STATUS = {408, 429, 500, 502, 503, 504}
FIXED_RANGE_START = date(2022, 1, 1)
FIXED_RANGE_END = date(2025, 12, 31)

STAGE_BY_ARTIFACT_TYPE = {
    ARTIFACT_MONTH_CHUNK_REQUEST_CONTRACT: "month_chunk_request_contract",
    ARTIFACT_REQUEST_ATTEMPT_RECORD: "request_attempt_record",
    ARTIFACT_RAW_PROVIDER_PAGE: "raw_provider_page",
    ARTIFACT_MONTH_CHUNK_COMPLETENESS_MANIFEST: "month_chunk_completeness_manifest",
    ARTIFACT_MONTH_NORMALIZED_15M_OHLCV: "month_normalized_15m_ohlcv",
    ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS: "month_normalized_aggregate_audit_fields",
    ARTIFACT_MONTH_ACQUISITION_RECEIPT: "month_acquisition_receipt",
}
ARTIFACT_TYPE_BY_STAGE = {stage: artifact_type for artifact_type, stage in STAGE_BY_ARTIFACT_TYPE.items()}

FICTIONAL_TICKER_PREFIXES = ("FAKE", "TEST", "SYNTH")


class MonthlyAcquisitionError(ValueError):
    """Raised when offline monthly acquisition cannot continue."""


@dataclass(frozen=True, slots=True)
class MonthChunkRequest:
    schema_version: str
    contract_v2_1_digest: str
    contract_v2_base_digest: str
    acquisition_generation_test_identity: str
    identity_segment_test_identity: str
    canonical_ticker: str
    month_key: str
    effective_start_date: str
    effective_end_date: str
    multiplier: int
    timespan: str
    adjusted: bool
    sort: str
    limit: int
    source_timestamp_contract_version: str
    provider_business_identity: str
    provider_entitlement_status: str
    request_semantic_digest: str


@dataclass(frozen=True, slots=True)
class LogicalPageRequest:
    logical_page_request_id: str
    month_request_digest: str
    page_ordinal: int
    predecessor_accepted_page_identity: str | None
    sanitized_continuation_identity: str | None


@dataclass(frozen=True, slots=True)
class RawPageRecord:
    artifact: dict[str, Any]
    manifest_ref: str
    body_sha256: str
    byte_size: int


@dataclass(frozen=True, slots=True)
class AttemptCandidate:
    attempt_record: dict[str, Any]
    parsed: ParsedProviderResponse
    raw_page: RawPageRecord


@dataclass(frozen=True, slots=True)
class RecordingSleeper:
    delays: list[int]

    def sleep(self, seconds: int) -> None:
        self.delays.append(seconds)


class DeterministicClock:
    def __init__(self, start: datetime | None = None) -> None:
        self._current = start or datetime(2026, 1, 1, tzinfo=UTC)

    def now(self) -> str:
        value = self._current
        self._current = self._current + timedelta(seconds=1)
        return value.isoformat().replace("+00:00", "Z")


class _ArtifactIdFactory:
    def __init__(self) -> None:
        self._next = 1

    def __call__(self, artifact_type: str) -> str:
        value = f"month-art-{self._next:04d}-{artifact_type.lower().replace('_', '-')}"
        self._next += 1
        return value


def _contract_digests() -> tuple[str, str]:
    v2 = contract_v2.default_contract()
    v21 = contract_v21.default_contract()
    base_digest = contract_v21.verify_base_contract_digest(v21)
    v2_digest = contract_v2.contract_digest(v2)
    if base_digest != v2_digest:
        raise MonthlyAcquisitionError("v2.1 base contract digest mismatch")
    return v2_digest, contract_v21.contract_digest(v21)


def _utc_now(clock: DeterministicClock | None) -> str:
    return clock.now() if clock is not None else datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _opaque_id(value: str, field_name: str) -> str:
    if not value or any(part in value for part in ("/", "\\", "..", ":", "*", "?", "[", "]", "\x00")):
        raise MonthlyAcquisitionError(f"{field_name} must be path-safe")
    return value


def _as_payload(value: Any) -> Any:
    if isinstance(value, Decimal):
        if value == 0:
            return "0"
        normalized = value.normalize()
        text = format(normalized, "f")
        return text.rstrip("0").rstrip(".") if "." in text else text
    if isinstance(value, dict):
        return {str(key): _as_payload(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_as_payload(item) for item in value]
    return value


def _manifest_ref(manifest: dict[str, Any], *, run_root: str | Path) -> str:
    payload_path = artifacts._safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    return artifacts._safe_relative_path(payload_path.with_suffix(payload_path.suffix + ".manifest.json"), run_root)


def _load_monthly_manifest_ref(run_root: str | Path, manifest_ref: str) -> dict[str, Any]:
    path = artifacts._safe_ref_to_path(run_root, manifest_ref)
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MonthlyAcquisitionError("monthly manifest reference does not exist") from exc
    if not isinstance(manifest, dict):
        raise MonthlyAcquisitionError("monthly manifest must be an object")
    return manifest


def validate_saved_monthly_manifest(
    manifest: dict[str, Any],
    *,
    run_root: str | Path,
    expected_run_id: str | None = None,
    expected_artifact_type: str | None = None,
    expected_input_refs: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    required = {
        "schema_version",
        "artifact_id",
        "run_id",
        "artifact_type",
        "stage",
        "payload_ref",
        "payload_sha256",
        "payload_byte_size",
        "payload_media_type",
        "semantic_payload_digest",
        "input_manifest_refs",
    }
    if set(manifest) - {
        *required,
        "created_at_utc",
        "contract_v2_1_digest",
        "contract_v2_base_digest",
        "processing_engine_version",
        "provider_business_identity",
        "legacy_adapter_family",
        "provenance",
        "month_request_digest",
        "month_key",
        "canonical_ticker",
        "page_ordinal",
        "attempt_ordinal",
        "primary_parent_artifact_id",
        "primary_parent_manifest_ref",
        "input_artifact_ids",
    }:
        raise MonthlyAcquisitionError("monthly manifest contains unknown fields")
    missing = required - set(manifest)
    if missing:
        raise MonthlyAcquisitionError("monthly manifest is missing required fields")
    if manifest["schema_version"] != MONTHLY_ACQUISITION_MANIFEST_SCHEMA_VERSION:
        raise MonthlyAcquisitionError("monthly manifest schema mismatch")
    artifact_type = str(manifest["artifact_type"])
    if expected_artifact_type is not None and artifact_type != expected_artifact_type:
        raise MonthlyAcquisitionError("monthly manifest artifact type mismatch")
    expected_stage = STAGE_BY_ARTIFACT_TYPE.get(artifact_type)
    if expected_stage is None or manifest["stage"] != expected_stage:
        raise MonthlyAcquisitionError("monthly manifest stage mismatch")
    if expected_run_id is not None and manifest["run_id"] != expected_run_id:
        raise MonthlyAcquisitionError("monthly manifest run mismatch")
    if expected_input_refs is not None and tuple(manifest["input_manifest_refs"]) != expected_input_refs:
        raise MonthlyAcquisitionError("monthly manifest input refs mismatch")
    payload_path = artifacts._safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    if not payload_path.is_file():
        raise MonthlyAcquisitionError("monthly payload is not selectable")
    payload_bytes = payload_path.read_bytes()
    if artifacts.sha256_bytes(payload_bytes) != manifest["payload_sha256"]:
        raise MonthlyAcquisitionError("monthly payload digest mismatch")
    if len(payload_bytes) != manifest["payload_byte_size"]:
        raise MonthlyAcquisitionError("monthly payload byte-size mismatch")
    for input_ref in manifest.get("input_manifest_refs") or []:
        input_manifest = _load_monthly_manifest_ref(run_root, str(input_ref))
        validate_saved_monthly_manifest(input_manifest, run_root=run_root, expected_run_id=str(manifest["run_id"]))
    parent_ref = manifest.get("primary_parent_manifest_ref")
    if parent_ref:
        parent = _load_monthly_manifest_ref(run_root, str(parent_ref))
        validate_saved_monthly_manifest(parent, run_root=run_root, expected_run_id=str(manifest["run_id"]))
    return manifest


def _commit_monthly_artifact(
    *,
    payload: dict[str, Any] | bytes,
    run_root: str | Path,
    run_id: str,
    artifact_type: str,
    artifact_id_factory: _ArtifactIdFactory,
    created_at_utc: str,
    month_request: MonthChunkRequest,
    page_ordinal: int | None = None,
    attempt_ordinal: int | None = None,
    primary_parent_manifest: dict[str, Any] | None = None,
    input_manifests: tuple[dict[str, Any], ...] = (),
    provenance: str = FAKE_FIXTURE_PROVENANCE,
) -> dict[str, Any]:
    root = Path(run_root)
    run_dir = root / _opaque_id(run_id, "run_id")
    if not run_dir.is_dir():
        raise MonthlyAcquisitionError("monthly run directory does not exist")
    stage = STAGE_BY_ARTIFACT_TYPE[artifact_type]
    stage_dir = run_dir / stage
    stage_dir.mkdir(parents=True, exist_ok=True)
    artifact_id = _opaque_id(artifact_id_factory(artifact_type), "artifact_id")
    suffix = ".json" if isinstance(payload, dict) else ".bin"
    payload_path = stage_dir / f"{artifact_id}{suffix}"
    manifest_path = stage_dir / f"{artifact_id}{suffix}.manifest.json"
    if payload_path.exists() or manifest_path.exists():
        raise MonthlyAcquisitionError("monthly artifact already exists")

    if isinstance(payload, bytes):
        payload_bytes = payload
        semantic_payload_digest = artifacts.sha256_bytes(payload_bytes)
        media_type = "application/vnd.marketflow.provider-raw+octet-stream"
    else:
        payload = _as_payload(payload)
        payload_bytes = artifacts.canonical_json_bytes(payload)
        semantic_payload_digest = artifacts.semantic_digest(payload)
        media_type = artifacts.PAYLOAD_MEDIA_TYPE_CANONICAL_JSON

    input_manifest_refs = tuple(_manifest_ref(item, run_root=root) for item in input_manifests)
    input_artifact_ids = tuple(str(item["artifact_id"]) for item in input_manifests)
    primary_parent_ref = _manifest_ref(primary_parent_manifest, run_root=root) if primary_parent_manifest else None
    manifest = {
        "schema_version": MONTHLY_ACQUISITION_MANIFEST_SCHEMA_VERSION,
        "artifact_id": artifact_id,
        "run_id": run_id,
        "artifact_type": artifact_type,
        "stage": stage,
        "created_at_utc": created_at_utc,
        "contract_v2_1_digest": month_request.contract_v2_1_digest,
        "contract_v2_base_digest": month_request.contract_v2_base_digest,
        "processing_engine_version": MONTHLY_ACQUISITION_ENGINE_VERSION,
        "provider_business_identity": "Massive.com",
        "legacy_adapter_family": "polygon-api-client",
        "provenance": provenance,
        "month_request_digest": month_request.request_semantic_digest,
        "month_key": month_request.month_key,
        "canonical_ticker": month_request.canonical_ticker,
        "page_ordinal": page_ordinal,
        "attempt_ordinal": attempt_ordinal,
        "primary_parent_artifact_id": primary_parent_manifest["artifact_id"] if primary_parent_manifest else None,
        "primary_parent_manifest_ref": primary_parent_ref,
        "input_artifact_ids": list(input_artifact_ids),
        "input_manifest_refs": list(input_manifest_refs),
        "payload_ref": artifacts._safe_relative_path(payload_path, root),
        "payload_sha256": artifacts.sha256_bytes(payload_bytes),
        "payload_byte_size": len(payload_bytes),
        "payload_media_type": media_type,
        "semantic_payload_digest": semantic_payload_digest,
    }
    temp_payload = artifacts._write_temp_bytes(stage_dir, payload_bytes, ".payload.tmp")
    try:
        artifacts._install_without_replace(temp_payload, payload_path)
        temp_manifest = artifacts._write_temp_bytes(stage_dir, artifacts.canonical_json_bytes(manifest), ".manifest.tmp")
        artifacts._install_without_replace(temp_manifest, manifest_path)
    except Exception:
        if payload_path.exists() and not manifest_path.exists():
            payload_path.unlink()
        raise
    saved_manifest = _load_monthly_manifest_ref(root, artifacts._safe_relative_path(manifest_path, root))
    return validate_saved_monthly_manifest(
        saved_manifest,
        run_root=root,
        expected_run_id=run_id,
        expected_artifact_type=artifact_type,
        expected_input_refs=input_manifest_refs,
    )


def _month_bounds(month_key: str) -> tuple[date, date]:
    try:
        year_text, month_text = month_key.split("-", 1)
        year = int(year_text)
        month = int(month_text)
        if len(year_text) != 4 or len(month_text) != 2:
            raise ValueError
        last_day = calendar.monthrange(year, month)[1]
    except ValueError as exc:
        raise MonthlyAcquisitionError("month_key must be YYYY-MM") from exc
    return date(year, month, 1), date(year, month, last_day)


def build_month_chunk_request(
    *,
    canonical_ticker: str,
    month_key: str,
    effective_start_date: str | None = None,
    effective_end_date: str | None = None,
    acquisition_generation_test_identity: str = "FAKE_MONTHLY_GENERATION_V1",
    identity_segment_test_identity: str = "FAKE_IDENTITY_SEGMENT_V1",
) -> MonthChunkRequest:
    ticker = canonical_ticker.strip().upper()
    if not ticker.startswith(FICTIONAL_TICKER_PREFIXES):
        raise MonthlyAcquisitionError("fake monthly acquisition accepts fictional test tickers only")
    month_start, month_end = _month_bounds(month_key)
    start = date.fromisoformat(effective_start_date) if effective_start_date else month_start
    end = date.fromisoformat(effective_end_date) if effective_end_date else month_end
    if start < month_start or end > month_end or start > end:
        raise MonthlyAcquisitionError("effective dates must be a clipped range inside month_key")
    if start < FIXED_RANGE_START or end > FIXED_RANGE_END:
        raise MonthlyAcquisitionError("effective dates must stay inside the fixed 2022-01-01 through 2025-12-31 range")
    v2_digest, v21_digest = _contract_digests()
    base = {
        "schema_version": "marketflow.month_chunk_request_contract.v1",
        "contract_v2_1_digest": v21_digest,
        "contract_v2_base_digest": v2_digest,
        "acquisition_generation_test_identity": acquisition_generation_test_identity,
        "identity_segment_test_identity": identity_segment_test_identity,
        "canonical_ticker": ticker,
        "month_key": month_key,
        "effective_start_date": start.isoformat(),
        "effective_end_date": end.isoformat(),
        "multiplier": 15,
        "timespan": "minute",
        "adjusted": True,
        "sort": "asc",
        "limit": 50000,
        "source_timestamp_contract_version": contract_v21.CONTRACT_SCHEMA_VERSION,
        "provider_business_identity": "Massive.com",
        "provider_entitlement_status": "OPERATOR_ATTESTED_CONFIRMED",
    }
    digest = artifacts.semantic_digest(base)
    return MonthChunkRequest(request_semantic_digest=digest, **base)


def _request_payload(
    month_request: MonthChunkRequest,
    *,
    provenance: str = FAKE_FIXTURE_PROVENANCE,
    provider_execution_enabled: bool = False,
) -> dict[str, Any]:
    return {
        "request": asdict(month_request),
        "acquisition_enabled": False,
        "provider_execution_enabled": provider_execution_enabled,
        "provenance": provenance,
    }


def build_logical_page_request(
    month_request: MonthChunkRequest,
    *,
    page_ordinal: int,
    predecessor_accepted_page_identity: str | None = None,
    sanitized_continuation_identity: str | None = None,
) -> LogicalPageRequest:
    if page_ordinal == 1 and (predecessor_accepted_page_identity or sanitized_continuation_identity):
        raise MonthlyAcquisitionError("first logical page must not bind predecessor or continuation")
    if page_ordinal > 1 and (not predecessor_accepted_page_identity or not sanitized_continuation_identity):
        raise MonthlyAcquisitionError("continuation pages must bind predecessor and sanitized continuation")
    digest = artifacts.semantic_digest(
        {
            "month_request_digest": month_request.request_semantic_digest,
            "page_ordinal": page_ordinal,
            "predecessor_accepted_page_identity": predecessor_accepted_page_identity,
            "sanitized_continuation_identity": sanitized_continuation_identity,
        }
    )
    return LogicalPageRequest(
        logical_page_request_id=f"page-{digest[:24]}",
        month_request_digest=month_request.request_semantic_digest,
        page_ordinal=page_ordinal,
        predecessor_accepted_page_identity=predecessor_accepted_page_identity,
        sanitized_continuation_identity=sanitized_continuation_identity,
    )


def fake_transport_request(month_request: MonthChunkRequest, logical_page: LogicalPageRequest) -> FakeTransportRequest:
    return FakeTransportRequest(
        logical_page_request_id=logical_page.logical_page_request_id,
        request_semantic_digest=month_request.request_semantic_digest,
        page_ordinal=logical_page.page_ordinal,
        month_key=month_request.month_key,
        sanitized_continuation_identity=logical_page.sanitized_continuation_identity,
    )


def _failure_from_outcome(outcome_type: str, http_status: int | None) -> str:
    if outcome_type in {OUTCOME_TRANSPORT_TIMEOUT, OUTCOME_NO_RESPONSE}:
        return "TRANSPORT_TIMEOUT"
    if outcome_type in {OUTCOME_CONNECTION_RESET, OUTCOME_CRASH_AFTER_BODY}:
        return "CONNECTION_RESET"
    if http_status in RETRYABLE_HTTP_STATUS:
        return f"HTTP_{http_status}"
    return "HTTP_STATUS_NON_SUCCESS"


def _transport_failure_category(outcome: object) -> str | None:
    headers = getattr(outcome, "headers", None)
    if isinstance(headers, dict):
        category = headers.get("failure_category")
        if isinstance(category, str) and category:
            return category
    return None


def _retry_after_delay(headers: Any, http_status: int | None, configured_backoff: int) -> tuple[int | None, str | None]:
    if http_status not in {429, 503}:
        return configured_backoff, None
    retry_after = None
    if isinstance(headers, dict):
        retry_after = headers.get("Retry-After") or headers.get("retry-after")
    if retry_after is None:
        return configured_backoff, None
    try:
        parsed = int(str(retry_after))
    except ValueError:
        return None, RETRY_AFTER_POLICY_VIOLATION
    if str(parsed) != str(retry_after).strip() or parsed < 0 or parsed > 60:
        return None, RETRY_AFTER_POLICY_VIOLATION
    return max(configured_backoff, parsed), None


def _attempt_base(logical_page: LogicalPageRequest, attempt_ordinal: int, started_at: str) -> dict[str, Any]:
    return {
        "logical_page_request_id": logical_page.logical_page_request_id,
        "attempt_id": f"{logical_page.logical_page_request_id}-attempt-{attempt_ordinal}",
        "page_ordinal": logical_page.page_ordinal,
        "attempt_ordinal": attempt_ordinal,
        "attempt_started_at_utc": started_at,
        "attempt_finished_at_utc": None,
        "attempt_status": None,
        "observed_transport_outcome": None,
        "http_status": None,
        "http_category": None,
        "response_body_available": False,
        "response_body_complete": False,
        "failure_category": None,
        "retryable": False,
        "scheduled_retry_delay_seconds": None,
        "retry_after_policy_status": None,
        "raw_page_artifact_id": None,
        "raw_page_manifest_ref": None,
        "semantic_projection_digest": None,
        "accepted_attempt": False,
        "sanitized_error_code": None,
        "sanitized_schema_diagnostics": None,
    }


def _status_from_block(block_status: str) -> str:
    if block_status in {
        MONTH_ACQUISITION_RETRY_EXHAUSTED,
        MONTH_ACQUISITION_RESPONSE_VARIANCE,
        MONTH_ACQUISITION_PAGINATION_INVALID,
        MONTH_ACQUISITION_AUTHENTICATION_FAILED,
        MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED,
    }:
        return block_status
    if block_status == MONTH_ACQUISITION_INVALID:
        return MONTH_ACQUISITION_INVALID
    return MONTH_ACQUISITION_BLOCKED


def _block_status_from_failed_page(terminal_status: str | None, attempts: list[dict[str, Any]]) -> tuple[str, str]:
    for attempt in attempts:
        if attempt.get("failure_category") == AUTHENTICATION_FAILURE and attempt.get("http_status") == 401:
            return MONTH_ACQUISITION_AUTHENTICATION_FAILED, AUTHENTICATION_FAILURE
        if attempt.get("failure_category") == SCHEMA_FAILURE:
            return MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED, RESPONSE_SCHEMA_INVALID
        if attempt.get("failure_category") == TIMESTAMP_ORDER:
            return MONTH_ACQUISITION_INVALID, TIMESTAMP_ORDER
        if attempt.get("failure_category") == TIMESTAMP_RANGE_INVALID:
            return MONTH_ACQUISITION_INVALID, TIMESTAMP_RANGE_INVALID
    block_status = terminal_status or MONTH_ACQUISITION_BLOCKED
    return block_status, block_status


def _pagination_status(*, status: str, page_count: int) -> str:
    if status == MONTH_ACQUISITION_COMPLETED:
        return PAGINATION_CHAIN_VALID
    if page_count == 0 and status != MONTH_ACQUISITION_PAGINATION_INVALID:
        return PAGINATION_NOT_STARTED
    return PAGINATION_CHAIN_INVALID


def _write_attempts(
    attempts: Iterable[dict[str, Any]],
    *,
    run_root: str | Path,
    run_id: str,
    month_request: MonthChunkRequest,
    artifact_id_factory: _ArtifactIdFactory,
    clock: DeterministicClock,
    request_manifest: dict[str, Any],
    raw_manifests_by_id: dict[str, dict[str, Any]],
    provenance: str = FAKE_FIXTURE_PROVENANCE,
) -> list[dict[str, Any]]:
    manifests: list[dict[str, Any]] = []
    for attempt in attempts:
        inputs = ()
        raw_id = attempt.get("raw_page_artifact_id")
        if raw_id:
            inputs = (raw_manifests_by_id[str(raw_id)],)
        manifests.append(
            _commit_monthly_artifact(
                payload=attempt,
                run_root=run_root,
                run_id=run_id,
                artifact_type=ARTIFACT_REQUEST_ATTEMPT_RECORD,
                artifact_id_factory=artifact_id_factory,
                created_at_utc=clock.now(),
                month_request=month_request,
                page_ordinal=int(attempt["page_ordinal"]),
                attempt_ordinal=int(attempt["attempt_ordinal"]),
                primary_parent_manifest=request_manifest,
                input_manifests=inputs,
                provenance=provenance,
            )
        )
    return manifests


def _write_raw_page(
    *,
    body: bytes,
    run_root: str | Path,
    run_id: str,
    month_request: MonthChunkRequest,
    artifact_id_factory: _ArtifactIdFactory,
    clock: DeterministicClock,
    request_manifest: dict[str, Any],
    logical_page: LogicalPageRequest,
    attempt_ordinal: int,
    provenance: str = FAKE_FIXTURE_PROVENANCE,
) -> RawPageRecord:
    manifest = _commit_monthly_artifact(
        payload=body,
        run_root=run_root,
        run_id=run_id,
        artifact_type=ARTIFACT_RAW_PROVIDER_PAGE,
        artifact_id_factory=artifact_id_factory,
        created_at_utc=clock.now(),
        month_request=month_request,
        page_ordinal=logical_page.page_ordinal,
        attempt_ordinal=attempt_ordinal,
        primary_parent_manifest=request_manifest,
        provenance=provenance,
    )
    return RawPageRecord(
        artifact=manifest,
        manifest_ref=_manifest_ref(manifest, run_root=run_root),
        body_sha256=artifacts.sha256_bytes(body),
        byte_size=len(body),
    )


def _parse_body(
    *,
    body: bytes,
    body_sha256: str,
    month_request: MonthChunkRequest,
) -> ParsedProviderResponse:
    return parse_provider_response(
        body,
        body_sha256=body_sha256,
        context=ResponseRequestContext(
            canonical_ticker=month_request.canonical_ticker,
            month_key=month_request.month_key,
            effective_start_date=month_request.effective_start_date,
            effective_end_date=month_request.effective_end_date,
            adjusted=month_request.adjusted,
            sort=month_request.sort,
            limit=month_request.limit,
            month_request_digest=month_request.request_semantic_digest,
        ),
    )


def _finalize_page_attempts(candidates: list[AttemptCandidate], attempts: list[dict[str, Any]]) -> AttemptCandidate:
    first = candidates[0]
    for candidate in candidates[1:]:
        if candidate.parsed.semantic_projection_digest != first.parsed.semantic_projection_digest:
            raise MonthlyAcquisitionError(PROVIDER_RESPONSE_VARIANCE)
    accepted_attempt_ordinal = first.attempt_record["attempt_ordinal"]
    for attempt in attempts:
        if attempt["attempt_ordinal"] == accepted_attempt_ordinal:
            attempt["attempt_status"] = ATTEMPT_ACCEPTED
            attempt["accepted_attempt"] = True
        elif attempt.get("semantic_projection_digest"):
            attempt["attempt_status"] = ATTEMPT_VALID_NOT_ACCEPTED
    return first


def _acquire_page(
    *,
    month_request: MonthChunkRequest,
    logical_page: LogicalPageRequest,
    transport: ScriptedFakeTransport,
    run_root: str | Path,
    run_id: str,
    request_manifest: dict[str, Any],
    artifact_id_factory: _ArtifactIdFactory,
    clock: DeterministicClock,
    sleeper: RecordingSleeper,
    raw_continuation_evidence: str | None = None,
    provenance: str = FAKE_FIXTURE_PROVENANCE,
) -> tuple[AttemptCandidate | None, list[dict[str, Any]], dict[str, dict[str, Any]], str | None]:
    attempts: list[dict[str, Any]] = []
    raw_manifests_by_id: dict[str, dict[str, Any]] = {}
    candidates: list[AttemptCandidate] = []
    terminal_status: str | None = None

    for attempt_ordinal in range(1, MAXIMUM_ATTEMPTS + 1):
        started_at = clock.now()
        attempt = _attempt_base(logical_page, attempt_ordinal, started_at)
        attempts.append(attempt)
        try:
            protocol_request = fake_transport_request(month_request, logical_page)
            if raw_continuation_evidence is None:
                outcome = transport.send(protocol_request)
            else:
                try:
                    outcome = transport.send(protocol_request, raw_next_url=raw_continuation_evidence)
                except TypeError:
                    outcome = transport.send(protocol_request)
            attempt["observed_transport_outcome"] = outcome.outcome_type
            attempt["http_status"] = outcome.http_status
            attempt["http_category"] = f"HTTP_{outcome.http_status}" if outcome.http_status is not None else None
            body = outcome.body
            if outcome.outcome_type in {OUTCOME_HTTP_RESPONSE, OUTCOME_CRASH_AFTER_BODY} and body is not None:
                attempt["response_body_available"] = True
                attempt["response_body_complete"] = True
                if outcome.http_status == 200:
                    body_sha256 = artifacts.sha256_bytes(body)
                    try:
                        parsed = _parse_body(body=body, body_sha256=body_sha256, month_request=month_request)
                    except ProviderResponseError as exc:
                        failure_category = getattr(exc, "failure_category", None) or SCHEMA_FAILURE
                        attempt["failure_category"] = failure_category
                        attempt["attempt_status"] = ATTEMPT_REJECTED_NON_RETRYABLE
                        if failure_category == TIMESTAMP_RANGE_INVALID:
                            attempt["sanitized_error_code"] = SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE
                            terminal_status = MONTH_ACQUISITION_INVALID
                        elif failure_category != SCHEMA_FAILURE:
                            attempt["sanitized_error_code"] = failure_category
                            terminal_status = MONTH_ACQUISITION_INVALID
                        else:
                            attempt["sanitized_error_code"] = "PROVIDER_RESPONSE_SCHEMA_FAILURE"
                            terminal_status = MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED
                        diagnostics = getattr(exc, "sanitized_diagnostics", None)
                        if isinstance(diagnostics, dict):
                            attempt["sanitized_schema_diagnostics"] = diagnostics
                        break
                    raw_page = _write_raw_page(
                        body=body,
                        run_root=run_root,
                        run_id=run_id,
                        month_request=month_request,
                        artifact_id_factory=artifact_id_factory,
                        clock=clock,
                        request_manifest=request_manifest,
                        logical_page=logical_page,
                        attempt_ordinal=attempt_ordinal,
                        provenance=provenance,
                    )
                    raw_manifests_by_id[raw_page.artifact["artifact_id"]] = raw_page.artifact
                    attempt["raw_page_artifact_id"] = raw_page.artifact["artifact_id"]
                    attempt["raw_page_manifest_ref"] = raw_page.manifest_ref
                    attempt["semantic_projection_digest"] = parsed.semantic_projection_digest
                    candidates.append(AttemptCandidate(attempt, parsed, raw_page))
                    if outcome.outcome_type == OUTCOME_HTTP_RESPONSE:
                        break
                    attempt["failure_category"] = "CONNECTION_RESET"
                else:
                    transport_category = _transport_failure_category(outcome)
                    if transport_category not in {AUTHENTICATION_FAILURE, AUTHORIZATION_FAILURE}:
                        raw_page = _write_raw_page(
                            body=body,
                            run_root=run_root,
                            run_id=run_id,
                            month_request=month_request,
                            artifact_id_factory=artifact_id_factory,
                            clock=clock,
                            request_manifest=request_manifest,
                            logical_page=logical_page,
                            attempt_ordinal=attempt_ordinal,
                            provenance=provenance,
                        )
                        raw_manifests_by_id[raw_page.artifact["artifact_id"]] = raw_page.artifact
                        attempt["raw_page_artifact_id"] = raw_page.artifact["artifact_id"]
                        attempt["raw_page_manifest_ref"] = raw_page.manifest_ref
            transport_category = _transport_failure_category(outcome)
            if transport_category is not None:
                failure_category = transport_category
            elif candidates and outcome.outcome_type == OUTCOME_CRASH_AFTER_BODY:
                failure_category = "CONNECTION_RESET"
            else:
                failure_category = _failure_from_outcome(outcome.outcome_type, outcome.http_status)
            attempt["failure_category"] = attempt["failure_category"] or failure_category
            retryable = failure_category in RETRYABLE_CATEGORIES
            attempt["retryable"] = retryable
            if not retryable:
                attempt["attempt_status"] = ATTEMPT_REJECTED_NON_RETRYABLE
                terminal_status = MONTH_ACQUISITION_INVALID
                break
            if attempt_ordinal == MAXIMUM_ATTEMPTS:
                attempt["attempt_status"] = ATTEMPT_RETRY_EXHAUSTED if not candidates else ATTEMPT_VALID_NOT_ACCEPTED
                terminal_status = MONTH_ACQUISITION_RETRY_EXHAUSTED if not candidates else None
                break
            configured_backoff = RETRY_BACKOFF_SECONDS[attempt_ordinal - 1]
            delay, violation = _retry_after_delay(outcome.headers, outcome.http_status, configured_backoff)
            if violation:
                attempt["retry_after_policy_status"] = violation
                attempt["attempt_status"] = ATTEMPT_REJECTED_NON_RETRYABLE
                terminal_status = MONTH_ACQUISITION_INVALID
                break
            attempt["attempt_status"] = ATTEMPT_RETRY_SCHEDULED
            attempt["scheduled_retry_delay_seconds"] = delay
            sleeper.sleep(int(delay))
        except FakeTransportError:
            attempt["observed_transport_outcome"] = "FAKE_TRANSPORT_SCRIPT_VIOLATION"
            attempt["failure_category"] = "INVALID_REQUEST"
            attempt["attempt_status"] = ATTEMPT_REJECTED_NON_RETRYABLE
            attempt["sanitized_error_code"] = "FAKE_TRANSPORT_SCRIPT_VIOLATION"
            terminal_status = MONTH_ACQUISITION_INVALID
            break
        finally:
            attempt["attempt_finished_at_utc"] = clock.now()

    if candidates and terminal_status is None:
        try:
            accepted = _finalize_page_attempts(candidates, attempts)
            return accepted, attempts, raw_manifests_by_id, None
        except MonthlyAcquisitionError:
            for attempt in attempts:
                if attempt.get("semantic_projection_digest"):
                    attempt["attempt_status"] = ATTEMPT_VALID_NOT_ACCEPTED
            return None, attempts, raw_manifests_by_id, MONTH_ACQUISITION_RESPONSE_VARIANCE
    return None, attempts, raw_manifests_by_id, terminal_status or MONTH_ACQUISITION_RETRY_EXHAUSTED


def _normalized_rows(rows: Iterable[AggregateRow]) -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "window_start_utc": row.window_start_utc,
            "window_end_utc": row.window_end_utc,
            "open": row.open,
            "high": row.high,
            "low": row.low,
            "close": row.close,
            "volume": row.volume,
        }
        for row in rows
    )


def _audit_rows(rows: Iterable[AggregateRow], *, month_request: MonthChunkRequest) -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "window_start_utc": row.window_start_utc,
            "window_end_utc": row.window_end_utc,
            "provider_timestamp": row.provider_timestamp,
            "provider_adjusted": month_request.adjusted,
            "calendar_session_id": None,
            "bar_window_label": "SOURCE_15M_LEFT_CLOSED_RIGHT_OPEN",
            "raw_page_digest": row.raw_page_digest,
            "corporate_action_boundary_id": None,
            "vwap_status": VWAP_PRESENT if row.vwap is not None else VWAP_ABSENT,
            "vwap": row.vwap,
            "transaction_count_status": TRANSACTION_COUNT_PRESENT if row.transaction_count is not None else TRANSACTION_COUNT_ABSENT,
            "transaction_count": row.transaction_count,
        }
        for row in rows
    )


def _range_coverage_status(rows: list[AggregateRow], *, month_request: MonthChunkRequest) -> str:
    if not rows:
        return RANGE_COVERAGE_INCOMPLETE
    source_tz = ZoneInfo(contract_v21.SESSION_MAPPING_TIMEZONE)
    first_date = datetime.fromisoformat(rows[0].window_start_utc.replace("Z", "+00:00")).astimezone(source_tz).date().isoformat()
    last_date = datetime.fromisoformat(rows[-1].window_start_utc.replace("Z", "+00:00")).astimezone(source_tz).date().isoformat()
    if first_date != month_request.effective_start_date or last_date != month_request.effective_end_date:
        return RANGE_COVERAGE_INCOMPLETE
    return RANGE_COVERAGE_COMPLETE


def _receipt(
    *,
    status: str,
    month_request: MonthChunkRequest,
    run_id: str,
    request_manifest: dict[str, Any],
    attempt_manifests: list[dict[str, Any]],
    extra_manifests: list[dict[str, Any]],
    fixed_findings: list[str],
    page_count: int,
    row_count: int,
    attempt_records: list[dict[str, Any]],
    semantic_retry_status: str,
    retry_delays: list[int],
    provenance: str = FAKE_FIXTURE_PROVENANCE,
    provider_execution_enabled: bool = False,
) -> dict[str, Any]:
    artifact_receipts = []
    for manifest in [request_manifest, *attempt_manifests, *extra_manifests]:
        artifact_receipts.append(
            {
                "artifact_id": manifest["artifact_id"],
                "artifact_type": manifest["artifact_type"],
                "manifest_ref": manifest["payload_ref"] + ".manifest.json",
                "semantic_payload_digest": manifest["semantic_payload_digest"],
            }
        )
    return {
        "status": status,
        "fake_execution_id": run_id,
        "run_id": run_id,
        "month_request_id": month_request.request_semantic_digest,
        "month_request_digest": month_request.request_semantic_digest,
        "month_key": month_request.month_key,
        "canonical_ticker": month_request.canonical_ticker,
        "contract_v2_digest": month_request.contract_v2_base_digest,
        "contract_v2_1_digest": month_request.contract_v2_1_digest,
        "provider_business_identity": "Massive.com",
        "legacy_adapter_family": "polygon-api-client",
        "provider_entitlement_status": month_request.provider_entitlement_status,
        "provider_execution_enabled": provider_execution_enabled,
        "acquisition_enabled": False,
        "runtime_migration_performed": False,
        "provenance": provenance,
        "pagination_status": _pagination_status(status=status, page_count=page_count),
        "semantic_retry_status": semantic_retry_status,
        "maximum_attempts": MAXIMUM_ATTEMPTS,
        "retry_backoff_seconds": list(RETRY_BACKOFF_SECONDS),
        "retry_jitter": RETRY_JITTER,
        "recorded_retry_delays_seconds": retry_delays,
        "intended_retry_delays_seconds": retry_delays,
        "attempt_count": len(attempt_records),
        "accepted_page_count": page_count,
        "failed_or_rejected_attempt_count": sum(1 for attempt in attempt_records if not attempt.get("accepted_attempt")),
        "completeness_status": "COMPLETE" if status == MONTH_ACQUISITION_COMPLETED else "INCOMPLETE",
        "page_count": page_count,
        "raw_page_count": sum(1 for attempt in attempt_records if attempt.get("raw_page_artifact_id")),
        "row_count": row_count,
        "artifact_count": len(artifact_receipts),
        "artifact_receipts": artifact_receipts,
        "fixed_findings": fixed_findings,
        "sanitization": "NO_RAW_OHLCV_NO_RAW_BODY_NO_RAW_URL_NO_CREDENTIALS_NO_ABSOLUTE_PATHS_NO_RAW_EXCEPTIONS",
    }


def execute_fake_monthly_acquisition(
    *,
    month_request: MonthChunkRequest,
    transport: ScriptedFakeTransport,
    run_root: str | Path,
    run_id: str | None = None,
    clock: DeterministicClock | None = None,
    sleeper: RecordingSleeper | None = None,
    provenance: str = FAKE_FIXTURE_PROVENANCE,
    provider_execution_enabled: bool = False,
) -> dict[str, Any]:
    clock = clock or DeterministicClock()
    sleeper = sleeper or RecordingSleeper([])
    artifact_id_factory = _ArtifactIdFactory()
    actual_run_id = _opaque_id(run_id or f"monthly-{month_request.request_semantic_digest[:20]}", "run_id")
    artifacts.create_historical_run(run_root=run_root, run_id=actual_run_id, created_at_utc=clock.now())
    request_manifest = _commit_monthly_artifact(
        payload=_request_payload(
            month_request,
            provenance=provenance,
            provider_execution_enabled=provider_execution_enabled,
        ),
        run_root=run_root,
        run_id=actual_run_id,
        artifact_type=ARTIFACT_MONTH_CHUNK_REQUEST_CONTRACT,
        artifact_id_factory=artifact_id_factory,
        created_at_utc=clock.now(),
        month_request=month_request,
        provenance=provenance,
    )

    all_attempt_manifests: list[dict[str, Any]] = []
    extra_manifests: list[dict[str, Any]] = []
    raw_manifests_by_id: dict[str, dict[str, Any]] = {}
    all_attempt_records: list[dict[str, Any]] = []
    accepted_pages: list[AttemptCandidate] = []
    all_rows: list[AggregateRow] = []
    seen_timestamps: set[str] = set()
    seen_continuations: set[str] = set()
    fixed_findings: list[str] = []
    page_ordinal = 1
    predecessor: str | None = None
    continuation: str | None = None
    raw_continuation_evidence: str | None = None
    block_status: str | None = None

    while True:
        logical_page = build_logical_page_request(
            month_request,
            page_ordinal=page_ordinal,
            predecessor_accepted_page_identity=predecessor,
            sanitized_continuation_identity=continuation,
        )
        accepted, attempts, page_raw_manifests, terminal_status = _acquire_page(
            month_request=month_request,
            logical_page=logical_page,
            transport=transport,
            run_root=run_root,
            run_id=actual_run_id,
            request_manifest=request_manifest,
            artifact_id_factory=artifact_id_factory,
            clock=clock,
            sleeper=sleeper,
            raw_continuation_evidence=raw_continuation_evidence,
            provenance=provenance,
        )
        raw_manifests_by_id.update(page_raw_manifests)
        all_attempt_records.extend(attempts)
        all_attempt_manifests.extend(
            _write_attempts(
                attempts,
                run_root=run_root,
                run_id=actual_run_id,
                month_request=month_request,
                artifact_id_factory=artifact_id_factory,
                clock=clock,
                request_manifest=request_manifest,
                raw_manifests_by_id=raw_manifests_by_id,
                provenance=provenance,
            )
        )
        if accepted is None:
            block_status, finding = _block_status_from_failed_page(terminal_status, attempts)
            fixed_findings.append(finding)
            break
        accepted_pages.append(accepted)
        for row in accepted.parsed.rows:
            if row.window_start_utc in seen_timestamps:
                block_status = MONTH_ACQUISITION_PAGINATION_INVALID
                fixed_findings.append("PAGINATION_DUPLICATE_TIMESTAMP")
                break
            seen_timestamps.add(row.window_start_utc)
            all_rows.append(row)
        if block_status:
            break
        next_continuation = accepted.parsed.sanitized_continuation_identity
        next_raw_continuation_evidence = accepted.parsed.raw_next_url
        predecessor = accepted.attempt_record["logical_page_request_id"]
        if not next_continuation:
            break
        if next_continuation in seen_continuations:
            block_status = MONTH_ACQUISITION_PAGINATION_INVALID
            fixed_findings.append("PAGINATION_REPEATED_CONTINUATION")
            break
        seen_continuations.add(next_continuation)
        continuation = next_continuation
        raw_continuation_evidence = next_raw_continuation_evidence
        page_ordinal += 1

    if not block_status and _range_coverage_status(all_rows, month_request=month_request) != RANGE_COVERAGE_COMPLETE:
        block_status = MONTH_ACQUISITION_PAGINATION_INVALID
        fixed_findings.append(RANGE_COVERAGE_INCOMPLETE)
    status = _status_from_block(block_status) if block_status else MONTH_ACQUISITION_COMPLETED
    if status == MONTH_ACQUISITION_COMPLETED:
        raw_page_manifests = tuple(candidate.raw_page.artifact for candidate in accepted_pages)
        completeness_payload = {
            "schema_version": "marketflow.month_chunk_completeness_manifest.v1",
            "month_request_digest": month_request.request_semantic_digest,
            "month_request_id": month_request.request_semantic_digest,
            "month_key": month_request.month_key,
            "effective_start_date": month_request.effective_start_date,
            "effective_end_date": month_request.effective_end_date,
            "pagination_status": PAGINATION_CHAIN_VALID,
            "pagination_exhausted": True,
            "range_coverage_status": RANGE_COVERAGE_COMPLETE,
            "duplicate_status": "NO_DUPLICATES",
            "conflict_status": "NO_CONFLICTS",
            "completion_status": "COMPLETE",
            "page_count": len(accepted_pages),
            "row_count": len(all_rows),
            "first_source_window_start_utc": all_rows[0].window_start_utc if all_rows else None,
            "last_source_window_start_utc": all_rows[-1].window_start_utc if all_rows else None,
            "accepted_pages": [
                {
                    "page_ordinal": index + 1,
                    "logical_page_request_id": candidate.attempt_record["logical_page_request_id"],
                    "accepted_page_identity": candidate.attempt_record["logical_page_request_id"],
                    "accepted_attempt_id": candidate.attempt_record["attempt_id"],
                    "accepted_attempt_ordinal": candidate.attempt_record["attempt_ordinal"],
                    "raw_page_artifact_id": candidate.raw_page.artifact["artifact_id"],
                    "raw_page_sha256": candidate.raw_page.body_sha256,
                    "semantic_projection_digest": candidate.parsed.semantic_projection_digest,
                    "continuation_present": candidate.parsed.continuation_present,
                    "sanitized_continuation_identity": candidate.parsed.sanitized_continuation_identity,
                }
                for index, candidate in enumerate(accepted_pages)
            ],
        }
        completeness_payload["page_chain_digest"] = artifacts.semantic_digest(completeness_payload["accepted_pages"])
        completeness_manifest = _commit_monthly_artifact(
            payload=completeness_payload,
            run_root=run_root,
            run_id=actual_run_id,
            artifact_type=ARTIFACT_MONTH_CHUNK_COMPLETENESS_MANIFEST,
            artifact_id_factory=artifact_id_factory,
            created_at_utc=clock.now(),
            month_request=month_request,
            primary_parent_manifest=request_manifest,
            input_manifests=raw_page_manifests,
            provenance=provenance,
        )
        normalized_manifest = _commit_monthly_artifact(
            payload={
                "schema_version": "marketflow.month_normalized_15m_ohlcv.v1",
                "month_request_digest": month_request.request_semantic_digest,
                "provenance": provenance,
                "rth_filtering_applied": False,
                "rows": _normalized_rows(all_rows),
            },
            run_root=run_root,
            run_id=actual_run_id,
            artifact_type=ARTIFACT_MONTH_NORMALIZED_15M_OHLCV,
            artifact_id_factory=artifact_id_factory,
            created_at_utc=clock.now(),
            month_request=month_request,
            primary_parent_manifest=completeness_manifest,
            input_manifests=(completeness_manifest,),
            provenance=provenance,
        )
        audit_manifest = _commit_monthly_artifact(
            payload={
                "schema_version": "marketflow.month_normalized_aggregate_audit_fields.v1",
                "month_request_digest": month_request.request_semantic_digest,
                "provenance": provenance,
                "rows": _audit_rows(all_rows, month_request=month_request),
            },
            run_root=run_root,
            run_id=actual_run_id,
            artifact_type=ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS,
            artifact_id_factory=artifact_id_factory,
            created_at_utc=clock.now(),
            month_request=month_request,
            primary_parent_manifest=completeness_manifest,
            input_manifests=(completeness_manifest,),
            provenance=provenance,
        )
        extra_manifests.extend([completeness_manifest, normalized_manifest, audit_manifest])
    valid_attempt_count = sum(1 for attempt in all_attempt_records if attempt.get("semantic_projection_digest"))
    if status == MONTH_ACQUISITION_RESPONSE_VARIANCE:
        semantic_retry_status = PROVIDER_RESPONSE_VARIANCE
    elif status == MONTH_ACQUISITION_COMPLETED and valid_attempt_count > len(accepted_pages):
        semantic_retry_status = SEMANTICALLY_EQUIVALENT_RETRIES
    elif status == MONTH_ACQUISITION_COMPLETED and valid_attempt_count == len(accepted_pages):
        semantic_retry_status = ONE_VALID_ATTEMPT_PER_PAGE
    else:
        semantic_retry_status = SEMANTIC_RETRY_NOT_APPLICABLE
    receipt_payload = _receipt(
        status=status,
        month_request=month_request,
        run_id=actual_run_id,
        request_manifest=request_manifest,
        attempt_manifests=all_attempt_manifests,
        extra_manifests=extra_manifests,
        fixed_findings=fixed_findings,
        page_count=len(accepted_pages),
        row_count=len(all_rows) if status == MONTH_ACQUISITION_COMPLETED else 0,
        attempt_records=all_attempt_records,
        semantic_retry_status=semantic_retry_status,
        retry_delays=sleeper.delays,
        provenance=provenance,
        provider_execution_enabled=provider_execution_enabled,
    )
    _commit_monthly_artifact(
        payload=receipt_payload,
        run_root=run_root,
        run_id=actual_run_id,
        artifact_type=ARTIFACT_MONTH_ACQUISITION_RECEIPT,
        artifact_id_factory=artifact_id_factory,
        created_at_utc=clock.now(),
        month_request=month_request,
        primary_parent_manifest=extra_manifests[0] if extra_manifests else request_manifest,
        input_manifests=tuple(all_attempt_manifests + extra_manifests),
        provenance=provenance,
    )
    return receipt_payload


def _self_check_body(*, next_url: str | None = None, close: str = "100.0", t: int = 1704105000000) -> bytes:
    next_part = f',"next_url":"{next_url}"' if next_url else ""
    return (
        '{"adjusted":true,"queryCount":1,"results":[{"c":'
        + close
        + ',"h":101,"l":99,"n":10,"o":100,"t":'
        + str(t)
        + ',"v":1000,"vw":100.5}],'
        + '"resultsCount":1,"status":"OK","ticker":"FAKEFLOW"'
        + next_part
        + "}"
    ).encode("utf-8")


def monthly_acquisition_self_check(run_root: str | Path) -> dict[str, Any]:
    month_request = build_month_chunk_request(
        canonical_ticker="FAKEFLOW",
        month_key="2024-01",
        effective_start_date="2024-01-01",
        effective_end_date="2024-01-01",
    )
    first_page = build_logical_page_request(month_request, page_ordinal=1)
    next_url = "https://api.massive.com/v2/aggs/ticker/FAKEFLOW/range/15/minute/2024-01-01/2024-01-01?cursor=selfcheck2&adjusted=true&sort=asc&limit=50000"
    continuation = parse_provider_response(
        _self_check_body(next_url=next_url),
        body_sha256="self-check",
        context=ResponseRequestContext(
            canonical_ticker=month_request.canonical_ticker,
            month_key=month_request.month_key,
            effective_start_date=month_request.effective_start_date,
            effective_end_date=month_request.effective_end_date,
            adjusted=month_request.adjusted,
            sort=month_request.sort,
            limit=month_request.limit,
            month_request_digest=month_request.request_semantic_digest,
        ),
    ).sanitized_continuation_identity
    second_page = build_logical_page_request(
        month_request,
        page_ordinal=2,
        predecessor_accepted_page_identity=first_page.logical_page_request_id,
        sanitized_continuation_identity=continuation,
    )
    transport = ScriptedFakeTransport(
        [
            ScriptedExchange(
                fake_transport_request(month_request, first_page),
                crash_after_body(200, _self_check_body(close="100", next_url=next_url)),
            ),
            ScriptedExchange(
                fake_transport_request(month_request, first_page),
                http_response(200, _self_check_body(close="100.0", next_url=next_url)),
            ),
            ScriptedExchange(
                fake_transport_request(month_request, second_page),
                http_response(200, _self_check_body(close="101", t=1704105900000)),
            ),
        ]
    )
    receipt = execute_fake_monthly_acquisition(
        month_request=month_request,
        transport=transport,
        run_root=run_root,
        run_id="monthly-self-check",
        clock=DeterministicClock(),
        sleeper=RecordingSleeper([]),
    )
    transport.assert_consumed()
    return {
        "status": "MARKETFLOW_FAKE_TRANSPORT_MONTHLY_ACQUISITION_SELF_CHECK",
        "monthly_acquisition_status": receipt["status"],
        "contract_v2_digest": receipt["contract_v2_digest"],
        "contract_v2_1_digest": receipt["contract_v2_1_digest"],
        "provider_business_identity": receipt["provider_business_identity"],
        "provider_entitlement_status": receipt["provider_entitlement_status"],
        "provider_execution_enabled": False,
        "acquisition_enabled": False,
        "runtime_migration_performed": False,
        "provenance": FAKE_FIXTURE_PROVENANCE,
        "page_count": receipt["page_count"],
        "row_count": receipt["row_count"],
        "artifact_count": receipt["artifact_count"],
        "recorded_retry_delays_seconds": receipt["recorded_retry_delays_seconds"],
        "sanitization": receipt["sanitization"],
    }
