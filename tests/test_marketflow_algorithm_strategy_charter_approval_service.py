from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_algorithm_strategy_charter_approval_service as approval_service,
)
from marketflow.services import (
    marketflow_algorithm_strategy_charter_operator_review_service as review_service,
)


def _attestation(**overrides: object) -> dict:
    source = review_service.build_marketflow_algorithm_strategy_charter_operator_review_v1()
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T12:00:00Z",
        "operator_attestation_phrase": approval_service.REQUIRED_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_charter_review_digest": approval_service.EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST,
        "operator_confirms_charter_digest": approval_service.EXPECTED_SOURCE_CHARTER_DIGEST,
        "operator_confirms_final_archive_digest": source["source_final_archive_digest"],
        "operator_confirms_records_digest": source["records_digest"],
        "operator_confirms_target_universe": list(source["target_universe"]),
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_strategy_direction": approval_service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        **{
            field: True
            for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
        },
    }
    values.update(overrides)
    return approval_service.build_marketflow_algorithm_strategy_charter_approval_attestation_v1(
        **values
    )


@pytest.fixture
def approval() -> dict:
    return approval_service.build_marketflow_algorithm_strategy_charter_approval_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_all_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == (
        approval_service.OPERATOR_DECISION_APPROVE_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER
    )
    assert attestation["approved_strategy_direction"] == (
        approval_service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE
    )
    assert attestation["operator_attestation_version"] == (
        approval_service.OPERATOR_ATTESTATION_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_V1
    )
    assert all(
        attestation[field] is True
        for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_builds_offline_and_writer_is_non_overwriting(
    tmp_path,
) -> None:
    result = approval_service.write_marketflow_algorithm_strategy_charter_approval_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )
    path = tmp_path / "marketflow_algorithm_strategy_charter_approval_v1.json"
    payload = json.loads(path.read_text())
    assert payload["created_offline"] is True
    assert payload["provider_requests_made_in_approval"] is False
    assert result["marketflow_algorithm_strategy_charter_approval_digest"] == payload[
        "marketflow_algorithm_strategy_charter_approval_digest"
    ]
    with pytest.raises(
        approval_service.MarketFlowAlgorithmStrategyCharterApprovalError
    ):
        approval_service.write_marketflow_algorithm_strategy_charter_approval_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVED"),
        ("approval_status", "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVED"),
        ("approval_scope", "STRATEGY_CHARTER_APPROVAL_ONLY"),
        ("approved_strategy_direction", "EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE"),
        ("source_charter_review_digest", "d75e541f3f9d16593eb3a4da6f4f6de7a451c259295ce4e3e8f09171bbcbe8f9"),
        ("source_charter_digest", "3f5e3fd4088c38c5783618642c378874d2c0fbcc72954945cdca9fca68281853"),
        ("source_final_archive_digest", "31b61c934f3bc4970973dd2cfc0e18fb3ea4ca76e02c815bed5cf509e4a5440b"),
        ("feature_label_matrix_digest", "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"),
        ("feature_values_digest", "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"),
        ("redesigned_label_values_digest", "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"),
        ("records_digest", "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"),
        ("marketflow_algorithm_strategy_charter_approved", True),
        ("marketflow_algorithm_strategy_charter_authorized", True),
        ("ready_for_expectancy_objective_candidate", True),
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
    ],
)
def test_required_top_level_values(
    approval: dict,
    field: str,
    expected: object,
) -> None:
    assert approval[field] == expected


def test_universe_order_counts_and_meta_limitation_are_preserved(
    approval: dict,
) -> None:
    assert approval["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]
    assert approval["target_universe_count"] == 12
    assert approval["total_canonical_record_count"] == 11946
    assert approval["meta_record_count"] == 913
    assert approval["non_meta_record_count"] == 1003
    assert approval["meta_reduced_record_count_preserved"] is True


def test_operator_decision_and_exact_phrase_are_bound(approval: dict) -> None:
    operator = approval["operator_attestation"]
    assert operator["operator_decision"] == (
        "APPROVE_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER"
    )
    assert operator["operator_attestation_phrase"] == (
        approval_service.REQUIRED_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_ATTESTATION_PHRASE
    )


def test_approved_strategy_philosophy_is_present_and_research_only(
    approval: dict,
) -> None:
    philosophy = approval["approved_strategy_philosophy"]
    assert philosophy["approval_status"] == (
        "APPROVED_FOR_FUTURE_RESEARCH_PLANNING_ONLY"
    )
    assert philosophy["research_only"] is True
    assert philosophy["non_actionable"] is True
    assert philosophy["core_philosophy"] == (
        "Do not optimize for classification accuracy alone. Optimize for tradable expectancy, "
        "risk-adjusted opportunity, and abstention quality."
    )


def test_all_strategy_principles_are_approved_for_future_planning_only(
    approval: dict,
) -> None:
    rows = approval["approved_strategy_principles"]
    assert len(rows) == 10
    assert all(
        row["approval_status"] == "APPROVED_FOR_FUTURE_RESEARCH_PLANNING_ONLY"
        for row in rows.values()
    )
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows.values())


