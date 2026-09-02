"""Approve the reviewed module-detail exposure/binding package for future execution."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVED_V1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVED"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_ONLY_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1"
SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE = "PACKAGE_EXPOSE_OR_BIND_COMPLETE_RECOVERED_MODULE_GROUPING_DETAIL_FOR_REENTRY"
SOURCE_OPERATOR_REVIEW_DIGEST = "8ea86457a92bccbcb9712b208140300964fbcf3c361f21819aa008cd7ebec17b"
OPERATOR_DECISION = "APPROVE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING"
OPERATOR_ATTESTATION_VERSION = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_attestation_v1"
REQUIRED_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_ATTESTATION_PHRASE_V1 = (
    "APPROVE REENTRY MODULE GROUPING DETAIL EXPOSURE OR BINDING "
    "PACKAGE_EXPOSE_OR_BIND_COMPLETE_RECOVERED_MODULE_GROUPING_DETAIL_FOR_REENTRY "
    "MARKETFLOW EXPOSE OR BIND COMPLETE RECOVERED 29 ROW MODULE GROUPING DETAIL FOR FUTURE REENTRY ONLY "
    "NO DETAIL EXPOSURE NOW NO CACHE READ NO SOURCE RECOVERY NO PLANNING REENTRY NO RETRY NO FULL PYTEST NO MAIN PUSH "
    "DETAIL_EXPOSURE_BINDING_APPROVAL_ONLY_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_RETRY_NOT_MAIN"
)
APPROVED_ONLY = "APPROVED_FOR_FUTURE_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_ONLY"
AUTHORIZED_NOT_GENERATED = "AUTHORIZED_NOT_GENERATED"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_V1"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVED_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVED = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_ONLY_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_retry_failure_counts", "operator_confirms_recovered_module_summary",
    "operator_confirms_top_five_paths", "operator_confirms_top_five_count_sum_612",
    "operator_confirms_top_ten_count_sum_1069", "operator_confirms_available_committed_reentry_detail",
    "operator_confirms_missing_committed_reentry_detail", "operator_confirms_live_reentry_source_lacks_complete_29_rows",
    "operator_confirms_success_path_with_injected_snapshot", "operator_confirms_approval_scope_only",
    "operator_confirms_no_detail_exposure_execution", "operator_confirms_no_complete_29_row_detail_exposed",
    "operator_confirms_no_complete_29_row_detail_bound", "operator_confirms_no_module_paths_recovered",
    "operator_confirms_no_per_module_counts_recovered", "operator_confirms_no_bounded_nodeid_samples_recovered",
    "operator_confirms_no_cache_read", "operator_confirms_no_cache_modification",
    "operator_confirms_no_source_recovery", "operator_confirms_no_source_recovery_rerun",
    "operator_confirms_no_planning_reentry_execution", "operator_confirms_no_diagnostic_command",
    "operator_confirms_no_diagnostic_execution", "operator_confirms_no_remediation_execution",
    "operator_confirms_no_classification_execution", "operator_confirms_no_retry",
    "operator_confirms_no_full_pytest", "operator_confirms_no_targeted_diagnostic_candidate",
    "operator_confirms_no_new_retry_candidate", "operator_confirms_no_retry_results_review",
    "operator_confirms_no_integration_results_review", "operator_confirms_no_integration_success",
    "operator_confirms_no_successful_integration_digest", "operator_confirms_no_integration_branch_push",
    "operator_confirms_no_main_push", "operator_confirms_origin_main_not_modified",
    "operator_confirms_no_branch_delete", "operator_confirms_no_force_push",
    "operator_confirms_no_tag_mutation", "operator_confirms_no_evidence_regeneration",
    "operator_confirms_no_marketflow_commit", "operator_confirms_no_pytest_cache_commit",
    "operator_confirms_no_provider_requests", "operator_confirms_no_market_data_acquisition",
    "operator_confirms_no_dataset_generation", "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training", "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_trade_recommendations", "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance", "operator_confirms_runtime_not_authorized",
    "operator_confirms_broker_not_authorized", "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

APPROVED_REQUIREMENT_IDS = [
    "source_diagnosis_must_be_ready", "source_diagnosis_digest_must_be_bound",
    "source_blocked_reentry_execution_digest_must_be_bound", "source_blocked_reentry_manifest_digest_must_be_bound",
    "source_blocked_reentry_reason_must_be_bound", "source_recovery_results_review_must_be_ready",
    "source_recovery_detail_digest_must_be_bound", "source_recovery_manifest_digest_must_be_bound",
    "complete_29_row_detail_source_must_be_identified", "complete_29_row_detail_must_not_be_inferred",
    "module_paths_must_be_source_derived", "per_module_counts_must_be_source_derived",
    "bounded_nodeid_samples_must_be_source_derived", "top_five_and_top_ten_concentration_must_be_preserved",
    "unsupported_claims_boundary_must_be_preserved", "detail_exposure_must_not_rerun_retry",
    "detail_exposure_must_not_run_full_pytest", "detail_exposure_must_not_execute_diagnostics",
    "detail_exposure_must_not_execute_remediation", "detail_exposure_must_not_claim_root_cause",
    "detail_exposure_must_not_recommend_direct_code_remediation", "detail_exposure_must_not_treat_detail_as_retry_success",
    "detail_exposure_must_not_commit_pytest_cache", "detail_exposure_must_not_commit_marketflow_outputs",
    "detail_exposure_must_preserve_origin_main", "detail_exposure_must_preserve_integration_branch",
    "detail_exposure_must_preserve_staged_evidence", "future_detail_exposure_results_review_required",
    "future_after_v2_planning_reentry_requires_detail_exposure_results_review", "future_retry_requires_separate_approval",
    "main_merge_requires_passing_retry_results_review",
]
APPROVED_FUTURE_REQUIREMENTS = [
    {"requirement_id": item, "requirement_value": True, "approval_status": APPROVED_ONLY}
    for item in APPROVED_REQUIREMENT_IDS
]

FUTURE_PLAN_STEPS = [
    "Bind diagnosis digest, blocked reentry execution digest, and blocked reason.",
    "Bind source recovery results-review digest and recovered detail digest.",
    "Use the selected controlled exposure or binding source.",
    "Verify the selected source contains all 29 module rows.",
    "Verify module paths, per-module counts, bounded samples, top-five concentration, and top-ten concentration.",
    "Produce or expose a bounded complete 29-row module grouping source suitable for planning reentry.",
    "Preserve unsupported claims: no failure/error separation, first-order claim, traceback root cause, direct remediation, retry success, or main merge readiness.",
    "Require detail exposure/binding results review.",
    "Re-enter after-v2 planning execution only after results review.",
    "Keep diagnostic capture, retry, main merge, runtime, and trading closed.",
]
APPROVED_FUTURE_PLAN = [
    {"step_id": f"future_detail_exposure_or_binding_step_{index:02d}", "step": step,
     "approval_status": APPROVED_ONLY, "execution_status": NOT_EXECUTED}
    for index, step in enumerate(FUTURE_PLAN_STEPS, 1)
]

PLANNED_OUTPUT_IDS = [
    "detail_exposure_or_binding_approval_manifest", "complete_29_row_source_identification_report",
    "complete_module_grouping_detail_binding_plan", "recovered_module_paths_binding_plan",
    "per_module_counts_binding_plan", "bounded_nodeid_samples_binding_plan",
    "top_module_concentration_preservation_plan", "unsupported_claims_boundary_report",
    "detail_exposure_limitations_report", "planning_reentry_enablement_report",
    "recommended_next_package_report", "digest_manifest",
]
AUTHORIZED_PLANNED_OUTPUTS = [
    {"output_id": item, "authorization_status": AUTHORIZED_NOT_GENERATED}
    for item in PLANNED_OUTPUT_IDS
]

SUPPORTING_PACKAGE_STATUSES = {
    "PACKAGE_EXPOSE_COMPLETE_29_ROW_DETAIL_FROM_SOURCE_RECOVERY_EXECUTION_ARTIFACT": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_BIND_COMPLETE_29_ROW_DETAIL_AS_COMMITTED_STATUS_SOURCE": "AVAILABLE_NOT_SELECTED_HIGH_CONTROL",
    "PACKAGE_USE_OPERATOR_PROVIDED_RECOVERY_DETAIL_REPORT_PATH": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_RECONSTRUCT_29_ROW_DETAIL_FROM_REVIEWED_CACHE_READ_ONLY": "AVAILABLE_NOT_SELECTED_REQUIRES_SEPARATE_APPROVAL",
    "PACKAGE_REDUCED_SCOPE_TOP_FIVE_ONLY_PLANNING_REENTRY": "AVAILABLE_NOT_SELECTED_NOT_RECOMMENDED",
}
SUPPORTING_PACKAGES = [
    {"package_id": package, "approval_status": status, "selected": False, "approved": False}
    for package, status in SUPPORTING_PACKAGE_STATUSES.items()
]
BLOCKED_PACKAGE_STATUSES = {
    "PACKAGE_INFER_MISSING_24_MODULES": "BLOCKED_NOT_APPROVED",
    "PACKAGE_RERUN_PYTEST_TO_RECREATE_DETAIL": "BLOCKED_NOT_APPROVED",
    "PACKAGE_DIRECT_DIAGNOSTIC_CAPTURE_WITHOUT_REENTRY_REVIEW": "BLOCKED_NOT_APPROVED",
    "PACKAGE_NEW_RETRY_DESPITE_BLOCKED_REENTRY": "BLOCKED_NOT_APPROVED",
    "PACKAGE_MAIN_MERGE_DESPITE_BLOCKED_REENTRY_AND_FAILED_RETRY": "BLOCKED_NOT_APPROVED",
}
BLOCKED_PACKAGES = [
    {"package_id": package, "approval_status": status, "selected": False, "approved": False}
    for package, status in BLOCKED_PACKAGE_STATUSES.items()
]

NEXT_CHAIN = [
    "Detail Exposure or Binding Execution v1, if approved.",
    "Detail Exposure or Binding Results Review v1.",
    "Re-enter after-v2 planning execution using complete recovered detail.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "reentry_module_grouping_detail_exposure_or_binding_execution_if_approved",
    "reentry_module_grouping_detail_exposure_or_binding_results_review",
    "after_v2_planning_reentry_execution_with_complete_detail",
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
    "targeted_diagnostic_output_capture_candidate_if_supported",
    "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "approval_detail_binding_does_not_execute_detail_exposure", "approval_detail_binding_does_not_expose_29_module_rows",
    "approval_detail_binding_does_not_bind_complete_detail", "approval_detail_binding_does_not_recover_module_grouping_again",
    "approval_detail_binding_does_not_read_cache", "approval_detail_binding_does_not_modify_cache",
    "approval_detail_binding_does_not_parse_operator_logs", "approval_detail_binding_does_not_run_diagnostic_commands",
    "approval_detail_binding_does_not_execute_diagnostics", "approval_detail_binding_does_not_execute_remediation",
    "approval_detail_binding_does_not_execute_classification", "approval_detail_binding_does_not_classify_modules_again",
    "approval_detail_binding_does_not_execute_after_v2_planning_reentry", "approval_detail_binding_does_not_rerun_retry",
    "approval_detail_binding_does_not_run_full_pytest", "approval_detail_binding_does_not_create_new_retry_candidate",
    "approval_detail_binding_does_not_create_retry_results_review", "approval_detail_binding_does_not_create_integration_results_review",
    "approval_detail_binding_does_not_mark_integration_successful", "approval_detail_binding_does_not_generate_successful_integration_digest",
    "approval_detail_binding_does_not_claim_failure_error_separation", "approval_detail_binding_does_not_claim_first_failure",
    "approval_detail_binding_does_not_claim_first_error", "approval_detail_binding_does_not_claim_traceback_root_cause",
    "approval_detail_binding_does_not_recommend_direct_code_remediation", "approval_detail_binding_does_not_treat_recovered_detail_as_retry_success",
    "approval_detail_binding_does_not_push_integration_branch", "approval_detail_binding_does_not_push_main",
    "approval_detail_binding_does_not_delete_integration_branch", "approval_detail_binding_does_not_delete_worktree",
    "approval_detail_binding_does_not_force_push", "approval_detail_binding_does_not_prune_remotes",
    "approval_detail_binding_does_not_modify_tags", "approval_detail_binding_does_not_modify_staged_evidence",
    "approval_detail_binding_does_not_regenerate_evidence", "approval_detail_binding_does_not_call_providers",
    "approval_detail_binding_does_not_acquire_market_data", "approval_detail_binding_does_not_regenerate_dataset",
    "approval_detail_binding_does_not_recompute_metrics", "approval_detail_binding_does_not_train_models",
    "approval_detail_binding_does_not_score_strategy", "approval_detail_binding_does_not_generate_recommendations",
    "approval_detail_binding_does_not_accept_predictive_usefulness", "approval_detail_binding_does_not_accept_profitability",
    "approval_detail_binding_does_not_authorize_runtime", "approval_detail_binding_does_not_authorize_broker_execution",
    "selected_detail_exposure_package_approved_for_future_execution_only",
    "detail_exposure_output_would_be_planning_source_not_root_cause", "source_detail_gap_is_not_retry_success",
    "source_detail_gap_is_not_root_cause_of_original_pytest_failures", "previous_blocked_execution_remains_historically_blocked",
    "previous_source_recovery_results_review_remains_valid", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_execution_required_before_detail_exposure",
    "separate_results_review_required_after_detail_exposure", "separate_retry_approval_required_before_new_retry",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]

FALSE_BOUNDARIES = [
    "detail_exposure_or_binding_executed", "complete_29_row_detail_exposed", "complete_29_row_detail_bound",
    "module_grouping_detail_exposed_by_approval", "module_paths_recovered_by_approval",
    "per_module_counts_recovered_by_approval", "bounded_nodeid_samples_recovered_by_approval",
    "after_v2_planning_execution_reentry_created", "after_v2_planning_execution_reentry_performed",
    "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created", "new_retry_executed",
    "new_retry_results_review_created", "main_merge_approval_created", "source_recovery_rerun_performed",
    "cache_read_in_approval", "module_grouping_recovered_in_approval", "retry_rerun_performed",
    "full_pytest_performed", "diagnostic_command_executed", "diagnostic_output_captured",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
    "evidence_regenerated", "provider_requests_made_in_approval", "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]

UNSUPPORTED_CLAIMS_FIELDS = [
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "retry_success_claimed", "main_merge_readiness_claimed", "diagnostic_method_executed",
    "code_remediation_executed", "evidence_remediation_executed",
    "classification_execution_performed_in_approval",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError(ValueError):
    """Raised when approval inputs or authority boundaries are invalid."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _committed_source_review() -> dict[str, Any]:
    return source.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1()


def _attestation_string_expectations() -> dict[str, str]:
    review = _committed_source_review()
    return {
        "operator_decision": OPERATOR_DECISION,
        "selected_detail_exposure_or_binding_package": SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
        "operator_attestation_phrase": REQUIRED_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_ATTESTATION_PHRASE_V1,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_digest": review["source_detail_exposure_or_binding_candidate_digest"],
        "operator_confirms_source_diagnosis_digest": review["source_reentry_failure_diagnosis_digest"],
        "operator_confirms_primary_failure_class": review["primary_failure_class"],
        "operator_confirms_source_blocked_reentry_execution_digest": review["source_reentry_execution_blocked_digest"],
        "operator_confirms_source_blocked_reentry_manifest_digest": review["source_reentry_execution_blocked_manifest_digest"],
        "operator_confirms_source_blocked_reentry_reason": review["source_reentry_execution_blocked_reason"],
        "operator_confirms_source_planning_reentry_digest": review["source_after_v2_planning_reentry_digest"],
        "operator_confirms_source_recovery_results_review_digest": review["source_module_grouping_source_recovery_results_review_digest"],
        "operator_confirms_source_recovery_results_review_manifest_digest": review["source_module_grouping_source_recovery_results_review_manifest_digest"],
        "operator_confirms_source_recovery_execution_digest": review["source_module_grouping_source_recovery_execution_digest"],
        "operator_confirms_source_recovery_detail_digest": review["source_module_grouping_source_recovery_detail_digest"],
        "operator_confirms_source_recovery_digest_manifest_digest": review["source_module_grouping_source_recovery_digest_manifest_digest"],
        "operator_confirms_source_blocked_after_v2_execution_digest": review["source_blocked_after_v2_execution_digest"],
        "operator_confirms_source_after_v2_approval_digest": review["source_after_v2_approval_digest"],
        "operator_confirms_source_results_review_v2_digest": review["source_results_review_v2_digest"],
        "operator_confirms_source_execution_v2_digest": review["source_execution_v2_digest"],
        "operator_confirms_source_module_grouping_digest": review["source_module_grouping_digest"],
        "operator_confirms_retry_execution_commit": review["retry_execution_commit"],
        "operator_confirms_selected_detail_exposure_or_binding_package": SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    for field, expected in _attestation_string_expectations().items():
        if attestation.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError(f"{field} mismatch")
    if not _iso_utc(attestation.get("operator_attestation_timestamp_utc")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError("operator attestation timestamp invalid")
    if not isinstance(attestation.get("operator_reference"), str) or not attestation["operator_reference"].strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError("operator reference missing")
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError(f"{field} must be true")


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_attestation_v1(
    *, operator_reference: str, operator_attestation_timestamp_utc: str, operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str, operator_confirms_source_candidate_digest: str,
    operator_confirms_source_diagnosis_digest: str, operator_confirms_primary_failure_class: str,
    operator_confirms_source_blocked_reentry_execution_digest: str, operator_confirms_source_blocked_reentry_manifest_digest: str,
    operator_confirms_source_blocked_reentry_reason: str, operator_confirms_source_planning_reentry_digest: str,
    operator_confirms_source_recovery_results_review_digest: str, operator_confirms_source_recovery_results_review_manifest_digest: str,
    operator_confirms_source_recovery_execution_digest: str, operator_confirms_source_recovery_detail_digest: str,
    operator_confirms_source_recovery_digest_manifest_digest: str, operator_confirms_source_blocked_after_v2_execution_digest: str,
    operator_confirms_source_after_v2_approval_digest: str, operator_confirms_source_results_review_v2_digest: str,
    operator_confirms_source_execution_v2_digest: str, operator_confirms_source_module_grouping_digest: str,
    operator_confirms_retry_execution_commit: str, operator_confirms_retry_failure_counts: bool,
    operator_confirms_recovered_module_summary: bool, operator_confirms_top_five_paths: bool,
    operator_confirms_top_five_count_sum_612: bool, operator_confirms_top_ten_count_sum_1069: bool,
    operator_confirms_available_committed_reentry_detail: bool, operator_confirms_missing_committed_reentry_detail: bool,
    operator_confirms_live_reentry_source_lacks_complete_29_rows: bool, operator_confirms_success_path_with_injected_snapshot: bool,
    operator_confirms_selected_detail_exposure_or_binding_package: str, operator_confirms_approval_scope_only: bool,
    operator_confirms_no_detail_exposure_execution: bool, operator_confirms_no_complete_29_row_detail_exposed: bool,
    operator_confirms_no_complete_29_row_detail_bound: bool, operator_confirms_no_module_paths_recovered: bool,
    operator_confirms_no_per_module_counts_recovered: bool, operator_confirms_no_bounded_nodeid_samples_recovered: bool,
    operator_confirms_no_cache_read: bool, operator_confirms_no_cache_modification: bool,
    operator_confirms_no_source_recovery: bool, operator_confirms_no_source_recovery_rerun: bool,
    operator_confirms_no_planning_reentry_execution: bool, operator_confirms_no_diagnostic_command: bool,
    operator_confirms_no_diagnostic_execution: bool, operator_confirms_no_remediation_execution: bool,
    operator_confirms_no_classification_execution: bool, operator_confirms_no_retry: bool,
    operator_confirms_no_full_pytest: bool, operator_confirms_no_targeted_diagnostic_candidate: bool,
    operator_confirms_no_new_retry_candidate: bool, operator_confirms_no_retry_results_review: bool,
    operator_confirms_no_integration_results_review: bool, operator_confirms_no_integration_success: bool,
    operator_confirms_no_successful_integration_digest: bool, operator_confirms_no_integration_branch_push: bool,
    operator_confirms_no_main_push: bool, operator_confirms_origin_main_not_modified: bool,
    operator_confirms_no_branch_delete: bool, operator_confirms_no_force_push: bool,
    operator_confirms_no_tag_mutation: bool, operator_confirms_no_evidence_regeneration: bool,
    operator_confirms_no_marketflow_commit: bool, operator_confirms_no_pytest_cache_commit: bool,
    operator_confirms_no_provider_requests: bool, operator_confirms_no_market_data_acquisition: bool,
    operator_confirms_no_dataset_generation: bool, operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool, operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_trade_recommendations: bool, operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool, operator_confirms_runtime_not_authorized: bool,
    operator_confirms_broker_not_authorized: bool, operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_detail_exposure_or_binding_package: str = SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    attestation = dict(locals())
    attestation["operator_attestation_version"] = OPERATOR_ATTESTATION_VERSION
    _validate_attestation(attestation)
    return attestation


SOURCE_COPY_FIELDS = [
    "source_reentry_failure_diagnosis_digest", "primary_failure_class", "recommended_next_package_from_diagnosis",
    "source_reentry_execution_blocked_digest", "source_reentry_execution_blocked_manifest_digest",
    "source_reentry_execution_blocked_reason", "source_after_v2_planning_reentry_digest",
    "source_module_grouping_source_recovery_results_review_digest",
    "source_module_grouping_source_recovery_results_review_manifest_digest",
    "source_module_grouping_source_recovery_execution_digest", "source_module_grouping_source_recovery_detail_digest",
    "source_module_grouping_source_recovery_digest_manifest_digest", "source_module_grouping_source_recovery_approval_digest",
    "source_module_grouping_source_recovery_operator_review_digest", "source_module_grouping_source_recovery_candidate_digest",
    "source_blocked_after_v2_execution_digest", "source_blocked_after_v2_manifest_digest",
    "source_after_v2_approval_digest", "source_after_v2_operator_review_digest", "source_after_v2_candidate_digest",
    "source_results_review_v2_digest", "source_execution_v2_digest", "source_module_grouping_digest",
    "source_approval_v2_digest", "source_staged_inventory_digest", "retry_execution_commit", "retry_failure_context",
    "recovered_module_grouping_source_summary", "top_module_summary", "top_5_count_sum", "top_10_count_sum",
    "available_committed_reentry_detail", "missing_committed_reentry_detail",
    "actual_live_reentry_source_lacks_complete_29_rows", "reentry_success_path_tested_with_complete_29_row_snapshot",
]


def _approval_base(attestation: Mapping[str, Any]) -> dict[str, Any]:
    review = _committed_source_review()
    approval: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_detail_exposure_or_binding_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_detail_exposure_or_binding_operator_review_status": source.REVIEW_STATUS,
        "source_detail_exposure_or_binding_operator_review_scope": source.REVIEW_SCOPE,
        "source_detail_exposure_or_binding_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_detail_exposure_or_binding_candidate_digest": review["source_detail_exposure_or_binding_candidate_digest"],
    }
    approval.update({field: deepcopy(review[field]) for field in SOURCE_COPY_FIELDS})
    approval.update({
        "approved_package": {
            "package_id": SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE, "approval_status": APPROVED_ONLY,
            "selected": True, "approved": True, "authorized_for_future_execution": True, "executed": False,
            "purpose": "Future execution may expose, bind, or carry forward the complete recovered 29-row module grouping detail so after-v2 planning reentry can execute without cache reread, pytest rerun, inference, diagnostics, remediation, or retry.",
        },
        "selected_detail_exposure_or_binding_package": SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
        "approved_future_detail_exposure_or_binding_requirements": deepcopy(APPROVED_FUTURE_REQUIREMENTS),
        "approved_future_detail_exposure_or_binding_plan": deepcopy(APPROVED_FUTURE_PLAN),
        "authorized_planned_outputs": deepcopy(AUTHORIZED_PLANNED_OUTPUTS),
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES), "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "detail_exposure_or_binding_selected": True, "detail_exposure_or_binding_approved": True,
        "detail_exposure_or_binding_authorized": True, "detail_exposure_or_binding_approval_created": True,
        "ready_for_detail_exposure_or_binding_execution": True,
        "marketflow_outputs_tracked_in_repository": False, "pytest_cache_tracked_in_repository": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    })
    approval.update({field: False for field in FALSE_BOUNDARIES})
    approval.update({field: False for field in UNSUPPORTED_CLAIMS_FIELDS})
    return approval


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected),
            "actual": deepcopy(actual), "severity": BLOCKER,
            "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    review = _committed_source_review()
    attestation = approval.get("operator_attestation", {})
    values: dict[str, tuple[Any, Any]] = {
        "source_operator_review_digest_bound": (SOURCE_OPERATOR_REVIEW_DIGEST, approval.get("source_detail_exposure_or_binding_operator_review_digest")),
        "source_candidate_digest_bound": (review["source_detail_exposure_or_binding_candidate_digest"], approval.get("source_detail_exposure_or_binding_candidate_digest")),
        "source_diagnosis_digest_bound": (review["source_reentry_failure_diagnosis_digest"], approval.get("source_reentry_failure_diagnosis_digest")),
        "source_primary_failure_class_bound": (review["primary_failure_class"], approval.get("primary_failure_class")),
        "source_reentry_execution_blocked_digest_bound": (review["source_reentry_execution_blocked_digest"], approval.get("source_reentry_execution_blocked_digest")),
        "source_reentry_execution_blocked_manifest_digest_bound": (review["source_reentry_execution_blocked_manifest_digest"], approval.get("source_reentry_execution_blocked_manifest_digest")),
        "source_reentry_execution_blocked_reason_bound": (review["source_reentry_execution_blocked_reason"], approval.get("source_reentry_execution_blocked_reason")),
        "source_after_v2_planning_reentry_digest_bound": (review["source_after_v2_planning_reentry_digest"], approval.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (review["source_module_grouping_source_recovery_results_review_digest"], approval.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (review["source_module_grouping_source_recovery_results_review_manifest_digest"], approval.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (review["source_module_grouping_source_recovery_execution_digest"], approval.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (review["source_module_grouping_source_recovery_detail_digest"], approval.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (review["source_module_grouping_source_recovery_digest_manifest_digest"], approval.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_blocked_after_v2_execution_digest_bound": (review["source_blocked_after_v2_execution_digest"], approval.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (review["source_blocked_after_v2_manifest_digest"], approval.get("source_blocked_after_v2_manifest_digest")),
        "source_after_v2_approval_digest_bound": (review["source_after_v2_approval_digest"], approval.get("source_after_v2_approval_digest")),
        "source_results_review_v2_digest_bound": (review["source_results_review_v2_digest"], approval.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (review["source_execution_v2_digest"], approval.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (review["source_module_grouping_digest"], approval.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": (review["retry_execution_commit"], approval.get("retry_execution_commit")),
        "retry_failure_counts_bound": (review["retry_failure_context"]["counts"], approval.get("retry_failure_context", {}).get("counts")),
        "recovered_module_summary_bound": (review["recovered_module_grouping_source_summary"], approval.get("recovered_module_grouping_source_summary")),
        "top_five_paths_bound": (review["top_module_summary"], approval.get("top_module_summary")),
        "top_five_count_sum_612_bound": (612, approval.get("top_5_count_sum")),
        "top_ten_count_sum_1069_bound": (1069, approval.get("top_10_count_sum")),
        "available_committed_reentry_detail_recorded": (review["available_committed_reentry_detail"], approval.get("available_committed_reentry_detail")),
        "missing_committed_reentry_detail_recorded": (review["missing_committed_reentry_detail"], approval.get("missing_committed_reentry_detail")),
        "actual_live_reentry_source_lacks_complete_29_rows_true": (True, approval.get("actual_live_reentry_source_lacks_complete_29_rows")),
        "success_path_with_injected_snapshot_recorded": (True, approval.get("reentry_success_path_tested_with_complete_29_row_snapshot")),
        "operator_decision_matches": (OPERATOR_DECISION, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_ATTESTATION_PHRASE_V1, attestation.get("operator_attestation_phrase")),
        "approval_scope_only": (True, attestation.get("operator_confirms_approval_scope_only")),
        "selected_package_expose_or_bind_complete_detail": (SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE, approval.get("selected_detail_exposure_or_binding_package")),
        "approval_created_true": (True, approval.get("detail_exposure_or_binding_approval_created")),
        "detail_exposure_or_binding_selected_true": (True, approval.get("detail_exposure_or_binding_selected")),
        "detail_exposure_or_binding_approved_true": (True, approval.get("detail_exposure_or_binding_approved")),
        "detail_exposure_or_binding_authorized_true": (True, approval.get("detail_exposure_or_binding_authorized")),
        "ready_for_detail_exposure_or_binding_execution_true": (True, approval.get("ready_for_detail_exposure_or_binding_execution")),
    }
    false_check_fields = {
        "detail_exposure_or_binding_executed_false": "detail_exposure_or_binding_executed",
        "complete_29_row_detail_exposed_false": "complete_29_row_detail_exposed",
        "complete_29_row_detail_bound_false": "complete_29_row_detail_bound",
        "module_grouping_detail_exposed_by_approval_false": "module_grouping_detail_exposed_by_approval",
        "module_paths_recovered_by_approval_false": "module_paths_recovered_by_approval",
        "per_module_counts_recovered_by_approval_false": "per_module_counts_recovered_by_approval",
        "bounded_nodeid_samples_recovered_by_approval_false": "bounded_nodeid_samples_recovered_by_approval",
        "after_v2_planning_reentry_created_false": "after_v2_planning_execution_reentry_created",
        "after_v2_planning_reentry_performed_false": "after_v2_planning_execution_reentry_performed",
        "targeted_diagnostic_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created_false": "new_retry_candidate_created", "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created",
        "source_recovery_rerun_false": "source_recovery_rerun_performed",
        "cache_read_in_approval_false": "cache_read_in_approval",
        "module_grouping_recovered_in_approval_false": "module_grouping_recovered_in_approval",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed", "diagnostic_output_false": "diagnostic_output_captured",
        "integration_success_false": "integration_execution_successful", "integration_branch_pushed_false": "integration_branch_pushed",
        "main_push_false": "main_push_performed", "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed", "pytest_cache_committed_false": "pytest_cache_committed",
        "evidence_regenerated_false": "evidence_regenerated", "provider_requests_false": "provider_requests_made_in_approval",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_approval",
        "dataset_generation_false": "dataset_generation_performed_in_approval",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values.update({check: (False, approval.get(field)) for check, field in false_check_fields.items()})
    values.update({
        "successful_integration_digest_false": ([False, False], [approval.get("successful_integration_execution_digest_generated"), approval.get("successful_integration_validation_digest_generated")]),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, approval.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, approval.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, approval.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, approval.get("broker_execution")),
        "requirements_approved_for_future_execution": (APPROVED_FUTURE_REQUIREMENTS, approval.get("approved_future_detail_exposure_or_binding_requirements")),
        "future_plan_approved_not_executed": (APPROVED_FUTURE_PLAN, approval.get("approved_future_detail_exposure_or_binding_plan")),
        "planned_outputs_authorized_not_generated": (AUTHORIZED_PLANNED_OUTPUTS, approval.get("authorized_planned_outputs")),
        "supporting_packages_not_selected": (SUPPORTING_PACKAGES, approval.get("supporting_packages")),
        "blocked_packages_not_approved": (BLOCKED_PACKAGES, approval.get("blocked_packages")),
        "next_chain_defined": (NEXT_CHAIN, approval.get("next_chain")), "next_gates_defined": (NEXT_GATES, approval.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, approval.get("risk_controls")),
        "no_tracked_marketflow_files": (False, approval.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, approval.get("pytest_cache_tracked_in_repository")),
    })
    return [_check(check_id, expected, actual) for check_id, (expected, actual) in values.items()]


def _summary(approval: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "detail_exposure_or_binding_selected": approval.get("detail_exposure_or_binding_selected"),
        "detail_exposure_or_binding_approved": approval.get("detail_exposure_or_binding_approved"),
        "detail_exposure_or_binding_authorized": approval.get("detail_exposure_or_binding_authorized"),
        "detail_exposure_or_binding_approval_created": approval.get("detail_exposure_or_binding_approval_created"),
        "selected_detail_exposure_or_binding_package": approval.get("selected_detail_exposure_or_binding_package"),
        "ready_for_detail_exposure_or_binding_execution": approval.get("ready_for_detail_exposure_or_binding_execution"),
        "detail_exposure_or_binding_executed": approval.get("detail_exposure_or_binding_executed"),
        "complete_29_row_detail_exposed": approval.get("complete_29_row_detail_exposed"),
        "complete_29_row_detail_bound": approval.get("complete_29_row_detail_bound"),
        "after_v2_planning_execution_reentry_created": approval.get("after_v2_planning_execution_reentry_created"),
        "after_v2_planning_execution_reentry_performed": approval.get("after_v2_planning_execution_reentry_performed"),
        "targeted_diagnostic_output_capture_candidate_created": approval.get("targeted_diagnostic_output_capture_candidate_created"),
        "new_retry_candidate_created": approval.get("new_retry_candidate_created"),
        "new_retry_executed": approval.get("new_retry_executed"),
        "integration_execution_successful": approval.get("integration_execution_successful"),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest_v1(approval: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(approval))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    _validate_attestation(operator_attestation)
    if source_review is not None:
        source.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(source_review)
        if source_review.get("marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_digest") != SOURCE_OPERATOR_REVIEW_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError("source operator-review digest mismatch")
    approval = _approval_base(operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval, approval["checklist"])
    approval["marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest"] = marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest_v1(approval)
    validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(approval: dict) -> dict:
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError("approval must be an object")
    _validate_attestation(approval.get("operator_attestation", {}))
    expected = _approval_base(approval["operator_attestation"])
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError(f"{field} mismatch")
    checklist = _checklist(approval)
    if approval.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError("checklist invalid")
    summary = _summary(approval, checklist)
    if approval.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError("summary mismatch")
    digest = approval.get("marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError("approval digest missing")
    if digest != marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest_v1(approval):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError("approval digest mismatch")
    return {
        "artifact_kind": approval["artifact_kind"], "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest": digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(
    output_dir: str | Path, *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    approval = build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(
        source_review=source_review, operator_attestation=operator_attestation
    )
    path = Path(output_dir) / "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError("output already exists")
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": approval["artifact_kind"],
            "approval_status": approval["approval_status"], "approval_scope": approval["approval_scope"],
            "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest": approval["marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest"],
            "payload_sha256": sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_markdown_v1(approval: dict) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(approval)
    sections = [
        ("Operator Attestation", [f"Decision: `{OPERATOR_DECISION}`."]),
        ("Source Operator Review", [f"Digest: `{SOURCE_OPERATOR_REVIEW_DIGEST}`."]),
        ("Source Detail Exposure or Binding Candidate", [f"Digest: `{approval['source_detail_exposure_or_binding_candidate_digest']}`."]),
        ("Source Reentry Failure Diagnosis", [approval["primary_failure_class"], approval["source_reentry_failure_diagnosis_digest"]]),
        ("Source Blocked Reentry Execution", [approval["source_reentry_execution_blocked_digest"], approval["source_reentry_execution_blocked_reason"]]),
        ("Source Recovery Results Review", [approval["source_module_grouping_source_recovery_results_review_digest"], approval["source_module_grouping_source_recovery_detail_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the root regression is not retry evidence."]),
        ("Recovered Module Grouping Source Summary", [str(approval["recovered_module_grouping_source_summary"])]),
        ("Available and Missing Committed Detail", [*[f"Available: {item}" for item in approval["available_committed_reentry_detail"]], *[f"Missing: {item}" for item in approval["missing_committed_reentry_detail"]]]),
        ("Approval Scope", [APPROVAL_SCOPE]),
        ("Selected Detail Exposure or Binding Package", [SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE]),
        ("Approved Future Detail Exposure or Binding Requirements", [item["requirement_id"] for item in APPROVED_FUTURE_REQUIREMENTS]),
        ("Approved Future Detail Exposure or Binding Plan", [item["step"] for item in APPROVED_FUTURE_PLAN]),
        ("Planned Outputs", [item["output_id"] for item in AUTHORIZED_PLANNED_OUTPUTS]),
        ("Supporting Packages", [item["package_id"] for item in SUPPORTING_PACKAGES]),
        ("Blocked Packages", [item["package_id"] for item in BLOCKED_PACKAGES]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Approval only; detail exposure, binding, cache access, recovery, planning reentry, diagnostics, remediation, classification, retry, main merge, runtime, and trading remain unexecuted."]),
        ("Checklist Summary", [f"`{validation['passed_checks']}/{validation['total_checks']}` checks pass."]),
        ("Guardrails", ["Separate detail exposure/binding execution and results review are required before planning reentry."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Reentry Module Grouping Detail Exposure or Binding Approval v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND", "APPROVAL_STATUS", "APPROVAL_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVED",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_ONLY_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN",
    "SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE",
    "REQUIRED_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_ATTESTATION_PHRASE_V1",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1",
    "write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_markdown_v1",
    "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest_v1",
]
