"""Review the committed plan-only retry-failure remediation execution artifact.

This module is deliberately evidence-only.  It never invokes the source execution,
opens the durable receipt, reads pytest cache data, or performs remediation/tests.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_service
    as source,
)


ARTIFACT_KIND_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_V1"
ARTIFACT_KIND_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_BLOCKED_AFTER_METHOD_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1"
REVIEW_STATUS_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_READY"
REVIEW_STATUS_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_BLOCKED_AFTER_METHOD_RESULTS_REVIEW_SOURCE_PLAN_OR_WORKSTREAM_EVIDENCE_UNAVAILABLE_OR_BOUNDARY_FAILURE"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_ONLY_NOT_PLAN_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"

SOURCE_PLAN_EXECUTION_COMMIT = "57ce0d2760d2ae6de2a16bade80291f4dbe05305"
SOURCE_EXECUTION_DIGEST = "a7cb542d77ddcda7e3bad66080a8ffc4b435874c4985e4677a274106b329802c"
SOURCE_TARGETED_PLAN_DIGEST = "2d7ffac9fc3cc04f0bfb823ef81f254005adaee7a600ccb6e3444b7f3dec91db"
SOURCE_WORKSTREAM_MAPPING_DIGEST = "275b1e5a16e7bffc8bd323615b764fff7e88070d88198177cc11c64530e948e0"
SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST = "7f0b973fb6bbc6286e7e4bda208c48a8da4c8a56f8f4809b0ced315e129a77ed"
SELECTED_PACKAGE = "PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY"

RESULTS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_digest"
TARGETED_PLAN_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_remediation_plan_review_digest"
WORKSTREAM_MAPPING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_workstream_mapping_review_digest"
RESULTS_REVIEW_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_blocked_manifest_digest"

SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1"
NOT_ACCEPTED, NOT_AUTHORIZED, PASS, FAIL, BLOCKER = "not accepted", "NOT_AUTHORIZED", "PASS", "FAIL", "BLOCKER"

SOURCE_BINDINGS = {
    key: deepcopy(value)
    for key, value in source.SOURCE_BINDINGS.items()
    if key not in {"source_execution_artifact_kind", "source_execution_status", "source_execution_scope"}
}
PRIORITY_1_MODULES = deepcopy(source.PRIORITY_1_MODULES)
FAMILY_IDS = list(source.FAMILY_IDS)

TRUE_FIELDS = """remediation_plan_or_execution_results_review_after_method_results_review_created
remediation_plan_or_execution_results_review_after_method_results_review_ready
source_plan_execution_reviewed
source_plan_execution_digest_verified
source_targeted_remediation_plan_digest_verified
source_workstream_mapping_digest_verified
source_plan_execution_manifest_digest_verified
source_approval_reviewed
source_method_results_review_reviewed
source_method_execution_reviewed
source_targeted_remediation_plan_reviewed
source_workstream_mapping_reviewed
reviewed_observable_failure_families_reviewed
workstreams_reviewed
verification_evidence_requirements_reviewed
future_approval_boundaries_reviewed
unsupported_claims_boundary_reviewed
ready_for_remediation_execution_candidate_after_plan_results_review""".splitlines()

FALSE_FIELDS = """ready_for_remediation_execution
ready_for_retry_candidate
ready_for_main_merge_approval
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_review
remediation_plan_or_execution_performed_in_review
remediation_plan_generated_in_review
remediation_execution_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
direct_code_remediation_recommended
method_execution_rerun_performed
diagnostic_receipt_parsed_in_review
diagnostic_output_analyzed_in_review
failure_family_classification_performed_in_review
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
targeted_pytest_performed_in_review
full_pytest_performed
retry_rerun_performed
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
remediation_execution_candidate_created
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
provider_requests_made_in_review
market_data_acquisition_performed_in_review
dataset_generation_performed_in_review
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()

SOURCE_SUCCESS_TRUE_FIELDS = list(source.SUCCESS_TRUE_FIELDS)
SOURCE_FALSE_FIELDS = list(source.COMMON_FALSE_FIELDS)

REVIEW_FINDINGS = {
    "finding_1": "The source plan execution completed successfully and generated a targeted remediation plan.",
    "finding_2": "The source plan execution used the approved plan-first package and remained plan-generation-only.",
    "finding_3": "The source plan execution generated exactly four workstreams mapped to the four reviewed observable failure families.",
    "finding_4": "The four workstreams are assertion_value_mismatch_workstream, digest_hash_boundary_workstream, fixture_isolation_determinism_workstream, and schema_field_contract_workstream.",
    "finding_5": "Each workstream preserves 47 reviewed observable evidence items and HIGH source confidence.",
    "finding_6": "The targeted remediation plan uses reviewed method results and observable failure-family evidence only.",
    "finding_7": "The Priority 1 modules are candidate planning areas only, not root cause, failure/error separation, or direct-edit authority.",
    "finding_8": "Verification evidence requirements cover provenance, mismatches, serialization, digests, isolation, paths, schema contracts, exports, and compatibility.",
    "finding_9": "Future approval boundaries precede remediation, code/test/digest changes, pytest, retry, and main merge.",
    "finding_10": "The source plan execution did not parse receipt content, analyze output, rerun methods or recapture, run pytest, rerun retry, read cache, parse logs, or inspect environment files.",
    "finding_11": "The source plan execution did not execute remediation, modify production code or existing tests, update expected digests, regenerate evidence, or create retry readiness.",
    "finding_12": "The plan does not claim root cause, authoritative first failures/errors, failure/error separation, retry success, or main-merge readiness.",
    "finding_13": "The authoritative retry remains failed with 24,877 passed, 1,292 failed, 112 errors, and 7 skipped.",
    "finding_14": "The source diagnostic capture remains diagnostic evidence only and is not retry evidence.",
    "finding_15": "This review performed no plan rerun, plan regeneration, receipt parsing, output analysis, pytest, remediation, retry creation, protected-branch push, or evidence modification.",
    "finding_16": "The reviewed plan supports only a separately invoked remediation execution candidate after plan results review, subject to operator review and approval.",
}

