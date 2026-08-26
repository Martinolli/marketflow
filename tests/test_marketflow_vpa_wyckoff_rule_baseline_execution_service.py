from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_file
from marketflow.services import (
    marketflow_vpa_wyckoff_rule_baseline_execution_service as execution_service,
)


def _feature_bundle(index: int) -> dict:
    positive = index == 0
    values = {
        "GROUP_VOLUME_CHANGE_AND_ZSCORE": {
            "volume_zscore_20": "1.2" if positive else "-0.6"
        },
        "GROUP_SPREAD_VOLUME_INTERACTION": {
            "spread_volume_interaction": "0.5",
            "volume_zscore_20": "1.2" if positive else "-0.6",
        },
        "GROUP_EFFORT_RESULT_DIVERGENCE": {
            "effort_result_ratio": "1.0",
            "volume_zscore_20": "1.2" if positive else "-0.6",
        },
        "GROUP_CLOSE_LOCATION_VALUE": {
            "close_location_value": "0.70" if positive else "0.20"
        },
        "GROUP_INTRADAY_RANGE_AND_BODY": {"intraday_range_fraction": "0.02"},
        "GROUP_MOVING_AVERAGE_SLOPE": {
            "sma_20_slope_10": "0.01" if positive else "-0.01"
        },
        "GROUP_RELATIVE_STRENGTH_VS_UNIVERSE": {
            "relative_strength_return_20": "0.02" if positive else "-0.02"
        },
        "GROUP_RELATIVE_STRENGTH_RANK": {
            "relative_strength_percentile_20": "0.80" if positive else "0.20"
        },
        "GROUP_ATR_AND_VOLATILITY_COMPRESSION": {
            "volatility_compression_ratio": "0.70" if positive else "1.30"
        },
        "GROUP_ABSTENTION_NOISE_CONTEXT": {
            "noise_to_trend_ratio_20": "1.0" if positive else "2.5",
            "abstention_noise_flag": not positive,
        },
        "GROUP_DATA_AVAILABILITY_FLAGS": {"sufficient_history_20": True},
        "GROUP_META_LIMITATION_FLAGS": {
            "canonical_record_count_for_ticker": 2,
            "meta_reduced_record_count_flag": True,
            "meta_limitation_preserved": True,
        },
        "GROUP_CLOSE_TO_CLOSE_RETURNS": {
            "trailing_return_1": "0.01" if positive else "-0.01",
            "trailing_return_5": "0.03" if positive else "-0.03",
        },
    }
    return {
        group: {
            "feature_available": True,
            "feature_family": f"FEATURE_{group}",
            "feature_formula_version": "marketflow_signal_or_feature_formula_v1",
            "feature_unavailable_reason": None,
            "feature_values": values[group],
            "history_lookback_available": 30,
            "history_lookback_required": 20,
            "signal_family": f"SIGNAL_{group}",
        }
        for group in execution_service.APPROVED_FEATURE_GROUPS
    }


def _source_rows() -> list[dict]:
    rows = []
    for index, date in enumerate(("2022-01-03", "2022-01-04")):
        for family_index in range(5):
            for horizon in (5, 10, 20):
                rows.append(
                    {
                        "canonical_record_index": index,
                        "dataset_name": "expanded_universe_canonical_dataset_v1",
                        "date": date,
                        "feature_bundle": _feature_bundle(index),
                        "feature_bundle_available": True,
                        "feature_group_count": 13,
                        "feature_unavailable_group_count": 0,
                        "forward_end_date": "2022-02-01",
                        "forward_start_date": "2022-01-05",
                        "non_actionable": True,
                        "records_digest": execution_service.EXPECTED_SOURCE_RECORDS_DIGEST,
                        "research_only": True,
                        "selected_feature_package": execution_service.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
                        "selected_label_target_package": execution_service.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
                        "selected_matrix_layout": execution_service.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
                        "selected_matrix_package": execution_service.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
                        "selected_objective_path": execution_service.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
                        "source_feature_values_digest": execution_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
                        "source_matrix_approval_digest": "0f438427e1b5149b4afb15a8cf0c9af6bb39a95f18e47b8413da6d4e34a9f888",
                        "source_profile": "RTH_FULL_SESSION_1D",
                        "source_target_values_digest": execution_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
                        "target_available": True,
                        "target_class": "POSITIVE",
                        "target_family": f"TARGET_FAMILY_{family_index}",
                        "target_horizon_sessions": horizon,
                        "target_profile": f"TARGET_FAMILY_{family_index}_HORIZON_{horizon}",
                        "target_unavailable_reason": None,
                        "target_value": "0.01",
                        "ticker": "META",
                        "timeframe": "1d",
                    }
                )
    return rows


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json_bytes(row) for row in rows))


