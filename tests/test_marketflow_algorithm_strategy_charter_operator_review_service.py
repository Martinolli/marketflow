from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services.marketflow_algorithm_strategy_charter_operator_review_service import (
    ARTIFACT_KIND_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE,
    EXPECTED_SOURCE_CHARTER_DIGEST,
    MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE_READY,
    STRATEGY_CHARTER_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
    MarketFlowAlgorithmStrategyCharterOperatorReviewError,
    build_marketflow_algorithm_strategy_charter_operator_review_markdown_v1,
    build_marketflow_algorithm_strategy_charter_operator_review_v1,
    marketflow_algorithm_strategy_charter_operator_review_digest_v1,
    per_ticker_marketflow_algorithm_strategy_charter_review_digest_v1,
    validate_marketflow_algorithm_strategy_charter_operator_review_v1,
    write_marketflow_algorithm_strategy_charter_operator_review_v1,
)
from marketflow.services.marketflow_algorithm_strategy_charter_service import (
    EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
    build_marketflow_algorithm_strategy_charter_v1,
)


@pytest.fixture
def review() -> dict:
    return build_marketflow_algorithm_strategy_charter_operator_review_v1()


def test_operator_review_builds_offline_and_writer_is_non_overwriting(tmp_path) -> None:
    result = write_marketflow_algorithm_strategy_charter_operator_review_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_algorithm_strategy_charter_operator_review_v1.json").read_text())
    assert payload["created_offline"] is True
    assert payload["provider_requests_made_in_review"] is False
    assert result["marketflow_algorithm_strategy_charter_operator_review_digest"] == payload[
        "marketflow_algorithm_strategy_charter_operator_review_digest"
    ]
    with pytest.raises(MarketFlowAlgorithmStrategyCharterOperatorReviewError):
        write_marketflow_algorithm_strategy_charter_operator_review_v1(tmp_path)


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", ARTIFACT_KIND_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE),
        ("review_status", MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE_READY),
        ("review_scope", STRATEGY_CHARTER_OPERATOR_REVIEW_ONLY_NOT_APPROVAL),
        ("source_charter_digest", EXPECTED_SOURCE_CHARTER_DIGEST),
        ("strategy_direction", EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE),
        ("source_final_archive_digest", "31b61c934f3bc4970973dd2cfc0e18fb3ea4ca76e02c815bed5cf509e4a5440b"),
        ("source_archive_digest", "e38963a93be3518b531f60c55924b985d42761b60c07300450944b3e876dce99"),
        ("feature_label_matrix_digest", "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"),
        ("feature_values_digest", "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"),
        ("redesigned_label_values_digest", "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"),
        ("records_digest", "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"),
        ("marketflow_algorithm_strategy_charter_review_created", True),
        ("marketflow_algorithm_strategy_charter_review_ready", True),
        ("marketflow_algorithm_strategy_charter_approved", False),
        ("ready_for_marketflow_algorithm_strategy_charter_approval", False),
        ("expectancy_objective_candidate_created", False),
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
def test_required_top_level_values(review: dict, field: str, expected: object) -> None:
    assert review[field] == expected


