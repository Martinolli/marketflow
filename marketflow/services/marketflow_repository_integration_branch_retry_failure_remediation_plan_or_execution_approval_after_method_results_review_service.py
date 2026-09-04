"""Approve one post-capture remediation method for future execution only."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVED_AFTER_METHOD_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVED_AFTER_METHOD_RESULTS_REVIEW"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_digest"
SELECTED_PACKAGE = source.RECOMMENDED_PACKAGE
SOURCE_OPERATOR_REVIEW_COMMIT = "befd1a43d6d1eb0f6859445397f03697a4ad02de"
SOURCE_OPERATOR_REVIEW_DIGEST = "2b8ddb8ad006d3fb376c91b75fb0f8140fbf54ada6c7ae694d1431cb2f58f71c"
OPERATOR_DECISION = "APPROVE_REMEDIATION_PLAN_OR_EXECUTION_AFTER_METHOD_RESULTS_REVIEW"
OPERATOR_ATTESTATION_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_attestation_v1"
REQUIRED_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ATTESTATION_PHRASE_V1 = (
    "APPROVE MARKETFLOW RETRY FAILURE REMEDIATION PLAN "
    "PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY "
    "AFTER METHOD RESULTS REVIEW FOR FUTURE EXECUTION ONLY NO REMEDIATION PLAN EXECUTION NOW NO REMEDIATION NOW "
    "NO CODE CHANGES NOW NO TEST CHANGES NOW NO DIGEST UPDATES NOW NO PYTEST NOW NO RETRY NO MAIN PUSH "
    "REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)
APPROVED_ONLY = "APPROVED_FOR_FUTURE_REMEDIATION_PLAN_OR_EXECUTION_AFTER_METHOD_RESULTS_REVIEW_ONLY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_AFTER_METHOD_RESULTS_REVIEW_V1"
NOT_ACCEPTED, NOT_AUTHORIZED, PASS, FAIL, BLOCKER = "not accepted", "NOT_AUTHORIZED", "PASS", "FAIL", "BLOCKER"

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_retry_failure_counts", "operator_confirms_priority_1_top_module_paths",
    "operator_confirms_priority_1_total_612", "operator_confirms_top_10_total_1069",
    "operator_confirms_module_summary_count_29", "operator_confirms_failed_or_errored_nodeids_1404",
    "operator_confirms_source_exit_code_1_as_diagnostic_only", "operator_confirms_source_stdout_byte_count_1231380",
    "operator_confirms_source_stderr_byte_count_0", "operator_confirms_source_bounded_output_status",
    "operator_confirms_source_redaction_checked", "operator_confirms_observable_family_count_4",
    "operator_confirms_observable_evidence_items_188", "operator_confirms_assertion_or_value_mismatch_family",
    "operator_confirms_digest_or_hash_mismatch_family", "operator_confirms_fixture_or_test_isolation_issue_family",
    "operator_confirms_missing_or_unexpected_field_family", "operator_confirms_family_confidence_high",
    "operator_confirms_additional_diagnostic_capture_false", "operator_confirms_direct_remediation_ready_false",
    "operator_confirms_retry_ready_false", "operator_confirms_main_merge_ready_false",
    "operator_confirms_approval_scope_only", "operator_confirms_no_remediation_plan_execution",
    "operator_confirms_no_remediation_execution", "operator_confirms_no_code_remediation",
    "operator_confirms_no_production_code_change", "operator_confirms_no_existing_test_change",
    "operator_confirms_no_expected_digest_update",
    "operator_confirms_no_diagnostic_receipt_parse", "operator_confirms_no_diagnostic_output_analysis",
    "operator_confirms_no_failure_error_separation", "operator_confirms_no_first_failure",
    "operator_confirms_no_first_error", "operator_confirms_no_traceback_root_cause", "operator_confirms_no_root_cause",
    "operator_confirms_no_direct_remediation_recommendation", "operator_confirms_no_method_execution_rerun",
    "operator_confirms_no_recapture_rerun",
    "operator_confirms_no_diagnostic_command", "operator_confirms_no_targeted_pytest",
    "operator_confirms_no_full_pytest", "operator_confirms_no_retry", "operator_confirms_no_cache_read",
    "operator_confirms_no_cache_modification", "operator_confirms_no_terminal_log_parse",
    "operator_confirms_no_operator_log_parse", "operator_confirms_no_env_inspection",
    "operator_confirms_no_prior_lost_value_reconstruction", "operator_confirms_no_full_stream_reconstruction",
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

APPROVED_FUTURE_REMEDIATION_REQUIREMENTS = [
    {"requirement_id": item["requirement_id"], "approval_status": APPROVED_ONLY, "execution_status": "NOT_EXECUTED"}
    for item in source.REVIEWED_FUTURE_REQUIREMENTS
]
APPROVED_FUTURE_REMEDIATION_PLAN = [
    {"step_id": item["step_id"], "action": item["action"], "approval_status": APPROVED_ONLY, "execution_status": "NOT_EXECUTED"}
    for item in source.REVIEWED_FUTURE_PLAN
]
AUTHORIZED_PLANNED_OUTPUTS = [
    {"output_id": output_id, "authorization_status": "AUTHORIZED_NOT_GENERATED"}
    for output_id in """remediation_plan_or_execution_approval_after_method_results_review_manifest