def test_all_research_questions_remain_unanswered(approval: dict) -> None:
    rows = approval["approved_research_questions"]
    assert len(rows) == 10
    assert all(row["answered_by_this_approval"] is False for row in rows)
    assert all(row["requires_future_research"] is True for row in rows)


@pytest.mark.parametrize(
    ("field", "count", "status_field", "status", "approval_status"),
    [
        (
            "approved_objective_families",
            10,
            "objective_status",
            "CANDIDATE_OBJECTIVE_NOT_GENERATED",
            "APPROVED_FOR_FUTURE_EXPECTANCY_OBJECTIVE_CANDIDACY_ONLY",
        ),
        (
            "approved_signal_families",
            10,
            "signal_status",
            "CANDIDATE_SIGNAL_NOT_GENERATED",
            "APPROVED_FOR_FUTURE_SIGNAL_CANDIDACY_ONLY",
        ),
        (
            "approved_validation_metrics",
            14,
            "metric_status",
            "CANDIDATE_METRIC_NOT_COMPUTED",
            "APPROVED_FOR_FUTURE_METRIC_CANDIDACY_ONLY",
        ),
        (
            "approved_baselines",
            7,
            "baseline_status",
            "CANDIDATE_BASELINE_NOT_EXECUTED",
            "APPROVED_FOR_FUTURE_BASELINE_CANDIDACY_ONLY",
        ),
    ],
)
def test_candidate_catalogs_are_approved_without_execution(
    approval: dict,
    field: str,
    count: int,
    status_field: str,
    status: str,
    approval_status: str,
) -> None:
    rows = approval[field]
    assert len(rows) == count
    assert all(row[status_field] == status for row in rows.values())
    assert all(row["approval_status"] == approval_status for row in rows.values())


def test_phase_plan_is_approved_as_a_future_staged_plan(approval: dict) -> None:
    rows = list(approval["approved_phase_plan"].values())
    assert len(rows) == 9
    assert rows[0]["status"] == "COMPLETED_BY_SOURCE_ARTIFACT"
    assert rows[1]["status"] == "FUTURE_READY_FOR_CANDIDATE_CREATION"
    assert all(row["status"] == "FUTURE_NOT_STARTED" for row in rows[2:])


def test_acceptance_gates_are_approved_but_remain_closed(
    approval: dict,
) -> None:
    rows = approval["approved_acceptance_gates"]
    assert len(rows) == 10
    assert all(
        row["approval_status"] == "APPROVED_AS_FUTURE_GATE_ONLY"
        for row in rows.values()
    )
    assert all(row["gate_status"] == "CLOSED_FUTURE_GATE" for row in rows.values())
    assert all(row["opened_by_this_approval"] is False for row in rows.values())


def test_non_goals_are_preserved(approval: dict) -> None:
    assert len(approval["non_goals"]) == 13
    assert all(row["active"] is True for row in approval["non_goals"])


def test_per_ticker_entries_and_digests_are_complete(approval: dict) -> None:
    rows = approval["per_ticker_strategy_charter_approval_entries"]
    assert len(rows) == 12
    assert all(
        row["per_ticker_strategy_charter_approval_digest"]
        == approval_service.per_ticker_marketflow_algorithm_strategy_charter_approval_digest_v1(
            row
        )
        for row in rows
    )
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["approval_note"] == (
        "PRESERVE_META_LIMITATION_IN_ALGORITHM_STRATEGY_CHARTER_APPROVAL"
    )
    assert all(
        row["historical_record_count"] == 1003
        and row["meta_reduced_record_count_flag"] is False
        for row in rows
        if row["ticker"] != "META"
    )


def test_next_chain_next_gates_and_risk_controls_are_defined(
    approval: dict,
) -> None:
    assert len(approval["next_chain"]) == 10
    assert len(approval["next_gates"]) == 10
    assert len(approval["risk_controls"]) == 24
    assert "approval_does_not_create_expectancy_objective_candidate" in approval[
        "risk_controls"
    ]
    assert "all_outputs_research_only" in approval["risk_controls"]


def test_checklist_passes_and_summary_is_closed(approval: dict) -> None:
    assert len(approval["approval_checklist"]) == 62
    assert all(row["status"] == "PASS" for row in approval["approval_checklist"])
    summary = approval["approval_summary"]
    assert summary["total_checks"] == 62
    assert summary["passed_checks"] == 62
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["strategy_charter_approved"] is True
    assert summary["ready_for_expectancy_objective_candidate"] is True
    assert summary["expectancy_objective_candidate_created"] is False
    assert summary["runtime_authorized"] is False


def test_approval_and_per_ticker_digests_are_deterministic(
    approval: dict,
) -> None:
    again = approval_service.build_marketflow_algorithm_strategy_charter_approval_v1(
        operator_attestation=_attestation()
    )
    digest = approval["marketflow_algorithm_strategy_charter_approval_digest"]
    assert digest == again["marketflow_algorithm_strategy_charter_approval_digest"]
    assert digest == (
        approval_service.marketflow_algorithm_strategy_charter_approval_digest_v1(
            approval
        )
    )
    assert [
        row["per_ticker_strategy_charter_approval_digest"]
        for row in approval["per_ticker_strategy_charter_approval_entries"]
    ] == [
        row["per_ticker_strategy_charter_approval_digest"]
        for row in again["per_ticker_strategy_charter_approval_entries"]
    ]


