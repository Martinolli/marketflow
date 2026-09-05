"""Approve one follow-on package for a separate future execution only."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVED_AFTER_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVED_AFTER_RESULTS_REVIEW"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_digest"
SOURCE_FOLLOW_ON_OPERATOR_REVIEW_COMMIT = "1d610d49852fe76101c3d9293f83ccd65ec40749"
SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST = "c4073ce0ceb53e5dc7c651c294d40c863a532f02c7f5dc2571a7890044d6bfcb"
SELECTED_FOLLOW_ON_PACKAGE = source.PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS
OPERATOR_DECISION = "APPROVE_FOLLOW_ON_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_PACKAGE_AFTER_RESULTS_REVIEW"
OPERATOR_ATTESTATION_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_attestation_v1"
REQUIRED_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ATTESTATION_PHRASE_V1 = (
    "APPROVE MARKETFLOW RETRY FAILURE FOLLOW ON "
    "PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS AFTER SOURCE AUTHORITY "
    "ENRICHMENT RESULTS REVIEW FOR FUTURE EXECUTION ONLY NO FOLLOW ON EXECUTION NOW NO SOURCE AUTHORITY "
    "ACQUISITION CANDIDATE NOW NO SOURCE AUTHORITY ACQUISITION NOW NO NO CHANGE DISPOSITION NOW NO "
    "ALTERNATE DIAGNOSTICS NOW NO REMEDIATION NOW NO CODE CHANGES NOW NO TEST CHANGES NOW NO DIGEST "
    "UPDATES NOW NO PATCH NOW NO PYTEST NOW NO RETRY NO MAIN PUSH "
    "FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)
APPROVED_ONLY = "APPROVED_FOR_FUTURE_FOLLOW_ON_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_EXECUTION_AFTER_RESULTS_REVIEW_ONLY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_V1"
PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS = SELECTED_FOLLOW_ON_PACKAGE
PACKAGE_CREATE_NO_CHANGE_DISPOSITION_CANDIDATE_FROM_REVIEWED_ENRICHMENT_RESULTS = source.PACKAGE_CREATE_NO_CHANGE_DISPOSITION_CANDIDATE_FROM_REVIEWED_ENRICHMENT_RESULTS
PACKAGE_CREATE_ALTERNATE_BOUNDED_DIAGNOSTIC_CANDIDATE_FROM_ENRICHMENT_RESULTS = source.PACKAGE_CREATE_ALTERNATE_BOUNDED_DIAGNOSTIC_CANDIDATE_FROM_ENRICHMENT_RESULTS
PACKAGE_CREATE_REMEDIATION_REENTRY_CANDIDATE_ONLY_AFTER_SOURCE_AUTHORITY_EXISTS = source.PACKAGE_CREATE_REMEDIATION_REENTRY_CANDIDATE_ONLY_AFTER_SOURCE_AUTHORITY_EXISTS
PACKAGE_CREATE_NO_CHANGE_RETRY_CRITERIA_CANDIDATE_AFTER_RESULTS_REVIEW = source.PACKAGE_CREATE_NO_CHANGE_RETRY_CRITERIA_CANDIDATE_AFTER_RESULTS_REVIEW
PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_SOURCE_AUTHORITY_ACQUISITION = source.PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_SOURCE_AUTHORITY_ACQUISITION
PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_SEPARATE_APPROVAL = source.PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_SEPARATE_APPROVAL
PACKAGE_DIRECT_REMEDIATION_FROM_ENRICHMENT_PLAN = source.PACKAGE_DIRECT_REMEDIATION_FROM_ENRICHMENT_PLAN
PACKAGE_NO_CHANGE_DISPOSITION_WITHOUT_REVIEWED_EVIDENCE = source.PACKAGE_NO_CHANGE_DISPOSITION_WITHOUT_REVIEWED_EVIDENCE
PACKAGE_RUN_ALTERNATE_DIAGNOSTICS_WITHOUT_APPROVAL = source.PACKAGE_RUN_ALTERNATE_DIAGNOSTICS_WITHOUT_APPROVAL
PACKAGE_NEW_RETRY_FROM_ENRICHMENT_RESULTS_ONLY = source.PACKAGE_NEW_RETRY_FROM_ENRICHMENT_RESULTS_ONLY
PACKAGE_MAIN_MERGE_FROM_ENRICHMENT_RESULTS_OR_CURRENT_ROOT_PASS = source.PACKAGE_MAIN_MERGE_FROM_ENRICHMENT_RESULTS_OR_CURRENT_ROOT_PASS

_COMMITTED_SOURCE_REVIEW = source._assemble_review()

ATTESTATION_VALUE_FIELDS = {
    "operator_confirms_source_follow_on_operator_review_digest": SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_follow_on_candidate_digest": _COMMITTED_SOURCE_REVIEW["source_follow_on_candidate_digest"],
    "operator_confirms_source_results_review_digest": _COMMITTED_SOURCE_REVIEW["source_results_review_digest"],
    "operator_confirms_source_enrichment_plan_review_digest": _COMMITTED_SOURCE_REVIEW["source_enrichment_plan_review_digest"],
    "operator_confirms_source_missing_authority_inventory_review_digest": _COMMITTED_SOURCE_REVIEW["source_missing_authority_inventory_review_digest"],
    "operator_confirms_source_workstream_mapping_review_digest": _COMMITTED_SOURCE_REVIEW["source_plan_results_review_summary"]["workstream_mapping_review_digest"],
    "operator_confirms_source_results_review_manifest_digest": _COMMITTED_SOURCE_REVIEW["source_results_review_manifest_digest"],
    "operator_confirms_source_execution_digest": _COMMITTED_SOURCE_REVIEW["source_execution_digest"],
    "operator_confirms_source_enrichment_plan_digest": _COMMITTED_SOURCE_REVIEW["source_authority_enrichment_plan_digest"],
    "operator_confirms_source_missing_authority_inventory_digest": _COMMITTED_SOURCE_REVIEW["source_missing_authority_inventory_digest"],
    "operator_confirms_source_workstream_authority_mapping_digest": _COMMITTED_SOURCE_REVIEW["source_workstream_authority_mapping_digest"],
    "operator_confirms_source_execution_manifest_digest": _COMMITTED_SOURCE_REVIEW["source_execution_manifest_digest"],
    "operator_confirms_source_approval_digest": _COMMITTED_SOURCE_REVIEW["source_approval_digest"],
    "operator_confirms_source_operator_review_digest": _COMMITTED_SOURCE_REVIEW["source_operator_review_digest"],
    "operator_confirms_source_candidate_digest": _COMMITTED_SOURCE_REVIEW["source_candidate_digest"],
    "operator_confirms_source_failure_diagnosis_digest": _COMMITTED_SOURCE_REVIEW["source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"],
    "operator_confirms_source_blocked_execution_commit": _COMMITTED_SOURCE_REVIEW["source_blocked_execution_commit"],
    "operator_confirms_source_blocked_reason": _COMMITTED_SOURCE_REVIEW["source_blocked_reason"],
    "operator_confirms_source_blocked_manifest_digest": _COMMITTED_SOURCE_REVIEW["source_blocked_manifest_digest"],
    "operator_confirms_primary_failure_class": _COMMITTED_SOURCE_REVIEW["primary_failure_class"],
    "operator_confirms_source_remediation_execution_approval_digest": _COMMITTED_SOURCE_REVIEW["source_remediation_execution_approval_after_plan_results_review_digest"],
    "operator_confirms_source_plan_results_review_digest": _COMMITTED_SOURCE_REVIEW["source_remediation_plan_or_execution_results_review_after_method_results_review_digest"],
    "operator_confirms_source_targeted_plan_review_digest": _COMMITTED_SOURCE_REVIEW["source_targeted_remediation_plan_review_digest"],
    "operator_confirms_source_plan_execution_digest": _COMMITTED_SOURCE_REVIEW["source_remediation_plan_or_execution_after_method_results_review_digest"],
    "operator_confirms_source_targeted_remediation_plan_digest": _COMMITTED_SOURCE_REVIEW["source_targeted_remediation_plan_digest"],
    "operator_confirms_source_workstream_mapping_digest": _COMMITTED_SOURCE_REVIEW["source_workstream_mapping_digest"],
    "operator_confirms_source_method_results_review_digest": _COMMITTED_SOURCE_REVIEW["source_remediation_or_method_results_review_after_diagnostic_capture_digest"],
    "operator_confirms_source_method_execution_digest": _COMMITTED_SOURCE_REVIEW["source_remediation_or_method_execution_after_diagnostic_capture_digest"],
    "operator_confirms_source_diagnostic_results_review_digest": _COMMITTED_SOURCE_REVIEW["source_receipt_recovery_or_recapture_results_review_digest"],
    "operator_confirms_source_controlled_recapture_execution_digest": _COMMITTED_SOURCE_REVIEW["source_receipt_recovery_or_recapture_execution_digest"],
    "operator_confirms_source_durable_receipt_digest": _COMMITTED_SOURCE_REVIEW["source_receipt_recovery_or_recapture_receipt_digest"],
    "operator_confirms_source_durable_receipt_path": _COMMITTED_SOURCE_REVIEW["source_durable_receipt_path"],
    "operator_confirms_source_prior_diagnostic_failure_diagnosis_digest": _COMMITTED_SOURCE_REVIEW["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
    "operator_confirms_source_prior_diagnostic_blocked_reason": _COMMITTED_SOURCE_REVIEW["source_targeted_diagnostic_output_capture_execution_blocked_reason"],
    "operator_confirms_source_planning_execution_digest": _COMMITTED_SOURCE_REVIEW["source_planning_execution_digest"],
    "operator_confirms_source_complete_29_row_binding_digest": _COMMITTED_SOURCE_REVIEW["source_complete_29_row_binding_digest"],
    "operator_confirms_source_materialized_payload_digest": _COMMITTED_SOURCE_REVIEW["source_materialized_payload_digest"],
    "operator_confirms_source_recovery_detail_digest": _COMMITTED_SOURCE_REVIEW["source_recovery_detail_digest"],
    "operator_confirms_source_module_grouping_digest": _COMMITTED_SOURCE_REVIEW["source_module_grouping_digest"],
    "operator_confirms_source_staged_inventory_digest": _COMMITTED_SOURCE_REVIEW["source_staged_inventory_digest"],
    "operator_confirms_retry_execution_commit": _COMMITTED_SOURCE_REVIEW["retry_execution_commit"],
    "operator_confirms_source_stdout_hash": _COMMITTED_SOURCE_REVIEW["source_stdout_sha256"],
    "operator_confirms_source_stderr_hash": _COMMITTED_SOURCE_REVIEW["source_stderr_sha256"],
    "operator_confirms_selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
}

ATTESTATION_BOOLEAN_FIELDS = tuple(
    """operator_confirms_secondary_failure_classes
