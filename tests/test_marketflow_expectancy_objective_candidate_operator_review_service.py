from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_expectancy_objective_candidate_operator_review_service as review_service,
)
from marketflow.services import (
    marketflow_expectancy_objective_candidate_service as candidate_service,
)


@pytest.fixture
def review() -> dict:
    return review_service.build_marketflow_expectancy_objective_candidate_operator_review_v1()


def test_operator_review_builds_offline_and_writer_is_non_overwriting(
    tmp_path,
) -> None:
    result = (
        review_service.write_marketflow_expectancy_objective_candidate_operator_review_v1(
            tmp_path
        )
    )
    path = (
        tmp_path
        / "marketflow_expectancy_objective_candidate_operator_review_v1.json"
    )
    payload = json.loads(path.read_text())
    assert payload["created_offline"] is True
    assert payload["provider_requests_made_in_review"] is False
    assert result[
        "marketflow_expectancy_objective_candidate_operator_review_digest"
    ] == payload["marketflow_expectancy_objective_candidate_operator_review_digest"]
    with pytest.raises(
        review_service.MarketFlowExpectancyObjectiveCandidateOperatorReviewError
    ):
        review_service.write_marketflow_expectancy_objective_candidate_operator_review_v1(
            tmp_path
        )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_PACKAGE"),
        ("review_status", "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"),
        ("review_scope", "EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"),
        ("source_expectancy_objective_candidate_digest", "9b241ab1be15921384d97d75a11ac7858065d041c0b8a02144e97c3e3ed3bc17"),
        ("source_strategy_charter_approval_digest", "ea6c77007c4827fbdd4015425bc92af40eb59b08daba3d5c2e41090df0762b92"),
        ("source_strategy_charter_digest", "3f5e3fd4088c38c5783618642c378874d2c0fbcc72954945cdca9fca68281853"),
        ("source_expectancy_objective_candidate_status", "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_READY_FOR_OPERATOR_REVIEW"),
        ("source_expectancy_objective_candidate_scope", "EXPECTANCY_OBJECTIVE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION"),
        ("candidate_direction", "EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE"),
        ("feature_label_matrix_digest", "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"),
        ("feature_values_digest", "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"),
        ("redesigned_label_values_digest", "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"),
        ("records_digest", "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"),
        ("expectancy_objective_candidate_review_created", True),
        ("expectancy_objective_candidate_review_ready", True),
        ("ready_for_expectancy_objective_approval", False),
        ("expectancy_objective_selected", False),
        ("expectancy_objective_approved", False),
        ("selection_created", False),
        ("approval_created", False),
        ("generation_created", False),
        ("label_generation_authorized", False),
        ("new_targets_created", False),
        ("feature_generation_authorized", False),
        ("feature_label_matrix_created", False),
        ("backtest_execution_authorized", False),
        ("model_training_authorized", False),
        ("metric_computation_authorized", False),
        ("strategy_scoring_performed", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("provider_requests_made_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
    ],
)
def test_required_top_level_values(
    review: dict,
    field: str,
    expected: object,
) -> None:
    assert review[field] == expected


def test_universe_order_counts_and_meta_limitation_are_preserved(
    review: dict,
) -> None:
    assert review["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]
    assert review["target_universe_count"] == 12
    assert review["total_canonical_record_count"] == 11946
    assert review["meta_record_count"] == 913
    assert review["non_meta_record_count"] == 1003
    assert review["meta_reduced_record_count_preserved"] is True


def test_builder_accepts_exact_source_candidate() -> None:
    candidate = candidate_service.build_marketflow_expectancy_objective_candidate_v1()
    review = (
        review_service.build_marketflow_expectancy_objective_candidate_operator_review_v1(
            candidate
        )
    )
    assert review["source_expectancy_objective_candidate_digest"] == (
        review_service.EXPECTED_SOURCE_EXPECTANCY_OBJECTIVE_CANDIDATE_DIGEST
    )


def test_builder_rejects_changed_source_candidate() -> None:
    candidate = candidate_service.build_marketflow_expectancy_objective_candidate_v1()
    candidate["candidate_direction"] = "CHANGED"
    with pytest.raises(ValueError):
        review_service.build_marketflow_expectancy_objective_candidate_operator_review_v1(
            candidate
        )


def test_objective_philosophy_is_reviewed_not_approved(review: dict) -> None:
    philosophy = review["reviewed_objective_philosophy"]
    assert philosophy["review_status"] == "REVIEWED_CANDIDATE_PHILOSOPHY"
    assert philosophy["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
    assert philosophy["objective_candidate_philosophy"] == (
        "Define expectancy-oriented objectives before generating any labels or targets."
    )


def test_objective_families_are_reviewed_not_generated(review: dict) -> None:
    rows = review["reviewed_objective_families"]
    assert len(rows) == 10
    assert all(
        row["review_status"] == "REVIEWED_OBJECTIVE_CANDIDATE_NOT_GENERATED"
        for row in rows.values()
    )
    assert all(
        row["candidate_status"] == "OBJECTIVE_CANDIDATE_DEFINED_NOT_GENERATED"
        for row in rows.values()
    )
    assert all(row["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW" for row in rows.values())


def test_objective_clusters_are_reviewed_without_selection(
    review: dict,
) -> None:
    clusters = review["reviewed_objective_clusters"]
    assert list(clusters) == [
        "CLUSTER_EXPECTANCY_AND_PAYOFF",
        "CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE",
        "CLUSTER_ABSTENTION_AND_NO_TRADE",
        "CLUSTER_CONTEXTUAL_SELECTION",
    ]
    assert clusters["CLUSTER_EXPECTANCY_AND_PAYOFF"]["review_status"] == (
        "REVIEWED_RECOMMENDED_PRIMARY_CLUSTER"
    )
    assert clusters["CLUSTER_ABSTENTION_AND_NO_TRADE"]["review_status"] == (
        "REVIEWED_RECOMMENDED_SUPPORTING_CLUSTER"
    )
    assert all(row["selection_created"] is False for row in clusters.values())


def test_recommended_path_is_reviewed_not_selected(review: dict) -> None:
    assert review["recommended_objective_path"] == (
        "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
    )
    assert review["recommendation_status"] == (
        "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    )
    assert review["selection_created"] is False
    assert review["approval_created"] is False
    assert review["generation_created"] is False


def test_research_questions_are_reviewed_not_answered(review: dict) -> None:
    rows = review["reviewed_research_questions"]
    assert len(rows) == 10
    assert all(row["question_status"] == "REVIEWED_NOT_ANSWERED" for row in rows)
    assert all(row["answered_by_this_review"] is False for row in rows)
    assert all(row["requires_future_research"] is True for row in rows)


def test_design_dimensions_are_reviewed_not_executed(review: dict) -> None:
    rows = review["reviewed_design_dimensions"]
    assert len(rows) == 12
    assert all(
        row["review_status"] == "REVIEWED_CANDIDATE_DIMENSION_NOT_EXECUTED"
        for row in rows.values()
    )
    assert all(
        row["dimension_status"] == "CANDIDATE_DIMENSION_NOT_EXECUTED"
        for row in rows.values()
    )


def test_future_outputs_are_reviewed_not_generated(review: dict) -> None:
    rows = review["reviewed_future_outputs"]
    assert len(rows) == 11
    assert all(
        row["review_status"] == "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED"
        for row in rows.values()
    )
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows.values())


def test_per_ticker_entries_and_digests_are_complete(review: dict) -> None:
    rows = review["per_ticker_expectancy_objective_candidate_review_entries"]
    assert len(rows) == 12
    assert all(
        row["per_ticker_expectancy_objective_candidate_review_digest"]
        == review_service.per_ticker_expectancy_objective_candidate_review_digest_v1(
            row
        )
        for row in rows
    )
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["review_note"] == (
        "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_CANDIDATE_REVIEW"
    )
    assert all(
        row["historical_record_count"] == 1003
        and row["meta_reduced_record_count_flag"] is False
        for row in rows
        if row["ticker"] != "META"
    )


def test_next_chain_next_gates_and_risk_controls_are_defined(
    review: dict,
) -> None:
    assert len(review["next_chain"]) == 9
    assert len(review["next_gates"]) == 9
    assert len(review["risk_controls"]) == 25
    assert "review_does_not_select_objective" in review["risk_controls"]
    assert "all_outputs_research_only" in review["risk_controls"]


def test_checklist_passes_and_summary_is_review_only(review: dict) -> None:
    assert len(review["review_checklist"]) == 63
    assert all(row["status"] == "PASS" for row in review["review_checklist"])
    summary = review["review_summary"]
    assert summary["total_checks"] == 63
    assert summary["passed_checks"] == 63
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["expectancy_objective_candidate_review_created"] is True
    assert summary["ready_for_expectancy_objective_approval"] is False
    assert summary["selection_created"] is False
    assert summary["approval_created"] is False
    assert summary["generation_created"] is False
    assert summary["runtime_authorized"] is False


def test_review_and_per_ticker_digests_are_deterministic(review: dict) -> None:
    again = (
        review_service.build_marketflow_expectancy_objective_candidate_operator_review_v1()
    )
    digest = review[
        "marketflow_expectancy_objective_candidate_operator_review_digest"
    ]
    assert digest == again[
        "marketflow_expectancy_objective_candidate_operator_review_digest"
    ]
    assert digest == (
        review_service.marketflow_expectancy_objective_candidate_operator_review_digest_v1(
            review
        )
    )
    assert [
        row["per_ticker_expectancy_objective_candidate_review_digest"]
        for row in review["per_ticker_expectancy_objective_candidate_review_entries"]
    ] == [
        row["per_ticker_expectancy_objective_candidate_review_digest"]
        for row in again["per_ticker_expectancy_objective_candidate_review_entries"]
    ]


def test_validator_accepts_valid_review(review: dict) -> None:
    result = (
        review_service.validate_marketflow_expectancy_objective_candidate_operator_review_v1(
            review
        )
    )
    assert result["status"] == (
        "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_VALID"
    )
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_expectancy_objective_candidate_digest", "0" * 64),
        ("source_strategy_charter_approval_digest", "0" * 64),
        ("source_expectancy_objective_candidate_status", "WRONG"),
        ("source_expectancy_objective_candidate_scope", "WRONG"),
        ("candidate_direction", "WRONG"),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("expectancy_objective_candidate_review_created", False),
        ("expectancy_objective_candidate_review_ready", False),
        ("ready_for_expectancy_objective_approval", True),
        ("expectancy_objective_selected", True),
        ("expectancy_objective_approved", True),
        ("selection_created", True),
        ("approval_created", True),
        ("generation_created", True),
        ("label_generation_authorized", True),
        ("new_targets_created", True),
        ("feature_generation_authorized", True),
        ("feature_label_matrix_created", True),
        ("backtest_execution_authorized", True),
        ("model_training_authorized", True),
        ("metric_computation_authorized", True),
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
        ("reviewed_objective_philosophy", {}),
        ("reviewed_objective_families", {}),
        ("reviewed_objective_clusters", {}),
        ("reviewed_research_questions", []),
        ("reviewed_design_dimensions", {}),
        ("reviewed_future_outputs", {}),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_mutated_review(
    review: dict,
    field: str,
    bad_value: object,
) -> None:
    mutated = deepcopy(review)
    mutated[field] = bad_value
    with pytest.raises(
        review_service.MarketFlowExpectancyObjectiveCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_expectancy_objective_candidate_operator_review_v1(
            mutated
        )


def test_validator_rejects_missing_review_digest(review: dict) -> None:
    review.pop("marketflow_expectancy_objective_candidate_operator_review_digest")
    with pytest.raises(
        review_service.MarketFlowExpectancyObjectiveCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_expectancy_objective_candidate_operator_review_v1(
            review
        )


def test_validator_rejects_missing_per_ticker_digest(review: dict) -> None:
    review["per_ticker_expectancy_objective_candidate_review_entries"][0].pop(
        "per_ticker_expectancy_objective_candidate_review_digest"
    )
    with pytest.raises(
        review_service.MarketFlowExpectancyObjectiveCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_expectancy_objective_candidate_operator_review_v1(
            review
        )


def test_markdown_includes_all_required_sections(review: dict) -> None:
    markdown = (
        review_service.build_marketflow_expectancy_objective_candidate_operator_review_markdown_v1(
            review
        )
    )
    required_sections = [
        "Title",
        "Expectancy Objective Candidate Operator Review v1",
        "Source Expectancy Objective Candidate",
        "Bound Evidence",
        "Dataset and Universe",
        "Reviewed Candidate Basis",
        "Reviewed Objective Philosophy",
        "Reviewed Objective Families",
        "Reviewed Objective Clusters",
        "Reviewed Candidate Recommendation",
        "Reviewed Research Questions",
        "Reviewed Design Dimensions",
        "Reviewed Future Outputs",
        "Per-Ticker Review Summary",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in required_sections)
