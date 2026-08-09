from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow.services import (
    predictive_usefulness_review_candidate_operator_review_service as review_service,
)


def _review_package() -> dict[str, Any]:
    return review_service.build_predictive_usefulness_review_candidate_review_package_v1()


def _mutated_review_package(field: str, value: Any) -> dict[str, Any]:
    review_package = _review_package()
    review_package[field] = value
    return review_package


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        review_service.candidate_service.acquisition,
        "fetch_massive_custom_bars_v1",
        fail_provider_call,
    )

    review_package = _review_package()

    assert review_package["created_offline"] is True
    assert review_package["provider_requests_made_in_review"] is False


def test_artifact_kind_and_status_are_candidate_review_package():
    review_package = _review_package()

    assert review_package["artifact_kind"] == (
        review_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE
    )
    assert review_package["review_status"] == (
        review_service.PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_predictive_candidate_digest_is_bound():
    assert _review_package()["reviewed_candidate_digest"] == (
        review_service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
    )


def test_source_evidence_and_reviewed_result_facts_are_bound():
    review_package = _review_package()

    assert review_package["campaign_execution_results_review_package_digest"] == (
        review_service.candidate_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert review_package["campaign_execution_digest"] == (
        review_service.candidate_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST
    )
    assert review_package["execution_request_id"] == (
        review_service.candidate_service.EXPECTED_EXECUTION_REQUEST_ID
    )
    assert review_package["outputs_reviewed"] == 12
    assert review_package["all_outputs_research_only_non_actionable"] is True
    assert review_package["failure_count"] == 0
    assert review_package["warning_count"] == 0


def test_data_quality_and_module_readiness_are_true_without_predictive_evidence():
    review_package = _review_package()

    assert review_package["data_quality_readiness"] is True
    assert review_package["module_compatibility_readiness"] is True
    assert review_package["predictive_experiment_results_available"] is False
    assert review_package["walk_forward_results_available"] is False
    assert review_package["out_of_sample_results_available"] is False
    assert review_package["label_definition_available"] is False
    assert review_package["predictive_metrics_available"] is False


def test_additional_evidence_and_predictive_experiment_planning_state():
    review_package = _review_package()

    assert review_package["additional_evidence_required"] == (
        review_service.candidate_service.ADDITIONAL_EVIDENCE_REQUIRED
    )
    assert review_package["ready_for_predictive_experiment_planning"] is True


def test_predictive_profitability_and_runtime_boundaries_remain_closed():
    review_package = _review_package()

    assert review_package["predictive_usefulness"] == (
        review_service.candidate_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert review_package["predictive_usefulness_acceptance_ready"] is False
    assert review_package["profitability"] == (
        review_service.candidate_service.acquisition.PROFITABILITY_NOT_ACCEPTED
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


def test_execution_and_scoring_boundaries_remain_false():
    review_package = _review_package()

    assert review_package["provider_requests_made_in_review"] is False
    assert review_package["campaign_reexecution_performed"] is False
    assert review_package["new_strategy_scoring_performed"] is False
    assert review_package["walk_forward_validation_performed"] is False
    assert review_package["trade_recommendations_generated"] is False


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
    assert summary["ready_for_predictive_experiment_planning"] is True
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic():
    first = _review_package()
    second = _review_package()

    assert first["predictive_usefulness_review_candidate_review_package_digest"] == second[
        "predictive_usefulness_review_candidate_review_package_digest"
    ]
    assert first["predictive_usefulness_review_candidate_review_package_digest"] == (
        review_service.predictive_usefulness_review_candidate_review_package_digest_v1(first)
    )


def test_validator_accepts_valid_review_package():
    validation = review_service.validate_predictive_usefulness_review_candidate_review_package_v1(
        _review_package()
    )

    assert validation["status"] == (
        "PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert validation["ready_for_operator_assessment"] is True
    assert validation["ready_for_predictive_experiment_planning"] is True


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("reviewed_candidate_digest", "0" * 64, "reviewed_candidate_digest"),
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
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
        ("campaign_reexecution_performed", True, "campaign_reexecution_performed"),
        ("new_strategy_scoring_performed", True, "new_strategy_scoring_performed"),
        ("walk_forward_validation_performed", True, "walk_forward_validation_performed"),
        ("trade_recommendations_generated", True, "trade_recommendations_generated"),
    ],
)
def test_validator_rejects_forbidden_review_package_mutations(
    field: str,
    value: Any,
    match: str,
):
    review_package = _mutated_review_package(field, value)

    with pytest.raises(
        review_service.PredictiveUsefulnessReviewCandidateReviewPackageError,
        match=match,
    ):
        review_service.validate_predictive_usefulness_review_candidate_review_package_v1(
            review_package
        )


def test_validator_rejects_wrong_artifact_kind():
    review_package = _mutated_review_package("artifact_kind", "WRONG")

    with pytest.raises(
        review_service.PredictiveUsefulnessReviewCandidateReviewPackageError,
        match="artifact_kind",
    ):
        review_service.validate_predictive_usefulness_review_candidate_review_package_v1(
            review_package
        )


def test_validator_rejects_wrong_review_status():
    review_package = _mutated_review_package("review_status", "WRONG")

    with pytest.raises(
        review_service.PredictiveUsefulnessReviewCandidateReviewPackageError,
        match="review_status",
    ):
        review_service.validate_predictive_usefulness_review_candidate_review_package_v1(
            review_package
        )


def test_validator_rejects_missing_campaign_results_review_digest():
    review_package = _review_package()
    review_package["campaign_execution_results_review_package_digest"] = None

    with pytest.raises(
        review_service.PredictiveUsefulnessReviewCandidateReviewPackageError,
        match="campaign_execution_results_review_package_digest",
    ):
        review_service.validate_predictive_usefulness_review_candidate_review_package_v1(
            review_package
        )


def test_validator_rejects_missing_additional_evidence_required():
    review_package = _review_package()
    review_package["additional_evidence_required"] = []

    with pytest.raises(
        review_service.PredictiveUsefulnessReviewCandidateReviewPackageError,
        match="additional_evidence_required",
    ):
        review_service.validate_predictive_usefulness_review_candidate_review_package_v1(
            review_package
        )


def test_validator_rejects_missing_review_package_digest():
    review_package = _review_package()
    review_package.pop("predictive_usefulness_review_candidate_review_package_digest")

    with pytest.raises(
        review_service.PredictiveUsefulnessReviewCandidateReviewPackageError,
        match="predictive_usefulness_review_candidate_review_package_digest",
    ):
        review_service.validate_predictive_usefulness_review_candidate_review_package_v1(
            review_package
        )


def test_markdown_writer_includes_required_sections():
    markdown = review_service.build_predictive_usefulness_review_candidate_review_markdown_v1(
        _review_package()
    )

    for section in (
        "## Title",
        "## Reviewed Predictive Usefulness Candidate",
        "## Source Research Results",
        "## Evidence Classification",
        "## Additional Evidence Required",
        "## Boundary Conditions",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = review_service.write_predictive_usefulness_review_candidate_review_package_v1(
        tmp_path
    )

    assert result["artifact_kind"] == (
        review_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE
    )
    assert result["payload_sha256"]
    with pytest.raises(
        review_service.PredictiveUsefulnessReviewCandidateReviewPackageError,
        match="already exists",
    ):
        review_service.write_predictive_usefulness_review_candidate_review_package_v1(
            tmp_path
        )


def test_candidate_review_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE == (
        review_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_READY == (
        review_service.PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_predictive_usefulness_review_candidate_review_package_v1 is (
        review_service.build_predictive_usefulness_review_candidate_review_package_v1
    )
    assert services.validate_predictive_usefulness_review_candidate_review_package_v1 is (
        review_service.validate_predictive_usefulness_review_candidate_review_package_v1
    )
    assert services.write_predictive_usefulness_review_candidate_review_package_v1 is (
        review_service.write_predictive_usefulness_review_candidate_review_package_v1
    )
    assert services.build_predictive_usefulness_review_candidate_review_markdown_v1 is (
        review_service.build_predictive_usefulness_review_candidate_review_markdown_v1
    )


def test_object_binding_mode_is_recorded_when_candidate_is_supplied():
    candidate = review_service.candidate_service.build_predictive_usefulness_review_candidate_v1()

    review_package = review_service.build_predictive_usefulness_review_candidate_review_package_v1(
        candidate=candidate
    )

    assert review_package["candidate_binding_mode"] == (
        review_service.PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_OBJECT_BINDING
    )
