from __future__ import annotations

import ast
import dataclasses
import json
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from marketflow.research import acquisition_contract_v2 as acv2
from marketflow.research import fixed_date_acquisition_contract as fdac


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG = REPO_ROOT / "config" / "fixed_date_acquisition_contract_v2.toml"
V1_CONFIG = REPO_ROOT / "config" / "fixed_date_acquisition_contract.example.toml"
MODULE = REPO_ROOT / "marketflow" / "research" / "acquisition_contract_v2.py"
V1_DIGEST = "29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e"


def _payload() -> dict:
    with CONFIG.open("rb") as handle:
        return tomllib.load(handle)


def _contract() -> acv2.AcquisitionContractV2:
    return acv2.load_contract_toml(CONFIG)


def test_v2_contract_loads_with_ready_status_and_disabled_execution():
    contract = _contract()
    receipt = acv2.readiness_receipt(contract)
    rendered = json.dumps(receipt, sort_keys=True)

    assert contract.contract_schema_version == acv2.CONTRACT_SCHEMA_VERSION
    assert contract.contract_status == acv2.CONTRACT_STATUS_READY
    assert contract.human_decisions_status == acv2.HUMAN_DECISIONS_COMPLETE
    assert contract.acquisition_enabled is False
    assert contract.provider_execution_enabled is False
    assert contract.calendar_generation_enabled is False
    assert contract.normalization_enabled is False
    assert contract.registry_authority_enabled is False
    assert contract.runtime_profile_migration_status == "LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION"
    assert receipt["readiness_note"] == "DECLARATIVE_OFFLINE_ONLY_NO_ACQUISITION"
    assert "api_key" not in rendered.lower()
    assert ":\\" not in rendered


def test_provider_identity_uses_massive_business_brand_and_legacy_polygon_adapter():
    provider = _contract().provider_policy

    assert provider.business_provider == "MASSIVE.COM"
    assert provider.former_brand == "POLYGON.IO"
    assert provider.installed_adapter_family == "polygon-api-client"
    assert provider.installed_adapter_version == "1.14.6"
    assert provider.subscription_plan == "STOCKS_STARTER"
    assert provider.entitlement_evidence == "OPERATOR_ATTESTED"
    assert provider.provider_entitlement_status == "OPERATOR_ATTESTED_CONFIRMED"
    assert provider.historical_access == "FIVE_YEARS"
    assert provider.market_data_recency == "FIFTEEN_MINUTE_DELAYED"
    assert provider.aggregate_access == "INTRADAY_AND_DAILY_AVAILABLE"
    assert provider.entitlement_api_verified is False
    assert provider.provider_execution_enabled is False
    assert provider.sdk_migration_status == "NOT_PERFORMED"


def test_fixed_date_range_is_exact_and_rejects_relative_or_moving_dates():
    policy = _contract().fixed_range_policy

    assert policy.start_date == "2022-01-01"
    assert policy.end_date == "2025-12-31"
    assert policy.common_range_for_all_profiles is True
    assert policy.rolling_window_allowed is False
    assert policy.current_date_dependency_allowed is False

    for bad_value in ("today", "now", "365d", "5y", "2022/01/01"):
        with pytest.raises(acv2.ContractV2ValidationError):
            dataclasses.replace(policy, start_date=bad_value).validate()
    with pytest.raises(acv2.ContractV2ValidationError):
        dataclasses.replace(policy, end_date="2022-01-01").validate()


