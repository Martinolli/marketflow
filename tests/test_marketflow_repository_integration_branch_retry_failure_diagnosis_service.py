from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_diagnosis_service as service,
)


@pytest.fixture
def diagnosis():
    return service.build_marketflow_repository_integration_branch_retry_failure_diagnosis_v1()


def test_diagnosis_builds_offline_and_deterministically(diagnosis):
    assert service.build_marketflow_repository_integration_branch_retry_failure_diagnosis_v1() == diagnosis
    assert diagnosis["created_offline"] is True
    assert diagnosis["governance_only"] is True
    assert diagnosis["diagnosis_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1),
        ("diagnosis_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_READY),
        ("diagnosis_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("source_retry_execution_artifact_kind", service.SOURCE_RETRY_EXECUTION_ARTIFACT_KIND),
        ("source_retry_execution_status", service.SOURCE_RETRY_EXECUTION_STATUS),
        ("source_retry_execution_scope", service.SOURCE_RETRY_EXECUTION_SCOPE),
        ("source_retry_approval_digest", service.SOURCE_RETRY_APPROVAL_DIGEST),
        ("source_retry_operator_review_digest", service.SOURCE_RETRY_OPERATOR_REVIEW_DIGEST),
        ("source_retry_candidate_digest", service.SOURCE_RETRY_CANDIDATE_DIGEST),
        ("source_remediation_results_review_digest", service.SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_execution_digest", service.SOURCE_REMEDIATION_EXECUTION_DIGEST),
        ("source_staged_inventory_digest", service.SOURCE_STAGED_INVENTORY_DIGEST),
        ("source_failure_diagnosis_digest", service.SOURCE_FAILURE_DIAGNOSIS_DIGEST),
        ("source_merge_strategy_approval_digest", service.SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST),
        ("retry_execution_branch", service.RETRY_EXECUTION_BRANCH),
        ("retry_execution_commit", service.RETRY_EXECUTION_COMMIT),
        ("retry_pytest_command", service.RETRY_PYTEST_COMMAND),
        ("retry_pytest_working_directory", service.RETRY_PYTEST_WORKING_DIRECTORY),
        ("retry_pytest_ran_from_detached_worktree", True),
        ("retry_pytest_used_root_virtualenv_python", True),
        ("retry_pytest_first_result_authoritative", True),
        ("retry_pytest_performed", True),
        ("retry_pytest_exit_code", 1),
        ("retry_pytest_passed", False),
        ("retry_pytest_failed", True),
        ("retry_pytest_passed_count", 24877),
        ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112),
        ("retry_pytest_skipped_count", 7),
        ("first_retry_failure_authoritative", True),
        ("later_retry_rerun_performed", False),
        ("later_retry_rerun_overrides_first_retry_failure", False),
        ("retry_execution_successful", False),
        ("ready_for_retry_results_review", False),
        ("retry_results_review_created", False),
        ("integration_results_review_created", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("origin_main_commit_before_retry", service.ORIGIN_MAIN_COMMIT),
        ("origin_main_commit_after_retry", service.ORIGIN_MAIN_COMMIT),
        ("integration_branch_name", service.INTEGRATION_BRANCH_NAME),
        ("integration_branch_head_commit_before_retry", service.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("integration_branch_head_commit_after_retry", service.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("remote_integration_branch_exists_before_retry", False),
        ("remote_integration_branch_exists_after_retry", False),
        ("detached_integration_worktree_path", service.RETRY_PYTEST_WORKING_DIRECTORY),
        ("detached_integration_worktree_head_commit_before_retry", service.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("detached_integration_worktree_head_commit_after_retry", service.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("detached_integration_worktree_is_detached", True),
        ("detached_integration_worktree_clean_before_retry", True),
        ("detached_integration_worktree_clean_after_retry", True),
        ("staged_evidence_manifest_digest_before_retry", service.SOURCE_STAGED_INVENTORY_DIGEST),
        ("staged_evidence_manifest_digest_after_retry", service.SOURCE_STAGED_INVENTORY_DIGEST),
        ("staged_evidence_unchanged_by_retry", True),
        ("marketflow_outputs_tracked_in_repository", False),
        ("marketflow_outputs_tracked_in_detached_worktree", False),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("root_full_regression_passed_count", 29066),
        ("root_full_regression_skipped_count", 7),
        ("root_full_regression_is_retry_evidence", False),
        ("root_full_regression_does_not_override_detached_retry_failure", True),
        ("diagnosis_created", True),
        ("diagnosis_ready", True),
        ("integration_branch_pushed", False),
        ("remote_integration_branch_created", False),
        ("main_merge_performed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("provider_requests_made_in_diagnosis", False),
        ("market_data_acquisition_performed_in_diagnosis", False),
        ("dataset_generation_performed_in_diagnosis", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", service.NOT_ACCEPTED),
        ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED),
        ("broker_execution", service.NOT_AUTHORIZED),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
        ("recommended_next_task_status", service.RECOMMENDED_NEXT_TASK_STATUS),
        ("recommended_action", service.RECOMMENDED_ACTION),
        ("retry_results_review_blocked", True),
        ("main_merge_approval_blocked", True),
        ("integration_retry_allowed_now", False),
    ],
)
def test_required_diagnosis_fields(diagnosis, field, expected):
    assert diagnosis[field] == expected


def test_diagnosis_domains_are_exact(diagnosis):
    assert diagnosis["diagnosis_domains"] == service.DIAGNOSIS_DOMAINS
    assert len(diagnosis["diagnosis_domains"]) == 11
    assert {row["domain"] for row in diagnosis["diagnosis_domains"]} >= {
        "RETRY_GATE_STATUS", "PYTEST_ERROR_DOMAIN", "PYTEST_FAILURE_DOMAIN",
        "STAGED_EVIDENCE_VALIDITY", "AUTHORITY_BOUNDARY",
    }


def test_diagnostic_comparison_and_delta_are_exact(diagnosis):
    comparison = diagnosis["diagnostic_comparison"]
    assert comparison["original_failed_run"] == service.ORIGINAL_FAILED_RUN
    assert comparison["retry_failed_run"] == service.RETRY_FAILED_RUN
    assert comparison["delta"] == {"passed": 396, "failed": -8, "errors": -388, "skipped": 0}
    assert comparison["interpretation"] == service.COMPARISON_INTERPRETATION


def test_root_cause_questions_are_preserved(diagnosis):
    assert diagnosis["root_cause_questions"] == service.ROOT_CAUSE_QUESTIONS
    assert len(diagnosis["root_cause_questions"]) == 13


def test_recommendation_chain_gates_and_risk_controls(diagnosis):
    assert diagnosis["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert diagnosis["next_chain"] == service.NEXT_CHAIN
    assert diagnosis["next_gates"] == service.NEXT_GATES
    assert diagnosis["risk_controls"] == service.RISK_CONTROLS
    assert "diagnosis_does_not_rerun_retry" in diagnosis["risk_controls"]
    assert "preserve_meta_limitation" in diagnosis["risk_controls"]


def test_checklist_and_summary_pass(diagnosis):
    assert [row["check_id"] for row in diagnosis["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in diagnosis["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in diagnosis["checklist"])
    assert diagnosis["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 53
    assert diagnosis["summary"]["passed_checks"] == 53
    assert diagnosis["summary"]["failed_checks"] == 0
    assert diagnosis["summary"]["blocker_count"] == 0
    assert diagnosis["summary"]["retry_execution_successful"] is False


def test_diagnosis_digest_is_deterministic(diagnosis):
    assert diagnosis["marketflow_repository_integration_branch_retry_failure_diagnosis_digest"] == (
        service.marketflow_repository_integration_branch_retry_failure_diagnosis_digest_v1(diagnosis)
    )


def test_validator_accepts_valid_diagnosis(diagnosis):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(diagnosis)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_READY
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"), ("diagnosis_status", "WRONG"),
        ("diagnosis_scope", "WRONG"), ("source_retry_approval_digest", "0" * 64),
        ("retry_execution_commit", ""), ("retry_pytest_performed", False),
        ("retry_pytest_first_result_authoritative", False), ("retry_pytest_failed", False),
        ("retry_pytest_passed", True), ("successful_integration_execution_digest_generated", True),
        ("successful_integration_validation_digest_generated", True), ("retry_results_review_created", True),
        ("integration_results_review_created", True), ("retry_execution_successful", True),
        ("root_full_regression_is_retry_evidence", True), ("origin_main_commit_after_retry", "0" * 40),
        ("integration_branch_head_commit_after_retry", "0" * 40),
        ("detached_integration_worktree_head_commit_after_retry", "0" * 40),
        ("staged_evidence_unchanged_by_retry", False), ("marketflow_outputs_tracked_in_repository", True),
        ("provider_requests_made_in_diagnosis", True),
        ("market_data_acquisition_performed_in_diagnosis", True),
        ("dataset_generation_performed_in_diagnosis", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_invalid_boundaries(diagnosis, field, bad_value):
    invalid = deepcopy(diagnosis)
    invalid[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(invalid)


@pytest.mark.parametrize(
    "field", ["diagnosis_domains", "diagnostic_comparison", "root_cause_questions", "risk_controls"]
)
def test_validator_rejects_missing_governance_sections(diagnosis, field):
    invalid = deepcopy(diagnosis)
    invalid.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(invalid)


def test_validator_rejects_missing_digest(diagnosis):
    invalid = deepcopy(diagnosis)
    invalid.pop("marketflow_repository_integration_branch_retry_failure_diagnosis_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(invalid)


def test_invalid_source_execution_and_failure_snapshot_fail_closed():
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError):
        service.build_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(
            source_execution={"source_retry_approval_digest": "0" * 64}
        )
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError):
        service.build_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(
            failure_snapshot={"integration_branch_head_commit_after_retry": "0" * 40}
        )


def test_markdown_includes_required_sections(diagnosis):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_diagnosis_markdown_v1(diagnosis)
    for title in (
        "MarketFlow Repository Integration Branch Retry Failure Diagnosis v1", "Source Retry Execution",
        "Failure Summary", "Retry Environment", "Original Failure Comparison", "Root Regression Boundary",
        "Diagnosis Domains", "Root-Cause Questions", "Recommendation", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert title in markdown
    assert "not retry evidence" in markdown


def test_writer_round_trips_without_overwrite(tmp_path, diagnosis):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_diagnosis_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == diagnosis
    assert receipt["marketflow_repository_integration_branch_retry_failure_diagnosis_digest"] == (
        diagnosis["marketflow_repository_integration_branch_retry_failure_diagnosis_digest"]
    )
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError):
        service.write_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(tmp_path)