def test_universe_order_counts_and_meta_limitation_are_preserved(review: dict) -> None:
    assert review["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]
    assert review["target_universe_count"] == 12
    assert review["total_canonical_record_count"] == 11946
    assert review["meta_record_count"] == 913
    assert review["non_meta_record_count"] == 1003
    assert review["meta_reduced_record_count_preserved"] is True


def test_strategy_philosophy_is_reviewed_without_answer_or_approval(review: dict) -> None:
    philosophy = review["reviewed_strategy_philosophy"]
    assert philosophy["review_status"] == "REVIEWED_RESEARCH_ONLY"
    assert philosophy["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
    assert philosophy["answered_by_this_review"] is False
    assert philosophy["core_philosophy"] == (
        "Do not optimize for classification accuracy alone. Optimize for tradable expectancy, "
        "risk-adjusted opportunity, and abstention quality."
    )


def test_all_strategy_principles_are_reviewed_research_only(review: dict) -> None:
    rows = review["reviewed_strategy_principles"]
    assert len(rows) == 10
    assert all(row["review_status"] == "REVIEWED_RESEARCH_ONLY" for row in rows.values())
    assert all(row["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW" for row in rows.values())
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows.values())


def test_all_research_questions_are_reviewed_and_unanswered(review: dict) -> None:
    rows = review["reviewed_research_questions"]
    assert len(rows) == 10
    assert all(row["answered_by_this_review"] is False for row in rows)
    assert all(row["requires_future_research"] is True for row in rows)


@pytest.mark.parametrize(
    ("field", "count", "status_field", "status"),
    [
        ("reviewed_objective_families", 10, "objective_status", "CANDIDATE_OBJECTIVE_NOT_GENERATED"),
        ("reviewed_signal_families", 10, "signal_status", "CANDIDATE_SIGNAL_NOT_GENERATED"),
        ("reviewed_validation_metrics", 14, "metric_status", "CANDIDATE_METRIC_NOT_COMPUTED"),
        ("reviewed_baselines", 7, "baseline_status", "CANDIDATE_BASELINE_NOT_EXECUTED"),
    ],
)
def test_candidate_catalogs_are_reviewed_without_execution(
    review: dict,
    field: str,
    count: int,
    status_field: str,
    status: str,
) -> None:
    rows = review[field]
    assert len(rows) == count
    assert all(row[status_field] == status for row in rows.values())
    assert all(row["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW" for row in rows.values())


def test_phase_plan_is_reviewed_without_starting_future_phases(review: dict) -> None:
    rows = list(review["reviewed_phase_plan"].values())
    assert len(rows) == 9
    assert rows[0]["status"] == "COMPLETED_BY_SOURCE_ARTIFACT"
    assert all(row["status"] == "FUTURE_NOT_STARTED" for row in rows[1:])


def test_acceptance_gates_are_reviewed_and_closed(review: dict) -> None:
    rows = review["reviewed_acceptance_gates"]
    assert len(rows) == 10
    assert all(row["review_status"] == "REVIEWED_CLOSED_FUTURE_GATE" for row in rows.values())
    assert all(row["gate_status"] == "CLOSED_FUTURE_GATE" for row in rows.values())
    assert all(row["opened_by_this_review"] is False for row in rows.values())


def test_non_goals_remain_active(review: dict) -> None:
    rows = review["reviewed_non_goals"]
    assert len(rows) == 13
    assert all(row["review_status"] == "REVIEWED_ACTIVE" for row in rows)
    assert all(row["active"] is True for row in rows)


def test_per_ticker_entries_and_digests_are_complete(review: dict) -> None:
    rows = review["per_ticker_strategy_charter_review_entries"]
    assert len(rows) == 12
    assert all(
        row["per_ticker_strategy_charter_review_digest"]
        == per_ticker_marketflow_algorithm_strategy_charter_review_digest_v1(row)
        for row in rows
    )
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["review_note"] == (
        "PRESERVE_META_LIMITATION_IN_ALGORITHM_STRATEGY_CHARTER_REVIEW"
    )
    assert all(
        row["historical_record_count"] == 1003
        and row["meta_reduced_record_count_flag"] is False
        for row in rows
        if row["ticker"] != "META"
    )


def test_risk_controls_next_chain_and_next_gates_are_defined(review: dict) -> None:
    assert len(review["risk_controls"]) == 25
    assert "review_does_not_approve_strategy_charter" in review["risk_controls"]
    assert "all_outputs_research_only" in review["risk_controls"]
    assert len(review["next_chain"]) == 8
    assert len(review["next_gates"]) == 9


def test_checklist_passes_and_summary_preserves_closed_boundary(review: dict) -> None:
    assert len(review["review_checklist"]) == 59
    assert all(row["status"] == "PASS" for row in review["review_checklist"])
    assert review["review_summary"] == {
        "total_checks": 59,
        "passed_checks": 59,
        "failed_checks": 0,
        "blocker_count": 0,
        "strategy_charter_review_created": True,
        "strategy_charter_review_ready": True,
        "ready_for_approval": False,
        "strategy_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "expectancy_objective_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def test_review_and_per_ticker_digests_are_deterministic(review: dict) -> None:
    again = build_marketflow_algorithm_strategy_charter_operator_review_v1()
    digest = review["marketflow_algorithm_strategy_charter_operator_review_digest"]
    assert digest == again["marketflow_algorithm_strategy_charter_operator_review_digest"]
    assert digest == marketflow_algorithm_strategy_charter_operator_review_digest_v1(review)
    assert [
        row["per_ticker_strategy_charter_review_digest"]
        for row in review["per_ticker_strategy_charter_review_entries"]
    ] == [
        row["per_ticker_strategy_charter_review_digest"]
        for row in again["per_ticker_strategy_charter_review_entries"]
    ]


def test_builder_accepts_exact_committed_source_charter() -> None:
    source = build_marketflow_algorithm_strategy_charter_v1()
    review = build_marketflow_algorithm_strategy_charter_operator_review_v1(source)
    assert review["source_charter_digest"] == EXPECTED_SOURCE_CHARTER_DIGEST


def test_builder_rejects_changed_source_charter() -> None:
    source = build_marketflow_algorithm_strategy_charter_v1()
    source["strategy_direction"] = "CHANGED"
    with pytest.raises(ValueError):
        build_marketflow_algorithm_strategy_charter_operator_review_v1(source)


def test_validator_accepts_valid_review(review: dict) -> None:
    result = validate_marketflow_algorithm_strategy_charter_operator_review_v1(review)
    assert result["status"] == "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_VALID"
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("path", "bad_value"),
    [
        (("artifact_kind",), "WRONG"),
        (("review_status",), "WRONG"),
        (("review_scope",), "WRONG"),
        (("source_charter_digest",), "0" * 64),
        (("strategy_direction",), "WRONG"),
        (("target_universe",), ["MSFT"]),
        (("target_universe_count",), 11),
        (("records_digest",), "0" * 64),
        (("meta_record_count",), 1003),
        (("marketflow_algorithm_strategy_charter_review_created",), False),
        (("marketflow_algorithm_strategy_charter_review_ready",), False),
        (("marketflow_algorithm_strategy_charter_approved",), True),
        (("ready_for_marketflow_algorithm_strategy_charter_approval",), True),
        (("expectancy_objective_candidate_created",), True),
        (("reviewed_strategy_philosophy",), {}),
        (("reviewed_strategy_principles",), {}),
        (("reviewed_research_questions",), []),
        (("reviewed_objective_families",), {}),
        (("reviewed_signal_families",), {}),
        (("reviewed_validation_metrics",), {}),
        (("reviewed_baselines",), {}),
        (("reviewed_phase_plan",), {}),
        (("reviewed_acceptance_gates",), {}),
        (("label_generation_authorized",), True),
        (("new_targets_created",), True),
        (("feature_generation_authorized",), True),
        (("feature_label_matrix_created",), True),
        (("backtest_execution_authorized",), True),
        (("model_training_authorized",), True),
        (("metric_computation_authorized",), True),
        (("strategy_scoring_performed",), True),
        (("predictive_usefulness",), "accepted"),
        (("profitability",), "accepted"),
        (("runtime_use",), "AUTHORIZED"),
        (("strategy_use",), "AUTHORIZED"),
        (("paper_trading",), "AUTHORIZED"),
        (("broker_execution",), "AUTHORIZED"),
        (("trade_recommendations_generated",), True),
        (("provider_requests_made_in_review",), True),
        (("market_data_acquisition_performed_in_review",), True),
        (("canonical_dataset_regenerated_in_review",), True),
        (("risk_controls",), []),
    ],
)
def test_validator_rejects_mutated_review(
    review: dict,
    path: tuple[str, ...],
    bad_value: object,
) -> None:
    mutated = deepcopy(review)
    mutated[path[0]] = bad_value
    with pytest.raises(MarketFlowAlgorithmStrategyCharterOperatorReviewError):
        validate_marketflow_algorithm_strategy_charter_operator_review_v1(mutated)


def test_validator_rejects_missing_review_digest(review: dict) -> None:
    review.pop("marketflow_algorithm_strategy_charter_operator_review_digest")
    with pytest.raises(MarketFlowAlgorithmStrategyCharterOperatorReviewError):
        validate_marketflow_algorithm_strategy_charter_operator_review_v1(review)


def test_validator_rejects_missing_per_ticker_digest(review: dict) -> None:
    review["per_ticker_strategy_charter_review_entries"][0].pop(
        "per_ticker_strategy_charter_review_digest"
    )
    with pytest.raises(MarketFlowAlgorithmStrategyCharterOperatorReviewError):
        validate_marketflow_algorithm_strategy_charter_operator_review_v1(review)


def test_markdown_includes_all_required_sections(review: dict) -> None:
    markdown = build_marketflow_algorithm_strategy_charter_operator_review_markdown_v1(review)
    required_sections = [
        "Title",
        "MarketFlow Algorithm Strategy Charter Operator Review",
        "Source Strategy Charter",
        "Bound Evidence",
        "Dataset and Universe",
        "Reviewed Algorithm Identity",
        "Reviewed Strategy Philosophy",
        "Reviewed Strategy Principles",
        "Reviewed Research Questions",
        "Reviewed Objective Families",
        "Reviewed Signal Families",
        "Reviewed Validation Metrics",
        "Reviewed Baselines",
        "Reviewed Phase Plan",
        "Reviewed Acceptance Gates",
        "Reviewed Non-Goals",
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
