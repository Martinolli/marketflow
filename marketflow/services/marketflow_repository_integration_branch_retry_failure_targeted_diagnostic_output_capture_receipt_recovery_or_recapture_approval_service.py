"""Approve future controlled diagnostic recapture without executing it."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVED_V1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVED"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_ONLY_NOT_EXECUTION_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1"
DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_digest"
SOURCE_OPERATOR_REVIEW_DIGEST = "c9e9844aef0926585bc96d44d37c25577ac3a29246bc0a5bd57729db0149fd6c"
SELECTED_PACKAGE = source.RECOMMENDED_PACKAGE
OPERATOR_DECISION = "APPROVE_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE"
ATTESTATION_VERSION = "receipt_recovery_or_recapture_approval_attestation_v1"
RETRY_EXECUTION_COMMIT = "ab178b65c69f0274b0abbf9c20df102d35e78d34"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

REQUIRED_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_ATTESTATION_PHRASE_V1 = (
    "APPROVE TARGETED DIAGNOSTIC OUTPUT CAPTURE RECEIPT RECOVERY OR CONTROLLED RECAPTURE "
    "PACKAGE_CONTROLLED_SINGLE_RECAPTURE_WITH_PREWRITE_RECEIPT_FILE_AND_NO_CACHEPROVIDER MARKETFLOW "
    "CONTROLLED SINGLE RECAPTURE WITH PREWRITTEN DURABLE RECEIPT SCAFFOLD FOR FUTURE EXECUTION ONLY "
    "NO RECAPTURE NOW NO DIAGNOSTIC COMMAND NOW NO TARGETED PYTEST NOW NO RETRY NO CACHE READ NO MAIN PUSH "
    "RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_ONLY_NOT_EXECUTION_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
)

SOURCE_BINDINGS = {
    "source_receipt_recovery_or_recapture_candidate_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    **deepcopy(source.SOURCE_BINDINGS),
}

STRING_CONFIRMATIONS = {
    "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_failure_diagnosis_digest": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
    "operator_confirms_source_execution_digest": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_digest"],
    "operator_confirms_source_blocked_manifest_digest": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest"],
    "operator_confirms_source_blocked_reason": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"],
    "operator_confirms_source_primary_failure_class": SOURCE_BINDINGS["source_primary_failure_class"],
    "operator_confirms_source_secondary_failure_class": SOURCE_BINDINGS["source_secondary_failure_class"],
    "operator_confirms_source_approval_digest": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_approval_digest"],
    "operator_confirms_source_targeted_diagnostic_candidate_operator_review_digest": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_candidate_operator_review_digest"],
    "operator_confirms_source_targeted_diagnostic_candidate_digest": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_candidate_digest"],
    "operator_confirms_source_results_review_digest": SOURCE_BINDINGS["source_results_review_digest"],
    "operator_confirms_source_prioritized_planning_review_digest": SOURCE_BINDINGS["source_prioritized_planning_review_digest"],
    "operator_confirms_source_results_review_manifest_digest": SOURCE_BINDINGS["source_results_review_manifest_digest"],
    "operator_confirms_source_planning_execution_digest": SOURCE_BINDINGS["source_planning_execution_digest"],
    "operator_confirms_source_prioritized_planning_digest": SOURCE_BINDINGS["source_prioritized_planning_digest"],
    "operator_confirms_source_planning_digest_manifest_digest": SOURCE_BINDINGS["source_planning_digest_manifest_digest"],
    "operator_confirms_source_detail_binding_results_review_digest": SOURCE_BINDINGS["source_detail_binding_results_review_digest"],
    "operator_confirms_source_complete_29_row_binding_digest": SOURCE_BINDINGS["source_complete_29_row_binding_digest"],
    "operator_confirms_source_materialized_payload_digest": SOURCE_BINDINGS["source_materialized_payload_digest"],
    "operator_confirms_source_detail_binding_approval_digest": SOURCE_BINDINGS["source_detail_binding_approval_digest"],
    "operator_confirms_source_recovery_results_review_digest": SOURCE_BINDINGS["source_recovery_results_review_digest"],
    "operator_confirms_source_recovery_detail_digest": SOURCE_BINDINGS["source_recovery_detail_digest"],
    "operator_confirms_source_after_v2_approval_digest": SOURCE_BINDINGS["source_after_v2_approval_digest"],
    "operator_confirms_source_module_grouping_digest": SOURCE_BINDINGS["source_module_grouping_digest"],
    "operator_confirms_retry_execution_commit": RETRY_EXECUTION_COMMIT,
    "operator_confirms_selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
}

BOOLEAN_CONFIRMATION_FIELDS = [
    "operator_confirms_retry_failure_counts", "operator_confirms_priority_1_top_module_paths",
    "operator_confirms_priority_1_total_612", "operator_confirms_top_10_total_1069",
    "operator_confirms_module_summary_count_29", "operator_confirms_failed_or_errored_nodeids_1404",
    "operator_confirms_diagnostic_command_executed_once", "operator_confirms_transient_success_artifact_returned",
    "operator_confirms_durable_success_receipt_not_retained", "operator_confirms_unavailable_payload_fields",
    "operator_confirms_unavailable_values_not_reconstructed", "operator_confirms_unavailable_values_not_inferred",
    "operator_confirms_approval_scope_only", "operator_confirms_no_receipt_recovery",
    "operator_confirms_no_recapture", "operator_confirms_no_diagnostic_command",
    "operator_confirms_no_diagnostic_output", "operator_confirms_no_targeted_pytest",
    "operator_confirms_no_full_pytest", "operator_confirms_no_retry", "operator_confirms_no_cache_read",
    "operator_confirms_no_cache_modification", "operator_confirms_no_terminal_log_parse",
    "operator_confirms_no_operator_log_parse", "operator_confirms_no_env_inspection",
    "operator_confirms_no_output_reconstruction", "operator_confirms_no_remediation_execution",
    "operator_confirms_no_classification_execution", "operator_confirms_no_failure_error_separation",
    "operator_confirms_no_first_failure", "operator_confirms_no_first_error",
    "operator_confirms_no_traceback_root_cause", "operator_confirms_no_direct_remediation",
    "operator_confirms_no_retry_success", "operator_confirms_no_main_merge_readiness",
    "operator_confirms_no_new_retry_candidate", "operator_confirms_no_retry_results_review",
    "operator_confirms_no_integration_results_review", "operator_confirms_no_main_merge_approval",
    "operator_confirms_no_integration_success", "operator_confirms_no_successful_integration_digest",
    "operator_confirms_no_integration_branch_push", "operator_confirms_no_main_push",
    "operator_confirms_origin_main_not_modified", "operator_confirms_no_branch_delete",
    "operator_confirms_no_force_push", "operator_confirms_no_tag_mutation",
    "operator_confirms_no_evidence_regeneration", "operator_confirms_no_marketflow_commit",
    "operator_confirms_no_pytest_cache_commit", "operator_confirms_no_provider_requests",
    "operator_confirms_no_market_data_acquisition", "operator_confirms_no_dataset_generation",
    "operator_confirms_no_metric_recomputation", "operator_confirms_no_model_training",
    "operator_confirms_no_strategy_scoring", "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_predictive_usefulness_acceptance", "operator_confirms_no_profitability_acceptance",
    "operator_confirms_runtime_not_authorized", "operator_confirms_broker_not_authorized",
    "operator_confirms_no_api_key_storage_or_printing", "operator_confirms_no_secret_capture_or_commit",
]

APPROVED_PACKAGE = {
    "package_id": SELECTED_PACKAGE,
    "approval_status": "APPROVED_FOR_FUTURE_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_EXECUTION_ONLY",
    "selected": True,
    "approved": True,
    "authorized_for_future_execution": True,
    "executed": False,
    "purpose": (
        "Future execution may perform one controlled recapture of the approved five-module diagnostic command only "
        "after prewriting a durable receipt scaffold, verifying source digests and boundaries, using the detached "
        "integration worktree, using the approved Python executable, using `-p no:cacheprovider`, bounding output, "
        "hashing full streams, redacting secret-like patterns, and preserving the failed retry as authoritative."
    ),
}
APPROVED_REQUIREMENTS = [
    {
        "requirement_id": item["requirement_id"],
        "approval_status": "APPROVED_FOR_FUTURE_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_EXECUTION_ONLY",
        "execution_status": "NOT_EXECUTED",
    }
    for item in source.REVIEWED_REQUIREMENTS
]
APPROVED_PLAN_STEPS = [
    "Bind this approval and the source operator-review evidence.",
    "Bind the source candidate and failure-diagnosis evidence.",
    "Bind the blocked execution digest, blocked manifest digest, and blocked reason.",
    "Bind the approval, operator-review, candidate, planning, detail-binding, materialization, and recovery digests.",
    "Bind retry failure counts and Priority 1 module facts.",
    "Use the selected controlled single recapture package.",
    "Prewrite a durable receipt scaffold before command execution.",
    "Record source digests, command, cwd, target modules, and start timestamp before command execution.",
    "Use only the approved five Priority 1 modules unless a separate approval expands scope.",
    "Use the detached integration worktree as cwd.",
    "Use the approved repository virtualenv Python executable.",
    "Use `-p no:cacheprovider`.",
    "Capture command, cwd, target modules, exit code, stdout hash, stderr hash, byte counts, duration, bounded excerpts, and redaction summary.",
    "Preserve nonzero exit as diagnostic evidence only.",
    "Preserve the failed retry as authoritative.",
    "Require recovery or recapture results review before any remediation or method candidate.",
    "Keep new retry, main merge, runtime, broker, and trading closed.",
]
APPROVED_PLAN = [
    {
        "step_id": index,
        "step": step,
        "approval_status": "APPROVED_FOR_FUTURE_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_EXECUTION_ONLY",
        "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(APPROVED_PLAN_STEPS, start=1)
]
FUTURE_COMMAND_TEMPLATE = {
    "future_recapture_command_template_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
    "future_recapture_working_directory": source.source.FUTURE_COMMAND_TEMPLATE["future_recapture_working_directory"],
    "future_recapture_python_executable": source.source.FUTURE_COMMAND_TEMPLATE["future_recapture_python_executable"],
    "future_recapture_command_template": source.source.FUTURE_COMMAND_TEMPLATE["future_recapture_command_template"],
    "future_recapture_command_is_retry": False,
    "future_recapture_command_is_full_pytest": False,
    "future_recapture_command_executed": False,
}
APPROVED_SAFEGUARDS = [
    {
        "safeguard_id": item["safeguard_id"],
        "approval_status": "APPROVED_FOR_FUTURE_CONTROLLED_RECAPTURE_EXECUTION_ONLY",
        "execution_status": "NOT_EXECUTED",
    }
    for item in source.REVIEWED_SAFEGUARDS
]
PLANNED_OUTPUT_IDS = [
    "receipt_recovery_or_recapture_approval_manifest", "source_failure_diagnosis_binding_report",
    "receipt_loss_classification_report", "unavailable_payload_fields_report", "package_comparison_report",
    "approved_recapture_package_report", "approved_priority_1_target_modules_preservation_report",
    "future_recovery_boundary_report", "future_controlled_recapture_command_template_report",
    "future_durable_receipt_persistence_guard_report", "future_output_bounding_and_redaction_plan",
    "future_results_review_enablement_report", "remediation_or_method_gate_preservation_report",
    "retry_gate_preservation_report", "unsupported_claims_boundary_report", "digest_manifest",
]
PLANNED_OUTPUTS = [{"output_id": output_id, "status": "AUTHORIZED_NOT_GENERATED"} for output_id in PLANNED_OUTPUT_IDS]
SUPPORTING_PACKAGE_STATUS = {
    "PACKAGE_RECOVER_EXISTING_TRANSIENT_SUCCESS_RECEIPT_IF_LOCATABLE": "AVAILABLE_NOT_SELECTED_LOW_CONFIDENCE",
    "PACKAGE_OPERATOR_PROVIDES_HASH_VERIFIABLE_TERMINAL_TRANSCRIPT": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_CREATE_COMMAND_MANIFEST_AND_CAPTURE_WRAPPER_FIX_ONLY": "AVAILABLE_NOT_SELECTED",
}
SUPPORTING_PACKAGES = [
    {"package_id": package_id, "approval_status": status, "selected": False, "approved": False, "executed": False}
    for package_id, status in SUPPORTING_PACKAGE_STATUS.items()
]
BLOCKED_PACKAGE_IDS = [
    "PACKAGE_RECOVER_FROM_UNBOUNDED_TERMINAL_BUFFER_OR_SHELL_HISTORY",
    "PACKAGE_ACCEPT_BLOCKED_RECEIPT_AS_DIAGNOSTIC_SUCCESS",
    "PACKAGE_RECONSTRUCT_OUTPUT_HASHES_FROM_MEMORY_OR_SUMMARY",
    "PACKAGE_RERUN_WITHOUT_SEPARATE_APPROVAL",
    "PACKAGE_PROCEED_TO_REMEDIATION_WITHOUT_DIAGNOSTIC_RESULTS_REVIEW",
    "PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_RESULTS_REVIEW",
    "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY",
]
BLOCKED_PACKAGES = [
    {"package_id": package_id, "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False, "executed": False}
    for package_id in BLOCKED_PACKAGE_IDS
]

NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_V1"
NEXT_CHAIN = [
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
    "approval_receipt_recovery_or_recapture_does_not_recover_receipt",
    "approval_receipt_recovery_or_recapture_does_not_execute_recapture",
    "approval_receipt_recovery_or_recapture_does_not_run_diagnostic_command",
    "approval_receipt_recovery_or_recapture_does_not_run_targeted_pytest",
    "approval_receipt_recovery_or_recapture_does_not_run_full_pytest",
    "approval_receipt_recovery_or_recapture_does_not_rerun_retry",
    "approval_receipt_recovery_or_recapture_does_not_read_cache",
    "approval_receipt_recovery_or_recapture_does_not_modify_cache",
    "approval_receipt_recovery_or_recapture_does_not_search_transient_memory",
    "approval_receipt_recovery_or_recapture_does_not_parse_terminal_logs",
    "approval_receipt_recovery_or_recapture_does_not_parse_operator_logs",
    "approval_receipt_recovery_or_recapture_does_not_inspect_env",
    "approval_receipt_recovery_or_recapture_does_not_reconstruct_stdout_hash",
    "approval_receipt_recovery_or_recapture_does_not_reconstruct_stderr_hash",
    "approval_receipt_recovery_or_recapture_does_not_reconstruct_exit_code",
    "approval_receipt_recovery_or_recapture_does_not_reconstruct_excerpts",
    "approval_receipt_recovery_or_recapture_does_not_infer_missing_payload",
    "approval_receipt_recovery_or_recapture_does_not_execute_remediation",
    "approval_receipt_recovery_or_recapture_does_not_execute_classification",
    "approval_receipt_recovery_or_recapture_does_not_classify_modules_again",
    "approval_receipt_recovery_or_recapture_does_not_identify_first_failure",
    "approval_receipt_recovery_or_recapture_does_not_identify_first_error",
    "approval_receipt_recovery_or_recapture_does_not_claim_traceback_root_cause",
    "approval_receipt_recovery_or_recapture_does_not_recommend_direct_code_remediation",
    "approval_receipt_recovery_or_recapture_does_not_create_diagnostic_results_review",
    "approval_receipt_recovery_or_recapture_does_not_create_remediation_or_method_candidate",
    "approval_receipt_recovery_or_recapture_does_not_create_new_retry_candidate",
    "approval_receipt_recovery_or_recapture_does_not_create_retry_results_review",
    "approval_receipt_recovery_or_recapture_does_not_create_integration_results_review",
    "approval_receipt_recovery_or_recapture_does_not_mark_integration_successful",
    "approval_receipt_recovery_or_recapture_does_not_generate_successful_integration_digest",
    "approval_receipt_recovery_or_recapture_does_not_treat_transient_success_as_durable_success",
    "approval_receipt_recovery_or_recapture_does_not_treat_future_recapture_as_retry",
    "approval_receipt_recovery_or_recapture_does_not_push_integration_branch",
    "approval_receipt_recovery_or_recapture_does_not_push_main",
    "approval_receipt_recovery_or_recapture_does_not_delete_integration_branch",
    "approval_receipt_recovery_or_recapture_does_not_delete_worktree",
    "approval_receipt_recovery_or_recapture_does_not_force_push",
    "approval_receipt_recovery_or_recapture_does_not_prune_remotes",
    "approval_receipt_recovery_or_recapture_does_not_modify_tags",
    "approval_receipt_recovery_or_recapture_does_not_modify_staged_evidence",
    "approval_receipt_recovery_or_recapture_does_not_regenerate_evidence",
    "approval_receipt_recovery_or_recapture_does_not_call_providers",
    "approval_receipt_recovery_or_recapture_does_not_acquire_market_data",
    "approval_receipt_recovery_or_recapture_does_not_regenerate_dataset",
    "approval_receipt_recovery_or_recapture_does_not_recompute_metrics",
    "approval_receipt_recovery_or_recapture_does_not_train_models",
    "approval_receipt_recovery_or_recapture_does_not_score_strategy",
    "approval_receipt_recovery_or_recapture_does_not_generate_recommendations",
    "approval_receipt_recovery_or_recapture_does_not_accept_predictive_usefulness",
    "approval_receipt_recovery_or_recapture_does_not_accept_profitability",
    "approval_receipt_recovery_or_recapture_does_not_authorize_runtime",
    "approval_receipt_recovery_or_recapture_does_not_authorize_broker_execution",
    "selected_recapture_package_approved_for_future_execution_only",
    "future_recapture_must_prewrite_durable_receipt_before_command", "future_recapture_is_not_retry_success",
    "priority_1_selection_is_not_root_cause", "module_concentration_is_not_failure_error_separation",
    "blocked_execution_remains_historically_blocked",
    "single_permitted_diagnostic_run_acknowledged_but_not_accepted_as_durable_success",
    "previous_receipt_recovery_candidate_operator_review_remains_source_evidence",
    "previous_receipt_recovery_candidate_remains_source_evidence",
    "previous_failure_diagnosis_remains_source_evidence", "previous_approval_remains_source_evidence",
    "previous_operator_review_remains_source_evidence", "previous_candidate_remains_source_evidence",
    "previous_planning_results_review_remains_valid", "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_execution_required_before_receipt_recovery_or_recapture",
    "separate_results_review_required_after_receipt_recovery_or_recapture",
    "separate_remediation_or_method_candidate_required_after_diagnostic_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "receipt_recovery_or_recapture_approval_created", "receipt_recovery_or_recapture_package_selected",
    "receipt_recovery_or_recapture_package_approved", "receipt_recovery_or_recapture_package_authorized",
    "controlled_recapture_package_selected", "controlled_recapture_package_approved",
    "controlled_recapture_package_authorized", "ready_for_receipt_recovery_or_recapture_execution",
    "ready_for_controlled_recapture_execution", "diagnostic_command_executed_once",
    "transient_success_artifact_returned",
]
FALSE_FIELDS = [
    "durable_success_receipt_retained", "diagnostic_exit_code_available", "diagnostic_duration_seconds_available",
    "stdout_hash_available", "stderr_hash_available", "stdout_byte_count_available", "stderr_byte_count_available",
    "combined_output_byte_count_available", "bounded_stdout_excerpt_available", "bounded_stderr_excerpt_available",
    "redaction_patterns_available", "success_payload_digest_available", "success_digest_manifest_digest_available",
    "unavailable_values_reconstructed", "unavailable_values_inferred", "diagnostic_command_rerun_to_recover_values",
    "receipt_recovery_package_selected", "receipt_recovery_package_approved", "receipt_recovery_package_authorized",
    "receipt_recovery_execution_performed", "receipt_recovered", "controlled_recapture_execution_performed",
    "diagnostic_command_executed_in_approval", "diagnostic_output_captured_in_approval",
    "targeted_pytest_performed", "full_pytest_performed", "retry_rerun_performed",
    "ready_for_diagnostic_results_review", "ready_for_remediation_or_method_candidate", "ready_for_retry_candidate",
    "diagnostic_results_review_created", "remediation_or_method_candidate_after_diagnostic_capture_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
    "main_merge_approval_created", "cache_read_in_approval", "cache_modified_in_approval",
    "operator_logs_parsed", "terminal_logs_parsed", "env_inspection_performed",
    "classification_execution_performed_in_approval", "remediation_execution_performed",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended", "retry_success_claimed",
    "main_merge_readiness_claimed", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_approval", "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError(ValueError):
    """Raised when attestation, source evidence, or approval boundaries fail."""


def _is_utc_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_candidate_digest: str,
    operator_confirms_source_failure_diagnosis_digest: str,
    operator_confirms_source_execution_digest: str,
    operator_confirms_source_blocked_manifest_digest: str,
    operator_confirms_source_blocked_reason: str,
    operator_confirms_source_primary_failure_class: str,
    operator_confirms_source_secondary_failure_class: str,
    operator_confirms_source_approval_digest: str,
    operator_confirms_source_targeted_diagnostic_candidate_operator_review_digest: str,
    operator_confirms_source_targeted_diagnostic_candidate_digest: str,
    operator_confirms_source_results_review_digest: str,
    operator_confirms_source_prioritized_planning_review_digest: str,
    operator_confirms_source_results_review_manifest_digest: str,
    operator_confirms_source_planning_execution_digest: str,
    operator_confirms_source_prioritized_planning_digest: str,
    operator_confirms_source_planning_digest_manifest_digest: str,
    operator_confirms_source_detail_binding_results_review_digest: str,
    operator_confirms_source_complete_29_row_binding_digest: str,
    operator_confirms_source_materialized_payload_digest: str,
    operator_confirms_source_detail_binding_approval_digest: str,
    operator_confirms_source_recovery_results_review_digest: str,
    operator_confirms_source_recovery_detail_digest: str,
    operator_confirms_source_after_v2_approval_digest: str,
    operator_confirms_source_module_grouping_digest: str,
    operator_confirms_retry_execution_commit: str,
    operator_confirms_retry_failure_counts: bool,
    operator_confirms_priority_1_top_module_paths: bool,
    operator_confirms_priority_1_total_612: bool,
    operator_confirms_top_10_total_1069: bool,
    operator_confirms_module_summary_count_29: bool,
    operator_confirms_failed_or_errored_nodeids_1404: bool,
    operator_confirms_diagnostic_command_executed_once: bool,
    operator_confirms_transient_success_artifact_returned: bool,
    operator_confirms_durable_success_receipt_not_retained: bool,
    operator_confirms_unavailable_payload_fields: bool,
    operator_confirms_unavailable_values_not_reconstructed: bool,
    operator_confirms_unavailable_values_not_inferred: bool,
    operator_confirms_selected_receipt_recovery_or_recapture_package: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_no_receipt_recovery: bool,
    operator_confirms_no_recapture: bool,
    operator_confirms_no_diagnostic_command: bool,
    operator_confirms_no_diagnostic_output: bool,
    operator_confirms_no_targeted_pytest: bool,
    operator_confirms_no_full_pytest: bool,
    operator_confirms_no_retry: bool,
    operator_confirms_no_cache_read: bool,
    operator_confirms_no_cache_modification: bool,
    operator_confirms_no_terminal_log_parse: bool,
    operator_confirms_no_operator_log_parse: bool,
    operator_confirms_no_env_inspection: bool,
    operator_confirms_no_output_reconstruction: bool,
    operator_confirms_no_remediation_execution: bool,
    operator_confirms_no_classification_execution: bool,
    operator_confirms_no_failure_error_separation: bool,
    operator_confirms_no_first_failure: bool,
    operator_confirms_no_first_error: bool,
    operator_confirms_no_traceback_root_cause: bool,
    operator_confirms_no_direct_remediation: bool,
    operator_confirms_no_retry_success: bool,
    operator_confirms_no_main_merge_readiness: bool,
    operator_confirms_no_new_retry_candidate: bool,
    operator_confirms_no_retry_results_review: bool,
    operator_confirms_no_integration_results_review: bool,
    operator_confirms_no_main_merge_approval: bool,
    operator_confirms_no_integration_success: bool,
    operator_confirms_no_successful_integration_digest: bool,
    operator_confirms_no_integration_branch_push: bool,
    operator_confirms_no_main_push: bool,
    operator_confirms_origin_main_not_modified: bool,
    operator_confirms_no_branch_delete: bool,
    operator_confirms_no_force_push: bool,
    operator_confirms_no_tag_mutation: bool,
    operator_confirms_no_evidence_regeneration: bool,
    operator_confirms_no_marketflow_commit: bool,
    operator_confirms_no_pytest_cache_commit: bool,
    operator_confirms_no_provider_requests: bool,
    operator_confirms_no_market_data_acquisition: bool,
    operator_confirms_no_dataset_generation: bool,
    operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_runtime_not_authorized: bool,
    operator_confirms_broker_not_authorized: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_secret_capture_or_commit: bool,
    selected_receipt_recovery_or_recapture_package: str = SELECTED_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build and validate the exact non-secret operator attestation."""

    values = locals()
    attestation = {
        "operator_decision": operator_decision,
        "selected_receipt_recovery_or_recapture_package": selected_receipt_recovery_or_recapture_package,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": ATTESTATION_VERSION,
        "operator_reference": operator_reference,
        **{field: values[field] for field in STRING_CONFIRMATIONS},
        **{field: values[field] for field in BOOLEAN_CONFIRMATION_FIELDS},
    }
    _validate_attestation(attestation)
    attestation["operator_attestation_digest"] = semantic_digest(attestation)
    return attestation


