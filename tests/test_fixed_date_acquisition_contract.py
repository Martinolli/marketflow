from __future__ import annotations

import ast
import dataclasses
import json
import subprocess
import sys
from pathlib import Path

import pytest

from marketflow.research import fixed_date_acquisition_contract as fdac


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = REPO_ROOT / "config" / "fixed_date_acquisition_contract.example.toml"
MODULE = REPO_ROOT / "marketflow" / "research" / "fixed_date_acquisition_contract.py"


def _contract() -> fdac.FixedDateAcquisitionContract:
    return fdac.default_proposed_contract()


def _as_payload(contract: fdac.FixedDateAcquisitionContract) -> dict:
    return dataclasses.asdict(contract)


def _fake_response(**overrides):
    response = {
        "status": "OK",
        "ticker": "SYNTH",
        "adjusted": True,
        "results": [
            {
                "timestamp_utc": "2026-01-02T14:30:00+00:00",
                "open": 10.0,
                "high": 11.0,
                "low": 9.5,
                "close": 10.5,
                "volume": 100,
                "completed": True,
            },
            {
                "timestamp_utc": "2026-01-02T18:30:00+00:00",
                "open": 10.5,
                "high": 12.0,
                "low": 10.0,
                "close": 11.5,
                "volume": 200,
                "completed": True,
            },
        ],
    }
    response.update(overrides)
    return response


def test_contract_is_immutable_and_validates_with_blockers():
    contract = _contract()
    contract.validate()

    assert contract.readiness_status == fdac.ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS
    assert contract.acquisition_enabled is False
    assert contract.provider_request.provider_entitlement_status == fdac.OPERATOR_ATTESTED_CONFIRMED
    assert fdac.PROVIDER_ENTITLEMENT_NOT_CONFIRMED not in contract.blockers
    assert fdac.FIXED_DATES_NOT_APPROVED in contract.blockers
    with pytest.raises(dataclasses.FrozenInstanceError):
        contract.acquisition_enabled = True


def test_example_toml_loads_and_receipt_is_sanitized():
    contract = fdac.load_contract_toml(EXAMPLE)
    receipt = fdac.readiness_receipt(contract)
    rendered = json.dumps(receipt, sort_keys=True)

    assert receipt["status"] == fdac.ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS
    assert receipt["acquisition_enabled"] is False
    assert receipt["provider_business_identity"] == "MASSIVE.COM"
    assert receipt["provider_legacy_adapter_identity"] == "POLYGON.IO"
    assert receipt["provider_entitlement_status"] == fdac.OPERATOR_ATTESTED_CONFIRMED
    assert receipt["provider_entitlement_confirmed"] is True
    assert receipt["provider_plan_category"] == "STOCKS_STARTER"
    assert receipt["provider_historical_entitlement"] == "FIVE_YEARS"
    assert receipt["provider_data_recency"] == "FIFTEEN_MINUTE_DELAYED"
    assert receipt["provider_aggregate_access"] == "INTRADAY_AND_DAILY_AVAILABLE"
    assert receipt["SWING_timeframe"] == "4h"
    assert receipt["SWING_minimum_rows"] == 390
    assert receipt["POSITION_SWING_timeframe"] == "1d"
    assert receipt["POSITION_SWING_minimum_rows"] == 560
    assert "api_key" not in rendered.lower()
    assert ":\\" not in rendered
    assert "2026-" not in rendered


def test_canonical_serialization_and_digest_are_stable_and_sensitive():
    contract = _contract()
    digest_one = fdac.contract_digest(contract)
    digest_two = fdac.contract_digest(contract)
    changed = dataclasses.replace(
        contract,
        provider_request=dataclasses.replace(contract.provider_request, expected_response_schema="CHANGED_SCHEMA"),
    )

    assert fdac.canonical_json_bytes(contract) == fdac.canonical_json_bytes(contract)
    assert digest_one == digest_two
    assert fdac.contract_digest(changed) != digest_one


