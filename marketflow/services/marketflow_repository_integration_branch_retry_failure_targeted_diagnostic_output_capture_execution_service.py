"""Execute the approved bounded Priority 1 diagnostic-output capture once."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib
from pathlib import Path
import re
import subprocess
import time
from typing import Any, Callable, Mapping, Sequence

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_service
    as source,
)


ARTIFACT_KIND_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTED_V1"
ARTIFACT_KIND_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_BLOCKED_V1"
EXECUTION_STATUS_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTED_PRIORITY_1_DIAGNOSTIC_OUTPUT_CAPTURED"
EXECUTION_STATUS_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_BLOCKED_COMMAND_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_ONLY_DIAGNOSTIC_OUTPUT_CAPTURE_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
SOURCE_APPROVAL_DIGEST = "85b7bc5ddde9dd6aaacc2b870e42cbd380484ea006df8081c0d9f95bcf113255"
EXPECTED_ORIGIN_MAIN = "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
INTEGRATION_BRANCH = "integration/marketflow-terminal-evidence-stack-validation-v1"
INTEGRATION_HEAD = "220fbc220365fce9cae13ab4853cddff118c0187"
RETRY_EXECUTION_COMMIT = "ab178b65c69f0274b0abbf9c20df102d35e78d34"
EXPECTED_REPO_ROOT = Path(__file__).resolve().parents[2]
APPROVED_WORKING_DIRECTORY = Path(r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1")
APPROVED_PYTHON_EXECUTABLE = EXPECTED_REPO_ROOT / "env" / "Scripts" / "python.exe"
TARGET_MODULES = [item["module_path"] for item in source.source.source.TOP_MODULES]
APPROVED_ARGV = [
    str(APPROVED_PYTHON_EXECUTABLE), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=short", "-rA",
    *TARGET_MODULES,
]
APPROVED_COMMAND = " ".join(APPROVED_ARGV)
EXPECTED_ARGV = tuple(APPROVED_ARGV)

EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_digest"
PAYLOAD_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_payload_digest"
DIGEST_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_digest_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_blocked_manifest_digest"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

SOURCE_BINDINGS = {
    "source_targeted_diagnostic_output_capture_approval_digest": SOURCE_APPROVAL_DIGEST,
    **deepcopy(source.SOURCE_BINDINGS),
}

SUCCESS_OUTPUT_IDS = [
    "targeted_diagnostic_output_capture_execution_manifest", "diagnostic_command_record",
    "priority_1_target_module_execution_record", "diagnostic_exit_code_report",
    "diagnostic_stdout_hash_report", "diagnostic_stderr_hash_report",
    "bounded_stdout_excerpt_report", "bounded_stderr_excerpt_report",
    "diagnostic_output_volume_report", "diagnostic_redaction_summary",
    "diagnostic_cache_write_control_report", "diagnostic_results_review_enablement_report",
    "retry_gate_preservation_report", "unsupported_claims_boundary_report", "digest_manifest",
]
SUCCESS_OUTPUTS = [
    {"output_id": output_id, "status": "GENERATED_DIAGNOSTIC_EVIDENCE_ONLY"}
    for output_id in SUCCESS_OUTPUT_IDS
]
SUCCESS_NEXT_CHAIN = [
    "Targeted Diagnostic Output Capture Results Review v1.",
    "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1, if supported by results review.",
    "Remediation or Method Operator Review v1, if needed.", "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.", "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Targeted Diagnostic Output Capture Execution Failure Diagnosis v1.",
    "Alternate diagnostic capture candidate, if needed.",
    "No remediation/method candidate, retry, or main merge.",
]
SUCCESS_NEXT_GATES = [
    "targeted_diagnostic_output_capture_results_review",
    "retry_failure_remediation_or_method_candidate_after_diagnostic_capture_if_supported",
    "remediation_or_method_operator_review_if_needed", "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved", "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "targeted_diagnostic_output_capture_execution_failure_diagnosis",
    "alternate_diagnostic_capture_candidate_if_needed",
    "remediation_or_method_candidate_blocked_until_diagnostic_results_review_passes",
    "new_retry_blocked_until_remediation_or_method_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]
RISK_CONTROLS = [
    "diagnostic_capture_execution_uses_approved_package_only",
    "diagnostic_capture_execution_targets_priority_1_modules_only",
    "diagnostic_capture_execution_uses_detached_worktree_cwd",
    "diagnostic_capture_execution_uses_approved_python_executable",
    "diagnostic_capture_execution_uses_cacheprovider_disabled",
    "diagnostic_capture_execution_records_command_cwd_exit_stdout_stderr_duration",
    "diagnostic_capture_execution_bounds_output_volume", "diagnostic_capture_execution_hashes_full_output_streams",
    "diagnostic_capture_execution_redacts_secret_like_patterns", "diagnostic_capture_execution_does_not_inspect_env",
    "diagnostic_capture_execution_does_not_read_pytest_cache", "diagnostic_capture_execution_does_not_commit_pytest_cache",
    "diagnostic_capture_execution_does_not_commit_marketflow_outputs", "diagnostic_capture_execution_does_not_rerun_planning",
    "diagnostic_capture_execution_does_not_rerun_detail_binding", "diagnostic_capture_execution_does_not_rerun_materialization",
    "diagnostic_capture_execution_does_not_rerun_source_recovery", "diagnostic_capture_execution_does_not_execute_remediation",
    "diagnostic_capture_execution_does_not_execute_classification", "diagnostic_capture_execution_does_not_classify_modules_again",
    "diagnostic_capture_execution_does_not_identify_first_failure", "diagnostic_capture_execution_does_not_identify_first_error",
    "diagnostic_capture_execution_does_not_claim_traceback_root_cause",
    "diagnostic_capture_execution_does_not_recommend_direct_code_remediation",
    "diagnostic_capture_execution_does_not_create_diagnostic_results_review",
    "diagnostic_capture_execution_does_not_create_remediation_or_method_candidate",
    "diagnostic_capture_execution_does_not_create_new_retry_candidate",
    "diagnostic_capture_execution_does_not_create_retry_results_review",
    "diagnostic_capture_execution_does_not_create_integration_results_review",
    "diagnostic_capture_execution_does_not_mark_integration_successful",
    "diagnostic_capture_execution_does_not_generate_successful_integration_digest",
    "diagnostic_capture_execution_does_not_treat_diagnostic_capture_as_retry",
    "diagnostic_capture_execution_does_not_treat_diagnostic_exit_code_as_retry_result",
    "diagnostic_capture_execution_does_not_push_integration_branch", "diagnostic_capture_execution_does_not_push_main",
    "diagnostic_capture_execution_does_not_delete_integration_branch", "diagnostic_capture_execution_does_not_delete_worktree",
    "diagnostic_capture_execution_does_not_force_push", "diagnostic_capture_execution_does_not_prune_remotes",
    "diagnostic_capture_execution_does_not_modify_tags", "diagnostic_capture_execution_does_not_modify_staged_evidence",
    "diagnostic_capture_execution_does_not_regenerate_evidence", "diagnostic_capture_execution_does_not_call_providers",
    "diagnostic_capture_execution_does_not_acquire_market_data", "diagnostic_capture_execution_does_not_regenerate_dataset",
    "diagnostic_capture_execution_does_not_recompute_metrics", "diagnostic_capture_execution_does_not_train_models",
    "diagnostic_capture_execution_does_not_score_strategy", "diagnostic_capture_execution_does_not_generate_recommendations",
    "diagnostic_capture_execution_does_not_accept_predictive_usefulness",
    "diagnostic_capture_execution_does_not_accept_profitability", "diagnostic_capture_execution_does_not_authorize_runtime",
    "diagnostic_capture_execution_does_not_authorize_broker_execution",
    "diagnostic_capture_output_is_diagnostic_evidence_only",
    "future_diagnostic_results_review_required_before_remediation_or_method_candidate",
    "future_diagnostic_capture_is_not_retry_success", "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation", "previous_approval_remains_source_evidence",
    "previous_operator_review_remains_source_evidence", "previous_candidate_remains_source_evidence",
    "previous_planning_results_review_remains_valid", "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_results_review_required_after_diagnostic_capture",
    "separate_remediation_or_method_candidate_required_after_diagnostic_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

SUCCESS_TRUE_FIELDS = [
    "targeted_diagnostic_output_capture_execution_created", "targeted_diagnostic_output_capture_execution_performed",
    "diagnostic_capture_execution_performed", "diagnostic_command_executed", "diagnostic_output_captured",
    "diagnostic_method_executed", "targeted_pytest_performed", "approved_priority_1_modules_targeted",
    "only_priority_1_modules_targeted", "diagnostic_command_used_cacheprovider_disabled",
    "diagnostic_command_used_approved_python", "diagnostic_command_used_detached_worktree_cwd",
    "diagnostic_command_exit_code_captured", "diagnostic_stdout_captured", "diagnostic_stderr_captured",
    "diagnostic_output_bounded", "diagnostic_output_hashed", "diagnostic_output_redaction_checked",
]
CLOSED_FALSE_FIELDS = [
    "diagnostic_capture_results_review_created", "diagnostic_results_review_created",
    "remediation_or_method_candidate_after_diagnostic_capture_created", "remediation_execution_performed",
    "classification_execution_performed_in_execution", "new_retry_candidate_created", "new_retry_executed",
    "new_retry_results_review_created", "main_merge_approval_created", "cache_read_in_execution",
    "cache_modified_intentionally_in_execution", "cache_committed", "pytest_cache_committed",
    "marketflow_outputs_committed", "planning_reentry_rerun_performed", "detail_binding_reattempt_rerun_performed",
    "materialization_execution_rerun_performed", "source_recovery_rerun_performed",
    "module_grouping_recovered_in_execution", "retry_rerun_performed", "full_pytest_performed",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made", "traceback_root_cause_claimed",
    "direct_code_remediation_recommended", "retry_success_claimed", "main_merge_readiness_claimed",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "evidence_regenerated", "provider_requests_made_in_execution",
    "env_inspection_performed", "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]

REDACTION_PATTERNS = [
    ("bearer_token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"), "Bearer <REDACTED>"),
    ("environment_secret_assignment", re.compile(r"\b[A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*=[^\s,;]+"), "<REDACTED_ENV_ASSIGNMENT>"),
    ("secret_assignment", re.compile(r"(?i)\b(api[_-]?key|password|token|secret)\s*[:=]\s*[^\s,;]+"), r"\1=<REDACTED>"),
    ("ibkr_account_identifier", re.compile(r"\b[UD]\d{7,10}\b"), "<REDACTED_ACCOUNT>"),
]


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError(ValueError):
    """Raised when execution evidence violates the approved boundary."""


def _utc_timestamp(value: str | None) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if not isinstance(value, str) or not value.endswith("Z"):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("UTC run timestamp required")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("UTC run timestamp required") from exc
    if parsed.utcoffset() != timedelta(0):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("UTC run timestamp required")
    return value


def _git(args: Sequence[str], cwd: Path) -> tuple[int, str]:
    completed = subprocess.run(["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, shell=False)
    return completed.returncode, completed.stdout.decode("utf-8", errors="replace").strip()


def _read_execution_environment(worktree: Path, python_executable: Path) -> dict[str, Any]:
    head_code, head = _git(["rev-parse", "HEAD"], worktree) if worktree.is_dir() else (1, "")
    status_code, status = _git(["status", "--porcelain"], worktree) if worktree.is_dir() else (1, "")
    detached_code, _ = _git(["symbolic-ref", "-q", "HEAD"], worktree) if worktree.is_dir() else (0, "")
    origin_code, origin_main = _git(["rev-parse", "origin/main"], EXPECTED_REPO_ROOT)
    integration_code, integration_head = _git(["rev-parse", INTEGRATION_BRANCH], EXPECTED_REPO_ROOT)
    remote_code, remote_integration = _git(["show-ref", "--verify", "--hash", f"refs/remotes/origin/{INTEGRATION_BRANCH}"], EXPECTED_REPO_ROOT)
    root_marketflow_code, root_marketflow = _git(["ls-files", ".marketflow"], EXPECTED_REPO_ROOT)
    root_cache_code, root_cache = _git(["ls-files", ".pytest_cache"], EXPECTED_REPO_ROOT)
    worktree_marketflow_code, worktree_marketflow = _git(["ls-files", ".marketflow"], worktree) if worktree.is_dir() else (1, "")
    worktree_cache_code, worktree_cache = _git(["ls-files", ".pytest_cache"], worktree) if worktree.is_dir() else (1, "")
    return {
        "worktree_exists": worktree.is_dir(), "worktree_head": head if head_code == 0 else None,
        "worktree_is_detached": detached_code != 0, "worktree_clean": status_code == 0 and status == "",
        "python_executable_exists": python_executable.is_file(),
        "target_module_presence": {target: (worktree / target).is_file() for target in TARGET_MODULES},
        "origin_main": origin_main if origin_code == 0 else None,
        "integration_branch_head": integration_head if integration_code == 0 else None,
        "remote_integration_branch_exists": remote_code == 0 and bool(remote_integration),
        "root_tracked_marketflow_count": len(root_marketflow.splitlines()) if root_marketflow_code == 0 and root_marketflow else 0,
        "root_tracked_pytest_cache_count": len(root_cache.splitlines()) if root_cache_code == 0 and root_cache else 0,
        "worktree_tracked_marketflow_count": len(worktree_marketflow.splitlines()) if worktree_marketflow_code == 0 and worktree_marketflow else 0,
        "worktree_tracked_pytest_cache_count": len(worktree_cache.splitlines()) if worktree_cache_code == 0 and worktree_cache else 0,
    }


def _precheck_errors(state: Mapping[str, Any], worktree: Path, python_executable: Path, argv: Sequence[str], max_stdout: int, max_stderr: int) -> list[str]:
    checks = {
        "detached_worktree_missing": state.get("worktree_exists") is True,
        "detached_worktree_head_mismatch": state.get("worktree_head") == INTEGRATION_HEAD,
        "detached_worktree_not_detached": state.get("worktree_is_detached") is True,
        "detached_worktree_not_clean": state.get("worktree_clean") is True,
        "approved_python_missing": state.get("python_executable_exists") is True,
        "target_module_missing": all(state.get("target_module_presence", {}).get(target) is True for target in TARGET_MODULES),
        "wrong_diagnostic_working_directory": worktree.resolve(strict=False) == APPROVED_WORKING_DIRECTORY.resolve(strict=False),
        "wrong_python_executable": python_executable.resolve(strict=False) == APPROVED_PYTHON_EXECUTABLE.resolve(strict=False),
        "wrong_or_extra_target_module": tuple(argv) == EXPECTED_ARGV,
        "cacheprovider_not_disabled": "no:cacheprovider" in argv and "-p" in argv,
        "full_pytest_boundary_failure": list(argv)[-len(TARGET_MODULES):] == TARGET_MODULES,
        "retry_command_boundary_failure": list(argv) != [str(APPROVED_PYTHON_EXECUTABLE), "-m", "pytest", "-q"],
        "origin_main_changed": state.get("origin_main") == EXPECTED_ORIGIN_MAIN,
        "integration_branch_head_changed": state.get("integration_branch_head") == INTEGRATION_HEAD,
        "remote_integration_branch_present": state.get("remote_integration_branch_exists") is False,
        "tracked_marketflow_present": state.get("root_tracked_marketflow_count") == 0 and state.get("worktree_tracked_marketflow_count") == 0,
        "tracked_pytest_cache_present": state.get("root_tracked_pytest_cache_count") == 0 and state.get("worktree_tracked_pytest_cache_count") == 0,
        "invalid_stdout_bound": isinstance(max_stdout, int) and 0 < max_stdout <= 20000,
        "invalid_stderr_bound": isinstance(max_stderr, int) and 0 < max_stderr <= 20000,
    }
    return [reason for reason, passed in checks.items() if not passed]


def _default_command_runner(argv: Sequence[str], cwd: Path) -> dict[str, Any]:
    started = time.perf_counter()
    completed = subprocess.run(list(argv), cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, shell=False)
    return {
        "exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr,
        "duration_seconds": f"{time.perf_counter() - started:.6f}",
    }


def _normalise_runner_result(result: Any, elapsed_seconds: float) -> dict[str, Any]:
    if isinstance(result, subprocess.CompletedProcess):
        exit_code, stdout, stderr, duration = result.returncode, result.stdout or b"", result.stderr or b"", elapsed_seconds
    elif isinstance(result, Mapping):
        exit_code = result.get("exit_code", result.get("returncode"))
        stdout, stderr = result.get("stdout", b""), result.get("stderr", b"")
        duration = result.get("duration_seconds", elapsed_seconds)
    else:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("command runner returned unsupported result")
    if not isinstance(exit_code, int):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("command runner did not return integer exit code")
    if isinstance(stdout, str):
        stdout = stdout.encode("utf-8")
    if isinstance(stderr, str):
        stderr = stderr.encode("utf-8")
    if not isinstance(stdout, bytes) or not isinstance(stderr, bytes):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("command output must be bytes or text")
    return {"exit_code": exit_code, "stdout": stdout, "stderr": stderr, "duration_seconds": f"{float(duration):.6f}"}


def _redact(value: str) -> tuple[str, bool, list[str]]:
    applied: list[str] = []
    redacted = value
    for pattern_id, pattern, replacement in REDACTION_PATTERNS:
        redacted, count = pattern.subn(replacement, redacted)
        if count:
            applied.append(pattern_id)
    return redacted, bool(applied), applied


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _payload(execution: Mapping[str, Any]) -> dict[str, Any]:
    return {field: deepcopy(execution.get(field)) for field in (
        "diagnostic_command_record", "diagnostic_target_modules", "diagnostic_execution_result",
        "diagnostic_output_capture_summary", "bounded_stdout_excerpt", "bounded_stderr_excerpt",
        "redaction_summary", "post_execution_boundary_checks",
    )}


def _execution_digest(execution: Mapping[str, Any]) -> str:
    value = deepcopy(dict(execution))
    for field in ("checklist", "summary", EXECUTION_DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def _blocked_manifest_digest(execution: Mapping[str, Any]) -> str:
    value = deepcopy(dict(execution))
    for field in ("checklist", "summary", EXECUTION_DIGEST_KEY, BLOCKED_MANIFEST_DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def _base_execution(run_timestamp: str) -> dict[str, Any]:
    execution: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "diagnostic_capture_execution_only": True, "run_timestamp_utc": run_timestamp,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {
            "passed": 24877, "failed": 1292, "errors": 112, "skipped": 7,
            "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True,
            "root_full_regression_is_retry_evidence": False,
        },
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "priority_1_top_module_groups": deepcopy(source.source.source.TOP_MODULES),
        "diagnostic_command_is_retry": False, "diagnostic_command_is_full_pytest": False,
        "diagnostic_capture_results_review_created": False, "diagnostic_results_review_created": False,
        "remediation_or_method_candidate_after_diagnostic_capture_created": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "risk_controls": list(RISK_CONTROLS),
    }
    execution.update({field: False for field in CLOSED_FALSE_FIELDS})
    return execution


def _build_blocked(run_timestamp: str, reason: str, state: Mapping[str, Any] | None = None, missing: Sequence[str] = ()) -> dict[str, Any]:
    execution = _base_execution(run_timestamp)
    execution.update({
        "artifact_kind": ARTIFACT_KIND_BLOCKED, "execution_status": EXECUTION_STATUS_BLOCKED,
        "created_offline": True, "governance_only": False,
        "targeted_diagnostic_output_capture_execution_created": True,
        "targeted_diagnostic_output_capture_execution_performed": False,
        "diagnostic_capture_execution_performed": False, "diagnostic_command_executed": False,
        "diagnostic_output_captured": False, "diagnostic_method_executed": False,
        "targeted_pytest_performed": False, "approved_priority_1_modules_targeted": False,
        "only_priority_1_modules_targeted": False, "diagnostic_command_used_cacheprovider_disabled": False,
        "diagnostic_command_used_approved_python": False, "diagnostic_command_used_detached_worktree_cwd": False,
        "diagnostic_command_exit_code_captured": False, "diagnostic_stdout_captured": False,
        "diagnostic_stderr_captured": False, "diagnostic_output_bounded": False,
        "diagnostic_output_hashed": False, "diagnostic_output_redaction_checked": False,
        "blocked_reason": reason,
        "available_data": {
            "source_approval_digest": SOURCE_APPROVAL_DIGEST, "selected_package": SELECTED_PACKAGE,
            "planned_command": APPROVED_COMMAND, "planned_cwd": str(APPROVED_WORKING_DIRECTORY),
            "planned_target_modules": list(TARGET_MODULES), "completed_precheck_facts": deepcopy(dict(state or {})),
        },
        "missing_data": list(missing), "outputs": [],
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_V1",
        "recommended_next_task_status": "FUTURE_FAILURE_DIAGNOSIS_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS",
        "ready_for_targeted_diagnostic_output_capture_results_review": False,
        "ready_for_remediation_or_method_candidate_after_diagnostic_capture": False,
        "ready_for_retry_candidate": False, "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(BLOCKED_NEXT_GATES),
    })
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = _blocked_manifest_digest(execution)
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    execution[EXECUTION_DIGEST_KEY] = _execution_digest(execution)
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(execution)
    return execution


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    checks = [
        _check("source_approval_digest_bound", SOURCE_APPROVAL_DIGEST, execution.get("source_targeted_diagnostic_output_capture_approval_digest")),
        _check("source_operator_review_digest_bound", source.SOURCE_OPERATOR_REVIEW_DIGEST, execution.get("source_targeted_diagnostic_output_capture_candidate_operator_review_digest")),
        _check("source_candidate_digest_bound", source.source.SOURCE_CANDIDATE_DIGEST, execution.get("source_targeted_diagnostic_output_capture_candidate_digest")),
        _check("source_results_review_digest_bound", source.SOURCE_BINDINGS["source_results_review_digest"], execution.get("source_results_review_digest")),
        _check("source_prioritized_planning_review_digest_bound", source.SOURCE_BINDINGS["source_prioritized_planning_review_digest"], execution.get("source_prioritized_planning_review_digest")),
        _check("source_results_review_manifest_digest_bound", source.SOURCE_BINDINGS["source_results_review_manifest_digest"], execution.get("source_results_review_manifest_digest")),
        _check("source_planning_execution_digest_bound", source.SOURCE_BINDINGS["source_planning_execution_digest"], execution.get("source_planning_execution_digest")),
        _check("source_prioritized_planning_digest_bound", source.SOURCE_BINDINGS["source_prioritized_planning_digest"], execution.get("source_prioritized_planning_digest")),
        _check("source_planning_digest_manifest_digest_bound", source.SOURCE_BINDINGS["source_planning_digest_manifest_digest"], execution.get("source_planning_digest_manifest_digest")),
        _check("source_detail_binding_results_review_digest_bound", source.SOURCE_BINDINGS["source_detail_binding_results_review_digest"], execution.get("source_detail_binding_results_review_digest")),
        _check("source_complete_29_row_binding_digest_bound", source.SOURCE_BINDINGS["source_complete_29_row_binding_digest"], execution.get("source_complete_29_row_binding_digest")),
        _check("source_materialized_payload_digest_bound", source.SOURCE_BINDINGS["source_materialized_payload_digest"], execution.get("source_materialized_payload_digest")),
        _check("source_detail_binding_approval_digest_bound", source.SOURCE_BINDINGS["source_detail_binding_approval_digest"], execution.get("source_detail_binding_approval_digest")),
        _check("source_prior_blocked_detail_binding_execution_digest_bound", source.SOURCE_BINDINGS["source_prior_blocked_detail_binding_execution_digest"], execution.get("source_prior_blocked_detail_binding_execution_digest")),
        _check("source_prior_blocked_detail_binding_reason_bound", source.SOURCE_BINDINGS["source_prior_blocked_detail_binding_reason"], execution.get("source_prior_blocked_detail_binding_reason")),
        _check("source_recovery_results_review_digest_bound", source.SOURCE_BINDINGS["source_recovery_results_review_digest"], execution.get("source_recovery_results_review_digest")),
        _check("source_recovery_detail_digest_bound", source.SOURCE_BINDINGS["source_recovery_detail_digest"], execution.get("source_recovery_detail_digest")),
        _check("source_after_v2_approval_digest_bound", source.SOURCE_BINDINGS["source_after_v2_approval_digest"], execution.get("source_after_v2_approval_digest")),
        _check("source_module_grouping_digest_bound", source.SOURCE_BINDINGS["source_module_grouping_digest"], execution.get("source_module_grouping_digest")),
        _check("retry_execution_commit_bound", RETRY_EXECUTION_COMMIT, execution.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, {key: execution.get("retry_failure_context", {}).get(key) for key in ("passed", "failed", "errors", "skipped")}),
        _check("selected_diagnostic_capture_package_bound", SELECTED_PACKAGE, execution.get("selected_targeted_diagnostic_capture_package")),
        _check("approval_authorizes_execution_true", True, SOURCE_APPROVAL_DIGEST == execution.get("source_targeted_diagnostic_output_capture_approval_digest")),
        _check("priority_1_top_module_paths_bound", TARGET_MODULES, [item.get("module_path") for item in execution.get("priority_1_top_module_groups", [])]),
        _check("priority_1_top_module_counts_bound", [136, 131, 122, 112, 111], [item.get("failed_or_errored_nodeid_count") for item in execution.get("priority_1_top_module_groups", [])]),
        _check("priority_1_total_612_bound", 612, execution.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, execution.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, execution.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, execution.get("failed_or_errored_nodeids_count")),
    ]
    if success:
        pre = execution.get("diagnostic_command_record", {}).get("pre_execution_checks", {})
        result = execution.get("diagnostic_execution_result", {})
        checks.extend([
            _check("detached_worktree_exists_if_success", True, pre.get("worktree_exists")),
            _check("detached_worktree_head_verified_if_success", INTEGRATION_HEAD, pre.get("worktree_head")),
            _check("detached_worktree_clean_if_success", True, pre.get("worktree_clean")),
            _check("approved_python_exists_if_success", True, pre.get("python_executable_exists")),
            _check("target_modules_exist_if_success", True, all(pre.get("target_module_presence", {}).values())),
            _check("only_priority_1_modules_targeted_if_success", TARGET_MODULES, execution.get("diagnostic_target_modules")),
            _check("command_uses_cacheprovider_disabled_if_success", True, execution.get("diagnostic_command_used_cacheprovider_disabled")),
            _check("command_is_not_full_pytest_if_success", False, execution.get("diagnostic_command_is_full_pytest")),
            _check("command_is_not_retry_if_success", False, execution.get("diagnostic_command_is_retry")),
            _check("diagnostic_command_executed_true_if_success", True, execution.get("diagnostic_command_executed")),
            _check("targeted_pytest_performed_true_if_success", True, execution.get("targeted_pytest_performed")),
            _check("diagnostic_output_captured_true_if_success", True, execution.get("diagnostic_output_captured")),
            _check("exit_code_captured_if_success", True, isinstance(result.get("exit_code"), int)),
            _check("stdout_hash_captured_if_success", True, isinstance(result.get("stdout_sha256"), str) and len(result.get("stdout_sha256")) == 64),
            _check("stderr_hash_captured_if_success", True, isinstance(result.get("stderr_sha256"), str) and len(result.get("stderr_sha256")) == 64),
            _check("bounded_stdout_excerpt_captured_if_success", True, isinstance(execution.get("bounded_stdout_excerpt"), str)),
            _check("bounded_stderr_excerpt_captured_if_success", True, isinstance(execution.get("bounded_stderr_excerpt"), str)),
            _check("output_volume_recorded_if_success", result.get("stdout_byte_count", 0) + result.get("stderr_byte_count", 0), result.get("combined_output_byte_count")),
            _check("redaction_summary_recorded_if_success", True, isinstance(execution.get("redaction_summary"), Mapping)),
            _check("execution_duration_recorded_if_success", True, isinstance(result.get("duration_seconds"), str)),
            _check("payload_digest_generated_if_success", True, isinstance(execution.get(PAYLOAD_DIGEST_KEY), str) and len(execution.get(PAYLOAD_DIGEST_KEY)) == 64),
            _check("digest_manifest_digest_generated_if_success", True, isinstance(execution.get(DIGEST_MANIFEST_DIGEST_KEY), str) and len(execution.get(DIGEST_MANIFEST_DIGEST_KEY)) == 64),
        ])
    else:
        checks.extend([
            _check("blocked_reason_recorded_if_blocked", True, isinstance(execution.get("blocked_reason"), str) and bool(execution.get("blocked_reason"))),
            _check("blocked_manifest_digest_generated_if_blocked", True, isinstance(execution.get(BLOCKED_MANIFEST_DIGEST_KEY), str) and len(execution.get(BLOCKED_MANIFEST_DIGEST_KEY)) == 64),
        ])
    false_aliases = {
        "diagnostic_capture_results_review_created": "diagnostic_results_review_created_false",
        "diagnostic_results_review_created": "diagnostic_results_review_alias_created_false",
        "remediation_or_method_candidate_after_diagnostic_capture_created": "remediation_or_method_candidate_after_diagnostic_capture_created_false",
        "planning_reentry_rerun_performed": "planning_reentry_rerun_false",
        "detail_binding_reattempt_rerun_performed": "detail_binding_reattempt_rerun_false",
        "materialization_execution_rerun_performed": "materialization_execution_rerun_false",
        "source_recovery_rerun_performed": "source_recovery_rerun_false",
        "retry_rerun_performed": "retry_rerun_false", "full_pytest_performed": "full_pytest_false",
        "classification_execution_performed_in_execution": "classification_execution_false",
        "remediation_execution_performed": "remediation_execution_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "main_push_performed": "main_push_false", "origin_main_modified_by_this_task": "origin_main_modified_false",
        "provider_requests_made_in_execution": "provider_requests_false", "env_inspection_performed": "env_inspection_false",
        "market_data_acquisition_performed_in_execution": "market_data_acquisition_false",
        "dataset_generation_performed_in_execution": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    for field in CLOSED_FALSE_FIELDS:
        checks.append(_check(false_aliases.get(field, f"{field}_false"), False, execution.get(field)))
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, execution.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, execution.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, execution.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, execution.get("broker_execution")),
        _check("next_chain_defined", SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, execution.get("next_chain")),
        _check("next_gates_defined", SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES, execution.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, execution.get("risk_controls")),
        _check("no_tracked_marketflow_files", False, execution.get("marketflow_outputs_committed")),
        _check("no_tracked_pytest_cache_files", False, execution.get("pytest_cache_committed")),
    ])
    return checks


def _summary(execution: Mapping[str, Any]) -> dict[str, Any]:
    checklist = execution.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    fields = {field: execution.get(field) for field in SUCCESS_TRUE_FIELDS if field in execution}
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed, **fields,
        "targeted_diagnostic_output_capture_execution_created": True,
        "new_retry_candidate_created": False, "new_retry_executed": False,
        "integration_execution_successful": False, "priority_1_top_module_count": 5,
        "priority_1_total_nodeids": 612, "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "ready_for_targeted_diagnostic_output_capture_results_review": success,
        "ready_for_remediation_or_method_candidate_after_diagnostic_capture": False,
        "ready_for_retry_candidate": False,
        "recommended_next_task": execution.get("recommended_next_task"),
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
        **({"blocked_reason": execution.get("blocked_reason")} if not success else {}),
    }


def _validate_source_approval(value: Mapping[str, Any] | None) -> None:
    if value is None:
        return
    expected = {
        "artifact_kind": source.ARTIFACT_KIND, "approval_status": source.APPROVAL_STATUS,
        "approval_scope": source.APPROVAL_SCOPE, source.DIGEST_KEY: SOURCE_APPROVAL_DIGEST,
        "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "diagnostic_capture_package_authorized": True,
        "ready_for_targeted_diagnostic_output_capture_execution": True,
        "diagnostic_capture_execution_performed": False,
    }
    if not isinstance(value, Mapping) or any(value.get(field) != expected_value for field, expected_value in expected.items()):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("source approval mismatch")


def execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(
    *, source_approval: dict | None = None, run_timestamp_utc: str | None = None,
    command_runner: Callable[[Sequence[str], Path], Any] | None = None,
    diagnostic_working_directory: str | Path | None = None,
    python_executable: str | Path | None = None,
    max_stdout_excerpt_chars: int = 20000, max_stderr_excerpt_chars: int = 20000,
) -> dict:
    """Run the approved five-module command once, or return a fail-closed artifact."""

    run_timestamp = _utc_timestamp(run_timestamp_utc)
    try:
        _validate_source_approval(source_approval)
    except MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError as exc:
        return _build_blocked(run_timestamp, "SOURCE_APPROVAL_BOUNDARY_CHECK_FAILED", missing=[str(exc)])
    worktree = Path(diagnostic_working_directory) if diagnostic_working_directory is not None else APPROVED_WORKING_DIRECTORY
    executable = Path(python_executable) if python_executable is not None else APPROVED_PYTHON_EXECUTABLE
    argv = [str(executable), *APPROVED_ARGV[1:]]
    pre = _read_execution_environment(worktree, executable)
    errors = _precheck_errors(pre, worktree, executable, argv, max_stdout_excerpt_chars, max_stderr_excerpt_chars)
    if errors:
        return _build_blocked(run_timestamp, "PRE_EXECUTION_BOUNDARY_CHECK_FAILED", pre, errors)
    runner = command_runner or _default_command_runner
    started = time.perf_counter()
    try:
        raw_result = runner(tuple(argv), worktree)
        result = _normalise_runner_result(raw_result, time.perf_counter() - started)
    except Exception as exc:  # command/process boundary is converted to explicit blocked evidence
        return _build_blocked(run_timestamp, f"DIAGNOSTIC_COMMAND_EXECUTION_OR_CAPTURE_FAILED:{type(exc).__name__}", pre, [str(exc)])
    post = _read_execution_environment(worktree, executable)
    post_errors = _precheck_errors(post, worktree, executable, argv, max_stdout_excerpt_chars, max_stderr_excerpt_chars)
    if post_errors:
        return _build_blocked(run_timestamp, "POST_EXECUTION_BOUNDARY_CHECK_FAILED", post, post_errors)

    stdout_text = result["stdout"].decode("utf-8", errors="replace")
    stderr_text = result["stderr"].decode("utf-8", errors="replace")
    redacted_stdout, stdout_redacted, stdout_patterns = _redact(stdout_text)
    redacted_stderr, stderr_redacted, stderr_patterns = _redact(stderr_text)
    stdout_excerpt = redacted_stdout[:max_stdout_excerpt_chars]
    stderr_excerpt = redacted_stderr[:max_stderr_excerpt_chars]
    duration = result["duration_seconds"]
    end_timestamp = (datetime.fromisoformat(run_timestamp[:-1] + "+00:00") + timedelta(seconds=float(duration))).isoformat().replace("+00:00", "Z")
    execution = _base_execution(run_timestamp)
    execution.update({
        "artifact_kind": ARTIFACT_KIND_SUCCESS, "execution_status": EXECUTION_STATUS_SUCCESS,
        "created_offline": False, "governance_only": False,
        **{field: True for field in SUCCESS_TRUE_FIELDS},
        "diagnostic_command_record": {
            "command": APPROVED_COMMAND, "argv": list(argv), "cwd": str(worktree),
            "python_executable": str(executable), "target_modules": list(TARGET_MODULES),
            "start_timestamp_utc": run_timestamp, "end_timestamp_utc": end_timestamp,
            "pre_execution_checks": deepcopy(pre),
        },
        "diagnostic_target_modules": list(TARGET_MODULES),
        "diagnostic_execution_result": {
            "exit_code": result["exit_code"], "duration_seconds": duration,
            "stdout_sha256": hashlib.sha256(result["stdout"]).hexdigest(),
            "stderr_sha256": hashlib.sha256(result["stderr"]).hexdigest(),
            "stdout_byte_count": len(result["stdout"]), "stderr_byte_count": len(result["stderr"]),
            "combined_output_byte_count": len(result["stdout"]) + len(result["stderr"]),
            "stdout_excerpt_truncated": len(redacted_stdout) > max_stdout_excerpt_chars,
            "stderr_excerpt_truncated": len(redacted_stderr) > max_stderr_excerpt_chars,
        },
        "diagnostic_output_capture_summary": {
            "full_streams_stored": False, "full_stream_hashes_stored": True,
            "bounded_excerpts_stored": True, "maximum_stdout_excerpt_chars": max_stdout_excerpt_chars,
            "maximum_stderr_excerpt_chars": max_stderr_excerpt_chars,
            "nonzero_exit_code_is_diagnostic_evidence_only": result["exit_code"] != 0,
        },
        "bounded_stdout_excerpt": stdout_excerpt, "bounded_stderr_excerpt": stderr_excerpt,
        "redaction_summary": {
            "redaction_checked": True, "redaction_applied": stdout_redacted or stderr_redacted,
            "redaction_patterns_applied": sorted(set(stdout_patterns + stderr_patterns)),
            "available_redaction_pattern_ids": [item[0] for item in REDACTION_PATTERNS],
        },
        "post_execution_boundary_checks": deepcopy(post),
        "outputs": deepcopy(SUCCESS_OUTPUTS),
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RESULTS_REVIEW_V1",
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RESULTS_REVIEW",
        "ready_for_targeted_diagnostic_output_capture_results_review": True,
        "ready_for_remediation_or_method_candidate_after_diagnostic_capture": False,
        "ready_for_retry_candidate": False, "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
    })
    execution[PAYLOAD_DIGEST_KEY] = semantic_digest(_payload(execution))
    execution["digest_manifest"] = {
        "source_approval": SOURCE_APPROVAL_DIGEST,
        "source_operator_review": source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate": source.source.SOURCE_CANDIDATE_DIGEST,
        "diagnostic_payload": execution[PAYLOAD_DIGEST_KEY], "outputs": semantic_digest(SUCCESS_OUTPUTS),
        "risk_controls": semantic_digest(RISK_CONTROLS),
    }
    execution[DIGEST_MANIFEST_DIGEST_KEY] = semantic_digest(execution["digest_manifest"])
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    execution[EXECUTION_DIGEST_KEY] = _execution_digest(execution)
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(execution: dict) -> dict:
    """Validate either the successful diagnostic evidence or a blocked manifest."""

    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("execution must be an object")
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    expected_status = EXECUTION_STATUS_SUCCESS if success else EXECUTION_STATUS_BLOCKED
    expected_kind = ARTIFACT_KIND_SUCCESS if success else ARTIFACT_KIND_BLOCKED
    constants = {
        "artifact_kind": expected_kind, "execution_status": expected_status, "execution_scope": EXECUTION_SCOPE,
        "schema_version": SCHEMA_VERSION, "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "created_offline": not success, "governance_only": False, "diagnostic_capture_execution_only": True,
        "targeted_diagnostic_output_capture_execution_created": True, **SOURCE_BINDINGS,
        "retry_execution_commit": RETRY_EXECUTION_COMMIT, "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29, "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "priority_1_top_module_groups": source.source.source.TOP_MODULES,
        "diagnostic_command_is_retry": False, "diagnostic_command_is_full_pytest": False,
    }
    for field, expected in constants.items():
        if execution.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError(f"{field} mismatch")
    expected_counts = {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    if {key: execution.get("retry_failure_context", {}).get(key) for key in expected_counts} != expected_counts:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("retry failure counts mismatch")
    if any(execution.get(field) is not False for field in CLOSED_FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("closed boundary opened")
    if any(execution.get(field) != NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("runtime boundary changed")
    if execution.get("predictive_usefulness") != NOT_ACCEPTED or execution.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("acceptance boundary changed")
    if execution.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("risk controls mismatch")
    if success:
        if any(execution.get(field) is not True for field in SUCCESS_TRUE_FIELDS):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("successful execution fact missing")
        record, result = execution.get("diagnostic_command_record", {}), execution.get("diagnostic_execution_result", {})
        if record.get("argv") != list(EXPECTED_ARGV) or record.get("command") != APPROVED_COMMAND:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("approved command mismatch")
        if record.get("cwd") != str(APPROVED_WORKING_DIRECTORY) or record.get("python_executable") != str(APPROVED_PYTHON_EXECUTABLE):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("approved execution location mismatch")
        if record.get("target_modules") != TARGET_MODULES or execution.get("diagnostic_target_modules") != TARGET_MODULES:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("target modules mismatch")
        if not isinstance(result.get("exit_code"), int) or not isinstance(result.get("duration_seconds"), str):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("execution result incomplete")
        try:
            duration = float(result["duration_seconds"])
        except (TypeError, ValueError) as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("execution duration invalid") from exc
        if duration < 0:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("execution duration invalid")
        for field in ("stdout_sha256", "stderr_sha256"):
            if not isinstance(result.get(field), str) or re.fullmatch(r"[0-9a-f]{64}", result[field]) is None:
                raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError(f"{field} missing")
        if not isinstance(execution.get("bounded_stdout_excerpt"), str) or not isinstance(execution.get("bounded_stderr_excerpt"), str):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("bounded excerpts missing")
        counts = [result.get("stdout_byte_count"), result.get("stderr_byte_count"), result.get("combined_output_byte_count")]
        if any(not isinstance(count, int) or count < 0 for count in counts) or counts[0] + counts[1] != counts[2]:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("output byte counts invalid")
        capture = execution.get("diagnostic_output_capture_summary", {})
        stdout_limit = capture.get("maximum_stdout_excerpt_chars")
        stderr_limit = capture.get("maximum_stderr_excerpt_chars")
        if (
            not isinstance(stdout_limit, int) or not 0 < stdout_limit <= 20000
            or not isinstance(stderr_limit, int) or not 0 < stderr_limit <= 20000
            or len(execution["bounded_stdout_excerpt"]) > stdout_limit
            or len(execution["bounded_stderr_excerpt"]) > stderr_limit
            or not isinstance(result.get("stdout_excerpt_truncated"), bool)
            or not isinstance(result.get("stderr_excerpt_truncated"), bool)
        ):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("bounded output contract invalid")
        if not isinstance(execution.get("redaction_summary"), Mapping) or execution["redaction_summary"].get("redaction_checked") is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("redaction summary missing")
        if execution.get("outputs") != SUCCESS_OUTPUTS or execution.get("next_chain") != SUCCESS_NEXT_CHAIN or execution.get("next_gates") != SUCCESS_NEXT_GATES:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("success disposition mismatch")
        if execution.get(PAYLOAD_DIGEST_KEY) != semantic_digest(_payload(execution)):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("payload digest mismatch")
        expected_manifest = {
            "source_approval": SOURCE_APPROVAL_DIGEST, "source_operator_review": source.SOURCE_OPERATOR_REVIEW_DIGEST,
            "source_candidate": source.source.SOURCE_CANDIDATE_DIGEST,
            "diagnostic_payload": execution[PAYLOAD_DIGEST_KEY], "outputs": semantic_digest(SUCCESS_OUTPUTS),
            "risk_controls": semantic_digest(RISK_CONTROLS),
        }
        if execution.get("digest_manifest") != expected_manifest or execution.get(DIGEST_MANIFEST_DIGEST_KEY) != semantic_digest(expected_manifest):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("digest manifest mismatch")
    else:
        for field in ("targeted_diagnostic_output_capture_execution_performed", "diagnostic_capture_execution_performed", "diagnostic_command_executed", "diagnostic_output_captured", "targeted_pytest_performed"):
            if execution.get(field) is not False:
                raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("blocked artifact claims execution")
        if not isinstance(execution.get("blocked_reason"), str) or not execution["blocked_reason"]:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("blocked reason missing")
        if execution.get("next_chain") != BLOCKED_NEXT_CHAIN or execution.get("next_gates") != BLOCKED_NEXT_GATES:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("blocked disposition mismatch")
        if execution.get(BLOCKED_MANIFEST_DIGEST_KEY) != _blocked_manifest_digest(execution):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("blocked manifest digest mismatch")
    checklist = _checklist(execution)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("checklist mismatch")
    if execution.get("summary") != _summary(execution):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("summary mismatch")
    digest = execution.get(EXECUTION_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _execution_digest(execution):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError("execution digest mismatch")
    return {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"], "execution_digest": digest,
        **{field: execution["summary"][field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_markdown_v1(execution: dict) -> str:
    """Render validated success or blocked execution evidence as Markdown."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1(execution)
    success = execution["artifact_kind"] == ARTIFACT_KIND_SUCCESS
    sections = [
        ("Source Approval", [SOURCE_APPROVAL_DIGEST]),
        ("Source Operator Review and Candidate", [source.SOURCE_OPERATOR_REVIEW_DIGEST, source.source.SOURCE_CANDIDATE_DIGEST]),
        ("Source Remediation or Method Results Review", [source.SOURCE_BINDINGS["source_results_review_digest"]]),
        ("Source Planning Reentry with Complete Detail", [source.SOURCE_BINDINGS["source_planning_execution_digest"]]),
        ("Source Detail Binding Results Review", [source.SOURCE_BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; still authoritative."]),
        ("Execution Scope", [EXECUTION_SCOPE]),
        ("Approved Priority 1 Target Modules", TARGET_MODULES),
        ("Approved Diagnostic Command", [APPROVED_COMMAND]),
        ("Pre-Execution Checks", [str(execution.get("diagnostic_command_record", {}).get("pre_execution_checks", execution.get("available_data", {}).get("completed_precheck_facts", {})))]),
        ("Diagnostic Capture Result", [execution["execution_status"], str(execution.get("diagnostic_execution_result", execution.get("blocked_reason")))]),
        ("Diagnostic Output Capture Summary", [str(execution.get("diagnostic_output_capture_summary", "not captured"))]),
        ("Bounded Output Excerpts", [execution.get("bounded_stdout_excerpt", "not captured"), execution.get("bounded_stderr_excerpt", "not captured")]),
        ("Redaction Summary", [str(execution.get("redaction_summary", "not captured"))]),
        ("Unsupported Claims Boundary", ["No root-cause, remediation, retry-success, or merge-readiness claim is made."]),
        ("Success or Blocked Disposition", ["SUCCESS" if success else "BLOCKED"]),
        ("Recommendation", [execution["recommended_next_task"]]),
        ("Next Chain", execution["next_chain"]), ("Next Gates", execution["next_gates"]),
        ("Risk Controls", execution["risk_controls"]),
        ("Authority Boundaries", ["Diagnostic evidence only; no retry, main, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["No provider, evidence regeneration, full pytest, retry rerun, cache read, remediation, or classification."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Execution v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTED_V1 = ARTIFACT_KIND_SUCCESS
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_BLOCKED_V1 = ARTIFACT_KIND_BLOCKED
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTED_PRIORITY_1_DIAGNOSTIC_OUTPUT_CAPTURED = EXECUTION_STATUS_SUCCESS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_BLOCKED_COMMAND_UNAVAILABLE_OR_BOUNDARY_FAILURE = EXECUTION_STATUS_BLOCKED
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_ONLY_DIAGNOSTIC_OUTPUT_CAPTURE_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS = SELECTED_PACKAGE

__all__ = [
    "ARTIFACT_KIND_SUCCESS", "ARTIFACT_KIND_BLOCKED", "EXECUTION_STATUS_SUCCESS", "EXECUTION_STATUS_BLOCKED",
    "EXECUTION_SCOPE", "SELECTED_PACKAGE", "SOURCE_APPROVAL_DIGEST", "APPROVED_COMMAND", "APPROVED_ARGV",
    "APPROVED_WORKING_DIRECTORY", "APPROVED_PYTHON_EXECUTABLE", "TARGET_MODULES", "SOURCE_BINDINGS",
    "SUCCESS_OUTPUTS", "SUCCESS_NEXT_CHAIN", "BLOCKED_NEXT_CHAIN", "SUCCESS_NEXT_GATES", "BLOCKED_NEXT_GATES",
    "RISK_CONTROLS", "SUCCESS_TRUE_FIELDS", "CLOSED_FALSE_FIELDS", "EXECUTION_DIGEST_KEY", "PAYLOAD_DIGEST_KEY",
    "DIGEST_MANIFEST_DIGEST_KEY", "BLOCKED_MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTED_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_BLOCKED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTED_PRIORITY_1_DIAGNOSTIC_OUTPUT_CAPTURED",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_BLOCKED_COMMAND_UNAVAILABLE_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_ONLY_DIAGNOSTIC_OUTPUT_CAPTURE_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionError",
    "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_markdown_v1",
]