def test_source_bars_and_profiles_encode_15m_regular_session_policy():
    contract = _contract()
    profiles = {profile.profile_id: profile for profile in contract.profiles}

    assert contract.source_bar_policy.provider_source_interval == "15m"
    assert contract.source_bar_policy.provider_multiplier == 15
    assert contract.source_bar_policy.provider_native_4h_canonical is False
    assert contract.source_bar_policy.provider_native_1d_canonical is False
    assert contract.source_bar_policy.extended_hours_in_derived_datasets == "EXCLUDED"
    assert profiles["SWING"].profile_contract_version == "SWING_RTH_HALF_SESSION_V1"
    assert profiles["SWING"].canonical_bar_type == "RTH_HALF_SESSION_195M"
    assert profiles["SWING"].minimum_valid_rows == 390
    assert profiles["SWING"].source_bars_per_canonical_bar == 13
    assert profiles["SWING"].timestamp_semantic == "BAR_CLOSE_TIMESTAMP"
    assert [window.label for window in profiles["SWING"].window_segments] == ["MORNING_4H", "AFTERNOON_4H"]
    assert profiles["POSITION_SWING"].profile_contract_version == "POSITION_SWING_RTH_FULL_SESSION_V1"
    assert profiles["POSITION_SWING"].canonical_bar_type == "RTH_FULL_SESSION_1D"
    assert profiles["POSITION_SWING"].minimum_valid_rows == 560
    assert profiles["POSITION_SWING"].source_bars_per_canonical_bar == 26
    assert profiles["POSITION_SWING"].timestamp_semantic == "SESSION_CLOSE_TIMESTAMP"
    assert profiles["POSITION_SWING"].window_segments[0].label == "FULL_RTH_DAY"


def test_profile_mutations_fail_closed():
    swing = _contract().profiles[0]

    for mutation in (
        {"minimum_valid_rows": 389},
        {"source_bars_per_canonical_bar": 12},
        {"session_policy": "PROVIDER_DEFAULT_SESSION"},
        {"early_close_policy": "INCLUDE_PARTIAL_SESSION"},
        {"higher_timeframe_context": "1d"},
        {"timestamp_semantic": "SESSION_OPEN_TIMESTAMP"},
    ):
        with pytest.raises(acv2.ContractV2ValidationError):
            dataclasses.replace(swing, **mutation).validate()


def test_aggregation_calendar_identity_and_corporate_action_policy_are_strict():
    contract = _contract()

    contract.aggregation_policy.validate()
    contract.calendar_policy.validate()
    contract.instrument_identity_policy.validate()
    contract.corporate_action_policy.validate()
    assert contract.aggregation_policy.provider_native_higher_timeframe_acceptance == "PROHIBITED"
    assert contract.calendar_policy.calendar_package == "exchange_calendars"
    assert contract.calendar_policy.calendar_package_version == "4.13.2"
    assert contract.calendar_policy.early_close_sessions == "EXCLUDED"
    assert contract.calendar_policy.requested_listing_mic_retention == "RETAIN_SEPARATELY_FROM_RESOLVED_CALENDAR"
    assert contract.calendar_policy.calendar_artifact_not_package_version is True
    assert contract.instrument_identity_policy.identity_source == "MASSIVE_POINT_IN_TIME_TICKER_OVERVIEW"
    assert contract.instrument_identity_policy.start_identity_snapshot_required is True
    assert contract.instrument_identity_policy.end_identity_snapshot_required is True
    assert contract.instrument_identity_policy.identity_change_segment_policy == "IMMUTABLE_IDENTITY_SEGMENTS"
    assert contract.instrument_identity_policy.automatic_stitching == "PROHIBITED"
    assert contract.corporate_action_policy.adjusted_request is True
    assert contract.corporate_action_policy.adjusted_response == "MUST_MATCH_TRUE"
    assert contract.corporate_action_policy.local_second_split_adjustment == "PROHIBITED"
    assert contract.corporate_action_policy.ex_dividend_policy == "RESET_ANALYTICAL_CONTINUITY_AT_EX_DIVIDEND_DATE"


def test_calendar_status_checks_installed_package_metadata_without_importing_calendar():
    status = acv2.calendar_package_status(_contract())

    assert status["calendar_package"] == "exchange_calendars"
    assert status["calendar_package_version_pin"] == "4.13.2"
    assert isinstance(status["calendar_package_installed"], bool)
    assert "calendar_package_installed_version" in status


