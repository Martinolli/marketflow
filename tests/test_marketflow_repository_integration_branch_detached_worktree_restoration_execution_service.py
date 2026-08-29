from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_execution_service as service,
)


@pytest.fixture
def execution():
    return service.execute_marketflow_repository_integration_branch_detached_worktree_restoration_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z",
        execute_git_operations=False,
    )


def test_fixture_execution_is_deterministic_and_does_not_call_subprocess(monkeypatch):
    calls = []

    def fail_subprocess(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("fixture mode must not invoke git")

    monkeypatch.setattr(service.subprocess, "run", fail_subprocess)
    first = service.execute_marketflow_repository_integration_branch_detached_worktree_restoration_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", execute_git_operations=False
    )
    second = service.execute_marketflow_repository_integration_branch_detached_worktree_restoration_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", execute_git_operations=False
    )
    assert first == second
    assert calls == []
    assert first["git_operation_mode"] == "DETERMINISTIC_OPERATION_FIXTURE"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_V1),
        ("execution_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED_REGISTERED_DETACHED_WORKTREE_CREATED),
        ("execution_scope", service.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW),
        ("selected_worktree_restoration_package", service.SELECTED_WORKTREE_RESTORATION_PACKAGE),
        ("created_offline_except_local_git_worktree_creation", True),
        ("governance_only", True),
        ("source_worktree_restoration_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_worktree_restoration_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_worktree_restoration_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_remediation_approval_digest", service.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST),
        ("source_remediation_operator_review_digest", service.EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST),
        ("source_remediation_candidate_digest", service.EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_DIAGNOSIS_DIGEST),
        ("source_merge_strategy_approval_digest", service.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST),
        ("blocked_remediation_execution_artifact_kind", service.EXPECTED_BLOCKED_EXECUTION_ARTIFACT_KIND),
        ("blocked_remediation_execution_status", service.EXPECTED_BLOCKED_EXECUTION_STATUS),
        ("origin_main_commit_before_execution", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("origin_main_commit_after_execution", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_name", service.EXPECTED_INTEGRATION_BRANCH_NAME),
        ("integration_branch_head_commit_before_execution", service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("integration_branch_head_commit_after_execution", service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("integration_branch_exists_local", True),
        ("integration_branch_matches_required_head", True),
        ("integration_branch_deleted_or_reset", False),
        ("worktree_restoration_path", str(service.DEFAULT_WORKTREE_PATH.resolve(strict=False))),
        ("worktree_restoration_path_deterministic", True),
        ("worktree_restoration_path_existed_before_execution", False),
        ("worktree_restoration_path_exists_after_execution", True),
        ("registered_worktree_entries_present_before_execution", False),
        ("registered_worktree_entries_present_after_execution", True),
        ("detached_worktree_created", True),
        ("detached_worktree_restored", True),
        ("detached_worktree_deleted", False),
        ("registered_detached_worktree_created", True),
        ("worktree_head_commit", service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("worktree_head_verified", True),
        ("worktree_is_detached", True),
        ("worktree_branch_checked_out", False),
        ("remote_integration_branch_exists_before_execution", False),
        ("remote_integration_branch_exists_after_execution", False),
        ("integration_branch_pushed", False),
        ("worktree_restoration_selected", True),
        ("worktree_restoration_approved", True),
        ("worktree_restoration_authorized", True),
        ("worktree_restoration_executed", True),
        ("ready_for_worktree_restoration_results_review", True),
        ("remediation_executed", False),
        ("evidence_staged", False),
        ("marketflow_outputs_copied", False),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("integration_retry_candidate_created", False),
        ("integration_retry_executed", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("provider_requests_made_in_execution", False),
        ("market_data_acquisition_performed_in_execution", False),
        ("dataset_generation_performed_in_execution", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("no_tracked_marketflow_files", True),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
    ],
)
def test_required_execution_fields(execution, field, expected):
    assert execution[field] == expected


def test_prechecks_and_execution_steps_are_complete_and_pass(execution):
    assert [row["step_id"] for row in execution["precheck_results"]] == service.PRECHECK_IDS
    assert [row["step_id"] for row in execution["execution_steps"]] == service.EXECUTION_STEP_IDS
    assert all(row["status"] == service.PASS for row in execution["precheck_results"])
    assert all(row["status"] == service.PASS for row in execution["execution_steps"])
    assert all(
        set(row) == {"step_id", "status", "expected", "actual", "message"}
        for row in execution["precheck_results"] + execution["execution_steps"]
    )


def test_next_chain_gates_and_risk_controls_are_exact(execution):
    assert execution["next_chain"] == service.NEXT_CHAIN
    assert execution["next_gates"] == service.NEXT_GATES
    assert execution["risk_controls"] == service.RISK_CONTROLS
    assert len(execution["next_chain"]) == 8
    assert len(execution["next_gates"]) == 8
    assert len(execution["risk_controls"]) == 36


def test_checklist_and_summary_pass(execution):
    assert [row["check_id"] for row in execution["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in execution["checklist"])
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in execution["checklist"]
    )
    assert execution["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 59
    assert execution["summary"]["passed_checks"] == 59
    assert execution["summary"]["failed_checks"] == 0
    assert execution["summary"]["blocker_count"] == 0


def test_digests_are_deterministic(execution):
    assert execution[
        "marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest"
    ] == service.marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest_v1(
        execution
    )
    assert execution[
        "marketflow_repository_integration_branch_detached_worktree_restoration_worktree_manifest_digest"
    ] == service.marketflow_repository_integration_branch_detached_worktree_restoration_worktree_manifest_digest_v1(
        execution
    )


def test_validator_accepts_valid_execution(execution):
    result = service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_execution_v1(
        execution
    )
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED_REGISTERED_DETACHED_WORKTREE_CREATED
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("execution_scope", "WRONG"),
        ("selected_worktree_restoration_package", "WRONG"),
        ("source_worktree_restoration_approval_digest", "0" * 64),
        ("source_worktree_restoration_operator_review_digest", "0" * 64),
        ("source_worktree_restoration_candidate_digest", "0" * 64),
        ("source_remediation_approval_digest", "0" * 64),
        ("source_failure_diagnosis_digest", "0" * 64),
        ("origin_main_commit_before_execution", "0" * 40),
        ("origin_main_commit_after_execution", "0" * 40),
        ("integration_branch_name", "WRONG"),
        ("integration_branch_head_commit_before_execution", "0" * 40),
        ("integration_branch_head_commit_after_execution", "0" * 40),
        ("integration_branch_exists_local", False),
        ("integration_branch_deleted_or_reset", True),
        ("worktree_restoration_path", "C:\\wrong"),
        ("worktree_restoration_path_existed_before_execution", True),
        ("worktree_restoration_path_exists_after_execution", False),
        ("registered_worktree_entries_present_before_execution", True),
        ("registered_worktree_entries_present_after_execution", False),
        ("detached_worktree_created", False),
        ("detached_worktree_restored", False),
        ("detached_worktree_deleted", True),
        ("registered_detached_worktree_created", False),
        ("worktree_head_commit", "0" * 40),
        ("worktree_head_verified", False),
        ("worktree_is_detached", False),
        ("worktree_branch_checked_out", True),
        ("remote_integration_branch_exists_before_execution", True),
        ("remote_integration_branch_exists_after_execution", True),
        ("integration_branch_pushed", True),
        ("worktree_restoration_executed", False),
        ("ready_for_worktree_restoration_results_review", False),
        ("remediation_executed", True),
        ("evidence_staged", True),
        ("marketflow_outputs_copied", True),
        ("marketflow_outputs_committed", True),
        ("integration_retry_candidate_created", True),
        ("integration_retry_executed", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("provider_requests_made_in_execution", True),
        ("market_data_acquisition_performed_in_execution", True),
        ("dataset_generation_performed_in_execution", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("risk_controls", []),
        ("next_chain", []),
        ("next_gates", []),
        ("no_tracked_marketflow_files", False),
    ],
)
def test_validator_rejects_invalid_boundaries(execution, field, bad_value):
    invalid = deepcopy(execution)
    invalid[field] = bad_value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError
    ):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_execution_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest",
        "marketflow_repository_integration_branch_detached_worktree_restoration_worktree_manifest_digest",
    ],
)
def test_validator_rejects_missing_digests(execution, field):
    execution.pop(field)
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError
    ):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_execution_v1(
            execution
        )


def test_markdown_contains_required_sections(execution):
    markdown = service.build_marketflow_repository_integration_branch_detached_worktree_restoration_execution_markdown_v1(
        execution
    )
    for heading in (
        "# MarketFlow Repository Integration Branch Detached Worktree Restoration Execution v1",
        "## Source Restoration Approval",
        "## Blocked Remediation Execution Observation",
        "## Execution Scope",
        "## Worktree Restoration Path",
        "## Registered Worktree Creation",
        "## Worktree Head Verification",
        "## Origin/Main Protection",
        "## Remote Integration Branch Check",
        "## Authority Boundaries",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_real_execution_path_is_injected_and_not_run_in_default_tests(monkeypatch):
    observed = []

    def isolated(repo_root, worktree_path):
        observed.append((repo_root, worktree_path))
        return service._observations_fixture()

    monkeypatch.setattr(service, "_execute_git_restoration", isolated)
    result = service.execute_marketflow_repository_integration_branch_detached_worktree_restoration_v1(
        repo_root="C:\\fixture-repo",
        run_timestamp_utc="2026-08-23T00:00:00Z",
        execute_git_operations=True,
    )
    assert len(observed) == 1
    assert str(observed[0][0]).endswith("fixture-repo")
    assert result["worktree_head_verified"] is True
