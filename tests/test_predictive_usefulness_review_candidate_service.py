from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import predictive_usefulness_review_candidate_service as candidate_service


def _candidate() -> dict[str, Any]:
    return candidate_service.build_predictive_usefulness_review_candidate_v1()


def _mutated_candidate(field: str, value: Any) -> dict[str, Any]:
    candidate = _candidate()
    candidate[field] = value
    return candidate


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        candidate_service.acquisition,
        "fetch_massive_custom_bars_v1",
        fail_provider_call,
    )

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_artifact_kind_and_status_are_predictive_usefulness_review_candidate():
    candidate = _candidate()

    assert candidate["artifact_kind"] == (
        candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE
    )
    assert candidate["candidate_status"] == (
        candidate_service.PREDICTIVE_USEFULNESS_REVIEW_READY_FOR_OPERATOR_REVIEW
    )


def test_source_evidence_and_reviewed_result_facts_are_bound():
    candidate = _candidate()

    assert candidate["campaign_execution_results_review_package_digest"] == (
        candidate_service.EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["campaign_execution_digest"] == (
        candidate_service.EXPECTED_CAMPAIGN_EXECUTION_DIGEST
    )
    assert candidate["execution_request_id"] == candidate_service.EXPECTED_EXECUTION_REQUEST_ID
    assert candidate["outputs_reviewed"] == 12
    assert candidate["all_outputs_research_only_non_actionable"] is True
    assert candidate["failure_count"] == 0
    assert candidate["warning_count"] == 0


def test_data_quality_and_module_readiness_are_true_without_predictive_evidence():
    candidate = _candidate()

    assert candidate["data_quality_readiness"] is True
    assert candidate["module_compatibility_readiness"] is True
    assert candidate["predictive_evidence_available"] is False
    assert candidate["predictive_experiment_results_available"] is False
    assert candidate["walk_forward_results_available"] is False
    assert candidate["out_of_sample_results_available"] is False
    assert candidate["label_definition_available"] is False
    assert candidate["predictive_metrics_available"] is False


def test_predictive_profitability_and_runtime_boundaries_remain_closed():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == (
        candidate_service.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert candidate["predictive_usefulness_acceptance_ready"] is False
    assert candidate["profitability"] == candidate_service.acquisition.PROFITABILITY_NOT_ACCEPTED
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


def test_execution_and_scoring_boundaries_remain_false():
    candidate = _candidate()

    assert candidate["provider_requests_made"] is False
    assert candidate["campaign_reexecution_performed"] is False
    assert candidate["new_strategy_scoring_performed"] is False
    assert candidate["walk_forward_validation_performed"] is False
    assert candidate["trade_recommendations_generated"] is False


def test_additional_evidence_required_list_is_populated():
    assert _candidate()["additional_evidence_required"] == (
        candidate_service.ADDITIONAL_EVIDENCE_REQUIRED
    )


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
    assert summary["ready_for_predictive_experiment_planning"] is True
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False


def test_candidate_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["predictive_usefulness_review_candidate_digest"] == second[
        "predictive_usefulness_review_candidate_digest"
    ]
    assert first["predictive_usefulness_review_candidate_digest"] == (
        candidate_service.predictive_usefulness_review_candidate_digest_v1(first)
    )


def test_validator_accepts_valid_candidate():
    validation = candidate_service.validate_predictive_usefulness_review_candidate_v1(
        _candidate()
    )

    assert validation["status"] == "PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_VALID"
    assert validation["ready_for_operator_review"] is True
    assert validation["ready_for_predictive_experiment_planning"] is True


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
        ("predictive_usefulness_acceptance_ready", True, "predictive_usefulness_acceptance_ready"),
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
        ("provider_requests_made", True, "provider_requests_made"),
        ("campaign_reexecution_performed", True, "campaign_reexecution_performed"),
        ("new_strategy_scoring_performed", True, "new_strategy_scoring_performed"),
        ("walk_forward_validation_performed", True, "walk_forward_validation_performed"),
        ("trade_recommendations_generated", True, "trade_recommendations_generated"),
    ],
)
def test_validator_rejects_forbidden_candidate_mutations(
    field: str,
    value: Any,
    match: str,
):
    candidate = _mutated_candidate(field, value)

    with pytest.raises(candidate_service.PredictiveUsefulnessReviewCandidateError, match=match):
        candidate_service.validate_predictive_usefulness_review_candidate_v1(candidate)