def test_builder_accepts_exact_source_review() -> None:
    source = review_service.build_marketflow_algorithm_strategy_charter_operator_review_v1()
    approval = approval_service.build_marketflow_algorithm_strategy_charter_approval_v1(
        source_review=source,
        operator_attestation=_attestation(),
    )
    assert approval["source_charter_review_digest"] == (
        approval_service.EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST
    )


def test_builder_rejects_changed_source_review() -> None:
    source = review_service.build_marketflow_algorithm_strategy_charter_operator_review_v1()
    source["strategy_direction"] = "CHANGED"
    with pytest.raises(ValueError):
        approval_service.build_marketflow_algorithm_strategy_charter_approval_v1(
            source_review=source,
            operator_attestation=_attestation(),
        )


def test_validator_accepts_valid_approval(approval: dict) -> None:
    result = approval_service.validate_marketflow_algorithm_strategy_charter_approval_v1(
        approval
    )
    assert result["status"] == (
        "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_VALID"
    )
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("approved_strategy_direction", "WRONG"),
        ("source_charter_review_digest", "0" * 64),
        ("source_charter_digest", "0" * 64),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("marketflow_algorithm_strategy_charter_approved", False),
        ("marketflow_algorithm_strategy_charter_authorized", False),
        ("ready_for_expectancy_objective_candidate", False),
        ("expectancy_objective_candidate_created", True),
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
        ("provider_requests_made_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True),
        ("canonical_dataset_regenerated_in_approval", True),
        ("approved_strategy_principles", {}),
        ("approved_objective_families", {}),
        ("approved_signal_families", {}),
        ("approved_validation_metrics", {}),
        ("approved_baselines", {}),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_mutated_approval(
    approval: dict,
    field: str,
    bad_value: object,
) -> None:
    mutated = deepcopy(approval)
    mutated[field] = bad_value
    with pytest.raises(
        approval_service.MarketFlowAlgorithmStrategyCharterApprovalError
    ):
        approval_service.validate_marketflow_algorithm_strategy_charter_approval_v1(
            mutated
        )


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_confirms_charter_review_digest", "0" * 64),
        ("operator_confirms_charter_digest", "0" * 64),
        ("operator_confirms_target_universe", ["MSFT"]),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_meta_record_count", 1003),
        ("operator_confirms_strategy_direction", "WRONG"),
        ("operator_confirms_approval_scope_only", False),
        ("operator_confirms_no_label_generation", False),
        ("operator_confirms_no_runtime_migration_approval", False),
        ("operator_confirms_no_broker_execution", False),
    ],
)
def test_builder_rejects_bad_attestation(
    field: str,
    bad_value: object,
) -> None:
    with pytest.raises(
        approval_service.MarketFlowAlgorithmStrategyCharterApprovalError
    ):
        approval_service.build_marketflow_algorithm_strategy_charter_approval_v1(
            operator_attestation=_attestation(**{field: bad_value})
        )


def test_builder_rejects_missing_attestation() -> None:
    with pytest.raises(
        approval_service.MarketFlowAlgorithmStrategyCharterApprovalError
    ):
        approval_service.build_marketflow_algorithm_strategy_charter_approval_v1(
            operator_attestation={}
        )


def test_validator_rejects_missing_approval_digest(approval: dict) -> None:
    approval.pop("marketflow_algorithm_strategy_charter_approval_digest")
    with pytest.raises(
        approval_service.MarketFlowAlgorithmStrategyCharterApprovalError
    ):
        approval_service.validate_marketflow_algorithm_strategy_charter_approval_v1(
            approval
        )


def test_validator_rejects_missing_per_ticker_digest(approval: dict) -> None:
    approval["per_ticker_strategy_charter_approval_entries"][0].pop(
        "per_ticker_strategy_charter_approval_digest"
    )
    with pytest.raises(
        approval_service.MarketFlowAlgorithmStrategyCharterApprovalError
    ):
        approval_service.validate_marketflow_algorithm_strategy_charter_approval_v1(
            approval
        )


def test_markdown_includes_all_required_sections(approval: dict) -> None:
    markdown = (
        approval_service.build_marketflow_algorithm_strategy_charter_approval_markdown_v1(
            approval
        )
    )
    required_sections = [
        "Title",
        "MarketFlow Algorithm Strategy Charter Approval",
        "Operator Attestation",
        "Source Charter Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Approved Algorithm Identity",
        "Approved Strategy Philosophy",
        "Approved Strategy Principles",
        "Approved Research Questions",
        "Approved Objective Families",
        "Approved Signal Families",
        "Approved Validation Metrics",
        "Approved Baselines",
        "Approved Phase Plan",
        "Approved Acceptance Gates",
        "Non-Goals",
        "Per-Ticker Approval Summary",
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