def test_loader_rejects_unknown_missing_credential_path_and_url_fields():
    payload = _as_payload(_contract())
    payload["unexpected"] = "value"
    with pytest.raises(fdac.ContractValidationError, match="unknown"):
        fdac.contract_from_dict(payload)

    payload = _as_payload(_contract())
    del payload["blockers"]
    with pytest.raises(fdac.ContractValidationError, match="missing"):
        fdac.contract_from_dict(payload)

    for bad_field in ("api_key", "download_url", "output_path"):
        payload = _as_payload(_contract())
        payload[bad_field] = "unsafe"
        with pytest.raises(fdac.ContractValidationError):
            fdac.contract_from_dict(payload)


def test_fixed_dates_remain_unapproved_and_reject_relative_or_unknown_status():
    contract = _contract()
    proposed_with_actual_dates = dataclasses.replace(
        contract.provider_request,
        ticker="SYNTH",
        start_date="2024-01-01",
        end_date="2024-12-31",
    )
    with pytest.raises(fdac.ContractValidationError, match="start_date"):
        proposed_with_actual_dates.validate()

    for bad_start in ("today", "now", "100d", "365d", "2y"):
        bad = dataclasses.replace(contract.provider_request, start_date=bad_start)
        with pytest.raises(fdac.ContractValidationError):
            bad.validate()

    unknown_status = dataclasses.replace(contract.provider_request, start_date_status="APPROVED")
    with pytest.raises(fdac.ContractValidationError, match="start_date_status"):
        unknown_status.validate()


def test_no_current_date_default_or_timezone_naive_canonical_response():
    contract = dataclasses.replace(
        _contract(),
        provider_request=dataclasses.replace(_contract().provider_request, ticker="SYNTH"),
    )
    response = _fake_response()
    response["results"][0]["timestamp_utc"] = "2026-01-02T14:30:00"

    with pytest.raises(fdac.ContractValidationError, match="timezone-aware"):
        fdac.validate_fake_provider_response(contract, response)


def test_canonical_response_timestamp_must_be_utc_as_supplied():
    contract = dataclasses.replace(
        _contract(),
        provider_request=dataclasses.replace(_contract().provider_request, ticker="SYNTH"),
    )
    response = _fake_response()
    response["results"][0]["timestamp_utc"] = "2026-01-02T18:30:00+04:00"

    with pytest.raises(fdac.ContractValidationError, match="UTC"):
        fdac.validate_fake_provider_response(contract, response)


def test_profile_contracts_preserve_exact_timeframes_and_row_gates():
    contract = _contract()
    profile_map = {profile.profile_id: profile for profile in contract.profiles}

    assert profile_map["SWING"].canonical_timeframe == "4h"
    assert profile_map["SWING"].minimum_valid_ohlcv_rows == 390
    assert profile_map["POSITION_SWING"].canonical_timeframe == "1d"
    assert profile_map["POSITION_SWING"].minimum_valid_ohlcv_rows == 560

    weakened = dataclasses.replace(profile_map["SWING"], minimum_valid_ohlcv_rows=389)
    with pytest.raises(fdac.ContractValidationError):
        weakened.validate()

    wrong_timeframe = dataclasses.replace(profile_map["POSITION_SWING"], canonical_timeframe="4h")
    with pytest.raises(fdac.ContractValidationError):
        wrong_timeframe.validate()


def test_unresolved_4h_native_and_session_policies_block_execution():
    contract = _contract()
    swing = contract.profiles[0]

    assert swing.bar_construction_policy == fdac.BAR_CONSTRUCTION_NOT_CONFIRMED
    assert swing.session_policy == fdac.SESSION_POLICY_NOT_CONFIRMED
    assert fdac.BAR_CONSTRUCTION_NOT_APPROVED in contract.blockers
    assert fdac.SESSION_POLICY_NOT_APPROVED in contract.blockers

    silently_approved = dataclasses.replace(
        swing,
        bar_construction_policy=fdac.BAR_PROVIDER_NATIVE_CLOCK_4H,
        bar_construction_status="APPROVED",
    )
    with pytest.raises(fdac.ContractValidationError):
        silently_approved.validate()


