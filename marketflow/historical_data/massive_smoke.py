"""Controlled Massive.com one-month smoke-test runner boundary."""

from __future__ import annotations

import getpass
import json
import sys
import tempfile
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

import httpx

from marketflow.historical_data import artifacts
from marketflow.historical_data.fake_transport import OUTCOME_HTTP_RESPONSE
from marketflow.historical_data.massive_transport import (
    MASSIVE_ADJUSTED,
    MASSIVE_LIMIT,
    MASSIVE_MULTIPLIER,
    MASSIVE_REST_HOST,
    MASSIVE_REST_SCHEME,
    MASSIVE_SORT,
    MASSIVE_TIMESPAN,
    MassiveRestTransport,
    ProviderApiKey,
)
from marketflow.historical_data.monthly_acquisition import (
    ARTIFACT_MONTH_CHUNK_COMPLETENESS_MANIFEST,
    ARTIFACT_MONTH_NORMALIZED_15M_OHLCV,
    ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS,
    ARTIFACT_RAW_PROVIDER_PAGE,
    AUTHENTICATION_FAILURE,
    MONTH_ACQUISITION_AUTHENTICATION_FAILED,
    MONTH_ACQUISITION_COMPLETED,
    MONTH_ACQUISITION_PAGINATION_INVALID,
    MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED,
    MonthChunkRequest,
    RecordingSleeper,
    execute_fake_monthly_acquisition,
)
from marketflow.research import acquisition_contract_v2 as contract_v2
from marketflow.research import acquisition_contract_v2_1 as contract_v21


SMOKE_SCHEMA_VERSION = "marketflow.massive_provider_smoke.v1"
SMOKE_CLASSIFICATION = "NONCANONICAL_PROVIDER_SMOKE"
SMOKE_PROVIDER = "MASSIVE.COM"
SMOKE_ENDPOINT = "STOCKS_CUSTOM_BARS_V2"
SMOKE_TICKER = "AAPL"
SMOKE_MONTH_KEY = "2025-01"
SMOKE_EFFECTIVE_START = "2025-01-01"
SMOKE_EFFECTIVE_END = "2025-01-31"
LIVE_PROVIDER_SMOKE_PROVENANCE = "LIVE_PROVIDER_SMOKE_NONCANONICAL"
SMOKE_RUNTIME_ROOT = Path(".marketflow/provider_smoke/runs")
SMOKE_DIGEST_PREFIX_LENGTH = 12

SMOKE_PLAN_VALID = "SMOKE_PLAN_VALID"
SMOKE_AUTHORIZATION_REJECTED = "SMOKE_AUTHORIZATION_REJECTED"
SMOKE_CREDENTIAL_REJECTED = "SMOKE_CREDENTIAL_REJECTED"
SMOKE_TRANSPORT_FAILED = "SMOKE_TRANSPORT_FAILED"
SMOKE_MONTH_INCOMPLETE = "SMOKE_MONTH_INCOMPLETE"
SMOKE_PROVIDER_RESPONSE_REJECTED = "SMOKE_PROVIDER_RESPONSE_REJECTED"
SMOKE_COMPLETED_NONCANONICAL = "SMOKE_COMPLETED_NONCANONICAL"
SMOKE_INVALID = "SMOKE_INVALID"

_NO_STRATEGY_TEXT = "NO STRATEGY"
_NO_REGISTRY_TEXT = "NO CANONICAL REGISTRY"
_NO_PERFORMANCE_TEXT = "NO PERFORMANCE ANALYSIS"


class MassiveSmokeError(ValueError):
    """Raised when the controlled smoke runner boundary is violated."""


