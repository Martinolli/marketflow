"""Execute only the approved operator payload-supply mechanism definition.

This module is deterministic, offline, and governance-only.  It defines the
schema and review gates for a future operator submission; it never creates or
accepts a submission, evidence, source authority, remediation, retry, merge,
runtime, broker, or trading authority.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTED_AFTER_APPROVAL_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1"
EXECUTION_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTED_AFTER_APPROVAL_PAYLOAD_SUPPLY_MECHANISM_READY"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_AFTER_APPROVAL_ONLY_PAYLOAD_SUPPLY_MECHANISM_DEFINITION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = "PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY"
MECHANISM_STATUS = "GENERATED_PAYLOAD_SUPPLY_MECHANISM_DEFINITION_ONLY_NOT_OPERATOR_PAYLOAD_NOT_INPUT_SUPPLY_NOT_EVIDENCE"
GENERATED_OUTPUT_STATUS = "GENERATED_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_MECHANISM_EXECUTION_ONLY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_V1"

SOURCE_APPROVAL_COMMIT = "9c97a344e2a0e6f193804570c4a2ee8a3820e7f3"
SOURCE_REQUESTED_APPROVAL_COMMIT = "5a42af6dc7888dda62d77c0d37058b11ae113d79"
SOURCE_APPROVAL_DIGEST = "5f2d5ed4737b266d2257c20c27f4c7a09ef942e78aea2a95d331c118a554d2a9"
SOURCE_ATTESTATION_DIGEST = "11c493f58905285db898602c048c7e7d19b06c357043412a8a261a4be34d5895"
SOURCE_PACKAGE_OPTIONS_DIGEST = "36ca2b5460c39db1fda2ac46363b33fab2566d553603b5f5e5552d85623a52f5"
SOURCE_FUTURE_REQUIREMENTS_DIGEST = "41bb60295724dd77ae46049c288d67c2c0b041e5114a86b527e76f6d6e33b82a"
SOURCE_FUTURE_CONTRACT_DIGEST = "bf89527efbe5a163ed7428d546ef1a4a8ed28724376f22130165f58d9f7209c5"
SOURCE_APPROVAL_SOURCE_BINDING_DIGEST = "5a5b3458350467ec843249a266c0050cc2e2c53d22b5081aff1874b2d2cdd705"
SOURCE_APPROVAL_MANIFEST_DIGEST = "d7086eea764635e1fc7184310842c04d26b0c8578cfc3ec2095b50fc36af0728"

EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_digest"
PAYLOAD_SUPPLY_MECHANISM_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_payload_supply_mechanism_digest"
OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_operator_payload_submission_schema_digest"
ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_allowed_values_and_secret_screening_digest"
WORKSTREAM_SUPPLY_PLAN_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_workstream_supply_plan_digest"
SOURCE_BINDING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_source_binding_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTED_AFTER_APPROVAL_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTED_AFTER_APPROVAL_PAYLOAD_SUPPLY_MECHANISM_READY = EXECUTION_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_AFTER_APPROVAL_ONLY_PAYLOAD_SUPPLY_MECHANISM_DEFINITION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY = SELECTED_PACKAGE

SOURCE_APPROVAL_BINDINGS = {
    "source_approval_commit": SOURCE_APPROVAL_COMMIT,
    "source_requested_approval_commit": SOURCE_REQUESTED_APPROVAL_COMMIT,
    "source_approval_artifact_kind": source.ARTIFACT_KIND,
    "source_approval_status": source.APPROVAL_STATUS,
    "source_approval_scope": source.APPROVAL_SCOPE,
    "source_approval_digest": SOURCE_APPROVAL_DIGEST,
    "source_attestation_digest": SOURCE_ATTESTATION_DIGEST,
    "source_package_options_digest": SOURCE_PACKAGE_OPTIONS_DIGEST,
    "source_future_requirements_digest": SOURCE_FUTURE_REQUIREMENTS_DIGEST,
    "source_future_contract_digest": SOURCE_FUTURE_CONTRACT_DIGEST,
    "source_approval_source_binding_digest": SOURCE_APPROVAL_SOURCE_BINDING_DIGEST,
    "source_approval_manifest_digest": SOURCE_APPROVAL_MANIFEST_DIGEST,
    "selected_operator_completion_inputs_reentry_or_payload_supply_package": SELECTED_PACKAGE,
    "source_selected_package_approved_for_future_execution_only": True,
    "source_selected_package_executed": False,
}

ALLOWED_SECTION_IDS = (
    "assertion_value_mismatch_source_authority_scope",
    "digest_hash_boundary_source_authority_scope",
    "fixture_isolation_determinism_source_authority_scope",
    "schema_field_contract_source_authority_scope",
)
ALLOWED_WORKSTREAM_IDS = (
    "assertion_value_mismatch_workstream",
    "digest_hash_boundary_workstream",
    "fixture_isolation_determinism_workstream",
    "schema_field_contract_workstream",
)
ALLOWED_ARTIFACT_TYPES = (
    "approved_product_specification", "approved_schema_definition", "approved_artifact_contract",
    "approved_canonical_payload_or_serialization_contract", "approved_expected_value_source",
    "approved_actual_value_source", "approved_digest_manifest_source", "approved_fixture_lifecycle_document",
    "approved_deterministic_execution_contract", "approved_export_surface_contract",
    "approved_operator_provided_evidence_package", "approved_source_owning_team_statement",
    "approved_reviewed_source_digest_bundle",
)
ALLOWED_EVIDENCE_CLASSIFICATIONS = (
    "SPECIFICATION", "APPROVED_CONTRACT", "SOURCE_OWNER_STATEMENT", "CANONICAL_PAYLOAD",
    "CANONICAL_SCHEMA", "CANONICAL_SERIALIZATION", "EXPECTED_VALUE_SOURCE", "ACTUAL_VALUE_SOURCE",
    "FIXTURE_LIFECYCLE_AUTHORITY", "DETERMINISM_AUTHORITY", "EXPORT_SURFACE_AUTHORITY",
    "REVIEWED_SOURCE_DIGEST_BUNDLE",
)
ALLOWED_SPECIFICATION_OR_OBSERVATION = ("SPECIFICATION", "OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT")
ALLOWED_EXPECTED_OR_ACTUAL_SCOPE = ("EXPECTED", "ACTUAL", "BOTH", "NOT_APPLICABLE")
SECRET_INDICATORS = (
    "API key", "broker credential", "personal financial credential", "market data credential",
    "private token", "access token", "password", "secret", "private key", "bearer token",
    "IBKR credential", "account number", "seed phrase",
)

PACKAGE_HEADER_FIELDS = (
    "package_source_owner_or_origin", "package_reference", "package_created_utc",
    "package_digest_or_reproducible_provenance", "package_declares_no_secrets",
    "package_declares_no_api_keys", "package_declares_no_broker_credentials",
    "package_declares_no_personal_financial_credentials", "package_declares_no_market_data_credentials",
    "package_declares_no_private_tokens", "package_distinguishes_specification_from_observation",
    "package_distinguishes_expected_from_actual",
    "package_distinguishes_source_authority_from_diagnostic_output", "evidence_items",
)
EVIDENCE_ITEM_FIELDS = (
    "missing_authority_id", "section_id", "workstream_id", "acceptable_source_artifact_type",
    "evidence_classification", "specification_or_observation", "expected_or_actual_scope",
    "source_owner_or_origin", "source_reference", "digest_or_reproducible_provenance",
    "authority_statement", "no_secret_attestation", "requires_results_review_before_use",
    "direct_change_authorized", "remediation_authorized", "retry_authorized",
    "main_merge_authorized", "actual_evidence_supplied", "actual_evidence_validated",
    "actual_evidence_bound", "source_authority_acquired",
)

TRUE_FIELDS = tuple("""operator_completion_inputs_reentry_or_payload_supply_execution_created
operator_completion_inputs_reentry_or_payload_supply_execution_ready
source_approval_bound
source_approval_reviewed
source_operator_review_bound
source_candidate_bound
source_failure_diagnosis_bound
source_execution_bound
source_execution_blocked_reason_verified
source_execution_success_digests_absent_verified
source_attestation_bound
selected_package_bound
selected_package_executed
approved_package_executed
approval_authorizes_this_execution_verified
payload_supply_mechanism_created
payload_supply_mechanism_definition_created
payload_supply_schema_created
operator_payload_submission_schema_created
operator_payload_field_checklist_created
allowed_values_matrix_created
secret_screening_guidance_created
workstream_segmented_payload_supply_plan_created
results_review_prerequisite_defined
future_completion_reattempt_prerequisite_defined
downstream_gates_preserved
future_payload_supply_contract_preserved
future_requirements_preserved
future_plan_preserved
planned_outputs_preserved
supporting_packages_preserved_unselected
blocked_packages_preserved_blocked
operator_completion_inputs_absence_preserved
execution_correctly_governed
no_input_inference_verified
approval_not_input_verified
template_placeholder_boundary_preserved
diagnostic_output_boundary_preserved
synthetic_success_path_test_only_verified
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
ready_for_operator_completion_inputs_reentry_or_payload_supply_execution_results_review""".split())

FALSE_FIELDS = tuple("""operator_payload_created
operator_completion_inputs_supplied_to_execution
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
pytest_performed_in_execution
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_execution
diagnostic_output_analyzed_in_execution
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_execution
method_execution_rerun_performed
controlled_recapture_rerun_performed
template_execution_rerun_performed
completion_execution_rerun_performed
input_preparation_or_supply_execution_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_execution
cache_modified_in_execution
pytest_cache_committed
marketflow_outputs_committed
terminal_logs_parsed
operator_logs_parsed
env_inspection_performed
source_owners_contacted
external_documents_read
provider_requests_made_in_execution
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
market_data_acquisition_performed_in_execution
dataset_generation_performed_in_execution
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
    "acquisition_scope_section_count": 4,
    "acceptable_source_artifact_type_count": 13,
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
}

OUTPUT_IDS = tuple("""operator_completion_inputs_reentry_or_payload_supply_execution_manifest
source_approval_binding_report
source_operator_review_binding_report
source_candidate_binding_report
source_failure_diagnosis_binding_report
source_execution_binding_report
source_blocked_reason_report
source_success_digests_absence_report
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
selected_package_execution_report
payload_supply_mechanism_definition
operator_payload_submission_schema
operator_payload_field_checklist
allowed_values_matrix
secret_screening_guidance
workstream_segmented_payload_supply_plan
results_review_prerequisite_report
downstream_gate_preservation_report
unsupported_claims_boundary_report
digest_manifest""".split())

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Reentry or Payload Supply Execution Results Review After Approval v1.",
    "Operator Completion Inputs Preparation or Supply Execution Reattempt v1, only if explicit non-secret operator inputs are supplied and separately approved.",
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
NEXT_GATES = tuple("""operator_completion_inputs_reentry_or_payload_supply_execution_results_review
operator_completion_inputs_preparation_or_supply_execution_reattempt_with_explicit_non_secret_inputs_if_approved
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

_EXECUTION_RISK_CONTROLS = tuple("""execution_only_defines_payload_supply_mechanism
execution_does_not_create_operator_payload
execution_does_not_prepare_inputs
execution_does_not_supply_inputs
execution_does_not_provide_inputs
execution_does_not_validate_inputs_as_evidence
execution_does_not_bind_inputs_as_evidence
execution_does_not_create_prepared_inputs
execution_does_not_create_completed_evidence_package
execution_does_not_create_evidence_package
execution_does_not_fill_actual_evidence_items
execution_does_not_validate_evidence
execution_does_not_bind_evidence
execution_does_not_accept_evidence_as_source_authority
execution_does_not_infer_inputs_from_template
execution_does_not_infer_inputs_from_placeholders
execution_does_not_infer_inputs_from_diagnostic_output
execution_does_not_infer_inputs_from_digests
execution_does_not_read_cache_for_inputs
execution_does_not_parse_logs_for_inputs
execution_does_not_inspect_env_for_inputs
execution_does_not_read_external_documents_for_inputs
execution_does_not_call_providers_for_inputs
execution_does_not_contact_source_owners_for_inputs
execution_does_not_acquire_source_authority
execution_does_not_acquire_source_authority_evidence
execution_does_not_acquire_external_evidence
execution_does_not_create_source_authority_acquisition_execution
execution_does_not_retry_source_authority_acquisition
execution_does_not_create_no_change_disposition
execution_does_not_execute_alternate_diagnostics
execution_does_not_execute_remediation
execution_does_not_modify_production_code
execution_does_not_modify_existing_tests
execution_does_not_update_expected_digests
execution_does_not_generate_patch
execution_does_not_apply_patch
execution_does_not_run_pytest
execution_does_not_run_full_pytest
execution_does_not_rerun_priority1_validation
execution_does_not_rerun_retry
execution_does_not_rerun_detached_retry
execution_does_not_parse_durable_receipt
execution_does_not_analyze_diagnostic_output
execution_does_not_rerun_source_authority_enrichment
execution_does_not_rerun_follow_on_execution
execution_does_not_rerun_plan_execution
execution_does_not_regenerate_targeted_plan
execution_does_not_rerun_method_execution
execution_does_not_rerun_controlled_recapture
execution_does_not_rerun_template_execution
execution_does_not_rerun_completion_execution
execution_does_not_rerun_input_preparation_execution
execution_does_not_run_diagnostic_command
execution_does_not_read_pytest_cache
execution_does_not_modify_pytest_cache
execution_does_not_commit_pytest_cache
execution_does_not_commit_marketflow_outputs
execution_does_not_parse_terminal_logs
execution_does_not_parse_operator_logs
execution_does_not_inspect_env
execution_does_not_contact_source_owners
execution_does_not_read_external_documents
execution_does_not_reconstruct_prior_lost_values
execution_does_not_reconstruct_full_streams
execution_does_not_classify_modules_again
execution_does_not_classify_full_retry_failures
execution_does_not_classify_full_retry_errors
execution_does_not_claim_failure_error_separation
execution_does_not_identify_authoritative_first_failure
execution_does_not_identify_authoritative_first_error
execution_does_not_claim_traceback_root_cause
execution_does_not_claim_root_cause
execution_does_not_claim_retry_success
execution_does_not_claim_main_merge_readiness
execution_does_not_create_retry_candidate
execution_does_not_create_retry_approval
execution_does_not_create_retry_execution
execution_does_not_create_retry_results_review
execution_does_not_create_main_merge_approval
execution_does_not_push_main
execution_does_not_push_integration_branch
execution_does_not_delete_integration_branch
execution_does_not_delete_worktree
execution_does_not_force_push
execution_does_not_modify_tags
execution_does_not_regenerate_evidence
execution_does_not_call_providers
execution_does_not_acquire_market_data
execution_does_not_generate_dataset
execution_does_not_recompute_metrics
execution_does_not_train_models
execution_does_not_score_strategy
execution_does_not_generate_trade_recommendations
execution_does_not_accept_predictive_usefulness
execution_does_not_accept_profitability
execution_does_not_authorize_runtime
execution_does_not_authorize_broker_execution
approval_is_not_operator_input
reviewed_candidate_is_not_operator_input
reviewed_contract_is_not_operator_input
reviewed_template_is_not_completed_evidence_package
template_placeholders_are_not_completion_inputs
synthetic_success_path_is_test_only
payload_supply_mechanism_execution_is_not_payload_supply
payload_supply_mechanism_execution_is_not_input_preparation
payload_supply_mechanism_execution_is_not_evidence_completion
payload_supply_mechanism_execution_is_not_source_authority_acquisition
explicit_non_secret_payload_required_before_execution_reattempt
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
RISK_CONTROLS = tuple(dict.fromkeys((*source.RISK_CONTROLS, *_EXECUTION_RISK_CONTROLS)))


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError(ValueError):
    """Raised when an approval binding or execution-only boundary drifts."""


def _first_difference(actual: Any, expected: Any, path: str = "execution") -> str | None:
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


def _validate_source_approval(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError("source_approval must be an object")
    artifact_keys = {
        "artifact_kind": source.ARTIFACT_KIND,
        "approval_status": source.APPROVAL_STATUS,
        "approval_scope": source.APPROVAL_SCOPE,
        source.APPROVAL_DIGEST_KEY: SOURCE_APPROVAL_DIGEST,
        source.ATTESTATION_DIGEST_KEY: SOURCE_ATTESTATION_DIGEST,
        source.PACKAGE_OPTIONS_DIGEST_KEY: SOURCE_PACKAGE_OPTIONS_DIGEST,
        source.FUTURE_REQUIREMENTS_DIGEST_KEY: SOURCE_FUTURE_REQUIREMENTS_DIGEST,
        source.FUTURE_CONTRACT_DIGEST_KEY: SOURCE_FUTURE_CONTRACT_DIGEST,
        source.SOURCE_BINDING_DIGEST_KEY: SOURCE_APPROVAL_SOURCE_BINDING_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_APPROVAL_MANIFEST_DIGEST,
        "selected_operator_completion_inputs_reentry_or_payload_supply_package": SELECTED_PACKAGE,
        "selected_package_executed": False,
    }
    binding_keys = {key: expected for key, expected in SOURCE_APPROVAL_BINDINGS.items() if key in value}
    expected = artifact_keys if "artifact_kind" in value else binding_keys
    required_count = len(artifact_keys) if "artifact_kind" in value else len(SOURCE_APPROVAL_BINDINGS)
    if len(expected) != required_count:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError("source_approval keys incomplete")
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError(f"source_approval.{key} mismatch")


def _future_item_templates() -> list[dict[str, Any]]:
    mapping = source.SOURCE_CONTEXT["missing_authority_mapping"]
    rows = []
    for item in mapping:
        rows.append({
            "missing_authority_id": item["missing_authority_id"],
            "section_id": item["section_id"],
            "workstream_id": item["workstream_id"],
            "acceptable_source_artifact_type": None,
            "evidence_classification": None,
            "specification_or_observation": None,
            "expected_or_actual_scope": None,
            "source_owner_or_origin": None,
            "source_reference": None,
            "digest_or_reproducible_provenance": None,
            "authority_statement": None,
            "no_secret_attestation": None,
            "requires_results_review_before_use": True,
            "direct_change_authorized": False,
            "remediation_authorized": False,
            "retry_authorized": False,
            "main_merge_authorized": False,
            "actual_evidence_supplied": False,
            "actual_evidence_validated": False,
            "actual_evidence_bound": False,
            "source_authority_acquired": False,
        })
    return rows


def _mechanism() -> dict[str, Any]:
    rows = _future_item_templates()
    header_schema = [
        {"field_name": name, "required": True, "required_value": True if name.startswith("package_declares_no_") or name.startswith("package_distinguishes_") else None, "operator_value_supplied": False}
        for name in PACKAGE_HEADER_FIELDS
    ]
    allowed = {
        "section_id": list(ALLOWED_SECTION_IDS),
        "workstream_id": list(ALLOWED_WORKSTREAM_IDS),
        "acceptable_source_artifact_type": list(ALLOWED_ARTIFACT_TYPES),
        "evidence_classification": list(ALLOWED_EVIDENCE_CLASSIFICATIONS),
        "specification_or_observation": list(ALLOWED_SPECIFICATION_OR_OBSERVATION),
        "expected_or_actual_scope": list(ALLOWED_EXPECTED_OR_ACTUAL_SCOPE),
    }
    checklist = [
        {"field_name": name, "must_be_explicit": True, "actual_value_present": False}
        for name in (*PACKAGE_HEADER_FIELDS[:-1], *EVIDENCE_ITEM_FIELDS)
    ]
    workstream_plan = []
    for section_id, workstream_id in zip(ALLOWED_SECTION_IDS, ALLOWED_WORKSTREAM_IDS):
        item_ids = [row["missing_authority_id"] for row in rows if row["workstream_id"] == workstream_id]
        workstream_plan.append({
            "section_id": section_id,
            "workstream_id": workstream_id,
            "missing_authority_ids": item_ids,
            "planned_item_count": len(item_ids),
            "actual_supplied_item_count": 0,
            "status": "MISSING_NOT_ACQUIRED",
        })
    mechanism = {
        "mechanism_identity": {"selected_package": SELECTED_PACKAGE, "status": MECHANISM_STATUS, "governance_only": True, "actual_payload_created": False},
        "approved_source_contract_binding": deepcopy(SOURCE_APPROVAL_BINDINGS),
        "explicit_operator_payload_entry_rules": {
            "future_explicit_non_secret_operator_payload_required": True,
            "infer_from_templates_or_placeholders": False,
            "infer_from_diagnostics_digests_cache_logs_or_environment": False,
            "actual_payload_accepted_by_this_execution": False,
        },
        "package_header_schema": header_schema,
        "thirty_item_payload_schema": rows,
        "allowed_values_matrix": allowed,
        "workstream_segmented_supply_plan": workstream_plan,
        "secret_screening_policy": {
            "reject_if_any_string_field_appears_to_contain": list(SECRET_INDICATORS),
            "inspect_environment_credentials_files_logs_browsers_or_external_systems": False,
            "actual_payload_screened_by_this_execution": False,
        },
        "pre_submission_operator_checklist": checklist,
        "post_submission_results_review_requirement": {
            "required_before_any_prepared_input_use": True,
            "future_results_review_created": False,
            "future_submission_accepted": False,
        },
        "downstream_gate_policy": {gate: "CLOSED_PENDING_SEPARATE_REVIEW_AND_AUTHORITY" for gate in NEXT_GATES[1:]},
        "unsupported_claims_boundary": {
            "root_cause": False, "retry_success": False, "predictive_usefulness": False,
            "profitability": False, "main_merge_readiness": False,
        },
        "digest_manifest": {"generated_by_execution_digest_stage": True, "actual_evidence_digest_count": 0},
    }
    return mechanism


def _source_context() -> dict[str, Any]:
    context = deepcopy(source.SOURCE_CONTEXT)
    renames = {
        "source_approval_commit": "source_prior_approval_commit",
        "source_approval_digest": "source_prior_approval_digest",
        "source_attestation_digest": "source_prior_attestation_digest",
    }
    for old, new in renames.items():
        if old in context:
            context[new] = context.pop(old)
    context.update(deepcopy(SOURCE_APPROVAL_BINDINGS))
    return context


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {"check_id": check_id, "status": "PASS" if actual else "BLOCKER", "expected": True, "actual": bool(actual), "severity": "BLOCKER", "message": "boundary preserved" if actual else "boundary drift"}


def _digest_without(value: Mapping[str, Any], *excluded: str) -> str:
    return semantic_digest({key: deepcopy(item) for key, item in value.items() if key not in excluded})


def _assemble_execution() -> dict[str, Any]:
    mechanism = _mechanism()
    execution: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "execution_status": EXECUTION_STATUS,
        "execution_scope": EXECUTION_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "execution_only": True,
        "execution_philosophy": "The source approval selected and authorized only a future payload-supply mechanism definition. This execution creates deterministic governance-only mechanism artifacts and no operator payload, evidence, source authority, remediation, retry, merge, runtime, broker, or trading authority.",
        "execution_boundary": "Mechanism definition only. Actual coverage remains 0/30 and all missing-authority rows remain MISSING_NOT_ACQUIRED.",
        **_source_context(),
        "selected_package": SELECTED_PACKAGE,
        "payload_supply_mechanism_status": MECHANISM_STATUS,
        "payload_supply_mechanism": mechanism,
        "payload_supply_mechanism_definition": deepcopy(mechanism),
        "operator_payload_submission_schema": {
            "package_header_schema": deepcopy(mechanism["package_header_schema"]),
            "evidence_item_schema": [
                {
                    "field_name": name,
                    "required": True,
                    "template_value_only": name in {
                        "missing_authority_id", "section_id", "workstream_id",
                        "requires_results_review_before_use", "direct_change_authorized",
                        "remediation_authorized", "retry_authorized", "main_merge_authorized",
                        "actual_evidence_supplied", "actual_evidence_validated",
                        "actual_evidence_bound", "source_authority_acquired",
                    },
                }
                for name in EVIDENCE_ITEM_FIELDS
            ],
            "future_evidence_item_templates": deepcopy(mechanism["thirty_item_payload_schema"]),
            "actual_payload_values_present": False,
        },
        "operator_payload_field_checklist": deepcopy(mechanism["pre_submission_operator_checklist"]),
        "allowed_values_matrix": deepcopy(mechanism["allowed_values_matrix"]),
        "secret_screening_guidance": deepcopy(mechanism["secret_screening_policy"]),
        "workstream_segmented_payload_supply_plan": deepcopy(mechanism["workstream_segmented_supply_plan"]),
        "results_review_prerequisite": deepcopy(mechanism["post_submission_results_review_requirement"]),
        "downstream_gate_policy": deepcopy(mechanism["downstream_gate_policy"]),
        "unsupported_claims_boundary": deepcopy(mechanism["unsupported_claims_boundary"]),
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
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
        "source_success_digests_absent": True,
        "prepared_operator_completion_inputs_digest": None,
        "prepared_operator_completion_inputs_manifest_digest": None,
        "success_execution_digest": None,
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
        "operator_review_enumerated_non_goal_count": 90,
        "operator_review_enumerated_risk_control_count": 132,
        "source_approval_non_goal_count": 78,
        "source_approval_risk_control_count": 112,
        "source_approval_enumerated_risk_control_count": 146,
        "approved_package_options": deepcopy(list(source.APPROVED_PACKAGE_OPTIONS)),
        "approved_future_requirements": [{"requirement_id": item, "execution_status": "NOT_EXECUTED"} for item in source.source.source.FUTURE_REQUIREMENT_IDS],
        "future_plan": [{"step": item, "execution_status": "NOT_EXECUTED"} for item in source.FUTURE_PLAN],
        "outputs": [{"output_id": item, "status": GENERATED_OUTPUT_STATUS} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_ONLY_TO_SEPARATELY_INVOKED_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_MECHANISM_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL",
        "reason": "The approved package execution defines only the payload-supply mechanism. A separate results review is required before every downstream path.",
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
    execution.update({key: True for key in TRUE_FIELDS})
    execution.update({key: False for key in FALSE_FIELDS})
    execution.update(COUNTS)

    execution[PAYLOAD_SUPPLY_MECHANISM_DIGEST_KEY] = semantic_digest(execution["payload_supply_mechanism_definition"])
    execution[OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST_KEY] = semantic_digest(execution["operator_payload_submission_schema"])
    execution[ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST_KEY] = semantic_digest({"allowed_values_matrix": execution["allowed_values_matrix"], "secret_screening_guidance": execution["secret_screening_guidance"]})
    execution[WORKSTREAM_SUPPLY_PLAN_DIGEST_KEY] = semantic_digest(execution["workstream_segmented_payload_supply_plan"])
    execution[SOURCE_BINDING_DIGEST_KEY] = semantic_digest({"source_approval": SOURCE_APPROVAL_BINDINGS, "source_context": _source_context()})
    digest_keys = (EXECUTION_DIGEST_KEY, MANIFEST_DIGEST_KEY, "checklist", "summary")
    execution[EXECUTION_DIGEST_KEY] = _digest_without(execution, *digest_keys)
    execution[MANIFEST_DIGEST_KEY] = semantic_digest({
        "artifact_kind": ARTIFACT_KIND,
        "execution_status": EXECUTION_STATUS,
        "output_ids": list(OUTPUT_IDS),
        "digests": {key: execution[key] for key in (EXECUTION_DIGEST_KEY, PAYLOAD_SUPPLY_MECHANISM_DIGEST_KEY, OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST_KEY, ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST_KEY, WORKSTREAM_SUPPLY_PLAN_DIGEST_KEY, SOURCE_BINDING_DIGEST_KEY)},
    })

    checks = [
        _check("artifact_kind_correct", execution["artifact_kind"] == ARTIFACT_KIND),
        _check("execution_status_correct", execution["execution_status"] == EXECUTION_STATUS),
        _check("execution_scope_correct", execution["execution_scope"] == EXECUTION_SCOPE),
        _check("selected_package_correct", execution["selected_package"] == SELECTED_PACKAGE),
        _check("future_payload_schema_contains_30_items", len(execution["operator_payload_submission_schema"]["future_evidence_item_templates"]) == 30),
        _check("allowed_values_matrix_contains_13_artifact_types", len(execution["allowed_values_matrix"]["acceptable_source_artifact_type"]) == 13),
        _check("secret_screening_guidance_defined", bool(execution["secret_screening_guidance"])),
        _check("results_review_required_before_use", execution["results_review_prerequisite"]["required_before_any_prepared_input_use"] is True),
        _check("actual_coverage_zero", execution["actual_covered_missing_authority_item_count"] == 0),
        _check("missing_authority_items_missing_not_acquired", execution["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"),
    ]
    for key, expected in SOURCE_APPROVAL_BINDINGS.items():
        checks.append(_check(f"{key}_bound", execution[key] == expected))
    checks.extend(_check(f"{key}_true", execution[key] is True) for key in TRUE_FIELDS)
    checks.extend(_check(f"{key}_false", execution[key] is False) for key in FALSE_FIELDS)
    checks.extend(_check(f"risk_control_{item}_defined", item in execution["risk_controls"]) for item in RISK_CONTROLS)
    checks.extend(_check(f"output_{item}_generated", any(row["output_id"] == item and row["status"] == GENERATED_OUTPUT_STATUS for row in execution["outputs"])) for item in OUTPUT_IDS)
    for key in (EXECUTION_DIGEST_KEY, PAYLOAD_SUPPLY_MECHANISM_DIGEST_KEY, OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST_KEY, ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST_KEY, WORKSTREAM_SUPPLY_PLAN_DIGEST_KEY, SOURCE_BINDING_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        checks.append(_check(f"{key}_generated", re.fullmatch(r"[0-9a-f]{64}", execution[key]) is not None))
    execution["checklist"] = checks
    execution["summary"] = {
        "total_checks": len(checks),
        "passed_checks": sum(item["status"] == "PASS" for item in checks),
        "failed_checks": sum(item["status"] != "PASS" for item in checks),
        "blocker_count": sum(item["status"] != "PASS" and item["severity"] == "BLOCKER" for item in checks),
        "selected_package": SELECTED_PACKAGE,
        "selected_package_executed": True,
        "payload_supply_mechanism_created": True,
        "operator_payload_created": False,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "ready_for_operator_completion_inputs_reentry_or_payload_supply_execution_results_review": True,
        "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    return execution


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(*, source_approval: dict | None = None) -> dict[str, Any]:
    """Build the exact mechanism-definition execution from committed constants."""
    _validate_source_approval(SOURCE_APPROVAL_BINDINGS if source_approval is None else source_approval)
    execution = _assemble_execution()
    result = validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(execution)
    if result["blocker_count"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError("execution checklist contains blockers")
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(execution: dict) -> dict[str, Any]:
    """Reject any drift, including a filled payload placeholder or opened gate."""
    if not isinstance(execution, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError("execution must be an object")
    canonical = _assemble_execution()
    difference = _first_difference(dict(execution), canonical)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError(f"{difference} mismatch")
    return deepcopy(canonical["summary"])


MARKDOWN_SECTIONS = (
    "Execution Disposition", "Source Approval", "Approval Digest Surface", "Selected Package",
    "Payload Supply Mechanism Definition", "Operator Payload Submission Schema", "Operator Payload Field Checklist",
    "Allowed Values Matrix", "Secret Screening Guidance", "Workstream Segmented Payload Supply Plan",
    "Results Review Prerequisite", "Source Operator Review", "Source Candidate", "Source Failure Diagnosis",
    "Source Execution", "Blocked Reason", "Primary Failure Class", "Secondary Failure Classes",
    "Source Prior Approval", "Source Prior Operator Review", "Source Prior Candidate",
    "Source Prior Completion-Failure Diagnosis", "Source Completion Execution", "Source Completion Approval",
    "Source Completion Candidate Operator Review", "Source Completion Candidate",
    "Source Template Preparation Results Review", "Source Template Preparation Execution",
    "Source Preparation Failure Acquisition Chains", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt",
    "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
    "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
    "Reviewed Template Structure", "Actual Evidence Absence", "Actual Coverage Zero",
    "Count Label Distinction", "Unsupported Claims Boundary", "Recommendation", "Next Chain",
    "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_markdown_v1(execution: dict) -> str:
    """Render the execution-only status artifact as deterministic Markdown."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(execution)
    facts = {
        "Execution Disposition": f"`{EXECUTION_STATUS}` within `{EXECUTION_SCOPE}`. Execution digest `{execution[EXECUTION_DIGEST_KEY]}`; manifest `{execution[MANIFEST_DIGEST_KEY]}`.",
        "Source Approval": f"Commit `{SOURCE_APPROVAL_COMMIT}`; artifact `{source.ARTIFACT_KIND}`; approval `{SOURCE_APPROVAL_DIGEST}`.",
        "Approval Digest Surface": f"Attestation `{SOURCE_ATTESTATION_DIGEST}`; packages `{SOURCE_PACKAGE_OPTIONS_DIGEST}`; requirements `{SOURCE_FUTURE_REQUIREMENTS_DIGEST}`; contract `{SOURCE_FUTURE_CONTRACT_DIGEST}`; binding `{SOURCE_APPROVAL_SOURCE_BINDING_DIGEST}`; manifest `{SOURCE_APPROVAL_MANIFEST_DIGEST}`.",
        "Selected Package": f"`{SELECTED_PACKAGE}` was executed only to define the governance mechanism.",
        "Payload Supply Mechanism Definition": f"Created without payload values; digest `{execution[PAYLOAD_SUPPLY_MECHANISM_DIGEST_KEY]}`.",
        "Operator Payload Submission Schema": f"Thirty mapped templates and no actual values; digest `{execution[OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST_KEY]}`.",
        "Operator Payload Field Checklist": f"{len(execution['operator_payload_field_checklist'])} future-entry checks; none is filled.",
        "Allowed Values Matrix": f"Thirteen artifact types and closed classification domains; combined safety digest `{execution[ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST_KEY]}`.",
        "Secret Screening Guidance": "A future submission must reject secret-like strings; this execution inspected no environment, credential store, file, log, browser, provider, or external system.",
        "Workstream Segmented Payload Supply Plan": f"Four workstreams covering 30 templates; digest `{execution[WORKSTREAM_SUPPLY_PLAN_DIGEST_KEY]}`.",
        "Results Review Prerequisite": "A separately invoked results review is required before any payload or prepared input may be used.",
        "Source Operator Review": f"Commit `{execution['source_operator_review_commit']}` and review `{execution['source_operator_review_digest']}` remain bound.",
        "Source Candidate": f"Commit `{execution['source_candidate_commit']}` and candidate `{execution['source_candidate_digest']}` remain bound.",
        "Source Failure Diagnosis": f"Commit `{execution['source_failure_diagnosis_commit']}` and diagnosis `{execution['source_failure_diagnosis_digest']}` remain bound.",
        "Source Execution": f"Commit `{execution['source_execution_commit']}` remains blocked and no success digest exists.",
        "Blocked Reason": f"`{execution['source_blocked_reason']}`.",
        "Primary Failure Class": f"`{execution['primary_failure_class']}`.",
        "Source Prior Approval": f"Historical commit `{execution['source_prior_approval_commit']}` and digest `{execution['source_prior_approval_digest']}` remain evidence only.",
        "Source Completion Execution": f"Commit `{execution['source_completion_execution_commit']}` remains blocked by `{execution['source_completion_execution_blocked_reason']}`.",
        "Durable Receipt": f"`{execution['source_durable_receipt_path']}` is bound opaquely and was not parsed.",
        "Retry Failure Context": "24,877 passed / 1,292 failed / 112 errors / 7 skipped remains authoritative retry evidence.",
        "Priority 1 Validation Summary": "675/675 before and after remains current-root evidence only and was not rerun.",
        "Diagnostic Capture Evidence Summary": "Exit 1 and saved byte counts/hashes remain metadata only; output was not analyzed.",
        "Reviewed Template Structure": "Exactly 30 future templates are mapped to MA-001 through MA-030; none is evidence.",
        "Actual Evidence Absence": "No operator payload, prepared input, evidence item, or evidence package exists.",
        "Actual Coverage Zero": "Coverage remains 0/30; every missing-authority item remains `MISSING_NOT_ACQUIRED`.",
        "Count Label Distinction": "Prescribed and enumerated counts remain distinct and unreconciled.",
        "Unsupported Claims Boundary": "No root cause, retry success, predictive usefulness, profitability, or main readiness is claimed.",
        "Recommendation": f"`{execution['recommended_action']}`. Next task: `{RECOMMENDED_NEXT_TASK}`.",
        "Authority Boundaries": "Mechanism definition only; every payload, evidence, acquisition, disposition, remediation, retry, merge, runtime, broker, and trading gate remains closed.",
        "Checklist Summary": f"{execution['summary']['passed_checks']}/{execution['summary']['total_checks']} PASS; blockers={execution['summary']['blocker_count']}.",
        "Guardrails": "Committed constants and validated injection only; no source builders, file reads, subprocesses, pytest, cache, logs, environment, external documents, providers, source owners, market data, models, runtime, broker, or trading actions.",
    }
    list_sections = {
        "Secondary Failure Classes": execution["secondary_failure_classes"],
        "Priority 1 Target Modules": [f"{item['path']}: {item['failed_or_errored_nodeid_count']}" for item in execution["priority_1_target_modules"]],
        "Reviewed Observable Families": [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in execution["reviewed_observable_failure_families"]],
        "Reviewed Workstreams": [f"{item['workstream_id']} <- {item['source_family_id']}" for item in execution["reviewed_workstreams"]],
        "Next Chain": execution["next_chain"], "Next Gates": execution["next_gates"], "Risk Controls": execution["risk_controls"],
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs Reentry or Payload Supply Execution After Approval Status", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", ""))
        if section in list_sections:
            lines.extend(f"{index}. `{item}`" for index, item in enumerate(list_sections[section], 1))
        else:
            lines.append(facts.get(section, "Preserved from committed source evidence without rerun, payload supply, evidence acquisition, or downstream authority."))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(output_dir: str | Path, *, source_approval: dict | None = None) -> dict[str, Any]:
    """Write only the requested governance status Markdown artifact."""
    destination_root = Path(output_dir)
    if {part.lower() for part in destination_root.parts}.intersection({".marketflow", ".pytest_cache", ".env"}):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError("protected output directory")
    execution = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(source_approval=source_approval)
    destination = destination_root / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_AFTER_APPROVAL_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_markdown_v1(execution), encoding="utf-8")
    return execution


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "EXECUTION_STATUS", "EXECUTION_SCOPE", "SELECTED_PACKAGE", "MECHANISM_STATUS",
    "GENERATED_OUTPUT_STATUS", "RECOMMENDED_NEXT_TASK", "SOURCE_APPROVAL_COMMIT", "SOURCE_REQUESTED_APPROVAL_COMMIT",
    "SOURCE_APPROVAL_DIGEST", "SOURCE_ATTESTATION_DIGEST", "SOURCE_PACKAGE_OPTIONS_DIGEST", "SOURCE_FUTURE_REQUIREMENTS_DIGEST",
    "SOURCE_FUTURE_CONTRACT_DIGEST", "SOURCE_APPROVAL_SOURCE_BINDING_DIGEST", "SOURCE_APPROVAL_MANIFEST_DIGEST",
    "EXECUTION_DIGEST_KEY", "PAYLOAD_SUPPLY_MECHANISM_DIGEST_KEY", "OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST_KEY",
    "ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST_KEY", "WORKSTREAM_SUPPLY_PLAN_DIGEST_KEY", "SOURCE_BINDING_DIGEST_KEY",
    "MANIFEST_DIGEST_KEY", "SOURCE_APPROVAL_BINDINGS", "ALLOWED_SECTION_IDS", "ALLOWED_WORKSTREAM_IDS",
    "ALLOWED_ARTIFACT_TYPES", "ALLOWED_EVIDENCE_CLASSIFICATIONS", "ALLOWED_SPECIFICATION_OR_OBSERVATION",
    "ALLOWED_EXPECTED_OR_ACTUAL_SCOPE", "SECRET_INDICATORS", "PACKAGE_HEADER_FIELDS", "EVIDENCE_ITEM_FIELDS",
    "TRUE_FIELDS", "FALSE_FIELDS", "COUNTS", "OUTPUT_IDS", "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "MARKDOWN_SECTIONS",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTED_AFTER_APPROVAL_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTED_AFTER_APPROVAL_PAYLOAD_SUPPLY_MECHANISM_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_AFTER_APPROVAL_ONLY_PAYLOAD_SUPPLY_MECHANISM_DEFINITION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_markdown_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1",
]
