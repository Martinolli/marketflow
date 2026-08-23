from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.historical_data.artifacts import semantic_digest, sha256_file
from marketflow.services import (
    marketflow_objective_label_or_target_generation_results_review_service as service,
)


@pytest.fixture(scope="module")
def review():
    return service.build_marketflow_objective_label_or_target_generation_results_review_v1()


def test_results_review_builds_offline_without_mutating_source():
    root = service.DEFAULT_OUTPUT_ROOT
    before = {name: sha256_file(root / name) for name in service.EXPECTED_OUTPUT_FILENAMES}
    review = service.build_marketflow_objective_label_or_target_generation_results_review_v1()
    after = {name: sha256_file(root / name) for name in service.EXPECTED_OUTPUT_FILENAMES}
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["market_data_acquisition_performed_in_review"] is False
    assert review["target_generation_execution_rerun_performed"] is False
    assert before == after


def test_results_review_blocks_when_output_root_is_missing(tmp_path):
    blocked = service.build_marketflow_objective_label_or_target_generation_results_review_v1(
        output_root=tmp_path / "missing"
    )
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_BLOCKED
    assert blocked["review_status"] == service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert blocked["objective_label_or_target_generation_results_review_created"] is False
    assert blocked["objective_label_or_target_generation_results_review_ready"] is False
    assert blocked["ready_for_signal_or_feature_generation_candidate"] is False
    result = service.validate_marketflow_objective_label_or_target_generation_results_review_v1(blocked)
    assert result["status"] == service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_BLOCKED_VALID


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE),
        ("review_status", service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE_READY),
        ("review_scope", service.OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_GENERATION_NOT_BACKTEST),
        ("source_objective_label_or_target_generation_execution_digest", service.EXPECTED_SOURCE_EXECUTION_DIGEST),
        ("source_objective_label_or_target_generation_output_binding_digest", service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST),
        ("source_objective_label_or_target_values_digest", service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
        ("source_objective_label_or_target_generation_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("selected_label_target_package", service.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET),
        ("selected_objective_path", service.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT),
        ("target_universe_count", 12),
        ("meta_record_count", 913),
        ("expected_output_count", 11),
        ("observed_output_count", 11),
        ("output_digest_mismatch_count", 0),
        ("target_profile_count", 15),
        ("target_row_count", 179190),
        ("available_target_row_count", 177090),
        ("unavailable_target_row_count", 2100),
    ],
)
def test_review_contract_fields(review, field, expected):
    assert review[field] == expected


@pytest.mark.parametrize(
    "evidence_key",
    [
        "marketflow_objective_label_or_target_generation_execution_digest",
        "objective_label_or_target_generation_output_binding_digest",
        "objective_label_or_target_values_digest",
        "marketflow_objective_label_or_target_generation_approval_digest",
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest",
        "feature_label_matrix_digest",
        "feature_values_digest",
        "redesigned_label_values_digest",
        "records_digest",
    ],
)
def test_bound_source_evidence(review, evidence_key):
    assert review["source_evidence"][evidence_key] == service.SOURCE_EVIDENCE[evidence_key]


def test_universe_order_and_records_digest_are_preserved(review):
    assert review["target_universe"] == service.TARGET_UNIVERSE
    assert review["records_digest"] == service.execution.EXPECTED_RECORDS_DIGEST
    assert review["total_canonical_record_count"] == 11946


def test_all_local_output_hashes_are_bound_and_verified(review):
    assert list(review["local_output_digests"]) == service.EXPECTED_OUTPUT_FILENAMES
    assert len(review["output_digest_bindings"]) == 11
    assert review["recorded_file_digest_match_count"] == 9
    assert all(row["verification_status"] == service.PASS for row in review["output_digest_bindings"])
    assert review["local_output_digests"]["target_values.jsonl"] == service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST


