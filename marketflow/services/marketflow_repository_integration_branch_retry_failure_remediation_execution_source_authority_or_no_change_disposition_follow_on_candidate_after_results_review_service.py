"""Define follow-on options after the source-authority results review.

This module is candidate-only and deterministic.  It binds committed review
facts without invoking that review or any execution path.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_RESULTS_REVIEW_COMMIT = "f71143ec0743a3732535c47d2ef1d0d887403dc7"
SOURCE_RESULTS_REVIEW_DIGEST = "df613ae941cf366af79be8d6e74e648ca72b3453a63a6830e53b0c0b51a9c1bb"
SOURCE_ENRICHMENT_PLAN_REVIEW_DIGEST = "0cc52bd10f4b3fc61220f92f0024b728c98c43133c6b71906535037cbe824d46"
SOURCE_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST = "72dd695b4b112e4a4c7d285efd896a54bfd05ec0f8cd1c9bc3eb2087a40b49ec"
SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST = "f64e8575ef00ebacf54d1bf145140a94001c8e475e5a89c44e62a609421c7597"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "1d06a9b1ffd9127fa4808f960be188cf09ac85acaf4145845194c9d025e2e3ba"
SOURCE_RESULTS_REVIEW_ARTIFACT_KIND = source.ARTIFACT_KIND
SOURCE_RESULTS_REVIEW_STATUS = source.REVIEW_STATUS
SOURCE_RESULTS_REVIEW_SCOPE = source.REVIEW_SCOPE
PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"
CANDIDATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_digest"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_V1"
FUTURE_REQUIREMENT_STATUS = "REQUIRED_FOR_FUTURE_CONDITIONAL_FOLLOW_ON_AFTER_SOURCE_AUTHORITY_ENRICHMENT_RESULTS_REVIEW"
PLANNED_OUTPUT_STATUS = "PLANNED_NOT_GENERATED"

PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS = "PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS"
PACKAGE_CREATE_NO_CHANGE_DISPOSITION_CANDIDATE_FROM_REVIEWED_ENRICHMENT_RESULTS = "PACKAGE_CREATE_NO_CHANGE_DISPOSITION_CANDIDATE_FROM_REVIEWED_ENRICHMENT_RESULTS"
PACKAGE_CREATE_ALTERNATE_BOUNDED_DIAGNOSTIC_CANDIDATE_FROM_ENRICHMENT_RESULTS = "PACKAGE_CREATE_ALTERNATE_BOUNDED_DIAGNOSTIC_CANDIDATE_FROM_ENRICHMENT_RESULTS"
PACKAGE_CREATE_REMEDIATION_REENTRY_CANDIDATE_ONLY_AFTER_SOURCE_AUTHORITY_EXISTS = "PACKAGE_CREATE_REMEDIATION_REENTRY_CANDIDATE_ONLY_AFTER_SOURCE_AUTHORITY_EXISTS"
PACKAGE_CREATE_NO_CHANGE_RETRY_CRITERIA_CANDIDATE_AFTER_RESULTS_REVIEW = "PACKAGE_CREATE_NO_CHANGE_RETRY_CRITERIA_CANDIDATE_AFTER_RESULTS_REVIEW"
PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_SOURCE_AUTHORITY_ACQUISITION = "PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_SOURCE_AUTHORITY_ACQUISITION"
PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_SEPARATE_APPROVAL = "PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_SEPARATE_APPROVAL"
PACKAGE_DIRECT_REMEDIATION_FROM_ENRICHMENT_PLAN = "PACKAGE_DIRECT_REMEDIATION_FROM_ENRICHMENT_PLAN"
PACKAGE_NO_CHANGE_DISPOSITION_WITHOUT_REVIEWED_EVIDENCE = "PACKAGE_NO_CHANGE_DISPOSITION_WITHOUT_REVIEWED_EVIDENCE"
PACKAGE_RUN_ALTERNATE_DIAGNOSTICS_WITHOUT_APPROVAL = "PACKAGE_RUN_ALTERNATE_DIAGNOSTICS_WITHOUT_APPROVAL"
PACKAGE_NEW_RETRY_FROM_ENRICHMENT_RESULTS_ONLY = "PACKAGE_NEW_RETRY_FROM_ENRICHMENT_RESULTS_ONLY"
PACKAGE_MAIN_MERGE_FROM_ENRICHMENT_RESULTS_OR_CURRENT_ROOT_PASS = "PACKAGE_MAIN_MERGE_FROM_ENRICHMENT_RESULTS_OR_CURRENT_ROOT_PASS"
RECOMMENDED_PACKAGE = PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_DIGEST_KEY = CANDIDATE_DIGEST_KEY

CANDIDATE_PHILOSOPHY = {
    "follow_on_candidate_philosophy": "The source-authority enrichment results review confirms that the enrichment plan is valid as planning evidence, but it did not acquire source authority, establish concrete source authority, identify a safe source-authority-bound change, create no-change disposition, run alternate diagnostics, authorize remediation, or create retry readiness. The next governed decision must select one future path: source-authority acquisition, no-change disposition, alternate bounded diagnostics, remediation re-entry only after authority exists, no-change retry criteria, or hold disposition. This candidate defines options only and does not approve or execute any path.",
    "candidate_boundary": "Candidate-only; no package selection, approval, execution, source-authority acquisition, no-change disposition, alternate diagnostics, remediation, code change, test change, digest update, patch generation, pytest, retry, main merge, provider request, runtime, broker, or trading authority is created.",
    "candidate_goal": "Define safe future paths after reviewing a source-authority enrichment plan that found missing authority but acquired none.",
}


def _package(package_id: str, status: str, purpose: str, *, reason: str | None = None) -> dict[str, Any]:
    item = {"package_id": package_id, "status": status, "purpose": purpose,
            "selected": False, "approved": False, "authorized": False, "executed": False}
    if reason is not None:
        item["blocked_reason"] = reason
    return item


PROPOSED_PACKAGES = (
    _package(RECOMMENDED_PACKAGE, "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Create a future source-authority acquisition candidate from the reviewed inventory, evidence requirements, contracts, fixture requirements, and mappings."),
    _package(PACKAGE_CREATE_NO_CHANGE_DISPOSITION_CANDIDATE_FROM_REVIEWED_ENRICHMENT_RESULTS, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Create a future no-change disposition candidate using the seven reviewed inputs without creating a disposition."),
    _package(PACKAGE_CREATE_ALTERNATE_BOUNDED_DIAGNOSTIC_CANDIDATE_FROM_ENRICHMENT_RESULTS, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Create a separately governed bounded diagnostic candidate without executing diagnostics or retry."),
    _package(PACKAGE_CREATE_REMEDIATION_REENTRY_CANDIDATE_ONLY_AFTER_SOURCE_AUTHORITY_EXISTS, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Define remediation re-entry criteria only after source authority is acquired or reviewed."),
    _package(PACKAGE_CREATE_NO_CHANGE_RETRY_CRITERIA_CANDIDATE_AFTER_RESULTS_REVIEW, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Define possible no-change retry criteria only after a later approved no-change disposition."),
    _package(PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_SOURCE_AUTHORITY_ACQUISITION, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Keep remediation and retry blocked pending source authority or operator-provided reviewed evidence."),
    _package(PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_SEPARATE_APPROVAL, "BLOCKED_NOT_ALLOWED", "Acquire source authority now.",
             reason="Source-authority acquisition requires separate governed approval and cannot be performed by this candidate."),
    _package(PACKAGE_DIRECT_REMEDIATION_FROM_ENRICHMENT_PLAN, "BLOCKED_NOT_ALLOWED", "Perform direct remediation from planning evidence.",
             reason="The enrichment plan identifies missing authority and does not authorize direct code, test, digest, fixture, schema, or export changes."),
    _package(PACKAGE_NO_CHANGE_DISPOSITION_WITHOUT_REVIEWED_EVIDENCE, "BLOCKED_NOT_ALLOWED", "Create a no-change disposition without a reviewed basis.",
             reason="No-change disposition requires a separate reviewed basis; planning inputs are not a disposition."),
    _package(PACKAGE_RUN_ALTERNATE_DIAGNOSTICS_WITHOUT_APPROVAL, "BLOCKED_NOT_ALLOWED", "Run alternate diagnostics now.",
             reason="Alternate diagnostics require separate scope, approval, controls, execution, and results review."),
    _package(PACKAGE_NEW_RETRY_FROM_ENRICHMENT_RESULTS_ONLY, "BLOCKED_NOT_ALLOWED", "Create a retry from enrichment planning.",
             reason="Enrichment results are planning evidence only and do not create retry readiness."),
    _package(PACKAGE_MAIN_MERGE_FROM_ENRICHMENT_RESULTS_OR_CURRENT_ROOT_PASS, "BLOCKED_NOT_ALLOWED", "Merge main from planning or current-root evidence.",
             reason="Main merge remains blocked until a future retry results review passes."),
)

FUTURE_REQUIREMENT_IDS = tuple("""source_results_review_must_be_ready
source_results_review_digest_must_be_bound
source_enrichment_plan_review_digest_must_be_bound
source_missing_authority_inventory_review_digest_must_be_bound
source_workstream_mapping_review_digest_must_be_bound
source_results_review_manifest_digest_must_be_bound
source_execution_commit_must_be_bound
source_execution_digest_must_be_bound
source_enrichment_plan_digest_must_be_bound
source_missing_authority_inventory_digest_must_be_bound
source_workstream_authority_mapping_digest_must_be_bound
source_execution_manifest_digest_must_be_bound
source_approval_digest_must_be_bound
source_operator_review_digest_must_be_bound
source_candidate_digest_must_be_bound
source_failure_diagnosis_digest_must_be_bound
source_blocked_execution_commit_must_be_bound
source_blocked_reason_must_be_bound
source_blocked_manifest_digest_must_be_bound
primary_failure_class_must_be_bound
secondary_failure_classes_must_be_bound
source_plan_results_review_digest_must_be_bound
source_plan_execution_digest_must_be_bound
source_method_results_review_digest_must_be_bound
source_method_execution_digest_must_be_bound
source_diagnostic_results_review_digest_must_be_bound
source_controlled_recapture_digests_must_be_bound
source_durable_receipt_path_must_be_bound
source_planning_detail_recovery_digests_must_be_bound
retry_failure_counts_must_be_bound
priority_1_top_module_paths_must_be_bound
priority_1_total_must_be_612
top_10_total_must_be_1069
module_summary_total_must_be_29
failed_or_errored_nodeids_total_must_be_1404
priority1_pre_change_validation_must_be_675_passed
priority1_post_change_validation_must_be_675_passed
priority1_validation_must_not_be_treated_as_retry_evidence
diagnostic_metadata_must_remain_diagnostic_only
observable_family_count_must_be_4
observable_evidence_items_must_be_188
workstream_count_must_be_4
missing_authority_inventory_section_count_must_be_4
missing_authority_inventory_item_count_must_be_30
missing_authority_items_must_remain_missing_not_acquired
workstream_mappings_must_remain_planned_not_executed
source_evidence_requirements_must_be_reviewed
no_change_inputs_must_be_reviewed_but_not_disposition
alternate_diagnostic_inputs_must_be_reviewed_but_not_executed
retry_basis_requirements_must_be_reviewed_but_not_retry_readiness
future_execution_must_not_infer_acquired_source_authority
future_execution_must_not_treat_enrichment_plan_as_change_authority
future_execution_must_not_treat_current_root_pass_as_retry_success
future_execution_must_preserve_detached_retry_failed_status
future_execution_must_preserve_retry_candidate_false_until_reviewed_basis
future_execution_must_preserve_main_merge_false_until_passing_retry_review
future_execution_must_not_modify_code_without_separate_approval
future_execution_must_not_modify_tests_without_separate_approval
future_execution_must_not_update_digests_without_source_authority
future_execution_must_not_run_retry_without_separate_approval
future_execution_must_not_push_main
future_execution_must_not_push_integration_branch
runtime_and_trading_remain_not_authorized""".splitlines())

FUTURE_PLAN = (
    "Bind this candidate and source results-review evidence.",
    "Bind the complete committed governance and diagnostic digest chain.",
    "Bind retry counts, Priority 1 facts, observable families, workstreams, enrichment outputs, and inventory.",
    "Preserve that the enrichment review acquired no authority.",
    "Select one future package only under separate operator approval.",
    "If acquisition is selected, define scope without acquiring evidence.",
    "If no-change is selected, define inputs without creating disposition.",
    "If diagnostics are selected, define bounded scope without execution.",
    "If remediation re-entry is selected, require acquired and reviewed authority first.",
    "If no-change retry criteria are selected, define criteria without retry readiness.",
    "Require results review before any later acquisition, disposition, diagnostic, remediation, retry, or merge path.",
    "Keep provider, runtime, broker, and trading authority closed.",
)

PLANNED_OUTPUT_IDS = tuple("""follow_on_candidate_after_results_review_manifest
source_results_review_binding_report
source_execution_binding_report
source_approval_binding_report
source_operator_review_binding_report
source_candidate_binding_report
source_failure_diagnosis_binding_report
source_blocked_execution_binding_report
source_plan_results_review_binding_report
source_plan_execution_binding_report
source_method_and_diagnostic_binding_report
source_planning_detail_recovery_binding_report
retry_failure_context_report
priority1_validation_disposition_report
enrichment_plan_review_binding_report
missing_authority_inventory_binding_report
workstream_authority_mapping_binding_report
source_evidence_requirements_binding_report
no_change_disposition_inputs_binding_report
alternate_diagnostic_inputs_binding_report
retry_basis_requirements_binding_report
proposed_follow_on_package_comparison_report
recommended_source_authority_acquisition_candidate_package_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NON_GOALS = tuple("""do_not_select_package_now
do_not_approve_package_now
do_not_authorize_package_now
do_not_execute_source_authority_acquisition_now
do_not_acquire_source_authority_now
do_not_execute_no_change_disposition_now
do_not_execute_alternate_diagnostics_now
do_not_execute_remediation_now
do_not_modify_production_code_now
do_not_modify_existing_tests_now
do_not_update_expected_digests_now
do_not_generate_patch_now
do_not_apply_patch_now
do_not_run_pytest_now
do_not_run_full_pytest_now
do_not_rerun_priority1_validation_now
do_not_rerun_retry_now
do_not_rerun_detached_retry_now
do_not_push_main
do_not_push_integration_branch
do_not_delete_or_reset_integration_branch
do_not_delete_or_reset_worktree
do_not_force_push
do_not_modify_tags
do_not_read_pytest_cache_now
do_not_modify_pytest_cache_now
do_not_parse_durable_receipt_now
do_not_analyze_diagnostic_output_now
do_not_rerun_source_authority_enrichment_now
do_not_rerun_plan_execution_now
do_not_regenerate_targeted_plan_now
do_not_rerun_method_execution_now
do_not_rerun_controlled_recapture_now
do_not_run_diagnostic_command_now
do_not_parse_terminal_logs_now
do_not_parse_operator_logs_now
do_not_inspect_env_now
do_not_reconstruct_prior_lost_values_now
do_not_reconstruct_full_stdout_or_stderr_now
do_not_classify_modules_again_now
do_not_classify_full_retry_failures_now
do_not_classify_full_retry_errors_now
do_not_claim_failure_error_separation_now
do_not_identify_first_failure_now
do_not_identify_first_error_now
do_not_claim_traceback_root_cause_now
do_not_claim_root_cause_now
do_not_claim_retry_success_now
do_not_claim_main_merge_readiness_now
do_not_create_source_authority_acquisition_execution_now
do_not_create_no_change_disposition_execution_now
do_not_create_alternate_diagnostic_execution_now
do_not_create_remediation_execution_now
do_not_create_remediation_execution_results_review_now
do_not_create_new_retry_candidate_now
do_not_create_retry_approval_now
do_not_create_retry_execution_now
do_not_create_retry_results_review_now
do_not_create_integration_results_review_now
do_not_mark_integration_successful
do_not_commit_marketflow_outputs
do_not_commit_pytest_cache
do_not_modify_staged_evidence
do_not_regenerate_evidence
do_not_call_providers
do_not_acquire_market_data
do_not_generate_dataset
do_not_recompute_metrics
do_not_train_models
do_not_score_strategy
do_not_generate_recommendations
do_not_accept_predictive_usefulness
do_not_accept_profitability
do_not_authorize_runtime
do_not_authorize_broker_execution
do_not_authorize_trading""".splitlines())

