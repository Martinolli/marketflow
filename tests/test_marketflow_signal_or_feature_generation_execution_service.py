from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import (
    marketflow_signal_or_feature_generation_execution_service as execution_service,
)


FIXED_TIMESTAMP = "2026-08-24T00:00:00Z"
EXPECTED_EXECUTION_DIGEST = (
    "bcccbdc57616e7ff0c350535628a4a2b2cb752e11b4c98b0b9905fed9f9e4e60"
)
EXPECTED_OUTPUT_BINDING_DIGEST = (
    "5e0ef154d13782bc58c284b2d664f35e7f0724bb890efc2235e840df62dbf4e8"
)
EXPECTED_FEATURE_VALUES_DIGEST = (
    "7512da78cb0d222bddb2e0e5c5cb8307064ad47ebc6817025f1eaea2bcd8815e"
)


@pytest.fixture(scope="module")
def execution_result(tmp_path_factory: pytest.TempPathFactory) -> tuple[dict, Path]:
    output = tmp_path_factory.mktemp("signal_feature_execution")
    artifact = execution_service.execute_marketflow_signal_or_feature_generation_v1(
        output_root=output,
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    return artifact, output


@pytest.fixture(scope="module")
def artifact(execution_result: tuple[dict, Path]) -> dict:
    return execution_result[0]


@pytest.fixture(scope="module")
def output_root(execution_result: tuple[dict, Path]) -> Path:
    return execution_result[1]


def test_execution_builds_offline(artifact: dict) -> None:
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False
    assert artifact["market_data_acquisition_performed_in_execution"] is False
    assert artifact["canonical_dataset_regenerated_in_execution"] is False


def test_execution_blocks_if_canonical_source_is_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(execution_service, "DEFAULT_CANONICAL_ROOT", tmp_path / "missing")
    blocked = execution_service.execute_marketflow_signal_or_feature_generation_v1(
        output_root=tmp_path / "output",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert blocked["artifact_kind"] == "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_BLOCKED"
    assert blocked["execution_status"] == (
        "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_BLOCKED_MISSING_OR_INVALID_CANONICAL_SOURCE"
    )
    assert blocked["signal_or_feature_generation_performed"] is False
    assert blocked["feature_values_created"] is False
    assert blocked["generated_output_count"] == 0
    assert not (tmp_path / "output").exists()


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED"),
    ("schema_version", "marketflow_signal_or_feature_generation_execution_v1"),
    ("execution_status", "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY"),
    (
        "execution_scope",
        "SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST",
    ),
    ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
    (
        "selected_label_target_package",
        "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET",
    ),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    ("dataset_name", "expanded_universe_canonical_dataset_v1"),
    ("source_profile", "RTH_FULL_SESSION_1D"),
    ("timeframe", "1d"),
    ("date_range_start", "2022-01-01"),
    ("date_range_end", "2025-12-31"),
    ("target_universe_count", 12),
    ("total_canonical_record_count", 11946),
    ("meta_record_count", 913),
    ("non_meta_record_count", 1003),
    ("selected_signal_family_count", 7),
    ("selected_feature_family_count", 8),
    ("selected_feature_group_count", 13),
    ("feature_row_count", 155298),
    ("generated_output_count", 10),
    ("expected_output_count", 10),
    ("observed_output_count", 10),
    ("signal_or_feature_generation_performed", True),
    ("signal_generation_performed", True),
    ("feature_generation_performed", True),
    ("feature_values_created", True),
    ("signal_or_feature_generation_results_created", True),
    ("predictive_usefulness", "not accepted"),
    ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"),
    ("strategy_use", "NOT_AUTHORIZED"),
    ("paper_trading", "NOT_AUTHORIZED"),
    ("broker_execution", "NOT_AUTHORIZED"),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_required_core_field(artifact: dict, field: str, expected: object) -> None:
    assert artifact[field] == expected


BOUND_DIGESTS = {
    "source_signal_or_feature_generation_approval_digest": execution_service.EXPECTED_SOURCE_APPROVAL_DIGEST,
    "source_candidate_review_digest": execution_service.approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
    "source_candidate_digest": execution_service.approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "source_target_results_review_digest": execution_service.approval_service.SOURCE_EVIDENCE_DIGESTS[
        "marketflow_objective_label_or_target_generation_results_review_digest"
    ],
    "source_target_values_digest": execution_service.approval_service.SOURCE_EVIDENCE_DIGESTS[
        "objective_label_or_target_values_digest"
    ],
    "records_digest": execution_service.EXPECTED_RECORDS_DIGEST,
}


@pytest.mark.parametrize(("field", "expected"), list(BOUND_DIGESTS.items()))
def test_required_source_digest_is_bound(
    artifact: dict, field: str, expected: str
) -> None:
    assert artifact[field] == expected
    assert len(artifact[field]) == 64


@pytest.mark.parametrize(
    "key",
    [
        "feature_label_matrix_digest",
        "feature_values_digest",
        "redesigned_label_values_digest",
        "research_registry_approval_digest",
        "records_digest",
    ],
)
def test_prior_evidence_digest_is_bound(artifact: dict, key: str) -> None:
    assert artifact["source_evidence"][key] == execution_service._source_evidence()[key]


def test_universe_counts_and_source_verification_are_preserved(artifact: dict) -> None:
    assert artifact["target_universe"] == execution_service.TARGET_UNIVERSE
    assert artifact["per_ticker_record_counts"] == execution_service.EXPECTED_RECORD_COUNTS
    assert artifact["source_verification"]["canonical_source_unchanged"] is True
    assert artifact["source_verification"]["source_evidence_unchanged"] is True
    assert artifact["source_verification"]["before_generation_records_digest"] == (
        execution_service.EXPECTED_RECORDS_DIGEST
    )
    assert artifact["source_verification"]["after_generation_records_digest"] == (
        execution_service.EXPECTED_RECORDS_DIGEST
    )


def test_generated_family_and_group_counts_are_exact(artifact: dict) -> None:
    assert artifact["selected_signal_families"] == execution_service.SELECTED_SIGNAL_FAMILIES
    assert artifact["selected_feature_families"] == execution_service.SELECTED_FEATURE_FAMILIES
    assert artifact["selected_feature_groups"] == execution_service.SELECTED_FEATURE_GROUPS
    assert len(artifact["selected_signal_families"]) == 7
    assert len(artifact["selected_feature_families"]) == 8
    assert len(artifact["selected_feature_groups"]) == 13


def test_all_ten_outputs_exist_and_no_extra_output_exists(output_root: Path) -> None:
    assert sorted(path.name for path in output_root.iterdir()) == sorted(
        execution_service.OUTPUT_FILENAMES
    )


def test_feature_values_jsonl_has_exact_count_and_schema(output_root: Path) -> None:
    path = output_root / "feature_values.jsonl"
    with path.open("r", encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    assert len(rows) == 155298
    expected_fields = set(execution_service.FEATURE_VALUES_FIELDS)
    forbidden = set(execution_service.FORBIDDEN_FEATURE_FIELDS)
    assert all(set(row) == expected_fields for row in rows)
    assert all(not forbidden.intersection(row) for row in rows)
    assert all(row["research_only"] is True and row["non_actionable"] is True for row in rows)
    assert all(row["feature_group"] in execution_service.SELECTED_FEATURE_GROUPS for row in rows)
    assert all(row["records_digest"] == execution_service.EXPECTED_RECORDS_DIGEST for row in rows)


def test_insufficient_history_is_null_without_dropping_rows(output_root: Path) -> None:
    rows = [
        json.loads(line)
        for line in (output_root / "feature_values.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    first_return = next(
        row
        for row in rows
        if row["ticker"] == "MSFT"
        and row["canonical_record_index"] == 0
        and row["feature_group"] == "GROUP_CLOSE_TO_CLOSE_RETURNS"
    )
    assert first_return["feature_available"] is False
    assert first_return["feature_unavailable_reason"] == "FULL_GROUP_INSUFFICIENT_HISTORY"
    assert all(value is None for value in first_return["feature_values"].values())
    first_availability = next(
        row
        for row in rows
        if row["ticker"] == "MSFT"
        and row["canonical_record_index"] == 0
        and row["feature_group"] == "GROUP_DATA_AVAILABILITY_FLAGS"
    )
    assert first_availability["feature_available"] is True
    assert first_availability["feature_values"]["sufficient_history_20"] is False


def test_feature_coverage_report_is_complete(artifact: dict, output_root: Path) -> None:
    report = json.loads(
        (output_root / "feature_coverage_report.json").read_text(encoding="utf-8")
    )
    assert report["feature_row_count"] == 155298
    assert report["available_feature_row_count"] == artifact["available_feature_row_count"]
    assert report["unavailable_feature_row_count"] == artifact["unavailable_feature_row_count"]
    assert report["all_canonical_records_retained"] is True
    assert report["rows_dropped"] == 0
    assert len(report["coverage_entries"]) == 13
    assert all(row["feature_row_count"] == 11946 for row in report["coverage_entries"])


def test_feature_group_report_documents_all_formulas(output_root: Path) -> None:
    report = json.loads(
        (output_root / "feature_group_report.json").read_text(encoding="utf-8")
    )
    assert [row["feature_group"] for row in report["feature_group_entries"]] == (
        execution_service.SELECTED_FEATURE_GROUPS
    )
    assert all(row["generation_status"] == "GENERATED_RESEARCH_ONLY" for row in report["feature_group_entries"])
    assert all(row["features"] for row in report["feature_group_entries"])


def test_no_peek_report_preserves_target_separation(output_root: Path) -> None:
    report = json.loads(
        (output_root / "no_peek_feature_report.json").read_text(encoding="utf-8")
    )
    assert [row["rule_id"] for row in report["no_peek_and_target_separation_rules"]] == (
        execution_service.NO_PEEK_RULES
    )
    assert len(report["no_peek_and_target_separation_rules"]) == 10
    assert report["target_values_used_as_features"] is False
    assert report["target_classes_used_as_features"] is False
    assert report["forward_returns_used_as_features"] is False
    assert report["future_data_used_as_features"] is False
    assert report["same_date_cross_section_only"] is True
    assert report["per_ticker_history_only"] is True


def test_per_ticker_feature_report_has_exact_counts_and_digests(
    artifact: dict, output_root: Path
) -> None:
    report = json.loads(
        (output_root / "per_ticker_feature_report.json").read_text(encoding="utf-8")
    )
    entries = report["per_ticker_signal_or_feature_generation_execution_entries"]
    assert entries == artifact["per_ticker_signal_or_feature_generation_execution_entries"]
    assert [row["ticker"] for row in entries] == execution_service.TARGET_UNIVERSE
    for row in entries:
        expected_records = 913 if row["ticker"] == "META" else 1003
        expected_features = 11869 if row["ticker"] == "META" else 13039
        assert row["historical_record_count"] == expected_records
        assert row["feature_row_count"] == expected_features
        assert row["per_ticker_signal_or_feature_generation_execution_digest"] == (
            execution_service.per_ticker_signal_or_feature_generation_execution_digest_v1(
                row
            )
        )


def test_meta_limitation_report_preserves_913_without_repair(output_root: Path) -> None:
    report = json.loads(
        (output_root / "meta_limitation_report.json").read_text(encoding="utf-8")
    )
    assert report["historical_record_count"] == 913
    assert report["feature_row_count"] == 11869
    assert report["meta_reduced_record_count_flag"] is True
    assert report["no_repair"] is True
    assert report["no_backfill"] is True
    assert report["no_synthetic_rows"] is True


def test_digest_manifest_has_explicit_self_reference_policy(
    artifact: dict, output_root: Path
) -> None:
    report = json.loads(
        (output_root / "signal_feature_generation_digest_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["manifest_self_reference_policy"] == (
        "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    )
    assert report["output_digest_manifest"] == artifact["output_digest_manifest"]
    assert len(report["output_digest_manifest"]) == 10
    assert report["output_digest_manifest"][-1] == {
        "filename": "signal_feature_generation_digest_manifest.json",
        "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "sha256": None,
    }
    for entry in report["output_digest_manifest"][1:-1]:
        assert sha256_file(output_root / entry["filename"]) == entry["sha256"]


def test_generation_digests_are_deterministic(artifact: dict, output_root: Path) -> None:
    assert artifact["marketflow_signal_or_feature_generation_execution_digest"] == (
        EXPECTED_EXECUTION_DIGEST
    )
    assert artifact["signal_or_feature_generation_output_binding_digest"] == (
        EXPECTED_OUTPUT_BINDING_DIGEST
    )
    assert artifact["signal_or_feature_values_digest"] == EXPECTED_FEATURE_VALUES_DIGEST
    assert sha256_file(output_root / "feature_values.jsonl") == EXPECTED_FEATURE_VALUES_DIGEST
    assert execution_service.marketflow_signal_or_feature_generation_execution_digest_v1(
        artifact
    ) == EXPECTED_EXECUTION_DIGEST


CLOSED_FALSE_FIELDS = [
    "target_values_used_as_features",
    "target_classes_used_as_features",
    "forward_returns_used_as_features",
    "future_data_used_as_features",
    "feature_label_matrix_created",
    "backtest_execution_authorized",
    "backtest_execution_performed",
    "model_training_authorized",
    "model_training_performed",
    "metric_computation_authorized",
    "metric_computation_performed",
    "strategy_scoring_performed",
    "predictive_usefulness_acceptance_candidate_created",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "provider_requests_made_in_execution",
    "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution",
    "target_generation_execution_rerun_performed",
    "target_generation_results_review_rerun_performed",
    "candidate_creation_rerun_performed",
    "candidate_review_rerun_performed",
    "approval_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_downstream_and_external_authorities_remain_closed(
    artifact: dict, field: str
) -> None:
    assert artifact[field] is False


def test_next_chain_gates_risks_and_checklist_are_complete(artifact: dict) -> None:
    assert artifact["next_chain"] == execution_service.NEXT_CHAIN
    assert artifact["next_gates"] == execution_service.NEXT_GATES
    assert artifact["risk_controls"] == execution_service.RISK_CONTROLS
    assert len(artifact["risk_controls"]) == 27
    assert artifact["execution_summary"]["total_checks"] == 87
    assert artifact["execution_summary"]["passed_checks"] == 87
    assert artifact["execution_summary"]["failed_checks"] == 0
    assert artifact["execution_summary"]["blocker_count"] == 0
    assert all(row["status"] == "PASS" for row in artifact["execution_checklist"])


INVALID_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("execution_status", "WRONG"),
    ("execution_scope", "WRONG"),
    ("selected_feature_package", "WRONG"),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("source_signal_or_feature_generation_approval_digest", "0" * 64),
    ("source_candidate_review_digest", "0" * 64),
    ("source_target_results_review_digest", "0" * 64),
    ("source_target_values_digest", "0" * 64),
    ("target_universe", ["MSFT"]),
    ("target_universe_count", 11),
    ("records_digest", "0" * 64),
    ("meta_record_count", 1003),
    ("signal_or_feature_generation_performed", False),
    ("signal_generation_performed", False),
    ("feature_generation_performed", False),
    ("feature_values_created", False),
    ("selected_signal_families", []),
    ("selected_feature_families", []),
    ("selected_feature_groups", []),
    ("feature_row_count", 155297),
    ("generated_output_count", 9),
    ("feature_label_matrix_created", True),
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
    ("candidate_creation_rerun_performed", True),
    ("candidate_review_rerun_performed", True),
    ("approval_rerun_performed", True),
    ("target_values_used_as_features", True),
    ("target_classes_used_as_features", True),
    ("forward_returns_used_as_features", True),
    ("future_data_used_as_features", True),
    ("generated_output_names", []),
    ("risk_controls", []),
    ("signal_or_feature_values_digest", None),
    ("signal_or_feature_generation_output_binding_digest", None),
    ("marketflow_signal_or_feature_generation_execution_digest", None),
]


@pytest.mark.parametrize(("field", "value"), INVALID_MUTATIONS)
def test_validator_rejects_invalid_artifact_field(
    artifact: dict, field: str, value: object
) -> None:
    mutated = deepcopy(artifact)
    mutated[field] = value
    with pytest.raises(execution_service.MarketFlowSignalOrFeatureGenerationExecutionError):
        execution_service.validate_marketflow_signal_or_feature_generation_execution_v1(
            mutated
        )


def test_validator_rejects_changed_source_evidence(artifact: dict) -> None:
    mutated = deepcopy(artifact)
    mutated["source_evidence"]["records_digest"] = "0" * 64
    with pytest.raises(execution_service.MarketFlowSignalOrFeatureGenerationExecutionError):
        execution_service.validate_marketflow_signal_or_feature_generation_execution_v1(
            mutated
        )


def test_validator_rejects_missing_per_ticker_digest(artifact: dict) -> None:
    mutated = deepcopy(artifact)
    mutated["per_ticker_signal_or_feature_generation_execution_entries"][0].pop(
        "per_ticker_signal_or_feature_generation_execution_digest"
    )
    with pytest.raises(execution_service.MarketFlowSignalOrFeatureGenerationExecutionError):
        execution_service.validate_marketflow_signal_or_feature_generation_execution_v1(
            mutated
        )


def test_validator_accepts_valid_artifact(artifact: dict) -> None:
    result = execution_service.validate_marketflow_signal_or_feature_generation_execution_v1(
        artifact
    )
    assert result["status"] == "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_VALID"
    assert result["feature_row_count"] == 155298
    assert result["generated_output_count"] == 10
    assert result["failure_count"] == 0


def test_execution_refuses_nonempty_output_root(
    output_root: Path,
) -> None:
    with pytest.raises(execution_service.MarketFlowSignalOrFeatureGenerationExecutionError):
        execution_service.execute_marketflow_signal_or_feature_generation_v1(
            output_root=output_root,
            run_timestamp_utc=FIXED_TIMESTAMP,
        )


def test_markdown_contains_all_required_sections(artifact: dict) -> None:
    markdown = execution_service.build_marketflow_signal_or_feature_generation_execution_markdown_v1(
        artifact
    )
    sections = [
        "Signal or Feature Generation Execution v1",
        "Source Approval",
        "Bound Evidence",
        "Dataset and Universe",
        "Execution Scope",
        "Selected Feature Package",
        "Selected Target Package and Objective Path",
        "Generated Signal Families",
        "Generated Feature Families",
        "Feature Groups",
        "Feature Values Output",
        "No-Peek and Target-Separation Controls",
        "Feature Coverage Report",
        "Per-Ticker Feature Report",
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
    ]
    assert all(
        (f"# {section}" in markdown or f"## {section}" in markdown)
        for section in sections
    )
    assert "not accepted" in markdown
    assert "NOT_AUTHORIZED" in markdown


def test_public_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED == execution_service.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED
    assert services.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY == execution_service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY
    assert services.SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST == execution_service.SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST
    assert services.execute_marketflow_signal_or_feature_generation_v1 is execution_service.execute_marketflow_signal_or_feature_generation_v1
    assert services.validate_marketflow_signal_or_feature_generation_execution_v1 is execution_service.validate_marketflow_signal_or_feature_generation_execution_v1
    assert services.build_marketflow_signal_or_feature_generation_execution_markdown_v1 is execution_service.build_marketflow_signal_or_feature_generation_execution_markdown_v1
