from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow.services import (
    predictive_experiment_plan_candidate_operator_review_service as review_service,
)


EXPECTED_REVIEW_PACKAGE_DIGEST = (
    "e71197fb6838e2caa99d1cffa3c6bd8847d3170d6f842ea921e5345dac349180"
)


def _review_package() -> dict[str, Any]:
    return review_service.build_predictive_experiment_plan_candidate_review_package_v1()


def _mutated_review_package(field: str, value: Any) -> dict[str, Any]:
    review_package = _review_package()
    review_package[field] = value
    return review_package


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        review_service.plan_service.acquisition,
        "fetch_massive_custom_bars_v1",
        fail_provider_call,
    )

    review_package = _review_package()

    assert review_package["created_offline"] is True
    assert review_package["provider_requests_made_in_review"] is False


def test_artifact_kind_and_status_are_plan_candidate_review_package():
    review_package = _review_package()

    assert review_package["artifact_kind"] == (
        review_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert review_package["review_status"] == (
        review_service.PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_reviewed_plan_digest_is_bound():
    assert _review_package()["reviewed_plan_digest"] == (
        review_service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_DIGEST
    )


def test_source_evidence_digests_and_execution_request_are_bound():
    review_package = _review_package()

    assert review_package["predictive_usefulness_review_candidate_digest"] == (
        review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
    )
    assert review_package["predictive_usefulness_review_candidate_review_package_digest"] == (
        review_service.plan_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert review_package["campaign_execution_results_review_package_digest"] == (
        review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert review_package["campaign_execution_digest"] == (
        review_service.plan_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST
    )
    assert review_package["execution_request_id"] == (
        review_service.plan_service.EXPECTED_EXECUTION_REQUEST_ID
    )
    assert review_package["swing_registry_approval_digest"] == (
        review_service.plan_service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert review_package["position_swing_registry_approval_digest"] == (
        review_service.plan_service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_experiment_scope_is_research_only_aapl_only_and_date_bound():
    review_package = _review_package()

    assert review_package["experiment_scope"] == "RESEARCH_ONLY"
    assert review_package["ticker_universe"] == ["AAPL"]
    assert [item["profile"] for item in review_package["dataset_profiles"]] == [
        "SWING",
        "POSITION_SWING",
    ]
    assert review_package["date_range_start"] == "2022-01-01"
    assert review_package["date_range_end"] == "2025-12-31"


def test_plan_design_sections_are_preserved_for_review():
    review_package = _review_package()

    assert [item["label"] for item in review_package["label_definitions"]] == (
        review_service.plan_service.LABEL_DEFINITIONS
    )
    assert [item["feature_family"] for item in review_package["feature_family_plan"]] == (
        review_service.plan_service.FEATURE_FAMILIES
    )
    assert review_package["walk_forward_plan"]["method"] == "chronological_walk_forward"
    assert review_package["out_of_sample_plan"]["no_future_leakage"] is True
    assert review_package["baseline_comparisons"] == (
        review_service.plan_service.BASELINE_COMPARISONS
    )
    assert [item["metric"] for item in review_package["signal_quality_metrics"]] == (
        review_service.plan_service.SIGNAL_QUALITY_METRICS
    )
    assert review_package["stability_checks"] == review_service.plan_service.STABILITY_CHECKS
    assert review_package["false_positive_false_negative_analysis"]["status"] == "PLANNED_ONLY"
    assert review_package["leakage_controls"] == review_service.plan_service.LEAKAGE_CONTROLS


def test_planned_outputs_remain_not_generated_and_research_only():
    outputs = _review_package()["planned_outputs"]

    assert {item["generation_status"] for item in outputs} == {
        review_service.plan_service.PLANNED_NOT_GENERATED
    }
    assert {item["output_label"] for item in outputs} == {
        review_service.plan_service.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_execution_gates_and_risk_controls_are_preserved_for_review():
    review_package = _review_package()

    assert review_package["execution_gates"] == review_service.plan_service.EXECUTION_GATES
    assert review_package["risk_controls"] == review_service.plan_service.RISK_CONTROLS


def test_execution_acceptance_and_runtime_boundaries_remain_closed():
    review_package = _review_package()

    assert review_package["predictive_experiment_execution_authorized"] is False
    assert review_package["predictive_experiment_executed"] is False
    assert review_package["walk_forward_validation_performed"] is False
    assert review_package["out_of_sample_evaluation_performed"] is False
    assert review_package["new_strategy_scoring_performed"] is False
    assert review_package["trade_recommendations_generated"] is False
    assert review_package["predictive_usefulness"] == (
        review_service.plan_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert review_package["predictive_usefulness_acceptance_ready"] is False
    assert review_package["profitability"] == (
        review_service.plan_service.acquisition.PROFITABILITY_NOT_ACCEPTED
    )
    assert review_package["profitability_acceptance_ready"] is False
    assert review_package["runtime_migration_recommended"] is False
    assert review_package["runtime_migration_approved"] is False
    assert review_package["runtime_migration_active"] is False
    assert review_package["strategy_runtime_migration"] is False
    assert review_package["runtime_use"] == review_service.NOT_AUTHORIZED
    assert review_package["strategy_use"] == review_service.NOT_AUTHORIZED
    assert review_package["paper_trading"] == review_service.NOT_AUTHORIZED
    assert review_package["broker_execution"] == review_service.NOT_AUTHORIZED
    assert review_package["automatic_stitching"] is False


def test_checklist_contains_all_required_check_ids_and_passes():
    checklist = _review_package()["review_checklist"]

    assert [item["check_id"] for item in checklist] == review_service.REQUIRED_CHECK_IDS
    assert {item["status"] for item in checklist} == {review_service.PASS}


def test_summary_counts_total_passed_failed_and_blockers():
    review_package = _review_package()
    summary = review_package["review_summary"]

    assert summary["total_checks"] == len(review_service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review_service.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_predictive_experiment_execution_candidate"] is True
    assert summary["predictive_experiment_execution_authorized"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic():
    first = _review_package()
    second = _review_package()

    assert first["predictive_experiment_plan_candidate_review_package_digest"] == (
        second["predictive_experiment_plan_candidate_review_package_digest"]
    )
    assert first["predictive_experiment_plan_candidate_review_package_digest"] == (
        EXPECTED_REVIEW_PACKAGE_DIGEST
    )
    assert first["predictive_experiment_plan_candidate_review_package_digest"] == (
        review_service.predictive_experiment_plan_candidate_review_package_digest_v1(first)
    )


def test_validator_accepts_valid_review_package():
    validation = review_service.validate_predictive_experiment_plan_candidate_review_package_v1(
        _review_package()
    )

    assert validation["status"] == "PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert validation["ready_for_operator_assessment"] is True
    assert validation["ready_for_predictive_experiment_execution_candidate"] is True
    assert validation["predictive_experiment_execution_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("reviewed_plan_digest", "0" * 64, "reviewed_plan_digest"),
        ("predictive_experiment_execution_authorized", True, "predictive_experiment_execution_authorized"),
        ("predictive_experiment_executed", True, "predictive_experiment_executed"),
        ("walk_forward_validation_performed", True, "walk_forward_validation_performed"),
        ("out_of_sample_evaluation_performed", True, "out_of_sample_evaluation_performed"),
        ("new_strategy_scoring_performed", True, "new_strategy_scoring_performed"),
        ("trade_recommendations_generated", True, "trade_recommendations_generated"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
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
def test_validator_rejects_forbidden_review_package_mutations(
    field: str,
    value: Any,
    match: str,
):
    review_package = _mutated_review_package(field, value)

    with pytest.raises(
        review_service.PredictiveExperimentPlanCandidateReviewPackageError,
        match=match,
    ):
        review_service.validate_predictive_experiment_plan_candidate_review_package_v1(
            review_package
        )


def test_validator_rejects_wrong_artifact_kind():
    review_package = _mutated_review_package("artifact_kind", "WRONG")

    with pytest.raises(
        review_service.PredictiveExperimentPlanCandidateReviewPackageError,
        match="artifact_kind",
    ):
        review_service.validate_predictive_experiment_plan_candidate_review_package_v1(
            review_package
        )


def test_validator_rejects_wrong_review_status():
    review_package = _mutated_review_package("review_status", "WRONG")

    with pytest.raises(
        review_service.PredictiveExperimentPlanCandidateReviewPackageError,
        match="review_status",
    ):
        review_service.validate_predictive_experiment_plan_candidate_review_package_v1(
            review_package
        )


def test_validator_rejects_missing_review_package_digest():
    review_package = _review_package()
    review_package.pop("predictive_experiment_plan_candidate_review_package_digest")

    with pytest.raises(
        review_service.PredictiveExperimentPlanCandidateReviewPackageError,
        match="predictive_experiment_plan_candidate_review_package_digest",
    ):
        review_service.validate_predictive_experiment_plan_candidate_review_package_v1(
            review_package
        )


def test_markdown_writer_includes_required_sections():
    markdown = review_service.build_predictive_experiment_plan_candidate_review_markdown_v1(
        _review_package()
    )

    for section in (
        "## Title",
        "## Reviewed Predictive Experiment Plan",
        "## Source Evidence",
        "## Experiment Scope",
        "## Labels and Features",
        "## Walk-Forward / OOS Design",
        "## Baselines and Metrics",
        "## Leakage Controls",
        "## Execution Gates",
        "## Risk Controls",
        "## Boundary Conditions",
        "## Checklist Summary",
        "## Remaining Tasks",
    ):
        assert section in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = review_service.write_predictive_experiment_plan_candidate_review_package_v1(
        tmp_path
    )

    assert result["artifact_kind"] == (
        review_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert result["payload_sha256"]
    with pytest.raises(
        review_service.PredictiveExperimentPlanCandidateReviewPackageError,
        match="already exists",
    ):
        review_service.write_predictive_experiment_plan_candidate_review_package_v1(
            tmp_path
        )


def test_plan_review_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE == (
        review_service.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY == (
        review_service.PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_predictive_experiment_plan_candidate_review_package_v1 is (
        review_service.build_predictive_experiment_plan_candidate_review_package_v1
    )
    assert services.validate_predictive_experiment_plan_candidate_review_package_v1 is (
        review_service.validate_predictive_experiment_plan_candidate_review_package_v1
    )
    assert services.write_predictive_experiment_plan_candidate_review_package_v1 is (
        review_service.write_predictive_experiment_plan_candidate_review_package_v1
    )
    assert services.build_predictive_experiment_plan_candidate_review_markdown_v1 is (
        review_service.build_predictive_experiment_plan_candidate_review_markdown_v1
    )


def test_object_binding_mode_is_recorded_when_plan_is_supplied():
    plan = review_service.plan_service.build_predictive_experiment_plan_candidate_v1()

    review_package = review_service.build_predictive_experiment_plan_candidate_review_package_v1(
        plan=plan
    )

    assert review_package["plan_binding_mode"] == (
        review_service.PREDICTIVE_EXPERIMENT_PLAN_CANDIDATE_OBJECT_BINDING
    )
