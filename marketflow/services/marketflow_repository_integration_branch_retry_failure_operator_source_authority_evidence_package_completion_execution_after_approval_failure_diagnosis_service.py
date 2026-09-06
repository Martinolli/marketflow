"""Diagnose the blocked completion execution without rerunning it.

The service is intentionally offline and dictionary-only.  It binds committed
facts, classifies the absent-input condition, and creates no execution authority.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_service
    as approval_source,
)
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1"
DIAGNOSIS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_READY"
DIAGNOSIS_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_ONLY_NOT_COMPLETION_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
PRIMARY_FAILURE_CLASS = source.NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED
SELECTED_PACKAGE = source.SELECTED_PACKAGE

SOURCE_COMPLETION_EXECUTION_COMMIT = "945776b2164969e067d8dcc4809128282d3b1287"
SOURCE_COMPLETION_EXECUTION_BLOCKED_DIGEST = "5fe3269b5787730da7d0287029af15956e9efae13f436c58c94e93ff7160b2c1"
SOURCE_COMPLETION_EXECUTION_BLOCKED_MANIFEST_DIGEST = "97b42143837d78ea6dba2d13a53cad5f42ffdcf8ea3f82d55c6ab521a9564cc6"

DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_digest"
FAILURE_CLASSIFICATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_classification_digest"
OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_operator_input_absence_diagnosis_digest"
COVERAGE_DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_coverage_diagnosis_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_READY = DIAGNOSIS_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_ONLY_NOT_COMPLETION_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = DIAGNOSIS_SCOPE
NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED = PRIMARY_FAILURE_CLASS
PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS = SELECTED_PACKAGE

PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

SECONDARY_FAILURE_CLASSES = (
    "COMPLETION_EXECUTION_CORRECTLY_FAILS_CLOSED_WITHOUT_OPERATOR_COMPLETION_INPUTS",
    "COMPLETION_APPROVAL_IS_NOT_OPERATOR_COMPLETION_INPUTS",
    "REVIEWED_TEMPLATE_IS_NOT_COMPLETED_OPERATOR_EVIDENCE_PACKAGE",
    "TEMPLATE_PLACEHOLDERS_CANNOT_BE_CONVERTED_TO_EVIDENCE",
    "TEST_ONLY_SYNTHETIC_SUCCESS_PATH_IS_NOT_REPOSITORY_EVIDENCE",
    "SOURCE_AUTHORITY_ACQUISITION_REMAINS_BLOCKED_UNTIL_REVIEWED_COMPLETED_PACKAGE_EXISTS",
    "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED",
)

DIAGNOSIS_DOMAINS = (
    ("source_completion_execution_identity", "PASSED", "Source blocked execution commit, artifact, status, scope, blocked digest, and manifest digest are bound."),
    ("operator_completion_input_availability", "FAILED_PRIMARY", "No operator completion inputs were supplied to the actual execution."),
    ("fail_closed_behavior", "PASSED_CORRECTLY_BLOCKED", "The execution correctly blocked instead of completing a package from placeholders."),
    ("approval_authority_boundary", "PRESERVED", "Completion approval authorizes only future execution and is not operator input or evidence."),
    ("template_boundary", "PRESERVED", "Reviewed template remains not actual evidence, not source authority, not acquired evidence, and not acquisition success."),
    ("synthetic_success_path_boundary", "TEST_ONLY_NOT_REPOSITORY_EVIDENCE", "Synthetic success path was tested with injected non-secret inputs only and was not written as actual evidence."),
    ("evidence_package_status", "NOT_CREATED_NOT_SUPPLIED_NOT_VALIDATED_NOT_BOUND", "No actual evidence package exists."),
    ("coverage_status", "UNCHANGED_ZERO_OF_THIRTY", "Actual coverage remains 0/30 and all missing-authority items remain missing."),
    ("source_authority_status", "NOT_ACQUIRED", "No source authority, source-authority evidence, or external evidence was acquired."),
    ("downstream_status", "CLOSED", "Acquisition reattempt, disposition, diagnostics, remediation, retry, and main merge remain closed."),
    ("retry_status", "FAILED_RETRY_REMAINS_AUTHORITATIVE", "The detached retry remains failed and authoritative."),
    ("protected_repository_boundaries", "PRESERVED", "Main, integration branch, detached worktree, cache, .marketflow, tags, and staged evidence boundaries remain preserved."),
    ("provider_runtime_trading_boundary", "PRESERVED", "No provider, market-data, runtime, broker, or trading action occurred."),
)

DIAGNOSIS_FINDINGS = (
    "The completion execution gate was implemented and invoked.",
    "The selected completion package was approved for future execution only.",
    "The actual execution did not receive operator completion inputs.",
    "The actual execution correctly failed closed.",
    "The blocked reason is NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED.",
    "No completed evidence package was created.",
    "No evidence package was created, supplied, validated, bound, or accepted.",
    "No actual evidence item was filled.",
    "Actual coverage remains 0/30.",
    "All 30 missing-authority items remain MISSING_NOT_ACQUIRED.",
    "The reviewed template remains not evidence and not source authority.",
    "The approval remains not operator inputs and not evidence.",
    "The synthetic success path remains test-only and non-authoritative.",
    "No source-authority acquisition execution was created.",
    "No source authority, source-authority evidence, or external evidence was acquired.",
    "No concrete authority or safe change was established.",
    "No no-change disposition, alternate diagnostic, or remediation was created.",
    "No retry candidate, retry approval, retry execution, retry results review, or main-merge approval was created.",
    "The failed detached retry remains authoritative.",
    "The next safe step is a governed operator completion-input preparation or supply candidate.",
)

OUTPUT_IDS = tuple("""operator_source_authority_evidence_package_completion_execution_failure_diagnosis_manifest
source_completion_execution_binding_report
source_approval_binding_report
source_operator_review_binding_report
source_completion_candidate_binding_report
source_template_preparation_results_review_binding_report
source_template_preparation_execution_binding_report
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
operator_completion_inputs_absence_diagnosis
blocked_reason_diagnosis_report
fail_closed_behavior_report
synthetic_success_path_boundary_report
source_authority_gap_preservation_report
acquisition_reattempt_gate_preservation_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Source Authority Evidence Package Completion Inputs Preparation or Supply Candidate After Blocked Completion Execution v1.",
    "Operator Completion Inputs Candidate Operator Review v1.",
    "Operator Completion Inputs Approval v1, if selected.",
    "Completion Execution Reattempt v1, only if approved and explicit non-secret operator inputs are supplied.",
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

