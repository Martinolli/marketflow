from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_file
from marketflow.services import (
    marketflow_expectancy_backtest_lab_execution_service as execution,
)
from marketflow.services import (
    marketflow_expectancy_backtest_lab_results_review_service as review_service,
)


def _matrix_row(ticker: str, index: int) -> dict:
    return {
        "canonical_record_index": index,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "date": "2022-01-03",
        "feature_bundle": {"GROUP_CLOSE_TO_CLOSE_RETURNS": {"feature_values": {"trailing_return_1": "0.01"}}},
        "forward_end_date": "2022-01-10", "forward_start_date": "2022-01-04",
        "records_digest": execution.EXPECTED_SOURCE_RECORDS_DIGEST,
        "selected_feature_package": execution.SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_matrix_layout": execution.SELECTED_MATRIX_LAYOUT,
        "selected_matrix_package": execution.SELECTED_MATRIX_PACKAGE,
        "selected_objective_path": execution.SELECTED_OBJECTIVE_PATH,
        "source_profile": "RTH_FULL_SESSION_1D",
        "source_target_values_digest": execution.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "target_available": True, "target_class": "POSITIVE_EXPECTANCY",
        "target_family": "TARGET_EXPECTANCY_SCORE", "target_horizon_sessions": 5,
        "target_profile": "TARGET_EXPECTANCY_SCORE_HORIZON_5",
        "target_unavailable_reason": None, "target_value": "0.01",
        "ticker": ticker, "timeframe": "1d",
    }


def _vpa_row(matrix: dict, matrix_digest: str) -> dict:
    return {
        **{key: matrix[key] for key in execution.IDENTITY_KEYS},
        "records_digest": execution.EXPECTED_SOURCE_RECORDS_DIGEST,
        "rule_values": {f"VPA_RULE_{index}": {"available": True, "tag": "demand_confirmation" if index == 0 else "neutral"} for index in range(8)},
        "selected_vpa_wyckoff_package": execution.SELECTED_VPA_WYCKOFF_PACKAGE,
        "selected_matrix_package": execution.SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": execution.SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": execution.SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": execution.SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": execution.SELECTED_OBJECTIVE_PATH,
        "source_matrix_rows_digest": matrix_digest,
        "state_values": {f"WYCKOFF_STATE_{index}": {"available": True, "value": index == 0} for index in range(6)},
        "target_available": True,
    }


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json_bytes(row) for row in rows))


