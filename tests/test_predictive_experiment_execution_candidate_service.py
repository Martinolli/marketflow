from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow.services import predictive_experiment_execution_candidate_service as candidate_service


EXPECTED_CANDIDATE_DIGEST = (
    "36d724706fe3ea43592eb4589ffae3370f15dd4393d3226fbf9c9155f02561da"
)


def _candidate() -> dict[str, Any]:
    return candidate_service.build_predictive_experiment_execution_candidate_v1()


def _mutated_candidate(field: str, value: Any) -> dict[str, Any]:
    candidate = _candidate()
    candidate[field] = value
    return candidate


def test_execution_candidate_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        candidate_service.plan_review_service.plan_service.acquisition,
        "fetch_massive_custom_bars_v1",
        fail_provider_call,
    )

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_artifact_kind_and_status_are_execution_candidate():
    candidate = _candidate()

    assert candidate["artifact_kind"] == (
        candidate_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE
    )
    assert candidate["candidate_status"] == (
        candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW
    )


def test_predictive_experiment_plan_and_review_digests_are_bound():
    candidate = _candidate()

    assert candidate["predictive_experiment_plan_digest"] == (
        candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
    )
    assert candidate["predictive_experiment_plan_review_package_digest"] == (
        candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
    )


def test_predictive_usefulness_and_campaign_evidence_digests_are_bound():
    candidate = _candidate()

    assert candidate["predictive_usefulness_review_candidate_digest"] == (
        candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
    )
    assert candidate["predictive_usefulness_review_candidate_review_package_digest"] == (
        candidate_service.plan_review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["campaign_execution_results_review_package_digest"] == (
        candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["campaign_execution_digest"] == (
        candidate_service.plan_review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST
    )


def test_dataset_registry_approval_and_row_digests_are_bound():
    candidate = _candidate()

    assert candidate["swing_registry_approval_digest"] == (
        candidate_service.plan_review_service.plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert candidate["position_swing_registry_approval_digest"] == (
        candidate_service.plan_review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert candidate["swing_dataset_rows_digest"] == (
        candidate_service.EXPECTED_SWING_DATASET_ROWS_DIGEST
    )
    assert candidate["position_swing_dataset_rows_digest"] == (
        candidate_service.EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST
    )


def test_execution_request_id_is_deterministic():
    assert _candidate()["predictive_experiment_execution_request_id"] == (
        "AAPL_PREDICTIVE_EXPERIMENT_EXECUTION_2022_2025_V1"
    )


def test_experiment_scope_is_research_only_aapl_only_and_date_bound():
    candidate = _candidate()

    assert candidate["research_only"] is True
    assert candidate["experiment_scope"] == "RESEARCH_ONLY"
    assert candidate["ticker_universe"] == ["AAPL"]
    assert [item["profile"] for item in candidate["dataset_profiles"]] == [
        "SWING",
        "POSITION_SWING",
    ]
    assert candidate["date_range_start"] == "2022-01-01"
    assert candidate["date_range_end"] == "2025-12-31"
    assert candidate["runtime_use"] == candidate_service.NOT_AUTHORIZED
    assert candidate["strategy_use"] == candidate_service.NOT_AUTHORIZED


def test_execution_modes_are_non_runtime_non_strategy_and_broker_disabled():
    candidate = _candidate()

    assert candidate["execution_mode"] == "OFFLINE_RESEARCH_EXPERIMENT"
    assert candidate["runtime_mode"] == "NOT_RUNTIME"
    assert candidate["strategy_mode"] == "NOT_STRATEGY_INPUT"
    assert candidate["broker_mode"] == "DISABLED"
    assert candidate["paper_trading_mode"] == "DISABLED"


def test_planned_input_files_are_declared_without_generation():
    candidate = _candidate()

    assert candidate["planned_output_root"] == (
        ".marketflow/predictive_experiments/AAPL/2022_2025/"
    )
    assert [item["path"] for item in candidate["planned_input_files"]] == [
        (
            ".marketflow/canonical_candidates/AAPL/SWING/"
            "AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv"
        ),
        (
            ".marketflow/canonical_candidates/AAPL/POSITION_SWING/"
            "AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv"
        ),
    ]


def test_labels_features_walk_forward_oos_baselines_and_leakage_are_defined():
    candidate = _candidate()

    assert [item["label"] for item in candidate["label_definitions"]] == (
        candidate_service.LABEL_DEFINITIONS
    )
    assert [item["feature_family"] for item in candidate["feature_family_plan"]] == (
        candidate_service.FEATURE_FAMILIES
    )
    assert candidate["walk_forward_plan"]["method"] == "chronological_walk_forward"
    assert candidate["walk_forward_plan"]["training_window"] == "planned"
    assert candidate["walk_forward_plan"]["validation_window"] == "planned"
    assert candidate["walk_forward_plan"]["test_window"] == "planned"
    assert candidate["walk_forward_plan"]["no_shuffle"] is True
    assert candidate["walk_forward_plan"]["time_order_preserved"] is True
    assert candidate["out_of_sample_plan"]["final_holdout_period"] == "planned"
    assert candidate["out_of_sample_plan"]["no_future_leakage"] is True
    assert candidate["baseline_comparisons"] == candidate_service.BASELINE_COMPARISONS
    assert candidate["leakage_controls"] == candidate_service.LEAKAGE_CONTROLS


def test_metrics_are_defined_as_research_only_not_performance_acceptance():
    metrics = _candidate()["signal_quality_metrics"]

    assert [item["metric"] for item in metrics] == candidate_service.SIGNAL_QUALITY_METRICS
    assert {item["acceptance_label"] for item in metrics} == {
        candidate_service.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
    }


def test_planned_outputs_are_not_generated_and_research_only_non_actionable():
    outputs = _candidate()["planned_outputs"]

    assert [item["name"] for item in outputs] == candidate_service.PLANNED_OUTPUT_NAMES
    assert {item["generation_status"] for item in outputs} == {
        candidate_service.PLANNED_NOT_GENERATED
    }
    assert {item["output_label"] for item in outputs} == {
        candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_execution_gates_and_risk_controls_are_defined():
    candidate = _candidate()

    assert candidate["execution_gates"] == candidate_service.EXECUTION_GATES
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS


def test_execution_acceptance_and_runtime_boundaries_remain_closed():
    candidate = _candidate()

    assert candidate["predictive_experiment_execution_authorized"] is False
    assert candidate["predictive_experiment_executed"] is False
    assert candidate["walk_forward_validation_performed"] is False
    assert candidate["out_of_sample_evaluation_performed"] is False
    assert candidate["label_generation_performed"] is False
    assert candidate["feature_matrix_generation_performed"] is False
    assert candidate["new_strategy_scoring_performed"] is False
    assert candidate["trade_recommendations_generated"] is False
    assert candidate["predictive_usefulness"] == (
        candidate_service.plan_review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert candidate["predictive_usefulness_acceptance_ready"] is False
    assert candidate["profitability"] == (
        candidate_service.plan_review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED
    )
    assert candidate["profitability_acceptance_ready"] is False
    assert candidate["runtime_migration_recommended"] is False
    assert candidate["runtime_migration_approved"] is False
    assert candidate["runtime_migration_active"] is False
    assert candidate["strategy_runtime_migration"] is False
    assert candidate["runtime_use"] == candidate_service.NOT_AUTHORIZED
    assert candidate["strategy_use"] == candidate_service.NOT_AUTHORIZED
    assert candidate["paper_trading"] == candidate_service.NOT_AUTHORIZED
    assert candidate["broker_execution"] == candidate_service.NOT_AUTHORIZED
    assert candidate["automatic_stitching"] is False


def test_checklist_contains_all_required_check_ids_and_passes():
    checklist = _candidate()["candidate_checklist"]

    assert [item["check_id"] for item in checklist] == candidate_service.REQUIRED_CHECK_IDS
    assert {item["status"] for item in checklist} == {candidate_service.PASS}


def test_summary_counts_total_passed_failed_and_blockers():
    candidate = _candidate()
    summary = candidate["candidate_summary"]

    assert summary["total_checks"] == len(candidate_service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(candidate_service.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["experiment_execution_authorized"] is False
    assert summary["experiment_execution_performed"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_candidate_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["predictive_experiment_execution_candidate_digest"] == second[
        "predictive_experiment_execution_candidate_digest"
    ]
    assert first["predictive_experiment_execution_candidate_digest"] == (
        EXPECTED_CANDIDATE_DIGEST
    )
    assert first["predictive_experiment_execution_candidate_digest"] == (
        candidate_service.predictive_experiment_execution_candidate_digest_v1(first)
    )


def test_validator_accepts_valid_candidate():
    validation = candidate_service.validate_predictive_experiment_execution_candidate_v1(
        _candidate()
    )

    assert validation["status"] == "PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE_VALID"
    assert validation["ready_for_operator_review"] is True
    assert validation["experiment_execution_authorized"] is False
    assert validation["experiment_execution_performed"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("predictive_experiment_execution_authorized", True, "predictive_experiment_execution_authorized"),
        ("predictive_experiment_executed", True, "predictive_experiment_executed"),
        ("walk_forward_validation_performed", True, "walk_forward_validation_performed"),
        ("out_of_sample_evaluation_performed", True, "out_of_sample_evaluation_performed"),
        ("label_generation_performed", True, "label_generation_performed"),
        ("feature_matrix_generation_performed", True, "feature_matrix_generation_performed"),
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
def test_validator_rejects_forbidden_candidate_mutations(
    field: str,
    value: Any,
    match: str,
):
    candidate = _mutated_candidate(field, value)

    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match=match,
    ):
        candidate_service.validate_predictive_experiment_execution_candidate_v1(candidate)


def test_validator_rejects_wrong_artifact_kind():
    candidate = _mutated_candidate("artifact_kind", "WRONG")

    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match="artifact_kind",
    ):
        candidate_service.validate_predictive_experiment_execution_candidate_v1(candidate)


def test_validator_rejects_non_aapl_ticker_universe():
    candidate = _mutated_candidate("ticker_universe", ["AAPL", "MSFT"])

    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match="ticker_universe",
    ):
        candidate_service.validate_predictive_experiment_execution_candidate_v1(candidate)


def test_validator_rejects_missing_swing_profile():
    candidate = _candidate()
    candidate["dataset_profiles"] = [
        item for item in candidate["dataset_profiles"] if item["profile"] != "SWING"
    ]

    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match="dataset_profiles",
    ):
        candidate_service.validate_predictive_experiment_execution_candidate_v1(candidate)


def test_validator_rejects_missing_position_swing_profile():
    candidate = _candidate()
    candidate["dataset_profiles"] = [
        item
        for item in candidate["dataset_profiles"]
        if item["profile"] != "POSITION_SWING"
    ]

    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match="dataset_profiles",
    ):
        candidate_service.validate_predictive_experiment_execution_candidate_v1(candidate)


def test_validator_rejects_missing_predictive_experiment_plan_review_digest():
    candidate = _mutated_candidate("predictive_experiment_plan_review_package_digest", None)

    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match="predictive_experiment_plan_review_package_digest",
    ):
        candidate_service.validate_predictive_experiment_execution_candidate_v1(candidate)


def test_validator_rejects_missing_execution_gates():
    candidate = _mutated_candidate("execution_gates", [])

    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match="execution_gates",
    ):
        candidate_service.validate_predictive_experiment_execution_candidate_v1(candidate)


def test_validator_rejects_missing_risk_controls():
    candidate = _mutated_candidate("risk_controls", [])

    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match="risk_controls",
    ):
        candidate_service.validate_predictive_experiment_execution_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("predictive_experiment_execution_candidate_digest")

    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match="predictive_experiment_execution_candidate_digest",
    ):
        candidate_service.validate_predictive_experiment_execution_candidate_v1(candidate)


def test_markdown_writer_includes_required_sections():
    markdown = candidate_service.build_predictive_experiment_execution_candidate_markdown_v1(
        _candidate()
    )

    for section in (
        "## Title",
        "## Purpose",
        "## Execution Candidate Scope",
        "## Source Evidence",
        "## Planned Inputs",
        "## Labels and Features",
        "## Walk-Forward / OOS Design",
        "## Planned Outputs",
        "## Execution Gates",
        "## Risk Controls",
        "## Boundary Conditions",
        "## Checklist Summary",
        "## Non-Goals",
    ):
        assert section in markdown


def test_write_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = candidate_service.write_predictive_experiment_execution_candidate_v1(tmp_path)

    assert result["artifact_kind"] == (
        candidate_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE
    )
    assert result["payload_sha256"]
    with pytest.raises(
        candidate_service.PredictiveExperimentExecutionCandidateError,
        match="already exists",
    ):
        candidate_service.write_predictive_experiment_execution_candidate_v1(tmp_path)


def test_execution_candidate_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE == (
        candidate_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE
    )
    assert services.PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW == (
        candidate_service.PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_predictive_experiment_execution_candidate_v1 is (
        candidate_service.build_predictive_experiment_execution_candidate_v1
    )
    assert services.validate_predictive_experiment_execution_candidate_v1 is (
        candidate_service.validate_predictive_experiment_execution_candidate_v1
    )
    assert services.write_predictive_experiment_execution_candidate_v1 is (
        candidate_service.write_predictive_experiment_execution_candidate_v1
    )
    assert services.build_predictive_experiment_execution_candidate_markdown_v1 is (
        candidate_service.build_predictive_experiment_execution_candidate_markdown_v1
    )
