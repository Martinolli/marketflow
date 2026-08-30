from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_execution_service as service,
)


@pytest.fixture
def execution():
    return service.execute_marketflow_repository_integration_branch_validation_failure_remediation_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z",
        execute_file_operations=False,
    )


def test_fixture_execution_is_deterministic_and_does_not_touch_files_or_git(monkeypatch):
    calls = []

    def fail_operation(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("fixture mode must not touch files or git")

    monkeypatch.setattr(service, "_execute_file_staging", fail_operation)
    monkeypatch.setattr(service.subprocess, "run", fail_operation)
    first = service.execute_marketflow_repository_integration_branch_validation_failure_remediation_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", execute_file_operations=False
    )
    second = service.execute_marketflow_repository_integration_branch_validation_failure_remediation_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", execute_file_operations=False
    )
    assert first == second
    assert calls == []
    assert first["file_operation_mode"] == "DETERMINISTIC_FILE_OPERATION_FIXTURE"


def test_copy_logic_is_isolated_to_temporary_directories(tmp_path):
    source = tmp_path / "source"
    target = tmp_path / "nested" / "target"
    source.mkdir()
    (source / "manifest.json").write_text('{"frozen":true}', encoding="utf-8")
    (source / "evidence.bin").write_bytes(b"frozen-evidence")
    source_rows, staged_rows = service._copy_evidence_root(source, target)
    assert source_rows == staged_rows
    assert (target / "manifest.json").read_text(encoding="utf-8") == '{"frozen":true}'
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError
    ):
        service._copy_evidence_root(source, target)


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_RETRY_AFTER_WORKTREE_RESTORATION_V1),
        ("execution_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED_EVIDENCE_STAGED_AFTER_WORKTREE_RESTORATION),
        ("execution_scope", service.REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("selected_remediation_package", service.SELECTED_REMEDIATION_PACKAGE),
        ("created_offline_except_local_file_staging", True),
        ("governance_only", True),
        ("source_worktree_restoration_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_worktree_restoration_results_review_worktree_manifest_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_worktree_restoration_execution_digest", service.EXPECTED_SOURCE_RESTORATION_EXECUTION_DIGEST),
        ("source_worktree_restoration_execution_manifest_digest", service.EXPECTED_SOURCE_RESTORATION_EXECUTION_MANIFEST_DIGEST),
        ("source_worktree_restoration_approval_digest", service.EXPECTED_SOURCE_RESTORATION_APPROVAL_DIGEST),
        ("source_remediation_approval_digest", service.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST),
        ("source_remediation_operator_review_digest", service.EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST),
        ("source_remediation_candidate_digest", service.EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_DIAGNOSIS_DIGEST),
        ("source_merge_strategy_approval_digest", service.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST),
        ("attempted_execution_branch", service.ATTEMPTED_EXECUTION_BRANCH),
        ("attempted_execution_commit", service.ATTEMPTED_EXECUTION_COMMIT),
        ("integration_branch_name", service.INTEGRATION_BRANCH_NAME),
        ("integration_branch_head_commit_before_remediation", service.INTEGRATION_HEAD_COMMIT),
        ("integration_branch_head_commit_after_remediation", service.INTEGRATION_HEAD_COMMIT),
        ("integration_base_commit", service.INTEGRATION_BASE_COMMIT),
        ("integration_source_commit", service.INTEGRATION_SOURCE_COMMIT),
        ("origin_main_commit_before_remediation", service.INTEGRATION_BASE_COMMIT),
        ("origin_main_commit_after_remediation", service.INTEGRATION_BASE_COMMIT),
        ("detached_integration_worktree_path", str(service.DEFAULT_INTEGRATION_WORKTREE_PATH.resolve(strict=False))),
        ("detached_integration_worktree_exists", True),
        ("detached_integration_worktree_head_commit", service.INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_head_verified", True),
        ("detached_integration_worktree_is_detached", True),
        ("detached_integration_worktree_clean_before_staging", True),
        ("first_integration_pytest_authoritative", True),
        ("first_integration_pytest_passed", False),
        ("first_integration_pytest_passed_count", 24481),
        ("first_integration_pytest_failed_count", 1300),
        ("first_integration_pytest_error_count", 500),
        ("first_integration_pytest_skipped_count", 7),
        ("later_isolated_rerun_passed_count", 26842),
        ("later_isolated_rerun_skipped_count", 7),
        ("later_isolated_rerun_classification", "DIAGNOSTIC_ONLY_NOT_ACCEPTANCE_EVIDENCE"),
        ("later_isolated_rerun_overrides_first_failure", False),
        ("representative_failure", service.REPRESENTATIVE_FAILURE),
        ("diagnosed_root_cause", service.DIAGNOSED_ROOT_CAUSE),
        ("missing_required_file", service.REQUIRED_MANIFEST_NAME),
        ("remediation_selected", True),
        ("remediation_approved", True),
        ("remediation_authorized", True),
        ("remediation_executed", True),
        ("evidence_root_inventory_performed", True),
        ("source_frozen_evidence_roots_verified", True),
        ("acquisition_provider_evidence_root_verified", True),
        ("required_manifest_verified_before_staging", True),
        ("source_evidence_root_path", str(service.DEFAULT_SOURCE_EVIDENCE_ROOT.resolve(strict=False))),
        ("staged_evidence_root_created", True),
        ("staged_evidence_root_verified", True),
        ("staged_required_manifest_verified", True),
        ("staged_evidence_root_untracked", True),
        ("marketflow_outputs_copied_to_integration_worktree", True),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("source_evidence_root_untracked", True),
        ("source_evidence_file_count", 7),
        ("staged_evidence_file_count", 7),
        ("source_evidence_total_bytes", 2458181),
        ("staged_evidence_total_bytes", 2458181),
        ("source_evidence_manifest_digest", service.EXPECTED_EVIDENCE_MANIFEST_DIGEST),
        ("staged_evidence_manifest_digest", service.EXPECTED_EVIDENCE_MANIFEST_DIGEST),
        ("source_and_staged_evidence_match", True),
        ("required_ready_digest_prefix_verified", True),
        ("required_ready_digest_prefix", "57c0a06e"),
        ("blocked_digest_prefix_not_accepted_as_ready", True),
        ("blocked_digest_prefix", "783e0013"),
        ("remediation_precheck_working_directory", str(service.DEFAULT_INTEGRATION_WORKTREE_PATH.resolve(strict=False))),
        ("remediation_precheck_ran_from_detached_integration_worktree", True),
        ("wrong_worktree_pytest_blocked", True),
        ("integration_retry_candidate_created", False),
        ("integration_retry_approved", False),
        ("integration_retry_executed", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("remote_integration_branch_created", False),
        ("main_merge_performed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("tracked_marketflow_file_count", 0),
        ("no_tracked_marketflow_files", True),
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
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
    ],
)
def test_required_execution_fields(execution, field, expected):
    assert execution[field] == expected


def test_evidence_manifests_are_exact(execution):
    assert execution["source_evidence_manifest"] == service.EXPECTED_EVIDENCE_MANIFEST_ROWS
    assert execution["staged_evidence_manifest"] == service.EXPECTED_EVIDENCE_MANIFEST_ROWS
    assert execution["source_evidence_manifest"] is not execution["staged_evidence_manifest"]


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
    assert len(execution["next_chain"]) == 6
    assert len(execution["next_gates"]) == 6
    assert len(execution["risk_controls"]) == 39


def test_checklist_and_summary_pass(execution):
    assert [row["check_id"] for row in execution["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in execution["checklist"])
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in execution["checklist"]
    )
    assert execution["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert execution["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert execution["summary"]["failed_checks"] == 0
    assert execution["summary"]["blocker_count"] == 0


def test_digests_are_deterministic(execution):
    assert execution[
        "marketflow_repository_integration_branch_validation_failure_remediation_execution_digest"
    ] == service.marketflow_repository_integration_branch_validation_failure_remediation_execution_digest_v1(
        execution
    )
    assert execution[
        "marketflow_repository_integration_branch_validation_failure_remediation_evidence_manifest_digest"
    ] == service.marketflow_repository_integration_branch_validation_failure_remediation_evidence_manifest_digest_v1(
        execution
    )


def test_validator_accepts_valid_execution(execution):
    result = service.validate_marketflow_repository_integration_branch_validation_failure_remediation_execution_v1(
        execution
    )
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED_EVIDENCE_STAGED_AFTER_WORKTREE_RESTORATION
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("execution_scope", "WRONG"),
        ("selected_remediation_package", "WRONG"),
        ("source_worktree_restoration_results_review_digest", "0" * 64),
        ("source_worktree_restoration_results_review_worktree_manifest_digest", "0" * 64),
        ("source_remediation_approval_digest", "0" * 64),
        ("source_failure_diagnosis_digest", "0" * 64),
        ("attempted_execution_commit", ""),
        ("integration_branch_name", "WRONG"),
        ("integration_branch_head_commit_before_remediation", "0" * 40),
        ("integration_branch_head_commit_after_remediation", "0" * 40),
        ("origin_main_commit_before_remediation", "0" * 40),
        ("origin_main_commit_after_remediation", "0" * 40),
        ("detached_integration_worktree_exists", False),
        ("detached_integration_worktree_head_commit", "0" * 40),
        ("detached_integration_worktree_head_verified", False),
        ("detached_integration_worktree_is_detached", False),
        ("first_integration_pytest_authoritative", False),
        ("first_integration_pytest_passed", True),
        ("later_isolated_rerun_overrides_first_failure", True),
        ("later_isolated_rerun_classification", "ACCEPTANCE_EVIDENCE"),
        ("diagnosed_root_cause", ""),
        ("remediation_executed", False),
        ("evidence_root_inventory_performed", False),
        ("source_frozen_evidence_roots_verified", False),
        ("acquisition_provider_evidence_root_verified", False),
        ("required_manifest_verified_before_staging", False),
        ("staged_evidence_root_created", False),
        ("staged_evidence_root_verified", False),
        ("staged_required_manifest_verified", False),
        ("staged_evidence_root_untracked", False),
        ("source_and_staged_evidence_match", False),
        ("required_ready_digest_prefix_verified", False),
        ("blocked_digest_prefix_not_accepted_as_ready", False),
        ("remediation_precheck_ran_from_detached_integration_worktree", False),
        ("wrong_worktree_pytest_blocked", False),
        ("marketflow_outputs_committed", True),
        ("evidence_regenerated", True),
        ("integration_retry_candidate_created", True),
        ("integration_retry_executed", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("successful_integration_validation_digest_generated", True),
        ("integration_branch_pushed", True),
        ("remote_integration_branch_created", True),
        ("main_merge_performed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("tracked_marketflow_file_count", 1),
        ("no_tracked_marketflow_files", False),
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
        ("next_chain", []),
        ("next_gates", []),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_invalid_boundaries(execution, field, bad_value):
    invalid = deepcopy(execution)
    invalid[field] = bad_value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError
    ):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_execution_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_repository_integration_branch_validation_failure_remediation_execution_digest",
        "marketflow_repository_integration_branch_validation_failure_remediation_evidence_manifest_digest",
    ],
)
def test_validator_rejects_missing_digests(execution, field):
    execution.pop(field)
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError
    ):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_execution_v1(
            execution
        )


def test_wrong_worktree_and_source_paths_are_rejected_in_fixture_mode():
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError
    ):
        service.execute_marketflow_repository_integration_branch_validation_failure_remediation_v1(
            integration_worktree_path="C:\\wrong-worktree", execute_file_operations=False
        )
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError
    ):
        service.execute_marketflow_repository_integration_branch_validation_failure_remediation_v1(
            source_evidence_root_path="C:\\wrong-source", execute_file_operations=False
        )


def test_markdown_contains_required_sections(execution):
    markdown = service.build_marketflow_repository_integration_branch_validation_failure_remediation_execution_markdown_v1(
        execution
    )
    for heading in (
        "# MarketFlow Repository Integration Branch Validation Failure Remediation Execution v1",
        "## Source Worktree Restoration Results Review",
        "## Source Remediation Approval",
        "## Failure Summary",
        "## Root Cause",
        "## Execution Scope",
        "## Detached Worktree Verification",
        "## Evidence Root Inventory",
        "## Evidence Staging",
        "## Digest Verification",
        "## Wrong-Worktree Guard",
        "## Authority Boundaries",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown
