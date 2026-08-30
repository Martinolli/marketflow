from __future__ import annotations

import subprocess
from copy import deepcopy

import pytest

from marketflow.services import marketflow_repository_integration_branch_retry_execution_service as service


def _snapshot() -> dict:
    return {
        "repo_root": str(service.EXPECTED_REPO_ROOT.resolve(strict=False)),
        "worktree_path": str(service.EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)),
        "python_executable": str(service.EXPECTED_ROOT_PYTHON.resolve(strict=False)),
        "origin_main_commit": service.EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_head_commit": service.INTEGRATION_HEAD_COMMIT,
        "remote_integration_branch_exists": False,
        "worktree_exists": True,
        "worktree_head_commit": service.INTEGRATION_HEAD_COMMIT,
        "worktree_is_detached": True,
        "worktree_clean": True,
        "evidence_root_path": str(service.EXPECTED_STAGED_EVIDENCE_ROOT.resolve(strict=False)),
        "evidence_root_exists": True,
        "manifest_path": str(service.EXPECTED_STAGED_REQUIRED_MANIFEST.resolve(strict=False)),
        "manifest_exists": True,
        "evidence_inventory_digest": service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
        "evidence_file_count": 7,
        "evidence_total_bytes": 2458181,
        "evidence_root_ignored": True,
        "repository_tracked_marketflow_count": 0,
        "worktree_tracked_marketflow_count": 0,
        "root_virtualenv_python_exists": True,
    }


def _success_result() -> dict:
    return {
        "exit_code": 0,
        "passed_count": 26842,
        "failed_count": 0,
        "error_count": 0,
        "skipped_count": 7,
        "duration_seconds": "123.456000",
        "output_summary": "26842 passed, 7 skipped in 123.46s",
    }


def _failure_result() -> dict:
    return {
        "exit_code": 1,
        "passed_count": 26841,
        "failed_count": 1,
        "error_count": 0,
        "skipped_count": 7,
        "duration_seconds": "120.000000",
        "output_summary": "1 failed, 26841 passed, 7 skipped in 120.00s",
    }


def _execute(monkeypatch, result: dict) -> dict:
    monkeypatch.setattr(service, "_read_repository_snapshot", lambda *args: deepcopy(_snapshot()))
    monkeypatch.setattr(service, "_run_pytest", lambda *args: deepcopy(result))
    return service.execute_marketflow_repository_integration_branch_retry_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z"
    )


@pytest.fixture
def success(monkeypatch):
    return _execute(monkeypatch, _success_result())


@pytest.fixture
def blocked(monkeypatch):
    return _execute(monkeypatch, _failure_result())


def test_success_execution_builds_deterministic_artifact_in_fixture_mode(monkeypatch):
    first = _execute(monkeypatch, _success_result())
    second = _execute(monkeypatch, _success_result())
    assert first == second


def test_blocked_failure_execution_builds_deterministic_artifact_in_fixture_mode(monkeypatch):
    first = _execute(monkeypatch, _failure_result())
    second = _execute(monkeypatch, _failure_result())
    assert first == second


