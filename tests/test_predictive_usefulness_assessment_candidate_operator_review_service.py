from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import predictive_usefulness_assessment_candidate_operator_review_service as review


def _package() -> dict[str, Any]:
    return review.build_predictive_usefulness_assessment_candidate_review_package_v1()


def _redigest(package: dict[str, Any]) -> dict[str, Any]:
    package["review_checklist"] = review._checklist(package)
    package["review_summary"] = review._summary(package["review_checklist"])
    package["predictive_usefulness_assessment_candidate_review_package_digest"] = (
        review.predictive_usefulness_assessment_candidate_review_package_digest_v1(package)
    )
    return package


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("assessment candidate must not be rebuilt by status binding")

    monkeypatch.setattr(
        review.candidate_service,
        "build_predictive_usefulness_assessment_candidate_v1",
        fail_if_called,
    )

    assert _package()["provider_requests_made_in_review"] is False


def test_artifact_kind_is_assessment_candidate_review_package():
    assert _package()["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE
    )


def test_review_status_is_ready():
    assert _package()["review_status"] == (
        review.PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_assessment_candidate_digest_matches_expected():
    assert _package()["reviewed_assessment_candidate_digest"] == (
        review.EXPECTED_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_DIGEST
    )


def test_predictive_experiment_results_review_digest_is_bound():
    assert _package()["predictive_experiment_results_review_package_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
    )


def test_predictive_experiment_execution_digest_is_bound():
    assert _package()["predictive_experiment_execution_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
    )


def test_predictive_experiment_execution_approval_digest_is_bound():
    assert _package()["predictive_experiment_execution_approval_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
    )


def test_predictive_experiment_plan_digest_is_bound():
    assert _package()["predictive_experiment_plan_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
    )


def test_swing_registry_approval_digest_is_bound():
    assert _package()["swing_registry_approval_digest"] == (
        review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_position_swing_registry_approval_digest_is_bound():
    assert _package()["position_swing_registry_approval_digest"] == (
        review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_output_count_is_thirteen():
    assert _package()["output_count"] == 13


def test_outputs_are_research_only_non_actionable():
    assert _package()["all_outputs_research_only_non_actionable"] is True


def test_metrics_label_is_research_only_not_performance_acceptance():
    assert _package()["metrics_label"] == review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE


def test_labels_generated_is_true():
    assert _package()["labels_generated"] is True


def test_feature_matrices_generated_is_true():
    assert _package()["feature_matrices_generated"] is True


def test_walk_forward_result_is_available_research_only():
    package = _package()

    assert package["walk_forward_result_generated"] is True
    assert package["assessment_classification"]["walk_forward_evidence_status"] == (
        review.candidate_service.AVAILABLE_RESEARCH_ONLY
    )


def test_oos_result_is_available_research_only():
    package = _package()

    assert package["out_of_sample_result_generated"] is True
    assert package["assessment_classification"]["out_of_sample_evidence_status"] == (
        review.candidate_service.AVAILABLE_RESEARCH_ONLY
    )


def test_baseline_result_count_is_eight():
    assert _package()["baseline_result_count"] == 8


def test_metric_result_count_is_eight():
    assert _package()["metric_result_count"] == 8


def test_failure_warning_counts_unavailable_are_acknowledged():
    package = _package()

    assert package["failure_count_status"] == review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS
    assert package["warning_count_status"] == review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS


def test_data_quality_evidence_status_is_pass():
    assert _package()["assessment_classification"]["data_quality_evidence_status"] == review.PASS


def test_assessment_limitations_are_defined():
    assert _package()["assessment_limitations"] == review.EXPECTED_ASSESSMENT_LIMITATIONS


def test_next_gates_are_defined():
    assert _package()["additional_evidence_next_gates"] == review.EXPECTED_NEXT_GATES


def test_predictive_usefulness_remains_not_accepted():
    assert _package()["predictive_usefulness"] == "not accepted"


def test_predictive_usefulness_acceptance_ready_remains_false():
    assert _package()["predictive_usefulness_acceptance_ready"] is False


def test_predictive_usefulness_acceptance_recommended_remains_false():
    assert _package()["predictive_usefulness_acceptance_recommended"] is False


def test_profitability_remains_not_accepted():
    assert _package()["profitability"] == "not accepted"


def test_profitability_acceptance_ready_remains_false():
    assert _package()["profitability_acceptance_ready"] is False


def test_profitability_acceptance_recommended_remains_false():
    assert _package()["profitability_acceptance_recommended"] is False


def test_runtime_migration_recommended_remains_false():
    assert _package()["runtime_migration_recommended"] is False


def test_runtime_migration_approved_remains_false():
    assert _package()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _package()["runtime_migration_active"] is False


def test_strategy_runtime_migration_remains_false():
    assert _package()["strategy_runtime_migration"] is False


def test_runtime_use_remains_not_authorized():
    assert _package()["runtime_use"] == review.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _package()["strategy_use"] == review.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _package()["paper_trading"] == review.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _package()["broker_execution"] == review.NOT_AUTHORIZED


def test_new_strategy_scoring_remains_false():
    assert _package()["new_strategy_scoring_performed"] is False


def test_trade_recommendations_generated_remains_false():
    assert _package()["trade_recommendations_generated"] is False


def test_checklist_contains_all_required_check_ids():
    package = _package()

    assert [item["check_id"] for item in package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_ready_review_package():
    assert {item["status"] for item in _package()["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_and_failed_correctly():
    summary = _package()["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_predictive_usefulness_acceptance_candidate"] is False


def test_review_package_digest_is_deterministic():
    assert _package()["predictive_usefulness_assessment_candidate_review_package_digest"] == (
        _package()["predictive_usefulness_assessment_candidate_review_package_digest"]
    )


def test_validator_accepts_valid_review_package():
    validation = review.validate_predictive_usefulness_assessment_candidate_review_package_v1(
        _package()
    )

    assert validation["status"] == (
        "PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert validation["ready_for_predictive_usefulness_acceptance_candidate"] is False


def test_validator_rejects_modified_assessment_candidate_digest():
    package = deepcopy(_package())
    package["reviewed_assessment_candidate_digest"] = "0" * 64
    _redigest(package)

    with pytest.raises(review.PredictiveUsefulnessAssessmentCandidateReviewPackageError):
        review.validate_predictive_usefulness_assessment_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("profitability_acceptance_recommended", True),
        ("runtime_migration_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("provider_requests_made_in_review", True),
        ("experiment_reexecution_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_forbidden_values(field: str, value: Any):
    package = _package()
    package[field] = value

    with pytest.raises(review.PredictiveUsefulnessAssessmentCandidateReviewPackageError):
        review.validate_predictive_usefulness_assessment_candidate_review_package_v1(package)


@pytest.mark.parametrize("field", ["assessment_limitations", "additional_evidence_next_gates"])
def test_validator_rejects_missing_required_lists(field: str):
    package = deepcopy(_package())
    package.pop(field)
    _redigest(package)

    with pytest.raises(review.PredictiveUsefulnessAssessmentCandidateReviewPackageError):
        review.validate_predictive_usefulness_assessment_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    "field",
    [
        "predictive_experiment_results_review_package_digest",
        "predictive_experiment_execution_digest",
        "predictive_usefulness_assessment_candidate_review_package_digest",
    ],
)
def test_validator_rejects_missing_required_digests(field: str):
    package = deepcopy(_package())
    package.pop(field)
    if field != "predictive_usefulness_assessment_candidate_review_package_digest":
        _redigest(package)

    with pytest.raises(review.PredictiveUsefulnessAssessmentCandidateReviewPackageError):
        review.validate_predictive_usefulness_assessment_candidate_review_package_v1(package)


def test_markdown_writer_includes_required_sections():
    markdown = review.build_predictive_usefulness_assessment_candidate_review_markdown_v1(
        _package()
    )

    for section in [
        "## Title",
        "## Reviewed Predictive Usefulness Assessment Candidate",
        "## Source Evidence",
        "## Assessment Classification",
        "## Evidence Summary",
        "## Limitations",
        "## Additional Evidence / Next Gates",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert section in markdown


def test_writer_rejects_existing_output_file(tmp_path: Path):
    output_path = tmp_path / "predictive_usefulness_assessment_candidate_review_package_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(review.PredictiveUsefulnessAssessmentCandidateReviewPackageError):
        review.write_predictive_usefulness_assessment_candidate_review_package_v1(tmp_path)