@pytest.fixture(scope="module")
def review_environment(tmp_path_factory: pytest.TempPathFactory):
    root = tmp_path_factory.mktemp("expectancy_lab_results_review")
    matrix_path = root / "source" / "matrix.jsonl"
    vpa_path = root / "source" / "vpa.jsonl"
    matrix_rows = [_matrix_row(ticker, index) for index, ticker in enumerate(execution.TARGET_UNIVERSE)]
    _write_jsonl(matrix_path, matrix_rows)
    matrix_digest = sha256_file(matrix_path)
    _write_jsonl(vpa_path, [_vpa_row(row, matrix_digest) for row in matrix_rows])
    execution_names = [
        "DEFAULT_MATRIX_ROWS_PATH", "DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH",
        "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST", "EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST",
        "EXPECTED_SOURCE_MATRIX_ROW_COUNT", "EXPECTED_EVALUABLE_TARGET_ROW_COUNT",
        "EXPECTED_UNAVAILABLE_TARGET_ROW_COUNT", "EXPECTED_LAB_ROW_COUNTS",
        "EXPECTED_EVALUABLE_COUNTS", "EXPECTED_UNAVAILABLE_COUNTS",
    ]
    execution_original = {name: getattr(execution, name) for name in execution_names}
    execution_replacements = {
        "DEFAULT_MATRIX_ROWS_PATH": matrix_path,
        "DEFAULT_VPA_WYCKOFF_RULE_VALUES_PATH": vpa_path,
        "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST": matrix_digest,
        "EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST": sha256_file(vpa_path),
        "EXPECTED_SOURCE_MATRIX_ROW_COUNT": 12,
        "EXPECTED_EVALUABLE_TARGET_ROW_COUNT": 12,
        "EXPECTED_UNAVAILABLE_TARGET_ROW_COUNT": 0,
        "EXPECTED_LAB_ROW_COUNTS": {ticker: 1 for ticker in execution.TARGET_UNIVERSE},
        "EXPECTED_EVALUABLE_COUNTS": {ticker: 1 for ticker in execution.TARGET_UNIVERSE},
        "EXPECTED_UNAVAILABLE_COUNTS": {ticker: 0 for ticker in execution.TARGET_UNIVERSE},
    }
    for name, value in execution_replacements.items():
        setattr(execution, name, value)
    output_root = root / "execution_outputs"
    execution_artifact = execution.execute_marketflow_expectancy_backtest_lab_v1(
        output_root=output_root, run_timestamp_utc="2026-08-27T00:00:00Z"
    )
    review_names = [
        "DEFAULT_OUTPUT_ROOT", "EXPECTED_SOURCE_EXECUTION_DIGEST",
        "EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST", "EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST",
        "EXPECTED_SOURCE_METRIC_REPORT_DIGEST", "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST",
        "EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST", "EXPECTED_ROW_COUNT",
        "EXPECTED_EVALUABLE_COUNT", "EXPECTED_UNAVAILABLE_COUNT",
        "EXPECTED_EMBARGOED_COUNT", "EXPECTED_AGGREGATE_METRIC_ELIGIBLE_COUNT",
        "EXPECTED_LAB_ROW_COUNTS", "EXPECTED_EVALUABLE_COUNTS", "EXPECTED_UNAVAILABLE_COUNTS",
    ]
    review_original = {name: getattr(review_service, name) for name in review_names}
    review_replacements = {
        "DEFAULT_OUTPUT_ROOT": output_root,
        "EXPECTED_SOURCE_EXECUTION_DIGEST": execution_artifact["marketflow_expectancy_backtest_lab_execution_digest"],
        "EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST": execution_artifact["expectancy_backtest_lab_output_binding_digest"],
        "EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST": execution_artifact["expectancy_backtest_rows_digest"],
        "EXPECTED_SOURCE_METRIC_REPORT_DIGEST": execution_artifact["expectancy_metric_report_digest"],
        "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST": matrix_digest,
        "EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST": execution_replacements["EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST"],
        "EXPECTED_ROW_COUNT": 12, "EXPECTED_EVALUABLE_COUNT": 12,
        "EXPECTED_UNAVAILABLE_COUNT": 0, "EXPECTED_EMBARGOED_COUNT": 0,
        "EXPECTED_AGGREGATE_METRIC_ELIGIBLE_COUNT": 12,
        "EXPECTED_LAB_ROW_COUNTS": {ticker: 1 for ticker in execution.TARGET_UNIVERSE},
        "EXPECTED_EVALUABLE_COUNTS": {ticker: 1 for ticker in execution.TARGET_UNIVERSE},
        "EXPECTED_UNAVAILABLE_COUNTS": {ticker: 0 for ticker in execution.TARGET_UNIVERSE},
    }
    for name, value in review_replacements.items():
        setattr(review_service, name, value)
    review = review_service.build_marketflow_expectancy_backtest_lab_results_review_v1()
    yield {"review": review, "root": root, "output_root": output_root}
    for name, value in review_original.items():
        setattr(review_service, name, value)
    for name, value in execution_original.items():
        setattr(execution, name, value)


def test_results_review_builds_offline(review_environment: dict) -> None:
    review = review_environment["review"]
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["market_data_acquisition_performed_in_review"] is False


def test_results_review_blocks_when_output_root_missing(review_environment: dict) -> None:
    blocked = review_service.build_marketflow_expectancy_backtest_lab_results_review_v1(
        output_root=review_environment["root"] / "missing"
    )
    assert blocked["artifact_kind"] == review_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_BLOCKED
    assert blocked["expectancy_backtest_lab_results_review_created"] is False
    assert blocked["ready_for_predictive_usefulness_reassessment_using_expectancy_lab_evidence"] is False


def test_results_review_uses_streaming_row_inspection(review_environment: dict) -> None:
    inspection = review_environment["review"]["backtest_rows_streaming_inspection"]
    assert inspection["streaming_read_used"] is True
    assert inspection["entire_backtest_rows_jsonl_loaded_into_memory"] is False


