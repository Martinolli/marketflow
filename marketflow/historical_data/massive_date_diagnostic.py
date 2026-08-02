"""Noncanonical Massive.com date-differential diagnostic boundary."""

from __future__ import annotations

import getpass
import json
import sys
from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any, Callable

import httpx

from marketflow.historical_data import artifacts
from marketflow.historical_data.massive_transport import (
    AUTHENTICATION_FAILURE,
    CONTENT_TYPE,
    MASSIVE_ADJUSTED,
    MASSIVE_LIMIT,
    MASSIVE_MULTIPLIER,
    MASSIVE_REST_HOST,
    MASSIVE_REST_SCHEME,
    MASSIVE_SORT,
    MASSIVE_TIMESPAN,
    MassiveTransportError,
    ProviderApiKey,
)
from marketflow.historical_data.provider_response import (
    AGGREGATE_ROW_FIELDS,
    AGGREGATE_ROW_REQUIRED_FIELDS,
    TOP_LEVEL_FIELDS,
    ProviderResponseError,
    ResponseRequestContext,
    parse_provider_response,
)


DATE_DIAGNOSTIC_SCHEMA_VERSION = "marketflow.massive_provider_date_diagnostic.v1"
DATE_DIAGNOSTIC_CLASSIFICATION = "NONCANONICAL_PROVIDER_DATE_DIAGNOSTIC"
DATE_DIAGNOSTIC_PROVIDER = "MASSIVE.COM"
DATE_DIAGNOSTIC_ENDPOINT = "STOCKS_CUSTOM_BARS_V2"
DATE_DIAGNOSTIC_TICKER = "AAPL"
DATE_DIAGNOSTIC_MONTH_KEY = "2026-01"
DATE_DIAGNOSTIC_EFFECTIVE_START = "2026-01-01"
DATE_DIAGNOSTIC_EFFECTIVE_END = "2026-01-31"
DATE_DIAGNOSTIC_MAXIMUM_PROVIDER_PAGES = 1
DATE_DIAGNOSTIC_DIGEST_PREFIX_LENGTH = 12

DATE_DIAGNOSTIC_PLAN_VALID = "DATE_DIAGNOSTIC_PLAN_VALID"
DATE_DIAGNOSTIC_SCHEMA_ACCEPTED = "DATE_DIAGNOSTIC_SCHEMA_ACCEPTED"
DATE_DIAGNOSTIC_SCHEMA_REJECTED = "DATE_DIAGNOSTIC_SCHEMA_REJECTED"
DATE_DIAGNOSTIC_TRANSPORT_FAILED = "DATE_DIAGNOSTIC_TRANSPORT_FAILED"
DATE_DIAGNOSTIC_AUTHENTICATION_FAILED = "DATE_DIAGNOSTIC_AUTHENTICATION_FAILED"
DATE_DIAGNOSTIC_INVALID = "DATE_DIAGNOSTIC_INVALID"

PARSER_SCHEMA_ACCEPTED = "RESPONSE_SCHEMA_ACCEPTED"
PARSER_SCHEMA_REJECTED = "RESPONSE_SCHEMA_REJECTED"
PARSER_NOT_RUN = "RESPONSE_SCHEMA_NOT_RUN"

_NO_STRATEGY_TEXT = "NO STRATEGY"
_NO_CANONICAL_TEXT = "NO CANONICAL ACQUISITION"
_NO_REGISTRY_TEXT = "NO REGISTRY"
_SENSITIVE_FIELD_NAMES = frozenset({"next_url", "request_id"})


class MassiveDateDiagnosticError(ValueError):
    """Raised when the fixed date-diagnostic boundary is violated."""


@dataclass(frozen=True, slots=True)
class MassiveDateDiagnosticSpec:
    schema_version: str
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
    maximum_provider_pages: int
    canonical_eligibility: bool
    registry_eligibility: bool
    acquisition_generation_eligibility: bool
    strategy_enabled: bool

    def validate(self) -> None:
        expected = {
            "schema_version": DATE_DIAGNOSTIC_SCHEMA_VERSION,
            "classification": DATE_DIAGNOSTIC_CLASSIFICATION,
            "provider": DATE_DIAGNOSTIC_PROVIDER,
            "endpoint": DATE_DIAGNOSTIC_ENDPOINT,
            "ticker": DATE_DIAGNOSTIC_TICKER,
            "month_key": DATE_DIAGNOSTIC_MONTH_KEY,
            "effective_start": DATE_DIAGNOSTIC_EFFECTIVE_START,
            "effective_end": DATE_DIAGNOSTIC_EFFECTIVE_END,
            "multiplier": MASSIVE_MULTIPLIER,
            "timespan": MASSIVE_TIMESPAN,
            "adjusted": MASSIVE_ADJUSTED,
            "sort": MASSIVE_SORT,
            "limit": MASSIVE_LIMIT,
            "maximum_provider_pages": DATE_DIAGNOSTIC_MAXIMUM_PROVIDER_PAGES,
            "canonical_eligibility": False,
            "registry_eligibility": False,
            "acquisition_generation_eligibility": False,
            "strategy_enabled": False,
        }
        for key, value in expected.items():
            if getattr(self, key) != value:
                raise MassiveDateDiagnosticError("date diagnostic fixed field mismatch")


@dataclass(slots=True)
class _AuthorizationState:
    authorized_digest: str | None = None


@dataclass(frozen=True, slots=True)
class _HttpOutcome:
    http_status: int | None
    response_body_complete: bool
    body: bytes | None
    failure_category: str | None
    request_count: int


_LIVE_AUTHORIZATION_STATE = _AuthorizationState()


def default_date_diagnostic_spec() -> MassiveDateDiagnosticSpec:
    return MassiveDateDiagnosticSpec(
        schema_version=DATE_DIAGNOSTIC_SCHEMA_VERSION,
        classification=DATE_DIAGNOSTIC_CLASSIFICATION,
        provider=DATE_DIAGNOSTIC_PROVIDER,
        endpoint=DATE_DIAGNOSTIC_ENDPOINT,
        ticker=DATE_DIAGNOSTIC_TICKER,
        month_key=DATE_DIAGNOSTIC_MONTH_KEY,
        effective_start=DATE_DIAGNOSTIC_EFFECTIVE_START,
        effective_end=DATE_DIAGNOSTIC_EFFECTIVE_END,
        multiplier=MASSIVE_MULTIPLIER,
        timespan=MASSIVE_TIMESPAN,
        adjusted=MASSIVE_ADJUSTED,
        sort=MASSIVE_SORT,
        limit=MASSIVE_LIMIT,
        maximum_provider_pages=DATE_DIAGNOSTIC_MAXIMUM_PROVIDER_PAGES,
        canonical_eligibility=False,
        registry_eligibility=False,
        acquisition_generation_eligibility=False,
        strategy_enabled=False,
    )


def date_diagnostic_spec_payload(spec: MassiveDateDiagnosticSpec | None = None) -> dict[str, object]:
    actual = spec or default_date_diagnostic_spec()
    return asdict(actual)


def date_diagnostic_spec_digest(spec: MassiveDateDiagnosticSpec | None = None) -> str:
    return artifacts.sha256_bytes(artifacts.canonical_json_bytes(date_diagnostic_spec_payload(spec)))


def date_diagnostic_digest_prefix(spec: MassiveDateDiagnosticSpec | None = None) -> str:
    return date_diagnostic_spec_digest(spec)[:DATE_DIAGNOSTIC_DIGEST_PREFIX_LENGTH]


def date_diagnostic_confirmation_phrase(spec: MassiveDateDiagnosticSpec | None = None) -> str:
    return f"RUN MARKETFLOW MASSIVE DATE DIAGNOSTIC {date_diagnostic_digest_prefix(spec)}"


def _safe_identifier(value: str) -> str:
    if type(value) is not str or not value or len(value) > 64:
        return "UNSAFE_IDENTIFIER"
    if not all(char.isascii() and (char.isalnum() or char == "_") for char in value):
        return "UNSAFE_IDENTIFIER"
    return value