def test_retry_constants_and_retry_after_policy_are_exact():
    constants = _contract().technical_constants

    assert constants.provider_maximum_attempts == 3
    assert constants.retry_backoff_seconds == (2, 5)
    assert constants.retry_jitter is False
    assert constants.registry_mutex_wait_seconds == 10
    assert constants.retryable_categories == (
        "TRANSPORT_TIMEOUT",
        "CONNECTION_RESET",
        "HTTP_408",
        "HTTP_429",
        "HTTP_500",
        "HTTP_502",
        "HTTP_503",
        "HTTP_504",
    )
    assert constants.retry_after_effective_wait_policy == "MAX_CONFIGURED_BACKOFF_AND_RETRY_AFTER"
    assert acv2.validate_retry_after_delay(429, 0) == 0
    assert acv2.validate_retry_after_delay(503, 60) == 60
    assert acv2.validate_retry_after_delay(500, None) is None
    assert acv2.effective_retry_wait_seconds(2, 429, 5) == 5
    assert acv2.effective_retry_wait_seconds(5, 429, 2) == 5
    for status_code, retry_after in ((429, -1), (503, 61), (500, 1), (429, "1")):
        with pytest.raises(acv2.ContractV2ValidationError):
            acv2.validate_retry_after_delay(status_code, retry_after)


def test_chunking_semantic_normalization_generation_registry_and_authority_policy_are_exact():
    contract = _contract()

    assert contract.chunking_policy.partition == "FIXED_CALENDAR_MONTH"
    assert contract.chunking_policy.baseline_month_count == 48
    assert contract.chunking_policy.chunk_count_before_identity_clipping == 48
    assert contract.chunking_policy.mandatory_pagination_exhaustion is True
    assert contract.chunking_policy.first_page_only_acceptance == "PROHIBITED"
    assert contract.chunking_policy.exact_provider_bytes_required is True
    assert contract.chunking_policy.accepted_attempt_policy == "ONE_EXPLICITLY_ACCEPTED_ATTEMPT_PER_LOGICAL_PAGE"
    assert contract.chunking_policy.equivalent_retry_selection == "LOWEST_VALID_ATTEMPT_ORDINAL"
    assert contract.chunking_policy.differing_projection_status == "PROVIDER_RESPONSE_VARIANCE"
    assert contract.chunking_policy.completeness_acceptance == "ALL_EXPECTED_SOURCE_SLOTS_PRESENT_AFTER_CALENDAR_JOIN"
    assert contract.semantic_equivalence_policy.semantic_retry_projection == "OHLCV_PLUS_CONTRACTED_AUDIT_FIELDS_V1"
    assert contract.semantic_equivalence_policy.numeric_equivalence == "STRICT_CANONICAL_DECIMAL_VALUE_EQUALITY"
    assert contract.semantic_equivalence_policy.tolerance_allowed is False
    assert contract.semantic_equivalence_policy.optional_presence_sensitive_fields == ("vwap", "transaction_count")
    assert contract.semantic_equivalence_policy.missing_supplemental_value_policy == "NEVER_FABRICATE_ZERO_FILL_OR_FORWARD_FILL"
    assert contract.normalization_policy.monthly_normalized_ohlcv_artifact == "MONTHLY_NORMALIZED_OHLCV"
    assert contract.normalization_policy.monthly_normalized_audit_artifact == "MONTHLY_NORMALIZED_AGGREGATE_AUDIT_FIELDS"
    assert contract.normalization_policy.core_artifact_columns == ("timestamp_utc", "open", "high", "low", "close", "volume")
    assert contract.normalization_policy.identity_segment_consolidation == "EXPLICIT_ORDERED_IDENTITY_SEGMENT_CONSOLIDATION"
    assert contract.normalization_policy.dynamic_strategy_month_scan == "PROHIBITED"
    assert contract.generation_policy.generation_statuses == ("OPEN", "INCOMPLETE", "BLOCKED", "READY_FOR_FREEZE", "PREPARED", "FROZEN")
    assert contract.generation_policy.two_phase_freeze_required is True
    assert contract.generation_policy.provisional_strategy_use == "PROHIBITED"
    assert contract.generation_policy.automatic_freeze_allowed is False
    assert contract.generation_policy.automatic_canonical_approval_allowed is False
    assert contract.registry_policy.approval_granularity == "PROFILE_IDENTITY_SEGMENT_GENERATION"
    assert contract.registry_policy.two_phase_approval_required is True
    assert contract.registry_policy.maximum_active_approval_per_key == 1
    assert contract.registry_policy.newest_generation_promotion == "PROHIBITED"
    assert contract.registry_policy.partial_generation_registration_allowed is False
    assert contract.quarantine_policy.immediate_fail_closed_per_key is True
    assert contract.quarantine_policy.reinstatement_policy == "NEW_APPROVAL_RECORD_ONLY"
    assert contract.quarantine_policy.blocks_candidate_generation is True
    assert contract.authority_storage_policy.immutable_event_file_per_event is True
    assert contract.authority_storage_policy.journal_head_pointer_ordering == "JOURNAL_THEN_HEAD_THEN_POINTER"
    assert contract.authority_storage_policy.startup_auto_repair == "PROHIBITED"
    assert contract.authority_storage_policy.registry_mutex_wait_seconds == 10
    assert contract.authority_audit_policy.explicit_full_audit_command_required is True
    assert contract.authority_audit_policy.authority_changing_effect == "PROHIBITED"
    assert contract.authority_audit_policy.non_atomic_multi_key_classification == "BATCH_NOT_ATOMIC"