@dataclass(frozen=True, slots=True)
class MassiveSmokeSpec:
    smoke_schema_version: str
    classification: str
    provider: str
    endpoint: str
    ticker: str
    month_key: str
    effective_start: str
    effective_end: str
    multiplier: int
    timespan: str
    adjusted: bool
    sort: str
    limit: int
    strategy_enabled: bool
    calendar_bar_derivation_enabled: bool
    registry_eligibility: bool
    canonical_eligibility: bool
    acquisition_enabled: bool
    runtime_migration_enabled: bool
    provider_execution_requires_interactive_authorization: bool
    contract_v2_digest: str
    contract_v2_1_digest: str

    def validate(self) -> None:
        expected = {
            "smoke_schema_version": SMOKE_SCHEMA_VERSION,
            "classification": SMOKE_CLASSIFICATION,
            "provider": SMOKE_PROVIDER,
            "endpoint": SMOKE_ENDPOINT,
            "ticker": SMOKE_TICKER,
            "month_key": SMOKE_MONTH_KEY,
            "effective_start": SMOKE_EFFECTIVE_START,
            "effective_end": SMOKE_EFFECTIVE_END,
            "multiplier": MASSIVE_MULTIPLIER,
            "timespan": MASSIVE_TIMESPAN,
            "adjusted": MASSIVE_ADJUSTED,
            "sort": MASSIVE_SORT,
            "limit": MASSIVE_LIMIT,
            "strategy_enabled": False,
            "calendar_bar_derivation_enabled": False,
            "registry_eligibility": False,
            "canonical_eligibility": False,
            "acquisition_enabled": False,
            "runtime_migration_enabled": False,
            "provider_execution_requires_interactive_authorization": True,
            "contract_v2_digest": contract_v2.contract_digest(contract_v2.default_contract()),
            "contract_v2_1_digest": contract_v21.contract_digest(contract_v21.default_contract()),
        }
        actual = asdict(self)
        for key, value in expected.items():
            if actual[key] != value:
                raise MassiveSmokeError("smoke specification fixed field mismatch")
        contract_v21.verify_base_contract_digest(contract_v21.default_contract())


@dataclass(slots=True)
class _AuthorizationState:
    authorized_digest: str | None = None


_LIVE_AUTHORIZATION_STATE = _AuthorizationState()


def default_smoke_spec() -> MassiveSmokeSpec:
    v2 = contract_v2.default_contract()
    v21 = contract_v21.default_contract()
    contract_v21.verify_base_contract_digest(v21)
    return MassiveSmokeSpec(
        smoke_schema_version=SMOKE_SCHEMA_VERSION,
        classification=SMOKE_CLASSIFICATION,
        provider=SMOKE_PROVIDER,
        endpoint=SMOKE_ENDPOINT,
        ticker=SMOKE_TICKER,
        month_key=SMOKE_MONTH_KEY,
        effective_start=SMOKE_EFFECTIVE_START,
        effective_end=SMOKE_EFFECTIVE_END,
        multiplier=MASSIVE_MULTIPLIER,
        timespan=MASSIVE_TIMESPAN,
        adjusted=MASSIVE_ADJUSTED,
        sort=MASSIVE_SORT,
        limit=MASSIVE_LIMIT,
        strategy_enabled=False,
        calendar_bar_derivation_enabled=False,
        registry_eligibility=False,
        canonical_eligibility=False,
        acquisition_enabled=False,
        runtime_migration_enabled=False,
        provider_execution_requires_interactive_authorization=True,
        contract_v2_digest=contract_v2.contract_digest(v2),
        contract_v2_1_digest=contract_v21.contract_digest(v21),
    )


def smoke_spec_payload(spec: MassiveSmokeSpec | None = None) -> dict[str, object]:
    actual = spec or default_smoke_spec()
    return asdict(actual)


def smoke_spec_bytes(spec: MassiveSmokeSpec | None = None) -> bytes:
    return artifacts.canonical_json_bytes(smoke_spec_payload(spec))


def smoke_spec_digest(spec: MassiveSmokeSpec | None = None) -> str:
    return artifacts.sha256_bytes(smoke_spec_bytes(spec))


def smoke_digest_prefix(spec: MassiveSmokeSpec | None = None) -> str:
    return smoke_spec_digest(spec)[:SMOKE_DIGEST_PREFIX_LENGTH]


def smoke_confirmation_phrase(spec: MassiveSmokeSpec | None = None) -> str:
    return f"RUN MARKETFLOW MASSIVE SMOKE {smoke_digest_prefix(spec)}"


def smoke_plan_receipt(spec: MassiveSmokeSpec | None = None) -> dict[str, object]:
    actual = spec or default_smoke_spec()
    actual.validate()
    digest = smoke_spec_digest(actual)
    return {
        "status": SMOKE_PLAN_VALID,
        "smoke_schema_version": actual.smoke_schema_version,
        "smoke_specification_digest": digest,
        "digest_prefix": digest[:SMOKE_DIGEST_PREFIX_LENGTH],
        "classification": actual.classification,
        "provider": actual.provider,
        "endpoint": actual.endpoint,
        "ticker": actual.ticker,
        "month_key": actual.month_key,
        "effective_start": actual.effective_start,
        "effective_end": actual.effective_end,
        "multiplier": actual.multiplier,
        "timespan": actual.timespan,
        "adjusted": actual.adjusted,
        "sort": actual.sort,
        "limit": actual.limit,
        "strategy_enabled": False,
        "calendar_bar_derivation_enabled": False,
        "registry_eligibility": False,
        "canonical_eligibility": False,
        "acquisition_enabled": False,
        "runtime_migration_enabled": False,
        "network_execution_enabled": False,
        "credential_prompted": False,
        "runtime_artifact_written": False,
        "contract_v2_digest": actual.contract_v2_digest,
        "contract_v2_1_digest": actual.contract_v2_1_digest,
        "operator_confirmation_phrase": smoke_confirmation_phrase(actual),
        "required_warnings": [_NO_STRATEGY_TEXT, _NO_REGISTRY_TEXT, _NO_PERFORMANCE_TEXT],
    }


