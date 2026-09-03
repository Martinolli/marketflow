from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_service
    as service,
)


def _state() -> dict:
    return {
        "worktree_exists": True,
        "worktree_head": service.INTEGRATION_HEAD,
        "worktree_is_detached": True,
        "worktree_clean": True,
        "python_executable_exists": True,
        "target_module_presence": {target: True for target in service.TARGET_MODULES},
        "origin_main": service.EXPECTED_ORIGIN_MAIN,
        "integration_branch_head": service.INTEGRATION_HEAD,
        "remote_integration_branch_exists": False,
        "root_tracked_marketflow_count": 0,
        "root_tracked_pytest_cache_count": 0,
        "worktree_tracked_marketflow_count": 0,
        "worktree_tracked_pytest_cache_count": 0,
    }


RAW_STDOUT = b"failure detail API_KEY=example-secret\n" + (b"x" * 250)
RAW_STDERR = b"Bearer example.token.value\n" + (b"y" * 250)


def _runner(argv, cwd) -> dict:
    return {
        "exit_code": 1,
        "stdout": RAW_STDOUT,
        "stderr": RAW_STDERR,
        "duration_seconds": "1.250000",
    }


def _execute(monkeypatch: pytest.MonkeyPatch, **kwargs) -> dict:
    monkeypatch.setattr(service, "_read_execution_environment", lambda *args: deepcopy(_state()))
    return service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z",
        command_runner=_runner,
        max_stdout_excerpt_chars=120,
        max_stderr_excerpt_chars=120,
        **kwargs,
    )


@pytest.fixture
def success(monkeypatch: pytest.MonkeyPatch) -> dict:
    return _execute(monkeypatch)


def test_success_execution_builds_with_nonzero_injected_result(success: dict) -> None:
    assert success["artifact_kind"] == service.ARTIFACT_KIND_SUCCESS
    assert success["diagnostic_execution_result"]["exit_code"] == 1
    assert success["diagnostic_output_capture_summary"]["nonzero_exit_code_is_diagnostic_evidence_only"] is True


def test_command_runner_is_called_once(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []
    monkeypatch.setattr(service, "_read_execution_environment", lambda *args: deepcopy(_state()))
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z",
        command_runner=lambda argv, cwd: calls.append((argv, cwd)) or _runner(argv, cwd),
    )
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_SUCCESS
    assert len(calls) == 1


def test_default_runner_uses_list_form_without_shell(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, 1, stdout=b"out", stderr=b"err")

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = service._default_command_runner(service.EXPECTED_ARGV, service.APPROVED_WORKING_DIRECTORY)
    assert result["exit_code"] == 1
    assert calls[0][0] == list(service.EXPECTED_ARGV)
    assert calls[0][1]["shell"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_SUCCESS),
        ("execution_status", service.EXECUTION_STATUS_SUCCESS),
        ("execution_scope", service.EXECUTION_SCOPE),
        ("selected_targeted_diagnostic_capture_package", service.SELECTED_PACKAGE),
        ("source_targeted_diagnostic_output_capture_approval_digest", service.SOURCE_APPROVAL_DIGEST),
        ("retry_execution_commit", service.RETRY_EXECUTION_COMMIT),
        ("failed_or_errored_nodeids_count", 1404), ("module_summary_module_count", 29),
        ("priority_1_total_nodeids", 612), ("top_10_count_sum", 1069),
        ("diagnostic_command_is_retry", False), ("diagnostic_command_is_full_pytest", False),
        ("predictive_usefulness", "not accepted"), ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"), ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_success_scalar_fields(success: dict, field: str, expected: object) -> None:
    assert success[field] == expected


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_all_source_bindings_are_exact(success: dict, field: str) -> None:
    assert success[field] == service.SOURCE_BINDINGS[field]


@pytest.mark.parametrize("field", service.SUCCESS_TRUE_FIELDS)
def test_success_execution_facts_are_true(success: dict, field: str) -> None:
    assert success[field] is True


@pytest.mark.parametrize("field", service.CLOSED_FALSE_FIELDS)
def test_closed_boundaries_are_false(success: dict, field: str) -> None:
    assert success[field] is False


def test_command_cwd_targets_and_duration_recorded(success: dict) -> None:
    record = success["diagnostic_command_record"]
    assert record["command"] == service.APPROVED_COMMAND
    assert record["argv"] == list(service.EXPECTED_ARGV)
    assert record["cwd"] == str(service.APPROVED_WORKING_DIRECTORY)
    assert record["python_executable"] == str(service.APPROVED_PYTHON_EXECUTABLE)
    assert record["target_modules"] == service.TARGET_MODULES
    assert success["diagnostic_execution_result"]["duration_seconds"] == "1.250000"


