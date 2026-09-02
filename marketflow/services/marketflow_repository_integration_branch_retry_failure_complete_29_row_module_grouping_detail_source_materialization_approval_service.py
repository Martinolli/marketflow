"""Approve future materialization of the complete 29-row detail source."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVED_V1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVED"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1"
SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE = "PACKAGE_MATERIALIZE_OR_BIND_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_FOR_REENTRY"
SOURCE_OPERATOR_REVIEW_DIGEST = "72c8e88d3939ecda52acf8b0193a9df340dba832d3947daaf2449d04b0678d90"
OPERATOR_DECISION = "APPROVE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION"
OPERATOR_ATTESTATION_VERSION = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_attestation_v1"
REQUIRED_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVAL_ATTESTATION_PHRASE_V1 = (
    "APPROVE COMPLETE 29 ROW MODULE GROUPING DETAIL SOURCE MATERIALIZATION "
    "PACKAGE_MATERIALIZE_OR_BIND_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_FOR_REENTRY "
    "MARKETFLOW MATERIALIZE OR BIND COMPLETE RECOVERED 29 ROW MODULE GROUPING DETAIL SOURCE FOR FUTURE REENTRY ONLY "
    "NO MATERIALIZATION NOW NO CACHE READ NO SOURCE RECOVERY NO DETAIL BINDING NO PLANNING REENTRY NO RETRY NO FULL PYTEST NO MAIN PUSH "
    "MATERIALIZATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_RETRY_NOT_MAIN"
)
APPROVED_ONLY = "APPROVED_FOR_FUTURE_COMPLETE_29_ROW_MATERIALIZATION_OR_BINDING_EXECUTION_ONLY"
AUTHORIZED_NOT_GENERATED = "AUTHORIZED_NOT_GENERATED"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_V1"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVED_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVED = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE


ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_retry_failure_counts", "operator_confirms_recovered_module_summary",
    "operator_confirms_top_five_paths", "operator_confirms_top_five_count_sum_612",
    "operator_confirms_top_ten_count_sum_1069", "operator_confirms_available_data",
    "operator_confirms_missing_data", "operator_confirms_live_detail_binding_source_lacks_complete_29_rows",
    "operator_confirms_success_path_with_injected_snapshot", "operator_confirms_approval_scope_only",
    "operator_confirms_no_materialization_execution", "operator_confirms_no_complete_29_row_detail_materialized",
    "operator_confirms_no_complete_29_row_detail_exposed", "operator_confirms_no_complete_29_row_detail_bound",
    "operator_confirms_no_complete_29_row_committed_source_created", "operator_confirms_no_module_paths_recovered",
    "operator_confirms_no_per_module_counts_recovered", "operator_confirms_no_bounded_nodeid_samples_recovered",
    "operator_confirms_no_cache_read", "operator_confirms_no_cache_modification",
    "operator_confirms_no_source_recovery", "operator_confirms_no_source_recovery_rerun",
    "operator_confirms_no_detail_binding_execution", "operator_confirms_no_planning_reentry_execution",
    "operator_confirms_no_diagnostic_command", "operator_confirms_no_diagnostic_execution",
    "operator_confirms_no_remediation_execution", "operator_confirms_no_classification_execution",
    "operator_confirms_no_retry", "operator_confirms_no_full_pytest",
    "operator_confirms_no_targeted_diagnostic_candidate", "operator_confirms_no_new_retry_candidate",
    "operator_confirms_no_retry_results_review", "operator_confirms_no_integration_results_review",
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
    "operator_confirms_no_api_key_storage_or_printing", "operator_confirms_no_raw_payload_commit",
]

APPROVED_FUTURE_REQUIREMENTS = [
    {"requirement_id": requirement_id, "approval_status": APPROVED_ONLY, "execution_status": NOT_EXECUTED}
    for requirement_id in source.source.FUTURE_REQUIREMENTS
]

FUTURE_PLAN_STEPS = [
    "Bind this approval, source operator review, source candidate, source diagnosis, blocked detail-binding execution, and blocked reason.",
    "Bind source recovery results-review digest and recovered detail digest.",
    "Use selected controlled complete-detail materialization or binding source.",
    "Verify the selected source contains exactly 29 module rows.",
    "Verify total failed-or-errored node IDs equals 1,404.",
    "Verify top-five counts, top-five sum, top-ten sum, and tier sums.",
    "Verify module paths, per-module counts, and bounded samples are source-derived.",
    "Produce a bounded complete 29-row module grouping source suitable for planning reentry.",
    "Preserve unsupported claims: no failure/error separation, first-order claim, traceback root cause, direct remediation, retry success, or main merge readiness.",
    "Require materialization results review before detail-binding reattempt.",
    "Reattempt detail exposure/binding only after materialization results review.",
    "Keep diagnostic capture, retry, main merge, runtime, and trading closed.",
]
APPROVED_FUTURE_PLAN = [
    {"step_id": f"future_materialization_or_binding_step_{index:02d}", "step": step,
     "approval_status": APPROVED_ONLY, "execution_status": NOT_EXECUTED}
    for index, step in enumerate(FUTURE_PLAN_STEPS, 1)
]

PLANNED_OUTPUT_IDS = [
    "complete_29_row_materialization_approval_manifest", "complete_29_row_payload_source_selection_report",
    "complete_29_row_payload_integrity_requirements", "source_derived_module_paths_requirement_report",
    "per_module_counts_requirement_report", "bounded_nodeid_samples_requirement_report",
    "top_module_concentration_preservation_plan", "tier_sum_preservation_plan",
    "digest_is_not_payload_report", "unsupported_claims_boundary_report",
    "materialization_limitations_report", "detail_binding_reattempt_enablement_report",
    "recommended_next_package_report", "digest_manifest",
]
AUTHORIZED_PLANNED_OUTPUTS = [
    {"output_id": output_id, "authorization_status": AUTHORIZED_NOT_GENERATED}
    for output_id in PLANNED_OUTPUT_IDS
]

SUPPORTING_PACKAGE_STATUSES = {
    "PACKAGE_MATERIALIZE_COMPLETE_29_ROW_DETAIL_FROM_REVIEWED_CACHE_READ_ONLY": "AVAILABLE_NOT_SELECTED_REQUIRES_SEPARATE_APPROVAL",
    "PACKAGE_BIND_COMPLETE_29_ROW_DETAIL_AS_COMMITTED_STATUS_SOURCE_FROM_EXISTING_RECOVERY_ARTIFACT_IF_LOCATABLE": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_OPERATOR_PROVIDES_EXISTING_COMPLETE_RECOVERY_DETAIL_REPORT_PATH": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_CREATE_HIGH_CONTROL_29_ROW_SOURCE_CONSTANT_FROM_REVIEWED_RECOVERY_EVIDENCE": "AVAILABLE_NOT_SELECTED_HIGH_CONTROL",
    "PACKAGE_REDUCED_SCOPE_TOP_FIVE_ONLY_PLANNING": "AVAILABLE_NOT_SELECTED_NOT_RECOMMENDED",
}
SUPPORTING_PACKAGES = [
    {"package_id": package_id, "approval_status": status, "selected": False, "approved": False}
    for package_id, status in SUPPORTING_PACKAGE_STATUSES.items()
]
BLOCKED_PACKAGE_IDS = [
    "PACKAGE_USE_RECOVERY_DETAIL_DIGEST_AS_PROXY_FOR_ROWS", "PACKAGE_INFER_MISSING_24_MODULE_ROWS",
    "PACKAGE_RERUN_PYTEST_TO_RECREATE_ROWS", "PACKAGE_DIRECT_DIAGNOSTIC_CAPTURE_WITHOUT_COMPLETE_DETAIL_REVIEW",
    "PACKAGE_NEW_RETRY_DESPITE_BLOCKED_DETAIL_BINDING", "PACKAGE_MAIN_MERGE_DESPITE_BLOCKED_DETAIL_BINDING_AND_FAILED_RETRY",
]
BLOCKED_PACKAGES = [
    {"package_id": package_id, "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False}
    for package_id in BLOCKED_PACKAGE_IDS
]

NEXT_CHAIN = [
    "Complete 29-row Module Grouping Detail Source Materialization Execution v1, if approved.",
    "Complete 29-row Module Grouping Detail Source Materialization Results Review v1.",
    "Detail Exposure or Binding Execution reattempt using complete committed source.",
    "Detail Exposure or Binding Results Review.",
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
    "complete_29_row_module_grouping_detail_source_materialization_execution_if_approved",
    "complete_29_row_module_grouping_detail_source_materialization_results_review",
    "detail_exposure_or_binding_execution_reattempt_with_complete_source", "detail_exposure_or_binding_results_review",
    "after_v2_planning_reentry_execution_with_complete_detail",
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
    "targeted_diagnostic_output_capture_candidate_if_supported", "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected", "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review", "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "approval_materialization_does_not_execute_materialization", "approval_materialization_does_not_materialize_29_row_source",
    "approval_materialization_does_not_expose_29_module_rows", "approval_materialization_does_not_bind_complete_detail",
    "approval_materialization_does_not_recover_module_grouping_again", "approval_materialization_does_not_read_cache",
    "approval_materialization_does_not_modify_cache", "approval_materialization_does_not_parse_operator_logs",
    "approval_materialization_does_not_run_diagnostic_commands", "approval_materialization_does_not_execute_diagnostics",
    "approval_materialization_does_not_execute_remediation", "approval_materialization_does_not_execute_classification",
    "approval_materialization_does_not_classify_modules_again", "approval_materialization_does_not_execute_detail_binding",
    "approval_materialization_does_not_execute_after_v2_planning_reentry", "approval_materialization_does_not_rerun_retry",
    "approval_materialization_does_not_run_full_pytest", "approval_materialization_does_not_create_targeted_diagnostic_candidate",
    "approval_materialization_does_not_create_new_retry_candidate", "approval_materialization_does_not_create_retry_results_review",
    "approval_materialization_does_not_create_integration_results_review", "approval_materialization_does_not_mark_integration_successful",
    "approval_materialization_does_not_generate_successful_integration_digest", "approval_materialization_does_not_claim_failure_error_separation",
    "approval_materialization_does_not_claim_first_failure", "approval_materialization_does_not_claim_first_error",
    "approval_materialization_does_not_claim_traceback_root_cause", "approval_materialization_does_not_recommend_direct_code_remediation",
    "approval_materialization_does_not_treat_digest_as_payload", "approval_materialization_does_not_treat_detail_as_retry_success",
    "approval_materialization_does_not_push_integration_branch", "approval_materialization_does_not_push_main",
    "approval_materialization_does_not_delete_integration_branch", "approval_materialization_does_not_delete_worktree",
    "approval_materialization_does_not_force_push", "approval_materialization_does_not_prune_remotes",
    "approval_materialization_does_not_modify_tags", "approval_materialization_does_not_modify_staged_evidence",
    "approval_materialization_does_not_regenerate_evidence", "approval_materialization_does_not_call_providers",
    "approval_materialization_does_not_acquire_market_data", "approval_materialization_does_not_regenerate_dataset",
    "approval_materialization_does_not_recompute_metrics", "approval_materialization_does_not_train_models",
    "approval_materialization_does_not_score_strategy", "approval_materialization_does_not_generate_recommendations",
    "approval_materialization_does_not_accept_predictive_usefulness", "approval_materialization_does_not_accept_profitability",
    "approval_materialization_does_not_authorize_runtime", "approval_materialization_does_not_authorize_broker_execution",
    "selected_materialization_package_approved_for_future_execution_only", "complete_detail_materialization_output_would_be_planning_source_not_root_cause",
    "digest_only_is_not_complete_detail_payload", "top_five_only_is_not_complete_29_row_source",
    "complete_detail_gap_is_not_retry_success", "complete_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_execution_remains_historically_blocked", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_execution_required_before_materialization", "separate_results_review_required_after_materialization",
    "separate_detail_binding_reattempt_required_after_materialization_review", "separate_retry_approval_required_before_new_retry",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]

FALSE_BOUNDARIES = [
    "materialization_package_executed", "complete_29_row_detail_materialized", "complete_29_row_detail_exposed",
    "complete_29_row_detail_bound", "complete_29_row_detail_committed_source_created",
    "module_grouping_detail_materialized_by_approval", "module_paths_recovered_by_approval",
    "per_module_counts_recovered_by_approval", "bounded_nodeid_samples_recovered_by_approval",
    "detail_exposure_or_binding_reattempt_created", "after_v2_planning_execution_reentry_created",
    "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
    "main_merge_approval_created", "source_recovery_rerun_performed", "cache_read_in_approval",
    "module_grouping_recovered_in_approval", "retry_rerun_performed", "full_pytest_performed",
    "diagnostic_command_executed", "diagnostic_output_captured", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_approval", "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]
UNSUPPORTED_CLAIMS_FIELDS = [
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended", "retry_success_claimed",
    "main_merge_readiness_claimed", "diagnostic_method_executed", "code_remediation_executed",
    "evidence_remediation_executed", "classification_execution_performed_in_approval",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError(ValueError):
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
    return source.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1()


def _attestation_string_expectations() -> dict[str, str]:
    review = _committed_source_review()
    return {
        "operator_decision": OPERATOR_DECISION,
        "selected_complete_29_row_materialization_package": SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
        "operator_attestation_phrase": REQUIRED_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVAL_ATTESTATION_PHRASE_V1,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_digest": review["source_complete_29_row_materialization_candidate_digest"],
        "operator_confirms_source_diagnosis_digest": review["source_detail_exposure_or_binding_execution_failure_diagnosis_digest"],
        "operator_confirms_primary_failure_class": review["primary_failure_class"],
        "operator_confirms_source_detail_binding_blocked_execution_digest": review["source_detail_exposure_or_binding_execution_blocked_digest"],
        "operator_confirms_source_detail_binding_blocked_manifest_digest": review["source_detail_exposure_or_binding_execution_blocked_manifest_digest"],
        "operator_confirms_source_detail_binding_blocked_reason": review["blocked_reason"],
        "operator_confirms_source_detail_binding_approval_digest": review["source_detail_exposure_or_binding_approval_digest"],
        "operator_confirms_source_detail_binding_operator_review_digest": review["source_detail_exposure_or_binding_operator_review_digest"],
        "operator_confirms_source_detail_binding_candidate_digest": review["source_detail_exposure_or_binding_candidate_digest"],
        "operator_confirms_source_reentry_failure_diagnosis_digest": review["source_reentry_failure_diagnosis_digest"],
        "operator_confirms_source_reentry_blocked_execution_digest": review["source_reentry_execution_blocked_digest"],
        "operator_confirms_source_reentry_blocked_manifest_digest": review["source_reentry_execution_blocked_manifest_digest"],
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
        "operator_confirms_selected_materialization_package": SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    for field, expected in _attestation_string_expectations().items():
        if attestation.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError(f"{field} mismatch")
    if not _iso_utc(attestation.get("operator_attestation_timestamp_utc")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError("operator attestation timestamp invalid")
    if not isinstance(attestation.get("operator_reference"), str) or not attestation["operator_reference"].strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError("operator reference missing")
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError(f"{field} must be true")


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_candidate_digest: str,
    operator_confirms_source_diagnosis_digest: str,
    operator_confirms_primary_failure_class: str,
    operator_confirms_source_detail_binding_blocked_execution_digest: str,
    operator_confirms_source_detail_binding_blocked_manifest_digest: str,
    operator_confirms_source_detail_binding_blocked_reason: str,
    operator_confirms_source_detail_binding_approval_digest: str,
    operator_confirms_source_detail_binding_operator_review_digest: str,
    operator_confirms_source_detail_binding_candidate_digest: str,
    operator_confirms_source_reentry_failure_diagnosis_digest: str,
    operator_confirms_source_reentry_blocked_execution_digest: str,
    operator_confirms_source_reentry_blocked_manifest_digest: str,
    operator_confirms_source_planning_reentry_digest: str,
    operator_confirms_source_recovery_results_review_digest: str,
    operator_confirms_source_recovery_results_review_manifest_digest: str,
    operator_confirms_source_recovery_execution_digest: str,
    operator_confirms_source_recovery_detail_digest: str,
    operator_confirms_source_recovery_digest_manifest_digest: str,
    operator_confirms_source_blocked_after_v2_execution_digest: str,
    operator_confirms_source_after_v2_approval_digest: str,
    operator_confirms_source_results_review_v2_digest: str,
    operator_confirms_source_execution_v2_digest: str,
    operator_confirms_source_module_grouping_digest: str,
    operator_confirms_retry_execution_commit: str,
    operator_confirms_retry_failure_counts: bool,
    operator_confirms_recovered_module_summary: bool,
    operator_confirms_top_five_paths: bool,
    operator_confirms_top_five_count_sum_612: bool,
    operator_confirms_top_ten_count_sum_1069: bool,
    operator_confirms_available_data: bool,
    operator_confirms_missing_data: bool,
    operator_confirms_live_detail_binding_source_lacks_complete_29_rows: bool,
    operator_confirms_success_path_with_injected_snapshot: bool,
    operator_confirms_selected_materialization_package: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_no_materialization_execution: bool,
    operator_confirms_no_complete_29_row_detail_materialized: bool,
    operator_confirms_no_complete_29_row_detail_exposed: bool,
    operator_confirms_no_complete_29_row_detail_bound: bool,
    operator_confirms_no_complete_29_row_committed_source_created: bool,
    operator_confirms_no_module_paths_recovered: bool,
    operator_confirms_no_per_module_counts_recovered: bool,
    operator_confirms_no_bounded_nodeid_samples_recovered: bool,
    operator_confirms_no_cache_read: bool,
    operator_confirms_no_cache_modification: bool,
    operator_confirms_no_source_recovery: bool,
    operator_confirms_no_source_recovery_rerun: bool,
    operator_confirms_no_detail_binding_execution: bool,
    operator_confirms_no_planning_reentry_execution: bool,
    operator_confirms_no_diagnostic_command: bool,
    operator_confirms_no_diagnostic_execution: bool,
    operator_confirms_no_remediation_execution: bool,
    operator_confirms_no_classification_execution: bool,
    operator_confirms_no_retry: bool,
    operator_confirms_no_full_pytest: bool,
    operator_confirms_no_targeted_diagnostic_candidate: bool,
    operator_confirms_no_new_retry_candidate: bool,
    operator_confirms_no_retry_results_review: bool,
    operator_confirms_no_integration_results_review: bool,
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
    operator_confirms_no_raw_payload_commit: bool,
    selected_complete_29_row_materialization_package: str = SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Create and validate the non-secret operator approval attestation."""

    attestation = dict(locals())
    attestation["operator_attestation_version"] = OPERATOR_ATTESTATION_VERSION
    _validate_attestation(attestation)
    return attestation


