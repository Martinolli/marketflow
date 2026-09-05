"""Define candidate-only next paths after the blocked remediation execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
CANDIDATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest"
SOURCE_FAILURE_DIAGNOSIS_COMMIT = "954a3654bc6b1a485d2b13fe2462510ffebe1025"
SOURCE_FAILURE_DIAGNOSIS_DIGEST = "0cdff5ed2e41e77a90c1be358428aaf74a3fcf04b82513771e64e01493381171"

PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION = "PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION"
PACKAGE_CREATE_NO_CHANGE_DISPOSITION_REVIEW_FOR_CURRENT_ROOT_PRIORITY1_PASSING_STATE = "PACKAGE_CREATE_NO_CHANGE_DISPOSITION_REVIEW_FOR_CURRENT_ROOT_PRIORITY1_PASSING_STATE"
PACKAGE_REQUEST_ALTERNATE_BOUNDED_DIAGNOSTIC_CAPTURE_FOR_DETACHED_RETRY_FAILURES = "PACKAGE_REQUEST_ALTERNATE_BOUNDED_DIAGNOSTIC_CAPTURE_FOR_DETACHED_RETRY_FAILURES"
PACKAGE_COMPARE_CURRENT_ROOT_PRIORITY1_PASSING_STATE_TO_DETACHED_RETRY_CONTEXT = "PACKAGE_COMPARE_CURRENT_ROOT_PRIORITY1_PASSING_STATE_TO_DETACHED_RETRY_CONTEXT"
PACKAGE_CREATE_NO_CHANGE_RETRY_CANDIDATE_CRITERIA_ONLY = "PACKAGE_CREATE_NO_CHANGE_RETRY_CANDIDATE_CRITERIA_ONLY"
PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_EXTERNAL_SOURCE_AUTHORITY = "PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_EXTERNAL_SOURCE_AUTHORITY"
PACKAGE_DIRECT_REMEDIATION_DESPITE_NO_SOURCE_AUTHORITY = "PACKAGE_DIRECT_REMEDIATION_DESPITE_NO_SOURCE_AUTHORITY"
PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_TO_MATCH_CURRENT_ROOT_PASSING_STATE = "PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_TO_MATCH_CURRENT_ROOT_PASSING_STATE"
PACKAGE_REWRITE_TESTS_OR_SKIP_FAILURES_WITHOUT_SOURCE_AUTHORITY = "PACKAGE_REWRITE_TESTS_OR_SKIP_FAILURES_WITHOUT_SOURCE_AUTHORITY"
PACKAGE_NEW_RETRY_BECAUSE_PRIORITY1_CURRENT_ROOT_PASSES = "PACKAGE_NEW_RETRY_BECAUSE_PRIORITY1_CURRENT_ROOT_PASSES"
PACKAGE_MAIN_MERGE_BECAUSE_CURRENT_ROOT_REGRESSION_PREVIOUSLY_PASSED = "PACKAGE_MAIN_MERGE_BECAUSE_CURRENT_ROOT_REGRESSION_PREVIOUSLY_PASSED"
PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY = "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY"
RECOMMENDED_PACKAGE = PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_V1"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

CANDIDATE_PHILOSOPHY = (
    "The blocked remediation execution and its diagnosis show that the reviewed plan and four workstreams provide "
    "planning structure but not concrete change authority. Priority 1 focused validation passes in the current root "
    "context, while the detached retry remains failed and authoritative. The next governed decision must choose "
    "whether to enrich source authority, request alternate bounded diagnostics, create a no-change disposition path, "
    "or hold retry and main merge blocked. This candidate defines options only and does not approve or execute any path."
)
CANDIDATE_BOUNDARY = "Candidate-only; no package selection, approval, execution, remediation, code change, test change, digest update, patch generation, pytest, retry, main merge, provider request, runtime, broker, or trading authority is created."
CANDIDATE_GOAL = "Define safe future paths after a blocked controlled remediation execution where no source-authority-bound change was identified."

PACKAGE_DEFINITIONS = (
    (PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION, "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED", "Future execution may create a source-authority enrichment plan to identify what evidence would be required before any concrete source, test, digest, fixture, schema, or export remediation can be justified. It may map each reviewed workstream to missing authority, required source documents/artifacts, canonical serialization requirements, field contracts, and verification expectations.", None),
    (PACKAGE_CREATE_NO_CHANGE_DISPOSITION_REVIEW_FOR_CURRENT_ROOT_PRIORITY1_PASSING_STATE, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "Future execution may create a no-change disposition review for the current root Priority 1 passing state, documenting that no remediation is justified from current evidence while keeping retry and main merge blocked unless a separate retry candidate is later approved.", None),
    (PACKAGE_REQUEST_ALTERNATE_BOUNDED_DIAGNOSTIC_CAPTURE_FOR_DETACHED_RETRY_FAILURES, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "Future execution may request a separately governed bounded diagnostic capture focused on detached retry failures or errors, preserving the failed retry and avoiding full pytest, retry rerun, cache mutation, or main-merge readiness claims unless separately approved.", None),
    (PACKAGE_COMPARE_CURRENT_ROOT_PRIORITY1_PASSING_STATE_TO_DETACHED_RETRY_CONTEXT, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "Future execution may compare current-root Priority 1 passing evidence with the detached retry context at a governance level, limited to context mismatch hypotheses such as branch content, worktree state, path/CWD assumptions, evidence availability, or test isolation differences. It must not claim root cause or retry success.", None),
    (PACKAGE_CREATE_NO_CHANGE_RETRY_CANDIDATE_CRITERIA_ONLY, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "Future execution may define criteria for a possible no-change retry candidate if a later reviewed disposition concludes no remediation is justified. It must not create a retry candidate, approve retry, or run retry.", None),
    (PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_EXTERNAL_SOURCE_AUTHORITY, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "Future execution may formally hold remediation and retry blocked pending external source authority, additional artifact evidence, or operator-provided reviewed source data.", None),
    (PACKAGE_DIRECT_REMEDIATION_DESPITE_NO_SOURCE_AUTHORITY, "BLOCKED_NOT_ALLOWED", None, "The prior execution already failed closed because no safe source-authority-bound remediation change was identified."),
    (PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_TO_MATCH_CURRENT_ROOT_PASSING_STATE, "BLOCKED_NOT_ALLOWED", None, "Current-root passing Priority 1 validation does not authorize digest or expected-value updates and is not detached retry evidence."),
    (PACKAGE_REWRITE_TESTS_OR_SKIP_FAILURES_WITHOUT_SOURCE_AUTHORITY, "BLOCKED_NOT_ALLOWED", None, "Test rewrites, skips, or weakened assertions without source authority can mask evidence-binding and governance defects."),
    (PACKAGE_NEW_RETRY_BECAUSE_PRIORITY1_CURRENT_ROOT_PASSES, "BLOCKED_NOT_ALLOWED", None, "Priority 1 current-root focused validation passing is not detached retry evidence and does not create retry readiness."),
    (PACKAGE_MAIN_MERGE_BECAUSE_CURRENT_ROOT_REGRESSION_PREVIOUSLY_PASSED, "BLOCKED_NOT_ALLOWED", None, "The prior root regression is not retry evidence, and the authoritative detached retry remains failed."),
    (PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY, "BLOCKED_NOT_ALLOWED", None, "Main merge remains blocked until a future retry results review passes."),
)

FUTURE_REQUIREMENT_IDS = tuple(
    """source_failure_diagnosis_must_be_ready