def test_canonical_decimal_text_is_strict_and_canonicalizes_negative_zero():
    assert acv2.canonical_decimal_text("1.2300") == "1.23"
    assert acv2.canonical_decimal_text("-0.000") == "0"
    assert acv2.canonical_decimal_text(5) == "5"
    for bad_value in (1.2, float("nan"), float("inf"), True, "NaN", "Infinity"):
        with pytest.raises(acv2.ContractV2ValidationError):
            acv2.canonical_decimal_text(bad_value)


def test_canonical_serialization_and_digest_are_stable_order_invariant_and_sensitive():
    contract = _contract()
    payload = _payload()
    reordered_payload = dict(reversed(list(payload.items())))
    changed = dataclasses.replace(
        contract,
        fixed_range_policy=dataclasses.replace(contract.fixed_range_policy, start_date="2022-01-03"),
    )

    assert acv2.contract_digest(contract) == acv2.contract_digest(acv2.contract_from_dict(reordered_payload))
    assert acv2.canonical_json_bytes(contract) == acv2.canonical_json_bytes(contract)
    assert acv2.contract_digest(changed) != acv2.contract_digest(contract)


def test_loader_rejects_unknown_missing_and_unsafe_operational_fields():
    payload = _payload()
    payload["unknown"] = "value"
    with pytest.raises(acv2.ContractV2ValidationError, match="unknown"):
        acv2.contract_from_dict(payload)

    payload = _payload()
    del payload["provider_policy"]
    with pytest.raises(acv2.ContractV2ValidationError, match="missing"):
        acv2.contract_from_dict(payload)

    for dotted_field in ("api_key", "download_url", "output_path", "ticker"):
        payload = _payload()
        payload[dotted_field] = "unsafe"
        with pytest.raises(acv2.ContractV2ValidationError):
            acv2.contract_from_dict(payload)


def test_loader_rejects_any_attempt_to_enable_operational_surfaces():
    payload = _payload()
    payload["acquisition_enabled"] = True
    with pytest.raises(acv2.ContractV2ValidationError):
        acv2.contract_from_dict(payload)

    payload = _payload()
    payload["provider_execution_enabled"] = True
    with pytest.raises(acv2.ContractV2ValidationError):
        acv2.contract_from_dict(payload)

    payload = _payload()
    payload["provider_policy"]["provider_execution_enabled"] = True
    with pytest.raises(acv2.ContractV2ValidationError):
        acv2.contract_from_dict(payload)