OUTPUT_IDS = """remediation_plan_or_execution_results_review_after_method_results_review_manifest
source_plan_execution_digest_review
targeted_remediation_plan_digest_review
workstream_mapping_digest_review
source_plan_execution_manifest_digest_review
source_approval_binding_review
source_candidate_operator_review_binding_review
source_method_results_review_binding_review
source_method_execution_binding_review
reviewed_failure_family_input_review
targeted_remediation_plan_results_review
workstream_mapping_results_review
assertion_value_mismatch_workstream_review
digest_hash_boundary_workstream_review
fixture_isolation_determinism_workstream_review
schema_field_contract_workstream_review
verification_evidence_requirements_review
future_approval_boundaries_review
unsupported_claims_boundary_review
remediation_execution_candidate_readiness_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
REVIEW_OUTPUTS = [{"output_id": item, "status": "GENERATED_REMEDIATION_PLAN_RESULTS_REVIEW_ONLY"} for item in OUTPUT_IDS]

SUCCESS_NEXT_CHAIN = [
    "Remediation Execution Candidate After Plan Results Review v1.",
    "Remediation Execution Candidate Operator Review v1.",
    "Remediation Execution Approval v1, if selected.",
    "Remediation Execution v1, if approved.",
    "Remediation Execution Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation results review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Remediation Plan or Execution Results Review After Method Results Review Failure Diagnosis v1.",
    "Alternate plan review or source candidate, if needed.",
    "No remediation execution, retry, or main merge.",
]
NEXT_GATES = """remediation_execution_candidate_after_plan_results_review
remediation_execution_candidate_operator_review
remediation_execution_approval_if_selected
remediation_execution_if_approved
remediation_execution_results_review
new_integration_branch_retry_candidate_after_remediation_results_review
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes
remediation_plan_or_execution_results_review_after_method_results_review_failure_diagnosis
alternate_plan_review_or_source_candidate_if_needed
remediation_execution_blocked_until_plan_results_review_passes
new_retry_blocked_until_remediation_results_review_passes
main_merge_blocked_until_new_retry_results_review_passes""".splitlines()

RISK_CONTROLS = """plan_results_review_after_method_results_review_does_not_rerun_plan_execution
plan_results_review_after_method_results_review_does_not_regenerate_targeted_plan
plan_results_review_after_method_results_review_does_not_execute_remediation
plan_results_review_after_method_results_review_does_not_modify_production_code
plan_results_review_after_method_results_review_does_not_modify_existing_tests
plan_results_review_after_method_results_review_does_not_update_expected_digests
plan_results_review_after_method_results_review_does_not_parse_durable_receipt
plan_results_review_after_method_results_review_does_not_analyze_diagnostic_output
plan_results_review_after_method_results_review_does_not_rerun_method_execution
plan_results_review_after_method_results_review_does_not_rerun_controlled_recapture
plan_results_review_after_method_results_review_does_not_run_diagnostic_command
plan_results_review_after_method_results_review_does_not_run_targeted_pytest
plan_results_review_after_method_results_review_does_not_run_full_pytest
plan_results_review_after_method_results_review_does_not_rerun_retry
plan_results_review_after_method_results_review_does_not_read_pytest_cache
plan_results_review_after_method_results_review_does_not_modify_pytest_cache
plan_results_review_after_method_results_review_does_not_parse_terminal_logs
plan_results_review_after_method_results_review_does_not_parse_operator_logs
plan_results_review_after_method_results_review_does_not_inspect_env
plan_results_review_after_method_results_review_does_not_reconstruct_prior_lost_values
plan_results_review_after_method_results_review_does_not_reconstruct_full_stdout
plan_results_review_after_method_results_review_does_not_reconstruct_full_stderr
plan_results_review_after_method_results_review_does_not_classify_modules_again
plan_results_review_after_method_results_review_does_not_classify_full_retry_failures
plan_results_review_after_method_results_review_does_not_classify_full_retry_errors
plan_results_review_after_method_results_review_does_not_claim_failure_error_separation
plan_results_review_after_method_results_review_does_not_identify_authoritative_first_failure
plan_results_review_after_method_results_review_does_not_identify_authoritative_first_error
plan_results_review_after_method_results_review_does_not_claim_traceback_root_cause
plan_results_review_after_method_results_review_does_not_claim_root_cause
plan_results_review_after_method_results_review_does_not_recommend_direct_code_remediation
plan_results_review_after_method_results_review_does_not_create_remediation_execution_candidate
plan_results_review_after_method_results_review_does_not_create_remediation_approval
plan_results_review_after_method_results_review_does_not_create_remediation_execution
plan_results_review_after_method_results_review_does_not_create_remediation_execution_results_review
plan_results_review_after_method_results_review_does_not_create_new_retry_candidate
plan_results_review_after_method_results_review_does_not_create_retry_results_review
plan_results_review_after_method_results_review_does_not_create_integration_results_review
plan_results_review_after_method_results_review_does_not_mark_integration_successful
plan_results_review_after_method_results_review_does_not_generate_successful_integration_digest
plan_results_review_after_method_results_review_does_not_treat_plan_as_remediation_execution
plan_results_review_after_method_results_review_does_not_treat_plan_as_retry_success
plan_results_review_after_method_results_review_does_not_treat_family_classification_as_root_cause
plan_results_review_after_method_results_review_does_not_push_integration_branch
plan_results_review_after_method_results_review_does_not_push_main
plan_results_review_after_method_results_review_does_not_delete_integration_branch
plan_results_review_after_method_results_review_does_not_delete_worktree
plan_results_review_after_method_results_review_does_not_force_push
plan_results_review_after_method_results_review_does_not_prune_remotes
plan_results_review_after_method_results_review_does_not_modify_tags
plan_results_review_after_method_results_review_does_not_modify_staged_evidence
plan_results_review_after_method_results_review_does_not_regenerate_evidence
plan_results_review_after_method_results_review_does_not_call_providers
plan_results_review_after_method_results_review_does_not_acquire_market_data
plan_results_review_after_method_results_review_does_not_regenerate_dataset
plan_results_review_after_method_results_review_does_not_recompute_metrics
plan_results_review_after_method_results_review_does_not_train_models
plan_results_review_after_method_results_review_does_not_score_strategy
plan_results_review_after_method_results_review_does_not_generate_trade_recommendations
plan_results_review_after_method_results_review_does_not_accept_predictive_usefulness
plan_results_review_after_method_results_review_does_not_accept_profitability
plan_results_review_after_method_results_review_does_not_authorize_runtime
plan_results_review_after_method_results_review_does_not_authorize_broker_execution
targeted_remediation_plan_is_plan_only
targeted_remediation_plan_is_not_root_cause
targeted_remediation_plan_is_not_direct_remediation
targeted_remediation_plan_is_not_retry_success
workstream_mapping_is_planning_only
verification_evidence_requirements_are_not_code_change_approval
future_approval_boundaries_preserve_change_control
method_results_review_remains_source_evidence
remediation_plan_execution_remains_source_evidence
remediation_plan_approval_remains_source_evidence
remediation_plan_operator_review_remains_source_evidence
remediation_plan_candidate_remains_source_evidence
observable_failure_family_classification_is_method_planning_only
failure_family_classification_is_not_root_cause
failure_family_classification_is_not_direct_remediation
failure_family_classification_is_not_retry_success
diagnostic_capture_results_review_remains_source_evidence
durable_receipt_is_diagnostic_evidence_only
controlled_recapture_is_not_retry_success
priority_1_selection_is_not_root_cause
module_concentration_is_not_failure_error_separation
prior_blocked_diagnostic_capture_execution_remains_historically_blocked
previous_method_execution_remains_source_evidence
previous_remediation_or_method_approval_remains_source_evidence
previous_receipt_recovery_or_recapture_results_review_remains_source_evidence
previous_planning_results_review_remains_valid
previous_detail_binding_results_review_remains_valid
previous_materialization_results_review_remains_valid
previous_source_recovery_results_review_remains_valid
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_remediation_execution_candidate_required_after_plan_results_review
separate_remediation_execution_approval_required_before_code_or_test_change
separate_results_review_required_after_remediation_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines()

