"""Offline declarative historical acquisition contract v2 for MarketFlow."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tomllib
from dataclasses import asdict, dataclass, replace
from datetime import date
from decimal import Decimal, InvalidOperation
from importlib import metadata
from pathlib import Path
from typing import Any


CONTRACT_SCHEMA_VERSION = "marketflow.acquisition_contract.v2"
DECISION_SET_VERSION = "marketflow.acquisition_decisions.v2"
CONTRACT_STATUS_READY = "ACQUISITION_CONTRACT_V2_READY_FOR_IMPLEMENTATION"
HUMAN_DECISIONS_COMPLETE = "COMPLETE"

PROVIDER_CURRENT_BRAND = "MASSIVE.COM"
PROVIDER_FORMER_BRAND = "POLYGON.IO"
PROVIDER_BUSINESS_IDENTITY = "MASSIVE_COM"
LEGACY_POLYGON_ADAPTER_IDENTITY = "polygon-api-client"
LEGACY_POLYGON_PACKAGE_VERSION = "1.14.6"
STOCKS_STARTER = "STOCKS_STARTER"
OPERATOR_ATTESTED = "OPERATOR_ATTESTED"
OPERATOR_ATTESTED_CONFIRMED = "OPERATOR_ATTESTED_CONFIRMED"
FIVE_YEARS = "FIVE_YEARS"
FIFTEEN_MINUTE_DELAYED = "FIFTEEN_MINUTE_DELAYED"
INTRADAY_AND_DAILY_AVAILABLE = "INTRADAY_AND_DAILY_AVAILABLE"
SDK_MIGRATION_NOT_PERFORMED = "NOT_PERFORMED"

PROFILE_SWING = "SWING"
PROFILE_POSITION_SWING = "POSITION_SWING"
TIMEFRAME_SWING = "4h"
TIMEFRAME_POSITION_SWING = "1d"
MINIMUM_ROWS_SWING = 390
MINIMUM_ROWS_POSITION_SWING = 560
SWING_PROFILE_CONTRACT_VERSION = "SWING_RTH_HALF_SESSION_V1"
POSITION_PROFILE_CONTRACT_VERSION = "POSITION_SWING_RTH_FULL_SESSION_V1"
SWING_CANONICAL_BAR_TYPE = "RTH_HALF_SESSION_195M"
POSITION_CANONICAL_BAR_TYPE = "RTH_FULL_SESSION_1D"
BAR_CLOSE_TIMESTAMP = "BAR_CLOSE_TIMESTAMP"
SESSION_CLOSE_TIMESTAMP = "SESSION_CLOSE_TIMESTAMP"
RUNTIME_MIGRATION_PENDING = "LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION"

REGULAR_SESSION = "REGULAR_TRADING_HOURS_ONLY"
FULL_SESSION_ONLY = "FULL_REGULAR_SESSION_ONLY"
EXCLUDE_ENTIRE_SESSION = "EXCLUDE_ENTIRE_SESSION"
INCLUDED = "INCLUDED"
EXCLUDED = "EXCLUDED"
PROHIBITED = "PROHIBITED"
REQUIRED = "REQUIRED"
NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
STRICT_DECIMAL_EQUALITY = "STRICT_CANONICAL_DECIMAL_VALUE_EQUALITY"

RETRYABLE_CATEGORIES = (
    "TRANSPORT_TIMEOUT",
    "CONNECTION_RESET",
    "HTTP_408",
    "HTTP_429",
    "HTTP_500",
    "HTTP_502",
    "HTTP_503",
    "HTTP_504",
)
NON_RETRYABLE_CATEGORIES = (
    "AUTHENTICATION_FAILURE",
    "AUTHORIZATION_FAILURE",
    "INVALID_REQUEST",
    "UNSUPPORTED_TICKER",
    "SCHEMA_FAILURE",
    "SEMANTIC_MISMATCH",
    "ADJUSTMENT_MISMATCH",
    "INVALID_TIMESTAMPS_OR_OHLCV",
    "PROVIDER_RESPONSE_VARIANCE",
)

DEFAULT_CONFIG_REFERENCE = "config/fixed_date_acquisition_contract_v2.toml"
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RELATIVE_DATE_RE = re.compile(r"^\d+(d|w|mo|m|y|h)$", re.IGNORECASE)
CREDENTIAL_FRAGMENTS = ("api_key", "apikey", "secret", "token", "password", "credential", "authorization")
URL_FIELD_FRAGMENTS = ("url", "uri")
PATH_FIELD_NAMES = {"path", "local_path", "absolute_path", "output_path", "directory", "folder"}
ALLOWED_PACKAGE_FIELDS = {
    "calendar_package",
    "calendar_package_version",
    "credential_bearing_continuation_retention",
    "installed_adapter_family",
    "installed_adapter_version",
}


class ContractV2ValidationError(ValueError):
    """Raised when the v2 acquisition contract is malformed or unsafe."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _as_dict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: _as_dict(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_as_dict(item) for item in value]
    if isinstance(value, list):
        return [_as_dict(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _as_dict(item) for key, item in value.items()}
    return value


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize a contract deterministically for semantic digesting."""
    return json.dumps(
        _as_dict(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def contract_digest(value: Any) -> str:
    """Return the deterministic SHA-256 digest for a contract payload."""
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _require_exact(value: Any, expected: Any, field_name: str) -> None:
    if value != expected:
        raise ContractV2ValidationError(f"{field_name} must be {expected!r}")


def _require_bool(value: Any, expected: bool, field_name: str) -> None:
    if type(value) is not bool or value is not expected:
        raise ContractV2ValidationError(f"{field_name} must be {expected!r}")


def _require_int(value: Any, expected: int, field_name: str) -> None:
    if type(value) is not int or value != expected:
        raise ContractV2ValidationError(f"{field_name} must be {expected!r}")


def _require_positive_int(value: Any, field_name: str) -> None:
    if type(value) is not int or value <= 0:
        raise ContractV2ValidationError(f"{field_name} must be a positive integer")


def _require_tuple(value: tuple[Any, ...], expected: tuple[Any, ...], field_name: str) -> None:
    if not isinstance(value, tuple) or value != expected:
        raise ContractV2ValidationError(f"{field_name} must be {expected!r}")


def _require_date_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str):
        raise ContractV2ValidationError(f"{field_name} must be a quoted ISO date string")
    lowered = value.strip().lower()
    if lowered in {"today", "now"} or RELATIVE_DATE_RE.match(lowered):
        raise ContractV2ValidationError(f"{field_name} must not be relative")
    if not ISO_DATE_RE.match(value):
        raise ContractV2ValidationError(f"{field_name} must be YYYY-MM-DD")
    date.fromisoformat(value)


def _reject_operational_field_names(payload: dict[str, Any], prefix: str = "") -> None:
    for key, value in payload.items():
        lowered = str(key).lower()
        dotted = f"{prefix}.{key}" if prefix else str(key)
        if lowered not in ALLOWED_PACKAGE_FIELDS:
            if any(fragment in lowered for fragment in CREDENTIAL_FRAGMENTS):
                raise ContractV2ValidationError(f"credential-like field is prohibited: {dotted}")
            if any(fragment in lowered for fragment in URL_FIELD_FRAGMENTS):
                raise ContractV2ValidationError(f"URL field is prohibited: {dotted}")
            if lowered in PATH_FIELD_NAMES or lowered.endswith("_path"):
                raise ContractV2ValidationError(f"local path field is prohibited: {dotted}")
        if isinstance(value, dict):
            _reject_operational_field_names(value, dotted)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_operational_field_names(item, f"{dotted}[{index}]")


def _validate_contract_reference(path: str | Path) -> Path:
    text = str(path)
    if not text or "://" in text or "\x00" in text or "$" in text or "%" in text:
        raise ContractV2ValidationError("contract path must be a direct repo config TOML reference")
    candidate = Path(path)
    if any(":" in part for part in candidate.parts[1:]):
        raise ContractV2ValidationError("contract path must not contain device or stream syntax")
    root = _repo_root().resolve()
    config_dir = (root / "config").resolve()
    resolved = (candidate if candidate.is_absolute() else root / candidate).resolve(strict=False)
    if resolved.parent != config_dir:
        raise ContractV2ValidationError("contract path must be a direct file under repo config")
    if resolved.name != "fixed_date_acquisition_contract_v2.toml":
        raise ContractV2ValidationError("contract path must be the approved v2 config file")
    if resolved.suffix.lower() != ".toml" or resolved.name in {"", ".", ".."}:
        raise ContractV2ValidationError("contract path must be a TOML file")
    if resolved.exists() and resolved.is_symlink():
        raise ContractV2ValidationError("contract path must not be a symlink")
    return resolved


def _expect_keys(payload: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(payload)
    missing = expected - actual
    unknown = actual - expected
    if missing:
        raise ContractV2ValidationError(f"{context} missing keys: {sorted(missing)}")
    if unknown:
        raise ContractV2ValidationError(f"{context} unknown keys: {sorted(unknown)}")


def _tuple_values(value: Any, field_name: str) -> tuple[Any, ...]:
    if not isinstance(value, (list, tuple)):
        raise ContractV2ValidationError(f"{field_name} must be a list")
    return tuple(value)


def canonical_decimal_text(value: str | int | Decimal) -> str:
    """Return canonical decimal text for semantic equality checks."""
    if isinstance(value, bool) or isinstance(value, float):
        raise ContractV2ValidationError("binary floats and booleans are prohibited for canonical numeric equality")
    try:
        decimal_value = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ContractV2ValidationError("invalid canonical decimal value") from exc
    if decimal_value.is_nan() or decimal_value.is_infinite():
        raise ContractV2ValidationError("NaN and infinity are prohibited")
    if decimal_value == 0:
        return "0"
    normalized = decimal_value.normalize()
    if normalized == normalized.to_integral():
        return format(normalized.quantize(Decimal(1)), "f")
    return format(normalized, "f")


def validate_retry_after_delay(status_code: int, retry_after_seconds: Any | None) -> int | None:
    """Validate the declarative Retry-After acceptance rule."""
    if retry_after_seconds is None:
        return None
    if status_code not in {429, 503}:
        raise ContractV2ValidationError("Retry-After is accepted only for HTTP 429 or 503")
    if type(retry_after_seconds) is not int:
        raise ContractV2ValidationError("Retry-After must be an integer second value")
    if retry_after_seconds < 0 or retry_after_seconds > 60:
        raise ContractV2ValidationError("Retry-After must be between 0 and 60 seconds")
    return retry_after_seconds


def effective_retry_wait_seconds(configured_backoff_seconds: int, status_code: int, retry_after_seconds: Any | None) -> int:
    """Return the accepted effective wait for one retry attempt."""
    if type(configured_backoff_seconds) is not int or configured_backoff_seconds < 0:
        raise ContractV2ValidationError("configured backoff must be a nonnegative integer")
    retry_after = validate_retry_after_delay(status_code, retry_after_seconds)
    return configured_backoff_seconds if retry_after is None else max(configured_backoff_seconds, retry_after)


@dataclass(frozen=True, slots=True)
class TechnicalConstants:
    registry_mutex_wait_seconds: int = 10
    mutex_wait_policy: str = "ONE_BOUNDED_WAIT"
    monotonic_timing_required: bool = True
    no_cli_override: bool = True
    no_environment_override: bool = True
    timeout_status: str = "FAIL_CLOSED"
    provider_maximum_attempts: int = 3
    retry_backoff_seconds: tuple[int, ...] = (2, 5)
    retry_jitter: bool = False
    retryable_categories: tuple[str, ...] = RETRYABLE_CATEGORIES
    non_retryable_categories: tuple[str, ...] = NON_RETRYABLE_CATEGORIES
    retry_after_policy: str = "STRICT_INTEGER_SECONDS_HTTP_429_503_ONLY"
    retry_after_min_seconds: int = 0
    retry_after_max_seconds: int = 60
    retry_after_effective_wait_policy: str = "MAX_CONFIGURED_BACKOFF_AND_RETRY_AFTER"
    retry_after_violation_status: str = "RETRY_AFTER_POLICY_VIOLATION"

    def validate(self) -> None:
        _require_int(self.registry_mutex_wait_seconds, 10, "technical_constants.registry_mutex_wait_seconds")
        _require_exact(self.mutex_wait_policy, "ONE_BOUNDED_WAIT", "technical_constants.mutex_wait_policy")
        _require_bool(self.monotonic_timing_required, True, "technical_constants.monotonic_timing_required")
        _require_bool(self.no_cli_override, True, "technical_constants.no_cli_override")
        _require_bool(self.no_environment_override, True, "technical_constants.no_environment_override")
        _require_exact(self.timeout_status, "FAIL_CLOSED", "technical_constants.timeout_status")
        _require_int(self.provider_maximum_attempts, 3, "technical_constants.provider_maximum_attempts")
        _require_tuple(self.retry_backoff_seconds, (2, 5), "technical_constants.retry_backoff_seconds")
        _require_bool(self.retry_jitter, False, "technical_constants.retry_jitter")
        _require_tuple(
            self.retryable_categories,
            RETRYABLE_CATEGORIES,
            "technical_constants.retryable_categories",
        )
        _require_tuple(
            self.non_retryable_categories,
            NON_RETRYABLE_CATEGORIES,
            "technical_constants.non_retryable_categories",
        )
        _require_exact(
            self.retry_after_policy,
            "STRICT_INTEGER_SECONDS_HTTP_429_503_ONLY",
            "technical_constants.retry_after_policy",
        )
        _require_int(self.retry_after_min_seconds, 0, "technical_constants.retry_after_min_seconds")
        _require_int(self.retry_after_max_seconds, 60, "technical_constants.retry_after_max_seconds")
        _require_exact(
            self.retry_after_effective_wait_policy,
            "MAX_CONFIGURED_BACKOFF_AND_RETRY_AFTER",
            "technical_constants.retry_after_effective_wait_policy",
        )
        _require_exact(
            self.retry_after_violation_status,
            "RETRY_AFTER_POLICY_VIOLATION",
            "technical_constants.retry_after_violation_status",
        )


@dataclass(frozen=True, slots=True)
class ProviderPolicy:
    business_provider: str = PROVIDER_CURRENT_BRAND
    provider_business_identity: str = PROVIDER_BUSINESS_IDENTITY
    former_brand: str = PROVIDER_FORMER_BRAND
    installed_adapter_family: str = LEGACY_POLYGON_ADAPTER_IDENTITY
    installed_adapter_version: str = LEGACY_POLYGON_PACKAGE_VERSION
    subscription_plan: str = STOCKS_STARTER
    entitlement_evidence: str = OPERATOR_ATTESTED
    provider_entitlement_status: str = OPERATOR_ATTESTED_CONFIRMED
    historical_access: str = FIVE_YEARS
    market_data_recency: str = FIFTEEN_MINUTE_DELAYED
    aggregate_access: str = INTRADAY_AND_DAILY_AVAILABLE
    entitlement_api_verified: bool = False
    provider_execution_enabled: bool = False
    sdk_migration_status: str = SDK_MIGRATION_NOT_PERFORMED

    def validate(self) -> None:
        _require_exact(self.business_provider, PROVIDER_CURRENT_BRAND, "provider_policy.business_provider")
        _require_exact(self.provider_business_identity, PROVIDER_BUSINESS_IDENTITY, "provider_policy.provider_business_identity")
        _require_exact(self.former_brand, PROVIDER_FORMER_BRAND, "provider_policy.former_brand")
        _require_exact(self.installed_adapter_family, LEGACY_POLYGON_ADAPTER_IDENTITY, "provider_policy.installed_adapter_family")
        _require_exact(self.installed_adapter_version, LEGACY_POLYGON_PACKAGE_VERSION, "provider_policy.installed_adapter_version")
        _require_exact(self.subscription_plan, STOCKS_STARTER, "provider_policy.subscription_plan")
        _require_exact(self.entitlement_evidence, OPERATOR_ATTESTED, "provider_policy.entitlement_evidence")
        _require_exact(
            self.provider_entitlement_status,
            OPERATOR_ATTESTED_CONFIRMED,
            "provider_policy.provider_entitlement_status",
        )
        _require_exact(self.historical_access, FIVE_YEARS, "provider_policy.historical_access")
        _require_exact(self.market_data_recency, FIFTEEN_MINUTE_DELAYED, "provider_policy.market_data_recency")
        _require_exact(self.aggregate_access, INTRADAY_AND_DAILY_AVAILABLE, "provider_policy.aggregate_access")
        _require_bool(self.entitlement_api_verified, False, "provider_policy.entitlement_api_verified")
        _require_bool(self.provider_execution_enabled, False, "provider_policy.provider_execution_enabled")
        _require_exact(self.sdk_migration_status, SDK_MIGRATION_NOT_PERFORMED, "provider_policy.sdk_migration_status")


@dataclass(frozen=True, slots=True)
class FixedRangePolicy:
    start_date: str = "2022-01-01"
    end_date: str = "2025-12-31"
    range_inclusive: bool = True
    common_range_for_all_profiles: bool = True
    rolling_window_allowed: bool = False
    relative_period_allowed: bool = False
    current_date_dependency_allowed: bool = False
    ticker_specific_extension_allowed: bool = False
    profile_specific_dates_allowed: bool = False
    row_gate_auto_extension_allowed: bool = False
    date_change_requires_new_generation: bool = True

    def validate(self) -> None:
        _require_date_text(self.start_date, "fixed_range_policy.start_date")
        _require_date_text(self.end_date, "fixed_range_policy.end_date")
        if date.fromisoformat(self.start_date) >= date.fromisoformat(self.end_date):
            raise ContractV2ValidationError("fixed_range_policy.start_date must be before end_date")
        for field_name in (
            "range_inclusive",
            "common_range_for_all_profiles",
            "date_change_requires_new_generation",
        ):
            _require_bool(getattr(self, field_name), True, f"fixed_range_policy.{field_name}")
        for field_name in (
            "rolling_window_allowed",
            "relative_period_allowed",
            "current_date_dependency_allowed",
            "ticker_specific_extension_allowed",
            "profile_specific_dates_allowed",
            "row_gate_auto_extension_allowed",
        ):
            _require_bool(getattr(self, field_name), False, f"fixed_range_policy.{field_name}")


@dataclass(frozen=True, slots=True)
class SourceBarPolicy:
    provider_source_interval: str = "15m"
    provider_timespan: str = "minute"
    provider_multiplier: int = 15
    adjusted: bool = True
    sort: str = "asc"
    limit: int = 50000
    source_timezone: str = "America/New_York"
    canonical_storage_timezone: str = "UTC"
    extended_hours_in_derived_datasets: str = EXCLUDED
    provider_native_4h_canonical: bool = False
    provider_native_1d_canonical: bool = False

    def validate(self) -> None:
        _require_exact(self.provider_source_interval, "15m", "source_bar_policy.provider_source_interval")
        _require_exact(self.provider_timespan, "minute", "source_bar_policy.provider_timespan")
        _require_int(self.provider_multiplier, 15, "source_bar_policy.provider_multiplier")
        _require_bool(self.adjusted, True, "source_bar_policy.adjusted")
        _require_exact(self.sort, "asc", "source_bar_policy.sort")
        _require_int(self.limit, 50000, "source_bar_policy.limit")
        _require_exact(self.source_timezone, "America/New_York", "source_bar_policy.source_timezone")
        _require_exact(self.canonical_storage_timezone, "UTC", "source_bar_policy.canonical_storage_timezone")
        _require_exact(
            self.extended_hours_in_derived_datasets,
            EXCLUDED,
            "source_bar_policy.extended_hours_in_derived_datasets",
        )
        _require_bool(self.provider_native_4h_canonical, False, "source_bar_policy.provider_native_4h_canonical")
        _require_bool(self.provider_native_1d_canonical, False, "source_bar_policy.provider_native_1d_canonical")


@dataclass(frozen=True, slots=True)
class BarWindow:
    label: str
    start_inclusive: str
    end_exclusive: str
    source_bars_required: int
    timezone: str = "America/New_York"

    def validate(self) -> None:
        if not all(isinstance(value, str) for value in (self.label, self.start_inclusive, self.end_exclusive, self.timezone)):
            raise ContractV2ValidationError("bar window fields must be strings")
        if not re.match(r"^\d{2}:\d{2}$", self.start_inclusive) or not re.match(r"^\d{2}:\d{2}$", self.end_exclusive):
            raise ContractV2ValidationError("bar window times must be HH:MM")
        _require_positive_int(self.source_bars_required, "bar_window.source_bars_required")
        _require_exact(self.timezone, "America/New_York", "bar_window.timezone")


@dataclass(frozen=True, slots=True)
class ProfileAcquisitionPolicy:
    profile_id: str
    profile_contract_version: str
    canonical_bar_type: str
    minimum_valid_rows: int
    source_interval: str
    source_bars_per_canonical_bar: int
    timestamp_semantic: str
    session_policy: str
    early_close_policy: str
    ex_dividend_cross_boundary_policy: str
    higher_timeframe_context: str
    window_segments: tuple[BarWindow, ...]

    def validate(self) -> None:
        for window in self.window_segments:
            window.validate()
        if self.profile_id == PROFILE_SWING:
            _require_exact(self.profile_contract_version, SWING_PROFILE_CONTRACT_VERSION, "profiles.SWING.profile_contract_version")
            _require_exact(self.canonical_bar_type, SWING_CANONICAL_BAR_TYPE, "profiles.SWING.canonical_bar_type")
            _require_int(self.minimum_valid_rows, MINIMUM_ROWS_SWING, "profiles.SWING.minimum_valid_rows")
            _require_int(self.source_bars_per_canonical_bar, 13, "profiles.SWING.source_bars_per_canonical_bar")
            _require_exact(self.timestamp_semantic, BAR_CLOSE_TIMESTAMP, "profiles.SWING.timestamp_semantic")
            expected = (
                BarWindow("MORNING_4H", "09:30", "12:45", 13),
                BarWindow("AFTERNOON_4H", "12:45", "16:00", 13),
            )
            _require_tuple(self.window_segments, expected, "profiles.SWING.window_segments")
        elif self.profile_id == PROFILE_POSITION_SWING:
            _require_exact(
                self.profile_contract_version,
                POSITION_PROFILE_CONTRACT_VERSION,
                "profiles.POSITION_SWING.profile_contract_version",
            )
            _require_exact(
                self.canonical_bar_type,
                POSITION_CANONICAL_BAR_TYPE,
                "profiles.POSITION_SWING.canonical_bar_type",
            )
            _require_int(
                self.minimum_valid_rows,
                MINIMUM_ROWS_POSITION_SWING,
                "profiles.POSITION_SWING.minimum_valid_rows",
            )
            _require_int(
                self.source_bars_per_canonical_bar,
                26,
                "profiles.POSITION_SWING.source_bars_per_canonical_bar",
            )
            _require_exact(
                self.timestamp_semantic,
                SESSION_CLOSE_TIMESTAMP,
                "profiles.POSITION_SWING.timestamp_semantic",
            )
            expected = (BarWindow("FULL_RTH_DAY", "09:30", "16:00", 26),)
            _require_tuple(self.window_segments, expected, "profiles.POSITION_SWING.window_segments")
        else:
            raise ContractV2ValidationError(f"unsupported profile_id: {self.profile_id}")
        _require_exact(self.source_interval, "15m", f"profiles.{self.profile_id}.source_interval")
        _require_exact(self.session_policy, REGULAR_SESSION, f"profiles.{self.profile_id}.session_policy")
        _require_exact(self.early_close_policy, EXCLUDE_ENTIRE_SESSION, f"profiles.{self.profile_id}.early_close_policy")
        _require_exact(
            self.ex_dividend_cross_boundary_policy,
            PROHIBITED,
            f"profiles.{self.profile_id}.ex_dividend_cross_boundary_policy",
        )
        _require_exact(self.higher_timeframe_context, NOT_IMPLEMENTED, f"profiles.{self.profile_id}.higher_timeframe_context")


@dataclass(frozen=True, slots=True)
class AggregationPolicy:
    open_rule: str = "FIRST_SOURCE_OPEN"
    high_rule: str = "MAX_SOURCE_HIGH"
    low_rule: str = "MIN_SOURCE_LOW"
    close_rule: str = "LAST_SOURCE_CLOSE"
    volume_rule: str = "SUM_SOURCE_VOLUME"
    expected_source_slots_required: bool = True
    missing_source_slot_repair: str = PROHIBITED
    partial_bar_acceptance: bool = False
    synthetic_bar_creation: str = PROHIBITED
    provider_native_higher_timeframe_acceptance: str = PROHIBITED

    def validate(self) -> None:
        expected = {
            "open_rule": "FIRST_SOURCE_OPEN",
            "high_rule": "MAX_SOURCE_HIGH",
            "low_rule": "MIN_SOURCE_LOW",
            "close_rule": "LAST_SOURCE_CLOSE",
            "volume_rule": "SUM_SOURCE_VOLUME",
            "missing_source_slot_repair": PROHIBITED,
            "synthetic_bar_creation": PROHIBITED,
            "provider_native_higher_timeframe_acceptance": PROHIBITED,
        }
        for field_name, value in expected.items():
            _require_exact(getattr(self, field_name), value, f"aggregation_policy.{field_name}")
        _require_bool(self.expected_source_slots_required, True, "aggregation_policy.expected_source_slots_required")
        _require_bool(self.partial_bar_acceptance, False, "aggregation_policy.partial_bar_acceptance")


@dataclass(frozen=True, slots=True)
class CalendarPolicy:
    calendar_architecture: str = "EXCHANGE_AWARE_FROZEN_CALENDAR_ARTIFACT"
    calendar_package: str = "exchange_calendars"
    calendar_package_version: str = "4.13.2"
    calendar_name: str = "XNYS"
    timezone: str = "America/New_York"
    requested_listing_mic_retention: str = "RETAIN_SEPARATELY_FROM_RESOLVED_CALENDAR"
    timezone_aware_utc_schedule_evidence: str = REQUIRED
    full_regular_sessions_only: str = INCLUDED
    early_close_sessions: str = EXCLUDED
    ad_hoc_closures: str = INCLUDED
    closure_inference_from_missing_provider_bars: str = PROHIBITED
    dynamic_unfrozen_calendar_use: str = PROHIBITED
    calendar_artifact_not_package_version: bool = True
    future_artifact_evidence: tuple[str, ...] = (
        "calendar_package",
        "calendar_package_version",
        "tzdata_version",
        "calendar_implementation_digest",
        "official_exchange_evidence_digest",
        "schedule_digest",
    )
    required_artifact_fields: tuple[str, ...] = (
        "calendar_artifact_id",
        "calendar_package",
        "calendar_package_version",
        "calendar_name",
        "session_date",
        "market_open",
        "market_close",
        "session_classification",
        "artifact_digest",
    )

    def validate(self) -> None:
        _require_exact(self.calendar_architecture, "EXCHANGE_AWARE_FROZEN_CALENDAR_ARTIFACT", "calendar_policy.calendar_architecture")
        _require_exact(self.calendar_package, "exchange_calendars", "calendar_policy.calendar_package")
        _require_exact(self.calendar_package_version, "4.13.2", "calendar_policy.calendar_package_version")
        _require_exact(self.calendar_name, "XNYS", "calendar_policy.calendar_name")
        _require_exact(self.timezone, "America/New_York", "calendar_policy.timezone")
        _require_exact(
            self.requested_listing_mic_retention,
            "RETAIN_SEPARATELY_FROM_RESOLVED_CALENDAR",
            "calendar_policy.requested_listing_mic_retention",
        )
        _require_exact(
            self.timezone_aware_utc_schedule_evidence,
            REQUIRED,
            "calendar_policy.timezone_aware_utc_schedule_evidence",
        )
        _require_exact(self.full_regular_sessions_only, INCLUDED, "calendar_policy.full_regular_sessions_only")
        _require_exact(self.early_close_sessions, EXCLUDED, "calendar_policy.early_close_sessions")
        _require_exact(self.ad_hoc_closures, INCLUDED, "calendar_policy.ad_hoc_closures")
        _require_exact(
            self.closure_inference_from_missing_provider_bars,
            PROHIBITED,
            "calendar_policy.closure_inference_from_missing_provider_bars",
        )
        _require_exact(
            self.dynamic_unfrozen_calendar_use,
            PROHIBITED,
            "calendar_policy.dynamic_unfrozen_calendar_use",
        )
        _require_bool(self.calendar_artifact_not_package_version, True, "calendar_policy.calendar_artifact_not_package_version")
        _require_tuple(
            self.future_artifact_evidence,
            (
                "calendar_package",
                "calendar_package_version",
                "tzdata_version",
                "calendar_implementation_digest",
                "official_exchange_evidence_digest",
                "schedule_digest",
            ),
            "calendar_policy.future_artifact_evidence",
        )
        _require_tuple(
            self.required_artifact_fields,
            (
                "calendar_artifact_id",
                "calendar_package",
                "calendar_package_version",
                "calendar_name",
                "session_date",
                "market_open",
                "market_close",
                "session_classification",
                "artifact_digest",
            ),
            "calendar_policy.required_artifact_fields",
        )


@dataclass(frozen=True, slots=True)
class InstrumentIdentityPolicy:
    identity_source: str = "MASSIVE_POINT_IN_TIME_TICKER_OVERVIEW"
    endpoint_family: str = "TICKER_OVERVIEW_V3"
    identity_continuity: str = "BOUNDARY_SNAPSHOTS_PLUS_STABLE_IDENTIFIER_EVENT_AUDIT"
    start_identity_snapshot_required: bool = True
    end_identity_snapshot_required: bool = True
    identity_change_segment_policy: str = "IMMUTABLE_IDENTITY_SEGMENTS"
    required_evidence: tuple[str, ...] = (
        "requested_ticker",
        "primary_exchange_mic",
        "composite_figi",
        "share_class_figi",
        "cik",
        "ticker_active_status",
        "name",
        "market",
        "locale",
        "primary_exchange",
        "query_date",
        "raw_identity_response_digest",
    )
    ticker_event_evidence_role: str = "SUPPORTING_EVIDENCE_NOT_SOLE_AUTHORITY"
    automatic_stitching: str = PROHIBITED
    ambiguous_identity_status: str = "IDENTITY_AMBIGUOUS_FAIL_CLOSED"

    def validate(self) -> None:
        _require_exact(self.identity_source, "MASSIVE_POINT_IN_TIME_TICKER_OVERVIEW", "instrument_identity_policy.identity_source")
        _require_exact(self.endpoint_family, "TICKER_OVERVIEW_V3", "instrument_identity_policy.endpoint_family")
        _require_exact(
            self.identity_continuity,
            "BOUNDARY_SNAPSHOTS_PLUS_STABLE_IDENTIFIER_EVENT_AUDIT",
            "instrument_identity_policy.identity_continuity",
        )
        _require_bool(self.start_identity_snapshot_required, True, "instrument_identity_policy.start_identity_snapshot_required")
        _require_bool(self.end_identity_snapshot_required, True, "instrument_identity_policy.end_identity_snapshot_required")
        _require_exact(
            self.identity_change_segment_policy,
            "IMMUTABLE_IDENTITY_SEGMENTS",
            "instrument_identity_policy.identity_change_segment_policy",
        )
        _require_tuple(
            self.required_evidence,
            (
                "requested_ticker",
                "primary_exchange_mic",
                "composite_figi",
                "share_class_figi",
                "cik",
                "ticker_active_status",
                "name",
                "market",
                "locale",
                "primary_exchange",
                "query_date",
                "raw_identity_response_digest",
            ),
            "instrument_identity_policy.required_evidence",
        )
        _require_exact(
            self.ticker_event_evidence_role,
            "SUPPORTING_EVIDENCE_NOT_SOLE_AUTHORITY",
            "instrument_identity_policy.ticker_event_evidence_role",
        )
        _require_exact(self.automatic_stitching, PROHIBITED, "instrument_identity_policy.automatic_stitching")
        _require_exact(
            self.ambiguous_identity_status,
            "IDENTITY_AMBIGUOUS_FAIL_CLOSED",
            "instrument_identity_policy.ambiguous_identity_status",
        )


@dataclass(frozen=True, slots=True)
class CorporateActionPolicy:
    split_provider_bars: str = "SPLIT_ADJUSTED"
    adjusted_request: bool = True
    adjusted_response: str = "MUST_MATCH_TRUE"
    independent_split_event_audit: str = REQUIRED
    local_second_split_adjustment: str = PROHIBITED
    dividend_price_adjustment: str = PROHIBITED
    dividend_event_audit: str = REQUIRED
    ex_dividend_policy: str = "RESET_ANALYTICAL_CONTINUITY_AT_EX_DIVIDEND_DATE"
    cross_boundary_true_range: str = PROHIBITED
    cross_boundary_wyckoff_structure: str = PROHIBITED
    post_boundary_readiness: str = "COMPONENT_BASED_READINESS"
    fixed_global_warmup_allowed: bool = False
    manual_operator_unlock_allowed: bool = False
    excluded_early_close_ex_dividend_segment_start: str = "NEXT_ELIGIBLE_FULL_SESSION_CANONICAL_BAR"

    def validate(self) -> None:
        expected = {
            "split_provider_bars": "SPLIT_ADJUSTED",
            "adjusted_response": "MUST_MATCH_TRUE",
            "independent_split_event_audit": REQUIRED,
            "local_second_split_adjustment": PROHIBITED,
            "dividend_price_adjustment": PROHIBITED,
            "dividend_event_audit": REQUIRED,
            "ex_dividend_policy": "RESET_ANALYTICAL_CONTINUITY_AT_EX_DIVIDEND_DATE",
            "cross_boundary_true_range": PROHIBITED,
            "cross_boundary_wyckoff_structure": PROHIBITED,
            "post_boundary_readiness": "COMPONENT_BASED_READINESS",
            "excluded_early_close_ex_dividend_segment_start": "NEXT_ELIGIBLE_FULL_SESSION_CANONICAL_BAR",
        }
        for field_name, value in expected.items():
            _require_exact(getattr(self, field_name), value, f"corporate_action_policy.{field_name}")
        _require_bool(self.adjusted_request, True, "corporate_action_policy.adjusted_request")
        _require_bool(self.fixed_global_warmup_allowed, False, "corporate_action_policy.fixed_global_warmup_allowed")
        _require_bool(self.manual_operator_unlock_allowed, False, "corporate_action_policy.manual_operator_unlock_allowed")


@dataclass(frozen=True, slots=True)
class ChunkingPolicy:
    partition: str = "FIXED_CALENDAR_MONTH"
    baseline_month_count: int = 48
    chunk_count_before_identity_clipping: int = 48
    identity_clipping_order: str = "AFTER_FIXED_MONTH_CHUNKING"
    segment_clipped_first_last_months_permitted: bool = True
    mandatory_pagination_exhaustion: bool = True
    no_partial_month_success: bool = True
    continuation_repetition_policy: str = "REJECT_DUPLICATE_PAGE_OR_REPEATED_CONTINUATION"
    first_page_only_acceptance: str = PROHIBITED
    one_raw_page_record_per_provider_page: bool = True
    exact_provider_bytes_required: bool = True
    month_completeness_manifest: str = REQUIRED
    reformatted_json_as_raw: str = PROHIBITED
    credential_bearing_continuation_retention: str = PROHIBITED
    every_attempt_preserved: bool = True
    failed_attempts_retained: bool = True
    accepted_attempt_policy: str = "ONE_EXPLICITLY_ACCEPTED_ATTEMPT_PER_LOGICAL_PAGE"
    multiple_valid_attempts_allowed: bool = True
    equivalent_retry_selection: str = "LOWEST_VALID_ATTEMPT_ORDINAL"
    differing_projection_status: str = "PROVIDER_RESPONSE_VARIANCE"
    latest_response_preference: str = PROHIBITED
    overlap_policy: str = "DETECT_AND_REJECT_EXCEPT_IDENTICAL_RETRY_ATTEMPTS"
    completeness_acceptance: str = "ALL_EXPECTED_SOURCE_SLOTS_PRESENT_AFTER_CALENDAR_JOIN"

    def validate(self) -> None:
        _require_exact(self.partition, "FIXED_CALENDAR_MONTH", "chunking_policy.partition")
        _require_int(self.baseline_month_count, 48, "chunking_policy.baseline_month_count")
        _require_int(self.chunk_count_before_identity_clipping, 48, "chunking_policy.chunk_count_before_identity_clipping")
        _require_exact(self.identity_clipping_order, "AFTER_FIXED_MONTH_CHUNKING", "chunking_policy.identity_clipping_order")
        for field_name in (
            "segment_clipped_first_last_months_permitted",
            "mandatory_pagination_exhaustion",
            "no_partial_month_success",
            "one_raw_page_record_per_provider_page",
            "exact_provider_bytes_required",
            "every_attempt_preserved",
            "failed_attempts_retained",
            "multiple_valid_attempts_allowed",
        ):
            _require_bool(getattr(self, field_name), True, f"chunking_policy.{field_name}")
        _require_exact(
            self.continuation_repetition_policy,
            "REJECT_DUPLICATE_PAGE_OR_REPEATED_CONTINUATION",
            "chunking_policy.continuation_repetition_policy",
        )
        _require_exact(self.first_page_only_acceptance, PROHIBITED, "chunking_policy.first_page_only_acceptance")
        _require_exact(self.month_completeness_manifest, REQUIRED, "chunking_policy.month_completeness_manifest")
        _require_exact(self.reformatted_json_as_raw, PROHIBITED, "chunking_policy.reformatted_json_as_raw")
        _require_exact(
            self.credential_bearing_continuation_retention,
            PROHIBITED,
            "chunking_policy.credential_bearing_continuation_retention",
        )
        _require_exact(
            self.accepted_attempt_policy,
            "ONE_EXPLICITLY_ACCEPTED_ATTEMPT_PER_LOGICAL_PAGE",
            "chunking_policy.accepted_attempt_policy",
        )
        _require_exact(
            self.equivalent_retry_selection,
            "LOWEST_VALID_ATTEMPT_ORDINAL",
            "chunking_policy.equivalent_retry_selection",
        )
        _require_exact(self.differing_projection_status, "PROVIDER_RESPONSE_VARIANCE", "chunking_policy.differing_projection_status")
        _require_exact(self.latest_response_preference, PROHIBITED, "chunking_policy.latest_response_preference")
        _require_exact(
            self.overlap_policy,
            "DETECT_AND_REJECT_EXCEPT_IDENTICAL_RETRY_ATTEMPTS",
            "chunking_policy.overlap_policy",
        )
        _require_exact(
            self.completeness_acceptance,
            "ALL_EXPECTED_SOURCE_SLOTS_PRESENT_AFTER_CALENDAR_JOIN",
            "chunking_policy.completeness_acceptance",
        )


@dataclass(frozen=True, slots=True)
class SemanticEquivalencePolicy:
    semantic_retry_projection: str = "OHLCV_PLUS_CONTRACTED_AUDIT_FIELDS_V1"
    numeric_equivalence: str = STRICT_DECIMAL_EQUALITY
    provider_json_numbers: str = "PARSE_WITHOUT_BINARY_FLOAT"
    canonical_numeric_type: str = "Decimal"
    tolerance_allowed: bool = False
    negative_zero_canonicalized: bool = True
    nan_infinity: str = "REJECTED"
    required_row_fields: tuple[str, ...] = ("timestamp_utc", "open", "high", "low", "close", "volume")
    exact_integer_fields: tuple[str, ...] = ("volume", "transaction_count")
    optional_presence_sensitive_fields: tuple[str, ...] = ("vwap", "transaction_count")
    missing_supplemental_value_policy: str = "NEVER_FABRICATE_ZERO_FILL_OR_FORWARD_FILL"
    optional_audit_fields: tuple[str, ...] = ("vwap", "transaction_count")
    presence_sensitive: bool = True
    excluded_from_equivalence: tuple[str, ...] = (
        "retrieved_at",
        "attempt_started_at",
        "attempt_finished_at",
        "operator",
    )

    def validate(self) -> None:
        _require_exact(
            self.semantic_retry_projection,
            "OHLCV_PLUS_CONTRACTED_AUDIT_FIELDS_V1",
            "semantic_equivalence_policy.semantic_retry_projection",
        )
        _require_exact(self.numeric_equivalence, STRICT_DECIMAL_EQUALITY, "semantic_equivalence_policy.numeric_equivalence")
        _require_exact(self.provider_json_numbers, "PARSE_WITHOUT_BINARY_FLOAT", "semantic_equivalence_policy.provider_json_numbers")
        _require_exact(self.canonical_numeric_type, "Decimal", "semantic_equivalence_policy.canonical_numeric_type")
        _require_bool(self.tolerance_allowed, False, "semantic_equivalence_policy.tolerance_allowed")
        _require_bool(self.negative_zero_canonicalized, True, "semantic_equivalence_policy.negative_zero_canonicalized")
        _require_exact(self.nan_infinity, "REJECTED", "semantic_equivalence_policy.nan_infinity")
        _require_tuple(
            self.required_row_fields,
            ("timestamp_utc", "open", "high", "low", "close", "volume"),
            "semantic_equivalence_policy.required_row_fields",
        )
        _require_tuple(
            self.exact_integer_fields,
            ("volume", "transaction_count"),
            "semantic_equivalence_policy.exact_integer_fields",
        )
        _require_tuple(
            self.optional_presence_sensitive_fields,
            ("vwap", "transaction_count"),
            "semantic_equivalence_policy.optional_presence_sensitive_fields",
        )
        _require_exact(
            self.missing_supplemental_value_policy,
            "NEVER_FABRICATE_ZERO_FILL_OR_FORWARD_FILL",
            "semantic_equivalence_policy.missing_supplemental_value_policy",
        )
        _require_tuple(
            self.optional_audit_fields,
            ("vwap", "transaction_count"),
            "semantic_equivalence_policy.optional_audit_fields",
        )
        _require_bool(self.presence_sensitive, True, "semantic_equivalence_policy.presence_sensitive")
        _require_tuple(
            self.excluded_from_equivalence,
            ("retrieved_at", "attempt_started_at", "attempt_finished_at", "operator"),
            "semantic_equivalence_policy.excluded_from_equivalence",
        )


@dataclass(frozen=True, slots=True)
class NormalizationPolicy:
    monthly_normalized_ohlcv_artifact: str = "MONTHLY_NORMALIZED_OHLCV"
    monthly_normalized_audit_artifact: str = "MONTHLY_NORMALIZED_AGGREGATE_AUDIT_FIELDS"
    core_artifact_columns: tuple[str, ...] = ("timestamp_utc", "open", "high", "low", "close", "volume")
    audit_artifact_columns: tuple[str, ...] = (
        "provider_timestamp",
        "provider_adjusted",
        "calendar_session_id",
        "bar_window_label",
        "raw_page_digest",
        "corporate_action_boundary_id",
    )
    same_timestamps_order_and_count_required: bool = True
    missing_audit_values_status_null: bool = True
    supplemental_fields_prohibited_from_strategy_input: bool = True
    monthly_normalization_first: bool = True
    identity_segment_consolidation: str = "EXPLICIT_ORDERED_IDENTITY_SEGMENT_CONSOLIDATION"
    mixed_adjustment_evidence_generations: str = PROHIBITED
    coherent_generation_per_identity_segment: bool = True
    segment_artifacts: tuple[str, ...] = ("RAW_PROVIDER_PAGE", "SOURCE_15M_DATASET", "CANONICAL_PROFILE_DATASET")
    dynamic_strategy_month_scan: str = PROHIBITED

    def validate(self) -> None:
        _require_exact(self.monthly_normalized_ohlcv_artifact, "MONTHLY_NORMALIZED_OHLCV", "normalization_policy.monthly_normalized_ohlcv_artifact")
        _require_exact(
            self.monthly_normalized_audit_artifact,
            "MONTHLY_NORMALIZED_AGGREGATE_AUDIT_FIELDS",
            "normalization_policy.monthly_normalized_audit_artifact",
        )
        _require_tuple(self.core_artifact_columns, ("timestamp_utc", "open", "high", "low", "close", "volume"), "normalization_policy.core_artifact_columns")
        _require_tuple(
            self.audit_artifact_columns,
            (
                "provider_timestamp",
                "provider_adjusted",
                "calendar_session_id",
                "bar_window_label",
                "raw_page_digest",
                "corporate_action_boundary_id",
            ),
            "normalization_policy.audit_artifact_columns",
        )
        _require_bool(
            self.same_timestamps_order_and_count_required,
            True,
            "normalization_policy.same_timestamps_order_and_count_required",
        )
        _require_bool(self.missing_audit_values_status_null, True, "normalization_policy.missing_audit_values_status_null")
        _require_bool(
            self.supplemental_fields_prohibited_from_strategy_input,
            True,
            "normalization_policy.supplemental_fields_prohibited_from_strategy_input",
        )
        _require_bool(self.monthly_normalization_first, True, "normalization_policy.monthly_normalization_first")
        _require_exact(
            self.identity_segment_consolidation,
            "EXPLICIT_ORDERED_IDENTITY_SEGMENT_CONSOLIDATION",
            "normalization_policy.identity_segment_consolidation",
        )
        _require_exact(
            self.mixed_adjustment_evidence_generations,
            PROHIBITED,
            "normalization_policy.mixed_adjustment_evidence_generations",
        )
        _require_bool(
            self.coherent_generation_per_identity_segment,
            True,
            "normalization_policy.coherent_generation_per_identity_segment",
        )
        _require_tuple(
            self.segment_artifacts,
            ("RAW_PROVIDER_PAGE", "SOURCE_15M_DATASET", "CANONICAL_PROFILE_DATASET"),
            "normalization_policy.segment_artifacts",
        )
        _require_exact(self.dynamic_strategy_month_scan, PROHIBITED, "normalization_policy.dynamic_strategy_month_scan")


@dataclass(frozen=True, slots=True)
class GenerationPolicy:
    generation_scope: str = "ONE_COHERENT_GENERATION"
    generation_statuses: tuple[str, ...] = ("OPEN", "INCOMPLETE", "BLOCKED", "READY_FOR_FREEZE", "PREPARED", "FROZEN")
    lifecycle: tuple[str, ...] = (
        "CREATE_GENERATION",
        "ACQUIRE_RAW",
        "NORMALIZE_SOURCE_15M",
        "BUILD_CANONICAL_PROFILE_DATASETS",
        "VALIDATE_COMPLETENESS",
        "WRITE_RECEIPT",
        "AWAIT_HUMAN_FREEZE",
    )
    digest_bound_human_freeze_required: bool = True
    two_phase_freeze_required: bool = True
    explicit_recovery_required: bool = True
    provisional_strategy_use: str = PROHIBITED
    automatic_freeze_allowed: bool = False
    automatic_canonical_approval_allowed: bool = False
    generation_replacement_policy: str = "MAKE_BEFORE_BREAK"

    def validate(self) -> None:
        _require_exact(self.generation_scope, "ONE_COHERENT_GENERATION", "generation_policy.generation_scope")
        _require_tuple(
            self.generation_statuses,
            ("OPEN", "INCOMPLETE", "BLOCKED", "READY_FOR_FREEZE", "PREPARED", "FROZEN"),
            "generation_policy.generation_statuses",
        )
        _require_tuple(
            self.lifecycle,
            (
                "CREATE_GENERATION",
                "ACQUIRE_RAW",
                "NORMALIZE_SOURCE_15M",
                "BUILD_CANONICAL_PROFILE_DATASETS",
                "VALIDATE_COMPLETENESS",
                "WRITE_RECEIPT",
                "AWAIT_HUMAN_FREEZE",
            ),
            "generation_policy.lifecycle",
        )
        _require_bool(self.digest_bound_human_freeze_required, True, "generation_policy.digest_bound_human_freeze_required")
        _require_bool(self.two_phase_freeze_required, True, "generation_policy.two_phase_freeze_required")
        _require_bool(self.explicit_recovery_required, True, "generation_policy.explicit_recovery_required")
        _require_exact(self.provisional_strategy_use, PROHIBITED, "generation_policy.provisional_strategy_use")
        _require_bool(self.automatic_freeze_allowed, False, "generation_policy.automatic_freeze_allowed")
        _require_bool(
            self.automatic_canonical_approval_allowed,
            False,
            "generation_policy.automatic_canonical_approval_allowed",
        )
        _require_exact(self.generation_replacement_policy, "MAKE_BEFORE_BREAK", "generation_policy.generation_replacement_policy")


@dataclass(frozen=True, slots=True)
class RegistryPolicy:
    approval_granularity: str = "PROFILE_IDENTITY_SEGMENT_GENERATION"
    registry_key_fields: tuple[str, ...] = (
        "canonical_ticker",
        "profile_id",
        "generation_id",
        "contract_digest",
        "dataset_digest",
    )
    human_approval_required_for_active_use: bool = True
    digest_bound_approval_required: bool = True
    two_phase_approval_required: bool = True
    maximum_active_approval_per_key: int = 1
    newest_generation_promotion: str = PROHIBITED
    manual_file_edit_as_approval: str = PROHIBITED
    ambiguous_duplicate_status: str = "REGISTRY_IDENTITY_AMBIGUOUS_FAIL_CLOSED"
    supersession_policy: str = "MAKE_BEFORE_BREAK"
    partial_generation_registration_allowed: bool = False

    def validate(self) -> None:
        _require_exact(self.approval_granularity, "PROFILE_IDENTITY_SEGMENT_GENERATION", "registry_policy.approval_granularity")
        _require_tuple(
            self.registry_key_fields,
            ("canonical_ticker", "profile_id", "generation_id", "contract_digest", "dataset_digest"),
            "registry_policy.registry_key_fields",
        )
        _require_bool(self.human_approval_required_for_active_use, True, "registry_policy.human_approval_required_for_active_use")
        _require_bool(self.digest_bound_approval_required, True, "registry_policy.digest_bound_approval_required")
        _require_bool(self.two_phase_approval_required, True, "registry_policy.two_phase_approval_required")
        _require_int(self.maximum_active_approval_per_key, 1, "registry_policy.maximum_active_approval_per_key")
        _require_exact(self.newest_generation_promotion, PROHIBITED, "registry_policy.newest_generation_promotion")
        _require_exact(self.manual_file_edit_as_approval, PROHIBITED, "registry_policy.manual_file_edit_as_approval")
        _require_exact(
            self.ambiguous_duplicate_status,
            "REGISTRY_IDENTITY_AMBIGUOUS_FAIL_CLOSED",
            "registry_policy.ambiguous_duplicate_status",
        )
        _require_exact(self.supersession_policy, "MAKE_BEFORE_BREAK", "registry_policy.supersession_policy")
        _require_bool(
            self.partial_generation_registration_allowed,
            False,
            "registry_policy.partial_generation_registration_allowed",
        )


@dataclass(frozen=True, slots=True)
class QuarantinePolicy:
    quarantine_status: str = "QUARANTINED_UNTIL_EXPLICIT_HUMAN_APPROVAL"
    immediate_fail_closed_per_key: bool = True
    persistent_pre_gate_latches: tuple[str, ...] = ("PENDING", "ACTIVE")
    immutable_evidence_required: bool = True
    abort_unfinished_runs: bool = True
    validation_epochs_required: bool = True
    per_key_named_mutex_required: bool = True
    clearance_suspension_reviewed: bool = True
    reinstatement_policy: str = "NEW_APPROVAL_RECORD_ONLY"
    old_run_revival: str = PROHIBITED
    blocks_candidate_generation: bool = True
    blocks_monte_carlo: bool = True
    blocks_performance_reporting: bool = True
    quarantine_reasons_required: bool = True

    def validate(self) -> None:
        _require_exact(self.quarantine_status, "QUARANTINED_UNTIL_EXPLICIT_HUMAN_APPROVAL", "quarantine_policy.quarantine_status")
        _require_bool(self.immediate_fail_closed_per_key, True, "quarantine_policy.immediate_fail_closed_per_key")
        _require_tuple(self.persistent_pre_gate_latches, ("PENDING", "ACTIVE"), "quarantine_policy.persistent_pre_gate_latches")
        _require_bool(self.immutable_evidence_required, True, "quarantine_policy.immutable_evidence_required")
        _require_bool(self.abort_unfinished_runs, True, "quarantine_policy.abort_unfinished_runs")
        _require_bool(self.validation_epochs_required, True, "quarantine_policy.validation_epochs_required")
        _require_bool(self.per_key_named_mutex_required, True, "quarantine_policy.per_key_named_mutex_required")
        _require_bool(self.clearance_suspension_reviewed, True, "quarantine_policy.clearance_suspension_reviewed")
        _require_exact(self.reinstatement_policy, "NEW_APPROVAL_RECORD_ONLY", "quarantine_policy.reinstatement_policy")
        _require_exact(self.old_run_revival, PROHIBITED, "quarantine_policy.old_run_revival")
        _require_bool(self.blocks_candidate_generation, True, "quarantine_policy.blocks_candidate_generation")
        _require_bool(self.blocks_monte_carlo, True, "quarantine_policy.blocks_monte_carlo")
        _require_bool(self.blocks_performance_reporting, True, "quarantine_policy.blocks_performance_reporting")
        _require_bool(self.quarantine_reasons_required, True, "quarantine_policy.quarantine_reasons_required")


@dataclass(frozen=True, slots=True)
class AuthorityStoragePolicy:
    registry_mutex_wait_seconds: int = 10
    immutable_event_file_per_event: bool = True
    immutable_head_snapshot_per_generation: bool = True
    atomic_current_head_ref: bool = True
    journal_head_pointer_ordering: str = "JOURNAL_THEN_HEAD_THEN_POINTER"
    explicit_head_pointer_recovery: bool = True
    external_two_phase_recovery_records: bool = True
    recovery_sentinels_required: bool = True
    startup_auto_repair: str = PROHIBITED
    authority_event_storage_model: str = "ONE_EVENT_RECORD_PER_AUTHORITY_CHANGE"
    append_only_authority_journal: str = REQUIRED
    digest_chained_head_record: str = REQUIRED
    pointer_update_policy: str = "ATOMIC_REPLACE_AFTER_JOURNAL_APPEND"
    recovery_policy: str = "RECONCILE_POINTER_WITH_DIGEST_CHAIN"
    handle_inheritance_allowed: bool = False
    current_user_acl_only: bool = True

    def validate(self) -> None:
        _require_int(self.registry_mutex_wait_seconds, 10, "authority_storage_policy.registry_mutex_wait_seconds")
        _require_bool(self.immutable_event_file_per_event, True, "authority_storage_policy.immutable_event_file_per_event")
        _require_bool(
            self.immutable_head_snapshot_per_generation,
            True,
            "authority_storage_policy.immutable_head_snapshot_per_generation",
        )
        _require_bool(self.atomic_current_head_ref, True, "authority_storage_policy.atomic_current_head_ref")
        _require_exact(
            self.journal_head_pointer_ordering,
            "JOURNAL_THEN_HEAD_THEN_POINTER",
            "authority_storage_policy.journal_head_pointer_ordering",
        )
        _require_bool(self.explicit_head_pointer_recovery, True, "authority_storage_policy.explicit_head_pointer_recovery")
        _require_bool(
            self.external_two_phase_recovery_records,
            True,
            "authority_storage_policy.external_two_phase_recovery_records",
        )
        _require_bool(self.recovery_sentinels_required, True, "authority_storage_policy.recovery_sentinels_required")
        _require_exact(self.startup_auto_repair, PROHIBITED, "authority_storage_policy.startup_auto_repair")
        _require_exact(
            self.authority_event_storage_model,
            "ONE_EVENT_RECORD_PER_AUTHORITY_CHANGE",
            "authority_storage_policy.authority_event_storage_model",
        )
        _require_exact(self.append_only_authority_journal, REQUIRED, "authority_storage_policy.append_only_authority_journal")
        _require_exact(self.digest_chained_head_record, REQUIRED, "authority_storage_policy.digest_chained_head_record")
        _require_exact(
            self.pointer_update_policy,
            "ATOMIC_REPLACE_AFTER_JOURNAL_APPEND",
            "authority_storage_policy.pointer_update_policy",
        )
        _require_exact(self.recovery_policy, "RECONCILE_POINTER_WITH_DIGEST_CHAIN", "authority_storage_policy.recovery_policy")
        _require_bool(self.handle_inheritance_allowed, False, "authority_storage_policy.handle_inheritance_allowed")
        _require_bool(self.current_user_acl_only, True, "authority_storage_policy.current_user_acl_only")


@dataclass(frozen=True, slots=True)
class AuthorityAuditPolicy:
    requested_key_validation: str = "FULL_KEY_VALIDATION_BEFORE_DECISION"
    explicit_full_audit_command_required: bool = True
    one_key_mutex_at_a_time: bool = True
    immutable_audit_evidence_required: bool = True
    authority_changing_effect: str = PROHIBITED
    deterministic_ordering: bool = True
    single_mutex_for_batch: bool = True
    non_atomic_multi_key_classification: str = "BATCH_NOT_ATOMIC"
    start_end_reconciliation_required: bool = True
    authority_change_reason_required: bool = True

    def validate(self) -> None:
        _require_exact(
            self.requested_key_validation,
            "FULL_KEY_VALIDATION_BEFORE_DECISION",
            "authority_audit_policy.requested_key_validation",
        )
        _require_bool(
            self.explicit_full_audit_command_required,
            True,
            "authority_audit_policy.explicit_full_audit_command_required",
        )
        _require_bool(self.one_key_mutex_at_a_time, True, "authority_audit_policy.one_key_mutex_at_a_time")
        _require_bool(
            self.immutable_audit_evidence_required,
            True,
            "authority_audit_policy.immutable_audit_evidence_required",
        )
        _require_exact(self.authority_changing_effect, PROHIBITED, "authority_audit_policy.authority_changing_effect")
        _require_bool(self.deterministic_ordering, True, "authority_audit_policy.deterministic_ordering")
        _require_bool(self.single_mutex_for_batch, True, "authority_audit_policy.single_mutex_for_batch")
        _require_exact(
            self.non_atomic_multi_key_classification,
            "BATCH_NOT_ATOMIC",
            "authority_audit_policy.non_atomic_multi_key_classification",
        )
        _require_bool(
            self.start_end_reconciliation_required,
            True,
            "authority_audit_policy.start_end_reconciliation_required",
        )
        _require_bool(self.authority_change_reason_required, True, "authority_audit_policy.authority_change_reason_required")


@dataclass(frozen=True, slots=True)
class AcquisitionContractV2:
    contract_schema_version: str
    decision_set_version: str
    contract_status: str
    human_decisions_status: str
    acquisition_enabled: bool
    provider_execution_enabled: bool
    calendar_generation_enabled: bool
    normalization_enabled: bool
    registry_authority_enabled: bool
    runtime_profile_migration_status: str
    technical_constants: TechnicalConstants
    provider_policy: ProviderPolicy
    fixed_range_policy: FixedRangePolicy
    source_bar_policy: SourceBarPolicy
    profiles: tuple[ProfileAcquisitionPolicy, ...]
    aggregation_policy: AggregationPolicy
    calendar_policy: CalendarPolicy
    instrument_identity_policy: InstrumentIdentityPolicy
    corporate_action_policy: CorporateActionPolicy
    chunking_policy: ChunkingPolicy
    semantic_equivalence_policy: SemanticEquivalencePolicy
    normalization_policy: NormalizationPolicy
    generation_policy: GenerationPolicy
    registry_policy: RegistryPolicy
    quarantine_policy: QuarantinePolicy
    authority_storage_policy: AuthorityStoragePolicy
    authority_audit_policy: AuthorityAuditPolicy

    def validate(self) -> None:
        _require_exact(self.contract_schema_version, CONTRACT_SCHEMA_VERSION, "contract_schema_version")
        _require_exact(self.decision_set_version, DECISION_SET_VERSION, "decision_set_version")
        _require_exact(self.contract_status, CONTRACT_STATUS_READY, "contract_status")
        _require_exact(self.human_decisions_status, HUMAN_DECISIONS_COMPLETE, "human_decisions_status")
        for field_name in (
            "acquisition_enabled",
            "provider_execution_enabled",
            "calendar_generation_enabled",
            "normalization_enabled",
            "registry_authority_enabled",
        ):
            _require_bool(getattr(self, field_name), False, field_name)
        _require_exact(
            self.runtime_profile_migration_status,
            RUNTIME_MIGRATION_PENDING,
            "runtime_profile_migration_status",
        )
        self.technical_constants.validate()
        self.provider_policy.validate()
        self.fixed_range_policy.validate()
        self.source_bar_policy.validate()
        profile_ids = tuple(profile.profile_id for profile in self.profiles)
        _require_tuple(profile_ids, (PROFILE_SWING, PROFILE_POSITION_SWING), "profiles.profile_id order")
        for profile in self.profiles:
            profile.validate()
        self.aggregation_policy.validate()
        self.calendar_policy.validate()
        self.instrument_identity_policy.validate()
        self.corporate_action_policy.validate()
        self.chunking_policy.validate()
        self.semantic_equivalence_policy.validate()
        self.normalization_policy.validate()
        self.generation_policy.validate()
        self.registry_policy.validate()
        self.quarantine_policy.validate()
        self.authority_storage_policy.validate()
        self.authority_audit_policy.validate()


_TOP_LEVEL_KEYS = {
    "contract_schema_version",
    "decision_set_version",
    "contract_status",
    "human_decisions_status",
    "acquisition_enabled",
    "provider_execution_enabled",
    "calendar_generation_enabled",
    "normalization_enabled",
    "registry_authority_enabled",
    "runtime_profile_migration_status",
    "technical_constants",
    "provider_policy",
    "fixed_range_policy",
    "source_bar_policy",
    "profiles",
    "aggregation_policy",
    "calendar_policy",
    "instrument_identity_policy",
    "corporate_action_policy",
    "chunking_policy",
    "semantic_equivalence_policy",
    "normalization_policy",
    "generation_policy",
    "registry_policy",
    "quarantine_policy",
    "authority_storage_policy",
    "authority_audit_policy",
}

_TUPLE_FIELDS_BY_CLASS = {
    TechnicalConstants: ("retry_backoff_seconds", "retryable_categories", "non_retryable_categories"),
    CalendarPolicy: ("future_artifact_evidence", "required_artifact_fields"),
    InstrumentIdentityPolicy: ("required_evidence",),
    SemanticEquivalencePolicy: (
        "required_row_fields",
        "exact_integer_fields",
        "optional_presence_sensitive_fields",
        "optional_audit_fields",
        "excluded_from_equivalence",
    ),
    NormalizationPolicy: ("core_artifact_columns", "audit_artifact_columns", "segment_artifacts"),
    GenerationPolicy: ("generation_statuses", "lifecycle"),
    RegistryPolicy: ("registry_key_fields",),
    QuarantinePolicy: ("persistent_pre_gate_latches",),
}


def _build_model(model_type: type[Any], payload: dict[str, Any], context: str) -> Any:
    expected = set(model_type.__dataclass_fields__)  # type: ignore[attr-defined]
    _expect_keys(payload, expected, context)
    values = dict(payload)
    for field_name in _TUPLE_FIELDS_BY_CLASS.get(model_type, ()):
        values[field_name] = _tuple_values(values[field_name], f"{context}.{field_name}")
    model = model_type(**values)
    model.validate()
    return model


def _build_profile(payload: dict[str, Any], context: str) -> ProfileAcquisitionPolicy:
    expected = set(ProfileAcquisitionPolicy.__dataclass_fields__)
    _expect_keys(payload, expected, context)
    values = dict(payload)
    windows = values["window_segments"]
    if not isinstance(windows, list):
        raise ContractV2ValidationError(f"{context}.window_segments must be a list")
    parsed_windows = []
    for index, window_payload in enumerate(windows):
        if not isinstance(window_payload, dict):
            raise ContractV2ValidationError(f"{context}.window_segments[{index}] must be a table")
        _expect_keys(window_payload, set(BarWindow.__dataclass_fields__), f"{context}.window_segments[{index}]")
        parsed_windows.append(BarWindow(**window_payload))
    values["window_segments"] = tuple(parsed_windows)
    profile = ProfileAcquisitionPolicy(**values)
    profile.validate()
    return profile


def contract_from_dict(payload: dict[str, Any]) -> AcquisitionContractV2:
    """Build and validate a v2 acquisition contract from parsed TOML data."""
    _reject_operational_field_names(payload)
    _expect_keys(payload, _TOP_LEVEL_KEYS, "contract")
    if payload.get("contract_schema_version") != CONTRACT_SCHEMA_VERSION:
        raise ContractV2ValidationError("unknown or unsupported acquisition contract schema version")
    profiles_payload = payload["profiles"]
    if not isinstance(profiles_payload, list):
        raise ContractV2ValidationError("profiles must be a list of tables")
    contract = AcquisitionContractV2(
        contract_schema_version=payload["contract_schema_version"],
        decision_set_version=payload["decision_set_version"],
        contract_status=payload["contract_status"],
        human_decisions_status=payload["human_decisions_status"],
        acquisition_enabled=payload["acquisition_enabled"],
        provider_execution_enabled=payload["provider_execution_enabled"],
        calendar_generation_enabled=payload["calendar_generation_enabled"],
        normalization_enabled=payload["normalization_enabled"],
        registry_authority_enabled=payload["registry_authority_enabled"],
        runtime_profile_migration_status=payload["runtime_profile_migration_status"],
        technical_constants=_build_model(TechnicalConstants, payload["technical_constants"], "technical_constants"),
        provider_policy=_build_model(ProviderPolicy, payload["provider_policy"], "provider_policy"),
        fixed_range_policy=_build_model(FixedRangePolicy, payload["fixed_range_policy"], "fixed_range_policy"),
        source_bar_policy=_build_model(SourceBarPolicy, payload["source_bar_policy"], "source_bar_policy"),
        profiles=tuple(_build_profile(profile, f"profiles[{index}]") for index, profile in enumerate(profiles_payload)),
        aggregation_policy=_build_model(AggregationPolicy, payload["aggregation_policy"], "aggregation_policy"),
        calendar_policy=_build_model(CalendarPolicy, payload["calendar_policy"], "calendar_policy"),
        instrument_identity_policy=_build_model(
            InstrumentIdentityPolicy,
            payload["instrument_identity_policy"],
            "instrument_identity_policy",
        ),
        corporate_action_policy=_build_model(CorporateActionPolicy, payload["corporate_action_policy"], "corporate_action_policy"),
        chunking_policy=_build_model(ChunkingPolicy, payload["chunking_policy"], "chunking_policy"),
        semantic_equivalence_policy=_build_model(
            SemanticEquivalencePolicy,
            payload["semantic_equivalence_policy"],
            "semantic_equivalence_policy",
        ),
        normalization_policy=_build_model(NormalizationPolicy, payload["normalization_policy"], "normalization_policy"),
        generation_policy=_build_model(GenerationPolicy, payload["generation_policy"], "generation_policy"),
        registry_policy=_build_model(RegistryPolicy, payload["registry_policy"], "registry_policy"),
        quarantine_policy=_build_model(QuarantinePolicy, payload["quarantine_policy"], "quarantine_policy"),
        authority_storage_policy=_build_model(AuthorityStoragePolicy, payload["authority_storage_policy"], "authority_storage_policy"),
        authority_audit_policy=_build_model(AuthorityAuditPolicy, payload["authority_audit_policy"], "authority_audit_policy"),
    )
    contract.validate()
    return contract


def load_contract_toml(path: str | Path = DEFAULT_CONFIG_REFERENCE) -> AcquisitionContractV2:
    """Load a source-controlled v2 contract from repo config."""
    validated = _validate_contract_reference(path)
    with validated.open("rb") as handle:
        payload = tomllib.load(handle)
    return contract_from_dict(payload)


def default_contract() -> AcquisitionContractV2:
    """Return the checked-in default v2 contract."""
    return load_contract_toml(DEFAULT_CONFIG_REFERENCE)


def calendar_package_status(contract: AcquisitionContractV2) -> dict[str, Any]:
    """Report calendar package install status without importing the package."""
    package_name = contract.calendar_policy.calendar_package
    try:
        installed_version = metadata.version(package_name)
    except metadata.PackageNotFoundError:
        installed_version = None
    return {
        "calendar_package": package_name,
        "calendar_package_version_pin": contract.calendar_policy.calendar_package_version,
        "calendar_package_installed": installed_version is not None,
        "calendar_package_installed_version": installed_version or "NOT_INSTALLED",
        "calendar_package_pin_matches_installed": installed_version == contract.calendar_policy.calendar_package_version,
    }


def readiness_receipt(contract: AcquisitionContractV2) -> dict[str, Any]:
    """Return a sanitized offline readiness receipt."""
    contract.validate()
    profile_receipts = {
        profile.profile_id: {
            "profile_contract_version": profile.profile_contract_version,
            "canonical_bar_type": profile.canonical_bar_type,
            "minimum_valid_rows": profile.minimum_valid_rows,
            "source_interval": profile.source_interval,
            "source_bars_per_canonical_bar": profile.source_bars_per_canonical_bar,
            "timestamp_semantic": profile.timestamp_semantic,
            "session_policy": profile.session_policy,
            "early_close_policy": profile.early_close_policy,
            "higher_timeframe_context": profile.higher_timeframe_context,
        }
        for profile in contract.profiles
    }
    return {
        "contract_schema_version": contract.contract_schema_version,
        "decision_set_version": contract.decision_set_version,
        "contract_status": contract.contract_status,
        "human_decisions_status": contract.human_decisions_status,
        "contract_digest": contract_digest(contract),
        "acquisition_enabled": contract.acquisition_enabled,
        "provider_execution_enabled": contract.provider_execution_enabled,
        "calendar_generation_enabled": contract.calendar_generation_enabled,
        "normalization_enabled": contract.normalization_enabled,
        "registry_authority_enabled": contract.registry_authority_enabled,
        "runtime_profile_migration_status": contract.runtime_profile_migration_status,
        "provider_business_identity": contract.provider_policy.business_provider,
        "provider_former_brand": contract.provider_policy.former_brand,
        "provider_entitlement_status": contract.provider_policy.provider_entitlement_status,
        "provider_entitlement_evidence": contract.provider_policy.entitlement_evidence,
        "provider_subscription_plan": contract.provider_policy.subscription_plan,
        "provider_historical_access": contract.provider_policy.historical_access,
        "provider_data_recency": contract.provider_policy.market_data_recency,
        "provider_aggregate_access": contract.provider_policy.aggregate_access,
        "legacy_adapter_family": contract.provider_policy.installed_adapter_family,
        "legacy_adapter_version": contract.provider_policy.installed_adapter_version,
        "fixed_start_date": contract.fixed_range_policy.start_date,
        "fixed_end_date": contract.fixed_range_policy.end_date,
        "source_interval": contract.source_bar_policy.provider_source_interval,
        "source_timezone": contract.source_bar_policy.source_timezone,
        "canonical_storage_timezone": contract.source_bar_policy.canonical_storage_timezone,
        "profiles": profile_receipts,
        "calendar_package": calendar_package_status(contract),
        "readiness_note": "DECLARATIVE_OFFLINE_ONLY_NO_ACQUISITION",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit the offline MarketFlow acquisition contract v2 receipt.")
    parser.parse_args(argv)
    contract = default_contract()
    print(json.dumps(readiness_receipt(contract), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