def test_provider_request_policy_statuses_cannot_contradict_blockers():
    request = _contract().provider_request

    with pytest.raises(fdac.ContractValidationError, match="pagination policy"):
        dataclasses.replace(request, pagination_policy_status="APPROVED").validate()
    with pytest.raises(fdac.ContractValidationError, match="session policy"):
        dataclasses.replace(request, requested_session_policy=fdac.SESSION_PROVIDER_DEFAULT).validate()


def test_local_aggregation_mode_is_represented_but_not_implemented_or_enabled():
    swing = dataclasses.replace(
        _contract().profiles[0],
        bar_construction_policy=fdac.BAR_DETERMINISTIC_LOCAL_AGGREGATION,
    )

    swing.validate()
    assert swing.bar_construction_status == fdac.NOT_APPROVED


def test_daily_provider_native_mode_remains_pending_session_review():
    daily = _contract().profiles[1]

    assert daily.bar_construction_policy == fdac.BAR_PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW
    assert daily.session_policy == fdac.SESSION_POLICY_NOT_CONFIRMED
    assert daily.bar_construction_status == fdac.NOT_APPROVED


def test_session_policy_has_no_hidden_default_approval():
    profile = dataclasses.replace(_contract().profiles[0], session_policy=fdac.SESSION_PROVIDER_DEFAULT)

    profile.validate()
    assert profile.session_policy_status == fdac.NOT_APPROVED


def test_adjustment_policy_requires_split_adjusted_and_no_dividend_claim():
    policy = fdac.AdjustmentPolicy()
    policy.validate()

    with pytest.raises(fdac.ContractValidationError):
        dataclasses.replace(policy, split_adjusted_requested=False).validate()
    with pytest.raises(fdac.ContractValidationError):
        dataclasses.replace(policy, dividend_adjusted=True).validate()
    with pytest.raises(fdac.ContractValidationError, match="provenance"):
        dataclasses.replace(policy, adjustment_provenance_status="CONFIRMED").validate()


def test_timezone_policy_fields_are_strict_and_unapproved():
    policy = fdac.TimezonePolicy()
    policy.validate()

    mutations = [
        {"source_aggregation_timezone": "UTC"},
        {"canonical_storage_timezone": "AMERICA_NEW_YORK"},
        {"original_provider_timestamps": "DROP_PROVIDER_EPOCH_TIMESTAMPS"},
        {"source_local_timezone_metadata": "AUTHORITATIVE"},
        {"dst_conversion_policy": "SOURCE_LOCAL_FIRST"},
        {"naive_canonical_timestamps_allowed": True},
        {"timezone_policy_status": "APPROVED"},
    ]
    for mutation in mutations:
        with pytest.raises(fdac.ContractValidationError):
            dataclasses.replace(policy, **mutation).validate()


def test_adjusted_response_mismatch_invalidates_acquisition():
    contract = _contract()

    with pytest.raises(fdac.ContractValidationError, match="adjusted response"):
        fdac.validate_provider_adjusted_metadata(contract, False)

    response = _fake_response(adjusted="false")
    contract = dataclasses.replace(
        contract,
        provider_request=dataclasses.replace(contract.provider_request, ticker="SYNTH"),
    )
    with pytest.raises(fdac.ContractValidationError, match="boolean"):
        fdac.validate_fake_provider_response(contract, response)


