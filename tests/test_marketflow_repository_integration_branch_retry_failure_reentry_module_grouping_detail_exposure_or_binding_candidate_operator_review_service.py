from __future__ import annotations

import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_service
    as service,
)


def build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1()


def validate(review: dict) -> dict:
    return service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(review)


def test_review_builds_offline_with_correct_identity() -> None:
    review = build()
    assert review["created_offline"] is True
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["review_status"] == service.REVIEW_STATUS
    assert review["review_scope"] == service.REVIEW_SCOPE


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_detail_exposure_or_binding_candidate_digest", service.SOURCE_CANDIDATE_DIGEST),
        ("source_reentry_failure_diagnosis_digest", service.source.SOURCE_DIAGNOSIS_DIGEST),
        ("primary_failure_class", service.source.PRIMARY_FAILURE_CLASS),
        ("source_reentry_execution_blocked_digest", service.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_reentry_execution_blocked_manifest_digest", service.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("source_reentry_execution_blocked_reason", service.source.source.SOURCE_BLOCKED_REASON),
        ("source_after_v2_planning_reentry_digest", service.source.source.SOURCE_REENTRY_DIGEST),
        ("source_module_grouping_source_recovery_results_review_digest", service.source.source.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", service.source.source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_execution_digest", service.source.source.SOURCE_RECOVERY_EXECUTION_DIGEST),
        ("source_module_grouping_source_recovery_detail_digest", service.source.source.SOURCE_RECOVERY_DETAIL_DIGEST),
        ("source_module_grouping_source_recovery_digest_manifest_digest", service.source.source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST),
        ("source_blocked_after_v2_execution_digest", service.source.source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST),
        ("source_after_v2_approval_digest", service.source.source.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_results_review_v2_digest", service.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.source.source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.source.source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", service.source.source.RETRY_EXECUTION_COMMIT),
    ],
)
def test_source_chain_is_bound(field: str, expected: str) -> None:
    assert build()[field] == expected


def test_retry_and_module_summaries_are_preserved_without_detail_exposure() -> None:
    review = build()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["recovered_module_grouping_source_summary"]["module_summary_module_count"] == 29
    assert review["top_module_summary"] == service.source.source.TOP_FIVE
    assert review["top_5_count_sum"] == 612
    assert review["top_10_count_sum"] == 1069
    assert len(review["top_module_summary"]) == 5
    assert "module_rows" not in review


def test_available_missing_detail_and_source_gap_are_preserved() -> None:
    review = build()
    assert review["available_committed_reentry_detail"] == service.source.source.AVAILABLE_COMMITTED_DETAIL
    assert review["missing_committed_reentry_detail"] == service.source.source.MISSING_COMMITTED_DETAIL
    assert review["actual_live_reentry_source_lacks_complete_29_rows"] is True
    assert review["reentry_success_path_tested_with_complete_29_row_snapshot"] is True


def test_all_packages_requirements_plan_outputs_and_non_goals_are_reviewed() -> None:
    review = build()
    assert len(review["reviewed_packages"]) == 11
    assert sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in review["reviewed_packages"]) == 5
    assert len(review["reviewed_future_detail_exposure_or_binding_requirements"]) == len(service.source.FUTURE_REQUIREMENTS)
    assert len(review["reviewed_future_detail_exposure_or_binding_plan"]) == 10
    assert len(review["reviewed_planned_outputs"]) == 12
    assert len(review["reviewed_non_goals"]) == len(service.source.NON_GOALS)


@pytest.mark.parametrize("field", service.FALSE_BOUNDARIES)
def test_all_review_execution_boundaries_remain_false(field: str) -> None:
    assert build()[field] is False


@pytest.mark.parametrize("field", ["detail_exposure_or_binding_packages_reviewed", "future_detail_exposure_or_binding_requirements_reviewed", "future_detail_exposure_or_binding_plan_reviewed", "planned_outputs_reviewed", "non_goals_reviewed"])
def test_review_completion_flags_are_true(field: str) -> None:
    assert build()[field] is True


def test_recommendation_is_reviewed_but_not_selected_or_approval_ready() -> None:
    review = build()
    assert review["recommended_detail_exposure_or_binding_package"] == service.source.RECOMMENDED_PACKAGE
    assert review["recommendation"]["selected"] is False
    assert review["recommendation"]["approved"] is False
    assert review["ready_for_detail_exposure_or_binding_approval"] is False
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK


def test_checklist_digest_and_validation_are_deterministic() -> None:
    first = build()
    second = build()
    assert first == second
    assert first["summary"]["total_checks"] == 95
    assert first["summary"]["passed_checks"] == 95
    assert first["summary"]["failed_checks"] == 0
    result = validate(first)
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("review_scope", "WRONG"),
        ("source_detail_exposure_or_binding_candidate_digest", "0" * 64),
        ("source_reentry_failure_diagnosis_digest", "0" * 64), ("primary_failure_class", "WRONG"),
        ("source_reentry_execution_blocked_digest", "0" * 64),
        ("source_reentry_execution_blocked_manifest_digest", "0" * 64),
        ("source_reentry_execution_blocked_reason", ""),
        ("source_after_v2_planning_reentry_digest", "0" * 64),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_after_v2_approval_digest", "0" * 64), ("source_results_review_v2_digest", "0" * 64),
        ("source_execution_v2_digest", "0" * 64), ("source_module_grouping_digest", "0" * 64),
        ("top_5_count_sum", 611), ("top_10_count_sum", 1068),
        ("actual_live_reentry_source_lacks_complete_29_rows", False),
        ("ready_for_detail_exposure_or_binding_approval", True),
        *[(field, True) for field in service.FALSE_BOUNDARIES if field != "ready_for_detail_exposure_or_binding_approval"],
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_tampered_scalar_fields(field: str, replacement: object) -> None:
    review = build()
    review[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError):
        validate(review)


@pytest.mark.parametrize("field", ["retry_failure_context", "recovered_module_grouping_source_summary", "top_module_summary", "available_committed_reentry_detail", "missing_committed_reentry_detail", "reviewed_packages", "reviewed_future_detail_exposure_or_binding_requirements", "reviewed_future_detail_exposure_or_binding_plan", "reviewed_planned_outputs", "reviewed_non_goals", "next_chain", "risk_controls"])
def test_validator_rejects_missing_review_structures(field: str) -> None:
    review = build()
    review.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError):
        validate(review)


def test_builder_accepts_exact_source_candidate_and_rejects_changed_source() -> None:
    candidate = service._committed_source_candidate()
    assert service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(source_candidate=candidate)["detail_exposure_or_binding_packages_reviewed"] is True
    candidate["primary_failure_class"] = "WRONG"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(source_candidate=candidate)


def test_writer_round_trips_in_temporary_directory(tmp_path) -> None:
    result = service.write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == result["artifact"]


@pytest.mark.parametrize("heading", ["Source Detail Exposure or Binding Candidate", "Source Reentry Failure Diagnosis", "Source Blocked Reentry Execution", "Source Recovery Results Review", "Retry Failure Context", "Recovered Module Grouping Source Summary", "Available and Missing Committed Detail", "Review Scope", "Reviewed Candidate Philosophy", "Reviewed Detail Exposure or Binding Packages", "Reviewed Future Detail Exposure or Binding Requirements", "Reviewed Future Detail Exposure or Binding Plan", "Reviewed Planned Outputs", "Reviewed Non-Goals", "Recommendation", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails"])
def test_markdown_includes_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_markdown_v1(build())
    assert f"## {heading}" in markdown
