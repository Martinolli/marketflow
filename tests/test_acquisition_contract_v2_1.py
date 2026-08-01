from __future__ import annotations

import ast
import dataclasses
import json
import subprocess
import sys
import tomllib
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from marketflow.research import acquisition_contract_v2 as acv2
from marketflow.research import acquisition_contract_v2_1 as acv21
from marketflow.research import fixed_date_acquisition_contract as fdac


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG = REPO_ROOT / "config" / "fixed_date_acquisition_contract_v2_1.toml"
V2_CONFIG = REPO_ROOT / "config" / "fixed_date_acquisition_contract_v2.toml"
V1_CONFIG = REPO_ROOT / "config" / "fixed_date_acquisition_contract.example.toml"
MODULE = REPO_ROOT / "marketflow" / "research" / "acquisition_contract_v2_1.py"
V1_DIGEST = "29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e"
V2_DIGEST = "59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0"


def _payload() -> dict:
    with CONFIG.open("rb") as handle:
        return tomllib.load(handle)


def _contract() -> acv21.AcquisitionContractV21:
    return acv21.load_contract_toml(CONFIG)


def test_v2_1_contract_loads_with_distinct_schema_base_binding_and_disabled_execution():
    contract = _contract()
    receipt = acv21.readiness_receipt(contract)
    rendered = json.dumps(receipt, sort_keys=True)

    assert contract.contract_schema_version == "marketflow.acquisition_contract.v2.1"
    assert contract.decision_set_version == "marketflow.acquisition_decisions.v2.1"
    assert contract.contract_status == "ACQUISITION_CONTRACT_V2_1_READY_FOR_IMPLEMENTATION"
    assert contract.base_contract_schema == "marketflow.acquisition_contract.v2"
    assert contract.base_contract_digest == V2_DIGEST
    assert acv21.verify_base_contract_digest(contract) == V2_DIGEST
    assert receipt["timestamp_policy_complete"] is True
    assert receipt["acquisition_enabled"] is False
    assert receipt["provider_execution_enabled"] is False
    assert receipt["calendar_generation_enabled"] is False
    assert receipt["normalization_enabled"] is False
    assert receipt["registry_authority_enabled"] is False
    assert receipt["frozen_calendar_engine"] == "NOT_IMPLEMENTED"
    assert receipt["bar_engine"] == "NOT_IMPLEMENTED"
    assert "api_key" not in rendered.lower()
    assert ":\\" not in rendered


def test_v1_and_v2_digests_are_unchanged_and_loaders_are_version_separated():
    v1_contract = fdac.load_contract_toml(V1_CONFIG)
    v2_contract = acv2.load_contract_toml(V2_CONFIG)

    assert fdac.contract_digest(v1_contract) == V1_DIGEST
    assert acv2.contract_digest(v2_contract) == V2_DIGEST
    with pytest.raises(acv2.ContractV2ValidationError):
        acv2.load_contract_toml(CONFIG)
    with pytest.raises(acv21.ContractV21ValidationError):
        acv21.load_contract_toml(V1_CONFIG)
    with pytest.raises(acv21.ContractV21ValidationError):
        acv21.load_contract_toml(V2_CONFIG)


def test_source_timestamp_policy_is_endpoint_specific_window_start_and_strict():
    policy = _contract().source_timestamp_policy

    assert policy.provider_endpoint_family == "STOCKS_CUSTOM_BARS_V2"
    assert policy.provider_timestamp_field == "t"
    assert policy.provider_timestamp_unit == "UNIX_EPOCH_MILLISECONDS"
    assert policy.provider_timestamp_semantic == "START_OF_AGGREGATE_WINDOW"
    assert policy.source_interval_minutes == 15
    assert policy.source_interval_duration == "PT15M"
    assert policy.interval_boundary == "LEFT_CLOSED_RIGHT_OPEN"
    assert policy.canonical_start_field == "window_start_utc"
    assert policy.canonical_end_field == "window_end_utc"
    assert policy.derived_bar_timestamp_semantic == "WINDOW_END"
    assert policy.exact_slot_alignment_required is True
    assert policy.timestamp_snapping_enabled is False
    assert policy.timestamp_tolerance_enabled is False

    for mutation in (
        {"provider_endpoint_family": "GROUPED_DAILY"},
        {"provider_timestamp_field": "timestamp_utc"},
        {"provider_timestamp_unit": "UNIX_SECONDS"},
        {"provider_timestamp_semantic": "CLOSE_OF_AGGREGATE_WINDOW"},
        {"provider_timestamp_semantic": "PROVIDER_EPOCH_AMBIGUOUS"},
        {"source_interval_minutes": 30},
        {"source_interval_duration": "PT30M"},
        {"interval_boundary": "RIGHT_CLOSED"},
        {"derived_bar_timestamp_semantic": "WINDOW_START"},
        {"timestamp_snapping_enabled": True},
        {"timestamp_tolerance_enabled": True},
    ):
        with pytest.raises(acv21.ContractV21ValidationError):
            dataclasses.replace(policy, **mutation).validate()


