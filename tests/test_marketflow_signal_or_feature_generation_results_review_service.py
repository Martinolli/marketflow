from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import semantic_digest, sha256_file
from marketflow.services import (
    marketflow_signal_or_feature_generation_results_review_service as service,
)


EXPECTED_REVIEW_DIGEST = (
    "8de3cfa3d4543a05956c4d9e55940525417336ffcbe523c674b43924fd22ddb7"
)


@pytest.fixture(scope="module")
def review():
    return service.build_marketflow_signal_or_feature_generation_results_review_v1()


def test_results_review_builds_offline_without_mutating_source():
    root = service.DEFAULT_OUTPUT_ROOT
    before = {
        name: sha256_file(root / name) for name in service.EXPECTED_OUTPUT_FILENAMES
    }
    review = service.build_marketflow_signal_or_feature_generation_results_review_v1()
    after = {
        name: sha256_file(root / name) for name in service.EXPECTED_OUTPUT_FILENAMES
    }
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["market_data_acquisition_performed_in_review"] is False
    assert review["signal_or_feature_generation_execution_rerun_performed"] is False
    assert before == after


def test_results_review_blocks_when_output_root_is_missing(tmp_path):
    blocked = service.build_marketflow_signal_or_feature_generation_results_review_v1(
        output_root=tmp_path / "missing"
    )
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED
    assert blocked["review_status"] == service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert blocked["signal_or_feature_generation_results_review_created"] is False
    assert blocked["signal_or_feature_generation_results_review_ready"] is False
    assert blocked["ready_for_feature_label_matrix_candidate"] is False
    assert blocked["feature_label_matrix_candidate_created"] is False
    result = service.validate_marketflow_signal_or_feature_generation_results_review_v1(
        blocked
    )
    assert result["status"] == service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_VALID


def test_results_review_blocks_when_output_inventory_is_incomplete(tmp_path):
    blocked = service.build_marketflow_signal_or_feature_generation_results_review_v1(
        output_root=tmp_path
    )
    assert blocked["review_status"] == service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert blocked["failures"][0]["failure_id"] == "output_file_inventory_mismatch"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE),
        ("review_status", service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY),
        ("review_scope", service.SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST),
        ("source_signal_or_feature_generation_execution_digest", service.EXPECTED_SOURCE_EXECUTION_DIGEST),
        ("source_signal_or_feature_generation_output_binding_digest", service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST),
        ("source_signal_or_feature_values_digest", service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST),
        ("source_signal_or_feature_generation_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("selected_feature_package", service.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET),
        ("selected_label_target_package", service.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET),
        ("selected_objective_path", service.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT),
        ("target_universe_count", 12),
        ("meta_record_count", 913),
        ("expected_output_count", 10),
        ("observed_output_count", 10),
        ("output_digest_mismatch_count", 0),
        ("selected_signal_family_count", 7),
        ("selected_feature_family_count", 8),
        ("selected_feature_group_count", 13),
        ("feature_row_count", 155298),
        ("available_feature_row_count", 155142),
        ("unavailable_feature_row_count", 156),
    ],
)
def test_review_contract_fields(review, field, expected):
    assert review[field] == expected


