from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_service
    as service,
)


def _state(**overrides: object) -> dict:
    value = {
        "worktree_exists": True,
        "worktree_head": service.INTEGRATION_HEAD,
        "worktree_is_detached": True,
        "worktree_clean": True,
        "python_executable_exists": True,
        "target_module_presence": {item: True for item in service.TARGET_MODULES},
        "origin_main": service.EXPECTED_ORIGIN_MAIN,
        "integration_branch_head": service.INTEGRATION_HEAD,
        "remote_integration_branch_exists": False,
        "root_tracked_marketflow_count": 0,
        "root_tracked_pytest_cache_count": 0,
        "worktree_tracked_marketflow_count": 0,
        "worktree_tracked_pytest_cache_count": 0,
    }
    value.update(overrides)
    return value


def _receipt_path(tmp_path: Path) -> Path:
    return tmp_path / "docs" / "status" / service.DEFAULT_RECEIPT_FILENAME


def _runner(argv, cwd):
    return {
        "exit_code": 1,
        "stdout": b"A" * 22000 + b" API_KEY=abc123 Bearer token.value",
        "stderr": b"PASSWORD=hunter2 U12345678",
        "duration_seconds": "1.250000",
    }


def _build(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, runner=_runner) -> dict:
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state())
    return service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z",
        command_runner=runner,
        durable_receipt_path=_receipt_path(tmp_path),
    )


def _set_path(value: dict, path: str, replacement: object) -> None:
    target = value
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = replacement


def test_nonzero_execution_is_successful_diagnostic_evidence(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    artifact = _build(tmp_path, monkeypatch)
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_SUCCESS
    assert artifact["execution_status"] == service.EXECUTION_STATUS_SUCCESS
    assert artifact["controlled_recapture_execution_result"]["exit_code"] == 1
    assert artifact["controlled_recapture_output_capture_summary"]["nonzero_exit_code_is_diagnostic_evidence_only"] is True
    assert artifact["retry_success_claimed"] is False


def test_receipt_is_prewritten_before_runner_and_finalized_afterward(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = _receipt_path(tmp_path)
    seen = {}

    def runner(argv, cwd):
        seen.update(json.loads(path.read_text(encoding="utf-8")))
        return {"exit_code": 2, "stdout": b"out", "stderr": b"err", "duration_seconds": "0.5"}

    artifact = _build(tmp_path, monkeypatch, runner=runner)
    assert seen["receipt_status"] == "PREWRITTEN_BEFORE_COMMAND"
    assert seen["command_executed"] is False and seen["receipt_finalized"] is False
    assert seen["approved_command_argv"] == service.APPROVED_ARGV
    assert seen["approved_cwd"] == str(service.APPROVED_WORKING_DIRECTORY)
    receipt = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["receipt_status"] == "FINALIZED_AFTER_COMMAND"
    assert receipt["command_executed"] is True and receipt["receipt_finalized"] is True
    assert receipt[service.RECEIPT_DIGEST_KEY] == artifact[service.RECEIPT_DIGEST_KEY]
    assert receipt[service.PAYLOAD_DIGEST_KEY] == artifact[service.PAYLOAD_DIGEST_KEY]
    assert receipt[service.DIGEST_MANIFEST_DIGEST_KEY] == artifact[service.DIGEST_MANIFEST_DIGEST_KEY]


def test_success_records_hashes_counts_bounds_and_redaction(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    artifact = _build(tmp_path, monkeypatch)
    result = artifact["controlled_recapture_execution_result"]
    assert len(result["stdout_sha256"]) == len(result["stderr_sha256"]) == 64
    assert result["stdout_byte_count"] + result["stderr_byte_count"] == result["combined_output_byte_count"]
    assert result["stdout_excerpt_truncated"] is True
    assert result["stderr_excerpt_truncated"] is False
    assert len(artifact["bounded_stdout_excerpt"]) == 20000
    assert "abc123" not in artifact["bounded_stdout_excerpt"]
    assert "hunter2" not in artifact["bounded_stderr_excerpt"]
    assert "U12345678" not in artifact["bounded_stderr_excerpt"]
    assert artifact["redaction_summary"]["redaction_checked"] is True


@pytest.mark.parametrize("field", service.SUCCESS_TRUE_FIELDS)
def test_success_authorized_facts_are_true(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str) -> None:
    assert _build(tmp_path, monkeypatch)[field] is True


@pytest.mark.parametrize("field", service.CLOSED_FALSE_FIELDS)
def test_closed_boundaries_remain_false(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str) -> None:
    assert _build(tmp_path, monkeypatch)[field] is False


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_source_bindings_are_exact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str) -> None:
    assert _build(tmp_path, monkeypatch)[field] == service.SOURCE_BINDINGS[field]


def test_success_digests_are_deterministic(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    first = _build(tmp_path, monkeypatch)
    _receipt_path(tmp_path).unlink()
    second = _build(tmp_path, monkeypatch)
    for field in (service.EXECUTION_DIGEST_KEY, service.PAYLOAD_DIGEST_KEY, service.RECEIPT_DIGEST_KEY, service.DIGEST_MANIFEST_DIGEST_KEY):
        assert first[field] == second[field]


def test_injected_completed_process_is_supported(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    artifact = _build(tmp_path, monkeypatch, runner=lambda argv, cwd: subprocess.CompletedProcess(argv, 3, b"out", b"err"))
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_SUCCESS
    assert artifact["controlled_recapture_execution_result"]["exit_code"] == 3


def test_default_runner_uses_list_argv_without_shell(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = {}

    def run(argv, **kwargs):
        seen["argv"] = argv
        seen.update(kwargs)
        return subprocess.CompletedProcess(argv, 1, b"out", b"err")

    monkeypatch.setattr(service.subprocess, "run", run)
    result = service._default_command_runner(service.APPROVED_ARGV, service.APPROVED_WORKING_DIRECTORY)
    assert seen["argv"] == service.APPROVED_ARGV
    assert seen["cwd"] == service.APPROVED_WORKING_DIRECTORY
    assert seen["shell"] is False
    assert result["exit_code"] == 1


@pytest.mark.parametrize(
    ("argv", "reason"),
    [
        ([*service.APPROVED_ARGV, "tests/extra.py"], "wrong_or_extra_target_module"),
        ([item for item in service.APPROVED_ARGV if item not in {"-p", "no:cacheprovider"}], "cacheprovider_not_disabled"),
        (service.APPROVED_ARGV[:-len(service.TARGET_MODULES)], "full_pytest_boundary_failure"),
        ([str(service.APPROVED_PYTHON_EXECUTABLE), "-m", "pytest", "-q"], "retry_command_boundary_failure"),
    ],
)
def test_command_boundary_mutations_are_rejected(tmp_path: Path, argv: list[str], reason: str) -> None:
    errors = service._precheck_errors(
        _state(), service.APPROVED_WORKING_DIRECTORY, service.APPROVED_PYTHON_EXECUTABLE,
        argv, _receipt_path(tmp_path), 20000, 20000,
    )
    assert reason in errors


@pytest.mark.parametrize(
    ("overrides", "missing"),
    [
        ({"worktree_exists": False}, "detached_worktree_missing"),
        ({"worktree_head": "0" * 40}, "detached_worktree_head_mismatch"),
        ({"worktree_is_detached": False}, "detached_worktree_not_detached"),
        ({"worktree_clean": False}, "detached_worktree_not_clean"),
        ({"python_executable_exists": False}, "approved_python_missing"),
        ({"origin_main": "0" * 40}, "origin_main_changed"),
        ({"integration_branch_head": "0" * 40}, "integration_branch_head_changed"),
        ({"remote_integration_branch_exists": True}, "remote_integration_branch_present"),
        ({"root_tracked_marketflow_count": 1}, "tracked_marketflow_present"),
        ({"worktree_tracked_pytest_cache_count": 1}, "tracked_pytest_cache_present"),
    ],
)
def test_precheck_failures_block_without_running(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, overrides: dict, missing: str) -> None:
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state(**overrides))
    called = False

    def runner(argv, cwd):
        nonlocal called
        called = True
        return _runner(argv, cwd)

    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=runner, durable_receipt_path=_receipt_path(tmp_path)
    )
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_BLOCKED
    assert artifact["blocked_reason"] == "PRE_EXECUTION_BOUNDARY_CHECK_FAILED"
    assert missing in artifact["missing_data"]
    assert called is False


def test_missing_target_module_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    presence = {item: True for item in service.TARGET_MODULES}
    presence[service.TARGET_MODULES[0]] = False
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state(target_module_presence=presence))
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner, durable_receipt_path=_receipt_path(tmp_path)
    )
    assert "target_module_missing" in artifact["missing_data"]


def test_wrong_worktree_and_python_block(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state())
    first = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner,
        diagnostic_working_directory=tmp_path, durable_receipt_path=_receipt_path(tmp_path),
    )
    assert "wrong_diagnostic_working_directory" in first["missing_data"]
    second = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner,
        python_executable=tmp_path / "python.exe", durable_receipt_path=_receipt_path(tmp_path),
    )
    assert "wrong_python_executable" in second["missing_data"]