source_failure_diagnosis_digest_must_be_bound
source_blocked_execution_commit_must_be_bound
source_blocked_reason_must_be_bound
source_blocked_manifest_digest_must_be_bound
primary_failure_class_must_be_bound
secondary_failure_classes_must_be_bound
source_approval_digest_must_be_bound
selected_remediation_execution_package_must_be_bound
source_operator_review_digest_must_be_bound
source_candidate_digest_must_be_bound
source_plan_results_review_digest_must_be_bound
source_targeted_plan_review_digest_must_be_bound
source_workstream_mapping_review_digest_must_be_bound
source_plan_execution_digest_must_be_bound
source_targeted_remediation_plan_digest_must_be_bound
source_workstream_mapping_digest_must_be_bound
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
observable_family_count_must_be_4
observable_evidence_items_must_be_188
workstream_count_must_be_4
safe_source_authority_bound_change_must_remain_false_until_new_evidence
retained_change_records_must_remain_false_until_remediation_execution
future_execution_must_not_infer_missing_source_authority
future_execution_must_not_treat_workstreams_as_direct_change_authority
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
runtime_and_trading_remain_not_authorized""".splitlines()
)
FUTURE_PLAN = (
    "Bind this candidate and source failure-diagnosis evidence.",
    "Bind blocked execution reason, manifest, and Priority 1 validation facts.",
    "Bind approval, review, plan, method, diagnostic, receipt, planning, detail-binding, recovery, module-grouping, and staged-inventory digests.",
    "Bind retry failure counts, Priority 1 modules, observable families, and reviewed workstreams.",
    "Review the no-source-authority failure class and confirm no retained remediation change exists.",
    "Select one future package only under separate operator approval.",
    "If source-authority enrichment is selected, create missing-authority inventory and evidence requirements without remediation.",
    "If no-change disposition is selected, create a formal review while keeping retry and main merge blocked.",
    "If alternate diagnostics are selected, define bounded diagnostic scope under separate approval.",
    "If no-change retry criteria are selected, define criteria only and do not create retry readiness.",
    "Require results review before any remediation, retry candidate, or main-merge path.",
    "Keep provider, runtime, broker, and trading authority closed.",
)
PLANNED_OUTPUT_NAMES = tuple(
    """source_authority_or_no_change_disposition_candidate_manifest
source_failure_diagnosis_binding_report
source_blocked_execution_binding_report
source_approval_binding_report
source_operator_review_and_candidate_binding_report
source_plan_results_review_binding_report
source_plan_execution_binding_report
source_method_and_diagnostic_binding_report
source_planning_detail_recovery_binding_report
retry_failure_context_report
priority1_validation_disposition_report
reviewed_workstream_authority_gap_report
proposed_package_comparison_report
recommended_source_authority_enrichment_package_report
no_change_disposition_option_report
alternate_diagnostic_option_report
no_change_retry_criteria_option_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
)
NON_GOALS = tuple(
    """do_not_select_package_now
do_not_approve_package_now
do_not_authorize_package_now
do_not_execute_source_authority_enrichment_now
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
do_not_authorize_trading""".splitlines()
)

