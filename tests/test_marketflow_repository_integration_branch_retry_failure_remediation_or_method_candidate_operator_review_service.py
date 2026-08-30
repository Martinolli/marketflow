from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_service as service,
)


@pytest.fixture
def review():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1()


def test_review_builds_offline_and_deterministically(review):
    assert service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1() == review
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_READY),
        ("review_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("source_retry_failure_method_candidate_digest", service.SOURCE_METHOD_CANDIDATE_DIGEST),
        ("source_retry_failure_diagnosis_digest", service.source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST),
        ("source_retry_approval_digest", service.source.SOURCE_RETRY_APPROVAL_DIGEST),
        ("source_retry_operator_review_digest", service.source.SOURCE_RETRY_OPERATOR_REVIEW_DIGEST),
        ("source_retry_candidate_digest", service.source.SOURCE_RETRY_CANDIDATE_DIGEST),
        ("source_remediation_results_review_digest", service.source.SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_execution_digest", service.source.SOURCE_REMEDIATION_EXECUTION_DIGEST),
        ("source_staged_inventory_digest", service.source.SOURCE_STAGED_INVENTORY_DIGEST),
        ("retry_execution_commit", service.source.source.RETRY_EXECUTION_COMMIT),
        ("retry_pytest_passed_count", 24877), ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112), ("retry_pytest_skipped_count", 7),
        ("original_failed_run_passed_count", 24481), ("original_failed_run_failed_count", 1300),
        ("original_failed_run_error_count", 500), ("original_failed_run_skipped_count", 7),
        ("retry_delta_passed_count", 396), ("retry_delta_failed_count", -8),
        ("retry_delta_error_count", -388), ("retry_delta_skipped_count", 0),
        ("root_full_regression_passed_count", 29200), ("root_full_regression_skipped_count", 7),
        ("root_full_regression_is_retry_evidence", False),
        ("root_full_regression_does_not_override_detached_retry_failure", True),
        ("origin_main_commit", service.source.source.ORIGIN_MAIN_COMMIT),
        ("integration_branch_head_commit", service.source.source.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("detached_integration_worktree_head_commit", service.source.source.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("staged_evidence_manifest_digest", service.source.SOURCE_STAGED_INVENTORY_DIGEST),
        ("retry_failure_candidate_created", True),
        ("retry_failure_candidate_ready_for_operator_review", True),
        ("retry_failure_candidate_operator_review_created", True),
        ("retry_failure_candidate_operator_review_ready", True),
        ("method_packages_reviewed", True), ("future_method_requirements_reviewed", True),
        ("future_method_plan_reviewed", True), ("planned_outputs_reviewed", True),
        ("non_goals_reviewed", True), ("ready_for_retry_failure_method_approval", False),
        ("retry_failure_method_selected", False), ("retry_failure_method_approved", False),
        ("retry_failure_method_authorized", False), ("retry_failure_method_executed", False),
        ("new_remediation_candidate_created", False), ("new_retry_candidate_created", False),
        ("new_retry_approved", False), ("new_retry_executed", False),
        ("new_retry_results_review_created", False), ("main_merge_approval_created", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("integration_branch_pushed", False), ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False), ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False), ("provider_requests_made_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False), ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", service.NOT_ACCEPTED), ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED), ("broker_execution", service.NOT_AUTHORIZED),
        ("reviewed_candidate_philosophy", service.REVIEWED_CANDIDATE_PHILOSOPHY),
        ("reviewed_candidate_boundary", service.REVIEWED_CANDIDATE_BOUNDARY),
        ("reviewed_candidate_goal", service.REVIEWED_CANDIDATE_GOAL),
        ("review_disposition", service.REVIEW_DISPOSITION),
        ("recommended_retry_failure_method_package", service.source.RECOMMENDED_PACKAGE),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
        ("recommended_next_task_status", service.RECOMMENDED_NEXT_TASK_STATUS),
        ("recommended_action", service.RECOMMENDED_ACTION),
    ],
)
def test_required_review_fields(review, field, expected):
    assert review[field] == expected


