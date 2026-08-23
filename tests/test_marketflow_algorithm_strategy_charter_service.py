from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import marketflow_algorithm_strategy_charter_service as service


@pytest.fixture
def charter() -> dict:
    return service.build_marketflow_algorithm_strategy_charter_v1()


def test_charter_builds_offline(charter: dict) -> None:
    assert charter["created_offline"] is True
    assert charter["provider_requests_made_in_charter"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_V1),
        (
            "charter_status",
            service.MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_READY_FOR_OPERATOR_REVIEW,
        ),
        ("charter_scope", service.STRATEGY_CHARTER_ONLY_NOT_EXECUTION),
        ("strategy_direction", service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE),
        ("source_final_archive_digest", service.EXPECTED_FINAL_ARCHIVE_DIGEST),
        ("source_archive_digest", service.EXPECTED_ARCHIVE_DIGEST),
        ("source_selection_digest", service.EXPECTED_SELECTION_DIGEST),
        ("feature_label_matrix_digest", service.EXPECTED_MATRIX_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_LABEL_VALUES_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_charter_identity_and_digest_bindings(
    charter: dict, field: str, expected: object
) -> None:
    assert charter[field] == expected


def test_universe_count_order_and_meta_are_preserved(charter: dict) -> None:
    assert charter["target_universe_count"] == 12
    assert charter["target_universe"] == service.TARGET_UNIVERSE
    assert charter["meta_record_count"] == 913
    assert charter["non_meta_record_count"] == 1003


def test_previous_chain_outcome_is_preserved(charter: dict) -> None:
    assert charter["previous_chain_status"] == "ARCHIVED_NOT_READY"
    assert charter["previous_predictive_usefulness_decision"] == "NOT_ACCEPTED"
    assert charter["previous_acceptance_readiness_decision"] == "NOT_READY"
    assert charter["previous_runtime_decision"] == "NOT_AUTHORIZED"
    assert charter["previous_profitability_decision"] == "NOT_ACCEPTED"


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_algorithm_strategy_charter_created",
        "marketflow_algorithm_strategy_charter_ready_for_operator_review",
        "marketflow_next_algorithm_phase_defined",
        "expectancy_first_research_direction_defined",
    ],
)
def test_charter_definition_flags_are_true(charter: dict, field: str) -> None:
    assert charter[field] is True


def test_strategy_philosophy_is_defined(charter: dict) -> None:
    assert charter["marketflow_algorithm_identity"] == service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE
    assert charter["marketflow_algorithm_definition"] == service.MARKETFLOW_ALGORITHM_DEFINITION
    assert charter["core_philosophy"] == service.CORE_PHILOSOPHY
    assert charter["primary_question"] == service.PRIMARY_QUESTION
    assert charter["secondary_question"] == service.SECONDARY_QUESTION


def test_strategy_principles_are_defined(charter: dict) -> None:
    assert charter["strategy_principles"] == service.STRATEGY_PRINCIPLES
    assert len(charter["strategy_principles"]) == 10


def test_research_questions_are_defined(charter: dict) -> None:
    assert charter["research_questions"] == service.RESEARCH_QUESTIONS
    assert len(charter["research_questions"]) == 10


def test_objective_families_are_candidates_and_not_generated(charter: dict) -> None:
    families = charter["candidate_objective_families"]
    assert list(families) == service.OBJECTIVE_FAMILY_NAMES
    assert all(value["status"] == "CANDIDATE_OBJECTIVE_NOT_GENERATED" for value in families.values())
    assert all(value["label_generation_authorized"] is False for value in families.values())
    assert all(value["target_creation_authorized"] is False for value in families.values())


def test_signal_families_are_candidates_and_not_generated(charter: dict) -> None:
    families = charter["candidate_signal_families"]
    assert list(families) == service.SIGNAL_FAMILY_NAMES
    assert all(value["status"] == "CANDIDATE_SIGNAL_NOT_GENERATED" for value in families.values())
    assert all(value["feature_generation_authorized"] is False for value in families.values())


