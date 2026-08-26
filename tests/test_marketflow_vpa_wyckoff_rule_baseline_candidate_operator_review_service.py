from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_service as service,
)


EXPECTED_REVIEW_DIGEST = (
    "8447ca124e62ef8ea346aa2ee23d0a0c209791bf960659adf7cd75dc363dfbd9"
)


@pytest.fixture(scope="module")
def source_candidate() -> dict:
    return service.candidate_service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_v1()


@pytest.fixture(scope="module")
def review(source_candidate: dict) -> dict:
    return service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(
        source_candidate
    )


def test_operator_review_builds_offline_without_execution(review: dict) -> None:
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["feature_label_matrix_execution_rerun_performed"] is False
    assert review["feature_label_matrix_results_review_rerun_performed"] is False
    assert review["vpa_wyckoff_candidate_creation_rerun_performed"] is False


def test_default_builder_validates_and_builds_source_candidate() -> None:
    review = service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1()
    assert review["marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest"] == EXPECTED_REVIEW_DIGEST


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE"),
    ("schema_version", "marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1"),
    ("review_status", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"),
    ("review_scope", "VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"),
    ("source_vpa_wyckoff_rule_baseline_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
    ("source_feature_label_matrix_results_review_digest", service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST),
    ("source_feature_label_matrix_execution_digest", service.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST),
    ("source_feature_label_matrix_rows_digest", service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST),
    ("source_feature_values_digest", service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST),
    ("source_target_values_digest", service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
    ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ("selected_matrix_package", service.candidate_service.execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX),
    ("selected_feature_package", service.candidate_service.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET),
    ("selected_label_target_package", service.candidate_service.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET),
    ("selected_objective_path", service.candidate_service.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT),
    ("target_universe_count", 12), ("total_canonical_record_count", 11946),
    ("meta_record_count", 913), ("non_meta_record_count", 1003),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_review_core_contract(review: dict, field: str, expected: object) -> None:
    assert review[field] == expected


def test_complete_source_evidence_chain_is_bound(review: dict, source_candidate: dict) -> None:
    expected = {
        "marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest": service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        **source_candidate["source_evidence"],
    }
    assert review["source_evidence"] == expected


def test_universe_order_records_and_meta_are_preserved(review: dict) -> None:
    assert review["target_universe"] == service.TARGET_UNIVERSE
    assert review["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST
    assert review["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize("field", [
    "vpa_wyckoff_rule_baseline_candidate_created",
    "vpa_wyckoff_rule_baseline_candidate_ready_for_operator_review",
    "vpa_wyckoff_rule_baseline_candidate_review_created",
    "vpa_wyckoff_rule_baseline_candidate_review_ready",
])
def test_candidate_and_review_readiness_fields_are_true(review: dict, field: str) -> None:
    assert review[field] is True


def test_ready_for_approval_is_false(review: dict) -> None:
    assert review["ready_for_vpa_wyckoff_rule_baseline_approval"] is False


def test_candidate_basis_and_philosophy_are_reviewed(review: dict) -> None:
    assert review["candidate_philosophy"] == service.candidate_service.CANDIDATE_PHILOSOPHY
    assert review["candidate_primary_question"] == service.candidate_service.CANDIDATE_PRIMARY_QUESTION
    assert review["candidate_secondary_question"] == service.candidate_service.CANDIDATE_SECONDARY_QUESTION
    assert review["candidate_boundary"] == service.candidate_service.CANDIDATE_BOUNDARY
    assert review["matrix_row_count"] == 179190


def test_ten_rule_families_are_reviewed_but_not_executed(review: dict) -> None:
    rows = review["reviewed_vpa_wyckoff_rule_families"]
    assert [row["rule_family_id"] for row in rows] == service.candidate_service.VPA_RULE_FAMILY_IDS
    assert len(rows) == 10
    assert all(row["review_status"] == "REVIEWED_VPA_WYCKOFF_RULE_CANDIDATE_NOT_EXECUTED" for row in rows)
    assert all(row["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW" for row in rows)
    assert all(row["rule_execution_authorized"] is False for row in rows)
    assert all(row["rule_values_created"] is False for row in rows)


def test_eight_state_families_are_reviewed_but_not_executed(review: dict) -> None:
    rows = review["reviewed_wyckoff_state_families"]
    assert [row["state_family_id"] for row in rows] == service.candidate_service.WYCKOFF_STATE_FAMILY_IDS
    assert len(rows) == 8
    assert all(row["review_status"] == "REVIEWED_WYCKOFF_STATE_CANDIDATE_NOT_EXECUTED" for row in rows)
    assert all(row["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW" for row in rows)
    assert all(row["state_values_created"] is False for row in rows)


def test_recommended_package_is_reviewed_but_not_selected(review: dict) -> None:
    package = review["reviewed_baseline_packages"][0]
    assert package["package_id"] == service.candidate_service.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE
    assert package["source_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert package["selection_created"] is False


def test_supporting_package_is_reviewed_but_not_selected(review: dict) -> None:
    package = review["reviewed_baseline_packages"][1]
    assert package["package_id"] == service.candidate_service.PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT
    assert package["source_status"] == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["review_status"] == "REVIEWED_AVAILABLE_SUPPORTING_PACKAGE_NOT_SELECTED"
    assert package["selection_created"] is False


def test_all_feature_group_mappings_are_reviewed_without_targets(review: dict) -> None:
    rows = review["reviewed_feature_group_mapping"]
    assert len(rows) == 13
    assert all(row["review_status"] == "REVIEWED_PLANNED_MAPPING_NOT_EXECUTED" for row in rows)
    assert all(row["mapping_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["target_values_used"] is False and row["future_data_used"] is False for row in rows)


def test_twelve_design_questions_are_reviewed_and_unanswered(review: dict) -> None:
    rows = review["reviewed_rule_design_questions"]
    assert len(rows) == 12
    assert all(row["review_status"] == "REVIEWED_QUESTION_NOT_ANSWERED" for row in rows)
    assert all(row["question_status"] == "NOT_ANSWERED" for row in rows)


def test_future_outputs_are_reviewed_and_not_generated(review: dict) -> None:
    rows = review["reviewed_planned_future_outputs"]
    assert [row["output_id"] for row in rows] == service.candidate_service.FUTURE_OUTPUT_IDS
    assert len(rows) == 10
    assert all(row["review_status"] == "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED" for row in rows)
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)


PLANNED_COUNTS = [
    ("planned_source_matrix_row_count", 179190),
    ("planned_rule_family_count", 10),
    ("planned_wyckoff_state_family_count", 8),
    ("planned_primary_package_rule_family_count", 8),
    ("planned_primary_package_state_family_count", 6),
    ("planned_rule_value_rows", 179190),
    ("planned_rule_state_rows", 179190),
]


@pytest.mark.parametrize(("field", "expected"), PLANNED_COUNTS)
def test_planned_counts_are_reviewed(review: dict, field: str, expected: int) -> None:
    assert review[field] == expected


def test_per_ticker_review_entries_and_digests(review: dict) -> None:
    entries = review["per_ticker_vpa_wyckoff_rule_baseline_candidate_review_entries"]
    assert [row["ticker"] for row in entries] == service.TARGET_UNIVERSE
    for row in entries:
        payload = deepcopy(row)
        digest = payload.pop("per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest")
        assert digest == semantic_digest(payload)
        assert row["vpa_wyckoff_rule_baseline_candidate_review_status"] == "READY_FOR_OPERATOR_ASSESSMENT"
        assert row["vpa_wyckoff_rule_baseline_selected"] is False
        if row["ticker"] == "META":
            assert (row["historical_record_count"], row["planned_matrix_row_count"]) == (913, 13695)
            assert row["review_note"] == "PRESERVE_META_LIMITATION_IN_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_REVIEW"
        else:
            assert (row["historical_record_count"], row["planned_matrix_row_count"]) == (1003, 15045)


CLOSED_FALSE_FIELDS = [
    "ready_for_vpa_wyckoff_rule_baseline_approval",
    "vpa_wyckoff_rule_baseline_selected", "vpa_wyckoff_rule_baseline_approved",
    "vpa_wyckoff_rule_baseline_authorized", "vpa_wyckoff_rule_baseline_executed",
    "vpa_wyckoff_rule_values_created", "vpa_wyckoff_baseline_outputs_created",
    "selection_created", "approval_created", "execution_created", "generation_created",
    "expectancy_backtest_lab_candidate_created", "backtest_execution_authorized",
    "backtest_execution_performed", "model_training_authorized", "model_training_performed",
    "metric_computation_authorized", "metric_computation_performed", "strategy_scoring_performed",
    "trade_recommendations_generated", "provider_requests_made_in_review",
    "market_data_acquisition_performed_in_review", "canonical_dataset_regenerated_in_review",
    "feature_label_matrix_execution_rerun_performed",
    "feature_label_matrix_results_review_rerun_performed",
    "vpa_wyckoff_candidate_creation_rerun_performed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_review_keeps_selection_execution_and_authority_closed(review: dict, field: str) -> None:
    assert review[field] is False


def test_acceptance_profitability_runtime_and_trading_remain_closed(review: dict) -> None:
    assert review["predictive_usefulness"] == service.NOT_ACCEPTED
    assert review["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert review[field] == service.NOT_AUTHORIZED


def test_next_chain_gates_and_risk_controls_are_defined(review: dict) -> None:
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_review_checklist_passes(review: dict) -> None:
    assert [row["check_id"] for row in review["review_checklist"]] == service.REQUIRED_CHECK_IDS
    assert len(service.REQUIRED_CHECK_IDS) == 60
    assert all(row["status"] == service.PASS for row in review["review_checklist"])
    assert review["review_summary"]["passed_checks"] == 60
    assert review["review_summary"]["failed_checks"] == 0


def test_review_and_per_ticker_digests_are_deterministic(review: dict, source_candidate: dict) -> None:
    second = service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(source_candidate)
    assert review["marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest"] == EXPECTED_REVIEW_DIGEST
    assert second["marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest"] == EXPECTED_REVIEW_DIGEST
    assert second["per_ticker_vpa_wyckoff_rule_baseline_candidate_review_entries"] == review["per_ticker_vpa_wyckoff_rule_baseline_candidate_review_entries"]


def test_validator_accepts_valid_review(review: dict) -> None:
    result = service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(review)
    assert result["status"] == service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_VALID
    assert result["passed_checks"] == 60


SCALAR_MUTATIONS = [
    ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("review_scope", "WRONG"),
    ("source_vpa_wyckoff_rule_baseline_candidate_digest", "0" * 64),
    ("source_feature_label_matrix_results_review_digest", "0" * 64),
    ("source_feature_label_matrix_rows_digest", "0" * 64),
    ("selected_matrix_package", "WRONG"), ("selected_feature_package", "WRONG"),
    ("selected_label_target_package", "WRONG"), ("target_universe", ["MSFT"]),
    ("target_universe_count", 11), ("records_digest", "0" * 64),
    ("meta_record_count", 912), ("vpa_wyckoff_rule_baseline_candidate_review_created", False),
    ("vpa_wyckoff_rule_baseline_candidate_review_ready", False),
    ("ready_for_vpa_wyckoff_rule_baseline_approval", True),
    ("selection_created", True), ("approval_created", True), ("execution_created", True),
    ("vpa_wyckoff_rule_baseline_selected", True),
    ("vpa_wyckoff_rule_baseline_approved", True),
    ("vpa_wyckoff_rule_baseline_executed", True),
    ("vpa_wyckoff_rule_values_created", True),
    ("vpa_wyckoff_baseline_outputs_created", True),
    ("expectancy_backtest_lab_candidate_created", True),
    ("backtest_execution_performed", True), ("model_training_performed", True),
    ("metric_computation_performed", True), ("strategy_scoring_performed", True),
    ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
    ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True), ("provider_requests_made_in_review", True),
    ("market_data_acquisition_performed_in_review", True),
    ("canonical_dataset_regenerated_in_review", True),
    ("feature_label_matrix_execution_rerun_performed", True),
    ("feature_label_matrix_results_review_rerun_performed", True),
    ("vpa_wyckoff_candidate_creation_rerun_performed", True),
    ("risk_controls", []),
]


@pytest.mark.parametrize(("field", "value"), SCALAR_MUTATIONS)
def test_validator_rejects_contract_mutations(review: dict, field: str, value: object) -> None:
    invalid = deepcopy(review)
    invalid[field] = value
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(invalid)


@pytest.mark.parametrize("field", [
    "reviewed_vpa_wyckoff_rule_families", "reviewed_wyckoff_state_families",
    "reviewed_baseline_packages", "reviewed_feature_group_mapping",
    "reviewed_rule_design_questions", "reviewed_planned_future_outputs",
])
def test_validator_rejects_missing_review_components(review: dict, field: str) -> None:
    invalid = deepcopy(review)
    invalid[field] = []
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(invalid)


def test_validator_rejects_missing_review_digest(review: dict) -> None:
    invalid = deepcopy(review)
    invalid.pop("marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest")
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(review: dict) -> None:
    invalid = deepcopy(review)
    invalid["per_ticker_vpa_wyckoff_rule_baseline_candidate_review_entries"][0].pop(
        "per_ticker_vpa_wyckoff_rule_baseline_candidate_review_digest"
    )
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(invalid)


def test_builder_rejects_mutated_source_candidate(source_candidate: dict) -> None:
    invalid = deepcopy(source_candidate)
    invalid["marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest"] = "0" * 64
    with pytest.raises(service.candidate_service.MarketFlowVpaWyckoffRuleBaselineCandidateError):
        service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(invalid)


def test_markdown_includes_required_sections(review: dict) -> None:
    markdown = service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_markdown_v1(review)
    for section in (
        "VPA/Wyckoff Rule Baseline Candidate Operator Review v1",
        "Source VPA/Wyckoff Candidate", "Source Feature-Label Matrix Results Review",
        "Bound Evidence", "Dataset and Universe", "Reviewed Candidate Basis",
        "Reviewed Candidate Philosophy", "Reviewed VPA/Wyckoff Rule Families",
        "Reviewed Wyckoff State Families", "Reviewed Recommended Package",
        "Reviewed Supporting Package", "Reviewed Feature Group Mapping",
        "Reviewed Rule Design Questions", "Reviewed Planned Outputs", "Reviewed Planned Counts",
        "Per-Ticker Review Summary", "Next Chain", "Next Gates", "Risk Controls",
        "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary",
        "Checklist Summary", "Guardrails",
    ):
        assert section in markdown


def test_writer_uses_explicit_isolated_directory(source_candidate: dict, tmp_path: Path) -> None:
    result = service.write_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(
        tmp_path, candidate=source_candidate
    )
    json_path = Path(result["json_path"])
    markdown_path = Path(result["markdown_path"])
    assert json_path.is_file() and markdown_path.is_file()
    persisted = json.loads(json_path.read_text(encoding="utf-8"))
    assert persisted["marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest"] == EXPECTED_REVIEW_DIGEST
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateOperatorReviewError):
        service.write_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1(
            tmp_path, candidate=source_candidate
        )


def test_services_export_operator_review_api() -> None:
    assert services.build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1 is service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1
    assert services.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1 is service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1
    assert services.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE == "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE"