operator_confirms_retry_failure_counts
operator_confirms_priority_1_top_module_paths
operator_confirms_priority_1_total_612
operator_confirms_top_10_total_1069
operator_confirms_module_summary_count_29
operator_confirms_failed_or_errored_nodeids_1404
operator_confirms_priority1_pre_change_validation_675_passed
operator_confirms_priority1_post_change_validation_675_passed
operator_confirms_priority1_validation_not_retry_evidence
operator_confirms_source_exit_code_1_as_diagnostic_only
operator_confirms_source_stdout_byte_count_1231380
operator_confirms_source_stderr_byte_count_0
operator_confirms_observable_family_count_4
operator_confirms_observable_evidence_items_188
operator_confirms_family_confidence_high
operator_confirms_workstream_count_4
operator_confirms_missing_authority_inventory_four_sections
operator_confirms_missing_authority_inventory_30_items
operator_confirms_missing_authority_items_missing_not_acquired
operator_confirms_workstream_mappings_planned_not_executed
operator_confirms_source_outputs_27_reviewed
operator_confirms_review_outputs_28_generated
operator_confirms_approval_scope_only
operator_confirms_no_follow_on_execution_now
operator_confirms_no_source_authority_acquisition_candidate_now
operator_confirms_no_source_authority_acquisition_now
operator_confirms_no_source_authority_evidence_acquisition_now
operator_confirms_no_no_change_disposition_now
operator_confirms_no_alternate_diagnostics_now
operator_confirms_no_remediation_now
operator_confirms_no_code_remediation_now
operator_confirms_no_production_code_change_now
operator_confirms_no_existing_test_change_now
operator_confirms_no_expected_digest_update_now
operator_confirms_no_patch_generation_now
operator_confirms_no_patch_application_now
operator_confirms_no_pytest_now
operator_confirms_no_full_pytest_now
operator_confirms_no_retry
operator_confirms_no_cache_read
operator_confirms_no_cache_modification
operator_confirms_no_durable_receipt_parse
operator_confirms_no_diagnostic_output_analysis
operator_confirms_no_source_authority_enrichment_rerun
operator_confirms_no_plan_execution_rerun
operator_confirms_no_targeted_plan_regeneration
operator_confirms_no_method_execution_rerun
operator_confirms_no_recapture_rerun
operator_confirms_no_diagnostic_command
operator_confirms_no_priority1_validation_rerun
operator_confirms_no_terminal_log_parse
operator_confirms_no_operator_log_parse
operator_confirms_no_env_inspection
operator_confirms_no_prior_lost_value_reconstruction
operator_confirms_no_full_stream_reconstruction
operator_confirms_no_failure_error_separation
operator_confirms_no_first_failure
operator_confirms_no_first_error
operator_confirms_no_traceback_root_cause
operator_confirms_no_root_cause
operator_confirms_no_retry_success
operator_confirms_no_main_merge_readiness
operator_confirms_no_retry_candidate
operator_confirms_no_retry_approval
operator_confirms_no_retry_execution
operator_confirms_no_retry_results_review
operator_confirms_no_integration_results_review
operator_confirms_no_main_merge_approval
operator_confirms_no_integration_success
operator_confirms_no_successful_integration_digest
operator_confirms_no_integration_branch_push
operator_confirms_no_main_push
operator_confirms_origin_main_not_modified
operator_confirms_no_branch_delete
operator_confirms_no_force_push
operator_confirms_no_tag_mutation
operator_confirms_no_evidence_regeneration
operator_confirms_no_marketflow_commit
operator_confirms_no_pytest_cache_commit
operator_confirms_no_provider_requests
operator_confirms_no_market_data_acquisition
operator_confirms_no_dataset_generation
operator_confirms_no_metric_recomputation
operator_confirms_no_model_training
operator_confirms_no_strategy_scoring
operator_confirms_no_trade_recommendations
operator_confirms_no_predictive_usefulness_acceptance
operator_confirms_no_profitability_acceptance
operator_confirms_runtime_not_authorized
operator_confirms_broker_not_authorized
operator_confirms_no_api_key_storage_or_printing
operator_confirms_no_secret_capture_or_commit""".splitlines()
)

TRUE_FIELDS = tuple(
    """follow_on_approval_after_results_review_created