def _safe_field_names(fields: set[str]) -> list[str]:
    return sorted({_safe_identifier(field) for field in fields if field not in _SENSITIVE_FIELD_NAMES})


def _json_type_category(value: object) -> str:
    if value is None:
        return "NULL"
    if type(value) is bool:
        return "BOOL"
    if type(value) is int:
        return "INTEGER"
    if type(value) is Decimal:
        return "NUMBER"
    if type(value) is str:
        return "STRING"
    if isinstance(value, list):
        return "ARRAY"
    if isinstance(value, dict):
        return "OBJECT"
    return "UNKNOWN"


def _json_constant(value: str) -> None:
    raise ValueError(f"JSON constant rejected: {value}")


def _load_json_for_diagnostics(body: bytes | None) -> object | None:
    if not body:
        return None
    try:
        return json.loads(body.decode("utf-8"), parse_float=Decimal, parse_int=int, parse_constant=_json_constant)
    except (UnicodeDecodeError, ValueError):
        return None


def _optional_count(value: object) -> int | None:
    if type(value) is int and value >= 0:
        return value
    return None


def _provider_status(value: object) -> str | None:
    if type(value) is not str:
        return None
    return _safe_identifier(value)


def _structural_diagnostics(body: bytes | None) -> dict[str, object]:
    payload = _load_json_for_diagnostics(body)
    diagnostics: dict[str, object] = {
        "top_level_fields": [],
        "aggregate_row_field_sets": [],
        "missing_top_level_fields": [],
        "unexpected_top_level_fields": [],
        "aggregate_row_failures": [],
        "type_mismatches": [],
        "query_count": None,
        "results_count": None,
        "results_present": False,
        "continuation_present": False,
        "provider_response_status": None,
    }
    if not isinstance(payload, dict):
        diagnostics["top_level_type"] = _json_type_category(payload)
        return diagnostics
    top_fields = set(payload)
    diagnostics["top_level_fields"] = _safe_field_names(top_fields)
    diagnostics["missing_top_level_fields"] = _safe_field_names(
        {"adjusted", "queryCount", "results", "resultsCount", "status", "ticker"} - top_fields
    )
    diagnostics["unexpected_top_level_fields"] = _safe_field_names(top_fields - TOP_LEVEL_FIELDS)
    diagnostics["query_count"] = _optional_count(payload.get("queryCount"))
    diagnostics["results_count"] = _optional_count(payload.get("resultsCount"))
    diagnostics["provider_response_status"] = _provider_status(payload.get("status"))
    diagnostics["continuation_present"] = payload.get("next_url") is not None
    type_mismatches: list[dict[str, object]] = []
    expected_top_level = {
        "adjusted": "BOOL",
        "count": "INTEGER",
        "queryCount": "INTEGER",
        "results": "ARRAY",
        "resultsCount": "INTEGER",
        "status": "STRING",
        "ticker": "STRING",
    }
    for field, expected in expected_top_level.items():
        if field not in payload:
            continue
        actual = _json_type_category(payload[field])
        if actual != expected:
            type_mismatches.append(
                {
                    "scope": "top_level",
                    "field": _safe_identifier(field),
                    "expected_type": expected,
                    "actual_type": actual,
                }
            )
    results = payload.get("results")
    diagnostics["results_present"] = isinstance(results, list) and len(results) > 0
    if not isinstance(results, list):
        diagnostics["results_type"] = _json_type_category(results)
        diagnostics["type_mismatches"] = type_mismatches
        return diagnostics
    row_field_sets: list[list[str]] = []
    row_failures: list[dict[str, object]] = []
    for index, item in enumerate(results):
        if not isinstance(item, dict):
            row_failures.append({"row_index": index, "row_type": _json_type_category(item)})
            continue
        row_fields = set(item)
        row_field_sets.append(_safe_field_names(row_fields))
        unexpected = row_fields - AGGREGATE_ROW_FIELDS
        missing = AGGREGATE_ROW_REQUIRED_FIELDS - row_fields
        if unexpected or missing:
            row_failures.append(
                {
                    "row_index": index,
                    "unexpected_row_fields": _safe_field_names(unexpected),
                    "missing_row_fields": _safe_field_names(missing),
                }
            )
        for field in sorted(AGGREGATE_ROW_REQUIRED_FIELDS | {"n", "otc"}):
            if field not in item:
                continue
            actual = _json_type_category(item[field])
            expected = "BOOL" if field == "otc" else "INTEGER" if field in {"n", "t"} else "NUMBER"
            if actual != expected and not (expected == "NUMBER" and actual == "INTEGER"):
                type_mismatches.append(
                    {
                        "scope": "aggregate_row",
                        "row_index": index,
                        "field": _safe_identifier(field),
                        "expected_type": expected,
                        "actual_type": actual,
                    }
                )
    diagnostics["aggregate_row_field_sets"] = row_field_sets
    diagnostics["aggregate_row_failures"] = row_failures
    diagnostics["type_mismatches"] = type_mismatches
    return diagnostics


