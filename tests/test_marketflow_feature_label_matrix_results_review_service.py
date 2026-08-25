from __future__ import annotations

from copy import deepcopy
import inspect
import json
from pathlib import Path
import shutil

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_file
from marketflow.services import marketflow_feature_label_matrix_execution_service as execution
from marketflow.services import marketflow_feature_label_matrix_results_review_service as service


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json_bytes(row) for row in rows))


def _source_rows() -> tuple[list[dict], list[dict]]:
    features: list[dict] = []
    targets: list[dict] = []
    for index, date in enumerate(("2022-01-03", "2022-01-04")):
        for group_index, group in enumerate(execution.SELECTED_FEATURE_GROUPS):
            available = not (index == 0 and group_index == 0)
            features.append({
                "canonical_record_index": index,
                "dataset_name": "expanded_universe_canonical_dataset_v1",
                "date": date,
                "feature_available": available,
                "feature_family": f"FEATURE_FAMILY_{group_index}",
                "feature_formula_version": "marketflow_signal_or_feature_formula_v1",
                "feature_group": group,
                "feature_unavailable_reason": None if available else "INSUFFICIENT_HISTORY",
                "feature_values": {"value": str(index + group_index) if available else None},
                "history_lookback_available": index + 1,
                "history_lookback_required": group_index,
                "non_actionable": True,
                "records_digest": execution.EXPECTED_RECORDS_DIGEST,
                "research_only": True,
                "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
                "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
                "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
                "signal_family": f"SIGNAL_FAMILY_{group_index}",
                "source_approval_digest": "d174f5d775cb7b423121333838ab74956384068b8a46240760d399f02e229a8c",
                "source_profile": "RTH_FULL_SESSION_1D",
                "ticker": "META",
                "timeframe": "1d",
            })
        for family_index in range(5):
            for horizon in (5, 10, 20):
                available = index == 0
                targets.append({
                    "canonical_record_index": index,
                    "dataset_name": "expanded_universe_canonical_dataset_v1",
                    "date": date,
                    "formula_version": "marketflow_objective_target_formula_v1",
                    "forward_end_date": "2022-02-01" if available else None,
                    "forward_start_date": "2022-01-05" if available else None,
                    "non_actionable": True,
                    "records_digest": execution.EXPECTED_RECORDS_DIGEST,
                    "research_only": True,
                    "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
                    "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
                    "source_approval_digest": "df3ee8758ca86a04f944ed1a46ede444693833009c99692e490f6cae5e21414b",
                    "source_profile": "RTH_FULL_SESSION_1D",
                    "target_available": available,
                    "target_class": "POSITIVE" if available else None,
                    "target_family": f"TARGET_FAMILY_{family_index}",
                    "target_horizon_sessions": horizon,
                    "target_profile": f"TARGET_FAMILY_{family_index}_HORIZON_{horizon}",
                    "target_value": "0.01" if available and family_index != 3 else None,
                    "ticker": "META",
                    "timeframe": "1d",
                    "unavailable_reason": None if available else "INSUFFICIENT_FORWARD_BARS",
                })
    return features, targets


