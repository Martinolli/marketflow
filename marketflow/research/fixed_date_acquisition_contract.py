"""Offline fixed-date historical acquisition contract for MarketFlow."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import tomllib
from dataclasses import asdict, dataclass, field, replace
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


CONTRACT_VERSION = "marketflow.fixed_date_acquisition_contract.v1"
PROVIDER_IDENTITY = "MASSIVE_POLYGON_STOCKS_CUSTOM_BARS"
PROVIDER_BUSINESS_IDENTITY = "MASSIVE.COM"
PROVIDER_FORMER_BRAND = "POLYGON.IO"
ENDPOINT_FAMILY = "STOCKS_AGGREGATES_CUSTOM_BARS"
ENDPOINT_CONTRACT_VERSION = "v2_aggs_ticker_range"
ASSET_CLASS_US_EQUITY = "US_EQUITY"
CANONICAL_STORAGE_TIMEZONE = "UTC"
SOURCE_AGGREGATION_TIMEZONE = "AMERICA_NEW_YORK"
PROVIDER_ENTITLEMENT_NOT_CONFIRMED = "PROVIDER_ENTITLEMENT_NOT_CONFIRMED"
OPERATOR_ATTESTED_CONFIRMED = "OPERATOR_ATTESTED_CONFIRMED"
OPERATOR_ATTESTED = "OPERATOR_ATTESTED"
STOCKS_STARTER = "STOCKS_STARTER"
FIVE_YEARS = "FIVE_YEARS"
FIFTEEN_MINUTE_DELAYED = "FIFTEEN_MINUTE_DELAYED"
INTRADAY_AND_DAILY_AVAILABLE = "INTRADAY_AND_DAILY_AVAILABLE"
HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
NOT_CONFIRMED = "NOT_CONFIRMED"
NOT_APPROVED = "NOT_APPROVED"
NOT_SET = "NOT_SET"
CONTRACT_PROPOSED = "CONTRACT_PROPOSED"
MUST_MATCH_REQUEST = "MUST_MATCH_REQUEST"

PROFILE_SWING = "SWING"
PROFILE_POSITION_SWING = "POSITION_SWING"
TIMEFRAME_SWING = "4h"
TIMEFRAME_POSITION_SWING = "1d"
MINIMUM_ROWS_SWING = 390
MINIMUM_ROWS_POSITION_SWING = 560

BAR_PROVIDER_NATIVE_CLOCK_4H = "PROVIDER_NATIVE_CLOCK_4H"
BAR_DETERMINISTIC_LOCAL_AGGREGATION = "DETERMINISTIC_LOCAL_AGGREGATION"
BAR_CONSTRUCTION_NOT_CONFIRMED = "BAR_CONSTRUCTION_NOT_CONFIRMED"
BAR_PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW = "PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW"

SESSION_REGULAR_TRADING_HOURS_ONLY = "REGULAR_TRADING_HOURS_ONLY"
SESSION_EXTENDED_HOURS_INCLUDED = "EXTENDED_HOURS_INCLUDED"
SESSION_PROVIDER_DEFAULT = "PROVIDER_DEFAULT_SESSION"
SESSION_POLICY_NOT_CONFIRMED = "SESSION_POLICY_NOT_CONFIRMED"

ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS = "ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS"
ACQUISITION_CONTRACT_READY_FOR_APPROVAL = "ACQUISITION_CONTRACT_READY_FOR_APPROVAL"
ACQUISITION_CONTRACT_FROZEN = "ACQUISITION_CONTRACT_FROZEN"
FIXED_DATES_NOT_APPROVED = "FIXED_DATES_NOT_APPROVED"
BAR_CONSTRUCTION_NOT_APPROVED = "BAR_CONSTRUCTION_NOT_APPROVED"
SESSION_POLICY_NOT_APPROVED = "SESSION_POLICY_NOT_APPROVED"
ADJUSTMENT_POLICY_NOT_APPROVED = "ADJUSTMENT_POLICY_NOT_APPROVED"
PAGINATION_POLICY_NOT_APPROVED = "PAGINATION_POLICY_NOT_APPROVED"

REQUEST_COMPLETE = "REQUEST_COMPLETE"
REQUEST_TRUNCATED = "REQUEST_TRUNCATED"
PAGINATION_INCOMPLETE = "PAGINATION_INCOMPLETE"
PAGE_DUPLICATE = "PAGE_DUPLICATE"
RANGE_COVERAGE_INCOMPLETE = "RANGE_COVERAGE_INCOMPLETE"
PROVIDER_RESPONSE_INVALID = "PROVIDER_RESPONSE_INVALID"

RAW_PROVIDER_RESPONSE = "RAW_PROVIDER_RESPONSE"
NORMALIZED_OHLCV_DATASET = "NORMALIZED_OHLCV_DATASET"
ACQUISITION_REQUEST_CONTRACT = "ACQUISITION_REQUEST_CONTRACT"
ANNOTATED_DATASET = "ANNOTATED_DATASET"

RELATIVE_PERIOD_RE = re.compile(r"^\d+(d|w|mo|m|y|h)$", re.IGNORECASE)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CREDENTIAL_FRAGMENTS = ("api_key", "apikey", "secret", "token", "password", "credential", "authorization")
PATH_FIELD_NAMES = {"path", "local_path", "absolute_path", "output_path", "file", "directory", "folder"}
URL_FIELD_FRAGMENTS = ("url", "uri")
ALLOWED_SAFETY_DECLARATION_FIELDS = {"absolute_path_storage_allowed", "credential_storage_allowed"}


class ContractValidationError(ValueError):
    """Raised when the fixed-date acquisition contract is unsafe or invalid."""


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
    """Serialize a contract deterministically for semantic digests."""
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


def _require_enum(value: str, allowed: set[str], field_name: str) -> None:
    if value not in allowed:
        raise ContractValidationError(f"{field_name} has unsupported value: {value}")


def _reject_operational_field_names(payload: dict[str, Any], prefix: str = "") -> None:
    for key, value in payload.items():
        lowered = str(key).lower()
        dotted = f"{prefix}.{key}" if prefix else str(key)
        if lowered in ALLOWED_SAFETY_DECLARATION_FIELDS:
            continue
        if any(fragment in lowered for fragment in CREDENTIAL_FRAGMENTS):
            raise ContractValidationError(f"credential-like field is prohibited: {dotted}")
        if any(fragment in lowered for fragment in URL_FIELD_FRAGMENTS):
            raise ContractValidationError(f"arbitrary URL field is prohibited: {dotted}")
        if lowered in PATH_FIELD_NAMES or lowered.endswith("_path") or lowered.endswith("_file"):
            raise ContractValidationError(f"local path field is prohibited: {dotted}")
        if isinstance(value, dict):
            _reject_operational_field_names(value, dotted)


def _is_relative_date_token(value: str) -> bool:
    text = str(value).strip().lower()
    return text in {"today", "now"} or bool(RELATIVE_PERIOD_RE.match(text))


def _validate_date_value(value: str, status: str, field_name: str) -> None:
    if status != HUMAN_APPROVAL_REQUIRED:
        raise ContractValidationError(f"{field_name}_status must remain HUMAN_APPROVAL_REQUIRED in the proposed contract")
    if status == HUMAN_APPROVAL_REQUIRED:
        if value != HUMAN_APPROVAL_REQUIRED:
            raise ContractValidationError(f"{field_name} must remain HUMAN_APPROVAL_REQUIRED until approved")
        return
    if _is_relative_date_token(value):
        raise ContractValidationError(f"{field_name} must be a fixed ISO calendar date")
    if not ISO_DATE_RE.match(value):
        raise ContractValidationError(f"{field_name} must be YYYY-MM-DD")
    date.fromisoformat(value)


def _parse_approved_date(value: str, field_name: str) -> date:
    if _is_relative_date_token(value) or not ISO_DATE_RE.match(value):
        raise ContractValidationError(f"{field_name} must be a fixed ISO calendar date")
    return date.fromisoformat(value)


def _parse_utc_instant(value: Any, field_name: str) -> datetime:
    text = str(value)
    parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ContractValidationError(f"{field_name} must be timezone-aware")
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ContractValidationError(f"{field_name} must be UTC")
    parsed_utc = parsed.astimezone(timezone.utc)
    if parsed_utc.utcoffset() != timezone.utc.utcoffset(parsed_utc):
        raise ContractValidationError(f"{field_name} must resolve to UTC")
    return parsed_utc


@dataclass(frozen=True, slots=True)
class ProviderEntitlement:
    confirmation_status: str = OPERATOR_ATTESTED_CONFIRMED
    provider_current_brand: str = PROVIDER_BUSINESS_IDENTITY
    provider_former_brand: str = PROVIDER_FORMER_BRAND
    provider_plan_category: str = STOCKS_STARTER
    entitlement_evidence: str = OPERATOR_ATTESTED
    historical_years_available: str = FIVE_YEARS
    intraday_aggregate_access: str = INTRADAY_AND_DAILY_AVAILABLE
    daily_aggregate_access: str = INTRADAY_AND_DAILY_AVAILABLE
    delayed_or_realtime_classification: str = FIFTEEN_MINUTE_DELAYED
    confirmation_date: str = HUMAN_APPROVAL_REQUIRED

    def validate(self) -> None:
        if self.confirmation_status != OPERATOR_ATTESTED_CONFIRMED:
            raise ContractValidationError("provider entitlement must be operator-attested confirmed")
        if self.provider_current_brand != PROVIDER_BUSINESS_IDENTITY:
            raise ContractValidationError("provider current brand must be Massive.com")
        if self.provider_former_brand != PROVIDER_FORMER_BRAND:
            raise ContractValidationError("provider former brand must be Polygon.io")
        if self.provider_plan_category != STOCKS_STARTER:
            raise ContractValidationError("provider plan category must match operator attestation")
        if self.entitlement_evidence != OPERATOR_ATTESTED:
            raise ContractValidationError("provider entitlement evidence must be operator attested")
        if self.historical_years_available != FIVE_YEARS:
            raise ContractValidationError("historical entitlement must match operator attestation")
        if self.intraday_aggregate_access != INTRADAY_AND_DAILY_AVAILABLE:
            raise ContractValidationError("intraday aggregate access must match operator attestation")
        if self.daily_aggregate_access != INTRADAY_AND_DAILY_AVAILABLE:
            raise ContractValidationError("daily aggregate access must match operator attestation")
        if self.delayed_or_realtime_classification != FIFTEEN_MINUTE_DELAYED:
            raise ContractValidationError("data recency must match operator attestation")


@dataclass(frozen=True, slots=True)
class ProviderRequestContract:
    provider_identity: str
    endpoint_family: str
    endpoint_contract_version: str
    asset_class: str
    ticker: str
    multiplier: int
    timespan: str
    start_date: str
    end_date: str
    start_date_status: str
    end_date_status: str
    adjusted: bool
    sort: str
    base_aggregate_limit: int
    maximum_supported_limit: int
    pagination_policy_status: str
    requested_session_policy: str
    source_aggregation_timezone: str
    canonical_storage_timezone: str
    expected_response_schema: str
    provider_entitlement_status: str

    def validate(self) -> None:
        if self.provider_identity != PROVIDER_IDENTITY:
            raise ContractValidationError("provider identity mismatch")
        if self.endpoint_family != ENDPOINT_FAMILY:
            raise ContractValidationError("endpoint family mismatch")
        if self.endpoint_contract_version != ENDPOINT_CONTRACT_VERSION:
            raise ContractValidationError("endpoint contract version mismatch")
        if self.asset_class != ASSET_CLASS_US_EQUITY:
            raise ContractValidationError("asset class mismatch")
        if self.ticker != HUMAN_APPROVAL_REQUIRED and not re.match(r"^[A-Z][A-Z0-9._-]{0,14}$", self.ticker):
            raise ContractValidationError("ticker must be exact and non-operational in the example")
        if self.multiplier <= 0:
            raise ContractValidationError("multiplier must be positive")
        if self.timespan not in {"hour", "day"}:
            raise ContractValidationError("timespan must be hour or day for accepted profiles")
        _validate_date_value(self.start_date, self.start_date_status, "start_date")
        _validate_date_value(self.end_date, self.end_date_status, "end_date")
        if self.start_date_status != HUMAN_APPROVAL_REQUIRED and self.end_date_status != HUMAN_APPROVAL_REQUIRED:
            if _parse_approved_date(self.start_date, "start_date") >= _parse_approved_date(self.end_date, "end_date"):
                raise ContractValidationError("start_date must be strictly before end_date")
        if self.adjusted is not True:
            raise ContractValidationError("future requests must explicitly use adjusted=true")
        if self.sort != "asc":
            raise ContractValidationError("sort must be asc")
        if self.base_aggregate_limit <= 0 or self.base_aggregate_limit > self.maximum_supported_limit:
            raise ContractValidationError("base aggregate limit is invalid")
        if self.maximum_supported_limit != 50000:
            raise ContractValidationError("maximum supported base-aggregate limit must be explicit")
        if self.pagination_policy_status != NOT_APPROVED:
            raise ContractValidationError("provider request pagination policy must remain not approved")
        _require_enum(self.requested_session_policy, SESSION_POLICIES, "requested_session_policy")
        if self.requested_session_policy != SESSION_POLICY_NOT_CONFIRMED:
            raise ContractValidationError("provider request session policy must remain not confirmed")
        if self.source_aggregation_timezone != SOURCE_AGGREGATION_TIMEZONE:
            raise ContractValidationError("source aggregation timezone must be explicit")
        if self.canonical_storage_timezone != CANONICAL_STORAGE_TIMEZONE:
            raise ContractValidationError("canonical storage timezone must be UTC")
        if self.provider_entitlement_status != OPERATOR_ATTESTED_CONFIRMED:
            raise ContractValidationError("provider entitlement status must be operator-attested confirmed")


@dataclass(frozen=True, slots=True)
class ProfileAcquisitionRequirement:
    profile_id: str
    canonical_timeframe: str
    minimum_valid_ohlcv_rows: int
    acquisition_date_range_status: str
    bar_construction_policy: str
    bar_construction_status: str
    session_policy: str
    session_policy_status: str
    multiplier: int
    timespan: str

    def validate(self) -> None:
        if self.profile_id == PROFILE_SWING:
            if (
                self.canonical_timeframe != TIMEFRAME_SWING
                or self.minimum_valid_ohlcv_rows != MINIMUM_ROWS_SWING
                or self.multiplier != 4
                or self.timespan != "hour"
            ):
                raise ContractValidationError("SWING acquisition requirements changed")
            if self.bar_construction_policy == BAR_PROVIDER_NATIVE_CLOCK_4H and self.bar_construction_status != NOT_APPROVED:
                raise ContractValidationError("provider-native 4h cannot be silently approved")
        elif self.profile_id == PROFILE_POSITION_SWING:
            if (
                self.canonical_timeframe != TIMEFRAME_POSITION_SWING
                or self.minimum_valid_ohlcv_rows != MINIMUM_ROWS_POSITION_SWING
                or self.multiplier != 1
                or self.timespan != "day"
            ):
                raise ContractValidationError("POSITION_SWING acquisition requirements changed")
        else:
            raise ContractValidationError("unsupported profile")
        if self.acquisition_date_range_status != NOT_SET:
            raise ContractValidationError("profile date range must remain NOT_SET")
        _require_enum(self.bar_construction_policy, BAR_CONSTRUCTION_POLICIES, "bar_construction_policy")
        _require_enum(self.session_policy, SESSION_POLICIES, "session_policy")
        if self.bar_construction_status != NOT_APPROVED:
            raise ContractValidationError("bar construction must remain not approved")
        if self.session_policy_status != NOT_APPROVED:
            raise ContractValidationError("session policy must not be silently approved")


@dataclass(frozen=True, slots=True)
class AdjustmentPolicy:
    split_adjusted_requested: bool = True
    provider_adjusted_response: str = MUST_MATCH_REQUEST
    dividend_adjusted: bool = False
    corporate_action_metadata_status: str = NOT_CONFIRMED
    adjustment_provenance_status: str = CONTRACT_PROPOSED
    adjustment_policy_status: str = NOT_APPROVED

    def validate(self) -> None:
        if self.split_adjusted_requested is not True:
            raise ContractValidationError("split adjustment request must be explicit")
        if self.provider_adjusted_response != MUST_MATCH_REQUEST:
            raise ContractValidationError("provider adjusted response must match request")
        if self.dividend_adjusted is not False:
            raise ContractValidationError("dividend-adjusted claim is not approved")
        if self.corporate_action_metadata_status != NOT_CONFIRMED:
            raise ContractValidationError("corporate-action metadata is not confirmed")
        if self.adjustment_provenance_status != CONTRACT_PROPOSED:
            raise ContractValidationError("adjustment provenance must remain proposed")
        if self.adjustment_policy_status != NOT_APPROVED:
            raise ContractValidationError("adjustment policy must remain not approved")


@dataclass(frozen=True, slots=True)
class TimezonePolicy:
    source_aggregation_timezone: str = SOURCE_AGGREGATION_TIMEZONE
    canonical_storage_timezone: str = CANONICAL_STORAGE_TIMEZONE
    original_provider_timestamps: str = "PRESERVE_PROVIDER_EPOCH_TIMESTAMPS"
    source_local_timezone_metadata: str = "RECORD_FOR_DIAGNOSTICS"
    dst_conversion_policy: str = "EPOCH_TO_UTC_FIRST_THEN_SOURCE_LOCAL_DIAGNOSTICS"
    naive_canonical_timestamps_allowed: bool = False
    timezone_policy_status: str = NOT_APPROVED

    def validate(self) -> None:
        if self.source_aggregation_timezone != SOURCE_AGGREGATION_TIMEZONE:
            raise ContractValidationError("source aggregation timezone must be explicit")
        if self.canonical_storage_timezone != CANONICAL_STORAGE_TIMEZONE:
            raise ContractValidationError("canonical stored timezone must be UTC")
        if self.original_provider_timestamps != "PRESERVE_PROVIDER_EPOCH_TIMESTAMPS":
            raise ContractValidationError("provider epoch timestamp preservation must remain explicit")
        if self.source_local_timezone_metadata != "RECORD_FOR_DIAGNOSTICS":
            raise ContractValidationError("source-local timezone metadata must remain diagnostic only")
        if self.dst_conversion_policy != "EPOCH_TO_UTC_FIRST_THEN_SOURCE_LOCAL_DIAGNOSTICS":
            raise ContractValidationError("DST conversion policy must remain epoch-to-UTC first")
        if self.naive_canonical_timestamps_allowed is not False:
            raise ContractValidationError("naive canonical timestamps are prohibited")
        if self.timezone_policy_status != NOT_APPROVED:
            raise ContractValidationError("timezone policy must remain not approved")


@dataclass(frozen=True, slots=True)
class PaginationCompletenessPolicy:
    base_aggregate_limit: int = 50000
    maximum_supported_limit: int = 50000
    request_chunk_boundaries: str = HUMAN_APPROVAL_REQUIRED
    iterator_exhaustion_required: bool = True
    duplicate_boundary_handling: str = "REJECT_DUPLICATE_BOUNDARY_ROWS"
    response_count_validation: str = "VALIDATE_WHERE_MEANINGFUL"
    partial_result_acceptance: bool = False
    pagination_policy_status: str = NOT_APPROVED

    def validate(self) -> None:
        if self.base_aggregate_limit <= 0 or self.base_aggregate_limit > self.maximum_supported_limit:
            raise ContractValidationError("invalid pagination limit")
        if self.iterator_exhaustion_required is not True:
            raise ContractValidationError("iterator exhaustion is required")
        if self.partial_result_acceptance is not False:
            raise ContractValidationError("partial result acceptance is prohibited")
        if self.pagination_policy_status != NOT_APPROVED:
            raise ContractValidationError("pagination policy must remain not approved")


@dataclass(frozen=True, slots=True)
class ArtifactProvenanceDesign:
    lineage_design_status: str = CONTRACT_PROPOSED
    artifact_chain: tuple[str, ...] = (
        ACQUISITION_REQUEST_CONTRACT,
        RAW_PROVIDER_RESPONSE,
        NORMALIZED_OHLCV_DATASET,
        ANNOTATED_DATASET,
    )
    raw_response_retention: str = "PRESERVE_EXACT_PROVIDER_RESPONSE_BYTES_WHERE_PERMITTED"
    normalized_dataset_timezone: str = CANONICAL_STORAGE_TIMEZONE
    credential_storage_allowed: bool = False
    absolute_path_storage_allowed: bool = False

    def validate(self) -> None:
        if self.artifact_chain != (
            ACQUISITION_REQUEST_CONTRACT,
            RAW_PROVIDER_RESPONSE,
            NORMALIZED_OHLCV_DATASET,
            ANNOTATED_DATASET,
        ):
            raise ContractValidationError("artifact lineage chain changed")
        if self.credential_storage_allowed or self.absolute_path_storage_allowed:
            raise ContractValidationError("provenance must not store credentials or absolute paths")


@dataclass(frozen=True, slots=True)
class FixedDateAcquisitionContract:
    contract_version: str
    readiness_status: str
    acquisition_enabled: bool
    provider_entitlement: ProviderEntitlement
    provider_request: ProviderRequestContract
    profiles: tuple[ProfileAcquisitionRequirement, ...]
    adjustment_policy: AdjustmentPolicy
    timezone_policy: TimezonePolicy
    pagination_policy: PaginationCompletenessPolicy
    artifact_provenance: ArtifactProvenanceDesign
    blockers: tuple[str, ...] = field(default_factory=tuple)

    def validate(self) -> None:
        if self.contract_version != CONTRACT_VERSION:
            raise ContractValidationError("contract version mismatch")
        _require_enum(self.readiness_status, READINESS_STATUSES, "readiness_status")
        if self.acquisition_enabled is not False:
            raise ContractValidationError("acquisition must remain disabled")
        if self.readiness_status == ACQUISITION_CONTRACT_FROZEN:
            raise ContractValidationError("this task cannot freeze the contract")
        self.provider_entitlement.validate()
        self.provider_request.validate()
        self.adjustment_policy.validate()
        self.timezone_policy.validate()
        self.pagination_policy.validate()
        self.artifact_provenance.validate()
        profile_ids = tuple(profile.profile_id for profile in self.profiles)
        if profile_ids != (PROFILE_SWING, PROFILE_POSITION_SWING):
            raise ContractValidationError("profiles must be SWING then POSITION_SWING")
        for profile in self.profiles:
            profile.validate()
        expected_blockers = (
            FIXED_DATES_NOT_APPROVED,
            BAR_CONSTRUCTION_NOT_APPROVED,
            SESSION_POLICY_NOT_APPROVED,
            ADJUSTMENT_POLICY_NOT_APPROVED,
            PAGINATION_POLICY_NOT_APPROVED,
        )
        if self.blockers != expected_blockers:
            raise ContractValidationError("required blockers must remain explicit and exact")
        if FIXED_DATES_NOT_APPROVED in self.blockers and (
            self.provider_request.start_date_status != HUMAN_APPROVAL_REQUIRED
            or self.provider_request.end_date_status != HUMAN_APPROVAL_REQUIRED
            or self.provider_request.start_date != HUMAN_APPROVAL_REQUIRED
            or self.provider_request.end_date != HUMAN_APPROVAL_REQUIRED
        ):
            raise ContractValidationError("fixed dates cannot be approved while date blocker remains")
        if self.readiness_status != ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS:
            raise ContractValidationError("proposed contract must remain with blockers")


SESSION_POLICIES = {
    SESSION_REGULAR_TRADING_HOURS_ONLY,
    SESSION_EXTENDED_HOURS_INCLUDED,
    SESSION_PROVIDER_DEFAULT,
    SESSION_POLICY_NOT_CONFIRMED,
}
BAR_CONSTRUCTION_POLICIES = {
    BAR_PROVIDER_NATIVE_CLOCK_4H,
    BAR_DETERMINISTIC_LOCAL_AGGREGATION,
    BAR_CONSTRUCTION_NOT_CONFIRMED,
    BAR_PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW,
}
READINESS_STATUSES = {
    ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS,
    ACQUISITION_CONTRACT_READY_FOR_APPROVAL,
    ACQUISITION_CONTRACT_FROZEN,
}


def default_proposed_contract() -> FixedDateAcquisitionContract:
    """Return the safe non-operational proposed contract."""
    return FixedDateAcquisitionContract(
        contract_version=CONTRACT_VERSION,
        readiness_status=ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS,
        acquisition_enabled=False,
        provider_entitlement=ProviderEntitlement(),
        provider_request=ProviderRequestContract(
            provider_identity=PROVIDER_IDENTITY,
            endpoint_family=ENDPOINT_FAMILY,
            endpoint_contract_version=ENDPOINT_CONTRACT_VERSION,
            asset_class=ASSET_CLASS_US_EQUITY,
            ticker=HUMAN_APPROVAL_REQUIRED,
            multiplier=4,
            timespan="hour",
            start_date=HUMAN_APPROVAL_REQUIRED,
            end_date=HUMAN_APPROVAL_REQUIRED,
            start_date_status=HUMAN_APPROVAL_REQUIRED,
            end_date_status=HUMAN_APPROVAL_REQUIRED,
            adjusted=True,
            sort="asc",
            base_aggregate_limit=50000,
            maximum_supported_limit=50000,
            pagination_policy_status=NOT_APPROVED,
            requested_session_policy=SESSION_POLICY_NOT_CONFIRMED,
            source_aggregation_timezone=SOURCE_AGGREGATION_TIMEZONE,
            canonical_storage_timezone=CANONICAL_STORAGE_TIMEZONE,
            expected_response_schema="POLYGON_AGGS_V2_RESULTS_WITH_REQUEST_METADATA",
            provider_entitlement_status=OPERATOR_ATTESTED_CONFIRMED,
        ),
        profiles=(
            ProfileAcquisitionRequirement(
                profile_id=PROFILE_SWING,
                canonical_timeframe=TIMEFRAME_SWING,
                minimum_valid_ohlcv_rows=MINIMUM_ROWS_SWING,
                acquisition_date_range_status=NOT_SET,
                bar_construction_policy=BAR_CONSTRUCTION_NOT_CONFIRMED,
                bar_construction_status=NOT_APPROVED,
                session_policy=SESSION_POLICY_NOT_CONFIRMED,
                session_policy_status=NOT_APPROVED,
                multiplier=4,
                timespan="hour",
            ),
            ProfileAcquisitionRequirement(
                profile_id=PROFILE_POSITION_SWING,
                canonical_timeframe=TIMEFRAME_POSITION_SWING,
                minimum_valid_ohlcv_rows=MINIMUM_ROWS_POSITION_SWING,
                acquisition_date_range_status=NOT_SET,
                bar_construction_policy=BAR_PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW,
                bar_construction_status=NOT_APPROVED,
                session_policy=SESSION_POLICY_NOT_CONFIRMED,
                session_policy_status=NOT_APPROVED,
                multiplier=1,
                timespan="day",
            ),
        ),
        adjustment_policy=AdjustmentPolicy(),
        timezone_policy=TimezonePolicy(),
        pagination_policy=PaginationCompletenessPolicy(),
        artifact_provenance=ArtifactProvenanceDesign(),
        blockers=(
            FIXED_DATES_NOT_APPROVED,
            BAR_CONSTRUCTION_NOT_APPROVED,
            SESSION_POLICY_NOT_APPROVED,
            ADJUSTMENT_POLICY_NOT_APPROVED,
            PAGINATION_POLICY_NOT_APPROVED,
        ),
    )


def _construct_dataclass(cls: type[Any], payload: dict[str, Any]) -> Any:
    field_names = set(cls.__dataclass_fields__)
    keys = set(payload)
    missing = {name for name in field_names if name not in payload}
    unknown = keys - field_names
    if missing:
        raise ContractValidationError(f"{cls.__name__} missing fields: {sorted(missing)}")
    if unknown:
        raise ContractValidationError(f"{cls.__name__} unknown fields: {sorted(unknown)}")
    if cls is ArtifactProvenanceDesign and isinstance(payload.get("artifact_chain"), list):
        payload = dict(payload)
        payload["artifact_chain"] = tuple(payload["artifact_chain"])
    return cls(**payload)


def contract_from_dict(payload: dict[str, Any]) -> FixedDateAcquisitionContract:
    """Build a strict contract from a JSON/TOML-like dictionary."""
    _reject_operational_field_names(payload)
    expected = set(FixedDateAcquisitionContract.__dataclass_fields__)
    unknown = set(payload) - expected
    missing = expected - set(payload)
    if unknown:
        raise ContractValidationError(f"contract unknown fields: {sorted(unknown)}")
    if missing:
        raise ContractValidationError(f"contract missing fields: {sorted(missing)}")
    profiles = payload["profiles"]
    if not isinstance(profiles, list):
        raise ContractValidationError("profiles must be a list")
    contract = FixedDateAcquisitionContract(
        contract_version=payload["contract_version"],
        readiness_status=payload["readiness_status"],
        acquisition_enabled=payload["acquisition_enabled"],
        provider_entitlement=_construct_dataclass(ProviderEntitlement, payload["provider_entitlement"]),
        provider_request=_construct_dataclass(ProviderRequestContract, payload["provider_request"]),
        profiles=tuple(_construct_dataclass(ProfileAcquisitionRequirement, profile) for profile in profiles),
        adjustment_policy=_construct_dataclass(AdjustmentPolicy, payload["adjustment_policy"]),
        timezone_policy=_construct_dataclass(TimezonePolicy, payload["timezone_policy"]),
        pagination_policy=_construct_dataclass(PaginationCompletenessPolicy, payload["pagination_policy"]),
        artifact_provenance=_construct_dataclass(ArtifactProvenanceDesign, payload["artifact_provenance"]),
        blockers=tuple(payload["blockers"]),
    )
    contract.validate()
    return contract


def load_contract_toml(path: str | Path) -> FixedDateAcquisitionContract:
    """Load a strict offline contract TOML file."""
    with Path(path).open("rb") as handle:
        payload = tomllib.load(handle)
    return contract_from_dict(payload)


def readiness_receipt(contract: FixedDateAcquisitionContract) -> dict[str, Any]:
    """Return a sanitized acquisition-readiness receipt."""
    contract.validate()
    profile_map = {profile.profile_id: profile for profile in contract.profiles}
    swing = profile_map[PROFILE_SWING]
    position = profile_map[PROFILE_POSITION_SWING]
    return {
        "status": contract.readiness_status,
        "contract_version": contract.contract_version,
        "provider_identity": contract.provider_request.provider_identity,
        "provider_business_identity": contract.provider_entitlement.provider_current_brand,
        "provider_legacy_adapter_identity": contract.provider_entitlement.provider_former_brand,
        "provider_entitlement_status": contract.provider_request.provider_entitlement_status,
        "provider_entitlement_confirmed": True,
        "provider_plan_category": contract.provider_entitlement.provider_plan_category,
        "provider_entitlement_evidence": contract.provider_entitlement.entitlement_evidence,
        "provider_historical_entitlement": contract.provider_entitlement.historical_years_available,
        "provider_data_recency": contract.provider_entitlement.delayed_or_realtime_classification,
        "provider_aggregate_access": contract.provider_entitlement.intraday_aggregate_access,
        "SWING_timeframe": swing.canonical_timeframe,
        "SWING_minimum_rows": swing.minimum_valid_ohlcv_rows,
        "SWING_date_status": swing.acquisition_date_range_status,
        "SWING_bar_construction_status": swing.bar_construction_status,
        "SWING_session_status": swing.session_policy_status,
        "POSITION_SWING_timeframe": position.canonical_timeframe,
        "POSITION_SWING_minimum_rows": position.minimum_valid_ohlcv_rows,
        "POSITION_SWING_date_status": position.acquisition_date_range_status,
        "POSITION_SWING_bar_construction_status": position.bar_construction_status,
        "POSITION_SWING_session_status": position.session_policy_status,
        "adjustment_policy_status": contract.adjustment_policy.adjustment_policy_status,
        "timezone_policy_status": contract.timezone_policy.timezone_policy_status,
        "pagination_completeness_status": contract.pagination_policy.pagination_policy_status,
        "artifact_lineage_design_status": contract.artifact_provenance.lineage_design_status,
        "contract_digest": contract_digest(contract),
        "acquisition_enabled": False,
        "blockers": list(contract.blockers),
    }


def validate_provider_adjusted_metadata(contract: FixedDateAcquisitionContract, adjusted: bool) -> None:
    if adjusted is not contract.adjustment_policy.split_adjusted_requested:
        raise ContractValidationError("provider adjusted response does not match request")


def _finite_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise ContractValidationError(f"{field_name} must be numeric")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ContractValidationError(f"{field_name} must be numeric") from exc
    if not math.isfinite(number):
        raise ContractValidationError(f"{field_name} must be finite")
    return number


def validate_fake_provider_response(contract: FixedDateAcquisitionContract, response: dict[str, Any]) -> str:
    """Validate a synthetic provider response against the contract."""
    contract.validate()
    required = {"status", "ticker", "adjusted", "results"}
    if set(response) - required:
        raise ContractValidationError("unknown provider response shape")
    if not required.issubset(response):
        raise ContractValidationError("missing provider response fields")
    if response["status"] != "OK":
        raise ContractValidationError("provider response status is not OK")
    if contract.provider_request.ticker != HUMAN_APPROVAL_REQUIRED and response["ticker"] != contract.provider_request.ticker:
        raise ContractValidationError("provider response ticker mismatch")
    if not isinstance(response["adjusted"], bool):
        raise ContractValidationError("provider adjusted response must be a boolean")
    validate_provider_adjusted_metadata(contract, response["adjusted"])
    start_bound: date | None = None
    end_bound: date | None = None
    if (
        contract.provider_request.start_date_status != HUMAN_APPROVAL_REQUIRED
        and contract.provider_request.end_date_status != HUMAN_APPROVAL_REQUIRED
    ):
        start_bound = _parse_approved_date(contract.provider_request.start_date, "start_date")
        end_bound = _parse_approved_date(contract.provider_request.end_date, "end_date")
    previous_timestamp: str | None = None
    seen: set[str] = set()
    if not isinstance(response["results"], list) or not response["results"]:
        raise ContractValidationError("response results must be a non-empty list")
    for row in response["results"]:
        if set(row) != {"timestamp_utc", "open", "high", "low", "close", "volume", "completed"}:
            raise ContractValidationError("unknown result shape")
        parsed_utc = _parse_utc_instant(row["timestamp_utc"], "canonical timestamp")
        if start_bound is not None and end_bound is not None and not (start_bound <= parsed_utc.date() <= end_bound):
            raise ContractValidationError("response timestamp is outside approved fixed date range")
        normalized_timestamp = parsed_utc.isoformat()
        if previous_timestamp is not None and normalized_timestamp <= previous_timestamp:
            raise ContractValidationError("response timestamps must be strictly ascending")
        if normalized_timestamp in seen:
            raise ContractValidationError("duplicate response timestamp")
        seen.add(normalized_timestamp)
        previous_timestamp = normalized_timestamp
        high = _finite_number(row["high"], "high")
        low = _finite_number(row["low"], "low")
        _finite_number(row["open"], "open")
        _finite_number(row["close"], "close")
        volume = _finite_number(row["volume"], "volume")
        if high < low:
            raise ContractValidationError("high must be greater than or equal to low")
        if volume < 0:
            raise ContractValidationError("volume must be nonnegative")
        if row["completed"] is not True:
            raise ContractValidationError("partial final bars are rejected")
    return REQUEST_COMPLETE


def validate_pagination_sequence(pages: list[dict[str, Any]], expected_first: str, expected_last: str) -> str:
    """Validate a deterministic fake pagination sequence."""
    if not pages:
        return PAGINATION_INCOMPLETE
    try:
        expected_first_instant = _parse_utc_instant(expected_first, "expected_first")
        expected_last_instant = _parse_utc_instant(expected_last, "expected_last")
    except (ContractValidationError, ValueError):
        return PROVIDER_RESPONSE_INVALID
    seen_pages: set[str] = set()
    timestamps: list[datetime] = []
    previous_page_id: str | None = None
    for page in pages:
        if set(page) != {"page_id", "results", "has_more", "expected_count"}:
            return PROVIDER_RESPONSE_INVALID
        page_id = str(page["page_id"])
        if page_id in seen_pages:
            return PAGE_DUPLICATE
        seen_pages.add(page_id)
        results = page["results"]
        if not isinstance(results, list) or len(results) != int(page["expected_count"]):
            return REQUEST_TRUNCATED
        for timestamp in results:
            try:
                instant = _parse_utc_instant(timestamp, "page timestamp")
            except (ContractValidationError, ValueError):
                return PROVIDER_RESPONSE_INVALID
            if timestamps and instant <= timestamps[-1]:
                return PAGE_DUPLICATE if instant == timestamps[-1] else PROVIDER_RESPONSE_INVALID
            timestamps.append(instant)
        previous_page_id = page_id
    if previous_page_id is None or pages[-1]["has_more"] is True:
        return PAGINATION_INCOMPLETE
    if not timestamps or timestamps[0] != expected_first_instant or timestamps[-1] != expected_last_instant:
        return RANGE_COVERAGE_INCOMPLETE
    return REQUEST_COMPLETE


def artifact_relationship_metadata(
    *,
    raw_response_bytes: bytes,
    normalized_rows: list[dict[str, Any]],
    request_contract: FixedDateAcquisitionContract,
    code_commit: str,
    client_package_version: str,
) -> dict[str, Any]:
    """Return sanitized raw/normalized provenance metadata without writing artifacts."""
    if not re.match(r"^[0-9a-f]{7,40}$", code_commit):
        raise ContractValidationError("code_commit must be a sanitized git hex id")
    client_text = str(client_package_version)
    if (
        any(fragment in client_text.lower() for fragment in CREDENTIAL_FRAGMENTS)
        or "://" in client_text
        or ":\\" in client_text
        or client_text.startswith(("/", "\\", "~"))
        or "\x00" in client_text
    ):
        raise ContractValidationError("client_package_version must be sanitized")
    raw_digest = hashlib.sha256(raw_response_bytes).hexdigest()
    normalized_digest = contract_digest(normalized_rows)
    return {
        "provider_identity": request_contract.provider_request.provider_identity,
        "provider_endpoint_family": request_contract.provider_request.endpoint_family,
        "provider_request_contract_digest": contract_digest(request_contract),
        "exact_ticker": request_contract.provider_request.ticker,
        "fixed_start_date_status": request_contract.provider_request.start_date_status,
        "fixed_end_date_status": request_contract.provider_request.end_date_status,
        "multiplier": request_contract.provider_request.multiplier,
        "timespan": request_contract.provider_request.timespan,
        "session_policy": request_contract.provider_request.requested_session_policy,
        "source_timezone": request_contract.provider_request.source_aggregation_timezone,
        "canonical_timezone": request_contract.provider_request.canonical_storage_timezone,
        "adjusted_request": request_contract.provider_request.adjusted,
        "adjusted_response_policy": request_contract.adjustment_policy.provider_adjusted_response,
        "client_package_version": client_text,
        "pagination_chunk_completeness": request_contract.pagination_policy.pagination_policy_status,
        "raw_response_digest": raw_digest,
        "normalized_dataset_digest": normalized_digest,
        "parent_relationship": f"{RAW_PROVIDER_RESPONSE}->{NORMALIZED_OHLCV_DATASET}",
        "row_count": len(normalized_rows),
        "corporate_action_provenance_status": request_contract.adjustment_policy.corporate_action_metadata_status,
        "code_commit": code_commit,
    }


def _example_path() -> Path:
    return Path(__file__).resolve().parents[2] / "config" / "fixed_date_acquisition_contract.example.toml"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m marketflow.research.fixed_date_acquisition_contract",
        description="Validate the offline fixed-date acquisition contract example.",
    )
    parser.parse_args(argv)
    contract = load_contract_toml(_example_path())
    print(json.dumps(readiness_receipt(contract), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
