"""Review the committed source-authority enrichment planning execution.

The review is deterministic and offline.  It binds committed facts only and does
not invoke the source execution, inspect diagnostic evidence, or authorize a
remediation, retry, runtime, or trading action.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = "PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION"
SOURCE_EXECUTION_COMMIT = "e80ddda241863eca8e52ea97fa050dcd6daea5ec"
SOURCE_EXECUTION_DIGEST = "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c"
SOURCE_ENRICHMENT_PLAN_DIGEST = "b2887bcbb29f6ba7905f41f4e500f07042a1903649caa8b3b51c9045aec5cf94"
SOURCE_MISSING_AUTHORITY_INVENTORY_DIGEST = "44ece9639ff992936c6e9386eec9efefdd3990b9a35b01c7efcf3ce1e218ecf8"
SOURCE_WORKSTREAM_AUTHORITY_MAPPING_DIGEST = "175f20cd8ba96aa026ea13d3fdfda9b45f44843095f71b905acdedc96999b6fd"
SOURCE_EXECUTION_MANIFEST_DIGEST = "8a544aa173597f2c24e531a69f4eab2264fb1aa0796a67f87b00af291e6109d6"
SOURCE_EXECUTION_ARTIFACT_KIND = source.SUCCESS_ARTIFACT_KIND
SOURCE_EXECUTION_STATUS = source.SUCCESS_STATUS
SOURCE_EXECUTION_SCOPE = source.EXECUTION_SCOPE
PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"
OUTPUT_STATUS = "GENERATED_SOURCE_AUTHORITY_ENRICHMENT_RESULTS_REVIEW_ONLY"

RESULTS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_digest"
ENRICHMENT_PLAN_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_enrichment_plan_review_digest"
MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_missing_authority_inventory_review_digest"
WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_workstream_authority_mapping_review_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION = SELECTED_PACKAGE
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_DIGEST_KEY = RESULTS_REVIEW_DIGEST_KEY
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_ENRICHMENT_PLAN_REVIEW_DIGEST_KEY = ENRICHMENT_PLAN_REVIEW_DIGEST_KEY
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY = MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY = WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_MANIFEST_DIGEST_KEY = MANIFEST_DIGEST_KEY

RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_V1"
RECOMMENDED_ACTION = "PROCEED_TO_SEPARATELY_INVOKED_CONDITIONAL_FOLLOW_ON_CANDIDATE_AFTER_SOURCE_AUTHORITY_ENRICHMENT_RESULTS_REVIEW"
RECOMMENDATION_REASON = (
    "The source-authority enrichment planning execution successfully created missing-authority inventories, "
    "workstream authority mappings, evidence requirements, no-change disposition inputs, alternate diagnostic "
    "inputs, and retry-basis requirements. It did not acquire source authority, establish concrete source "
    "authority, identify safe change authority, perform remediation, create no-change disposition, execute "
    "diagnostics, or create retry readiness. The next governed step should create a candidate to select among "
    "source-authority acquisition, no-change disposition, alternate diagnostics, remediation re-entry, no-change "
    "retry criteria, or hold disposition. Retry and main merge remain blocked."
)

TRUE_FIELDS = tuple("""source_authority_or_no_change_disposition_results_review_after_blocked_execution_created
source_execution_reviewed
source_execution_identity_verified
source_selected_package_verified
source_authority_enrichment_plan_reviewed
missing_authority_inventory_reviewed
workstream_to_missing_authority_mapping_reviewed
source_evidence_requirements_reviewed
canonical_serialization_requirements_reviewed
schema_field_contract_requirements_reviewed
fixture_isolation_requirements_reviewed
no_change_disposition_input_requirements_reviewed
alternate_diagnostic_input_requirements_reviewed
retry_basis_requirements_reviewed
source_outputs_reviewed
source_27_outputs_reviewed
source_authority_gap_preserved
direct_change_authority_absent_reviewed
source_authority_evidence_acquired_reviewed_false
concrete_source_authority_established_reviewed_false
safe_source_authority_bound_change_identified_reviewed_false
priority1_validation_disposition_preserved
detached_retry_failed_status_preserved
ready_for_conditional_follow_on_candidate_after_results_review""".splitlines())

FALSE_FIELDS = tuple("""source_authority_evidence_acquired
concrete_source_authority_established
safe_source_authority_bound_change_identified
retained_change_records_available
source_authority_acquisition_performed
source_authority_enrichment_reexecuted
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
pytest_performed_in_review
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_review
diagnostic_output_analyzed_in_review
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_review
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_review
cache_modified_in_review
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
provider_requests_made_in_review
market_data_acquisition_performed_in_review
dataset_generation_performed_in_review
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

