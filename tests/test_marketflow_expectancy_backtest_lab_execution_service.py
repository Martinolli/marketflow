from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_file
from marketflow.services import (
    marketflow_expectancy_backtest_lab_execution_service as execution_service,
)


def _matrix_row(ticker: str, index: int) -> dict:
    return {
        "canonical_record_index": index,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "date": "2022-01-03",
        "feature_bundle": {
            "GROUP_CLOSE_TO_CLOSE_RETURNS": {
                "feature_values": {"trailing_return_1": "0.01"}
            }
        },
        "forward_end_date": "2022-01-10",
        "forward_start_date": "2022-01-04",
        "records_digest": execution_service.EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_feature_package": execution_service.SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": execution_service.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_matrix_layout": execution_service.SELECTED_MATRIX_LAYOUT,
        "selected_matrix_package": execution_service.SELECTED_MATRIX_PACKAGE,
        "selected_objective_path": execution_service.SELECTED_OBJECTIVE_PATH,
        "source_profile": "RTH_FULL_SESSION_1D",
        "source_target_values_digest": execution_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "target_available": True,
        "target_class": "POSITIVE_EXPECTANCY",
        "target_family": "TARGET_EXPECTANCY_SCORE",
        "target_horizon_sessions": 5,
        "target_profile": "TARGET_EXPECTANCY_SCORE_HORIZON_5",
        "target_unavailable_reason": None,
        "target_value": "0.01",
        "ticker": ticker,
        "timeframe": "1d",
    }


def _vpa_row(matrix: dict) -> dict:
    favorable_rule = {"available": True, "tag": "demand_confirmation"}
    neutral_rule = {"available": True, "tag": "neutral"}
    rules = {
        f"VPA_RULE_{index}": favorable_rule if index == 0 else neutral_rule
        for index in range(8)
    }
    states = {
        f"WYCKOFF_STATE_{index}": {"available": True, "value": index == 0}
        for index in range(6)
    }
    return {
        **{key: matrix[key] for key in execution_service.IDENTITY_KEYS},
        "records_digest": execution_service.EXPECTED_SOURCE_RECORDS_DIGEST,
        "rule_values": rules,
        "selected_vpa_wyckoff_package": execution_service.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": execution_service.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": execution_service.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": execution_service.SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": execution_service.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": execution_service.SELECTED_OBJECTIVE_PATH,
        "source_matrix_rows_digest": execution_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "state_values": states,
        "target_available": True,
    }


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json_bytes(row) for row in rows))


@pytest.fixture(scope="module")
def execution_environment(tmp_path_factory: pytest.TempPathFactory):
    root = tmp_path_factory.mktemp("expectancy_backtest_lab_execution")
    matrix_path = root / "source" / "matrix_rows.jsonl"
    vpa_path = root / "source" / "vpa_wyckoff_rule_values.jsonl"
    matrix_rows = [_matrix_row(ticker, index) for index, ticker in enumerate(execution_service.TARGET_UNIVERSE)]
    _write_jsonl(matrix_path, matrix_rows)
    matrix_digest = sha256_file(matrix_path)
    vpa_rows = [_vpa_row(row) for row in matrix_rows]
    for row in vpa_rows:
        row["source_matrix_rows_digest"] = matrix_digest
    _write_jsonl(vpa_path, vpa_rows)
    names = [
        "DEFAULT_MATRIX_ROWS_PATH", "DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH",
        "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST", "EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST",
        "EXPECTED_SOURCE_MATRIX_ROW_COUNT", "EXPECTED_EVALUABLE_TARGET_ROW_COUNT",
        "EXPECTED_UNAVAILABLE_TARGET_ROW_COUNT", "EXPECTED_LAB_ROW_COUNTS",
        "EXPECTED_EVALUABLE_COUNTS", "EXPECTED_UNAVAILABLE_COUNTS",
    ]
    original = {name: getattr(execution_service, name) for name in names}
    replacements = {
        "DEFAULT_MATRIX_ROWS_PATH": matrix_path,
        "DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH": vpa_path,
        "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST": matrix_digest,
        "EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST": sha256_file(vpa_path),
        "EXPECTED_SOURCE_MATRIX_ROW_COUNT": 12,
        "EXPECTED_EVALUABLE_TARGET_ROW_COUNT": 12,
        "EXPECTED_UNAVAILABLE_TARGET_ROW_COUNT": 0,
        "EXPECTED_LAB_ROW_COUNTS": {ticker: 1 for ticker in execution_service.TARGET_UNIVERSE},
        "EXPECTED_EVALUABLE_COUNTS": {ticker: 1 for ticker in execution_service.TARGET_UNIVERSE},
        "EXPECTED_UNAVAILABLE_COUNTS": {ticker: 0 for ticker in execution_service.TARGET_UNIVERSE},
    }
    for name, value in replacements.items():
        setattr(execution_service, name, value)
    output_root = root / "outputs"
    artifact = execution_service.execute_marketflow_expectancy_backtest_lab_v1(
        output_root=output_root,
        run_timestamp_utc="2026-08-27T00:00:00Z",
    )
    yield {"artifact": artifact, "output_root": output_root, "root": root}
    for name, value in original.items():
        setattr(execution_service, name, value)


