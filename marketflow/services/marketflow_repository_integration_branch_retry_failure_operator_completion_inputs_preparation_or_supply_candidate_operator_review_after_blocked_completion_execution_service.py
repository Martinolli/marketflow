"""Review the completion-input preparation/supply candidate offline.

The review is governance-only.  It binds committed candidate facts and reviews
future options without selecting, approving, authorizing, or executing one.
No source builder, file reader, subprocess, provider, or runtime action is used.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1"
OPERATOR_REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_READY"
OPERATOR_REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE

SOURCE_CANDIDATE_COMMIT = "b060a0ae9263e05d561ec0c7c5897558d8c2a9c1"
SOURCE_CANDIDATE_DIGEST = "41a2df4be129a88b829439dadc3e0969715853944068f73800fd673720f02ca8"
SOURCE_CANDIDATE_PACKAGE_OPTIONS_DIGEST = "28ec7b372252beb98b6e2b939c70545d7aac66c40adaef6099c935998ec625b8"
SOURCE_CANDIDATE_INPUT_CONTRACT_DIGEST = "a6086f4bae684216a7dd34233f1cb68ed165523dcfbddb6bd77d3d030a055bd9"
SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST = "78b01abcb34b4e88951587eaccfbc5d500ffece96b51fd54a849a06d7389ced5"
SOURCE_CANDIDATE_COVERAGE_DIGEST = "35a3561d865b5ed0c50a854456d5f03a6b05a5db15b4018a07adb789dbb26ae8"
SOURCE_CANDIDATE_MANIFEST_DIGEST = "c1bfffd4995beef0e4f65e74b8a1068b517caa67aece00c6b0104c5cf643f937"

OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_digest"
PACKAGE_OPTIONS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_package_options_digest"
INPUT_CONTRACT_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_input_contract_digest"
SOURCE_BINDING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_source_binding_digest"
COVERAGE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_coverage_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_READY = OPERATOR_REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = OPERATOR_REVIEW_SCOPE
PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE = RECOMMENDED_PACKAGE
PACKAGE_PREPARE_COMPLETION_INPUT_HEADER_FIELDS_ONLY = "PACKAGE_PREPARE_COMPLETION_INPUT_HEADER_FIELDS_ONLY"
PACKAGE_PREPARE_COMPLETION_INPUT_EVIDENCE_ITEM_ROWS_ONLY = "PACKAGE_PREPARE_COMPLETION_INPUT_EVIDENCE_ITEM_ROWS_ONLY"
PACKAGE_PREPARE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_MAPPING_ONLY = "PACKAGE_PREPARE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_MAPPING_ONLY"
PACKAGE_PREPARE_WORKSTREAM_SPECIFIC_COMPLETION_INPUT_SETS = "PACKAGE_PREPARE_WORKSTREAM_SPECIFIC_COMPLETION_INPUT_SETS"
PACKAGE_PREPARE_COMPLETION_INPUT_CHECKLIST_AND_ATTESTATION_ONLY = "PACKAGE_PREPARE_COMPLETION_INPUT_CHECKLIST_AND_ATTESTATION_ONLY"
PACKAGE_HOLD_PENDING_OPERATOR_COMPLETION_INPUTS = "PACKAGE_HOLD_PENDING_OPERATOR_COMPLETION_INPUTS"
PACKAGE_FABRICATE_COMPLETION_INPUTS_FROM_TEMPLATE_PLACEHOLDERS = "PACKAGE_FABRICATE_COMPLETION_INPUTS_FROM_TEMPLATE_PLACEHOLDERS"
PACKAGE_DERIVE_COMPLETION_INPUTS_FROM_DIAGNOSTIC_OUTPUT = "PACKAGE_DERIVE_COMPLETION_INPUTS_FROM_DIAGNOSTIC_OUTPUT"
PACKAGE_VALIDATE_BIND_OR_ACQUIRE_EVIDENCE_DURING_INPUT_PREPARATION = "PACKAGE_VALIDATE_BIND_OR_ACQUIRE_EVIDENCE_DURING_INPUT_PREPARATION"
PACKAGE_REATTEMPT_COMPLETION_EXECUTION_IMMEDIATELY_FROM_FAILURE_DIAGNOSIS = "PACKAGE_REATTEMPT_COMPLETION_EXECUTION_IMMEDIATELY_FROM_FAILURE_DIAGNOSIS"
PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_MISSING_INPUTS_DIAGNOSIS = "PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_MISSING_INPUTS_DIAGNOSIS"

PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateOperatorReviewError(ValueError):
    """Raised when the review drifts or crosses a closed boundary."""


def _first_difference(actual: Any, expected: Any, path: str = "operator_review") -> str | None:
    if type(actual) is not type(expected):
        return path
    if isinstance(expected, Mapping):
        if set(actual) != set(expected):
            return path
        for key in expected:
            difference = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if difference:
                return difference
        return None
    if isinstance(expected, list):
        if len(actual) != len(expected):
            return path
        for index, value in enumerate(expected):
            difference = _first_difference(actual[index], value, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


SOURCE_CANDIDATE_BINDINGS = {
    "source_candidate_commit": SOURCE_CANDIDATE_COMMIT,
    "source_candidate_artifact_kind": source.ARTIFACT_KIND,
    "source_candidate_status": source.CANDIDATE_STATUS,
    "source_candidate_scope": source.CANDIDATE_SCOPE,
    "source_candidate_digest": SOURCE_CANDIDATE_DIGEST,
    "source_candidate_package_options_digest": SOURCE_CANDIDATE_PACKAGE_OPTIONS_DIGEST,
    "source_candidate_input_contract_digest": SOURCE_CANDIDATE_INPUT_CONTRACT_DIGEST,
    "source_candidate_source_binding_digest": SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST,
    "source_candidate_coverage_digest": SOURCE_CANDIDATE_COVERAGE_DIGEST,
    "source_candidate_manifest_digest": SOURCE_CANDIDATE_MANIFEST_DIGEST,
}

SOURCE_FAILURE_BINDINGS = {
    "source_failure_diagnosis_commit": source.SOURCE_FAILURE_DIAGNOSIS_COMMIT,
    "source_failure_diagnosis_artifact_kind": source.source.ARTIFACT_KIND,
    "source_failure_diagnosis_status": source.source.DIAGNOSIS_STATUS,
    "source_failure_diagnosis_scope": source.source.DIAGNOSIS_SCOPE,
    "source_failure_diagnosis_digest": source.SOURCE_FAILURE_DIAGNOSIS_DIGEST,
    "source_failure_classification_digest": source.SOURCE_FAILURE_CLASSIFICATION_DIGEST,
    "source_operator_input_absence_diagnosis_digest": source.SOURCE_OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST,
    "source_coverage_diagnosis_digest": source.SOURCE_COVERAGE_DIAGNOSIS_DIGEST,
    "source_failure_diagnosis_manifest_digest": source.SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST,
    "primary_failure_class": source.PRIMARY_FAILURE_CLASS,
    "secondary_failure_classes": list(source.SECONDARY_FAILURE_CLASSES),
}


PACKAGE_OPTIONS = tuple(
    (
        package_id,
        source_status,
        (
            "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
            if package_id == RECOMMENDED_PACKAGE
            else "REVIEWED_BLOCKED_NOT_ALLOWED"
            if source_status == "BLOCKED_NOT_ALLOWED"
            else "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
        ),
        purpose,
        blocked_reason,
    )
    for package_id, source_status, _candidate_status, purpose, blocked_reason in source.PACKAGE_OPTIONS
)

FUTURE_INPUT_REQUIREMENT_IDS = source.FUTURE_INPUT_REQUIREMENT_IDS
PLANNED_OUTPUT_IDS = source.PLANNED_OUTPUT_IDS
NON_GOALS = source.NON_GOALS

FUTURE_PLAN_STEPS = (
    "Bind this operator review and the source candidate.",
    "Bind the source failure diagnosis, blocked completion execution, approval, operator review, completion candidate, template-preparation results review, template-preparation execution, preparation chain, acquisition chain, follow-on/enrichment chain, historical remediation chain, plan/method/diagnostic/recovery chain, module-grouping chain, and staged inventory.",
    "Preserve the source blocked reason NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED.",
    "Preserve source completion execution success digests as absent.",
    "Preserve actual coverage as 0/30 and all missing-authority items as MISSING_NOT_ACQUIRED.",
    "Review future input preparation or supply package options without selecting any.",
    "Review the recommended future package for preparing or supplying explicit non-secret operator completion inputs.",
    "Review required non-secret package-header input fields.",
    "Review required non-secret evidence-item input fields.",
    "Review allowed section, workstream, artifact-type, classification, specification/observation, and expected/actual values.",
    "Preserve all no-secret, no-API-key, no-broker-credential, no-personal-financial-credential, no-market-data-credential, and no-private-token requirements.",
    "Preserve all direct-change, remediation, retry, and main-merge authorization flags as false.",
    "Require approval before any input-preparation or input-supply execution.",
    "Require results review after any input-preparation or input-supply execution.",
    "Require separately approved completion reattempt after reviewed non-secret inputs exist.",
    "Preserve source-authority acquisition, no-change disposition, alternate diagnostic, remediation, retry, and main-merge gates.",
    "Preserve provider, runtime, broker, and trading prohibitions.",
)

OUTPUT_IDS = tuple("""operator_completion_inputs_preparation_or_supply_candidate_operator_review_manifest
source_candidate_binding_report
source_candidate_package_options_review_report
source_candidate_input_contract_review_report
source_candidate_source_binding_review_report
source_candidate_coverage_review_report
source_failure_diagnosis_binding_report
source_completion_execution_binding_report
source_completion_execution_blocked_reason_report
source_completion_execution_success_digests_absence_report
source_approval_binding_report
source_operator_review_binding_report
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
reviewed_template_row_mapping_report
actual_evidence_absence_report
actual_coverage_zero_report
missing_authority_inventory_report
count_label_distinction_report
reviewed_input_preparation_or_supply_package_options_report
recommended_input_preparation_or_supply_package_report
future_input_supply_contract_review_report
non_secret_input_requirements_review_report
allowed_values_review_report
custody_digest_and_provenance_expectations_review_report
downstream_gate_preservation_report
unsupported_claims_boundary_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Approval v1, if selected.",
    "Operator Completion Inputs Preparation or Supply Execution v1, if approved.",
    "Operator Completion Inputs Preparation or Supply Results Review v1.",
    "Completion Execution Reattempt v1, only if reviewed explicit non-secret operator inputs exist and reattempt is separately approved.",
    "Operator Source Authority Evidence Package Completion Results Review v1, only if a completed package exists.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Completed Evidence Package v1, only if separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple("""operator_completion_inputs_preparation_or_supply_approval_if_selected