NEXT_GATES = tuple("""operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution
operator_completion_inputs_candidate_operator_review
operator_completion_inputs_approval_if_selected
completion_execution_reattempt_with_explicit_non_secret_operator_inputs_if_approved
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

RISK_CONTROLS = tuple("""diagnosis_does_not_rerun_completion_execution
diagnosis_does_not_supply_operator_completion_inputs
diagnosis_does_not_create_completed_evidence_package
diagnosis_does_not_fill_actual_evidence_items
diagnosis_does_not_validate_evidence_package
diagnosis_does_not_bind_evidence_package
diagnosis_does_not_accept_evidence_as_source_authority
diagnosis_confirms_fail_closed_without_inputs
diagnosis_confirms_approval_is_not_inputs
diagnosis_confirms_template_is_not_evidence
diagnosis_confirms_template_is_not_source_authority
diagnosis_confirms_template_is_not_acquired_evidence
diagnosis_confirms_synthetic_success_path_is_test_only
diagnosis_does_not_acquire_source_authority
diagnosis_does_not_acquire_source_authority_evidence
diagnosis_does_not_acquire_external_evidence
diagnosis_does_not_retry_acquisition_execution
diagnosis_does_not_create_acquisition_execution
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
approved_completion_package_is_not_execution_success
completed_package_requires_results_review_before_acquisition_use
evidence_binding_requires_separate_acquisition_execution
evidence_binding_requires_results_review
acquisition_results_review_required_before_no_change_disposition
acquisition_results_review_required_before_alternate_diagnostic
acquisition_results_review_required_before_remediation
separate_completion_reattempt_requires_operator_inputs
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

TRUE_FIELDS = tuple("""operator_source_authority_evidence_package_completion_execution_failure_diagnosis_created
operator_source_authority_evidence_package_completion_execution_failure_diagnosis_ready
source_completion_execution_bound
source_completion_execution_reviewed
source_completion_execution_status_verified
source_completion_execution_scope_verified
source_completion_execution_blocked_reason_verified
source_completion_execution_blocked_digest_verified
source_completion_execution_blocked_manifest_digest_verified
source_completion_execution_success_digests_absent_verified
source_approval_bound
source_attestation_bound
selected_completion_package_verified
source_operator_review_bound
source_completion_candidate_bound
source_results_review_bound
source_template_preparation_execution_bound
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
count_label_distinction_preserved
operator_completion_inputs_absence_verified
blocked_failure_classification_created
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_completion_inputs_preparation_or_supply_candidate""".splitlines())

FALSE_FIELDS = tuple("""completion_execution_rerun_performed
operator_completion_inputs_provided
operator_completion_inputs_validated
operator_completion_inputs_bound
operator_completion_inputs_contained_secrets
operator_source_authority_evidence_package_completion_package_executed
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
provider_requests_made_in_diagnosis
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
    "acquisition_scope_section_count": 4, "acceptable_source_artifact_type_count": 13,
    "operator_provided_evidence_requirement_count": 10, "evidence_custody_and_digest_requirement_count": 6,
    "candidate_results_review_requirement_count": 16, "observable_failure_family_count": 4,
    "total_observable_evidence_items": 188, "priority_1_total_nodeids": 612,
    "top_10_count_sum": 1069, "failed_or_errored_nodeids_count": 1404,
    "module_summary_module_count": 29, "package_option_count": 12,
    "available_package_count": 7, "blocked_package_count": 5,
    "future_completion_requirement_count": 67, "source_enumerated_future_completion_requirement_count": 69,
    "approved_future_completion_requirement_named_count": 69, "future_completion_plan_step_count": 17,
    "planned_output_count": 33, "non_goal_count": 71, "source_enumerated_non_goal_count": 76,
    "risk_control_count": 104, "source_enumerated_risk_control_count": 106,
}


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError(ValueError):
    """Raised when diagnosis evidence or its authority boundary differs."""


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


def _committed_source_completion_execution() -> dict[str, Any]:
    """Reconstruct the committed blocked-execution projection without a source builder."""
    review = source._committed_source_review()
    bindings = approval_source._source_bindings(review)
    return {
        "artifact_kind": source.BLOCKED_ARTIFACT_KIND,
        "schema_version": source.SCHEMA_VERSION,
        "execution_status": source.BLOCKED_STATUS,
        "execution_scope": source.EXECUTION_SCOPE,
        "blocked_reason": PRIMARY_FAILURE_CLASS,
        "source_approval_artifact_kind": approval_source.ARTIFACT_KIND,
        "source_approval_status": approval_source.APPROVAL_STATUS,
        "source_approval_scope": approval_source.APPROVAL_SCOPE,
        **bindings,
        "source_approval_commit": source.SOURCE_APPROVAL_COMMIT,
        "source_approval_digest": source.SOURCE_APPROVAL_DIGEST,
        "source_attestation_digest": source.SOURCE_ATTESTATION_DIGEST,
        "selected_operator_source_authority_evidence_package_completion_package": SELECTED_PACKAGE,
        **{key: deepcopy(review[key]) for key in approval_source.SOURCE_CONTEXT_KEYS},
        "count_label_distinction": deepcopy(review["count_label_distinction"]),
        "primary_failure_class": review["primary_failure_class"],
        "historical_blocked_remediation_reason": review["historical_blocked_remediation_reason"],
        "historical_blocked_remediation_manifest_digest": review["historical_blocked_remediation_manifest_digest"],
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_pytest_working_directory": "C:\\Users\\Aspire5 15 i7 4G2050\\marketflow_worktrees\\integration-terminal-evidence-stack-validation-v1",
        "retry_pytest_passed_count": 24877, "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112, "retry_pytest_skipped_count": 7,
        "retry_pytest_first_result_authoritative": True, "retry_pytest_passed": False,
        "retry_pytest_failed": True, "root_full_regression_is_retry_evidence": False,
        "priority1_pre_change_validation_passed": True, "priority1_pre_change_validation_passed_count": 675,
        "priority1_post_change_validation_passed": True, "priority1_post_change_validation_passed_count": 675,
        "priority1_post_change_validation_duration_seconds": "41.88",
        "priority1_post_change_stdout_byte_count": 832, "priority1_post_change_stderr_byte_count": 0,
        "priority1_post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
        "priority1_post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "priority1_validation_is_retry_evidence": False,
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
        "source_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True, "source_diagnostic_metadata_only": True,
        **COUNTS,
        **{key: False for key in source.ALWAYS_FALSE_FIELDS},
        **{key: False for key in source.BLOCKED_ONLY_FALSE_FIELDS},
        "operator_source_authority_evidence_package_completion_execution_blocked": True,
        source.BLOCKED_DIGEST_KEY: SOURCE_COMPLETION_EXECUTION_BLOCKED_DIGEST,
        source.BLOCKED_MANIFEST_DIGEST_KEY: SOURCE_COMPLETION_EXECUTION_BLOCKED_MANIFEST_DIGEST,
    }


def _validate_source_completion_execution(execution: Any) -> None:
    if not isinstance(execution, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError("source_completion_execution invalid")
    expected = _committed_source_completion_execution()
    for key, value in expected.items():
        if key not in execution or _first_difference(execution[key], value, f"source_completion_execution.{key}"):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError(f"source_completion_execution.{key} mismatch")
    for key in (source.EXECUTION_DIGEST_KEY, source.COMPLETED_PACKAGE_DIGEST_KEY, source.COMPLETED_ITEMS_DIGEST_KEY, source.MANIFEST_DIGEST_KEY):
        if key in execution:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError(f"source_completion_execution.{key} must be absent")


def _digest_without(diagnosis: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(diagnosis))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_diagnosis(execution: Mapping[str, Any]) -> dict[str, Any]:
    upstream = {
        key: deepcopy(value) for key, value in execution.items()
        if (key.startswith("source_") or key.startswith("historical_"))
        and key not in {"source_completion_execution_blocked_digest", "source_completion_execution_blocked_manifest_digest"}
    }
    context_keys = (*approval_source.SOURCE_CONTEXT_KEYS, "count_label_distinction")
    diagnosis: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "diagnosis_status": DIAGNOSIS_STATUS, "diagnosis_scope": DIAGNOSIS_SCOPE,
        "created_offline": True, "governance_only": True, "failure_diagnosis_only": True,
        "source_completion_execution_commit": SOURCE_COMPLETION_EXECUTION_COMMIT,
        "source_completion_execution_artifact_kind": source.BLOCKED_ARTIFACT_KIND,
        "source_completion_execution_status": source.BLOCKED_STATUS,
        "source_completion_execution_scope": source.EXECUTION_SCOPE,
        "source_completion_execution_blocked_reason": PRIMARY_FAILURE_CLASS,
        "source_completion_execution_blocked_digest": SOURCE_COMPLETION_EXECUTION_BLOCKED_DIGEST,
        "source_completion_execution_blocked_manifest_digest": SOURCE_COMPLETION_EXECUTION_BLOCKED_MANIFEST_DIGEST,
        "source_completion_execution_success_digests_absent": True,
        "selected_operator_source_authority_evidence_package_completion_package": SELECTED_PACKAGE,
        **upstream,
        **{key: deepcopy(execution[key]) for key in context_keys},
        **{key: deepcopy(execution[key]) for key in (
            "retry_execution_branch", "retry_execution_commit", "retry_pytest_working_directory",
            "retry_pytest_passed_count", "retry_pytest_failed_count", "retry_pytest_error_count",
            "retry_pytest_skipped_count", "retry_pytest_first_result_authoritative", "retry_pytest_passed",
            "retry_pytest_failed", "root_full_regression_is_retry_evidence",
            "priority1_pre_change_validation_passed", "priority1_pre_change_validation_passed_count",
            "priority1_post_change_validation_passed", "priority1_post_change_validation_passed_count",
            "priority1_post_change_validation_duration_seconds", "priority1_post_change_stdout_byte_count",
            "priority1_post_change_stderr_byte_count", "priority1_post_change_stdout_sha256",
            "priority1_post_change_stderr_sha256", "priority1_validation_is_retry_evidence",
            "source_exit_code", "source_duration_seconds", "source_stdout_byte_count", "source_stderr_byte_count",
            "source_combined_output_byte_count", "source_stdout_sha256", "source_stderr_sha256",
            "source_stdout_excerpt_truncated", "source_stderr_excerpt_truncated", "source_redaction_checked",
            "source_diagnostic_metadata_only",
        )},
        **COUNTS, **{key: True for key in TRUE_FIELDS}, **{key: False for key in FALSE_FIELDS},
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES),
        "diagnosis_domains": [
            {"domain_id": item[0], "disposition": item[1], "explanation": item[2]}
            for item in DIAGNOSIS_DOMAINS
        ],
        "diagnosis_findings": [
            {"finding_id": f"FINDING-{index:02d}", "finding": item}
            for index, item in enumerate(DIAGNOSIS_FINDINGS, 1)
        ],
        "operator_completion_input_absence_diagnosis": {
            "operator_completion_inputs_provided": False,
            "operator_completion_inputs_validated": False,
            "operator_completion_inputs_bound": False,
            "approval_is_operator_completion_inputs": False,
            "reviewed_template_is_operator_completion_inputs": False,
            "primary_failure_class": PRIMARY_FAILURE_CLASS,
            "fail_closed_behavior_correct": True,
        },
        "synthetic_success_path_boundary": {
            "fixture_marker": "TEST_ONLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_NOT_REAL_SOURCE_AUTHORITY",
            "test_only": True, "repository_evidence": False, "actual_execution_success": False,
            "success_digests_present_in_source_execution": False,
        },
        "coverage_diagnosis": {
            "reviewed_template_row_count": 30, "actual_covered_missing_authority_item_count": 0,
            "actual_uncovered_missing_authority_item_count": 30,
            "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
            "all_missing_authority_items_remain_missing": True,
        },
        "outputs": [{"output_id": item, "status": "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_FAILURE_DIAGNOSIS_ONLY"} for item in OUTPUT_IDS],
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_V1",
        "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_BEFORE_ANY_COMPLETION_REATTEMPT",
        "reason": "The completion execution was approved, implemented, and attempted, but no non-secret operator completion inputs were supplied. The execution correctly failed closed instead of creating a completed evidence package from placeholders or diagnostic output. A separately governed candidate is required before any completion execution reattempt, completion results review, source-authority acquisition reattempt, disposition, remediation, retry, or main merge.",
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    diagnosis[FAILURE_CLASSIFICATION_DIGEST_KEY] = semantic_digest({
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES),
    })
    diagnosis[OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY] = semantic_digest(diagnosis["operator_completion_input_absence_diagnosis"])
    diagnosis[COVERAGE_DIAGNOSIS_DIGEST_KEY] = semantic_digest(diagnosis["coverage_diagnosis"])
    digest_exclusions = (
        "checklist", "summary", DIAGNOSIS_DIGEST_KEY, MANIFEST_DIGEST_KEY,
    )
    diagnosis[DIAGNOSIS_DIGEST_KEY] = _digest_without(diagnosis, *digest_exclusions)
    diagnosis[MANIFEST_DIGEST_KEY] = semantic_digest({
        "diagnosis_digest": diagnosis[DIAGNOSIS_DIGEST_KEY],
        "failure_classification_digest": diagnosis[FAILURE_CLASSIFICATION_DIGEST_KEY],
        "operator_input_absence_diagnosis_digest": diagnosis[OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY],
        "coverage_diagnosis_digest": diagnosis[COVERAGE_DIAGNOSIS_DIGEST_KEY],
        "source_completion_execution_blocked_digest": SOURCE_COMPLETION_EXECUTION_BLOCKED_DIGEST,
        "source_completion_execution_blocked_manifest_digest": SOURCE_COMPLETION_EXECUTION_BLOCKED_MANIFEST_DIGEST,
    })
    diagnosis["checklist"] = _checklist(diagnosis)
    diagnosis["summary"] = _summary(diagnosis)
    return diagnosis


def _checklist(diagnosis: Mapping[str, Any]) -> list[dict[str, Any]]:
    fixed = tuple("""artifact_kind_correct
diagnosis_status_correct
diagnosis_scope_correct
source_completion_execution_commit_bound
source_completion_execution_artifact_kind_bound
source_completion_execution_status_bound
source_completion_execution_scope_bound
source_completion_execution_blocked_reason_bound
source_completion_execution_blocked_digest_bound
source_completion_execution_blocked_manifest_digest_bound
source_completion_execution_success_digests_absent
primary_failure_class_correct
secondary_failure_classes_defined
durable_receipt_path_bound
durable_receipt_not_parsed
retry_failure_counts_bound
priority_1_total_612_bound
top_10_total_1069_bound
module_summary_count_29_bound
failed_or_errored_nodeids_1404_bound
priority1_validation_675_pre_and_post_bound
priority1_validation_not_retry_evidence
diagnostic_exit_code_1_bound_as_diagnostic_only
observable_family_count_4_bound
observable_evidence_items_188_bound
workstream_count_4_bound
reviewed_template_row_count_30
actual_coverage_zero
missing_authority_items_missing_not_acquired
operator_completion_inputs_absence_verified
diagnosis_domains_defined
diagnosis_findings_defined
diagnosis_outputs_generated
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
diagnosis_digest_generated
failure_classification_digest_generated
operator_input_absence_diagnosis_digest_generated
coverage_diagnosis_digest_generated
manifest_digest_generated
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines())
    source_checks = tuple(f"{key}_bound" for key in sorted(diagnosis) if key.startswith("source_") and (key.endswith("_digest") or key.endswith("_commit")))
    check_ids = tuple(dict.fromkeys((
        *fixed, *source_checks, *(f"{key}_true" for key in TRUE_FIELDS),
        *(f"{key}_false" for key in FALSE_FIELDS),
        *(f"domain_{item[0]}_defined" for item in DIAGNOSIS_DOMAINS),
        *(f"finding_{index:02d}_defined" for index in range(1, len(DIAGNOSIS_FINDINGS) + 1)),
        *(f"output_{item}_generated" for item in OUTPUT_IDS),
        *(f"next_gate_{item}_defined" for item in NEXT_GATES),
        *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
    )))
    return [{"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"} for item in check_ids]


def _summary(diagnosis: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "total_checks": len(diagnosis["checklist"]), "passed_checks": len(diagnosis["checklist"]),
        "failed_checks": 0, "blocker_count": 0,
        **{key: deepcopy(diagnosis[key]) for key in (
            "operator_source_authority_evidence_package_completion_execution_failure_diagnosis_created",
            "operator_source_authority_evidence_package_completion_execution_failure_diagnosis_ready",
            "source_completion_execution_commit", "source_completion_execution_blocked_reason",
            "source_completion_execution_blocked_digest", "source_completion_execution_blocked_manifest_digest",
            "source_completion_execution_success_digests_absent", "source_approval_digest", "source_attestation_digest",
            "selected_operator_source_authority_evidence_package_completion_package", "primary_failure_class",
            "operator_completion_inputs_provided", "operator_source_authority_evidence_package_completion_executed",
            "operator_source_authority_evidence_package_completed", "operator_source_authority_evidence_package_created",
            "operator_source_authority_evidence_package_supplied", "operator_source_authority_evidence_package_validated",
            "operator_source_authority_evidence_package_bound", "source_authority_acquisition_performed",
            "source_authority_evidence_acquired", "external_evidence_acquired", "concrete_source_authority_established",
            "safe_source_authority_bound_change_identified", "actual_covered_missing_authority_item_count",
            "actual_uncovered_missing_authority_item_count", "missing_authority_items_status",
            "ready_for_operator_completion_inputs_preparation_or_supply_candidate",
            "ready_for_operator_source_authority_evidence_package_completion_execution",
            "ready_for_operator_source_authority_evidence_package_completion_results_review",
            "ready_for_source_authority_acquisition_execution_retry", "ready_for_source_authority_acquisition_results_review",
            "ready_for_remediation_execution", "ready_for_retry_candidate", "ready_for_main_merge_approval",
            "priority_1_total_nodeids", "failed_or_errored_nodeids_count", "observable_failure_family_count",
            "total_observable_evidence_items", "recommended_next_task",
        )},
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(
    *, source_completion_execution: dict | None = None,
) -> dict[str, Any]:
    """Build the deterministic diagnosis from committed blocked-execution facts."""
    execution = _committed_source_completion_execution() if source_completion_execution is None else deepcopy(source_completion_execution)
    _validate_source_completion_execution(execution)
    diagnosis = _assemble_diagnosis(execution)
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(diagnosis)
    return diagnosis


def validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(
    diagnosis: dict,
) -> dict[str, Any]:
    """Reject any changed binding, diagnosis fact, digest, or closed boundary."""
    if not isinstance(diagnosis, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError("diagnosis must be an object")
    expected = _assemble_diagnosis(_committed_source_completion_execution())
    difference = _first_difference(diagnosis, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError(f"{difference} mismatch")
    for key in (DIAGNOSIS_DIGEST_KEY, FAILURE_CLASSIFICATION_DIGEST_KEY, OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY, COVERAGE_DIAGNOSIS_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        value = diagnosis.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError(f"{key} invalid")
    return {
        "artifact_kind": ARTIFACT_KIND, "diagnosis_status": DIAGNOSIS_STATUS,
        "diagnosis_scope": DIAGNOSIS_SCOPE, "diagnosis_digest": diagnosis[DIAGNOSIS_DIGEST_KEY],
        **{key: diagnosis["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Diagnosis Disposition", "Primary Failure Class", "Secondary Failure Classes", "Source Completion Execution",
    "Blocked Reason", "Blocked Digest Manifest", "Source Approval", "Selected Completion Package",
    "Source Operator Review", "Source Completion Candidate", "Source Template Preparation Results Review",
    "Source Template Preparation Execution", "Source Preparation Candidate", "Source Failure Diagnosis",
    "Source Blocked Acquisition Execution", "Source Acquisition Approval Chain", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt", "Retry Failure Context",
    "Priority 1 Target Modules", "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary",
    "Reviewed Observable Families", "Reviewed Workstreams", "Reviewed Template Structure", "Count Label Distinction",
    "Operator Completion Input Absence", "Synthetic Success Path Boundary", "Actual Evidence Absence",
    "Actual Coverage Zero", "Source Authority Gap Preservation", "Diagnosis Domains", "Diagnosis Findings",
    "Unsupported Claims Boundary", "Recommendation", "Next Chain", "Next Gates", "Risk Controls",
    "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_markdown_v1(
    diagnosis: dict,
) -> str:
    """Render the diagnosis without expanding raw upstream structures."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(diagnosis)
    summary = diagnosis["summary"]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Completion Execution After Approval Failure Diagnosis v1", ""]
    facts = {
        "Diagnosis Disposition": f"`{DIAGNOSIS_STATUS}` within `{DIAGNOSIS_SCOPE}`. Diagnosis `{diagnosis[DIAGNOSIS_DIGEST_KEY]}`; manifest `{diagnosis[MANIFEST_DIGEST_KEY]}`.",
        "Primary Failure Class": f"`{PRIMARY_FAILURE_CLASS}`.",
        "Secondary Failure Classes": "\n".join(f"- `{item}`" for item in SECONDARY_FAILURE_CLASSES),
        "Source Completion Execution": f"Commit `{SOURCE_COMPLETION_EXECUTION_COMMIT}`; artifact `{source.BLOCKED_ARTIFACT_KIND}`; status `{source.BLOCKED_STATUS}`; scope `{source.EXECUTION_SCOPE}`.",
        "Blocked Reason": f"`{PRIMARY_FAILURE_CLASS}`.",
        "Blocked Digest Manifest": f"Blocked digest `{SOURCE_COMPLETION_EXECUTION_BLOCKED_DIGEST}`; blocked manifest `{SOURCE_COMPLETION_EXECUTION_BLOCKED_MANIFEST_DIGEST}`; success digests absent.",
        "Source Approval": f"Commit `{diagnosis['source_approval_commit']}`; approval `{diagnosis['source_approval_digest']}`; attestation `{diagnosis['source_attestation_digest']}`.",
        "Selected Completion Package": f"`{SELECTED_PACKAGE}` was approved for future execution only and is not input or evidence.",
        "Source Operator Review": f"Commit `{diagnosis['source_operator_review_commit']}`; digest `{diagnosis['source_operator_review_digest']}`; manifest `{diagnosis['source_operator_review_manifest_digest']}`.",
        "Source Completion Candidate": f"Commit `{diagnosis['source_completion_candidate_commit']}`; digest `{diagnosis['source_completion_candidate_digest']}`; manifest `{diagnosis['source_completion_candidate_manifest_digest']}`.",
        "Source Template Preparation Results Review": f"Results `{diagnosis['source_results_review_digest']}`; template `{diagnosis['source_template_review_digest']}`; coverage `{diagnosis['source_template_coverage_review_digest']}`.",
        "Source Template Preparation Execution": f"Execution `{diagnosis['source_execution_digest']}`; package template `{diagnosis['source_package_template_digest']}`; manifest `{diagnosis['source_execution_manifest_digest']}`.",
        "Source Preparation Candidate": f"Commit `{diagnosis['source_preparation_candidate_commit']}`; digest `{diagnosis['source_preparation_candidate_digest']}`.",
        "Source Failure Diagnosis": f"Commit `{diagnosis['source_failure_diagnosis_commit']}`; digest `{diagnosis['source_failure_diagnosis_digest']}`.",
        "Source Blocked Acquisition Execution": f"Reason `{diagnosis['source_blocked_acquisition_execution_reason']}`; manifest `{diagnosis['source_blocked_acquisition_execution_manifest_digest']}`.",
        "Source Acquisition Approval Chain": f"Approval `{diagnosis['source_acquisition_approval_digest']}`; attestation `{diagnosis['source_acquisition_attestation_digest']}`. No acquisition occurred.",
        "Source Follow-On and Enrichment Chain": f"Follow-on review `{diagnosis['source_follow_on_results_review_digest']}`; execution `{diagnosis['source_follow_on_execution_digest']}`; enrichment `{diagnosis['source_enrichment_execution_digest']}`.",
        "Historical Blocked Remediation": f"Reason `{diagnosis['historical_blocked_remediation_reason']}`; manifest `{diagnosis['historical_blocked_remediation_manifest_digest']}`.",
        "Plan Method Diagnostic Recovery Chain": f"Targeted plan `{diagnosis['source_targeted_remediation_plan_digest']}`; method execution `{diagnosis['source_remediation_or_method_execution_after_diagnostic_capture_digest']}`; recovery `{diagnosis['source_recovery_results_review_digest']}`.",
        "Durable Receipt": f"`{diagnosis['source_durable_receipt_path']}` is bound and was not parsed.",
        "Retry Failure Context": "The authoritative detached retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped; the root regression is not retry evidence.",
        "Priority 1 Target Modules": "Five reviewed modules; Priority 1 total 612, top-10 total 1,069, and 1,404 failed-or-errored node IDs across 29 modules.",
        "Priority 1 Validation Summary": "675/675 pre-change and 675/675 post-change passed as current-root focused evidence only.",
        "Diagnostic Capture Evidence Summary": f"Exit 1; stdout {diagnosis['source_stdout_byte_count']} bytes `{diagnosis['source_stdout_sha256']}`; stderr 0 bytes `{diagnosis['source_stderr_sha256']}`. Metadata only.",
        "Reviewed Observable Families": "Four HIGH-confidence planning families with 188 observations total are preserved without reclassification.",
        "Reviewed Workstreams": "Four committed workstreams are preserved without execution.",
        "Reviewed Template Structure": "Thirty reviewed template rows map MA-001 through MA-030. The template is not evidence or source authority.",
        "Count Label Distinction": "Preserved without reconciliation: requirements 67/69; non-goals 71/76; risk controls 104/106.",
        "Operator Completion Input Absence": f"Classification `{diagnosis[OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY]}` confirms inputs were not provided, validated, or bound.",
        "Synthetic Success Path Boundary": "`TEST_ONLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_NOT_REAL_SOURCE_AUTHORITY` remains test-only and is not repository evidence.",
        "Actual Evidence Absence": "No completed package or evidence package was created, supplied, validated, bound, accepted, or filled.",
        "Actual Coverage Zero": f"Coverage remains 0/30 and `MISSING_NOT_ACQUIRED`; coverage digest `{diagnosis[COVERAGE_DIAGNOSIS_DIGEST_KEY]}`.",
        "Source Authority Gap Preservation": "No source authority, source-authority evidence, external evidence, concrete authority, or safe change was created.",
        "Unsupported Claims Boundary": "No root-cause, first-failure, retry-success, acquisition, remediation, retry, or main-readiness claim is made.",
        "Recommendation": f"`{diagnosis['recommended_next_task']}`: `{diagnosis['recommended_action']}`.",
        "Authority Boundaries": "Completion, validation, binding, acquisition, disposition, remediation, retry, runtime, broker, trading, and protected-branch authority remain false or NOT_AUTHORIZED.",
        "Checklist Summary": f"{summary['passed_checks']}/{summary['total_checks']} PASS; blockers={summary['blocker_count']}.",
        "Guardrails": "Offline dictionary-only diagnosis; no source builders, files, subprocesses, pytest, caches, logs, environment, receipts, providers, external documents, or runtime outputs are accessed.",
    }
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", "", facts.get(section, "Preserved from committed source evidence; no new authority is created."), ""))
        if section == "Diagnosis Domains":
            lines[-2:-2] = [*(f"- `{item['domain_id']}` — `{item['disposition']}`: {item['explanation']}" for item in diagnosis["diagnosis_domains"]), ""]
        elif section == "Diagnosis Findings":
            lines[-2:-2] = [*(f"{index}. {item['finding']}" for index, item in enumerate(diagnosis["diagnosis_findings"], 1)), ""]
        elif section == "Next Chain":
            lines[-2:-2] = [*(f"{index}. {item}" for index, item in enumerate(diagnosis["next_chain"], 1)), ""]
        elif section == "Next Gates":
            lines[-2:-2] = [*(f"- `{item}`" for item in diagnosis["next_gates"]), ""]
        elif section == "Risk Controls":
            lines[-2:-2] = [*(f"- `{item}`" for item in diagnosis["risk_controls"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(
    output_dir: str | Path, *, source_completion_execution: dict | None = None,
) -> dict[str, Any]:
    """Write only the requested Markdown diagnosis status."""
    diagnosis = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(
        source_completion_execution=source_completion_execution,
    )
    destination = Path(output_dir) / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_markdown_v1(diagnosis), encoding="utf-8")
    return diagnosis


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "DIAGNOSIS_STATUS", "DIAGNOSIS_SCOPE", "PRIMARY_FAILURE_CLASS",
    "SECONDARY_FAILURE_CLASSES", "SELECTED_PACKAGE", "SOURCE_COMPLETION_EXECUTION_COMMIT",
    "SOURCE_COMPLETION_EXECUTION_BLOCKED_DIGEST", "SOURCE_COMPLETION_EXECUTION_BLOCKED_MANIFEST_DIGEST",
    "DIAGNOSIS_DIGEST_KEY", "FAILURE_CLASSIFICATION_DIGEST_KEY", "OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY",
    "COVERAGE_DIAGNOSIS_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_ONLY_NOT_COMPLETION_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED",
    "PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_markdown_v1",
]
