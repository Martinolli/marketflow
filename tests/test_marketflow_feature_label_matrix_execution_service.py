from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_file
from marketflow.services import marketflow_feature_label_matrix_execution_service as execution_service


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json_bytes(row) for row in rows))


def _source_rows() -> tuple[list[dict], list[dict]]:
    features: list[dict] = []
    targets: list[dict] = []
    dates = ["2022-01-03", "2022-01-04"]
    for index, date in enumerate(dates):
        for group_index, group in enumerate(execution_service.SELECTED_FEATURE_GROUPS):
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
                "records_digest": execution_service.EXPECTED_RECORDS_DIGEST,
                "research_only": True,
                "selected_feature_package": execution_service.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
                "selected_label_target_package": execution_service.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
                "selected_objective_path": execution_service.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
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
                    "records_digest": execution_service.EXPECTED_RECORDS_DIGEST,
                    "research_only": True,
                    "selected_label_target_package": execution_service.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
                    "selected_objective_path": execution_service.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
                    "source_approval_digest": "df3ee8758ca86a04f944ed1a46ede444693833009c99692e490f6cae5e21414b",
                    "source_profile": "RTH_FULL_SESSION_1D",
                    "target_available": available,
                    "target_class": "POSITIVE" if available else None,
                    "target_family": f"TARGET_FAMILY_{family_index}",
                    "target_horizon_sessions": horizon,
                    "target_profile": f"TARGET_FAMILY_{family_index}_HORIZON_{horizon}",
                    "target_value": (
                        "0.01" if available and family_index != 3 else None
                    ),
                    "ticker": "META",
                    "timeframe": "1d",
                    "unavailable_reason": None if available else "INSUFFICIENT_FORWARD_BARS",
                })
    return features, targets