def _month_request_from_spec(spec: MassiveSmokeSpec) -> MonthChunkRequest:
    base = {
        "schema_version": "marketflow.month_chunk_request_contract.v1",
        "contract_v2_1_digest": spec.contract_v2_1_digest,
        "contract_v2_base_digest": spec.contract_v2_digest,
        "acquisition_generation_test_identity": "NONCANONICAL_PROVIDER_SMOKE_ONLY",
        "identity_segment_test_identity": "NONCANONICAL_PROVIDER_SMOKE_AAPL",
        "canonical_ticker": spec.ticker,
        "month_key": spec.month_key,
        "effective_start_date": spec.effective_start,
        "effective_end_date": spec.effective_end,
        "multiplier": spec.multiplier,
        "timespan": spec.timespan,
        "adjusted": spec.adjusted,
        "sort": spec.sort,
        "limit": spec.limit,
        "source_timestamp_contract_version": contract_v21.CONTRACT_SCHEMA_VERSION,
        "provider_business_identity": "Massive.com",
        "provider_entitlement_status": "OPERATOR_ATTESTED_CONFIRMED",
    }
    return MonthChunkRequest(request_semantic_digest=artifacts.semantic_digest(base), **base)


def _authorize_smoke(
    confirmation: str,
    *,
    spec: MassiveSmokeSpec,
    state: _AuthorizationState | None = None,
) -> None:
    digest = smoke_spec_digest(spec)
    if state is not None and state.authorized_digest == digest:
        raise MassiveSmokeError("smoke authorization already used")
    if confirmation != smoke_confirmation_phrase(spec):
        raise MassiveSmokeError("smoke authorization phrase mismatch")
    if state is not None:
        state.authorized_digest = digest


def _stdio_is_interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def _opaque_smoke_run_id() -> str:
    return f"smoke-{uuid.uuid4().hex}"


def _smoke_status_from_monthly(receipt: dict[str, object]) -> str:
    status = receipt.get("status")
    findings = set(str(item) for item in receipt.get("fixed_findings", []) if item)
    if status == MONTH_ACQUISITION_COMPLETED:
        return SMOKE_COMPLETED_NONCANONICAL
    if status == MONTH_ACQUISITION_AUTHENTICATION_FAILED and AUTHENTICATION_FAILURE in findings:
        return SMOKE_CREDENTIAL_REJECTED
    if status == MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED and findings.intersection({"RESPONSE_SCHEMA_INVALID", "SCHEMA_FAILURE"}):
        return SMOKE_PROVIDER_RESPONSE_REJECTED
    if status == MONTH_ACQUISITION_PAGINATION_INVALID and "RANGE_COVERAGE_INCOMPLETE" in findings:
        return SMOKE_MONTH_INCOMPLETE
    if status in {"MONTH_ACQUISITION_RETRY_EXHAUSTED", "MONTH_ACQUISITION_BLOCKED"}:
        return SMOKE_TRANSPORT_FAILED
    return SMOKE_INVALID


def _safe_receipts(monthly_receipt: dict[str, object], artifact_types: set[str]) -> list[dict[str, object]]:
    receipts = monthly_receipt.get("artifact_receipts", [])
    if not isinstance(receipts, list):
        return []
    safe: list[dict[str, object]] = []
    for item in receipts:
        if isinstance(item, dict) and item.get("artifact_type") in artifact_types:
            safe.append(
                {
                    "artifact_id": item.get("artifact_id"),
                    "artifact_type": item.get("artifact_type"),
                    "manifest_ref": item.get("manifest_ref"),
                    "semantic_payload_digest": item.get("semantic_payload_digest"),
                }
            )
    return safe