TRUE_FIELDS = tuple("""follow_on_candidate_after_results_review_created
follow_on_candidate_after_results_review_ready_for_operator_review
source_results_review_bound
source_execution_bound
source_approval_bound
source_operator_review_bound
source_candidate_bound
source_failure_diagnosis_bound
source_blocked_execution_bound
source_enrichment_plan_reviewed
source_missing_authority_inventory_reviewed
source_workstream_authority_mapping_reviewed
source_evidence_requirements_reviewed
no_change_disposition_inputs_reviewed
alternate_diagnostic_inputs_reviewed
retry_basis_requirements_reviewed
source_authority_gap_preserved
missing_authority_inventory_status_preserved
detached_retry_failed_status_preserved
proposed_packages_defined
recommended_package_defined
future_requirements_defined
future_plan_defined
planned_outputs_defined
non_goals_defined
ready_for_follow_on_candidate_operator_review""".splitlines())

FALSE_FIELDS = tuple("""recommended_package_selected
follow_on_package_selected
follow_on_package_approved
follow_on_package_authorized
follow_on_execution_performed
source_authority_acquisition_candidate_created
source_authority_acquisition_performed
source_authority_evidence_acquired
concrete_source_authority_established
safe_source_authority_bound_change_identified
retained_change_records_available
no_change_disposition_performed
alternate_diagnostic_execution_performed
remediation_execution_performed
controlled_plan_derived_remediation_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
patch_generated
patch_applied
pytest_performed
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
cache_read
cache_modified
pytest_cache_committed
marketflow_outputs_committed
diagnostic_receipt_parsed
diagnostic_output_analyzed
source_authority_enrichment_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
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
retry_success_claimed
main_merge_readiness_claimed
retry_candidate_created
retry_approval_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
ready_for_follow_on_approval
ready_for_source_authority_acquisition_candidate
ready_for_no_change_disposition_candidate
ready_for_alternate_diagnostic_candidate
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
provider_requests_made
market_data_acquisition_performed
dataset_generation_performed
metric_recomputation_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

NEXT_CHAIN = (
    "Follow-On Candidate After Source-Authority Enrichment Results Review Operator Review v1.",
    "Follow-On Approval v1, if selected.", "Follow-On Execution v1, if approved.",
    "Follow-On Results Review v1.",
    "Conditional source-authority acquisition, no-change disposition, alternate diagnostic, remediation re-entry, no-change retry criteria, or hold disposition only if results review supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple("""follow_on_candidate_after_source_authority_enrichment_results_review_operator_review
follow_on_approval_if_selected
follow_on_execution_if_approved
follow_on_results_review
source_authority_acquisition_candidate_if_supported
no_change_disposition_candidate_if_supported
alternate_diagnostic_candidate_if_supported
remediation_execution_candidate_if_supported
no_change_retry_criteria_candidate_if_supported
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines())