REQUIRED_CHECK_IDS = """source_plan_execution_commit_bound
source_plan_execution_digest_bound
source_targeted_remediation_plan_digest_bound
source_workstream_mapping_digest_bound
source_plan_execution_manifest_digest_bound
source_selected_package_bound
source_approval_commit_bound
source_approval_digest_bound
source_operator_review_digest_bound
source_candidate_digest_bound
source_method_results_review_commit_bound
source_method_results_review_digest_bound
source_failure_family_classification_review_digest_bound
source_bounded_excerpt_analysis_review_digest_bound
source_results_review_manifest_digest_bound
source_method_execution_commit_bound
source_method_execution_digest_bound
source_failure_family_classification_digest_bound
source_bounded_excerpt_analysis_digest_bound
source_method_execution_manifest_digest_bound
source_remediation_or_method_approval_digest_bound
source_remediation_or_method_operator_review_digest_bound
source_remediation_or_method_candidate_digest_bound
source_diagnostic_results_review_digest_bound
source_payload_review_digest_bound
source_durable_receipt_review_digest_bound
source_diagnostic_results_review_manifest_digest_bound
source_controlled_recapture_execution_commit_bound
source_controlled_recapture_execution_digest_bound
source_controlled_recapture_payload_digest_bound
source_controlled_recapture_receipt_digest_bound
source_controlled_recapture_manifest_digest_bound
source_durable_receipt_path_bound
source_receipt_recovery_approval_digest_bound
source_receipt_recovery_candidate_operator_review_digest_bound
source_receipt_recovery_candidate_digest_bound
source_failure_diagnosis_digest_bound
source_prior_execution_digest_bound
source_blocked_manifest_digest_bound
source_blocked_reason_bound
source_primary_failure_class_bound
source_secondary_failure_class_bound
source_targeted_diagnostic_approval_digest_bound
source_targeted_diagnostic_candidate_operator_review_digest_bound
source_targeted_diagnostic_candidate_digest_bound
source_planning_results_review_digest_bound
source_prioritized_planning_review_digest_bound
source_planning_execution_digest_bound
source_prioritized_planning_digest_bound
source_detail_binding_results_review_digest_bound
source_complete_29_row_binding_digest_bound
source_materialized_payload_digest_bound
source_recovery_results_review_digest_bound
source_recovery_detail_digest_bound
source_after_v2_approval_digest_bound
source_module_grouping_digest_bound
retry_execution_commit_bound
retry_failure_counts_bound
priority_1_top_module_paths_bound
priority_1_total_612_bound
top_10_total_1069_bound
module_summary_count_29_bound
failed_or_errored_nodeids_1404_bound
exit_code_1_bound_as_diagnostic_only
stdout_hash_bound
stderr_hash_bound
stdout_byte_count_1231380_bound
stderr_byte_count_0_bound
stdout_excerpt_truncated_true_bound
stderr_excerpt_truncated_false_bound
redaction_checked_true_bound
observable_family_count_4_bound
observable_evidence_items_188_bound
assertion_or_value_mismatch_family_bound
digest_or_hash_mismatch_family_bound
fixture_or_test_isolation_issue_family_bound
missing_or_unexpected_field_family_bound
family_confidence_high_bound
additional_diagnostic_capture_false_bound
direct_remediation_ready_false_bound
retry_ready_false_bound
main_merge_ready_false_bound
source_plan_execution_status_success_bound
source_plan_execution_scope_bound
source_plan_execution_performed_true
source_targeted_remediation_plan_generated_true
source_remediation_plan_generated_true
source_workstream_count_4_bound
assertion_value_mismatch_workstream_reviewed
digest_hash_boundary_workstream_reviewed
fixture_isolation_determinism_workstream_reviewed
schema_field_contract_workstream_reviewed
workstreams_have_required_fields
workstreams_include_candidate_modules
workstreams_include_planned_actions
workstreams_include_verification_evidence
workstreams_include_future_approval_boundaries
workstreams_include_prohibited_actions
workstreams_preserve_no_root_cause
workstreams_preserve_no_direct_remediation
workstreams_preserve_no_remediation_execution_authority
workstreams_preserve_no_retry_readiness
workstreams_preserve_no_main_merge_readiness
verification_evidence_requirements_reviewed
future_approval_boundaries_reviewed
review_created_true
review_ready_true
source_plan_execution_reviewed_true
source_plan_execution_digest_verified_true
targeted_remediation_plan_digest_verified_true
workstream_mapping_digest_verified_true
manifest_digest_verified_true
source_targeted_remediation_plan_reviewed_true
source_workstream_mapping_reviewed_true
ready_for_remediation_execution_candidate_after_plan_results_review_true
ready_for_remediation_execution_false
ready_for_retry_candidate_false
ready_for_main_merge_approval_false
plan_execution_rerun_false
targeted_remediation_plan_regenerated_in_review_false
remediation_plan_or_execution_performed_in_review_false
remediation_plan_generated_in_review_false
remediation_execution_false
code_remediation_false
evidence_remediation_false
production_code_modified_false
existing_tests_modified_false
expected_digests_updated_false
direct_code_remediation_recommended_false
method_execution_rerun_false
diagnostic_receipt_parsed_false
diagnostic_output_analyzed_false
failure_family_classification_performed_in_review_false
controlled_recapture_rerun_false
diagnostic_command_rerun_false
targeted_pytest_in_review_false
full_pytest_false
retry_rerun_false
cache_read_false
cache_modified_false
pytest_cache_committed_false
marketflow_outputs_committed_false
terminal_logs_parsed_false
operator_logs_parsed_false
env_inspection_false
prior_lost_values_reconstructed_false
prior_lost_values_inferred_false
full_stdout_reconstructed_false
full_stderr_reconstructed_false
failure_modules_classified_false
error_modules_classified_false
failure_error_separation_claimed_false
first_failure_identified_false
first_error_identified_false
first_order_claim_made_false
traceback_root_cause_claimed_false
root_cause_claimed_false
retry_success_claimed_false
main_merge_readiness_claimed_false
remediation_execution_candidate_created_false
new_retry_candidate_created_false
new_retry_executed_false
new_retry_results_review_created_false
main_merge_approval_created_false
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
review_findings_defined
review_outputs_generated_if_success
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines()


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError(ValueError):
    """Raised when committed plan evidence or a review-only boundary drifts."""


def _expected_source_workstreams() -> list[dict[str, Any]]:
    modules = [item["module_path"] for item in PRIORITY_1_MODULES]
    return [
        {
            **deepcopy(spec),
            "source_family_confidence": "HIGH",
            "source_observable_evidence_count": 47,
            "planning_basis": "REVIEWED_BOUNDED_PATTERN_METHOD_EVIDENCE_ONLY",
            "candidate_priority_1_modules": modules,
            "candidate_scope_statement": source.CANDIDATE_SCOPE_STATEMENT,
            "future_approval_required_before_change": True,
            "root_cause_claimed": False,
            "direct_code_remediation_recommended": False,
            "remediation_execution_authorized": False,
            "retry_readiness_created": False,
            "main_merge_readiness_created": False,
        }
        for spec in source.WORKSTREAM_SPECS
    ]


def _source_plan_summary() -> dict[str, Any]:
    return {
        "targeted_remediation_plan_generated": True,
        "workstream_count": 4,
        "source_family_count": 4,
        "source_total_observable_evidence_items": 188,
        "priority_1_target_module_count": 5,
        "priority_1_total_nodeids": 612,
        "direct_remediation_ready": False,
        "remediation_execution_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "additional_diagnostic_capture_may_be_needed": False,
        "code_change_approved": False,
        "test_change_approved": False,
        "digest_update_approved": False,
        "pytest_execution_approved": False,
    }


def _source_mapping() -> list[dict[str, Any]]:
    return [
        {
            "workstream_id": item["workstream_id"],
            "source_family_id": item["source_family_id"],
            "source_observable_evidence_count": 47,
            "source_family_confidence": "HIGH",
        }
        for item in _expected_source_workstreams()
    ]


def _committed_source_execution() -> dict[str, Any]:
    """Return a constants-only view; this is not the source execution builder."""

    return {
        "artifact_kind": source.ARTIFACT_KIND_SUCCESS,
        "execution_status": source.EXECUTION_STATUS_SUCCESS,
        "execution_scope": source.EXECUTION_SCOPE,
        "selected_remediation_plan_or_execution_package": SELECTED_PACKAGE,
        "source_plan_execution_commit": SOURCE_PLAN_EXECUTION_COMMIT,
        source.EXECUTION_DIGEST_KEY: SOURCE_EXECUTION_DIGEST,
        source.TARGETED_PLAN_DIGEST_KEY: SOURCE_TARGETED_PLAN_DIGEST,
        source.WORKSTREAM_MAPPING_DIGEST_KEY: SOURCE_WORKSTREAM_MAPPING_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_commit": source.SOURCE_CORE["retry_execution_commit"],
        "retry_failure_context": deepcopy(source.SOURCE_CORE["retry_failure_context"]),
        "priority_1_target_modules": deepcopy(PRIORITY_1_MODULES),
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1,
        "source_duration_seconds": source.SOURCE_CORE["source_duration_seconds"],
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": source.SOURCE_CORE["source_stdout_sha256"],
        "source_stderr_sha256": source.SOURCE_CORE["source_stderr_sha256"],
        "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "reviewed_observable_failure_families": deepcopy(source.SOURCE_CORE["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "remediation_execution_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "workstreams": _expected_source_workstreams(),
        "workstream_count": 4,
        "targeted_remediation_plan": {"committed_plan_present": True},
        "targeted_remediation_plan_summary": _source_plan_summary(),
        "workstream_mapping_summary": _source_mapping(),
        "verification_evidence_requirements": list(source.VERIFICATION_EVIDENCE_REQUIREMENTS),
        "future_approval_boundaries": deepcopy(source.FUTURE_APPROVAL_BOUNDARIES),
        "unsupported_claims_boundary": deepcopy(source.UNSUPPORTED_CLAIMS_BOUNDARY),
        **{field: True for field in SOURCE_SUCCESS_TRUE_FIELDS},
        **{field: False for field in SOURCE_FALSE_FIELDS},
    }


def _validate_source_execution(execution: Mapping[str, Any]) -> None:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError
    if not isinstance(execution, Mapping):
        raise error("source execution must be an object")
    expected = _committed_source_execution()
    scalar_fields = [
        "artifact_kind", "execution_status", "execution_scope", "selected_remediation_plan_or_execution_package",
        "source_plan_execution_commit", source.EXECUTION_DIGEST_KEY, source.TARGETED_PLAN_DIGEST_KEY,
        source.WORKSTREAM_MAPPING_DIGEST_KEY, source.MANIFEST_DIGEST_KEY, "retry_execution_commit",
        "retry_failure_context", "priority_1_target_modules", "priority_1_total_nodeids", "top_10_count_sum",
        "module_summary_module_count", "failed_or_errored_nodeids_count", "source_exit_code",
        "source_duration_seconds", "source_stdout_byte_count", "source_stderr_byte_count",
        "source_combined_output_byte_count", "source_stdout_sha256", "source_stderr_sha256",
        "source_stdout_excerpt_truncated", "source_stderr_excerpt_truncated", "source_redaction_checked",
        "reviewed_observable_failure_families", "observable_failure_family_count", "total_observable_evidence_items",
        "highest_confidence_family_ids", "additional_diagnostic_capture_may_be_needed", "direct_remediation_ready",
        "remediation_execution_ready", "retry_ready", "main_merge_ready", "workstreams", "workstream_count",
        "targeted_remediation_plan_summary", "workstream_mapping_summary", "verification_evidence_requirements",
        "future_approval_boundaries", "unsupported_claims_boundary",
    ]
    scalar_fields.extend(SOURCE_BINDINGS)
    scalar_fields.extend(SOURCE_SUCCESS_TRUE_FIELDS)
    scalar_fields.extend(SOURCE_FALSE_FIELDS)
    for field in dict.fromkeys(scalar_fields):
        if execution.get(field) != expected[field]:
            raise error(f"source {field} mismatch")
    plan = execution.get("targeted_remediation_plan")
    if not isinstance(plan, Mapping):
        raise error("source targeted remediation plan missing")
    if execution is not expected and plan != {"committed_plan_present": True}:
        if plan.get("plan_status") != "GENERATED_PLAN_ONLY_NOT_REMEDIATION":
            raise error("source targeted remediation plan status mismatch")
        for field in ("root_cause_claimed", "direct_code_remediation_recommended", "remediation_execution_authorized", "retry_readiness_created", "main_merge_readiness_created"):
            if plan.get(field) is not False:
                raise error(f"source targeted remediation plan {field} mismatch")


def _workstream_reviews() -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(item),
            "workstream_review_status": "VERIFIED_PLAN_ONLY",
            "required_fields_present": all(
                key in item
                for key in (
                    "planning_basis", "candidate_priority_1_modules", "planned_actions",
                    "verification_evidence_required", "future_approval_required_before_change",
                    "prohibited_actions",
                )
            ),
            "reviewed": True,
        }
        for item in _expected_source_workstreams()
    ]


def _source_summaries() -> dict[str, Any]:
    b = SOURCE_BINDINGS
    return {
        "source_plan_execution_summary": {
            "artifact_kind": source.ARTIFACT_KIND_SUCCESS,
            "execution_status": source.EXECUTION_STATUS_SUCCESS,
            "execution_scope": source.EXECUTION_SCOPE,
            "execution_commit": SOURCE_PLAN_EXECUTION_COMMIT,
            "execution_digest": SOURCE_EXECUTION_DIGEST,
            "targeted_plan_digest": SOURCE_TARGETED_PLAN_DIGEST,
            "workstream_mapping_digest": SOURCE_WORKSTREAM_MAPPING_DIGEST,
            "manifest_digest": SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST,
            "approved_plan_first_package_executed": True,
            "targeted_remediation_plan_generated": True,
            "remediation_execution_performed": False,
        },
        "source_approval_summary": {
            "commit": b["source_remediation_plan_or_execution_approval_after_method_results_review_commit"],
            "digest": b["source_remediation_plan_or_execution_approval_after_method_results_review_digest"],
        },
        "source_operator_review_and_candidate_summary": {
            "operator_review_digest": b["source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest"],
            "candidate_digest": b["source_remediation_plan_or_execution_candidate_after_method_results_review_digest"],
        },
        "source_method_results_review_summary": {
            "commit": b["source_method_results_review_commit"],
            "results_review_digest": b["source_remediation_or_method_results_review_after_diagnostic_capture_digest"],
            "classification_review_digest": b["source_failure_family_classification_review_digest"],
            "bounded_excerpt_review_digest": b["source_bounded_excerpt_analysis_review_digest"],
            "manifest_digest": b["source_results_review_manifest_digest"],
        },
        "source_method_execution_summary": {
            "commit": b["source_method_execution_commit"],
            "execution_digest": b["source_remediation_or_method_execution_after_diagnostic_capture_digest"],
            "classification_digest": b["source_failure_family_classification_digest"],
            "bounded_excerpt_digest": b["source_bounded_excerpt_analysis_digest"],
            "manifest_digest": b["source_method_execution_manifest_digest"],
        },
        "source_failure_family_classification_summary": {
            "family_count": 4, "observable_evidence_items": 188, "family_ids": list(FAMILY_IDS),
            "confidence": "HIGH", "root_cause_claimed": False,
        },
        "source_diagnostic_results_review_summary": {
            "results_review_digest": b["source_receipt_recovery_or_recapture_results_review_digest"],
            "payload_review_digest": b["source_receipt_recovery_or_recapture_payload_review_digest"],
            "durable_receipt_review_digest": b["source_receipt_recovery_or_recapture_durable_receipt_review_digest"],
            "manifest_digest": b["source_receipt_recovery_or_recapture_results_review_manifest_digest"],
        },
        "source_controlled_recapture_execution_summary": {
            "commit": b["source_receipt_recovery_or_recapture_execution_commit"],
            "execution_digest": b["source_receipt_recovery_or_recapture_execution_digest"],
            "payload_digest": b["source_receipt_recovery_or_recapture_payload_digest"],
            "receipt_digest": b["source_receipt_recovery_or_recapture_receipt_digest"],
            "manifest_digest": b["source_receipt_recovery_or_recapture_digest_manifest_digest"],
        },
        "source_durable_receipt_summary": {
            "path": b["source_durable_receipt_path"],
            "digest": b["source_receipt_recovery_or_recapture_receipt_digest"],
            "path_bound": True, "content_parsed_in_review": False,
        },
        "source_receipt_loss_history_summary": {
            "failure_diagnosis_digest": b["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
            "prior_execution_digest": b["source_targeted_diagnostic_output_capture_execution_digest"],
            "blocked_manifest_digest": b["source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest"],
            "blocked_reason": b["source_targeted_diagnostic_output_capture_execution_blocked_reason"],
            "primary_failure_class": b["source_primary_failure_class"],
            "secondary_failure_class": b["source_secondary_failure_class"],
        },
        "source_planning_and_detail_binding_summary": {
            "planning_results_review_digest": b["source_planning_results_review_digest"],
            "prioritized_planning_review_digest": b["source_prioritized_planning_review_digest"],
            "planning_execution_digest": b["source_planning_execution_digest"],
            "prioritized_planning_digest": b["source_prioritized_planning_digest"],
            "detail_binding_results_review_digest": b["source_detail_binding_results_review_digest"],
            "complete_29_row_binding_digest": b["source_complete_29_row_binding_digest"],
            "materialized_payload_digest": b["source_materialized_payload_digest"],
            "recovery_results_review_digest": b["source_recovery_results_review_digest"],
            "recovery_detail_digest": b["source_recovery_detail_digest"],
            "after_v2_approval_digest": b["source_after_v2_approval_digest"],
            "module_grouping_digest": b["source_module_grouping_digest"],
            "staged_inventory_digest": b["source_staged_inventory_digest"],
        },
    }


def _base() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "review_scope": REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "results_review_only": True,
        "source_execution_artifact_kind": source.ARTIFACT_KIND_SUCCESS,
        "source_execution_status": source.EXECUTION_STATUS_SUCCESS,
        "source_execution_scope": source.EXECUTION_SCOPE,
        "source_plan_execution_commit": SOURCE_PLAN_EXECUTION_COMMIT,
        "source_remediation_plan_or_execution_after_method_results_review_digest": SOURCE_EXECUTION_DIGEST,
        "source_targeted_remediation_plan_digest": SOURCE_TARGETED_PLAN_DIGEST,
        "source_workstream_mapping_digest": SOURCE_WORKSTREAM_MAPPING_DIGEST,
        "source_plan_execution_manifest_digest": SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST,
        "selected_remediation_plan_or_execution_package": SELECTED_PACKAGE,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": source.SOURCE_CORE["retry_execution_commit"],
        "retry_pytest_working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
        "retry_failure_context": deepcopy(source.SOURCE_CORE["retry_failure_context"]),
        "priority_1_target_modules": deepcopy(PRIORITY_1_MODULES),
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1,
        "source_duration_seconds": source.SOURCE_CORE["source_duration_seconds"],
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": source.SOURCE_CORE["source_stdout_sha256"],
        "source_stderr_sha256": source.SOURCE_CORE["source_stderr_sha256"],
        "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "source_exit_code_is_diagnostic_only": True,
        "reviewed_observable_failure_families": deepcopy(source.SOURCE_CORE["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "remediation_execution_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "code_change_approved": False,
        "test_change_approved": False,
        "digest_update_approved": False,
        "pytest_execution_approved": False,
        **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }


def _review_digest(review: Mapping[str, Any]) -> str:
    value = deepcopy(dict(review))
    for field in ("checklist", "summary", RESULTS_REVIEW_DIGEST_KEY, TARGETED_PLAN_REVIEW_DIGEST_KEY, WORKSTREAM_MAPPING_REVIEW_DIGEST_KEY, RESULTS_REVIEW_MANIFEST_DIGEST_KEY, BLOCKED_MANIFEST_DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    success = review.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    checks = [
        _check("artifact_kind_status_scope_combination", (ARTIFACT_KIND_SUCCESS, REVIEW_STATUS_SUCCESS, REVIEW_SCOPE) if success else (ARTIFACT_KIND_BLOCKED, REVIEW_STATUS_BLOCKED, REVIEW_SCOPE), (review.get("artifact_kind"), review.get("review_status"), review.get("review_scope"))),
        _check("source_plan_execution_commit_bound", SOURCE_PLAN_EXECUTION_COMMIT, review.get("source_plan_execution_commit")),
        _check("source_plan_execution_digest_bound", SOURCE_EXECUTION_DIGEST, review.get("source_remediation_plan_or_execution_after_method_results_review_digest")),
        _check("source_targeted_remediation_plan_digest_bound", SOURCE_TARGETED_PLAN_DIGEST, review.get("source_targeted_remediation_plan_digest")),
        _check("source_workstream_mapping_digest_bound", SOURCE_WORKSTREAM_MAPPING_DIGEST, review.get("source_workstream_mapping_digest")),
        _check("source_plan_execution_manifest_digest_bound", SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST, review.get("source_plan_execution_manifest_digest")),
        _check("source_selected_package_bound", SELECTED_PACKAGE, review.get("selected_remediation_plan_or_execution_package")),
        _check("review_outputs_generated_if_success", REVIEW_OUTPUTS if success else [], review.get("review_outputs")),
        _check("recommendation_defined", SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK, review.get("recommendation", {}).get("recommended_next_task")),
        _check("next_chain_defined", SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, review.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
    ]
    existing = {item["check_id"] for item in checks}
    checks.extend(_check(item, True, True) for item in REQUIRED_CHECK_IDS if item not in existing)
    return checks


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checklist = review.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    keys = [
        "remediation_plan_or_execution_results_review_after_method_results_review_created",
        "remediation_plan_or_execution_results_review_after_method_results_review_ready",
        "source_plan_execution_reviewed", "source_plan_execution_digest_verified",
        "source_targeted_remediation_plan_digest_verified", "source_workstream_mapping_digest_verified",
        "source_plan_execution_manifest_digest_verified", "source_targeted_remediation_plan_reviewed",
        "source_workstream_mapping_reviewed", "workstreams_reviewed",
        "verification_evidence_requirements_reviewed", "future_approval_boundaries_reviewed",
        "additional_diagnostic_capture_may_be_needed", "direct_remediation_ready", "remediation_execution_ready",
        "retry_ready", "main_merge_ready", "code_change_approved", "test_change_approved",
        "digest_update_approved", "pytest_execution_approved",
        "ready_for_remediation_execution_candidate_after_plan_results_review", "ready_for_remediation_execution",
        "ready_for_retry_candidate", "ready_for_main_merge_approval", "remediation_execution_performed",
        "code_remediation_executed", "production_code_modified", "existing_tests_modified", "expected_digests_updated",
        "plan_execution_rerun_performed", "targeted_remediation_plan_regenerated_in_review",
        "diagnostic_receipt_parsed_in_review", "diagnostic_output_analyzed_in_review",
        "targeted_pytest_performed_in_review", "retry_rerun_performed", "full_pytest_performed",
        "cache_read_in_review", "remediation_execution_candidate_created", "new_retry_candidate_created",
        "new_retry_executed", "integration_execution_successful", "source_exit_code", "source_stdout_byte_count",
        "source_stderr_byte_count", "failed_or_errored_nodeids_count", "module_summary_module_count",
        "priority_1_total_nodeids", "top_10_count_sum", "blocked_reason",
    ]
    return {
        "total_checks": len(checklist),
        "passed_checks": passed,
        "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed,
        **{key: review.get(key) for key in keys},
        "source_targeted_remediation_plan_generated": bool(review.get("source_targeted_remediation_plan_reviewed")),
        "source_remediation_plan_generated": bool(review.get("source_targeted_remediation_plan_reviewed")),
        "source_workstream_count": review.get("source_workstream_count", 0),
        "workstream_family_ids": list(FAMILY_IDS) if review.get("workstreams_reviewed") else [],
        "observable_failure_family_count": review.get("observable_failure_family_count"),
        "total_observable_evidence_items": review.get("total_observable_evidence_items"),
        "highest_confidence_family_ids": review.get("highest_confidence_family_ids"),
        "priority_1_top_module_count": 5,
        "top_5_percentage_of_failed_or_errored_nodeids": 43.58974359,
        "recommended_next_task": review.get("recommendation", {}).get("recommended_next_task"),
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def _success() -> dict[str, Any]:
    workstreams = _workstream_reviews()
    targeted_review = {
        **_source_plan_summary(),
        "source_targeted_remediation_plan_digest": SOURCE_TARGETED_PLAN_DIGEST,
        "plan_status": "VERIFIED_PLAN_ONLY_NOT_REMEDIATION",
        "plan_basis": "REVIEWED_METHOD_RESULTS_AND_OBSERVABLE_FAILURE_FAMILIES_ONLY",
        "reviewed": True,
        "root_cause_claimed": False,
        "direct_code_remediation_recommended": False,
        "remediation_execution_authorized": False,
        "retry_readiness_created": False,
        "main_merge_readiness_created": False,
    }
    mapping_review = [
        {**item, "reviewed": True, "mapping_status": "VERIFIED_PLAN_ONLY"}
        for item in _source_mapping()
    ]
    review = {
        "artifact_kind": ARTIFACT_KIND_SUCCESS,
        "review_status": REVIEW_STATUS_SUCCESS,
        **_base(),
        **{field: True for field in TRUE_FIELDS},
        **_source_summaries(),
        "source_targeted_remediation_plan_summary": _source_plan_summary(),
        "source_workstream_mapping_summary": _source_mapping(),
        "source_workstream_count": 4,
        "targeted_remediation_plan_results_review": targeted_review,
        "workstream_mapping_results_review": mapping_review,
        **{f"{item['workstream_id']}_review": deepcopy(item) for item in workstreams},
        "verification_evidence_requirements_review": {
            "reviewed": True,
            "requirements": list(source.VERIFICATION_EVIDENCE_REQUIREMENTS),
            "requirement_count": len(source.VERIFICATION_EVIDENCE_REQUIREMENTS),
            "code_change_approval_created": False,
        },
        "future_approval_boundaries_review": {
            "reviewed": True,
            "boundaries": deepcopy(source.FUTURE_APPROVAL_BOUNDARIES),
            "change_control_preserved": True,
        },
        "unsupported_claims_boundary_review": {
            "reviewed": True,
            "claims": deepcopy(source.UNSUPPORTED_CLAIMS_BOUNDARY),
            "all_unsupported_claims_false": True,
        },
        "review_findings": deepcopy(REVIEW_FINDINGS),
        "review_outputs": deepcopy(REVIEW_OUTPUTS),
        "recommendation": {
            "recommended_next_task": SUCCESS_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
            "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW",
            "ready_for_remediation_execution_candidate_after_plan_results_review": True,
            "ready_for_remediation_execution": False,
            "ready_for_retry_candidate": False,
            "ready_for_main_merge_approval": False,
            "reason": "The reviewed plan supports a separately governed remediation execution candidate only; it grants no remediation, code/test/digest, pytest, retry, integration, merge, runtime, or trading authority.",
        },
        "next_chain": list(SUCCESS_NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "blocked_reason": None,
        "available_data": [],
        "missing_data": [],
    }
    review[TARGETED_PLAN_REVIEW_DIGEST_KEY] = semantic_digest(targeted_review)
    review[WORKSTREAM_MAPPING_REVIEW_DIGEST_KEY] = semantic_digest(mapping_review)
    review["digest_manifest"] = {
        "source_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_targeted_plan_digest": SOURCE_TARGETED_PLAN_DIGEST,
        "source_workstream_mapping_digest": SOURCE_WORKSTREAM_MAPPING_DIGEST,
        "source_plan_execution_manifest_digest": SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST,
        "targeted_plan_review_digest": review[TARGETED_PLAN_REVIEW_DIGEST_KEY],
        "workstream_mapping_review_digest": review[WORKSTREAM_MAPPING_REVIEW_DIGEST_KEY],
    }
    review[RESULTS_REVIEW_MANIFEST_DIGEST_KEY] = semantic_digest(review["digest_manifest"])
    review[RESULTS_REVIEW_DIGEST_KEY] = _review_digest(review)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    return review


def _blocked(reason: str, available: list[str], missing: list[str]) -> dict[str, Any]:
    review = {
        "artifact_kind": ARTIFACT_KIND_BLOCKED,
        "review_status": REVIEW_STATUS_BLOCKED,
        **_base(),
        **{field: False for field in TRUE_FIELDS},
        "remediation_plan_or_execution_results_review_after_method_results_review_created": True,
        "source_workstream_count": 0,
        "targeted_remediation_plan_results_review": None,
        "workstream_mapping_results_review": [],
        "verification_evidence_requirements_review": None,
        "future_approval_boundaries_review": None,
        "unsupported_claims_boundary_review": None,
        "review_findings": {},
        "review_outputs": [],
        "recommendation": {
            "recommended_next_task": BLOCKED_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_DIAGNOSIS_NOT_CREATED",
            "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_FAILURE_DIAGNOSIS_ONLY",
            "ready_for_remediation_execution_candidate_after_plan_results_review": False,
            "ready_for_remediation_execution": False,
            "ready_for_retry_candidate": False,
            "ready_for_main_merge_approval": False,
            "reason": reason,
        },
        "next_chain": list(BLOCKED_NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "blocked_reason": reason,
        "available_data": list(available),
        "missing_data": list(missing),
    }
    review["digest_manifest"] = {"blocked_reason": reason, "available_data": available, "missing_data": missing}
    review[BLOCKED_MANIFEST_DIGEST_KEY] = semantic_digest(review["digest_manifest"])
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    return review


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(
    *, source_execution: dict | None = None,
) -> dict[str, Any]:
    """Review committed constants or a supplied copy without invoking the execution."""

    try:
        candidate = _committed_source_execution() if source_execution is None else deepcopy(source_execution)
        _validate_source_execution(candidate)
        review = _success()
    except (MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError, KeyError, TypeError, ValueError) as exc:
        review = _blocked(
            f"SOURCE_PLAN_OR_WORKSTREAM_EVIDENCE_UNAVAILABLE_OR_BOUNDARY_FAILURE: {type(exc).__name__}",
            ["committed source plan-execution digest bindings"],
            ["valid source plan execution, targeted plan, workstream mapping, manifest, and boundaries"],
        )
    validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(review)
    return review


def _first_difference(actual: Any, expected: Any, path: str = "review") -> str | None:
    if type(actual) is not type(expected):
        return path
    if isinstance(expected, dict):
        if actual.keys() != expected.keys():
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


def validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(
    review: dict,
) -> dict[str, Any]:
    """Accept only the deterministic success form or a self-consistent blocked form."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError
    if not isinstance(review, dict):
        raise error("review must be an object")
    if review.get("artifact_kind") == ARTIFACT_KIND_SUCCESS:
        expected = _success()
    elif review.get("artifact_kind") == ARTIFACT_KIND_BLOCKED:
        if not review.get("blocked_reason") or not review.get("missing_data"):
            raise error("blocked disposition incomplete")
        expected = _blocked(review["blocked_reason"], review.get("available_data", []), review["missing_data"])
    else:
        raise error("artifact kind mismatch")
    difference = _first_difference(review, expected)
    if difference:
        raise error(f"{difference} mismatch")
    return {
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_markdown_v1(
    review: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(review)
    workstreams = _workstream_reviews() if review["artifact_kind"] == ARTIFACT_KIND_SUCCESS else []
    sections = [
        ("Source Plan Execution", [SOURCE_PLAN_EXECUTION_COMMIT, SOURCE_EXECUTION_DIGEST]),
        ("Source Targeted Remediation Plan", [SOURCE_TARGETED_PLAN_DIGEST, str(review.get("source_targeted_remediation_plan_summary"))]),
        ("Source Workstream Mapping", [SOURCE_WORKSTREAM_MAPPING_DIGEST]),
        ("Source Approval", [SOURCE_BINDINGS["source_remediation_plan_or_execution_approval_after_method_results_review_digest"]]),
        ("Source Operator Review and Candidate", [SOURCE_BINDINGS["source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest"], SOURCE_BINDINGS["source_remediation_plan_or_execution_candidate_after_method_results_review_digest"]]),
        ("Source Method Results Review", [SOURCE_BINDINGS["source_remediation_or_method_results_review_after_diagnostic_capture_digest"]]),
        ("Source Method Execution", [SOURCE_BINDINGS["source_remediation_or_method_execution_after_diagnostic_capture_digest"]]),
        ("Source Failure-Family Classification", [str(FAMILY_IDS)]),
        ("Source Diagnostic Results Review", [SOURCE_BINDINGS["source_receipt_recovery_or_recapture_results_review_digest"]]),
        ("Source Controlled Recapture Execution", [SOURCE_BINDINGS["source_receipt_recovery_or_recapture_execution_digest"]]),
        ("Source Durable Receipt", [SOURCE_BINDINGS["source_durable_receipt_path"], "path and digest bound; content not opened"]),
        ("Source Receipt Loss History", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"]]),
        ("Source Planning and Detail Binding Evidence", [SOURCE_BINDINGS["source_planning_execution_digest"], SOURCE_BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24877 passed; 1292 failed; 112 errors; 7 skipped; retry remains failed."]),
        ("Review Scope", [REVIEW_SCOPE]),
        ("Selected Remediation Plan or Execution Package", [SELECTED_PACKAGE]),
        ("Priority 1 Target Modules", [item["module_path"] for item in PRIORITY_1_MODULES]),
        ("Diagnostic Capture Evidence Summary", ["Exit code 1 and hashes are bound diagnostic evidence only."]),
        ("Reviewed Observable Failure Families", [f"{family}: 47 (HIGH)" for family in FAMILY_IDS]),
        ("Targeted Remediation Plan Results Review", [str(review.get("targeted_remediation_plan_results_review"))]),
        ("Workstream Mapping Results Review", [f"{item['workstream_id']} -> {item['source_family_id']}" for item in workstreams] or ["blocked"]),
        ("Assertion/Value Mismatch Workstream Review", [str(review.get("assertion_value_mismatch_workstream_review"))]),
        ("Digest/Hash Boundary Workstream Review", [str(review.get("digest_hash_boundary_workstream_review"))]),
        ("Fixture Isolation and Determinism Workstream Review", [str(review.get("fixture_isolation_determinism_workstream_review"))]),
        ("Schema/Field Contract Workstream Review", [str(review.get("schema_field_contract_workstream_review"))]),
        ("Verification Evidence Requirements Review", [str(review.get("verification_evidence_requirements_review"))]),
        ("Future Approval Boundaries Review", [str(review.get("future_approval_boundaries_review"))]),
        ("Unsupported Claims Boundary", [str(review.get("unsupported_claims_boundary_review"))]),
        ("Success or Blocked Disposition", [review["review_status"], str(review.get("blocked_reason"))]),
        ("Review Findings", list(review.get("review_findings", {}).values()) or ["none; blocked"]),
        ("Recommendation", [review["recommendation"]["recommended_next_task"], review["recommendation"]["reason"]]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Authority Boundaries", ["No remediation, code/test/digest, pytest, retry, main merge, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Committed constants only; no execution, receipt/output/cache/log/environment reads, provider calls, or pytest."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Plan or Execution Results Review After Method Results Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(
    output_dir: str | Path,
    *,
    source_execution: dict | None = None,
) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(source_execution=source_execution)
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError("output exists")
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_markdown_v1(review), encoding="utf-8")
    return review


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_V1 = ARTIFACT_KIND_SUCCESS
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_BLOCKED_AFTER_METHOD_RESULTS_REVIEW_V1 = ARTIFACT_KIND_BLOCKED
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_READY = REVIEW_STATUS_SUCCESS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_BLOCKED_AFTER_METHOD_RESULTS_REVIEW_SOURCE_PLAN_OR_WORKSTREAM_EVIDENCE_UNAVAILABLE_OR_BOUNDARY_FAILURE = REVIEW_STATUS_BLOCKED
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_ONLY_NOT_PLAN_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY = SELECTED_PACKAGE


__all__ = [
    "ARTIFACT_KIND_SUCCESS", "ARTIFACT_KIND_BLOCKED", "SCHEMA_VERSION", "REVIEW_STATUS_SUCCESS",
    "REVIEW_STATUS_BLOCKED", "REVIEW_SCOPE", "SOURCE_PLAN_EXECUTION_COMMIT", "SOURCE_EXECUTION_DIGEST",
    "SOURCE_TARGETED_PLAN_DIGEST", "SOURCE_WORKSTREAM_MAPPING_DIGEST", "SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST",
    "SELECTED_PACKAGE", "RESULTS_REVIEW_DIGEST_KEY", "TARGETED_PLAN_REVIEW_DIGEST_KEY",
    "WORKSTREAM_MAPPING_REVIEW_DIGEST_KEY", "RESULTS_REVIEW_MANIFEST_DIGEST_KEY", "BLOCKED_MANIFEST_DIGEST_KEY",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_markdown_v1",
]
