from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow.services import predictive_experiment_plan_candidate_service as plan_service


def _plan() -> dict[str, Any]:
    return plan_service.build_predictive_experiment_plan_candidate_v1()


def _mutated_plan(field: str, value: Any) -> dict[str, Any]:
    plan = _plan()
    plan[field] = value
    return plan


def test_plan_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        plan_service.acquisition,
        "fetch_massive_custom_bars_v1",
        fail_provider_call,
    )

    plan = _plan()

    assert plan["created_offline"] is True
    assert plan["provider_requests_made"] is False


def test_artifact_kind_and_status_are_predictive_experiment_plan_candidate():
    plan = _plan()

    assert plan["artifact_kind"] == (
        plan_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE
    )
    assert plan["plan_status"] == plan_service.PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW


def test_source_evidence_digests_are_bound():
    plan = _plan()

    assert plan["predictive_usefulness_review_candidate_digest"] == (
        plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
    )
    assert plan["predictive_usefulness_review_candidate_review_package_digest"] == (
        plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert plan["campaign_execution_results_review_package_digest"] == (
        plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert plan["swing_registry_approval_digest"] == (
        plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert plan["position_swing_registry_approval_digest"] == (
        plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_experiment_scope_is_research_only_and_aapl_only():
    plan = _plan()

    assert plan["experiment_scope"]["research_only"] is True
    assert plan["ticker_universe"] == ["AAPL"]
    assert plan["date_range"] == {"start": "2022-01-01", "end": "2025-12-31"}


def test_profiles_include_swing_and_position_swing():
    profiles = [item["profile"] for item in _plan()["dataset_profiles"]]

    assert profiles == ["SWING", "POSITION_SWING"]


def test_experiment_design_sections_are_defined():
    plan = _plan()

    assert [item["label"] for item in plan["label_definitions"]] == plan_service.LABEL_DEFINITIONS
    assert [item["feature_family"] for item in plan["feature_family_plan"]] == (
        plan_service.FEATURE_FAMILIES
    )
    assert plan["walk_forward_plan"]["method"] == "chronological_walk_forward"
    assert plan["out_of_sample_plan"]["no_future_leakage"] is True
    assert plan["baseline_comparisons"] == plan_service.BASELINE_COMPARISONS
    assert [item["metric"] for item in plan["signal_quality_metrics"]] == (
        plan_service.SIGNAL_QUALITY_METRICS
    )
    assert plan["stability_checks"] == plan_service.STABILITY_CHECKS
    assert plan["false_positive_false_negative_analysis"]["status"] == "PLANNED_ONLY"
    assert plan["leakage_controls"] == plan_service.LEAKAGE_CONTROLS


def test_planned_outputs_are_not_generated_and_research_only():
    outputs = _plan()["planned_outputs"]

    assert {item["generation_status"] for item in outputs} == {plan_service.PLANNED_NOT_GENERATED}
    assert {item["output_label"] for item in outputs} == {
        plan_service.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_execution_gates_and_risk_controls_are_defined():
    plan = _plan()

    assert plan["execution_gates"] == plan_service.EXECUTION_GATES
    assert plan["risk_controls"] == plan_service.RISK_CONTROLS


def test_execution_acceptance_and_runtime_boundaries_remain_closed():
    plan = _plan()

    assert plan["predictive_experiment_execution_authorized"] is False
    assert plan["predictive_experiment_executed"] is False
    assert plan["walk_forward_validation_performed"] is False
    assert plan["out_of_sample_evaluation_performed"] is False
    assert plan["new_strategy_scoring_performed"] is False
    assert plan["trade_recommendations_generated"] is False
    assert plan["predictive_usefulness"] == plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert plan["predictive_usefulness_acceptance_ready"] is False
    assert plan["profitability"] == plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert plan["profitability_acceptance_ready"] is False
    assert plan["runtime_migration_recommended"] is False
    assert plan["runtime_migration_approved"] is False
    assert plan["runtime_migration_active"] is False
    assert plan["strategy_runtime_migration"] is False
    assert plan["runtime_use"] == plan_service.NOT_AUTHORIZED
    assert plan["strategy_use"] == plan_service.NOT_AUTHORIZED
    assert plan["paper_trading"] == plan_service.NOT_AUTHORIZED
    assert plan["broker_execution"] == plan_service.NOT_AUTHORIZED
    assert plan["automatic_stitching"] is False


def test_checklist_contains_all_required_check_ids_and_passes():
    checklist = _plan()["plan_checklist"]

    assert [item["check_id"] for item in checklist] == plan_service.REQUIRED_CHECK_IDS
    assert {item["status"] for item in checklist} == {plan_service.PASS}


def test_summary_counts_total_passed_failed_and_blockers():
    plan = _plan()
    summary = plan["plan_summary"]

    assert summary["total_checks"] == len(plan_service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(plan_service.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["experiment_execution_authorized"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_candidate_digest_is_deterministic():
    first = _plan()
    second = _plan()

    assert first["predictive_experiment_plan_candidate_digest"] == second[
        "predictive_experiment_plan_candidate_digest"
    ]
    assert first["predictive_experiment_plan_candidate_digest"] == (
        plan_service.predictive_experiment_plan_candidate_digest_v1(first)
    )


def test_validator_accepts_valid_plan():
    validation = plan_service.validate_predictive_experiment_plan_candidate_v1(_plan())

    assert validation["status"] == "PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_VALID"
    assert validation["ready_for_operator_review"] is True
    assert validation["experiment_execution_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("predictive_experiment_execution_authorized", True, "predictive_experiment_execution_authorized"),
        ("predictive_experiment_executed", True, "predictive_experiment_executed"),
        ("walk_forward_validation_performed", True, "walk_forward_validation_performed"),
        ("out_of_sample_evaluation_performed", True, "out_of_sample_evaluation_performed"),
        ("new_strategy_scoring_performed", True, "new_strategy_scoring_performed"),
        ("trade_recommendations_generated", True, "trade_recommendations_generated"),
        ("provider_requests_made", True, "provider_requests_made"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("predictive_usefulness_acceptance_ready", True, "predictive_usefulness_acceptance_ready"),
        ("profitability", "accepted", "profitability"),
        ("profitability_acceptance_ready", True, "profitability_acceptance_ready"),
        ("runtime_migration_recommended", True, "runtime_migration_recommended"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("automatic_stitching", True, "automatic_stitching"),
    ],
)
def test_validator_rejects_forbidden_plan_mutations(field: str, value: Any, match: str):
    plan = _mutated_plan(field, value)

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match=match):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_wrong_artifact_kind():
    plan = _mutated_plan("artifact_kind", "WRONG")

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="artifact_kind"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_non_aapl_ticker_universe():
    plan = _mutated_plan("ticker_universe", ["MSFT"])

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="ticker_universe"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_missing_swing_profile():
    plan = _plan()
    plan["dataset_profiles"] = [plan["dataset_profiles"][1]]

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="dataset_profiles"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_missing_position_swing_profile():
    plan = _plan()
    plan["dataset_profiles"] = [plan["dataset_profiles"][0]]

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="dataset_profiles"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_missing_label_definitions():
    plan = _mutated_plan("label_definitions", [])

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="label_definitions"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_missing_walk_forward_plan():
    plan = _mutated_plan("walk_forward_plan", {})

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="walk_forward_plan"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_missing_oos_plan():
    plan = _mutated_plan("out_of_sample_plan", {})

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="out_of_sample_plan"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_missing_leakage_controls():
    plan = _mutated_plan("leakage_controls", [])

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="leakage_controls"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_missing_execution_gates():
    plan = _mutated_plan("execution_gates", [])

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="execution_gates"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_missing_risk_controls():
    plan = _mutated_plan("risk_controls", [])

    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="risk_controls"):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_validator_rejects_missing_plan_digest():
    plan = _plan()
    plan.pop("predictive_experiment_plan_candidate_digest")

    with pytest.raises(
        plan_service.PredictiveExperimentPlanCandidateError,
        match="predictive_experiment_plan_candidate_digest",
    ):
        plan_service.validate_predictive_experiment_plan_candidate_v1(plan)


def test_markdown_writer_includes_required_sections():
    markdown = plan_service.build_predictive_experiment_plan_candidate_markdown_v1(_plan())

    for section in (
        "## Title",
        "## Purpose",
        "## Source Evidence",
        "## Experiment Scope",
        "## Planned Labels",
        "## Planned Feature Families",
        "## Walk-Forward Plan",
        "## Out-of-Sample Plan",
        "## Baselines and Metrics",
        "## Leakage Controls",
        "## Execution Gates",
        "## Risk Controls",
        "## Boundary Conditions",
        "## Checklist Summary",
        "## Remaining Tasks",
    ):
        assert section in markdown


def test_write_plan_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = plan_service.write_predictive_experiment_plan_candidate_v1(tmp_path)

    assert result["artifact_kind"] == (
        plan_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE
    )
    assert result["payload_sha256"]
    with pytest.raises(plan_service.PredictiveExperimentPlanCandidateError, match="already exists"):
        plan_service.write_predictive_experiment_plan_candidate_v1(tmp_path)


def test_predictive_experiment_plan_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE == (
        plan_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE
    )
    assert services.PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW == (
        plan_service.PREDICTIVE_EXPERIMENT_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_predictive_experiment_plan_candidate_v1 is (
        plan_service.build_predictive_experiment_plan_candidate_v1
    )
    assert services.validate_predictive_experiment_plan_candidate_v1 is (
        plan_service.validate_predictive_experiment_plan_candidate_v1
    )
    assert services.write_predictive_experiment_plan_candidate_v1 is (
        plan_service.write_predictive_experiment_plan_candidate_v1
    )
    assert services.build_predictive_experiment_plan_candidate_markdown_v1 is (
        plan_service.build_predictive_experiment_plan_candidate_markdown_v1
    )