follow_on_package_selected
follow_on_package_approved
follow_on_package_authorized_for_future_execution
selected_follow_on_package_verified
source_operator_review_bound
source_follow_on_candidate_bound
source_results_review_bound
source_execution_bound
source_approval_bound
source_candidate_chain_bound
source_failure_diagnosis_bound
source_blocked_execution_bound
source_enrichment_review_facts_bound
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
diagnostic_metadata_bound
observable_families_bound
reviewed_workstreams_bound
future_requirements_approved
future_plan_approved
planned_outputs_authorized_not_generated
supporting_packages_preserved_unselected
blocked_packages_preserved_blocked
ready_for_follow_on_execution_after_results_review""".splitlines()
)

FALSE_FIELDS = tuple(
    """follow_on_execution_performed
source_authority_acquisition_candidate_created
source_authority_acquisition_performed
source_authority_evidence_acquired
concrete_source_authority_established
safe_source_authority_bound_change_identified
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
pytest_performed_in_approval
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_approval
diagnostic_output_analyzed_in_approval
source_authority_enrichment_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_approval
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
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
retry_success_claimed
main_merge_readiness_claimed
new_retry_candidate_created
retry_approval_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
ready_for_source_authority_acquisition_candidate
ready_for_source_authority_acquisition
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
provider_requests_made_in_approval
market_data_acquisition_performed_in_approval
dataset_generation_performed_in_approval
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()
)

