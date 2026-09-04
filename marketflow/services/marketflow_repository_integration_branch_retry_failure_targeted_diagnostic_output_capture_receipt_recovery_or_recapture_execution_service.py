"""Execute the approved single diagnostic recapture with a durable receipt."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from typing import Any, Callable, Mapping, Sequence

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_service
    as prior_execution,
)
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_service
    as source,
)


ARTIFACT_KIND_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTED_V1"
ARTIFACT_KIND_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_BLOCKED_V1"
EXECUTION_STATUS_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTED_CONTROLLED_SINGLE_RECAPTURE_RECEIPT_FINALIZED"
EXECUTION_STATUS_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_BLOCKED_RECEIPT_OR_RECAPTURE_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_ONLY_CONTROLLED_RECAPTURE_DIAGNOSTIC_OUTPUT_CAPTURE_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
SOURCE_APPROVAL_DIGEST = "e745e07163a3bc0535b039e94433da59fb4f405558f13d69aaacfce848cf3cf9"
EXPECTED_ORIGIN_MAIN = prior_execution.EXPECTED_ORIGIN_MAIN
INTEGRATION_BRANCH = prior_execution.INTEGRATION_BRANCH
INTEGRATION_HEAD = prior_execution.INTEGRATION_HEAD
RETRY_EXECUTION_COMMIT = prior_execution.RETRY_EXECUTION_COMMIT
EXPECTED_REPO_ROOT = Path(__file__).resolve().parents[2]
APPROVED_WORKING_DIRECTORY = prior_execution.APPROVED_WORKING_DIRECTORY
APPROVED_PYTHON_EXECUTABLE = prior_execution.APPROVED_PYTHON_EXECUTABLE
TARGET_MODULES = list(prior_execution.TARGET_MODULES)
APPROVED_ARGV = list(prior_execution.APPROVED_ARGV)
APPROVED_COMMAND = prior_execution.APPROVED_COMMAND
EXPECTED_ARGV = tuple(APPROVED_ARGV)
DEFAULT_RECEIPT_FILENAME = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_RECEIPT_V1.json"

EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_digest"
PAYLOAD_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_payload_digest"
RECEIPT_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_receipt_digest"
DIGEST_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_digest_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_blocked_manifest_digest"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

SOURCE_BINDINGS = {
    "source_receipt_recovery_or_recapture_approval_digest": SOURCE_APPROVAL_DIGEST,
    **deepcopy(source.SOURCE_BINDINGS),
}

SUCCESS_OUTPUT_IDS = [
    "receipt_recovery_or_recapture_execution_manifest", "durable_receipt_scaffold_record",
    "durable_receipt_finalization_record", "controlled_recapture_command_record",
    "priority_1_target_module_execution_record", "controlled_recapture_exit_code_report",
    "controlled_recapture_stdout_hash_report", "controlled_recapture_stderr_hash_report",
    "bounded_stdout_excerpt_report", "bounded_stderr_excerpt_report",
    "controlled_recapture_output_volume_report", "controlled_recapture_redaction_summary",
    "controlled_recapture_cache_write_control_report", "controlled_recapture_results_review_enablement_report",
    "retry_gate_preservation_report", "unsupported_claims_boundary_report", "digest_manifest",
]
SUCCESS_OUTPUTS = [{"output_id": item, "status": "GENERATED_DIAGNOSTIC_EVIDENCE_ONLY"} for item in SUCCESS_OUTPUT_IDS]
SUCCESS_NEXT_CHAIN = [
    "Receipt Recovery or Controlled Recapture Results Review v1.",
    "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1, if supported by results review.",
    "Remediation or Method Operator Review v1, if needed.", "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.", "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Receipt Recovery or Controlled Recapture Execution Failure Diagnosis v1.",
    "Alternate receipt recovery or controlled recapture candidate, if needed.",
    "No remediation/method candidate, retry, or main merge.",
]
SUCCESS_NEXT_GATES = [
    "receipt_recovery_or_controlled_recapture_results_review",
    "retry_failure_remediation_or_method_candidate_after_diagnostic_capture_if_supported",
    "remediation_or_method_operator_review_if_needed", "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved", "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "receipt_recovery_or_controlled_recapture_execution_failure_diagnosis",
    "alternate_receipt_recovery_or_recapture_candidate_if_needed",
    "remediation_or_method_candidate_blocked_until_recapture_results_review_passes",
    "new_retry_blocked_until_remediation_or_method_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]
RISK_CONTROLS = [
    "controlled_recapture_execution_uses_approved_package_only",
    "controlled_recapture_execution_prewrites_durable_receipt_scaffold",
    "controlled_recapture_execution_finalizes_durable_receipt_after_command",
    "controlled_recapture_execution_receipt_survives_print_wrapper_failure",
    "controlled_recapture_execution_targets_priority_1_modules_only",
    "controlled_recapture_execution_uses_detached_worktree_cwd",
    "controlled_recapture_execution_uses_approved_python_executable",
    "controlled_recapture_execution_uses_cacheprovider_disabled",
    "controlled_recapture_execution_records_command_cwd_exit_stdout_stderr_duration",
    "controlled_recapture_execution_bounds_output_volume",
    "controlled_recapture_execution_hashes_full_output_streams",
    "controlled_recapture_execution_redacts_secret_like_patterns",
    "controlled_recapture_execution_does_not_inspect_env",
    "controlled_recapture_execution_does_not_read_pytest_cache",
    "controlled_recapture_execution_does_not_commit_pytest_cache",
    "controlled_recapture_execution_does_not_commit_marketflow_outputs",
    "controlled_recapture_execution_does_not_search_transient_memory",
    "controlled_recapture_execution_does_not_parse_terminal_logs",
    "controlled_recapture_execution_does_not_parse_operator_logs",
    "controlled_recapture_execution_does_not_reconstruct_prior_missing_values",
    "controlled_recapture_execution_does_not_rerun_planning",
    "controlled_recapture_execution_does_not_rerun_detail_binding",
    "controlled_recapture_execution_does_not_rerun_materialization",
    "controlled_recapture_execution_does_not_rerun_source_recovery",
    "controlled_recapture_execution_does_not_execute_remediation",
    "controlled_recapture_execution_does_not_execute_classification",
    "controlled_recapture_execution_does_not_classify_modules_again",
    "controlled_recapture_execution_does_not_identify_first_failure",
    "controlled_recapture_execution_does_not_identify_first_error",
    "controlled_recapture_execution_does_not_claim_traceback_root_cause",
    "controlled_recapture_execution_does_not_recommend_direct_code_remediation",
    "controlled_recapture_execution_does_not_create_diagnostic_results_review",
    "controlled_recapture_execution_does_not_create_remediation_or_method_candidate",
    "controlled_recapture_execution_does_not_create_new_retry_candidate",
    "controlled_recapture_execution_does_not_create_retry_results_review",
    "controlled_recapture_execution_does_not_create_integration_results_review",
    "controlled_recapture_execution_does_not_mark_integration_successful",
    "controlled_recapture_execution_does_not_generate_successful_integration_digest",
    "controlled_recapture_execution_does_not_treat_recapture_as_retry",
    "controlled_recapture_execution_does_not_treat_recapture_exit_code_as_retry_result",
    "controlled_recapture_execution_does_not_push_integration_branch",
    "controlled_recapture_execution_does_not_push_main",
    "controlled_recapture_execution_does_not_delete_integration_branch",
    "controlled_recapture_execution_does_not_delete_worktree",
    "controlled_recapture_execution_does_not_force_push",
    "controlled_recapture_execution_does_not_prune_remotes",
    "controlled_recapture_execution_does_not_modify_tags",
    "controlled_recapture_execution_does_not_modify_staged_evidence",
    "controlled_recapture_execution_does_not_regenerate_evidence",
    "controlled_recapture_execution_does_not_call_providers",
    "controlled_recapture_execution_does_not_acquire_market_data",
    "controlled_recapture_execution_does_not_regenerate_dataset",
    "controlled_recapture_execution_does_not_recompute_metrics",
    "controlled_recapture_execution_does_not_train_models",
    "controlled_recapture_execution_does_not_score_strategy",
    "controlled_recapture_execution_does_not_generate_recommendations",
    "controlled_recapture_execution_does_not_accept_predictive_usefulness",
    "controlled_recapture_execution_does_not_accept_profitability",
    "controlled_recapture_execution_does_not_authorize_runtime",
    "controlled_recapture_execution_does_not_authorize_broker_execution",
    "controlled_recapture_output_is_diagnostic_evidence_only",
    "future_recapture_results_review_required_before_remediation_or_method_candidate",
    "future_recapture_is_not_retry_success", "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation", "previous_approval_remains_source_evidence",
    "previous_operator_review_remains_source_evidence", "previous_candidate_remains_source_evidence",
    "previous_failure_diagnosis_remains_source_evidence",
    "previous_blocked_execution_remains_historically_blocked",
    "first_diagnostic_command_run_acknowledged_but_not_accepted_as_durable_success",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_results_review_required_after_controlled_recapture",
    "separate_remediation_or_method_candidate_required_after_recapture_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

SUCCESS_TRUE_FIELDS = [
    "receipt_recovery_or_recapture_execution_created", "receipt_recovery_or_recapture_execution_performed",
    "controlled_recapture_execution_performed", "durable_receipt_scaffold_prewritten",
    "durable_receipt_finalized", "durable_receipt_retained", "durable_receipt_survives_reporting_wrapper_failure",
    "diagnostic_command_executed_in_execution", "diagnostic_output_captured_in_execution",
    "diagnostic_method_executed", "targeted_pytest_performed", "approved_priority_1_modules_targeted",
    "only_priority_1_modules_targeted", "controlled_recapture_command_used_cacheprovider_disabled",
    "controlled_recapture_command_used_approved_python", "controlled_recapture_command_used_detached_worktree_cwd",
    "controlled_recapture_command_exit_code_captured", "controlled_recapture_stdout_captured",
    "controlled_recapture_stderr_captured", "controlled_recapture_output_bounded",
    "controlled_recapture_output_hashed", "controlled_recapture_redaction_checked",
    "ready_for_receipt_recovery_or_recapture_results_review",
]
CLOSED_FALSE_FIELDS = [
    "receipt_recovery_execution_performed", "receipt_recovered", "controlled_recapture_command_is_retry",
    "controlled_recapture_command_is_full_pytest", "diagnostic_results_review_created",
    "remediation_or_method_candidate_after_diagnostic_capture_created", "new_retry_candidate_created",
    "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "cache_read_in_execution", "cache_modified_intentionally_in_execution", "cache_committed",
    "pytest_cache_committed", "marketflow_outputs_committed", "operator_logs_parsed", "terminal_logs_parsed",
    "env_inspection_performed", "unavailable_prior_values_reconstructed", "unavailable_prior_values_inferred",
    "planning_reentry_rerun_performed", "detail_binding_reattempt_rerun_performed",
    "materialization_execution_rerun_performed", "source_recovery_rerun_performed",
    "module_grouping_recovered_in_execution", "classification_execution_performed_in_execution",
    "remediation_execution_performed", "failure_modules_classified", "error_modules_classified",
    "failure_error_separation_claimed", "first_failure_identified", "first_error_identified",
    "first_order_claim_made", "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "retry_rerun_performed", "full_pytest_performed", "retry_success_claimed", "main_merge_readiness_claimed",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "evidence_regenerated", "provider_requests_made_in_execution",
    "market_data_acquisition_performed_in_execution", "dataset_generation_performed_in_execution",
    "metric_recomputation_from_raw_rows_performed", "model_training_performed", "strategy_scoring_performed",
    "trade_recommendations_generated", "ready_for_diagnostic_results_review",
    "ready_for_remediation_or_method_candidate", "ready_for_retry_candidate",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError(ValueError):
    """Raised when recapture evidence violates its approved boundary."""


def _utc_timestamp(value: str | None) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if not isinstance(value, str) or not value.endswith("Z"):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError("UTC run timestamp required")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError("UTC run timestamp required") from exc
    if parsed.utcoffset() != timedelta(0):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError("UTC run timestamp required")
    return value


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _persist_json(path: Path, payload: Mapping[str, Any], *, exclusive: bool = False) -> None:
    """Persist canonical JSON and fsync before returning."""

    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "xb" if exclusive else "wb"
    with path.open(mode) as handle:
        handle.write(canonical_json_bytes(dict(payload)))
        handle.flush()
        os.fsync(handle.fileno())


def _receipt_digest(receipt: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(receipt))
    for field in (RECEIPT_DIGEST_KEY, PAYLOAD_DIGEST_KEY, DIGEST_MANIFEST_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _payload(execution: Mapping[str, Any]) -> dict[str, Any]:
    payload = {field: deepcopy(execution.get(field)) for field in (
        "controlled_recapture_command_record", "controlled_recapture_target_modules", "durable_receipt_record",
        "controlled_recapture_execution_result", "controlled_recapture_output_capture_summary",
        "bounded_stdout_excerpt", "bounded_stderr_excerpt", "redaction_summary", "post_execution_boundary_checks",
    )}
    receipt = payload.get("durable_receipt_record")
    if isinstance(receipt, dict):
        receipt.pop(PAYLOAD_DIGEST_KEY, None)
        receipt.pop(DIGEST_MANIFEST_DIGEST_KEY, None)
    return payload


def _execution_digest(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for field in ("checklist", "summary", EXECUTION_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _blocked_manifest_digest(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for field in ("checklist", "summary", EXECUTION_DIGEST_KEY, BLOCKED_MANIFEST_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _read_environment(worktree: Path, executable: Path) -> dict[str, Any]:
    return prior_execution._read_execution_environment(worktree, executable)


def _precheck_errors(
    state: Mapping[str, Any], worktree: Path, executable: Path, argv: Sequence[str],
    receipt_path: Path, max_stdout: int, max_stderr: int,
) -> list[str]:
    receipt_in_docs_status = tuple(part.lower() for part in receipt_path.parent.parts[-2:]) == ("docs", "status")
    checks = {
        "detached_worktree_missing": state.get("worktree_exists") is True,
        "detached_worktree_head_mismatch": state.get("worktree_head") == INTEGRATION_HEAD,
        "detached_worktree_not_detached": state.get("worktree_is_detached") is True,
        "detached_worktree_not_clean": state.get("worktree_clean") is True,
        "approved_python_missing": state.get("python_executable_exists") is True,
        "target_module_missing": all(state.get("target_module_presence", {}).get(target) is True for target in TARGET_MODULES),
        "wrong_diagnostic_working_directory": worktree.resolve(strict=False) == APPROVED_WORKING_DIRECTORY.resolve(strict=False),
        "wrong_python_executable": executable.resolve(strict=False) == APPROVED_PYTHON_EXECUTABLE.resolve(strict=False),
        "wrong_or_extra_target_module": tuple(argv) == EXPECTED_ARGV,
        "cacheprovider_not_disabled": "-p" in argv and "no:cacheprovider" in argv,
        "full_pytest_boundary_failure": list(argv)[-len(TARGET_MODULES):] == TARGET_MODULES,
        "retry_command_boundary_failure": list(argv) != [str(APPROVED_PYTHON_EXECUTABLE), "-m", "pytest", "-q"],
        "receipt_path_not_docs_status": receipt_in_docs_status,
        "receipt_already_exists": not receipt_path.exists(),
        "origin_main_changed": state.get("origin_main") == EXPECTED_ORIGIN_MAIN,
        "integration_branch_head_changed": state.get("integration_branch_head") == INTEGRATION_HEAD,
        "remote_integration_branch_present": state.get("remote_integration_branch_exists") is False,
        "tracked_marketflow_present": state.get("root_tracked_marketflow_count") == 0 and state.get("worktree_tracked_marketflow_count") == 0,
        "tracked_pytest_cache_present": state.get("root_tracked_pytest_cache_count") == 0 and state.get("worktree_tracked_pytest_cache_count") == 0,
        "invalid_stdout_bound": isinstance(max_stdout, int) and 0 < max_stdout <= 20000,
        "invalid_stderr_bound": isinstance(max_stderr, int) and 0 < max_stderr <= 20000,
    }
    return [reason for reason, passed in checks.items() if not passed]


def _postcheck_errors(state: Mapping[str, Any]) -> list[str]:
    checks = {
        "detached_worktree_head_changed": state.get("worktree_head") == INTEGRATION_HEAD,
        "detached_worktree_not_detached": state.get("worktree_is_detached") is True,
        "detached_worktree_not_clean": state.get("worktree_clean") is True,
        "origin_main_changed": state.get("origin_main") == EXPECTED_ORIGIN_MAIN,
        "integration_branch_head_changed": state.get("integration_branch_head") == INTEGRATION_HEAD,
        "remote_integration_branch_present": state.get("remote_integration_branch_exists") is False,
        "tracked_marketflow_present": state.get("root_tracked_marketflow_count") == 0 and state.get("worktree_tracked_marketflow_count") == 0,
        "tracked_pytest_cache_present": state.get("root_tracked_pytest_cache_count") == 0 and state.get("worktree_tracked_pytest_cache_count") == 0,
    }
    return [reason for reason, passed in checks.items() if not passed]


def _default_command_runner(argv: Sequence[str], cwd: Path) -> dict[str, Any]:
    started = time.perf_counter()
    completed = subprocess.run(list(argv), cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, shell=False)
    return {"exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr, "duration_seconds": f"{time.perf_counter() - started:.6f}"}


def _base_execution(run_timestamp: str) -> dict[str, Any]:
    execution: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        "controlled_recapture_execution_only": True, "run_timestamp_utc": run_timestamp,
        **deepcopy(SOURCE_BINDINGS), "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {
            "passed": 24877, "failed": 1292, "errors": 112, "skipped": 7,
            "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True,
            "root_full_regression_is_retry_evidence": False,
        },
        "diagnostic_command_executed_once": True, "transient_success_artifact_returned": True,
        "durable_success_receipt_retained": False,
        "unavailable_diagnostic_payload_fields": list(source.source.source.UNAVAILABLE_FIELDS),
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "priority_1_top_module_groups": deepcopy(source.source.source.PRIORITY_1_TARGET_MODULES),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "risk_controls": list(RISK_CONTROLS),
    }
    execution.update({field: False for field in CLOSED_FALSE_FIELDS})
    return execution


def _build_blocked(
    run_timestamp: str, reason: str, *, state: Mapping[str, Any] | None = None,
    missing: Sequence[str] = (), receipt_path: Path | None = None,
    scaffold_prewritten: bool = False, command_executed: bool = False,
    output_captured: bool = False, targeted_pytest_performed: bool = False,
    retained_receipt: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    execution = _base_execution(run_timestamp)
    execution.update({
        "artifact_kind": ARTIFACT_KIND_BLOCKED, "execution_status": EXECUTION_STATUS_BLOCKED,
        "created_offline": not command_executed, "governance_only": False,
        "receipt_recovery_or_recapture_execution_created": True,
        "receipt_recovery_or_recapture_execution_performed": command_executed,
        "controlled_recapture_execution_performed": command_executed,
        "durable_receipt_scaffold_prewritten": scaffold_prewritten,
        "durable_receipt_finalized": False, "durable_receipt_retained": scaffold_prewritten and receipt_path is not None and receipt_path.exists(),
        "durable_receipt_survives_reporting_wrapper_failure": scaffold_prewritten,
        "diagnostic_command_executed_in_execution": command_executed,
        "diagnostic_output_captured_in_execution": output_captured,
        "diagnostic_method_executed": command_executed, "targeted_pytest_performed": targeted_pytest_performed,
        "approved_priority_1_modules_targeted": command_executed, "only_priority_1_modules_targeted": command_executed,
        "controlled_recapture_command_used_cacheprovider_disabled": command_executed,
        "controlled_recapture_command_used_approved_python": command_executed,
        "controlled_recapture_command_used_detached_worktree_cwd": command_executed,
        "controlled_recapture_command_exit_code_captured": False, "controlled_recapture_stdout_captured": output_captured,
        "controlled_recapture_stderr_captured": output_captured, "controlled_recapture_output_bounded": False,
        "controlled_recapture_output_hashed": False, "controlled_recapture_redaction_checked": False,
        "blocked_reason": reason,
        "durable_receipt_path": str(receipt_path) if receipt_path is not None else None,
        "durable_receipt_record": deepcopy(dict(retained_receipt or {})),
        "available_data": {
            "source_approval_digest": SOURCE_APPROVAL_DIGEST, "selected_package": SELECTED_PACKAGE,
            "planned_command": APPROVED_COMMAND, "planned_cwd": str(APPROVED_WORKING_DIRECTORY),
            "planned_target_modules": list(TARGET_MODULES), "durable_receipt_scaffold_path": str(receipt_path) if receipt_path else None,
            "completed_precheck_facts": deepcopy(dict(state or {})),
        },
        "missing_data": list(missing), "outputs": [],
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_FAILURE_DIAGNOSIS_V1",
        "recommended_next_task_status": "FUTURE_FAILURE_DIAGNOSIS_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_EXECUTION_FAILURE_DIAGNOSIS",
        "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(BLOCKED_NEXT_GATES),
    })
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = _blocked_manifest_digest(execution)
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    execution[EXECUTION_DIGEST_KEY] = _execution_digest(execution)
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(execution)
    return execution


def _validate_source_approval(value: Mapping[str, Any] | None) -> None:
    if value is None:
        return
    expected = {
        "artifact_kind": source.ARTIFACT_KIND, "approval_status": source.APPROVAL_STATUS,
        "approval_scope": source.APPROVAL_SCOPE, source.DIGEST_KEY: SOURCE_APPROVAL_DIGEST,
        "selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        "ready_for_receipt_recovery_or_recapture_execution": True,
        "ready_for_controlled_recapture_execution": True,
        "controlled_recapture_execution_performed": False,
    }
    if not isinstance(value, Mapping) or any(value.get(field) != expected_value for field, expected_value in expected.items()):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError("source approval mismatch")


def _scaffold(run_timestamp: str, receipt_path: Path, pre: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_RECEIPT_V1",
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        **deepcopy(SOURCE_BINDINGS), "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_failure_counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "approved_command": APPROVED_COMMAND, "approved_command_argv": list(APPROVED_ARGV),
        "approved_cwd": str(APPROVED_WORKING_DIRECTORY), "approved_python_executable": str(APPROVED_PYTHON_EXECUTABLE),
        "approved_target_modules": list(TARGET_MODULES), "receipt_path": str(receipt_path),
        "receipt_scaffold_timestamp_utc": run_timestamp, "receipt_status": "PREWRITTEN_BEFORE_COMMAND",
        "command_executed": False, "receipt_finalized": False,
        "pre_execution_checks": deepcopy(dict(pre)),
        "prior_unavailable_values_reconstructed": False, "prior_unavailable_values_inferred": False,
    }


def execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
    *, source_approval: dict | None = None, run_timestamp_utc: str | None = None,
    command_runner: Callable[[Sequence[str], Path], Any] | None = None,
    diagnostic_working_directory: str | Path | None = None,
    python_executable: str | Path | None = None,
    durable_receipt_path: str | Path | None = None,
    max_stdout_excerpt_chars: int = 20000, max_stderr_excerpt_chars: int = 20000,
) -> dict:
    """Run the approved command once after fsyncing its receipt scaffold."""

    run_timestamp = _utc_timestamp(run_timestamp_utc)
    receipt_path = Path(durable_receipt_path) if durable_receipt_path is not None else EXPECTED_REPO_ROOT / "docs" / "status" / DEFAULT_RECEIPT_FILENAME
    try:
        _validate_source_approval(source_approval)
    except MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError as exc:
        return _build_blocked(run_timestamp, "SOURCE_APPROVAL_BOUNDARY_CHECK_FAILED", missing=[str(exc)], receipt_path=receipt_path)
    worktree = Path(diagnostic_working_directory) if diagnostic_working_directory is not None else APPROVED_WORKING_DIRECTORY
    executable = Path(python_executable) if python_executable is not None else APPROVED_PYTHON_EXECUTABLE
    argv = [str(executable), *APPROVED_ARGV[1:]]
    pre = _read_environment(worktree, executable)
    errors = _precheck_errors(pre, worktree, executable, argv, receipt_path, max_stdout_excerpt_chars, max_stderr_excerpt_chars)
    if errors:
        return _build_blocked(run_timestamp, "PRE_EXECUTION_BOUNDARY_CHECK_FAILED", state=pre, missing=errors, receipt_path=receipt_path)

    scaffold = _scaffold(run_timestamp, receipt_path, pre)
    try:
        _persist_json(receipt_path, scaffold, exclusive=True)
    except (OSError, TypeError, ValueError) as exc:
        return _build_blocked(run_timestamp, "DURABLE_RECEIPT_SCAFFOLD_PREWRITE_FAILED", state=pre, missing=[type(exc).__name__], receipt_path=receipt_path)

    runner = command_runner or _default_command_runner
    started = time.perf_counter()
    try:
        raw_result = runner(tuple(argv), worktree)
        result = prior_execution._normalise_runner_result(raw_result, time.perf_counter() - started)
    except Exception as exc:  # process boundary becomes explicit blocked evidence; the command is never retried
        return _build_blocked(
            run_timestamp, f"CONTROLLED_RECAPTURE_COMMAND_EXECUTION_OR_CAPTURE_FAILED:{type(exc).__name__}",
            state=pre, missing=[str(exc)], receipt_path=receipt_path, scaffold_prewritten=True, retained_receipt=scaffold,
        )

    stdout_text = result["stdout"].decode("utf-8", errors="replace")
    stderr_text = result["stderr"].decode("utf-8", errors="replace")
    redacted_stdout, stdout_redacted, stdout_patterns = prior_execution._redact(stdout_text)
    redacted_stderr, stderr_redacted, stderr_patterns = prior_execution._redact(stderr_text)
    stdout_excerpt = redacted_stdout[:max_stdout_excerpt_chars]
    stderr_excerpt = redacted_stderr[:max_stderr_excerpt_chars]
    duration = result["duration_seconds"]
    end_timestamp = (datetime.fromisoformat(run_timestamp[:-1] + "+00:00") + timedelta(seconds=float(duration))).isoformat().replace("+00:00", "Z")
    post = _read_environment(worktree, executable)
    post_errors = _postcheck_errors(post)

    result_record = {
        "exit_code": result["exit_code"], "duration_seconds": duration,
        "stdout_sha256": hashlib.sha256(result["stdout"]).hexdigest(),
        "stderr_sha256": hashlib.sha256(result["stderr"]).hexdigest(),
        "stdout_byte_count": len(result["stdout"]), "stderr_byte_count": len(result["stderr"]),
        "combined_output_byte_count": len(result["stdout"]) + len(result["stderr"]),
        "stdout_excerpt_truncated": len(redacted_stdout) > max_stdout_excerpt_chars,
        "stderr_excerpt_truncated": len(redacted_stderr) > max_stderr_excerpt_chars,
    }
    redaction = {
        "redaction_checked": True, "redaction_applied": stdout_redacted or stderr_redacted,
        "redaction_patterns_applied": sorted(set(stdout_patterns + stderr_patterns)),
        "available_redaction_pattern_ids": [item[0] for item in prior_execution.REDACTION_PATTERNS],
    }
    final_receipt = {
        **scaffold, "receipt_status": "FINALIZED_AFTER_COMMAND" if not post_errors else "BLOCKED_AFTER_COMMAND_BOUNDARY_FAILURE",
        "command_executed": True, "receipt_finalized": not post_errors,
        "command_end_timestamp_utc": end_timestamp, "controlled_recapture_execution_result": deepcopy(result_record),
        "bounded_stdout_excerpt": stdout_excerpt, "bounded_stderr_excerpt": stderr_excerpt,
        "redaction_summary": deepcopy(redaction), "post_execution_boundary_checks": deepcopy(post),
        "post_execution_boundary_errors": list(post_errors),
    }
    final_receipt[RECEIPT_DIGEST_KEY] = _receipt_digest(final_receipt)
    try:
        _persist_json(receipt_path, final_receipt)
    except (OSError, TypeError, ValueError) as exc:
        return _build_blocked(
            run_timestamp, "DURABLE_RECEIPT_FINALIZATION_FAILED", state=post, missing=[type(exc).__name__],
            receipt_path=receipt_path, scaffold_prewritten=True, command_executed=True, output_captured=True,
            targeted_pytest_performed=True, retained_receipt=scaffold,
        )
    if post_errors:
        return _build_blocked(
            run_timestamp, "POST_EXECUTION_BOUNDARY_CHECK_FAILED", state=post, missing=post_errors,
            receipt_path=receipt_path, scaffold_prewritten=True, command_executed=True, output_captured=True,
            targeted_pytest_performed=True, retained_receipt=final_receipt,
        )

    execution = _base_execution(run_timestamp)
    execution.update({
        "artifact_kind": ARTIFACT_KIND_SUCCESS, "execution_status": EXECUTION_STATUS_SUCCESS,
        "created_offline": False, "governance_only": False, **{field: True for field in SUCCESS_TRUE_FIELDS},
        "durable_receipt_path": str(receipt_path),
        "controlled_recapture_command_record": {
            "command": APPROVED_COMMAND, "argv": list(argv), "cwd": str(worktree),
            "python_executable": str(executable), "target_modules": list(TARGET_MODULES),
            "start_timestamp_utc": run_timestamp, "end_timestamp_utc": end_timestamp,
            "pre_execution_checks": deepcopy(pre),
        },
        "controlled_recapture_target_modules": list(TARGET_MODULES),
        "durable_receipt_record": deepcopy(final_receipt),
        "controlled_recapture_execution_result": result_record,
        "controlled_recapture_output_capture_summary": {
            "full_streams_stored": False, "full_stream_hashes_stored": True, "bounded_excerpts_stored": True,
            "maximum_stdout_excerpt_chars": max_stdout_excerpt_chars,
            "maximum_stderr_excerpt_chars": max_stderr_excerpt_chars,
            "nonzero_exit_code_is_diagnostic_evidence_only": result["exit_code"] != 0,
        },
        "bounded_stdout_excerpt": stdout_excerpt, "bounded_stderr_excerpt": stderr_excerpt,
        "redaction_summary": redaction, "post_execution_boundary_checks": deepcopy(post),
        "outputs": deepcopy(SUCCESS_OUTPUTS),
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_V1",
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_RESULTS_REVIEW",
        "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
        RECEIPT_DIGEST_KEY: final_receipt[RECEIPT_DIGEST_KEY],
    })
    execution[PAYLOAD_DIGEST_KEY] = semantic_digest(_payload(execution))
    execution["digest_manifest"] = {
        "source_approval": SOURCE_APPROVAL_DIGEST,
        "source_operator_review": source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate": source.source.SOURCE_CANDIDATE_DIGEST,
        "source_failure_diagnosis": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
        "diagnostic_payload": execution[PAYLOAD_DIGEST_KEY], "durable_receipt": execution[RECEIPT_DIGEST_KEY],
        "outputs": semantic_digest(SUCCESS_OUTPUTS), "risk_controls": semantic_digest(RISK_CONTROLS),
    }
    execution[DIGEST_MANIFEST_DIGEST_KEY] = semantic_digest(execution["digest_manifest"])
    final_receipt[PAYLOAD_DIGEST_KEY] = execution[PAYLOAD_DIGEST_KEY]
    final_receipt[DIGEST_MANIFEST_DIGEST_KEY] = execution[DIGEST_MANIFEST_DIGEST_KEY]
    execution["durable_receipt_record"] = deepcopy(final_receipt)
    try:
        _persist_json(receipt_path, final_receipt)
    except (OSError, TypeError, ValueError) as exc:
        return _build_blocked(
            run_timestamp, "DURABLE_RECEIPT_DERIVED_DIGEST_FINALIZATION_FAILED", state=post,
            missing=[type(exc).__name__], receipt_path=receipt_path, scaffold_prewritten=True,
            command_executed=True, output_captured=True, targeted_pytest_performed=True,
            retained_receipt=final_receipt,
        )
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    execution[EXECUTION_DIGEST_KEY] = _execution_digest(execution)
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(execution)
    return execution


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    checks = [_check(f"{field}_bound", expected, execution.get(field)) for field, expected in SOURCE_BINDINGS.items()]
    checks.extend([
        _check("retry_execution_commit_bound", RETRY_EXECUTION_COMMIT, execution.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, {key: execution.get("retry_failure_context", {}).get(key) for key in ("passed", "failed", "errors", "skipped")}),
        _check("selected_package_bound", SELECTED_PACKAGE, execution.get("selected_receipt_recovery_or_recapture_package")),
        _check("priority_1_top_module_paths_bound", TARGET_MODULES, [item.get("module_path") for item in execution.get("priority_1_top_module_groups", [])]),
        _check("priority_1_total_612_bound", 612, execution.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, execution.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, execution.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, execution.get("failed_or_errored_nodeids_count")),
        _check("unavailable_prior_values_not_reconstructed", False, execution.get("unavailable_prior_values_reconstructed")),
        _check("unavailable_prior_values_not_inferred", False, execution.get("unavailable_prior_values_inferred")),
    ])
    if success:
        record = execution.get("controlled_recapture_command_record", {})
        result = execution.get("controlled_recapture_execution_result", {})
        receipt = execution.get("durable_receipt_record", {})
        checks.extend([
            _check("receipt_scaffold_prewritten_if_success", True, execution.get("durable_receipt_scaffold_prewritten")),
            _check("receipt_finalized_if_success", True, execution.get("durable_receipt_finalized")),
            _check("receipt_retained_if_success", True, execution.get("durable_receipt_retained")),
            _check("command_argv_if_success", list(APPROVED_ARGV), record.get("argv")),
            _check("command_cwd_if_success", str(APPROVED_WORKING_DIRECTORY), record.get("cwd")),
            _check("command_python_if_success", str(APPROVED_PYTHON_EXECUTABLE), record.get("python_executable")),
            _check("target_modules_if_success", TARGET_MODULES, execution.get("controlled_recapture_target_modules")),
            _check("receipt_status_if_success", "FINALIZED_AFTER_COMMAND", receipt.get("receipt_status")),
            _check("receipt_digest_if_success", execution.get(RECEIPT_DIGEST_KEY), receipt.get(RECEIPT_DIGEST_KEY)),
            _check("exit_code_captured_if_success", True, isinstance(result.get("exit_code"), int)),
            _check("stdout_hash_captured_if_success", True, isinstance(result.get("stdout_sha256"), str) and len(result.get("stdout_sha256")) == 64),
            _check("stderr_hash_captured_if_success", True, isinstance(result.get("stderr_sha256"), str) and len(result.get("stderr_sha256")) == 64),
            _check("bounded_stdout_excerpt_captured_if_success", True, isinstance(execution.get("bounded_stdout_excerpt"), str)),
            _check("bounded_stderr_excerpt_captured_if_success", True, isinstance(execution.get("bounded_stderr_excerpt"), str)),
            _check("output_volume_recorded_if_success", result.get("stdout_byte_count", 0) + result.get("stderr_byte_count", 0), result.get("combined_output_byte_count")),
            _check("redaction_summary_recorded_if_success", True, execution.get("redaction_summary", {}).get("redaction_checked")),
            _check("payload_digest_generated_if_success", True, isinstance(execution.get(PAYLOAD_DIGEST_KEY), str) and len(execution.get(PAYLOAD_DIGEST_KEY)) == 64),
            _check("receipt_digest_generated_if_success", True, isinstance(execution.get(RECEIPT_DIGEST_KEY), str) and len(execution.get(RECEIPT_DIGEST_KEY)) == 64),
            _check("digest_manifest_digest_generated_if_success", True, isinstance(execution.get(DIGEST_MANIFEST_DIGEST_KEY), str) and len(execution.get(DIGEST_MANIFEST_DIGEST_KEY)) == 64),
        ])
    else:
        checks.extend([
            _check("blocked_reason_recorded_if_blocked", True, isinstance(execution.get("blocked_reason"), str) and bool(execution.get("blocked_reason"))),
            _check("blocked_manifest_digest_generated_if_blocked", True, isinstance(execution.get(BLOCKED_MANIFEST_DIGEST_KEY), str) and len(execution.get(BLOCKED_MANIFEST_DIGEST_KEY)) == 64),
        ])
    for field in CLOSED_FALSE_FIELDS:
        checks.append(_check(f"{field}_false", False, execution.get(field)))
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, execution.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, execution.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, execution.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, execution.get("broker_execution")),
        _check("next_chain_defined", SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, execution.get("next_chain")),
        _check("next_gates_defined", SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES, execution.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, execution.get("risk_controls")),
    ])
    return checks


def _summary(execution: Mapping[str, Any]) -> dict[str, Any]:
    checklist = execution.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed,
        "receipt_recovery_or_recapture_execution_created": True,
        "receipt_recovery_or_recapture_execution_performed": execution.get("receipt_recovery_or_recapture_execution_performed", False),
        "controlled_recapture_execution_performed": execution.get("controlled_recapture_execution_performed", False),
        "receipt_recovery_execution_performed": False, "receipt_recovered": False,
        "durable_receipt_scaffold_prewritten": execution.get("durable_receipt_scaffold_prewritten", False),
        "durable_receipt_finalized": execution.get("durable_receipt_finalized", False),
        "durable_receipt_retained": execution.get("durable_receipt_retained", False),
        "diagnostic_command_executed_in_execution": execution.get("diagnostic_command_executed_in_execution", False),
        "diagnostic_output_captured_in_execution": execution.get("diagnostic_output_captured_in_execution", False),
        "targeted_pytest_performed": execution.get("targeted_pytest_performed", False),
        "full_pytest_performed": False, "retry_rerun_performed": False,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "ready_for_receipt_recovery_or_recapture_results_review": success,
        "ready_for_diagnostic_results_review": False, "ready_for_remediation_or_method_candidate": False,
        "ready_for_retry_candidate": False, "new_retry_candidate_created": False, "new_retry_executed": False,
        "integration_execution_successful": False, "recommended_next_task": execution.get("recommended_next_task"),
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
        **({"blocked_reason": execution.get("blocked_reason")} if not success else {}),
    }


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(execution: dict) -> dict:
    """Validate successful or fail-closed controlled-recapture evidence."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError
    if not isinstance(execution, dict):
        raise error("execution must be an object")
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    expected = {
        "artifact_kind": ARTIFACT_KIND_SUCCESS if success else ARTIFACT_KIND_BLOCKED,
        "execution_status": EXECUTION_STATUS_SUCCESS if success else EXECUTION_STATUS_BLOCKED,
        "execution_scope": EXECUTION_SCOPE, "schema_version": SCHEMA_VERSION,
        "selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        "controlled_recapture_execution_only": True, **SOURCE_BINDINGS,
        "retry_execution_commit": RETRY_EXECUTION_COMMIT, "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29, "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "priority_1_top_module_groups": source.source.source.PRIORITY_1_TARGET_MODULES,
    }
    for field, value in expected.items():
        if execution.get(field) != value:
            raise error(f"{field} mismatch")
    counts = {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    if {key: execution.get("retry_failure_context", {}).get(key) for key in counts} != counts:
        raise error("retry failure counts mismatch")
    if any(execution.get(field) is not False for field in CLOSED_FALSE_FIELDS):
        raise error("closed boundary opened")
    if execution.get("predictive_usefulness") != NOT_ACCEPTED or execution.get("profitability") != NOT_ACCEPTED:
        raise error("acceptance boundary changed")
    if any(execution.get(field) != NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")):
        raise error("runtime boundary changed")
    if execution.get("risk_controls") != RISK_CONTROLS:
        raise error("risk controls mismatch")
    if success:
        if any(execution.get(field) is not True for field in SUCCESS_TRUE_FIELDS):
            raise error("successful execution fact missing")
        record, result, receipt = execution.get("controlled_recapture_command_record", {}), execution.get("controlled_recapture_execution_result", {}), execution.get("durable_receipt_record", {})
        if record.get("argv") != list(APPROVED_ARGV) or record.get("command") != APPROVED_COMMAND:
            raise error("approved command mismatch")
        if record.get("cwd") != str(APPROVED_WORKING_DIRECTORY) or record.get("python_executable") != str(APPROVED_PYTHON_EXECUTABLE):
            raise error("approved execution location mismatch")
        if record.get("target_modules") != TARGET_MODULES or execution.get("controlled_recapture_target_modules") != TARGET_MODULES:
            raise error("target modules mismatch")
        if receipt.get("receipt_status") != "FINALIZED_AFTER_COMMAND" or receipt.get("command_executed") is not True or receipt.get("receipt_finalized") is not True:
            raise error("durable receipt not finalized")
        if receipt.get(RECEIPT_DIGEST_KEY) != _receipt_digest(receipt) or execution.get(RECEIPT_DIGEST_KEY) != receipt.get(RECEIPT_DIGEST_KEY):
            raise error("receipt digest mismatch")
        if not isinstance(result.get("exit_code"), int):
            raise error("exit code missing")
        try:
            duration = float(result.get("duration_seconds"))
        except (TypeError, ValueError) as exc:
            raise error("execution duration invalid") from exc
        if duration < 0:
            raise error("execution duration invalid")
        for field in ("stdout_sha256", "stderr_sha256"):
            if not isinstance(result.get(field), str) or re.fullmatch(r"[0-9a-f]{64}", result[field]) is None:
                raise error(f"{field} missing")
        counts_out = [result.get("stdout_byte_count"), result.get("stderr_byte_count"), result.get("combined_output_byte_count")]
        if any(not isinstance(item, int) or item < 0 for item in counts_out) or counts_out[0] + counts_out[1] != counts_out[2]:
            raise error("output byte counts invalid")
        capture = execution.get("controlled_recapture_output_capture_summary", {})
        stdout_limit, stderr_limit = capture.get("maximum_stdout_excerpt_chars"), capture.get("maximum_stderr_excerpt_chars")
        if not isinstance(stdout_limit, int) or not 0 < stdout_limit <= 20000 or not isinstance(stderr_limit, int) or not 0 < stderr_limit <= 20000:
            raise error("bounded output contract invalid")
        if not isinstance(execution.get("bounded_stdout_excerpt"), str) or len(execution["bounded_stdout_excerpt"]) > stdout_limit:
            raise error("bounded stdout excerpt invalid")
        if not isinstance(execution.get("bounded_stderr_excerpt"), str) or len(execution["bounded_stderr_excerpt"]) > stderr_limit:
            raise error("bounded stderr excerpt invalid")
        if execution.get("redaction_summary", {}).get("redaction_checked") is not True:
            raise error("redaction summary missing")
        if execution.get("outputs") != SUCCESS_OUTPUTS or execution.get("next_chain") != SUCCESS_NEXT_CHAIN or execution.get("next_gates") != SUCCESS_NEXT_GATES:
            raise error("success disposition mismatch")
        if execution.get(PAYLOAD_DIGEST_KEY) != semantic_digest(_payload(execution)):
            raise error("payload digest mismatch")
        expected_manifest = {
            "source_approval": SOURCE_APPROVAL_DIGEST, "source_operator_review": source.SOURCE_OPERATOR_REVIEW_DIGEST,
            "source_candidate": source.source.SOURCE_CANDIDATE_DIGEST,
            "source_failure_diagnosis": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
            "diagnostic_payload": execution[PAYLOAD_DIGEST_KEY], "durable_receipt": execution[RECEIPT_DIGEST_KEY],
            "outputs": semantic_digest(SUCCESS_OUTPUTS), "risk_controls": semantic_digest(RISK_CONTROLS),
        }
        if execution.get("digest_manifest") != expected_manifest or execution.get(DIGEST_MANIFEST_DIGEST_KEY) != semantic_digest(expected_manifest):
            raise error("digest manifest mismatch")
    else:
        if not isinstance(execution.get("blocked_reason"), str) or not execution["blocked_reason"]:
            raise error("blocked reason missing")
        if execution.get("next_chain") != BLOCKED_NEXT_CHAIN or execution.get("next_gates") != BLOCKED_NEXT_GATES:
            raise error("blocked disposition mismatch")
        if execution.get(BLOCKED_MANIFEST_DIGEST_KEY) != _blocked_manifest_digest(execution):
            raise error("blocked manifest digest mismatch")
    checklist = _checklist(execution)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if execution.get("summary") != _summary(execution):
        raise error("summary mismatch")
    digest = execution.get(EXECUTION_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _execution_digest(execution):
        raise error("execution digest mismatch")
    return {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"], "execution_digest": digest,
        **{field: execution["summary"][field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
    output_dir: str | Path, *, source_approval: dict | None = None, run_timestamp_utc: str | None = None,
    command_runner: Callable[[Sequence[str], Path], Any] | None = None,
    durable_receipt_filename: str = DEFAULT_RECEIPT_FILENAME,
) -> dict:
    """Execute using a receipt below the supplied docs/status directory."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError("protected output directory")
    if Path(durable_receipt_filename).name != durable_receipt_filename or durable_receipt_filename != DEFAULT_RECEIPT_FILENAME:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError("durable receipt filename mismatch")
    return execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(
        source_approval=source_approval, run_timestamp_utc=run_timestamp_utc, command_runner=command_runner,
        durable_receipt_path=output / durable_receipt_filename,
    )


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_markdown_v1(execution: dict) -> str:
    """Render a bounded status summary after strict validation."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(execution)
    success = execution["artifact_kind"] == ARTIFACT_KIND_SUCCESS
    sections = [
        ("Source Receipt Recovery or Recapture Approval", [SOURCE_APPROVAL_DIGEST]),
        ("Source Candidate Operator Review and Candidate", [source.SOURCE_OPERATOR_REVIEW_DIGEST, source.source.SOURCE_CANDIDATE_DIGEST]),
        ("Source Execution Failure Diagnosis", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"]]),
        ("Source Targeted Diagnostic Output Capture Execution", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_digest"]]),
        ("Source Planning and Detail Binding Evidence", [SOURCE_BINDINGS["source_results_review_digest"], SOURCE_BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the first retry remains authoritative."]),
        ("Execution Scope", [EXECUTION_SCOPE]), ("Approved Priority 1 Target Modules", TARGET_MODULES),
        ("Approved Controlled Recapture Command", [APPROVED_COMMAND]),
        ("Durable Receipt Scaffold", [execution.get("durable_receipt_path", "not written"), str(execution.get("durable_receipt_scaffold_prewritten"))]),
        ("Pre-Execution Checks", [str(execution.get("controlled_recapture_command_record", {}).get("pre_execution_checks", execution.get("available_data", {}).get("completed_precheck_facts", {})))]),
        ("Controlled Recapture Result", [execution["execution_status"], str(execution.get("controlled_recapture_execution_result", execution.get("blocked_reason")))]),
        ("Diagnostic Output Capture Summary", [str(execution.get("controlled_recapture_output_capture_summary", "not captured"))]),
        ("Bounded Output Excerpts", [execution.get("bounded_stdout_excerpt", "not captured"), execution.get("bounded_stderr_excerpt", "not captured")]),
        ("Redaction Summary", [str(execution.get("redaction_summary", "not captured"))]),
        ("Post-Execution Boundary Checks", [str(execution.get("post_execution_boundary_checks", "not performed"))]),
        ("Unsupported Claims Boundary", ["No root-cause, remediation, retry-success, integration-success, or merge-readiness claim is made."]),
        ("Success or Blocked Disposition", ["SUCCESS" if success else "BLOCKED"]),
        ("Recommendation", [execution["recommended_next_task"]]),
        ("Next Chain", execution["next_chain"]), ("Next Gates", execution["next_gates"]),
        ("Risk Controls", execution["risk_controls"]),
        ("Authority Boundaries", ["Diagnostic evidence only; no retry, main, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["No provider, evidence regeneration, full pytest, retry rerun, cache read, remediation, or classification."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Receipt Recovery or Recapture Execution v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTED_V1 = ARTIFACT_KIND_SUCCESS
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_BLOCKED_V1 = ARTIFACT_KIND_BLOCKED
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTED_CONTROLLED_SINGLE_RECAPTURE_RECEIPT_FINALIZED = EXECUTION_STATUS_SUCCESS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_BLOCKED_RECEIPT_OR_RECAPTURE_UNAVAILABLE_OR_BOUNDARY_FAILURE = EXECUTION_STATUS_BLOCKED
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_ONLY_CONTROLLED_RECAPTURE_DIAGNOSTIC_OUTPUT_CAPTURE_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_CONTROLLED_SINGLE_RECAPTURE_WITH_PREWRITE_RECEIPT_FILE_AND_NO_CACHEPROVIDER = SELECTED_PACKAGE


__all__ = [
    "ARTIFACT_KIND_SUCCESS", "ARTIFACT_KIND_BLOCKED", "EXECUTION_STATUS_SUCCESS", "EXECUTION_STATUS_BLOCKED",
    "EXECUTION_SCOPE", "SELECTED_PACKAGE", "SOURCE_APPROVAL_DIGEST", "SOURCE_BINDINGS",
    "APPROVED_COMMAND", "APPROVED_ARGV", "APPROVED_WORKING_DIRECTORY", "APPROVED_PYTHON_EXECUTABLE", "TARGET_MODULES",
    "DEFAULT_RECEIPT_FILENAME", "SUCCESS_OUTPUTS", "SUCCESS_NEXT_CHAIN", "BLOCKED_NEXT_CHAIN",
    "SUCCESS_NEXT_GATES", "BLOCKED_NEXT_GATES", "RISK_CONTROLS", "SUCCESS_TRUE_FIELDS", "CLOSED_FALSE_FIELDS",
    "EXECUTION_DIGEST_KEY", "PAYLOAD_DIGEST_KEY", "RECEIPT_DIGEST_KEY", "DIGEST_MANIFEST_DIGEST_KEY", "BLOCKED_MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTED_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_BLOCKED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTED_CONTROLLED_SINGLE_RECAPTURE_RECEIPT_FINALIZED",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_BLOCKED_RECEIPT_OR_RECAPTURE_UNAVAILABLE_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_ONLY_CONTROLLED_RECAPTURE_DIAGNOSTIC_OUTPUT_CAPTURE_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CONTROLLED_SINGLE_RECAPTURE_WITH_PREWRITE_RECEIPT_FILE_AND_NO_CACHEPROVIDER",
    "MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError",
    "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1",
    "write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_markdown_v1",
]