def _load_completeness_window(run_root: str | Path, monthly_receipt: dict[str, object]) -> tuple[str | None, str | None]:
    completeness = _safe_receipts(monthly_receipt, {ARTIFACT_MONTH_CHUNK_COMPLETENESS_MANIFEST})
    if not completeness:
        return None, None
    manifest_ref = completeness[0].get("manifest_ref")
    if not isinstance(manifest_ref, str):
        return None, None
    manifest_path = artifacts._safe_ref_to_path(run_root, manifest_ref)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload_path = artifacts._safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    return payload.get("first_source_window_start_utc"), payload.get("last_source_window_start_utc")


def _write_smoke_receipt(run_root: str | Path, run_id: str, receipt: dict[str, object]) -> dict[str, object]:
    root = Path(run_root)
    receipt_dir = root / run_id / "smoke_receipt"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_dir / "smoke-receipt.json"
    receipt = dict(receipt)
    receipt["smoke_receipt_ref"] = artifacts._safe_relative_path(receipt_path, root)
    payload = artifacts.canonical_json_bytes(receipt)
    temp_path = artifacts._write_temp_bytes(receipt_dir, payload, ".smoke-receipt.tmp")
    artifacts._install_without_replace(temp_path, receipt_path)
    receipt["smoke_receipt_sha256"] = artifacts.sha256_bytes(payload)
    return receipt


def _smoke_receipt(
    *,
    smoke_status: str,
    spec: MassiveSmokeSpec,
    run_id: str | None,
    monthly_receipt: dict[str, object] | None = None,
    fixed_findings: list[str] | None = None,
) -> dict[str, object]:
    monthly = monthly_receipt or {}
    raw_page_count = len(_safe_receipts(monthly, {ARTIFACT_RAW_PROVIDER_PAGE}))
    if raw_page_count == 0 and isinstance(monthly.get("raw_page_count"), int):
        raw_page_count = int(monthly["raw_page_count"])
    normalized = _safe_receipts(
        monthly,
        {ARTIFACT_MONTH_NORMALIZED_15M_OHLCV, ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS},
    )
    return {
        "smoke_status": smoke_status,
        "smoke_specification_digest": smoke_spec_digest(spec),
        "smoke_run_id": run_id,
        "classification": spec.classification,
        "provenance": LIVE_PROVIDER_SMOKE_PROVENANCE,
        "provider_identity": spec.provider,
        "ticker": spec.ticker,
        "month_key": spec.month_key,
        "request_status": monthly.get("status"),
        "provider_execution_enabled": monthly.get("provider_execution_enabled", False),
        "attempt_count": monthly.get("attempt_count", 0),
        "accepted_page_count": monthly.get("accepted_page_count", 0),
        "pagination_status": monthly.get("pagination_status"),
        "completeness_status": monthly.get("completeness_status"),
        "normalized_artifact_receipts": normalized,
        "raw_page_count": raw_page_count,
        "total_normalized_row_count": monthly.get("row_count", 0),
        "first_source_window_start_utc": None,
        "last_source_window_start_utc": None,
        "contract_v2_1_digest": spec.contract_v2_1_digest,
        "strategy_enabled": False,
        "calendar_bar_derivation_enabled": False,
        "registry_eligibility": False,
        "canonical_eligibility": False,
        "acquisition_enabled": False,
        "runtime_migration_enabled": False,
        "fixed_findings": fixed_findings or list(monthly.get("fixed_findings", [])),
        "sanitization": "NO_KEY_NO_AUTH_HEADER_NO_RAW_URL_NO_NEXT_URL_NO_RAW_BODY_NO_OHLCV_NO_ABSOLUTE_PATHS_NO_RAW_EXCEPTIONS",
    }