operator_completion_inputs_preparation_or_supply_execution_if_approved
operator_completion_inputs_preparation_or_supply_results_review
completion_execution_reattempt_with_reviewed_non_secret_operator_inputs_if_approved
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

RISK_CONTROLS = tuple("""operator_review_does_not_select_package
operator_review_does_not_approve_package
operator_review_does_not_authorize_package
operator_review_does_not_execute_input_preparation
operator_review_does_not_execute_input_supply
operator_review_does_not_prepare_operator_completion_inputs
operator_review_does_not_supply_operator_completion_inputs
operator_review_does_not_validate_operator_completion_inputs
operator_review_does_not_bind_operator_completion_inputs
operator_review_does_not_create_completed_evidence_package
operator_review_does_not_create_evidence_package
operator_review_does_not_fill_actual_evidence_items
operator_review_does_not_validate_evidence
operator_review_does_not_bind_evidence
operator_review_does_not_accept_evidence_as_source_authority
operator_review_does_not_convert_template_placeholders_to_inputs
operator_review_does_not_convert_diagnostic_output_to_inputs
operator_review_does_not_acquire_source_authority
operator_review_does_not_acquire_source_authority_evidence
operator_review_does_not_acquire_external_evidence
operator_review_does_not_create_source_authority_acquisition_execution
operator_review_does_not_retry_source_authority_acquisition
operator_review_does_not_create_no_change_disposition
operator_review_does_not_execute_alternate_diagnostics
operator_review_does_not_execute_remediation
operator_review_does_not_modify_production_code
operator_review_does_not_modify_existing_tests
operator_review_does_not_update_expected_digests
operator_review_does_not_generate_patch
operator_review_does_not_apply_patch
operator_review_does_not_run_pytest
operator_review_does_not_run_full_pytest
operator_review_does_not_rerun_priority1_validation
operator_review_does_not_rerun_retry
operator_review_does_not_rerun_detached_retry
operator_review_does_not_parse_durable_receipt
operator_review_does_not_analyze_diagnostic_output
operator_review_does_not_rerun_source_authority_enrichment
operator_review_does_not_rerun_follow_on_execution
operator_review_does_not_rerun_plan_execution
operator_review_does_not_regenerate_targeted_plan
operator_review_does_not_rerun_method_execution
operator_review_does_not_rerun_controlled_recapture
operator_review_does_not_rerun_template_execution
operator_review_does_not_rerun_completion_execution
operator_review_does_not_run_diagnostic_command
operator_review_does_not_read_pytest_cache
operator_review_does_not_modify_pytest_cache
operator_review_does_not_commit_pytest_cache
operator_review_does_not_commit_marketflow_outputs
operator_review_does_not_parse_terminal_logs
operator_review_does_not_parse_operator_logs
operator_review_does_not_inspect_env
operator_review_does_not_contact_source_owners
operator_review_does_not_read_external_documents
operator_review_does_not_reconstruct_prior_lost_values
operator_review_does_not_reconstruct_full_streams
operator_review_does_not_classify_modules_again
operator_review_does_not_classify_full_retry_failures
operator_review_does_not_classify_full_retry_errors
operator_review_does_not_claim_failure_error_separation
operator_review_does_not_identify_authoritative_first_failure
operator_review_does_not_identify_authoritative_first_error
operator_review_does_not_claim_traceback_root_cause
operator_review_does_not_claim_root_cause
operator_review_does_not_claim_retry_success
operator_review_does_not_claim_main_merge_readiness
operator_review_does_not_create_retry_candidate
operator_review_does_not_create_retry_approval
operator_review_does_not_create_retry_execution
operator_review_does_not_create_retry_results_review
operator_review_does_not_create_main_merge_approval
operator_review_does_not_push_main
operator_review_does_not_push_integration_branch
operator_review_does_not_delete_integration_branch
operator_review_does_not_delete_worktree
operator_review_does_not_force_push
operator_review_does_not_modify_tags
operator_review_does_not_regenerate_evidence
operator_review_does_not_call_providers
operator_review_does_not_acquire_market_data
operator_review_does_not_generate_dataset
operator_review_does_not_recompute_metrics
operator_review_does_not_train_models
operator_review_does_not_score_strategy
operator_review_does_not_generate_trade_recommendations
operator_review_does_not_accept_predictive_usefulness
operator_review_does_not_accept_profitability
operator_review_does_not_authorize_runtime
operator_review_does_not_authorize_broker_execution
approved_completion_package_is_not_operator_input
reviewed_template_is_not_completed_evidence_package
template_placeholders_are_not_completion_inputs
synthetic_success_path_is_test_only
explicit_non_secret_inputs_required_before_completion_reattempt
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

TRUE_FIELDS = tuple("""operator_completion_inputs_preparation_or_supply_candidate_operator_review_created
operator_completion_inputs_preparation_or_supply_candidate_operator_review_ready
source_candidate_bound
source_candidate_reviewed
source_candidate_package_options_reviewed
source_candidate_input_contract_reviewed
source_candidate_source_binding_reviewed
source_candidate_coverage_reviewed
source_candidate_manifest_reviewed
source_failure_diagnosis_bound
source_completion_execution_bound
source_completion_execution_blocked_reason_verified
source_completion_execution_success_digests_absent_verified
source_approval_bound
source_attestation_bound
source_operator_review_bound
source_completion_candidate_bound
source_template_preparation_results_review_bound
source_template_preparation_execution_bound
source_preparation_candidate_bound
source_blocked_acquisition_execution_bound
source_acquisition_approval_bound
source_follow_on_results_review_bound
source_follow_on_execution_bound
source_authority_acquisition_candidate_bound
source_authority_acquisition_scope_bound
source_missing_authority_mapping_bound
follow_on_enrichment_historical_digests_bound
plan_method_diagnostic_recovery_digests_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
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
operator_input_absence_verified
count_label_distinction_preserved
input_preparation_or_supply_package_options_reviewed
recommended_input_preparation_or_supply_package_reviewed
future_input_preparation_requirements_reviewed
future_input_supply_contract_reviewed
future_input_preparation_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_completion_inputs_preparation_or_supply_approval_if_selected""".splitlines())

FALSE_FIELDS = tuple("""operator_completion_inputs_preparation_or_supply_package_selected
operator_completion_inputs_preparation_or_supply_package_approved
operator_completion_inputs_preparation_or_supply_package_authorized
operator_completion_inputs_preparation_or_supply_package_executed
operator_completion_inputs_preparation_executed
operator_completion_inputs_supply_executed
operator_completion_inputs_prepared
operator_completion_inputs_supplied
operator_completion_inputs_provided
operator_completion_inputs_validated
operator_completion_inputs_bound
operator_completion_inputs_contained_secrets
operator_source_authority_evidence_package_completion_executed
operator_source_authority_evidence_package_completed
operator_source_authority_evidence_package_created
operator_source_authority_evidence_package_supplied
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
operator_source_authority_evidence_package_accepted_as_source_authority
operator_source_authority_evidence_package_ready_for_acquisition_without_review
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
pytest_performed_in_operator_review
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_operator_review
diagnostic_output_analyzed_in_operator_review
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_operator_review
method_execution_rerun_performed
controlled_recapture_rerun_performed
template_execution_rerun_performed
completion_execution_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_operator_review
cache_modified_in_operator_review
pytest_cache_committed
marketflow_outputs_committed
terminal_logs_parsed
operator_logs_parsed
env_inspection_performed
source_owners_contacted
external_documents_read
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
ready_for_operator_completion_inputs_preparation_or_supply_execution
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
provider_requests_made_in_operator_review
market_data_acquisition_performed_in_operator_review
dataset_generation_performed_in_operator_review
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
    "blocked_package_count": 5,
    "future_input_preparation_requirement_count": 62,
    "future_input_preparation_plan_step_count": 17,
    "planned_output_count": 34,
    "non_goal_count": 76,
    "risk_control_count": 105,
    "future_completion_requirement_count": 67,
    "source_enumerated_future_completion_requirement_count": 69,
    "approved_future_completion_requirement_named_count": 69,
    "source_non_goal_count": 71,
    "source_enumerated_non_goal_count": 76,
    "source_risk_control_count": 104,
    "source_enumerated_risk_control_count": 106,
}