def _request_url(spec: MassiveDateDiagnosticSpec) -> str:
    path = f"/v2/aggs/ticker/{spec.ticker}/range/{spec.multiplier}/{spec.timespan}/{spec.effective_start}/{spec.effective_end}"
    query = f"adjusted={str(spec.adjusted).lower()}&sort={spec.sort}&limit={spec.limit}"
    return f"{MASSIVE_REST_SCHEME}://{MASSIVE_REST_HOST}{path}?{query}"


def _request_context(spec: MassiveDateDiagnosticSpec) -> ResponseRequestContext:
    return ResponseRequestContext(
        canonical_ticker=spec.ticker,
        month_key=spec.month_key,
        effective_start_date=spec.effective_start,
        effective_end_date=spec.effective_end,
        adjusted=spec.adjusted,
        sort=spec.sort,
        limit=spec.limit,
        month_request_digest=date_diagnostic_spec_digest(spec),
    )


def _send_one_request(
    spec: MassiveDateDiagnosticSpec,
    api_key: ProviderApiKey,
    *,
    http_transport: httpx.BaseTransport | None = None,
) -> _HttpOutcome:
    client = httpx.Client(
        timeout=httpx.Timeout(connect=10, read=30, write=10, pool=10),
        follow_redirects=False,
        trust_env=False,
        verify=True,
        transport=http_transport,
    )
    try:
        with client.stream(
            "GET",
            _request_url(spec),
            headers={
                "Authorization": api_key.authorization_header(),
                "Accept": "application/json",
                "Accept-Encoding": "identity",
                "User-Agent": "MarketFlow-Massive-Date-Diagnostic/1",
            },
        ) as response:
            if response.status_code == 401:
                return _HttpOutcome(response.status_code, False, None, AUTHENTICATION_FAILURE, 1)
            body = response.read()
            return _HttpOutcome(response.status_code, True, body, None, 1)
    except httpx.TimeoutException:
        return _HttpOutcome(None, False, None, "TRANSPORT_TIMEOUT", 1)
    except httpx.TransportError:
        return _HttpOutcome(None, False, None, "TRANSPORT_FAILURE", 1)
    finally:
        client.cookies.clear()
        client.close()