def run_massive_smoke_live(
    *,
    run_root: str | Path = SMOKE_RUNTIME_ROOT,
    _input_func: Callable[[str], str] = input,
    _getpass_func: Callable[[str], str] = getpass.getpass,
    _is_interactive: Callable[[], bool] = _stdio_is_interactive,
    _transport_factory: Callable[[MonthChunkRequest, ProviderApiKey], MassiveRestTransport] | None = None,
    _run_id_factory: Callable[[], str] = _opaque_smoke_run_id,
    _authorization_state: _AuthorizationState | None = None,
    _emit_ceremony: bool = True,
) -> dict[str, object]:
    spec = default_smoke_spec()
    plan = smoke_plan_receipt(spec)
    if not _is_interactive():
        return _smoke_receipt(
            smoke_status=SMOKE_AUTHORIZATION_REJECTED,
            spec=spec,
            run_id=None,
            fixed_findings=["LIVE_SMOKE_REQUIRES_INTERACTIVE_TTY"],
        )
    if _emit_ceremony:
        print(json.dumps(plan, sort_keys=True, indent=2))
        print(SMOKE_CLASSIFICATION)
        print(_NO_STRATEGY_TEXT)
        print(_NO_REGISTRY_TEXT)
        print(_NO_PERFORMANCE_TEXT)
    try:
        confirmation = _input_func("Type confirmation phrase: ")
        state = _authorization_state if _authorization_state is not None else _LIVE_AUTHORIZATION_STATE
        _authorize_smoke(confirmation, spec=spec, state=state)
    except MassiveSmokeError:
        return _smoke_receipt(
            smoke_status=SMOKE_AUTHORIZATION_REJECTED,
            spec=spec,
            run_id=None,
            fixed_findings=["SMOKE_AUTHORIZATION_REJECTED"],
        )
    try:
        provider_key = ProviderApiKey(_getpass_func("Massive.com API key: "))
    except Exception:
        return _smoke_receipt(
            smoke_status=SMOKE_CREDENTIAL_REJECTED,
            spec=spec,
            run_id=None,
            fixed_findings=["SMOKE_CREDENTIAL_REJECTED"],
        )

    month_request = _month_request_from_spec(spec)
    actual_run_id = _run_id_factory()
    transport = (_transport_factory or (lambda request, key: MassiveRestTransport(month_request=request, api_key=key)))(
        month_request, provider_key
    )
    try:
        monthly_receipt = execute_fake_monthly_acquisition(
            month_request=month_request,
            transport=transport,
            run_root=run_root,
            run_id=actual_run_id,
            sleeper=RecordingSleeper([]),
            provenance=LIVE_PROVIDER_SMOKE_PROVENANCE,
            provider_execution_enabled=True,
        )
    finally:
        close = getattr(transport, "close", None)
        if callable(close):
            close()
        del provider_key
    smoke_status = _smoke_status_from_monthly(monthly_receipt)
    receipt = _smoke_receipt(smoke_status=smoke_status, spec=spec, run_id=actual_run_id, monthly_receipt=monthly_receipt)
    first, last = _load_completeness_window(run_root, monthly_receipt) if smoke_status == SMOKE_COMPLETED_NONCANONICAL else (None, None)
    receipt["first_source_window_start_utc"] = first
    receipt["last_source_window_start_utc"] = last
    return _write_smoke_receipt(run_root, actual_run_id, receipt)


def massive_smoke_plan() -> dict[str, object]:
    return smoke_plan_receipt()


def massive_smoke_self_check() -> dict[str, object]:
    spec = default_smoke_spec()
    next_url = (
        "https://api.massive.com/v2/aggs/ticker/AAPL/range/15/minute/"
        "2025-01-01/2025-01-31?cursor=selfcheck&adjusted=true&sort=asc&limit=50000"
    )
    bodies = iter(
        [
            b'{"adjusted":true,"queryCount":1,"results":[{"c":100,"h":101,"l":99,"n":1,"o":100,"t":1735741800000,"v":1000}],"resultsCount":1,"status":"OK","ticker":"AAPL","next_url":"'
            + next_url.encode("utf-8")
            + b'"}',
            b'{"adjusted":true,"queryCount":1,"results":[{"c":101,"h":102,"l":100,"n":1,"o":101,"t":1738333800000,"v":1000}],"resultsCount":1,"status":"OK","ticker":"AAPL"}',
        ]
    )

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"Content-Type": "application/json"}, content=next(bodies))

    def transport_factory(month_request: MonthChunkRequest, api_key: ProviderApiKey) -> MassiveRestTransport:
        return MassiveRestTransport(month_request=month_request, api_key=api_key, http_transport=httpx.MockTransport(handler))

    with tempfile.TemporaryDirectory(prefix="marketflow-massive-smoke-self-check-") as run_root:
        receipt = run_massive_smoke_live(
            run_root=run_root,
            _input_func=lambda prompt: smoke_confirmation_phrase(spec),
            _getpass_func=lambda prompt: "fictional-smoke-self-check-key",
            _is_interactive=lambda: True,
            _transport_factory=transport_factory,
            _run_id_factory=lambda: "smoke-self-check-run",
            _authorization_state=_AuthorizationState(),
            _emit_ceremony=False,
        )
    result = dict(receipt)
    result["status"] = "MASSIVE_SMOKE_SELF_CHECK"
    result["mock_http_only"] = True
    result["real_provider_call_performed"] = False
    result["persistent_artifact_written"] = False
    return result