def test_validator_rejects_missing_campaign_results_review_digest():
    candidate = _candidate()
    candidate["campaign_execution_results_review_package_digest"] = None

    with pytest.raises(
        candidate_service.PredictiveUsefulnessReviewCandidateError,
        match="campaign_execution_results_review_package_digest",
    ):
        candidate_service.validate_predictive_usefulness_review_candidate_v1(candidate)


def test_validator_rejects_missing_additional_evidence_required():
    candidate = _candidate()
    candidate["additional_evidence_required"] = []

    with pytest.raises(
        candidate_service.PredictiveUsefulnessReviewCandidateError,
        match="additional_evidence_required",
    ):
        candidate_service.validate_predictive_usefulness_review_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("predictive_usefulness_review_candidate_digest")

    with pytest.raises(
        candidate_service.PredictiveUsefulnessReviewCandidateError,
        match="predictive_usefulness_review_candidate_digest",
    ):
        candidate_service.validate_predictive_usefulness_review_candidate_v1(candidate)


def test_validator_rejects_wrong_artifact_kind():
    candidate = _mutated_candidate("artifact_kind", "WRONG")

    with pytest.raises(
        candidate_service.PredictiveUsefulnessReviewCandidateError,
        match="artifact_kind",
    ):
        candidate_service.validate_predictive_usefulness_review_candidate_v1(candidate)


def test_markdown_writer_includes_required_sections():
    markdown = candidate_service.build_predictive_usefulness_review_candidate_markdown_v1(
        _candidate()
    )

    for section in (
        "## Title",
        "## Purpose",
        "## Source Research Results",
        "## Predictive Evidence Classification",
        "## Additional Evidence Required",
        "## Boundary Conditions",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = candidate_service.write_predictive_usefulness_review_candidate_v1(tmp_path)

    assert result["artifact_kind"] == (
        candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE
    )
    assert result["payload_sha256"]
    with pytest.raises(
        candidate_service.PredictiveUsefulnessReviewCandidateError,
        match="already exists",
    ):
        candidate_service.write_predictive_usefulness_review_candidate_v1(tmp_path)


def test_candidate_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE == (
        candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE
    )
    assert services.PREDICTIVE_USEFULNESS_REVIEW_READY_FOR_OPERATOR_REVIEW == (
        candidate_service.PREDICTIVE_USEFULNESS_REVIEW_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_predictive_usefulness_review_candidate_v1 is (
        candidate_service.build_predictive_usefulness_review_candidate_v1
    )
    assert services.validate_predictive_usefulness_review_candidate_v1 is (
        candidate_service.validate_predictive_usefulness_review_candidate_v1
    )
    assert services.write_predictive_usefulness_review_candidate_v1 is (
        candidate_service.write_predictive_usefulness_review_candidate_v1
    )
    assert services.build_predictive_usefulness_review_candidate_markdown_v1 is (
        candidate_service.build_predictive_usefulness_review_candidate_markdown_v1
    )


def test_nested_predictive_evidence_classification_matches_top_level_fields():
    candidate = _candidate()
    classification = candidate["predictive_evidence_classification"]

    for field in (
        "data_quality_readiness",
        "module_compatibility_readiness",
        "predictive_evidence_available",
        "predictive_experiment_results_available",
        "walk_forward_results_available",
        "out_of_sample_results_available",
        "label_definition_available",
        "predictive_metrics_available",
        "predictive_usefulness_acceptance_ready",
        "profitability_acceptance_ready",
    ):
        assert classification[field] == candidate[field]


def test_digest_changes_when_source_digest_changes():
    candidate = deepcopy(_candidate())
    original_digest = candidate["predictive_usefulness_review_candidate_digest"]
    candidate["campaign_execution_digest"] = "0" * 64

    assert candidate_service.predictive_usefulness_review_candidate_digest_v1(candidate) != (
        original_digest
    )