@pytest.fixture(scope="module")
def execution_environment(tmp_path_factory: pytest.TempPathFactory):
    root = tmp_path_factory.mktemp("vpa_wyckoff_execution")
    source_path = root / "source" / "matrix_rows.jsonl"
    output_root = root / "outputs"
    _write_jsonl(source_path, _source_rows())
    names = [
        "DEFAULT_SOURCE_MATRIX_PATH",
        "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST",
        "TARGET_UNIVERSE",
        "EXPECTED_RECORD_COUNTS",
        "EXPECTED_SOURCE_MATRIX_ROW_COUNT",
        "EXPECTED_RULE_VALUE_ROW_COUNT",
        "EXPECTED_STATE_VALUE_ROW_COUNT",
        "EXPECTED_RULE_FAMILY_REFERENCE_COUNT",
        "EXPECTED_STATE_FAMILY_REFERENCE_COUNT",
    ]
    original = {name: getattr(execution_service, name) for name in names}
    replacements = {
        "DEFAULT_SOURCE_MATRIX_PATH": source_path,
        "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST": sha256_file(source_path),
        "TARGET_UNIVERSE": ["META"],
        "EXPECTED_RECORD_COUNTS": {"META": 2},
        "EXPECTED_SOURCE_MATRIX_ROW_COUNT": 30,
        "EXPECTED_RULE_VALUE_ROW_COUNT": 30,
        "EXPECTED_STATE_VALUE_ROW_COUNT": 30,
        "EXPECTED_RULE_FAMILY_REFERENCE_COUNT": 240,
        "EXPECTED_STATE_FAMILY_REFERENCE_COUNT": 180,
    }
    for name, value in replacements.items():
        setattr(execution_service, name, value)
    artifact = execution_service.execute_marketflow_vpa_wyckoff_rule_baseline_v1(
        output_root=output_root,
        run_timestamp_utc="2026-08-26T12:00:00Z",
    )
    yield {
        "artifact": artifact,
        "output_root": output_root,
        "source_path": source_path,
        "root": root,
    }
    for name, value in original.items():
        setattr(execution_service, name, value)