SOURCE_COPY_FIELDS = [
    "source_detail_exposure_or_binding_execution_failure_diagnosis_digest", "primary_failure_class",
    "source_detail_exposure_or_binding_execution_blocked_digest",
    "source_detail_exposure_or_binding_execution_blocked_manifest_digest",
    "source_detail_exposure_or_binding_approval_digest", "source_detail_exposure_or_binding_operator_review_digest",
    "source_detail_exposure_or_binding_candidate_digest", "source_reentry_failure_diagnosis_digest",
    "source_primary_failure_class", "source_reentry_execution_blocked_digest",
    "source_reentry_execution_blocked_manifest_digest", "source_reentry_execution_blocked_reason",
    "source_after_v2_planning_reentry_digest", "source_module_grouping_source_recovery_results_review_digest",
    "source_module_grouping_source_recovery_results_review_manifest_digest",
    "source_module_grouping_source_recovery_execution_digest", "source_module_grouping_source_recovery_detail_digest",
    "source_module_grouping_source_recovery_digest_manifest_digest", "source_module_grouping_source_recovery_approval_digest",
    "source_module_grouping_source_recovery_operator_review_digest", "source_module_grouping_source_recovery_candidate_digest",
    "source_blocked_after_v2_execution_digest", "source_blocked_after_v2_manifest_digest",
    "source_after_v2_approval_digest", "source_after_v2_operator_review_digest", "source_after_v2_candidate_digest",
    "source_results_review_v2_digest", "source_execution_v2_digest", "source_module_grouping_digest",
    "source_approval_v2_digest", "source_staged_inventory_digest", "retry_execution_commit", "retry_failure_context",
    "recovered_module_grouping_source_summary", "top_module_summary", "top_5_count_sum", "top_10_count_sum",
    "source_execution_available_data", "source_execution_missing_data",
    "actual_live_detail_binding_source_lacks_complete_29_rows",
    "detail_binding_success_path_tested_with_complete_29_row_snapshot",
]