def test_digest_manifest_special_policies_are_verified(review):
    assert review["digest_manifest_self_reference_policy"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    assert review["execution_artifact_special_policy"] == "SELF_REFERENTIAL_EXECUTION_ARTIFACT"
    assert any(row["recorded_digest_kind"] == "SELF_REFERENTIAL_EXECUTION_ARTIFACT" for row in review["output_digest_bindings"])
    assert any(row["recorded_digest_kind"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE" for row in review["output_digest_bindings"])


@pytest.mark.parametrize(
    "field",
    [
        "target_values_jsonl_schema_verified",
        "target_values_count_verified",
        "unavailable_tail_rows_null_verified",
        "per_ticker_target_counts_verified",
        "meta_limitation_verified",
    ],
)
def test_target_value_verifications_pass(review, field):
    assert review[field] is True


def test_target_values_inspection_has_exact_counts_families_and_horizons(review):
    inspection = review["target_values_inspection"]
    assert inspection["target_row_count"] == 179190
    assert inspection["available_target_row_count"] == 177090
    assert inspection["unavailable_target_row_count"] == 2100
    assert inspection["target_profile_count"] == 15
    assert inspection["target_families"] == service.TARGET_FAMILIES
    assert inspection["target_horizons"] == service.TARGET_HORIZONS
    assert inspection["forbidden_target_fields_found"] == []
    assert inspection["research_only_non_actionable_verified"] is True


def test_non_meta_and_meta_counts_are_verified(review):
    inspection = review["target_values_inspection"]
    assert inspection["non_meta_ticker_counts_verified"] is True
    assert inspection["meta_counts_verified"] is True
    assert inspection["per_ticker_target_row_counts"]["META"] == 13695
    assert inspection["per_ticker_available_target_row_counts"]["META"] == 13520
    assert inspection["per_ticker_unavailable_target_row_counts"]["META"] == 175
    for ticker in service.TARGET_UNIVERSE:
        if ticker != "META":
            assert inspection["per_ticker_target_row_counts"][ticker] == 15045
            assert inspection["per_ticker_available_target_row_counts"][ticker] == 14870
            assert inspection["per_ticker_unavailable_target_row_counts"][ticker] == 175


@pytest.mark.parametrize(
    "review_key",
    [
        "target_schema_verified",
        "formula_definition_verified",
        "availability_no_peek_rules_verified",
        "cost_slippage_assumptions_verified",
        "coverage_report_verified",
        "per_ticker_target_report_verified",
        "meta_limitation_report_verified",
        "operator_summary_verified",
        "common_output_boundary_verified",
    ],
)
def test_generated_reports_are_verified(review, review_key):
    assert review["report_reviews"][review_key] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("target_values_jsonl_review", "VERIFIED_RESEARCH_ONLY"),
        ("target_schema_review", "VERIFIED"),
        ("formula_definition_review", "VERIFIED"),
        ("availability_no_peek_rule_review", "VERIFIED"),
        ("cost_slippage_assumption_review", "VERIFIED"),
        ("target_coverage_report_review", "VERIFIED"),
        ("per_ticker_target_report_review", "VERIFIED"),
        ("meta_limitation_report_review", "VERIFIED"),
        ("operator_summary_review", "VERIFIED"),
        ("digest_manifest_review", "VERIFIED_ZERO_MISMATCHES"),
    ],
)
def test_review_status_fields(review, field, expected):
    assert review[field] == expected


def test_per_ticker_review_entries_and_digests(review):
    entries = review["per_ticker_objective_label_or_target_generation_results_review_entries"]
    assert [row["ticker"] for row in entries] == service.TARGET_UNIVERSE
    for row in entries:
        payload = deepcopy(row)
        digest = payload.pop("per_ticker_objective_label_or_target_generation_results_review_digest")
        assert digest == semantic_digest(payload)
        assert row["feature_generation_authorized"] is False
        assert row["runtime_use"] == service.NOT_AUTHORIZED
        if row["ticker"] == "META":
            assert (row["historical_record_count"], row["target_row_count"], row["available_target_row_count"], row["unavailable_target_row_count"]) == (913, 13695, 13520, 175)
            assert row["review_note"] == "PRESERVE_META_LIMITATION_IN_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW"
        else:
            assert (row["historical_record_count"], row["target_row_count"], row["available_target_row_count"], row["unavailable_target_row_count"]) == (1003, 15045, 14870, 175)


@pytest.mark.parametrize(
    "field",
    [
        "objective_label_or_target_generation_results_review_created",
        "objective_label_or_target_generation_results_review_ready",
        "ready_for_signal_or_feature_generation_candidate",
    ],
)
def test_review_readiness_flags_are_true(review, field):
    assert review[field] is True


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
        "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "target_generation_execution_rerun_performed",
        "candidate_creation_rerun_performed",
        "candidate_review_rerun_performed",
        "approval_rerun_performed",
    ],
)
def test_closed_review_flags_remain_false(review, field):
    assert review[field] is False


