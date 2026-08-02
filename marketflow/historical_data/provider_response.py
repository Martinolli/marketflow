"""Strict Massive.com aggregate response parsing for fake monthly acquisition."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.research import acquisition_contract_v2_1 as contract_v21


PROJECTION_VERSION = "OHLCV_PLUS_CONTRACTED_AUDIT_FIELDS_V1"
VWAP_PRESENT = "VWAP_PRESENT"
VWAP_ABSENT = "VWAP_ABSENT"
TRANSACTION_COUNT_PRESENT = "TRANSACTION_COUNT_PRESENT"
TRANSACTION_COUNT_ABSENT = "TRANSACTION_COUNT_ABSENT"
VALID_PROVIDER_STATUSES = frozenset({"OK"})
TOP_LEVEL_FIELDS = frozenset({"adjusted", "count", "next_url", "queryCount", "request_id", "results", "resultsCount", "status", "ticker"})
AGGREGATE_ROW_REQUIRED_FIELDS = frozenset({"c", "h", "l", "o", "t", "v"})
AGGREGATE_ROW_OPTIONAL_FIELDS = frozenset({"n", "otc", "vw"})
AGGREGATE_ROW_FIELDS = AGGREGATE_ROW_REQUIRED_FIELDS | AGGREGATE_ROW_OPTIONAL_FIELDS
SCHEMA_DIAGNOSTIC_VERSION = "massive_custom_bars_schema_diagnostics.v1"
_MAX_DIAGNOSTIC_IDENTIFIER_LENGTH = 64
_SENSITIVE_DIAGNOSTIC_FIELD_NAMES = frozenset({"next_url", "request_id"})
TOP_LEVEL_SCHEMA = "TOP_LEVEL_SCHEMA"
ROW_SCHEMA = "ROW_SCHEMA"
ROW_TYPE = "ROW_TYPE"
TIMESTAMP_ORDER = "TIMESTAMP_ORDER"
TIMESTAMP_RANGE = "TIMESTAMP_RANGE"
OHLCV_GEOMETRY = "OHLCV_GEOMETRY"
COUNT_CONSISTENCY = "COUNT_CONSISTENCY"
TIMESTAMP_RANGE_INVALID = "TIMESTAMP_RANGE_INVALID"
SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE = "SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE"


class ProviderResponseError(ValueError):
    """Raised when a provider response fails strict offline contract parsing."""

    def __init__(
        self,
        message: str,
        *,
        sanitized_diagnostics: dict[str, Any] | None = None,
        failure_category: str | None = None,
    ) -> None:
        super().__init__(message)
        self.sanitized_diagnostics = sanitized_diagnostics
        self.failure_category = failure_category


@dataclass(frozen=True, slots=True)
class ResponseRequestContext:
    canonical_ticker: str
    month_key: str
    effective_start_date: str
    effective_end_date: str
    adjusted: bool
    sort: str
    limit: int
    month_request_digest: str


@dataclass(frozen=True, slots=True)
class AggregateRow:
    provider_timestamp: int
    window_start_utc: str
    window_end_utc: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    vwap: Decimal | None
    transaction_count: int | None
    raw_page_digest: str


@dataclass(frozen=True, slots=True)
class ParsedProviderResponse:
    ticker: str
    adjusted: bool
    status: str
    query_count: int
    results_count: int
    rows: tuple[AggregateRow, ...]
    continuation_present: bool
    raw_next_url: str | None
    sanitized_continuation_identity: str | None
    semantic_projection: dict[str, Any]
    semantic_projection_digest: str


def _reject_json_constant(value: str) -> None:
    raise ProviderResponseError(f"provider JSON constant is rejected: {value}")


def _object_pairs_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ProviderResponseError("provider JSON object contains duplicate keys")
        result[key] = value
    return result


def _load_json(body: bytes) -> Any:
    if type(body) is not bytes or not body:
        raise ProviderResponseError("provider response body must be non-empty bytes")
    try:
        text = body.decode("utf-8")
        return json.loads(
            text,
            parse_float=Decimal,
            parse_int=int,
            parse_constant=_reject_json_constant,
            object_pairs_hook=_object_pairs_without_duplicates,
        )
    except UnicodeDecodeError as exc:
        raise ProviderResponseError("provider response body must be UTF-8 JSON") from exc
    except json.JSONDecodeError as exc:
        raise ProviderResponseError("provider response body must be valid JSON") from exc


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProviderResponseError(f"{field_name} must be an object")
    return value


def _require_text(value: Any, field_name: str) -> str:
    if type(value) is not str or not value:
        raise ProviderResponseError(f"{field_name} must be non-empty text")
    return value


def _require_bool(value: Any, field_name: str) -> bool:
    if type(value) is not bool:
        raise ProviderResponseError(f"{field_name} must be boolean")
    return value


def _require_int(value: Any, field_name: str) -> int:
    if type(value) is not int:
        raise ProviderResponseError(f"{field_name} must be an exact integer")
    return value


def _safe_field_identifier(value: str) -> str:
    if type(value) is not str or not value or len(value) > _MAX_DIAGNOSTIC_IDENTIFIER_LENGTH:
        return "UNSAFE_FIELD_IDENTIFIER"
    if not all(char.isascii() and (char.isalnum() or char in {"_"}) for char in value):
        return "UNSAFE_FIELD_IDENTIFIER"
    return value


def _safe_field_names(values: set[str]) -> list[str]:
    return sorted({_safe_field_identifier(value) for value in values if value not in _SENSITIVE_DIAGNOSTIC_FIELD_NAMES})


def _json_type_category(value: Any) -> str:
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


def _schema_diagnostics(payload: Any) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {"schema_diagnostic_version": SCHEMA_DIAGNOSTIC_VERSION}
    if not isinstance(payload, dict):
        diagnostics["top_level_type"] = _json_type_category(payload)
        return diagnostics
    top_fields = set(payload)
    diagnostics["top_level_fields"] = _safe_field_names(top_fields)
    diagnostics["unexpected_top_level_fields"] = _safe_field_names(top_fields - TOP_LEVEL_FIELDS)
    diagnostics["missing_top_level_fields"] = _safe_field_names(
        field for field in {"adjusted", "queryCount", "results", "resultsCount", "status", "ticker"} if field not in payload
    )
    type_mismatches: list[dict[str, str]] = []
    expected_top_level = {
        "adjusted": "BOOL",
        "count": "INTEGER",
        "queryCount": "INTEGER",
        "resultsCount": "INTEGER",
        "status": "STRING",
        "ticker": "STRING",
    }
    for field, expected in expected_top_level.items():
        if field in payload:
            actual = _json_type_category(payload[field])
            if actual != expected:
                type_mismatches.append({"field": field, "expected_type": expected, "actual_type": actual})
    results = payload.get("results")
    if isinstance(results, list):
        row_field_sets: list[list[str]] = []
        row_failures: list[dict[str, Any]] = []
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
                if field in item:
                    actual = _json_type_category(item[field])
                    expected = "BOOL" if field == "otc" else "INTEGER" if field in {"n", "t"} else "NUMBER"
                    if actual != expected and not (expected == "NUMBER" and actual == "INTEGER"):
                        type_mismatches.append(
                            {
                                "field": _safe_field_identifier(field),
                                "row_index": index,
                                "scope": "aggregate_row",
                                "expected_type": expected,
                                "actual_type": actual,
                            }
                        )
        diagnostics["aggregate_row_field_sets"] = row_field_sets
        diagnostics["aggregate_row_failures"] = row_failures
    else:
        diagnostics["results_type"] = _json_type_category(results)
    diagnostics["type_mismatches"] = type_mismatches
    return diagnostics


def _diagnostics_with_category(diagnostics: dict[str, Any], failure_stage: str) -> dict[str, Any]:
    result = dict(diagnostics)
    result["failure_stage"] = failure_stage
    return result


def _raise_schema_error(message: str, payload: Any, *, failure_stage: str) -> None:
    raise ProviderResponseError(
        message,
        sanitized_diagnostics=_diagnostics_with_category(_schema_diagnostics(payload), failure_stage),
        failure_category="SCHEMA_FAILURE",
    )


def _reject_unknown_top_level_fields(payload: dict[str, Any]) -> None:
    if set(payload) - TOP_LEVEL_FIELDS:
        _raise_schema_error("provider response contains unexpected top-level field", payload, failure_stage=TOP_LEVEL_SCHEMA)


def _validate_optional_count(payload: dict[str, Any], results_count: int, result_length: int) -> None:
    if "count" not in payload:
        return
    if type(payload["count"]) is not int:
        _raise_schema_error("count must be an exact integer", payload, failure_stage=COUNT_CONSISTENCY)
    count = payload["count"]
    if count < 0 or count != results_count or count != result_length:
        _raise_schema_error("count must equal resultsCount and parsed result count", payload, failure_stage=COUNT_CONSISTENCY)


def _reject_unknown_or_missing_row_fields(row: dict[str, Any], payload: dict[str, Any], index: int) -> None:
    row_fields = set(row)
    if row_fields - AGGREGATE_ROW_FIELDS:
        _raise_schema_error(f"results[{index}] contains unexpected aggregate field", payload, failure_stage=ROW_SCHEMA)
    if AGGREGATE_ROW_REQUIRED_FIELDS - row_fields:
        _raise_schema_error(f"results[{index}] is missing required aggregate field", payload, failure_stage=ROW_SCHEMA)


def _validate_optional_otc(row: dict[str, Any], payload: dict[str, Any]) -> None:
    if "otc" in row and type(row["otc"]) is not bool:
        _raise_schema_error("results[].otc must be boolean", payload, failure_stage=ROW_SCHEMA)


def _require_decimal(value: Any, field_name: str) -> Decimal:
    if type(value) is bool or isinstance(value, str) or isinstance(value, float):
        raise ProviderResponseError(f"{field_name} must be a JSON number parsed without binary float")
    if type(value) is int:
        decimal = Decimal(value)
    elif type(value) is Decimal:
        decimal = value
    else:
        raise ProviderResponseError(f"{field_name} must be a JSON number")
    if decimal.is_nan() or decimal.is_infinite():
        raise ProviderResponseError(f"{field_name} must be finite")
    if decimal == 0:
        return Decimal("0")
    return decimal


def _canonical_decimal(value: Decimal) -> str:
    if value == 0:
        return "0"
    normalized = value.normalize()
    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _date_from_iso(value: str, field_name: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ProviderResponseError(f"{field_name} must be an ISO date") from exc


def _iso_utc(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ProviderResponseError("timestamp must be timezone-aware")
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _local_date_bounds_as_utc(start_date: date, end_date: date) -> tuple[datetime, datetime]:
    source_tz = ZoneInfo(contract_v21.SESSION_MAPPING_TIMEZONE)
    local_start = datetime.combine(start_date, time.min, tzinfo=source_tz)
    local_end_exclusive = datetime.combine(end_date + timedelta(days=1), time.min, tzinfo=source_tz)
    return local_start.astimezone(UTC), local_end_exclusive.astimezone(UTC)


def _validate_source_window_in_effective_local_range(
    *,
    window_start: datetime,
    window_end: datetime,
    utc_start: datetime,
    utc_end_exclusive: datetime,
    row_index: int,
) -> None:
    for field_name, value in {
        "window_start": window_start,
        "window_end": window_end,
        "utc_start": utc_start,
        "utc_end_exclusive": utc_end_exclusive,
    }.items():
        if value.tzinfo is None or value.utcoffset() is None:
            raise ProviderResponseError(
                f"{field_name} must be timezone-aware",
                sanitized_diagnostics={
                    "schema_diagnostic_version": SCHEMA_DIAGNOSTIC_VERSION,
                    "failure_stage": TIMESTAMP_RANGE,
                    "failure_category": TIMESTAMP_RANGE_INVALID,
                    "row_index": row_index,
                    "source_timezone": contract_v21.SESSION_MAPPING_TIMEZONE,
                },
                failure_category=TIMESTAMP_RANGE_INVALID,
            )
    if window_start < utc_start or window_start >= utc_end_exclusive or window_end > utc_end_exclusive:
        raise ProviderResponseError(
            "provider source window falls outside effective local date range",
            sanitized_diagnostics={
                "schema_diagnostic_version": SCHEMA_DIAGNOSTIC_VERSION,
                "failure_stage": TIMESTAMP_RANGE,
                "failure_category": TIMESTAMP_RANGE_INVALID,
                "fixed_finding": SOURCE_WINDOW_OUTSIDE_EFFECTIVE_LOCAL_DATE_RANGE,
                "row_index": row_index,
                "source_timezone": contract_v21.SESSION_MAPPING_TIMEZONE,
            },
            failure_category=TIMESTAMP_RANGE_INVALID,
        )


def _parse_query(query: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    if not query:
        raise ProviderResponseError("continuation URL must include query")
    for part in query.split("&"):
        if not part or "=" not in part:
            raise ProviderResponseError("continuation URL query is malformed")
        key, value = part.split("=", 1)
        lower_key = key.lower()
        if any(secret in lower_key for secret in ("api", "key", "token", "secret", "credential", "auth", "account")):
            raise ProviderResponseError("continuation URL contains prohibited credential-like parameter")
        if key in parsed:
            raise ProviderResponseError("continuation URL query contains duplicate parameter")
        parsed[key] = value
    return parsed


def sanitize_continuation_identity(raw_next_url: Any, context: ResponseRequestContext) -> str | None:
    if raw_next_url is None:
        return None
    raw = _require_text(raw_next_url, "next_url")
    prefix = "https://api.massive.com"
    if not raw.startswith(prefix):
        raise ProviderResponseError("continuation URL must target Massive.com aggregate API")
    remainder = raw[len(prefix) :]
    if "#" in remainder:
        raise ProviderResponseError("continuation URL fragments are prohibited")
    path, separator, query = remainder.partition("?")
    if separator != "?":
        raise ProviderResponseError("continuation URL must include sanitized query material")
    expected_path_prefix = f"/v2/aggs/ticker/{context.canonical_ticker}/range/15/minute/"
    if not path.startswith(expected_path_prefix):
        raise ProviderResponseError("continuation URL path does not match the month request")
    range_suffix = path[len(expected_path_prefix) :]
    range_parts = range_suffix.split("/")
    if range_parts != [context.effective_start_date, context.effective_end_date]:
        raise ProviderResponseError("continuation URL range does not match the month request")
    params = _parse_query(query)
    allowed = {"cursor", "adjusted", "sort", "limit"}
    if set(params) - allowed:
        raise ProviderResponseError("continuation URL contains unsupported parameter")
    cursor = params.get("cursor")
    if not cursor:
        raise ProviderResponseError("continuation URL must include an opaque cursor")
    if params.get("adjusted", str(context.adjusted).lower()) != str(context.adjusted).lower():
        raise ProviderResponseError("continuation adjusted parameter mismatch")
    if params.get("sort", context.sort) != context.sort:
        raise ProviderResponseError("continuation sort parameter mismatch")
    if params.get("limit", str(context.limit)) != str(context.limit):
        raise ProviderResponseError("continuation limit parameter mismatch")
    return "cont-" + semantic_digest(
        {
            "cursor": cursor,
            "month_key": context.month_key,
            "month_request_digest": context.month_request_digest,
            "ticker": context.canonical_ticker,
        }
    )[:24]


def parse_provider_response(
    body: bytes,
    *,
    body_sha256: str,
    context: ResponseRequestContext,
) -> ParsedProviderResponse:
    payload = _require_mapping(_load_json(body), "provider response")
    _reject_unknown_top_level_fields(payload)
    ticker = _require_text(payload.get("ticker"), "ticker")
    if ticker != context.canonical_ticker:
        raise ProviderResponseError("provider ticker mismatch")
    adjusted = _require_bool(payload.get("adjusted"), "adjusted")
    if adjusted is not context.adjusted:
        raise ProviderResponseError("provider adjusted flag mismatch")
    status = _require_text(payload.get("status"), "status")
    if status not in VALID_PROVIDER_STATUSES:
        raise ProviderResponseError("provider status is not accepted")
    query_count = _require_int(payload.get("queryCount"), "queryCount")
    results_count = _require_int(payload.get("resultsCount"), "resultsCount")
    results = payload.get("results")
    if not isinstance(results, list):
        raise ProviderResponseError("results must be an array")
    _validate_optional_count(payload, results_count, len(results))
    if results_count != len(results):
        raise ProviderResponseError("resultsCount must equal parsed result count")
    if results_count <= 0:
        raise ProviderResponseError("provider response must contain at least one aggregate row")
    if query_count < results_count or query_count < 0 or results_count < 0:
        raise ProviderResponseError("provider counts must be nonnegative and coherent")

    start_date = _date_from_iso(context.effective_start_date, "effective_start_date")
    end_date = _date_from_iso(context.effective_end_date, "effective_end_date")
    utc_start, utc_end_exclusive = _local_date_bounds_as_utc(start_date, end_date)

    rows: list[AggregateRow] = []
    previous_start: datetime | None = None
    projection_rows: list[dict[str, Any]] = []
    for index, item in enumerate(results):
        row = _require_mapping(item, f"results[{index}]")
        _reject_unknown_or_missing_row_fields(row, payload, index)
        _validate_optional_otc(row, payload)
        timestamp = _require_int(row.get("t"), "results[].t")
        try:
            window_start, window_end = contract_v21.source_window_from_epoch_ms(timestamp)
        except contract_v21.ContractV21ValidationError as exc:
            raise ProviderResponseError("provider timestamp violates v2.1 source-window contract") from exc
        _validate_source_window_in_effective_local_range(
            window_start=window_start,
            window_end=window_end,
            utc_start=utc_start,
            utc_end_exclusive=utc_end_exclusive,
            row_index=index,
        )
        if previous_start is not None and window_start <= previous_start:
            raise ProviderResponseError("provider timestamps must be strictly ascending", failure_category=TIMESTAMP_ORDER)
        previous_start = window_start

        open_value = _require_decimal(row.get("o"), "results[].o")
        high_value = _require_decimal(row.get("h"), "results[].h")
        low_value = _require_decimal(row.get("l"), "results[].l")
        close_value = _require_decimal(row.get("c"), "results[].c")
        volume_value = _require_decimal(row.get("v"), "results[].v")
        if volume_value < 0:
            raise ProviderResponseError("provider volume must be nonnegative")
        if high_value < low_value:
            raise ProviderResponseError("provider high must be greater than or equal to low")
        vwap = _require_decimal(row["vw"], "results[].vw") if "vw" in row else None
        transaction_count = _require_int(row["n"], "results[].n") if "n" in row else None
        if transaction_count is not None and transaction_count < 0:
            raise ProviderResponseError("provider transaction count must be nonnegative")

        row_record = AggregateRow(
            provider_timestamp=timestamp,
            window_start_utc=_iso_utc(window_start),
            window_end_utc=_iso_utc(window_end),
            open=open_value,
            high=high_value,
            low=low_value,
            close=close_value,
            volume=volume_value,
            vwap=vwap,
            transaction_count=transaction_count,
            raw_page_digest=body_sha256,
        )
        rows.append(row_record)
        projection_rows.append(
            {
                "close": _canonical_decimal(close_value),
                "high": _canonical_decimal(high_value),
                "low": _canonical_decimal(low_value),
                "open": _canonical_decimal(open_value),
                "transaction_count": transaction_count if transaction_count is not None else None,
                "transaction_count_status": TRANSACTION_COUNT_PRESENT if transaction_count is not None else TRANSACTION_COUNT_ABSENT,
                "volume": _canonical_decimal(volume_value),
                "vwap": _canonical_decimal(vwap) if vwap is not None else None,
                "vwap_status": VWAP_PRESENT if vwap is not None else VWAP_ABSENT,
                "window_end_utc": row_record.window_end_utc,
                "window_start_utc": row_record.window_start_utc,
            }
        )

    continuation = sanitize_continuation_identity(payload.get("next_url"), context)
    projection = {
        "adjusted": adjusted,
        "continuation_present": continuation is not None,
        "sanitized_continuation_identity": continuation,
        "month_key": context.month_key,
        "projection_version": PROJECTION_VERSION,
        "query_count": query_count,
        "results_count": results_count,
        "rows": projection_rows,
        "status": status,
        "ticker": ticker,
    }
    return ParsedProviderResponse(
        ticker=ticker,
        adjusted=adjusted,
        status=status,
        query_count=query_count,
        results_count=results_count,
        rows=tuple(rows),
        continuation_present=continuation is not None,
        raw_next_url=payload.get("next_url") if continuation is not None else None,
        sanitized_continuation_identity=continuation,
        semantic_projection=projection,
        semantic_projection_digest=semantic_digest(projection),
    )