def _validate_attestation(attestation: Any) -> None:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError
    if not isinstance(attestation, Mapping):
        raise error("operator attestation must be an object")
    constants = {
        "operator_decision": OPERATOR_DECISION,
        "selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        "operator_attestation_phrase": REQUIRED_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_ATTESTATION_PHRASE_V1,
        "operator_attestation_version": ATTESTATION_VERSION,
        **STRING_CONFIRMATIONS,
    }
    for field, expected in constants.items():
        if attestation.get(field) != expected:
            raise error(f"{field} mismatch")
    if not isinstance(attestation.get("operator_reference"), str) or not attestation["operator_reference"].strip():
        raise error("operator reference required")
    if not _is_utc_timestamp(attestation.get("operator_attestation_timestamp_utc")):
        raise error("UTC attestation timestamp required")
    for field in BOOLEAN_CONFIRMATION_FIELDS:
        if attestation.get(field) is not True:
            raise error(f"{field} must be true")
    digest = attestation.get("operator_attestation_digest")
    if digest is not None:
        payload = dict(attestation)
        payload.pop("operator_attestation_digest", None)
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != semantic_digest(payload):
            raise error("operator attestation digest mismatch")


def _expected_source_review() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND, "review_status": source.REVIEW_STATUS,
        "review_scope": source.REVIEW_SCOPE, source.DIGEST_KEY: SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_receipt_recovery_or_recapture_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
        "recommended_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        "receipt_recovery_or_recapture_candidate_operator_review_created": True,
        "receipt_recovery_or_recapture_candidate_operator_review_ready": True,
        "source_candidate_reviewed": True, "source_failure_diagnosis_reviewed": True,
        "receipt_loss_failure_class_reviewed": True, "unavailable_payload_fields_reviewed": True,
        "future_receipt_recovery_or_recapture_packages_reviewed": True,
        "future_receipt_recovery_requirements_reviewed": True,
        "future_controlled_recapture_requirements_reviewed": True,
        "future_recovery_or_recapture_plan_reviewed": True,
        "future_controlled_recapture_command_template_reviewed": True,
        "future_durable_receipt_safeguards_reviewed": True,
        "planned_outputs_reviewed": True, "non_goals_reviewed": True,
        "recommended_package_selected": False, "receipt_recovery_package_selected": False,
        "receipt_recovery_package_approved": False, "receipt_recovery_package_authorized": False,
        "receipt_recovery_execution_performed": False, "receipt_recovered": False,
        "controlled_recapture_package_selected": False, "controlled_recapture_package_approved": False,
        "controlled_recapture_package_authorized": False, "controlled_recapture_execution_performed": False,
        "ready_for_receipt_recovery_or_recapture_approval": False,
        "ready_for_receipt_recovery_or_recapture_execution": False,
        "ready_for_diagnostic_results_review": False, "ready_for_remediation_or_method_candidate": False,
        "ready_for_retry_candidate": False,
    }


