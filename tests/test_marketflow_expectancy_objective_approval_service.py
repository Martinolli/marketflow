from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_expectancy_objective_approval_service as approval_service,
)
from marketflow.services import (
    marketflow_expectancy_objective_candidate_operator_review_service as review_service,
)


def _attestation(**overrides: object) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": approval_service.REQUIRED_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_candidate_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_strategy_charter_approval_digest": approval_service.EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
        "operator_confirms_records_digest": "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044",
        "operator_confirms_target_universe": [
            "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
            "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
        ],
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_objective_path": "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT",
        "operator_confirms_approval_scope_only": True,
        "operator_confirms_objective_selected": True,
        "operator_confirms_objective_approved": True,
        "operator_confirms_ready_for_design_execution": True,
        "operator_confirms_no_objective_generation": True,
        "operator_confirms_no_label_generation": True,
        "operator_confirms_no_new_targets": True,
        "operator_confirms_no_feature_generation": True,
        "operator_confirms_no_feature_label_matrix": True,
        "operator_confirms_no_backtest_execution": True,
        "operator_confirms_no_model_training": True,
        "operator_confirms_no_metric_computation": True,
        "operator_confirms_no_strategy_scoring": True,
        "operator_confirms_no_predictive_usefulness_acceptance": True,
        "operator_confirms_no_profitability_acceptance": True,
        "operator_confirms_no_runtime_migration_approval": True,
        "operator_confirms_no_strategy_authorization": True,
        "operator_confirms_no_paper_trading": True,
        "operator_confirms_no_broker_execution": True,
        "operator_confirms_no_trade_recommendations": True,
        "operator_confirms_no_api_key_storage_or_printing": True,
        "operator_confirms_no_raw_payload_commit": True,
    }
    values.update(overrides)
    return approval_service.build_marketflow_expectancy_objective_approval_attestation_v1(
        **values
    )


@pytest.fixture(scope="module")
def approval() -> dict:
    return approval_service.build_marketflow_expectancy_objective_approval_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == "APPROVE_EXPECTANCY_OBJECTIVE"
    assert attestation["selected_objective_path"] == (
        "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
    )
    assert attestation["approved_strategy_direction"] == (
        "EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE"
    )
    assert attestation["operator_attestation_version"] == (
        "marketflow_expectancy_objective_approval_operator_attestation_v1"
    )
    assert all(
        attestation[field] is True
        for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_builds_offline_and_writer_is_non_overwriting(tmp_path) -> None:
    result = approval_service.write_marketflow_expectancy_objective_approval_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )
    path = tmp_path / "marketflow_expectancy_objective_approval_v1.json"
    payload = json.loads(path.read_text())
    assert payload["created_offline"] is True
    assert payload["provider_requests_made_in_approval"] is False
    assert result["marketflow_expectancy_objective_approval_digest"] == (
        payload["marketflow_expectancy_objective_approval_digest"]
    )
    with pytest.raises(approval_service.MarketFlowExpectancyObjectiveApprovalError):
        approval_service.write_marketflow_expectancy_objective_approval_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVED"),
        ("approval_status", "MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVED"),
        ("approval_scope", "EXPECTANCY_OBJECTIVE_APPROVAL_ONLY"),
        ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
        ("approved_primary_objective_cluster", "CLUSTER_EXPECTANCY_AND_PAYOFF"),
        ("approved_supporting_objective_cluster", "CLUSTER_ABSTENTION_AND_NO_TRADE"),
        ("approved_secondary_objective_cluster", "CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE"),
        ("source_expectancy_objective_candidate_review_digest", "baac33f292d77d26eae6eacc4cffaa5cdabe17785cb2c090c053c82d1bfe551d"),
        ("source_expectancy_objective_candidate_digest", "9b241ab1be15921384d97d75a11ac7858065d041c0b8a02144e97c3e3ed3bc17"),
        ("source_strategy_charter_approval_digest", "ea6c77007c4827fbdd4015425bc92af40eb59b08daba3d5c2e41090df0762b92"),
        ("feature_label_matrix_digest", "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"),
        ("feature_values_digest", "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"),
        ("redesigned_label_values_digest", "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"),
        ("records_digest", "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"),
        ("expectancy_objective_selected", True),
        ("expectancy_objective_approved", True),
        ("expectancy_objective_authorized", True),
        ("expectancy_objective_approval_created", True),
        ("ready_for_expectancy_objective_design_execution", True),
        ("expectancy_objective_generation_authorized", False),
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


def test_operator_decision_and_exact_attestation_phrase_are_bound(
    approval: dict,
) -> None:
    operator = approval["operator_attestation"]
    assert operator["operator_decision"] == "APPROVE_EXPECTANCY_OBJECTIVE"
    assert operator["operator_attestation_phrase"] == (
        approval_service.REQUIRED_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_ATTESTATION_PHRASE
    )