def test_receipt_outside_docs_status_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state())
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner, durable_receipt_path=tmp_path / service.DEFAULT_RECEIPT_FILENAME
    )
    assert "receipt_path_not_docs_status" in artifact["missing_data"]


def test_existing_receipt_blocks_and_is_not_overwritten(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state())
    path = _receipt_path(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_text("sentinel", encoding="utf-8")
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner, durable_receipt_path=path
    )
    assert "receipt_already_exists" in artifact["missing_data"]
    assert path.read_text(encoding="utf-8") == "sentinel"


def test_scaffold_write_failure_blocks_before_command(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state())
    monkeypatch.setattr(service, "_persist_json", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("no write")))
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=lambda argv, cwd: pytest.fail("command ran"), durable_receipt_path=_receipt_path(tmp_path)
    )
    assert artifact["blocked_reason"] == "DURABLE_RECEIPT_SCAFFOLD_PREWRITE_FAILED"


def test_command_exception_blocks_without_rerun_and_keeps_scaffold(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state())
    calls = 0

    def runner(argv, cwd):
        nonlocal calls
        calls += 1
        raise RuntimeError("boom")

    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=runner, durable_receipt_path=_receipt_path(tmp_path)
    )
    assert calls == 1
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_BLOCKED
    assert artifact["durable_receipt_scaffold_prewritten"] is True
    assert json.loads(_receipt_path(tmp_path).read_text(encoding="utf-8"))["receipt_status"] == "PREWRITTEN_BEFORE_COMMAND"


def test_finalization_failure_blocks_without_rerun(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state())
    real_persist = service._persist_json
    writes = 0
    runs = 0

    def persist(path, payload, **kwargs):
        nonlocal writes
        writes += 1
        if writes == 2:
            raise OSError("final write failed")
        return real_persist(path, payload, **kwargs)

    def runner(argv, cwd):
        nonlocal runs
        runs += 1
        return _runner(argv, cwd)

    monkeypatch.setattr(service, "_persist_json", persist)
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=runner, durable_receipt_path=_receipt_path(tmp_path)
    )
    assert runs == 1 and writes == 2
    assert artifact["blocked_reason"] == "DURABLE_RECEIPT_FINALIZATION_FAILED"
    assert artifact["diagnostic_command_executed_in_execution"] is True