def _bind_source_review(value: dict | None) -> dict[str, Any]:
    expected = _expected_source_review()
    if value is None:
        return deepcopy(expected)
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError("source operator review must be an object")
    try:
        source.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(dict(value))
    except source.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError("source operator review validation failed") from exc
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError(f"source operator review {field} mismatch")
    return deepcopy(expected)


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


SOURCE_CHECKS = {
    "source_receipt_recovery_or_recapture_candidate_operator_review_digest": "source_operator_review_digest_bound",
    "source_receipt_recovery_or_recapture_candidate_digest": "source_candidate_digest_bound",
    "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest": "source_failure_diagnosis_digest_bound",
    "source_targeted_diagnostic_output_capture_execution_digest": "source_execution_digest_bound",
    "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest": "source_blocked_manifest_digest_bound",
    "source_targeted_diagnostic_output_capture_execution_blocked_reason": "source_blocked_reason_bound",
    "source_primary_failure_class": "source_primary_failure_class_bound",
    "source_secondary_failure_class": "source_secondary_failure_class_bound",
    "source_targeted_diagnostic_output_capture_approval_digest": "source_approval_digest_bound",
    "source_targeted_diagnostic_output_capture_candidate_operator_review_digest": "source_targeted_diagnostic_candidate_operator_review_digest_bound",
    "source_targeted_diagnostic_output_capture_candidate_digest": "source_targeted_diagnostic_candidate_digest_bound",
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


def _retry_context() -> dict[str, Any]:
    return {
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_pytest_working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
        "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "retry_pytest_first_result_authoritative": True, "retry_pytest_passed": False,
        "retry_pytest_failed": True, "root_full_regression_is_retry_evidence": False,
    }


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [_check(check_id, SOURCE_BINDINGS[field], approval.get(field)) for field, check_id in SOURCE_CHECKS.items()]
    attestation = approval.get("operator_attestation", {})
    checks.extend([
        _check("retry_execution_commit_bound", RETRY_EXECUTION_COMMIT, approval.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", _retry_context()["counts"], approval.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", [item["module_path"] for item in source.source.PRIORITY_1_TARGET_MODULES], [item.get("module_path") for item in approval.get("priority_1_target_modules", [])]),
        _check("priority_1_total_612_bound", 612, approval.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, approval.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, approval.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, approval.get("failed_or_errored_nodeids_count")),
        _check("diagnostic_command_executed_once_acknowledged", True, approval.get("diagnostic_command_executed_once")),
        _check("transient_success_acknowledged", True, approval.get("transient_success_artifact_returned")),
        _check("durable_success_receipt_missing", False, approval.get("durable_success_receipt_retained")),
        _check("unavailable_fields_preserved", source.source.UNAVAILABLE_FIELDS, approval.get("unavailable_diagnostic_payload_fields")),
        _check("missing_values_not_reconstructed", False, approval.get("unavailable_values_reconstructed")),
        _check("missing_values_not_inferred", False, approval.get("unavailable_values_inferred")),
        _check("operator_decision_matches", OPERATOR_DECISION, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_ATTESTATION_PHRASE_V1, attestation.get("operator_attestation_phrase")),
        _check("approval_created_true", True, approval.get("receipt_recovery_or_recapture_approval_created")),
        _check("approval_scope_only", APPROVAL_SCOPE, approval.get("approval_scope")),
        _check("selected_receipt_recovery_or_recapture_package_bound", SELECTED_PACKAGE, approval.get("selected_receipt_recovery_or_recapture_package")),
        _check("receipt_recovery_or_recapture_package_selected_true", True, approval.get("receipt_recovery_or_recapture_package_selected")),
        _check("receipt_recovery_or_recapture_package_approved_true", True, approval.get("receipt_recovery_or_recapture_package_approved")),
        _check("receipt_recovery_or_recapture_package_authorized_true", True, approval.get("receipt_recovery_or_recapture_package_authorized")),
        _check("controlled_recapture_package_selected_true", True, approval.get("controlled_recapture_package_selected")),
        _check("controlled_recapture_package_approved_true", True, approval.get("controlled_recapture_package_approved")),
        _check("controlled_recapture_package_authorized_true", True, approval.get("controlled_recapture_package_authorized")),
        _check("ready_for_receipt_recovery_or_recapture_execution_true", True, approval.get("ready_for_receipt_recovery_or_recapture_execution")),
        _check("future_recapture_command_template_approved_not_executed", FUTURE_COMMAND_TEMPLATE, approval.get("future_controlled_recapture_command_template")),
        _check("future_requirements_approved_for_future_execution", APPROVED_REQUIREMENTS, approval.get("approved_future_receipt_recovery_or_recapture_requirements")),
        _check("future_plan_approved_not_executed", APPROVED_PLAN, approval.get("approved_future_recovery_or_recapture_plan")),
        _check("future_durable_receipt_safeguards_approved_not_executed", APPROVED_SAFEGUARDS, approval.get("approved_future_durable_receipt_safeguards")),
        _check("planned_outputs_authorized_not_generated", PLANNED_OUTPUTS, approval.get("planned_outputs")),
        _check("supporting_packages_not_selected", SUPPORTING_PACKAGES, approval.get("supporting_packages")),
        _check("blocked_packages_not_approved", BLOCKED_PACKAGES, approval.get("blocked_packages")),
    ])
    aliases = {
        "receipt_recovery_execution_performed": "receipt_recovery_execution_false",
        "receipt_recovered": "receipt_recovered_false",
        "controlled_recapture_execution_performed": "controlled_recapture_execution_false",
        "diagnostic_command_executed_in_approval": "diagnostic_command_executed_in_approval_false",
        "diagnostic_output_captured_in_approval": "diagnostic_output_captured_in_approval_false",
        "targeted_pytest_performed": "targeted_pytest_false", "full_pytest_performed": "full_pytest_false",
        "retry_rerun_performed": "retry_rerun_false", "cache_read_in_approval": "cache_read_in_approval_false",
        "cache_modified_in_approval": "cache_modified_in_approval_false",
        "terminal_logs_parsed": "terminal_logs_parsed_false", "operator_logs_parsed": "operator_logs_parsed_false",
        "env_inspection_performed": "env_inspection_false",
        "unavailable_values_reconstructed": "unavailable_values_reconstructed_false",
        "unavailable_values_inferred": "unavailable_values_inferred_false",
        "diagnostic_results_review_created": "diagnostic_results_review_created_false",
        "remediation_or_method_candidate_after_diagnostic_capture_created": "remediation_or_method_candidate_created_false",
        "new_retry_candidate_created": "new_retry_candidate_created_false", "new_retry_executed": "new_retry_executed_false",
        "new_retry_results_review_created": "new_retry_results_review_created_false",
        "main_merge_approval_created": "main_merge_approval_created_false",
        "classification_execution_performed_in_approval": "classification_execution_false",
        "remediation_execution_performed": "remediation_execution_false",
        "failure_modules_classified": "failure_modules_classified_false",
        "error_modules_classified": "error_modules_classified_false",
        "failure_error_separation_claimed": "failure_error_separation_claimed_false",
        "first_failure_identified": "first_failure_identified_false", "first_error_identified": "first_error_identified_false",
        "first_order_claim_made": "first_order_claim_made_false", "traceback_root_cause_claimed": "traceback_root_cause_claimed_false",
        "direct_code_remediation_recommended": "direct_code_remediation_recommended_false",
        "retry_success_claimed": "retry_success_claimed_false", "main_merge_readiness_claimed": "main_merge_readiness_claimed_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "integration_branch_pushed": "integration_branch_pushed_false", "main_push_performed": "main_push_false",
        "origin_main_modified_by_this_task": "origin_main_modified_false",
        "marketflow_outputs_committed": "marketflow_outputs_committed_false",
        "pytest_cache_committed": "pytest_cache_committed_false", "evidence_regenerated": "evidence_regenerated_false",
        "provider_requests_made_in_approval": "provider_requests_false",
        "market_data_acquisition_performed_in_approval": "market_data_acquisition_false",
        "dataset_generation_performed_in_approval": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    checklist_false_fields = list(aliases)
    checks.extend(_check(aliases[field], False, approval.get(field)) for field in checklist_false_fields)
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, approval.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, approval.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, approval.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, approval.get("broker_execution")),
        _check("next_chain_defined", NEXT_CHAIN, approval.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, approval.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, approval.get("risk_controls")),
        _check("no_tracked_marketflow_files", False, approval.get("marketflow_outputs_committed")),
        _check("no_tracked_pytest_cache_files", False, approval.get("pytest_cache_committed")),
    ])
    return checks


