"""Define offline candidate options for recovering or recapturing a diagnostic receipt."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_V1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1"
DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_digest"
SOURCE_DIAGNOSIS_DIGEST = "20ca664e0d673808b8be152589b76ad6f92ef9cb5be55f6c76ce87646baa9935"
RECOMMENDED_PACKAGE = "PACKAGE_CONTROLLED_SINGLE_RECAPTURE_WITH_PREWRITE_RECEIPT_FILE_AND_NO_CACHEPROVIDER"
NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_OPERATOR_REVIEW_V1"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"

SOURCE_BINDINGS = {
    "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest": SOURCE_DIAGNOSIS_DIGEST,
    "source_primary_failure_class": source.PRIMARY_FAILURE_CLASS,
    "source_secondary_failure_class": source.SECONDARY_FAILURE_CLASS,
    **deepcopy(source.SOURCE_BINDINGS),
}

UNAVAILABLE_FIELDS = list(source.UNAVAILABLE_FIELDS)
PRIORITY_1_TARGET_MODULES = [
    {"module_path": "tests/test_marketflow_signal_or_feature_generation_results_review_service.py", "failed_or_errored_nodeid_count": 136},
    {"module_path": "tests/test_post_identity_freeze_registry_inventory_approval_service.py", "failed_or_errored_nodeid_count": 131},
    {"module_path": "tests/test_corporate_action_authority_plan_candidate_service.py", "failed_or_errored_nodeid_count": 122},
    {"module_path": "tests/test_feature_generation_results_review_redesigned_labels_service.py", "failed_or_errored_nodeid_count": 112},
    {"module_path": "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py", "failed_or_errored_nodeid_count": 111},
]

CANDIDATE_PHILOSOPHY = {
    "receipt_recovery_or_recapture_candidate_philosophy": "The approved targeted diagnostic command executed once and transiently succeeded, but the durable success receipt was lost by a post-capture reporting wrapper failure. The next safe step is to define governed options for either recovering an already-existing durable receipt, binding a hash-verifiable operator-provided transcript, or approving a controlled single recapture with pre-command persistence safeguards. The candidate must not rerun diagnostics, reconstruct missing values, infer output hashes, or proceed to remediation/retry without reviewed diagnostic evidence.",
    "candidate_boundary": "Candidate-only; no receipt recovery, recapture, diagnostic command, targeted pytest, remediation, classification, retry, results review, main merge, runtime, or trading authority is created.",
    "candidate_goal": "Define safe future packages to recover or recapture durable diagnostic evidence after receipt loss.",
}

PROPOSED_PACKAGES = [
    {"package_id": "PACKAGE_RECOVER_EXISTING_TRANSIENT_SUCCESS_RECEIPT_IF_LOCATABLE", "status": "AVAILABLE_FOR_OPERATOR_REVIEW_LOW_CONFIDENCE_NOT_SELECTED", "purpose": "Future execution may search only explicitly approved, non-secret, bounded, local committed-or-designated receipt locations for an already persisted success receipt, without parsing operator logs, shell history, .env, cache files, or unbounded terminal buffers.", "selected": False, "approved": False, "executed": False},
    {"package_id": "PACKAGE_OPERATOR_PROVIDES_HASH_VERIFIABLE_TERMINAL_TRANSCRIPT", "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "purpose": "Future execution may bind an operator-provided diagnostic transcript only if it is explicit, hash-verifiable, bounded, redacted, and contains command, cwd, target modules, exit code, stdout/stderr evidence, and timestamps sufficient for review.", "selected": False, "approved": False, "executed": False},
    {"package_id": RECOMMENDED_PACKAGE, "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED", "purpose": "Future execution may perform one controlled recapture of the approved five-module diagnostic command only after prewriting a durable receipt scaffold, verifying source digests and boundaries, using the detached integration worktree, using the approved Python executable, using -p no:cacheprovider, bounding output, hashing full streams, redacting secret-like patterns, and preserving the failed retry as authoritative.", "recommended_reason": "The diagnosis shows the diagnostic command execution path passed and transiently returned success, but the durable receipt was lost after capture. The strongest mitigation is a controlled single recapture with persistence-before-reporting safeguards and no cacheprovider.", "selected": False, "approved": False, "executed": False},
    {"package_id": "PACKAGE_CREATE_COMMAND_MANIFEST_AND_CAPTURE_WRAPPER_FIX_ONLY", "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "purpose": "Future execution may create a command manifest and wrapper-hardening plan only, without recapture.", "selected": False, "approved": False, "executed": False},
    {"package_id": "PACKAGE_RECOVER_FROM_UNBOUNDED_TERMINAL_BUFFER_OR_SHELL_HISTORY", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "Unbounded terminal buffers or shell history are not controlled diagnostic evidence and may contain unrelated or sensitive information.", "selected": False, "approved": False, "executed": False},
    {"package_id": "PACKAGE_ACCEPT_BLOCKED_RECEIPT_AS_DIAGNOSTIC_SUCCESS", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "The durable diagnostic output fields and success digests are missing.", "selected": False, "approved": False, "executed": False},
    {"package_id": "PACKAGE_RECONSTRUCT_OUTPUT_HASHES_FROM_MEMORY_OR_SUMMARY", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "The transient output payload was not retained and must not be guessed, inferred, or reconstructed.", "selected": False, "approved": False, "executed": False},
    {"package_id": "PACKAGE_RERUN_WITHOUT_SEPARATE_APPROVAL", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "The approved command already executed once; any recapture requires separate operator review and approval.", "selected": False, "approved": False, "executed": False},
    {"package_id": "PACKAGE_PROCEED_TO_REMEDIATION_WITHOUT_DIAGNOSTIC_RESULTS_REVIEW", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "Remediation or method candidate remains blocked until diagnostic capture evidence is reviewed.", "selected": False, "approved": False, "executed": False},
    {"package_id": "PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_RESULTS_REVIEW", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "New retry remains blocked until diagnostic capture, review, and any required remediation or method chain are completed.", "selected": False, "approved": False, "executed": False},
    {"package_id": "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "Main merge remains blocked until a future retry results review passes.", "selected": False, "approved": False, "executed": False},
]

RECOMMENDATION = {
    "recommended_receipt_recovery_or_recapture_package": RECOMMENDED_PACKAGE,
    "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
    "reason": "The diagnosis confirms a single permitted diagnostic run occurred and transiently succeeded, but durable output receipt fields were lost after capture. A controlled single recapture with a prewritten receipt scaffold, cacheprovider disabled, bounded output, stream hashes, redaction, and no retry-success claim is the safest reviewable next package.",
}

FUTURE_REQUIREMENTS = {
    key: True for key in (
        "source_failure_diagnosis_must_be_ready", "source_failure_diagnosis_digest_must_be_bound",
        "source_execution_blocked_digest_must_be_bound", "source_execution_blocked_manifest_must_be_bound",
        "source_blocked_reason_must_be_bound", "source_primary_failure_class_must_be_bound",
        "source_secondary_failure_class_must_be_bound", "source_approval_digest_must_be_bound",
        "source_operator_review_digest_must_be_bound", "source_candidate_digest_must_be_bound",
        "source_planning_results_review_digest_must_be_bound", "source_priority_planning_digest_must_be_bound",
        "source_detail_binding_digest_must_be_bound", "source_materialized_payload_digest_must_be_bound",
        "retry_failure_counts_must_be_bound", "priority_1_top_module_paths_must_be_bound",
        "priority_1_total_must_be_612", "top_10_total_must_be_1069",
        "module_summary_total_must_be_29", "failed_or_errored_nodeids_total_must_be_1404",
        "future_recovery_must_not_reconstruct_missing_values", "future_recovery_must_not_parse_unbounded_logs",
        "future_recovery_must_not_inspect_env", "future_recovery_must_not_read_pytest_cache",
        "future_recovery_must_not_commit_pytest_cache", "future_recovery_must_not_commit_marketflow_outputs",
        "future_recapture_requires_separate_approval", "future_recapture_must_target_priority_1_modules_only",
        "future_recapture_must_use_approved_python_executable", "future_recapture_must_use_detached_worktree_cwd",
        "future_recapture_must_use_cacheprovider_disabled", "future_recapture_must_prewrite_durable_receipt_scaffold",
        "future_recapture_must_capture_command_cwd_exit_code_stdout_stderr_duration",
        "future_recapture_must_hash_full_output_streams", "future_recapture_must_bound_output_excerpts",
        "future_recapture_must_apply_secret_like_redaction", "future_recapture_must_not_be_treated_as_retry",
        "future_recapture_must_not_claim_root_cause", "future_recapture_results_review_required",
        "future_remediation_or_method_candidate_requires_diagnostic_results_review",
        "future_retry_requires_separate_candidate_approval_execution_and_review",
        "main_merge_requires_passing_retry_results_review",
    )
}

FUTURE_PLAN = {
    "steps": [
        "Bind this candidate and the source failure-diagnosis evidence.",
        "Bind the blocked execution digest, blocked manifest digest, and blocked reason.",
        "Bind the approval, operator-review, candidate, planning, detail-binding, materialization, and recovery digests.",
        "Bind retry failure counts and Priority 1 module facts.", "Select one recovery or recapture package.",
        "If recovery is selected, restrict search to explicit approved non-secret receipt paths only.",
        "If operator transcript is selected, require hash-verifiable bounded transcript with command, cwd, target modules, exit code, timestamps, and output evidence.",
        "If controlled recapture is selected, prewrite a durable receipt scaffold before command execution.",
        "Use only the approved five Priority 1 modules unless a separate approval expands scope.",
        "Use the detached integration worktree as cwd.", "Use the approved repository virtualenv Python executable.",
        "Use -p no:cacheprovider.",
        "Capture command, cwd, target modules, exit code, stdout hash, stderr hash, byte counts, duration, bounded excerpts, and redaction summary.",
        "Preserve nonzero exit as diagnostic evidence only.", "Preserve the failed retry as authoritative.",
        "Require recovery or recapture results review before any remediation or method candidate.",
        "Keep new retry, main merge, runtime, broker, and trading closed.",
    ],
    "plan_status": "PLANNED_NOT_EXECUTED",
}

FUTURE_COMMAND_TEMPLATE = {
    "future_recapture_command_template_status": "PLANNED_NOT_EXECUTED",
    "future_recapture_working_directory": source.RETRY_PYTEST_WORKING_DIRECTORY,
    "future_recapture_python_executable": r"C:\Users\Aspire5 15 i7 4G2050\marketflow\env\Scripts\python.exe",
    "future_recapture_command_template": r"C:\Users\Aspire5 15 i7 4G2050\marketflow\env\Scripts\python.exe -m pytest -q -p no:cacheprovider --tb=short -rA tests/test_marketflow_signal_or_feature_generation_results_review_service.py tests/test_post_identity_freeze_registry_inventory_approval_service.py tests/test_corporate_action_authority_plan_candidate_service.py tests/test_feature_generation_results_review_redesigned_labels_service.py tests/test_marketflow_objective_label_or_target_generation_results_review_service.py",
    "future_recapture_command_is_retry": False, "future_recapture_command_is_full_pytest": False,
    "future_recapture_command_executed": False,
}

FUTURE_RECEIPT_SAFEGUARDS = {
    key: True for key in (
        "future_receipt_scaffold_required_before_command",
        "future_receipt_scaffold_must_record_source_digests_before_command",
        "future_receipt_scaffold_must_record_command_before_command",
        "future_receipt_scaffold_must_record_cwd_before_command",
        "future_receipt_scaffold_must_record_target_modules_before_command",
        "future_receipt_scaffold_must_record_start_timestamp_before_command",
        "future_receipt_must_be_finalized_after_command", "future_receipt_must_survive_print_wrapper_failure",
        "future_receipt_must_include_exit_code_or_block", "future_receipt_must_include_stdout_hash_or_block",
        "future_receipt_must_include_stderr_hash_or_block", "future_receipt_must_include_bounded_excerpts_or_block",
        "future_receipt_must_include_redaction_summary_or_block", "future_receipt_must_include_payload_digest_or_block",
        "future_receipt_must_include_digest_manifest_or_block",
    )
}

PLANNED_OUTPUT_NAMES = [
    "receipt_recovery_or_recapture_candidate_manifest", "source_failure_diagnosis_binding_report",
    "receipt_loss_classification_report", "unavailable_payload_fields_report", "package_comparison_report",
    "recommended_recapture_package_report", "approved_priority_1_target_modules_preservation_report",
    "future_recovery_boundary_report", "future_controlled_recapture_command_template_report",
    "future_durable_receipt_persistence_guard_report", "future_output_bounding_and_redaction_plan",
    "future_results_review_enablement_report", "remediation_or_method_gate_preservation_report",
    "retry_gate_preservation_report", "unsupported_claims_boundary_report", "digest_manifest",
]
PLANNED_OUTPUTS = {name: PLANNED_NOT_GENERATED for name in PLANNED_OUTPUT_NAMES}

NON_GOALS = [
    "do_not_recover_receipt_now", "do_not_recaputure_now", "do_not_execute_diagnostic_command_now",
    "do_not_run_targeted_pytest_now", "do_not_run_full_pytest_now", "do_not_rerun_retry_now",
    "do_not_read_cache_now", "do_not_modify_cache_now", "do_not_parse_operator_logs_now",
    "do_not_inspect_env_now", "do_not_reconstruct_output_hashes_now", "do_not_reconstruct_exit_code_now",
    "do_not_reconstruct_excerpts_now", "do_not_infer_missing_payload_now", "do_not_execute_remediation_now",
    "do_not_execute_classification_now", "do_not_classify_modules_again_now", "do_not_identify_first_failure_now",
    "do_not_identify_first_error_now", "do_not_claim_traceback_root_cause_now",
    "do_not_recommend_direct_code_remediation_now", "do_not_create_diagnostic_results_review_now",
    "do_not_create_remediation_or_method_candidate_now", "do_not_create_new_retry_candidate_now",
    "do_not_create_retry_results_review_now", "do_not_create_integration_results_review_now",
    "do_not_mark_integration_successful", "do_not_push_integration_branch", "do_not_push_main",
    "do_not_commit_marketflow_outputs", "do_not_commit_pytest_cache", "do_not_modify_staged_evidence",
    "do_not_regenerate_evidence", "do_not_call_providers", "do_not_accept_predictive_usefulness",
    "do_not_accept_profitability", "do_not_authorize_runtime", "do_not_authorize_trading",
]

NEXT_CHAIN = [
    "Targeted Diagnostic Output Capture Receipt Recovery or Recapture Candidate Operator Review v1.",
    "Targeted Diagnostic Output Capture Receipt Recovery or Recapture Approval v1, if selected.",
    "Receipt Recovery or Controlled Recapture Execution v1, if approved.",
    "Receipt Recovery or Controlled Recapture Results Review v1.",
    "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1, if supported by results review.",
    "Remediation or Method Operator Review v1, if needed.", "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.", "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
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
    "candidate_receipt_recovery_does_not_recover_receipt", "candidate_receipt_recovery_does_not_execute_recapture",
    "candidate_receipt_recovery_does_not_run_diagnostic_command", "candidate_receipt_recovery_does_not_run_targeted_pytest",
    "candidate_receipt_recovery_does_not_run_full_pytest", "candidate_receipt_recovery_does_not_rerun_retry",
    "candidate_receipt_recovery_does_not_read_cache", "candidate_receipt_recovery_does_not_modify_cache",
    "candidate_receipt_recovery_does_not_parse_operator_logs", "candidate_receipt_recovery_does_not_inspect_env",
    "candidate_receipt_recovery_does_not_reconstruct_stdout_hash", "candidate_receipt_recovery_does_not_reconstruct_stderr_hash",
    "candidate_receipt_recovery_does_not_reconstruct_exit_code", "candidate_receipt_recovery_does_not_reconstruct_excerpts",
    "candidate_receipt_recovery_does_not_infer_missing_payload", "candidate_receipt_recovery_does_not_execute_remediation",
    "candidate_receipt_recovery_does_not_execute_classification", "candidate_receipt_recovery_does_not_classify_modules_again",
    "candidate_receipt_recovery_does_not_identify_first_failure", "candidate_receipt_recovery_does_not_identify_first_error",
    "candidate_receipt_recovery_does_not_claim_traceback_root_cause", "candidate_receipt_recovery_does_not_recommend_direct_code_remediation",
    "candidate_receipt_recovery_does_not_create_diagnostic_results_review", "candidate_receipt_recovery_does_not_create_remediation_or_method_candidate",
    "candidate_receipt_recovery_does_not_create_new_retry_candidate", "candidate_receipt_recovery_does_not_create_retry_results_review",
    "candidate_receipt_recovery_does_not_create_integration_results_review", "candidate_receipt_recovery_does_not_mark_integration_successful",
    "candidate_receipt_recovery_does_not_generate_successful_integration_digest", "candidate_receipt_recovery_does_not_treat_transient_success_as_durable_success",
    "candidate_receipt_recovery_does_not_treat_diagnostic_run_as_retry", "candidate_receipt_recovery_does_not_push_integration_branch",
    "candidate_receipt_recovery_does_not_push_main", "candidate_receipt_recovery_does_not_delete_integration_branch",
    "candidate_receipt_recovery_does_not_delete_worktree", "candidate_receipt_recovery_does_not_force_push",
    "candidate_receipt_recovery_does_not_prune_remotes", "candidate_receipt_recovery_does_not_modify_tags",
    "candidate_receipt_recovery_does_not_modify_staged_evidence", "candidate_receipt_recovery_does_not_regenerate_evidence",
    "candidate_receipt_recovery_does_not_call_providers", "candidate_receipt_recovery_does_not_acquire_market_data",
    "candidate_receipt_recovery_does_not_regenerate_dataset", "candidate_receipt_recovery_does_not_recompute_metrics",
    "candidate_receipt_recovery_does_not_train_models", "candidate_receipt_recovery_does_not_score_strategy",
    "candidate_receipt_recovery_does_not_generate_recommendations", "candidate_receipt_recovery_does_not_accept_predictive_usefulness",
    "candidate_receipt_recovery_does_not_accept_profitability", "candidate_receipt_recovery_does_not_authorize_runtime",
    "candidate_receipt_recovery_does_not_authorize_broker_execution", "candidate_output_is_planning_only_not_recovery_execution",
    "future_recapture_requires_separate_operator_review_and_approval", "future_recapture_must_prewrite_durable_receipt_before_command",
    "future_recapture_is_not_retry_success", "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation", "blocked_execution_remains_historically_blocked",
    "single_permitted_diagnostic_run_acknowledged_but_not_accepted_as_durable_success",
    "previous_failure_diagnosis_remains_source_evidence", "previous_approval_remains_source_evidence",
    "previous_operator_review_remains_source_evidence", "previous_candidate_remains_source_evidence",
    "previous_planning_results_review_remains_valid", "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_results_review_required_after_receipt_recovery_or_recapture",
    "separate_remediation_or_method_candidate_required_after_diagnostic_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "receipt_recovery_or_recapture_candidate_created",
    "receipt_recovery_or_recapture_candidate_ready_for_operator_review", "source_failure_diagnosis_reviewed",
    "receipt_loss_failure_class_bound", "future_receipt_recovery_or_recapture_packages_defined",
    "future_receipt_recovery_requirements_defined", "future_controlled_recapture_requirements_defined",
    "future_persistence_guard_plan_defined", "ready_for_receipt_recovery_or_recapture_candidate_operator_review",
    "diagnostic_command_executed_once", "transient_success_artifact_returned",
]
FALSE_FIELDS = [
    "durable_success_receipt_retained", "diagnostic_exit_code_available", "diagnostic_duration_seconds_available",
    "stdout_hash_available", "stderr_hash_available", "stdout_byte_count_available", "stderr_byte_count_available",
    "combined_output_byte_count_available", "bounded_stdout_excerpt_available", "bounded_stderr_excerpt_available",
    "redaction_patterns_available", "success_payload_digest_available", "success_digest_manifest_digest_available",
    "unavailable_values_reconstructed", "unavailable_values_inferred", "diagnostic_command_rerun_to_recover_values",
    "recommended_package_selected", "receipt_recovery_package_selected", "receipt_recovery_package_approved",
    "receipt_recovery_package_authorized", "receipt_recovery_execution_performed", "receipt_recovered",
    "controlled_recapture_package_selected", "controlled_recapture_package_approved",
    "controlled_recapture_package_authorized", "controlled_recapture_execution_performed",
    "diagnostic_command_executed_in_candidate", "diagnostic_output_captured_in_candidate",
    "targeted_pytest_performed", "full_pytest_performed", "retry_rerun_performed",
    "ready_for_receipt_recovery_or_recapture_approval", "ready_for_receipt_recovery_or_recapture_execution",
    "ready_for_diagnostic_results_review", "ready_for_remediation_or_method_candidate", "ready_for_retry_candidate",
    "diagnostic_results_review_created", "remediation_or_method_candidate_after_diagnostic_capture_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
    "main_merge_approval_created", "cache_read_in_candidate", "cache_modified_in_candidate",
    "operator_logs_parsed", "env_inspection_performed", "classification_execution_performed_in_candidate",
    "remediation_execution_performed", "failure_modules_classified", "error_modules_classified",
    "failure_error_separation_claimed", "first_failure_identified", "first_error_identified",
    "first_order_claim_made", "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "retry_success_claimed", "main_merge_readiness_claimed", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_candidate", "market_data_acquisition_performed_in_candidate",
    "dataset_generation_performed_in_candidate", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError(ValueError):
    """Raised when candidate evidence drifts or opens prohibited authority."""


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _source_summary() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND, "diagnosis_status": source.DIAGNOSIS_STATUS,
        "diagnosis_scope": source.DIAGNOSIS_SCOPE, source.DIGEST_KEY: SOURCE_DIAGNOSIS_DIGEST,
        "primary_failure_class": source.PRIMARY_FAILURE_CLASS, "secondary_failure_class": source.SECONDARY_FAILURE_CLASS,
        "diagnostic_command_executed_once": True, "transient_success_artifact_returned": True,
        "durable_success_receipt_retained": False, "unavailable_values_reconstructed": False,
        "unavailable_values_inferred": False, "diagnostic_command_rerun_to_recover_values": False,
    }


def _bind_source(value: Mapping[str, Any] | None) -> dict[str, Any]:
    expected = _source_summary()
    if value is None:
        return deepcopy(expected)
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("source failure diagnosis must be an object")
    try:
        source.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(dict(value))
    except source.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError(
            "source failure diagnosis validation failed"
        ) from exc
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError(f"source failure diagnosis {field} mismatch")
    return deepcopy(expected)


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_checks = {
        "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest": "source_failure_diagnosis_digest_bound",
        "source_targeted_diagnostic_output_capture_execution_digest": "source_execution_digest_bound",
        "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest": "source_blocked_manifest_digest_bound",
        "source_targeted_diagnostic_output_capture_execution_blocked_reason": "source_blocked_reason_bound",
        "source_primary_failure_class": "source_primary_failure_class_bound",
        "source_secondary_failure_class": "source_secondary_failure_class_bound",
        "source_targeted_diagnostic_output_capture_approval_digest": "source_approval_digest_bound",
        "source_targeted_diagnostic_output_capture_candidate_operator_review_digest": "source_operator_review_digest_bound",
        "source_targeted_diagnostic_output_capture_candidate_digest": "source_candidate_digest_bound",
        "source_results_review_digest": "source_results_review_digest_bound",
        "source_prioritized_planning_review_digest": "source_prioritized_planning_review_digest_bound",
        "source_results_review_manifest_digest": "source_results_review_manifest_digest_bound",
        "source_planning_execution_digest": "source_planning_execution_digest_bound",
        "source_prioritized_planning_digest": "source_prioritized_planning_digest_bound",
        "source_planning_digest_manifest_digest": "source_planning_manifest_digest_bound",
        "source_detail_binding_results_review_digest": "source_detail_binding_results_review_digest_bound",
        "source_complete_29_row_binding_digest": "source_complete_29_row_binding_digest_bound",
        "source_materialized_payload_digest": "source_materialized_payload_digest_bound",
        "source_detail_binding_approval_digest": "source_detail_binding_approval_digest_bound",
        "source_recovery_results_review_digest": "source_recovery_results_review_digest_bound",
        "source_recovery_detail_digest": "source_recovery_detail_digest_bound",
        "source_after_v2_approval_digest": "source_after_v2_approval_digest_bound",
        "source_module_grouping_digest": "source_module_grouping_digest_bound",
    }
    checks = [_check(check_id, SOURCE_BINDINGS[field], candidate.get(field)) for field, check_id in source_checks.items()]
    checks.extend([
        _check("retry_execution_commit_bound", source.source.RETRY_EXECUTION_COMMIT, candidate.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, candidate.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", [x["module_path"] for x in PRIORITY_1_TARGET_MODULES], [x.get("module_path") for x in candidate.get("priority_1_target_modules", [])]),
        _check("priority_1_total_612_bound", 612, candidate.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, candidate.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, candidate.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, candidate.get("failed_or_errored_nodeids_count")),
        _check("diagnostic_command_executed_once_acknowledged", True, candidate.get("diagnostic_command_executed_once")),
        _check("transient_success_acknowledged", True, candidate.get("transient_success_artifact_returned")),
        _check("durable_success_receipt_missing", False, candidate.get("durable_success_receipt_retained")),
        _check("unavailable_fields_recorded", UNAVAILABLE_FIELDS, candidate.get("unavailable_diagnostic_payload_fields")),
        _check("missing_values_not_reconstructed", False, candidate.get("unavailable_values_reconstructed")),
        _check("missing_values_not_inferred", False, candidate.get("unavailable_values_inferred")),
        _check("candidate_created_true", True, candidate.get("receipt_recovery_or_recapture_candidate_created")),
        _check("candidate_ready_true", True, candidate.get("receipt_recovery_or_recapture_candidate_ready_for_operator_review")),
        _check("future_packages_defined", True, candidate.get("future_receipt_recovery_or_recapture_packages_defined")),
        _check("recommended_package_defined", RECOMMENDED_PACKAGE, candidate.get("recommended_receipt_recovery_or_recapture_package")),
        _check("recommended_package_not_selected", False, candidate.get("recommended_package_selected")),
        _check("packages_present_11", 11, len(candidate.get("proposed_receipt_recovery_or_recapture_packages", []))),
        _check("blocked_packages_present_7", 7, sum(x.get("status") == "BLOCKED_NOT_ALLOWED" for x in candidate.get("proposed_receipt_recovery_or_recapture_packages", []))),
        _check("future_requirements_defined", FUTURE_REQUIREMENTS, candidate.get("future_receipt_recovery_or_recapture_requirements")),
        _check("future_plan_defined", FUTURE_PLAN, candidate.get("future_recovery_or_recapture_plan")),
        _check("future_recapture_command_template_defined_not_executed", FUTURE_COMMAND_TEMPLATE, candidate.get("future_controlled_recapture_command_template")),
        _check("future_receipt_safeguards_defined", FUTURE_RECEIPT_SAFEGUARDS, candidate.get("future_durable_receipt_safeguards")),
        _check("planned_outputs_defined", PLANNED_OUTPUTS, candidate.get("planned_outputs")),
        _check("non_goals_defined", NON_GOALS, candidate.get("non_goals")),
    ])
    aliases = {
        "receipt_recovery_package_selected": "receipt_recovery_package_selected_false",
        "receipt_recovery_package_approved": "receipt_recovery_package_approved_false",
        "receipt_recovery_execution_performed": "receipt_recovery_execution_false",
        "receipt_recovered": "receipt_recovered_false",
        "controlled_recapture_package_selected": "controlled_recapture_package_selected_false",
        "controlled_recapture_package_approved": "controlled_recapture_package_approved_false",
        "controlled_recapture_execution_performed": "controlled_recapture_execution_false",
        "diagnostic_command_executed_in_candidate": "diagnostic_command_executed_in_candidate_false",
        "diagnostic_output_captured_in_candidate": "diagnostic_output_captured_in_candidate_false",
        "targeted_pytest_performed": "targeted_pytest_false", "full_pytest_performed": "full_pytest_false",
        "retry_rerun_performed": "retry_rerun_false", "cache_read_in_candidate": "cache_read_false",
        "cache_modified_in_candidate": "cache_modified_false", "operator_logs_parsed": "operator_logs_parsed_false",
        "env_inspection_performed": "env_inspection_false", "diagnostic_results_review_created": "diagnostic_results_review_created_false",
        "remediation_or_method_candidate_after_diagnostic_capture_created": "remediation_or_method_candidate_created_false",
        "new_retry_candidate_created": "new_retry_candidate_created_false", "new_retry_executed": "new_retry_executed_false",
        "new_retry_results_review_created": "new_retry_results_review_created_false",
        "main_merge_approval_created": "main_merge_approval_created_false",
        "classification_execution_performed_in_candidate": "classification_execution_false",
        "remediation_execution_performed": "remediation_execution_false", "failure_modules_classified": "failure_modules_classified_false",
        "error_modules_classified": "error_modules_classified_false", "failure_error_separation_claimed": "failure_error_separation_claimed_false",
        "first_failure_identified": "first_failure_identified_false", "first_error_identified": "first_error_identified_false",
        "first_order_claim_made": "first_order_claim_made_false", "traceback_root_cause_claimed": "traceback_root_cause_claimed_false",
        "direct_code_remediation_recommended": "direct_code_remediation_recommended_false",
        "retry_success_claimed": "retry_success_claimed_false", "main_merge_readiness_claimed": "main_merge_readiness_claimed_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "integration_branch_pushed": "integration_branch_pushed_false", "main_push_performed": "main_push_false",
        "origin_main_modified_by_this_task": "origin_main_modified_false", "marketflow_outputs_committed": "marketflow_outputs_committed_false",
        "pytest_cache_committed": "pytest_cache_committed_false", "evidence_regenerated": "evidence_regenerated_false",
        "provider_requests_made_in_candidate": "provider_requests_false",
        "market_data_acquisition_performed_in_candidate": "market_data_acquisition_false",
        "dataset_generation_performed_in_candidate": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
        "unavailable_values_reconstructed": "unavailable_values_reconstructed_false",
        "unavailable_values_inferred": "unavailable_values_inferred_false",
    }
    required_false_check_fields = [
        "receipt_recovery_package_selected", "receipt_recovery_package_approved", "receipt_recovery_execution_performed",
        "receipt_recovered", "controlled_recapture_package_selected", "controlled_recapture_package_approved",
        "controlled_recapture_execution_performed", "diagnostic_command_executed_in_candidate",
        "diagnostic_output_captured_in_candidate", "targeted_pytest_performed", "full_pytest_performed",
        "retry_rerun_performed", "cache_read_in_candidate", "cache_modified_in_candidate", "operator_logs_parsed",
        "env_inspection_performed", "unavailable_values_reconstructed", "unavailable_values_inferred",
        "diagnostic_results_review_created", "remediation_or_method_candidate_after_diagnostic_capture_created",
        "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
        "classification_execution_performed_in_candidate", "remediation_execution_performed", "failure_modules_classified",
        "error_modules_classified", "failure_error_separation_claimed", "first_failure_identified", "first_error_identified",
        "first_order_claim_made", "traceback_root_cause_claimed", "direct_code_remediation_recommended",
        "retry_success_claimed", "main_merge_readiness_claimed", "integration_execution_successful",
        "successful_integration_execution_digest_generated", "integration_branch_pushed", "main_push_performed",
        "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
        "provider_requests_made_in_candidate", "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate", "metric_recomputation_from_raw_rows_performed",
        "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
    ]
    checks.extend(_check(aliases[field], False, candidate.get(field)) for field in required_false_check_fields)
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, candidate.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("next_chain_defined", NEXT_CHAIN, candidate.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, candidate.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("no_tracked_marketflow_files", False, candidate.get("marketflow_outputs_committed")),
        _check("no_tracked_pytest_cache_files", False, candidate.get("pytest_cache_committed")),
    ])
    return checks


def _summary(candidate: Mapping[str, Any]) -> dict[str, Any]:
    checklist = candidate.get("checklist", [])
    passed = sum(x.get("status") == PASS for x in checklist)
    fields = [
        "receipt_recovery_or_recapture_candidate_created", "receipt_recovery_or_recapture_candidate_ready_for_operator_review",
        "source_failure_diagnosis_reviewed", "receipt_loss_failure_class_bound", "recommended_receipt_recovery_or_recapture_package",
        "receipt_recovery_package_selected", "receipt_recovery_package_approved", "receipt_recovery_execution_performed",
        "receipt_recovered", "controlled_recapture_package_selected", "controlled_recapture_package_approved",
        "controlled_recapture_execution_performed", "diagnostic_command_executed_in_candidate",
        "diagnostic_output_captured_in_candidate", "targeted_pytest_performed", "retry_rerun_performed",
        "full_pytest_performed", "diagnostic_command_executed_once", "transient_success_artifact_returned",
        "durable_success_receipt_retained", "unavailable_values_reconstructed", "unavailable_values_inferred",
        "ready_for_receipt_recovery_or_recapture_candidate_operator_review",
        "ready_for_receipt_recovery_or_recapture_approval", "ready_for_receipt_recovery_or_recapture_execution",
        "ready_for_diagnostic_results_review", "ready_for_remediation_or_method_candidate", "ready_for_retry_candidate",
        "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "priority_1_total_nodeids", "top_10_count_sum",
    ]
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed, **{field: candidate.get(field) for field in fields},
        "priority_1_top_module_count": 5, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "recommended_next_task": NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _candidate_digest(candidate: Mapping[str, Any]) -> str:
    value = deepcopy(dict(candidate))
    for field in ("checklist", "summary", DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(
    *, source_failure_diagnosis: dict | None = None,
) -> dict:
    """Build the candidate without recovering or recapturing diagnostic evidence."""

    bound_source = _bind_source(source_failure_diagnosis)
    retry_context = {
        "retry_execution_branch": source.RETRY_EXECUTION_BRANCH, "retry_execution_commit": source.source.RETRY_EXECUTION_COMMIT,
        "retry_pytest_working_directory": source.RETRY_PYTEST_WORKING_DIRECTORY,
        "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "retry_pytest_first_result_authoritative": True, "retry_pytest_passed": False,
        "retry_pytest_failed": True, "root_full_regression_is_retry_evidence": False,
    }
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True, "operator_review_required": True,
        "source_failure_diagnosis_artifact_kind": source.ARTIFACT_KIND,
        "source_failure_diagnosis_status": source.DIAGNOSIS_STATUS,
        "source_failure_diagnosis_scope": source.DIAGNOSIS_SCOPE,
        **deepcopy(SOURCE_BINDINGS), "source_failure_diagnosis_summary": bound_source,
        "source_execution_blocked_summary": {
            "execution_digest": source.SOURCE_EXECUTION_DIGEST,
            "blocked_manifest_digest": source.SOURCE_BLOCKED_MANIFEST_DIGEST,
            "blocked_reason": source.SOURCE_BLOCKED_REASON,
        },
        "retry_execution_commit": source.source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": retry_context,
        "unavailable_diagnostic_payload_fields": list(UNAVAILABLE_FIELDS),
        "priority_1_target_modules": deepcopy(PRIORITY_1_TARGET_MODULES),
        "priority_1_total_nodeids": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "candidate_philosophy": deepcopy(CANDIDATE_PHILOSOPHY),
        "proposed_receipt_recovery_or_recapture_packages": deepcopy(PROPOSED_PACKAGES),
        **deepcopy(RECOMMENDATION),
        "future_receipt_recovery_or_recapture_requirements": deepcopy(FUTURE_REQUIREMENTS),
        "future_recovery_or_recapture_plan": deepcopy(FUTURE_PLAN),
        "future_controlled_recapture_command_template": deepcopy(FUTURE_COMMAND_TEMPLATE),
        "future_durable_receipt_safeguards": deepcopy(FUTURE_RECEIPT_SAFEGUARDS),
        "planned_outputs": deepcopy(PLANNED_OUTPUTS), "non_goals": list(NON_GOALS),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": NEXT_TASK, "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    candidate.update({field: True for field in TRUE_FIELDS})
    candidate.update({field: False for field in FALSE_FIELDS})
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate)
    candidate[DIGEST_KEY] = _candidate_digest(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(candidate: dict) -> dict:
    """Reject source drift, execution, evidence fabrication, or authority expansion."""

    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("candidate must be an object")
    constants = {
        **SOURCE_BINDINGS, "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True, "operator_review_required": True,
        "source_failure_diagnosis_artifact_kind": source.ARTIFACT_KIND,
        "source_failure_diagnosis_status": source.DIAGNOSIS_STATUS,
        "source_failure_diagnosis_scope": source.DIAGNOSIS_SCOPE,
        "retry_execution_commit": source.source.RETRY_EXECUTION_COMMIT,
        "priority_1_total_nodeids": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "recommended_next_task": NEXT_TASK,
    }
    for field, expected in constants.items():
        if candidate.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError(f"{field} mismatch")
    expected_retry = {
        "retry_execution_branch": source.RETRY_EXECUTION_BRANCH, "retry_execution_commit": source.source.RETRY_EXECUTION_COMMIT,
        "retry_pytest_working_directory": source.RETRY_PYTEST_WORKING_DIRECTORY,
        "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "retry_pytest_first_result_authoritative": True, "retry_pytest_passed": False,
        "retry_pytest_failed": True, "root_full_regression_is_retry_evidence": False,
    }
    structures = {
        "source_failure_diagnosis_summary": _source_summary(),
        "source_execution_blocked_summary": {"execution_digest": source.SOURCE_EXECUTION_DIGEST, "blocked_manifest_digest": source.SOURCE_BLOCKED_MANIFEST_DIGEST, "blocked_reason": source.SOURCE_BLOCKED_REASON},
        "retry_failure_context": expected_retry, "unavailable_diagnostic_payload_fields": UNAVAILABLE_FIELDS,
        "priority_1_target_modules": PRIORITY_1_TARGET_MODULES, "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "proposed_receipt_recovery_or_recapture_packages": PROPOSED_PACKAGES,
        "future_receipt_recovery_or_recapture_requirements": FUTURE_REQUIREMENTS,
        "future_recovery_or_recapture_plan": FUTURE_PLAN,
        "future_controlled_recapture_command_template": FUTURE_COMMAND_TEMPLATE,
        "future_durable_receipt_safeguards": FUTURE_RECEIPT_SAFEGUARDS,
        "planned_outputs": PLANNED_OUTPUTS, "non_goals": NON_GOALS,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected in structures.items():
        if candidate.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError(f"{field} mismatch")
    for field, expected in RECOMMENDATION.items():
        if candidate.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError(f"{field} mismatch")
    if any(candidate.get(field) is not True for field in TRUE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("candidate fact missing")
    if any(candidate.get(field) is not False for field in FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("closed boundary opened")
    if candidate.get("predictive_usefulness") != NOT_ACCEPTED or candidate.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("acceptance boundary changed")
    if any(candidate.get(field) != NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("runtime boundary changed")
    checklist = _checklist(candidate)
    if candidate.get("checklist") != checklist or any(x["status"] != PASS for x in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("checklist mismatch")
    if candidate.get("summary") != _summary(candidate):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("summary mismatch")
    digest = candidate.get(DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _candidate_digest(candidate):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("candidate digest mismatch")
    return {"artifact_kind": ARTIFACT_KIND, "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE, "candidate_digest": digest, **{k: candidate["summary"][k] for k in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(
    output_dir: str | Path, *, source_failure_diagnosis: dict | None = None,
) -> dict:
    """Write deterministic candidate JSON outside protected runtime paths."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("protected output directory")
    candidate = build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(source_failure_diagnosis=source_failure_diagnosis)
    path = output / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError("output exists")
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": ARTIFACT_KIND, "candidate_status": CANDIDATE_STATUS, "candidate_digest": candidate[DIGEST_KEY], "payload_sha256": sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_markdown_v1(candidate: dict) -> str:
    """Render a sanitized candidate summary after strict validation."""

    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(candidate)
    sections = [
        ("Source Failure Diagnosis", f"Digest: `{SOURCE_DIAGNOSIS_DIGEST}`; status: `{source.DIAGNOSIS_STATUS}`."),
        ("Source Targeted Diagnostic Output Capture Execution", f"Blocked reason: `{source.SOURCE_BLOCKED_REASON}`."),
        ("Source Approval and Operator Review", "All prior source approval, review, and candidate digests remain bound."),
        ("Source Planning and Detail Binding Evidence", "Planning, detail-binding, materialization, and recovery evidence remain immutable source bindings."),
        ("Retry Failure Context", "24,877 passed; 1,292 failed; 112 errors; 7 skipped. The failed retry remains authoritative."),
        ("Candidate Scope", f"`{CANDIDATE_SCOPE}`"),
        ("Receipt Loss Summary", f"Primary: `{source.PRIMARY_FAILURE_CLASS}`. Contributing: `{source.SECONDARY_FAILURE_CLASS}`."),
        ("Unavailable Diagnostic Payload Fields", ", ".join(f"`{x}`" for x in UNAVAILABLE_FIELDS)),
        ("Priority 1 Target Modules", "\n".join(f"- `{x['module_path']}`: {x['failed_or_errored_nodeid_count']}" for x in PRIORITY_1_TARGET_MODULES)),
        ("Candidate Philosophy", CANDIDATE_PHILOSOPHY["receipt_recovery_or_recapture_candidate_philosophy"]),
        ("Proposed Receipt Recovery or Recapture Packages", "\n".join(f"- `{x['package_id']}`: `{x['status']}`" for x in PROPOSED_PACKAGES)),
        ("Recommended Package", f"`{RECOMMENDED_PACKAGE}` remains recommended for review and not selected."),
        ("Future Recovery or Recapture Requirements", f"{len(FUTURE_REQUIREMENTS)} requirements are defined and not executed."),
        ("Future Recovery or Recapture Plan", f"{len(FUTURE_PLAN['steps'])} steps; status `{FUTURE_PLAN['plan_status']}`."),
        ("Future Controlled Recapture Command Template", "The five-module command is planning-only and was not executed."),
        ("Future Durable Receipt Safeguards", f"{len(FUTURE_RECEIPT_SAFEGUARDS)} persistence safeguards are required."),
        ("Planned Outputs", "All planned outputs remain `PLANNED_NOT_GENERATED`."),
        ("Non-Goals", ", ".join(f"`{x}`" for x in NON_GOALS)),
        ("Next Chain", "\n".join(f"{i}. {x}" for i, x in enumerate(NEXT_CHAIN, 1))),
        ("Next Gates", "\n".join(f"- `{x}`" for x in NEXT_GATES)),
        ("Risk Controls", "\n".join(f"- `{x}`" for x in RISK_CONTROLS)),
        ("Authority Boundaries", "No recovery, recapture, execution, retry, predictive, profitability, runtime, or trading authority is created."),
        ("Checklist Summary", f"{candidate['summary']['passed_checks']}/{candidate['summary']['total_checks']} checks passed."),
        ("Guardrails", "MarketFlow remains research and decision-support software, not execution software."),
    ]
    title = "# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Receipt Recovery or Recapture Candidate v1"
    return title + "\n\n" + "\n\n".join(f"## {heading}\n\n{body}" for heading, body in sections) + "\n"


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE
PACKAGE_CONTROLLED_SINGLE_RECAPTURE_WITH_PREWRITE_RECEIPT_FILE_AND_NO_CACHEPROVIDER = RECOMMENDED_PACKAGE