@pytest.fixture(scope="module")
def execution_environment(tmp_path_factory: pytest.TempPathFactory):
    root = tmp_path_factory.mktemp("feature_label_matrix_execution")
    feature_path = root / "source" / "feature_values.jsonl"
    target_path = root / "source" / "target_values.jsonl"
    output_root = root / "outputs"
    features, targets = _source_rows()
    _write_jsonl(feature_path, features)
    _write_jsonl(target_path, targets)
    names = [
        "DEFAULT_FEATURE_VALUES_PATH", "DEFAULT_TARGET_VALUES_PATH",
        "EXPECTED_FEATURE_VALUES_DIGEST", "EXPECTED_TARGET_VALUES_DIGEST",
        "TARGET_UNIVERSE", "EXPECTED_RECORD_COUNTS", "EXPECTED_MATRIX_ROW_COUNT",
        "EXPECTED_AVAILABLE_MATRIX_ROW_COUNT",
        "EXPECTED_UNAVAILABLE_TARGET_MATRIX_ROW_COUNT",
        "EXPECTED_FEATURE_SOURCE_ROW_COUNT", "EXPECTED_TARGET_SOURCE_ROW_COUNT",
        "EXPECTED_FEATURE_GROUP_REFERENCE_COUNT",
    ]
    original = {name: getattr(execution_service, name) for name in names}
    replacements = {
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
    for name, value in replacements.items():
        setattr(execution_service, name, value)
    artifact = execution_service.execute_marketflow_feature_label_matrix_v1(
        output_root=output_root,
        run_timestamp_utc="2026-08-25T12:00:00Z",
    )
    yield {
        "artifact": artifact,
        "output_root": output_root,
        "feature_path": feature_path,
        "target_path": target_path,
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


def test_execution_blocks_if_source_output_is_missing(
    execution_environment: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        execution_service, "DEFAULT_FEATURE_VALUES_PATH",
        execution_environment["root"] / "missing.jsonl",
    )
    blocked = execution_service.execute_marketflow_feature_label_matrix_v1(
        output_root=execution_environment["root"] / "blocked_missing",
        run_timestamp_utc="2026-08-25T12:00:00Z",
    )
    assert blocked["artifact_kind"] == "MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED"
    assert blocked["execution_status"] == "MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED_MISSING_OR_INVALID_SOURCE_OUTPUTS"
    assert blocked["feature_label_matrix_created"] is False


def test_execution_blocks_if_source_digest_is_invalid(
    execution_environment: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(execution_service, "EXPECTED_TARGET_VALUES_DIGEST", "0" * 64)
    blocked = execution_service.execute_marketflow_feature_label_matrix_v1(
        output_root=execution_environment["root"] / "blocked_digest",
        run_timestamp_utc="2026-08-25T12:00:00Z",
    )
    assert blocked["artifact_kind"] == "MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED"
    assert any(row["failure_id"] == "target_values_digest_mismatch" for row in blocked["failures"])


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED"),
    ("schema_version", "marketflow_feature_label_matrix_execution_v1"),
    ("execution_status", "MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY"),
    ("execution_scope", "FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING"),
    ("selected_matrix_package", "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"),
    ("selected_matrix_layout", "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"),
    ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
    ("selected_label_target_package", "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    ("source_feature_label_matrix_approval_digest", execution_service.EXPECTED_SOURCE_APPROVAL_DIGEST),
    ("source_candidate_review_digest", execution_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST),
    ("source_matrix_candidate_digest", execution_service.EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST),
    ("records_digest", execution_service.EXPECTED_RECORDS_DIGEST),
    ("feature_label_matrix_created", True),
    ("feature_label_matrix_rows_created", True),
    ("feature_label_matrix_execution_performed", True),
    ("joined_matrix_output_created", True),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_execution_core_fields(
    execution_environment: dict, field: str, expected: object
) -> None:
    assert execution_environment["artifact"][field] == expected


COUNT_FIELDS = [
    ("matrix_row_count", 30),
    ("available_matrix_row_count", 15),
    ("unavailable_target_matrix_row_count", 15),
    ("feature_group_count_per_matrix_row", 13),
    ("feature_group_reference_count", 390),
    ("feature_source_row_count", 26),
    ("target_source_row_count", 30),
    ("generated_output_count", 12),
    ("expected_output_count", 12),
    ("observed_output_count", 12),
]


@pytest.mark.parametrize(("field", "expected"), COUNT_FIELDS)
def test_execution_counts(
    execution_environment: dict, field: str, expected: int
) -> None:
    assert execution_environment["artifact"][field] == expected


def test_execution_preserves_universe_and_meta_limitation(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["target_universe"] == ["META"]
    assert artifact["target_universe_count"] == 1
    assert artifact["meta_record_count"] == 2
    assert artifact["meta_reduced_record_count_preserved"] is True


def test_real_contract_preserves_ordered_twelve_ticker_universe() -> None:
    assert approval_universe() == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]


def approval_universe() -> list[str]:
    return list(execution_service.approval_service.TARGET_UNIVERSE)


def test_real_contract_preserves_meta_913() -> None:
    assert execution_service.approval_service.BOUND_EVIDENCE["records_digest"] == execution_service.EXPECTED_RECORDS_DIGEST
    assert execution_service.approval_service.review_service.candidate_service.TARGET_UNIVERSE[4] == "META"
    assert execution_service._canonical_source_approval()["meta_record_count"] == 913


def test_matrix_rows_jsonl_schema_and_join(execution_environment: dict) -> None:
    path = execution_environment["output_root"] / "matrix_rows.jsonl"
    first = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    assert list(first) == sorted(execution_service.MATRIX_ROW_FIELDS)
    assert first["ticker"] == "META"
    assert first["target_value"] == "0.01"
    assert first["target_class"] == "POSITIVE"
    assert first["feature_group_count"] == 13
    assert list(first["feature_bundle"]) == sorted(execution_service.SELECTED_FEATURE_GROUPS)


def test_feature_bundle_schema_and_leakage_controls(execution_environment: dict) -> None:
    first = json.loads(
        (execution_environment["output_root"] / "matrix_rows.jsonl")
        .read_text(encoding="utf-8").splitlines()[0]
    )
    for bundle_entry in first["feature_bundle"].values():
        assert set(bundle_entry) == set(execution_service.FEATURE_BUNDLE_FIELDS)
        assert not execution_service.FORBIDDEN_FEATURE_BUNDLE_FIELDS.intersection(bundle_entry)
    assert not execution_service.FORBIDDEN_MATRIX_FIELDS.intersection(first)


def test_unavailable_target_and_feature_values_are_retained(execution_environment: dict) -> None:
    rows = [json.loads(line) for line in (execution_environment["output_root"] / "matrix_rows.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(row["target_available"] is False and row["target_value"] is None and row["target_class"] is None for row in rows)
    assert any(row["feature_bundle_available"] is False and row["feature_unavailable_group_count"] == 1 for row in rows)
    assert any(row["target_available"] is True and row["target_value"] is None and row["target_class"] is not None for row in rows)


@pytest.mark.parametrize("filename", execution_service.OUTPUT_FILENAMES)
def test_exact_generated_output_exists(execution_environment: dict, filename: str) -> None:
    assert (execution_environment["output_root"] / filename).is_file()


def test_output_digest_manifest_policy_and_file_hashes(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    manifest = artifact["output_digest_manifest"]
    assert manifest[0]["digest_kind"] == "SELF_REFERENTIAL_EXECUTION_ARTIFACT"
    assert manifest[0]["sha256"] is None
    assert manifest[-1]["digest_kind"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    assert manifest[-1]["sha256"] is None
    for entry in manifest[1:-1]:
        assert entry["sha256"] == sha256_file(execution_environment["output_root"] / entry["filename"])


def test_matrix_and_output_binding_digests_are_deterministic(execution_environment: dict) -> None:
    second_root = execution_environment["root"] / "deterministic_second"
    second = execution_service.execute_marketflow_feature_label_matrix_v1(
        output_root=second_root,
        run_timestamp_utc="2026-08-25T12:00:00Z",
    )
    first = execution_environment["artifact"]
    assert second["feature_label_matrix_rows_digest"] == first["feature_label_matrix_rows_digest"]
    assert second["feature_label_matrix_output_binding_digest"] == first["feature_label_matrix_output_binding_digest"]
    assert second["marketflow_feature_label_matrix_execution_digest"] == first["marketflow_feature_label_matrix_execution_digest"]


def test_per_ticker_entry_and_digest(execution_environment: dict) -> None:
    entries = execution_environment["artifact"]["per_ticker_feature_label_matrix_execution_entries"]
    assert len(entries) == 1
    assert entries[0]["matrix_row_count"] == 30
    assert entries[0]["feature_source_row_count"] == 26
    assert entries[0]["per_ticker_feature_label_matrix_execution_digest"] == execution_service.per_ticker_feature_label_matrix_execution_digest_v1(entries[0])


CLOSED_BOUNDARY_FIELDS = [
    ("backtest_execution_authorized", False),
    ("backtest_execution_performed", False),
    ("model_training_authorized", False),
    ("model_training_performed", False),
    ("metric_computation_authorized", False),
    ("metric_computation_performed", False),
    ("strategy_scoring_performed", False),
    ("predictive_usefulness", "not accepted"),
    ("predictive_usefulness_acceptance_candidate_created", False),
    ("predictive_usefulness_acceptance_ready", False),
    ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"),
    ("strategy_use", "NOT_AUTHORIZED"),
    ("paper_trading", "NOT_AUTHORIZED"),
    ("broker_execution", "NOT_AUTHORIZED"),
    ("trade_recommendations_generated", False),
    ("provider_requests_made_in_execution", False),
    ("market_data_acquisition_performed_in_execution", False),
    ("canonical_dataset_regenerated_in_execution", False),
    ("target_generation_execution_rerun_performed", False),
    ("target_generation_results_review_rerun_performed", False),
    ("signal_feature_generation_execution_rerun_performed", False),
    ("signal_feature_results_review_rerun_performed", False),
    ("matrix_candidate_creation_rerun_performed", False),
    ("matrix_candidate_review_rerun_performed", False),
    ("approval_rerun_performed", False),
]


@pytest.mark.parametrize(("field", "expected"), CLOSED_BOUNDARY_FIELDS)
def test_execution_keeps_adjacent_authority_closed(
    execution_environment: dict, field: str, expected: object
) -> None:
    assert execution_environment["artifact"][field] == expected


def test_source_outputs_are_unchanged(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["source_verification"]["feature_source_unchanged"] is True
    assert artifact["source_verification"]["target_source_unchanged"] is True
    assert artifact["source_verification"]["source_outputs_unchanged"] is True


def test_next_chain_gates_and_risk_controls_are_defined(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["next_chain"] == execution_service.NEXT_CHAIN
    assert artifact["next_gates"] == execution_service.NEXT_GATES
    assert artifact["risk_controls"] == execution_service.RISK_CONTROLS


def test_checklist_passes(execution_environment: dict) -> None:
    artifact = execution_environment["artifact"]
    assert artifact["execution_summary"]["failed_checks"] == 0
    assert artifact["execution_summary"]["blocker_count"] == 0
    assert artifact["execution_summary"]["passed_checks"] == artifact["execution_summary"]["total_checks"]
    assert all(row["status"] == "PASS" for row in artifact["execution_checklist"])
    assert "records_digest_preserved" in {
        row["check_id"] for row in artifact["execution_checklist"]
    }


def test_validator_accepts_valid_artifact(execution_environment: dict) -> None:
    result = execution_service.validate_marketflow_feature_label_matrix_execution_v1(
        execution_environment["artifact"]
    )
    assert result["status"] == "MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTION_VALID"
    assert result["failed_checks"] == 0


VALIDATOR_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("execution_status", "WRONG"),
    ("execution_scope", "WRONG"),
    ("selected_matrix_package", "WRONG"),
    ("selected_matrix_layout", "WRONG"),
    ("selected_feature_package", "WRONG"),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("source_feature_label_matrix_approval_digest", "0" * 64),
    ("source_candidate_review_digest", "0" * 64),
    ("source_feature_values_digest", "0" * 64),
    ("source_target_values_digest", "0" * 64),
    ("target_universe", ["MSFT"]),
    ("target_universe_count", 12),
    ("records_digest", "0" * 64),
    ("meta_record_count", 913),
    ("feature_label_matrix_created", False),
    ("feature_label_matrix_rows_created", False),
    ("joined_matrix_output_created", False),
    ("matrix_row_count", 29),
    ("available_matrix_row_count", 14),
    ("unavailable_target_matrix_row_count", 16),
    ("feature_group_count_per_matrix_row", 12),
    ("feature_group_reference_count", 389),
    ("generated_output_count", 11),
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
    ("target_generation_execution_rerun_performed", True),
    ("target_generation_results_review_rerun_performed", True),
    ("signal_feature_generation_execution_rerun_performed", True),
    ("signal_feature_results_review_rerun_performed", True),
    ("matrix_candidate_creation_rerun_performed", True),
    ("matrix_candidate_review_rerun_performed", True),
    ("approval_rerun_performed", True),
    ("feature_label_matrix_rows_digest", None),
]


@pytest.mark.parametrize(("field", "value"), VALIDATOR_MUTATIONS)
def test_validator_rejects_invalid_scalar(
    execution_environment: dict, field: str, value: object
) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid[field] = value
    with pytest.raises(execution_service.MarketFlowFeatureLabelMatrixExecutionError):
        execution_service.validate_marketflow_feature_label_matrix_execution_v1(invalid)


@pytest.mark.parametrize(
    "field",
    [
        "target_values_not_inside_feature_bundle",
        "target_classes_not_inside_feature_bundle",
        "forward_returns_not_inside_feature_bundle",
        "future_data_not_inside_feature_bundle",
        "prediction_fields_absent",
        "strategy_score_fields_absent",
        "trade_recommendation_fields_absent",
    ],
)
def test_validator_rejects_schema_or_leakage_violation(
    execution_environment: dict, field: str
) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid["matrix_schema_validation"][field] = False
    with pytest.raises(execution_service.MarketFlowFeatureLabelMatrixExecutionError):
        execution_service.validate_marketflow_feature_label_matrix_execution_v1(invalid)


def test_validator_rejects_missing_output_report(execution_environment: dict) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid["output_digest_manifest"][5]["filename"] = "missing.json"
    with pytest.raises(execution_service.MarketFlowFeatureLabelMatrixExecutionError):
        execution_service.validate_marketflow_feature_label_matrix_execution_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(execution_environment: dict) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid["per_ticker_feature_label_matrix_execution_entries"][0].pop(
        "per_ticker_feature_label_matrix_execution_digest"
    )
    with pytest.raises(execution_service.MarketFlowFeatureLabelMatrixExecutionError):
        execution_service.validate_marketflow_feature_label_matrix_execution_v1(invalid)


def test_validator_rejects_missing_risk_controls(execution_environment: dict) -> None:
    invalid = deepcopy(execution_environment["artifact"])
    invalid["risk_controls"] = []
    with pytest.raises(execution_service.MarketFlowFeatureLabelMatrixExecutionError):
        execution_service.validate_marketflow_feature_label_matrix_execution_v1(invalid)


def test_markdown_includes_required_sections(execution_environment: dict) -> None:
    markdown = execution_service.build_marketflow_feature_label_matrix_execution_markdown_v1(
        execution_environment["artifact"]
    )
    for section in (
        "Feature-Label Matrix Execution v1", "Source Matrix Approval",
        "Bound Evidence", "Dataset and Universe", "Execution Scope",
        "Selected Matrix Package", "Selected Matrix Layout",
        "Source Feature and Target Outputs", "Matrix Construction Method",
        "Matrix Rows Output", "Feature Bundle Schema", "Target Profile Schema",
        "No-Peek and Leakage Controls", "Matrix Coverage Report",
        "Target Availability Report", "Per-Ticker Matrix Report",
        "META Limitation", "Output Digest Manifest", "Next Chain", "Next Gates",
        "Risk Controls", "Predictive Usefulness Boundary", "Profitability Boundary",
        "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert section in markdown


def test_services_exports_execution_api() -> None:
    assert services.execute_marketflow_feature_label_matrix_v1 is execution_service.execute_marketflow_feature_label_matrix_v1
    assert services.validate_marketflow_feature_label_matrix_execution_v1 is execution_service.validate_marketflow_feature_label_matrix_execution_v1
    assert services.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED == "MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED"