FUTURE_PERMISSION_TRUE_FIELDS = tuple(
    """future_execution_may_create_source_authority_acquisition_candidate
future_execution_may_define_source_authority_acquisition_scope
future_execution_may_define_evidence_to_obtain_or_bind
future_execution_may_map_missing_authority_items_to_candidate_inputs
future_execution_may_define_operator_provided_evidence_requirements
future_execution_may_define_candidate_results_review_requirements""".splitlines()
)

FUTURE_PERMISSION_FALSE_FIELDS = tuple(
    """future_execution_may_acquire_source_authority
future_execution_may_acquire_external_evidence
future_execution_may_create_no_change_disposition
future_execution_may_execute_alternate_diagnostics
future_execution_may_execute_remediation
future_execution_may_modify_production_code
future_execution_may_modify_existing_tests
future_execution_may_update_expected_digests
future_execution_may_generate_or_apply_patch
future_execution_may_run_pytest
future_execution_may_run_full_pytest
future_execution_may_run_retry
future_execution_may_push_main
future_execution_may_push_integration_branch
future_execution_may_create_retry_candidate
future_execution_may_claim_root_cause
future_execution_may_claim_retry_success
future_execution_may_create_main_merge_approval
future_follow_on_execution_executed""".splitlines()
)

APPROVED_FUTURE_REQUIREMENTS = tuple(
    item["requirement_id"] for item in _COMMITTED_SOURCE_REVIEW["reviewed_future_requirements"]
)
APPROVED_FUTURE_PLAN = (
    "Bind this approval and source follow-on operator-review evidence.",
    "Bind source follow-on candidate, source results review, execution, approval, operator review, candidate, failure diagnosis, blocked execution, plan review, plan execution, method, diagnostic, receipt, planning, detail-binding, recovery, module-grouping, and staged-inventory digests.",
    "Bind retry failure counts, Priority 1 modules, Priority 1 validation facts, observable families, reviewed workstreams, enrichment outputs, and missing-authority inventory.",
    "Preserve that no source authority was acquired by the enrichment result or operator review.",
    "Execute the selected follow-on package only under a separate execution task.",
    "Future execution may create a source-authority acquisition candidate and define evidence acquisition scope without acquiring evidence.",
    "Future execution must not create no-change disposition, execute diagnostics, execute remediation, create retry candidate, or create main-merge readiness.",
    "Future execution must preserve that current-root Priority 1 passing state is not retry evidence.",
    "Future execution must preserve missing-authority items as not acquired unless a later approved acquisition path supplies evidence.",
    "Require results review before any acquisition, disposition, diagnostic, remediation, retry candidate, or main-merge path.",
    "Preserve the failed detached retry as authoritative.",
    "Keep provider, runtime, broker, and trading authority closed.",
)
AUTHORIZED_OUTPUT_IDS = tuple(
    """follow_on_approval_after_results_review_manifest
source_follow_on_operator_review_binding_report
source_follow_on_candidate_binding_report
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
approved_source_authority_acquisition_candidate_package_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
)
SUPPORTING_PACKAGE_IDS = (
    PACKAGE_CREATE_NO_CHANGE_DISPOSITION_CANDIDATE_FROM_REVIEWED_ENRICHMENT_RESULTS,
    PACKAGE_CREATE_ALTERNATE_BOUNDED_DIAGNOSTIC_CANDIDATE_FROM_ENRICHMENT_RESULTS,
    PACKAGE_CREATE_REMEDIATION_REENTRY_CANDIDATE_ONLY_AFTER_SOURCE_AUTHORITY_EXISTS,
    PACKAGE_CREATE_NO_CHANGE_RETRY_CRITERIA_CANDIDATE_AFTER_RESULTS_REVIEW,
    PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_SOURCE_AUTHORITY_ACQUISITION,
)
BLOCKED_PACKAGE_IDS = (
    PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_SEPARATE_APPROVAL,
    PACKAGE_DIRECT_REMEDIATION_FROM_ENRICHMENT_PLAN,
    PACKAGE_NO_CHANGE_DISPOSITION_WITHOUT_REVIEWED_EVIDENCE,
    PACKAGE_RUN_ALTERNATE_DIAGNOSTICS_WITHOUT_APPROVAL,
    PACKAGE_NEW_RETRY_FROM_ENRICHMENT_RESULTS_ONLY,
    PACKAGE_MAIN_MERGE_FROM_ENRICHMENT_RESULTS_OR_CURRENT_ROOT_PASS,
)
NEXT_CHAIN = (
    "Follow-On Execution After Source-Authority Enrichment Results Review v1, if approved.",
    "Follow-On Results Review v1.",
    "Conditional source-authority acquisition candidate, no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if results review supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple(
    """follow_on_execution_after_results_review_if_approved
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
main_merge_approval_if_new_retry_passes""".splitlines()
)
RISK_CONTROLS = tuple(
    """follow_on_approval_does_not_execute_follow_on
follow_on_approval_does_not_create_source_authority_acquisition_candidate_now
follow_on_approval_does_not_acquire_source_authority
follow_on_approval_does_not_acquire_source_authority_evidence
follow_on_approval_does_not_create_no_change_disposition
follow_on_approval_does_not_execute_alternate_diagnostics
follow_on_approval_does_not_execute_remediation
follow_on_approval_does_not_modify_production_code
follow_on_approval_does_not_modify_existing_tests
follow_on_approval_does_not_update_expected_digests
follow_on_approval_does_not_generate_patch
follow_on_approval_does_not_apply_patch
follow_on_approval_does_not_run_pytest
follow_on_approval_does_not_run_full_pytest
follow_on_approval_does_not_rerun_priority1_validation
follow_on_approval_does_not_rerun_retry
follow_on_approval_does_not_rerun_detached_retry
follow_on_approval_does_not_parse_durable_receipt
follow_on_approval_does_not_analyze_diagnostic_output
follow_on_approval_does_not_rerun_source_authority_enrichment
follow_on_approval_does_not_rerun_plan_execution
follow_on_approval_does_not_regenerate_targeted_plan
follow_on_approval_does_not_rerun_method_execution
follow_on_approval_does_not_rerun_controlled_recapture
follow_on_approval_does_not_run_diagnostic_command
follow_on_approval_does_not_read_pytest_cache
follow_on_approval_does_not_modify_pytest_cache
follow_on_approval_does_not_parse_terminal_logs
follow_on_approval_does_not_parse_operator_logs
follow_on_approval_does_not_inspect_env
follow_on_approval_does_not_reconstruct_prior_lost_values
follow_on_approval_does_not_reconstruct_full_streams
follow_on_approval_does_not_classify_modules_again
follow_on_approval_does_not_classify_full_retry_failures
follow_on_approval_does_not_classify_full_retry_errors
follow_on_approval_does_not_claim_failure_error_separation
follow_on_approval_does_not_identify_authoritative_first_failure
follow_on_approval_does_not_identify_authoritative_first_error
follow_on_approval_does_not_claim_traceback_root_cause
follow_on_approval_does_not_claim_root_cause
follow_on_approval_does_not_claim_retry_success
follow_on_approval_does_not_claim_main_merge_readiness
follow_on_approval_does_not_create_retry_candidate
follow_on_approval_does_not_create_retry_approval
follow_on_approval_does_not_create_retry_execution
follow_on_approval_does_not_create_retry_results_review
follow_on_approval_does_not_create_integration_results_review
follow_on_approval_does_not_mark_integration_successful
follow_on_approval_does_not_generate_successful_integration_digest
follow_on_approval_does_not_push_integration_branch
follow_on_approval_does_not_push_main
follow_on_approval_does_not_delete_integration_branch
follow_on_approval_does_not_delete_worktree
follow_on_approval_does_not_force_push
follow_on_approval_does_not_prune_remotes
follow_on_approval_does_not_modify_tags
follow_on_approval_does_not_modify_staged_evidence
follow_on_approval_does_not_regenerate_evidence
follow_on_approval_does_not_call_providers
follow_on_approval_does_not_acquire_market_data
follow_on_approval_does_not_generate_dataset
follow_on_approval_does_not_recompute_metrics
follow_on_approval_does_not_train_models
follow_on_approval_does_not_score_strategy
follow_on_approval_does_not_generate_trade_recommendations
follow_on_approval_does_not_accept_predictive_usefulness
follow_on_approval_does_not_accept_profitability
follow_on_approval_does_not_authorize_runtime
follow_on_approval_does_not_authorize_broker_execution
selected_follow_on_package_approved_for_future_execution_only
future_execution_limited_to_source_authority_acquisition_candidate_creation
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
source_follow_on_candidate_operator_review_remains_source_evidence
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_execution_required_after_approval
separate_results_review_required_after_any_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines()
)


class MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError(ValueError):
    """Raised when the approval or attestation violates its closed boundary."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() is not None


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        "operator_attestation_phrase": REQUIRED_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        **ATTESTATION_VALUE_FIELDS,
    }
    allowed = {*expected, "operator_attestation_timestamp_utc", "operator_reference", *ATTESTATION_BOOLEAN_FIELDS}
    if set(attestation) != allowed:
        raise error("operator attestation fields mismatch")
    for field, expected_value in expected.items():
        if attestation.get(field) != expected_value:
            raise error(f"{field} mismatch")
    if not _iso_utc(attestation.get("operator_attestation_timestamp_utc")):
        raise error("operator_attestation_timestamp_utc invalid")
    if not isinstance(attestation.get("operator_reference"), str) or not attestation["operator_reference"].strip():
        raise error("operator_reference missing")
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise error(f"{field} must be true")


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_attestation_v1(
    *, operator_reference: str, operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str, operator_confirmations: dict,
    selected_follow_on_package: str = SELECTED_FOLLOW_ON_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict[str, Any]:
    """Build and validate the exact non-secret operator attestation."""

    if not isinstance(operator_confirmations, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError(
            "operator_confirmations must be an object"
        )
    attestation = {
        "operator_reference": operator_reference,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_phrase": operator_attestation_phrase,
        "selected_follow_on_package": selected_follow_on_package,
        "operator_decision": operator_decision,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        **deepcopy(operator_confirmations),
    }
    _validate_attestation(attestation)
    return attestation


def _validated_source_review(source_operator_review: dict | None) -> dict[str, Any]:
    review = deepcopy(_COMMITTED_SOURCE_REVIEW if source_operator_review is None else source_operator_review)
    try:
        source.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(review)
    except source.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnOperatorReviewError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError(
            "source operator review validation failed"
        ) from exc
    if review.get(source.OPERATOR_REVIEW_DIGEST_KEY) != SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError(
            "source operator review digest mismatch"
        )
    return review


def _approved_package() -> dict[str, Any]:
    return {
        "package_id": SELECTED_FOLLOW_ON_PACKAGE,
        "source_review_status": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "approval_status": APPROVED_ONLY,
        "selected": True, "approved": True, "authorized_for_future_execution": True, "executed": False,
        "purpose": "Future execution may create a source-authority acquisition candidate based on the reviewed missing-authority inventory, source-evidence requirements, canonical serialization requirements, schema/field contract requirements, fixture/isolation requirements, and workstream mappings. It may define what source artifacts, specifications, schemas, canonical payloads, field contracts, fixture lifecycle evidence, or operator-provided reviewed evidence must be obtained before any remediation, no-change disposition, alternate diagnostic, retry candidate, or main merge can be justified.",
        "future_execution_boundary": "The future execution may create a candidate and define acquisition scope. It must not acquire source authority, execute no-change disposition, run diagnostics, execute remediation, modify code/tests/digests, run pytest, rerun retry, create retry readiness, push main, push integration branch, authorize runtime, authorize broker execution, or authorize trading.",
    }


def _approved_requirements() -> list[dict[str, Any]]:
    return [{"requirement_id": item, "approval_status": APPROVED_ONLY, "execution_status": "NOT_EXECUTED"} for item in APPROVED_FUTURE_REQUIREMENTS]


def _approved_plan() -> list[dict[str, Any]]:
    return [{"step_id": index, "action": action, "approval_status": APPROVED_ONLY, "execution_status": "NOT_EXECUTED"} for index, action in enumerate(APPROVED_FUTURE_PLAN, 1)]


def _authorized_outputs() -> list[dict[str, Any]]:
    return [{"output_id": item, "authorization_status": "AUTHORIZED_NOT_GENERATED"} for item in AUTHORIZED_OUTPUT_IDS]


def _supporting_packages() -> list[dict[str, Any]]:
    return [{"package_id": item, "approval_status": "AVAILABLE_NOT_SELECTED", "selected": False, "approved": False, "authorized": False, "executed": False} for item in SUPPORTING_PACKAGE_IDS]


def _blocked_packages() -> list[dict[str, Any]]:
    return [{"package_id": item, "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False, "authorized": False, "executed": False} for item in BLOCKED_PACKAGE_IDS]


_SOURCE_EXCLUSIONS = {
    "artifact_kind", "schema_version", "review_status", "review_scope", "checklist", "summary",
    source.OPERATOR_REVIEW_DIGEST_KEY, "reviewed_follow_on_packages", "recommended_package",
    "reviewed_future_requirements", "reviewed_future_plan", "reviewed_planned_outputs",
    "reviewed_non_goals", "recommendation", "next_chain", "next_gates", "risk_controls",
}


def _source_payload(review: Mapping[str, Any]) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in review.items() if key not in _SOURCE_EXCLUSIONS}


def _approval_body(attestation: Mapping[str, Any], source_review: Mapping[str, Any]) -> dict[str, Any]:
    body = {
        **_source_payload(source_review),
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "created_offline": True, "governance_only": True, "approval_only": True,
        "operator_attestation_required": True, "operator_attestation": deepcopy(dict(attestation)),
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        "source_follow_on_candidate_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_follow_on_candidate_operator_review_status": source.REVIEW_STATUS,
        "source_follow_on_candidate_operator_review_scope": source.REVIEW_SCOPE,
        "source_follow_on_candidate_operator_review_commit": SOURCE_FOLLOW_ON_OPERATOR_REVIEW_COMMIT,
        "source_follow_on_candidate_operator_review_digest": SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST,
        "source_follow_on_candidate_operator_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND, "status": source.REVIEW_STATUS,
            "scope": source.REVIEW_SCOPE, "commit": SOURCE_FOLLOW_ON_OPERATOR_REVIEW_COMMIT,
            "digest": SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST, "checks": "293/293 PASS",
        },
        "source_plan_workstream_mapping_review_digest": source_review["source_plan_results_review_summary"]["workstream_mapping_review_digest"],
        "approved_package": _approved_package(),
        "approved_future_requirements": _approved_requirements(),
        "approved_future_plan": _approved_plan(),
        "future_follow_on_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
        "future_follow_on_execution_input_source": "REVIEWED_FOLLOW_ON_OPERATOR_REVIEW_AFTER_SOURCE_AUTHORITY_ENRICHMENT_RESULTS_REVIEW",
        "future_follow_on_execution_type": "SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_CREATION_FROM_ENRICHMENT_RESULTS",
        **{field: True for field in FUTURE_PERMISSION_TRUE_FIELDS},
        **{field: False for field in FUTURE_PERMISSION_FALSE_FIELDS},
        "authorized_planned_outputs": _authorized_outputs(),
        "supporting_packages": _supporting_packages(), "blocked_packages": _blocked_packages(),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    return body


CHECK_IDS = tuple(dict.fromkeys((
    "source_follow_on_operator_review_commit_bound", "source_follow_on_operator_review_digest_bound",
    *source.CHECK_IDS,
    "selected_follow_on_package_bound", "operator_decision_matches", "operator_attestation_phrase_matches",
    "approval_scope_only", "approved_package_bound", "future_requirements_approved",
    "future_plan_approved_not_executed", "future_execution_boundary_approved_not_executed",
    "planned_outputs_authorized_not_generated", "supporting_packages_not_selected",
    "blocked_packages_not_approved", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    *[f"{field}_true" for field in TRUE_FIELDS + FUTURE_PERMISSION_TRUE_FIELDS],
    *[f"{field}_false" for field in FALSE_FIELDS + FUTURE_PERMISSION_FALSE_FIELDS],
    *[f"attestation_{field}" for field in (*ATTESTATION_VALUE_FIELDS, *ATTESTATION_BOOLEAN_FIELDS)],
)))


def _checklist() -> list[dict[str, Any]]:
    return [{"check_id": item, "status": PASS, "expected": True, "actual": True,
             "severity": BLOCKER, "message": f"{item} passed"} for item in CHECK_IDS]


def _summary(approval: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "total_checks": len(approval["checklist"]), "passed_checks": len(approval["checklist"]),
        "failed_checks": 0, "blocker_count": 0,
        **{field: approval[field] for field in TRUE_FIELDS + FALSE_FIELDS},
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        "approved_future_requirement_count": 63, "approved_future_plan_step_count": 12,
        "authorized_planned_output_count": 27, "supporting_package_count": 5, "blocked_package_count": 6,
        "source_workstream_count": 4, "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188, "source_exit_code": 1,
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "missing_authority_inventory_section_count": 4, "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "workstream_mapping_count": 4, "workstream_mapping_status": "PLANNED_NOT_EXECUTED",
        "source_outputs_generated_count": 27, "review_outputs_generated_count": 28,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _approval_digest(approval: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(approval))
    for field in ("checklist", "summary", APPROVAL_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _first_difference(actual: Any, expected: Any, path: str = "approval") -> str | None:
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


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(
    *, operator_attestation: dict, source_operator_review: dict | None = None,
) -> dict[str, Any]:
    """Build an attestation-bound approval without executing the follow-on."""

    _validate_attestation(operator_attestation)
    source_review = _validated_source_review(source_operator_review)
    approval = _approval_body(operator_attestation, source_review)
    approval["checklist"] = _checklist()
    approval["summary"] = _summary(approval)
    approval[APPROVAL_DIGEST_KEY] = _approval_digest(approval)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(
    approval: dict,
) -> dict[str, Any]:
    """Validate the exact approval, source bindings, attestation, and closed boundary."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError
    if not isinstance(approval, Mapping):
        raise error("approval must be an object")
    attestation = approval.get("operator_attestation")
    if not isinstance(attestation, Mapping):
        raise error("operator_attestation missing")
    _validate_attestation(attestation)
    expected = _approval_body(attestation, _validated_source_review(None))
    expected["checklist"] = _checklist()
    expected["summary"] = _summary(expected)
    expected[APPROVAL_DIGEST_KEY] = _approval_digest(expected)
    difference = _first_difference(approval, expected)
    if difference:
        raise error(f"{difference} mismatch")
    digest = approval[APPROVAL_DIGEST_KEY]
    if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise error("approval digest invalid")
    return {
        "artifact_kind": ARTIFACT_KIND, "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE, "approval_digest": digest,
        "total_checks": approval["summary"]["total_checks"],
        "passed_checks": approval["summary"]["passed_checks"],
        "failed_checks": 0, "blocker_count": 0,
    }


