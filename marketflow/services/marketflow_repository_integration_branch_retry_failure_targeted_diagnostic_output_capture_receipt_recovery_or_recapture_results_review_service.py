"""Review the committed controlled-recapture receipt without rerunning commands."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_ONLY_NOT_RECAPTURE_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1"
SOURCE_EXECUTION_COMMIT = "51175f3d24232773ae3982a97b05877e18ff699e"
SOURCE_EXECUTION_DIGEST = "25a70331c48eedeb62c6f8532dba0e1b782904ff4b753934c2fd12ccbec47e46"
SOURCE_PAYLOAD_DIGEST = "073b47101ff05794af3f92489bd1f97a286cfc7c29c1d95d1ca2a022270d2c38"
SOURCE_RECEIPT_DIGEST = "dfd7f50c4065e759ccfee0f160c97177f4d9a1cfe977fb6db1ce240f8ad3345b"
SOURCE_DIGEST_MANIFEST_DIGEST = "77b91f2d514128e014e0d141ff38f86d3379f43d97082f0cf84ffb037ae415ab"
SOURCE_DURABLE_RECEIPT_PATH = f"docs/status/{source.DEFAULT_RECEIPT_FILENAME}"
DEFAULT_DURABLE_RECEIPT_PATH = Path(__file__).resolve().parents[2] / SOURCE_DURABLE_RECEIPT_PATH
SELECTED_PACKAGE = source.SELECTED_PACKAGE
RETRY_EXECUTION_COMMIT = source.RETRY_EXECUTION_COMMIT
PRIORITY_1_TARGET_MODULES = deepcopy(source.source.source.source.PRIORITY_1_TARGET_MODULES)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

RESULTS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_digest"
PAYLOAD_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_payload_review_digest"
DURABLE_RECEIPT_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_durable_receipt_review_digest"
RESULTS_REVIEW_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_manifest_digest"

SOURCE_BINDINGS = deepcopy(source.SOURCE_BINDINGS)

OUTPUT_IDS = [
    "receipt_recovery_or_recapture_results_review_manifest", "source_execution_digest_review",
    "diagnostic_payload_digest_review", "durable_receipt_digest_review", "durable_receipt_file_review",
    "controlled_recapture_command_review", "priority_1_target_module_review",
    "controlled_recapture_exit_code_review", "stdout_hash_and_volume_review", "stderr_hash_and_volume_review",
    "bounded_output_excerpt_review", "redaction_summary_review", "post_execution_boundary_review",
    "unsupported_claims_boundary_review", "remediation_or_method_candidate_readiness_report",
    "retry_gate_preservation_report", "digest_manifest",
]
REVIEW_OUTPUTS = [{"output_id": item, "status": "GENERATED_DIAGNOSTIC_RESULTS_REVIEW_ONLY"} for item in OUTPUT_IDS]

REVIEW_FINDINGS = {
    "finding_1": "The controlled single recapture execution completed successfully and created a finalized durable receipt.",
    "finding_2": "The durable receipt scaffold was prewritten before command execution and finalized after command completion.",
    "finding_3": "The reviewed command used the approved Python executable, detached integration worktree cwd, exactly the five approved Priority 1 module paths, and `-p no:cacheprovider`.",
    "finding_4": "The reviewed command was not the failed retry command and was not full pytest.",
    "finding_5": "The command exit code was 1, which is accepted as diagnostic evidence only and is not retry evidence.",
    "finding_6": "The command captured stdout and stderr stream hashes, byte counts, duration, and bounded excerpts.",
    "finding_7": "The stdout stream was 1,231,380 bytes and was stored only as a bounded truncated excerpt.",
    "finding_8": "The stderr stream was empty, with SHA-256 equal to the empty-stream digest.",
    "finding_9": "Redaction checking was performed before storing bounded excerpts.",
    "finding_10": "The execution digest, diagnostic payload digest, durable receipt digest, and digest-manifest digest are bound and reviewed.",
    "finding_11": "The prior failed diagnostic-capture execution remains historically blocked due to receipt loss and is not converted into success.",
    "finding_12": "The authoritative detached retry remains failed with 24,877 passed, 1,292 failed, 112 errors, and 7 skipped.",
    "finding_13": "This results review did not rerun recapture, run pytest, rerun retry, read cache, parse logs, inspect `.env`, execute remediation, execute classification, or create a retry candidate.",
    "finding_14": "The reviewed diagnostic evidence supports a separately invoked remediation-or-method candidate after diagnostic capture.",
    "finding_15": "The reviewed diagnostic evidence does not support direct remediation, failure/error separation, first-failure identification, traceback root-cause claim, retry success, or main-merge readiness.",
}

NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_V1"
NEXT_TASK_STATUS = "FUTURE_CANDIDATE_NOT_CREATED"
RECOMMENDED_ACTION = "PROCEED_TO_SEPARATELY_INVOKED_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE"
RECOMMENDATION_REASON = (
    "The controlled recapture produced a finalized durable diagnostic receipt with command, cwd, approved target "
    "modules, exit code, stdout/stderr hashes, byte counts, bounded output, and redaction status. This is sufficient "
    "to create a separately governed remediation-or-method candidate, but it is not retry evidence and does not "
    "authorize a retry or main merge."
)
NEXT_CHAIN = [
    "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1.",
    "Remediation or Method Candidate Operator Review v1.", "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.", "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "retry_failure_remediation_or_method_candidate_after_diagnostic_capture",
    "remediation_or_method_candidate_operator_review", "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved", "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "results_review_does_not_rerun_controlled_recapture", "results_review_does_not_run_diagnostic_command",
    "results_review_does_not_run_targeted_pytest", "results_review_does_not_run_full_pytest",
    "results_review_does_not_rerun_retry", "results_review_does_not_read_pytest_cache",
    "results_review_does_not_modify_pytest_cache", "results_review_does_not_parse_terminal_logs",
    "results_review_does_not_parse_operator_logs", "results_review_does_not_inspect_env",
    "results_review_does_not_reconstruct_prior_lost_values", "results_review_does_not_execute_remediation",
    "results_review_does_not_execute_classification", "results_review_does_not_classify_modules_again",
    "results_review_does_not_identify_first_failure", "results_review_does_not_identify_first_error",
    "results_review_does_not_claim_traceback_root_cause", "results_review_does_not_recommend_direct_code_remediation",
    "results_review_does_not_create_remediation_or_method_candidate", "results_review_does_not_create_new_retry_candidate",
    "results_review_does_not_create_retry_results_review", "results_review_does_not_create_integration_results_review",
    "results_review_does_not_mark_integration_successful", "results_review_does_not_generate_successful_integration_digest",
    "results_review_does_not_treat_controlled_recapture_as_retry", "results_review_does_not_treat_exit_code_as_retry_result",
    "results_review_does_not_push_integration_branch", "results_review_does_not_push_main",
    "results_review_does_not_delete_integration_branch", "results_review_does_not_delete_worktree",
    "results_review_does_not_force_push", "results_review_does_not_prune_remotes",
    "results_review_does_not_modify_tags", "results_review_does_not_modify_staged_evidence",
    "results_review_does_not_regenerate_evidence", "results_review_does_not_call_providers",
    "results_review_does_not_acquire_market_data", "results_review_does_not_regenerate_dataset",
    "results_review_does_not_recompute_metrics", "results_review_does_not_train_models",
    "results_review_does_not_score_strategy", "results_review_does_not_generate_recommendations",
    "results_review_does_not_accept_predictive_usefulness", "results_review_does_not_accept_profitability",
    "results_review_does_not_authorize_runtime", "results_review_does_not_authorize_broker_execution",
    "durable_receipt_is_diagnostic_evidence_only", "controlled_recapture_is_not_retry_success",
    "priority_1_selection_is_not_root_cause", "module_concentration_is_not_failure_error_separation",
    "prior_blocked_diagnostic_capture_execution_remains_historically_blocked",
    "previous_receipt_recovery_or_recapture_approval_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_operator_review_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_candidate_remains_source_evidence",
    "previous_failure_diagnosis_remains_source_evidence", "previous_targeted_diagnostic_approval_remains_source_evidence",
    "previous_planning_results_review_remains_valid", "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_remediation_or_method_candidate_required_after_this_review",
    "separate_retry_approval_required_before_new_retry", "main_merge_requires_passing_new_retry_results_review",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "receipt_recovery_or_recapture_results_review_created", "receipt_recovery_or_recapture_results_review_ready",
    "source_execution_reviewed", "source_execution_digest_verified", "source_payload_digest_verified",
    "source_durable_receipt_digest_verified", "source_digest_manifest_verified", "source_durable_receipt_file_reviewed",
    "controlled_recapture_execution_reviewed", "durable_receipt_scaffold_reviewed",
    "durable_receipt_finalization_reviewed", "diagnostic_output_capture_reviewed", "bounded_output_reviewed",
    "redaction_summary_reviewed", "post_execution_boundary_checks_reviewed", "unsupported_claims_boundary_reviewed",
    "ready_for_remediation_or_method_candidate_after_diagnostic_capture",
]
FALSE_FIELDS = [
    "ready_for_retry_candidate", "ready_for_main_merge_approval", "controlled_recapture_rerun_performed",
    "diagnostic_command_rerun_performed", "targeted_pytest_performed_in_review", "full_pytest_performed",
    "retry_rerun_performed", "cache_read_in_review", "cache_modified_in_review", "pytest_cache_committed",
    "marketflow_outputs_committed", "terminal_logs_parsed", "operator_logs_parsed", "env_inspection_performed",
    "prior_lost_values_reconstructed", "prior_lost_values_inferred", "diagnostic_results_review_created",
    "remediation_or_method_candidate_after_diagnostic_capture_created", "remediation_execution_performed",
    "classification_execution_performed_in_review", "new_retry_candidate_created", "new_retry_executed",
    "new_retry_results_review_created", "main_merge_approval_created", "failure_modules_classified",
    "error_modules_classified", "failure_error_separation_claimed", "first_failure_identified",
    "first_error_identified", "first_order_claim_made", "traceback_root_cause_claimed",
    "direct_code_remediation_recommended", "retry_success_claimed", "main_merge_readiness_claimed",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "evidence_regenerated", "provider_requests_made_in_review",
    "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
    "metric_recomputation_from_raw_rows_performed", "model_training_performed", "strategy_scoring_performed",
    "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError(ValueError):
    """Raised when committed source evidence or review content is invalid."""


def _read_receipt(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError("durable receipt unavailable") from exc
    if not isinstance(value, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError("durable receipt must be an object")
    return value


def _execution_from_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Rebuild the committed source artifact from receipt facts without execution."""

    result = deepcopy(receipt.get("controlled_recapture_execution_result", {}))
    execution = source._base_execution(str(receipt.get("receipt_scaffold_timestamp_utc")))
    execution.update({
        "artifact_kind": source.ARTIFACT_KIND_SUCCESS, "execution_status": source.EXECUTION_STATUS_SUCCESS,
        "created_offline": False, "governance_only": False, **{field: True for field in source.SUCCESS_TRUE_FIELDS},
        "durable_receipt_path": str(Path(SOURCE_DURABLE_RECEIPT_PATH)),
        "controlled_recapture_command_record": {
            "command": receipt.get("approved_command"), "argv": deepcopy(receipt.get("approved_command_argv")),
            "cwd": receipt.get("approved_cwd"), "python_executable": receipt.get("approved_python_executable"),
            "target_modules": deepcopy(receipt.get("approved_target_modules")),
            "start_timestamp_utc": receipt.get("receipt_scaffold_timestamp_utc"),
            "end_timestamp_utc": receipt.get("command_end_timestamp_utc"),
            "pre_execution_checks": deepcopy(receipt.get("pre_execution_checks")),
        },
        "controlled_recapture_target_modules": deepcopy(receipt.get("approved_target_modules")),
        "durable_receipt_record": deepcopy(dict(receipt)), "controlled_recapture_execution_result": result,
        "controlled_recapture_output_capture_summary": {
            "full_streams_stored": False, "full_stream_hashes_stored": True, "bounded_excerpts_stored": True,
            "maximum_stdout_excerpt_chars": 20000, "maximum_stderr_excerpt_chars": 20000,
            "nonzero_exit_code_is_diagnostic_evidence_only": result.get("exit_code") != 0,
        },
        "bounded_stdout_excerpt": receipt.get("bounded_stdout_excerpt"),
        "bounded_stderr_excerpt": receipt.get("bounded_stderr_excerpt"),
        "redaction_summary": deepcopy(receipt.get("redaction_summary")),
        "post_execution_boundary_checks": deepcopy(receipt.get("post_execution_boundary_checks")),
        "outputs": deepcopy(source.SUCCESS_OUTPUTS),
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_V1",
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_RESULTS_REVIEW",
        "next_chain": list(source.SUCCESS_NEXT_CHAIN), "next_gates": list(source.SUCCESS_NEXT_GATES),
        source.RECEIPT_DIGEST_KEY: receipt.get(source.RECEIPT_DIGEST_KEY),
        source.PAYLOAD_DIGEST_KEY: receipt.get(source.PAYLOAD_DIGEST_KEY),
    })
    execution["digest_manifest"] = {
        "source_approval": source.SOURCE_APPROVAL_DIGEST,
        "source_operator_review": source.source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate": source.source.source.SOURCE_CANDIDATE_DIGEST,
        "source_failure_diagnosis": source.SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
        "diagnostic_payload": execution[source.PAYLOAD_DIGEST_KEY],
        "durable_receipt": execution[source.RECEIPT_DIGEST_KEY],
        "outputs": semantic_digest(source.SUCCESS_OUTPUTS), "risk_controls": semantic_digest(source.RISK_CONTROLS),
    }
    execution[source.DIGEST_MANIFEST_DIGEST_KEY] = receipt.get(source.DIGEST_MANIFEST_DIGEST_KEY)
    execution["checklist"] = source._checklist(execution)
    execution["summary"] = source._summary(execution)
    execution[source.EXECUTION_DIGEST_KEY] = source._execution_digest(execution)
    source.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(execution)
    return execution