def test_pagination_sequence_statuses():
    assert (
        fdac.validate_pagination_sequence(
            [
                {"page_id": "1", "results": ["2026-01-01T00:00:00Z"], "has_more": True, "expected_count": 1},
                {"page_id": "2", "results": ["2026-01-02T00:00:00Z"], "has_more": False, "expected_count": 1},
            ],
            "2026-01-01T00:00:00Z",
            "2026-01-02T00:00:00Z",
        )
        == fdac.REQUEST_COMPLETE
    )
    assert fdac.validate_pagination_sequence([], "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z") == fdac.PAGINATION_INCOMPLETE
    assert (
        fdac.validate_pagination_sequence(
            [{"page_id": "1", "results": ["2026-01-01T00:00:00Z"], "has_more": True, "expected_count": 1}],
            "2026-01-01T00:00:00Z",
            "2026-01-01T00:00:00Z",
        )
        == fdac.PAGINATION_INCOMPLETE
    )
    assert (
        fdac.validate_pagination_sequence(
            [
                {"page_id": "1", "results": ["2026-01-01T00:00:00Z"], "has_more": True, "expected_count": 1},
                {"page_id": "1", "results": ["2026-01-02T00:00:00Z"], "has_more": False, "expected_count": 1},
            ],
            "2026-01-01T00:00:00Z",
            "2026-01-02T00:00:00Z",
        )
        == fdac.PAGE_DUPLICATE
    )
    assert (
        fdac.validate_pagination_sequence(
            [{"page_id": "1", "results": ["2026-01-01T00:00:00Z"], "has_more": False, "expected_count": 2}],
            "2026-01-01T00:00:00Z",
            "2026-01-01T00:00:00Z",
        )
        == fdac.REQUEST_TRUNCATED
    )
    assert (
        fdac.validate_pagination_sequence(
            [{"page_id": "1", "results": ["2026-01-02T00:00:00Z"], "has_more": False, "expected_count": 1}],
            "2026-01-01T00:00:00Z",
            "2026-01-02T00:00:00Z",
        )
        == fdac.RANGE_COVERAGE_INCOMPLETE
    )


def test_blocker_list_is_exact_and_sanitized():
    contract = _contract()
    with pytest.raises(fdac.ContractValidationError, match="blockers"):
        dataclasses.replace(contract, blockers=contract.blockers + ("api_key=unsafe",)).validate()
    with pytest.raises(fdac.ContractValidationError, match="blockers"):
        dataclasses.replace(contract, blockers=contract.blockers[:-1]).validate()


def test_duplicate_boundary_and_missing_page_are_not_silent_success():
    boundary_duplicate = [
        {"page_id": "1", "results": ["2026-01-01T00:00:00Z"], "has_more": True, "expected_count": 1},
        {"page_id": "2", "results": ["2026-01-01T00:00:00Z"], "has_more": False, "expected_count": 1},
    ]
    missing_last = [
        {"page_id": "1", "results": ["2026-01-01T00:00:00Z"], "has_more": False, "expected_count": 1}
    ]

    assert fdac.validate_pagination_sequence(boundary_duplicate, "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z") == fdac.PAGE_DUPLICATE
    assert fdac.validate_pagination_sequence(missing_last, "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z") == fdac.RANGE_COVERAGE_INCOMPLETE


@pytest.mark.parametrize(
    "mutate,match",
    [
        (lambda r: r.update({"status": "FAIL"}), "status"),
        (lambda r: r.update({"adjusted": False}), "adjusted response"),
        (lambda r: r["results"][1].update({"timestamp_utc": "2026-01-02T14:30:00+00:00"}), "ascending"),
        (lambda r: r["results"][1].update({"timestamp_utc": "2026-01-02T14:30:00+00:00"}), "ascending"),
        (lambda r: r["results"][0].update({"open": float("nan")}), "finite"),
        (lambda r: r["results"][0].update({"high": 8.0}), "high"),
        (lambda r: r["results"][0].update({"volume": -1}), "volume"),
        (lambda r: r["results"][1].update({"completed": False}), "partial"),
    ],
)
def test_response_validation_failures(mutate, match):
    contract = dataclasses.replace(
        _contract(),
        provider_request=dataclasses.replace(_contract().provider_request, ticker="SYNTH"),
    )
    response = _fake_response()
    mutate(response)

    with pytest.raises(fdac.ContractValidationError, match=match):
        fdac.validate_fake_provider_response(contract, response)


def test_empty_response_results_are_not_complete():
    contract = dataclasses.replace(
        _contract(),
        provider_request=dataclasses.replace(_contract().provider_request, ticker="SYNTH"),
    )

    with pytest.raises(fdac.ContractValidationError, match="non-empty"):
        fdac.validate_fake_provider_response(contract, _fake_response(results=[]))