def test_output_is_hashed_counted_bounded_and_truncated(success: dict) -> None:
    result = success["diagnostic_execution_result"]
    assert result["stdout_sha256"] == hashlib.sha256(RAW_STDOUT).hexdigest()
    assert result["stderr_sha256"] == hashlib.sha256(RAW_STDERR).hexdigest()
    assert result["stdout_byte_count"] == len(RAW_STDOUT)
    assert result["stderr_byte_count"] == len(RAW_STDERR)
    assert result["combined_output_byte_count"] == len(RAW_STDOUT) + len(RAW_STDERR)
    assert result["stdout_excerpt_truncated"] is True
    assert result["stderr_excerpt_truncated"] is True
    assert len(success["bounded_stdout_excerpt"]) <= 120
    assert len(success["bounded_stderr_excerpt"]) <= 120


def test_output_excerpts_are_redacted(success: dict) -> None:
    combined = success["bounded_stdout_excerpt"] + success["bounded_stderr_excerpt"]
    assert "example-secret" not in combined
    assert "example.token.value" not in combined
    assert "<REDACTED>" in combined
    assert success["redaction_summary"]["redaction_applied"] is True
    assert set(success["redaction_summary"]["redaction_patterns_applied"]) == {
        "bearer_token", "environment_secret_assignment"
    }


def test_success_outputs_and_recommendation(success: dict) -> None:
    assert success["outputs"] == service.SUCCESS_OUTPUTS
    assert len(success["outputs"]) == 15
    assert success["ready_for_targeted_diagnostic_output_capture_results_review"] is True
    assert success["ready_for_retry_candidate"] is False
    assert success["recommended_next_task"].endswith("TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RESULTS_REVIEW_V1")


def test_success_digests_are_deterministic(monkeypatch: pytest.MonkeyPatch) -> None:
    first = _execute(monkeypatch)
    second = _execute(monkeypatch)
    for field in (service.EXECUTION_DIGEST_KEY, service.PAYLOAD_DIGEST_KEY, service.DIGEST_MANIFEST_DIGEST_KEY):
        assert first[field] == second[field]


def test_success_validator_accepts(success: dict) -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(success)
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("state_field", "replacement", "missing_reason"),
    [
        ("python_executable_exists", False, "approved_python_missing"),
        ("worktree_exists", False, "detached_worktree_missing"),
        ("worktree_head", "0" * 40, "detached_worktree_head_mismatch"),
        ("worktree_is_detached", False, "detached_worktree_not_detached"),
        ("worktree_clean", False, "detached_worktree_not_clean"),
        ("origin_main", "0" * 40, "origin_main_changed"),
        ("integration_branch_head", "0" * 40, "integration_branch_head_changed"),
        ("remote_integration_branch_exists", True, "remote_integration_branch_present"),
        ("root_tracked_pytest_cache_count", 1, "tracked_pytest_cache_present"),
        ("worktree_tracked_marketflow_count", 1, "tracked_marketflow_present"),
    ],
)
def test_precheck_failure_builds_blocked_artifact(monkeypatch: pytest.MonkeyPatch, state_field: str, replacement: object, missing_reason: str) -> None:
    state = _state()
    state[state_field] = replacement
    monkeypatch.setattr(service, "_read_execution_environment", lambda *args: deepcopy(state))
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner
    )
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_BLOCKED
    assert artifact["diagnostic_command_executed"] is False
    assert missing_reason in artifact["missing_data"]


def test_missing_target_module_builds_blocked_artifact(monkeypatch: pytest.MonkeyPatch) -> None:
    state = _state()
    state["target_module_presence"][service.TARGET_MODULES[0]] = False
    monkeypatch.setattr(service, "_read_execution_environment", lambda *args: deepcopy(state))
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner
    )
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_BLOCKED
    assert "target_module_missing" in artifact["missing_data"]


@pytest.mark.parametrize(
    ("argv", "reason"),
    [
        (list(service.EXPECTED_ARGV) + ["tests/test_extra.py"], "wrong_or_extra_target_module"),
        ([item for item in service.EXPECTED_ARGV if item != "no:cacheprovider"], "cacheprovider_not_disabled"),
        ([str(service.APPROVED_PYTHON_EXECUTABLE), "-m", "pytest", "-q"], "wrong_or_extra_target_module"),
    ],
)
def test_command_boundary_rejects_extra_cacheless_or_retry_command(argv: list[str], reason: str) -> None:
    errors = service._precheck_errors(
        _state(), service.APPROVED_WORKING_DIRECTORY, service.APPROVED_PYTHON_EXECUTABLE, argv, 20000, 20000
    )
    assert reason in errors


def test_wrong_cwd_and_python_build_blocked(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(service, "_read_execution_environment", lambda *args: deepcopy(_state()))
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner,
        diagnostic_working_directory=tmp_path, python_executable=tmp_path / "python.exe",
    )
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_BLOCKED
    assert {"wrong_diagnostic_working_directory", "wrong_python_executable"}.issubset(artifact["missing_data"])


def test_runner_exception_builds_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "_read_execution_environment", lambda *args: deepcopy(_state()))

    def fail(argv, cwd):
        raise OSError("unavailable")

    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=fail
    )
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_BLOCKED
    assert artifact["blocked_reason"] == "DIAGNOSTIC_COMMAND_EXECUTION_OR_CAPTURE_FAILED:OSError"