def _approval_base(attestation: Mapping[str, Any]) -> dict[str, Any]:
    review = _committed_source_review()
    approval: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_complete_29_row_materialization_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_complete_29_row_materialization_operator_review_status": source.REVIEW_STATUS,
        "source_complete_29_row_materialization_operator_review_scope": source.REVIEW_SCOPE,
        "source_complete_29_row_materialization_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_complete_29_row_materialization_candidate_digest": review["source_complete_29_row_materialization_candidate_digest"],
    }
    approval.update({field: deepcopy(review[field]) for field in SOURCE_COPY_FIELDS})
    approval["source_detail_exposure_or_binding_execution_blocked_reason"] = review["blocked_reason"]
    approval["available_data"] = deepcopy(review["source_execution_available_data"])
    approval["missing_data"] = deepcopy(review["source_execution_missing_data"])
    approval.update({
        "approved_package": {
            "package_id": SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
            "approval_status": APPROVED_ONLY, "selected": True, "approved": True,
            "authorized_for_future_execution": True, "executed": False,
            "purpose": "Future execution may materialize, expose, or bind the complete 29-row recovered module grouping detail source required for deterministic planning reentry, without inference, retry rerun, provider calls, or main-merge authority.",
        },
        "selected_complete_29_row_materialization_package": SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
        "approved_future_materialization_or_binding_requirements": deepcopy(APPROVED_FUTURE_REQUIREMENTS),
        "approved_future_materialization_or_binding_plan": deepcopy(APPROVED_FUTURE_PLAN),
        "authorized_planned_outputs": deepcopy(AUTHORIZED_PLANNED_OUTPUTS),
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES), "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "materialization_package_selected": True, "materialization_package_approved": True,
        "materialization_package_authorized": True, "complete_29_row_materialization_approval_created": True,
        "ready_for_complete_29_row_materialization_execution": True,
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
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    review = _committed_source_review()
    attestation = approval.get("operator_attestation", {})
    values: dict[str, tuple[Any, Any]] = {
        "source_operator_review_digest_bound": (SOURCE_OPERATOR_REVIEW_DIGEST, approval.get("source_complete_29_row_materialization_operator_review_digest")),
        "source_candidate_digest_bound": (review["source_complete_29_row_materialization_candidate_digest"], approval.get("source_complete_29_row_materialization_candidate_digest")),
        "source_diagnosis_digest_bound": (review["source_detail_exposure_or_binding_execution_failure_diagnosis_digest"], approval.get("source_detail_exposure_or_binding_execution_failure_diagnosis_digest")),
        "source_primary_failure_class_bound": (review["primary_failure_class"], approval.get("primary_failure_class")),
        "source_detail_binding_execution_blocked_digest_bound": (review["source_detail_exposure_or_binding_execution_blocked_digest"], approval.get("source_detail_exposure_or_binding_execution_blocked_digest")),
        "source_detail_binding_execution_blocked_manifest_digest_bound": (review["source_detail_exposure_or_binding_execution_blocked_manifest_digest"], approval.get("source_detail_exposure_or_binding_execution_blocked_manifest_digest")),
        "source_detail_binding_execution_blocked_reason_bound": (review["blocked_reason"], approval.get("source_detail_exposure_or_binding_execution_blocked_reason")),
        "source_detail_binding_approval_digest_bound": (review["source_detail_exposure_or_binding_approval_digest"], approval.get("source_detail_exposure_or_binding_approval_digest")),
        "source_detail_binding_operator_review_digest_bound": (review["source_detail_exposure_or_binding_operator_review_digest"], approval.get("source_detail_exposure_or_binding_operator_review_digest")),
        "source_detail_binding_candidate_digest_bound": (review["source_detail_exposure_or_binding_candidate_digest"], approval.get("source_detail_exposure_or_binding_candidate_digest")),
        "source_reentry_failure_diagnosis_digest_bound": (review["source_reentry_failure_diagnosis_digest"], approval.get("source_reentry_failure_diagnosis_digest")),
        "source_reentry_execution_blocked_digest_bound": (review["source_reentry_execution_blocked_digest"], approval.get("source_reentry_execution_blocked_digest")),
        "source_reentry_execution_blocked_manifest_digest_bound": (review["source_reentry_execution_blocked_manifest_digest"], approval.get("source_reentry_execution_blocked_manifest_digest")),
        "source_reentry_execution_blocked_reason_bound": (review["source_reentry_execution_blocked_reason"], approval.get("source_reentry_execution_blocked_reason")),
        "source_planning_reentry_digest_bound": (review["source_after_v2_planning_reentry_digest"], approval.get("source_after_v2_planning_reentry_digest")),
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
        "available_data_recorded": (review["source_execution_available_data"], approval.get("available_data")),
        "missing_data_recorded": (review["source_execution_missing_data"], approval.get("missing_data")),
        "actual_live_detail_binding_source_lacks_complete_29_rows_true": (True, approval.get("actual_live_detail_binding_source_lacks_complete_29_rows")),
        "success_path_with_injected_snapshot_recorded": (True, approval.get("detail_binding_success_path_tested_with_complete_29_row_snapshot")),
        "operator_decision_matches": (OPERATOR_DECISION, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVAL_ATTESTATION_PHRASE_V1, attestation.get("operator_attestation_phrase")),
        "approval_scope_only": (True, attestation.get("operator_confirms_approval_scope_only")),
        "selected_package_materialize_or_bind_complete_29_row_source": (SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE, approval.get("selected_complete_29_row_materialization_package")),
        "approval_created_true": (True, approval.get("complete_29_row_materialization_approval_created")),
        "materialization_package_selected_true": (True, approval.get("materialization_package_selected")),
        "materialization_package_approved_true": (True, approval.get("materialization_package_approved")),
        "materialization_package_authorized_true": (True, approval.get("materialization_package_authorized")),
        "ready_for_complete_29_row_materialization_execution_true": (True, approval.get("ready_for_complete_29_row_materialization_execution")),
    }
    false_check_fields = {
        "materialization_package_executed_false": "materialization_package_executed",
        "complete_29_row_detail_materialized_false": "complete_29_row_detail_materialized",
        "complete_29_row_detail_exposed_false": "complete_29_row_detail_exposed",
        "complete_29_row_detail_bound_false": "complete_29_row_detail_bound",
        "complete_29_row_detail_committed_source_created_false": "complete_29_row_detail_committed_source_created",
        "module_grouping_detail_materialized_by_approval_false": "module_grouping_detail_materialized_by_approval",
        "module_paths_recovered_by_approval_false": "module_paths_recovered_by_approval",
        "per_module_counts_recovered_by_approval_false": "per_module_counts_recovered_by_approval",
        "bounded_nodeid_samples_recovered_by_approval_false": "bounded_nodeid_samples_recovered_by_approval",
        "detail_binding_reattempt_created_false": "detail_exposure_or_binding_reattempt_created",
        "after_v2_planning_reentry_created_false": "after_v2_planning_execution_reentry_created",
        "after_v2_planning_reentry_performed_false": "after_v2_planning_execution_reentry_performed",
        "targeted_diagnostic_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created_false": "new_retry_candidate_created",
        "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created",
        "source_recovery_rerun_false": "source_recovery_rerun_performed",
        "cache_read_in_approval_false": "cache_read_in_approval",
        "module_grouping_recovered_in_approval_false": "module_grouping_recovered_in_approval",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed", "diagnostic_output_false": "diagnostic_output_captured",
        "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed", "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed", "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_approval",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_approval",
        "dataset_generation_false": "dataset_generation_performed_in_approval",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values.update({check_id: (False, approval.get(field)) for check_id, field in false_check_fields.items()})
    values.update({
        "successful_integration_digest_false": ([False, False], [approval.get("successful_integration_execution_digest_generated"), approval.get("successful_integration_validation_digest_generated")]),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, approval.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, approval.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, approval.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, approval.get("broker_execution")),
        "requirements_approved_for_future_execution": (APPROVED_FUTURE_REQUIREMENTS, approval.get("approved_future_materialization_or_binding_requirements")),
        "future_plan_approved_not_executed": (APPROVED_FUTURE_PLAN, approval.get("approved_future_materialization_or_binding_plan")),
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
        "materialization_package_selected": approval.get("materialization_package_selected"),
        "materialization_package_approved": approval.get("materialization_package_approved"),
        "materialization_package_authorized": approval.get("materialization_package_authorized"),
        "complete_29_row_materialization_approval_created": approval.get("complete_29_row_materialization_approval_created"),
        "selected_complete_29_row_materialization_package": approval.get("selected_complete_29_row_materialization_package"),
        "ready_for_complete_29_row_materialization_execution": approval.get("ready_for_complete_29_row_materialization_execution"),
        "materialization_package_executed": approval.get("materialization_package_executed"),
        "complete_29_row_detail_materialized": approval.get("complete_29_row_detail_materialized"),
        "complete_29_row_detail_exposed": approval.get("complete_29_row_detail_exposed"),
        "complete_29_row_detail_bound": approval.get("complete_29_row_detail_bound"),
        "complete_29_row_detail_committed_source_created": approval.get("complete_29_row_detail_committed_source_created"),
        "detail_exposure_or_binding_reattempt_created": approval.get("detail_exposure_or_binding_reattempt_created"),
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


def marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(approval))
    for field in (
        "checklist", "summary",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Build the offline approval; no materialization or source access occurs."""

    _validate_attestation(operator_attestation)
    if source_review is not None:
        source.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(source_review)
        digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_digest"
        if source_review.get(digest_key) != SOURCE_OPERATOR_REVIEW_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError("source operator-review digest mismatch")
    approval = _approval_base(operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval, approval["checklist"])
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest"
    approval[digest_key] = marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest_v1(approval)
    validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(
    approval: dict,
) -> dict:
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError("approval must be an object")
    _validate_attestation(approval.get("operator_attestation", {}))
    expected = _approval_base(approval["operator_attestation"])
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError(f"{field} mismatch")
    checklist = _checklist(approval)
    if approval.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError("checklist invalid")
    summary = _summary(approval, checklist)
    if approval.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError("summary mismatch")
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest"
    digest = approval.get(digest_key)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError("approval digest missing")
    if digest != marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest_v1(approval):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError("approval digest mismatch")
    return {
        "artifact_kind": approval["artifact_kind"], "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"], digest_key: digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(
    output_dir: str | Path, *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    approval = build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(
        source_review=source_review, operator_attestation=operator_attestation,
    )
    path = Path(output_dir) / "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError("output already exists")
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest"
    return {
        "path": str(path), "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"], "approval_scope": approval["approval_scope"],
        digest_key: approval[digest_key], "payload_sha256": sha256_bytes(payload),
    }


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_markdown_v1(
    approval: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(approval)
    sections = [
        ("Operator Attestation", [f"Decision: `{OPERATOR_DECISION}`."]),
        ("Source Materialization Candidate Operator Review", [SOURCE_OPERATOR_REVIEW_DIGEST, source.REVIEW_STATUS]),
        ("Source Materialization Candidate", [approval["source_complete_29_row_materialization_candidate_digest"]]),
        ("Source Detail Exposure or Binding Execution Failure Diagnosis", [approval["source_detail_exposure_or_binding_execution_failure_diagnosis_digest"], approval["primary_failure_class"]]),
        ("Source Blocked Detail Exposure or Binding Execution", [approval["source_detail_exposure_or_binding_execution_blocked_digest"], approval["source_detail_exposure_or_binding_execution_blocked_reason"]]),
        ("Source Detail Exposure or Binding Approval", [approval["source_detail_exposure_or_binding_approval_digest"]]),
        ("Source Reentry Failure Diagnosis", [approval["source_reentry_failure_diagnosis_digest"]]),
        ("Source Recovery Results Review", [approval["source_module_grouping_source_recovery_results_review_digest"], approval["source_module_grouping_source_recovery_detail_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the root regression is not retry evidence."]),
        ("Recovered Module Grouping Source Summary", [str(approval["recovered_module_grouping_source_summary"])]),
        ("Available and Missing Detail Source", [*[f"Available: {item}" for item in approval["available_data"]], *[f"Missing: {item}" for item in approval["missing_data"]]]),
        ("Approval Scope", [APPROVAL_SCOPE]),
        ("Selected Complete 29-row Materialization Package", [SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE]),
        ("Approved Future Materialization or Binding Requirements", [item["requirement_id"] for item in APPROVED_FUTURE_REQUIREMENTS]),
        ("Approved Future Materialization or Binding Plan", [item["step"] for item in APPROVED_FUTURE_PLAN]),
        ("Planned Outputs", [item["output_id"] for item in AUTHORIZED_PLANNED_OUTPUTS]),
        ("Supporting Packages", [item["package_id"] for item in SUPPORTING_PACKAGES]),
        ("Blocked Packages", [item["package_id"] for item in BLOCKED_PACKAGES]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Approval only; materialization, row exposure, detail binding, cache access, recovery, planning reentry, diagnostics, remediation, classification, retry, main merge, runtime, and trading remain unexecuted."]),
        ("Checklist Summary", [f"`{validation['passed_checks']}/{validation['total_checks']}` checks pass."]),
        ("Guardrails", ["Separate materialization execution and results review are required before any detail-binding reattempt."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Complete 29-row Module Grouping Detail Source Materialization Approval v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND", "APPROVAL_STATUS", "APPROVAL_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVED",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN",
    "SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE",
    "REQUIRED_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVAL_ATTESTATION_PHRASE_V1",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1",
    "write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_markdown_v1",
    "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest_v1",
]
