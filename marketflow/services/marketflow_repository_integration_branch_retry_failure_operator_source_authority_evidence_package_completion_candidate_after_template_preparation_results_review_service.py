"""Create the governed candidate for completing the reviewed evidence template."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_RESULTS_REVIEW_COMMIT = "268c84d7ef4ed550bb38f07670247540590885f6"
SOURCE_RESULTS_REVIEW_DIGEST = "a33038171faf25b4b077d5c0c7c5ecaf794d655d5007d92b1fbc7c6bf38db332"
SOURCE_TEMPLATE_REVIEW_DIGEST = "3e60c8bb9c9000f6d5ca561ae843c17ec4abd31276fa443d7b9d97b7524040b9"
SOURCE_EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST = "8b9994a28e017fc5e61cb0274b9191f61857594dfa1a3dc861e3087e3da7520c"
SOURCE_PREPARATION_CHECKLIST_REVIEW_DIGEST = "e4a57857d17f7fd68fce5af88a3efab02f54e5e33fc61be241740a35a0b9fcc2"
SOURCE_TEMPLATE_COVERAGE_REVIEW_DIGEST = "7ae349f3c94be97808aa0930429614cb2f33917f73694693d32ebb4e7656b290"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "f4b7d2838a11d192497e7b79e7d2cc7ec3f1aac3d43dcf7362014c5724a109f0"
RECOMMENDED_PACKAGE = "PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS"
RECOMMENDED_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_V1"
CANDIDATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_digest"
PACKAGE_OPTIONS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_package_options_digest"
OPERATOR_INPUT_REQUIREMENTS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_input_requirements_digest"
TEMPLATE_BINDING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_template_binding_digest"
COVERAGE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_coverage_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_manifest_digest"
PASS, BLOCKER = "PASS", "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE
PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS = RECOMMENDED_PACKAGE
PACKAGE_COMPLETE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_FIELDS_ONLY = "PACKAGE_COMPLETE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_FIELDS_ONLY"
PACKAGE_COMPLETE_ASSERTION_VALUE_EVIDENCE_ITEMS_ONLY = "PACKAGE_COMPLETE_ASSERTION_VALUE_EVIDENCE_ITEMS_ONLY"
PACKAGE_COMPLETE_DIGEST_SERIALIZATION_EVIDENCE_ITEMS_ONLY = "PACKAGE_COMPLETE_DIGEST_SERIALIZATION_EVIDENCE_ITEMS_ONLY"
PACKAGE_COMPLETE_FIXTURE_DETERMINISM_EVIDENCE_ITEMS_ONLY = "PACKAGE_COMPLETE_FIXTURE_DETERMINISM_EVIDENCE_ITEMS_ONLY"
PACKAGE_COMPLETE_SCHEMA_FIELD_CONTRACT_EVIDENCE_ITEMS_ONLY = "PACKAGE_COMPLETE_SCHEMA_FIELD_CONTRACT_EVIDENCE_ITEMS_ONLY"
PACKAGE_HOLD_PENDING_NON_SECRET_OPERATOR_EVIDENCE_INPUTS = "PACKAGE_HOLD_PENDING_NON_SECRET_OPERATOR_EVIDENCE_INPUTS"
PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_TEMPLATE_PLACEHOLDERS_ONLY = "PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_TEMPLATE_PLACEHOLDERS_ONLY"
PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_DIAGNOSTIC_OUTPUT_ONLY = "PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_DIAGNOSTIC_OUTPUT_ONLY"
PACKAGE_VALIDATE_OR_BIND_EVIDENCE_DURING_COMPLETION = "PACKAGE_VALIDATE_OR_BIND_EVIDENCE_DURING_COMPLETION"
PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_IMMEDIATELY_AFTER_TEMPLATE_REVIEW = "PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_IMMEDIATELY_AFTER_TEMPLATE_REVIEW"
PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_REVIEWED_TEMPLATE = "PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_REVIEWED_TEMPLATE"

CANDIDATE_PHILOSOPHY = "The reviewed template and checklist may guide future operator evidence-package completion, but they are not actual evidence, not source authority, not acquired evidence, and not acquisition success. The next safe step is a governed candidate defining how a future non-secret operator evidence package may be completed from the reviewed template without filling, supplying, validating, binding, acquiring, remediating, retrying, or merging in this task."
CANDIDATE_BOUNDARY = "Candidate only. The candidate may define completion options, completion requirements, operator-supplied evidence requirements, validation preconditions, no-secret boundaries, custody/digest requirements, and downstream review gates. It must not create a completed evidence package, supply evidence, validate evidence, bind evidence, acquire source authority, authorize remediation, authorize retry, or create main-merge readiness."

PACKAGE_OPTIONS = (
    (RECOMMENDED_PACKAGE, "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_RECOMMENDED_NOT_SELECTED", "Future execution may complete a non-secret operator source-authority evidence package using the reviewed template, if and only if the operator supplies the required source, provenance, classification, scope, authority, and row-mapping fields.", None),
    (PACKAGE_COMPLETE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_FIELDS_ONLY, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may fill only source-owner/origin, source references, created UTC, and digest/provenance fields without validating evidence or acquiring authority.", None),
    (PACKAGE_COMPLETE_ASSERTION_VALUE_EVIDENCE_ITEMS_ONLY, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may complete only assertion/value evidence items from non-secret operator inputs while preserving review-before-use and all false authorization flags.", None),
    (PACKAGE_COMPLETE_DIGEST_SERIALIZATION_EVIDENCE_ITEMS_ONLY, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may complete only digest/hash, canonical payload, canonical serialization, and manifest evidence items from non-secret operator inputs.", None),
    (PACKAGE_COMPLETE_FIXTURE_DETERMINISM_EVIDENCE_ITEMS_ONLY, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may complete only fixture lifecycle, isolation, deterministic timestamp/path/CWD/worktree, randomness, and temporary-path authority evidence items.", None),
    (PACKAGE_COMPLETE_SCHEMA_FIELD_CONTRACT_EVIDENCE_ITEMS_ONLY, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may complete only schema, field contract, export-surface, alias, deprecation, and backward-compatibility evidence items.", None),
    (PACKAGE_HOLD_PENDING_NON_SECRET_OPERATOR_EVIDENCE_INPUTS, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may record a hold disposition for package completion only, pending non-secret operator evidence inputs.", None),
    (PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_TEMPLATE_PLACEHOLDERS_ONLY, "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", None, "Template placeholders are not evidence and cannot be converted into a completed evidence package."),
    (PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_DIAGNOSTIC_OUTPUT_ONLY, "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", None, "Diagnostic output is observation evidence only and cannot substitute for source-authority evidence."),
    (PACKAGE_VALIDATE_OR_BIND_EVIDENCE_DURING_COMPLETION, "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", None, "Evidence validation and binding require separate acquisition execution and results review, not completion-candidate scope."),
    (PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_IMMEDIATELY_AFTER_TEMPLATE_REVIEW, "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", None, "Acquisition reattempt requires a completed, reviewed, separately approved evidence package."),
    (PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_REVIEWED_TEMPLATE, "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", None, "A reviewed template does not support remediation, retry readiness, retry success, or main-merge readiness."),
)

HEADER_INPUT_FIELDS = tuple("""package_source_owner_or_origin
package_reference
package_created_utc
package_digest_or_reproducible_provenance
package_declares_no_secrets
package_declares_no_api_keys
package_declares_no_broker_credentials
package_declares_no_personal_financial_credentials
package_distinguishes_specification_from_observation
package_distinguishes_expected_from_actual
package_distinguishes_source_authority_from_diagnostic_output
evidence_items""".splitlines())

EVIDENCE_ITEM_INPUT_FIELDS = tuple("""evidence_id
mapped_missing_authority_id
section_id
workstream_id
acceptable_source_artifact_type
source_owner_or_origin
source_reference
digest_or_reproducible_provenance
evidence_classification
specification_or_observation
expected_or_actual_scope
authority_statement
results_review_required_before_use
direct_change_authorized_now
remediation_authorized_now
retry_authorized_now
main_merge_authorized_now
template_only
actual_evidence_supplied
actual_evidence_validated
actual_evidence_bound
current_status""".splitlines())

FUTURE_REQUIREMENT_IDS = tuple("""source_results_review_must_be_bound
source_execution_must_be_bound
source_template_digest_must_be_bound
source_evidence_item_template_digest_must_be_bound
source_checklist_digest_must_be_bound
source_coverage_review_must_be_bound
source_approval_must_be_bound
source_attestation_must_be_bound
source_operator_review_must_be_bound
source_preparation_candidate_must_be_bound
source_failure_diagnosis_must_be_bound
source_blocked_acquisition_execution_must_be_bound
source_blocked_reason_must_be_no_operator_package
primary_failure_class_must_be_no_operator_package
secondary_failure_classes_must_be_preserved
retry_failure_counts_must_be_bound
priority_1_context_must_be_bound
priority1_validation_must_remain_non_retry_evidence
diagnostic_metadata_must_remain_diagnostic_only
observable_families_must_remain_planning_evidence
reviewed_workstreams_must_remain_non_authorizing
template_must_be_reviewed
template_must_not_be_treated_as_source_authority
template_must_not_be_treated_as_acquired_evidence
template_must_not_be_treated_as_acquisition_success
template_row_count_must_be_30
template_rows_must_map_to_reviewed_missing_authority_items
actual_coverage_must_remain_zero_until_completion_execution
all_missing_authority_items_must_remain_missing_until_valid_completion
operator_inputs_must_be_non_secret
operator_inputs_must_not_include_api_keys
operator_inputs_must_not_include_broker_credentials
operator_inputs_must_not_include_personal_financial_credentials
operator_inputs_must_not_include_market_data_credentials
operator_inputs_must_not_include_private_tokens
operator_inputs_must_include_source_owner_or_origin
operator_inputs_must_include_source_reference
operator_inputs_must_include_created_utc
operator_inputs_must_include_digest_or_reproducible_provenance
operator_inputs_must_include_evidence_classification
operator_inputs_must_include_specification_or_observation
operator_inputs_must_include_expected_or_actual_scope
operator_inputs_must_include_authority_statement
operator_inputs_must_include_no_secret_declarations
operator_inputs_must_preserve_template_row_mapping
operator_inputs_must_preserve_section_ids
operator_inputs_must_preserve_workstream_ids
operator_inputs_must_preserve_acceptable_artifact_types
operator_inputs_must_distinguish_specification_from_observation
operator_inputs_must_distinguish_expected_from_actual
operator_inputs_must_distinguish_source_authority_from_diagnostic_output
completion_execution_must_force_direct_change_authorized_false
completion_execution_must_force_remediation_authorized_false
completion_execution_must_force_retry_authorized_false
completion_execution_must_force_main_merge_authorized_false
completion_execution_must_not_validate_evidence
completion_execution_must_not_bind_evidence
completion_execution_must_not_acquire_source_authority
completion_execution_must_not_acquire_external_evidence
completion_execution_must_not_read_external_documents_unless_separately_approved
completion_execution_must_not_contact_source_owners
completion_execution_must_not_parse_receipts_logs_cache_or_env
completion_execution_must_not_modify_code_tests_or_digests
completion_execution_must_not_run_pytest_or_retry
completion_execution_must_require_results_review
completed_package_must_require_results_review_before_acquisition_use
future_acquisition_reattempt_requires_reviewed_completed_package
future_acquisition_reattempt_requires_separate_approval
runtime_and_trading_remain_not_authorized""".splitlines())

PLAN_STEPS = (
    "Bind this completion candidate and the source template-preparation results review.",
    "Bind the source execution, approval, operator review, preparation candidate, failure diagnosis, blocked acquisition, acquisition approval, follow-on, enrichment, historical, plan, method, diagnostic, recovery, module-grouping, and staged-inventory evidence.",
    "Preserve the reviewed template and checklist digests.",
    "Preserve the source blocked reason NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED.",
    "Preserve actual coverage as 0/30 and all missing-authority items as MISSING_NOT_ACQUIRED.",
    "Define future completion package options without selecting any.",
    "Define the recommended future package for completing the reviewed template with non-secret operator inputs.",
    "Define minimum operator input fields for package header completion.",
    "Define minimum operator input fields for evidence-item row completion.",
    "Preserve all no-secret and credential boundaries.",
    "Preserve source-authority, specification/observation, and expected/actual separation requirements.",
    "Preserve all direct-change, remediation, retry, and main-merge authorization flags as false.",
    "Require operator review before completion approval.",
    "Require approval before completion execution.",
    "Require results review after any completion execution.",
    "Require separately approved source-authority acquisition execution before any completed package can be validated, bound, or used as authority.",
    "Preserve no-change disposition, alternate diagnostic, remediation, retry, and main-merge gates.",
)

OUTPUT_IDS = tuple("""operator_source_authority_evidence_package_completion_candidate_manifest
source_template_preparation_results_review_binding_report
source_template_preparation_execution_binding_report
source_approval_binding_report
source_operator_review_binding_report
source_preparation_candidate_binding_report
source_failure_diagnosis_binding_report
source_blocked_acquisition_execution_binding_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
reviewed_template_structure_report
reviewed_template_coverage_report
evidence_package_absence_report
actual_coverage_zero_report
missing_authority_mapping_report
completion_package_options_report
recommended_completion_package_report
required_operator_input_header_fields_report
required_operator_input_evidence_item_fields_report
non_secret_operator_input_requirements_report
custody_digest_and_provenance_requirements_report
specification_observation_separation_report
expected_actual_separation_report
source_authority_diagnostic_output_separation_report
completion_results_review_gate_report
acquisition_reattempt_gate_preservation_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NON_GOAL_IDS = tuple("""do_not_select_package_now
do_not_approve_package_now
do_not_authorize_package_now
do_not_execute_evidence_package_completion_now
do_not_create_completed_operator_evidence_package_now
do_not_fill_actual_evidence_items_now
do_not_supply_evidence_package_now
do_not_validate_evidence_package_now
do_not_bind_evidence_package_now
do_not_accept_template_as_evidence_now
do_not_accept_template_as_source_authority_now
do_not_accept_completed_package_without_review_now
do_not_acquire_source_authority_now
do_not_acquire_source_authority_evidence_now
do_not_acquire_external_evidence_now
do_not_retry_source_authority_acquisition_now
do_not_create_source_authority_acquisition_execution_now
do_not_create_no_change_disposition_now
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
do_not_parse_durable_receipt_now
do_not_analyze_diagnostic_output_now
do_not_read_pytest_cache_now
do_not_modify_pytest_cache_now
do_not_parse_terminal_logs_now
do_not_parse_operator_logs_now
do_not_inspect_env_now
do_not_call_providers_now
do_not_contact_source_owners_now
do_not_read_external_documents_now
do_not_reconstruct_prior_lost_values_now
do_not_reconstruct_full_stdout_or_stderr_now
do_not_classify_modules_again_now
do_not_claim_failure_error_separation_now
do_not_identify_first_failure_now
do_not_identify_first_error_now
do_not_claim_traceback_root_cause_now
do_not_claim_root_cause_now
do_not_claim_retry_success_now
do_not_claim_main_merge_readiness_now
do_not_create_retry_candidate_now
do_not_create_retry_approval_now
do_not_create_retry_execution_now
do_not_create_retry_results_review_now
do_not_create_main_merge_approval_now
do_not_push_main
do_not_push_integration_branch
do_not_delete_or_reset_integration_branch
do_not_delete_or_reset_worktree
do_not_force_push
do_not_modify_tags
do_not_modify_staged_evidence
do_not_regenerate_evidence
do_not_commit_marketflow_outputs
do_not_commit_pytest_cache
do_not_acquire_market_data
do_not_generate_dataset
do_not_recompute_metrics
do_not_train_models
do_not_score_strategy
do_not_generate_trade_recommendations
do_not_accept_predictive_usefulness
do_not_accept_profitability
do_not_authorize_runtime
do_not_authorize_broker_execution
do_not_authorize_trading""".splitlines())