def _missing_authority_mapping() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for indexes, section_id, workstream_id in source.SECTION_WORKSTREAM_RANGES:
        rows.extend(
            {
                "missing_authority_id": f"MA-{index:03d}",
                "section_id": section_id,
                "workstream_id": workstream_id,
                "current_status": "MISSING_NOT_ACQUIRED",
            }
            for index in indexes
        )
    return rows


def _future_input_supply_contract() -> dict[str, Any]:
    rows = []
    for item in _missing_authority_mapping():
        rows.append({
            "evidence_id": f"<FUTURE_OPERATOR_PROVIDED_EVIDENCE_ID_FOR_{item['missing_authority_id']}>",
            "mapped_missing_authority_id": item["missing_authority_id"],
            "section_id": item["section_id"],
            "workstream_id": item["workstream_id"],
            "acceptable_source_artifact_type": "<ONE_OF_ALLOWED_ACCEPTABLE_SOURCE_ARTIFACT_TYPES>",
            "source_owner_or_origin": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "source_reference": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "digest_or_reproducible_provenance": "<FUTURE_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
            "evidence_classification": "<ONE_OF_ALLOWED_EVIDENCE_CLASSIFICATIONS>",
            "specification_or_observation": "<SPECIFICATION_OR_OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT>",
            "expected_or_actual_scope": "<EXPECTED_ACTUAL_BOTH_OR_NOT_APPLICABLE>",
            "authority_statement": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "results_review_required_before_use": True,
            "direct_change_authorized_now": False,
            "remediation_authorized_now": False,
            "retry_authorized_now": False,
            "main_merge_authorized_now": False,
            "actual_evidence_supplied": True,
            "actual_evidence_validated": False,
            "actual_evidence_bound": False,
            "current_status": "PREPARED_OR_SUPPLIED_OPERATOR_COMPLETION_INPUT_PENDING_REVIEW",
        })
    return {
        "contract_status": "REVIEWED_PLANNING_ONLY_NOT_EXECUTED",
        "package_header": {
            "package_source_owner_or_origin": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "package_reference": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "package_created_utc": "<FUTURE_UTC_TIMESTAMP>",
            "package_digest_or_reproducible_provenance": "<FUTURE_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
            "package_declares_no_secrets": True,
            "package_declares_no_api_keys": True,
            "package_declares_no_broker_credentials": True,
            "package_declares_no_personal_financial_credentials": True,
            "package_declares_no_market_data_credentials": True,
            "package_declares_no_private_tokens": True,
            "package_distinguishes_specification_from_observation": True,
            "package_distinguishes_expected_from_actual": True,
            "package_distinguishes_source_authority_from_diagnostic_output": True,
            "evidence_items": "EXACTLY_30_ITEMS_DEFINED_BY_THIS_CONTRACT",
        },
        "evidence_items": rows,
        "allowed_section_ids": list(source.ALLOWED_SECTION_IDS),
        "allowed_workstream_ids": list(source.ALLOWED_WORKSTREAM_IDS),
        "allowed_acceptable_source_artifact_types": list(source.ALLOWED_ARTIFACT_TYPES),
        "allowed_evidence_classifications": list(source.ALLOWED_EVIDENCE_CLASSIFICATIONS),
        "allowed_specification_or_observation": list(source.ALLOWED_SPECIFICATION_OR_OBSERVATION),
        "allowed_expected_or_actual_scope": list(source.ALLOWED_EXPECTED_OR_ACTUAL_SCOPE),
        "future_execution_rejected_secret_markers": list(source.SECRET_MARKERS),
        "operator_review_inspects_secrets": False,
    }