def test_validation_metrics_are_candidates_and_not_computed(charter: dict) -> None:
    metrics = charter["candidate_validation_metrics"]
    assert list(metrics) == service.VALIDATION_METRIC_NAMES
    assert all(value["status"] == "CANDIDATE_METRIC_NOT_COMPUTED" for value in metrics.values())
    assert all(value["metric_computation_authorized"] is False for value in metrics.values())


def test_baselines_are_candidates_and_not_executed(charter: dict) -> None:
    baselines = charter["candidate_baselines"]
    assert list(baselines) == service.BASELINE_NAMES
    assert all(value["status"] == "CANDIDATE_BASELINE_NOT_EXECUTED" for value in baselines.values())
    assert all(value["model_training_authorized"] is False for value in baselines.values())
    assert all(value["backtest_authorized"] is False for value in baselines.values())


def test_phase_plan_is_defined_and_future_phases_not_started(charter: dict) -> None:
    phases = charter["proposed_phase_plan"]
    assert list(phases) == service.PHASE_NAMES
    assert phases["PHASE_1_STRATEGY_CHARTER"]["status"] == "COMPLETED_BY_THIS_ARTIFACT"
    assert all(
        phases[name]["status"] == "FUTURE_NOT_STARTED"
        for name in service.PHASE_NAMES[1:]
    )


def test_acceptance_gates_are_defined_and_closed(charter: dict) -> None:
    gates = charter["proposed_acceptance_gates"]
    assert list(gates) == service.ACCEPTANCE_GATE_NAMES
    assert all(value["status"] == "CLOSED_FUTURE_GATE" for value in gates.values())
    assert all(value["approval_created"] is False for value in gates.values())
    assert all(value["execution_created"] is False for value in gates.values())


def test_non_goals_are_defined(charter: dict) -> None:
    assert charter["non_goals"] == service.NON_GOALS
    assert len(charter["non_goals"]) == 13


def test_per_ticker_entries_and_digests_are_complete(charter: dict) -> None:
    entries = charter["per_ticker_charter_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_strategy_charter_digest"]) == 64 for entry in entries)
    meta = next(entry for entry in entries if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["charter_note"] == "PRESERVE_META_LIMITATION_IN_ALGORITHM_STRATEGY_CHARTER"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("label_generation_authorized", False),
        ("label_generation_performed", False),
        ("new_targets_created", False),
        ("feature_generation_authorized", False),
        ("feature_generation_performed", False),
        ("feature_label_matrix_created", False),
        ("backtest_execution_authorized", False),
        ("backtest_execution_performed", False),
        ("model_training_authorized", False),
        ("model_training_performed", False),
        ("metric_recomputation_performed_in_charter", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("provider_requests_made_in_charter", False),
        ("market_data_acquisition_performed_in_charter", False),
    ],
)
def test_charter_authority_and_activity_boundaries(
    charter: dict, field: str, expected: object
) -> None:
    assert charter[field] == expected


def test_next_chain_gates_and_risk_controls_are_defined(charter: dict) -> None:
    assert charter["next_chain"] == service.NEXT_CHAIN
    assert charter["next_gates"] == service.NEXT_GATES
    assert charter["risk_controls"] == service.RISK_CONTROLS
    assert len(charter["next_chain"]) == 6
    assert len(charter["next_gates"]) == 10
    assert len(charter["risk_controls"]) == 23


def test_checklist_passes(charter: dict) -> None:
    summary = charter["charter_summary"]
    assert summary["total_checks"] == 58
    assert summary["passed_checks"] == 58
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


def test_charter_digest_is_deterministic(charter: dict) -> None:
    rebuilt = service.build_marketflow_algorithm_strategy_charter_v1()
    assert rebuilt["marketflow_algorithm_strategy_charter_v1_digest"] == charter[
        "marketflow_algorithm_strategy_charter_v1_digest"
    ]


def test_per_ticker_digests_are_deterministic(charter: dict) -> None:
    rebuilt = service.build_marketflow_algorithm_strategy_charter_v1()
    assert [row["per_ticker_strategy_charter_digest"] for row in rebuilt["per_ticker_charter_entries"]] == [
        row["per_ticker_strategy_charter_digest"] for row in charter["per_ticker_charter_entries"]
    ]