def test_wrong_source_approval_builds_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
        source_approval={"artifact_kind": "WRONG"}, run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner
    )
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_BLOCKED
    assert artifact["blocked_reason"] == "SOURCE_APPROVAL_BOUNDARY_CHECK_FAILED"


def test_blocked_artifact_has_manifest_and_validates(monkeypatch: pytest.MonkeyPatch) -> None:
    state = _state()
    state["python_executable_exists"] = False
    monkeypatch.setattr(service, "_read_execution_environment", lambda *args: deepcopy(state))
    first = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner
    )
    second = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner
    )
    assert first[service.BLOCKED_MANIFEST_DIGEST_KEY] == second[service.BLOCKED_MANIFEST_DIGEST_KEY]
    assert first[service.EXECUTION_DIGEST_KEY] == second[service.EXECUTION_DIGEST_KEY]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(first)["failed_checks"] == 0


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("execution_status", "WRONG"), ("execution_scope", "WRONG"),
        ("created_offline", True), ("governance_only", True),
        ("targeted_diagnostic_output_capture_execution_created", False),
        ("selected_targeted_diagnostic_capture_package", "WRONG"),
        ("source_targeted_diagnostic_output_capture_approval_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_operator_review_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64), ("source_prioritized_planning_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64), ("source_materialized_payload_digest", "0" * 64),
        ("source_detail_binding_approval_digest", "0" * 64), ("source_recovery_detail_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_failure_context", {}),
        ("priority_1_top_module_groups", []), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403), ("diagnostic_command_executed", False),
        ("targeted_pytest_performed", False), ("diagnostic_output_captured", False),
        ("diagnostic_command_used_detached_worktree_cwd", False), ("diagnostic_command_used_approved_python", False),
        ("diagnostic_command_used_cacheprovider_disabled", False), ("diagnostic_command_is_retry", True),
        ("diagnostic_command_is_full_pytest", True), ("diagnostic_command_record.target_modules", []),
        ("diagnostic_execution_result.exit_code", None), ("diagnostic_execution_result.stdout_sha256", None),
        ("diagnostic_execution_result.stderr_sha256", None), ("bounded_stdout_excerpt", None),
        ("bounded_stderr_excerpt", None), (service.PAYLOAD_DIGEST_KEY, None),
        ("diagnostic_execution_result.duration_seconds", "invalid"),
        ("diagnostic_execution_result.combined_output_byte_count", -1),
        ("diagnostic_output_capture_summary.maximum_stdout_excerpt_chars", 20001),
        ("redaction_summary.redaction_checked", False),
        (service.DIGEST_MANIFEST_DIGEST_KEY, None), ("diagnostic_results_review_created", True),
        ("remediation_or_method_candidate_after_diagnostic_capture_created", True),
        ("new_retry_candidate_created", True), ("new_retry_executed", True),
        ("cache_read_in_execution", True), ("pytest_cache_committed", True),
        ("marketflow_outputs_committed", True), ("planning_reentry_rerun_performed", True),
        ("detail_binding_reattempt_rerun_performed", True), ("materialization_execution_rerun_performed", True),
        ("source_recovery_rerun_performed", True), ("retry_rerun_performed", True),
        ("full_pytest_performed", True), ("classification_execution_performed_in_execution", True),
        ("remediation_execution_performed", True), ("failure_error_separation_claimed", True),
        ("first_failure_identified", True), ("first_error_identified", True),
        ("first_order_claim_made", True), ("traceback_root_cause_claimed", True),
        ("direct_code_remediation_recommended", True), ("retry_success_claimed", True),
        ("main_merge_readiness_claimed", True), ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True), ("integration_branch_pushed", True),
        ("main_push_performed", True), ("origin_main_modified_by_this_task", True),
        ("evidence_regenerated", True), ("provider_requests_made_in_execution", True),
        ("env_inspection_performed", True), ("market_data_acquisition_performed_in_execution", True),
        ("dataset_generation_performed_in_execution", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("risk_controls", []), (service.EXECUTION_DIGEST_KEY, "0" * 64),
    ],
)
def test_validator_rejects_success_mutation(success: dict, path: str, replacement: object) -> None:
    value = deepcopy(success)
    target = value
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = replacement
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(value)


def test_markdown_has_required_sections(success: dict) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_markdown_v1(success)
    for heading in (
        "Source Approval", "Source Operator Review and Candidate", "Source Remediation or Method Results Review",
        "Source Planning Reentry with Complete Detail", "Source Detail Binding Results Review", "Retry Failure Context",
        "Execution Scope", "Approved Priority 1 Target Modules", "Approved Diagnostic Command", "Pre-Execution Checks",
        "Diagnostic Capture Result", "Diagnostic Output Capture Summary", "Bounded Output Excerpts", "Redaction Summary",
        "Unsupported Claims Boundary", "Success or Blocked Disposition", "Recommendation", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown
