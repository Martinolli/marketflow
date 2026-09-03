"""Diagnose the blocked targeted diagnostic-output capture receipt offline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_V1"
DIAGNOSIS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_READY"
DIAGNOSIS_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1"
DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"
SOURCE_EXECUTION_DIGEST = "587a13409b9654639f2282eb0c0b55c4270ba7f1cc25ad97ad7adec6630ca21d"
SOURCE_BLOCKED_MANIFEST_DIGEST = "cfd72e69861ebbdde2a290c2d9266fbc9dfd51fc8f0fcb4b8ebe5175adaeb236"
SOURCE_BLOCKED_REASON = "POST_CAPTURE_ARTIFACT_REPORTING_BOUNDARY_FAILED"
PRIMARY_FAILURE_CLASS = "POST_CAPTURE_DURABLE_SUCCESS_RECEIPT_LOSS_AFTER_SINGLE_PERMITTED_DIAGNOSTIC_RUN"
SECONDARY_FAILURE_CLASS = "OUTER_REPORTING_WRAPPER_NAMEERROR_AFTER_TRANSIENT_SERVICE_SUCCESS"
RETRY_EXECUTION_BRANCH = "feature/marketflow-repository-integration-branch-retry-execution-v1"
RETRY_PYTEST_WORKING_DIRECTORY = r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
RECOMMENDED_PACKAGE = "PACKAGE_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_CANDIDATE"
NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_V1"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

SOURCE_BINDINGS = {
    "source_targeted_diagnostic_output_capture_execution_digest": SOURCE_EXECUTION_DIGEST,
    "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
    "source_targeted_diagnostic_output_capture_execution_blocked_reason": SOURCE_BLOCKED_REASON,
    **{
        field: deepcopy(value)
        for field, value in source.SOURCE_BINDINGS.items()
        if field.startswith("source_")
    },
}

FINDINGS = {
    "finding_1": "The approved targeted diagnostic command passed all pre-execution checks and was executed exactly once.",
    "finding_2": "The command used the approved Python executable, detached integration worktree cwd, the five approved Priority 1 module paths, and -p no:cacheprovider.",
    "finding_3": "The command was diagnostic capture only and was not the failed retry command, not a full pytest run, and not retry evidence.",
    "finding_4": "The service transiently produced a success artifact with diagnostic command execution, diagnostic output capture, and targeted pytest flags true.",
    "finding_5": "The outer print/reporting wrapper raised NameError after the transient service artifact was returned.",
    "finding_6": "Because the transient success receipt was not durably retained, exit code, duration, stdout/stderr hashes, byte counts, truncation flags, excerpts, redaction summary, success payload digest, and success digest-manifest digest are unavailable.",
    "finding_7": "The execution correctly failed closed and did not reconstruct missing receipt fields.",
    "finding_8": "The failure is a durable receipt/reporting boundary failure, not a diagnostic command precheck failure.",
    "finding_9": "The failure is not classified as wrong cwd, wrong Python, wrong module list, missing module, cache-provider boundary failure, retry rerun, full-pytest execution, provider/data/runtime failure, or Git protected-ref failure.",
    "finding_10": "Post-execution checks preserved the clean detached worktree, unchanged origin/main, unchanged local-only integration branch, no tracked .marketflow, and no tracked .pytest_cache.",
    "finding_11": "The authoritative retry remains 24,877 passed, 1,292 failed, 112 errors, and 7 skipped.",
    "finding_12": "No failure/error separation, first failure, first error, traceback root cause, remediation, retry success, or main-merge readiness can be claimed from the blocked receipt.",
}


def _domain(domain_id: str, classification: str, evidence: str, boundary: str, next_action: bool) -> dict[str, Any]:
    return {
        "domain_id": domain_id, "classification": classification, "evidence_summary": evidence,
        "boundary_status": boundary, "next_action_required": next_action,
    }


DIAGNOSIS_DOMAINS = [
    _domain("approved_package_binding", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "The blocked receipt binds the approved package and approval digest.", "PRESERVED", False),
    _domain("pre_execution_checks", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "All approved pre-execution checks passed.", "PRESERVED", False),
    _domain("diagnostic_command_invocation", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "One command invocation and transient service success were observed.", "SINGLE_RUN_ACKNOWLEDGED", False),
    _domain("diagnostic_cwd_and_python", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "Approved detached CWD and repository Python were used.", "PRESERVED", False),
    _domain("target_module_scope", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "Only the five approved Priority 1 modules were targeted.", "PRESERVED", False),
    _domain("cacheprovider_boundary", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "The command used -p no:cacheprovider and tracked-cache checks stayed clear.", "PRESERVED", False),
    _domain("diagnostic_output_capture", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "Output capture and bounding were transiently validated before receipt loss.", "TRANSIENT_ONLY_NOT_DURABLE", False),
    _domain("durable_success_receipt_persistence", "FAILED_PRIMARY", "The validated success receipt was not durably retained after the single permitted run.", "FAILED_CLOSED", True),
    _domain("outer_reporting_wrapper", "FAILED_CONTRIBUTING", "The outer print wrapper raised NameError after the artifact returned.", "FAILED_CLOSED", True),
    _domain("post_execution_git_boundaries", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "Protected refs, detached cleanliness, and tracked-output exclusions passed after execution.", "PRESERVED", False),
    _domain("unsupported_claim_boundaries", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "No unavailable value or downstream claim was inferred, and no provider, data, runtime, or trading action occurred.", "PRESERVED", False),
    _domain("next_package_direction", "ACTION_REQUIRED_NOT_FAILURE", "A separate recovery-or-controlled-recapture candidate is required.", "SEPARATELY_GATED", True),
]

UNAVAILABLE_FIELDS = [
    "diagnostic_exit_code", "diagnostic_duration_seconds", "stdout_sha256", "stderr_sha256",
    "stdout_byte_count", "stderr_byte_count", "combined_output_byte_count",
    "stdout_excerpt_truncated", "stderr_excerpt_truncated", "bounded_stdout_excerpt",
    "bounded_stderr_excerpt", "redaction_patterns_applied", "success_payload_digest",
    "success_digest_manifest_digest",
]

RECOMMENDATION = {
    "recommended_next_package": RECOMMENDED_PACKAGE,
    "recommended_next_task": NEXT_TASK,
    "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
    "recommended_action": "CREATE_SEPARATE_CANDIDATE_FOR_DURABLE_RECEIPT_RECOVERY_OR_CONTROLLED_SINGLE_RECAPTURE_WITH_PERSISTENCE_GUARDS",
    "reason": "The approved diagnostic command executed once, but the durable success receipt was lost after transient success. A separate candidate is required to decide whether to recover an existing receipt, bind an operator-provided terminal transcript, or approve a controlled recapture with pre-command durable persistence safeguards.",
}

FUTURE_PACKAGES = [
    {"package_id": "PACKAGE_RECOVER_EXISTING_TRANSIENT_SUCCESS_RECEIPT_IF_LOCATABLE", "status": "FUTURE_CANDIDATE_OPTION_NOT_SELECTED", "selected": False, "approved": False},
    {"package_id": "PACKAGE_OPERATOR_PROVIDES_HASH_VERIFIABLE_TERMINAL_TRANSCRIPT", "status": "FUTURE_CANDIDATE_OPTION_NOT_SELECTED", "selected": False, "approved": False},
    {"package_id": "PACKAGE_CONTROLLED_SINGLE_RECAPTURE_WITH_PREWRITE_RECEIPT_FILE_AND_NO_CACHEPROVIDER", "status": "FUTURE_CANDIDATE_OPTION_NOT_SELECTED", "selected": False, "approved": False},
    {"package_id": "PACKAGE_CREATE_COMMAND_MANIFEST_AND_CAPTURE_WRAPPER_FIX_ONLY", "status": "FUTURE_CANDIDATE_OPTION_NOT_SELECTED", "selected": False, "approved": False},
    {"package_id": "PACKAGE_ACCEPT_BLOCKED_RECEIPT_AS_DIAGNOSTIC_SUCCESS", "status": "BLOCKED_NOT_ALLOWED", "selected": False, "approved": False, "blocked_reason": "The durable diagnostic output fields and digests are missing."},
    {"package_id": "PACKAGE_RECONSTRUCT_OUTPUT_HASHES_FROM_MEMORY_OR_SUMMARY", "status": "BLOCKED_NOT_ALLOWED", "selected": False, "approved": False, "blocked_reason": "The transient output payload was not retained and must not be guessed."},
    {"package_id": "PACKAGE_RERUN_WITHOUT_SEPARATE_APPROVAL", "status": "BLOCKED_NOT_ALLOWED", "selected": False, "approved": False, "blocked_reason": "The approved command already executed once; any recapture requires separate governance."},
    {"package_id": "PACKAGE_PROCEED_TO_REMEDIATION_WITHOUT_DIAGNOSTIC_RESULTS_REVIEW", "status": "BLOCKED_NOT_ALLOWED", "selected": False, "approved": False, "blocked_reason": "Remediation or method candidate remains blocked until diagnostic capture evidence is reviewed."},
    {"package_id": "PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_RESULTS_REVIEW", "status": "BLOCKED_NOT_ALLOWED", "selected": False, "approved": False, "blocked_reason": "New retry remains blocked until diagnostic capture, review, and any required remediation/method chain."},
    {"package_id": "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY", "status": "BLOCKED_NOT_ALLOWED", "selected": False, "approved": False, "blocked_reason": "Main merge remains blocked until a future retry results review passes."},
]

NEXT_CHAIN = [
    "Targeted Diagnostic Output Capture Receipt Recovery or Recapture Candidate v1.", "Candidate Operator Review v1.",
    "Approval v1, if selected.", "Receipt Recovery or Controlled Recapture Execution v1, if approved.",
    "Results Review v1.", "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1, if supported by results review.",
    "Remediation or Method Operator Review v1, if needed.", "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.", "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate",
    "targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review",
    "targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_if_selected",
    "targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_if_approved",
    "targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review",
    "retry_failure_remediation_or_method_candidate_after_diagnostic_capture_if_supported",
    "remediation_or_method_operator_review_if_needed", "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved", "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "diagnosis_does_not_rerun_diagnostic_command", "diagnosis_does_not_run_targeted_pytest",
    "diagnosis_does_not_run_full_pytest", "diagnosis_does_not_rerun_retry", "diagnosis_does_not_read_cache",
    "diagnosis_does_not_modify_cache", "diagnosis_does_not_reconstruct_missing_stdout_hashes",
    "diagnosis_does_not_reconstruct_missing_stderr_hashes", "diagnosis_does_not_reconstruct_missing_exit_code",
    "diagnosis_does_not_infer_missing_diagnostic_payload", "diagnosis_does_not_parse_operator_logs",
    "diagnosis_does_not_inspect_env", "diagnosis_does_not_execute_remediation",
    "diagnosis_does_not_execute_classification", "diagnosis_does_not_classify_modules_again",
    "diagnosis_does_not_identify_first_failure", "diagnosis_does_not_identify_first_error",
    "diagnosis_does_not_claim_traceback_root_cause", "diagnosis_does_not_recommend_direct_code_remediation",
    "diagnosis_does_not_create_diagnostic_results_review", "diagnosis_does_not_create_remediation_or_method_candidate",
    "diagnosis_does_not_create_new_retry_candidate", "diagnosis_does_not_create_retry_results_review",
    "diagnosis_does_not_create_integration_results_review", "diagnosis_does_not_mark_integration_successful",
    "diagnosis_does_not_generate_successful_integration_digest", "diagnosis_does_not_treat_transient_success_as_durable_success",
    "diagnosis_does_not_treat_diagnostic_run_as_retry", "diagnosis_does_not_push_integration_branch",
    "diagnosis_does_not_push_main", "diagnosis_does_not_delete_integration_branch",
    "diagnosis_does_not_delete_worktree", "diagnosis_does_not_force_push", "diagnosis_does_not_prune_remotes",
    "diagnosis_does_not_modify_tags", "diagnosis_does_not_modify_staged_evidence", "diagnosis_does_not_regenerate_evidence",
    "diagnosis_does_not_call_providers", "diagnosis_does_not_acquire_market_data", "diagnosis_does_not_regenerate_dataset",
    "diagnosis_does_not_recompute_metrics", "diagnosis_does_not_train_models", "diagnosis_does_not_score_strategy",
    "diagnosis_does_not_generate_recommendations", "diagnosis_does_not_accept_predictive_usefulness",
    "diagnosis_does_not_accept_profitability", "diagnosis_does_not_authorize_runtime",
    "diagnosis_does_not_authorize_broker_execution", "blocked_execution_remains_historically_blocked",
    "single_permitted_diagnostic_run_acknowledged_but_not_accepted_as_durable_success",
    "receipt_loss_requires_separate_candidate_before_recovery_or_recapture",
    "future_recapture_requires_separate_operator_review_and_approval",
    "future_diagnostic_results_review_required_before_remediation_or_method_candidate",
    "future_diagnostic_capture_is_not_retry_success", "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation", "previous_approval_remains_source_evidence",
    "previous_operator_review_remains_source_evidence", "previous_candidate_remains_source_evidence",
    "previous_planning_results_review_remains_valid", "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "diagnosis_created", "diagnosis_ready", "diagnostic_command_executed_once",
    "transient_success_artifact_returned", "ready_for_receipt_recovery_or_recapture_candidate",
]
FALSE_FIELDS = [
    "durable_success_receipt_retained", "diagnostic_exit_code_available", "diagnostic_duration_available",
    "stdout_hash_available", "stderr_hash_available", "bounded_excerpts_available", "redaction_summary_available",
    "success_payload_digest_available", "success_digest_manifest_digest_available",
    "unavailable_values_reconstructed", "unavailable_values_inferred", "diagnostic_command_rerun_to_recover_values",
    "targeted_pytest_rerun_performed", "full_pytest_performed", "retry_rerun_performed", "cache_read_in_diagnosis",
    "cache_modified_in_diagnosis", "operator_logs_parsed", "env_inspection_performed",
    "diagnostic_results_review_created", "remediation_or_method_candidate_created", "new_retry_candidate_created",
    "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "classification_execution_performed", "remediation_execution_performed", "failure_modules_classified",
    "error_modules_classified", "failure_error_separation_claimed", "first_failure_identified",
    "first_error_identified", "first_order_claim_made", "traceback_root_cause_claimed",
    "direct_code_remediation_recommended", "retry_success_claimed", "main_merge_readiness_claimed",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
    "evidence_regenerated", "provider_requests_made_in_diagnosis", "market_data_acquisition_performed_in_diagnosis",
    "dataset_generation_performed_in_diagnosis", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
    "ready_for_diagnostic_results_review", "ready_for_remediation_or_method_candidate", "ready_for_retry_candidate",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError(ValueError):
    """Raised when the offline diagnosis expands or corrupts its evidence."""


def _expected_source_execution() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND_BLOCKED, "execution_status": source.EXECUTION_STATUS_BLOCKED,
        "execution_scope": source.EXECUTION_SCOPE, source.EXECUTION_DIGEST_KEY: SOURCE_EXECUTION_DIGEST,
        source.BLOCKED_MANIFEST_DIGEST_KEY: SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason": SOURCE_BLOCKED_REASON, "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "targeted_diagnostic_output_capture_execution_created": True,
        "targeted_diagnostic_output_capture_execution_performed": False,
        "diagnostic_capture_execution_performed": False, "diagnostic_command_executed": False,
        "diagnostic_output_captured": False, "targeted_pytest_performed": False,
    }


def _bind_source_execution(value: Mapping[str, Any] | None) -> dict[str, Any]:
    expected = _expected_source_execution()
    if value is None:
        return deepcopy(expected)
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("source execution must be an object")
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError(f"source execution {field} mismatch")
    return deepcopy(dict(value))


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(diagnosis: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_checks = {
        "source_targeted_diagnostic_output_capture_execution_digest": "source_execution_digest_bound",
        "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest": "source_blocked_manifest_digest_bound",
        "source_targeted_diagnostic_output_capture_execution_blocked_reason": "source_blocked_reason_bound",
        "source_targeted_diagnostic_output_capture_approval_digest": "source_approval_digest_bound",
        "source_targeted_diagnostic_output_capture_candidate_operator_review_digest": "source_operator_review_digest_bound",
        "source_targeted_diagnostic_output_capture_candidate_digest": "source_candidate_digest_bound",
        "source_results_review_digest": "source_results_review_digest_bound",
        "source_prioritized_planning_review_digest": "source_prioritized_planning_review_digest_bound",
        "source_results_review_manifest_digest": "source_results_review_manifest_digest_bound",
        "source_planning_execution_digest": "source_planning_execution_digest_bound",
        "source_prioritized_planning_digest": "source_prioritized_planning_digest_bound",
        "source_planning_digest_manifest_digest": "source_planning_digest_manifest_digest_bound",
        "source_detail_binding_results_review_digest": "source_detail_binding_results_review_digest_bound",
        "source_complete_29_row_binding_digest": "source_complete_29_row_binding_digest_bound",
        "source_materialized_payload_digest": "source_materialized_payload_digest_bound",
        "source_detail_binding_approval_digest": "source_detail_binding_approval_digest_bound",
        "source_recovery_results_review_digest": "source_recovery_results_review_digest_bound",
        "source_recovery_detail_digest": "source_recovery_detail_digest_bound",
        "source_after_v2_approval_digest": "source_after_v2_approval_digest_bound",
        "source_module_grouping_digest": "source_module_grouping_digest_bound",
    }
    checks = [_check(check_id, SOURCE_BINDINGS[field], diagnosis.get(field)) for field, check_id in source_checks.items()]
    checks.extend([
        _check("retry_execution_commit_bound", source.RETRY_EXECUTION_COMMIT, diagnosis.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, diagnosis.get("retry_failure_counts")),
        _check("priority_1_top_module_paths_bound", source.TARGET_MODULES, [item.get("module_path") for item in diagnosis.get("priority_1_top_module_groups", [])]),
        _check("priority_1_total_612_bound", 612, diagnosis.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, diagnosis.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, diagnosis.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, diagnosis.get("failed_or_errored_nodeids_count")),
        _check("diagnosis_created_true", True, diagnosis.get("diagnosis_created")),
        _check("diagnosis_ready_true", True, diagnosis.get("diagnosis_ready")),
        _check("primary_failure_class_bound", PRIMARY_FAILURE_CLASS, diagnosis.get("primary_failure_class")),
        _check("secondary_failure_class_bound", SECONDARY_FAILURE_CLASS, diagnosis.get("secondary_failure_class")),
        _check("diagnostic_command_executed_once_acknowledged", True, diagnosis.get("diagnostic_command_executed_once")),
        _check("transient_success_acknowledged", True, diagnosis.get("transient_success_artifact_returned")),
        _check("durable_success_receipt_missing", False, diagnosis.get("durable_success_receipt_retained")),
        _check("exit_code_unavailable_recorded", False, diagnosis.get("diagnostic_exit_code_available")),
        _check("stdout_hash_unavailable_recorded", False, diagnosis.get("stdout_hash_available")),
        _check("stderr_hash_unavailable_recorded", False, diagnosis.get("stderr_hash_available")),
        _check("bounded_excerpts_unavailable_recorded", False, diagnosis.get("bounded_excerpts_available")),
        _check("redaction_summary_unavailable_recorded", False, diagnosis.get("redaction_summary_available")),
        _check("success_payload_digest_unavailable_recorded", False, diagnosis.get("success_payload_digest_available")),
        _check("success_digest_manifest_unavailable_recorded", False, diagnosis.get("success_digest_manifest_digest_available")),
        _check("recommended_next_package_defined", RECOMMENDED_PACKAGE, diagnosis.get("recommended_next_package")),
    ])
    aliases = {
        "unavailable_values_reconstructed": "missing_values_not_reconstructed",
        "unavailable_values_inferred": "missing_values_not_inferred",
        "diagnostic_command_rerun_to_recover_values": "diagnostic_command_not_rerun",
        "targeted_pytest_rerun_performed": "targeted_pytest_not_rerun",
        "full_pytest_performed": "full_pytest_false", "retry_rerun_performed": "retry_rerun_false",
        "cache_read_in_diagnosis": "cache_read_false", "cache_modified_in_diagnosis": "cache_modified_false",
        "operator_logs_parsed": "operator_logs_not_parsed", "env_inspection_performed": "env_inspection_false",
        "diagnostic_results_review_created": "diagnostic_results_review_created_false",
        "remediation_or_method_candidate_created": "remediation_or_method_candidate_created_false",
        "classification_execution_performed": "classification_execution_false",
        "remediation_execution_performed": "remediation_execution_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "main_push_performed": "main_push_false", "origin_main_modified_by_this_task": "origin_main_modified_false",
        "provider_requests_made_in_diagnosis": "provider_requests_false",
        "market_data_acquisition_performed_in_diagnosis": "market_data_acquisition_false",
        "dataset_generation_performed_in_diagnosis": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    for field in FALSE_FIELDS:
        checks.append(_check(aliases.get(field, f"{field}_false"), False, diagnosis.get(field)))
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, diagnosis.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, diagnosis.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, diagnosis.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, diagnosis.get("broker_execution")),
        _check("next_chain_defined", NEXT_CHAIN, diagnosis.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, diagnosis.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, diagnosis.get("risk_controls")),
        _check("no_tracked_marketflow_files", False, diagnosis.get("marketflow_outputs_committed")),
        _check("no_tracked_pytest_cache_files", False, diagnosis.get("pytest_cache_committed")),
    ])
    return checks


def _summary(diagnosis: Mapping[str, Any]) -> dict[str, Any]:
    checklist = diagnosis.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed, "diagnosis_created": True, "diagnosis_ready": True,
        "primary_failure_class": PRIMARY_FAILURE_CLASS, "secondary_failure_class": SECONDARY_FAILURE_CLASS,
        "source_execution_blocked_reason": SOURCE_BLOCKED_REASON,
        **{field: diagnosis.get(field) for field in (
            "diagnostic_command_executed_once", "transient_success_artifact_returned",
            "durable_success_receipt_retained", "diagnostic_exit_code_available", "stdout_hash_available",
            "stderr_hash_available", "bounded_excerpts_available", "success_payload_digest_available",
            "success_digest_manifest_digest_available", "unavailable_values_reconstructed",
            "unavailable_values_inferred", "diagnostic_command_rerun_to_recover_values",
            "ready_for_receipt_recovery_or_recapture_candidate", "ready_for_diagnostic_results_review",
            "ready_for_remediation_or_method_candidate", "ready_for_retry_candidate",
            "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
        )},
        "recommended_next_task": NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _diagnosis_digest(diagnosis: Mapping[str, Any]) -> str:
    value = deepcopy(dict(diagnosis))
    for field in ("checklist", "summary", DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(
    *, source_execution: dict | None = None,
) -> dict:
    """Build the offline receipt-loss diagnosis without rerunning execution."""

    bound_source = _bind_source_execution(source_execution)
    diagnosis: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "diagnosis_status": DIAGNOSIS_STATUS, "diagnosis_scope": DIAGNOSIS_SCOPE,
        "created_offline": True, "governance_only": True, "diagnosis_only": True,
        "source_execution_artifact_kind": source.ARTIFACT_KIND_BLOCKED,
        "source_execution_status": source.EXECUTION_STATUS_BLOCKED,
        "source_execution_scope": source.EXECUTION_SCOPE,
        **deepcopy(SOURCE_BINDINGS),
        "source_execution_summary": bound_source,
        "primary_failure_class": PRIMARY_FAILURE_CLASS, "secondary_failure_class": SECONDARY_FAILURE_CLASS,
        "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "retry_execution_branch": RETRY_EXECUTION_BRANCH,
        "retry_execution_commit": source.RETRY_EXECUTION_COMMIT,
        "retry_pytest_working_directory": RETRY_PYTEST_WORKING_DIRECTORY,
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "retry_failure_counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "retry_pytest_first_result_authoritative": True, "retry_pytest_passed": False,
        "retry_pytest_failed": True,
        "root_full_regression_is_retry_evidence": False,
        "priority_1_top_module_groups": deepcopy(source.source.source.source.TOP_MODULES),
        "priority_1_total_nodeids": 612, "priority_1_percentage": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "diagnosis_findings": deepcopy(FINDINGS), "failure_classification_domains": deepcopy(DIAGNOSIS_DOMAINS),
        "unavailable_due_to_receipt_loss": list(UNAVAILABLE_FIELDS),
        **deepcopy(RECOMMENDATION), "possible_future_packages": deepcopy(FUTURE_PACKAGES),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    diagnosis.update({field: True for field in TRUE_FIELDS})
    diagnosis.update({field: False for field in FALSE_FIELDS})
    diagnosis["checklist"] = _checklist(diagnosis)
    diagnosis["summary"] = _summary(diagnosis)
    diagnosis[DIGEST_KEY] = _diagnosis_digest(diagnosis)
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(diagnosis)
    return diagnosis


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(diagnosis: dict) -> dict:
    """Reject source drift, reconstructed data, execution, or authority expansion."""

    if not isinstance(diagnosis, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("diagnosis must be an object")
    constants = {
        **SOURCE_BINDINGS,
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "diagnosis_status": DIAGNOSIS_STATUS, "diagnosis_scope": DIAGNOSIS_SCOPE,
        "created_offline": True, "governance_only": True, "diagnosis_only": True,
        "source_execution_artifact_kind": source.ARTIFACT_KIND_BLOCKED,
        "source_execution_status": source.EXECUTION_STATUS_BLOCKED,
        "source_execution_scope": source.EXECUTION_SCOPE,
        "primary_failure_class": PRIMARY_FAILURE_CLASS, "secondary_failure_class": SECONDARY_FAILURE_CLASS,
        "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "retry_execution_branch": RETRY_EXECUTION_BRANCH,
        "retry_execution_commit": source.RETRY_EXECUTION_COMMIT,
        "retry_pytest_working_directory": RETRY_PYTEST_WORKING_DIRECTORY,
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "retry_pytest_first_result_authoritative": True,
        "retry_pytest_passed": False,
        "retry_pytest_failed": True,
        "root_full_regression_is_retry_evidence": False,
        "priority_1_total_nodeids": 612, "priority_1_percentage": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
    }
    for field, expected in constants.items():
        if diagnosis.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError(f"{field} mismatch")
    if diagnosis.get("retry_failure_counts") != {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("retry failure counts mismatch")
    if diagnosis.get("priority_1_top_module_groups") != source.source.source.source.TOP_MODULES:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("Priority 1 modules mismatch")
    structures = {
        "diagnosis_findings": FINDINGS, "failure_classification_domains": DIAGNOSIS_DOMAINS,
        "unavailable_due_to_receipt_loss": UNAVAILABLE_FIELDS, "possible_future_packages": FUTURE_PACKAGES,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected in structures.items():
        if diagnosis.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError(f"{field} mismatch")
    for field, expected in RECOMMENDATION.items():
        if diagnosis.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError(f"{field} mismatch")
    if any(diagnosis.get(field) is not True for field in TRUE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("diagnosis fact missing")
    if any(diagnosis.get(field) is not False for field in FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("closed boundary opened")
    if diagnosis.get("predictive_usefulness") != NOT_ACCEPTED or diagnosis.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("acceptance boundary changed")
    if any(diagnosis.get(field) != NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("runtime boundary changed")
    checklist = _checklist(diagnosis)
    if diagnosis.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("checklist mismatch")
    if diagnosis.get("summary") != _summary(diagnosis):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("summary mismatch")
    digest = diagnosis.get(DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _diagnosis_digest(diagnosis):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("diagnosis digest mismatch")
    return {
        "artifact_kind": diagnosis["artifact_kind"], "diagnosis_status": diagnosis["diagnosis_status"],
        "diagnosis_scope": diagnosis["diagnosis_scope"], "diagnosis_digest": digest,
        **{field: diagnosis["summary"][field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(
    output_dir: str | Path, *, source_execution: dict | None = None,
) -> dict:
    """Write deterministic diagnosis JSON outside protected runtime paths."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("protected output directory")
    diagnosis = build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(source_execution=source_execution)
    path = output / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError("output exists")
    payload = canonical_json_bytes(diagnosis)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": ARTIFACT_KIND, "diagnosis_status": DIAGNOSIS_STATUS, "diagnosis_digest": diagnosis[DIGEST_KEY], "payload_sha256": sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_markdown_v1(diagnosis: dict) -> str:
    """Render the validated diagnosis as Markdown."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(diagnosis)
    sections = [
        ("Source Targeted Diagnostic Output Capture Execution", [SOURCE_EXECUTION_DIGEST, SOURCE_BLOCKED_MANIFEST_DIGEST, SOURCE_BLOCKED_REASON]),
        ("Source Approval and Operator Review", [source.SOURCE_APPROVAL_DIGEST, source.source.SOURCE_OPERATOR_REVIEW_DIGEST]),
        ("Source Planning and Detail Binding Evidence", [source.SOURCE_BINDINGS["source_planning_execution_digest"], source.SOURCE_BINDINGS["source_complete_29_row_binding_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; still authoritative."]),
        ("Diagnosis Scope", [DIAGNOSIS_SCOPE]),
        ("Execution Failure Summary", [PRIMARY_FAILURE_CLASS, SECONDARY_FAILURE_CLASS]),
        ("Transient Success and Durable Receipt Loss", [FINDINGS["finding_4"], FINDINGS["finding_5"], FINDINGS["finding_6"]]),
        ("Unavailable Diagnostic Payload Fields", UNAVAILABLE_FIELDS),
        ("Failure Classification Domains", [f"{item['domain_id']}: {item['classification']}" for item in DIAGNOSIS_DOMAINS]),
        ("Unsupported Claims Boundary", [FINDINGS["finding_12"]]),
        ("Recommendation", [RECOMMENDED_PACKAGE, NEXT_TASK]),
        ("Possible Future Packages", [f"{item['package_id']}: {item['status']}" for item in FUTURE_PACKAGES]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Diagnosis only; no recapture, diagnostic, retry, main, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Unavailable receipt values remain unavailable and the diagnostic command is not rerun."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Execution Failure Diagnosis v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_READY = DIAGNOSIS_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN = DIAGNOSIS_SCOPE
PACKAGE_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_CANDIDATE = RECOMMENDED_PACKAGE

__all__ = [
    "ARTIFACT_KIND", "DIAGNOSIS_STATUS", "DIAGNOSIS_SCOPE", "DIGEST_KEY",
    "SOURCE_EXECUTION_DIGEST", "SOURCE_BLOCKED_MANIFEST_DIGEST", "SOURCE_BLOCKED_REASON",
    "PRIMARY_FAILURE_CLASS", "SECONDARY_FAILURE_CLASS", "SELECTED_PACKAGE", "RECOMMENDED_PACKAGE",
    "NEXT_TASK", "SOURCE_BINDINGS", "FINDINGS", "DIAGNOSIS_DOMAINS", "UNAVAILABLE_FIELDS",
    "RECOMMENDATION", "FUTURE_PACKAGES", "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS",
    "TRUE_FIELDS", "FALSE_FIELDS",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN",
    "PACKAGE_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_CANDIDATE",
    "MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1",
    "write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_markdown_v1",
]