def test_all_eight_method_packages_are_reviewed_without_selection(review):
    packages = review["reviewed_method_packages"]
    assert packages == service.REVIEWED_METHOD_PACKAGES
    assert len(packages) == 8
    assert len([row for row in packages if row["source_status"].startswith("BLOCKED_")]) == 3
    assert all(row["review_status"].startswith("REVIEWED_") for row in packages)
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_recommended_package_is_reviewed_not_selected(review):
    recommended = next(
        row for row in review["reviewed_method_packages"]
        if row["package_id"] == service.source.RECOMMENDED_PACKAGE
    )
    assert recommended["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert recommended["selected"] is False
    assert review["ready_for_retry_failure_method_approval"] is False


def test_future_requirements_are_reviewed_not_executed(review):
    rows = review["reviewed_future_method_requirements"]
    assert rows == service.REVIEWED_FUTURE_METHOD_REQUIREMENTS
    assert len(rows) == 18
    assert all(row["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_METHOD_EXECUTION" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_future_plan_is_reviewed_not_executed(review):
    rows = review["reviewed_future_method_plan"]
    assert rows == service.REVIEWED_FUTURE_METHOD_PLAN
    assert len(rows) == 10
    assert all(row["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_planned_outputs_are_reviewed_not_generated(review):
    rows = review["reviewed_planned_outputs"]
    assert rows == service.REVIEWED_PLANNED_OUTPUTS
    assert len(rows) == 11
    assert all(row["review_status"] == "REVIEWED_PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["generation_status"] == "NOT_GENERATED" for row in rows)


def test_non_goals_remain_active(review):
    assert review["reviewed_non_goals"] == service.REVIEWED_NON_GOALS
    assert len(review["reviewed_non_goals"]) == len(service.source.NON_GOALS)
    assert all(row["review_status"] == "REVIEWED_ACTIVE" for row in review["reviewed_non_goals"])


def test_recommendation_chain_gates_and_risk_controls(review):
    assert review["recommendation_reason"] == service.RECOMMENDATION_REASON
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert "review_does_not_select_method_package" in review["risk_controls"]
    assert "preserve_meta_limitation" in review["risk_controls"]


def test_checklist_and_summary_pass(review):
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in review["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in review["checklist"])
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 60
    assert review["summary"]["passed_checks"] == 60
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert review["summary"]["recommended_package_selected"] is False
    assert review["summary"]["ready_for_retry_failure_method_approval"] is False


def test_review_digest_is_deterministic(review):
    assert review["marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest"] == (
        service.marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest_v1(review)
    )


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_READY
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("review_scope", "WRONG"),
        ("source_retry_failure_method_candidate_digest", "0" * 64),
        ("source_retry_failure_diagnosis_digest", "0" * 64), ("retry_execution_commit", ""),
        ("retry_pytest_failed_count", None), ("root_full_regression_is_retry_evidence", True),
        ("retry_failure_candidate_operator_review_created", False),
        ("retry_failure_candidate_operator_review_ready", False),
        ("ready_for_retry_failure_method_approval", True), ("retry_failure_method_selected", True),
        ("retry_failure_method_approved", True), ("retry_failure_method_executed", True),
        ("new_remediation_candidate_created", True), ("new_retry_candidate_created", True),
        ("new_retry_executed", True), ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True), ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True), ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True), ("marketflow_outputs_committed", True),
        ("evidence_regenerated", True), ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_invalid_boundaries(review, field, bad_value):
    invalid = deepcopy(review)
    invalid[field] = bad_value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(invalid)


def test_validator_rejects_selected_recommended_package(review):
    invalid = deepcopy(review)
    invalid["reviewed_method_packages"][0]["selected"] = True
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(invalid)


@pytest.mark.parametrize(
    "field",
    ["reviewed_method_packages", "reviewed_future_method_requirements", "reviewed_future_method_plan", "risk_controls"],
)
def test_validator_rejects_missing_review_sections(review, field):
    invalid = deepcopy(review)
    invalid.pop(field)
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(invalid)


def test_invalid_source_candidate_fails_closed():
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError
    ):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(
            source_candidate={"source_retry_failure_method_candidate_digest": "0" * 64}
        )


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_markdown_v1(review)
    for title in (
        "MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate Operator Review v1",
        "Source Method Candidate", "Source Retry Failure Diagnosis", "Failure Context", "Retry Environment",
        "Review Scope", "Reviewed Candidate Philosophy", "Reviewed Method Packages",
        "Reviewed Future Method Requirements", "Reviewed Future Method Plan", "Reviewed Planned Outputs",
        "Reviewed Non-Goals", "Recommendation", "Next Chain", "Next Gates", "Risk Controls",
        "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert title in markdown
    assert "not retry evidence" in markdown


def test_writer_round_trips_without_overwrite(tmp_path, review):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == review
    assert receipt["marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest"] == (
        review["marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest"]
    )
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError
    ):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(tmp_path)