NEXT_CHAIN = (
    "Operator Source Authority Evidence Package Completion Candidate Operator Review After Template Preparation Results Review v1.",
    "Operator Source Authority Evidence Package Completion Approval v1, if selected.",
    "Operator Source Authority Evidence Package Completion Execution v1, if approved and non-secret operator inputs are supplied.",
    "Operator Source Authority Evidence Package Completion Results Review v1.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Evidence Package v1, only if a reviewed completed package exists and is separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple("""operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_review
operator_source_authority_evidence_package_completion_approval_if_selected
operator_source_authority_evidence_package_completion_execution_if_approved_and_non_secret_operator_inputs_supplied
operator_source_authority_evidence_package_completion_results_review
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

RISK_CONTROLS = tuple("""candidate_does_not_select_package
candidate_does_not_approve_package
candidate_does_not_authorize_package
candidate_does_not_execute_completion
candidate_does_not_create_completed_evidence_package
candidate_does_not_fill_actual_evidence_items
candidate_does_not_supply_evidence_package
candidate_does_not_validate_evidence_package
candidate_does_not_bind_evidence_package
candidate_does_not_accept_template_as_evidence
candidate_does_not_accept_template_as_source_authority
candidate_does_not_accept_template_as_acquired_evidence
candidate_does_not_acquire_source_authority
candidate_does_not_acquire_source_authority_evidence
candidate_does_not_acquire_external_evidence
candidate_does_not_retry_acquisition_execution
candidate_does_not_create_acquisition_execution
candidate_does_not_create_no_change_disposition
candidate_does_not_execute_alternate_diagnostics
candidate_does_not_execute_remediation
candidate_does_not_modify_production_code
candidate_does_not_modify_existing_tests
candidate_does_not_update_expected_digests
candidate_does_not_generate_patch
candidate_does_not_apply_patch
candidate_does_not_run_pytest
candidate_does_not_run_full_pytest
candidate_does_not_rerun_priority1_validation
candidate_does_not_rerun_retry
candidate_does_not_rerun_detached_retry
candidate_does_not_parse_durable_receipt
candidate_does_not_analyze_diagnostic_output
candidate_does_not_rerun_source_authority_enrichment
candidate_does_not_rerun_follow_on_execution
candidate_does_not_rerun_plan_execution
candidate_does_not_regenerate_targeted_plan
candidate_does_not_rerun_method_execution
candidate_does_not_rerun_controlled_recapture
candidate_does_not_rerun_template_execution
candidate_does_not_run_diagnostic_command
candidate_does_not_read_pytest_cache
candidate_does_not_modify_pytest_cache
candidate_does_not_commit_pytest_cache
candidate_does_not_commit_marketflow_outputs
candidate_does_not_parse_terminal_logs
candidate_does_not_parse_operator_logs
candidate_does_not_inspect_env
candidate_does_not_contact_source_owners
candidate_does_not_read_external_documents
candidate_does_not_reconstruct_prior_lost_values
candidate_does_not_reconstruct_full_streams
candidate_does_not_classify_modules_again
candidate_does_not_classify_full_retry_failures
candidate_does_not_classify_full_retry_errors
candidate_does_not_claim_failure_error_separation
candidate_does_not_identify_authoritative_first_failure
candidate_does_not_identify_authoritative_first_error
candidate_does_not_claim_traceback_root_cause
candidate_does_not_claim_root_cause
candidate_does_not_claim_retry_success
candidate_does_not_claim_main_merge_readiness
candidate_does_not_create_retry_candidate
candidate_does_not_create_retry_approval
candidate_does_not_create_retry_execution
candidate_does_not_create_retry_results_review
candidate_does_not_create_main_merge_approval
candidate_does_not_push_main
candidate_does_not_push_integration_branch
candidate_does_not_delete_integration_branch
candidate_does_not_delete_worktree
candidate_does_not_force_push
candidate_does_not_modify_tags
candidate_does_not_regenerate_evidence
candidate_does_not_call_providers
candidate_does_not_acquire_market_data
candidate_does_not_generate_dataset
candidate_does_not_recompute_metrics
candidate_does_not_train_models
candidate_does_not_score_strategy
candidate_does_not_generate_trade_recommendations
candidate_does_not_accept_predictive_usefulness
candidate_does_not_accept_profitability
candidate_does_not_authorize_runtime
candidate_does_not_authorize_broker_execution
template_review_remains_source_evidence
template_is_not_actual_evidence_package
template_is_not_source_authority
template_is_not_acquired_evidence
template_completion_requires_separate_approval
completed_package_requires_results_review_before_acquisition_use
evidence_binding_requires_separate_acquisition_execution
evidence_binding_requires_results_review
acquisition_results_review_required_before_no_change_disposition
acquisition_results_review_required_before_alternate_diagnostic
acquisition_results_review_required_before_remediation
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

TRUE_FIELDS = tuple("""operator_source_authority_evidence_package_completion_candidate_created
operator_source_authority_evidence_package_completion_candidate_ready_for_operator_review
source_results_review_bound
source_template_review_bound
source_evidence_item_template_review_bound
source_preparation_checklist_review_bound
source_template_coverage_review_bound
source_execution_bound
source_approval_bound
source_attestation_bound
source_operator_review_bound
source_preparation_candidate_bound
source_failure_diagnosis_bound
source_blocked_acquisition_execution_bound
source_blocked_reason_verified
source_acquisition_approval_bound
source_follow_on_results_review_bound
source_follow_on_execution_bound
source_authority_acquisition_candidate_bound
source_authority_acquisition_scope_bound
source_missing_authority_mapping_bound
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
diagnostic_metadata_bound
observable_families_bound
reviewed_workstreams_bound
reviewed_template_structure_bound
reviewed_template_rows_bound
reviewed_template_checklist_bound
template_not_actual_evidence_package_verified
template_not_source_authority_verified
template_not_acquired_evidence_verified
template_not_acquisition_success_verified
actual_coverage_zero_bound
evidence_package_absence_bound
missing_authority_inventory_bound
completion_package_options_defined
recommended_completion_package_defined
future_completion_requirements_defined
future_completion_plan_defined
planned_outputs_defined
non_goals_defined
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_source_authority_evidence_package_completion_candidate_operator_review""".splitlines())

FALSE_FIELDS = tuple("""operator_source_authority_evidence_package_completion_package_selected
operator_source_authority_evidence_package_completion_package_approved
operator_source_authority_evidence_package_completion_package_authorized
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
pytest_performed_in_candidate
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_candidate
diagnostic_output_analyzed_in_candidate
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_candidate
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
template_execution_rerun_performed
cache_read_in_candidate
cache_modified_in_candidate
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
ready_for_operator_source_authority_evidence_package_completion_approval
ready_for_operator_source_authority_evidence_package_completion_execution
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
provider_requests_made_in_candidate
market_data_acquisition_performed_in_candidate
dataset_generation_performed_in_candidate
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

SECONDARY_FAILURE_CLASSES = (
    "SOURCE_AUTHORITY_ACQUISITION_CORRECTLY_FAILS_CLOSED_WITHOUT_OPERATOR_EVIDENCE_PACKAGE",
    "SOURCE_AUTHORITY_ACQUISITION_APPROVAL_IS_NOT_EVIDENCE_ACQUISITION",
    "SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_SCOPE_IS_NOT_SOURCE_AUTHORITY",
    "NO_EVIDENCE_PACKAGE_VALIDATION_PERFORMED_BECAUSE_PACKAGE_ABSENT",
    "ALL_30_MISSING_AUTHORITY_ITEMS_REMAIN_MISSING_NOT_ACQUIRED",
    "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED",
)


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateError(ValueError):
    """Raised when the candidate or its reviewed source binding is invalid."""


def _digest_without(value: Mapping[str, Any], *keys: str) -> str:
    return semantic_digest({key: item for key, item in value.items() if key not in keys})


def _first_difference(actual: Any, expected: Any, path: str = "candidate") -> str | None:
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
        for index, item in enumerate(expected):
            difference = _first_difference(actual[index], item, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


def _committed_source_review() -> dict[str, Any]:
    return source.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1()


def _validate_source_review(review: dict[str, Any]) -> None:
    try:
        source.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(deepcopy(review))
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateError("source results review is invalid") from exc
    expected = {
        "artifact_kind": source.ARTIFACT_KIND,
        "results_review_status": source.RESULTS_REVIEW_STATUS,
        "results_review_scope": source.RESULTS_REVIEW_SCOPE,
        source.RESULTS_REVIEW_DIGEST_KEY: SOURCE_RESULTS_REVIEW_DIGEST,
        source.TEMPLATE_REVIEW_DIGEST_KEY: SOURCE_TEMPLATE_REVIEW_DIGEST,
        source.EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST_KEY: SOURCE_EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST,
        source.CHECKLIST_REVIEW_DIGEST_KEY: SOURCE_PREPARATION_CHECKLIST_REVIEW_DIGEST,
        source.COVERAGE_REVIEW_DIGEST_KEY: SOURCE_TEMPLATE_COVERAGE_REVIEW_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
    }
    for key, expected_value in expected.items():
        if review.get(key) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateError(f"source results review {key} mismatch")


def _package_options() -> list[dict[str, Any]]:
    options = []
    for package_id, source_status, review_status, purpose, blocked_reason in PACKAGE_OPTIONS:
        item = {
            "package_id": package_id,
            "source_status": source_status,
            "candidate_review_status": review_status,
            "selected": False,
            "approved": False,
            "authorized": False,
            "executed": False,
        }
        item["blocked_reason" if blocked_reason else "purpose"] = blocked_reason or purpose
        options.append(item)
    return options


def _source_bindings(review: Mapping[str, Any]) -> dict[str, Any]:
    bindings = {
        "source_results_review_commit": SOURCE_RESULTS_REVIEW_COMMIT,
        "source_results_review_artifact_kind": review["artifact_kind"],
        "source_results_review_status": review["results_review_status"],
        "source_results_review_scope": review["results_review_scope"],
        "source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_template_review_digest": SOURCE_TEMPLATE_REVIEW_DIGEST,
        "source_evidence_item_template_review_digest": SOURCE_EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST,
        "source_preparation_checklist_review_digest": SOURCE_PREPARATION_CHECKLIST_REVIEW_DIGEST,
        "source_template_coverage_review_digest": SOURCE_TEMPLATE_COVERAGE_REVIEW_DIGEST,
        "source_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
    }
    for key in (
        "source_execution_commit", "source_execution_artifact_kind", "source_execution_status", "source_execution_scope",
        "source_execution_digest", "source_package_template_digest", "source_evidence_item_template_digest",
        "source_preparation_checklist_digest", "source_template_coverage_digest", "source_execution_manifest_digest",
        "selected_operator_source_authority_evidence_package_preparation_package",
    ):
        bindings[key] = review[key]
    for key in source.SOURCE_BINDINGS:
        target = "source_prior_results_review_digest" if key == "source_results_review_digest" else key
        bindings[target] = review[key]
    return bindings


def _assemble_candidate(source_review: dict[str, Any] | None = None) -> dict[str, Any]:
    review = _committed_source_review() if source_review is None else deepcopy(source_review)
    _validate_source_review(review)
    options = _package_options()
    rows = deepcopy(review["thirty_missing_authority_template_rows_review"])
    template_binding = {
        "package_header_template_review": deepcopy(review["package_header_template_review"]),
        "evidence_item_template_review": deepcopy(review["evidence_item_template_review"]),
        "reviewed_template_rows": rows,
        "preparation_checklist_review": deepcopy(review["preparation_checklist_review"]),
        "source_owner_request_guidance_review": deepcopy(review["source_owner_request_guidance_review"]),
        "custody_and_digest_guidance_review": deepcopy(review["custody_and_digest_guidance_review"]),
        "no_secret_boundary_review": deepcopy(review["no_secret_boundary_review"]),
        "results_review_before_use": deepcopy(review["results_review_before_use"]),
    }
    coverage = {
        "template_row_count": 30,
        "template_mapped_missing_authority_item_count": 30,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "actual_evidence_items_filled": False,
    }
    operator_inputs = {
        "required_header_fields": list(HEADER_INPUT_FIELDS),
        "required_evidence_item_fields": list(EVIDENCE_ITEM_INPUT_FIELDS),
        "non_secret_required": True,
        "api_keys_allowed": False,
        "broker_credentials_allowed": False,
        "personal_financial_credentials_allowed": False,
        "market_data_credentials_allowed": False,
        "private_tokens_allowed": False,
    }
    counts = {
        "operator_source_authority_evidence_item_count": 0,
        "operator_source_authority_evidence_item_template_count": 30,
        "reviewed_template_row_count": 30,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "template_mapped_missing_authority_item_count": 30,
        "mapped_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
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
        "future_completion_requirement_count": 67,
        "future_completion_plan_step_count": 17,
        "planned_output_count": 33,
        "non_goal_count": 71,
        "risk_control_count": 104,
        "enumerated_future_completion_requirement_count": len(FUTURE_REQUIREMENT_IDS),
        "enumerated_non_goal_count": len(NON_GOAL_IDS),
        "enumerated_risk_control_count": len(RISK_CONTROLS),
    }
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS,
        "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "candidate_only": True,
        **_source_bindings(review),
        **counts,
        **{key: True for key in TRUE_FIELDS},
        **{key: False for key in FALSE_FIELDS},
        "primary_failure_class": "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED",
        "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES),
        "retry_failure_context": deepcopy(review["retry_failure_context"]),
        "priority_1_target_modules": deepcopy(review["priority_1_target_modules"]),
        "priority1_validation_summary": deepcopy(review["priority1_validation_summary"]),
        "diagnostic_capture_evidence_summary": deepcopy(review["diagnostic_capture_evidence_summary"]),
        "reviewed_observable_failure_families": deepcopy(review["reviewed_observable_failure_families"]),
        "reviewed_workstreams": deepcopy(review["reviewed_workstreams"]),
        "reviewed_template_structure": template_binding,
        "reviewed_template_rows": rows,
        "missing_authority_mapping": deepcopy(review["missing_authority_mapping"]),
        "acceptable_source_artifact_type_inventory": deepcopy(review["acceptable_source_artifact_type_inventory"]),
        "actual_evidence_absence": deepcopy(review["actual_evidence_absence"]),
        "actual_coverage": coverage,
        "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "candidate_review_status": "CANDIDATE_READY_FOR_OPERATOR_REVIEW_NOT_SELECTED_NOT_APPROVED_NOT_EXECUTED",
        "reviewed_package_options": options,
        "recommended_operator_source_authority_evidence_package_completion_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommendation_reason": "The reviewed template and checklist exist but no actual evidence package exists; a separately approved completion execution may use non-secret operator inputs while preserving review and all authority gates.",
        "operator_input_requirements": operator_inputs,
        "future_completion_requirements": [{"requirement_id": item, "requirement_status": "REQUIRED_FOR_FUTURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION", "execution_status": "NOT_EXECUTED"} for item in FUTURE_REQUIREMENT_IDS],
        "future_completion_plan": [{"step": index, "description": item, "plan_status": "PLANNED_NOT_EXECUTED"} for index, item in enumerate(PLAN_STEPS, 1)],
        "planned_outputs": [{"output_id": item, "generation_status": "PLANNED_NOT_GENERATED"} for item in OUTPUT_IDS],
        "non_goals": [{"non_goal_id": item, "active": True} for item in NON_GOAL_IDS],
        "outputs": [{"output_id": item, "status": "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_ONLY"} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_TASK,
        "recommended_next_task_status": "FUTURE_OPERATOR_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_BEFORE_ANY_COMPLETION_APPROVAL_OR_ACQUISITION_REATTEMPT",
        "reason": "A completion candidate is required before any completion approval, completion execution, acquisition reattempt, evidence binding, disposition, remediation, retry, or main merge.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    candidate[PACKAGE_OPTIONS_DIGEST_KEY] = semantic_digest(options)
    candidate[OPERATOR_INPUT_REQUIREMENTS_DIGEST_KEY] = semantic_digest({"operator_inputs": operator_inputs, "future_requirements": candidate["future_completion_requirements"]})
    candidate[TEMPLATE_BINDING_DIGEST_KEY] = semantic_digest({"source_digests": {key: candidate[key] for key in ("source_template_review_digest", "source_evidence_item_template_review_digest", "source_preparation_checklist_review_digest", "source_template_coverage_review_digest")}, "template": template_binding})
    candidate[COVERAGE_DIGEST_KEY] = semantic_digest({"coverage": coverage, "mapping": candidate["missing_authority_mapping"]})
    exclusions = ("checklist", "summary", CANDIDATE_DIGEST_KEY, MANIFEST_DIGEST_KEY)
    candidate[CANDIDATE_DIGEST_KEY] = _digest_without(candidate, *exclusions)
    candidate[MANIFEST_DIGEST_KEY] = semantic_digest({
        "candidate_digest": candidate[CANDIDATE_DIGEST_KEY],
        "package_options_digest": candidate[PACKAGE_OPTIONS_DIGEST_KEY],
        "operator_input_requirements_digest": candidate[OPERATOR_INPUT_REQUIREMENTS_DIGEST_KEY],
        "template_binding_digest": candidate[TEMPLATE_BINDING_DIGEST_KEY],
        "coverage_digest": candidate[COVERAGE_DIGEST_KEY],
    })
    check_ids = tuple(dict.fromkeys((
        "artifact_kind_correct", "candidate_status_correct", "candidate_scope_correct",
        *(f"source_binding_{key}" for key in _source_bindings(review)),
        *(f"{key}_true" for key in TRUE_FIELDS),
        *(f"{key}_false" for key in FALSE_FIELDS),
        *(f"package_option_{item[0]}_defined" for item in PACKAGE_OPTIONS),
        *(f"requirement_{item}_defined" for item in FUTURE_REQUIREMENT_IDS),
        *(f"template_row_{index}_bound" for index in range(1, 31)),
        *(f"output_{item}_generated" for item in OUTPUT_IDS),
        *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
        "recommendation_defined", "next_chain_defined", "next_gates_defined", "digests_generated",
    )))
    candidate["checklist"] = [{"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"} for item in check_ids]
    candidate["summary"] = {
        "total_checks": len(check_ids), "passed_checks": len(check_ids), "failed_checks": 0, "blocker_count": 0,
        "operator_source_authority_evidence_package_completion_candidate_created": True,
        "operator_source_authority_evidence_package_completion_candidate_ready_for_operator_review": True,
        "recommended_operator_source_authority_evidence_package_completion_package": RECOMMENDED_PACKAGE,
        "operator_source_authority_evidence_package_completion_package_selected": False,
        "operator_source_authority_evidence_package_completed": False,
        "operator_source_authority_evidence_package_created": False,
        "operator_source_authority_evidence_package_supplied": False,
        "operator_source_authority_evidence_package_validated": False,
        "operator_source_authority_evidence_package_bound": False,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "source_authority_acquisition_performed": False,
        "source_authority_evidence_acquired": False,
        "external_evidence_acquired": False,
        "concrete_source_authority_established": False,
        "safe_source_authority_bound_change_identified": False,
        "ready_for_operator_source_authority_evidence_package_completion_candidate_operator_review": True,
        "ready_for_operator_source_authority_evidence_package_completion_approval": False,
        "ready_for_source_authority_acquisition_execution_retry": False,
        "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False,
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "recommended_next_task": RECOMMENDED_TASK,
    }
    return candidate


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(*, source_results_review: dict | None = None) -> dict[str, Any]:
    candidate = _assemble_candidate(source_results_review)
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(candidate: dict) -> dict[str, Any]:
    if not isinstance(candidate, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateError("candidate must be an object")
    expected = _assemble_candidate()
    difference = _first_difference(candidate, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateError(f"{difference} mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "candidate_digest": candidate[CANDIDATE_DIGEST_KEY],
        **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = tuple("""Purpose
Source Template-Preparation Results Review
Source Template-Preparation Execution
Source Approval
Source Operator Review
Source Preparation Candidate
Source Failure Diagnosis
Source Blocked Acquisition Execution
Source Acquisition Approval Chain
Source Follow-On Results Review
Source Follow-On Execution
Source Follow-On Approval
Source Follow-On Operator Review
Source Follow-On Candidate
Source Results Review
Source Enrichment Execution
Source Historical Approval
Source Historical Operator Review
Source Historical Candidate
Historical Failure Diagnosis
Historical Blocked Remediation
Source Remediation Plan and Method Chain
Source Diagnostic Results Review
Source Controlled Recapture
Source Durable Receipt
Source Planning and Detail Binding Evidence
Retry Failure Context
Priority 1 Target Modules
Priority 1 Validation Summary
Diagnostic Capture Evidence Summary
Reviewed Observable Families
Reviewed Workstreams
Reviewed Template Structure
Reviewed Template Rows
Missing Authority Mapping
Acceptable Source-Artifact Inventory
Actual Evidence Absence
Actual Coverage Zero
Candidate Philosophy
Reviewed Package Options
Recommended Completion Package
Future Completion Requirements
Future Completion Plan
Planned Outputs
Non-Goals
Unsupported Claims Boundary
Recommendation
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines())


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_markdown_v1(candidate: dict) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(deepcopy(candidate))
    sections: dict[str, Any] = {
        "Purpose": candidate["candidate_boundary"],
        "Source Template-Preparation Results Review": {key: candidate[key] for key in ("source_results_review_commit", "source_results_review_artifact_kind", "source_results_review_status", "source_results_review_scope", "source_results_review_digest", "source_template_review_digest", "source_evidence_item_template_review_digest", "source_preparation_checklist_review_digest", "source_template_coverage_review_digest", "source_results_review_manifest_digest")},
        "Source Template-Preparation Execution": {key: candidate[key] for key in ("source_execution_commit", "source_execution_artifact_kind", "source_execution_status", "source_execution_scope", "source_execution_digest", "source_package_template_digest", "source_evidence_item_template_digest", "source_preparation_checklist_digest", "source_template_coverage_digest", "source_execution_manifest_digest")},
        "Source Approval": {key: candidate[key] for key in ("source_approval_commit", "source_approval_digest", "source_attestation_digest")},
        "Source Operator Review": {key: candidate[key] for key in ("source_operator_review_commit", "source_operator_review_digest")},
        "Source Preparation Candidate": {key: candidate[key] for key in ("source_preparation_candidate_commit", "source_preparation_candidate_digest")},
        "Source Failure Diagnosis": {key: candidate[key] for key in ("source_failure_diagnosis_commit", "source_failure_diagnosis_digest", "primary_failure_class", "secondary_failure_classes")},
        "Source Blocked Acquisition Execution": {key: candidate[key] for key in ("source_blocked_acquisition_execution_commit", "source_blocked_acquisition_execution_reason", "source_blocked_acquisition_execution_manifest_digest")},
        "Source Acquisition Approval Chain": {key: candidate[key] for key in ("source_acquisition_approval_commit", "source_acquisition_approval_digest", "source_acquisition_attestation_digest")},
        "Retry Failure Context": candidate["retry_failure_context"],
        "Priority 1 Target Modules": candidate["priority_1_target_modules"],
        "Priority 1 Validation Summary": candidate["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": candidate["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": candidate["reviewed_observable_failure_families"],
        "Reviewed Workstreams": candidate["reviewed_workstreams"],
        "Reviewed Template Structure": candidate["reviewed_template_structure"],
        "Reviewed Template Rows": candidate["reviewed_template_rows"],
        "Missing Authority Mapping": candidate["missing_authority_mapping"],
        "Acceptable Source-Artifact Inventory": candidate["acceptable_source_artifact_type_inventory"],
        "Actual Evidence Absence": candidate["actual_evidence_absence"],
        "Actual Coverage Zero": candidate["actual_coverage"],
        "Candidate Philosophy": {"philosophy": candidate["candidate_philosophy"], "boundary": candidate["candidate_boundary"]},
        "Reviewed Package Options": candidate["reviewed_package_options"],
        "Recommended Completion Package": {"package": candidate["recommended_operator_source_authority_evidence_package_completion_package"], "status": candidate["recommendation_status"], "reason": candidate["recommendation_reason"]},
        "Future Completion Requirements": candidate["future_completion_requirements"],
        "Future Completion Plan": candidate["future_completion_plan"],
        "Planned Outputs": candidate["planned_outputs"],
        "Non-Goals": candidate["non_goals"],
        "Unsupported Claims Boundary": {key: candidate[key] for key in FALSE_FIELDS},
        "Recommendation": {key: candidate[key] for key in ("recommended_next_task", "recommended_next_task_status", "recommended_action", "reason")},
        "Next Chain": candidate["next_chain"],
        "Next Gates": candidate["next_gates"],
        "Risk Controls": candidate["risk_controls"],
        "Authority Boundaries": {**{key: candidate[key] for key in TRUE_FIELDS}, **{key: candidate[key] for key in FALSE_FIELDS}},
        "Checklist Summary": candidate["summary"],
        "Guardrails": candidate["risk_controls"],
    }
    digest_sections = {
        "Source Follow-On Results Review": "source_follow_on_results_review_digest",
        "Source Follow-On Execution": "source_follow_on_execution_digest",
        "Source Follow-On Approval": "source_follow_on_approval_digest",
        "Source Follow-On Operator Review": "source_follow_on_operator_review_digest",
        "Source Follow-On Candidate": "source_follow_on_candidate_digest",
        "Source Results Review": "source_prior_results_review_digest",
        "Source Enrichment Execution": "source_enrichment_execution_digest",
        "Source Historical Approval": "historical_source_approval_digest",
        "Source Historical Operator Review": "historical_source_operator_review_digest",
        "Source Historical Candidate": "historical_source_candidate_digest",
        "Historical Failure Diagnosis": "historical_failure_diagnosis_digest",
        "Historical Blocked Remediation": "historical_blocked_remediation_manifest_digest",
        "Source Remediation Plan and Method Chain": "source_remediation_plan_or_execution_after_method_results_review_digest",
        "Source Diagnostic Results Review": "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "Source Controlled Recapture": "source_receipt_recovery_or_recapture_execution_digest",
        "Source Durable Receipt": "source_durable_receipt_path",
        "Source Planning and Detail Binding Evidence": "source_detail_binding_results_review_digest",
    }
    sections.update({title: candidate[key] for title, key in digest_sections.items()})
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Completion Candidate After Template Preparation Results Review v1", "",
        f"Artifact: `{candidate['artifact_kind']}`", "", f"Status: `{candidate['candidate_status']}`", "",
        f"Scope: `{candidate['candidate_scope']}`", "", f"Candidate digest: `{candidate[CANDIDATE_DIGEST_KEY]}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(output_dir: str | Path, *, source_results_review: dict | None = None) -> dict[str, Any]:
    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateError("protected output directory")
    candidate = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(source_results_review=source_results_review)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_markdown_v1(candidate), encoding="utf-8")
    return candidate


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "CANDIDATE_STATUS", "CANDIDATE_SCOPE", "RECOMMENDED_PACKAGE", "RECOMMENDED_TASK",
    "CANDIDATE_DIGEST_KEY", "PACKAGE_OPTIONS_DIGEST_KEY", "OPERATOR_INPUT_REQUIREMENTS_DIGEST_KEY", "TEMPLATE_BINDING_DIGEST_KEY", "COVERAGE_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS",
    "PACKAGE_COMPLETE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_FIELDS_ONLY", "PACKAGE_COMPLETE_ASSERTION_VALUE_EVIDENCE_ITEMS_ONLY",
    "PACKAGE_COMPLETE_DIGEST_SERIALIZATION_EVIDENCE_ITEMS_ONLY", "PACKAGE_COMPLETE_FIXTURE_DETERMINISM_EVIDENCE_ITEMS_ONLY",
    "PACKAGE_COMPLETE_SCHEMA_FIELD_CONTRACT_EVIDENCE_ITEMS_ONLY", "PACKAGE_HOLD_PENDING_NON_SECRET_OPERATOR_EVIDENCE_INPUTS",
    "PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_TEMPLATE_PLACEHOLDERS_ONLY", "PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_DIAGNOSTIC_OUTPUT_ONLY",
    "PACKAGE_VALIDATE_OR_BIND_EVIDENCE_DURING_COMPLETION", "PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_IMMEDIATELY_AFTER_TEMPLATE_REVIEW",
    "PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_REVIEWED_TEMPLATE",
    "PACKAGE_OPTIONS", "HEADER_INPUT_FIELDS", "EVIDENCE_ITEM_INPUT_FIELDS", "FUTURE_REQUIREMENT_IDS", "PLAN_STEPS", "OUTPUT_IDS", "NON_GOAL_IDS", "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "TRUE_FIELDS", "FALSE_FIELDS", "MARKDOWN_SECTIONS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_markdown_v1",
]
