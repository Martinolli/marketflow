"""Strict Massive.com aggregate response parsing for fake monthly acquisition."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Any

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.research import acquisition_contract_v2_1 as contract_v21


PROJECTION_VERSION = "OHLCV_PLUS_CONTRACTED_AUDIT_FIELDS_V1"
VWAP_PRESENT = "VWAP_PRESENT"
VWAP_ABSENT = "VWAP_ABSENT"
TRANSACTION_COUNT_PRESENT = "TRANSACTION_COUNT_PRESENT"
TRANSACTION_COUNT_ABSENT = "TRANSACTION_COUNT_ABSENT"
VALID_PROVIDER_STATUSES = frozenset({"OK"})


class ProviderResponseError(ValueError):
    """Raised when a provider response fails strict offline contract parsing."""


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
    if results_count != len(results):
        raise ProviderResponseError("resultsCount must equal parsed result count")
    if results_count <= 0:
        raise ProviderResponseError("provider response must contain at least one aggregate row")
    if query_count < results_count or query_count < 0 or results_count < 0:
        raise ProviderResponseError("provider counts must be nonnegative and coherent")

    start_date = _date_from_iso(context.effective_start_date, "effective_start_date")
    end_date = _date_from_iso(context.effective_end_date, "effective_end_date")
    month_end_exclusive = datetime.combine(end_date + timedelta(days=1), time.min, tzinfo=UTC)

    rows: list[AggregateRow] = []
    previous_start: datetime | None = None
    projection_rows: list[dict[str, Any]] = []
    for index, item in enumerate(results):
        row = _require_mapping(item, f"results[{index}]")
        timestamp = _require_int(row.get("t"), "results[].t")
        try:
            window_start, window_end = contract_v21.source_window_from_epoch_ms(timestamp)
        except contract_v21.ContractV21ValidationError as exc:
            raise ProviderResponseError("provider timestamp violates v2.1 source-window contract") from exc
        if window_start.date() < start_date or window_end > month_end_exclusive:
            raise ProviderResponseError("provider timestamp falls outside effective month")
        if previous_start is not None and window_start <= previous_start:
            raise ProviderResponseError("provider timestamps must be strictly ascending")
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
        sanitized_continuation_identity=continuation,
        semantic_projection=projection,
        semantic_projection_digest=semantic_digest(projection),
    )