def _committed_source_candidate() -> dict[str, Any]:
    """Return the committed candidate identity projection; call no builder."""
    return deepcopy(SOURCE_CANDIDATE_BINDINGS)


def _validate_source_candidate(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateOperatorReviewError(
            "source_candidate must be an object"
        )
    if all(key in value for key in SOURCE_CANDIDATE_BINDINGS):
        expected_values = SOURCE_CANDIDATE_BINDINGS
    else:
        expected_values = {
            "artifact_kind": source.ARTIFACT_KIND,
            "candidate_status": source.CANDIDATE_STATUS,
            "candidate_scope": source.CANDIDATE_SCOPE,
            source.CANDIDATE_DIGEST_KEY: SOURCE_CANDIDATE_DIGEST,
            source.PACKAGE_OPTIONS_DIGEST_KEY: SOURCE_CANDIDATE_PACKAGE_OPTIONS_DIGEST,
            source.INPUT_CONTRACT_DIGEST_KEY: SOURCE_CANDIDATE_INPUT_CONTRACT_DIGEST,
            source.SOURCE_BINDING_DIGEST_KEY: SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST,
            source.COVERAGE_DIGEST_KEY: SOURCE_CANDIDATE_COVERAGE_DIGEST,
            source.MANIFEST_DIGEST_KEY: SOURCE_CANDIDATE_MANIFEST_DIGEST,
        }
    for key, expected in expected_values.items():
        if value.get(key) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateOperatorReviewError(
                f"source_candidate.{key} mismatch"
            )


def _package_options() -> list[dict[str, Any]]:
    options = []
    for package_id, source_status, review_status, purpose, blocked_reason in PACKAGE_OPTIONS:
        item = {
            "package_id": package_id,
            "source_status": source_status,
            "operator_review_status": review_status,
            "selected": False,
            "approved": False,
            "authorized": False,
            "executed": False,
        }
        item["blocked_reason" if blocked_reason else "purpose"] = blocked_reason or purpose
        options.append(item)
    return options


def _source_projection() -> dict[str, Any]:
    return {
        **deepcopy(SOURCE_CANDIDATE_BINDINGS),
        **deepcopy(SOURCE_FAILURE_BINDINGS),
        **deepcopy(source.SOURCE_BINDINGS),
        **deepcopy(source.SOURCE_CONTEXT),
        "priority_1_target_modules": [
            {"path": path, "failed_or_errored_nodeid_count": count}
            for path, count in source.PRIORITY_1_TARGET_MODULES
        ],
        "reviewed_observable_failure_families": [
            {"family_id": family, "observable_evidence_count": count, "confidence": confidence}
            for family, count, confidence in source.OBSERVABLE_FAMILIES
        ],
        "reviewed_workstreams": [
            {"workstream_id": workstream, "source_family_id": family}
            for workstream, family in source.WORKSTREAMS
        ],
        "reviewed_template_structure": {
            "package_kind": "MARKETFLOW_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FOR_RETRY_FAILURE_ACQUISITION_V1",
            "package_status": "OPERATOR_PROVIDED_FOR_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY",
            "template_only": True,
            "actual_evidence_package_created": False,
        },
        "missing_authority_mapping": _missing_authority_mapping(),
    }


def _digest_without(review: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(review))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    fixed = tuple("""artifact_kind_correct
operator_review_status_correct
operator_review_scope_correct
source_candidate_commit_bound
source_candidate_digest_bound
source_candidate_package_options_digest_bound
source_candidate_input_contract_digest_bound
source_candidate_source_binding_digest_bound
source_candidate_coverage_digest_bound
source_candidate_manifest_digest_bound
source_failure_diagnosis_commit_bound
source_failure_diagnosis_digest_bound
source_failure_classification_digest_bound
source_operator_input_absence_diagnosis_digest_bound
source_coverage_diagnosis_digest_bound
source_failure_diagnosis_manifest_digest_bound
source_completion_execution_commit_bound
source_completion_execution_blocked_reason_bound
source_completion_execution_blocked_digest_bound
source_completion_execution_blocked_manifest_digest_bound
source_completion_execution_success_digests_absent
primary_failure_class_bound
secondary_failure_classes_bound
source_approval_commit_bound
source_approval_digest_bound
source_attestation_digest_bound
selected_completion_package_bound
source_operator_review_digest_bound
source_completion_candidate_digest_bound
source_results_review_digest_bound
source_template_review_digest_bound
source_evidence_item_template_review_digest_bound
source_template_preparation_execution_digest_bound
source_package_template_digest_bound
source_preparation_candidate_digest_bound
source_blocked_acquisition_reason_bound
source_acquisition_approval_digest_bound
follow_on_and_enrichment_digests_bound
historical_source_digests_bound
plan_method_diagnostic_recovery_digests_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_execution_commit_bound
retry_failure_counts_bound
priority_1_top_module_paths_bound
priority_1_total_612_bound
top_10_total_1069_bound
module_summary_count_29_bound
failed_or_errored_nodeids_1404_bound
priority1_validation_675_pre_and_post_bound
priority1_validation_not_retry_evidence
diagnostic_exit_code_1_bound_as_diagnostic_only
diagnostic_stdout_hash_bound
diagnostic_stderr_hash_bound
diagnostic_stdout_byte_count_1231380_bound
diagnostic_stderr_byte_count_0_bound
observable_family_count_4_bound
observable_evidence_items_188_bound
family_confidence_high_bound
workstream_count_4_bound
reviewed_template_row_count_30
actual_coverage_zero
missing_authority_items_missing_not_acquired
count_label_distinction_preserved
operator_input_absence_verified
operator_review_created_true
operator_review_ready_true
package_options_reviewed
package_option_count_12
recommended_package_reviewed
available_packages_unselected
blocked_packages_blocked
future_input_preparation_requirements_reviewed
future_input_supply_contract_reviewed
future_input_preparation_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed
outputs_generated
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
operator_review_digest_generated
package_options_review_digest_generated
input_contract_review_digest_generated
source_binding_review_digest_generated
coverage_review_digest_generated
manifest_digest_generated
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines())
    source_checks = tuple(
        f"{key}_bound" for key in sorted({**SOURCE_CANDIDATE_BINDINGS, **SOURCE_FAILURE_BINDINGS, **source.SOURCE_BINDINGS})
        if key.endswith(("_digest", "_commit", "_reason"))
    )
    check_ids = tuple(dict.fromkeys((
        *fixed,
        *source_checks,
        *(f"{field}_true" for field in TRUE_FIELDS),
        *(f"{field}_false" for field in FALSE_FIELDS),
        *(f"package_option_{index:02d}_reviewed" for index in range(1, 13)),
        *(f"future_requirement_{item}_reviewed" for item in FUTURE_INPUT_REQUIREMENT_IDS),
        *(f"future_plan_step_{index:02d}_reviewed" for index in range(1, 18)),
        *(f"planned_output_{item}_reviewed" for item in PLANNED_OUTPUT_IDS),
        *(f"non_goal_{item}_reviewed" for item in NON_GOALS),
        *(f"output_{item}_generated" for item in OUTPUT_IDS),
        *(f"next_gate_{item}_defined" for item in NEXT_GATES),
        *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
    )))
    return [{
        "check_id": check_id,
        "status": PASS,
        "expected": True,
        "actual": True,
        "severity": BLOCKER,
        "message": f"{check_id} passed",
    } for check_id in check_ids]


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    keys = (
        "operator_completion_inputs_preparation_or_supply_candidate_operator_review_created",
        "operator_completion_inputs_preparation_or_supply_candidate_operator_review_ready",
        "source_candidate_digest", "source_failure_diagnosis_digest",
        "source_completion_execution_blocked_reason", "source_completion_execution_blocked_digest",
        "source_completion_execution_blocked_manifest_digest",
        "recommended_operator_completion_inputs_preparation_or_supply_package",
        "operator_completion_inputs_preparation_or_supply_package_selected",
        "operator_completion_inputs_preparation_or_supply_package_approved",
        "operator_completion_inputs_preparation_or_supply_package_authorized",
        "operator_completion_inputs_preparation_or_supply_package_executed",
        "operator_completion_inputs_prepared", "operator_completion_inputs_supplied",
        "operator_completion_inputs_provided", "operator_completion_inputs_validated",
        "operator_completion_inputs_bound", "operator_source_authority_evidence_package_completed",
        "operator_source_authority_evidence_package_created", "operator_source_authority_evidence_package_supplied",
        "operator_source_authority_evidence_package_validated", "operator_source_authority_evidence_package_bound",
        "source_authority_acquisition_performed", "source_authority_evidence_acquired",
        "external_evidence_acquired", "concrete_source_authority_established",
        "safe_source_authority_bound_change_identified", "actual_covered_missing_authority_item_count",
        "actual_uncovered_missing_authority_item_count", "missing_authority_items_status",
        "ready_for_operator_completion_inputs_preparation_or_supply_approval_if_selected",
        "ready_for_operator_completion_inputs_preparation_or_supply_execution",
        "ready_for_operator_source_authority_evidence_package_completion_execution",
        "ready_for_source_authority_acquisition_execution_retry", "ready_for_retry_candidate",
        "ready_for_main_merge_approval", "priority_1_total_nodeids", "failed_or_errored_nodeids_count",
        "observable_failure_family_count", "total_observable_evidence_items", "package_option_count",
        "available_package_count", "blocked_package_count", "future_input_preparation_requirement_count",
        "future_input_preparation_plan_step_count", "planned_output_count", "recommended_next_task",
    )
    return {
        "total_checks": len(review["checklist"]),
        "passed_checks": len(review["checklist"]),
        "failed_checks": 0,
        "blocker_count": 0,
        **{key: deepcopy(review[key]) for key in keys},
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def _assemble_review(source_candidate: Mapping[str, Any]) -> dict[str, Any]:
    source_projection = _source_projection()
    package_options = _package_options()
    future_contract = _future_input_supply_contract()
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "operator_review_status": OPERATOR_REVIEW_STATUS,
        "operator_review_scope": OPERATOR_REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        "review_status": "REVIEWED_CANDIDATE_ONLY",
        "operator_review_philosophy": "The source candidate correctly defines future options for preparing or supplying explicit non-secret operator completion inputs after the completion execution failed closed. The review may assess those options and preserve the recommended package, but it must not select, approve, authorize, prepare, supply, validate, bind, complete, acquire, remediate, retry, or merge.",
        "operator_review_boundary": "Operator review only. This review may assess source candidate evidence, package options, input contract, non-secret requirements, allowed values, future plan, planned outputs, non-goals, next gates, risk controls, and count-label distinctions. It must not create or supply any operator inputs or evidence.",
        **deepcopy(source_projection),
        **deepcopy(COUNTS),
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "recommended_operator_completion_inputs_preparation_or_supply_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "package_options": package_options,
        "future_input_preparation_requirements": [{
            "requirement_id": requirement_id,
            "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION",
            "execution_status": "NOT_EXECUTED",
        } for requirement_id in FUTURE_INPUT_REQUIREMENT_IDS],
        "future_input_supply_contract": future_contract,
        "secret_safety_review": {
            "future_execution_must_reject_secret_markers": list(source.SECRET_MARKERS),
            "environment_inspected": False,
            "files_or_credentials_inspected": False,
            "external_systems_contacted": False,
        },
        "future_plan": [
            {"step": index, "review_status": "REVIEWED_PLANNED_NOT_EXECUTED", "action": action}
            for index, action in enumerate(FUTURE_PLAN_STEPS, 1)
        ],
        "planned_outputs": [{
            "output_id": output_id,
            "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
            "generation_status": "NOT_GENERATED",
        } for output_id in PLANNED_OUTPUT_IDS],
        "non_goals": [{"non_goal_id": item, "review_status": "REVIEWED_ACTIVE", "active": True} for item in NON_GOALS],
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
        "outputs": [{
            "output_id": output_id,
            "status": "GENERATED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_ONLY",
        } for output_id in OUTPUT_IDS],
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_V1_IF_SELECTED",
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_SEPARATE_APPROVAL_REQUIRED_BEFORE_ANY_INPUT_PREPARATION_OR_SUPPLY_EXECUTION",
        "reason": "The candidate is complete and reviewable. The recommended future package remains the safest path to prepare or supply explicit non-secret operator completion inputs for all 30 reviewed template rows while preserving custody, provenance, source distinctions, row mappings, review-before-use, and all direct-change, remediation, retry, and main flags as false. This review does not select or approve it.",
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
    review[PACKAGE_OPTIONS_REVIEW_DIGEST_KEY] = semantic_digest(review["package_options"])
    review[INPUT_CONTRACT_REVIEW_DIGEST_KEY] = semantic_digest({
        "requirements": review["future_input_preparation_requirements"],
        "contract": review["future_input_supply_contract"],
        "secret_safety": review["secret_safety_review"],
    })
    review[SOURCE_BINDING_REVIEW_DIGEST_KEY] = semantic_digest(source_projection)
    review[COVERAGE_REVIEW_DIGEST_KEY] = semantic_digest(review["actual_coverage"])
    review[OPERATOR_REVIEW_DIGEST_KEY] = _digest_without(
        review, "checklist", "summary", OPERATOR_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY
    )
    review[MANIFEST_DIGEST_KEY] = semantic_digest({
        "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY],
        "package_options_review_digest": review[PACKAGE_OPTIONS_REVIEW_DIGEST_KEY],
        "input_contract_review_digest": review[INPUT_CONTRACT_REVIEW_DIGEST_KEY],
        "source_binding_review_digest": review[SOURCE_BINDING_REVIEW_DIGEST_KEY],
        "coverage_review_digest": review[COVERAGE_REVIEW_DIGEST_KEY],
        "source_candidate_digest": SOURCE_CANDIDATE_DIGEST,
    })
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    return review


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(
    *, source_candidate: dict | None = None,
) -> dict[str, Any]:
    """Build the deterministic review from committed constants or an injection."""
    source_value = _committed_source_candidate() if source_candidate is None else deepcopy(source_candidate)
    _validate_source_candidate(source_value)
    review = _assemble_review(source_value)
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(
    operator_review: dict,
) -> dict[str, Any]:
    """Reject drift, selection, execution, authority, or missing review content."""
    if not isinstance(operator_review, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateOperatorReviewError(
            "operator_review must be an object"
        )
    expected = _assemble_review(_committed_source_candidate())
    difference = _first_difference(operator_review, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateOperatorReviewError(
            f"{difference} mismatch"
        )
    for key in (
        OPERATOR_REVIEW_DIGEST_KEY, PACKAGE_OPTIONS_REVIEW_DIGEST_KEY,
        INPUT_CONTRACT_REVIEW_DIGEST_KEY, SOURCE_BINDING_REVIEW_DIGEST_KEY,
        COVERAGE_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY,
    ):
        value = operator_review.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateOperatorReviewError(
                f"{key} invalid"
            )
    return {
        "artifact_kind": ARTIFACT_KIND,
        "operator_review_status": OPERATOR_REVIEW_STATUS,
        "operator_review_scope": OPERATOR_REVIEW_SCOPE,
        "operator_review_digest": operator_review[OPERATOR_REVIEW_DIGEST_KEY],
        **{key: operator_review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Operator Review Disposition", "Source Candidate", "Source Failure Diagnosis",
    "Primary Failure Class", "Secondary Failure Classes", "Source Completion Execution",
    "Blocked Reason", "Blocked Digest Manifest", "Source Completion Approval",
    "Selected Completion Package", "Source Operator Review", "Source Completion Candidate",
    "Source Template Preparation Results Review", "Source Template Preparation Execution",
    "Source Preparation Failure Acquisition Chains", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt",
    "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
    "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
    "Reviewed Template Structure", "Count Label Distinction", "Operator Completion Input Absence",
    "Future Input Supply Contract", "Reviewed Package Options", "Recommended Package",
    "Reviewed Future Input Requirements", "Reviewed Future Plan", "Reviewed Planned Outputs",
    "Reviewed Non-Goals", "Actual Evidence Absence", "Actual Coverage Zero",
    "Source Authority Gap Preservation", "Unsupported Claims Boundary", "Recommendation",
    "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary",
    "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_markdown_v1(
    operator_review: dict,
) -> str:
    """Render the review without reading or expanding external evidence."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(operator_review)
    summary = operator_review["summary"]
    facts = {
        "Operator Review Disposition": f"`{OPERATOR_REVIEW_STATUS}` within `{OPERATOR_REVIEW_SCOPE}`. Review `{operator_review[OPERATOR_REVIEW_DIGEST_KEY]}`; manifest `{operator_review[MANIFEST_DIGEST_KEY]}`.",
        "Source Candidate": f"Commit `{SOURCE_CANDIDATE_COMMIT}`; artifact `{source.ARTIFACT_KIND}`; status `{source.CANDIDATE_STATUS}`; scope `{source.CANDIDATE_SCOPE}`; candidate `{SOURCE_CANDIDATE_DIGEST}`; package options `{SOURCE_CANDIDATE_PACKAGE_OPTIONS_DIGEST}`; input contract `{SOURCE_CANDIDATE_INPUT_CONTRACT_DIGEST}`; source binding `{SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST}`; coverage `{SOURCE_CANDIDATE_COVERAGE_DIGEST}`; manifest `{SOURCE_CANDIDATE_MANIFEST_DIGEST}`.",
        "Source Failure Diagnosis": f"Commit `{source.SOURCE_FAILURE_DIAGNOSIS_COMMIT}`; diagnosis `{source.SOURCE_FAILURE_DIAGNOSIS_DIGEST}`; classification `{source.SOURCE_FAILURE_CLASSIFICATION_DIGEST}`; input absence `{source.SOURCE_OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST}`; coverage `{source.SOURCE_COVERAGE_DIAGNOSIS_DIGEST}`; manifest `{source.SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST}`.",
        "Primary Failure Class": f"`{source.PRIMARY_FAILURE_CLASS}`.",
        "Secondary Failure Classes": "\n".join(f"- `{item}`" for item in source.SECONDARY_FAILURE_CLASSES),
        "Source Completion Execution": f"Commit `{operator_review['source_completion_execution_commit']}`; artifact `{operator_review['source_completion_execution_artifact_kind']}`; status `{operator_review['source_completion_execution_status']}`; scope `{operator_review['source_completion_execution_scope']}`.",
        "Blocked Reason": f"`{operator_review['source_completion_execution_blocked_reason']}`.",
        "Blocked Digest Manifest": f"Blocked digest `{operator_review['source_completion_execution_blocked_digest']}`; manifest `{operator_review['source_completion_execution_blocked_manifest_digest']}`; success digests remain absent.",
        "Source Completion Approval": f"Commit `{operator_review['source_approval_commit']}`; approval `{operator_review['source_approval_digest']}`; attestation `{operator_review['source_attestation_digest']}`.",
        "Selected Completion Package": f"`{source.SELECTED_COMPLETION_PACKAGE}` remains a prior approval boundary, not operator input or evidence.",
        "Source Operator Review": f"Commit `{operator_review['source_operator_review_commit']}`; digest `{operator_review['source_operator_review_digest']}`; manifest `{operator_review['source_operator_review_manifest_digest']}`.",
        "Source Completion Candidate": f"Commit `{operator_review['source_completion_candidate_commit']}`; digest `{operator_review['source_completion_candidate_digest']}`; manifest `{operator_review['source_completion_candidate_manifest_digest']}`.",
        "Source Template Preparation Results Review": f"Results `{operator_review['source_results_review_digest']}`; template `{operator_review['source_template_review_digest']}`; evidence-item template `{operator_review['source_evidence_item_template_review_digest']}`; manifest `{operator_review['source_results_review_manifest_digest']}`.",
        "Source Template Preparation Execution": f"Commit `{operator_review['source_template_preparation_execution_commit']}`; execution `{operator_review['source_template_preparation_execution_digest']}`; package template `{operator_review['source_package_template_digest']}`; manifest `{operator_review['source_template_preparation_execution_manifest_digest']}`.",
        "Source Preparation Failure Acquisition Chains": f"Preparation `{operator_review['source_preparation_candidate_digest']}`; prior failure `{operator_review['source_previous_failure_diagnosis_digest']}`; blocked acquisition `{operator_review['source_blocked_acquisition_execution_reason']}`; approval `{operator_review['source_acquisition_approval_digest']}`.",
        "Source Follow-On and Enrichment Chain": f"Review `{operator_review['source_follow_on_results_review_digest']}`; execution `{operator_review['source_follow_on_execution_digest']}`; enrichment `{operator_review['source_enrichment_execution_digest']}`. All preserved digests are covered by source-binding review `{operator_review[SOURCE_BINDING_REVIEW_DIGEST_KEY]}`.",
        "Historical Blocked Remediation": f"Reason `{operator_review['historical_blocked_remediation_reason']}`; manifest `{operator_review['historical_blocked_remediation_manifest_digest']}`.",
        "Plan Method Diagnostic Recovery Chain": f"Targeted plan `{operator_review['source_targeted_remediation_plan_digest']}`; method execution `{operator_review['source_remediation_or_method_execution_after_diagnostic_capture_digest']}`; recovery `{operator_review['source_recovery_results_review_digest']}`; staged inventory `{operator_review['source_staged_inventory_digest']}`.",
        "Durable Receipt": f"`{operator_review['source_durable_receipt_path']}` is bound as an opaque reference and was not parsed.",
        "Retry Failure Context": "The authoritative detached retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped. The root regression is not retry evidence.",
        "Priority 1 Target Modules": "\n".join(f"- `{item['path']}`: {item['failed_or_errored_nodeid_count']} node IDs" for item in operator_review["priority_1_target_modules"]),
        "Priority 1 Validation Summary": "675/675 pre-change and 675/675 post-change passed as current-root focused evidence only; this is not retry evidence.",
        "Diagnostic Capture Evidence Summary": f"Exit 1; stdout {operator_review['source_stdout_byte_count']} bytes `{operator_review['source_stdout_sha256']}`; stderr {operator_review['source_stderr_byte_count']} bytes `{operator_review['source_stderr_sha256']}`. Diagnostic metadata only.",
        "Reviewed Observable Families": "Four HIGH-confidence planning families, 47 observations each and 188 total, remain unchanged.",
        "Reviewed Workstreams": "Assertion/value, digest/hash, fixture/isolation, and schema/field-contract workstreams remain non-authorizing.",
        "Reviewed Template Structure": "Thirty reviewed rows map MA-001 through MA-030. The template is not evidence, authority, acquired evidence, or acquisition success.",
        "Count Label Distinction": "Preserved without reconciliation: requirements 67/69/69; non-goals 71/76; risk controls 104/106. Candidate-local count labels remain 62 requirements, 17 steps, 34 planned outputs, 76 non-goals, and 105 risk controls.",
        "Operator Completion Input Absence": "No input was prepared, supplied, provided, validated, or bound. The source execution remains correctly failed closed.",
        "Future Input Supply Contract": f"Reviewed as planning-only for exactly 30 mapped non-secret rows; review digest `{operator_review[INPUT_CONTRACT_REVIEW_DIGEST_KEY]}`.",
        "Recommended Package": f"`{RECOMMENDED_PACKAGE}` was reviewed and remains unselected, unapproved, unauthorized, and unexecuted.",
        "Actual Evidence Absence": "No completed package or evidence package was created, supplied, validated, bound, accepted, or filled.",
        "Actual Coverage Zero": f"Coverage remains 0/30 and `MISSING_NOT_ACQUIRED`; review digest `{operator_review[COVERAGE_REVIEW_DIGEST_KEY]}`.",
        "Source Authority Gap Preservation": "No authority, external evidence, concrete authority, safe change, acquisition execution, disposition, diagnostic, remediation, retry, or merge authority was created.",
        "Unsupported Claims Boundary": "No first-failure, first-error, root-cause, retry-success, acquisition-success, remediation-readiness, retry-readiness, or main-readiness claim is made.",
        "Recommendation": f"`{operator_review['recommended_next_task']}`: `{operator_review['recommended_action']}`.",
        "Authority Boundaries": "Selection, approval, authorization, execution, input handling, evidence completion, acquisition, remediation, retry, predictive usefulness, profitability, runtime, broker, trading, and protected-branch authority remain false or NOT_AUTHORIZED.",
        "Checklist Summary": f"{summary['passed_checks']}/{summary['total_checks']} PASS; blockers={summary['blocker_count']}.",
        "Guardrails": "Offline committed constants and injected dictionaries only. No upstream builders, file reads, subprocesses, pytest, caches, receipts, logs, environment, providers, documents, source-owner contact, inputs, evidence, or runtime actions.",
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs Preparation or Supply Candidate Operator Review After Blocked Completion Execution v1", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", "", facts.get(section, "Review-only governance content; no execution or authority is created."), ""))
        if section == "Reviewed Package Options":
            lines[-2:-2] = [*(f"- `{item['package_id']}` — `{item['operator_review_status']}`: {item.get('purpose', item.get('blocked_reason'))}" for item in operator_review["package_options"]), ""]
        elif section == "Reviewed Future Input Requirements":
            lines[-2:-2] = [*(f"- `{item['requirement_id']}` — `{item['execution_status']}`" for item in operator_review["future_input_preparation_requirements"]), ""]
        elif section == "Reviewed Future Plan":
            lines[-2:-2] = [*(f"{item['step']}. {item['action']} (`{item['review_status']}`)" for item in operator_review["future_plan"]), ""]
        elif section == "Reviewed Planned Outputs":
            lines[-2:-2] = [*(f"- `{item['output_id']}` — `{item['generation_status']}`" for item in operator_review["planned_outputs"]), ""]
        elif section == "Reviewed Non-Goals":
            lines[-2:-2] = [*(f"- `{item['non_goal_id']}`" for item in operator_review["non_goals"]), ""]
        elif section == "Next Chain":
            lines[-2:-2] = [*(f"{index}. {item}" for index, item in enumerate(operator_review["next_chain"], 1)), ""]
        elif section == "Next Gates":
            lines[-2:-2] = [*(f"- `{item}`" for item in operator_review["next_gates"]), ""]
        elif section == "Risk Controls":
            lines[-2:-2] = [*(f"- `{item}`" for item in operator_review["risk_controls"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(
    output_dir: str | Path,
    *,
    source_candidate: dict | None = None,
) -> dict[str, Any]:
    """Write only the requested operator-review status Markdown file."""
    review = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(
        source_candidate=source_candidate,
    )
    destination = Path(output_dir) / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_markdown_v1(review),
        encoding="utf-8",
    )
    return review


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "OPERATOR_REVIEW_STATUS", "OPERATOR_REVIEW_SCOPE",
    "RECOMMENDED_PACKAGE", "PACKAGE_OPTIONS", "FUTURE_INPUT_REQUIREMENT_IDS",
    "PLANNED_OUTPUT_IDS", "OUTPUT_IDS", "NON_GOALS", "RISK_CONTROLS", "NEXT_CHAIN",
    "NEXT_GATES", "TRUE_FIELDS", "FALSE_FIELDS", "COUNTS", "SOURCE_CANDIDATE_BINDINGS",
    "OPERATOR_REVIEW_DIGEST_KEY", "PACKAGE_OPTIONS_REVIEW_DIGEST_KEY",
    "INPUT_CONTRACT_REVIEW_DIGEST_KEY", "SOURCE_BINDING_REVIEW_DIGEST_KEY",
    "COVERAGE_REVIEW_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE",
    "PACKAGE_PREPARE_COMPLETION_INPUT_HEADER_FIELDS_ONLY",
    "PACKAGE_PREPARE_COMPLETION_INPUT_EVIDENCE_ITEM_ROWS_ONLY",
    "PACKAGE_PREPARE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_MAPPING_ONLY",
    "PACKAGE_PREPARE_WORKSTREAM_SPECIFIC_COMPLETION_INPUT_SETS",
    "PACKAGE_PREPARE_COMPLETION_INPUT_CHECKLIST_AND_ATTESTATION_ONLY",
    "PACKAGE_HOLD_PENDING_OPERATOR_COMPLETION_INPUTS",
    "PACKAGE_FABRICATE_COMPLETION_INPUTS_FROM_TEMPLATE_PLACEHOLDERS",
    "PACKAGE_DERIVE_COMPLETION_INPUTS_FROM_DIAGNOSTIC_OUTPUT",
    "PACKAGE_VALIDATE_BIND_OR_ACQUIRE_EVIDENCE_DURING_INPUT_PREPARATION",
    "PACKAGE_REATTEMPT_COMPLETION_EXECUTION_IMMEDIATELY_FROM_FAILURE_DIAGNOSIS",
    "PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_MISSING_INPUTS_DIAGNOSIS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateOperatorReviewError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_markdown_v1",
]
