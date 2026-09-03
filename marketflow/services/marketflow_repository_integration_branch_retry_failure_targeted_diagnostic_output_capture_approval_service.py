"""Approve future targeted diagnostic-output capture without executing it."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVED_V1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVED"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ONLY_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1"
DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_digest"
SOURCE_OPERATOR_REVIEW_DIGEST = "ddb5a8eb865062d4b9d77b84eeedb9155ffe3ee08a0af229be24988a5e00bf60"
SELECTED_PACKAGE = source.PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS
OPERATOR_DECISION = "APPROVE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE"
ATTESTATION_VERSION = "targeted_diagnostic_output_capture_approval_attestation_v1"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ATTESTATION_PHRASE_V1 = (
    "APPROVE TARGETED DIAGNOSTIC OUTPUT CAPTURE "
    "PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS MARKETFLOW CAPTURE BOUNDED "
    "DIAGNOSTIC OUTPUT FOR PRIORITY 1 TOP MODULE GROUPS FOR FUTURE EXECUTION ONLY NO DIAGNOSTIC EXECUTION NOW "
    "NO PYTEST NOW NO TARGETED PYTEST NOW NO RETRY NO CACHE READ NO MAIN PUSH "
    "DIAGNOSTIC_CAPTURE_APPROVAL_ONLY_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
)

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVED_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVED = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ONLY_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS = SELECTED_PACKAGE

SOURCE_BINDINGS = {
    "source_targeted_diagnostic_output_capture_candidate_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    **deepcopy(source.SOURCE_BINDINGS),
}

STRING_CONFIRMATIONS = {
    "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_results_review_digest": source.SOURCE_BINDINGS["source_results_review_digest"],
    "operator_confirms_source_prioritized_planning_review_digest": source.SOURCE_BINDINGS["source_prioritized_planning_review_digest"],
    "operator_confirms_source_results_review_manifest_digest": source.SOURCE_BINDINGS["source_results_review_manifest_digest"],
    "operator_confirms_source_planning_execution_digest": source.SOURCE_BINDINGS["source_planning_execution_digest"],
    "operator_confirms_source_prioritized_planning_digest": source.SOURCE_BINDINGS["source_prioritized_planning_digest"],
    "operator_confirms_source_planning_digest_manifest_digest": source.SOURCE_BINDINGS["source_planning_digest_manifest_digest"],
    "operator_confirms_source_detail_binding_results_review_digest": source.SOURCE_BINDINGS["source_detail_binding_results_review_digest"],
    "operator_confirms_source_complete_29_row_binding_digest": source.SOURCE_BINDINGS["source_complete_29_row_binding_digest"],
    "operator_confirms_source_materialized_payload_digest": source.SOURCE_BINDINGS["source_materialized_payload_digest"],
    "operator_confirms_source_detail_binding_approval_digest": source.SOURCE_BINDINGS["source_detail_binding_approval_digest"],
    "operator_confirms_source_prior_blocked_detail_binding_execution_digest": source.SOURCE_BINDINGS["source_prior_blocked_detail_binding_execution_digest"],
    "operator_confirms_source_prior_blocked_detail_binding_reason": source.SOURCE_BINDINGS["source_prior_blocked_detail_binding_reason"],
    "operator_confirms_source_recovery_results_review_digest": source.SOURCE_BINDINGS["source_recovery_results_review_digest"],
    "operator_confirms_source_recovery_detail_digest": source.SOURCE_BINDINGS["source_recovery_detail_digest"],
    "operator_confirms_source_after_v2_approval_digest": source.SOURCE_BINDINGS["source_after_v2_approval_digest"],
    "operator_confirms_source_module_grouping_digest": source.SOURCE_BINDINGS["source_module_grouping_digest"],
    "operator_confirms_retry_execution_commit": source.source.RETRY_EXECUTION_COMMIT,
    "operator_confirms_selected_diagnostic_capture_package": SELECTED_PACKAGE,
}
BOOLEAN_CONFIRMATION_FIELDS = [
    "operator_confirms_retry_failure_counts", "operator_confirms_priority_1_top_module_paths",
    "operator_confirms_priority_1_top_module_counts", "operator_confirms_priority_1_total_612",
    "operator_confirms_top_10_total_1069", "operator_confirms_module_summary_count_29",
    "operator_confirms_failed_or_errored_nodeids_1404", "operator_confirms_approval_scope_only",
    "operator_confirms_no_diagnostic_execution", "operator_confirms_no_diagnostic_command",
    "operator_confirms_no_diagnostic_output", "operator_confirms_no_targeted_pytest",
    "operator_confirms_no_full_pytest", "operator_confirms_no_retry", "operator_confirms_no_cache_read",
    "operator_confirms_no_cache_modification", "operator_confirms_no_planning_rerun",
    "operator_confirms_no_detail_binding_rerun", "operator_confirms_no_materialization_rerun",
    "operator_confirms_no_source_recovery_rerun", "operator_confirms_no_remediation_execution",
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
    "operator_confirms_no_env_inspection", "operator_confirms_no_market_data_acquisition",
    "operator_confirms_no_dataset_generation", "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training", "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_trade_recommendations", "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance", "operator_confirms_runtime_not_authorized",
    "operator_confirms_broker_not_authorized", "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_secret_capture_or_commit",
]

APPROVED_PACKAGE = {
    "package_id": SELECTED_PACKAGE,
    "approval_status": "APPROVED_FOR_FUTURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_ONLY",
    "selected": True, "approved": True, "authorized_for_future_execution": True, "executed": False,
    "purpose": "Future execution may run controlled targeted diagnostic output capture against the five Priority 1 module files only, with bounded stdout/stderr capture, cache-write controls, no full pytest, no retry-success claim, no root-cause claim, no remediation execution, and no main-merge authority.",
}
APPROVED_REQUIREMENTS = [
    {"requirement_id": item["requirement_id"], "approval_status": "APPROVED_FOR_FUTURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_ONLY", "execution_status": "NOT_EXECUTED"}
    for item in source.REVIEWED_REQUIREMENTS
]
APPROVED_PLAN_STEPS = [
    "Bind this approval, source operator review, candidate, and source results-review evidence.",
    "Bind the planning execution digest, prioritized planning digest, and manifest digest.",
    "Bind the reviewed complete 29-row detail source and Priority 1 top module list.",
    "Use the selected targeted diagnostic output capture package.",
    "Verify the selected package targets only the five approved Priority 1 module paths unless a separate approval expands scope.",
    "Build and preserve an explicit diagnostic command template for future execution.",
    "Use the detached integration worktree as the future diagnostic working directory if execution is separately invoked.",
    "Use the repository virtual environment Python executable if execution is separately invoked.",
    "Disable or control pytest cache writes if pytest-based diagnostic capture is executed.",
    "Capture command, cwd, target modules, exit code, stdout, stderr, duration, and bounded diagnostic excerpts if execution is separately invoked.",
    "Preserve the failed retry as authoritative and avoid retry-success claims.",
    "Require diagnostic capture results review before any remediation/method candidate.",
    "Keep new retry, main merge, runtime, and trading closed.",
]
APPROVED_PLAN = [
    {"step_id": index, "step": step, "approval_status": "APPROVED_FOR_FUTURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_ONLY", "execution_status": "NOT_EXECUTED"}
    for index, step in enumerate(APPROVED_PLAN_STEPS, start=1)
]
FUTURE_COMMAND_TEMPLATE = {
    "future_diagnostic_command_template_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
    "future_diagnostic_working_directory": source.source.FUTURE_COMMAND_TEMPLATE["future_diagnostic_working_directory"],
    "future_diagnostic_python_executable": source.source.FUTURE_COMMAND_TEMPLATE["future_diagnostic_python_executable"],
    "future_diagnostic_command_template": source.source.FUTURE_COMMAND_TEMPLATE["future_diagnostic_command_template"],
    "future_diagnostic_command_is_retry": False, "future_diagnostic_command_is_full_pytest": False,
    "future_diagnostic_command_executed": False,
}
PLANNED_OUTPUT_IDS = [
    "targeted_diagnostic_output_capture_approval_manifest", "priority_1_top_module_target_selection_report",
    "diagnostic_command_template_report", "diagnostic_output_capture_boundary_report",
    "diagnostic_output_capture_integrity_requirements", "diagnostic_output_volume_bound_plan",
    "diagnostic_cache_write_prevention_plan", "diagnostic_secret_avoidance_plan",
    "diagnostic_results_review_enablement_report", "remediation_or_method_candidate_enablement_report",
    "retry_gate_preservation_report", "unsupported_claims_boundary_report",
    "recommended_next_package_report", "digest_manifest",
]
PLANNED_OUTPUTS = [{"output_id": output_id, "status": "AUTHORIZED_NOT_GENERATED"} for output_id in PLANNED_OUTPUT_IDS]

SUPPORTING_PACKAGE_STATUSES = [
    "AVAILABLE_NOT_SELECTED_HIGH_CONTROL", "AVAILABLE_NOT_SELECTED",
    "AVAILABLE_NOT_SELECTED_NOT_RECOMMENDED_FOR_FIRST_PASS", "AVAILABLE_NOT_SELECTED", "AVAILABLE_NOT_SELECTED",
]
SUPPORTING_PACKAGES = [
    {"package_id": package["package_id"], "approval_status": status, "selected": False, "approved": False, "executed": False}
    for package, status in zip(source.REVIEWED_PACKAGES[1:6], SUPPORTING_PACKAGE_STATUSES, strict=True)
]
BLOCKED_PACKAGES = [
    {"package_id": package["package_id"], "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False, "executed": False}
    for package in source.REVIEWED_PACKAGES[6:]
]

NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_V1"
NEXT_CHAIN = [
    "Targeted Diagnostic Output Capture Execution v1, if approved.",
    "Targeted Diagnostic Output Capture Results Review v1.",
    "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1, if needed.",
    "Remediation or Method Operator Review v1, if needed.", "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.", "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "targeted_diagnostic_output_capture_execution_if_approved", "targeted_diagnostic_output_capture_results_review",
    "retry_failure_remediation_or_method_candidate_after_diagnostic_capture_if_needed",
    "remediation_or_method_operator_review_if_needed", "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved", "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "approval_diagnostic_capture_does_not_execute_diagnostic_capture", "approval_diagnostic_capture_does_not_run_pytest",
    "approval_diagnostic_capture_does_not_run_targeted_pytest", "approval_diagnostic_capture_does_not_run_full_pytest",
    "approval_diagnostic_capture_does_not_rerun_retry", "approval_diagnostic_capture_does_not_read_cache",
    "approval_diagnostic_capture_does_not_modify_cache", "approval_diagnostic_capture_does_not_rerun_planning",
    "approval_diagnostic_capture_does_not_rerun_detail_binding", "approval_diagnostic_capture_does_not_rerun_materialization",
    "approval_diagnostic_capture_does_not_rerun_source_recovery", "approval_diagnostic_capture_does_not_execute_remediation",
    "approval_diagnostic_capture_does_not_execute_classification", "approval_diagnostic_capture_does_not_classify_modules_again",
    "approval_diagnostic_capture_does_not_identify_first_failure", "approval_diagnostic_capture_does_not_identify_first_error",
    "approval_diagnostic_capture_does_not_claim_traceback_root_cause", "approval_diagnostic_capture_does_not_recommend_direct_code_remediation",
    "approval_diagnostic_capture_does_not_create_diagnostic_results_review", "approval_diagnostic_capture_does_not_create_new_retry_candidate",
    "approval_diagnostic_capture_does_not_create_retry_results_review", "approval_diagnostic_capture_does_not_create_integration_results_review",
    "approval_diagnostic_capture_does_not_mark_integration_successful", "approval_diagnostic_capture_does_not_generate_successful_integration_digest",
    "approval_diagnostic_capture_does_not_push_integration_branch", "approval_diagnostic_capture_does_not_push_main",
    "approval_diagnostic_capture_does_not_delete_integration_branch", "approval_diagnostic_capture_does_not_delete_worktree",
    "approval_diagnostic_capture_does_not_force_push", "approval_diagnostic_capture_does_not_prune_remotes",
    "approval_diagnostic_capture_does_not_modify_tags", "approval_diagnostic_capture_does_not_modify_staged_evidence",
    "approval_diagnostic_capture_does_not_regenerate_evidence", "approval_diagnostic_capture_does_not_call_providers",
    "approval_diagnostic_capture_does_not_inspect_env", "approval_diagnostic_capture_does_not_acquire_market_data",
    "approval_diagnostic_capture_does_not_regenerate_dataset", "approval_diagnostic_capture_does_not_recompute_metrics",
    "approval_diagnostic_capture_does_not_train_models", "approval_diagnostic_capture_does_not_score_strategy",
    "approval_diagnostic_capture_does_not_generate_recommendations", "approval_diagnostic_capture_does_not_accept_predictive_usefulness",
    "approval_diagnostic_capture_does_not_accept_profitability", "approval_diagnostic_capture_does_not_authorize_runtime",
    "approval_diagnostic_capture_does_not_authorize_broker_execution",
    "selected_diagnostic_package_approved_for_future_execution_only", "future_diagnostic_capture_is_not_retry_success",
    "priority_1_selection_is_not_root_cause", "module_concentration_is_not_failure_error_separation",
    "previous_targeted_diagnostic_candidate_operator_review_remains_source_evidence",
    "previous_targeted_diagnostic_candidate_remains_source_evidence", "previous_planning_results_review_remains_valid",
    "previous_detail_binding_results_review_remains_valid", "previous_materialization_results_review_remains_valid",
    "previous_source_recovery_results_review_remains_valid", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_execution_required_before_diagnostic_capture",
    "separate_results_review_required_after_diagnostic_capture",
    "separate_remediation_or_method_candidate_required_after_diagnostic_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "targeted_diagnostic_output_capture_approval_created", "diagnostic_capture_package_selected",
    "diagnostic_capture_package_approved", "diagnostic_capture_package_authorized",
    "ready_for_targeted_diagnostic_output_capture_execution",
]
FALSE_FIELDS = [
    "diagnostic_capture_execution_performed", "diagnostic_capture_results_review_created", "diagnostic_output_captured",
    "diagnostic_command_executed", "diagnostic_method_executed", "targeted_pytest_performed",
    "full_pytest_performed", "retry_rerun_performed", "cache_read_in_approval", "cache_modified_in_approval",
    "planning_reentry_rerun_performed", "detail_binding_reattempt_rerun_performed",
    "materialization_execution_rerun_performed", "source_recovery_rerun_performed",
    "classification_execution_performed_in_approval", "code_remediation_executed", "evidence_remediation_executed",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended", "retry_success_claimed",
    "main_merge_readiness_claimed", "new_retry_candidate_created", "new_retry_executed",
    "new_retry_results_review_created", "main_merge_approval_created", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_approval", "env_inspection_performed_in_approval",
    "market_data_acquisition_performed_in_approval", "dataset_generation_performed_in_approval",
    "metric_recomputation_from_raw_rows_performed", "model_training_performed", "strategy_scoring_performed",
    "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError(ValueError):
    """Raised when attestation, source evidence, or approval boundaries fail."""


def _is_utc_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_attestation_v1(
    *, operator_reference: str, operator_attestation_timestamp_utc: str, operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str, operator_confirms_source_candidate_digest: str,
    operator_confirms_source_results_review_digest: str, operator_confirms_source_prioritized_planning_review_digest: str,
    operator_confirms_source_results_review_manifest_digest: str, operator_confirms_source_planning_execution_digest: str,
    operator_confirms_source_prioritized_planning_digest: str, operator_confirms_source_planning_digest_manifest_digest: str,
    operator_confirms_source_detail_binding_results_review_digest: str, operator_confirms_source_complete_29_row_binding_digest: str,
    operator_confirms_source_materialized_payload_digest: str, operator_confirms_source_detail_binding_approval_digest: str,
    operator_confirms_source_prior_blocked_detail_binding_execution_digest: str,
    operator_confirms_source_prior_blocked_detail_binding_reason: str, operator_confirms_source_recovery_results_review_digest: str,
    operator_confirms_source_recovery_detail_digest: str, operator_confirms_source_after_v2_approval_digest: str,
    operator_confirms_source_module_grouping_digest: str, operator_confirms_retry_execution_commit: str,
    operator_confirms_retry_failure_counts: bool, operator_confirms_priority_1_top_module_paths: bool,
    operator_confirms_priority_1_top_module_counts: bool, operator_confirms_priority_1_total_612: bool,
    operator_confirms_top_10_total_1069: bool, operator_confirms_module_summary_count_29: bool,
    operator_confirms_failed_or_errored_nodeids_1404: bool, operator_confirms_selected_diagnostic_capture_package: str,
    operator_confirms_approval_scope_only: bool, operator_confirms_no_diagnostic_execution: bool,
    operator_confirms_no_diagnostic_command: bool, operator_confirms_no_diagnostic_output: bool,
    operator_confirms_no_targeted_pytest: bool, operator_confirms_no_full_pytest: bool,
    operator_confirms_no_retry: bool, operator_confirms_no_cache_read: bool,
    operator_confirms_no_cache_modification: bool, operator_confirms_no_planning_rerun: bool,
    operator_confirms_no_detail_binding_rerun: bool, operator_confirms_no_materialization_rerun: bool,
    operator_confirms_no_source_recovery_rerun: bool, operator_confirms_no_remediation_execution: bool,
    operator_confirms_no_classification_execution: bool, operator_confirms_no_failure_error_separation: bool,
    operator_confirms_no_first_failure: bool, operator_confirms_no_first_error: bool,
    operator_confirms_no_traceback_root_cause: bool, operator_confirms_no_direct_remediation: bool,
    operator_confirms_no_retry_success: bool, operator_confirms_no_main_merge_readiness: bool,
    operator_confirms_no_new_retry_candidate: bool, operator_confirms_no_retry_results_review: bool,
    operator_confirms_no_integration_results_review: bool, operator_confirms_no_main_merge_approval: bool,
    operator_confirms_no_integration_success: bool, operator_confirms_no_successful_integration_digest: bool,
    operator_confirms_no_integration_branch_push: bool, operator_confirms_no_main_push: bool,
    operator_confirms_origin_main_not_modified: bool, operator_confirms_no_branch_delete: bool,
    operator_confirms_no_force_push: bool, operator_confirms_no_tag_mutation: bool,
    operator_confirms_no_evidence_regeneration: bool, operator_confirms_no_marketflow_commit: bool,
    operator_confirms_no_pytest_cache_commit: bool, operator_confirms_no_provider_requests: bool,
    operator_confirms_no_env_inspection: bool, operator_confirms_no_market_data_acquisition: bool,
    operator_confirms_no_dataset_generation: bool, operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool, operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_trade_recommendations: bool, operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool, operator_confirms_runtime_not_authorized: bool,
    operator_confirms_broker_not_authorized: bool, operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_secret_capture_or_commit: bool,
    selected_targeted_diagnostic_capture_package: str = SELECTED_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build and validate the exact non-secret operator attestation."""

    values = locals()
    attestation = {
        "operator_decision": operator_decision,
        "selected_targeted_diagnostic_capture_package": selected_targeted_diagnostic_capture_package,
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
    if not isinstance(attestation, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("operator attestation must be an object")
    constants = {
        "operator_decision": OPERATOR_DECISION,
        "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "operator_attestation_phrase": REQUIRED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ATTESTATION_PHRASE_V1,
        "operator_attestation_version": ATTESTATION_VERSION,
        **STRING_CONFIRMATIONS,
    }
    for field, expected in constants.items():
        if attestation.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError(f"{field} mismatch")
    if not isinstance(attestation.get("operator_reference"), str) or not attestation["operator_reference"].strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("operator reference required")
    if not _is_utc_timestamp(attestation.get("operator_attestation_timestamp_utc")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("UTC attestation timestamp required")
    for field in BOOLEAN_CONFIRMATION_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError(f"{field} must be true")
    digest = attestation.get("operator_attestation_digest")
    if digest is not None:
        payload = dict(attestation)
        payload.pop("operator_attestation_digest", None)
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != semantic_digest(payload):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("operator attestation digest mismatch")


def _expected_source_review() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND, "review_status": source.REVIEW_STATUS,
        "review_scope": source.REVIEW_SCOPE, source.DIGEST_KEY: SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_targeted_diagnostic_output_capture_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
        "recommended_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "targeted_diagnostic_output_capture_candidate_operator_review_created": True,
        "targeted_diagnostic_output_capture_candidate_operator_review_ready": True,
        "source_candidate_reviewed": True, "diagnostic_capture_packages_reviewed": True,
        "future_diagnostic_capture_requirements_reviewed": True, "future_diagnostic_capture_plan_reviewed": True,
        "diagnostic_capture_package_selected": False, "diagnostic_capture_package_approved": False,
        "diagnostic_capture_execution_performed": False, "ready_for_targeted_diagnostic_output_capture_approval": False,
        "ready_for_retry_candidate": False,
    }


def _bind_source_review(value: dict | None) -> dict[str, Any]:
    expected = _expected_source_review()
    if value is None:
        return deepcopy(expected)
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("source operator review must be an object")
    for field, required in expected.items():
        if value.get(field) != required:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError(f"source operator review {field} mismatch")
    return deepcopy(dict(value))


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


SOURCE_CHECKS = {
    "source_targeted_diagnostic_output_capture_candidate_operator_review_digest": "source_operator_review_digest_bound",
    "source_targeted_diagnostic_output_capture_candidate_digest": "source_candidate_digest_bound",
    "source_results_review_digest": "source_results_review_digest_bound",
    "source_prioritized_planning_review_digest": "source_prioritized_planning_review_digest_bound",
    "source_results_review_manifest_digest": "source_results_review_manifest_digest_bound",
    "source_planning_execution_digest": "source_planning_execution_digest_bound",
    "source_prioritized_planning_digest": "source_prioritized_planning_digest_bound",
    "source_planning_digest_manifest_digest": "source_planning_digest_manifest_digest_bound",
    "source_detail_binding_results_review_digest": "source_detail_binding_results_review_digest_bound",
    "source_complete_29_row_binding_review_digest": "source_complete_29_row_binding_review_digest_bound",
    "source_detail_binding_results_review_manifest_digest": "source_detail_binding_results_review_manifest_digest_bound",
    "source_detail_binding_reattempt_digest": "source_detail_binding_reattempt_digest_bound",
    "source_complete_29_row_binding_digest": "source_complete_29_row_binding_digest_bound",
    "source_materialization_results_review_digest": "source_materialization_results_review_digest_bound",
    "source_materialized_payload_digest": "source_materialized_payload_digest_bound",
    "source_detail_binding_approval_digest": "source_detail_binding_approval_digest_bound",
    "source_prior_blocked_detail_binding_execution_digest": "source_prior_blocked_detail_binding_execution_digest_bound",
    "source_prior_blocked_detail_binding_reason": "source_prior_blocked_detail_binding_reason_bound",
    "source_recovery_results_review_digest": "source_recovery_results_review_digest_bound",
    "source_recovery_detail_digest": "source_recovery_detail_digest_bound",
    "source_after_v2_approval_digest": "source_after_v2_approval_digest_bound",
    "source_module_grouping_digest": "source_module_grouping_digest_bound",
}


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [_check(check_id, SOURCE_BINDINGS[field], approval.get(field)) for field, check_id in SOURCE_CHECKS.items()]
    attestation = approval.get("operator_attestation", {})
    checks.extend([
        _check("source_selected_after_v2_planning_package_bound", source.source.SELECTED_AFTER_V2_PLANNING_PACKAGE, approval.get("selected_after_v2_planning_package")),
        _check("retry_execution_commit_bound", source.source.RETRY_EXECUTION_COMMIT, approval.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, approval.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", [x["module_path"] for x in source.source.TOP_MODULES], [x.get("module_path") for x in approval.get("priority_1_top_module_groups", [])]),
        _check("priority_1_top_module_counts_bound", [136, 131, 122, 112, 111], [x.get("failed_or_errored_nodeid_count") for x in approval.get("priority_1_top_module_groups", [])]),
        _check("priority_1_total_612_bound", 612, approval.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, approval.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, approval.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, approval.get("failed_or_errored_nodeids_count")),
        _check("operator_decision_matches", OPERATOR_DECISION, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ATTESTATION_PHRASE_V1, attestation.get("operator_attestation_phrase")),
        _check("approval_created_true", True, approval.get("targeted_diagnostic_output_capture_approval_created")),
        _check("approval_scope_only", APPROVAL_SCOPE, approval.get("approval_scope")),
        _check("selected_diagnostic_capture_package_bound", SELECTED_PACKAGE, approval.get("selected_targeted_diagnostic_capture_package")),
        _check("diagnostic_capture_package_selected_true", True, approval.get("diagnostic_capture_package_selected")),
        _check("diagnostic_capture_package_approved_true", True, approval.get("diagnostic_capture_package_approved")),
        _check("diagnostic_capture_package_authorized_true", True, approval.get("diagnostic_capture_package_authorized")),
        _check("ready_for_targeted_diagnostic_output_capture_execution_true", True, approval.get("ready_for_targeted_diagnostic_output_capture_execution")),
        _check("future_command_template_approved_not_executed", "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED", approval.get("future_diagnostic_command_template", {}).get("future_diagnostic_command_template_status")),
        _check("future_requirements_approved_for_future_execution", APPROVED_REQUIREMENTS, approval.get("approved_future_diagnostic_capture_requirements")),
        _check("future_plan_approved_not_executed", APPROVED_PLAN, approval.get("approved_future_diagnostic_capture_plan")),
        _check("planned_outputs_authorized_not_generated", PLANNED_OUTPUTS, approval.get("planned_outputs")),
        _check("supporting_packages_not_selected", SUPPORTING_PACKAGES, approval.get("supporting_packages")),
        _check("blocked_packages_not_approved", BLOCKED_PACKAGES, approval.get("blocked_packages")),
    ])
    false_aliases = {
        "diagnostic_capture_execution_performed": "diagnostic_capture_execution_false",
        "diagnostic_capture_results_review_created": "diagnostic_results_review_false",
        "targeted_pytest_performed": "targeted_pytest_false", "full_pytest_performed": "full_pytest_false",
        "retry_rerun_performed": "retry_rerun_false", "planning_reentry_rerun_performed": "planning_reentry_rerun_false",
        "detail_binding_reattempt_rerun_performed": "detail_binding_reattempt_rerun_false",
        "materialization_execution_rerun_performed": "materialization_execution_rerun_false",
        "source_recovery_rerun_performed": "source_recovery_rerun_false",
        "code_remediation_executed": "remediation_execution_false",
        "classification_execution_performed_in_approval": "classification_execution_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "main_push_performed": "main_push_false", "origin_main_modified_by_this_task": "origin_main_modified_false",
        "provider_requests_made_in_approval": "provider_requests_false", "env_inspection_performed_in_approval": "env_inspection_false",
        "market_data_acquisition_performed_in_approval": "market_data_acquisition_false",
        "dataset_generation_performed_in_approval": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    for field in FALSE_FIELDS:
        checks.append(_check(false_aliases.get(field, f"{field}_false"), False, approval.get(field)))
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
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": failed, "blocker_count": failed,
        **{field: approval.get(field) for field in TRUE_FIELDS},
        "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        **{field: approval.get(field) for field in (
            "diagnostic_capture_execution_performed", "diagnostic_capture_results_review_created",
            "diagnostic_output_captured", "diagnostic_command_executed", "targeted_pytest_performed",
            "retry_rerun_performed", "full_pytest_performed", "new_retry_candidate_created",
            "new_retry_executed", "integration_execution_successful",
        )},
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _approval_digest(approval: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(approval))
    for field in ("checklist", "summary", DIGEST_KEY, "approval_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(
    *, source_operator_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Create approval for future execution only after exact attestation."""

    source_review = _bind_source_review(source_operator_review)
    _validate_attestation(operator_attestation)
    approval: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True,
        "source_targeted_diagnostic_output_capture_candidate_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_targeted_diagnostic_output_capture_candidate_operator_review_status": source.REVIEW_STATUS,
        "source_targeted_diagnostic_output_capture_candidate_operator_review_scope": source.REVIEW_SCOPE,
        **deepcopy(SOURCE_BINDINGS),
        "operator_attestation": deepcopy(operator_attestation),
        "source_operator_review_summary": {
            "artifact_kind": source_review["artifact_kind"], "status": source_review["review_status"],
            "scope": source_review["review_scope"], "digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        },
        "selected_after_v2_planning_package": source.source.SELECTED_AFTER_V2_PLANNING_PACKAGE,
        "retry_execution_commit": source.source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {
            "branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
            "working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
            "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
            "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True,
            "root_full_regression_is_retry_evidence": False,
        },
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_1_total_nodeids": 612, "priority_1_top_module_groups": deepcopy(source.source.TOP_MODULES),
        "approved_package": deepcopy(APPROVED_PACKAGE),
        "approved_future_diagnostic_capture_requirements": deepcopy(APPROVED_REQUIREMENTS),
        "approved_future_diagnostic_capture_plan": deepcopy(APPROVED_PLAN),
        "future_diagnostic_command_template": deepcopy(FUTURE_COMMAND_TEMPLATE),
        "planned_outputs": deepcopy(PLANNED_OUTPUTS), "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "blocked_packages": deepcopy(BLOCKED_PACKAGES), "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
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
        "planned_outputs": semantic_digest(PLANNED_OUTPUTS), "supporting_packages": semantic_digest(SUPPORTING_PACKAGES),
        "blocked_packages": semantic_digest(BLOCKED_PACKAGES),
    }
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval, approval["checklist"])
    approval[DIGEST_KEY] = _approval_digest(approval)
    approval["approval_digest"] = approval[DIGEST_KEY]
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(
    approval: dict,
) -> dict:
    """Reject incomplete attestation, source drift, or authority expansion."""

    if not isinstance(approval, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("approval must be an object")
    constants = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "selected_targeted_diagnostic_capture_package": SELECTED_PACKAGE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True,
        "source_targeted_diagnostic_output_capture_candidate_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_targeted_diagnostic_output_capture_candidate_operator_review_status": source.REVIEW_STATUS,
        "source_targeted_diagnostic_output_capture_candidate_operator_review_scope": source.REVIEW_SCOPE,
        "selected_after_v2_planning_package": source.source.SELECTED_AFTER_V2_PLANNING_PACKAGE,
        "retry_execution_commit": source.source.RETRY_EXECUTION_COMMIT, **SOURCE_BINDINGS,
    }
    for field, expected in constants.items():
        if approval.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError(f"{field} mismatch")
    _validate_attestation(approval.get("operator_attestation"))
    if approval.get("retry_failure_context", {}).get("counts") != {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("retry failure counts mismatch")
    scalars = {
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111], "top_5_count_sum": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114", "priority_1_total_nodeids": 612,
        "priority_1_top_module_groups": source.source.TOP_MODULES,
    }
    for field, expected in scalars.items():
        if approval.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError(f"{field} mismatch")
    structures = {
        "approved_package": APPROVED_PACKAGE,
        "approved_future_diagnostic_capture_requirements": APPROVED_REQUIREMENTS,
        "approved_future_diagnostic_capture_plan": APPROVED_PLAN,
        "future_diagnostic_command_template": FUTURE_COMMAND_TEMPLATE,
        "planned_outputs": PLANNED_OUTPUTS, "supporting_packages": SUPPORTING_PACKAGES,
        "blocked_packages": BLOCKED_PACKAGES, "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in structures.items():
        if approval.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError(f"{field} mismatch")
    if any(approval.get(field) is not True for field in TRUE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("approval authority missing")
    if any(approval.get(field) is not False for field in FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("closed boundary opened")
    if approval.get("predictive_usefulness") != NOT_ACCEPTED or approval.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("acceptance boundary changed")
    if any(
        approval.get(field) != NOT_AUTHORIZED
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")
    ):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("runtime boundary changed")
    expected_manifest = {
        "source_operator_review": SOURCE_OPERATOR_REVIEW_DIGEST, "source_candidate": source.SOURCE_CANDIDATE_DIGEST,
        "operator_attestation": approval["operator_attestation"]["operator_attestation_digest"],
        "approved_package": semantic_digest(APPROVED_PACKAGE), "approved_requirements": semantic_digest(APPROVED_REQUIREMENTS),
        "approved_plan": semantic_digest(APPROVED_PLAN), "future_command_template": semantic_digest(FUTURE_COMMAND_TEMPLATE),
        "planned_outputs": semantic_digest(PLANNED_OUTPUTS), "supporting_packages": semantic_digest(SUPPORTING_PACKAGES),
        "blocked_packages": semantic_digest(BLOCKED_PACKAGES),
    }
    if approval.get("digest_manifest") != expected_manifest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("digest manifest mismatch")
    checklist = _checklist(approval)
    if approval.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("checklist mismatch")
    summary = _summary(approval, checklist)
    if approval.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("summary mismatch")
    digest = approval.get(DIGEST_KEY)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _approval_digest(approval):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("approval digest mismatch")
    if approval.get("approval_digest") != digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("approval digest alias mismatch")
    return {"artifact_kind": approval["artifact_kind"], "approval_status": approval["approval_status"], "approval_scope": approval["approval_scope"], "approval_digest": digest, **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(
    output_dir: str | Path, *, source_operator_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Write deterministic JSON outside protected runtime directories."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("protected output directory")
    approval = build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(source_operator_review=source_operator_review, operator_attestation=operator_attestation)
    path = output / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError("output exists")
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": approval["artifact_kind"], "approval_status": approval["approval_status"], "approval_digest": approval[DIGEST_KEY], "payload_sha256": sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render the validated approval as Markdown."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(approval)
    sections = [
        ("Operator Attestation", [approval["operator_attestation"]["operator_reference"], approval["operator_attestation"]["operator_attestation_timestamp_utc"], REQUIRED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ATTESTATION_PHRASE_V1]),
        ("Source Targeted Diagnostic Output Capture Candidate Operator Review", [SOURCE_OPERATOR_REVIEW_DIGEST, source.REVIEW_STATUS]),
        ("Source Targeted Diagnostic Output Capture Candidate", [source.SOURCE_CANDIDATE_DIGEST]),
        ("Source Remediation or Method Results Review", [SOURCE_BINDINGS["source_results_review_digest"], SOURCE_BINDINGS["source_prioritized_planning_review_digest"]]),
        ("Source Planning Reentry with Complete Detail", [SOURCE_BINDINGS["source_planning_execution_digest"], SOURCE_BINDINGS["source_prioritized_planning_digest"]]),
        ("Source Detail Binding Results Review", [SOURCE_BINDINGS["source_detail_binding_results_review_digest"], SOURCE_BINDINGS["source_complete_29_row_binding_digest"]]),
        ("Source Materialization Results Review", [SOURCE_BINDINGS["source_materialization_results_review_digest"], SOURCE_BINDINGS["source_materialized_payload_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the failed retry remains authoritative."]),
        ("Approval Scope", [APPROVAL_SCOPE]),
        ("Selected Diagnostic Capture Package", [SELECTED_PACKAGE, APPROVED_PACKAGE["approval_status"]]),
        ("Priority 1 Top Module Groups", [f"{x['rank']}. {x['module_path']}: {x['failed_or_errored_nodeid_count']}" for x in source.source.TOP_MODULES]),
        ("Future Diagnostic Command Template", [FUTURE_COMMAND_TEMPLATE["future_diagnostic_command_template_status"], FUTURE_COMMAND_TEMPLATE["future_diagnostic_command_template"]]),
        ("Approved Future Diagnostic Capture Requirements", [x["requirement_id"] for x in APPROVED_REQUIREMENTS]),
        ("Approved Future Diagnostic Capture Plan", [f"{x['step_id']}. {x['step']}" for x in APPROVED_PLAN]),
        ("Planned Outputs", [x["output_id"] for x in PLANNED_OUTPUTS]),
        ("Supporting Packages", [x["package_id"] for x in SUPPORTING_PACKAGES]),
        ("Blocked Packages", [x["package_id"] for x in BLOCKED_PACKAGES]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Only future targeted diagnostic-output capture execution is authorized. No execution, retry, main, runtime, or trading authority is created."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["No diagnostic command, pytest run, cache access, retry, remediation, provider, data, runtime, or trading action occurs in approval."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Approval v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND", "APPROVAL_STATUS", "APPROVAL_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVED",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ONLY_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS",
    "REQUIRED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ATTESTATION_PHRASE_V1",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1",
    "write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_markdown_v1",
]