def _summary(approval: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(item["status"] == PASS for item in checklist)
    fields = [
        "receipt_recovery_or_recapture_approval_created", "receipt_recovery_or_recapture_package_selected",
        "receipt_recovery_or_recapture_package_approved", "receipt_recovery_or_recapture_package_authorized",
        "selected_receipt_recovery_or_recapture_package", "controlled_recapture_package_selected",
        "controlled_recapture_package_approved", "controlled_recapture_package_authorized",
        "receipt_recovery_package_selected", "receipt_recovery_package_approved", "receipt_recovery_execution_performed",
        "receipt_recovered", "controlled_recapture_execution_performed", "diagnostic_command_executed_in_approval",
        "diagnostic_output_captured_in_approval", "targeted_pytest_performed", "retry_rerun_performed",
        "full_pytest_performed", "diagnostic_command_executed_once", "transient_success_artifact_returned",
        "durable_success_receipt_retained", "unavailable_values_reconstructed", "unavailable_values_inferred",
        "ready_for_receipt_recovery_or_recapture_execution", "ready_for_controlled_recapture_execution",
        "ready_for_diagnostic_results_review", "ready_for_remediation_or_method_candidate", "ready_for_retry_candidate",
        "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "priority_1_total_nodeids", "top_10_count_sum",
    ]
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed, **{field: approval.get(field) for field in fields},
        "priority_1_top_module_count": 5, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "recommended_next_task": NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _approval_digest(approval: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(approval))
    for field in ("checklist", "summary", DIGEST_KEY, "approval_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(
    *, source_operator_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Create approval for future controlled recapture after exact attestation."""

    bound_review = _bind_source_review(source_operator_review)
    _validate_attestation(operator_attestation)
    approval: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True, "approval_only": True,
        "source_receipt_recovery_or_recapture_candidate_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_receipt_recovery_or_recapture_candidate_operator_review_status": source.REVIEW_STATUS,
        "source_receipt_recovery_or_recapture_candidate_operator_review_scope": source.REVIEW_SCOPE,
        **deepcopy(SOURCE_BINDINGS), "operator_attestation": deepcopy(operator_attestation),
        "source_operator_review_summary": bound_review,
        "retry_execution_commit": RETRY_EXECUTION_COMMIT, "retry_failure_context": _retry_context(),
        "unavailable_diagnostic_payload_fields": list(source.source.UNAVAILABLE_FIELDS),
        "priority_1_target_modules": deepcopy(source.source.PRIORITY_1_TARGET_MODULES),
        "priority_1_total_nodeids": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "approved_package": deepcopy(APPROVED_PACKAGE),
        "approved_future_receipt_recovery_or_recapture_requirements": deepcopy(APPROVED_REQUIREMENTS),
        "approved_future_recovery_or_recapture_plan": deepcopy(APPROVED_PLAN),
        "future_controlled_recapture_command_template": deepcopy(FUTURE_COMMAND_TEMPLATE),
        "approved_future_durable_receipt_safeguards": deepcopy(APPROVED_SAFEGUARDS),
        "planned_outputs": deepcopy(PLANNED_OUTPUTS), "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "blocked_packages": deepcopy(BLOCKED_PACKAGES), "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    approval.update({field: True for field in TRUE_FIELDS})
    approval.update({field: False for field in FALSE_FIELDS})
    approval["digest_manifest"] = {
        "source_operator_review": SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate": source.SOURCE_CANDIDATE_DIGEST,
        "operator_attestation": operator_attestation["operator_attestation_digest"],
        "approved_package": semantic_digest(APPROVED_PACKAGE), "approved_requirements": semantic_digest(APPROVED_REQUIREMENTS),
        "approved_plan": semantic_digest(APPROVED_PLAN), "future_command_template": semantic_digest(FUTURE_COMMAND_TEMPLATE),
        "approved_safeguards": semantic_digest(APPROVED_SAFEGUARDS), "planned_outputs": semantic_digest(PLANNED_OUTPUTS),
        "supporting_packages": semantic_digest(SUPPORTING_PACKAGES), "blocked_packages": semantic_digest(BLOCKED_PACKAGES),
    }
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval, approval["checklist"])
    approval[DIGEST_KEY] = _approval_digest(approval)
    approval["approval_digest"] = approval[DIGEST_KEY]
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(
    approval: dict,
) -> dict:
    """Reject incomplete attestation, source drift, or authority expansion."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError
    if not isinstance(approval, dict):
        raise error("approval must be an object")
    constants = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "selected_receipt_recovery_or_recapture_package": SELECTED_PACKAGE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True, "approval_only": True,
        "source_receipt_recovery_or_recapture_candidate_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_receipt_recovery_or_recapture_candidate_operator_review_status": source.REVIEW_STATUS,
        "source_receipt_recovery_or_recapture_candidate_operator_review_scope": source.REVIEW_SCOPE,
        "retry_execution_commit": RETRY_EXECUTION_COMMIT, **SOURCE_BINDINGS,
    }
    for field, expected in constants.items():
        if approval.get(field) != expected:
            raise error(f"{field} mismatch")
    _validate_attestation(approval.get("operator_attestation"))
    structures = {
        "source_operator_review_summary": _expected_source_review(), "retry_failure_context": _retry_context(),
        "unavailable_diagnostic_payload_fields": source.source.UNAVAILABLE_FIELDS,
        "priority_1_target_modules": source.source.PRIORITY_1_TARGET_MODULES,
        "approved_package": APPROVED_PACKAGE,
        "approved_future_receipt_recovery_or_recapture_requirements": APPROVED_REQUIREMENTS,
        "approved_future_recovery_or_recapture_plan": APPROVED_PLAN,
        "future_controlled_recapture_command_template": FUTURE_COMMAND_TEMPLATE,
        "approved_future_durable_receipt_safeguards": APPROVED_SAFEGUARDS,
        "planned_outputs": PLANNED_OUTPUTS, "supporting_packages": SUPPORTING_PACKAGES,
        "blocked_packages": BLOCKED_PACKAGES, "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in structures.items():
        if approval.get(field) != expected:
            raise error(f"{field} mismatch")
    scalars = {
        "priority_1_total_nodeids": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
    }
    for field, expected in scalars.items():
        if approval.get(field) != expected:
            raise error(f"{field} mismatch")
    if any(approval.get(field) is not True for field in TRUE_FIELDS):
        raise error("approval authority missing")
    if any(approval.get(field) is not False for field in FALSE_FIELDS):
        raise error("closed boundary opened")
    if approval.get("predictive_usefulness") != NOT_ACCEPTED or approval.get("profitability") != NOT_ACCEPTED:
        raise error("acceptance boundary changed")
    if any(approval.get(field) != NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")):
        raise error("runtime boundary changed")
    manifest = {
        "source_operator_review": SOURCE_OPERATOR_REVIEW_DIGEST, "source_candidate": source.SOURCE_CANDIDATE_DIGEST,
        "operator_attestation": approval["operator_attestation"]["operator_attestation_digest"],
        "approved_package": semantic_digest(APPROVED_PACKAGE), "approved_requirements": semantic_digest(APPROVED_REQUIREMENTS),
        "approved_plan": semantic_digest(APPROVED_PLAN), "future_command_template": semantic_digest(FUTURE_COMMAND_TEMPLATE),
        "approved_safeguards": semantic_digest(APPROVED_SAFEGUARDS), "planned_outputs": semantic_digest(PLANNED_OUTPUTS),
        "supporting_packages": semantic_digest(SUPPORTING_PACKAGES), "blocked_packages": semantic_digest(BLOCKED_PACKAGES),
    }
    if approval.get("digest_manifest") != manifest:
        raise error("digest manifest mismatch")
    checklist = _checklist(approval)
    if approval.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    summary = _summary(approval, checklist)
    if approval.get("summary") != summary:
        raise error("summary mismatch")
    digest = approval.get(DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _approval_digest(approval):
        raise error("approval digest mismatch")
    if approval.get("approval_digest") != digest:
        raise error("approval digest alias mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "approval_digest": digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(
    output_dir: str | Path, *, source_operator_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Write deterministic approval JSON outside protected runtime paths."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError("protected output directory")
    approval = build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(source_operator_review=source_operator_review, operator_attestation=operator_attestation)
    path = output / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError("output exists")
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": ARTIFACT_KIND, "approval_status": APPROVAL_STATUS, "approval_digest": approval[DIGEST_KEY], "payload_sha256": sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized Markdown summary after strict validation."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(approval)
    sections = [
        ("Operator Attestation", [approval["operator_attestation"]["operator_reference"], approval["operator_attestation"]["operator_attestation_timestamp_utc"], REQUIRED_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_ATTESTATION_PHRASE_V1]),
        ("Source Receipt Recovery or Recapture Candidate Operator Review", [SOURCE_OPERATOR_REVIEW_DIGEST, source.REVIEW_STATUS]),
        ("Source Receipt Recovery or Recapture Candidate", [source.SOURCE_CANDIDATE_DIGEST]),
        ("Source Failure Diagnosis", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"], SOURCE_BINDINGS["source_primary_failure_class"]]),
        ("Source Targeted Diagnostic Output Capture Execution", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_digest"], SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"]]),
        ("Source Approval and Operator Review", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_approval_digest"], SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_candidate_operator_review_digest"]]),
        ("Source Planning and Detail Binding Evidence", [SOURCE_BINDINGS["source_results_review_digest"], SOURCE_BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the failed retry remains authoritative."]),
        ("Approval Scope", [APPROVAL_SCOPE]),
        ("Selected Receipt Recovery or Recapture Package", [SELECTED_PACKAGE, APPROVED_PACKAGE["approval_status"]]),
        ("Priority 1 Target Modules", [f"{item['module_path']}: {item['failed_or_errored_nodeid_count']}" for item in source.source.PRIORITY_1_TARGET_MODULES]),
        ("Unavailable Diagnostic Payload Fields", source.source.UNAVAILABLE_FIELDS),
        ("Future Controlled Recapture Command Template", [FUTURE_COMMAND_TEMPLATE["future_recapture_command_template_status"], FUTURE_COMMAND_TEMPLATE["future_recapture_command_template"]]),
        ("Approved Future Recovery or Recapture Requirements", [item["requirement_id"] for item in APPROVED_REQUIREMENTS]),
        ("Approved Future Recovery or Recapture Plan", [f"{item['step_id']}. {item['step']}" for item in APPROVED_PLAN]),
        ("Approved Future Durable Receipt Safeguards", [item["safeguard_id"] for item in APPROVED_SAFEGUARDS]),
        ("Planned Outputs", [item["output_id"] for item in PLANNED_OUTPUTS]),
        ("Supporting Packages", [item["package_id"] for item in SUPPORTING_PACKAGES]),
        ("Blocked Packages", [item["package_id"] for item in BLOCKED_PACKAGES]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Only future controlled recapture execution is authorized. No receipt recovery, recapture, diagnostic, retry, main, runtime, or trading action occurs in this approval."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["No secrets, provider calls, cache access, diagnostic execution, retry, remediation, runtime, or trading action is permitted by this approval artifact."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Receipt Recovery or Recapture Approval v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVED_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVED = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_ONLY_NOT_EXECUTION_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_CONTROLLED_SINGLE_RECAPTURE_WITH_PREWRITE_RECEIPT_FILE_AND_NO_CACHEPROVIDER = SELECTED_PACKAGE
