from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_service as service,
)


@pytest.fixture
def candidate():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1()


def test_candidate_builds_offline_and_deterministically(candidate):
    assert service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1() == candidate
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True
    assert candidate["operator_review_required"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1),
        ("candidate_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("candidate_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("source_retry_failure_diagnosis_digest", service.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST),
        ("source_retry_approval_digest", service.SOURCE_RETRY_APPROVAL_DIGEST),
        ("source_retry_operator_review_digest", service.SOURCE_RETRY_OPERATOR_REVIEW_DIGEST),
        ("source_retry_candidate_digest", service.SOURCE_RETRY_CANDIDATE_DIGEST),
        ("source_remediation_results_review_digest", service.SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_execution_digest", service.SOURCE_REMEDIATION_EXECUTION_DIGEST),
        ("source_staged_inventory_digest", service.SOURCE_STAGED_INVENTORY_DIGEST),
        ("retry_execution_commit", service.source.RETRY_EXECUTION_COMMIT),
        ("retry_pytest_passed_count", 24877), ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112), ("retry_pytest_skipped_count", 7),
        ("original_failed_run_passed_count", 24481), ("original_failed_run_failed_count", 1300),
        ("original_failed_run_error_count", 500), ("original_failed_run_skipped_count", 7),
        ("retry_delta_passed_count", 396), ("retry_delta_failed_count", -8),
        ("retry_delta_error_count", -388), ("retry_delta_skipped_count", 0),
        ("root_full_regression_passed_count", 29200), ("root_full_regression_skipped_count", 7),
        ("root_full_regression_is_retry_evidence", False),
        ("root_full_regression_does_not_override_detached_retry_failure", True),
        ("origin_main_commit", service.source.ORIGIN_MAIN_COMMIT),
        ("integration_branch_head_commit", service.source.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("detached_integration_worktree_head_commit", service.source.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("staged_evidence_manifest_digest", service.SOURCE_STAGED_INVENTORY_DIGEST),
        ("retry_failure_candidate_created", True),
        ("retry_failure_candidate_ready_for_operator_review", True),
        ("ready_for_retry_failure_candidate_operator_review", True),
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
        ("evidence_regenerated", False), ("provider_requests_made_in_candidate", False),
        ("market_data_acquisition_performed_in_candidate", False),
        ("dataset_generation_performed_in_candidate", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False), ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", service.NOT_ACCEPTED), ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED), ("broker_execution", service.NOT_AUTHORIZED),
        ("recommended_retry_failure_method_package", service.RECOMMENDED_PACKAGE),
        ("recommendation_status", service.RECOMMENDATION_STATUS),
        ("future_method_plan_status", service.FUTURE_METHOD_PLAN_STATUS),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
    ],
)
def test_required_candidate_fields(candidate, field, expected):
    assert candidate[field] == expected


def test_candidate_philosophy_boundary_and_goal(candidate):
    assert candidate["candidate_philosophy"] == service.CANDIDATE_PHILOSOPHY
    assert candidate["candidate_boundary"] == service.CANDIDATE_BOUNDARY
    assert candidate["candidate_goal"] == service.CANDIDATE_GOAL


def test_eight_method_packages_and_three_blocked_packages(candidate):
    packages = candidate["method_packages"]
    assert packages == service.METHOD_PACKAGES
    assert len(packages) == 8
    assert len([row for row in packages if row["status"].startswith("BLOCKED_")]) == 3
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_recommended_package_is_classification_and_not_selected(candidate):
    recommended = next(
        row for row in candidate["method_packages"] if row["package_id"] == service.RECOMMENDED_PACKAGE
    )
    assert recommended["status"] == service.RECOMMENDATION_STATUS
    assert recommended["selected"] is False
    assert candidate["recommendation_reason"] == service.RECOMMENDATION_REASON


def test_future_method_requirements_are_exact(candidate):
    assert candidate["future_method_requirements"] == service.FUTURE_METHOD_REQUIREMENTS
    assert len(candidate["future_method_requirements"]) == 18
    assert all(candidate["future_method_requirements"].values())


def test_future_method_plan_is_planned_not_executed(candidate):
    assert candidate["future_method_plan"] == service.FUTURE_METHOD_PLAN
    assert len(candidate["future_method_plan"]) == 10
    assert candidate["future_method_plan_status"] == "PLANNED_NOT_EXECUTED"


def test_planned_outputs_are_not_generated(candidate):
    assert candidate["planned_outputs"] == service.PLANNED_OUTPUTS
    assert len(candidate["planned_outputs"]) == 11
    assert all(row["status"] == "PLANNED_NOT_GENERATED" for row in candidate["planned_outputs"])


def test_non_goals_chain_gates_and_risk_controls(candidate):
    assert candidate["non_goals"] == service.NON_GOALS
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert "candidate_does_not_rerun_retry" in candidate["risk_controls"]
    assert "preserve_meta_limitation" in candidate["risk_controls"]


def test_checklist_and_summary_pass(candidate):
    assert [row["check_id"] for row in candidate["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in candidate["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 57
    assert candidate["summary"]["passed_checks"] == 57
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    assert candidate["summary"]["method_selected"] is False
    assert candidate["summary"]["new_retry_candidate_created"] is False


def test_candidate_digest_is_deterministic(candidate):
    assert candidate["marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest"] == (
        service.marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest_v1(candidate)
    )


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(candidate)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"), ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"), ("source_retry_failure_diagnosis_digest", "0" * 64),
        ("retry_execution_commit", ""), ("retry_pytest_failed_count", None),
        ("root_full_regression_is_retry_evidence", True),
        ("retry_failure_candidate_created", False),
        ("retry_failure_candidate_ready_for_operator_review", False),
        ("recommended_retry_failure_method_package", ""),
        ("retry_failure_method_selected", True), ("retry_failure_method_approved", True),
        ("retry_failure_method_executed", True), ("new_retry_candidate_created", True),
        ("new_retry_executed", True), ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True), ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True), ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True), ("marketflow_outputs_committed", True),
        ("evidence_regenerated", True), ("provider_requests_made_in_candidate", True),
        ("market_data_acquisition_performed_in_candidate", True),
        ("dataset_generation_performed_in_candidate", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_invalid_boundaries(candidate, field, bad_value):
    invalid = deepcopy(candidate)
    invalid[field] = bad_value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(invalid)


def test_validator_rejects_selected_recommended_package(candidate):
    invalid = deepcopy(candidate)
    invalid["method_packages"][0]["selected"] = True
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(invalid)


@pytest.mark.parametrize(
    "field", ["method_packages", "future_method_requirements", "future_method_plan", "risk_controls"]
)
def test_validator_rejects_missing_candidate_sections(candidate, field):
    invalid = deepcopy(candidate)
    invalid.pop(field)
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(invalid)


def test_validator_rejects_missing_digest(candidate):
    invalid = deepcopy(candidate)
    invalid.pop("marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest")
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(invalid)


def test_invalid_source_diagnosis_fails_closed():
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError
    ):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(
            source_diagnosis={"source_retry_failure_diagnosis_digest": "0" * 64}
        )


def test_markdown_includes_required_sections(candidate):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_markdown_v1(candidate)
    for title in (
        "MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate v1",
        "Source Retry Failure Diagnosis", "Failure Context", "Retry Environment", "Candidate Scope",
        "Candidate Philosophy", "Proposed Method Packages", "Recommended Method Package",
        "Future Method Requirements", "Future Method Plan", "Planned Outputs", "Non-Goals",
        "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary",
        "Guardrails",
    ):
        assert title in markdown
    assert "not retry evidence" in markdown


def test_writer_round_trips_without_overwrite(tmp_path, candidate):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == candidate
    assert receipt["marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest"] == (
        candidate["marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest"]
    )
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError
    ):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(tmp_path)