def test_builder_accepts_exact_source_review() -> None:
    source = review_service.build_marketflow_expectancy_objective_candidate_operator_review_v1()
    approval = approval_service.build_marketflow_expectancy_objective_approval_v1(
        source_review=source,
        operator_attestation=_attestation(),
    )
    assert approval["source_expectancy_objective_candidate_review_digest"] == (
        approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
    )


def test_builder_rejects_changed_source_review() -> None:
    source = review_service.build_marketflow_expectancy_objective_candidate_operator_review_v1()
    source["candidate_direction"] = "CHANGED"
    with pytest.raises(ValueError):
        approval_service.build_marketflow_expectancy_objective_approval_v1(
            source_review=source,
            operator_attestation=_attestation(),
        )


def test_approved_objective_philosophy_and_path_are_present(approval: dict) -> None:
    philosophy = approval["approved_objective_philosophy"]
    assert philosophy["approved_objective_path"] == (
        "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
    )
    assert philosophy["approved_objective_boundary"].startswith("Approval-only")
    assert approval["approved_objective_path"] == approval["selected_objective_path"]


def test_all_objective_families_are_approved_for_future_design_only(
    approval: dict,
) -> None:
    rows = approval["approved_objective_families"]
    assert len(rows) == 10
    assert all(
        row["approval_status"]
        == "APPROVED_FOR_FUTURE_OBJECTIVE_DESIGN_EXECUTION_ONLY"
        for row in rows.values()
    )
    assert all(row["objective_status"] == "OBJECTIVE_CANDIDATE_DEFINED_NOT_GENERATED" for row in rows.values())
    assert all(row["label_generation_authorized"] is False for row in rows.values())


def test_all_objective_clusters_are_approved_with_exact_roles(
    approval: dict,
) -> None:
    rows = approval["approved_objective_clusters"]
    assert len(rows) == 4
    assert rows["CLUSTER_EXPECTANCY_AND_PAYOFF"]["approval_status"] == (
        "APPROVED_PRIMARY_CLUSTER_FOR_FUTURE_DESIGN_EXECUTION"
    )
    assert rows["CLUSTER_ABSTENTION_AND_NO_TRADE"]["approval_status"] == (
        "APPROVED_SUPPORTING_CLUSTER_FOR_FUTURE_DESIGN_EXECUTION"
    )
    assert rows["CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE"]["approval_status"] == (
        "APPROVED_SECONDARY_CLUSTER_FOR_FUTURE_DESIGN_EXECUTION"
    )


def test_research_questions_are_approved_but_unanswered(approval: dict) -> None:
    rows = approval["approved_research_questions"]
    assert len(rows) == 10
    assert all(row["answered_by_this_approval"] is False for row in rows)
    assert all(row["requires_future_research"] is True for row in rows)


def test_design_dimensions_are_approved_but_unexecuted(approval: dict) -> None:
    rows = approval["approved_design_dimensions"]
    assert len(rows) == 12
    assert all(row["dimension_status"] == "CANDIDATE_DIMENSION_NOT_EXECUTED" for row in rows.values())
    assert all(row["generation_authorized"] is False for row in rows.values())


def test_future_outputs_are_authorized_not_generated(approval: dict) -> None:
    rows = approval["approved_future_outputs"]
    assert len(rows) == 11
    assert all(row["approval_status"] == "AUTHORIZED_NOT_GENERATED" for row in rows.values())
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows.values())


def test_per_ticker_entries_and_digests_are_complete(approval: dict) -> None:
    rows = approval["per_ticker_expectancy_objective_approval_entries"]
    assert len(rows) == 12
    assert all(
        row["per_ticker_expectancy_objective_approval_digest"]
        == approval_service.per_ticker_expectancy_objective_approval_digest_v1(row)
        for row in rows
    )
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["approval_note"] == (
        "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_APPROVAL"
    )
    assert all(
        row["historical_record_count"] == 1003
        and row["meta_reduced_record_count_flag"] is False
        for row in rows
        if row["ticker"] != "META"
    )


def test_next_chain_gates_and_risk_controls_are_exact(approval: dict) -> None:
    assert len(approval["next_chain"]) == 8
    assert len(approval["next_gates"]) == 9
    assert len(approval["risk_controls"]) == 23
    assert "approval_does_not_generate_labels" in approval["risk_controls"]
    assert "all_outputs_research_only" in approval["risk_controls"]


def test_checklist_passes_and_summary_is_approval_only(approval: dict) -> None:
    assert len(approval["approval_checklist"]) == 62
    assert all(row["status"] == "PASS" for row in approval["approval_checklist"])
    summary = approval["approval_summary"]
    assert summary["total_checks"] == 62
    assert summary["passed_checks"] == 62
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["expectancy_objective_selected"] is True
    assert summary["ready_for_expectancy_objective_design_execution"] is True
    assert summary["objective_generation_authorized"] is False
    assert summary["runtime_authorized"] is False


def test_approval_and_per_ticker_digests_are_deterministic(approval: dict) -> None:
    again = approval_service.build_marketflow_expectancy_objective_approval_v1(
        operator_attestation=_attestation()
    )
    digest = approval["marketflow_expectancy_objective_approval_digest"]
    assert digest == again["marketflow_expectancy_objective_approval_digest"]
    assert digest == approval_service.marketflow_expectancy_objective_approval_digest_v1(
        approval
    )
    assert [
        row["per_ticker_expectancy_objective_approval_digest"]
        for row in approval["per_ticker_expectancy_objective_approval_entries"]
    ] == [
        row["per_ticker_expectancy_objective_approval_digest"]
        for row in again["per_ticker_expectancy_objective_approval_entries"]
    ]


def test_validator_accepts_valid_approval(approval: dict) -> None:
    result = approval_service.validate_marketflow_expectancy_objective_approval_v1(
        approval
    )
    assert result["status"] == "MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_VALID"
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("selected_objective_path", "WRONG"),
        ("approved_primary_objective_cluster", "WRONG"),
        ("approved_supporting_objective_cluster", "WRONG"),
        ("approved_secondary_objective_cluster", "WRONG"),
        ("source_expectancy_objective_candidate_review_digest", "0" * 64),
        ("source_expectancy_objective_candidate_digest", "0" * 64),
        ("source_strategy_charter_approval_digest", "0" * 64),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("expectancy_objective_selected", False),
        ("expectancy_objective_approved", False),
        ("expectancy_objective_authorized", False),
        ("ready_for_expectancy_objective_design_execution", False),
        ("expectancy_objective_generation_authorized", True),
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
        ("approved_objective_philosophy", {}),
        ("approved_objective_families", {}),
        ("approved_objective_clusters", {}),
        ("approved_research_questions", []),
        ("approved_design_dimensions", {}),
        ("approved_future_outputs", {}),
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
    with pytest.raises(approval_service.MarketFlowExpectancyObjectiveApprovalError):
        approval_service.validate_marketflow_expectancy_objective_approval_v1(
            mutated
        )


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("selected_objective_path", "WRONG"),
        ("approved_strategy_direction", "WRONG"),
        ("operator_confirms_candidate_review_digest", "0" * 64),
        ("operator_confirms_candidate_digest", "0" * 64),
        ("operator_confirms_strategy_charter_approval_digest", "0" * 64),
        ("operator_confirms_records_digest", "0" * 64),
        ("operator_confirms_target_universe", ["MSFT"]),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_meta_record_count", 1003),
        ("operator_confirms_non_meta_record_count", 913),
        ("operator_confirms_selected_objective_path", "WRONG"),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
    ]
    + [(field, False) for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS],
)
def test_builder_rejects_incorrect_or_incomplete_attestation(
    field: str,
    bad_value: object,
) -> None:
    attestation = _attestation()
    attestation[field] = bad_value
    with pytest.raises(approval_service.MarketFlowExpectancyObjectiveApprovalError):
        approval_service.build_marketflow_expectancy_objective_approval_v1(
            operator_attestation=attestation
        )


def test_validator_rejects_missing_approval_digest(approval: dict) -> None:
    mutated = deepcopy(approval)
    mutated.pop("marketflow_expectancy_objective_approval_digest")
    with pytest.raises(approval_service.MarketFlowExpectancyObjectiveApprovalError):
        approval_service.validate_marketflow_expectancy_objective_approval_v1(
            mutated
        )


def test_validator_rejects_missing_per_ticker_digest(approval: dict) -> None:
    mutated = deepcopy(approval)
    mutated["per_ticker_expectancy_objective_approval_entries"][0].pop(
        "per_ticker_expectancy_objective_approval_digest"
    )
    with pytest.raises(approval_service.MarketFlowExpectancyObjectiveApprovalError):
        approval_service.validate_marketflow_expectancy_objective_approval_v1(
            mutated
        )


def test_markdown_includes_all_required_sections(approval: dict) -> None:
    markdown = approval_service.build_marketflow_expectancy_objective_approval_markdown_v1(
        approval
    )
    required_sections = [
        "Title",
        "Expectancy Objective Approval v1",
        "Operator Attestation",
        "Source Expectancy Objective Candidate Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Approved Objective Basis",
        "Approved Objective Philosophy",
        "Approved Objective Path",
        "Approved Objective Families",
        "Approved Objective Clusters",
        "Approved Research Questions",
        "Approved Design Dimensions",
        "Approved Future Outputs",
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