def test_loader_accepts_only_direct_repo_config_toml_references(tmp_path: Path):
    assert acv2.load_contract_toml("config/fixed_date_acquisition_contract_v2.toml").contract_status
    assert acv2.load_contract_toml(CONFIG).contract_status

    external = tmp_path / "fixed_date_acquisition_contract_v2.toml"
    external.write_text(CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
    for bad_ref in (
        external,
        "../config/fixed_date_acquisition_contract_v2.toml",
        "config/nested/fixed_date_acquisition_contract_v2.toml",
        "https://example.invalid/contract.toml",
        "$env:CONTRACT",
        "config/fixed_date_acquisition_contract_v2.toml:stream",
    ):
        with pytest.raises(acv2.ContractV2ValidationError):
            acv2.load_contract_toml(bad_ref)


def test_v2_loader_rejects_v1_contract_and_v1_digest_is_unchanged():
    with pytest.raises(acv2.ContractV2ValidationError):
        acv2.load_contract_toml(V1_CONFIG)

    v1_contract = fdac.load_contract_toml(V1_CONFIG)
    assert fdac.contract_digest(v1_contract) == V1_DIGEST
    assert fdac.readiness_receipt(v1_contract)["acquisition_enabled"] is False


def test_cli_outputs_sanitized_receipt_and_rejects_all_operational_args():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.research.acquisition_contract_v2"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["contract_status"] == "ACQUISITION_CONTRACT_V2_READY_FOR_IMPLEMENTATION"
    assert receipt["provider_business_identity"] == "MASSIVE.COM"
    assert receipt["acquisition_enabled"] is False
    assert "api_key" not in result.stdout.lower()
    for flag in ("--ticker", "--start-date", "--end-date", "--api-key", "--enable-acquisition"):
        rejected = subprocess.run(
            [sys.executable, "-m", "marketflow.research.acquisition_contract_v2", flag, "unsafe"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert rejected.returncode != 0


def test_v2_module_has_no_provider_network_candidate_outcome_or_environment_imports():
    source = MODULE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_modules = {
        "polygon",
        "requests",
        "httpx",
        "socket",
        "urllib",
        "yfinance",
        "openai",
        "streamlit",
        "exchange_calendars",
        "marketflow.marketflow_data_provider",
        "marketflow.marketflow_polygon_tools",
        "marketflow.marketflow_strategy",
        "marketflow.services.monte_carlo_service",
        "marketflow.services.backtest_result_service",
        "marketflow.services.walk_forward_validation_service",
    }
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    attrs = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }

    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert "getenv" not in attrs
    assert "environ" not in attrs
    assert "RESTClient" not in calls
    assert {"download", "request", "post", "put", "delete"}.isdisjoint(attrs)


def test_prior_profile_and_artifact_integrity_constants_remain_unchanged():
    from marketflow.marketflow_data_parameters import fixed_analysis_profiles
    from marketflow.operational_artifacts import ARTIFACT_TYPE_ANNOTATED_DATASET
    from marketflow.research.data_readiness_remediation import FIXED_PROFILE_REQUIREMENTS

    profiles = {profile.profile_id: profile for profile in fixed_analysis_profiles()}
    assert profiles["SWING"].candidate_timeframe == "4h"
    assert profiles["SWING"].minimum_valid_rows == 390
    assert profiles["POSITION_SWING"].candidate_timeframe == "1d"
    assert profiles["POSITION_SWING"].minimum_valid_rows == 560
    assert ARTIFACT_TYPE_ANNOTATED_DATASET == "ANNOTATED_DATASET"
    assert FIXED_PROFILE_REQUIREMENTS["SWING"] == {"timeframe": "4h", "required_rows": 390}
    assert FIXED_PROFILE_REQUIREMENTS["POSITION_SWING"] == {"timeframe": "1d", "required_rows": 560}