def test_normalized_source_bar_contract_names_window_start_and_end_explicitly():
    contract = _contract().normalized_source_bar_contract

    assert contract.identity_fields == ("window_start_utc", "window_end_utc", "open", "high", "low", "close", "volume")
    assert contract.window_start_source == "PROVIDER_FIELD_T"
    assert contract.window_end_rule == "WINDOW_START_PLUS_PT15M"
    assert contract.timezone_requirement == "TIMEZONE_AWARE_UTC"
    assert contract.timestamp_utc_compatibility_field == "timestamp_utc"
    assert contract.timestamp_utc_compatibility_semantic == "WINDOW_START"
    assert contract.caller_selected_timestamp_semantic == "PROHIBITED"
    assert contract.local_machine_timezone_dependency is False

    with pytest.raises(acv21.ContractV21ValidationError):
        dataclasses.replace(contract, timestamp_utc_compatibility_semantic="WINDOW_END").validate()


def test_epoch_millisecond_source_window_is_utc_aware_exact_and_grid_aligned():
    start, end = acv21.source_window_from_epoch_ms(1_704_204_000_000)

    assert start == datetime(2024, 1, 2, 14, 0, tzinfo=UTC)
    assert end == start + timedelta(minutes=15)
    assert end > start
    assert start.tzinfo is UTC
    assert end.tzinfo is UTC

    for bad_value in ("1704204000000", 1_704_204_000_000.0, True, 1_704_204_000_001, 1_704_204_060_000):
        with pytest.raises(acv21.ContractV21ValidationError):
            acv21.source_window_from_epoch_ms(bad_value)


def test_source_slot_examples_match_left_closed_right_open_rth_contract():
    starts = acv21.rth_source_start_labels()

    assert starts["morning"][0] == "09:30"
    assert starts["morning"][-1] == "12:30"
    assert starts["afternoon"][0] == "12:45"
    assert starts["afternoon"][-1] == "15:45"
    assert len(starts["morning"]) == 13
    assert len(starts["afternoon"]) == 13
    assert len(starts["daily"]) == 26
    assert "16:00" not in starts["daily"]

    start, end = acv21.source_window_for_local_start("2024-01-02", "09:30")
    assert start == datetime(2024, 1, 2, 14, 30, tzinfo=UTC)
    assert end == datetime(2024, 1, 2, 14, 45, tzinfo=UTC)
    start, end = acv21.source_window_for_local_start("2024-01-02", "15:45")
    assert start == datetime(2024, 1, 2, 20, 45, tzinfo=UTC)
    assert end == datetime(2024, 1, 2, 21, 0, tzinfo=UTC)


def test_dst_conversion_preserves_exact_15_minute_duration():
    winter_start, winter_end = acv21.source_window_for_local_start("2024-01-02", "09:30")
    summer_start, summer_end = acv21.source_window_for_local_start("2024-07-01", "09:30")

    assert winter_start == datetime(2024, 1, 2, 14, 30, tzinfo=UTC)
    assert summer_start == datetime(2024, 7, 1, 13, 30, tzinfo=UTC)
    assert winter_end - winter_start == timedelta(minutes=15)
    assert summer_end - summer_start == timedelta(minutes=15)


def test_derived_timestamps_remain_close_stamped_not_source_start_stamped():
    derived = _contract().derived_timestamp_contract

    assert derived.derived_bar_timestamp_semantic == "WINDOW_END"
    assert derived.source_bar_timestamp_semantic == "START_OF_AGGREGATE_WINDOW"
    assert acv21.derived_timestamp_utc("2024-01-02", derived.swing_morning_timestamp_local) == datetime(
        2024, 1, 2, 17, 45, tzinfo=UTC
    )
    assert acv21.derived_timestamp_utc("2024-01-02", derived.swing_afternoon_timestamp_local) == datetime(
        2024, 1, 2, 21, 0, tzinfo=UTC
    )
    assert acv21.derived_timestamp_utc("2024-07-01", derived.position_swing_timestamp_local) == datetime(
        2024, 7, 1, 20, 0, tzinfo=UTC
    )
    with pytest.raises(acv21.ContractV21ValidationError):
        dataclasses.replace(derived, derived_bar_timestamp_semantic="WINDOW_START").validate()