def test_execution_builds_offline(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False
    assert artifact["live_provider_transport_enabled_in_execution"] is False
    assert artifact["market_data_acquisition_performed_in_execution"] is False
    assert artifact["source_verification"]["streaming_read_used"] is True
    assert artifact["source_verification"]["entire_matrix_loaded_into_memory"] is False


def test_execution_blocks_if_source_matrix_is_missing(
    execution_environment: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        execution_service,
        "DEFAULT_SOURCE_MATRIX_PATH",
        execution_environment["root"] / "missing.jsonl",
    )
    blocked = execution_service.execute_marketflow_vpa_wyckoff_rule_baseline_v1(
        output_root=execution_environment["root"] / "blocked_missing",
        run_timestamp_utc="2026-08-26T12:00:00Z",
    )
    assert blocked["artifact_kind"] == "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_BLOCKED"
    assert blocked["execution_status"] == (
        "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_BLOCKED_MISSING_OR_INVALID_MATRIX_SOURCE"
    )
    assert blocked["vpa_wyckoff_rule_baseline_executed"] is False
    assert blocked["vpa_wyckoff_rule_values_created"] is False


def test_execution_blocks_if_source_matrix_digest_is_invalid(
    execution_environment: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(execution_service, "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST", "0" * 64)
    blocked = execution_service.execute_marketflow_vpa_wyckoff_rule_baseline_v1(
        output_root=execution_environment["root"] / "blocked_digest",
        run_timestamp_utc="2026-08-26T12:00:00Z",
    )
    assert blocked["artifact_kind"] == "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_BLOCKED"
    assert blocked["failures"][0]["failure_id"] == "matrix_source_digest_mismatch"


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED"),
    ("schema_version", "marketflow_vpa_wyckoff_rule_baseline_execution_v1"),
    ("execution_status", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY"),
    ("execution_scope", "VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING"),
    ("selected_vpa_wyckoff_package", "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE"),
    ("selected_matrix_package", "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"),
    ("selected_matrix_layout", "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"),
    ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
    ("selected_label_target_package", "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    ("source_vpa_wyckoff_rule_baseline_approval_digest", execution_service.EXPECTED_SOURCE_APPROVAL_DIGEST),
    ("source_candidate_review_digest", execution_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST),
    ("source_candidate_digest", execution_service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
    ("source_matrix_results_review_digest", execution_service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST),
    ("source_feature_values_digest", execution_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST),
    ("source_target_values_digest", execution_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
    ("source_records_digest", execution_service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ("vpa_wyckoff_rule_baseline_authorized", True),
    ("vpa_wyckoff_rule_baseline_executed", True),
    ("vpa_wyckoff_rule_values_created", True),
    ("vpa_wyckoff_state_values_created", True),
    ("vpa_wyckoff_baseline_outputs_created", True),
    ("rule_threshold_policy", "STATIC_TRANSPARENT_BASELINE_NOT_OPTIMIZED"),
    ("predictive_usefulness", "not accepted"),
    ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"),
    ("strategy_use", "NOT_AUTHORIZED"),
    ("paper_trading", "NOT_AUTHORIZED"),
    ("broker_execution", "NOT_AUTHORIZED"),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_execution_core_field(
    execution_environment: dict, field: str, expected: object
) -> None:
    assert execution_environment["artifact"][field] == expected


COUNT_FIELDS = [
    ("source_matrix_row_count", 30),
    ("rule_value_row_count", 30),
    ("state_value_row_count", 30),
    ("selected_rule_family_count", 8),
    ("selected_state_family_count", 6),
    ("rule_family_reference_count", 240),
    ("state_family_reference_count", 180),
    ("generated_output_count", 10),
    ("expected_output_count", 10),
    ("observed_output_count", 10),
]


@pytest.mark.parametrize(("field", "expected"), COUNT_FIELDS)
def test_execution_count(
    execution_environment: dict, field: str, expected: int
) -> None:
    assert execution_environment["artifact"][field] == expected


def test_real_contract_preserves_dataset_universe_and_meta() -> None:
    assert approval_universe() == [
        "MSFT",
        "NVDA",
        "AMZN",
        "GOOGL",
        "META",
        "TSLA",
        "JPM",
        "XOM",
        "JNJ",
        "WMT",
        "CAT",
        "LMT",
    ]
    assert approval_meta_count() == 913


def approval_universe() -> list[str]:
    return list(execution_service.approval_service.TARGET_UNIVERSE)


def approval_meta_count() -> int:
    return 913


def test_rule_values_jsonl_schema_and_no_leakage(execution_environment: dict) -> None:
    path = execution_environment["output_root"] / "vpa_wyckoff_rule_values.jsonl"
    with path.open("r", encoding="utf-8") as handle:
        first = json.loads(handle.readline())
    assert set(first) == set(execution_service.RULE_OUTPUT_ROW_FIELDS)
    assert set(first["rule_values"]) == set(execution_service.SELECTED_RULE_FAMILY_IDS)
    assert set(first["state_values"]) == set(execution_service.SELECTED_STATE_FAMILY_IDS)
    assert not execution_service.FORBIDDEN_RULE_OUTPUT_FIELDS.intersection(first)
    serialized = json.dumps(first)
    for forbidden in execution_service.FORBIDDEN_RULE_OUTPUT_FIELDS:
        assert f'"{forbidden}"' not in serialized


def test_transparent_rule_and_state_tags(execution_environment: dict) -> None:
    path = execution_environment["output_root"] / "vpa_wyckoff_rule_values.jsonl"
    with path.open("r", encoding="utf-8") as handle:
        first = json.loads(handle.readline())
    assert first["rule_values"]["VPA_RULE_VOLUME_CONFIRMATION"]["tag"] == (
        "bullish_effort_confirmed"
    )
    assert first["rule_values"]["VPA_RULE_CLOSE_LOCATION_PRESSURE"]["tag"] == (
        "demand_pressure"
    )
    assert first["rule_values"]["VPA_RULE_RELATIVE_STRENGTH_CONFIRMATION"]["tag"] == (
        "leadership_confirmed"
    )
    assert first["state_values"]["WYCKOFF_STATE_ACCUMULATION_CANDIDATE"]["value"] is True
    assert first["state_values"]["WYCKOFF_STATE_MARKUP_OR_UPTREND_CANDIDATE"]["value"] is True


@pytest.mark.parametrize("filename", execution_service.OUTPUT_FILENAMES)
def test_expected_output_exists(execution_environment: dict, filename: str) -> None:
    assert (execution_environment["output_root"] / filename).is_file()


def test_digest_manifest_and_digests(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    manifest = artifact["output_digest_manifest"]
    assert [row["filename"] for row in manifest] == execution_service.OUTPUT_FILENAMES
    assert manifest[-1]["digest_kind"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    assert manifest[-1]["sha256"] is None
    assert len(artifact["vpa_wyckoff_rule_values_digest"]) == 64
    assert len(artifact["vpa_wyckoff_rule_baseline_output_binding_digest"]) == 64
    assert artifact["vpa_wyckoff_rule_values_digest"] == sha256_file(
        execution_environment["output_root"] / "vpa_wyckoff_rule_values.jsonl"
    )


def test_per_ticker_execution_report(execution_environment: dict) -> None:
    entries = execution_environment["artifact"][
        "per_ticker_vpa_wyckoff_rule_baseline_execution_entries"
    ]
    assert len(entries) == 1
    assert entries[0]["ticker"] == "META"
    assert entries[0]["historical_record_count"] == 2
    assert entries[0]["source_matrix_row_count"] == 30
    assert entries[0]["rule_value_row_count"] == 30
    assert entries[0]["state_value_row_count"] == 30
    assert entries[0]["meta_reduced_record_count_flag"] is True
    assert len(entries[0]["per_ticker_vpa_wyckoff_rule_baseline_execution_digest"]) == 64


def test_no_peek_coverage_and_meta_reports(execution_environment: dict) -> None:
    root = execution_environment["output_root"]
    no_peek = json.loads(
        (root / "vpa_wyckoff_no_peek_report.json").read_text(encoding="utf-8")
    )
    assert all(no_peek["no_peek_controls"].values())
    coverage = json.loads(
        (root / "vpa_wyckoff_rule_coverage_report.json").read_text(encoding="utf-8")
    )
    assert coverage["coverage_is_descriptive_not_performance_metric"] is True
    meta = json.loads(
        (root / "vpa_wyckoff_meta_limitation_report.json").read_text(encoding="utf-8")
    )
    assert meta["historical_record_count"] == 2
    assert meta["repair_or_inference_performed"] is False


CLOSED_FIELDS = [
    "expectancy_backtest_lab_candidate_created",
    "backtest_execution_authorized",
    "backtest_execution_performed",
    "model_training_authorized",
    "model_training_performed",
    "metric_computation_authorized",
    "metric_computation_performed",
    "strategy_scoring_performed",
    "runtime_migration_approved",
    "runtime_migration_active",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "provider_requests_made_in_execution",
    "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution",
    "feature_label_matrix_execution_rerun_performed",
    "feature_label_matrix_results_review_rerun_performed",
    "vpa_wyckoff_candidate_creation_rerun_performed",
    "vpa_wyckoff_candidate_review_rerun_performed",
    "vpa_wyckoff_approval_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FIELDS)
def test_closed_boundary_field_remains_false(
    execution_environment: dict, field: str
) -> None:
    assert execution_environment["artifact"][field] is False


def test_source_matrix_is_unchanged(execution_environment: dict) -> None:
    verification = execution_environment["artifact"]["source_verification"]
    assert verification["source_matrix_unchanged"] is True
    assert verification["before_source_matrix_rows_digest"] == sha256_file(
        execution_environment["source_path"]
    )
    assert verification["after_source_matrix_rows_digest"] == sha256_file(
        execution_environment["source_path"]
    )


def test_next_chain_risks_and_checklist(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["next_chain"] == execution_service.NEXT_CHAIN
    assert artifact["next_gates"] == execution_service.NEXT_GATES
    assert artifact["risk_controls"] == execution_service.RISK_CONTROLS
    assert [row["check_id"] for row in artifact["execution_checklist"]] == (
        execution_service.REQUIRED_CHECK_IDS
    )
    assert all(row["status"] == "PASS" for row in artifact["execution_checklist"])
    assert artifact["execution_summary"]["failed_checks"] == 0
    assert artifact["execution_summary"]["blocker_count"] == 0


def test_execution_digest_is_deterministic_for_fixed_timestamp(
    execution_environment: dict,
) -> None:
    second_root = execution_environment["root"] / "outputs_second"
    second = execution_service.execute_marketflow_vpa_wyckoff_rule_baseline_v1(
        output_root=second_root,
        run_timestamp_utc="2026-08-26T12:00:00Z",
    )
    first = execution_environment["artifact"]
    assert second["marketflow_vpa_wyckoff_rule_baseline_execution_digest"] == first[
        "marketflow_vpa_wyckoff_rule_baseline_execution_digest"
    ]
    assert second["vpa_wyckoff_rule_values_digest"] == first[
        "vpa_wyckoff_rule_values_digest"
    ]
    assert second["vpa_wyckoff_rule_baseline_output_binding_digest"] == first[
        "vpa_wyckoff_rule_baseline_output_binding_digest"
    ]


def test_validator_accepts_valid_artifact(execution_environment: dict) -> None:
    result = execution_service.validate_marketflow_vpa_wyckoff_rule_baseline_execution_v1(
        execution_environment["artifact"]
    )
    assert result["status"] == "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_VALID"
    assert result["failed_checks"] == 0


MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("execution_status", "WRONG"),
    ("execution_scope", "WRONG"),
    ("selected_vpa_wyckoff_package", "WRONG"),
    ("selected_matrix_package", "WRONG"),
    ("selected_feature_package", "WRONG"),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("source_vpa_wyckoff_rule_baseline_approval_digest", "0" * 64),
    ("source_candidate_review_digest", "0" * 64),
    ("source_matrix_results_review_digest", "0" * 64),
    ("source_matrix_rows_digest", "0" * 64),
    ("target_universe", ["WRONG"]),
    ("target_universe_count", 99),
    ("records_digest", "0" * 64),
    ("meta_record_count", 99),
    ("vpa_wyckoff_rule_baseline_executed", False),
    ("vpa_wyckoff_rule_values_created", False),
    ("vpa_wyckoff_state_values_created", False),
    ("vpa_wyckoff_baseline_outputs_created", False),
    ("source_matrix_row_count", 29),
    ("rule_value_row_count", 29),
    ("state_value_row_count", 29),
    ("selected_rule_family_count", 7),
    ("selected_state_family_count", 5),
    ("generated_output_count", 9),
    ("backtest_execution_performed", True),
    ("model_training_performed", True),
    ("metric_computation_performed", True),
    ("strategy_scoring_performed", True),
    ("predictive_usefulness", "accepted"),
    ("profitability", "accepted"),
    ("runtime_use", "AUTHORIZED"),
    ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"),
    ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True),
    ("provider_requests_made_in_execution", True),
    ("market_data_acquisition_performed_in_execution", True),
    ("canonical_dataset_regenerated_in_execution", True),
    ("feature_label_matrix_execution_rerun_performed", True),
    ("feature_label_matrix_results_review_rerun_performed", True),
    ("vpa_wyckoff_candidate_creation_rerun_performed", True),
    ("vpa_wyckoff_candidate_review_rerun_performed", True),
    ("vpa_wyckoff_approval_rerun_performed", True),
]


@pytest.mark.parametrize(("field", "value"), MUTATIONS)
def test_validator_rejects_contract_mutation(
    execution_environment: dict, field: str, value: object
) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid[field] = value
    with pytest.raises(
        execution_service.MarketFlowVpaWyckoffRuleBaselineExecutionError
    ):
        execution_service.validate_marketflow_vpa_wyckoff_rule_baseline_execution_v1(
            invalid
        )


MISSING_FIELDS = [
    "vpa_wyckoff_rule_values_digest",
    "vpa_wyckoff_rule_baseline_output_binding_digest",
    "risk_controls",
    "marketflow_vpa_wyckoff_rule_baseline_execution_digest",
]


@pytest.mark.parametrize("field", MISSING_FIELDS)
def test_validator_rejects_missing_required_field(
    execution_environment: dict, field: str
) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid.pop(field)
    with pytest.raises(
        execution_service.MarketFlowVpaWyckoffRuleBaselineExecutionError
    ):
        execution_service.validate_marketflow_vpa_wyckoff_rule_baseline_execution_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    [
        "target_values_absent",
        "target_classes_absent",
        "forward_returns_absent",
        "future_data_absent",
        "prediction_fields_absent",
        "strategy_score_fields_absent",
        "trade_recommendation_fields_absent",
        "broker_order_fields_absent",
        "provider_payload_fields_absent",
        "api_key_fields_absent",
    ],
)
def test_validator_rejects_leakage_control_false(
    execution_environment: dict, field: str
) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid["rule_output_schema_validation"][field] = False
    with pytest.raises(
        execution_service.MarketFlowVpaWyckoffRuleBaselineExecutionError
    ):
        execution_service.validate_marketflow_vpa_wyckoff_rule_baseline_execution_v1(
            invalid
        )


def test_validator_rejects_missing_output_manifest_entry(
    execution_environment: dict,
) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid["output_digest_manifest"] = invalid["output_digest_manifest"][:-1]
    with pytest.raises(
        execution_service.MarketFlowVpaWyckoffRuleBaselineExecutionError
    ):
        execution_service.validate_marketflow_vpa_wyckoff_rule_baseline_execution_v1(
            invalid
        )


def test_validator_rejects_missing_per_ticker_digest(
    execution_environment: dict,
) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid["per_ticker_vpa_wyckoff_rule_baseline_execution_entries"][0].pop(
        "per_ticker_vpa_wyckoff_rule_baseline_execution_digest"
    )
    with pytest.raises(
        execution_service.MarketFlowVpaWyckoffRuleBaselineExecutionError
    ):
        execution_service.validate_marketflow_vpa_wyckoff_rule_baseline_execution_v1(
            invalid
        )


def test_markdown_includes_required_sections(execution_environment: dict) -> None:
    markdown = execution_service.build_marketflow_vpa_wyckoff_rule_baseline_execution_markdown_v1(
        execution_environment["artifact"]
    )
    for section in (
        "VPA/Wyckoff Rule Baseline Execution v1",
        "Source Approval",
        "Bound Evidence",
        "Dataset and Universe",
        "Execution Scope",
        "Selected VPA/Wyckoff Package",
        "Source Matrix Inputs",
        "Rule Threshold Policy",
        "Executed Rule Families",
        "Executed Wyckoff State Families",
        "Rule Values Output",
        "State Values Output",
        "No-Peek and Leakage Controls",
        "Coverage Report",
        "Per-Ticker Report",
        "META Limitation",
        "Output Digest Manifest",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ):
        assert section in markdown


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED == (
        execution_service.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED
    )
    assert services.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY == (
        execution_service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY
    )
    assert services.execute_marketflow_vpa_wyckoff_rule_baseline_v1 is (
        execution_service.execute_marketflow_vpa_wyckoff_rule_baseline_v1
    )