def test_acceptance_profitability_and_runtime_remain_closed(review):
    assert review["predictive_usefulness"] == service.NOT_ACCEPTED
    assert review["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert review[field] == service.NOT_AUTHORIZED


def test_next_chain_gates_and_risk_controls_are_defined(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_checklist_passes(review):
    assert [row["check_id"] for row in review["review_checklist"]] == service.REQUIRED_CHECK_IDS
    summary = review["review_summary"]
    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == summary["total_checks"]
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


def test_review_digest_is_deterministic(review):
    second = service.build_marketflow_objective_label_or_target_generation_results_review_v1()
    assert second["marketflow_objective_label_or_target_generation_results_review_digest"] == review["marketflow_objective_label_or_target_generation_results_review_digest"]
    assert second["per_ticker_objective_label_or_target_generation_results_review_entries"] == review["per_ticker_objective_label_or_target_generation_results_review_entries"]


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_objective_label_or_target_generation_results_review_v1(review)
    assert result["status"] == service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_VALID
    assert result["passed_checks"] == len(service.REQUIRED_CHECK_IDS)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_objective_label_or_target_generation_execution_digest", "0" * 64),
        ("source_objective_label_or_target_generation_output_binding_digest", "0" * 64),
        ("source_objective_label_or_target_values_digest", "0" * 64),
        ("source_objective_label_or_target_generation_approval_digest", "0" * 64),
        ("selected_label_target_package", "WRONG"),
        ("selected_objective_path", "WRONG"),
        ("target_universe", ["AAPL"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 914),
        ("expected_output_count", 10),
        ("observed_output_count", 10),
        ("output_digest_mismatch_count", 1),
        ("target_profile_count", 14),
        ("target_row_count", 179189),
        ("available_target_row_count", 177089),
        ("unavailable_target_row_count", 2099),
        ("objective_label_or_target_generation_results_review_created", False),
        ("objective_label_or_target_generation_results_review_ready", False),
        ("ready_for_signal_or_feature_generation_candidate", False),
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
        ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("canonical_dataset_regenerated_in_review", True),
        ("target_generation_execution_rerun_performed", True),
        ("candidate_creation_rerun_performed", True),
        ("candidate_review_rerun_performed", True),
        ("approval_rerun_performed", True),
        ("target_values_jsonl_schema_verified", False),
        ("formula_definition_review", None),
        ("target_coverage_report_review", None),
        ("per_ticker_target_report_review", None),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_invalid_review_fields(review, field, bad_value):
    changed = deepcopy(review)
    changed[field] = bad_value
    with pytest.raises(service.MarketFlowObjectiveLabelOrTargetGenerationResultsReviewError):
        service.validate_marketflow_objective_label_or_target_generation_results_review_v1(changed)


def test_validator_rejects_changed_target_values_digest_binding(review):
    changed = deepcopy(review)
    changed["local_output_digests"]["target_values.jsonl"] = "0" * 64
    with pytest.raises(service.MarketFlowObjectiveLabelOrTargetGenerationResultsReviewError):
        service.validate_marketflow_objective_label_or_target_generation_results_review_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(review):
    changed = deepcopy(review)
    changed["per_ticker_objective_label_or_target_generation_results_review_entries"][0].pop(
        "per_ticker_objective_label_or_target_generation_results_review_digest"
    )
    with pytest.raises(service.MarketFlowObjectiveLabelOrTargetGenerationResultsReviewError):
        service.validate_marketflow_objective_label_or_target_generation_results_review_v1(changed)


def test_writer_creates_json_and_markdown(review, tmp_path):
    result = service.write_marketflow_objective_label_or_target_generation_results_review_v1(tmp_path)
    json_path = tmp_path / "marketflow_objective_label_or_target_generation_results_review_v1.json"
    markdown_path = tmp_path / "marketflow_objective_label_or_target_generation_results_review_v1.md"
    assert json_path.is_file()
    assert markdown_path.is_file()
    assert json.loads(json_path.read_text(encoding="utf-8"))["marketflow_objective_label_or_target_generation_results_review_digest"] == review["marketflow_objective_label_or_target_generation_results_review_digest"]
    assert result["json_path"].endswith(json_path.name)
    assert result["markdown_path"].endswith(markdown_path.name)


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_objective_label_or_target_generation_results_review_markdown_v1(review)
    for heading in (
        "# Objective Label or Target Generation Results Review v1",
        "## Source Target Generation Execution",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Output Verification",
        "## Selected Package and Objective Path",
        "## Generated Target Families",
        "## Formula Definitions Review",
        "## Availability and No-Peek Review",
        "## Cost and Slippage Review",
        "## Target Values Review",
        "## Coverage Report Review",
        "## Per-Ticker Target Report Review",
        "## META Limitation Review",
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