@pytest.fixture(scope="module")
def review_environment(tmp_path_factory: pytest.TempPathFactory):
    root = tmp_path_factory.mktemp("feature_label_matrix_results_review")
    feature_path = root / "source" / "feature_values.jsonl"
    target_path = root / "source" / "target_values.jsonl"
    output_root = root / "outputs"
    features, targets = _source_rows()
    _write_jsonl(feature_path, features)
    _write_jsonl(target_path, targets)

    execution_replacements = {
        "DEFAULT_FEATURE_VALUES_PATH": feature_path,
        "DEFAULT_TARGET_VALUES_PATH": target_path,
        "EXPECTED_FEATURE_VALUES_DIGEST": sha256_file(feature_path),
        "EXPECTED_TARGET_VALUES_DIGEST": sha256_file(target_path),
        "TARGET_UNIVERSE": ["META"],
        "EXPECTED_RECORD_COUNTS": {"META": 2},
        "EXPECTED_MATRIX_ROW_COUNT": 30,
        "EXPECTED_AVAILABLE_MATRIX_ROW_COUNT": 15,
        "EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT": 15,
        "EXPECTED_FEATURE_SOURCE_ROW_COUNT": 26,
        "EXPECTED_TARGET_SOURCE_ROW_COUNT": 30,
        "EXPECTED_FEATURE_GROUP_REFERENCE_COUNT": 390,
    }
    execution_original = {
        name: getattr(execution, name) for name in execution_replacements
    }
    for name, value in execution_replacements.items():
        setattr(execution, name, value)
    source = execution.execute_marketflow_feature_label_matrix_v1(
        output_root=output_root,
        run_timestamp_utc="2026-08-25T12:00:00Z",
    )

    service_replacements = {
        "DEFAULT_OUTPUT_ROOT": output_root,
        "TARGET_UNIVERSE": ["META"],
        "EXPECTED_RECORD_COUNTS": {"META": 2},
        "EXPECTED_MATRIX_ROW_COUNT": 30,
        "EXPECTED_AVAILABLE_MATRIX_ROW_COUNT": 15,
        "EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT": 15,
        "EXPECTED_FEATURE_SOURCE_ROW_COUNT": 26,
        "EXPECTED_TARGET_SOURCE_ROW_COUNT": 30,
        "EXPECTED_FEATURE_GROUP_REFERENCE_COUNT": 390,
        "EXPECTED_PER_TICKER_UNAVAILABLE_TARGET_COUNT": 15,
        "EXPECTED_SOURCE_EXECUTION_DIGEST": source["marketflow_feature_label_matrix_execution_digest"],
        "EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST": source["feature_label_matrix_output_binding_digest"],
        "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST": source["feature_label_matrix_rows_digest"],
    }
    service_original = {name: getattr(service, name) for name in service_replacements}
    for name, value in service_replacements.items():
        setattr(service, name, value)
    review = service.build_marketflow_feature_label_matrix_results_review_v1()
    yield {"review": review, "source": source, "output_root": output_root, "root": root}
    for name, value in service_original.items():
        setattr(service, name, value)
    for name, value in execution_original.items():
        setattr(execution, name, value)


def test_review_is_ready_offline_and_does_not_mutate_outputs(review_environment: dict) -> None:
    review = review_environment["review"]
    inspection = review["matrix_rows_inspection"]
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["feature_label_matrix_execution_rerun_performed"] is False
    assert inspection["matrix_output_unchanged_during_review"] is True
    assert inspection["matrix_rows_digest_before_streaming"] == inspection["matrix_rows_digest_after_streaming"]


def test_matrix_inspector_is_streaming() -> None:
    source = inspect.getsource(service._inspect_matrix_rows)
    assert ".open(" in source
    assert "for line_number, line in enumerate(handle" in source
    assert ".read_text(" not in source
    assert "list(handle)" not in source


def test_missing_outputs_fail_closed(review_environment: dict) -> None:
    blocked = service.build_marketflow_feature_label_matrix_results_review_v1(
        output_root=review_environment["root"] / "missing"
    )
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED
    assert blocked["review_status"] == service.MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert blocked["feature_label_matrix_results_review_created"] is False
    assert blocked["ready_for_vpa_wyckoff_rule_baseline_candidate"] is False
    result = service.validate_marketflow_feature_label_matrix_results_review_v1(blocked)
    assert result["status"] == service.MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED_VALID


