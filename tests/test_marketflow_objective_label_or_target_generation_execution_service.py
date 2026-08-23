from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import (
    marketflow_objective_label_or_target_generation_execution_service as service,
)


FIXED_TIMESTAMP = "2026-08-23T18:00:00Z"


@pytest.fixture(scope="module")
def execution(tmp_path_factory):
    output_root = tmp_path_factory.mktemp("objective-target-generation")
    artifact = service.execute_marketflow_objective_label_or_target_generation_v1(
        output_root=output_root,
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    return artifact, output_root


@pytest.fixture(scope="module")
def artifact(execution):
    return execution[0]


@pytest.fixture(scope="module")
def output_root(execution):
    return execution[1]


def test_execution_builds_fully_offline(artifact):
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False
    assert artifact["market_data_acquisition_performed_in_execution"] is False


def test_execution_blocks_when_canonical_source_is_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(service, "DEFAULT_CANONICAL_ROOT", tmp_path / "missing")
    blocked = service.execute_marketflow_objective_label_or_target_generation_v1(
        output_root=tmp_path / "output",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_BLOCKED
    assert blocked["execution_status"] == service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_BLOCKED_MISSING_OR_INVALID_CANONICAL_SOURCE
    assert blocked["objective_label_or_target_generation_performed"] is False
    assert blocked["target_values_created"] is False
    assert blocked["generated_output_count"] == 0
    assert not (tmp_path / "output").exists()


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED),
        ("execution_status", service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTED_RESEARCH_ONLY),
        ("execution_scope", service.OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_ONLY_NOT_FEATURE_GENERATION_NOT_BACKTEST),
        ("selected_label_target_package", service.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET),
        ("selected_objective_path", service.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT),
        ("source_objective_label_or_target_generation_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
        ("target_universe_count", 12),
        ("meta_record_count", 913),
        ("selected_target_family_count", 5),
        ("target_horizon_count", 3),
        ("target_profile_count", 15),
        ("target_row_count", 179190),
        ("available_target_row_count", 177090),
        ("unavailable_target_row_count", 2100),
        ("generated_output_count", 11),
    ],
)
def test_execution_contract_fields(artifact, field, expected):
    assert artifact[field] == expected


@pytest.mark.parametrize(
    "evidence_key",
    [
        "marketflow_objective_label_or_target_generation_approval_digest",
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest",
        "feature_label_matrix_digest",
        "feature_values_digest",
        "redesigned_label_values_digest",
        "records_digest",
    ],
)
def test_key_source_evidence_digests_are_bound(artifact, evidence_key):
    assert artifact["source_evidence"][evidence_key] == service._source_evidence()[evidence_key]


def test_universe_count_and_order_are_preserved(artifact):
    assert artifact["target_universe"] == service.TARGET_UNIVERSE
    assert artifact["per_ticker_record_counts"] == service.EXPECTED_RECORD_COUNTS


def test_source_digest_is_verified_before_and_after_generation(artifact):
    verification = artifact["source_verification"]
    assert verification["before_generation_records_digest"] == service.EXPECTED_RECORDS_DIGEST
    assert verification["after_generation_records_digest"] == service.EXPECTED_RECORDS_DIGEST
    assert verification["canonical_source_unchanged"] is True


@pytest.mark.parametrize(
    "field",
    [
        "objective_label_or_target_generation_performed",
        "label_or_target_generation_executed",
        "target_generation_performed",
        "target_values_created",
        "new_targets_created",
        "label_generation_performed",
    ],
)
def test_generation_execution_flags_are_true(artifact, field):
    assert artifact[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "feature_generation_authorized",
        "feature_generation_performed",
        "feature_label_matrix_created",
        "backtest_execution_authorized",
        "backtest_execution_performed",
        "model_training_authorized",
        "model_training_performed",
        "metric_computation_authorized",
        "metric_computation_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made_in_execution",
        "market_data_acquisition_performed_in_execution",
        "canonical_dataset_regenerated_in_execution",
        "candidate_creation_rerun_performed",
        "candidate_review_rerun_performed",
        "approval_rerun_performed",
    ],
)
def test_closed_execution_flags_remain_false(artifact, field):
    assert artifact[field] is False