def test_postcheck_failure_persists_partial_blocked_receipt_without_rerun(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    states = iter([_state(), _state(worktree_clean=False)])
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: next(states))
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner, durable_receipt_path=_receipt_path(tmp_path)
    )
    assert artifact["blocked_reason"] == "POST_EXECUTION_BOUNDARY_CHECK_FAILED"
    receipt = json.loads(_receipt_path(tmp_path).read_text(encoding="utf-8"))
    assert receipt["receipt_status"] == "BLOCKED_AFTER_COMMAND_BOUNDARY_FAILURE"
    assert receipt["command_executed"] is True and receipt["receipt_finalized"] is False


def test_validator_accepts_success_and_blocked(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    success = _build(tmp_path, monkeypatch)
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(success)["failed_checks"] == 0
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state(worktree_exists=False))
    blocked = service.execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner, durable_receipt_path=tmp_path / "other" / "docs" / "status" / service.DEFAULT_RECEIPT_FILENAME
    )
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(blocked)["failed_checks"] == 0


@pytest.mark.parametrize(
    ("path", "replacement", "message"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("execution_status", "WRONG", "execution_status"),
        ("execution_scope", "WRONG", "execution_scope"),
        ("selected_receipt_recovery_or_recapture_package", "WRONG", "selected_receipt"),
        ("source_receipt_recovery_or_recapture_approval_digest", "0" * 64, "source_receipt"),
        ("source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest", "0" * 64, "source_targeted"),
        ("priority_1_total_nodeids", 611, "priority_1"),
        ("unavailable_prior_values_reconstructed", True, "closed boundary"),
        ("diagnostic_results_review_created", True, "closed boundary"),
        ("new_retry_candidate_created", True, "closed boundary"),
        ("retry_rerun_performed", True, "closed boundary"),
        ("full_pytest_performed", True, "closed boundary"),
        ("failure_error_separation_claimed", True, "closed boundary"),
        ("traceback_root_cause_claimed", True, "closed boundary"),
        ("integration_execution_successful", True, "closed boundary"),
        ("main_push_performed", True, "closed boundary"),
        ("provider_requests_made_in_execution", True, "closed boundary"),
        ("predictive_usefulness", "accepted", "acceptance boundary"),
        ("runtime_use", "AUTHORIZED", "runtime boundary"),
        ("controlled_recapture_command_record.argv", ["extra"], "approved command"),
        ("controlled_recapture_target_modules", ["extra"], "target modules"),
        ("durable_receipt_record.receipt_status", "PREWRITTEN_BEFORE_COMMAND", "durable receipt"),
        ("controlled_recapture_execution_result.stdout_sha256", "bad", "stdout_sha256"),
        ("bounded_stdout_excerpt", 4, "bounded stdout"),
        ("redaction_summary.redaction_checked", False, "redaction summary"),
        ("risk_controls", [], "risk controls"),
    ],
)
def test_validator_rejects_tampering(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, path: str, replacement: object, message: str) -> None:
    artifact = _build(tmp_path, monkeypatch)
    _set_path(artifact, path, replacement)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError, match=message):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(artifact)


def test_markdown_contains_required_sections(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_markdown_v1(_build(tmp_path, monkeypatch))
    for heading in (
        "Source Receipt Recovery or Recapture Approval", "Execution Scope", "Approved Priority 1 Target Modules",
        "Durable Receipt Scaffold", "Controlled Recapture Result", "Bounded Output Excerpts", "Redaction Summary",
        "Post-Execution Boundary Checks", "Unsupported Claims Boundary", "Authority Boundaries", "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_uses_exact_filename_and_protected_paths_fail(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "_read_environment", lambda worktree, executable: _state())
    output = tmp_path / "docs" / "status"
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        output, run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner
    )
    assert artifact["durable_receipt_path"] == str(output / service.DEFAULT_RECEIPT_FILENAME)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError, match="protected"):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
            tmp_path / ".marketflow", run_timestamp_utc="2026-08-23T00:00:00Z", command_runner=_runner
        )