def test_validator_accepts_valid_charter(charter: dict) -> None:
    validation = service.validate_marketflow_algorithm_strategy_charter_v1(charter)
    assert validation["status"] == "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_VALID"
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("charter_status", "WRONG"),
        ("charter_scope", "WRONG"),
        ("strategy_direction", "WRONG"),
        ("source_final_archive_digest", "0" * 64),
        ("target_universe", list(reversed(service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("marketflow_algorithm_strategy_charter_created", False),
        ("marketflow_algorithm_strategy_charter_ready_for_operator_review", False),
        ("expectancy_first_research_direction_defined", False),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("label_generation_authorized", True),
        ("new_targets_created", True),
        ("feature_generation_authorized", True),
        ("feature_label_matrix_created", True),
        ("backtest_execution_authorized", True),
        ("model_training_authorized", True),
        ("metric_recomputation_performed_in_charter", True),
        ("provider_requests_made_in_charter", True),
        ("market_data_acquisition_performed_in_charter", True),
        ("canonical_dataset_regenerated_in_charter", True),
    ],
)
def test_validator_rejects_invalid_charter_values(
    charter: dict, field: str, value: object
) -> None:
    invalid = deepcopy(charter)
    invalid[field] = value
    with pytest.raises(service.MarketFlowAlgorithmStrategyCharterError):
        service.validate_marketflow_algorithm_strategy_charter_v1(invalid)


@pytest.mark.parametrize(
    "field",
    [
        "strategy_philosophy",
        "strategy_principles",
        "research_questions",
        "candidate_objective_families",
        "candidate_signal_families",
        "candidate_validation_metrics",
        "candidate_baselines",
        "proposed_phase_plan",
        "proposed_acceptance_gates",
        "non_goals",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_charter_section(
    charter: dict, field: str
) -> None:
    invalid = deepcopy(charter)
    invalid.pop(field)
    with pytest.raises(service.MarketFlowAlgorithmStrategyCharterError):
        service.validate_marketflow_algorithm_strategy_charter_v1(invalid)


def test_validator_rejects_missing_charter_digest(charter: dict) -> None:
    invalid = deepcopy(charter)
    invalid.pop("marketflow_algorithm_strategy_charter_v1_digest")
    with pytest.raises(service.MarketFlowAlgorithmStrategyCharterError):
        service.validate_marketflow_algorithm_strategy_charter_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(charter: dict) -> None:
    invalid = deepcopy(charter)
    invalid["per_ticker_charter_entries"][0].pop("per_ticker_strategy_charter_digest")
    with pytest.raises(service.MarketFlowAlgorithmStrategyCharterError):
        service.validate_marketflow_algorithm_strategy_charter_v1(invalid)


def test_writer_uses_isolated_output_and_refuses_overwrite(tmp_path) -> None:
    result = service.write_marketflow_algorithm_strategy_charter_v1(tmp_path)
    assert result["path"].endswith("marketflow_algorithm_strategy_charter_v1.json")
    with pytest.raises(service.MarketFlowAlgorithmStrategyCharterError):
        service.write_marketflow_algorithm_strategy_charter_v1(tmp_path)


def test_markdown_includes_required_sections(charter: dict) -> None:
    markdown = service.build_marketflow_algorithm_strategy_charter_markdown_v1(charter)
    required = [
        "Title",
        "MarketFlow Algorithm Strategy Charter v1",
        "Source Final Archive Summary",
        "Bound Evidence",
        "Dataset and Universe",
        "Why the Previous Chain Was Archived",
        "Algorithm Identity",
        "Strategy Philosophy",
        "Strategy Principles",
        "Research Questions",
        "Candidate Objective Families",
        "Candidate Signal Families",
        "Candidate Validation Metrics",
        "Candidate Baselines",
        "Proposed Phase Plan",
        "Acceptance Gates",
        "Non-Goals",
        "Per-Ticker Charter Summary",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in required)