@pytest.mark.parametrize(
    "evidence_key",
    [
        "marketflow_signal_or_feature_generation_execution_digest",
        "signal_or_feature_generation_output_binding_digest",
        "signal_or_feature_values_digest",
        "marketflow_signal_or_feature_generation_approval_digest",
        "marketflow_signal_or_feature_generation_candidate_operator_review_digest",
        "marketflow_signal_or_feature_generation_candidate_v1_digest",
        "marketflow_objective_label_or_target_generation_results_review_digest",
        "marketflow_objective_label_or_target_generation_execution_digest",
        "objective_label_or_target_values_digest",
        "feature_label_matrix_digest",
        "feature_values_digest",
        "redesigned_label_values_digest",
        "research_registry_approval_digest",
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
    assert len(review["output_digest_bindings"]) == 10
    assert review["recorded_file_digest_match_count"] == 8
    assert review["local_output_digest_count"] == 10
    assert all(
        row["verification_status"] == service.PASS
        for row in review["output_digest_bindings"]
    )
    assert review["local_output_digests"]["feature_values.jsonl"] == service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST


def test_digest_manifest_special_policies_are_verified(review):
    assert review["digest_manifest_self_reference_policy"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    assert review["execution_artifact_special_policy"] == "SELF_REFERENTIAL_EXECUTION_ARTIFACT"
    kinds = {row["recorded_digest_kind"] for row in review["output_digest_bindings"]}
    assert "SELF_REFERENTIAL_EXECUTION_ARTIFACT" in kinds
    assert "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE" in kinds


@pytest.mark.parametrize(
    "field",
    [
        "feature_values_jsonl_schema_verified",
        "feature_values_count_verified",
        "per_ticker_feature_counts_verified",
        "meta_limitation_verified",
    ],
)
def test_feature_value_verifications_pass(review, field):
    assert review[field] is True


def test_feature_values_inspection_has_exact_counts_and_families(review):
    inspection = review["feature_values_inspection"]
    assert inspection["feature_row_count"] == 155298
    assert inspection["available_feature_row_count"] == 155142
    assert inspection["unavailable_feature_row_count"] == 156
    assert inspection["signal_families"] == service.SIGNAL_FAMILIES
    assert inspection["feature_families"] == service.FEATURE_FAMILIES
    assert inspection["feature_groups"] == service.FEATURE_GROUPS
    assert inspection["forbidden_feature_fields_found"] == []
    assert inspection["research_only_non_actionable_verified"] is True
    assert inspection["package_binding_verified"] is True


@pytest.mark.parametrize(
    "field",
    [
        "target_values_used_as_features",
        "target_classes_used_as_features",
        "forward_returns_used_as_features",
        "future_data_used_as_features",
        "prediction_fields_present",
        "strategy_score_fields_present",
        "trade_recommendation_fields_present",
    ],
)
def test_no_peek_and_forbidden_feature_fields_are_absent(review, field):
    assert review[field] is False


def test_non_meta_and_meta_counts_are_verified(review):
    inspection = review["feature_values_inspection"]
    assert inspection["non_meta_ticker_feature_counts_verified"] is True
    assert inspection["meta_feature_counts_verified"] is True
    assert inspection["per_ticker_feature_row_counts"]["META"] == 11869
    assert inspection["per_ticker_available_feature_row_counts"]["META"] == 11856
    assert inspection["per_ticker_unavailable_feature_row_counts"]["META"] == 13
    for ticker in service.TARGET_UNIVERSE:
        if ticker != "META":
            assert inspection["per_ticker_feature_row_counts"][ticker] == 13039
            assert inspection["per_ticker_available_feature_row_counts"][ticker] == 13026
            assert inspection["per_ticker_unavailable_feature_row_counts"][ticker] == 13


@pytest.mark.parametrize(
    "review_key",
    [
        "common_output_boundary_verified",
        "schema_report_verified",
        "coverage_report_verified",
        "feature_group_report_verified",
        "no_peek_feature_report_verified",
        "per_ticker_feature_report_verified",
        "meta_limitation_report_verified",
        "operator_summary_verified",
    ],
)
def test_generated_reports_are_verified(review, review_key):
    assert review["report_reviews"][review_key] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_values_jsonl_review", "VERIFIED_RESEARCH_ONLY"),
        ("signal_feature_schema_review", "VERIFIED"),
        ("feature_coverage_report_review", "VERIFIED"),
        ("feature_group_report_review", "VERIFIED"),
        ("no_peek_feature_report_review", "VERIFIED"),
        ("per_ticker_feature_report_review", "VERIFIED"),
        ("meta_limitation_report_review", "VERIFIED"),
        ("operator_summary_review", "VERIFIED"),
        ("digest_manifest_review", "VERIFIED_ZERO_MISMATCHES"),
    ],
)
def test_review_status_fields(review, field, expected):
    assert review[field] == expected


def test_per_ticker_review_entries_and_digests(review):
    entries = review[
        "per_ticker_signal_or_feature_generation_results_review_entries"
    ]
    assert [row["ticker"] for row in entries] == service.TARGET_UNIVERSE
    for row in entries:
        payload = deepcopy(row)
        digest = payload.pop(
            "per_ticker_signal_or_feature_generation_results_review_digest"
        )
        assert digest == semantic_digest(payload)
        assert row["feature_label_matrix_created"] is False
        assert row["runtime_use"] == service.NOT_AUTHORIZED
        if row["ticker"] == "META":
            assert (
                row["historical_record_count"], row["feature_row_count"],
                row["available_feature_row_count"], row["unavailable_feature_row_count"],
            ) == (913, 11869, 11856, 13)
            assert row["review_note"] == "PRESERVE_META_LIMITATION_IN_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW"
        else:
            assert (
                row["historical_record_count"], row["feature_row_count"],
                row["available_feature_row_count"], row["unavailable_feature_row_count"],
            ) == (1003, 13039, 13026, 13)


@pytest.mark.parametrize(
    "field",
    [
        "signal_or_feature_generation_results_review_created",
        "signal_or_feature_generation_results_review_ready",
        "ready_for_feature_label_matrix_candidate",
    ],
)
def test_review_readiness_flags_are_true(review, field):
    assert review[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "feature_label_matrix_candidate_created",
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
        "signal_or_feature_generation_execution_rerun_performed",
        "target_generation_execution_rerun_performed",
        "target_generation_results_review_rerun_performed",
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
    assert len(review["next_chain"]) == 9
    assert review["next_gates"] == service.NEXT_GATES
    assert len(review["next_gates"]) == 9
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(review["risk_controls"]) == 28


def test_checklist_passes(review):
    assert [row["check_id"] for row in review["review_checklist"]] == service.REQUIRED_CHECK_IDS
    summary = review["review_summary"]
    assert summary["total_checks"] == 104
    assert summary["passed_checks"] == 104
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


def test_review_and_per_ticker_digests_are_deterministic(review):
    assert review["marketflow_signal_or_feature_generation_results_review_digest"] == EXPECTED_REVIEW_DIGEST
    assert service.marketflow_signal_or_feature_generation_results_review_digest_v1(review) == EXPECTED_REVIEW_DIGEST
    second = service.build_marketflow_signal_or_feature_generation_results_review_v1()
    assert second["marketflow_signal_or_feature_generation_results_review_digest"] == EXPECTED_REVIEW_DIGEST
    assert second["per_ticker_signal_or_feature_generation_results_review_entries"] == review["per_ticker_signal_or_feature_generation_results_review_entries"]


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_signal_or_feature_generation_results_review_v1(
        review
    )
    assert result["status"] == service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_VALID
    assert result["passed_checks"] == 104


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_signal_or_feature_generation_execution_digest", "0" * 64),
        ("source_signal_or_feature_generation_output_binding_digest", "0" * 64),
        ("source_signal_or_feature_values_digest", "0" * 64),
        ("source_signal_or_feature_generation_approval_digest", "0" * 64),
        ("selected_feature_package", "WRONG"),
        ("selected_label_target_package", "WRONG"),
        ("selected_objective_path", "WRONG"),
        ("target_universe", ["AAPL"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 914),
        ("expected_output_count", 9),
        ("observed_output_count", 9),
        ("output_digest_mismatch_count", 1),
        ("selected_signal_family_count", 6),
        ("selected_feature_family_count", 7),
        ("selected_feature_group_count", 12),
        ("feature_row_count", 155297),
        ("available_feature_row_count", 155141),
        ("unavailable_feature_row_count", 155),
        ("signal_or_feature_generation_results_review_created", False),
        ("signal_or_feature_generation_results_review_ready", False),
        ("ready_for_feature_label_matrix_candidate", False),
        ("feature_label_matrix_candidate_created", True),
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
        ("signal_or_feature_generation_execution_rerun_performed", True),
        ("target_generation_execution_rerun_performed", True),
        ("target_generation_results_review_rerun_performed", True),
        ("candidate_creation_rerun_performed", True),
        ("candidate_review_rerun_performed", True),
        ("approval_rerun_performed", True),
        ("target_values_used_as_features", True),
        ("target_classes_used_as_features", True),
        ("forward_returns_used_as_features", True),
        ("future_data_used_as_features", True),
        ("prediction_fields_present", True),
        ("strategy_score_fields_present", True),
        ("trade_recommendation_fields_present", True),
        ("feature_values_jsonl_schema_verified", False),
        ("no_peek_feature_report_review", None),
        ("feature_coverage_report_review", None),
        ("per_ticker_feature_report_review", None),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_invalid_review_fields(review, field, bad_value):
    changed = deepcopy(review)
    changed[field] = bad_value
    with pytest.raises(service.MarketFlowSignalOrFeatureGenerationResultsReviewError):
        service.validate_marketflow_signal_or_feature_generation_results_review_v1(
            changed
        )


@pytest.mark.parametrize(
    "source_field",
    [
        "marketflow_signal_or_feature_generation_execution_digest",
        "signal_or_feature_generation_output_binding_digest",
        "signal_or_feature_values_digest",
        "marketflow_signal_or_feature_generation_approval_digest",
    ],
)
def test_validator_rejects_changed_source_evidence(review, source_field):
    changed = deepcopy(review)
    changed["source_evidence"][source_field] = "0" * 64
    with pytest.raises(service.MarketFlowSignalOrFeatureGenerationResultsReviewError):
        service.validate_marketflow_signal_or_feature_generation_results_review_v1(
            changed
        )


def test_validator_rejects_changed_feature_values_digest_binding(review):
    changed = deepcopy(review)
    changed["local_output_digests"]["feature_values.jsonl"] = "0" * 64
    with pytest.raises(service.MarketFlowSignalOrFeatureGenerationResultsReviewError):
        service.validate_marketflow_signal_or_feature_generation_results_review_v1(
            changed
        )


def test_validator_rejects_missing_per_ticker_digest(review):
    changed = deepcopy(review)
    changed["per_ticker_signal_or_feature_generation_results_review_entries"][0].pop(
        "per_ticker_signal_or_feature_generation_results_review_digest"
    )
    with pytest.raises(service.MarketFlowSignalOrFeatureGenerationResultsReviewError):
        service.validate_marketflow_signal_or_feature_generation_results_review_v1(
            changed
        )


def test_writer_creates_json_and_markdown(review, tmp_path):
    result = service.write_marketflow_signal_or_feature_generation_results_review_v1(
        tmp_path
    )
    json_path = tmp_path / "marketflow_signal_or_feature_generation_results_review_v1.json"
    markdown_path = tmp_path / "marketflow_signal_or_feature_generation_results_review_v1.md"
    assert json_path.is_file()
    assert markdown_path.is_file()
    written = json.loads(json_path.read_text(encoding="utf-8"))
    assert written["marketflow_signal_or_feature_generation_results_review_digest"] == EXPECTED_REVIEW_DIGEST
    assert result["json_path"].endswith(json_path.name)
    assert result["markdown_path"].endswith(markdown_path.name)
    with pytest.raises(service.MarketFlowSignalOrFeatureGenerationResultsReviewError):
        service.write_marketflow_signal_or_feature_generation_results_review_v1(tmp_path)


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_signal_or_feature_generation_results_review_markdown_v1(
        review
    )
    for heading in (
        "# Signal or Feature Generation Results Review v1",
        "## Source Signal or Feature Generation Execution",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Output Verification",
        "## Selected Feature Package",
        "## Generated Signal Families",
        "## Generated Feature Families",
        "## Feature Groups Review",
        "## Feature Values Review",
        "## No-Peek and Target-Separation Review",
        "## Feature Coverage Review",
        "## Per-Ticker Feature Report Review",
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


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE == service.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE
    assert services.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY == service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY
    assert services.SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST == service.SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST
    assert services.build_marketflow_signal_or_feature_generation_results_review_v1 is service.build_marketflow_signal_or_feature_generation_results_review_v1
    assert services.validate_marketflow_signal_or_feature_generation_results_review_v1 is service.validate_marketflow_signal_or_feature_generation_results_review_v1
    assert services.write_marketflow_signal_or_feature_generation_results_review_v1 is service.write_marketflow_signal_or_feature_generation_results_review_v1