def test_real_pytest_execution_is_isolated_during_tests(monkeypatch):
    calls = []
    monkeypatch.setattr(service, "_read_repository_snapshot", lambda *args: deepcopy(_snapshot()))
    monkeypatch.setattr(service, "_run_pytest", lambda *args: calls.append(args) or deepcopy(_success_result()))
    service.execute_marketflow_repository_integration_branch_retry_v1()
    assert len(calls) == 1


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED),
        ("execution_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED_AUTHORITATIVE_FULL_PYTEST_PASSED),
        ("execution_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_ONLY_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("selected_integration_branch_retry_package", service.SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE),
        ("source_integration_branch_retry_approval_digest", service.EXPECTED_SOURCE_RETRY_APPROVAL_DIGEST),
        ("source_integration_branch_retry_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_integration_branch_retry_candidate_digest", service.EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST),
        ("source_remediation_results_review_digest", service.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_execution_digest", service.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST),
        ("source_staged_inventory_digest", service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST),
        ("attempted_execution_commit", service.ATTEMPTED_EXECUTION_COMMIT),
        ("original_blocked_status", service.ORIGINAL_BLOCKED_STATUS),
        ("original_first_integration_pytest_authoritative", True),
        ("original_first_integration_pytest_passed", False),
        ("original_first_integration_pytest_passed_count", 24481),
        ("original_first_integration_pytest_failed_count", 1300),
        ("original_first_integration_pytest_error_count", 500),
        ("original_first_integration_pytest_skipped_count", 7),
        ("later_wrong_worktree_rerun_diagnostic_only", True),
        ("later_wrong_worktree_rerun_overrides_original_failure", False),
        ("origin_main_commit_before_retry", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("origin_main_commit_after_retry", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_head_commit_before_retry", service.INTEGRATION_HEAD_COMMIT),
        ("integration_branch_head_commit_after_retry", service.INTEGRATION_HEAD_COMMIT),
        ("remote_integration_branch_exists_before_retry", False),
        ("remote_integration_branch_exists_after_retry", False),
        ("detached_integration_worktree_path", str(service.EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False))),
        ("detached_integration_worktree_head_commit_before_retry", service.INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_head_commit_after_retry", service.INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_is_detached", True),
        ("detached_integration_worktree_clean_before_retry", True),
        ("detached_integration_worktree_clean_after_retry", True),
        ("staged_evidence_manifest_digest_before_retry", service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST),
        ("staged_evidence_manifest_digest_after_retry", service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST),
        ("staged_evidence_unchanged_by_retry", True),
        ("marketflow_outputs_tracked_in_repository", False),
        ("marketflow_outputs_tracked_in_detached_worktree", False),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("retry_pytest_command", service.RETRY_PYTEST_COMMAND),
        ("retry_pytest_working_directory", str(service.EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False))),
        ("retry_pytest_ran_from_detached_worktree", True),
        ("retry_pytest_used_root_virtualenv_python", True),
        ("retry_pytest_first_result_authoritative", True),
        ("retry_pytest_performed", True),
        ("retry_pytest_passed", True),
        ("retry_pytest_exit_code", 0),
        ("retry_pytest_failed_count", 0),
        ("retry_pytest_error_count", 0),
        ("integration_branch_retry_selected", True),
        ("integration_branch_retry_approved", True),
        ("integration_branch_retry_authorized", True),
        ("integration_branch_retry_executed", True),
        ("integration_branch_retry_execution_successful", True),
        ("ready_for_integration_branch_retry_results_review", True),
        ("integration_branch_retry_results_review_created", False),
        ("integration_results_review_created", False),
        ("successful_integration_execution_digest_generated", True),
        ("successful_integration_validation_digest_generated", True),
        ("integration_branch_pushed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("provider_requests_made_in_execution", False),
        ("market_data_acquisition_performed_in_execution", False),
        ("dataset_generation_performed_in_execution", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", service.NOT_ACCEPTED),
        ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED),
        ("broker_execution", service.NOT_AUTHORIZED),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK_SUCCESS),
    ],
)
def test_success_required_fields(success, field, expected):
    assert success[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED),
        ("execution_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED),
        ("retry_pytest_passed", False),
        ("retry_pytest_exit_code", 1),
        ("retry_pytest_failed_count", 1),
        ("integration_branch_retry_executed", True),
        ("integration_branch_retry_execution_successful", False),
        ("ready_for_integration_branch_retry_results_review", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK_BLOCKED),
    ],
)
def test_blocked_required_fields(blocked, field, expected):
    assert blocked[field] == expected


def test_success_digests_are_deterministic(success):
    assert success["marketflow_repository_integration_branch_retry_execution_digest"] == service.marketflow_repository_integration_branch_retry_execution_digest_v1(success)
    assert success["marketflow_repository_integration_branch_retry_validation_digest"] == service.marketflow_repository_integration_branch_retry_validation_digest_v1(success)


def test_blocked_artifact_has_no_success_digests(blocked):
    assert blocked.get("marketflow_repository_integration_branch_retry_execution_digest") is None
    assert blocked.get("marketflow_repository_integration_branch_retry_validation_digest") is None