def test_canonical_serialization_and_digest_are_stable_and_sensitive():
    contract = _contract()
    payload = _payload()
    reordered_payload = dict(reversed(list(payload.items())))
    changed = dataclasses.replace(
        contract,
        source_timestamp_policy=dataclasses.replace(contract.source_timestamp_policy, source_interval_minutes=30),
    )

    assert acv21.contract_digest(contract) == acv21.contract_digest(acv21.contract_from_dict(reordered_payload))
    assert acv21.canonical_json_bytes(contract) == acv21.canonical_json_bytes(contract)
    with pytest.raises(acv21.ContractV21ValidationError):
        changed.validate()


def test_loader_rejects_unknown_missing_unsafe_and_enabled_operational_fields(tmp_path: Path):
    payload = _payload()
    payload["unknown"] = "value"
    with pytest.raises(acv21.ContractV21ValidationError, match="unknown"):
        acv21.contract_from_dict(payload)

    payload = _payload()
    del payload["source_timestamp_policy"]
    with pytest.raises(acv21.ContractV21ValidationError, match="missing"):
        acv21.contract_from_dict(payload)

    for dotted_field in ("api_key", "download_url", "output_path", "ticker"):
        payload = _payload()
        payload[dotted_field] = "unsafe"
        with pytest.raises(acv21.ContractV21ValidationError):
            acv21.contract_from_dict(payload)

    payload = _payload()
    payload["acquisition_enabled"] = True
    with pytest.raises(acv21.ContractV21ValidationError):
        acv21.contract_from_dict(payload)

    external = tmp_path / "fixed_date_acquisition_contract_v2_1.toml"
    external.write_text(CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
    for bad_ref in (
        external,
        "../config/fixed_date_acquisition_contract_v2_1.toml",
        "config/nested/fixed_date_acquisition_contract_v2_1.toml",
        "https://example.invalid/contract.toml",
        "$env:CONTRACT",
        "config/fixed_date_acquisition_contract_v2_1.toml:stream",
    ):
        with pytest.raises(acv21.ContractV21ValidationError):
            acv21.load_contract_toml(bad_ref)


def test_dry_cli_outputs_sanitized_receipt_and_rejects_operational_args():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.research.acquisition_contract_v2_1"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["status"] == "ACQUISITION_CONTRACT_V2_1_READY_FOR_IMPLEMENTATION"
    assert receipt["source_endpoint"] == "STOCKS_CUSTOM_BARS_V2"
    assert receipt["source_timestamp_semantic"] == "START_OF_AGGREGATE_WINDOW"
    assert receipt["timestamp_utc_compatibility_semantic"] == "WINDOW_START"
    assert receipt["acquisition_enabled"] is False
    assert "api_key" not in result.stdout.lower()
    for flag in ("--ticker", "--start-date", "--end-date", "--semantic", "--enable-acquisition"):
        rejected = subprocess.run(
            [sys.executable, "-m", "marketflow.research.acquisition_contract_v2_1", flag, "unsafe"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert rejected.returncode != 0


def test_v2_1_module_has_no_provider_calendar_engine_network_candidate_or_environment_imports():
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
        "marketflow.historical_data",
        "marketflow.marketflow_strategy",
        "marketflow.services.monte_carlo_service",
        "marketflow.services.backtest_result_service",
        "marketflow.services.walk_forward_validation_service",
    }
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported_from = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    attrs = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }

    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert "getenv" not in attrs
    assert "environ" not in attrs
    assert {"download", "request", "post", "put", "delete"}.isdisjoint(attrs)
    assert "START_OF_AGGREGATE_WINDOW" in source
    assert "WINDOW_START" in source
    assert "CLOSE_OF_AGGREGATE_WINDOW" not in source
    assert "timestamp_snapping_enabled: bool = False" in source
    assert "provider_native_4h_canonical: bool = False" in source
    assert "provider_native_1d_canonical: bool = False" in source
    assert "epoch_milliseconds / 1000" not in source
    assert "divmod(epoch_milliseconds, 1000)" in source


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