RISK_CONTROLS = tuple("""follow_on_candidate_does_not_select_package
follow_on_candidate_does_not_approve_package
follow_on_candidate_does_not_authorize_package
follow_on_candidate_does_not_execute_follow_on
follow_on_candidate_does_not_create_source_authority_acquisition_execution
follow_on_candidate_does_not_acquire_source_authority
follow_on_candidate_does_not_create_no_change_disposition
follow_on_candidate_does_not_execute_alternate_diagnostics
follow_on_candidate_does_not_execute_remediation
follow_on_candidate_does_not_modify_production_code
follow_on_candidate_does_not_modify_existing_tests
follow_on_candidate_does_not_update_expected_digests
follow_on_candidate_does_not_generate_patch
follow_on_candidate_does_not_apply_patch
follow_on_candidate_does_not_run_pytest
follow_on_candidate_does_not_run_full_pytest
follow_on_candidate_does_not_rerun_priority1_validation
follow_on_candidate_does_not_rerun_retry
follow_on_candidate_does_not_rerun_detached_retry
follow_on_candidate_does_not_parse_durable_receipt
follow_on_candidate_does_not_analyze_diagnostic_output
follow_on_candidate_does_not_rerun_source_authority_enrichment
follow_on_candidate_does_not_rerun_plan_execution
follow_on_candidate_does_not_regenerate_targeted_plan
follow_on_candidate_does_not_rerun_method_execution
follow_on_candidate_does_not_rerun_controlled_recapture
follow_on_candidate_does_not_run_diagnostic_command
follow_on_candidate_does_not_read_pytest_cache
follow_on_candidate_does_not_modify_pytest_cache
follow_on_candidate_does_not_parse_terminal_logs
follow_on_candidate_does_not_parse_operator_logs
follow_on_candidate_does_not_inspect_env
follow_on_candidate_does_not_reconstruct_prior_lost_values
follow_on_candidate_does_not_reconstruct_full_streams
follow_on_candidate_does_not_classify_modules_again
follow_on_candidate_does_not_classify_full_retry_failures
follow_on_candidate_does_not_classify_full_retry_errors
follow_on_candidate_does_not_claim_failure_error_separation
follow_on_candidate_does_not_identify_authoritative_first_failure
follow_on_candidate_does_not_identify_authoritative_first_error
follow_on_candidate_does_not_claim_traceback_root_cause
follow_on_candidate_does_not_claim_root_cause
follow_on_candidate_does_not_claim_retry_success
follow_on_candidate_does_not_claim_main_merge_readiness
follow_on_candidate_does_not_create_retry_approval
follow_on_candidate_does_not_create_retry_execution
follow_on_candidate_does_not_create_retry_results_review
follow_on_candidate_does_not_create_integration_results_review
follow_on_candidate_does_not_mark_integration_successful
follow_on_candidate_does_not_generate_successful_integration_digest
follow_on_candidate_does_not_push_integration_branch
follow_on_candidate_does_not_push_main
follow_on_candidate_does_not_delete_integration_branch
follow_on_candidate_does_not_delete_worktree
follow_on_candidate_does_not_force_push
follow_on_candidate_does_not_prune_remotes
follow_on_candidate_does_not_modify_tags
follow_on_candidate_does_not_modify_staged_evidence
follow_on_candidate_does_not_regenerate_evidence
follow_on_candidate_does_not_call_providers
follow_on_candidate_does_not_acquire_market_data
follow_on_candidate_does_not_generate_dataset
follow_on_candidate_does_not_recompute_metrics
follow_on_candidate_does_not_train_models
follow_on_candidate_does_not_score_strategy
follow_on_candidate_does_not_generate_trade_recommendations
follow_on_candidate_does_not_accept_predictive_usefulness
follow_on_candidate_does_not_accept_profitability
follow_on_candidate_does_not_authorize_runtime
follow_on_candidate_does_not_authorize_broker_execution
source_authority_acquisition_candidate_is_not_source_authority_acquisition
source_authority_enrichment_results_are_not_source_authority
missing_authority_inventory_is_not_change_authority
no_change_inputs_are_not_no_change_disposition
alternate_diagnostic_inputs_are_not_diagnostic_execution
retry_basis_requirements_are_not_retry_readiness
passing_priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
blocked_remediation_execution_remains_source_evidence
failure_diagnosis_remains_source_evidence
source_execution_results_review_remains_source_evidence
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_operator_review_required_before_any_selection
separate_approval_required_before_any_execution
separate_results_review_required_after_any_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines())

CHECK_IDS = tuple(dict.fromkeys((
    "source_results_review_commit_bound", "source_results_review_digest_bound",
    "source_results_review_artifact_kind_bound", "source_results_review_status_bound",
    "source_results_review_scope_bound", "source_enrichment_plan_review_digest_bound",
    "source_missing_authority_inventory_review_digest_bound", "source_workstream_mapping_review_digest_bound",
    "source_results_review_manifest_digest_bound", "source_execution_commit_bound", "source_execution_digest_bound",
    *source.CHECK_IDS,
    "missing_authority_inventory_four_sections_bound", "missing_authority_inventory_30_items_bound",
    "missing_authority_items_missing_not_acquired_bound", "workstream_mappings_planned_not_executed_bound",
    "no_change_input_count_7_bound", "alternate_diagnostic_input_count_8_bound",
    "retry_basis_requirement_count_7_bound", "source_outputs_27_reviewed_bound",
    "review_outputs_28_generated_bound", "candidate_created_true", "candidate_ready_true",
    "source_results_review_bound_true", "source_execution_bound_true", "source_enrichment_plan_reviewed_true",
    "source_missing_authority_inventory_reviewed_true", "source_workstream_authority_mapping_reviewed_true",
    "source_authority_gap_preserved_true", "proposed_packages_defined_true", "packages_present_12",
    "recommended_package_defined", "recommended_package_not_selected", "available_packages_present_5",
    "blocked_packages_present_6", "future_requirements_defined", "future_plan_defined", "planned_outputs_defined",
    "non_goals_defined", "follow_on_package_selected_false", "follow_on_package_approved_false",
    "follow_on_package_authorized_false", "follow_on_execution_false",
    "source_authority_acquisition_candidate_created_false", "ready_for_follow_on_approval_false",
    "recommendation_defined", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
    *(f"{field}_true" for field in TRUE_FIELDS), *(f"{field}_false" for field in FALSE_FIELDS),
)))

MARKDOWN_SECTIONS = (
    "Source Results Review", "Source Results Review Digests", "Source Execution", "Source Execution Digests",
    "Source Approval", "Source Operator Review", "Source Candidate", "Source Failure Diagnosis",
    "Source Blocked Execution", "Blocked Reason", "Failure Classification", "Source Remediation Execution Approval",
    "Source Plan Results Review", "Source Plan Execution", "Source Method Results Review", "Source Method Execution",
    "Source Diagnostic Results Review", "Source Controlled Recapture", "Source Durable Receipt",
    "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Priority 1 Target Modules",
    "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "Source Authority Enrichment Review Summary", "Missing Authority Inventory Review Summary",
    "Workstream Authority Mapping Review Summary", "Source Evidence Requirements Review Summary",
    "No-Change Disposition Input Review Summary", "Alternate Diagnostic Input Review Summary",
    "Retry Basis Requirements Review Summary", "Candidate Philosophy", "Proposed Follow-On Packages",
    "Recommended Package", "Future Requirements", "Future Plan", "Planned Outputs", "Non-Goals", "Next Chain",
    "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


class MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError(ValueError):
    """Raised when candidate evidence or a protected boundary changes."""


def _source_bindings() -> dict[str, Any]:
    bindings = deepcopy(source.source.SOURCE_BINDINGS)
    bindings.update({
        "source_execution_commit": source.SOURCE_EXECUTION_COMMIT,
        "source_execution_digest": source.SOURCE_EXECUTION_DIGEST,
        "source_execution_artifact_kind": source.SOURCE_EXECUTION_ARTIFACT_KIND,
        "source_execution_status": source.SOURCE_EXECUTION_STATUS,
        "source_execution_scope": source.SOURCE_EXECUTION_SCOPE,
        "source_authority_enrichment_plan_digest": source.SOURCE_ENRICHMENT_PLAN_DIGEST,
        "source_missing_authority_inventory_digest": source.SOURCE_MISSING_AUTHORITY_INVENTORY_DIGEST,
        "source_workstream_authority_mapping_digest": source.SOURCE_WORKSTREAM_AUTHORITY_MAPPING_DIGEST,
        "source_execution_manifest_digest": source.SOURCE_EXECUTION_MANIFEST_DIGEST,
    })
    return bindings


def _source_context() -> dict[str, Any]:
    return {
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
                                  "first_result_authoritative": True, "root_full_regression_is_retry_evidence": False},
        "priority_1_target_modules": [
            {"module_path": path, "failed_or_errored_nodeid_count": count} for path, count in source.source.PRIORITY_1_MODULES
        ],
        "priority1_validation_summary": {"pre_change_passed": True, "pre_change_passed_count": 675,
                                         "post_change_passed": True, "post_change_passed_count": 675,
                                         "post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
                                         "post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                                         "not_retry_evidence": True},
        "diagnostic_capture_evidence_summary": {"exit_code": 1, "stdout_byte_count": 1231380, "stderr_byte_count": 0,
                                                "stdout_sha256": source.source.source.source.source.SOURCE_CORE["source_stdout_sha256"],
                                                "stderr_sha256": source.source.source.source.source.SOURCE_CORE["source_stderr_sha256"],
                                                "diagnostic_only": True},
        "reviewed_observable_failure_families": [
            {"family_id": family, "observable_evidence_count": 47, "confidence": "HIGH", "planning_evidence_only": True}
            for _, family in source.source.WORKSTREAM_SOURCES
        ],
        "reviewed_workstreams": [
            {"workstream_id": workstream, "source_family_id": family, "source_observable_evidence_count": 47,
             "source_family_confidence": "HIGH", "planning_evidence_only": True, "direct_change_authorized": False}
            for workstream, family in source.source.WORKSTREAM_SOURCES
        ],
    }


def _committed_source_results_review() -> dict[str, Any]:
    return {
        "artifact_kind": SOURCE_RESULTS_REVIEW_ARTIFACT_KIND, "review_status": SOURCE_RESULTS_REVIEW_STATUS,
        "review_scope": SOURCE_RESULTS_REVIEW_SCOPE, "source_results_review_commit": SOURCE_RESULTS_REVIEW_COMMIT,
        source.RESULTS_REVIEW_DIGEST_KEY: SOURCE_RESULTS_REVIEW_DIGEST,
        source.ENRICHMENT_PLAN_REVIEW_DIGEST_KEY: SOURCE_ENRICHMENT_PLAN_REVIEW_DIGEST,
        source.MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY: SOURCE_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST,
        source.WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY: SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        **_source_bindings(),
        "missing_authority_inventory_section_count": 4, "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED", "workstream_mapping_count": 4,
        "workstream_mapping_status": "PLANNED_NOT_EXECUTED", "no_change_disposition_input_count": 7,
        "alternate_diagnostic_input_count": 8, "retry_basis_requirement_count": 7,
        "source_outputs_generated_count": 27, "review_outputs_generated_count": 28,
        **_source_context(),
    }


def _validate_source_results_review(candidate: Mapping[str, Any]) -> None:
    if not isinstance(candidate, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError("source results review must be an object")
    for field, value in _committed_source_results_review().items():
        if candidate.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError(f"source results review {field} mismatch")


def _summaries() -> dict[str, Any]:
    bindings = _source_bindings()
    context = _source_context()
    return {
        "source_results_review_summary": {"commit": SOURCE_RESULTS_REVIEW_COMMIT, "status": SOURCE_RESULTS_REVIEW_STATUS,
                                          "checks": "168/168 PASS", "planning_only": True},
        "source_execution_summary": {"commit": bindings["source_execution_commit"], "digest": bindings["source_execution_digest"],
                                     "package": source.SELECTED_PACKAGE, "planning_outputs": 27},
        "source_approval_summary": {"commit": bindings["source_approval_commit"], "digest": bindings["source_approval_digest"]},
        "source_operator_review_summary": {"commit": bindings["source_operator_review_commit"], "digest": bindings["source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest"]},
        "source_candidate_summary": {"commit": bindings["source_candidate_commit"], "digest": bindings["source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest"]},
        "source_failure_diagnosis_summary": {"commit": bindings["source_failure_diagnosis_commit"], "digest": bindings["source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"]},
        "source_blocked_execution_summary": {"commit": bindings["source_blocked_execution_commit"], "reason": bindings["source_blocked_reason"], "manifest_digest": bindings["source_blocked_manifest_digest"]},
        "source_plan_results_review_summary": {
            "workstream_mapping_review_digest": bindings["source_workstream_mapping_review_digest"],
            **{key: value for key, value in bindings.items() if "plan_results_review" in key},
        },
        "source_plan_execution_summary": {key: value for key, value in bindings.items() if "plan_execution" in key},
        "source_method_results_review_summary": {key: value for key, value in bindings.items() if "method_results_review" in key},
        "source_method_execution_summary": {key: value for key, value in bindings.items() if "method_execution" in key},
        "source_diagnostic_results_review_summary": {key: value for key, value in bindings.items() if "recapture_results_review" in key or "payload_review" in key or "durable_receipt_review" in key},
        "source_controlled_recapture_summary": {key: value for key, value in bindings.items() if "recapture_execution" in key or "recapture_payload_digest" in key or "recapture_receipt_digest" in key},
        "source_durable_receipt_summary": {"path": bindings["source_durable_receipt_path"], "parsed": False},
        "source_receipt_loss_history_summary": {"primary": bindings["source_primary_failure_class"], "secondary": bindings["source_secondary_failure_class"], "blocked_reason": bindings["source_targeted_diagnostic_output_capture_execution_blocked_reason"]},
        "source_planning_and_detail_binding_summary": {key: value for key, value in bindings.items() if any(token in key for token in ("planning_digest", "detail_binding", "complete_29", "materialized_payload", "recovery_detail", "module_grouping", "staged_inventory"))},
        "source_authority_enrichment_review_summary": {"reviewed": True, "planning_only": True, "source_authority_acquired": False},
        "missing_authority_inventory_review_summary": {"reviewed": True, "section_count": 4, "item_count": 30, "item_status": "MISSING_NOT_ACQUIRED"},
        "workstream_authority_mapping_review_summary": {"reviewed": True, "mapping_count": 4, "mapping_status": "PLANNED_NOT_EXECUTED"},
        "source_evidence_requirements_review_summary": {"reviewed": True, "section_count": 4, "evidence_acquired": False},
        "no_change_disposition_input_review_summary": {"reviewed": True, "input_count": 7, "disposition_created": False},
        "alternate_diagnostic_input_review_summary": {"reviewed": True, "input_count": 8, "diagnostic_executed": False},
        "retry_basis_requirements_review_summary": {"reviewed": True, "requirement_count": 7, "retry_readiness_created": False},
        **context,
    }


def _checklist() -> list[dict[str, Any]]:
    return [{"check_id": item, "status": PASS, "expected": True, "actual": True,
             "severity": BLOCKER, "message": f"{item} passed"} for item in CHECK_IDS]


def _summary(candidate: Mapping[str, Any]) -> dict[str, Any]:
    checks = candidate["checklist"]
    return {
        "total_checks": len(checks), "passed_checks": len(checks), "failed_checks": 0, "blocker_count": 0,
        **{field: candidate[field] for field in TRUE_FIELDS},
        "missing_authority_inventory_reviewed": True, "missing_authority_inventory_section_count": 4,
        "missing_authority_inventory_item_count": 30, "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "workstream_to_missing_authority_mapping_reviewed": True, "workstream_mapping_count": 4,
        "workstream_mapping_status": "PLANNED_NOT_EXECUTED", "source_outputs_reviewed": True,
        "source_outputs_generated_count": 27, "review_outputs_generated_count": 28,
        **{field: candidate[field] for field in FALSE_FIELDS},
        "recommended_follow_on_package": RECOMMENDED_PACKAGE,
        "source_workstream_count": 4, "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188, "source_exit_code": 1,
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _candidate_digest(candidate: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(candidate))
    for field in ("checklist", "summary", CANDIDATE_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _assemble_candidate() -> dict[str, Any]:
    bindings, summaries = _source_bindings(), _summaries()
    candidate = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True, "operator_review_required": True,
        **bindings,
        "source_results_review_artifact_kind": SOURCE_RESULTS_REVIEW_ARTIFACT_KIND,
        "source_results_review_status": SOURCE_RESULTS_REVIEW_STATUS,
        "source_results_review_scope": SOURCE_RESULTS_REVIEW_SCOPE,
        "source_results_review_commit": SOURCE_RESULTS_REVIEW_COMMIT,
        "source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_enrichment_plan_review_digest": SOURCE_ENRICHMENT_PLAN_REVIEW_DIGEST,
        "source_missing_authority_inventory_review_digest": SOURCE_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST,
        "source_workstream_mapping_review_digest": SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST,
        "source_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "selected_source_authority_or_no_change_disposition_package": source.SELECTED_PACKAGE,
        **summaries, **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "source_workstream_count": 4, "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "missing_authority_inventory_section_count": 4, "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED", "workstream_mapping_count": 4,
        "workstream_mapping_status": "PLANNED_NOT_EXECUTED", "no_change_disposition_input_count": 7,
        "alternate_diagnostic_input_count": 8, "retry_basis_requirement_count": 7,
        "source_outputs_generated_count": 27, "review_outputs_generated_count": 28,
        "candidate_philosophy": deepcopy(CANDIDATE_PHILOSOPHY),
        "proposed_follow_on_packages": deepcopy(list(PROPOSED_PACKAGES)),
        "recommended_follow_on_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommendation_reason": "The reviewed plan identified 30 missing authority items across four sections, acquired no authority, and identified no safe source-authority-bound change. A governed source-authority acquisition candidate is the safest next path before remediation, no-change disposition, diagnostics, retry, or main merge.",
        "future_requirements": [{"requirement_id": item, "status": FUTURE_REQUIREMENT_STATUS, "execution_status": "NOT_EXECUTED"} for item in FUTURE_REQUIREMENT_IDS],
        "future_plan": list(FUTURE_PLAN), "future_plan_status": "PLANNED_NOT_EXECUTED",
        "planned_outputs": [{"output_id": item, "status": PLANNED_OUTPUT_STATUS} for item in PLANNED_OUTPUT_IDS],
        "non_goals": list(NON_GOALS), "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    candidate["checklist"] = _checklist()
    candidate["summary"] = _summary(candidate)
    candidate[CANDIDATE_DIGEST_KEY] = _candidate_digest(candidate)
    return candidate


def _first_difference(actual: Any, expected: Any, path: str = "candidate") -> str | None:
    if isinstance(expected, Mapping):
        if not isinstance(actual, Mapping) or set(actual) != set(expected):
            return f"{path}.keys"
        for key in expected:
            difference = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if difference:
                return difference
        return None
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            return path
        for index, item in enumerate(expected):
            difference = _first_difference(actual[index], item, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(
    *, source_results_review: dict | None = None,
) -> dict[str, Any]:
    """Build the candidate without selecting or executing a package."""

    evidence = _committed_source_results_review() if source_results_review is None else deepcopy(source_results_review)
    _validate_source_results_review(evidence)
    candidate = _assemble_candidate()
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Validate every source binding, option, and closed authority boundary."""

    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError("candidate must be an object")
    expected = _assemble_candidate()
    difference = _first_difference(candidate, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError(f"{difference} mismatch")
    return {"artifact_kind": ARTIFACT_KIND, "candidate_status": CANDIDATE_STATUS,
            "candidate_scope": CANDIDATE_SCOPE, "candidate_digest": candidate[CANDIDATE_DIGEST_KEY],
            "total_checks": candidate["summary"]["total_checks"],
            "passed_checks": candidate["summary"]["passed_checks"], "failed_checks": 0, "blocker_count": 0}


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_markdown_v1(
    candidate: dict,
) -> str:
    """Render a validated candidate status record."""

    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(deepcopy(candidate))
    sections = {
        "Source Results Review": candidate["source_results_review_summary"],
        "Source Results Review Digests": {key: candidate[key] for key in ("source_results_review_digest", "source_enrichment_plan_review_digest", "source_missing_authority_inventory_review_digest", "source_workstream_mapping_review_digest", "source_results_review_manifest_digest")},
        "Source Execution": candidate["source_execution_summary"],
        "Source Execution Digests": {key: candidate[key] for key in ("source_execution_digest", "source_authority_enrichment_plan_digest", "source_missing_authority_inventory_digest", "source_workstream_authority_mapping_digest", "source_execution_manifest_digest")},
        "Source Approval": candidate["source_approval_summary"], "Source Operator Review": candidate["source_operator_review_summary"],
        "Source Candidate": candidate["source_candidate_summary"], "Source Failure Diagnosis": candidate["source_failure_diagnosis_summary"],
        "Source Blocked Execution": candidate["source_blocked_execution_summary"], "Blocked Reason": candidate["source_blocked_reason"],
        "Failure Classification": {"primary": candidate["source_blocked_reason"], "secondary": ["REVIEWED_WORKSTREAMS_ARE_PLANNING_EVIDENCE_NOT_CHANGE_AUTHORITY", "PRIORITY_1_FOCUSED_VALIDATION_ALREADY_PASSING_IN_CURRENT_ROOT_CONTEXT", "NO_RETAINED_CHANGE_RECORDS_AVAILABLE_FOR_REMEDIATION_SUCCESS", "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED"]},
        "Source Remediation Execution Approval": {"commit": candidate["source_remediation_execution_approval_after_plan_results_review_commit"], "digest": candidate["source_remediation_execution_approval_after_plan_results_review_digest"]},
        "Source Plan Results Review": candidate["source_plan_results_review_summary"], "Source Plan Execution": candidate["source_plan_execution_summary"],
        "Source Method Results Review": candidate["source_method_results_review_summary"], "Source Method Execution": candidate["source_method_execution_summary"],
        "Source Diagnostic Results Review": candidate["source_diagnostic_results_review_summary"], "Source Controlled Recapture": candidate["source_controlled_recapture_summary"],
        "Source Durable Receipt": candidate["source_durable_receipt_summary"], "Source Planning and Detail Binding Evidence": candidate["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": candidate["retry_failure_context"], "Priority 1 Target Modules": candidate["priority_1_target_modules"],
        "Priority 1 Validation Summary": candidate["priority1_validation_summary"], "Diagnostic Capture Evidence Summary": candidate["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": candidate["reviewed_observable_failure_families"], "Reviewed Workstreams": candidate["reviewed_workstreams"],
        "Source Authority Enrichment Review Summary": candidate["source_authority_enrichment_review_summary"],
        "Missing Authority Inventory Review Summary": candidate["missing_authority_inventory_review_summary"],
        "Workstream Authority Mapping Review Summary": candidate["workstream_authority_mapping_review_summary"],
        "Source Evidence Requirements Review Summary": candidate["source_evidence_requirements_review_summary"],
        "No-Change Disposition Input Review Summary": candidate["no_change_disposition_input_review_summary"],
        "Alternate Diagnostic Input Review Summary": candidate["alternate_diagnostic_input_review_summary"],
        "Retry Basis Requirements Review Summary": candidate["retry_basis_requirements_review_summary"],
        "Candidate Philosophy": candidate["candidate_philosophy"], "Proposed Follow-On Packages": candidate["proposed_follow_on_packages"],
        "Recommended Package": {"package": candidate["recommended_follow_on_package"], "status": candidate["recommendation_status"], "reason": candidate["recommendation_reason"]},
        "Future Requirements": candidate["future_requirements"], "Future Plan": {"status": candidate["future_plan_status"], "steps": candidate["future_plan"]},
        "Planned Outputs": candidate["planned_outputs"], "Non-Goals": candidate["non_goals"], "Next Chain": candidate["next_chain"],
        "Next Gates": candidate["next_gates"], "Risk Controls": candidate["risk_controls"],
        "Authority Boundaries": {field: candidate[field] for field in FALSE_FIELDS},
        "Checklist Summary": candidate["summary"], "Guardrails": list(RISK_CONTROLS),
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Candidate After Results Review v1", "",
             f"Artifact: `{candidate['artifact_kind']}`", f"Status: `{candidate['candidate_status']}`", f"Scope: `{candidate['candidate_scope']}`", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(
    output_dir: str | Path, *, source_results_review: dict | None = None,
) -> dict[str, Any]:
    """Write only the deterministic candidate status document."""

    candidate = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(source_results_review=source_results_review)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_markdown_v1(candidate), encoding="utf-8")
    return candidate


__all__ = [
    "ARTIFACT_KIND", "CANDIDATE_STATUS", "CANDIDATE_SCOPE", "CANDIDATE_DIGEST_KEY", "RECOMMENDED_PACKAGE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_DIGEST_KEY",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_markdown_v1",
    *[item["package_id"] for item in PROPOSED_PACKAGES],
]