def _base_receipt(spec: MassiveDateDiagnosticSpec, *, status: str) -> dict[str, object]:
    return {
        "status": status,
        "schema_version": spec.schema_version,
        "classification": spec.classification,
        "provider": spec.provider,
        "endpoint": spec.endpoint,
        "ticker": spec.ticker,
        "effective_start": spec.effective_start,
        "effective_end": spec.effective_end,
        "multiplier": spec.multiplier,
        "timespan": spec.timespan,
        "adjusted": spec.adjusted,
        "sort": spec.sort,
        "limit": spec.limit,
        "maximum_provider_pages": spec.maximum_provider_pages,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "acquisition_generation_eligibility": False,
        "strategy_enabled": False,
        "diagnostic_specification_digest": date_diagnostic_spec_digest(spec),
        "network_execution_enabled": False,
        "credential_prompted": False,
        "request_performed": False,
        "transport_invocation_count": 0,
        "http_status": None,
        "response_body_complete": False,
        "parser_status": PARSER_NOT_RUN,
        "top_level_fields": [],
        "aggregate_row_field_sets": [],
        "missing_top_level_fields": [],
        "unexpected_top_level_fields": [],
        "aggregate_row_failures": [],
        "type_mismatches": [],
        "query_count": None,
        "results_count": None,
        "results_present": False,
        "continuation_present": False,
        "provider_response_status": None,
        "normalized_artifact_created": False,
        "raw_provider_body_persisted": False,
        "monthly_executor_invoked": False,
        "pagination_followed": False,
        "retry_attempted": False,
        "runtime_migration_performed": False,
        "fixed_findings": [],
        "sanitization": "NO_KEY_NO_AUTH_HEADER_NO_RAW_URL_NO_NEXT_URL_NO_CURSOR_NO_REQUEST_ID_VALUE_NO_RAW_BODY_NO_MARKET_VALUES_NO_RAW_EXCEPTIONS_NO_ABSOLUTE_PATHS",
    }


def date_diagnostic_plan_receipt(spec: MassiveDateDiagnosticSpec | None = None) -> dict[str, object]:
    actual = spec or default_date_diagnostic_spec()
    actual.validate()
    receipt = _base_receipt(actual, status=DATE_DIAGNOSTIC_PLAN_VALID)
    receipt["operator_confirmation_phrase"] = date_diagnostic_confirmation_phrase(actual)
    receipt["required_warnings"] = [_NO_STRATEGY_TEXT, _NO_CANONICAL_TEXT, _NO_REGISTRY_TEXT]
    return receipt


def _authorize_diagnostic(confirmation: str, *, spec: MassiveDateDiagnosticSpec, state: _AuthorizationState) -> None:
    digest = date_diagnostic_spec_digest(spec)
    if state.authorized_digest == digest:
        raise MassiveDateDiagnosticError("date diagnostic authorization already used")
    if confirmation != date_diagnostic_confirmation_phrase(spec):
        raise MassiveDateDiagnosticError("date diagnostic authorization phrase mismatch")
    state.authorized_digest = digest


def _stdio_is_interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def _parse_outcome(spec: MassiveDateDiagnosticSpec, outcome: _HttpOutcome) -> dict[str, object]:
    receipt = _base_receipt(spec, status=DATE_DIAGNOSTIC_TRANSPORT_FAILED)
    receipt["network_execution_enabled"] = True
    receipt["request_performed"] = True
    receipt["transport_invocation_count"] = outcome.request_count
    receipt["http_status"] = outcome.http_status
    receipt["response_body_complete"] = outcome.response_body_complete
    if outcome.failure_category == AUTHENTICATION_FAILURE or outcome.http_status == 401:
        receipt["status"] = DATE_DIAGNOSTIC_AUTHENTICATION_FAILED
        receipt["fixed_findings"] = [AUTHENTICATION_FAILURE]
        return receipt
    if outcome.http_status != 200 or outcome.body is None:
        receipt["status"] = DATE_DIAGNOSTIC_TRANSPORT_FAILED
        receipt["fixed_findings"] = [outcome.failure_category or "HTTP_STATUS_NON_SUCCESS"]
        return receipt
    diagnostics = _structural_diagnostics(outcome.body)
    receipt.update(diagnostics)
    try:
        parse_provider_response(
            outcome.body,
            body_sha256=artifacts.sha256_bytes(outcome.body),
            context=_request_context(spec),
        )
    except ProviderResponseError:
        receipt["status"] = DATE_DIAGNOSTIC_SCHEMA_REJECTED
        receipt["parser_status"] = PARSER_SCHEMA_REJECTED
        receipt["fixed_findings"] = ["RESPONSE_SCHEMA_INVALID"]
        return receipt
    receipt["status"] = DATE_DIAGNOSTIC_SCHEMA_ACCEPTED
    receipt["parser_status"] = PARSER_SCHEMA_ACCEPTED
    return receipt


