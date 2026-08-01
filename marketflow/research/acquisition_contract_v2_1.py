"""Offline declarative historical acquisition contract v2.1 for MarketFlow."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tomllib
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from marketflow.research import acquisition_contract_v2 as base_v2


CONTRACT_SCHEMA_VERSION = "marketflow.acquisition_contract.v2.1"
DECISION_SET_VERSION = "marketflow.acquisition_decisions.v2.1"
CONTRACT_STATUS_READY = "ACQUISITION_CONTRACT_V2_1_READY_FOR_IMPLEMENTATION"
BASE_CONTRACT_SCHEMA = "marketflow.acquisition_contract.v2"
BASE_CONTRACT_DIGEST = "59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0"
RUNTIME_MIGRATION_PENDING = "LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION"

STOCKS_CUSTOM_BARS_V2 = "STOCKS_CUSTOM_BARS_V2"
PROVIDER_TIMESTAMP_FIELD = "t"
UNIX_EPOCH_MILLISECONDS = "UNIX_EPOCH_MILLISECONDS"
START_OF_AGGREGATE_WINDOW = "START_OF_AGGREGATE_WINDOW"
SOURCE_INTERVAL_MINUTES = 15
SOURCE_INTERVAL_DURATION = "PT15M"
LEFT_CLOSED_RIGHT_OPEN = "LEFT_CLOSED_RIGHT_OPEN"
WINDOW_START_UTC = "window_start_utc"
WINDOW_END_UTC = "window_end_utc"
UTC_TEXT = "UTC"
SESSION_MAPPING_TIMEZONE = "America/New_York"
WINDOW_END = "WINDOW_END"
WINDOW_START = "WINDOW_START"
PROHIBITED = "PROHIBITED"

DEFAULT_CONFIG_REFERENCE = "config/fixed_date_acquisition_contract_v2_1.toml"
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CREDENTIAL_FRAGMENTS = ("api_key", "apikey", "secret", "token", "password", "credential", "authorization")
URL_FIELD_FRAGMENTS = ("url", "uri")
PATH_FIELD_NAMES = {"path", "local_path", "absolute_path", "output_path", "directory", "folder"}
ALLOWED_REFERENCE_FIELDS = {"base_contract_schema", "base_contract_digest"}
NORMALIZED_SOURCE_FIELDS = ("window_start_utc", "window_end_utc", "open", "high", "low", "close", "volume")


class ContractV21ValidationError(ValueError):
    """Raised when the v2.1 acquisition contract is malformed or unsafe."""


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
    """Serialize a v2.1 contract deterministically for semantic digesting."""
    return json.dumps(
        _as_dict(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def contract_digest(value: Any) -> str:
    """Return the deterministic SHA-256 digest for a v2.1 contract payload."""
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _require_exact(value: Any, expected: Any, field_name: str) -> None:
    if value != expected:
        raise ContractV21ValidationError(f"{field_name} must be {expected!r}")


def _require_bool(value: Any, expected: bool, field_name: str) -> None:
    if type(value) is not bool or value is not expected:
        raise ContractV21ValidationError(f"{field_name} must be {expected!r}")


def _require_int(value: Any, expected: int, field_name: str) -> None:
    if type(value) is not int or value != expected:
        raise ContractV21ValidationError(f"{field_name} must be {expected!r}")


def _require_tuple(value: tuple[Any, ...], expected: tuple[Any, ...], field_name: str) -> None:
    if not isinstance(value, tuple) or value != expected:
        raise ContractV21ValidationError(f"{field_name} must be {expected!r}")


def _expect_keys(payload: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(payload)
    missing = expected - actual
    unknown = actual - expected
    if missing:
        raise ContractV21ValidationError(f"{context} missing keys: {sorted(missing)}")
    if unknown:
        raise ContractV21ValidationError(f"{context} unknown keys: {sorted(unknown)}")


def _tuple_values(value: Any, field_name: str) -> tuple[Any, ...]:
    if not isinstance(value, (list, tuple)):
        raise ContractV21ValidationError(f"{field_name} must be a list")
    return tuple(value)


def _reject_operational_field_names(payload: dict[str, Any], prefix: str = "") -> None:
    for key, value in payload.items():
        lowered = str(key).lower()
        dotted = f"{prefix}.{key}" if prefix else str(key)
        if lowered not in ALLOWED_REFERENCE_FIELDS:
            if any(fragment in lowered for fragment in CREDENTIAL_FRAGMENTS):
                raise ContractV21ValidationError(f"credential-like field is prohibited: {dotted}")
            if any(fragment in lowered for fragment in URL_FIELD_FRAGMENTS):
                raise ContractV21ValidationError(f"URL field is prohibited: {dotted}")
            if lowered in PATH_FIELD_NAMES or lowered.endswith("_path"):
                raise ContractV21ValidationError(f"local path field is prohibited: {dotted}")
        if isinstance(value, dict):
            _reject_operational_field_names(value, dotted)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_operational_field_names(item, f"{dotted}[{index}]")


def _validate_contract_reference(path: str | Path) -> Path:
    text = str(path)
    if not text or "://" in text or "\x00" in text or "$" in text or "%" in text:
        raise ContractV21ValidationError("contract path must be a direct repo config TOML reference")
    candidate = Path(path)
    if any(":" in part for part in candidate.parts[1:]):
        raise ContractV21ValidationError("contract path must not contain device or stream syntax")
    root = _repo_root().resolve()
    config_dir = (root / "config").resolve()
    resolved = (candidate if candidate.is_absolute() else root / candidate).resolve(strict=False)
    if resolved.parent != config_dir:
        raise ContractV21ValidationError("contract path must be a direct file under repo config")
    if resolved.name != "fixed_date_acquisition_contract_v2_1.toml":
        raise ContractV21ValidationError("contract path must be the approved v2.1 config file")
    if resolved.suffix.lower() != ".toml" or resolved.name in {"", ".", ".."}:
        raise ContractV21ValidationError("contract path must be a TOML file")
    if resolved.exists() and resolved.is_symlink():
        raise ContractV21ValidationError("contract path must not be a symlink")
    return resolved


def _parse_hhmm(value: str, field_name: str) -> time:
    try:
        hour_text, minute_text = value.split(":", 1)
        parsed = time(hour=int(hour_text), minute=int(minute_text))
    except (ValueError, TypeError) as exc:
        raise ContractV21ValidationError(f"{field_name} must be HH:MM") from exc
    if parsed.second or parsed.microsecond:
        raise ContractV21ValidationError(f"{field_name} must not include seconds")
    return parsed


@dataclass(frozen=True, slots=True)
class SourceTimestampPolicy:
    provider_endpoint_family: str = STOCKS_CUSTOM_BARS_V2
    provider_timestamp_field: str = PROVIDER_TIMESTAMP_FIELD
    provider_timestamp_unit: str = UNIX_EPOCH_MILLISECONDS
    provider_timestamp_semantic: str = START_OF_AGGREGATE_WINDOW
    source_interval_minutes: int = SOURCE_INTERVAL_MINUTES
    source_interval_duration: str = SOURCE_INTERVAL_DURATION
    interval_boundary: str = LEFT_CLOSED_RIGHT_OPEN
    canonical_start_field: str = WINDOW_START_UTC
    canonical_end_field: str = WINDOW_END_UTC
    canonical_storage_timezone: str = UTC_TEXT
    session_mapping_timezone: str = SESSION_MAPPING_TIMEZONE
    derived_bar_timestamp_semantic: str = WINDOW_END
    exact_slot_alignment_required: bool = True
    timestamp_snapping_enabled: bool = False
    timestamp_tolerance_enabled: bool = False

    def validate(self) -> None:
        _require_exact(self.provider_endpoint_family, STOCKS_CUSTOM_BARS_V2, "source_timestamp_policy.provider_endpoint_family")
        _require_exact(self.provider_timestamp_field, PROVIDER_TIMESTAMP_FIELD, "source_timestamp_policy.provider_timestamp_field")
        _require_exact(self.provider_timestamp_unit, UNIX_EPOCH_MILLISECONDS, "source_timestamp_policy.provider_timestamp_unit")
        _require_exact(
            self.provider_timestamp_semantic,
            START_OF_AGGREGATE_WINDOW,
            "source_timestamp_policy.provider_timestamp_semantic",
        )
        _require_int(self.source_interval_minutes, SOURCE_INTERVAL_MINUTES, "source_timestamp_policy.source_interval_minutes")
        _require_exact(self.source_interval_duration, SOURCE_INTERVAL_DURATION, "source_timestamp_policy.source_interval_duration")
        _require_exact(self.interval_boundary, LEFT_CLOSED_RIGHT_OPEN, "source_timestamp_policy.interval_boundary")
        _require_exact(self.canonical_start_field, WINDOW_START_UTC, "source_timestamp_policy.canonical_start_field")
        _require_exact(self.canonical_end_field, WINDOW_END_UTC, "source_timestamp_policy.canonical_end_field")
        _require_exact(self.canonical_storage_timezone, UTC_TEXT, "source_timestamp_policy.canonical_storage_timezone")
        _require_exact(self.session_mapping_timezone, SESSION_MAPPING_TIMEZONE, "source_timestamp_policy.session_mapping_timezone")
        _require_exact(self.derived_bar_timestamp_semantic, WINDOW_END, "source_timestamp_policy.derived_bar_timestamp_semantic")
        _require_bool(self.exact_slot_alignment_required, True, "source_timestamp_policy.exact_slot_alignment_required")
        _require_bool(self.timestamp_snapping_enabled, False, "source_timestamp_policy.timestamp_snapping_enabled")
        _require_bool(self.timestamp_tolerance_enabled, False, "source_timestamp_policy.timestamp_tolerance_enabled")


@dataclass(frozen=True, slots=True)
class NormalizedSourceBarContract:
    identity_fields: tuple[str, ...] = NORMALIZED_SOURCE_FIELDS
    window_start_source: str = "PROVIDER_FIELD_T"
    window_end_rule: str = "WINDOW_START_PLUS_PT15M"
    timezone_requirement: str = "TIMEZONE_AWARE_UTC"
    timestamp_utc_compatibility_field: str = "timestamp_utc"
    timestamp_utc_compatibility_semantic: str = WINDOW_START
    caller_selected_timestamp_semantic: str = PROHIBITED
    local_machine_timezone_dependency: bool = False
    timestamp_snapping_enabled: bool = False
    timestamp_tolerance_enabled: bool = False

    def validate(self) -> None:
        _require_tuple(self.identity_fields, NORMALIZED_SOURCE_FIELDS, "normalized_source_bar_contract.identity_fields")
        _require_exact(self.window_start_source, "PROVIDER_FIELD_T", "normalized_source_bar_contract.window_start_source")
        _require_exact(self.window_end_rule, "WINDOW_START_PLUS_PT15M", "normalized_source_bar_contract.window_end_rule")
        _require_exact(self.timezone_requirement, "TIMEZONE_AWARE_UTC", "normalized_source_bar_contract.timezone_requirement")
        _require_exact(
            self.timestamp_utc_compatibility_field,
            "timestamp_utc",
            "normalized_source_bar_contract.timestamp_utc_compatibility_field",
        )
        _require_exact(
            self.timestamp_utc_compatibility_semantic,
            WINDOW_START,
            "normalized_source_bar_contract.timestamp_utc_compatibility_semantic",
        )
        _require_exact(
            self.caller_selected_timestamp_semantic,
            PROHIBITED,
            "normalized_source_bar_contract.caller_selected_timestamp_semantic",
        )
        _require_bool(self.local_machine_timezone_dependency, False, "normalized_source_bar_contract.local_machine_timezone_dependency")
        _require_bool(self.timestamp_snapping_enabled, False, "normalized_source_bar_contract.timestamp_snapping_enabled")
        _require_bool(self.timestamp_tolerance_enabled, False, "normalized_source_bar_contract.timestamp_tolerance_enabled")


@dataclass(frozen=True, slots=True)
class DerivedTimestampContract:
    derived_bar_timestamp_semantic: str = WINDOW_END
    swing_morning_timestamp_local: str = "12:45"
    swing_afternoon_timestamp_local: str = "16:00"
    position_swing_timestamp_local: str = "16:00"
    timezone: str = SESSION_MAPPING_TIMEZONE
    canonical_timezone: str = UTC_TEXT
    source_bar_timestamp_semantic: str = START_OF_AGGREGATE_WINDOW
    provider_native_4h_canonical: bool = False
    provider_native_1d_canonical: bool = False

    def validate(self) -> None:
        _require_exact(self.derived_bar_timestamp_semantic, WINDOW_END, "derived_timestamp_contract.derived_bar_timestamp_semantic")
        _require_exact(self.swing_morning_timestamp_local, "12:45", "derived_timestamp_contract.swing_morning_timestamp_local")
        _require_exact(self.swing_afternoon_timestamp_local, "16:00", "derived_timestamp_contract.swing_afternoon_timestamp_local")
        _require_exact(self.position_swing_timestamp_local, "16:00", "derived_timestamp_contract.position_swing_timestamp_local")
        _parse_hhmm(self.swing_morning_timestamp_local, "derived_timestamp_contract.swing_morning_timestamp_local")
        _parse_hhmm(self.swing_afternoon_timestamp_local, "derived_timestamp_contract.swing_afternoon_timestamp_local")
        _parse_hhmm(self.position_swing_timestamp_local, "derived_timestamp_contract.position_swing_timestamp_local")
        _require_exact(self.timezone, SESSION_MAPPING_TIMEZONE, "derived_timestamp_contract.timezone")
        _require_exact(self.canonical_timezone, UTC_TEXT, "derived_timestamp_contract.canonical_timezone")
        _require_exact(
            self.source_bar_timestamp_semantic,
            START_OF_AGGREGATE_WINDOW,
            "derived_timestamp_contract.source_bar_timestamp_semantic",
        )
        _require_bool(self.provider_native_4h_canonical, False, "derived_timestamp_contract.provider_native_4h_canonical")
        _require_bool(self.provider_native_1d_canonical, False, "derived_timestamp_contract.provider_native_1d_canonical")


@dataclass(frozen=True, slots=True)
class AcquisitionContractV21:
    contract_schema_version: str
    decision_set_version: str
    contract_status: str
    base_contract_schema: str
    base_contract_digest: str
    acquisition_enabled: bool
    provider_execution_enabled: bool
    calendar_generation_enabled: bool
    normalization_enabled: bool
    registry_authority_enabled: bool
    runtime_profile_migration_status: str
    source_timestamp_policy: SourceTimestampPolicy
    normalized_source_bar_contract: NormalizedSourceBarContract
    derived_timestamp_contract: DerivedTimestampContract

    def validate(self) -> None:
        _require_exact(self.contract_schema_version, CONTRACT_SCHEMA_VERSION, "contract_schema_version")
        _require_exact(self.decision_set_version, DECISION_SET_VERSION, "decision_set_version")
        _require_exact(self.contract_status, CONTRACT_STATUS_READY, "contract_status")
        _require_exact(self.base_contract_schema, BASE_CONTRACT_SCHEMA, "base_contract_schema")
        _require_exact(self.base_contract_digest, BASE_CONTRACT_DIGEST, "base_contract_digest")
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
        self.source_timestamp_policy.validate()
        self.normalized_source_bar_contract.validate()
        self.derived_timestamp_contract.validate()


_TOP_LEVEL_KEYS = {
    "contract_schema_version",
    "decision_set_version",
    "contract_status",
    "base_contract_schema",
    "base_contract_digest",
    "acquisition_enabled",
    "provider_execution_enabled",
    "calendar_generation_enabled",
    "normalization_enabled",
    "registry_authority_enabled",
    "runtime_profile_migration_status",
    "source_timestamp_policy",
    "normalized_source_bar_contract",
    "derived_timestamp_contract",
}

_TUPLE_FIELDS_BY_CLASS = {
    NormalizedSourceBarContract: ("identity_fields",),
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


def contract_from_dict(payload: dict[str, Any]) -> AcquisitionContractV21:
    """Build and validate a v2.1 acquisition contract from parsed TOML data."""
    _reject_operational_field_names(payload)
    _expect_keys(payload, _TOP_LEVEL_KEYS, "contract")
    if payload.get("contract_schema_version") != CONTRACT_SCHEMA_VERSION:
        raise ContractV21ValidationError("unknown or unsupported acquisition contract schema version")
    contract = AcquisitionContractV21(
        contract_schema_version=payload["contract_schema_version"],
        decision_set_version=payload["decision_set_version"],
        contract_status=payload["contract_status"],
        base_contract_schema=payload["base_contract_schema"],
        base_contract_digest=payload["base_contract_digest"],
        acquisition_enabled=payload["acquisition_enabled"],
        provider_execution_enabled=payload["provider_execution_enabled"],
        calendar_generation_enabled=payload["calendar_generation_enabled"],
        normalization_enabled=payload["normalization_enabled"],
        registry_authority_enabled=payload["registry_authority_enabled"],
        runtime_profile_migration_status=payload["runtime_profile_migration_status"],
        source_timestamp_policy=_build_model(
            SourceTimestampPolicy,
            payload["source_timestamp_policy"],
            "source_timestamp_policy",
        ),
        normalized_source_bar_contract=_build_model(
            NormalizedSourceBarContract,
            payload["normalized_source_bar_contract"],
            "normalized_source_bar_contract",
        ),
        derived_timestamp_contract=_build_model(
            DerivedTimestampContract,
            payload["derived_timestamp_contract"],
            "derived_timestamp_contract",
        ),
    )
    contract.validate()
    return contract


def load_contract_toml(path: str | Path = DEFAULT_CONFIG_REFERENCE) -> AcquisitionContractV21:
    """Load the source-controlled v2.1 contract from repo config."""
    validated = _validate_contract_reference(path)
    with validated.open("rb") as handle:
        payload = tomllib.load(handle)
    return contract_from_dict(payload)


def default_contract() -> AcquisitionContractV21:
    """Return the checked-in default v2.1 contract."""
    return load_contract_toml(DEFAULT_CONFIG_REFERENCE)


def verify_base_contract_digest(contract: AcquisitionContractV21) -> str:
    """Validate that the checked-in v2 contract still matches the v2.1 binding."""
    base_contract = base_v2.default_contract()
    digest = base_v2.contract_digest(base_contract)
    if digest != contract.base_contract_digest:
        raise ContractV21ValidationError("base v2 contract digest mismatch")
    return digest


def source_window_from_epoch_ms(epoch_milliseconds: Any) -> tuple[datetime, datetime]:
    """Return the exact UTC source interval for one provider timestamp field t."""
    if type(epoch_milliseconds) is not int:
        raise ContractV21ValidationError("provider timestamp t must be integer Unix epoch milliseconds")
    epoch_seconds, millisecond_remainder = divmod(epoch_milliseconds, 1000)
    if millisecond_remainder != 0:
        raise ContractV21ValidationError("provider timestamp t must align to an exact UTC second")
    window_start = datetime.fromtimestamp(epoch_seconds, tz=UTC)
    if window_start.second or window_start.microsecond:
        raise ContractV21ValidationError("provider timestamp t must align to an exact minute")
    if window_start.minute % SOURCE_INTERVAL_MINUTES != 0:
        raise ContractV21ValidationError("provider timestamp t must align to the exact 15-minute grid")
    window_end = window_start + timedelta(minutes=SOURCE_INTERVAL_MINUTES)
    return window_start, window_end


def source_window_for_local_start(session_date: str, local_start_hhmm: str) -> tuple[datetime, datetime]:
    """Return UTC source window bounds for a local RTH source-bar start."""
    if not ISO_DATE_RE.match(session_date):
        raise ContractV21ValidationError("session_date must be YYYY-MM-DD")
    parsed_date = date.fromisoformat(session_date)
    parsed_time = _parse_hhmm(local_start_hhmm, "local_start_hhmm")
    local_start = datetime.combine(parsed_date, parsed_time, tzinfo=ZoneInfo(SESSION_MAPPING_TIMEZONE))
    window_start = local_start.astimezone(UTC)
    return window_start, window_start + timedelta(minutes=SOURCE_INTERVAL_MINUTES)


def derived_timestamp_utc(session_date: str, local_hhmm: str) -> datetime:
    """Return the UTC close timestamp for a derived MarketFlow bar."""
    if not ISO_DATE_RE.match(session_date):
        raise ContractV21ValidationError("session_date must be YYYY-MM-DD")
    parsed_date = date.fromisoformat(session_date)
    parsed_time = _parse_hhmm(local_hhmm, "local_hhmm")
    local_timestamp = datetime.combine(parsed_date, parsed_time, tzinfo=ZoneInfo(SESSION_MAPPING_TIMEZONE))
    return local_timestamp.astimezone(UTC)


def rth_source_start_labels() -> dict[str, tuple[str, ...]]:
    """Return the documented ordinary-session source start labels."""
    morning = tuple(f"{hour:02d}:{minute:02d}" for hour, minute in _slot_pairs(time(9, 30), 13))
    afternoon = tuple(f"{hour:02d}:{minute:02d}" for hour, minute in _slot_pairs(time(12, 45), 13))
    return {
        "morning": morning,
        "afternoon": afternoon,
        "daily": morning + afternoon,
    }


def _slot_pairs(start: time, count: int) -> tuple[tuple[int, int], ...]:
    cursor = datetime.combine(date(2000, 1, 1), start)
    slots = []
    for _ in range(count):
        slots.append((cursor.hour, cursor.minute))
        cursor += timedelta(minutes=SOURCE_INTERVAL_MINUTES)
    return tuple(slots)


def readiness_receipt(contract: AcquisitionContractV21) -> dict[str, Any]:
    """Return a sanitized offline readiness receipt."""
    contract.validate()
    base_digest = verify_base_contract_digest(contract)
    return {
        "status": contract.contract_status,
        "contract_schema_version": contract.contract_schema_version,
        "decision_set_version": contract.decision_set_version,
        "contract_digest": contract_digest(contract),
        "base_contract_schema": contract.base_contract_schema,
        "base_contract_digest": base_digest,
        "timestamp_policy_complete": True,
        "source_endpoint": contract.source_timestamp_policy.provider_endpoint_family,
        "source_timestamp_field": contract.source_timestamp_policy.provider_timestamp_field,
        "source_timestamp_unit": contract.source_timestamp_policy.provider_timestamp_unit,
        "source_timestamp_semantic": contract.source_timestamp_policy.provider_timestamp_semantic,
        "source_interval_duration": contract.source_timestamp_policy.source_interval_duration,
        "interval_boundary": contract.source_timestamp_policy.interval_boundary,
        "canonical_start_field": contract.source_timestamp_policy.canonical_start_field,
        "canonical_end_field": contract.source_timestamp_policy.canonical_end_field,
        "derived_timestamp_semantic": contract.derived_timestamp_contract.derived_bar_timestamp_semantic,
        "timestamp_utc_compatibility_semantic": contract.normalized_source_bar_contract.timestamp_utc_compatibility_semantic,
        "acquisition_enabled": contract.acquisition_enabled,
        "provider_execution_enabled": contract.provider_execution_enabled,
        "calendar_generation_enabled": contract.calendar_generation_enabled,
        "normalization_enabled": contract.normalization_enabled,
        "registry_authority_enabled": contract.registry_authority_enabled,
        "frozen_calendar_engine": "NOT_IMPLEMENTED",
        "bar_engine": "NOT_IMPLEMENTED",
        "runtime_profile_migration_status": contract.runtime_profile_migration_status,
        "readiness_note": "DECLARATIVE_OFFLINE_ONLY_NO_ACQUISITION",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit the offline MarketFlow acquisition contract v2.1 receipt.")
    parser.parse_args(argv)
    contract = default_contract()
    print(json.dumps(readiness_receipt(contract), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