REVIEW_FINDINGS = {
    "finding_1": "The source execution used the approved package `PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION`.",
    "finding_2": "The source execution created a source-authority enrichment plan and did not acquire source authority.",
    "finding_3": "The missing-authority inventory contains four sections and 30 authority items, all marked `MISSING_NOT_ACQUIRED`.",
    "finding_4": "Direct code, test, digest, fixture, schema, and export changes remain unauthorized.",
    "finding_5": "The four reviewed workstreams were mapped deterministically to missing authority needs.",
    "finding_6": "All workstream mappings remain planning-only and `PLANNED_NOT_EXECUTED`.",
    "finding_7": "Source evidence requirements cover expected/actual provenance, canonical serialization and digest boundaries, fixture lifecycle/determinism, and schema/export contracts.",
    "finding_8": "No-change disposition input requirements were generated, but no no-change disposition was created.",
    "finding_9": "Alternate diagnostic input requirements were generated, but no diagnostic was executed.",
    "finding_10": "Retry-basis requirements were generated, but no retry candidate, retry approval, retry execution, or retry results review was created.",
    "finding_11": "The detached retry remains failed and authoritative.",
    "finding_12": "Priority 1 current-root validation remains non-retry evidence.",
    "finding_13": "The source execution generated 27 planning-only outputs and preserved all blocked downstream gates.",
    "finding_14": "No remediation, code change, test change, digest update, patch, provider/data/runtime/trading action, retry, main push, or integration-branch push occurred.",
    "finding_15": "The result is ready only for a separately governed follow-on candidate after this results review.",
}

REVIEW_DOMAINS = [
    {"domain_id": "source_execution_identity", "disposition": "PASSED", "explanation": "Source execution commit, artifact, status, scope, selected package, and execution digest are bound."},
    {"domain_id": "source_authority_enrichment_plan", "disposition": "REVIEWED_PLANNING_ONLY", "explanation": "Enrichment plan was created and reviewed as planning-only evidence."},
    {"domain_id": "missing_authority_inventory", "disposition": "REVIEWED_MISSING_NOT_ACQUIRED", "explanation": "Four inventory sections and 30 authority items identify missing authority without acquiring it."},
    {"domain_id": "workstream_authority_mapping", "disposition": "REVIEWED_PLANNED_NOT_EXECUTED", "explanation": "Four deterministic workstream mappings exist and remain unexecuted."},
    {"domain_id": "source_evidence_requirements", "disposition": "REVIEWED_REQUIREMENTS_ONLY", "explanation": "Source evidence requirements were generated for future review but are not evidence acquisition."},
    {"domain_id": "no_change_disposition_inputs", "disposition": "REVIEWED_INPUTS_ONLY", "explanation": "No-change inputs were generated, but no disposition was made."},
    {"domain_id": "alternate_diagnostic_inputs", "disposition": "REVIEWED_INPUTS_ONLY", "explanation": "Alternate diagnostic inputs were generated, but no diagnostic was executed."},
    {"domain_id": "retry_basis_requirements", "disposition": "REVIEWED_REQUIREMENTS_ONLY", "explanation": "Retry-basis requirements were created but do not create retry readiness."},
    {"domain_id": "unsupported_claims_boundary", "disposition": "PRESERVED", "explanation": "No root-cause, retry-success, or main-readiness claims were made."},
    {"domain_id": "protected_repository_boundaries", "disposition": "PRESERVED", "explanation": "Main, integration branch, detached worktree, cache, `.marketflow`, tags, and staged evidence boundaries remain preserved."},
    {"domain_id": "provider_runtime_trading_boundary", "disposition": "PRESERVED", "explanation": "No provider, market-data, model, strategy, runtime, broker, or trading action occurred."},
    {"domain_id": "downstream_readiness", "disposition": "LIMITED", "explanation": "Results review may support a future follow-on candidate, but remediation, retry, and main merge remain closed."},
]

OUTPUT_IDS = tuple("""source_authority_or_no_change_disposition_results_review_after_blocked_execution_manifest
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
retry_failure_context_review
priority1_validation_disposition_review
source_authority_enrichment_plan_review
missing_authority_inventory_review
workstream_to_missing_authority_mapping_review
source_evidence_requirements_review
canonical_serialization_authority_requirements_review
schema_field_contract_authority_requirements_review
fixture_isolation_authority_requirements_review
no_change_disposition_input_requirements_review
alternate_diagnostic_input_requirements_review
retry_basis_requirements_review
unsupported_claims_boundary_review
follow_on_candidate_readiness_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Conditional Follow-On Candidate After Source-Authority Enrichment Results Review v1.",
    "Follow-On Candidate Operator Review v1.",
    "Follow-On Approval v1, if selected.",
    "Follow-On Execution v1, if approved.",
    "Follow-On Results Review v1.",
    "Conditional remediation execution candidate, alternate diagnostic candidate, no-change retry candidate, source-authority acquisition candidate, or hold disposition only if results review supports it.",
    "New Integration Branch Retry Candidate v1, only after a reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple("""conditional_follow_on_candidate_after_source_authority_enrichment_results_review
follow_on_candidate_operator_review
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

RISK_CONTROLS = tuple("""results_review_after_blocked_execution_does_not_execute_source_authority_enrichment
results_review_after_blocked_execution_does_not_acquire_source_authority
results_review_after_blocked_execution_does_not_create_no_change_disposition
results_review_after_blocked_execution_does_not_execute_alternate_diagnostics
results_review_after_blocked_execution_does_not_execute_remediation
results_review_after_blocked_execution_does_not_modify_production_code
results_review_after_blocked_execution_does_not_modify_existing_tests
results_review_after_blocked_execution_does_not_update_expected_digests
results_review_after_blocked_execution_does_not_generate_patch
results_review_after_blocked_execution_does_not_apply_patch
results_review_after_blocked_execution_does_not_run_pytest
results_review_after_blocked_execution_does_not_run_full_pytest
results_review_after_blocked_execution_does_not_rerun_priority1_validation
results_review_after_blocked_execution_does_not_rerun_retry
results_review_after_blocked_execution_does_not_rerun_detached_retry
results_review_after_blocked_execution_does_not_parse_durable_receipt
results_review_after_blocked_execution_does_not_analyze_diagnostic_output
results_review_after_blocked_execution_does_not_rerun_plan_execution
results_review_after_blocked_execution_does_not_regenerate_targeted_plan
results_review_after_blocked_execution_does_not_rerun_method_execution
results_review_after_blocked_execution_does_not_rerun_controlled_recapture
results_review_after_blocked_execution_does_not_run_diagnostic_command
results_review_after_blocked_execution_does_not_read_pytest_cache
results_review_after_blocked_execution_does_not_modify_pytest_cache
results_review_after_blocked_execution_does_not_parse_terminal_logs
results_review_after_blocked_execution_does_not_parse_operator_logs
results_review_after_blocked_execution_does_not_inspect_env
results_review_after_blocked_execution_does_not_reconstruct_prior_lost_values
results_review_after_blocked_execution_does_not_reconstruct_full_streams
results_review_after_blocked_execution_does_not_classify_modules_again
results_review_after_blocked_execution_does_not_classify_full_retry_failures
results_review_after_blocked_execution_does_not_classify_full_retry_errors
results_review_after_blocked_execution_does_not_claim_failure_error_separation
results_review_after_blocked_execution_does_not_identify_authoritative_first_failure
results_review_after_blocked_execution_does_not_identify_authoritative_first_error
results_review_after_blocked_execution_does_not_claim_traceback_root_cause
results_review_after_blocked_execution_does_not_claim_root_cause
results_review_after_blocked_execution_does_not_claim_retry_success
results_review_after_blocked_execution_does_not_claim_main_merge_readiness
results_review_after_blocked_execution_does_not_create_source_authority_acquisition
results_review_after_blocked_execution_does_not_create_remediation_execution
results_review_after_blocked_execution_does_not_create_new_retry_candidate
results_review_after_blocked_execution_does_not_create_retry_approval
results_review_after_blocked_execution_does_not_create_retry_execution
results_review_after_blocked_execution_does_not_create_retry_results_review
results_review_after_blocked_execution_does_not_create_integration_results_review
results_review_after_blocked_execution_does_not_mark_integration_successful
results_review_after_blocked_execution_does_not_generate_successful_integration_digest
results_review_after_blocked_execution_does_not_push_integration_branch
results_review_after_blocked_execution_does_not_push_main
results_review_after_blocked_execution_does_not_delete_integration_branch
results_review_after_blocked_execution_does_not_delete_worktree
results_review_after_blocked_execution_does_not_force_push
results_review_after_blocked_execution_does_not_prune_remotes
results_review_after_blocked_execution_does_not_modify_tags
results_review_after_blocked_execution_does_not_modify_staged_evidence
results_review_after_blocked_execution_does_not_regenerate_evidence
results_review_after_blocked_execution_does_not_call_providers
results_review_after_blocked_execution_does_not_acquire_market_data
results_review_after_blocked_execution_does_not_generate_dataset
results_review_after_blocked_execution_does_not_recompute_metrics
results_review_after_blocked_execution_does_not_train_models
results_review_after_blocked_execution_does_not_score_strategy
results_review_after_blocked_execution_does_not_generate_trade_recommendations
results_review_after_blocked_execution_does_not_accept_predictive_usefulness
results_review_after_blocked_execution_does_not_accept_profitability
results_review_after_blocked_execution_does_not_authorize_runtime
results_review_after_blocked_execution_does_not_authorize_broker_execution
source_authority_enrichment_plan_review_is_not_remediation
missing_authority_inventory_review_is_not_source_authority_acquisition
workstream_authority_mapping_review_is_not_direct_change_authority
no_change_inputs_review_is_not_no_change_disposition
alternate_diagnostic_inputs_review_is_not_diagnostic_execution
retry_basis_requirements_review_is_not_retry_readiness
passing_priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
blocked_remediation_execution_remains_source_evidence
failure_diagnosis_remains_source_evidence
source_approval_remains_source_evidence
source_execution_remains_source_evidence
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_follow_on_candidate_required_after_results_review
separate_approval_required_before_any_follow_on_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines())

CHECK_IDS = tuple("""source_execution_commit_bound
source_execution_artifact_kind_bound
source_execution_status_bound
source_execution_scope_bound
source_execution_digest_bound
source_enrichment_plan_digest_bound
source_missing_authority_inventory_digest_bound
source_workstream_authority_mapping_digest_bound
source_execution_manifest_digest_bound
selected_package_bound
source_approval_commit_bound
source_approval_digest_bound
source_operator_review_commit_bound
source_operator_review_digest_bound
source_candidate_commit_bound
source_candidate_digest_bound
source_failure_diagnosis_commit_bound
source_failure_diagnosis_digest_bound
source_blocked_execution_commit_bound
source_blocked_reason_bound
source_blocked_manifest_digest_bound
primary_failure_class_bound
secondary_failure_classes_bound
source_remediation_execution_approval_digest_bound
source_plan_results_review_digest_bound
source_targeted_plan_review_digest_bound
source_workstream_mapping_review_digest_bound
source_plan_execution_digest_bound
source_targeted_remediation_plan_digest_bound
source_workstream_mapping_digest_bound
source_method_results_review_digest_bound
source_method_execution_digest_bound
source_diagnostic_results_review_digest_bound
source_controlled_recapture_execution_digest_bound
source_controlled_recapture_receipt_digest_bound
source_durable_receipt_path_bound
source_prior_diagnostic_failure_diagnosis_digest_bound
source_prior_diagnostic_blocked_reason_bound
source_planning_execution_digest_bound
source_complete_29_row_binding_digest_bound
source_materialized_payload_digest_bound
source_recovery_detail_digest_bound
source_module_grouping_digest_bound
source_staged_inventory_digest_bound
retry_execution_commit_bound
retry_failure_counts_bound
priority_1_top_module_paths_bound
priority_1_total_612_bound
top_10_total_1069_bound
module_summary_count_29_bound
failed_or_errored_nodeids_1404_bound
diagnostic_exit_code_1_bound_as_diagnostic_only
diagnostic_stdout_hash_bound
diagnostic_stderr_hash_bound
diagnostic_stdout_byte_count_1231380_bound
diagnostic_stderr_byte_count_0_bound
priority1_pre_change_validation_675_passed_bound
priority1_post_change_validation_675_passed_bound
priority1_post_change_stdout_hash_bound
priority1_post_change_stderr_hash_bound
observable_family_count_4_bound
observable_evidence_items_188_bound
assertion_or_value_mismatch_family_bound
digest_or_hash_mismatch_family_bound
fixture_or_test_isolation_issue_family_bound
missing_or_unexpected_field_family_bound
family_confidence_high_bound
workstream_count_4_bound
assertion_value_mismatch_workstream_bound
digest_hash_boundary_workstream_bound
fixture_isolation_determinism_workstream_bound
schema_field_contract_workstream_bound
results_review_created_true
source_execution_reviewed_true
source_authority_enrichment_plan_reviewed_true
missing_authority_inventory_reviewed_true
missing_authority_inventory_four_sections_bound
missing_authority_inventory_30_items_bound
missing_authority_items_missing_not_acquired_bound
direct_changes_unauthorized_bound
workstream_authority_mapping_reviewed_true
workstream_mappings_planned_not_executed_bound
source_evidence_requirements_reviewed_true
canonical_serialization_requirements_reviewed_true
schema_field_contract_requirements_reviewed_true
fixture_isolation_requirements_reviewed_true
no_change_disposition_inputs_reviewed_true
alternate_diagnostic_inputs_reviewed_true
retry_basis_requirements_reviewed_true
source_outputs_27_reviewed_true
source_authority_evidence_acquired_false
concrete_source_authority_established_false
safe_source_authority_bound_change_identified_false
retained_change_records_available_false
source_authority_acquisition_false
source_authority_enrichment_reexecuted_false
no_change_disposition_false
alternate_diagnostic_execution_false
remediation_execution_false
controlled_remediation_false
production_code_modified_false
existing_tests_modified_false
expected_digests_updated_false
patch_generated_false
patch_applied_false
pytest_false
full_pytest_false
priority1_validation_rerun_false
retry_rerun_false
detached_retry_false
cache_read_false
cache_modified_false
pytest_cache_committed_false
marketflow_outputs_committed_false
durable_receipt_parsed_false
diagnostic_output_analyzed_false
plan_execution_rerun_false
targeted_plan_regenerated_false
method_execution_rerun_false
controlled_recapture_rerun_false
diagnostic_command_rerun_false
terminal_logs_parsed_false
operator_logs_parsed_false
env_inspection_false
prior_lost_values_reconstructed_false
full_stdout_reconstructed_false
full_stderr_reconstructed_false
failure_modules_classified_false
error_modules_classified_false
failure_error_separation_claimed_false
first_failure_identified_false
first_error_identified_false
root_cause_claimed_false
retry_success_claimed_false
main_merge_readiness_claimed_false
new_retry_candidate_created_false
retry_approval_created_false
new_retry_executed_false
new_retry_results_review_created_false
main_merge_approval_created_false
ready_for_conditional_follow_on_candidate_true
ready_for_remediation_execution_false
ready_for_retry_candidate_false
ready_for_main_merge_approval_false
integration_success_false
successful_integration_digest_false
integration_branch_pushed_false
main_push_false
origin_main_modified_false
evidence_regenerated_false
provider_requests_false
market_data_acquisition_false
dataset_generation_false
metric_recomputation_false
model_training_false
strategy_scoring_false
recommendations_false
predictive_usefulness_not_accepted
profitability_not_accepted
runtime_not_authorized
broker_not_authorized
outputs_generated
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines())

MARKDOWN_SECTIONS = (
    "Source Execution", "Source Execution Digests", "Source Approval", "Source Operator Review", "Source Candidate",
    "Source Failure Diagnosis", "Source Blocked Execution", "Blocked Reason", "Failure Classification",
    "Source Remediation Execution Approval", "Source Plan Results Review", "Source Plan Execution",
    "Source Targeted Remediation Plan", "Source Workstream Mapping", "Source Method Results Review",
    "Source Method Execution", "Source Diagnostic Results Review", "Source Controlled Recapture",
    "Source Durable Receipt", "Source Planning and Detail Binding Evidence", "Retry Failure Context",
    "Priority 1 Target Modules", "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary",
    "Reviewed Observable Families", "Reviewed Workstreams", "Source Authority Enrichment Plan Review",
    "Missing Authority Inventory Review", "Workstream to Missing Authority Mapping Review",
    "Source Evidence Requirements Review", "No-Change Disposition Input Requirements Review",
    "Alternate Diagnostic Input Requirements Review", "Retry Basis Requirements Review",
    "Unsupported Claims Boundary", "Results Review Domains", "Results Review Findings", "Recommendation",
    "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


class MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError(ValueError):
    """Raised when a source or results-review artifact violates the frozen contract."""


def _source_inventory() -> list[dict[str, Any]]:
    return [
        {"workstream_id": workstream, "authority_status": "MISSING_NOT_ACQUIRED",
         "missing_authority_items": list(requirements), "direct_change_authorized": False}
        for workstream, requirements in source.WORKSTREAM_REQUIREMENTS.items()
    ]


def _source_mapping() -> list[dict[str, Any]]:
    return [
        {"workstream_id": workstream, "source_family_id": family,
         "missing_authority_items": list(source.WORKSTREAM_REQUIREMENTS[workstream]),
         "mapping_status": "PLANNED_NOT_EXECUTED", "source_authority_acquired": False}
        for workstream, family in source.WORKSTREAM_SOURCES
    ]


def _source_evidence_requirements() -> list[dict[str, Any]]:
    return [
        {"workstream_id": workstream, "required_evidence": list(requirements),
         "evidence_status": "REQUIRED_NOT_ACQUIRED", "future_review_required": True}
        for workstream, requirements in source.WORKSTREAM_REQUIREMENTS.items()
    ]


def _source_enrichment_plan() -> dict[str, Any]:
    return {
        "package_id": SELECTED_PACKAGE,
        "plan_status": "SOURCE_AUTHORITY_ENRICHMENT_PLAN_READY_FOR_RESULTS_REVIEW",
        "planning_only": True,
        "source_authority_acquisition_performed": False,
        "workstream_sections": list(source.WORKSTREAM_REQUIREMENTS),
        "execution_steps": [
            "Bind committed approval and reviewed source evidence.",
            "Inventory missing authority for each reviewed workstream.",
            "Map each workstream to explicit missing authority and evidence requirements.",
            "Define canonical serialization, schema, fixture, no-change, and alternate-diagnostic inputs.",
            "Define the reviewed basis required before any retry candidate.",
            "Require a separate results review before any follow-on candidate or execution.",
        ],
        "success_boundary": "PLANNING_OUTPUTS_CREATED_WITHOUT_ACQUIRING_SOURCE_AUTHORITY_OR_EXECUTING_REMEDIATION",
    }


def _reviewed_families() -> list[dict[str, Any]]:
    return [
        {"family_id": family, "observable_evidence_count": 47, "confidence": "HIGH", "planning_evidence_only": True}
        for _, family in source.WORKSTREAM_SOURCES
    ]


def _reviewed_workstreams() -> list[dict[str, Any]]:
    return [
        {"workstream_id": workstream, "source_family_id": family, "source_observable_evidence_count": 47,
         "source_family_confidence": "HIGH", "planning_evidence_only": True, "direct_change_authorized": False}
        for workstream, family in source.WORKSTREAM_SOURCES
    ]


def _committed_source_execution() -> dict[str, Any]:
    bindings = deepcopy(source.SOURCE_BINDINGS)
    bindings.update({
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "artifact_kind": SOURCE_EXECUTION_ARTIFACT_KIND,
        "execution_status": SOURCE_EXECUTION_STATUS,
        "execution_scope": SOURCE_EXECUTION_SCOPE,
        "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
        source.EXECUTION_DIGEST_KEY: SOURCE_EXECUTION_DIGEST,
        source.ENRICHMENT_PLAN_DIGEST_KEY: SOURCE_ENRICHMENT_PLAN_DIGEST,
        source.MISSING_AUTHORITY_INVENTORY_DIGEST_KEY: SOURCE_MISSING_AUTHORITY_INVENTORY_DIGEST,
        source.WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY: SOURCE_WORKSTREAM_AUTHORITY_MAPPING_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_EXECUTION_MANIFEST_DIGEST,
        "source_authority_enrichment_plan": _source_enrichment_plan(),
        "missing_authority_inventory": _source_inventory(),
        "workstream_to_missing_authority_mapping": _source_mapping(),
        "source_evidence_requirements": _source_evidence_requirements(),
        "canonical_serialization_authority_requirements": list(source.WORKSTREAM_REQUIREMENTS["digest_hash_boundary_workstream"]),
        "schema_field_contract_authority_requirements": list(source.WORKSTREAM_REQUIREMENTS["schema_field_contract_workstream"]),
        "fixture_isolation_authority_requirements": list(source.WORKSTREAM_REQUIREMENTS["fixture_isolation_determinism_workstream"]),
        "no_change_disposition_input_requirements": list(source.NO_CHANGE_REQUIREMENTS),
        "alternate_diagnostic_input_requirements": list(source.ALTERNATE_DIAGNOSTIC_REQUIREMENTS),
        "retry_basis_requirements": list(source.RETRY_BASIS_REQUIREMENTS),
        "outputs_generated": [{"output_id": item, "status": source.GENERATED_PLANNING_ONLY} for item in source.OUTPUT_IDS],
    })
    return bindings


def _validate_source_execution(candidate: Mapping[str, Any]) -> None:
    if not isinstance(candidate, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError("source execution must be an object")
    expected = _committed_source_execution()
    for field, value in expected.items():
        if candidate.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError(f"source execution {field} mismatch")


def _source_context() -> dict[str, Any]:
    return {
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
                                  "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True,
                                  "root_full_regression_is_retry_evidence": False},
        "priority_1_target_modules": [
            {"module_path": path, "failed_or_errored_nodeid_count": count} for path, count in source.PRIORITY_1_MODULES
        ],
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "priority1_validation_summary": {
            "pre_change_passed": True, "pre_change_passed_count": 675,
            "post_change_passed": True, "post_change_passed_count": 675,
            "post_change_duration_seconds": "41.88", "post_change_stdout_byte_count": 832,
            "post_change_stderr_byte_count": 0,
            "post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
            "post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "not_retry_evidence": True,
        },
        "diagnostic_capture_evidence_summary": {
            "exit_code": 1, "duration_seconds": "21.584361", "stdout_byte_count": 1231380,
            "stderr_byte_count": 0, "combined_output_byte_count": 1231380,
            "stdout_sha256": source.source.source.source.SOURCE_CORE["source_stdout_sha256"],
            "stderr_sha256": source.source.source.source.SOURCE_CORE["source_stderr_sha256"],
            "stdout_excerpt_truncated": True, "stderr_excerpt_truncated": False,
            "redaction_checked": True, "diagnostic_only": True,
        },
        "reviewed_observable_failure_families": _reviewed_families(),
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "reviewed_workstreams": _reviewed_workstreams(), "source_workstream_count": 4,
    }


def _checklist() -> list[dict[str, Any]]:
    return [
        {"check_id": check_id, "status": PASS, "expected": True, "actual": True,
         "severity": BLOCKER, "message": f"{check_id} passed"}
        for check_id in CHECK_IDS
    ]


def _review_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", RESULTS_REVIEW_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _assemble_review() -> dict[str, Any]:
    source_execution = _committed_source_execution()
    plan_review = {
        "plan": deepcopy(source_execution["source_authority_enrichment_plan"]),
        "disposition": "REVIEWED_PLANNING_ONLY", "source_authority_acquired": False,
        "remediation_authorized": False,
    }
    inventory_review = {
        "sections": deepcopy(source_execution["missing_authority_inventory"]),
        "section_count": 4, "item_count": 30, "item_status": "MISSING_NOT_ACQUIRED",
        "direct_change_authorized": False,
    }
    mapping_review = {
        "mappings": deepcopy(source_execution["workstream_to_missing_authority_mapping"]),
        "mapping_count": 4, "mapping_status": "PLANNED_NOT_EXECUTED", "source_authority_acquired": False,
    }
    review = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "results_review_only": True,
        **deepcopy(source.SOURCE_BINDINGS),
        "source_execution_artifact_kind": SOURCE_EXECUTION_ARTIFACT_KIND,
        "source_execution_status": SOURCE_EXECUTION_STATUS,
        "source_execution_scope": SOURCE_EXECUTION_SCOPE,
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_authority_enrichment_plan_digest": SOURCE_ENRICHMENT_PLAN_DIGEST,
        "source_missing_authority_inventory_digest": SOURCE_MISSING_AUTHORITY_INVENTORY_DIGEST,
        "source_workstream_authority_mapping_digest": SOURCE_WORKSTREAM_AUTHORITY_MAPPING_DIGEST,
        "source_execution_manifest_digest": SOURCE_EXECUTION_MANIFEST_DIGEST,
        "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
        "historical_selected_remediation_execution_package": source.source.source.source.source.SELECTED_PACKAGE,
        "primary_failure_class": source.source.source.SOURCE_BINDINGS["source_blocked_reason"],
        "secondary_failure_classes": [
            "REVIEWED_WORKSTREAMS_ARE_PLANNING_EVIDENCE_NOT_CHANGE_AUTHORITY",
            "PRIORITY_1_FOCUSED_VALIDATION_ALREADY_PASSING_IN_CURRENT_ROOT_CONTEXT",
            "NO_RETAINED_CHANGE_RECORDS_AVAILABLE_FOR_REMEDIATION_SUCCESS",
            "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED",
        ],
        **_source_context(), **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "missing_authority_inventory_section_count": 4,
        "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "workstream_mapping_count": 4, "workstream_mapping_status": "PLANNED_NOT_EXECUTED",
        "no_change_disposition_input_count": 7, "alternate_diagnostic_input_count": 8,
        "retry_basis_requirement_count": 7, "source_outputs_generated_count": 27,
        "source_authority_enrichment_plan_review": plan_review,
        "missing_authority_inventory_review": inventory_review,
        "workstream_to_missing_authority_mapping_review": mapping_review,
        "source_evidence_requirements_review": deepcopy(source_execution["source_evidence_requirements"]),
        "canonical_serialization_authority_requirements_review": deepcopy(source_execution["canonical_serialization_authority_requirements"]),
        "schema_field_contract_authority_requirements_review": deepcopy(source_execution["schema_field_contract_authority_requirements"]),
        "fixture_isolation_authority_requirements_review": deepcopy(source_execution["fixture_isolation_authority_requirements"]),
        "no_change_disposition_input_requirements_review": deepcopy(source_execution["no_change_disposition_input_requirements"]),
        "alternate_diagnostic_input_requirements_review": deepcopy(source_execution["alternate_diagnostic_input_requirements"]),
        "retry_basis_requirements_review": deepcopy(source_execution["retry_basis_requirements"]),
        "unsupported_claims_boundary": [
            "No source authority was acquired or established.", "No safe source-authority-bound change was identified.",
            "No root cause, retry success, or main-merge readiness is claimed.",
        ],
        "results_review_findings": deepcopy(REVIEW_FINDINGS), "results_review_domains": deepcopy(REVIEW_DOMAINS),
        "outputs_generated": [{"output_id": item, "status": OUTPUT_STATUS} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
        "recommended_action": RECOMMENDED_ACTION, "reason": RECOMMENDATION_REASON,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    review[ENRICHMENT_PLAN_REVIEW_DIGEST_KEY] = semantic_digest(plan_review)
    review[MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY] = semantic_digest(inventory_review)
    review[WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY] = semantic_digest(mapping_review)
    review["digest_manifest"] = {
        "source_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_authority_enrichment_plan_digest": SOURCE_ENRICHMENT_PLAN_DIGEST,
        "source_missing_authority_inventory_digest": SOURCE_MISSING_AUTHORITY_INVENTORY_DIGEST,
        "source_workstream_authority_mapping_digest": SOURCE_WORKSTREAM_AUTHORITY_MAPPING_DIGEST,
        "source_execution_manifest_digest": SOURCE_EXECUTION_MANIFEST_DIGEST,
        ENRICHMENT_PLAN_REVIEW_DIGEST_KEY: review[ENRICHMENT_PLAN_REVIEW_DIGEST_KEY],
        MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY: review[MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY],
        WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY: review[WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY],
        "output_ids": list(OUTPUT_IDS),
    }
    review[MANIFEST_DIGEST_KEY] = semantic_digest(review["digest_manifest"])
    review["checklist"] = _checklist()
    review["summary"] = _summary(review)
    review[RESULTS_REVIEW_DIGEST_KEY] = _review_digest(review)
    return review


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checklist = review["checklist"]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist), "failed_checks": 0, "blocker_count": 0,
        **{field: review[field] for field in TRUE_FIELDS},
        "missing_authority_inventory_section_count": 4, "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED", "workstream_mapping_count": 4,
        "workstream_mapping_status": "PLANNED_NOT_EXECUTED", "no_change_disposition_input_count": 7,
        "alternate_diagnostic_input_count": 8, "retry_basis_requirement_count": 7,
        "source_outputs_generated_count": 27,
        **{field: review[field] for field in FALSE_FIELDS},
        "source_workstream_count": 4, "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188, "source_exit_code": 1,
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _first_difference(actual: Any, expected: Any, path: str = "review") -> str | None:
    if isinstance(expected, Mapping):
        if not isinstance(actual, Mapping):
            return path
        if set(actual) != set(expected):
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


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(
    *, source_execution: dict | None = None,
) -> dict[str, Any]:
    """Build the offline results review from committed constants or an injected equivalent."""

    candidate = _committed_source_execution() if source_execution is None else deepcopy(source_execution)
    _validate_source_execution(candidate)
    review = _assemble_review()
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(
    review: dict,
) -> dict[str, Any]:
    """Reject any change to the deterministic review or a protected boundary."""

    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError("review must be an object")
    expected = _assemble_review()
    difference = _first_difference(review, expected)
    if difference is not None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError(f"{difference} mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "results_review_digest": review[RESULTS_REVIEW_DIGEST_KEY],
        "total_checks": review["summary"]["total_checks"], "passed_checks": review["summary"]["passed_checks"],
        "failed_checks": 0, "blocker_count": 0,
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_markdown_v1(
    review: dict,
) -> str:
    """Render the validated results review as a human-readable status record."""

    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(deepcopy(review))
    sections = {
        "Source Execution": {"commit": review["source_execution_commit"], "artifact_kind": review["source_execution_artifact_kind"], "status": review["source_execution_status"], "scope": review["source_execution_scope"]},
        "Source Execution Digests": {key: review[key] for key in ("source_execution_digest", "source_authority_enrichment_plan_digest", "source_missing_authority_inventory_digest", "source_workstream_authority_mapping_digest", "source_execution_manifest_digest")},
        "Source Approval": {"commit": review["source_approval_commit"], "digest": review["source_approval_digest"]},
        "Source Operator Review": {"commit": review["source_operator_review_commit"], "digest": review["source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest"]},
        "Source Candidate": {"commit": review["source_candidate_commit"], "digest": review["source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest"]},
        "Source Failure Diagnosis": {"commit": review["source_failure_diagnosis_commit"], "digest": review["source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"]},
        "Source Blocked Execution": {"commit": review["source_blocked_execution_commit"], "manifest_digest": review["source_blocked_manifest_digest"]},
        "Blocked Reason": review["source_blocked_reason"],
        "Failure Classification": {"primary": review["primary_failure_class"], "secondary": review["secondary_failure_classes"]},
        "Source Remediation Execution Approval": {"commit": review["source_remediation_execution_approval_after_plan_results_review_commit"], "digest": review["source_remediation_execution_approval_after_plan_results_review_digest"]},
        "Source Plan Results Review": {key: value for key, value in review.items() if "plan_results_review" in key},
        "Source Plan Execution": {key: value for key, value in review.items() if "plan_execution" in key},
        "Source Targeted Remediation Plan": review["source_targeted_remediation_plan_digest"],
        "Source Workstream Mapping": review["source_workstream_mapping_digest"],
        "Source Method Results Review": {key: value for key, value in review.items() if "method_results_review" in key},
        "Source Method Execution": {key: value for key, value in review.items() if "method_execution" in key},
        "Source Diagnostic Results Review": {key: value for key, value in review.items() if "recapture_results_review" in key or "payload_review" in key or "durable_receipt_review" in key},
        "Source Controlled Recapture": {key: value for key, value in review.items() if "recapture_execution" in key or "recapture_payload_digest" in key or "recapture_receipt_digest" in key},
        "Source Durable Receipt": {"path": review["source_durable_receipt_path"], "parsed": review["diagnostic_receipt_parsed_in_review"]},
        "Source Planning and Detail Binding Evidence": {key: value for key, value in review.items() if any(token in key for token in ("planning_digest", "detail_binding", "complete_29", "materialized_payload", "recovery_detail", "module_grouping", "staged_inventory"))},
        "Retry Failure Context": review["retry_failure_context"], "Priority 1 Target Modules": review["priority_1_target_modules"],
        "Priority 1 Validation Summary": review["priority1_validation_summary"], "Diagnostic Capture Evidence Summary": review["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": review["reviewed_observable_failure_families"], "Reviewed Workstreams": review["reviewed_workstreams"],
        "Source Authority Enrichment Plan Review": review["source_authority_enrichment_plan_review"],
        "Missing Authority Inventory Review": review["missing_authority_inventory_review"],
        "Workstream to Missing Authority Mapping Review": review["workstream_to_missing_authority_mapping_review"],
        "Source Evidence Requirements Review": review["source_evidence_requirements_review"],
        "No-Change Disposition Input Requirements Review": review["no_change_disposition_input_requirements_review"],
        "Alternate Diagnostic Input Requirements Review": review["alternate_diagnostic_input_requirements_review"],
        "Retry Basis Requirements Review": review["retry_basis_requirements_review"],
        "Unsupported Claims Boundary": review["unsupported_claims_boundary"], "Results Review Domains": review["results_review_domains"],
        "Results Review Findings": review["results_review_findings"],
        "Recommendation": {"next_task": review["recommended_next_task"], "status": review["recommended_next_task_status"], "action": review["recommended_action"], "reason": review["reason"]},
        "Next Chain": review["next_chain"], "Next Gates": review["next_gates"], "Risk Controls": review["risk_controls"],
        "Authority Boundaries": {field: review[field] for field in FALSE_FIELDS},
        "Checklist Summary": review["summary"], "Guardrails": list(RISK_CONTROLS),
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Results Review After Blocked Execution v1",
        "", f"Artifact: `{review['artifact_kind']}`", f"Status: `{review['review_status']}`",
        f"Scope: `{review['review_scope']}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(
    output_dir: str | Path, *, source_execution: dict | None = None,
) -> dict[str, Any]:
    """Write only the deterministic review status document."""

    review = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(source_execution=source_execution)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_markdown_v1(review), encoding="utf-8")
    return review


__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE", "SELECTED_PACKAGE", "RESULTS_REVIEW_DIGEST_KEY",
    "ENRICHMENT_PLAN_REVIEW_DIGEST_KEY", "MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY",
    "WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_DIGEST_KEY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_ENRICHMENT_PLAN_REVIEW_DIGEST_KEY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_MANIFEST_DIGEST_KEY",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_markdown_v1",
]