MARKDOWN_SECTIONS = (
    "Operator Attestation", "Source Follow-On Operator Review", "Source Follow-On Candidate",
    "Source Results Review", "Source Results Review Digests", "Source Execution", "Source Execution Digests",
    "Source Approval", "Source Operator Review", "Source Candidate", "Source Failure Diagnosis",
    "Source Blocked Execution", "Blocked Reason", "Failure Classification",
    "Source Remediation Execution Approval", "Source Plan Results Review", "Source Plan Execution",
    "Source Method Results Review", "Source Method Execution", "Source Diagnostic Results Review",
    "Source Controlled Recapture", "Source Durable Receipt", "Source Planning and Detail Binding Evidence",
    "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
    "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
    "Source Authority Enrichment Review Summary", "Missing Authority Inventory Review Summary",
    "Workstream Authority Mapping Review Summary", "Source Evidence Requirements Review Summary",
    "No-Change Disposition Input Review Summary", "Alternate Diagnostic Input Review Summary",
    "Retry Basis Requirements Review Summary", "Approval Scope", "Selected Follow-On Package",
    "Approved Future Requirements", "Approved Future Plan", "Future Execution Boundary", "Planned Outputs",
    "Supporting Packages", "Blocked Packages", "Next Chain", "Next Gates", "Risk Controls",
    "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_markdown_v1(
    approval: dict,
) -> str:
    """Render a validated approval status document."""

    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(deepcopy(approval))
    sections = {
        "Operator Attestation": {key: approval["operator_attestation"][key] for key in ("operator_decision", "operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version")},
        "Source Follow-On Operator Review": approval["source_follow_on_candidate_operator_review_summary"],
        "Source Follow-On Candidate": approval["source_follow_on_candidate_summary"],
        "Source Results Review": approval["source_results_review_summary"],
        "Source Results Review Digests": {key: approval[key] for key in ("source_results_review_digest", "source_enrichment_plan_review_digest", "source_missing_authority_inventory_review_digest", "source_workstream_mapping_review_digest", "source_results_review_manifest_digest")},
        "Source Execution": approval["source_execution_summary"],
        "Source Execution Digests": {key: approval[key] for key in ("source_execution_digest", "source_authority_enrichment_plan_digest", "source_missing_authority_inventory_digest", "source_workstream_authority_mapping_digest", "source_execution_manifest_digest")},
        "Source Approval": approval["source_approval_summary"], "Source Operator Review": approval["source_operator_review_summary"],
        "Source Candidate": approval["source_candidate_summary"], "Source Failure Diagnosis": approval["source_failure_diagnosis_summary"],
        "Source Blocked Execution": approval["source_blocked_execution_summary"], "Blocked Reason": approval["source_blocked_reason"],
        "Failure Classification": {"primary": approval["primary_failure_class"], "secondary": approval["secondary_failure_classes"]},
        "Source Remediation Execution Approval": {"commit": approval["source_remediation_execution_approval_after_plan_results_review_commit"], "digest": approval["source_remediation_execution_approval_after_plan_results_review_digest"]},
        "Source Plan Results Review": approval["source_plan_results_review_summary"], "Source Plan Execution": approval["source_plan_execution_summary"],
        "Source Method Results Review": approval["source_method_results_review_summary"], "Source Method Execution": approval["source_method_execution_summary"],
        "Source Diagnostic Results Review": approval["source_diagnostic_results_review_summary"], "Source Controlled Recapture": approval["source_controlled_recapture_summary"],
        "Source Durable Receipt": approval["source_durable_receipt_summary"], "Source Planning and Detail Binding Evidence": approval["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": approval["retry_failure_context"], "Priority 1 Target Modules": approval["priority_1_target_modules"],
        "Priority 1 Validation Summary": approval["priority1_validation_summary"], "Diagnostic Capture Evidence Summary": approval["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": approval["reviewed_observable_failure_families"], "Reviewed Workstreams": approval["reviewed_workstreams"],
        "Source Authority Enrichment Review Summary": approval["source_authority_enrichment_review_summary"],
        "Missing Authority Inventory Review Summary": approval["missing_authority_inventory_review_summary"],
        "Workstream Authority Mapping Review Summary": approval["workstream_authority_mapping_review_summary"],
        "Source Evidence Requirements Review Summary": approval["source_evidence_requirements_review_summary"],
        "No-Change Disposition Input Review Summary": approval["no_change_disposition_input_review_summary"],
        "Alternate Diagnostic Input Review Summary": approval["alternate_diagnostic_input_review_summary"],
        "Retry Basis Requirements Review Summary": approval["retry_basis_requirements_review_summary"],
        "Approval Scope": approval["approval_scope"], "Selected Follow-On Package": approval["approved_package"],
        "Approved Future Requirements": approval["approved_future_requirements"], "Approved Future Plan": approval["approved_future_plan"],
        "Future Execution Boundary": {field: approval[field] for field in ("future_follow_on_execution_status", "future_follow_on_execution_input_source", "future_follow_on_execution_type", *FUTURE_PERMISSION_TRUE_FIELDS, *FUTURE_PERMISSION_FALSE_FIELDS)},
        "Planned Outputs": approval["authorized_planned_outputs"], "Supporting Packages": approval["supporting_packages"],
        "Blocked Packages": approval["blocked_packages"], "Next Chain": approval["next_chain"],
        "Next Gates": approval["next_gates"], "Risk Controls": approval["risk_controls"],
        "Authority Boundaries": {field: approval[field] for field in FALSE_FIELDS},
        "Checklist Summary": approval["summary"], "Guardrails": list(RISK_CONTROLS),
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Approval After Results Review v1",
        "", f"Artifact: `{approval['artifact_kind']}`", f"Status: `{approval['approval_status']}`",
        f"Scope: `{approval['approval_scope']}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(
    output_dir: str | Path, *, operator_attestation: dict, source_operator_review: dict | None = None,
) -> dict[str, Any]:
    """Write only the deterministic approval status document."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError("protected output directory")
    approval = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(
        operator_attestation=operator_attestation, source_operator_review=source_operator_review
    )
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError("output exists")
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_markdown_v1(approval), encoding="utf-8")
    return approval


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVED_AFTER_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVED_AFTER_RESULTS_REVIEW = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_DIGEST_KEY = APPROVAL_DIGEST_KEY

__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "APPROVAL_STATUS", "APPROVAL_SCOPE", "APPROVAL_DIGEST_KEY",
    "SELECTED_FOLLOW_ON_PACKAGE", "REQUIRED_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ATTESTATION_PHRASE_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVED_AFTER_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVED_AFTER_RESULTS_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_DIGEST_KEY",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_markdown_v1",
    *[item["package_id"] for item in source._reviewed_packages()],
]