@pytest.mark.parametrize("fixture_name", ["success", "blocked"])
def test_prechecks_steps_risk_controls_and_checklist_pass(request, fixture_name):
    artifact = request.getfixturevalue(fixture_name)
    assert [row["check_id"] for row in artifact["precheck_results"]] == service.PRECHECK_IDS
    assert all(row["status"] == service.PASS for row in artifact["precheck_results"])
    assert [row["step_id"] for row in artifact["execution_steps"]] == service.EXECUTION_STEP_IDS
    assert all(row["status"] == service.PASS for row in artifact["execution_steps"])
    assert artifact["risk_controls"] == service.RISK_CONTROLS
    assert [row["check_id"] for row in artifact["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in artifact["checklist"])
    assert artifact["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert artifact["summary"]["failed_checks"] == 0


def test_success_and_blocked_next_paths(success, blocked):
    assert success["next_chain"] == service.SUCCESS_NEXT_CHAIN
    assert success["next_gates"] == service.SUCCESS_NEXT_GATES
    assert blocked["next_chain"] == service.BLOCKED_NEXT_CHAIN
    assert blocked["next_gates"] == service.BLOCKED_NEXT_GATES


def test_validator_accepts_valid_success_and_blocked(success, blocked):
    assert service.validate_marketflow_repository_integration_branch_retry_execution_v1(success)["execution_status"] == success["execution_status"]
    assert service.validate_marketflow_repository_integration_branch_retry_execution_v1(blocked)["execution_status"] == blocked["execution_status"]


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "wrong"),
        ("execution_status", "wrong"),
        ("execution_scope", "wrong"),
        ("selected_integration_branch_retry_package", "wrong"),
        ("source_integration_branch_retry_approval_digest", "0" * 64),
        ("source_remediation_results_review_digest", "0" * 64),
        ("source_staged_inventory_digest", "0" * 64),
        ("origin_main_commit_after_retry", "0" * 40),
        ("integration_branch_head_commit_after_retry", "0" * 40),
        ("detached_integration_worktree_path", "wrong"),
        ("detached_integration_worktree_head_commit_after_retry", "0" * 40),
        ("detached_integration_worktree_is_detached", False),
        ("detached_integration_worktree_clean_after_retry", False),
        ("staged_evidence_root_path", "missing"),
        ("staged_evidence_manifest_digest_after_retry", "0" * 64),
        ("retry_pytest_working_directory", "wrong"),
        ("retry_pytest_performed", False),
        ("retry_pytest_first_result_authoritative", False),
        ("retry_pytest_failed_count", 1),
        ("integration_branch_retry_results_review_created", True),
        ("integration_results_review_created", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
        ("evidence_regenerated", True),
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
    ],
)
def test_validator_rejects_invalid_success_boundaries(success, field, bad_value):
    changed = deepcopy(success)
    changed[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_execution_v1(changed)


def test_validator_rejects_success_without_digests(success):
    changed = deepcopy(success)
    changed.pop("marketflow_repository_integration_branch_retry_execution_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_execution_v1(changed)


def test_validator_rejects_blocked_marked_successful(blocked):
    changed = deepcopy(blocked)
    changed["integration_branch_retry_execution_successful"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_execution_v1(changed)


def test_wrong_worktree_blocks_without_running_pytest(monkeypatch):
    snapshot = _snapshot()
    snapshot["worktree_path"] = "C:\\wrong"
    monkeypatch.setattr(service, "_read_repository_snapshot", lambda *args: deepcopy(snapshot))
    monkeypatch.setattr(service, "_run_pytest", lambda *args: pytest.fail("pytest must not run"))
    artifact = service.execute_marketflow_repository_integration_branch_retry_v1()
    assert artifact["execution_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_WRONG_WORKTREE
    assert artifact["retry_pytest_performed"] is False


@pytest.mark.parametrize(
    ("output", "expected"),
    [
        ("26842 passed, 7 skipped in 10.00s", (26842, 0, 0, 7)),
        ("1 failed, 26841 passed, 7 skipped in 10.00s", (26841, 1, 0, 7)),
        ("2 errors, 10 passed in 1.00s", (10, 0, 2, 0)),
    ],
)
def test_pytest_result_parser(output, expected):
    result = subprocess.CompletedProcess(args=[], returncode=0, stdout=output, stderr="")
    parsed = service._parse_pytest_result(result, 10.0)
    assert (
        parsed["passed_count"],
        parsed["failed_count"],
        parsed["error_count"],
        parsed["skipped_count"],
    ) == expected


@pytest.mark.parametrize(
    "section",
    [
        "MarketFlow Repository Integration Branch Retry Execution v1",
        "Source Retry Approval",
        "Failure and Remediation Context",
        "Execution Scope",
        "Precheck Results",
        "Authoritative Retry Command",
        "Authoritative Retry Result",
        "Repository and Worktree Boundaries",
        "Success or Blocked Disposition",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ],
)
def test_markdown_includes_required_sections(success, section):
    markdown = service.build_marketflow_repository_integration_branch_retry_execution_markdown_v1(success)
    assert section in markdown
