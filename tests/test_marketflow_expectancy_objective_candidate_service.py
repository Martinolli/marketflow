from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import marketflow_expectancy_objective_candidate_service as candidate_service


@pytest.fixture
def candidate() -> dict:
    return candidate_service.build_marketflow_expectancy_objective_candidate_v1()


def test_candidate_builds_offline_and_writer_is_non_overwriting(
    tmp_path,
) -> None:
    result = candidate_service.write_marketflow_expectancy_objective_candidate_v1(
        tmp_path
    )
    path = tmp_path / "marketflow_expectancy_objective_candidate_v1.json"
    payload = json.loads(path.read_text())
    assert payload["created_offline"] is True
    assert payload["provider_requests_made_in_candidate"] is False
    assert result["marketflow_expectancy_objective_candidate_v1_digest"] == payload[
        "marketflow_expectancy_objective_candidate_v1_digest"
    ]
    with pytest.raises(candidate_service.MarketFlowExpectancyObjectiveCandidateError):
        candidate_service.write_marketflow_expectancy_objective_candidate_v1(
            tmp_path
        )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_V1"),
        ("candidate_status", "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_READY_FOR_OPERATOR_REVIEW"),
        ("candidate_scope", "EXPECTANCY_OBJECTIVE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION"),
        ("candidate_direction", "EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE"),
        ("source_strategy_charter_approval_digest", "ea6c77007c4827fbdd4015425bc92af40eb59b08daba3d5c2e41090df0762b92"),
        ("source_strategy_charter_review_digest", "d75e541f3f9d16593eb3a4da6f4f6de7a451c259295ce4e3e8f09171bbcbe8f9"),
        ("source_strategy_charter_digest", "3f5e3fd4088c38c5783618642c378874d2c0fbcc72954945cdca9fca68281853"),
        ("feature_label_matrix_digest", "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"),
        ("feature_values_digest", "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"),
        ("redesigned_label_values_digest", "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"),
        ("records_digest", "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"),
        ("marketflow_algorithm_strategy_charter_approved", True),
        ("ready_for_expectancy_objective_candidate", True),
        ("expectancy_objective_candidate_created", True),
        ("expectancy_objective_candidate_ready_for_operator_review", True),
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
        ("provider_requests_made_in_candidate", False),
        ("market_data_acquisition_performed_in_candidate", False),
    ],
)
def test_required_top_level_values(
    candidate: dict,
    field: str,
    expected: object,
) -> None:
    assert candidate[field] == expected


def test_universe_order_counts_and_meta_limitation_are_preserved(
    candidate: dict,
) -> None:
    assert candidate["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]
    assert candidate["target_universe_count"] == 12
    assert candidate["total_canonical_record_count"] == 11946
    assert candidate["meta_record_count"] == 913
    assert candidate["non_meta_record_count"] == 1003
    assert candidate["meta_reduced_record_count_preserved"] is True


def test_objective_candidate_philosophy_is_defined(candidate: dict) -> None:
    assert candidate["objective_candidate_philosophy"] == (
        "Define expectancy-oriented objectives before generating any labels or targets."
    )
    assert "tradable opportunity" in candidate[
        "objective_candidate_primary_question"
    ]
    assert "majority-class" in candidate[
        "objective_candidate_secondary_question"
    ]
    assert candidate["objective_candidate_boundary"].startswith("Candidate-only")


def test_objective_families_are_defined_not_generated(
    candidate: dict,
) -> None:
    rows = candidate["objective_candidate_families"]
    assert len(rows) == 10
    assert all(
        row["candidate_status"] == "OBJECTIVE_CANDIDATE_DEFINED_NOT_GENERATED"
        for row in rows.values()
    )
    assert all(row["operator_review_required"] is True for row in rows.values())
    assert all(row["label_generation_authorized"] is False for row in rows.values())
    assert all(row["target_creation_authorized"] is False for row in rows.values())


def test_recommended_objective_clusters_are_exact(candidate: dict) -> None:
    clusters = candidate["recommended_objective_clusters"]
    assert list(clusters) == [
        "CLUSTER_EXPECTANCY_AND_PAYOFF",
        "CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE",
        "CLUSTER_ABSTENTION_AND_NO_TRADE",
        "CLUSTER_CONTEXTUAL_SELECTION",
    ]
    assert clusters["CLUSTER_EXPECTANCY_AND_PAYOFF"]["status"] == (
        "RECOMMENDED_FOR_OPERATOR_REVIEW"
    )
    assert clusters["CLUSTER_ABSTENTION_AND_NO_TRADE"]["status"] == (
        "RECOMMENDED_SUPPORTING_OBJECTIVE"
    )


def test_candidate_recommendation_is_unselected(candidate: dict) -> None:
    assert candidate["recommended_objective_path"] == (
        "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
    )
    assert candidate["recommended_primary_objective_cluster"] == (
        "CLUSTER_EXPECTANCY_AND_PAYOFF"
    )
    assert candidate["recommended_supporting_objective_cluster"] == (
        "CLUSTER_ABSTENTION_AND_NO_TRADE"
    )
    assert candidate["recommendation_status"] == (
        "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    )
    assert candidate["selection_created"] is False
    assert candidate["approval_created"] is False
    assert candidate["generation_created"] is False


def test_research_questions_are_unanswered(candidate: dict) -> None:
    rows = candidate["objective_design_research_questions"]
    assert len(rows) == 10
    assert all(row["question_status"] == "NOT_ANSWERED" for row in rows)
    assert all(row["requires_future_research"] is True for row in rows)


def test_design_dimensions_are_not_executed(candidate: dict) -> None:
    rows = candidate["candidate_objective_design_dimensions"]
    assert len(rows) == 12
    assert all(
        row["dimension_status"] == "CANDIDATE_DIMENSION_NOT_EXECUTED"
        for row in rows.values()
    )
    assert all(row["generation_authorized"] is False for row in rows.values())
    assert all(
        row["metric_computation_authorized"] is False for row in rows.values()
    )


def test_future_outputs_are_planned_not_generated(candidate: dict) -> None:
    rows = candidate["candidate_future_outputs"]
    assert len(rows) == 11
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows.values())
    assert all(row["research_only"] is True for row in rows.values())
    assert all(row["non_actionable"] is True for row in rows.values())


def test_per_ticker_entries_and_digests_are_complete(candidate: dict) -> None:
    rows = candidate["per_ticker_expectancy_objective_candidate_entries"]
    assert len(rows) == 12
    assert all(
        row["per_ticker_expectancy_objective_candidate_digest"]
        == candidate_service.per_ticker_expectancy_objective_candidate_digest_v1(
            row
        )
        for row in rows
    )
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["candidate_note"] == (
        "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_CANDIDATE"
    )
    assert all(
        row["historical_record_count"] == 1003
        and row["meta_reduced_record_count_flag"] is False
        for row in rows
        if row["ticker"] != "META"
    )


def test_next_chain_next_gates_and_risk_controls_are_defined(
    candidate: dict,
) -> None:
    assert len(candidate["next_chain"]) == 10
    assert len(candidate["next_gates"]) == 10
    assert len(candidate["risk_controls"]) == 24
    assert "candidate_does_not_approve_objective" in candidate["risk_controls"]
    assert "all_outputs_research_only" in candidate["risk_controls"]


def test_checklist_passes_and_summary_is_candidate_only(
    candidate: dict,
) -> None:
    assert len(candidate["candidate_checklist"]) == 60
    assert all(row["status"] == "PASS" for row in candidate["candidate_checklist"])
    summary = candidate["candidate_summary"]
    assert summary["total_checks"] == 60
    assert summary["passed_checks"] == 60
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["expectancy_objective_candidate_created"] is True
    assert summary["selection_created"] is False
    assert summary["approval_created"] is False
    assert summary["generation_created"] is False
    assert summary["runtime_authorized"] is False


def test_candidate_and_per_ticker_digests_are_deterministic(
    candidate: dict,
) -> None:
    again = candidate_service.build_marketflow_expectancy_objective_candidate_v1()
    digest = candidate["marketflow_expectancy_objective_candidate_v1_digest"]
    assert digest == again["marketflow_expectancy_objective_candidate_v1_digest"]
    assert digest == candidate_service.marketflow_expectancy_objective_candidate_v1_digest(
        candidate
    )
    assert [
        row["per_ticker_expectancy_objective_candidate_digest"]
        for row in candidate["per_ticker_expectancy_objective_candidate_entries"]
    ] == [
        row["per_ticker_expectancy_objective_candidate_digest"]
        for row in again["per_ticker_expectancy_objective_candidate_entries"]
    ]


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = candidate_service.validate_marketflow_expectancy_objective_candidate_v1(
        candidate
    )
    assert result["status"] == "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_VALID"
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("candidate_direction", "WRONG"),
        ("source_strategy_charter_approval_digest", "0" * 64),
        ("source_strategy_charter_digest", "0" * 64),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("marketflow_algorithm_strategy_charter_approved", False),
        ("ready_for_expectancy_objective_candidate", False),
        ("expectancy_objective_candidate_created", False),
        ("expectancy_objective_candidate_ready_for_operator_review", False),
        ("objective_candidate_philosophy", ""),
        ("objective_candidate_families", {}),
        ("recommended_objective_clusters", {}),
        ("recommended_objective_path", ""),
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
        ("provider_requests_made_in_candidate", True),
        ("market_data_acquisition_performed_in_candidate", True),
        ("canonical_dataset_regenerated_in_candidate", True),
        ("objective_design_research_questions", []),
        ("candidate_objective_design_dimensions", {}),
        ("candidate_future_outputs", {}),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_mutated_candidate(
    candidate: dict,
    field: str,
    bad_value: object,
) -> None:
    mutated = deepcopy(candidate)
    mutated[field] = bad_value
    with pytest.raises(candidate_service.MarketFlowExpectancyObjectiveCandidateError):
        candidate_service.validate_marketflow_expectancy_objective_candidate_v1(
            mutated
        )


def test_validator_rejects_missing_candidate_digest(candidate: dict) -> None:
    candidate.pop("marketflow_expectancy_objective_candidate_v1_digest")
    with pytest.raises(candidate_service.MarketFlowExpectancyObjectiveCandidateError):
        candidate_service.validate_marketflow_expectancy_objective_candidate_v1(
            candidate
        )


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    candidate["per_ticker_expectancy_objective_candidate_entries"][0].pop(
        "per_ticker_expectancy_objective_candidate_digest"
    )
    with pytest.raises(candidate_service.MarketFlowExpectancyObjectiveCandidateError):
        candidate_service.validate_marketflow_expectancy_objective_candidate_v1(
            candidate
        )


def test_markdown_includes_all_required_sections(candidate: dict) -> None:
    markdown = candidate_service.build_marketflow_expectancy_objective_candidate_markdown_v1(
        candidate
    )
    required_sections = [
        "Title",
        "Expectancy Objective Candidate v1",
        "Source Strategy Charter Approval",
        "Bound Evidence",
        "Dataset and Universe",
        "Candidate Basis",
        "Objective Candidate Philosophy",
        "Objective Candidate Families",
        "Recommended Objective Clusters",
        "Candidate Recommendation",
        "Research Questions",
        "Objective Design Dimensions",
        "Future Outputs",
        "Per-Ticker Candidate Summary",
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