NEXT_CHAIN = (
    "Source Authority or No-Change Disposition Candidate After Blocked Execution Operator Review v1",
    "Source Authority or No-Change Disposition Approval v1 if selected",
    "Source Authority or No-Change Disposition Execution v1 if approved",
    "Source Authority or No-Change Disposition Results Review v1",
    "Conditional remediation execution candidate, alternate diagnostic candidate, no-change retry candidate, or hold disposition only if results review supports it",
    "New Integration Branch Retry Candidate v1 only after a reviewed and approved basis exists",
    "New Integration Branch Retry Approval v1", "New Integration Branch Retry Execution v1",
    "New Integration Branch Retry Results Review v1", "Main Merge Approval only if new retry results review passes",
)
NEXT_GATES = tuple(
    """source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review
source_authority_or_no_change_disposition_approval_if_selected
source_authority_or_no_change_disposition_execution_if_approved
source_authority_or_no_change_disposition_results_review
conditional_follow_on_candidate_if_results_review_supports
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()
)
RISK_CONTROLS = tuple(
    """candidate_after_blocked_execution_does_not_select_package
candidate_after_blocked_execution_does_not_approve_package
candidate_after_blocked_execution_does_not_authorize_package
candidate_after_blocked_execution_does_not_execute_source_authority_enrichment
candidate_after_blocked_execution_does_not_execute_no_change_disposition
candidate_after_blocked_execution_does_not_execute_alternate_diagnostics
candidate_after_blocked_execution_does_not_execute_remediation
candidate_after_blocked_execution_does_not_modify_production_code
candidate_after_blocked_execution_does_not_modify_existing_tests
candidate_after_blocked_execution_does_not_update_expected_digests
candidate_after_blocked_execution_does_not_generate_patch
candidate_after_blocked_execution_does_not_apply_patch
candidate_after_blocked_execution_does_not_run_pytest
candidate_after_blocked_execution_does_not_run_full_pytest
candidate_after_blocked_execution_does_not_rerun_priority1_validation
candidate_after_blocked_execution_does_not_rerun_retry
candidate_after_blocked_execution_does_not_rerun_detached_retry
candidate_after_blocked_execution_does_not_parse_durable_receipt
candidate_after_blocked_execution_does_not_analyze_diagnostic_output
candidate_after_blocked_execution_does_not_rerun_plan_execution
candidate_after_blocked_execution_does_not_regenerate_targeted_plan
candidate_after_blocked_execution_does_not_rerun_method_execution
candidate_after_blocked_execution_does_not_rerun_controlled_recapture
candidate_after_blocked_execution_does_not_run_diagnostic_command
candidate_after_blocked_execution_does_not_read_pytest_cache
candidate_after_blocked_execution_does_not_modify_pytest_cache
candidate_after_blocked_execution_does_not_parse_terminal_logs
candidate_after_blocked_execution_does_not_parse_operator_logs
candidate_after_blocked_execution_does_not_inspect_env
candidate_after_blocked_execution_does_not_reconstruct_prior_lost_values
candidate_after_blocked_execution_does_not_reconstruct_full_streams
candidate_after_blocked_execution_does_not_classify_modules_again
candidate_after_blocked_execution_does_not_classify_full_retry_failures
candidate_after_blocked_execution_does_not_classify_full_retry_errors
candidate_after_blocked_execution_does_not_claim_failure_error_separation
candidate_after_blocked_execution_does_not_identify_authoritative_first_failure
candidate_after_blocked_execution_does_not_identify_authoritative_first_error
candidate_after_blocked_execution_does_not_claim_traceback_root_cause
candidate_after_blocked_execution_does_not_claim_root_cause
candidate_after_blocked_execution_does_not_claim_retry_success
candidate_after_blocked_execution_does_not_claim_main_merge_readiness
candidate_after_blocked_execution_does_not_create_remediation_execution
candidate_after_blocked_execution_does_not_create_remediation_execution_results_review
candidate_after_blocked_execution_does_not_create_new_retry_candidate
candidate_after_blocked_execution_does_not_create_retry_approval
candidate_after_blocked_execution_does_not_create_retry_execution
candidate_after_blocked_execution_does_not_create_retry_results_review
candidate_after_blocked_execution_does_not_create_integration_results_review
candidate_after_blocked_execution_does_not_mark_integration_successful
candidate_after_blocked_execution_does_not_generate_successful_integration_digest
candidate_after_blocked_execution_does_not_push_integration_branch
candidate_after_blocked_execution_does_not_push_main
candidate_after_blocked_execution_does_not_delete_integration_branch
candidate_after_blocked_execution_does_not_delete_worktree
candidate_after_blocked_execution_does_not_force_push
candidate_after_blocked_execution_does_not_prune_remotes
candidate_after_blocked_execution_does_not_modify_tags
candidate_after_blocked_execution_does_not_modify_staged_evidence
candidate_after_blocked_execution_does_not_regenerate_evidence
candidate_after_blocked_execution_does_not_call_providers
candidate_after_blocked_execution_does_not_acquire_market_data
candidate_after_blocked_execution_does_not_generate_dataset
candidate_after_blocked_execution_does_not_recompute_metrics
candidate_after_blocked_execution_does_not_train_models
candidate_after_blocked_execution_does_not_score_strategy
candidate_after_blocked_execution_does_not_generate_trade_recommendations
candidate_after_blocked_execution_does_not_accept_predictive_usefulness
candidate_after_blocked_execution_does_not_accept_profitability
candidate_after_blocked_execution_does_not_authorize_runtime
candidate_after_blocked_execution_does_not_authorize_broker_execution
source_authority_candidate_is_not_source_authority_enrichment_execution
no_change_disposition_candidate_is_not_no_change_disposition_execution
alternate_diagnostic_option_is_not_diagnostic_execution
blocked_remediation_execution_remains_source_evidence
failure_diagnosis_remains_source_evidence
blocked_reason_remains_authoritative_for_candidate
source_authority_gap_is_not_root_cause
passing_priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
no_change_records_means_no_remediation_success
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
preserve_meta_limitation""".splitlines()
)

TRUE_FIELDS = tuple(
    """source_authority_or_no_change_disposition_candidate_after_blocked_execution_created
source_authority_or_no_change_disposition_candidate_after_blocked_execution_ready_for_operator_review
source_failure_diagnosis_bound
source_blocked_execution_bound
source_blocked_reason_bound
source_authority_gap_reviewed
priority1_validation_disposition_reviewed
retained_change_records_absence_reviewed
detached_retry_failed_status_preserved
proposed_packages_defined
recommended_package_defined
future_requirements_defined
future_plan_defined
planned_outputs_defined
non_goals_defined
ready_for_source_authority_or_no_change_disposition_candidate_operator_review""".splitlines()
)
FALSE_FIELDS = tuple(
    """recommended_package_selected
source_authority_or_no_change_disposition_package_selected
source_authority_or_no_change_disposition_package_approved
source_authority_or_no_change_disposition_package_authorized
source_authority_or_no_change_disposition_execution_performed
source_authority_enrichment_performed
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
ready_for_source_authority_or_no_change_disposition_approval
ready_for_remediation_execution
ready_for_retry_candidate
ready_for_main_merge_approval
pytest_performed
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
cache_read_in_candidate
cache_modified_in_candidate
pytest_cache_committed
marketflow_outputs_committed
diagnostic_receipt_parsed_in_candidate
diagnostic_output_analyzed_in_candidate
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_candidate
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
new_retry_candidate_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
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
trade_recommendations_generated
safe_source_authority_bound_change_identified
retained_change_records_available
success_digests_generated""".splitlines()
)


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError(ValueError):
    """Raised when candidate evidence or a closed boundary is changed."""


def _source_bindings(source_failure_diagnosis: dict | None = None) -> dict[str, Any]:
    if source_failure_diagnosis is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(
                deepcopy(source_failure_diagnosis)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError(
                "source failure diagnosis validation failed"
            ) from exc
        if source_failure_diagnosis.get(source.DIAGNOSIS_DIGEST_KEY) != SOURCE_FAILURE_DIAGNOSIS_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError(
                "source failure diagnosis digest mismatch"
            )
    bindings = deepcopy(source.SOURCE_BINDINGS)
    bindings.update(
        {
            "source_failure_diagnosis_artifact_kind": source.ARTIFACT_KIND,
            "source_failure_diagnosis_status": source.DIAGNOSIS_STATUS,
            "source_failure_diagnosis_scope": source.DIAGNOSIS_SCOPE,
            "source_failure_diagnosis_commit": SOURCE_FAILURE_DIAGNOSIS_COMMIT,
            "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest": SOURCE_FAILURE_DIAGNOSIS_DIGEST,
        }
    )
    return bindings


SOURCE_BINDINGS = _source_bindings()
SOURCE_CORE = source.SOURCE_CORE


def _packages() -> list[dict[str, Any]]:
    packages = []
    for package_id, status, purpose, blocked_reason in PACKAGE_DEFINITIONS:
        record = {
            "package_id": package_id, "status": status, "selected": False,
            "approved": False, "authorized": False, "executed": False,
        }
        if purpose is not None:
            record["purpose"] = purpose
        if package_id == RECOMMENDED_PACKAGE:
            record["recommended_reason"] = "The blocked execution failed closed because no source-authority-bound change was identified. The safest next step is to enrich source authority before attempting remediation, retry, or main merge."
        if blocked_reason is not None:
            record["blocked_reason"] = blocked_reason
        packages.append(record)
    return packages


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [_check(f"{field}_bound", expected, candidate.get(field)) for field, expected in SOURCE_BINDINGS.items()]
    checks.extend(
        [
            _check("primary_failure_class_bound", source.PRIMARY_FAILURE_CLASS, candidate.get("primary_failure_class")),
            _check("secondary_failure_classes_bound", list(source.SECONDARY_FAILURE_CLASSES), candidate.get("secondary_failure_classes")),
            _check("selected_remediation_execution_package_bound", source.source.SELECTED_PACKAGE, candidate.get("selected_remediation_execution_package")),
            _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, candidate.get("retry_failure_context", {}).get("counts")),
            _check("priority_1_top_module_paths_bound", list(SOURCE_CORE["priority_1_target_modules"]), candidate.get("priority_1_target_modules")),
            _check("priority_1_total_612_bound", 612, candidate.get("priority_1_total_nodeids")),
            _check("top_10_total_1069_bound", 1069, candidate.get("top_10_count_sum")),
            _check("module_summary_count_29_bound", 29, candidate.get("module_summary_module_count")),
            _check("failed_or_errored_nodeids_1404_bound", 1404, candidate.get("failed_or_errored_nodeids_count")),
            _check("diagnostic_exit_code_1_bound_as_diagnostic_only", 1, candidate.get("source_exit_code")),
            _check("diagnostic_stdout_hash_bound", SOURCE_CORE["source_stdout_sha256"], candidate.get("source_stdout_sha256")),
            _check("diagnostic_stderr_hash_bound", SOURCE_CORE["source_stderr_sha256"], candidate.get("source_stderr_sha256")),
            _check("priority1_pre_change_validation_675_passed_bound", 675, candidate.get("priority1_pre_change_validation_passed_count")),
            _check("priority1_post_change_validation_675_passed_bound", 675, candidate.get("priority1_post_change_validation_passed_count")),
            _check("priority1_post_change_stdout_hash_bound", "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374", candidate.get("priority1_post_change_stdout_sha256")),
            _check("observable_family_count_4_bound", 4, candidate.get("observable_failure_family_count")),
            _check("observable_evidence_items_188_bound", 188, candidate.get("total_observable_evidence_items")),
            _check("observable_family_ids_bound", set(source.source.FAMILY_IDS), {item.get("family_id") for item in candidate.get("reviewed_observable_failure_families", [])}),
            _check("workstream_count_4_bound", 4, candidate.get("source_workstream_count")),
            _check("workstream_ids_bound", set(source.source.WORKSTREAM_IDS), {item.get("workstream_id") for item in candidate.get("reviewed_workstreams", [])}),
            _check("packages_present_12", 12, len(candidate.get("proposed_source_authority_or_no_change_disposition_packages", []))),
            _check("blocked_packages_present_6", 6, sum(item.get("status") == "BLOCKED_NOT_ALLOWED" for item in candidate.get("proposed_source_authority_or_no_change_disposition_packages", []))),
            _check("recommended_package_defined", RECOMMENDED_PACKAGE, candidate.get("recommended_source_authority_or_no_change_disposition_package")),
            _check("future_requirements_defined", len(FUTURE_REQUIREMENT_IDS), len(candidate.get("future_requirements", []))),
            _check("future_plan_defined", len(FUTURE_PLAN), len(candidate.get("future_plan", []))),
            _check("planned_outputs_defined", len(PLANNED_OUTPUT_NAMES), len(candidate.get("planned_outputs", []))),
            _check("non_goals_defined", len(NON_GOALS), len(candidate.get("non_goals", []))),
            _check("recommendation_defined", True, bool(candidate.get("recommended_package"))),
            _check("next_chain_defined", True, bool(candidate.get("next_chain"))),
            _check("next_gates_defined", True, bool(candidate.get("next_gates"))),
            _check("risk_controls_defined", True, bool(candidate.get("risk_controls"))),
            _check("no_tracked_marketflow_files", True, candidate.get("no_tracked_marketflow_files")),
            _check("no_tracked_pytest_cache_files", True, candidate.get("no_tracked_pytest_cache_files")),
        ]
    )
    checks.extend(_check(f"{field}_true", True, candidate.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, candidate.get(field)) for field in FALSE_FIELDS)
    return checks


def _summary(candidate: Mapping[str, Any]) -> dict[str, Any]:
    checks = candidate["checklist"]
    passed = sum(item["status"] == PASS for item in checks)
    failed = len(checks) - passed
    keys = (
        "source_authority_or_no_change_disposition_candidate_after_blocked_execution_created",
        "source_authority_or_no_change_disposition_candidate_after_blocked_execution_ready_for_operator_review",
        "source_failure_diagnosis_bound", "source_blocked_execution_bound", "source_authority_gap_reviewed",
        "priority1_validation_disposition_reviewed", "retained_change_records_absence_reviewed",
        "detached_retry_failed_status_preserved", "proposed_packages_defined", "recommended_package_selected",
        "source_authority_or_no_change_disposition_package_selected", "source_authority_or_no_change_disposition_package_approved",
        "source_authority_or_no_change_disposition_package_authorized", "source_authority_or_no_change_disposition_execution_performed",
        "source_authority_enrichment_performed", "no_change_disposition_performed", "alternate_diagnostic_execution_performed",
        "remediation_execution_performed", "production_code_modified", "existing_tests_modified", "expected_digests_updated",
        "patch_generated", "patch_applied", "safe_source_authority_bound_change_identified", "retained_change_records_available",
        "success_digests_generated", "priority1_pre_change_validation_passed", "priority1_pre_change_validation_passed_count",
        "priority1_post_change_validation_passed", "priority1_post_change_validation_passed_count",
        "ready_for_source_authority_or_no_change_disposition_candidate_operator_review",
        "ready_for_source_authority_or_no_change_disposition_approval", "ready_for_remediation_execution",
        "ready_for_retry_candidate", "ready_for_main_merge_approval", "new_retry_candidate_created", "new_retry_executed",
        "integration_execution_successful",
    )
    summary = {"total_checks": len(checks), "passed_checks": passed, "failed_checks": failed, "blocker_count": failed}
    summary.update({key: deepcopy(candidate[key]) for key in keys})
    summary.update(
        {
            "source_blocked_reason": source.SOURCE_BLOCKED_REASON, "primary_failure_class": source.PRIMARY_FAILURE_CLASS,
            "secondary_failure_classes": list(source.SECONDARY_FAILURE_CLASSES),
            "recommended_source_authority_or_no_change_disposition_package": RECOMMENDED_PACKAGE,
            "source_workstream_count": 4, "workstream_family_ids": list(source.source.FAMILY_IDS),
            "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
            "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
            "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
            "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
            "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
            "recommended_next_task": RECOMMENDED_NEXT_TASK, "predictive_usefulness_accepted": False,
            "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
        }
    )
    return summary


def _digest(candidate: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(candidate))
    for field in ("checklist", "summary", CANDIDATE_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(
    *, source_failure_diagnosis: dict | None = None,
) -> dict[str, Any]:
    """Build an option-only candidate; no package is selected or authorized."""

    bindings = _source_bindings(source_failure_diagnosis)
    proposed = _packages()
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION, "candidate_status": CANDIDATE_STATUS,
        "candidate_scope": CANDIDATE_SCOPE, "created_offline": True, "governance_only": True,
        "candidate_only": True, "operator_review_required": True, **bindings,
        "selected_remediation_execution_package": source.source.SELECTED_PACKAGE,
        "primary_failure_class": source.PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(source.SECONDARY_FAILURE_CLASSES),
        "retry_failure_context": deepcopy(SOURCE_CORE["retry_failure_context"]),
        "source_failure_diagnosis_summary": {
            "artifact_kind": source.ARTIFACT_KIND, "status": source.DIAGNOSIS_STATUS, "scope": source.DIAGNOSIS_SCOPE,
            "commit": SOURCE_FAILURE_DIAGNOSIS_COMMIT, "digest": SOURCE_FAILURE_DIAGNOSIS_DIGEST,
            "checklist": "247/247 PASS", "recommended_package": source.RECOMMENDED_NEXT_PACKAGE,
        },
        "source_blocked_execution_summary": {
            "commit": source.SOURCE_BLOCKED_EXECUTION_COMMIT, "artifact_kind": source.source.BLOCKED_ARTIFACT_KIND,
            "status": source.source.BLOCKED_STATUS, "scope": source.source.EXECUTION_SCOPE,
            "reason": source.SOURCE_BLOCKED_REASON, "manifest_digest": source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        },
        "source_approval_summary": {"commit": source.source.SOURCE_APPROVAL_COMMIT, "digest": source.source.SOURCE_APPROVAL_DIGEST},
        "source_operator_review_and_candidate_summary": {
            "operator_review_commit": bindings["source_remediation_execution_candidate_after_plan_results_review_operator_review_commit"],
            "operator_review_digest": bindings["source_remediation_execution_candidate_after_plan_results_review_operator_review_digest"],
            "candidate_commit": bindings["source_remediation_execution_candidate_after_plan_results_review_commit"],
            "candidate_digest": bindings["source_remediation_execution_candidate_after_plan_results_review_digest"],
        },
        "source_plan_results_review_summary": deepcopy(SOURCE_CORE["source_plan_results_review_summary"]),
        "source_plan_execution_summary": deepcopy(SOURCE_CORE["source_plan_execution_summary"]),
        "source_targeted_remediation_plan_summary": deepcopy(SOURCE_CORE["source_targeted_remediation_plan_summary"]),
        "source_workstream_mapping_summary": deepcopy(SOURCE_CORE["source_workstream_mapping_summary"]),
        "source_method_results_review_summary": deepcopy(SOURCE_CORE["source_method_results_review_summary"]),
        "source_method_execution_summary": deepcopy(SOURCE_CORE["source_method_execution_summary"]),
        "source_diagnostic_results_review_summary": deepcopy(SOURCE_CORE["source_diagnostic_results_review_summary"]),
        "source_controlled_recapture_summary": deepcopy(SOURCE_CORE["source_controlled_recapture_execution_summary"]),
        "source_durable_receipt_summary": deepcopy(SOURCE_CORE["source_durable_receipt_summary"]),
        "source_receipt_loss_history_summary": deepcopy(SOURCE_CORE["source_receipt_loss_history_summary"]),
        "source_planning_and_detail_binding_summary": deepcopy(SOURCE_CORE["source_planning_and_detail_binding_summary"]),
        "priority_1_target_modules": deepcopy(SOURCE_CORE["priority_1_target_modules"]),
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069, "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "priority1_validation_summary": {
            "pre_change_passed": True, "pre_change_passed_count": 675,
            "post_change_passed": True, "post_change_passed_count": 675, "post_change_duration_seconds": "41.88",
            "post_change_stdout_byte_count": 832, "post_change_stderr_byte_count": 0,
            "post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
            "post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "not_retry_evidence": True,
        },
        "priority1_pre_change_validation_passed": True, "priority1_pre_change_validation_passed_count": 675,
        "priority1_post_change_validation_passed": True, "priority1_post_change_validation_passed_count": 675,
        "priority1_post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
        "priority1_post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_stdout_sha256": SOURCE_CORE["source_stdout_sha256"], "source_stderr_sha256": SOURCE_CORE["source_stderr_sha256"],
        "diagnostic_capture_evidence_summary": {
            "exit_code": 1, "duration_seconds": "21.584361", "stdout_byte_count": 1231380, "stderr_byte_count": 0,
            "stdout_sha256": SOURCE_CORE["source_stdout_sha256"], "stderr_sha256": SOURCE_CORE["source_stderr_sha256"],
            "diagnostic_only": True,
        },
        "reviewed_observable_failure_families": deepcopy(SOURCE_CORE["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "reviewed_workstreams": deepcopy(SOURCE_CORE["reviewed_workstreams"]), "source_workstream_count": 4,
        "candidate_philosophy": {
            "source_authority_or_no_change_disposition_candidate_philosophy": CANDIDATE_PHILOSOPHY,
            "candidate_boundary": CANDIDATE_BOUNDARY, "candidate_goal": CANDIDATE_GOAL,
        },
        "proposed_source_authority_or_no_change_disposition_packages": proposed,
        "recommended_source_authority_or_no_change_disposition_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommended_package": {
            "package_id": RECOMMENDED_PACKAGE, "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "selected": False, "approved": False, "authorized": False, "executed": False,
            "reason": "The blocked execution and diagnosis show that the workstreams are useful planning evidence but insufficient to authorize a concrete remediation change. A source-authority enrichment plan is the safest next package because it identifies what evidence is missing before any future remediation, no-change disposition, alternate diagnostics, retry candidate, or main merge can be considered.",
        },
        "future_requirements": [{"requirement_id": item, "status": "REQUIRED_FOR_FUTURE_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION", "execution_status": "NOT_EXECUTED"} for item in FUTURE_REQUIREMENT_IDS],
        "future_plan": [{"step": index, "action": item, "status": "PLANNED_NOT_EXECUTED"} for index, item in enumerate(FUTURE_PLAN, 1)],
        "future_plan_status": "PLANNED_NOT_EXECUTED",
        "planned_outputs": [{"output_name": item, "status": "PLANNED_NOT_GENERATED"} for item in PLANNED_OUTPUT_NAMES],
        "non_goals": list(NON_GOALS), "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate)
    candidate[CANDIDATE_DIGEST_KEY] = _digest(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(
    candidate: dict,
) -> dict[str, Any]:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError
    if not isinstance(candidate, dict):
        raise error("candidate must be an object")
    for field, expected in (
        ("artifact_kind", ARTIFACT_KIND), ("schema_version", SCHEMA_VERSION),
        ("candidate_status", CANDIDATE_STATUS), ("candidate_scope", CANDIDATE_SCOPE),
        ("selected_remediation_execution_package", source.source.SELECTED_PACKAGE),
        ("primary_failure_class", source.PRIMARY_FAILURE_CLASS),
        ("secondary_failure_classes", list(source.SECONDARY_FAILURE_CLASSES)),
        ("recommended_source_authority_or_no_change_disposition_package", RECOMMENDED_PACKAGE),
    ):
        if candidate.get(field) != expected:
            raise error(f"{field} mismatch")
    for field, expected in SOURCE_BINDINGS.items():
        if candidate.get(field) != expected:
            raise error(f"{field} mismatch")
    fixed = {
        "created_offline": True, "governance_only": True, "candidate_only": True,
        "operator_review_required": True,
        "priority_1_target_modules": SOURCE_CORE["priority_1_target_modules"], "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069, "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "priority1_pre_change_validation_passed": True, "priority1_pre_change_validation_passed_count": 675,
        "priority1_post_change_validation_passed": True, "priority1_post_change_validation_passed_count": 675,
        "priority1_post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
        "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_stdout_sha256": SOURCE_CORE["source_stdout_sha256"], "source_stderr_sha256": SOURCE_CORE["source_stderr_sha256"],
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188, "source_workstream_count": 4,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    for field, expected in fixed.items():
        if candidate.get(field) != expected:
            raise error(f"{field} mismatch")
    if candidate.get("retry_failure_context", {}).get("counts") != {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}:
        raise error("retry failure counts mismatch")
    families = candidate.get("reviewed_observable_failure_families", [])
    if {item.get("family_id") for item in families} != set(source.source.FAMILY_IDS) or any(item.get("confidence") != "HIGH" for item in families):
        raise error("observable families mismatch")
    if {item.get("workstream_id") for item in candidate.get("reviewed_workstreams", [])} != set(source.source.WORKSTREAM_IDS):
        raise error("reviewed workstreams mismatch")
    packages = candidate.get("proposed_source_authority_or_no_change_disposition_packages", [])
    if packages != _packages():
        raise error("proposed packages mismatch")
    if any(item.get("selected") or item.get("approved") or item.get("authorized") or item.get("executed") for item in packages):
        raise error("candidate package selected or authorized")
    if sum(item.get("status") == "BLOCKED_NOT_ALLOWED" for item in packages) != 6:
        raise error("blocked package count mismatch")
    expected_requirements = [
        {
            "requirement_id": item,
            "status": "REQUIRED_FOR_FUTURE_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION",
            "execution_status": "NOT_EXECUTED",
        }
        for item in FUTURE_REQUIREMENT_IDS
    ]
    if candidate.get("future_requirements") != expected_requirements:
        raise error("future requirements invalid")
    expected_plan = [
        {"step": index, "action": item, "status": "PLANNED_NOT_EXECUTED"}
        for index, item in enumerate(FUTURE_PLAN, 1)
    ]
    if candidate.get("future_plan") != expected_plan or candidate.get("future_plan_status") != "PLANNED_NOT_EXECUTED":
        raise error("future plan invalid")
    expected_outputs = [
        {"output_name": item, "status": "PLANNED_NOT_GENERATED"}
        for item in PLANNED_OUTPUT_NAMES
    ]
    if candidate.get("planned_outputs") != expected_outputs:
        raise error("planned outputs invalid")
    expected_philosophy = {
        "source_authority_or_no_change_disposition_candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "candidate_goal": CANDIDATE_GOAL,
    }
    if candidate.get("non_goals") != list(NON_GOALS) or candidate.get("candidate_philosophy") != expected_philosophy:
        raise error("candidate philosophy or non-goals missing")
    expected_recommendation = {
        "package_id": RECOMMENDED_PACKAGE,
        "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "selected": False,
        "approved": False,
        "authorized": False,
        "executed": False,
        "reason": "The blocked execution and diagnosis show that the workstreams are useful planning evidence but insufficient to authorize a concrete remediation change. A source-authority enrichment plan is the safest next package because it identifies what evidence is missing before any future remediation, no-change disposition, alternate diagnostics, retry candidate, or main merge can be considered.",
    }
    if candidate.get("recommended_package") != expected_recommendation:
        raise error("recommended package mismatch")
    if candidate.get("recommendation_status") != "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED":
        raise error("recommendation status mismatch")
    if candidate.get("next_chain") != list(NEXT_CHAIN) or candidate.get("next_gates") != list(NEXT_GATES) or candidate.get("risk_controls") != list(RISK_CONTROLS):
        raise error("recommendation or governance path missing")
    for field in TRUE_FIELDS:
        if candidate.get(field) is not True:
            raise error(f"{field} must be true")
    for field in FALSE_FIELDS:
        if candidate.get(field) is not False:
            raise error(f"{field} must be false")
    checklist = _checklist(candidate)
    if candidate.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if candidate.get("summary") != _summary(candidate):
        raise error("summary mismatch")
    digest = candidate.get(CANDIDATE_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _digest(candidate):
        raise error("candidate digest missing or changed")
    return {"artifact_kind": ARTIFACT_KIND, "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE, "candidate_digest": digest, **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


MARKDOWN_SECTIONS = (
    "Source Failure Diagnosis", "Source Blocked Execution", "Blocked Reason", "Failure Classification", "Source Approval",
    "Source Operator Review and Candidate", "Source Plan Results Review", "Source Plan Execution",
    "Source Targeted Remediation Plan", "Source Workstream Mapping", "Source Method Results Review", "Source Method Execution",
    "Source Diagnostic Results Review", "Source Controlled Recapture", "Source Durable Receipt",
    "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Priority 1 Target Modules",
    "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "Candidate Philosophy", "Proposed Packages", "Recommended Package", "Future Requirements",
    "Future Plan", "Planned Outputs", "Non-Goals", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
    "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_markdown_v1(candidate: dict) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(deepcopy(candidate))
    sections = {
        "Source Failure Diagnosis": candidate["source_failure_diagnosis_summary"], "Source Blocked Execution": candidate["source_blocked_execution_summary"],
        "Blocked Reason": candidate["source_blocked_reason"], "Failure Classification": {"primary": candidate["primary_failure_class"], "secondary": candidate["secondary_failure_classes"], "candidate_digest": candidate[CANDIDATE_DIGEST_KEY]},
        "Source Approval": candidate["source_approval_summary"], "Source Operator Review and Candidate": candidate["source_operator_review_and_candidate_summary"],
        "Source Plan Results Review": candidate["source_plan_results_review_summary"], "Source Plan Execution": candidate["source_plan_execution_summary"],
        "Source Targeted Remediation Plan": candidate["source_targeted_remediation_plan_summary"], "Source Workstream Mapping": candidate["source_workstream_mapping_summary"],
        "Source Method Results Review": candidate["source_method_results_review_summary"], "Source Method Execution": candidate["source_method_execution_summary"],
        "Source Diagnostic Results Review": candidate["source_diagnostic_results_review_summary"], "Source Controlled Recapture": candidate["source_controlled_recapture_summary"],
        "Source Durable Receipt": candidate["source_durable_receipt_summary"], "Source Planning and Detail Binding Evidence": candidate["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": candidate["retry_failure_context"], "Priority 1 Target Modules": candidate["priority_1_target_modules"],
        "Priority 1 Validation Summary": candidate["priority1_validation_summary"], "Diagnostic Capture Evidence Summary": candidate["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": candidate["reviewed_observable_failure_families"], "Reviewed Workstreams": candidate["reviewed_workstreams"],
        "Candidate Philosophy": candidate["candidate_philosophy"], "Proposed Packages": candidate["proposed_source_authority_or_no_change_disposition_packages"],
        "Recommended Package": candidate["recommended_package"], "Future Requirements": candidate["future_requirements"],
        "Future Plan": candidate["future_plan"], "Planned Outputs": candidate["planned_outputs"], "Non-Goals": candidate["non_goals"],
        "Next Chain": candidate["next_chain"], "Next Gates": candidate["next_gates"], "Risk Controls": candidate["risk_controls"],
        "Authority Boundaries": {"operator_review_required": True, "package_selected": False, "retry_ready": False, "runtime_use": candidate["runtime_use"]},
        "Checklist Summary": candidate["summary"], "Guardrails": list(FALSE_FIELDS),
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Candidate After Blocked Execution v1", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", f"```text\n{sections[title]!r}\n```", ""))
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(output_dir: str | Path, *, source_failure_diagnosis: dict | None = None) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError("protected output directory")
    candidate = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(source_failure_diagnosis=source_failure_diagnosis)
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError("output exists")
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_markdown_v1(candidate), encoding="utf-8")
    return candidate


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE
NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED = source.PRIMARY_FAILURE_CLASS
REVIEWED_WORKSTREAMS_ARE_PLANNING_EVIDENCE_NOT_CHANGE_AUTHORITY = source.SECONDARY_FAILURE_CLASSES[0]
PRIORITY_1_FOCUSED_VALIDATION_ALREADY_PASSING_IN_CURRENT_ROOT_CONTEXT = source.SECONDARY_FAILURE_CLASSES[1]
NO_RETAINED_CHANGE_RECORDS_AVAILABLE_FOR_REMEDIATION_SUCCESS = source.SECONDARY_FAILURE_CLASSES[2]
DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED = source.SECONDARY_FAILURE_CLASSES[3]
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_DIGEST_KEY = CANDIDATE_DIGEST_KEY