def _validate_source(execution: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError
    try:
        source.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(dict(execution))
    except source.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError as exc:
        raise error("source execution validation failed") from exc
    expected = {
        source.EXECUTION_DIGEST_KEY: SOURCE_EXECUTION_DIGEST,
        source.PAYLOAD_DIGEST_KEY: SOURCE_PAYLOAD_DIGEST,
        source.RECEIPT_DIGEST_KEY: SOURCE_RECEIPT_DIGEST,
        source.DIGEST_MANIFEST_DIGEST_KEY: SOURCE_DIGEST_MANIFEST_DIGEST,
    }
    if any(execution.get(field) != value for field, value in expected.items()):
        raise error("source execution digest mismatch")
    if execution.get("durable_receipt_record") != dict(receipt):
        raise error("source durable receipt mismatch")
    if receipt.get("receipt_status") != "FINALIZED_AFTER_COMMAND" or receipt.get("receipt_finalized") is not True:
        raise error("source receipt not finalized")
    if receipt.get(source.RECEIPT_DIGEST_KEY) != SOURCE_RECEIPT_DIGEST or source._receipt_digest(receipt) != SOURCE_RECEIPT_DIGEST:
        raise error("source durable receipt digest mismatch")


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _payload_review(review: Mapping[str, Any]) -> dict[str, Any]:
    return {field: deepcopy(review.get(field)) for field in (
        "source_execution_summary", "source_durable_receipt_summary", "controlled_recapture_result_review",
        "durable_receipt_review", "diagnostic_output_capture_review", "bounded_output_review",
        "redaction_review", "post_execution_boundary_review", "unsupported_claims_boundary_review",
    )}


def _review_digest(review: Mapping[str, Any]) -> str:
    value = deepcopy(dict(review))
    for field in ("checklist", "summary", RESULTS_REVIEW_DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    result = review.get("controlled_recapture_result_review", {})
    receipt = review.get("durable_receipt_review", {})
    checks = [
        _check("source_execution_commit_bound", SOURCE_EXECUTION_COMMIT, review.get("source_execution_commit")),
        _check("source_execution_digest_bound", SOURCE_EXECUTION_DIGEST, review.get("source_receipt_recovery_or_recapture_execution_digest")),
        _check("source_payload_digest_bound", SOURCE_PAYLOAD_DIGEST, review.get("source_receipt_recovery_or_recapture_payload_digest")),
        _check("source_durable_receipt_digest_bound", SOURCE_RECEIPT_DIGEST, review.get("source_receipt_recovery_or_recapture_receipt_digest")),
        _check("source_digest_manifest_digest_bound", SOURCE_DIGEST_MANIFEST_DIGEST, review.get("source_receipt_recovery_or_recapture_digest_manifest_digest")),
        _check("source_durable_receipt_path_bound", SOURCE_DURABLE_RECEIPT_PATH, review.get("source_durable_receipt_path")),
        *[_check(f"{field}_bound", value, review.get(field)) for field, value in SOURCE_BINDINGS.items()],
        _check("retry_execution_commit_bound", RETRY_EXECUTION_COMMIT, review.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, review.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", source.TARGET_MODULES, [item.get("module_path") for item in review.get("priority_1_target_modules", [])]),
        _check("priority_1_total_612_bound", 612, review.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, review.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, review.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, review.get("failed_or_errored_nodeids_count")),
        _check("source_exit_code_1_bound", 1, review.get("source_exit_code")),
        _check("source_duration_seconds_bound", "21.584361", review.get("source_duration_seconds")),
        _check("source_stdout_byte_count_bound", 1231380, review.get("source_stdout_byte_count")),
        _check("source_stderr_byte_count_bound", 0, review.get("source_stderr_byte_count")),
        _check("source_stdout_excerpt_truncated_bound", True, review.get("source_stdout_excerpt_truncated")),
        _check("source_stderr_excerpt_truncated_bound", False, review.get("source_stderr_excerpt_truncated")),
        _check("source_redaction_checked_bound", True, review.get("source_redaction_checked")),
        _check("source_execution_status_success_bound", source.EXECUTION_STATUS_SUCCESS, review.get("source_execution_status")),
        _check("source_execution_scope_bound", source.EXECUTION_SCOPE, review.get("source_execution_scope")),
        _check("controlled_recapture_execution_performed_true", True, result.get("controlled_recapture_execution_performed")),
        _check("durable_receipt_scaffold_prewritten_true", True, receipt.get("scaffold_prewritten")),
        _check("durable_receipt_finalized_true", True, receipt.get("finalized")),
        _check("durable_receipt_retained_true", True, receipt.get("retained")),
        _check("diagnostic_command_executed_true", True, result.get("diagnostic_command_executed")),
        _check("diagnostic_output_captured_true", True, result.get("diagnostic_output_captured")),
        _check("targeted_pytest_performed_true", True, result.get("targeted_pytest_performed")),
        _check("controlled_recapture_command_is_not_retry", False, result.get("command_is_retry")),
        _check("controlled_recapture_command_is_not_full_pytest", False, result.get("command_is_full_pytest")),
        _check("approved_python_used", str(source.APPROVED_PYTHON_EXECUTABLE), result.get("python_executable")),
        _check("detached_worktree_cwd_used", str(source.APPROVED_WORKING_DIRECTORY), result.get("cwd")),
        _check("only_priority_1_modules_targeted", source.TARGET_MODULES, result.get("target_modules")),
        _check("cacheprovider_disabled_used", True, result.get("cacheprovider_disabled")),
        _check("exit_code_1_reviewed", 1, result.get("exit_code")),
        _check("duration_reviewed", "21.584361", result.get("duration_seconds")),
        _check("stdout_sha256_reviewed", "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a", result.get("stdout_sha256")),
        _check("stderr_sha256_reviewed", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", result.get("stderr_sha256")),
        _check("stdout_byte_count_1231380_reviewed", 1231380, result.get("stdout_byte_count")),
        _check("stderr_byte_count_0_reviewed", 0, result.get("stderr_byte_count")),
        _check("combined_output_byte_count_1231380_reviewed", 1231380, result.get("combined_output_byte_count")),
        _check("stdout_excerpt_truncated_true", True, result.get("stdout_excerpt_truncated")),
        _check("stderr_excerpt_truncated_false", False, result.get("stderr_excerpt_truncated")),
        _check("redaction_checked_true", True, review.get("redaction_review", {}).get("redaction_checked")),
    ]
    checks.extend(_check(f"{field}_true", True, review.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, review.get(field)) for field in FALSE_FIELDS)
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
        _check("review_outputs_generated", REVIEW_OUTPUTS, review.get("review_outputs")),
        _check("recommendation_defined", NEXT_TASK, review.get("recommendation", {}).get("recommended_next_task")),
        _check("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
        _check("payload_review_digest_present", True, isinstance(review.get(PAYLOAD_REVIEW_DIGEST_KEY), str) and len(review.get(PAYLOAD_REVIEW_DIGEST_KEY)) == 64),
        _check("durable_receipt_review_digest_present", True, isinstance(review.get(DURABLE_RECEIPT_REVIEW_DIGEST_KEY), str) and len(review.get(DURABLE_RECEIPT_REVIEW_DIGEST_KEY)) == 64),
        _check("results_review_manifest_digest_present", True, isinstance(review.get(RESULTS_REVIEW_MANIFEST_DIGEST_KEY), str) and len(review.get(RESULTS_REVIEW_MANIFEST_DIGEST_KEY)) == 64),
    ])
    return checks


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checklist = review.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed,
        **{field: review.get(field) for field in TRUE_FIELDS},
        "controlled_recapture_execution_performed": True,
        "diagnostic_command_executed_in_source_execution": True,
        "diagnostic_output_captured_in_source_execution": True,
        "targeted_pytest_performed_in_source_execution": True,
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True, "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False, "new_retry_candidate_created": False,
        "new_retry_executed": False, "integration_execution_successful": False,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(
    *, source_execution: dict | None = None, durable_receipt_path: str | Path | None = None,
) -> dict:
    """Build an offline review from the committed receipt and no execution calls."""

    path = Path(durable_receipt_path) if durable_receipt_path is not None else DEFAULT_DURABLE_RECEIPT_PATH
    receipt = _read_receipt(path)
    try:
        execution = deepcopy(source_execution) if source_execution is not None else _execution_from_receipt(receipt)
    except source.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureExecutionError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError(
            "source execution validation failed"
        ) from exc
    _validate_source(execution, receipt)
    command = execution["controlled_recapture_command_record"]
    result = execution["controlled_recapture_execution_result"]
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "results_review_only": True,
        "source_execution_artifact_kind": source.ARTIFACT_KIND_SUCCESS,
        "source_execution_status": source.EXECUTION_STATUS_SUCCESS, "source_execution_scope": source.EXECUTION_SCOPE,
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_receipt_recovery_or_recapture_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_receipt_recovery_or_recapture_payload_digest": SOURCE_PAYLOAD_DIGEST,
        "source_receipt_recovery_or_recapture_receipt_digest": SOURCE_RECEIPT_DIGEST,
        "source_receipt_recovery_or_recapture_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_durable_receipt_path": SOURCE_DURABLE_RECEIPT_PATH,
        "selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        **deepcopy(SOURCE_BINDINGS), "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, "first_result_authoritative": True, "root_full_regression_is_retry_evidence": False},
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "priority_1_target_modules": deepcopy(PRIORITY_1_TARGET_MODULES),
        "source_exit_code": result["exit_code"], "source_duration_seconds": result["duration_seconds"],
        "source_stdout_byte_count": result["stdout_byte_count"],
        "source_stderr_byte_count": result["stderr_byte_count"],
        "source_stdout_excerpt_truncated": result["stdout_excerpt_truncated"],
        "source_stderr_excerpt_truncated": result["stderr_excerpt_truncated"],
        "source_redaction_checked": execution["redaction_summary"]["redaction_checked"],
        "source_execution_summary": {
            "artifact_kind": source.ARTIFACT_KIND_SUCCESS, "execution_status": source.EXECUTION_STATUS_SUCCESS,
            "execution_scope": source.EXECUTION_SCOPE, "execution_commit": SOURCE_EXECUTION_COMMIT,
            "execution_digest": SOURCE_EXECUTION_DIGEST, "payload_digest": SOURCE_PAYLOAD_DIGEST,
            "receipt_digest": SOURCE_RECEIPT_DIGEST, "digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        },
        "source_durable_receipt_summary": {
            "path": SOURCE_DURABLE_RECEIPT_PATH, "receipt_status": receipt["receipt_status"],
            "command_executed": receipt["command_executed"], "receipt_finalized": receipt["receipt_finalized"],
            "receipt_digest": receipt[source.RECEIPT_DIGEST_KEY],
        },
        "source_approval_summary": {"approval_digest": source.SOURCE_APPROVAL_DIGEST, "selected_package": SELECTED_PACKAGE},
        "source_failure_diagnosis_summary": {
            "diagnosis_digest": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
            "prior_blocked_reason": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"],
            "primary_failure_class": SOURCE_BINDINGS["source_primary_failure_class"],
            "secondary_failure_class": SOURCE_BINDINGS["source_secondary_failure_class"],
        },
        "source_planning_and_detail_binding_summary": {
            key: SOURCE_BINDINGS[key] for key in (
                "source_results_review_digest", "source_prioritized_planning_digest",
                "source_planning_execution_digest", "source_detail_binding_results_review_digest",
                "source_complete_29_row_binding_digest", "source_materialized_payload_digest",
                "source_recovery_detail_digest", "source_module_grouping_digest",
            )
        },
        "controlled_recapture_result_review": {
            "controlled_recapture_execution_performed": execution["controlled_recapture_execution_performed"],
            "diagnostic_command_executed": execution["diagnostic_command_executed_in_execution"],
            "diagnostic_output_captured": execution["diagnostic_output_captured_in_execution"],
            "targeted_pytest_performed": execution["targeted_pytest_performed"],
            "command_is_retry": execution["controlled_recapture_command_is_retry"],
            "command_is_full_pytest": execution["controlled_recapture_command_is_full_pytest"],
            "cacheprovider_disabled": execution["controlled_recapture_command_used_cacheprovider_disabled"],
            "python_executable": command["python_executable"], "cwd": command["cwd"],
            "target_modules": deepcopy(command["target_modules"]), **deepcopy(result),
            "nonzero_exit_code_is_diagnostic_evidence_only": result["exit_code"] != 0,
        },
        "durable_receipt_review": {
            "scaffold_prewritten": execution["durable_receipt_scaffold_prewritten"],
            "finalized": execution["durable_receipt_finalized"], "retained": execution["durable_receipt_retained"],
            "receipt_status": receipt["receipt_status"], "receipt_digest_verified": True,
        },
        "diagnostic_output_capture_review": {
            "output_captured": True, "full_streams_stored": False, "full_stream_hashes_reviewed": True,
            "stdout_sha256": result["stdout_sha256"], "stderr_sha256": result["stderr_sha256"],
            "stdout_byte_count": result["stdout_byte_count"], "stderr_byte_count": result["stderr_byte_count"],
            "combined_output_byte_count": result["combined_output_byte_count"],
        },
        "bounded_output_review": {
            "bounded_excerpts_stored": True, "maximum_stdout_excerpt_chars": 20000,
            "maximum_stderr_excerpt_chars": 20000,
            "stdout_excerpt_truncated": result["stdout_excerpt_truncated"],
            "stderr_excerpt_truncated": result["stderr_excerpt_truncated"],
        },
        "redaction_review": deepcopy(execution["redaction_summary"]),
        "post_execution_boundary_review": {"reviewed": True, "checks": deepcopy(execution["post_execution_boundary_checks"]), "boundary_errors": receipt.get("post_execution_boundary_errors", [])},
        "unsupported_claims_boundary_review": {
            "failure_error_separation_supported": False, "first_failure_supported": False,
            "first_error_supported": False, "traceback_root_cause_supported": False,
            "direct_remediation_supported": False, "retry_success_supported": False,
            "integration_success_supported": False, "main_merge_readiness_supported": False,
        },
        "review_findings": deepcopy(REVIEW_FINDINGS), "review_outputs": deepcopy(REVIEW_OUTPUTS),
        "recommendation": {"recommended_next_task": NEXT_TASK, "recommended_next_task_status": NEXT_TASK_STATUS, "recommended_action": RECOMMENDED_ACTION, "reason": RECOMMENDATION_REASON},
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    review.update({field: True for field in TRUE_FIELDS})
    review.update({field: False for field in FALSE_FIELDS})
    review[PAYLOAD_REVIEW_DIGEST_KEY] = semantic_digest(_payload_review(review))
    review[DURABLE_RECEIPT_REVIEW_DIGEST_KEY] = semantic_digest(review["durable_receipt_review"])
    review["digest_manifest"] = {
        "source_execution": SOURCE_EXECUTION_DIGEST, "source_payload": SOURCE_PAYLOAD_DIGEST,
        "source_receipt": SOURCE_RECEIPT_DIGEST, "source_digest_manifest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "payload_review": review[PAYLOAD_REVIEW_DIGEST_KEY],
        "durable_receipt_review": review[DURABLE_RECEIPT_REVIEW_DIGEST_KEY],
        "review_outputs": semantic_digest(REVIEW_OUTPUTS), "risk_controls": semantic_digest(RISK_CONTROLS),
    }
    review[RESULTS_REVIEW_MANIFEST_DIGEST_KEY] = semantic_digest(review["digest_manifest"])
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    review[RESULTS_REVIEW_DIGEST_KEY] = _review_digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(review: dict) -> dict:
    """Validate a complete offline results-review artifact."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError
    if not isinstance(review, dict):
        raise error("review must be an object")
    exact = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION, "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE, "created_offline": True, "governance_only": True,
        "results_review_only": True, "source_execution_artifact_kind": source.ARTIFACT_KIND_SUCCESS,
        "source_execution_status": source.EXECUTION_STATUS_SUCCESS, "source_execution_scope": source.EXECUTION_SCOPE,
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_receipt_recovery_or_recapture_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_receipt_recovery_or_recapture_payload_digest": SOURCE_PAYLOAD_DIGEST,
        "source_receipt_recovery_or_recapture_receipt_digest": SOURCE_RECEIPT_DIGEST,
        "source_receipt_recovery_or_recapture_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_durable_receipt_path": SOURCE_DURABLE_RECEIPT_PATH,
        "selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        **SOURCE_BINDINGS, "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "priority_1_target_modules": PRIORITY_1_TARGET_MODULES,
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
    }
    for field, expected in exact.items():
        if review.get(field) != expected:
            raise error(f"{field} mismatch")
    if review.get("retry_failure_context", {}).get("counts") != {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}:
        raise error("retry failure counts mismatch")
    if any(review.get(field) is not True for field in TRUE_FIELDS):
        raise error("required review fact missing")
    if any(review.get(field) is not False for field in FALSE_FIELDS):
        raise error("closed boundary opened")
    result = review.get("controlled_recapture_result_review", {})
    expected_result = {
        "controlled_recapture_execution_performed": True, "diagnostic_command_executed": True,
        "diagnostic_output_captured": True, "targeted_pytest_performed": True,
        "command_is_retry": False, "command_is_full_pytest": False, "cacheprovider_disabled": True,
        "python_executable": str(source.APPROVED_PYTHON_EXECUTABLE), "cwd": str(source.APPROVED_WORKING_DIRECTORY),
        "target_modules": source.TARGET_MODULES, "exit_code": 1, "duration_seconds": "21.584361",
        "stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "stdout_byte_count": 1231380, "stderr_byte_count": 0, "combined_output_byte_count": 1231380,
        "stdout_excerpt_truncated": True, "stderr_excerpt_truncated": False,
        "nonzero_exit_code_is_diagnostic_evidence_only": True,
    }
    if result != expected_result:
        raise error("controlled recapture result mismatch")
    receipt = review.get("durable_receipt_review", {})
    if receipt != {"scaffold_prewritten": True, "finalized": True, "retained": True, "receipt_status": "FINALIZED_AFTER_COMMAND", "receipt_digest_verified": True}:
        raise error("durable receipt review mismatch")
    if review.get("redaction_review", {}).get("redaction_checked") is not True:
        raise error("redaction review missing")
    if review.get("post_execution_boundary_review", {}).get("reviewed") is not True or review["post_execution_boundary_review"].get("boundary_errors") != []:
        raise error("post execution boundary review mismatch")
    if review.get("review_findings") != REVIEW_FINDINGS or review.get("review_outputs") != REVIEW_OUTPUTS:
        raise error("review content mismatch")
    if review.get("recommendation") != {"recommended_next_task": NEXT_TASK, "recommended_next_task_status": NEXT_TASK_STATUS, "recommended_action": RECOMMENDED_ACTION, "reason": RECOMMENDATION_REASON}:
        raise error("recommendation mismatch")
    if review.get("next_chain") != NEXT_CHAIN or review.get("next_gates") != NEXT_GATES or review.get("risk_controls") != RISK_CONTROLS:
        raise error("governance structure mismatch")
    if review.get("predictive_usefulness") != NOT_ACCEPTED or review.get("profitability") != NOT_ACCEPTED:
        raise error("acceptance boundary changed")
    if any(review.get(field) != NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")):
        raise error("runtime boundary changed")
    if review.get(PAYLOAD_REVIEW_DIGEST_KEY) != semantic_digest(_payload_review(review)):
        raise error("payload review digest mismatch")
    if review.get(DURABLE_RECEIPT_REVIEW_DIGEST_KEY) != semantic_digest(review["durable_receipt_review"]):
        raise error("durable receipt review digest mismatch")
    expected_manifest = {
        "source_execution": SOURCE_EXECUTION_DIGEST, "source_payload": SOURCE_PAYLOAD_DIGEST,
        "source_receipt": SOURCE_RECEIPT_DIGEST, "source_digest_manifest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "payload_review": review[PAYLOAD_REVIEW_DIGEST_KEY],
        "durable_receipt_review": review[DURABLE_RECEIPT_REVIEW_DIGEST_KEY],
        "review_outputs": semantic_digest(REVIEW_OUTPUTS), "risk_controls": semantic_digest(RISK_CONTROLS),
    }
    if review.get("digest_manifest") != expected_manifest or review.get(RESULTS_REVIEW_MANIFEST_DIGEST_KEY) != semantic_digest(expected_manifest):
        raise error("results review manifest digest mismatch")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if review.get("summary") != _summary(review):
        raise error("summary mismatch")
    digest = review.get(RESULTS_REVIEW_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _review_digest(review):
        raise error("results review digest mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "results_review_digest": digest,
        **{field: review["summary"][field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(
    output_dir: str | Path, *, source_execution: dict | None = None, durable_receipt_path: str | Path | None = None,
) -> dict:
    """Write deterministic review JSON outside protected runtime paths."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(source_execution=source_execution, durable_receipt_path=durable_receipt_path)
    path = output / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError("output exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS, "results_review_digest": review[RESULTS_REVIEW_DIGEST_KEY], "payload_sha256": sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_markdown_v1(review: dict) -> str:
    """Render a compact review summary after validation."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(review)
    sections = [
        ("Source Receipt Recovery or Controlled Recapture Execution", [SOURCE_EXECUTION_COMMIT, SOURCE_EXECUTION_DIGEST]),
        ("Source Durable Receipt", [SOURCE_DURABLE_RECEIPT_PATH, SOURCE_RECEIPT_DIGEST]),
        ("Source Approval and Operator Review", [source.SOURCE_APPROVAL_DIGEST, source.source.SOURCE_OPERATOR_REVIEW_DIGEST]),
        ("Source Execution Failure Diagnosis", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"], SOURCE_BINDINGS["source_primary_failure_class"]]),
        ("Source Planning and Detail Binding Evidence", [SOURCE_BINDINGS["source_results_review_digest"], SOURCE_BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the failed retry remains authoritative."]),
        ("Review Scope", [REVIEW_SCOPE]), ("Priority 1 Target Modules", source.TARGET_MODULES),
        ("Controlled Recapture Result Review", [str(review["controlled_recapture_result_review"])]),
        ("Durable Receipt Review", [str(review["durable_receipt_review"])]),
        ("Diagnostic Output Capture Review", [str(review["diagnostic_output_capture_review"])]),
        ("Bounded Output Review", [str(review["bounded_output_review"])]),
        ("Redaction Review", [str(review["redaction_review"])]),
        ("Post-Execution Boundary Review", [str(review["post_execution_boundary_review"])]),
        ("Unsupported Claims Boundary", [str(review["unsupported_claims_boundary_review"])]),
        ("Review Findings", list(review["review_findings"].values())),
        ("Recommendation", [RECOMMENDED_ACTION, RECOMMENDATION_REASON]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Results review only; no recapture, remediation, retry, main, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["No command, pytest, cache read, log parse, remediation, classification, provider, data, runtime, or trading action."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Receipt Recovery or Recapture Results Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_ONLY_NOT_RECAPTURE_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE

__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE", "SCHEMA_VERSION", "SOURCE_EXECUTION_COMMIT",
    "SOURCE_EXECUTION_DIGEST", "SOURCE_PAYLOAD_DIGEST", "SOURCE_RECEIPT_DIGEST",
    "SOURCE_DIGEST_MANIFEST_DIGEST", "SOURCE_DURABLE_RECEIPT_PATH", "SELECTED_PACKAGE", "SOURCE_BINDINGS",
    "RESULTS_REVIEW_DIGEST_KEY", "PAYLOAD_REVIEW_DIGEST_KEY", "DURABLE_RECEIPT_REVIEW_DIGEST_KEY",
    "RESULTS_REVIEW_MANIFEST_DIGEST_KEY", "REVIEW_OUTPUTS", "REVIEW_FINDINGS", "NEXT_TASK", "NEXT_CHAIN",
    "NEXT_GATES", "RISK_CONTROLS", "TRUE_FIELDS", "FALSE_FIELDS",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_ONLY_NOT_RECAPTURE_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_markdown_v1",
]