def test_response_validation_accepts_complete_fake_sequence():
    contract = dataclasses.replace(
        _contract(),
        provider_request=dataclasses.replace(_contract().provider_request, ticker="SYNTH"),
    )

    assert fdac.validate_fake_provider_response(contract, _fake_response()) == fdac.REQUEST_COMPLETE


def test_wrong_ticker_and_unknown_response_shape_rejected():
    contract = dataclasses.replace(
        _contract(),
        provider_request=dataclasses.replace(_contract().provider_request, ticker="SYNTH"),
    )
    wrong_ticker = _fake_response(ticker="OTHER")
    unknown_shape = _fake_response()
    unknown_shape["extra"] = "unsafe"

    with pytest.raises(fdac.ContractValidationError, match="ticker"):
        fdac.validate_fake_provider_response(contract, wrong_ticker)
    with pytest.raises(fdac.ContractValidationError, match="shape"):
        fdac.validate_fake_provider_response(contract, unknown_shape)


def test_raw_normalized_provenance_relationship_is_deterministic_and_sanitized():
    contract = dataclasses.replace(
        _contract(),
        provider_request=dataclasses.replace(_contract().provider_request, ticker="SYNTH"),
    )
    metadata = fdac.artifact_relationship_metadata(
        raw_response_bytes=b'{"status":"OK"}',
        normalized_rows=[
            {
                "ticker": "SYNTH",
                "timeframe": "4h",
                "timestamp_utc": "2026-01-02T14:30:00+00:00",
                "open": "10",
                "high": "11",
                "low": "9",
                "close": "10",
                "volume": "100",
            }
        ],
        request_contract=contract,
        code_commit="bf1187c",
        client_package_version="polygon-api-client==1.14.6",
    )
    rendered = json.dumps(metadata, sort_keys=True)

    assert metadata["parent_relationship"] == "RAW_PROVIDER_RESPONSE->NORMALIZED_OHLCV_DATASET"
    assert metadata["exact_ticker"] == "SYNTH"
    assert metadata["raw_response_digest"]
    assert metadata["normalized_dataset_digest"]
    assert "api_key" not in rendered.lower()
    assert ":\\" not in rendered

    unsafe_version = "C:" + "\\unsafe\\polygon-api-client"
    with pytest.raises(fdac.ContractValidationError, match="client_package_version"):
        fdac.artifact_relationship_metadata(
            raw_response_bytes=b"{}",
            normalized_rows=[],
            request_contract=contract,
            code_commit="bf1187c",
            client_package_version=unsafe_version,
        )


def test_cli_dry_run_outputs_blocked_receipt_and_rejects_operational_flags():
    result = subprocess.run(
        [sys.executable, "-m", "marketflow.research.fixed_date_acquisition_contract"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    receipt = json.loads(result.stdout)

    assert receipt["status"] == fdac.ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS
    assert receipt["acquisition_enabled"] is False
    for flag in ("--ticker", "--start-date", "--end-date", "--api-key"):
        rejected = subprocess.run(
            [sys.executable, "-m", "marketflow.research.fixed_date_acquisition_contract", flag, "unsafe"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert rejected.returncode != 0


def test_contract_module_has_no_provider_network_candidate_or_credential_imports():
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    forbidden_modules = {
        "polygon",
        "requests",
        "httpx",
        "socket",
        "streamlit",
        "openai",
        "yfinance",
        "marketflow.marketflow_data_provider",
        "marketflow.marketflow_polygon_tools",
        "marketflow.marketflow_strategy",
        "marketflow.services.monte_carlo_service",
        "marketflow.services.backtest_result_service",
        "marketflow.services.walk_forward_validation_service",
    }
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    called_attributes = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }

    assert forbidden_modules.isdisjoint(imported)
    assert forbidden_modules.isdisjoint(imported_from)
    assert "getenv" not in called_attributes
    assert "environ" not in MODULE.read_text(encoding="utf-8")
    assert {"RESTClient", "PolygonIOProvider", "rank_long_candidates", "build_candidate_from_prefix"}.isdisjoint(called_names)


def test_prior_integrity_constants_remain_unchanged():
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