def test_execution_builds_offline(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False
    assert artifact["market_data_acquisition_performed_in_execution"] is False
    assert artifact["source_verification"]["streaming_read_used"] is True
    assert artifact["source_verification"]["entire_source_jsonl_loaded_into_memory"] is False


def test_execution_blocks_if_source_is_missing(
    execution_environment: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(execution_service, "DEFAULT_MATRIX_ROWS_PATH", execution_environment["root"] / "missing.jsonl")
    blocked = execution_service.execute_marketflow_expectancy_backtest_lab_v1(
        output_root=execution_environment["root"] / "blocked-missing",
        run_timestamp_utc="2026-08-27T00:00:00Z",
    )
    assert blocked["artifact_kind"] == execution_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_BLOCKED
    assert blocked["expectancy_backtest_lab_executed"] is False
    assert blocked["metric_values_computed"] is False


def test_execution_blocks_if_source_digest_is_invalid(
    execution_environment: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(execution_service, "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST", "0" * 64)
    blocked = execution_service.execute_marketflow_expectancy_backtest_lab_v1(
        output_root=execution_environment["root"] / "blocked-digest",
        run_timestamp_utc="2026-08-27T00:00:00Z",
    )
    assert blocked["execution_status"] == execution_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_BLOCKED_MISSING_OR_INVALID_SOURCE_OUTPUTS
    assert blocked["failures"][0]["failure_id"] == "matrix_rows_digest_mismatch"


CORE_FIELDS = [
    ("artifact_kind", execution_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED),
    ("execution_status", execution_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED_RESEARCH_ONLY),
    ("execution_scope", execution_service.EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY_NOT_MODEL_TRAINING_NOT_RUNTIME),
    ("selected_backtest_lab_package", execution_service.SELECTED_BACKTEST_LAB_PACKAGE),
    ("selected_vpa_wyckoff_package", execution_service.SELECTED_VPA_WYCKOFF_PACKAGE),
    ("selected_matrix_package", execution_service.SELECTED_MATRIX_PACKAGE),
    ("selected_matrix_layout", execution_service.SELECTED_MATRIX_LAYOUT),
    ("selected_feature_package", execution_service.SELECTED_FEATURE_PACKAGE),
    ("source_expectancy_backtest_lab_approval_digest", execution_service.EXPECTED_SOURCE_APPROVAL_DIGEST),
    ("source_candidate_review_digest", execution_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST),
    ("source_vpa_wyckoff_rule_values_digest", None),
    ("source_feature_label_matrix_rows_digest", None),
    ("source_target_values_digest", execution_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
    ("records_digest", execution_service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ("target_universe", execution_service.TARGET_UNIVERSE),
    ("meta_record_count", 913),
    ("expectancy_backtest_lab_executed", True),
    ("expectancy_backtest_rows_created", True),
    ("expectancy_backtest_results_created", True),
    ("backtest_execution_performed", True),
    ("metric_values_computed", True),
    ("metric_reports_created", True),
    ("metric_computation_performed", True),
    ("source_matrix_row_count", 12),
    ("expectancy_backtest_lab_row_count", 12),
    ("evaluable_target_row_count", 12),
    ("unavailable_target_row_count", 0),
    ("vpa_wyckoff_rule_row_count", 12),
    ("vpa_wyckoff_state_row_count", 12),
    ("approved_metric_family_count", 13),
    ("approved_baseline_count", 6),
    ("generated_output_count", 14),
    ("model_training_performed", False),
    ("strategy_scoring_performed", False),
    ("predictive_usefulness", "not accepted"),
    ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"),
    ("trade_recommendations_generated", False),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_execution_core_contract(execution_environment: dict, field: str, expected: object) -> None:
    artifact = execution_environment["artifact"]
    if field == "source_vpa_wyckoff_rule_values_digest":
        expected = execution_service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
    elif field == "source_feature_label_matrix_rows_digest":
        expected = execution_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
    assert artifact[field] == expected


def test_all_fourteen_outputs_exist(execution_environment: dict) -> None:
    root = execution_environment["output_root"]
    assert [row["filename"] for row in execution_environment["artifact"]["output_digest_manifest"]] == execution_service.OUTPUT_FILENAMES
    assert all((root / filename).is_file() for filename in execution_service.OUTPUT_FILENAMES)


@pytest.mark.parametrize("filename", execution_service.OUTPUT_FILENAMES)
def test_each_required_output_exists(execution_environment: dict, filename: str) -> None:
    assert (execution_environment["output_root"] / filename).is_file()


def test_backtest_row_schema_and_no_leakage(execution_environment: dict) -> None:
    path = execution_environment["output_root"] / "expectancy_backtest_rows.jsonl"
    row = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    required = {
        *execution_service.IDENTITY_KEYS, "target_available", "target_value", "target_class",
        "chronological_split", "horizon_aware_embargo_status", "research_row_available",
        "vpa_wyckoff_rule_values", "vpa_wyckoff_state_values", "baseline_references",
        "objective_context", "metric_eligibility", "research_only", "non_actionable",
    }
    assert required <= set(row)
    assert not execution_service.FORBIDDEN_ROW_FIELDS.intersection(row)
    for field in execution_service.NESTED_NO_OUTCOME_FIELDS:
        encoded = json.dumps(row[field], sort_keys=True)
        assert "target_value" not in encoded
        assert "target_class" not in encoded


def test_baselines_and_metrics_respect_blocks(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["executed_baselines"] == execution_service.APPROVED_BASELINE_IDS
    assert artifact["blocked_baseline"]["status"] == "NOT_EXECUTED_BLOCKED"
    assert artifact["approved_metric_families"] == execution_service.APPROVED_METRIC_FAMILY_IDS
    assert artifact["blocked_metric_family"]["status"] == "NOT_COMPUTED_BLOCKED"


def test_chronology_embargo_and_prior_policy(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["chronological_split_plan"]["split_policy"] == "CHRONOLOGICAL_NO_SHUFFLE"
    report = json.loads((execution_environment["output_root"] / "no_peek_report.json").read_text(encoding="utf-8"))
    assert report["prior_rate_policy"] == "VALIDATION_USES_CALIBRATION_ONLY_HOLDOUT_USES_CALIBRATION_AND_VALIDATION"
    assert report["forward_returns_used_as_features"] is False


def test_digests_and_per_ticker_entries(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert len(artifact["expectancy_backtest_rows_digest"]) == 64
    assert len(artifact["expectancy_metric_report_digest"]) == 64
    assert len(artifact["expectancy_backtest_lab_output_binding_digest"]) == 64
    assert len(artifact["per_ticker_expectancy_backtest_lab_execution_entries"]) == 12
    assert all(len(row["per_ticker_expectancy_backtest_lab_execution_digest"]) == 64 for row in artifact["per_ticker_expectancy_backtest_lab_execution_entries"])
    assert artifact["digest_manifest_self_reference_policy"] == execution_service.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE


def test_checklist_passes(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["execution_summary"]["total_checks"] == len(execution_service.REQUIRED_CHECK_IDS)
    assert artifact["execution_summary"]["failed_checks"] == 0
    assert artifact["execution_summary"]["blocker_count"] == 0


def test_execution_is_deterministic_for_fixed_timestamp(execution_environment: dict) -> None:
    second = execution_service.execute_marketflow_expectancy_backtest_lab_v1(
        output_root=execution_environment["root"] / "second-output",
        run_timestamp_utc="2026-08-27T00:00:00Z",
    )
    first = execution_environment["artifact"]
    assert second["expectancy_backtest_rows_digest"] == first["expectancy_backtest_rows_digest"]
    assert second["expectancy_metric_report_digest"] == first["expectancy_metric_report_digest"]
    assert second["expectancy_backtest_lab_output_binding_digest"] == first["expectancy_backtest_lab_output_binding_digest"]
    assert second["marketflow_expectancy_backtest_lab_execution_digest"] == first["marketflow_expectancy_backtest_lab_execution_digest"]


def test_validator_accepts_valid_artifact(execution_environment: dict) -> None:
    validation = execution_service.validate_marketflow_expectancy_backtest_lab_execution_v1(execution_environment["artifact"])
    assert validation["status"] == execution_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTION_VALID


VALIDATOR_MUTATIONS = [
    ("artifact_kind", "WRONG"), ("execution_status", "WRONG"),
    ("execution_scope", "WRONG"), ("selected_backtest_lab_package", "WRONG"),
    ("source_expectancy_backtest_lab_approval_digest", "0" * 64),
    ("source_vpa_wyckoff_rule_values_digest", "0" * 64),
    ("source_feature_label_matrix_rows_digest", "0" * 64),
    ("expectancy_backtest_lab_executed", False),
    ("expectancy_backtest_rows_created", False), ("metric_values_computed", False),
    ("metric_computation_performed", False), ("expectancy_backtest_lab_row_count", -1),
    ("generated_output_count", 13), ("model_training_performed", True),
    ("strategy_scoring_performed", True), ("predictive_usefulness", "accepted"),
    ("runtime_use", "AUTHORIZED"), ("trade_recommendations_generated", True),
    ("expectancy_backtest_rows_digest", None), ("risk_controls", []),
]


@pytest.mark.parametrize(("field", "bad_value"), VALIDATOR_MUTATIONS)
def test_validator_rejects_invalid_contract(
    execution_environment: dict, field: str, bad_value: object
) -> None:
    changed = deepcopy(execution_environment["artifact"])
    changed[field] = bad_value
    with pytest.raises(execution_service.MarketFlowExpectancyBacktestLabExecutionError):
        execution_service.validate_marketflow_expectancy_backtest_lab_execution_v1(changed)


@pytest.mark.parametrize(
    ("control", "bad_value"),
    [
        ("target_values_only_as_outcomes", False),
        ("target_classes_only_as_outcomes", False),
        ("forward_returns_used_as_features", True),
        ("prediction_fields_present", True),
        ("strategy_score_fields_present", True),
        ("trade_recommendation_fields_present", True),
        ("broker_order_fields_present", True),
        ("provider_payload_fields_present", True),
        ("api_key_fields_present", True),
    ],
)
def test_validator_rejects_leakage_flags(
    execution_environment: dict, control: str, bad_value: object
) -> None:
    changed = deepcopy(execution_environment["artifact"])
    changed["no_peek_and_leakage_controls"][control] = bad_value
    with pytest.raises(execution_service.MarketFlowExpectancyBacktestLabExecutionError):
        execution_service.validate_marketflow_expectancy_backtest_lab_execution_v1(changed)


def test_markdown_includes_required_sections(execution_environment: dict) -> None:
    markdown = execution_service.build_marketflow_expectancy_backtest_lab_execution_markdown_v1(execution_environment["artifact"])
    for section in (
        "Expectancy Backtest Lab Execution v1", "Source Approval", "Bound Evidence",
        "Chronological Split Plan", "Executed Baselines", "Computed Metric Families",
        "No-Peek and Leakage Controls", "META Limitation", "Next Chain", "Risk Controls",
        "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary", "Guardrails",
    ):
        assert section in markdown


def test_public_exports() -> None:
    assert services.execute_marketflow_expectancy_backtest_lab_v1 is execution_service.execute_marketflow_expectancy_backtest_lab_v1
    assert services.validate_marketflow_expectancy_backtest_lab_execution_v1 is execution_service.validate_marketflow_expectancy_backtest_lab_execution_v1
    assert services.build_marketflow_expectancy_backtest_lab_execution_markdown_v1 is execution_service.build_marketflow_expectancy_backtest_lab_execution_markdown_v1