CORE_FIELDS = [
    ("artifact_kind", review_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE),
    ("review_status", review_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_PACKAGE_READY),
    ("review_scope", review_service.EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_ONLY_NOT_REASSESSMENT_NOT_RUNTIME),
    ("source_expectancy_backtest_lab_execution_digest", None),
    ("source_expectancy_backtest_lab_output_binding_digest", None),
    ("source_expectancy_backtest_rows_digest", None),
    ("source_expectancy_metric_report_digest", None),
    ("source_expectancy_backtest_lab_approval_digest", review_service.EXPECTED_SOURCE_APPROVAL_DIGEST),
    ("selected_backtest_lab_package", execution.SELECTED_BACKTEST_LAB_PACKAGE),
    ("selected_vpa_wyckoff_package", execution.SELECTED_VPA_WYCKOFF_PACKAGE),
    ("selected_matrix_package", execution.SELECTED_MATRIX_PACKAGE),
    ("selected_matrix_layout", execution.SELECTED_MATRIX_LAYOUT),
    ("selected_feature_package", execution.SELECTED_FEATURE_PACKAGE),
    ("source_target_values_digest", review_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
    ("records_digest", review_service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ("target_universe", review_service.TARGET_UNIVERSE),
    ("meta_record_count", 913), ("expected_output_count", 14),
    ("observed_output_count", 14), ("output_digest_mismatch_count", 0),
    ("backtest_rows_jsonl_schema_verified", True),
    ("expectancy_backtest_lab_row_count", 12), ("evaluable_target_row_count", 12),
    ("unavailable_target_row_count", 0),
    ("embargoed_cross_split_forward_horizon_row_count", 0),
    ("aggregate_metric_eligible_row_count", 12),
    ("approved_metric_family_count", 13), ("blocked_metric_family_count", 1),
    ("approved_baseline_count", 6), ("blocked_baseline_count", 1),
    ("blocked_randomized_null_reference_executed", False),
    ("blocked_bootstrap_metric_computed", False),
    ("chronological_split_policy", "CHRONOLOGICAL_NO_SHUFFLE"),
    ("horizon_aware_embargo_status", "APPLIED_AS_RESEARCH_CONTROL_NOT_MODEL_TRAINING"),
    ("target_values_used_as_predictors", False), ("target_classes_used_as_predictors", False),
    ("forward_returns_used_as_features", False), ("prediction_fields_present", False),
    ("strategy_score_fields_present", False), ("trade_recommendation_fields_present", False),
    ("broker_order_fields_present", False), ("provider_payload_fields_present", False),
    ("api_key_fields_present", False), ("expectancy_backtest_lab_results_review_created", True),
    ("expectancy_backtest_lab_results_review_ready", True),
    ("ready_for_predictive_usefulness_reassessment_using_expectancy_lab_evidence", True),
    ("predictive_usefulness_reassessment_created", False),
    ("predictive_usefulness_acceptance_candidate_created", False),
    ("model_training_performed", False), ("strategy_scoring_performed", False),
    ("predictive_usefulness", "not accepted"), ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"), ("trade_recommendations_generated", False),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_review_core_contract(review_environment: dict, field: str, expected: object) -> None:
    review = review_environment["review"]
    dynamic = {
        "source_expectancy_backtest_lab_execution_digest": review_service.EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_expectancy_backtest_lab_output_binding_digest": review_service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_expectancy_backtest_rows_digest": review_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_expectancy_metric_report_digest": review_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
    }
    assert review[field] == dynamic.get(field, expected)


@pytest.mark.parametrize(
    "field",
    [
        "result_summary_verified", "metric_report_verified",
        "baseline_comparison_report_verified", "vpa_wyckoff_rule_alignment_report_verified",
        "abstention_quality_report_verified", "per_ticker_backtest_report_verified",
        "chronological_split_report_verified", "meta_limitation_report_verified",
        "no_peek_report_verified", "operator_summary_verified",
    ],
)
def test_each_report_is_verified(review_environment: dict, field: str) -> None:
    assert review_environment["review"][field] is True


def test_output_digests_and_self_reference_policy(review_environment: dict) -> None:
    review = review_environment["review"]
    assert review["local_output_digests"]["expectancy_backtest_rows.jsonl"] == review_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
    assert review["local_output_digests"]["expectancy_metric_report.json"] == review_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
    assert review["digest_manifest_self_reference_policy"] == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE
    assert all(row["digest_verified"] for row in review["output_digest_bindings"])


def test_per_ticker_entries_and_digests(review_environment: dict) -> None:
    entries = review_environment["review"]["per_ticker_expectancy_backtest_lab_results_review_entries"]
    assert [row["ticker"] for row in entries] == review_service.TARGET_UNIVERSE
    assert all(row["per_ticker_expectancy_backtest_lab_results_review_digest"] == review_service.per_ticker_expectancy_backtest_lab_results_review_digest_v1(row) for row in entries)
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True


def test_next_chain_risk_controls_and_checklist(review_environment: dict) -> None:
    review = review_environment["review"]
    assert review["next_chain"] == review_service.NEXT_CHAIN
    assert review["next_gates"] == review_service.NEXT_GATES
    assert review["risk_controls"] == review_service.RISK_CONTROLS
    assert review["review_summary"]["failed_checks"] == 0
    assert review["review_summary"]["blocker_count"] == 0


def test_review_and_per_ticker_digests_are_deterministic(review_environment: dict) -> None:
    review = review_environment["review"]
    second = review_service.build_marketflow_expectancy_backtest_lab_results_review_v1(
        output_root=review_environment["output_root"]
    )
    assert second["marketflow_expectancy_backtest_lab_results_review_digest"] == review["marketflow_expectancy_backtest_lab_results_review_digest"]
    assert [row["per_ticker_expectancy_backtest_lab_results_review_digest"] for row in second["per_ticker_expectancy_backtest_lab_results_review_entries"]] == [row["per_ticker_expectancy_backtest_lab_results_review_digest"] for row in review["per_ticker_expectancy_backtest_lab_results_review_entries"]]


def test_validator_accepts_valid_review(review_environment: dict) -> None:
    result = review_service.validate_marketflow_expectancy_backtest_lab_results_review_v1(review_environment["review"])
    assert result["status"] == review_service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_RESULTS_REVIEW_VALID


MUTATIONS = [
    ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("review_scope", "WRONG"),
    ("source_expectancy_backtest_lab_execution_digest", "0" * 64),
    ("source_expectancy_backtest_rows_digest", "0" * 64),
    ("source_expectancy_metric_report_digest", "0" * 64),
    ("selected_backtest_lab_package", "WRONG"),
    ("expectancy_backtest_lab_row_count", -1), ("output_digest_mismatch_count", 1),
    ("expectancy_backtest_lab_results_review_ready", False),
    ("predictive_usefulness_reassessment_created", True),
    ("model_training_performed", True), ("strategy_scoring_performed", True),
    ("predictive_usefulness", "accepted"), ("runtime_use", "AUTHORIZED"),
    ("trade_recommendations_generated", True), ("metric_report_verified", False),
    ("risk_controls", []),
]


@pytest.mark.parametrize(("field", "bad_value"), MUTATIONS)
def test_validator_rejects_invalid_contract(
    review_environment: dict, field: str, bad_value: object
) -> None:
    changed = deepcopy(review_environment["review"])
    changed[field] = bad_value
    with pytest.raises(review_service.MarketFlowExpectancyBacktestLabResultsReviewError):
        review_service.validate_marketflow_expectancy_backtest_lab_results_review_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "target_values_used_as_predictors", "target_classes_used_as_predictors",
        "forward_returns_used_as_features", "prediction_fields_present",
        "strategy_score_fields_present", "trade_recommendation_fields_present",
        "broker_order_fields_present", "provider_payload_fields_present", "api_key_fields_present",
    ],
)
def test_validator_rejects_leakage_flags(review_environment: dict, field: str) -> None:
    changed = deepcopy(review_environment["review"])
    changed[field] = True
    with pytest.raises(review_service.MarketFlowExpectancyBacktestLabResultsReviewError):
        review_service.validate_marketflow_expectancy_backtest_lab_results_review_v1(changed)


def test_writer_round_trips_review(review_environment: dict) -> None:
    result = review_service.write_marketflow_expectancy_backtest_lab_results_review_v1(
        review_environment["root"] / "written_review",
        output_root=review_environment["output_root"],
    )
    restored = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
    assert restored == result["review"]
    assert "Expectancy Backtest Lab Results Review v1" in Path(result["markdown_path"]).read_text(encoding="utf-8")


def test_markdown_includes_required_sections(review_environment: dict) -> None:
    markdown = review_service.build_marketflow_expectancy_backtest_lab_results_review_markdown_v1(review_environment["review"])
    for section in (
        "Expectancy Backtest Lab Results Review v1", "Source Expectancy Backtest Lab Execution",
        "Bound Evidence", "Output Verification", "Backtest Rows Review", "Metric Report Review",
        "Baseline Comparison Review", "VPA/Wyckoff Rule Alignment Review",
        "No-Peek and Leakage Review", "Per-Ticker Backtest Review", "META Limitation Review",
        "Next Chain", "Next Gates", "Risk Controls", "Predictive Usefulness Boundary",
        "Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert section in markdown


def test_public_exports() -> None:
    assert services.build_marketflow_expectancy_backtest_lab_results_review_v1 is review_service.build_marketflow_expectancy_backtest_lab_results_review_v1
    assert services.validate_marketflow_expectancy_backtest_lab_results_review_v1 is review_service.validate_marketflow_expectancy_backtest_lab_results_review_v1
    assert services.write_marketflow_expectancy_backtest_lab_results_review_v1 is review_service.write_marketflow_expectancy_backtest_lab_results_review_v1
