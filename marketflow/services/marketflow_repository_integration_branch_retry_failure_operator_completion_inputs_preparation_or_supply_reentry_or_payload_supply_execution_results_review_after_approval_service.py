"""Review the approved payload-supply mechanism execution without rerunning it.

The review is deterministic, offline, and governance-only.  It verifies a
committed mechanism-definition execution while preserving the absence of any
operator payload, evidence, source authority, remediation, retry, merge,
runtime, broker, or trading authority.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1"
RESULTS_REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_READY"
RESULTS_REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
GENERATED_OUTPUT_STATUS = "GENERATED_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_MECHANISM_EXECUTION_RESULTS_REVIEW_ONLY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_CANDIDATE_AFTER_PAYLOAD_SUPPLY_MECHANISM_RESULTS_REVIEW_V1"

SOURCE_EXECUTION_COMMIT = "615c06c21360100c44a5f82c53a8d1606fd27e67"
SOURCE_EXECUTION_DIGEST = "e91075b6e70592c63b83b7614f1445d7ec2af7129a0675a0fc51031b5759ccb7"
SOURCE_PAYLOAD_SUPPLY_MECHANISM_DIGEST = "51c6d7f9c64f6e90a986a1fd93be987ec98fba6d241337caab46b8d72840b123"
SOURCE_OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST = "6c17ab33380e6a758e53012111bbe33d653acdda597b950d02b49d8b17e28574"
SOURCE_ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST = "cf1d5b5174fcc62336dd74a10728e6a61788d395d3a751524a4bbd40d92cf5e5"
SOURCE_WORKSTREAM_SUPPLY_PLAN_DIGEST = "6ebd76ad3559dd758b4aa34faaccd1a5b02c742283f5155e6a77740054fe4149"
SOURCE_EXECUTION_SOURCE_BINDING_DIGEST = "aad8a414581b2a42c87617a75fba94853f46c66ae85a705252bbe780dd328b5f"
SOURCE_EXECUTION_MANIFEST_DIGEST = "765c97e5993bfe090ada473cf1457abbdbd9501b35185bf08a774f8c9ec40539"

RESULTS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_digest"
PAYLOAD_SUPPLY_MECHANISM_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_payload_supply_mechanism_review_digest"
OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_operator_payload_submission_schema_review_digest"
ALLOWED_VALUES_AND_SECRET_SCREENING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_allowed_values_and_secret_screening_review_digest"
WORKSTREAM_SUPPLY_PLAN_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_workstream_supply_plan_review_digest"
SOURCE_BINDING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_source_binding_review_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_READY = RESULTS_REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = RESULTS_REVIEW_SCOPE
PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY = SELECTED_PACKAGE

SOURCE_EXECUTION_BINDINGS = {
    "source_execution_commit": SOURCE_EXECUTION_COMMIT,
    "source_execution_artifact_kind": source.ARTIFACT_KIND,
    "source_execution_status": source.EXECUTION_STATUS,
    "source_execution_scope": source.EXECUTION_SCOPE,
    "source_execution_digest": SOURCE_EXECUTION_DIGEST,
    "source_payload_supply_mechanism_digest": SOURCE_PAYLOAD_SUPPLY_MECHANISM_DIGEST,
    "source_operator_payload_submission_schema_digest": SOURCE_OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST,
    "source_allowed_values_and_secret_screening_digest": SOURCE_ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST,
    "source_workstream_supply_plan_digest": SOURCE_WORKSTREAM_SUPPLY_PLAN_DIGEST,
    "source_execution_source_binding_digest": SOURCE_EXECUTION_SOURCE_BINDING_DIGEST,
    "source_execution_manifest_digest": SOURCE_EXECUTION_MANIFEST_DIGEST,
    "source_selected_package": SELECTED_PACKAGE,
    "source_selected_package_executed": True,
    "source_payload_supply_mechanism_created": True,
    "source_payload_supply_mechanism_status": source.MECHANISM_STATUS,
}

TRUE_FIELDS = tuple("""operator_completion_inputs_reentry_or_payload_supply_execution_results_review_created
operator_completion_inputs_reentry_or_payload_supply_execution_results_review_ready
source_execution_bound
source_execution_reviewed
source_execution_status_verified
source_execution_scope_verified
source_execution_digest_verified
source_payload_supply_mechanism_digest_verified
source_operator_payload_submission_schema_digest_verified
source_allowed_values_and_secret_screening_digest_verified
source_workstream_supply_plan_digest_verified
source_execution_source_binding_digest_verified
source_execution_manifest_digest_verified
source_selected_package_bound
source_selected_package_executed_verified
source_payload_supply_mechanism_created_verified
payload_supply_mechanism_definition_reviewed
operator_payload_submission_schema_reviewed
operator_payload_field_checklist_reviewed
allowed_values_matrix_reviewed
secret_screening_guidance_reviewed
workstream_segmented_payload_supply_plan_reviewed
results_review_prerequisite_reviewed
future_completion_reattempt_prerequisite_reviewed
downstream_gates_reviewed
future_payload_supply_contract_reviewed
future_requirements_reviewed
future_plan_reviewed
planned_outputs_reviewed
supporting_packages_preserved_unselected
blocked_packages_preserved_blocked
source_approval_bound
source_operator_review_bound
source_candidate_bound
source_failure_diagnosis_bound
source_blocked_input_preparation_execution_bound
source_blocked_reason_verified
source_success_digests_absent_verified
operator_completion_inputs_absence_preserved
execution_correctly_governed
no_input_inference_verified
approval_not_input_verified
template_placeholder_boundary_preserved
diagnostic_output_boundary_preserved
synthetic_success_path_test_only_verified
source_prior_approval_bound
source_prior_operator_review_bound
source_prior_candidate_bound
source_prior_completion_failure_diagnosis_bound
source_completion_execution_bound
source_completion_approval_bound
source_completion_candidate_operator_review_bound
source_completion_candidate_bound
source_template_preparation_results_review_bound
source_template_preparation_execution_bound
source_preparation_failure_acquisition_chain_bound
follow_on_enrichment_historical_digests_bound
plan_method_diagnostic_recovery_digests_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
priority1_validation_not_retry_evidence
diagnostic_metadata_bound
observable_families_bound
reviewed_workstreams_bound
reviewed_template_structure_bound
reviewed_template_rows_bound
template_not_actual_evidence_package_verified
template_not_source_authority_verified
template_not_acquired_evidence_verified
template_not_acquisition_success_verified
actual_coverage_zero_bound
evidence_package_absence_bound
missing_authority_inventory_bound
count_label_distinction_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_if_explicit_payload_supplied_and_selected""".split())

FALSE_FIELDS = tuple("""source_execution_rerun_performed
payload_supply_mechanism_regenerated
operator_payload_created
operator_completion_inputs_supplied_to_results_review
operator_completion_inputs_prepared
operator_completion_inputs_supplied
operator_completion_inputs_provided
operator_completion_inputs_shape_validated_as_actual_payload
operator_completion_inputs_secret_screened_as_actual_payload
operator_completion_inputs_validated_as_evidence
operator_completion_inputs_bound_as_evidence
operator_completion_inputs_bound
operator_completion_inputs_contained_secrets
prepared_operator_completion_inputs_for_results_review
operator_completion_inputs_preparation_or_supply_execution_reattempt_created
operator_completion_inputs_preparation_or_supply_execution_reattempt_performed
operator_completion_inputs_preparation_or_supply_results_review_created
operator_source_authority_evidence_package_completion_executed
operator_source_authority_evidence_package_completed
operator_source_authority_evidence_package_created
operator_source_authority_evidence_package_supplied
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
operator_source_authority_evidence_package_accepted_as_source_authority
actual_evidence_items_filled
actual_evidence_items_supplied
actual_evidence_items_validated
actual_evidence_items_bound
source_authority_acquisition_execution_created
source_authority_acquisition_execution_performed
source_authority_acquisition_performed
source_authority_evidence_acquired
external_evidence_acquired
source_authority_evidence_items_bound_for_results_review
source_authority_evidence_mapping_created
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
pytest_performed_in_results_review
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_results_review
diagnostic_output_analyzed_in_results_review
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_results_review
method_execution_rerun_performed
controlled_recapture_rerun_performed
template_execution_rerun_performed
completion_execution_rerun_performed
input_preparation_or_supply_execution_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_results_review
cache_modified_in_results_review
pytest_cache_committed
marketflow_outputs_committed
terminal_logs_parsed
operator_logs_parsed
env_inspection_performed
source_owners_contacted
external_documents_read
provider_requests_made_in_results_review
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
ready_for_operator_completion_inputs_preparation_or_supply_execution_reattempt
ready_for_operator_completion_inputs_preparation_or_supply_results_review
ready_for_operator_source_authority_evidence_package_completion_execution
ready_for_operator_source_authority_evidence_package_completion_results_review
ready_for_source_authority_acquisition_execution_retry
ready_for_source_authority_acquisition_results_review
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
market_data_acquisition_performed_in_results_review
dataset_generation_performed_in_results_review
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated
predictive_usefulness_accepted
profitability_accepted
runtime_authorized
strategy_authorized
paper_trading_authorized
broker_execution_authorized""".split())

COUNTS = {
    "operator_source_authority_evidence_item_count": 0,
    "operator_source_authority_evidence_item_template_count": 30,
    "reviewed_template_row_count": 30,
    "actual_covered_missing_authority_item_count": 0,
    "actual_uncovered_missing_authority_item_count": 30,
    "template_mapped_missing_authority_item_count": 30,
    "mapped_missing_authority_item_count": 30,
    "completed_operator_evidence_item_count": 0,
    "operator_completion_input_item_count": 0,
    "future_operator_completion_input_item_count": 30,
    "prepared_operator_completion_input_item_count": 0,
    "payload_supply_mechanism_item_count": 30,
    "payload_supply_mechanism_section_count": 4,
    "package_header_schema_field_count": 14,
    "evidence_item_schema_field_count": 21,
    "workstream_segment_count": 4,
    "workstream_segment_item_counts": [8, 8, 7, 7],
    "acquisition_scope_section_count": 4,
    "acceptable_source_artifact_type_count": 13,
    "allowed_evidence_classification_count": 12,
    "secret_screening_indicator_count": 13,
    "pre_submission_checklist_field_count": 34,
    "source_execution_governance_output_record_count": 42,
    "operator_provided_evidence_requirement_count": 10,
    "evidence_custody_and_digest_requirement_count": 6,
    "candidate_results_review_requirement_count": 16,
    "observable_failure_family_count": 4,
    "total_observable_evidence_items": 188,
    "priority_1_total_nodeids": 612,
    "top_10_count_sum": 1069,
    "failed_or_errored_nodeids_count": 1404,
    "module_summary_module_count": 29,
    "package_option_count": 12,
    "available_package_count": 7,
    "supporting_package_count": 6,
    "blocked_package_count": 5,
    "future_requirement_count": 62,
    "future_plan_step_count": 15,
    "planned_output_count": 34,
    "non_goal_count": 78,
    "risk_control_count": 112,
    "operator_review_enumerated_non_goal_count": 90,
    "operator_review_enumerated_risk_control_count": 132,
    "approval_enumerated_risk_control_count": 146,
    "source_execution_risk_control_count": 246,
}

OUTPUT_IDS = tuple("""operator_completion_inputs_reentry_or_payload_supply_execution_results_review_manifest
source_execution_binding_report
source_execution_digest_review_report
source_selected_package_execution_review_report
source_payload_supply_mechanism_review_report
operator_payload_submission_schema_review_report
operator_payload_field_checklist_review_report
allowed_values_matrix_review_report
secret_screening_guidance_review_report
workstream_segmented_payload_supply_plan_review_report
results_review_prerequisite_review_report
source_approval_binding_report
source_operator_review_binding_report
source_candidate_binding_report
source_failure_diagnosis_binding_report
source_blocked_execution_binding_report
source_blocked_reason_report
source_success_digests_absence_report
source_prior_approval_binding_report
source_prior_operator_review_binding_report
source_prior_candidate_binding_report
source_prior_completion_failure_diagnosis_binding_report
source_completion_execution_binding_report
source_completion_approval_binding_report
source_completion_candidate_operator_review_binding_report
source_completion_candidate_binding_report
source_template_preparation_results_review_binding_report
source_template_preparation_execution_binding_report
source_preparation_failure_acquisition_chain_binding_report
follow_on_enrichment_historical_binding_report
plan_method_diagnostic_recovery_binding_report
durable_receipt_opaque_reference_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
reviewed_template_structure_report
actual_evidence_absence_report
actual_coverage_zero_report
missing_authority_inventory_report
count_label_distinction_report
source_authority_gap_preservation_report
unsupported_claims_boundary_report
downstream_gate_preservation_report
digest_manifest""".split())

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Execution Reattempt Candidate After Payload Supply Mechanism Results Review v1, only if explicit non-secret operator payload is available and selected.",
    "Operator Completion Inputs Preparation or Supply Execution Reattempt Candidate Operator Review v1.",
    "Operator Completion Inputs Preparation or Supply Execution Reattempt Approval v1, if selected.",
    "Operator Completion Inputs Preparation or Supply Execution Reattempt v1, only with explicit non-secret operator payload.",
    "Operator Completion Inputs Preparation or Supply Results Review v1, only if explicit non-secret inputs are prepared or supplied.",
    "Operator Source Authority Evidence Package Completion Execution Reattempt v1, only if reviewed explicit non-secret operator inputs exist and reattempt is separately approved.",
    "Operator Source Authority Evidence Package Completion Results Review v1, only if a completed package exists.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Completed Evidence Package v1, only if separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional disposition, diagnostic, remediation re-entry, retry-criteria, or hold candidate only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple("""operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_if_explicit_payload_available
operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review
operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_if_selected
operator_completion_inputs_preparation_or_supply_execution_reattempt_with_explicit_non_secret_payload_if_approved
operator_completion_inputs_preparation_or_supply_results_review_if_prepared_inputs_exist
operator_source_authority_evidence_package_completion_execution_reattempt_if_reviewed_inputs_exist_and_approved
operator_source_authority_evidence_package_completion_results_review_if_completed_package_exists
source_authority_acquisition_execution_reattempt_with_reviewed_completed_evidence_package_if_approved
source_authority_acquisition_results_review_if_evidence_bound
no_change_disposition_candidate_if_supported_by_reviewed_acquired_evidence
alternate_diagnostic_candidate_if_supported_by_reviewed_acquired_evidence
remediation_reentry_candidate_if_supported_by_reviewed_acquired_evidence
no_change_retry_criteria_candidate_if_supported_by_reviewed_acquired_evidence
hold_disposition_if_supported
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".split())

_REVIEW_RISK_CONTROLS = tuple("""results_review_does_not_execute_package
results_review_does_not_regenerate_payload_supply_mechanism
results_review_does_not_create_operator_payload
results_review_does_not_prepare_inputs
results_review_does_not_supply_inputs
results_review_does_not_provide_inputs
results_review_does_not_validate_inputs_as_evidence
results_review_does_not_bind_inputs_as_evidence
results_review_does_not_create_prepared_inputs
results_review_does_not_create_completed_evidence_package
results_review_does_not_create_evidence_package
results_review_does_not_fill_actual_evidence_items
results_review_does_not_validate_evidence
results_review_does_not_bind_evidence
results_review_does_not_accept_evidence_as_source_authority
results_review_does_not_infer_inputs_from_template
results_review_does_not_infer_inputs_from_placeholders
results_review_does_not_infer_inputs_from_diagnostic_output
results_review_does_not_infer_inputs_from_digests
results_review_does_not_read_cache_for_inputs
results_review_does_not_parse_logs_for_inputs
results_review_does_not_inspect_env_for_inputs
results_review_does_not_read_external_documents_for_inputs
results_review_does_not_call_providers_for_inputs
results_review_does_not_contact_source_owners_for_inputs
results_review_does_not_acquire_source_authority
results_review_does_not_acquire_source_authority_evidence
results_review_does_not_acquire_external_evidence
results_review_does_not_create_source_authority_acquisition_execution
results_review_does_not_retry_source_authority_acquisition
results_review_does_not_create_no_change_disposition
results_review_does_not_execute_alternate_diagnostics
results_review_does_not_execute_remediation
results_review_does_not_modify_production_code
results_review_does_not_modify_existing_tests
results_review_does_not_update_expected_digests
results_review_does_not_generate_patch
results_review_does_not_apply_patch
results_review_does_not_run_pytest
results_review_does_not_run_full_pytest
results_review_does_not_rerun_priority1_validation
results_review_does_not_rerun_retry
results_review_does_not_rerun_detached_retry
results_review_does_not_parse_durable_receipt
results_review_does_not_analyze_diagnostic_output
results_review_does_not_rerun_source_authority_enrichment
results_review_does_not_rerun_follow_on_execution
results_review_does_not_rerun_plan_execution
results_review_does_not_regenerate_targeted_plan
results_review_does_not_rerun_method_execution
results_review_does_not_rerun_controlled_recapture
results_review_does_not_rerun_template_execution
results_review_does_not_rerun_completion_execution
results_review_does_not_rerun_input_preparation_execution
results_review_does_not_run_diagnostic_command
results_review_does_not_read_pytest_cache
results_review_does_not_modify_pytest_cache
results_review_does_not_commit_pytest_cache
results_review_does_not_commit_marketflow_outputs
results_review_does_not_parse_terminal_logs
results_review_does_not_parse_operator_logs
results_review_does_not_inspect_env
results_review_does_not_contact_source_owners
results_review_does_not_read_external_documents
results_review_does_not_reconstruct_prior_lost_values
results_review_does_not_reconstruct_full_streams
results_review_does_not_classify_modules_again
results_review_does_not_classify_full_retry_failures
results_review_does_not_classify_full_retry_errors
results_review_does_not_claim_failure_error_separation
results_review_does_not_identify_authoritative_first_failure
results_review_does_not_identify_authoritative_first_error
results_review_does_not_claim_traceback_root_cause
results_review_does_not_claim_root_cause
results_review_does_not_claim_retry_success
results_review_does_not_claim_main_merge_readiness
results_review_does_not_create_retry_candidate
results_review_does_not_create_retry_approval
results_review_does_not_create_retry_execution
results_review_does_not_create_retry_results_review
results_review_does_not_create_main_merge_approval
results_review_does_not_push_main
results_review_does_not_push_integration_branch
results_review_does_not_delete_integration_branch
results_review_does_not_delete_worktree
results_review_does_not_force_push
results_review_does_not_modify_tags
results_review_does_not_regenerate_evidence
results_review_does_not_call_providers
results_review_does_not_acquire_market_data
results_review_does_not_generate_dataset
results_review_does_not_recompute_metrics
results_review_does_not_train_models
results_review_does_not_score_strategy
results_review_does_not_generate_trade_recommendations
results_review_does_not_accept_predictive_usefulness
results_review_does_not_accept_profitability
results_review_does_not_authorize_runtime
results_review_does_not_authorize_broker_execution
payload_supply_mechanism_definition_is_not_payload_supply
payload_supply_mechanism_definition_is_not_input_preparation
payload_supply_mechanism_definition_is_not_evidence_completion
payload_supply_mechanism_definition_is_not_source_authority_acquisition
future_explicit_non_secret_payload_required_before_input_preparation_or_supply_reattempt
prepared_inputs_require_results_review_before_completion_use
completed_package_requires_results_review_before_acquisition_use
evidence_binding_requires_separate_acquisition_execution
evidence_binding_requires_results_review
acquisition_results_review_required_before_no_change_disposition
acquisition_results_review_required_before_alternate_diagnostic
acquisition_results_review_required_before_remediation
separate_completion_reattempt_requires_reviewed_operator_inputs
separate_remediation_approval_required_before_code_or_test_changes
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".split())
RISK_CONTROLS = tuple(dict.fromkeys((*source.RISK_CONTROLS, *_REVIEW_RISK_CONTROLS)))


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError(ValueError):
    """Raised when source bindings or results-review boundaries drift."""


def _first_difference(actual: Any, expected: Any, path: str = "results_review") -> str | None:
    if type(actual) is not type(expected):
        return path
    if isinstance(expected, Mapping):
        if set(actual) != set(expected):
            return f"{path}.keys"
        for key in expected:
            difference = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if difference:
                return difference
        return None
    if isinstance(expected, list):
        if len(actual) != len(expected):
            return path
        for index, item in enumerate(expected):
            difference = _first_difference(actual[index], item, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


def _validate_source_execution(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError("source_execution must be an object")
    artifact_keys = {
        "artifact_kind": source.ARTIFACT_KIND,
        "execution_status": source.EXECUTION_STATUS,
        "execution_scope": source.EXECUTION_SCOPE,
        source.EXECUTION_DIGEST_KEY: SOURCE_EXECUTION_DIGEST,
        source.PAYLOAD_SUPPLY_MECHANISM_DIGEST_KEY: SOURCE_PAYLOAD_SUPPLY_MECHANISM_DIGEST,
        source.OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST_KEY: SOURCE_OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST,
        source.ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST_KEY: SOURCE_ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST,
        source.WORKSTREAM_SUPPLY_PLAN_DIGEST_KEY: SOURCE_WORKSTREAM_SUPPLY_PLAN_DIGEST,
        source.SOURCE_BINDING_DIGEST_KEY: SOURCE_EXECUTION_SOURCE_BINDING_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_EXECUTION_MANIFEST_DIGEST,
        "selected_package": SELECTED_PACKAGE,
        "selected_package_executed": True,
        "payload_supply_mechanism_created": True,
        "payload_supply_mechanism_status": source.MECHANISM_STATUS,
    }
    if "artifact_kind" in value:
        expected = artifact_keys
    else:
        if set(value) != set(SOURCE_EXECUTION_BINDINGS):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError("source_execution keys mismatch")
        expected = SOURCE_EXECUTION_BINDINGS
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError(f"source_execution.{key} mismatch")


def _source_context() -> dict[str, Any]:
    context = deepcopy(source.source.SOURCE_CONTEXT)
    renames = {
        "source_approval_commit": "source_prior_approval_commit",
        "source_approval_digest": "source_prior_approval_digest",
        "source_attestation_digest": "source_prior_attestation_digest",
        "source_execution_commit": "source_blocked_input_preparation_execution_commit",
        "source_blocked_reason": "source_blocked_input_preparation_execution_reason",
        "source_blocked_digest": "source_blocked_input_preparation_digest",
        "source_source_binding_digest": "source_blocked_input_preparation_source_binding_digest",
        "source_input_absence_digest": "source_blocked_input_preparation_input_absence_digest",
        "source_coverage_digest": "source_blocked_input_preparation_coverage_digest",
        "source_blocked_manifest_digest": "source_blocked_input_preparation_manifest_digest",
        "source_package_options_review_digest": "source_operator_review_package_options_review_digest",
        "source_future_requirements_review_digest": "source_operator_review_future_requirements_review_digest",
        "source_future_contract_review_digest": "source_operator_review_future_contract_review_digest",
        "source_binding_review_digest": "source_operator_review_source_binding_review_digest",
    }
    for old, new in renames.items():
        if old in context:
            context[new] = context.pop(old)
    context.update(deepcopy(source.SOURCE_APPROVAL_BINDINGS))
    context["source_approval_selected_package_executed"] = context.pop("source_selected_package_executed")
    context.update(deepcopy(SOURCE_EXECUTION_BINDINGS))
    return context


def _review_surfaces() -> dict[str, Any]:
    missing_ids = [f"MA-{index:03d}" for index in range(1, 31)]
    mechanism_review = {
        "source_digest": SOURCE_PAYLOAD_SUPPLY_MECHANISM_DIGEST,
        "definition_present": True,
        "actual_payload_created": False,
        "item_count": 30,
        "section_count": 4,
    }
    schema_review = {
        "source_digest": SOURCE_OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST,
        "package_header_fields": list(source.PACKAGE_HEADER_FIELDS),
        "evidence_item_fields": list(source.EVIDENCE_ITEM_FIELDS),
        "reviewed_missing_authority_ids": missing_ids,
        "actual_payload_values_present": False,
    }
    checklist_review = {
        "field_count": 34,
        "all_actual_values_absent": True,
        "explicit_non_secret_payload_required": True,
    }
    allowed_review = {
        "section_ids": list(source.ALLOWED_SECTION_IDS),
        "workstream_ids": list(source.ALLOWED_WORKSTREAM_IDS),
        "artifact_types": list(source.ALLOWED_ARTIFACT_TYPES),
        "evidence_classifications": list(source.ALLOWED_EVIDENCE_CLASSIFICATIONS),
        "specification_or_observation": list(source.ALLOWED_SPECIFICATION_OR_OBSERVATION),
        "expected_or_actual_scope": list(source.ALLOWED_EXPECTED_OR_ACTUAL_SCOPE),
    }
    secret_review = {
        "required_indicators": list(source.SECRET_INDICATORS),
        "future_rejection_required": True,
        "actual_payload_screened": False,
        "environment_or_external_system_inspected": False,
    }
    workstream_review = {
        "workstream_ids": list(source.ALLOWED_WORKSTREAM_IDS),
        "segment_item_counts": [8, 8, 7, 7],
        "mapped_item_count": 30,
        "actual_supplied_item_count": 0,
    }
    prerequisite_review = {
        "results_review_required_before_any_prepared_input_use": True,
        "future_reattempt_requires_explicit_non_secret_payload": True,
        "execution_reattempt_created": False,
    }
    return {
        "payload_supply_mechanism_definition_review": mechanism_review,
        "operator_payload_submission_schema_review": schema_review,
        "operator_payload_field_checklist_review": checklist_review,
        "allowed_values_matrix_review": allowed_review,
        "secret_screening_guidance_review": secret_review,
        "workstream_segmented_payload_supply_plan_review": workstream_review,
        "results_review_prerequisite": prerequisite_review,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {"check_id": check_id, "status": "PASS" if actual else "BLOCKER", "expected": True, "actual": bool(actual), "severity": "BLOCKER", "message": "review boundary preserved" if actual else "review boundary drift"}


def _digest_without(value: Mapping[str, Any], *excluded: str) -> str:
    return semantic_digest({key: deepcopy(item) for key, item in value.items() if key not in excluded})


def _assemble_results_review() -> dict[str, Any]:
    surfaces = _review_surfaces()
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "results_review_status": RESULTS_REVIEW_STATUS,
        "results_review_scope": RESULTS_REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "results_review_only": True,
        "results_review_philosophy": "The committed source execution defined a deterministic payload-supply mechanism only. This review verifies its identities, digests, schema counts, safety rules, workstream plan, prerequisite, and closed boundaries without rerunning or regenerating it.",
        "results_review_boundary": "Results review only. Actual payload and evidence remain absent, coverage remains 0/30, all missing-authority items remain MISSING_NOT_ACQUIRED, and downstream gates remain separately controlled.",
        **_source_context(),
        **surfaces,
        "source_success_digests_absent": True,
        "prepared_operator_completion_inputs_digest": None,
        "prepared_operator_completion_inputs_manifest_digest": None,
        "success_execution_digest": None,
        "primary_failure_class": "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION",
        "secondary_failure_classes": [
            "EXECUTION_CORRECTLY_FAILS_CLOSED_WITHOUT_EXPLICIT_OPERATOR_COMPLETION_INPUTS",
            "APPROVAL_IS_NOT_OPERATOR_COMPLETION_INPUTS",
            "REVIEWED_CANDIDATE_AND_INPUT_CONTRACT_ARE_NOT_SUPPLIED_INPUTS",
            "TEMPLATE_PLACEHOLDERS_ARE_NOT_OPERATOR_COMPLETION_INPUTS",
            "DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_ENV_AND_EXTERNAL_DOCUMENTS_ARE_NOT_INPUT_SOURCES",
            "SYNTHETIC_SUCCESS_PATH_IS_TEST_ONLY_AND_NOT_REPOSITORY_EVIDENCE",
            "COMPLETION_REATTEMPT_REQUIRES_REVIEWED_EXPLICIT_NON_SECRET_OPERATOR_INPUTS",
            "SOURCE_AUTHORITY_ACQUISITION_REMAINS_BLOCKED_UNTIL_REVIEWED_COMPLETED_PACKAGE_EXISTS",
            "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED",
        ],
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "future_completion_requirement_count": 67,
        "source_enumerated_future_completion_requirement_count": 69,
        "approved_future_completion_requirement_named_count": 69,
        "source_non_goal_count": 71,
        "source_enumerated_non_goal_count": 76,
        "source_risk_control_count": 104,
        "source_enumerated_risk_control_count": 106,
        "source_future_input_preparation_requirement_count": 62,
        "source_future_input_preparation_plan_step_count": 17,
        "source_planned_output_count": 34,
        "source_non_goal_count_local": 76,
        "source_risk_control_count_local": 105,
        "source_candidate_future_requirement_count": 62,
        "source_candidate_future_plan_step_count": 15,
        "source_candidate_planned_output_count": 34,
        "source_candidate_non_goal_count": 78,
        "source_candidate_risk_control_count": 112,
        "source_approval_non_goal_count": 78,
        "source_approval_risk_control_count": 112,
        "source_approval_enumerated_risk_control_count": 146,
        "outputs": [{"output_id": item, "status": GENERATED_OUTPUT_STATUS} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
        "recommended_action": "PROCEED_ONLY_TO_SEPARATELY_INVOKED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_CANDIDATE_AFTER_REVIEWED_PAYLOAD_SUPPLY_MECHANISM_IF_EXPLICIT_NON_SECRET_OPERATOR_PAYLOAD_IS_AVAILABLE",
        "reason": "The source execution created only a mechanism definition. The next safe step is only a separately invoked reattempt candidate, and only if explicit non-secret operator payload is available.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
    }
    review.update({key: True for key in TRUE_FIELDS})
    review.update({key: False for key in FALSE_FIELDS})
    review.update(deepcopy(COUNTS))
    review[PAYLOAD_SUPPLY_MECHANISM_REVIEW_DIGEST_KEY] = semantic_digest(review["payload_supply_mechanism_definition_review"])
    review[OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_REVIEW_DIGEST_KEY] = semantic_digest(review["operator_payload_submission_schema_review"])
    review[ALLOWED_VALUES_AND_SECRET_SCREENING_REVIEW_DIGEST_KEY] = semantic_digest({"allowed_values": review["allowed_values_matrix_review"], "secret_screening": review["secret_screening_guidance_review"]})
    review[WORKSTREAM_SUPPLY_PLAN_REVIEW_DIGEST_KEY] = semantic_digest(review["workstream_segmented_payload_supply_plan_review"])
    review[SOURCE_BINDING_REVIEW_DIGEST_KEY] = semantic_digest({"source_execution": SOURCE_EXECUTION_BINDINGS, "source_context": _source_context()})
    review[RESULTS_REVIEW_DIGEST_KEY] = _digest_without(review, RESULTS_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY, "checklist", "summary")
    review[MANIFEST_DIGEST_KEY] = semantic_digest({
        "artifact_kind": ARTIFACT_KIND,
        "results_review_status": RESULTS_REVIEW_STATUS,
        "output_ids": list(OUTPUT_IDS),
        "digests": {key: review[key] for key in (RESULTS_REVIEW_DIGEST_KEY, PAYLOAD_SUPPLY_MECHANISM_REVIEW_DIGEST_KEY, OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_REVIEW_DIGEST_KEY, ALLOWED_VALUES_AND_SECRET_SCREENING_REVIEW_DIGEST_KEY, WORKSTREAM_SUPPLY_PLAN_REVIEW_DIGEST_KEY, SOURCE_BINDING_REVIEW_DIGEST_KEY)},
    })
    checks = [
        _check("artifact_kind_correct", review["artifact_kind"] == ARTIFACT_KIND),
        _check("results_review_status_correct", review["results_review_status"] == RESULTS_REVIEW_STATUS),
        _check("results_review_scope_correct", review["results_review_scope"] == RESULTS_REVIEW_SCOPE),
        _check("future_payload_item_count_30", len(review["operator_payload_submission_schema_review"]["reviewed_missing_authority_ids"]) == 30),
        _check("workstream_segment_counts_preserved", review["workstream_segment_item_counts"] == [8, 8, 7, 7]),
        _check("actual_payload_values_absent", review["operator_payload_submission_schema_review"]["actual_payload_values_present"] is False),
        _check("actual_coverage_zero", review["actual_covered_missing_authority_item_count"] == 0),
        _check("missing_authority_items_missing_not_acquired", review["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"),
    ]
    checks.extend(_check(f"{key}_bound", review[key] == value) for key, value in SOURCE_EXECUTION_BINDINGS.items())
    checks.extend(_check(f"{key}_true", review[key] is True) for key in TRUE_FIELDS)
    checks.extend(_check(f"{key}_false", review[key] is False) for key in FALSE_FIELDS)
    checks.extend(_check(f"risk_control_{item}_defined", item in review["risk_controls"]) for item in RISK_CONTROLS)
    checks.extend(_check(f"output_{item}_generated", any(row["output_id"] == item and row["status"] == GENERATED_OUTPUT_STATUS for row in review["outputs"])) for item in OUTPUT_IDS)
    for key in (RESULTS_REVIEW_DIGEST_KEY, PAYLOAD_SUPPLY_MECHANISM_REVIEW_DIGEST_KEY, OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_REVIEW_DIGEST_KEY, ALLOWED_VALUES_AND_SECRET_SCREENING_REVIEW_DIGEST_KEY, WORKSTREAM_SUPPLY_PLAN_REVIEW_DIGEST_KEY, SOURCE_BINDING_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        checks.append(_check(f"{key}_generated", re.fullmatch(r"[0-9a-f]{64}", review[key]) is not None))
    review["checklist"] = checks
    review["summary"] = {
        "total_checks": len(checks), "passed_checks": sum(item["status"] == "PASS" for item in checks),
        "failed_checks": sum(item["status"] != "PASS" for item in checks),
        "blocker_count": sum(item["status"] != "PASS" and item["severity"] == "BLOCKER" for item in checks),
        "source_selected_package": SELECTED_PACKAGE, "source_selected_package_executed": True,
        "actual_covered_missing_authority_item_count": 0, "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "ready_for_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_if_explicit_payload_supplied_and_selected": True,
        "ready_for_operator_completion_inputs_preparation_or_supply_execution_reattempt": False,
        "ready_for_retry_candidate": False, "ready_for_main_merge_approval": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    return review


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(*, source_execution: dict | None = None) -> dict[str, Any]:
    """Build the review from committed source-execution constants."""
    _validate_source_execution(SOURCE_EXECUTION_BINDINGS if source_execution is None else source_execution)
    review = _assemble_results_review()
    result = validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(review)
    if result["blocker_count"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError("results review checklist contains blockers")
    return review


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(results_review: dict) -> dict[str, Any]:
    """Reject any source-binding, review-surface, or authority drift."""
    if not isinstance(results_review, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError("results_review must be an object")
    canonical = _assemble_results_review()
    difference = _first_difference(dict(results_review), canonical)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError(f"{difference} mismatch")
    return deepcopy(canonical["summary"])


MARKDOWN_SECTIONS = (
    "Results Review Disposition", "Source Execution", "Execution Digest Surface", "Selected Package Execution",
    "Payload Supply Mechanism Definition Review", "Operator Payload Submission Schema Review",
    "Operator Payload Field Checklist Review", "Allowed Values Matrix Review", "Secret Screening Guidance Review",
    "Workstream Segmented Payload Supply Plan Review", "Results Review Prerequisite", "Source Approval",
    "Source Operator Review", "Source Candidate", "Source Failure Diagnosis", "Source Blocked Input Preparation Execution",
    "Blocked Reason", "Primary Failure Class", "Secondary Failure Classes", "Source Prior Approval",
    "Source Prior Operator Review", "Source Prior Candidate", "Source Prior Completion-Failure Diagnosis",
    "Source Completion Execution", "Source Completion Approval", "Source Completion Candidate Operator Review",
    "Source Completion Candidate", "Source Template Preparation Results Review", "Source Template Preparation Execution",
    "Source Preparation Failure Acquisition Chains", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt",
    "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
    "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
    "Reviewed Template Structure", "Actual Evidence Absence", "Actual Coverage Zero", "Missing Authority Inventory",
    "Count Label Distinction", "Source Authority Gap Preservation", "Unsupported Claims Boundary", "Recommendation",
    "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_markdown_v1(results_review: dict) -> str:
    """Render deterministic Markdown for the results-review-only artifact."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(results_review)
    review = results_review
    facts = {
        "Results Review Disposition": f"`{RESULTS_REVIEW_STATUS}` within `{RESULTS_REVIEW_SCOPE}`. Review `{review[RESULTS_REVIEW_DIGEST_KEY]}`; manifest `{review[MANIFEST_DIGEST_KEY]}`.",
        "Source Execution": f"Commit `{SOURCE_EXECUTION_COMMIT}`; artifact `{source.ARTIFACT_KIND}`; checklist 515/515 PASS.",
        "Execution Digest Surface": f"Execution `{SOURCE_EXECUTION_DIGEST}`; mechanism `{SOURCE_PAYLOAD_SUPPLY_MECHANISM_DIGEST}`; schema `{SOURCE_OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST}`; allowed/safety `{SOURCE_ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST}`; workstreams `{SOURCE_WORKSTREAM_SUPPLY_PLAN_DIGEST}`; binding `{SOURCE_EXECUTION_SOURCE_BINDING_DIGEST}`; manifest `{SOURCE_EXECUTION_MANIFEST_DIGEST}`.",
        "Selected Package Execution": f"`{SELECTED_PACKAGE}` was executed in the source only for mechanism definition and was not rerun.",
        "Payload Supply Mechanism Definition Review": f"Definition and empty-payload boundary reviewed; digest `{review[PAYLOAD_SUPPLY_MECHANISM_REVIEW_DIGEST_KEY]}`.",
        "Operator Payload Submission Schema Review": f"14 header fields, 21 item fields, and MA-001 through MA-030 reviewed; digest `{review[OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_REVIEW_DIGEST_KEY]}`.",
        "Operator Payload Field Checklist Review": "Thirty-four future-entry fields reviewed; no actual value exists.",
        "Allowed Values Matrix Review": f"Four sections, four workstreams, 13 artifact types, 12 classifications, two observation domains, and four scope values reviewed; combined safety digest `{review[ALLOWED_VALUES_AND_SECRET_SCREENING_REVIEW_DIGEST_KEY]}`.",
        "Secret Screening Guidance Review": "Thirteen future rejection indicators reviewed; no actual payload, environment, credential source, file, log, browser, or external system was inspected.",
        "Workstream Segmented Payload Supply Plan Review": f"Segment counts 8, 8, 7, 7 and zero supplied items reviewed; digest `{review[WORKSTREAM_SUPPLY_PLAN_REVIEW_DIGEST_KEY]}`.",
        "Results Review Prerequisite": "A future reattempt candidate remains conditional on separately selected explicit non-secret operator payload.",
        "Source Approval": f"Commit `{review['source_approval_commit']}` and approval `{review['source_approval_digest']}` remain bound.",
        "Source Operator Review": f"Commit `{review['source_operator_review_commit']}` and digest `{review['source_operator_review_digest']}` remain bound.",
        "Source Candidate": f"Commit `{review['source_candidate_commit']}` and digest `{review['source_candidate_digest']}` remain bound.",
        "Source Failure Diagnosis": f"Commit `{review['source_failure_diagnosis_commit']}` and digest `{review['source_failure_diagnosis_digest']}` remain bound.",
        "Source Blocked Input Preparation Execution": f"Commit `{review['source_blocked_input_preparation_execution_commit']}` remains blocked.",
        "Blocked Reason": f"`{review['source_blocked_input_preparation_execution_reason']}`.",
        "Primary Failure Class": f"`{review['primary_failure_class']}`.",
        "Source Prior Approval": f"Historical commit `{review['source_prior_approval_commit']}` remains source evidence only.",
        "Source Completion Execution": f"Commit `{review['source_completion_execution_commit']}` remains blocked by `{review['source_completion_execution_blocked_reason']}`.",
        "Durable Receipt": f"`{review['source_durable_receipt_path']}` is bound opaquely and was not parsed.",
        "Retry Failure Context": "24,877 passed / 1,292 failed / 112 errors / 7 skipped remains authoritative retry evidence.",
        "Priority 1 Validation Summary": "675/675 before and after remains current-root evidence only and was not rerun.",
        "Diagnostic Capture Evidence Summary": "Exit 1 and committed byte counts/hashes remain diagnostic metadata only; output was not analyzed.",
        "Reviewed Template Structure": "Exactly 30 empty templates, 14 header fields, 21 item fields, and four workstreams were reviewed without regeneration.",
        "Actual Evidence Absence": "No payload, prepared input, evidence item, completed evidence package, or acquired authority exists.",
        "Actual Coverage Zero": "Coverage remains 0/30; all rows remain `MISSING_NOT_ACQUIRED`.",
        "Missing Authority Inventory": "MA-001 through MA-030 remain mapped and unacquired.",
        "Count Label Distinction": "All prescribed and enumerated count labels remain distinct and unreconciled.",
        "Source Authority Gap Preservation": "No source authority, evidence, external evidence, concrete authority, or safe change was created.",
        "Unsupported Claims Boundary": "No root cause, retry success, predictive usefulness, profitability, or main readiness is claimed.",
        "Recommendation": f"`{review['recommended_action']}`. Next task: `{RECOMMENDED_NEXT_TASK}`.",
        "Authority Boundaries": "Results review only; execution, payload, evidence, acquisition, disposition, remediation, retry, merge, runtime, broker, and trading gates remain closed.",
        "Checklist Summary": f"{review['summary']['passed_checks']}/{review['summary']['total_checks']} PASS; blockers={review['summary']['blocker_count']}.",
        "Guardrails": "Committed constants and validated injection only; no source builders, file reads, subprocesses, execution reruns, pytest, cache, logs, environment, external documents, providers, source owners, data, models, runtime, broker, or trading actions.",
    }
    list_sections = {
        "Secondary Failure Classes": review["secondary_failure_classes"],
        "Priority 1 Target Modules": [f"{item['path']}: {item['failed_or_errored_nodeid_count']}" for item in review["priority_1_target_modules"]],
        "Reviewed Observable Families": [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in review["reviewed_observable_failure_families"]],
        "Reviewed Workstreams": [f"{item['workstream_id']} <- {item['source_family_id']}" for item in review["reviewed_workstreams"]],
        "Next Chain": review["next_chain"], "Next Gates": review["next_gates"], "Risk Controls": review["risk_controls"],
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs Reentry or Payload Supply Execution Results Review After Approval Status", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", ""))
        if section in list_sections:
            lines.extend(f"{index}. `{item}`" for index, item in enumerate(list_sections[section], 1))
        else:
            lines.append(facts.get(section, "Preserved from committed source evidence without rerun, payload, evidence, acquisition, remediation, retry, or downstream authority."))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(output_dir: str | Path, *, source_execution: dict | None = None) -> dict[str, Any]:
    """Write only the requested results-review status Markdown artifact."""
    destination_root = Path(output_dir)
    if {part.lower() for part in destination_root.parts}.intersection({".marketflow", ".pytest_cache", ".env"}):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(source_execution=source_execution)
    destination = destination_root / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_markdown_v1(review), encoding="utf-8")
    return review


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "RESULTS_REVIEW_STATUS", "RESULTS_REVIEW_SCOPE", "SELECTED_PACKAGE",
    "GENERATED_OUTPUT_STATUS", "RECOMMENDED_NEXT_TASK", "SOURCE_EXECUTION_COMMIT", "SOURCE_EXECUTION_DIGEST",
    "SOURCE_PAYLOAD_SUPPLY_MECHANISM_DIGEST", "SOURCE_OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST",
    "SOURCE_ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST", "SOURCE_WORKSTREAM_SUPPLY_PLAN_DIGEST",
    "SOURCE_EXECUTION_SOURCE_BINDING_DIGEST", "SOURCE_EXECUTION_MANIFEST_DIGEST", "SOURCE_EXECUTION_BINDINGS",
    "RESULTS_REVIEW_DIGEST_KEY", "PAYLOAD_SUPPLY_MECHANISM_REVIEW_DIGEST_KEY",
    "OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_REVIEW_DIGEST_KEY", "ALLOWED_VALUES_AND_SECRET_SCREENING_REVIEW_DIGEST_KEY",
    "WORKSTREAM_SUPPLY_PLAN_REVIEW_DIGEST_KEY", "SOURCE_BINDING_REVIEW_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "TRUE_FIELDS", "FALSE_FIELDS", "COUNTS", "OUTPUT_IDS", "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "MARKDOWN_SECTIONS",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_markdown_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1",
]