def run_massive_date_diagnostic_2026_live(
    *,
    _input_func: Callable[[str], str] = input,
    _getpass_func: Callable[[str], str] = getpass.getpass,
    _is_interactive: Callable[[], bool] = _stdio_is_interactive,
    _http_transport: httpx.BaseTransport | None = None,
    _authorization_state: _AuthorizationState | None = None,
    _emit_ceremony: bool = True,
) -> dict[str, object]:
    spec = default_date_diagnostic_spec()
    plan = date_diagnostic_plan_receipt(spec)
    if not _is_interactive():
        receipt = _base_receipt(spec, status=DATE_DIAGNOSTIC_INVALID)
        receipt["fixed_findings"] = ["DATE_DIAGNOSTIC_REQUIRES_INTERACTIVE_TTY"]
        return receipt
    if _emit_ceremony:
        print(json.dumps(plan, sort_keys=True, indent=2))
    state = _authorization_state if _authorization_state is not None else _LIVE_AUTHORIZATION_STATE
    try:
        _authorize_diagnostic(_input_func("Type confirmation phrase: "), spec=spec, state=state)
    except MassiveDateDiagnosticError:
        receipt = _base_receipt(spec, status=DATE_DIAGNOSTIC_INVALID)
        receipt["fixed_findings"] = ["DATE_DIAGNOSTIC_AUTHORIZATION_REJECTED"]
        return receipt
    try:
        provider_key = ProviderApiKey(_getpass_func("Massive.com API key: "))
    except MassiveTransportError:
        receipt = _base_receipt(spec, status=DATE_DIAGNOSTIC_AUTHENTICATION_FAILED)
        receipt["credential_prompted"] = True
        receipt["fixed_findings"] = ["DATE_DIAGNOSTIC_CREDENTIAL_REJECTED"]
        return receipt
    try:
        outcome = _send_one_request(spec, provider_key, http_transport=_http_transport)
    finally:
        del provider_key
    receipt = _parse_outcome(spec, outcome)
    receipt["credential_prompted"] = True
    return receipt


def massive_date_diagnostic_2026_plan() -> dict[str, object]:
    return date_diagnostic_plan_receipt()


def massive_date_diagnostic_2026_self_check() -> dict[str, object]:
    spec = default_date_diagnostic_spec()
    valid_body = (
        b'{"adjusted":true,"queryCount":1,"results":[{"c":100,"h":101,"l":99,"n":1,'
        b'"o":100,"t":1767277800000,"v":1000,"vw":100.5,"otc":false}],'
        b'"resultsCount":1,"count":1,"status":"OK","ticker":"AAPL"}'
    )
    rejected_body = (
        b'{"adjusted":true,"queryCount":1,"results":[{"c":100,"h":101,"l":99,"n":1,'
        b'"o":100,"t":1767277800000,"v":1000,"mystery_row":"redacted"}],'
        b'"resultsCount":1,"status":"OK","ticker":"AAPL","mysteryTop":"redacted"}'
    )

    def run_body(body: bytes) -> dict[str, object]:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, headers={CONTENT_TYPE: "application/json"}, content=body)

        return run_massive_date_diagnostic_2026_live(
            _input_func=lambda prompt: date_diagnostic_confirmation_phrase(spec),
            _getpass_func=lambda prompt: "fictional-date-diagnostic-key",
            _is_interactive=lambda: True,
            _http_transport=httpx.MockTransport(handler),
            _authorization_state=_AuthorizationState(),
            _emit_ceremony=False,
        )

    valid = run_body(valid_body)
    rejected = run_body(rejected_body)
    return {
        "status": "MASSIVE_DATE_DIAGNOSTIC_2026_SELF_CHECK",
        "diagnostic_specification_digest": date_diagnostic_spec_digest(spec),
        "valid_schema_status": valid["status"],
        "rejected_schema_status": rejected["status"],
        "mock_http_only": True,
        "real_provider_call_performed": False,
        "persistent_artifact_written": False,
        "credential_source": "FICTIONAL_EXPLICIT_INJECTION",
        "request_count": int(valid["transport_invocation_count"]) + int(rejected["transport_invocation_count"]),
    }