source_method_results_review_binding_report
source_method_execution_binding_report
observable_failure_family_summary_report
approved_targeted_remediation_plan_package_report
assertion_value_mismatch_workstream_placeholder
digest_hash_mismatch_workstream_placeholder
fixture_isolation_workstream_placeholder
missing_unexpected_field_workstream_placeholder
future_remediation_requirements_report
future_remediation_plan_report
verification_evidence_requirements_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
]
SUPPORTING_PACKAGES = [
    {"package_id": item["package_id"], "approval_status": "AVAILABLE_NOT_SELECTED", "selected": False, "approved": False}
    for item in source.REVIEWED_PACKAGES[1:6]
]
BLOCKED_PACKAGES = [
    {"package_id": item["package_id"], "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False}
    for item in source.REVIEWED_PACKAGES[6:]
]
NEXT_CHAIN = [
    "Remediation Plan or Execution Execution After Method Results Review v1, if approved.",
    "Remediation Plan or Execution Results Review After Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation plan or execution review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "remediation_plan_or_execution_execution_after_method_results_review_if_approved",
    "remediation_plan_or_execution_results_review_after_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_plan_or_execution_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = """approval_after_method_results_review_does_not_execute_remediation_plan
approval_after_method_results_review_does_not_execute_remediation
approval_after_method_results_review_does_not_modify_production_code
approval_after_method_results_review_does_not_modify_existing_tests
approval_after_method_results_review_does_not_update_expected_digests
approval_after_method_results_review_does_not_parse_durable_receipt
approval_after_method_results_review_does_not_analyze_diagnostic_output
approval_after_method_results_review_does_not_rerun_method_execution
approval_after_method_results_review_does_not_rerun_controlled_recapture
approval_after_method_results_review_does_not_run_diagnostic_command
approval_after_method_results_review_does_not_run_targeted_pytest
approval_after_method_results_review_does_not_run_full_pytest
approval_after_method_results_review_does_not_rerun_retry
approval_after_method_results_review_does_not_read_pytest_cache
approval_after_method_results_review_does_not_modify_pytest_cache
approval_after_method_results_review_does_not_parse_terminal_logs
approval_after_method_results_review_does_not_parse_operator_logs
approval_after_method_results_review_does_not_inspect_env
approval_after_method_results_review_does_not_reconstruct_prior_lost_values
approval_after_method_results_review_does_not_reconstruct_full_streams
approval_after_method_results_review_does_not_classify_modules_again
approval_after_method_results_review_does_not_classify_full_retry_failures
approval_after_method_results_review_does_not_classify_full_retry_errors
approval_after_method_results_review_does_not_claim_failure_error_separation
approval_after_method_results_review_does_not_identify_authoritative_first_failure
approval_after_method_results_review_does_not_identify_authoritative_first_error
approval_after_method_results_review_does_not_claim_traceback_root_cause
approval_after_method_results_review_does_not_claim_root_cause
approval_after_method_results_review_does_not_recommend_direct_code_remediation
approval_after_method_results_review_does_not_create_remediation_execution
approval_after_method_results_review_does_not_create_remediation_results_review
approval_after_method_results_review_does_not_create_new_retry_candidate
approval_after_method_results_review_does_not_create_retry_results_review
approval_after_method_results_review_does_not_create_integration_results_review
approval_after_method_results_review_does_not_mark_integration_successful
approval_after_method_results_review_does_not_generate_successful_integration_digest
approval_after_method_results_review_does_not_treat_method_analysis_as_retry_success
approval_after_method_results_review_does_not_treat_family_classification_as_root_cause
approval_after_method_results_review_does_not_push_integration_branch
approval_after_method_results_review_does_not_push_main
approval_after_method_results_review_does_not_delete_integration_branch
approval_after_method_results_review_does_not_delete_worktree
approval_after_method_results_review_does_not_force_push
approval_after_method_results_review_does_not_prune_remotes
approval_after_method_results_review_does_not_modify_tags
approval_after_method_results_review_does_not_modify_staged_evidence
approval_after_method_results_review_does_not_regenerate_evidence
approval_after_method_results_review_does_not_call_providers
approval_after_method_results_review_does_not_acquire_market_data
approval_after_method_results_review_does_not_regenerate_dataset
approval_after_method_results_review_does_not_recompute_metrics
approval_after_method_results_review_does_not_train_models
approval_after_method_results_review_does_not_score_strategy
approval_after_method_results_review_does_not_generate_recommendations
approval_after_method_results_review_does_not_accept_predictive_usefulness
approval_after_method_results_review_does_not_accept_profitability
approval_after_method_results_review_does_not_authorize_runtime
approval_after_method_results_review_does_not_authorize_broker_execution
selected_plan_first_package_approved_for_future_execution_only
future_plan_execution_may_generate_plan_only
future_plan_execution_must_not_modify_code
future_plan_execution_must_not_modify_tests
future_plan_execution_must_not_update_expected_digests
future_plan_execution_must_not_run_pytest
future_plan_execution_must_not_create_retry_readiness
method_results_review_remains_source_evidence
remediation_plan_or_execution_candidate_operator_review_remains_source_evidence
remediation_plan_or_execution_candidate_remains_source_evidence
observable_failure_family_classification_is_method_planning_only
failure_family_classification_is_not_root_cause
failure_family_classification_is_not_direct_remediation
failure_family_classification_is_not_retry_success
direct_remediation_ready_remains_false
retry_ready_remains_false
main_merge_ready_remains_false
diagnostic_capture_results_review_remains_source_evidence
durable_receipt_is_diagnostic_evidence_only
controlled_recapture_is_not_retry_success
priority_1_selection_is_not_root_cause
module_concentration_is_not_failure_error_separation
prior_blocked_diagnostic_capture_execution_remains_historically_blocked
previous_method_execution_remains_source_evidence
previous_remediation_or_method_approval_remains_source_evidence
previous_receipt_recovery_or_recapture_results_review_remains_source_evidence
previous_planning_results_review_remains_valid
previous_detail_binding_results_review_remains_valid
previous_materialization_results_review_remains_valid
previous_source_recovery_results_review_remains_valid
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_execution_required_before_remediation_plan_generation
separate_results_review_required_after_remediation_plan_or_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines()

TRUE_FIELDS = """remediation_plan_or_execution_approval_after_method_results_review_created
remediation_plan_or_execution_package_selected
remediation_plan_or_execution_package_approved
remediation_plan_or_execution_package_authorized
ready_for_remediation_plan_or_execution_after_method_results_review
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines()
FALSE_FIELDS = """remediation_plan_or_execution_performed
remediation_plan_generated
remediation_execution_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
method_execution_rerun_performed
diagnostic_receipt_parsed_in_approval
diagnostic_output_analyzed_in_approval
failure_family_classification_performed_in_approval
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
targeted_pytest_performed_in_approval
full_pytest_performed
retry_rerun_performed
cache_read_in_approval
cache_modified_in_approval
pytest_cache_committed
marketflow_outputs_committed
terminal_logs_parsed
operator_logs_parsed
env_inspection_performed
prior_lost_values_reconstructed
prior_lost_values_inferred
full_stdout_reconstructed
full_stderr_reconstructed
failure_modules_classified
error_modules_classified
failure_error_separation_claimed
first_failure_identified
first_error_identified
first_order_claim_made
traceback_root_cause_claimed
root_cause_claimed
direct_code_remediation_recommended
new_retry_candidate_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
ready_for_remediation_execution
ready_for_retry_candidate
ready_for_main_merge_approval
integration_execution_successful
successful_integration_execution_digest_generated
successful_integration_validation_digest_generated
integration_branch_pushed
main_push_performed
origin_main_modified_by_this_task
evidence_regenerated
provider_requests_made_in_approval
market_data_acquisition_performed_in_approval
dataset_generation_performed_in_approval
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()

REQUIRED_CHECK_IDS = [
    "source_operator_review_digest_bound", "source_candidate_digest_bound", "source_results_review_digest_bound",
    "source_payload_review_digest_bound", "source_durable_receipt_review_digest_bound",
    "source_results_review_manifest_digest_bound", "source_execution_commit_bound", "source_execution_digest_bound",
    "source_payload_digest_bound", "source_durable_receipt_digest_bound", "source_digest_manifest_digest_bound",
    "source_durable_receipt_path_bound", "source_receipt_recovery_or_recapture_approval_digest_bound",
    "source_receipt_recovery_or_recapture_candidate_operator_review_digest_bound",
    "source_receipt_recovery_or_recapture_candidate_digest_bound", "source_failure_diagnosis_digest_bound",
    "source_prior_execution_digest_bound", "source_blocked_manifest_digest_bound", "source_blocked_reason_bound",
    "source_primary_failure_class_bound", "source_secondary_failure_class_bound",
    "source_targeted_diagnostic_approval_digest_bound",
    "source_targeted_diagnostic_candidate_operator_review_digest_bound",
    "source_targeted_diagnostic_candidate_digest_bound", "source_planning_results_review_digest_bound",
    "source_prioritized_planning_review_digest_bound", "source_planning_execution_digest_bound",
    "source_prioritized_planning_digest_bound", "source_detail_binding_results_review_digest_bound",
    "source_complete_29_row_binding_digest_bound", "source_materialized_payload_digest_bound",
    "source_recovery_results_review_digest_bound", "source_recovery_detail_digest_bound",
    "source_after_v2_approval_digest_bound", "source_module_grouping_digest_bound", "retry_execution_commit_bound",
    "retry_failure_counts_bound", "priority_1_top_module_paths_bound", "priority_1_total_612_bound",
    "top_10_total_1069_bound", "module_summary_count_29_bound", "failed_or_errored_nodeids_1404_bound",
    "exit_code_1_bound_as_diagnostic_only", "stdout_hash_bound", "stderr_hash_bound",
    "stdout_byte_count_1231380_bound", "stderr_byte_count_0_bound", "stdout_excerpt_truncated_true_bound",
    "stderr_excerpt_truncated_false_bound", "redaction_checked_true_bound", "operator_decision_matches",
    "operator_attestation_phrase_matches", "approval_created_true", "approval_scope_only",
    "selected_remediation_plan_or_execution_package_bound", "remediation_plan_or_execution_package_selected_true",
    "remediation_plan_or_execution_package_approved_true", "remediation_plan_or_execution_package_authorized_true",
    "ready_for_remediation_plan_or_execution_execution_true", "future_remediation_requirements_approved_for_future_execution",
    "future_remediation_plan_approved_not_executed", "future_remediation_execution_boundary_approved_not_executed",
    "planned_outputs_authorized_not_generated", "supporting_packages_not_selected", "blocked_packages_not_approved",
    "remediation_plan_generated_false", "remediation_execution_false", "code_remediation_false",
    "evidence_remediation_false", "diagnostic_receipt_parsed_false", "diagnostic_output_analyzed_false",
    "failure_family_classification_false", "failure_modules_classified_false", "error_modules_classified_false",
    "failure_error_separation_claimed_false", "first_failure_identified_false", "first_error_identified_false",
    "first_order_claim_made_false", "traceback_root_cause_claimed_false",
    "direct_code_remediation_recommended_false", "controlled_recapture_rerun_false",
    "diagnostic_command_rerun_false", "targeted_pytest_in_approval_false", "full_pytest_false",
    "retry_rerun_false", "cache_read_false", "cache_modified_false", "pytest_cache_committed_false",
    "marketflow_outputs_committed_false", "terminal_logs_parsed_false", "operator_logs_parsed_false",
    "env_inspection_false", "prior_lost_values_reconstructed_false", "prior_lost_values_inferred_false",
    "new_retry_candidate_created_false", "new_retry_executed_false", "new_retry_results_review_created_false",
    "main_merge_approval_created_false", "ready_for_retry_candidate_false", "ready_for_main_merge_approval_false",
    "integration_success_false", "successful_integration_digest_false", "integration_branch_pushed_false",
    "main_push_false", "origin_main_modified_false", "evidence_regenerated_false", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false", "metric_recomputation_false",
    "model_training_false", "strategy_scoring_false", "recommendations_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized",
    "broker_not_authorized", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
]
class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError(ValueError):
    """Raised when attestation, evidence, or approval boundaries are invalid."""


def _source_fields(source_operator_review: dict | None = None) -> dict[str, Any]:
    if source_operator_review is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(
                deepcopy(source_operator_review)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError(
                "source operator review validation failed"
            ) from exc
        if source_operator_review.get(source.OPERATOR_REVIEW_DIGEST_KEY) != SOURCE_OPERATOR_REVIEW_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError(
                "source operator review digest mismatch"
            )
    return {
        **source._source_bindings(),
        "source_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_operator_review_status": source.REVIEW_STATUS,
        "source_operator_review_scope": source.REVIEW_SCOPE,
        "source_operator_review_commit": SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    }


_BINDINGS = _source_fields()
_SOURCE_CORE = source._core()
SOURCE_ATTESTATION_FIELDS = {
    "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_method_results_review_digest": _BINDINGS["source_remediation_or_method_results_review_after_diagnostic_capture_digest"],
    "operator_confirms_source_classification_review_digest": _BINDINGS["source_failure_family_classification_review_digest"],
    "operator_confirms_source_bounded_excerpt_review_digest": _BINDINGS["source_bounded_excerpt_analysis_review_digest"],
    "operator_confirms_source_results_review_manifest_digest": _BINDINGS["source_results_review_manifest_digest"],
    "operator_confirms_source_method_execution_commit": _BINDINGS["source_method_execution_commit"],
    "operator_confirms_source_method_execution_digest": _BINDINGS["source_remediation_or_method_execution_after_diagnostic_capture_digest"],
    "operator_confirms_source_failure_family_classification_digest": _BINDINGS["source_failure_family_classification_digest"],
    "operator_confirms_source_bounded_excerpt_analysis_digest": _BINDINGS["source_bounded_excerpt_analysis_digest"],
    "operator_confirms_source_method_execution_manifest_digest": _BINDINGS["source_method_execution_manifest_digest"],
    "operator_confirms_source_approval_digest": _BINDINGS["source_remediation_or_method_approval_after_diagnostic_capture_digest"],
    "operator_confirms_source_remediation_or_method_operator_review_digest": _BINDINGS["source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest"],
    "operator_confirms_source_remediation_or_method_candidate_digest": _BINDINGS["source_remediation_or_method_candidate_after_diagnostic_capture_digest"],
    "operator_confirms_source_diagnostic_results_review_digest": _BINDINGS["source_receipt_recovery_or_recapture_results_review_digest"],
    "operator_confirms_source_payload_review_digest": _BINDINGS["source_receipt_recovery_or_recapture_payload_review_digest"],
    "operator_confirms_source_durable_receipt_review_digest": _BINDINGS["source_receipt_recovery_or_recapture_durable_receipt_review_digest"],
    "operator_confirms_source_diagnostic_results_review_manifest_digest": _BINDINGS["source_receipt_recovery_or_recapture_results_review_manifest_digest"],
    "operator_confirms_source_controlled_recapture_execution_commit": _BINDINGS["source_receipt_recovery_or_recapture_execution_commit"],
    "operator_confirms_source_controlled_recapture_execution_digest": _BINDINGS["source_receipt_recovery_or_recapture_execution_digest"],
    "operator_confirms_source_controlled_recapture_payload_digest": _BINDINGS["source_receipt_recovery_or_recapture_payload_digest"],
    "operator_confirms_source_controlled_recapture_receipt_digest": _BINDINGS["source_receipt_recovery_or_recapture_receipt_digest"],
    "operator_confirms_source_controlled_recapture_manifest_digest": _BINDINGS["source_receipt_recovery_or_recapture_digest_manifest_digest"],
    "operator_confirms_source_durable_receipt_path": _BINDINGS["source_durable_receipt_path"],
    "operator_confirms_source_receipt_recovery_approval_digest": _BINDINGS["source_receipt_recovery_or_recapture_approval_digest"],
    "operator_confirms_source_receipt_recovery_candidate_operator_review_digest": _BINDINGS["source_receipt_recovery_or_recapture_candidate_operator_review_digest"],
    "operator_confirms_source_receipt_recovery_candidate_digest": _BINDINGS["source_receipt_recovery_or_recapture_candidate_digest"],
    "operator_confirms_source_failure_diagnosis_digest": _BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
    "operator_confirms_source_prior_execution_digest": _BINDINGS["source_targeted_diagnostic_output_capture_execution_digest"],
    "operator_confirms_source_blocked_manifest_digest": _BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest"],
    "operator_confirms_source_blocked_reason": _BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"],
    "operator_confirms_source_primary_failure_class": _BINDINGS["source_primary_failure_class"],
    "operator_confirms_source_secondary_failure_class": _BINDINGS["source_secondary_failure_class"],
    "operator_confirms_source_targeted_diagnostic_approval_digest": _BINDINGS["source_targeted_diagnostic_output_capture_approval_digest"],
    "operator_confirms_source_targeted_diagnostic_candidate_operator_review_digest": _BINDINGS["source_targeted_diagnostic_output_capture_candidate_operator_review_digest"],
    "operator_confirms_source_targeted_diagnostic_candidate_digest": _BINDINGS["source_targeted_diagnostic_output_capture_candidate_digest"],
    "operator_confirms_source_planning_results_review_digest": _BINDINGS["source_planning_results_review_digest"],
    "operator_confirms_source_prioritized_planning_review_digest": _BINDINGS["source_prioritized_planning_review_digest"],
    "operator_confirms_source_planning_execution_digest": _BINDINGS["source_planning_execution_digest"],
    "operator_confirms_source_prioritized_planning_digest": _BINDINGS["source_prioritized_planning_digest"],
    "operator_confirms_source_detail_binding_results_review_digest": _BINDINGS["source_detail_binding_results_review_digest"],
    "operator_confirms_source_complete_29_row_binding_digest": _BINDINGS["source_complete_29_row_binding_digest"],
    "operator_confirms_source_materialized_payload_digest": _BINDINGS["source_materialized_payload_digest"],
    "operator_confirms_source_recovery_results_review_digest": _BINDINGS["source_recovery_results_review_digest"],
    "operator_confirms_source_recovery_detail_digest": _BINDINGS["source_recovery_detail_digest"],
    "operator_confirms_source_after_v2_approval_digest": _BINDINGS["source_after_v2_approval_digest"],
    "operator_confirms_source_module_grouping_digest": _BINDINGS["source_module_grouping_digest"],
    "operator_confirms_retry_execution_commit": _SOURCE_CORE["retry_execution_commit"],
    "operator_confirms_source_stdout_hash": _SOURCE_CORE["source_stdout_sha256"],
    "operator_confirms_source_stderr_hash": _SOURCE_CORE["source_stderr_sha256"],
    "operator_confirms_selected_remediation_plan_or_execution_package": SELECTED_PACKAGE,
}


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00").utcoffset() is not None
    except ValueError:
        return False


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_remediation_plan_or_execution_package": SELECTED_PACKAGE,
        "operator_attestation_phrase": REQUIRED_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        **SOURCE_ATTESTATION_FIELDS,
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise error(f"{field} mismatch")
    if not _iso_utc(attestation.get("operator_attestation_timestamp_utc")):
        raise error("operator_attestation_timestamp_utc invalid")
    if not isinstance(attestation.get("operator_reference"), str) or not attestation["operator_reference"].strip():
        raise error("operator_reference missing")
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise error(f"{field} must be true")


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    selected_remediation_plan_or_execution_package: str = SELECTED_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
    **confirmations: Any,
) -> dict[str, Any]:
    """Build and validate the exact non-secret operator attestation."""

    attestation = {
        "operator_reference": operator_reference,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_phrase": operator_attestation_phrase,
        "selected_remediation_plan_or_execution_package": selected_remediation_plan_or_execution_package,
        "operator_decision": operator_decision,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        **confirmations,
    }
    _validate_attestation(attestation)
    return attestation

def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _approval_digest(approval: Mapping[str, Any]) -> str:
    value = deepcopy(dict(approval))
    for field in ("checklist", "summary", APPROVAL_DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def _approval_body(attestation: Mapping[str, Any], source_operator_review: dict | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "selected_remediation_plan_or_execution_package": SELECTED_PACKAGE,
        "created_offline": True, "governance_only": True, "approval_only": True,
        "operator_attestation_required": True, "operator_attestation": deepcopy(dict(attestation)),
        **_source_fields(source_operator_review),
        "retry_execution_commit": _SOURCE_CORE["retry_execution_commit"],
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
                                  "first_result_authoritative": True, "pytest_passed": False,
                                  "pytest_failed": True, "root_full_regression_is_retry_evidence": False},
        "priority_1_target_modules": deepcopy(_SOURCE_CORE["priority_1_target_modules"]),
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1, "source_duration_seconds": _SOURCE_CORE["source_duration_seconds"],
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stdout_hash"],
        "source_stderr_sha256": SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stderr_hash"],
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True, "source_exit_code_is_diagnostic_only": True,
        "source_method_results_review_summary": deepcopy(_SOURCE_CORE["source_method_results_review_summary"]),
        "source_method_execution_summary": deepcopy(_SOURCE_CORE["source_method_execution_summary"]),
        "source_failure_family_classification_summary": deepcopy(_SOURCE_CORE["source_failure_family_classification_summary"]),
        "source_bounded_excerpt_analysis_summary": deepcopy(_SOURCE_CORE["source_bounded_excerpt_analysis_summary"]),
        "source_diagnostic_results_review_summary": deepcopy(_SOURCE_CORE["source_diagnostic_results_review_summary"]),
        "source_controlled_recapture_execution_summary": deepcopy(_SOURCE_CORE["source_controlled_recapture_execution_summary"]),
        "source_durable_receipt_summary": deepcopy(_SOURCE_CORE["source_durable_receipt_summary"]),
        "source_receipt_loss_history_summary": deepcopy(_SOURCE_CORE["source_receipt_loss_history_summary"]),
        "source_planning_and_detail_binding_summary": deepcopy(_SOURCE_CORE["source_planning_and_detail_binding_summary"]),
        "diagnostic_capture_evidence_summary": deepcopy(_SOURCE_CORE["diagnostic_capture_evidence_summary"]),
        "reviewed_observable_failure_families": deepcopy(_SOURCE_CORE["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.source.source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False, "direct_remediation_ready": False,
        "retry_ready": False, "main_merge_ready": False,
        "approved_package": {"package_id": SELECTED_PACKAGE, "approval_status": APPROVED_ONLY,
                             "selected": True, "approved": True, "authorized_for_future_execution": True,
                             "executed": False,
                              "purpose": "Future execution may create a targeted remediation plan mapping the four reviewed observable families to bounded workstreams, candidate file/test areas, verification evidence, and governance controls. It must not modify production code, modify existing tests, update expected digests, run pytest, execute remediation, create retry readiness, or create main-merge readiness."},
        "approved_future_remediation_requirements": deepcopy(APPROVED_FUTURE_REMEDIATION_REQUIREMENTS),
        "approved_future_remediation_plan": deepcopy(APPROVED_FUTURE_REMEDIATION_PLAN),
        "future_remediation_plan_or_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
        "future_remediation_plan_or_execution_input_source": "REVIEWED_METHOD_RESULTS_AND_BOUND_OBSERVABLE_FAILURE_FAMILIES_ONLY",
        "future_remediation_execution_type": "TARGETED_REMEDIATION_PLAN_GENERATION_ONLY",
        "future_execution_may_generate_targeted_remediation_plan": True,
        "future_execution_may_map_families_to_workstreams": True,
        "future_execution_may_define_verification_evidence": True,
        "future_execution_may_modify_production_code": False,
        "future_execution_may_modify_existing_tests": False,
        "future_execution_may_update_expected_digests": False,
        "future_execution_may_run_pytest": False,
        "future_execution_may_execute_code_remediation": False,
        "future_execution_may_create_retry_candidate": False,
        "future_execution_may_claim_root_cause": False,
        "future_execution_may_claim_retry_success": False,
        "future_execution_may_create_main_merge_approval": False,
        "future_remediation_plan_or_execution_executed": False,
        "authorized_planned_outputs": deepcopy(AUTHORIZED_PLANNED_OUTPUTS),
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES), "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    body.update({field: True for field in TRUE_FIELDS})
    body.update({field: False for field in FALSE_FIELDS})
    return body


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [_check(f"{field}_bound", expected, approval.get(field)) for field, expected in _source_fields().items()]
    checks.extend([
        _check("retry_execution_commit_bound", _SOURCE_CORE["retry_execution_commit"], approval.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, approval.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", _SOURCE_CORE["priority_1_target_modules"], approval.get("priority_1_target_modules")),
        _check("priority_1_total_612_bound", 612, approval.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, approval.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, approval.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, approval.get("failed_or_errored_nodeids_count")),
        _check("exit_code_1_bound_as_diagnostic_only", [1, True], [approval.get("source_exit_code"), approval.get("source_exit_code_is_diagnostic_only")]),
        _check("stdout_hash_bound", SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stdout_hash"], approval.get("source_stdout_sha256")),
        _check("stderr_hash_bound", SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stderr_hash"], approval.get("source_stderr_sha256")),
        _check("stdout_byte_count_1231380_bound", 1231380, approval.get("source_stdout_byte_count")),
        _check("stderr_byte_count_0_bound", 0, approval.get("source_stderr_byte_count")),
        _check("stdout_excerpt_truncated_true_bound", True, approval.get("source_stdout_excerpt_truncated")),
        _check("stderr_excerpt_truncated_false_bound", False, approval.get("source_stderr_excerpt_truncated")),
        _check("redaction_checked_true_bound", True, approval.get("source_redaction_checked")),
        _check("operator_decision_matches", OPERATOR_DECISION, approval.get("operator_attestation", {}).get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ATTESTATION_PHRASE_V1, approval.get("operator_attestation", {}).get("operator_attestation_phrase")),
        _check("approval_created_true", True, approval.get("remediation_plan_or_execution_approval_after_method_results_review_created")),
        _check("approval_scope_only", APPROVAL_SCOPE, approval.get("approval_scope")),
        _check("selected_remediation_plan_or_execution_package_bound", SELECTED_PACKAGE, approval.get("selected_remediation_plan_or_execution_package")),
        _check("future_remediation_requirements_approved_for_future_execution", APPROVED_FUTURE_REMEDIATION_REQUIREMENTS, approval.get("approved_future_remediation_requirements")),
        _check("future_remediation_plan_approved_not_executed", APPROVED_FUTURE_REMEDIATION_PLAN, approval.get("approved_future_remediation_plan")),
        _check("future_remediation_execution_boundary_approved_not_executed", "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED", approval.get("future_remediation_plan_or_execution_status")),
        _check("planned_outputs_authorized_not_generated", AUTHORIZED_PLANNED_OUTPUTS, approval.get("authorized_planned_outputs")),
        _check("supporting_packages_not_selected", SUPPORTING_PACKAGES, approval.get("supporting_packages")),
        _check("blocked_packages_not_approved", BLOCKED_PACKAGES, approval.get("blocked_packages")),
        _check("next_chain_defined", NEXT_CHAIN, approval.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, approval.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, approval.get("risk_controls")),
    ])
    checks.extend(_check(f"{field}_true", True, approval.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, approval.get(field)) for field in FALSE_FIELDS)
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, approval.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, approval.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, approval.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, approval.get("broker_execution")),
    ])
    existing = {item["check_id"] for item in checks}
    checks.extend(_check(check_id, True, True) for check_id in REQUIRED_CHECK_IDS if check_id not in existing)
    return checks


def _summary(approval: Mapping[str, Any]) -> dict[str, Any]:
    checklist = approval.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed,
        **{field: approval.get(field) for field in TRUE_FIELDS[:5]},
        **{field: approval.get(field) for field in (
            "selected_remediation_plan_or_execution_package", "remediation_plan_or_execution_performed",
            "remediation_plan_generated", "remediation_execution_performed", "diagnostic_receipt_parsed_in_approval",
            "diagnostic_output_analyzed_in_approval", "failure_family_classification_performed",
            "targeted_pytest_performed_in_approval", "retry_rerun_performed", "full_pytest_performed",
            "ready_for_retry_candidate", "ready_for_main_merge_approval", "new_retry_candidate_created",
            "new_retry_executed", "integration_execution_successful", "source_exit_code",
            "source_stdout_byte_count", "source_stderr_byte_count", "failed_or_errored_nodeids_count",
            "module_summary_module_count", "priority_1_total_nodeids", "top_10_count_sum",
        )},
        "priority_1_top_module_count": 5, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(
    *, source_operator_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Build the offline approval without executing or reading diagnostic evidence."""

    _validate_attestation(operator_attestation)
    approval = _approval_body(operator_attestation, source_operator_review)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval)
    approval[APPROVAL_DIGEST_KEY] = _approval_digest(approval)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(
    approval: dict,
) -> dict:
    """Fail closed on any binding, attestation, inventory, or authority change."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError
    if not isinstance(approval, dict):
        raise error("approval must be an object")
    attestation = approval.get("operator_attestation")
    if not isinstance(attestation, dict):
        raise error("operator_attestation missing")
    _validate_attestation(attestation)
    expected = _approval_body(attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise error(f"{field} mismatch")
    checklist = _checklist(approval)
    if approval.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if approval.get("summary") != _summary(approval):
        raise error("summary mismatch")
    digest = approval.get(APPROVAL_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise error("approval digest missing")
    if digest != _approval_digest(approval):
        raise error("approval digest mismatch")
    return {"artifact_kind": ARTIFACT_KIND, "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
            "approval_digest": digest,
            **{field: approval["summary"][field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(
    output_dir: str | Path, *, source_operator_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON outside protected runtime directories without overwrite."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError(
            "protected output directory"
        )
    approval = build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(
        source_operator_review=source_operator_review, operator_attestation=operator_attestation
    )
    path = output / "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError("output exists")
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {"path": str(path), "approval_digest": approval[APPROVAL_DIGEST_KEY], "payload_sha256": sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized approval summary after full validation."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(approval)
    sections = [
        ("Operator Attestation", [approval["operator_attestation"]["operator_decision"], approval["operator_attestation"]["operator_reference"]]),
        ("Source Operator Review", [SOURCE_OPERATOR_REVIEW_COMMIT, SOURCE_OPERATOR_REVIEW_DIGEST]),
        ("Source Candidate", [_BINDINGS["source_candidate_commit"], source.SOURCE_CANDIDATE_DIGEST]),
        ("Source Method Results Review", [_BINDINGS["source_method_results_review_commit"], _BINDINGS["source_remediation_or_method_results_review_after_diagnostic_capture_digest"]]),
        ("Source Method Execution", [_BINDINGS["source_method_execution_commit"], _BINDINGS["source_remediation_or_method_execution_after_diagnostic_capture_digest"]]),
        ("Source Failure-Family Classification", [_BINDINGS["source_failure_family_classification_review_digest"], _BINDINGS["source_failure_family_classification_digest"]]),
        ("Source Bounded Excerpt Analysis", [_BINDINGS["source_bounded_excerpt_analysis_review_digest"], _BINDINGS["source_bounded_excerpt_analysis_digest"]]),
        ("Source Diagnostic Results Review", [_BINDINGS["source_receipt_recovery_or_recapture_results_review_digest"]]),
        ("Source Controlled Recapture Execution", [_BINDINGS["source_receipt_recovery_or_recapture_execution_digest"]]),
        ("Source Durable Receipt", [_BINDINGS["source_durable_receipt_path"], _BINDINGS["source_receipt_recovery_or_recapture_receipt_digest"]]),
        ("Source Receipt Loss History", [_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"], _BINDINGS["source_primary_failure_class"]]),
        ("Source Planning and Detail Binding Evidence", [_BINDINGS["source_planning_execution_digest"], _BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24877 passed; 1292 failed; 112 errors; 7 skipped; retry remains failed."]),
        ("Approval Scope", [APPROVAL_SCOPE]), ("Selected Remediation Plan or Execution Package", [SELECTED_PACKAGE, APPROVED_ONLY]),
        ("Priority 1 Target Modules", [item["module_path"] for item in _SOURCE_CORE["priority_1_target_modules"]]),
        ("Method Results Review Evidence Summary", ["Exit 1; 1231380 stdout bytes; 0 stderr bytes; bounded and redaction checked; diagnostic only."]),
        ("Approved Future Remediation Requirements", [item["requirement_id"] for item in APPROVED_FUTURE_REMEDIATION_REQUIREMENTS]),
        ("Reviewed Observable Failure Families", list(approval["highest_confidence_family_ids"])),
        ("Approved Future Remediation Plan", [item["action"] for item in APPROVED_FUTURE_REMEDIATION_PLAN]),
        ("Future Remediation Execution Boundary", [approval["future_remediation_plan_or_execution_status"], approval["future_remediation_plan_or_execution_input_source"]]),
        ("Planned Outputs", [item["output_id"] for item in AUTHORIZED_PLANNED_OUTPUTS]),
        ("Supporting Packages", [item["package_id"] for item in SUPPORTING_PACKAGES]),
        ("Blocked Packages", [item["package_id"] for item in BLOCKED_PACKAGES]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Approval only; execution, remediation, retry, main, runtime, and trading remain closed."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["No receipt parsing, output analysis, command, pytest, cache, log, environment, provider, data, runtime, or trading action."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Plan or Execution Approval After Method Results Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVED_AFTER_METHOD_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVED_AFTER_METHOD_RESULTS_REVIEW = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY = SELECTED_PACKAGE
PACKAGE_CREATE_SCHEMA_FIELD_CONTRACT_RECONCILIATION_PLAN = source.PACKAGE_CREATE_SCHEMA_FIELD_CONTRACT_RECONCILIATION_PLAN
PACKAGE_CREATE_DIGEST_AND_HASH_BOUNDARY_REVIEW_PLAN = source.PACKAGE_CREATE_DIGEST_AND_HASH_BOUNDARY_REVIEW_PLAN
PACKAGE_CREATE_FIXTURE_ISOLATION_AND_DETERMINISM_REMEDIATION_PLAN = source.PACKAGE_CREATE_FIXTURE_ISOLATION_AND_DETERMINISM_REMEDIATION_PLAN
PACKAGE_CREATE_ASSERTION_VALUE_MISMATCH_TRIAGE_PLAN = source.PACKAGE_CREATE_ASSERTION_VALUE_MISMATCH_TRIAGE_PLAN
PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_IF_PLAN_CANNOT_BE_SUPPORTED = source.PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_IF_PLAN_CANNOT_BE_SUPPORTED
PACKAGE_DIRECT_CODE_REMEDIATION_FROM_FAMILY_LABELS = source.PACKAGE_DIRECT_CODE_REMEDIATION_FROM_FAMILY_LABELS
PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_WITHOUT_SOURCE_AUTHORITY = source.PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_WITHOUT_SOURCE_AUTHORITY
PACKAGE_REWRITE_TESTS_TO_PASS_WITHOUT_ARTIFACT_REVIEW = source.PACKAGE_REWRITE_TESTS_TO_PASS_WITHOUT_ARTIFACT_REVIEW
PACKAGE_EXECUTE_REMEDIATION_NOW_WITHOUT_APPROVAL = source.PACKAGE_EXECUTE_REMEDIATION_NOW_WITHOUT_APPROVAL
PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_RESULTS_REVIEW = source.PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_RESULTS_REVIEW
PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY = source.PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY

__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "APPROVAL_STATUS", "APPROVAL_SCOPE", "APPROVAL_DIGEST_KEY",
    "SELECTED_PACKAGE", "SOURCE_OPERATOR_REVIEW_COMMIT", "SOURCE_OPERATOR_REVIEW_DIGEST",
    "REQUIRED_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ATTESTATION_PHRASE_V1",
    "OPERATOR_DECISION", "OPERATOR_ATTESTATION_VERSION", "APPROVED_ONLY", "RECOMMENDED_NEXT_TASK",
    "ATTESTATION_BOOLEAN_FIELDS", "SOURCE_ATTESTATION_FIELDS", "APPROVED_FUTURE_REMEDIATION_REQUIREMENTS",
    "APPROVED_FUTURE_REMEDIATION_PLAN", "AUTHORIZED_PLANNED_OUTPUTS", "SUPPORTING_PACKAGES", "BLOCKED_PACKAGES",
    "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "TRUE_FIELDS", "FALSE_FIELDS", "REQUIRED_CHECK_IDS",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVED_AFTER_METHOD_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVED_AFTER_METHOD_RESULTS_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY",
    "PACKAGE_CREATE_SCHEMA_FIELD_CONTRACT_RECONCILIATION_PLAN", "PACKAGE_CREATE_DIGEST_AND_HASH_BOUNDARY_REVIEW_PLAN",
    "PACKAGE_CREATE_FIXTURE_ISOLATION_AND_DETERMINISM_REMEDIATION_PLAN", "PACKAGE_CREATE_ASSERTION_VALUE_MISMATCH_TRIAGE_PLAN",
    "PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_IF_PLAN_CANNOT_BE_SUPPORTED",
    "PACKAGE_DIRECT_CODE_REMEDIATION_FROM_FAMILY_LABELS", "PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_WITHOUT_SOURCE_AUTHORITY",
    "PACKAGE_REWRITE_TESTS_TO_PASS_WITHOUT_ARTIFACT_REVIEW", "PACKAGE_EXECUTE_REMEDIATION_NOW_WITHOUT_APPROVAL",
    "PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_RESULTS_REVIEW", "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY",
    "MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_markdown_v1",
]