def test_invalid_matrix_digest_fails_closed(review_environment: dict) -> None:
    copied = review_environment["root"] / "tampered"
    shutil.copytree(review_environment["output_root"], copied)
    with (copied / "matrix_rows.jsonl").open("ab") as handle:
        handle.write(b"\n")
    blocked = service.build_marketflow_feature_label_matrix_results_review_v1(output_root=copied)
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_BLOCKED
    assert blocked["feature_label_matrix_results_review_ready"] is False


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE"),
    ("schema_version", "marketflow_feature_label_matrix_results_review_v1"),
    ("review_status", "MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE_READY"),
    ("review_scope", "FEATURE_LABEL_MATRIX_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING"),
    ("selected_matrix_package", "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"),
    ("selected_matrix_layout", "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"),
    ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
    ("selected_label_target_package", "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    ("target_universe", ["META"]),
    ("target_universe_count", 1),
    ("meta_record_count", 2),
    ("expected_output_count", 12),
    ("observed_output_count", 12),
    ("output_digest_mismatch_count", 0),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_review_core_contract(review_environment: dict, field: str, expected: object) -> None:
    assert review_environment["review"][field] == expected


COUNT_FIELDS = [
    ("matrix_row_count", 30),
    ("available_matrix_row_count", 15),
    ("unavailable_target_matrix_row_count", 15),
    ("feature_group_count_per_matrix_row", 13),
    ("feature_group_reference_count", 390),
    ("feature_source_row_count", 26),
    ("target_source_row_count", 30),
    ("local_output_digest_count", 12),
    ("recorded_file_digest_match_count", 10),
]


@pytest.mark.parametrize(("field", "expected"), COUNT_FIELDS)
def test_review_counts(review_environment: dict, field: str, expected: int) -> None:
    assert review_environment["review"][field] == expected


def test_source_execution_and_all_outputs_are_digest_bound(review_environment: dict) -> None:
    review = review_environment["review"]
    source = review_environment["source"]
    assert review["source_feature_label_matrix_execution_digest"] == source["marketflow_feature_label_matrix_execution_digest"]
    assert review["source_feature_label_matrix_output_binding_digest"] == source["feature_label_matrix_output_binding_digest"]
    assert review["source_feature_label_matrix_rows_digest"] == source["feature_label_matrix_rows_digest"]
    assert list(review["local_output_digests"]) == service.EXPECTED_OUTPUT_FILENAMES
    assert len(review["output_digest_bindings"]) == 12
    assert all(row["verification_status"] == service.PASS for row in review["output_digest_bindings"])


def test_digest_manifest_special_policies_are_preserved(review_environment: dict) -> None:
    review = review_environment["review"]
    assert review["digest_manifest_self_reference_policy"] == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE
    assert review["execution_artifact_special_policy"] == "SELF_REFERENTIAL_EXECUTION_ARTIFACT"
    kinds = [row["recorded_digest_kind"] for row in review["output_digest_bindings"]]
    assert kinds[0] == "SELF_REFERENTIAL_EXECUTION_ARTIFACT"
    assert kinds[-1] == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE


@pytest.mark.parametrize("field", [
    "matrix_rows_jsonl_schema_verified", "research_only_non_actionable_verified",
    "package_binding_verified", "target_unavailable_nullability_verified",
    "non_meta_ticker_matrix_counts_verified", "meta_matrix_counts_verified",
    "matrix_output_unchanged_during_review",
])
def test_streaming_matrix_verifications_pass(review_environment: dict, field: str) -> None:
    assert review_environment["review"]["matrix_rows_inspection"][field] is True


@pytest.mark.parametrize("field", [
    "target_values_inside_feature_bundle", "target_classes_inside_feature_bundle",
    "forward_returns_inside_feature_bundle", "future_data_inside_feature_bundle",
    "prediction_fields_present", "strategy_score_fields_present",
    "trade_recommendation_fields_present", "broker_order_fields_present",
    "provider_payload_fields_present", "api_key_fields_present",
])
def test_leakage_and_sensitive_fields_are_absent(review_environment: dict, field: str) -> None:
    assert review_environment["review"][field] is False


@pytest.mark.parametrize("review_key", [
    "common_output_boundary_verified", "matrix_schema_verified",
    "feature_bundle_schema_verified", "target_profile_schema_verified",
    "matrix_coverage_report_verified", "matrix_no_peek_report_verified",
    "matrix_target_availability_report_verified", "per_ticker_matrix_report_verified",
    "meta_limitation_report_verified", "operator_summary_verified",
])
def test_all_reports_are_verified(review_environment: dict, review_key: str) -> None:
    assert review_environment["review"]["report_reviews"][review_key] is True


def test_per_ticker_entry_and_digest(review_environment: dict) -> None:
    rows = review_environment["review"]["per_ticker_feature_label_matrix_results_review_entries"]
    assert len(rows) == 1
    row = rows[0]
    assert (row["ticker"], row["historical_record_count"]) == ("META", 2)
    assert (row["matrix_row_count"], row["available_matrix_row_count"], row["unavailable_target_matrix_row_count"]) == (30, 15, 15)
    payload = deepcopy(row)
    digest = payload.pop("per_ticker_feature_label_matrix_results_review_digest")
    assert digest == semantic_digest(payload)
    assert row["review_note"] == "PRESERVE_META_LIMITATION_IN_FEATURE_LABEL_MATRIX_RESULTS_REVIEW"


@pytest.mark.parametrize("field", [
    "feature_label_matrix_results_review_created",
    "feature_label_matrix_results_review_ready",
    "ready_for_vpa_wyckoff_rule_baseline_candidate",
])
def test_review_readiness_is_open_only_for_next_candidate(review_environment: dict, field: str) -> None:
    assert review_environment["review"][field] is True


@pytest.mark.parametrize("field", [
    "vpa_wyckoff_rule_baseline_candidate_created", "expectancy_backtest_lab_candidate_created",
    "backtest_execution_authorized", "backtest_execution_performed",
    "model_training_authorized", "model_training_performed",
    "metric_computation_authorized", "metric_computation_performed",
    "strategy_scoring_performed", "trade_recommendations_generated",
    "provider_requests_made_in_review", "market_data_acquisition_performed_in_review",
    "canonical_dataset_regenerated_in_review", "feature_label_matrix_execution_rerun_performed",
    "target_generation_execution_rerun_performed", "target_generation_results_review_rerun_performed",
    "signal_feature_generation_execution_rerun_performed", "signal_feature_results_review_rerun_performed",
    "matrix_candidate_creation_rerun_performed", "matrix_candidate_review_rerun_performed",
    "matrix_approval_rerun_performed", "raw_provider_payloads_committed", "api_keys_stored_or_printed",
])
def test_closed_authority_flags_remain_false(review_environment: dict, field: str) -> None:
    assert review_environment["review"][field] is False


def test_acceptance_runtime_and_trading_remain_closed(review_environment: dict) -> None:
    review = review_environment["review"]
    assert review["predictive_usefulness"] == service.NOT_ACCEPTED
    assert review["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert review[field] == service.NOT_AUTHORIZED


def test_checklist_and_summary_are_complete(review_environment: dict) -> None:
    review = review_environment["review"]
    assert [row["check_id"] for row in review["review_checklist"]] == service.REQUIRED_CHECK_IDS
    assert len(service.REQUIRED_CHECK_IDS) == 115
    assert all(row["status"] == service.PASS for row in review["review_checklist"])
    assert review["review_summary"]["passed_checks"] == 115
    assert review["review_summary"]["failed_checks"] == 0
    assert review["review_summary"]["blocker_count"] == 0


def test_review_and_per_ticker_digests_are_deterministic(review_environment: dict) -> None:
    first = review_environment["review"]
    second = service.build_marketflow_feature_label_matrix_results_review_v1(
        output_root=review_environment["output_root"]
    )
    assert second["marketflow_feature_label_matrix_results_review_digest"] == first["marketflow_feature_label_matrix_results_review_digest"]
    assert second["per_ticker_feature_label_matrix_results_review_entries"] == first["per_ticker_feature_label_matrix_results_review_entries"]


def test_validator_accepts_ready_review(review_environment: dict) -> None:
    result = service.validate_marketflow_feature_label_matrix_results_review_v1(
        review_environment["review"]
    )
    assert result["status"] == service.MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_VALID
    assert result["passed_checks"] == 115


@pytest.mark.parametrize(("field", "value"), [
    ("artifact_kind", "WRONG"), ("review_status", "WRONG"),
    ("review_scope", "WRONG"), ("selected_matrix_package", "WRONG"),
    ("selected_matrix_layout", "WRONG"), ("source_feature_label_matrix_execution_digest", "0" * 64),
    ("source_feature_label_matrix_output_binding_digest", "0" * 64),
    ("source_feature_label_matrix_rows_digest", "0" * 64),
    ("matrix_row_count", 29), ("available_matrix_row_count", 14),
    ("unavailable_target_matrix_row_count", 16), ("feature_group_count_per_matrix_row", 12),
    ("feature_group_reference_count", 389), ("feature_label_matrix_results_review_ready", False),
    ("output_digest_mismatch_count", 1), ("output_file_inspection_performed", False),
    ("ready_for_vpa_wyckoff_rule_baseline_candidate", False),
    ("vpa_wyckoff_rule_baseline_candidate_created", True),
    ("backtest_execution_performed", True), ("model_training_performed", True),
    ("metric_computation_performed", True), ("strategy_scoring_performed", True),
    ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
    ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True), ("provider_requests_made_in_review", True),
    ("feature_label_matrix_execution_rerun_performed", True),
    ("target_values_inside_feature_bundle", True),
    ("forward_returns_inside_feature_bundle", True),
    ("future_data_inside_feature_bundle", True),
    ("provider_payload_fields_present", True),
    ("risk_controls", []),
])
def test_validator_rejects_contract_mutations(
    review_environment: dict, field: str, value: object
) -> None:
    invalid = deepcopy(review_environment["review"])
    invalid[field] = value
    with pytest.raises(service.MarketFlowFeatureLabelMatrixResultsReviewError):
        service.validate_marketflow_feature_label_matrix_results_review_v1(invalid)


def test_validator_rejects_per_ticker_digest_mutation(review_environment: dict) -> None:
    invalid = deepcopy(review_environment["review"])
    invalid["per_ticker_feature_label_matrix_results_review_entries"][0]["matrix_row_count"] = 29
    with pytest.raises(service.MarketFlowFeatureLabelMatrixResultsReviewError):
        service.validate_marketflow_feature_label_matrix_results_review_v1(invalid)


def test_markdown_contains_required_sections(review_environment: dict) -> None:
    markdown = service.build_marketflow_feature_label_matrix_results_review_markdown_v1(
        review_environment["review"]
    )
    for section in (
        "Feature-Label Matrix Results Review v1", "Source Feature-Label Matrix Execution",
        "Bound Evidence", "Dataset and Universe", "Output Verification",
        "Selected Matrix Package", "Selected Matrix Layout", "Matrix Rows Review",
        "Feature Bundle Review", "Target Profile Review", "No-Peek and Leakage Review",
        "Matrix Coverage Review", "Target Availability Review", "Per-Ticker Matrix Report Review",
        "META Limitation Review", "Output Digest Manifest", "Next Chain", "Next Gates",
        "Risk Controls", "Predictive Usefulness Boundary", "Profitability Boundary",
        "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert section in markdown


def test_writer_uses_explicit_isolated_directory(review_environment: dict) -> None:
    output_dir = review_environment["root"] / "written_review"
    result = service.write_marketflow_feature_label_matrix_results_review_v1(
        output_dir, output_root=review_environment["output_root"]
    )
    json_path = Path(result["json_path"])
    markdown_path = Path(result["markdown_path"])
    assert json_path.is_file() and json_path.parent == output_dir
    assert markdown_path.is_file() and markdown_path.parent == output_dir
    persisted = json.loads(json_path.read_text(encoding="utf-8"))
    assert persisted["marketflow_feature_label_matrix_results_review_digest"] == review_environment["review"]["marketflow_feature_label_matrix_results_review_digest"]


def test_services_export_results_review_api() -> None:
    assert services.build_marketflow_feature_label_matrix_results_review_v1 is service.build_marketflow_feature_label_matrix_results_review_v1
    assert services.validate_marketflow_feature_label_matrix_results_review_v1 is service.validate_marketflow_feature_label_matrix_results_review_v1
    assert services.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE == "MARKETFLOW_FEATURE_LABEL_MATRIX_RESULTS_REVIEW_PACKAGE"