def test_acceptance_profitability_and_runtime_remain_closed(artifact):
    assert artifact["predictive_usefulness"] == service.NOT_ACCEPTED
    assert artifact["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert artifact[field] == service.NOT_AUTHORIZED


def test_per_ticker_counts_and_digests_are_correct(artifact):
    entries = artifact["per_ticker_objective_label_or_target_generation_execution_entries"]
    assert [row["ticker"] for row in entries] == service.TARGET_UNIVERSE
    for row in entries:
        if row["ticker"] == "META":
            assert (row["historical_record_count"], row["target_row_count"], row["available_target_row_count"], row["unavailable_target_row_count"]) == (913, 13695, 13520, 175)
        else:
            assert (row["historical_record_count"], row["target_row_count"], row["available_target_row_count"], row["unavailable_target_row_count"]) == (1003, 15045, 14870, 175)
        assert len(row["per_ticker_objective_label_or_target_generation_execution_digest"]) == 64


def test_exact_generated_outputs_exist(output_root, artifact):
    assert sorted(path.name for path in output_root.iterdir()) == sorted(service.OUTPUT_FILENAMES)
    assert artifact["generated_output_names"] == service.OUTPUT_FILENAMES


def test_target_values_jsonl_schema_counts_and_unavailable_tails(output_root):
    row_count = available_count = unavailable_count = 0
    seen_profiles = set()
    ticker_unavailable = {ticker: 0 for ticker in service.TARGET_UNIVERSE}
    with (output_root / "target_values.jsonl").open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            assert set(service.TARGET_VALUES_FIELDS).issubset(row)
            assert not ({"feature_value", "prediction_value", "strategy_score", "trade_recommendation"} & set(row))
            seen_profiles.add(row["target_profile"])
            row_count += 1
            if row["target_available"]:
                available_count += 1
                assert row["target_class"] is not None
                assert row["unavailable_reason"] is None
                assert row["forward_start_date"] is not None
                assert row["forward_end_date"] is not None
            else:
                unavailable_count += 1
                ticker_unavailable[row["ticker"]] += 1
                assert row["target_value"] is None
                assert row["target_class"] is None
                assert row["unavailable_reason"] == "INSUFFICIENT_FUTURE_BARS"
                assert row["forward_start_date"] is None
                assert row["forward_end_date"] is None
    assert row_count == 179190
    assert available_count == 177090
    assert unavailable_count == 2100
    assert len(seen_profiles) == 15
    assert set(ticker_unavailable.values()) == {175}


@pytest.mark.parametrize(
    "filename",
    [
        "formula_definition_report.json",
        "availability_no_peek_rule_report.json",
        "cost_slippage_assumption_report.json",
        "target_coverage_report.json",
        "per_ticker_target_report.json",
        "meta_limitation_report.json",
    ],
)
def test_required_reports_exist_and_are_research_only(output_root, filename):
    report = json.loads((output_root / filename).read_text(encoding="utf-8"))
    assert report["output_label"] == service.OUTPUT_LABEL
    assert report["evidence_scope"] == service.EVIDENCE_SCOPE
    assert report["feature_generation_performed"] is False
    assert report["runtime_use"] == service.NOT_AUTHORIZED


def test_formula_and_assumption_reports_match_approved_design(output_root):
    formulas = json.loads((output_root / "formula_definition_report.json").read_text(encoding="utf-8"))
    assumptions = json.loads((output_root / "cost_slippage_assumption_report.json").read_text(encoding="utf-8"))
    assert formulas["approved_formula_dimensions"] == service.APPROVED_FORMULA_DIMENSIONS
    assert formulas["same_ticker_forward_ohlcv_only"] is True
    assert formulas["future_data_used_as_feature"] is False
    assert assumptions["round_trip_cost_fraction"] == "0.0010"
    assert assumptions["risk_floor_fraction"] == "0.0050"
    assert assumptions["material_move_threshold_fraction"] == "0.0150"


def test_availability_no_peek_report_has_all_rules(output_root):
    report = json.loads((output_root / "availability_no_peek_rule_report.json").read_text(encoding="utf-8"))
    assert report["availability_no_peek_rules"] == service.AVAILABILITY_NO_PEEK_RULES
    assert report["features_generated"] is False
    assert report["feature_label_matrix_created"] is False


def test_digest_manifest_has_explicit_self_reference_policy(output_root, artifact):
    report = json.loads((output_root / service.OUTPUT_FILENAMES[-1]).read_text(encoding="utf-8"))
    assert report["manifest_self_reference_policy"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    assert report["output_digest_manifest"] == artifact["output_digest_manifest"]
    assert len(report["output_digest_manifest"]) == 11
    for entry in report["output_digest_manifest"]:
        if entry["digest_kind"] == "FILE_SHA256":
            assert sha256_file(output_root / entry["filename"]) == entry["sha256"]
        else:
            assert entry["sha256"] is None


def test_target_values_and_output_binding_digests_match_outputs(output_root, artifact):
    assert sha256_file(output_root / "target_values.jsonl") == artifact["objective_label_or_target_values_digest"]
    assert artifact["objective_label_or_target_generation_output_binding_digest"] == service._output_binding_digest(artifact["output_digest_manifest"])


def test_execution_digests_are_deterministic_for_fixed_timestamp(artifact, tmp_path):
    second = service.execute_marketflow_objective_label_or_target_generation_v1(
        output_root=tmp_path / "second",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert second["marketflow_objective_label_or_target_generation_execution_digest"] == artifact["marketflow_objective_label_or_target_generation_execution_digest"]
    assert second["objective_label_or_target_generation_output_binding_digest"] == artifact["objective_label_or_target_generation_output_binding_digest"]
    assert second["objective_label_or_target_values_digest"] == artifact["objective_label_or_target_values_digest"]


def test_checklist_passes_completely(artifact):
    summary = artifact["execution_summary"]
    assert [row["check_id"] for row in artifact["execution_checklist"]] == service.REQUIRED_CHECK_IDS
    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == summary["total_checks"]
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


def test_validator_accepts_valid_artifact(artifact):
    result = service.validate_marketflow_objective_label_or_target_generation_execution_v1(artifact)
    assert result["status"] == service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_EXECUTION_VALID
    assert result["target_row_count"] == 179190


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("execution_scope", "WRONG"),
        ("selected_label_target_package", "WRONG"),
        ("selected_objective_path", "WRONG"),
        ("source_objective_label_or_target_generation_approval_digest", "0" * 64),
        ("target_universe", ["AAPL"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 914),
        ("label_or_target_generation_executed", False),
        ("target_values_created", False),
        ("new_targets_created", False),
        ("target_profile_count", 14),
        ("target_row_count", 179189),
        ("available_target_row_count", 177089),
        ("unavailable_target_row_count", 2099),
        ("generated_output_count", 10),
        ("feature_generation_performed", True),
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
        ("candidate_creation_rerun_performed", True),
        ("candidate_review_rerun_performed", True),
        ("approval_rerun_performed", True),
        ("generated_output_names", service.OUTPUT_FILENAMES[1:]),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_invalid_contract_fields(artifact, field, bad_value):
    changed = deepcopy(artifact)
    changed[field] = bad_value
    with pytest.raises(service.MarketFlowObjectiveLabelOrTargetGenerationExecutionError):
        service.validate_marketflow_objective_label_or_target_generation_execution_v1(changed)


def test_validator_rejects_missing_target_values_digest(artifact):
    changed = deepcopy(artifact)
    changed.pop("objective_label_or_target_values_digest")
    with pytest.raises(service.MarketFlowObjectiveLabelOrTargetGenerationExecutionError):
        service.validate_marketflow_objective_label_or_target_generation_execution_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(artifact):
    changed = deepcopy(artifact)
    changed["per_ticker_objective_label_or_target_generation_execution_entries"][0].pop(
        "per_ticker_objective_label_or_target_generation_execution_digest"
    )
    with pytest.raises(service.MarketFlowObjectiveLabelOrTargetGenerationExecutionError):
        service.validate_marketflow_objective_label_or_target_generation_execution_v1(changed)


def test_markdown_contains_required_sections(artifact):
    markdown = service.build_marketflow_objective_label_or_target_generation_execution_markdown_v1(artifact)
    for heading in (
        "# Objective Label or Target Generation Execution v1",
        "## Source Approval",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Execution Scope",
        "## Generated Target Families",
        "## Formula Definitions",
        "## Availability and No-Peek Controls",
        "## Cost and Slippage Assumptions",
        "## Target Values Output",
        "## Coverage Report",
        "## Per-Ticker Target Report",
        "## META Limitation",
        "## Output Digest Manifest",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown
