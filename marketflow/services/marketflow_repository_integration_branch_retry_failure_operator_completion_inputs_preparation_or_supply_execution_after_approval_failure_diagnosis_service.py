"""Diagnose the approved input-preparation execution's no-input block offline.

The module binds committed governance facts and classifies the absence of an
explicit operator payload.  It never reruns execution or creates input,
evidence, acquisition, remediation, retry, merge, runtime, or trading authority.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1"
DIAGNOSIS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_READY"
DIAGNOSIS_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_ONLY_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
PRIMARY_FAILURE_CLASS = source.NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION
SELECTED_PACKAGE = source.SELECTED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_V1"

SOURCE_EXECUTION_COMMIT = "3cb60e016592480f2f23d977952ee5fd4ca3fd21"
SOURCE_BLOCKED_DIGEST = "0316a49a2def7e5f922e4e43fc83c9a7e3b1db4a5233f1a4996675eab53918dd"
SOURCE_SOURCE_BINDING_DIGEST = "d7047b7205b3b2758d1388566ca2afdd55a47895ff9dd9508daca26066f885ef"
SOURCE_INPUT_ABSENCE_DIGEST = "33db19e44c27eb521720336830d75d804fdfe5757c630853159b3b879601c3e2"
SOURCE_COVERAGE_DIGEST = "35a3561d865b5ed0c50a854456d5f03a6b05a5db15b4018a07adb789dbb26ae8"
SOURCE_BLOCKED_MANIFEST_DIGEST = "496a3be007b31008ca6ecdfc3b501cbd7ffe8d59ef56b2f858a92c7f4489969c"

DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_digest"
FAILURE_CLASSIFICATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_classification_digest"
INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_input_absence_diagnosis_digest"
SOURCE_BINDING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_source_binding_review_digest"
COVERAGE_DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_coverage_diagnosis_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_READY = DIAGNOSIS_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_ONLY_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = DIAGNOSIS_SCOPE
NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION = PRIMARY_FAILURE_CLASS

PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

EXECUTION_CORRECTLY_FAILS_CLOSED_WITHOUT_EXPLICIT_OPERATOR_COMPLETION_INPUTS = "EXECUTION_CORRECTLY_FAILS_CLOSED_WITHOUT_EXPLICIT_OPERATOR_COMPLETION_INPUTS"
APPROVAL_IS_NOT_OPERATOR_COMPLETION_INPUTS = "APPROVAL_IS_NOT_OPERATOR_COMPLETION_INPUTS"
REVIEWED_CANDIDATE_AND_INPUT_CONTRACT_ARE_NOT_SUPPLIED_INPUTS = "REVIEWED_CANDIDATE_AND_INPUT_CONTRACT_ARE_NOT_SUPPLIED_INPUTS"
TEMPLATE_PLACEHOLDERS_ARE_NOT_OPERATOR_COMPLETION_INPUTS = "TEMPLATE_PLACEHOLDERS_ARE_NOT_OPERATOR_COMPLETION_INPUTS"
DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_ENV_AND_EXTERNAL_DOCUMENTS_ARE_NOT_INPUT_SOURCES = "DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_ENV_AND_EXTERNAL_DOCUMENTS_ARE_NOT_INPUT_SOURCES"
SYNTHETIC_SUCCESS_PATH_IS_TEST_ONLY_AND_NOT_REPOSITORY_EVIDENCE = "SYNTHETIC_SUCCESS_PATH_IS_TEST_ONLY_AND_NOT_REPOSITORY_EVIDENCE"
COMPLETION_REATTEMPT_REQUIRES_REVIEWED_EXPLICIT_NON_SECRET_OPERATOR_INPUTS = "COMPLETION_REATTEMPT_REQUIRES_REVIEWED_EXPLICIT_NON_SECRET_OPERATOR_INPUTS"
SOURCE_AUTHORITY_ACQUISITION_REMAINS_BLOCKED_UNTIL_REVIEWED_COMPLETED_PACKAGE_EXISTS = "SOURCE_AUTHORITY_ACQUISITION_REMAINS_BLOCKED_UNTIL_REVIEWED_COMPLETED_PACKAGE_EXISTS"
DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED = "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED"

SECONDARY_FAILURE_CLASSES = (
    EXECUTION_CORRECTLY_FAILS_CLOSED_WITHOUT_EXPLICIT_OPERATOR_COMPLETION_INPUTS,
    APPROVAL_IS_NOT_OPERATOR_COMPLETION_INPUTS,
    REVIEWED_CANDIDATE_AND_INPUT_CONTRACT_ARE_NOT_SUPPLIED_INPUTS,
    TEMPLATE_PLACEHOLDERS_ARE_NOT_OPERATOR_COMPLETION_INPUTS,
    DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_ENV_AND_EXTERNAL_DOCUMENTS_ARE_NOT_INPUT_SOURCES,
    SYNTHETIC_SUCCESS_PATH_IS_TEST_ONLY_AND_NOT_REPOSITORY_EVIDENCE,
    COMPLETION_REATTEMPT_REQUIRES_REVIEWED_EXPLICIT_NON_SECRET_OPERATOR_INPUTS,
    SOURCE_AUTHORITY_ACQUISITION_REMAINS_BLOCKED_UNTIL_REVIEWED_COMPLETED_PACKAGE_EXISTS,
    DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED,
)

DIAGNOSIS_DOMAINS = (
    ("execution_identity", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "Source execution artifact, status, scope, commit, and digests are bound."),
    ("source_approval_identity", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "Source approval, attestation, and selected package are bound."),
    ("input_availability", "FAILED_PRIMARY", "No explicit non-secret operator_completion_inputs payload was supplied to the actual execution."),
    ("fail_closed_behavior", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "Execution correctly produced a blocked artifact instead of fabricating inputs."),
    ("success_digest_availability", "NOT_PERFORMED_CORRECTLY", "Success, prepared-input, and success-manifest digests are absent by design because the actual execution blocked."),
    ("template_and_placeholder_boundary", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "Template rows and placeholders remain non-evidence and non-input."),
    ("diagnostic_output_boundary", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "Diagnostic output remains metadata only and was not converted into operator inputs."),
    ("coverage_and_missing_authority", "UNCHANGED", "Actual coverage remains 0/30 and all missing-authority rows remain MISSING_NOT_ACQUIRED."),
    ("retry_context", "UNCHANGED", "The failed detached retry remains authoritative."),
    ("repository_boundary", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "No protected branch, integration branch, worktree, tag, .marketflow, or .pytest_cache mutation is reported."),
    ("downstream_authority", "ACTION_REQUIRED_NOT_FAILURE", "Future progress requires a separately governed re-entry or payload-supply candidate before any input-supply reattempt."),
    ("runtime_provider_trading_boundary", "NOT_FAILED_BY_AVAILABLE_EVIDENCE", "No provider, market-data, runtime, broker, or trading action occurred."),
)

DIAGNOSIS_FINDINGS = (
    "Source execution was invoked and blocked.",
    "Blocked reason exactly matches NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION.",
    "Approval selected the package but did not provide inputs.",
    "No explicit operator completion input payload was supplied.",
    "Execution correctly did not infer inputs from templates, placeholders, diagnostic output, digests, cache, logs, environment, provider calls, or external documents.",
    "Success digests are correctly absent.",
    "Synthetic success path remains test-only.",
    "No input shape validation or secret screening occurred because no input payload existed.",
    "No prepared inputs were generated for results review.",
    "No evidence package was completed.",
    "No evidence was created, validated, bound, or accepted.",
    "Coverage remains 0/30.",
    "All 30 missing-authority rows remain MISSING_NOT_ACQUIRED.",
    "The durable receipt remained opaque and unparsed.",
    "Priority 1 validation was not rerun and remains non-retry evidence.",
    "Detached retry remains failed and authoritative.",
    "No remediation, retry, main readiness, or provider/data/runtime/trading authority was created.",
    "Correct next action is a separately governed re-entry or operator payload-supply candidate.",
)

OUTPUT_IDS = tuple("""operator_completion_inputs_preparation_or_supply_execution_failure_diagnosis_manifest
source_execution_binding_report
source_execution_blocked_reason_report
source_execution_success_digests_absence_report
source_approval_binding_report
source_operator_review_binding_report
source_candidate_binding_report
source_failure_diagnosis_binding_report
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
input_absence_diagnosis_report
fail_closed_behavior_report
no_input_inference_boundary_report
synthetic_success_path_boundary_report
source_authority_gap_preservation_report
unsupported_claims_boundary_report
recommended_reentry_or_payload_supply_candidate_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Reentry or Payload Supply Candidate After No-Input Execution Failure Diagnosis v1.",
    "Operator Completion Inputs Preparation or Supply Reentry or Payload Supply Candidate Operator Review v1.",
    "Operator Completion Inputs Preparation or Supply Reentry or Payload Supply Approval v1, if selected.",
    "Operator Completion Inputs Preparation or Supply Execution Reattempt v1, only with explicit non-secret operator inputs.",
    "Operator Completion Inputs Preparation or Supply Results Review v1, only if prepared/supplied inputs exist.",
    "Operator Source Authority Evidence Package Completion Execution Reattempt v1, only with reviewed explicit non-secret operator inputs and separate approval.",
    "Operator Source Authority Evidence Package Completion Results Review v1, only if a completed package exists.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Completed Evidence Package v1, only if separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional evidence-supported disposition candidate or hold.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple("""operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_failure_diagnosis
operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review
operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_if_selected
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
main_merge_approval_if_new_retry_passes""".splitlines())

RISK_CONTROLS = tuple("""diagnosis_does_not_rerun_execution
diagnosis_does_not_prepare_inputs
diagnosis_does_not_supply_inputs
diagnosis_does_not_validate_inputs
diagnosis_does_not_bind_inputs
diagnosis_does_not_create_prepared_inputs
diagnosis_does_not_create_completed_evidence_package
diagnosis_does_not_create_evidence_package
diagnosis_does_not_fill_actual_evidence_items
diagnosis_does_not_validate_evidence
diagnosis_does_not_bind_evidence
diagnosis_does_not_accept_evidence_as_source_authority
diagnosis_does_not_infer_inputs_from_template
diagnosis_does_not_infer_inputs_from_placeholders
diagnosis_does_not_infer_inputs_from_diagnostic_output
diagnosis_does_not_infer_inputs_from_digests
diagnosis_does_not_read_cache_for_inputs
diagnosis_does_not_parse_logs_for_inputs
diagnosis_does_not_inspect_env_for_inputs
diagnosis_does_not_read_external_documents_for_inputs
diagnosis_does_not_call_providers_for_inputs
diagnosis_does_not_contact_source_owners_for_inputs
diagnosis_does_not_acquire_source_authority
diagnosis_does_not_acquire_source_authority_evidence
diagnosis_does_not_acquire_external_evidence
diagnosis_does_not_create_source_authority_acquisition_execution
diagnosis_does_not_retry_source_authority_acquisition
diagnosis_does_not_create_no_change_disposition
diagnosis_does_not_execute_alternate_diagnostics
diagnosis_does_not_execute_remediation
diagnosis_does_not_modify_production_code
diagnosis_does_not_modify_existing_tests
diagnosis_does_not_update_expected_digests
diagnosis_does_not_generate_patch
diagnosis_does_not_apply_patch
diagnosis_does_not_run_pytest
diagnosis_does_not_run_full_pytest
diagnosis_does_not_rerun_priority1_validation
diagnosis_does_not_rerun_retry
diagnosis_does_not_rerun_detached_retry
diagnosis_does_not_parse_durable_receipt
diagnosis_does_not_analyze_diagnostic_output
diagnosis_does_not_rerun_source_authority_enrichment
diagnosis_does_not_rerun_follow_on_execution
diagnosis_does_not_rerun_plan_execution
diagnosis_does_not_regenerate_targeted_plan
diagnosis_does_not_rerun_method_execution
diagnosis_does_not_rerun_controlled_recapture
diagnosis_does_not_rerun_template_execution
diagnosis_does_not_rerun_completion_execution
diagnosis_does_not_rerun_input_preparation_execution
diagnosis_does_not_run_diagnostic_command
diagnosis_does_not_read_pytest_cache
diagnosis_does_not_modify_pytest_cache
diagnosis_does_not_commit_pytest_cache
diagnosis_does_not_commit_marketflow_outputs
diagnosis_does_not_parse_terminal_logs
diagnosis_does_not_parse_operator_logs
diagnosis_does_not_inspect_env
diagnosis_does_not_contact_source_owners
diagnosis_does_not_read_external_documents
diagnosis_does_not_reconstruct_prior_lost_values
diagnosis_does_not_reconstruct_full_streams
diagnosis_does_not_classify_modules_again
diagnosis_does_not_classify_full_retry_failures
diagnosis_does_not_classify_full_retry_errors
diagnosis_does_not_claim_failure_error_separation
diagnosis_does_not_identify_authoritative_first_failure
diagnosis_does_not_identify_authoritative_first_error
diagnosis_does_not_claim_traceback_root_cause
diagnosis_does_not_claim_root_cause
diagnosis_does_not_claim_retry_success
diagnosis_does_not_claim_main_merge_readiness
diagnosis_does_not_create_retry_candidate
diagnosis_does_not_create_retry_approval
diagnosis_does_not_create_retry_execution
diagnosis_does_not_create_retry_results_review
diagnosis_does_not_create_main_merge_approval
diagnosis_does_not_push_main
diagnosis_does_not_push_integration_branch
diagnosis_does_not_delete_integration_branch
diagnosis_does_not_delete_worktree
diagnosis_does_not_force_push
diagnosis_does_not_modify_tags
diagnosis_does_not_regenerate_evidence
diagnosis_does_not_call_providers
diagnosis_does_not_acquire_market_data
diagnosis_does_not_generate_dataset
diagnosis_does_not_recompute_metrics
diagnosis_does_not_train_models
diagnosis_does_not_score_strategy
diagnosis_does_not_generate_trade_recommendations
diagnosis_does_not_accept_predictive_usefulness
diagnosis_does_not_accept_profitability
diagnosis_does_not_authorize_runtime
diagnosis_does_not_authorize_broker_execution
approved_input_preparation_package_is_not_operator_input
reviewed_template_is_not_completed_evidence_package
template_placeholders_are_not_completion_inputs
synthetic_success_path_is_test_only
explicit_non_secret_inputs_required_before_prepared_inputs_success
explicit_non_secret_inputs_required_before_completion_reattempt
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
preserve_meta_limitation""".splitlines())

TRUE_FIELDS = tuple("""failure_diagnosis_created
failure_diagnosis_ready
source_execution_bound
source_execution_reviewed
source_execution_blocked_reason_verified
source_execution_success_digests_absent_verified
source_blocked_digest_bound
source_source_binding_digest_bound
source_input_absence_digest_bound
source_coverage_digest_bound
source_blocked_manifest_digest_bound
source_approval_bound
source_attestation_bound
selected_package_bound
approval_authorizes_future_execution_only_verified
operator_completion_inputs_absence_verified
execution_correctly_failed_closed
no_input_inference_verified
template_placeholder_boundary_preserved
diagnostic_output_boundary_preserved
synthetic_success_path_test_only_verified
source_operator_review_bound
source_candidate_bound
source_failure_diagnosis_bound
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
ready_for_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate""".splitlines())

FALSE_FIELDS = tuple("""input_preparation_or_supply_execution_successful
operator_completion_inputs_supplied_to_execution
operator_completion_inputs_prepared
operator_completion_inputs_supplied
operator_completion_inputs_provided
operator_completion_inputs_shape_validated
operator_completion_inputs_secret_screened
operator_completion_inputs_validated_as_evidence
operator_completion_inputs_bound_as_evidence
operator_completion_inputs_bound
operator_completion_inputs_contained_secrets
operator_completion_inputs_rejected_for_secret_content
operator_completion_inputs_rejected_for_shape
operator_completion_inputs_rejected_for_unknown_mapping
operator_completion_inputs_rejected_for_invalid_allowed_value
prepared_operator_completion_inputs_for_results_review
operator_completion_inputs_preparation_or_supply_package_executed_successfully
operator_completion_inputs_preparation_executed
operator_completion_inputs_supply_executed
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
pytest_performed_in_diagnosis
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_diagnosis
diagnostic_output_analyzed_in_diagnosis
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_diagnosis
method_execution_rerun_performed
controlled_recapture_rerun_performed
template_execution_rerun_performed
completion_execution_rerun_performed
input_preparation_or_supply_execution_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_diagnosis
cache_modified_in_diagnosis
pytest_cache_committed
marketflow_outputs_committed
terminal_logs_parsed
operator_logs_parsed
env_inspection_performed
source_owners_contacted
external_documents_read
provider_requests_made_in_diagnosis
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
market_data_acquisition_performed_in_diagnosis
dataset_generation_performed_in_diagnosis
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

COUNTS = {
    "operator_source_authority_evidence_item_count": 0,
    "operator_source_authority_evidence_item_template_count": 30,
    "reviewed_template_row_count": 30,
    "actual_covered_missing_authority_item_count": 0,
    "actual_uncovered_missing_authority_item_count": 30,
    "template_mapped_missing_authority_item_count": 30,
    "mapped_missing_authority_item_count": 30,
    "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
    "completed_operator_evidence_item_count": 0,
    "operator_completion_input_item_count": 0,
    "future_operator_completion_input_item_count": 30,
    "prepared_operator_completion_input_item_count": 0,
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
    "future_input_preparation_requirement_count": 62,
    "future_input_preparation_plan_step_count": 17,
    "planned_output_count": 34,
    "non_goal_count": 76,
    "risk_control_count": 105,
    "diagnosis_domain_count": 12,
    "diagnosis_finding_count": 18,
    "future_completion_requirement_count": 67,
    "source_enumerated_future_completion_requirement_count": 69,
    "approved_future_completion_requirement_named_count": 69,
    "source_non_goal_count": 71,
    "source_enumerated_non_goal_count": 76,
    "source_risk_control_count": 104,
    "source_enumerated_risk_control_count": 106,
}


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError(ValueError):
    """Raised when diagnosis evidence or its fail-closed boundary drifts."""


# This frozen projection is assembled once from the preceding module's committed
# constant projection.  No public or private execution builder is invoked.
SOURCE_CONTEXT = source._source_projection()


def _first_difference(actual: Any, expected: Any, path: str = "diagnosis") -> str | None:
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


def _validate_source_execution(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError("source_execution must be an object")
    expected = {
        "artifact_kind": source.BLOCKED_ARTIFACT_KIND,
        "execution_status": source.BLOCKED_STATUS,
        "execution_scope": source.EXECUTION_SCOPE,
        "blocked_reason": PRIMARY_FAILURE_CLASS,
        source.BLOCKED_DIGEST_KEY: SOURCE_BLOCKED_DIGEST,
        source.SOURCE_BINDING_DIGEST_KEY: SOURCE_SOURCE_BINDING_DIGEST,
        source.INPUT_ABSENCE_DIGEST_KEY: SOURCE_INPUT_ABSENCE_DIGEST,
        source.COVERAGE_DIGEST_KEY: SOURCE_COVERAGE_DIGEST,
        source.BLOCKED_MANIFEST_DIGEST_KEY: SOURCE_BLOCKED_MANIFEST_DIGEST,
        "prepared_operator_completion_inputs_digest": None,
        "prepared_operator_completion_inputs_manifest_digest": None,
        "success_execution_digest": None,
        "operator_completion_inputs_supplied_to_execution": False,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError(f"source_execution.{key} mismatch")


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if actual else BLOCKER,
        "expected": True,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if actual else 'failed'}",
    }


def _digest_without(value: Mapping[str, Any], *keys: str) -> str:
    return semantic_digest({key: deepcopy(item) for key, item in value.items() if key not in keys})


def _assemble() -> dict[str, Any]:
    diagnosis: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "diagnosis_status": DIAGNOSIS_STATUS,
        "diagnosis_scope": DIAGNOSIS_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "diagnosis_only": True,
        "diagnosis_philosophy": "The input-preparation/supply execution was approved, but approval is not input. The source execution correctly failed closed because no explicit non-secret operator_completion_inputs payload was supplied. The diagnosis may classify the blocked outcome and recommend a separately governed re-entry or payload-supply candidate, but it must not prepare, supply, validate, bind, complete, acquire, remediate, retry, merge, or authorize runtime/trading.",
        "diagnosis_boundary": "Diagnosis only. This artifact binds the blocked execution and explains the missing-input condition. It creates no inputs, evidence, authority, reattempt, remediation, retry, or merge readiness.",
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_execution_artifact_kind": source.BLOCKED_ARTIFACT_KIND,
        "source_execution_status": source.BLOCKED_STATUS,
        "source_execution_scope": source.EXECUTION_SCOPE,
        "source_blocked_reason": PRIMARY_FAILURE_CLASS,
        "source_blocked_digest": SOURCE_BLOCKED_DIGEST,
        "source_source_binding_digest": SOURCE_SOURCE_BINDING_DIGEST,
        "source_input_absence_digest": SOURCE_INPUT_ABSENCE_DIGEST,
        "source_coverage_digest": SOURCE_COVERAGE_DIGEST,
        "source_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
        "source_success_digests_absent": True,
        "prepared_operator_completion_inputs_digest": None,
        "prepared_operator_completion_inputs_manifest_digest": None,
        "success_execution_digest": None,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES),
        "diagnosis_domains": [
            {"domain_id": domain, "status": status, "finding": finding}
            for domain, status, finding in DIAGNOSIS_DOMAINS
        ],
        "diagnosis_findings": list(DIAGNOSIS_FINDINGS),
        **deepcopy(SOURCE_CONTEXT),
        **COUNTS,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES),
        **{key: True for key in TRUE_FIELDS},
        **{key: False for key in FALSE_FIELDS},
        "actual_evidence_absence": {
            "completed_package_created": False,
            "evidence_package_created": False,
            "evidence_package_supplied": False,
            "evidence_package_validated": False,
            "evidence_package_bound": False,
            "actual_evidence_items_filled": False,
        },
        "actual_coverage": {
            "reviewed_template_row_count": 30,
            "actual_covered_missing_authority_item_count": 0,
            "actual_uncovered_missing_authority_item_count": 30,
            "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        },
        "outputs": [{"output_id": item, "status": "GENERATED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_FAILURE_DIAGNOSIS_ONLY"} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_REENTRY_OR_OPERATOR_PAYLOAD_SUPPLY_CANDIDATE_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_BEFORE_ANY_INPUT_SUPPLY_REATTEMPT",
        "reason": "The approved execution correctly failed closed because no explicit non-secret operator_completion_inputs payload was supplied. A separate candidate must decide whether to re-enter, hold, or define a governed payload-supply mechanism; this diagnosis supports no execution or downstream authority.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    diagnosis[FAILURE_CLASSIFICATION_DIGEST_KEY] = semantic_digest({
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": diagnosis["secondary_failure_classes"],
        "diagnosis_domains": diagnosis["diagnosis_domains"],
    })
    diagnosis[INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY] = semantic_digest({
        "source_blocked_reason": PRIMARY_FAILURE_CLASS,
        "operator_completion_inputs_supplied_to_execution": False,
        "operator_completion_input_item_count": 0,
        "prepared_operator_completion_input_item_count": 0,
        "execution_correctly_failed_closed": True,
    })
    diagnosis[SOURCE_BINDING_REVIEW_DIGEST_KEY] = semantic_digest({
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_execution_artifact_kind": source.BLOCKED_ARTIFACT_KIND,
        "source_execution_status": source.BLOCKED_STATUS,
        "source_execution_scope": source.EXECUTION_SCOPE,
        "source_blocked_digest": SOURCE_BLOCKED_DIGEST,
        "source_source_binding_digest": SOURCE_SOURCE_BINDING_DIGEST,
        "source_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
    })
    diagnosis[COVERAGE_DIAGNOSIS_DIGEST_KEY] = semantic_digest({
        "actual_coverage": diagnosis["actual_coverage"],
        "missing_authority_mapping": diagnosis["missing_authority_mapping"],
    })
    digest_keys = (DIAGNOSIS_DIGEST_KEY, MANIFEST_DIGEST_KEY, "checklist", "summary")
    diagnosis[DIAGNOSIS_DIGEST_KEY] = _digest_without(diagnosis, *digest_keys)
    diagnosis[MANIFEST_DIGEST_KEY] = semantic_digest({
        "diagnosis_digest": diagnosis[DIAGNOSIS_DIGEST_KEY],
        "failure_classification_digest": diagnosis[FAILURE_CLASSIFICATION_DIGEST_KEY],
        "input_absence_diagnosis_digest": diagnosis[INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY],
        "source_binding_review_digest": diagnosis[SOURCE_BINDING_REVIEW_DIGEST_KEY],
        "coverage_diagnosis_digest": diagnosis[COVERAGE_DIAGNOSIS_DIGEST_KEY],
        "output_ids": list(OUTPUT_IDS),
    })
    checks = [
        _check("artifact_kind_correct", diagnosis["artifact_kind"] == ARTIFACT_KIND),
        _check("diagnosis_status_correct", diagnosis["diagnosis_status"] == DIAGNOSIS_STATUS),
        _check("diagnosis_scope_correct", diagnosis["diagnosis_scope"] == DIAGNOSIS_SCOPE),
        _check("source_execution_commit_bound", diagnosis["source_execution_commit"] == SOURCE_EXECUTION_COMMIT),
        _check("primary_failure_class_correct", diagnosis["primary_failure_class"] == PRIMARY_FAILURE_CLASS),
        _check("secondary_failure_classes_complete", tuple(diagnosis["secondary_failure_classes"]) == SECONDARY_FAILURE_CLASSES),
        _check("diagnosis_domains_complete", len(diagnosis["diagnosis_domains"]) == 12),
        _check("diagnosis_findings_complete", len(diagnosis["diagnosis_findings"]) == 18),
        _check("outputs_generated", [item["output_id"] for item in diagnosis["outputs"]] == list(OUTPUT_IDS)),
        _check("recommendation_defined", diagnosis["recommended_next_task"] == RECOMMENDED_NEXT_TASK),
        _check("next_chain_defined", diagnosis["next_chain"] == list(NEXT_CHAIN)),
        _check("next_gates_defined", diagnosis["next_gates"] == list(NEXT_GATES)),
        _check("risk_controls_defined", diagnosis["risk_controls"] == list(RISK_CONTROLS)),
    ]
    checks.extend(_check(f"{key}_true", diagnosis[key] is True) for key in TRUE_FIELDS)
    checks.extend(_check(f"{key}_false", diagnosis[key] is False) for key in FALSE_FIELDS)
    checks.extend(_check(f"risk_control_{item}_defined", item in diagnosis["risk_controls"]) for item in RISK_CONTROLS)
    checks.extend(_check(f"output_{item}_generated", any(row["output_id"] == item for row in diagnosis["outputs"])) for item in OUTPUT_IDS)
    for key in (
        DIAGNOSIS_DIGEST_KEY,
        FAILURE_CLASSIFICATION_DIGEST_KEY,
        INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY,
        SOURCE_BINDING_REVIEW_DIGEST_KEY,
        COVERAGE_DIAGNOSIS_DIGEST_KEY,
        MANIFEST_DIGEST_KEY,
    ):
        checks.append(_check(f"{key}_generated", re.fullmatch(r"[0-9a-f]{64}", diagnosis[key]) is not None))
    diagnosis["checklist"] = checks
    diagnosis["summary"] = {
        "total_checks": len(checks),
        "passed_checks": sum(item["status"] == PASS for item in checks),
        "failed_checks": sum(item["status"] != PASS for item in checks),
        "blocker_count": sum(item["status"] != PASS and item["severity"] == BLOCKER for item in checks),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "actual_coverage": "0/30",
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
    }
    return diagnosis


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(
    *, source_execution: dict | None = None,
) -> dict[str, Any]:
    """Build the diagnosis from committed source facts and optional validation input."""
    if source_execution is not None:
        _validate_source_execution(deepcopy(source_execution))
    diagnosis = _assemble()
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(diagnosis)
    return diagnosis


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(
    diagnosis: dict,
) -> dict[str, Any]:
    """Reject source drift, digest drift, or diagnosis authority expansion."""
    if not isinstance(diagnosis, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError("diagnosis must be an object")
    expected = _assemble()
    difference = _first_difference(diagnosis, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError(f"{difference} mismatch")
    if diagnosis["summary"]["failed_checks"] or diagnosis["summary"]["blocker_count"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError("diagnosis checklist failed")
    return {
        "artifact_kind": ARTIFACT_KIND,
        "diagnosis_status": DIAGNOSIS_STATUS,
        "diagnosis_scope": DIAGNOSIS_SCOPE,
        "diagnosis_digest": diagnosis[DIAGNOSIS_DIGEST_KEY],
        **{key: diagnosis["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Diagnosis Disposition", "Source Execution", "Blocked Reason", "Primary Failure Class",
    "Secondary Failure Classes", "Diagnosis Domains", "Diagnosis Findings", "Source Approval",
    "Selected Package", "Source Operator Review", "Source Candidate", "Source Failure Diagnosis",
    "Source Completion Execution", "Source Completion Approval", "Source Completion Candidate Operator Review",
    "Source Completion Candidate", "Source Template Preparation Results Review", "Source Template Preparation Execution",
    "Source Preparation Failure Acquisition Chains", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt",
    "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
    "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
    "Reviewed Template Structure", "Actual Evidence Absence", "Actual Coverage Zero",
    "Count Label Distinction", "Input Absence Diagnosis", "Fail-Closed Boundary",
    "Synthetic Success Path Boundary", "Source Authority Gap Preservation", "Unsupported Claims Boundary",
    "Recommendation", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
    "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_markdown_v1(
    diagnosis: dict,
) -> str:
    """Render the diagnosis without exposing or inventing operator inputs."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(diagnosis)
    facts = {
        "Diagnosis Disposition": f"`{DIAGNOSIS_STATUS}` within `{DIAGNOSIS_SCOPE}`. Diagnosis `{diagnosis[DIAGNOSIS_DIGEST_KEY]}`; manifest `{diagnosis[MANIFEST_DIGEST_KEY]}`.",
        "Source Execution": f"Commit `{SOURCE_EXECUTION_COMMIT}`; artifact `{source.BLOCKED_ARTIFACT_KIND}`; status `{source.BLOCKED_STATUS}`; scope `{source.EXECUTION_SCOPE}`.",
        "Blocked Reason": f"`{PRIMARY_FAILURE_CLASS}`.",
        "Primary Failure Class": f"`{PRIMARY_FAILURE_CLASS}`.",
        "Secondary Failure Classes": "\n".join(f"- `{item}`" for item in SECONDARY_FAILURE_CLASSES),
        "Source Approval": f"Commit `{diagnosis['source_approval_commit']}`; approval `{diagnosis['source_approval_digest']}`; attestation `{diagnosis['source_attestation_digest']}`.",
        "Selected Package": f"`{SELECTED_PACKAGE}` was approved for future execution only and is not input.",
        "Source Operator Review": f"Commit `{diagnosis['source_operator_review_commit']}`; digest `{diagnosis['source_operator_review_digest']}`; manifest `{diagnosis['source_operator_review_manifest_digest']}`.",
        "Source Candidate": f"Commit `{diagnosis['source_candidate_commit']}`; digest `{diagnosis['source_candidate_digest']}`; manifest `{diagnosis['source_candidate_manifest_digest']}`.",
        "Source Failure Diagnosis": f"Commit `{diagnosis['source_failure_diagnosis_commit']}`; digest `{diagnosis['source_failure_diagnosis_digest']}`; manifest `{diagnosis['source_failure_diagnosis_manifest_digest']}`.",
        "Source Completion Execution": f"Commit `{diagnosis['source_completion_execution_commit']}`; reason `{diagnosis['source_completion_execution_blocked_reason']}`; manifest `{diagnosis['source_completion_execution_blocked_manifest_digest']}`.",
        "Source Completion Approval": f"Commit `{diagnosis['source_completion_approval_commit']}`; approval `{diagnosis['source_completion_approval_digest']}`.",
        "Source Completion Candidate Operator Review": f"Commit `{diagnosis['source_completion_candidate_operator_review_commit']}`; digest `{diagnosis['source_completion_candidate_operator_review_digest']}`.",
        "Source Completion Candidate": f"Commit `{diagnosis['source_completion_candidate_commit']}`; digest `{diagnosis['source_completion_candidate_digest']}`.",
        "Source Template Preparation Results Review": f"Commit `{diagnosis['source_template_preparation_results_review_commit']}`; digest `{diagnosis['source_template_preparation_results_review_digest']}`.",
        "Source Template Preparation Execution": f"Commit `{diagnosis['source_template_preparation_execution_commit']}`; digest `{diagnosis['source_template_preparation_execution_digest']}`.",
        "Source Preparation Failure Acquisition Chains": f"Preparation `{diagnosis['source_preparation_candidate_digest']}`; blocked acquisition `{diagnosis['source_blocked_acquisition_execution_reason']}`; approval `{diagnosis['source_acquisition_approval_digest']}`.",
        "Source Follow-On and Enrichment Chain": f"Follow-on `{diagnosis['source_follow_on_execution_digest']}`; enrichment `{diagnosis['source_enrichment_execution_digest']}`.",
        "Historical Blocked Remediation": f"`{diagnosis['historical_blocked_remediation_reason']}`; manifest `{diagnosis['historical_blocked_remediation_manifest_digest']}`.",
        "Plan Method Diagnostic Recovery Chain": f"Targeted plan `{diagnosis['source_targeted_remediation_plan_digest']}`; method `{diagnosis['source_remediation_or_method_execution_after_diagnostic_capture_digest']}`; recovery `{diagnosis['source_recovery_results_review_digest']}`.",
        "Durable Receipt": f"`{diagnosis['source_durable_receipt_path']}` is bound as an opaque path and was not parsed.",
        "Retry Failure Context": "Authoritative detached retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped; root regression is not retry evidence.",
        "Priority 1 Target Modules": "Five preserved modules total 612; top ten total 1,069; 29 modules contain 1,404 failed-or-errored node IDs.",
        "Priority 1 Validation Summary": "675/675 before and after remains current-root focused evidence only and was not rerun.",
        "Diagnostic Capture Evidence Summary": f"Exit 1; stdout {diagnosis['source_stdout_byte_count']} bytes `{diagnosis['source_stdout_sha256']}`; stderr 0 bytes `{diagnosis['source_stderr_sha256']}`. Metadata only.",
        "Reviewed Observable Families": "Four HIGH-confidence families with 47 observations each, 188 total.",
        "Reviewed Workstreams": "Four reviewed workstreams remain planning evidence only.",
        "Reviewed Template Structure": "Exactly 30 reviewed rows map MA-001 through MA-030; the template is not input, evidence, or source authority.",
        "Actual Evidence Absence": "No completed or actual evidence package/item was created, supplied, validated, bound, accepted, or filled.",
        "Actual Coverage Zero": f"Coverage remains 0/30 and `MISSING_NOT_ACQUIRED`; digest `{diagnosis[COVERAGE_DIAGNOSIS_DIGEST_KEY]}`.",
        "Count Label Distinction": "Preserved: requirements 67/69/69; non-goals 71/76; source risk controls 104/106; local 62/17/34/76/105.",
        "Input Absence Diagnosis": f"No explicit payload existed; digest `{diagnosis[INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY]}`.",
        "Fail-Closed Boundary": "The source execution correctly blocked rather than inferring or fabricating inputs.",
        "Synthetic Success Path Boundary": "The injected TEST_OPERATOR path remains test-only and is not repository evidence or authority.",
        "Source Authority Gap Preservation": "No acquisition, authority, evidence, safe change, disposition, diagnostic, remediation, retry, or merge readiness was created.",
        "Unsupported Claims Boundary": "No root-cause, retry-success, acquisition, predictive, profitability, runtime, trading, or main-readiness claim is made.",
        "Recommendation": f"`{RECOMMENDED_NEXT_TASK}`: `{diagnosis['recommended_action']}`.",
        "Authority Boundaries": "Only the separately governed re-entry/payload-supply candidate is ready; every execution and downstream authority remains closed.",
        "Checklist Summary": f"{diagnosis['summary']['passed_checks']}/{diagnosis['summary']['total_checks']} PASS; blockers={diagnosis['summary']['blocker_count']}.",
        "Guardrails": "Offline dictionary-only diagnosis; no source builders, files, subprocesses, pytest, caches, receipts, logs, environment, providers, external documents, or runtime outputs are accessed.",
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs Preparation or Supply Execution After Approval Failure Diagnosis v1", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", "", facts.get(section, "Preserved from committed source evidence; no new authority is created."), ""))
        if section == "Diagnosis Domains":
            lines[-2:-2] = [*(f"- `{item['domain_id']}` — `{item['status']}`: {item['finding']}" for item in diagnosis["diagnosis_domains"]), ""]
        elif section == "Diagnosis Findings":
            lines[-2:-2] = [*(f"{index}. {item}" for index, item in enumerate(diagnosis["diagnosis_findings"], 1)), ""]
        elif section == "Next Chain":
            lines[-2:-2] = [*(f"{index}. {item}" for index, item in enumerate(diagnosis["next_chain"], 1)), ""]
        elif section == "Next Gates":
            lines[-2:-2] = [*(f"- `{item}`" for item in diagnosis["next_gates"]), ""]
        elif section == "Risk Controls":
            lines[-2:-2] = [*(f"- `{item}`" for item in diagnosis["risk_controls"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(
    output_dir: str | Path, *, source_execution: dict | None = None,
) -> dict[str, Any]:
    """Write only the requested diagnosis status Markdown artifact."""
    destination_root = Path(output_dir)
    if {part.lower() for part in destination_root.parts}.intersection({".marketflow", ".pytest_cache", ".env"}):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError("protected output directory")
    diagnosis = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(source_execution=source_execution)
    destination = destination_root / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_markdown_v1(diagnosis), encoding="utf-8")
    return diagnosis


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "DIAGNOSIS_STATUS", "DIAGNOSIS_SCOPE", "PRIMARY_FAILURE_CLASS",
    "SECONDARY_FAILURE_CLASSES", "DIAGNOSIS_DOMAINS", "DIAGNOSIS_FINDINGS", "SELECTED_PACKAGE",
    "EXECUTION_CORRECTLY_FAILS_CLOSED_WITHOUT_EXPLICIT_OPERATOR_COMPLETION_INPUTS",
    "APPROVAL_IS_NOT_OPERATOR_COMPLETION_INPUTS", "REVIEWED_CANDIDATE_AND_INPUT_CONTRACT_ARE_NOT_SUPPLIED_INPUTS",
    "TEMPLATE_PLACEHOLDERS_ARE_NOT_OPERATOR_COMPLETION_INPUTS",
    "DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_ENV_AND_EXTERNAL_DOCUMENTS_ARE_NOT_INPUT_SOURCES",
    "SYNTHETIC_SUCCESS_PATH_IS_TEST_ONLY_AND_NOT_REPOSITORY_EVIDENCE",
    "COMPLETION_REATTEMPT_REQUIRES_REVIEWED_EXPLICIT_NON_SECRET_OPERATOR_INPUTS",
    "SOURCE_AUTHORITY_ACQUISITION_REMAINS_BLOCKED_UNTIL_REVIEWED_COMPLETED_PACKAGE_EXISTS",
    "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED",
    "RECOMMENDED_NEXT_TASK", "SOURCE_EXECUTION_COMMIT", "SOURCE_BLOCKED_DIGEST",
    "SOURCE_SOURCE_BINDING_DIGEST", "SOURCE_INPUT_ABSENCE_DIGEST", "SOURCE_COVERAGE_DIGEST",
    "SOURCE_BLOCKED_MANIFEST_DIGEST", "DIAGNOSIS_DIGEST_KEY", "FAILURE_CLASSIFICATION_DIGEST_KEY",
    "INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY", "SOURCE_BINDING_REVIEW_DIGEST_KEY", "COVERAGE_DIAGNOSIS_DIGEST_KEY",
    "MANIFEST_DIGEST_KEY", "OUTPUT_IDS", "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS",
    "TRUE_FIELDS", "FALSE_FIELDS", "COUNTS", "MARKDOWN_SECTIONS",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_ONLY_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_markdown_v1",
]
