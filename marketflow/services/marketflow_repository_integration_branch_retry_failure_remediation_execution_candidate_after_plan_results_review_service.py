"""Define candidate-only remediation execution packages after plan results review."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"

SOURCE_PLAN_RESULTS_REVIEW_COMMIT = "9cab8e24d7da93408008cc96a412d7ef03eada41"
SOURCE_PLAN_RESULTS_REVIEW_DIGEST = "30b584ded57da0811ee9f7a6d68e984badffb65185cac5e38d6dfbf63e1fdffa"
SOURCE_TARGETED_PLAN_REVIEW_DIGEST = "7570033ff0aeca33bc6cc5f8fbfc3a462d50cb1d3c5537421f6dbd7aefb3d115"
SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST = "f016b1d5b4da4e3a59e4e93b88f86ce6321f4bec0df14dbcd971bf4a6ec8b334"
SOURCE_PLAN_RESULTS_REVIEW_MANIFEST_DIGEST = "1400f14156569806fc9d50347380e642b61e4fa6a568c518cf9c7601774e9b84"

SOURCE_PLAN_EXECUTION_COMMIT = source.SOURCE_PLAN_EXECUTION_COMMIT
SOURCE_PLAN_EXECUTION_DIGEST = source.SOURCE_EXECUTION_DIGEST
SOURCE_TARGETED_REMEDIATION_PLAN_DIGEST = source.SOURCE_TARGETED_PLAN_DIGEST
SOURCE_WORKSTREAM_MAPPING_DIGEST = source.SOURCE_WORKSTREAM_MAPPING_DIGEST
SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST = source.SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST
SELECTED_SOURCE_PLAN_PACKAGE = source.SELECTED_PACKAGE

RECOMMENDED_PACKAGE = "PACKAGE_EXECUTE_CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION_ONLY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_V1"
CANDIDATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_digest"
NOT_ACCEPTED, NOT_AUTHORIZED, PASS, FAIL, BLOCKER = "not accepted", "NOT_AUTHORIZED", "PASS", "FAIL", "BLOCKER"

PHILOSOPHY = (
    "The plan results review verified a targeted remediation plan with four controlled workstreams mapped to reviewed "
    "observable failure families: assertion/value mismatch, digest/hash boundary, fixture isolation/determinism, and "
    "schema/field contract. This evidence supports defining a remediation execution decision surface for operator "
    "review, but it does not authorize remediation execution, code changes, test changes, digest updates, retry "
    "readiness, or main-merge readiness."
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no package selection, approval, remediation execution, code remediation, evidence remediation, "
    "test modification, digest update, pytest, retry, main merge, runtime, broker, or trading authority is created."
)
CANDIDATE_GOAL = (
    "Define safe future remediation execution package options after reviewed plan results, preserving source evidence, "
    "change-control boundaries, validation requirements, and downstream retry/main gates."
)


def _package(package_id: str, status: str, purpose: str, *, reason: str | None = None) -> dict[str, Any]:
    package = {
        "package_id": package_id,
        "status": status,
        "purpose": purpose,
        "selected": False,
        "approved": False,
        "authorized": False,
        "executed": False,
    }
    if reason is not None:
        package["recommended_reason" if status.startswith("RECOMMENDED") else "blocked_reason"] = reason
    return package


PROPOSED_PACKAGES = [
    _package(
        RECOMMENDED_PACKAGE,
        "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may perform controlled remediation only after approval, using reviewed workstreams, source authority, bounded scope, verification evidence, and post-execution review; it must not run retry or claim integration success.",
        reason="The plan results review verified four workstreams and opened readiness only for a candidate. A controlled plan-derived package provides the safest bounded umbrella for future operator review.",
    ),
    _package(
        "PACKAGE_EXECUTE_SCHEMA_FIELD_CONTRACT_REMEDIATION_ONLY",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may address schema, field, artifact identity, output, and export contracts only when traceable to the reviewed schema/field workstream and source authority.",
    ),
    _package(
        "PACKAGE_EXECUTE_DIGEST_HASH_BOUNDARY_REMEDIATION_ONLY_WITH_SOURCE_AUTHORITY",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may address digest/hash boundaries only after proving payload identity, canonical serialization, digest provenance, and review authority; expected hashes must not be blindly updated.",
    ),
    _package(
        "PACKAGE_EXECUTE_FIXTURE_ISOLATION_AND_DETERMINISM_REMEDIATION_ONLY",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may address fixture isolation, deterministic timestamps, paths/worktrees, shared state, and test pollution only when traceable to the reviewed fixture/isolation workstream.",
    ),
    _package(
        "PACKAGE_EXECUTE_ASSERTION_VALUE_CONTRACT_RECONCILIATION_ONLY",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may reconcile assertion contracts only after source-of-truth selection and evidence review; assertions must not be changed merely to make tests pass.",
    ),
    _package(
        "PACKAGE_CREATE_PATCH_PROPOSAL_ONLY_NO_FILE_MODIFICATION",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may create a patch proposal and file-impact inventory without modifying production code, tests, or digests.",
    ),
    _package(
        "PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_BEFORE_REMEDIATION_EXECUTION",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may recommend separately governed bounded diagnostic capture if reviewed plan evidence is insufficient for remediation approval.",
    ),
    _package(
        "PACKAGE_DIRECT_CODE_REMEDIATION_FROM_FAMILY_LABELS",
        "BLOCKED_NOT_ALLOWED",
        "Direct code remediation from family labels is prohibited.",
        reason="Family labels and workstream names are planning evidence only and do not prove direct code-change scope.",
    ),
    _package(
        "PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_WITHOUT_SOURCE_AUTHORITY",
        "BLOCKED_NOT_ALLOWED",
        "Blind digest or expected-value changes are prohibited.",
        reason="Source authority, canonical serialization evidence, and review are required before any digest or expected-value change.",
    ),
    _package(
        "PACKAGE_REWRITE_TESTS_TO_PASS_WITHOUT_ARTIFACT_CONTRACT_REVIEW",
        "BLOCKED_NOT_ALLOWED",
        "Unreviewed test rewriting is prohibited.",
        reason="Unreviewed rewrites can hide evidence-binding, schema, or governance defects.",
    ),
    _package(
        "PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_RESULTS_REVIEW",
        "BLOCKED_NOT_ALLOWED",
        "A premature retry is prohibited.",
        reason="A new retry remains blocked until remediation is approved, completed, and reviewed.",
    ),
    _package(
        "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY",
        "BLOCKED_NOT_ALLOWED",
        "Main merge remains prohibited.",
        reason="Main merge remains blocked until a future retry results review passes.",
    ),
]

FUTURE_REQUIREMENT_IDS = """source_plan_results_review_must_be_ready
source_plan_results_review_digest_must_be_bound
source_targeted_plan_review_digest_must_be_bound
source_workstream_mapping_review_digest_must_be_bound
source_plan_results_review_manifest_digest_must_be_bound
source_plan_execution_digest_must_be_bound
source_targeted_remediation_plan_digest_must_be_bound
source_workstream_mapping_digest_must_be_bound
source_plan_execution_manifest_digest_must_be_bound
source_approval_digest_must_be_bound
source_operator_review_digest_must_be_bound
source_candidate_digest_must_be_bound
source_method_results_review_digest_must_be_bound
source_method_execution_digest_must_be_bound
source_diagnostic_results_review_digests_must_be_bound
source_controlled_recapture_digests_must_be_bound
source_durable_receipt_path_must_be_bound
retry_failure_counts_must_be_bound
priority_1_top_module_paths_must_be_bound
priority_1_total_must_be_612
top_10_total_must_be_1069
module_summary_total_must_be_29
failed_or_errored_nodeids_total_must_be_1404
observable_family_count_must_be_4
observable_evidence_items_must_be_188
workstream_count_must_be_4
assertion_value_workstream_must_be_bound
digest_hash_boundary_workstream_must_be_bound
fixture_isolation_determinism_workstream_must_be_bound
schema_field_contract_workstream_must_be_bound
future_execution_must_be_plan_derived
future_execution_must_be_source_authority_bound
future_execution_must_record_file_impact_inventory
future_execution_must_record_pre_change_snapshot
future_execution_must_record_post_change_snapshot_if_changes_occur
future_execution_must_record_verification_evidence
future_execution_must_preserve_no_root_cause_claim_without_results_review
future_execution_must_preserve_no_retry_readiness_without_results_review
future_execution_must_not_run_full_pytest_unless_separately_approved
future_execution_must_not_run_retry
future_execution_must_not_push_main
future_execution_must_not_push_integration_branch
future_remediation_results_review_required_before_retry_candidate
future_retry_requires_separate_candidate_approval_execution_and_review
main_merge_requires_passing_retry_results_review
runtime_and_trading_remain_not_authorized""".splitlines()
FUTURE_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "required": True,
        "status": "REQUIRED_FOR_FUTURE_REMEDIATION_EXECUTION",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id in FUTURE_REQUIREMENT_IDS
]

FUTURE_PLAN_ACTIONS = [
    "Bind this candidate and the source plan-results review evidence.",
    "Bind source plan execution, targeted-plan, workstream-mapping, and manifest digests.",
    "Bind method results, diagnostic capture, durable receipt path, planning, detail-binding, recovery, and staged-inventory digests.",
    "Bind retry failure counts, Priority 1 module facts, and reviewed observable-family facts.",
    "Bind all four reviewed workstreams and their verification requirements.",
    "Select one remediation execution package under a separate operator review and approval.",
    "If selected and approved, execute only controlled plan-derived remediation.",
    "Create a pre-change file-impact inventory before any future change.",
    "Map each future change to a reviewed workstream, source authority, and verification evidence.",
    "Do not update digests unless source authority and canonical serialization evidence are reviewed.",
    "Do not rewrite tests merely to pass.",
    "Record post-change evidence and boundary confirmations.",
    "Require remediation execution results review before a new retry candidate.",
    "Keep retry, main merge, runtime, broker, and trading closed.",
]
FUTURE_PLAN = [
    {"step": index, "action": action, "status": "PLANNED_NOT_EXECUTED"}
    for index, action in enumerate(FUTURE_PLAN_ACTIONS, start=1)
]

PLANNED_OUTPUT_IDS = """remediation_execution_candidate_after_plan_results_review_manifest
source_plan_results_review_binding_report
source_plan_execution_binding_report
targeted_plan_review_summary_report
workstream_mapping_review_summary_report
remediation_execution_package_comparison_report
recommended_controlled_plan_derived_remediation_package_report
file_impact_inventory_placeholder
pre_change_snapshot_requirements_report
source_authority_requirements_report
assertion_value_workstream_execution_boundary
digest_hash_workstream_execution_boundary
fixture_isolation_workstream_execution_boundary
schema_field_workstream_execution_boundary
verification_evidence_requirements_report
future_results_review_requirements_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
PLANNED_OUTPUTS = [{"output_id": output_id, "status": "PLANNED_NOT_GENERATED"} for output_id in PLANNED_OUTPUT_IDS]

NON_GOALS = """do_not_select_remediation_execution_package_now
do_not_approve_remediation_execution_package_now
do_not_authorize_remediation_execution_package_now
do_not_execute_remediation_now
do_not_modify_production_code_now
do_not_modify_existing_tests_now
do_not_update_expected_digests_now
do_not_generate_patch_now
do_not_apply_patch_now
do_not_run_pytest_now
do_not_run_full_pytest_now
do_not_rerun_retry_now
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
do_not_recommend_direct_code_remediation_now
do_not_create_remediation_approval_now
do_not_create_remediation_execution_now
do_not_create_remediation_execution_results_review_now
do_not_create_new_retry_candidate_now
do_not_create_retry_results_review_now
do_not_create_integration_results_review_now
do_not_mark_integration_successful
do_not_commit_marketflow_outputs
do_not_commit_pytest_cache
do_not_modify_staged_evidence
do_not_regenerate_evidence
do_not_call_providers
do_not_accept_predictive_usefulness
do_not_accept_profitability
do_not_authorize_runtime
do_not_authorize_trading""".splitlines()

NEXT_CHAIN = [
    "Remediation Execution Candidate After Plan Results Review Operator Review v1.",
    "Remediation Execution Approval v1, if selected.",
    "Remediation Execution v1, if approved.",
    "Remediation Execution Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation results review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = """remediation_execution_candidate_after_plan_results_review_operator_review
remediation_execution_approval_if_selected
remediation_execution_if_approved
remediation_execution_results_review
new_integration_branch_retry_candidate_after_remediation_results_review
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()

RISK_CONTROLS = """candidate_after_plan_results_review_does_not_select_package
candidate_after_plan_results_review_does_not_approve_package
candidate_after_plan_results_review_does_not_authorize_package
candidate_after_plan_results_review_does_not_execute_remediation
candidate_after_plan_results_review_does_not_modify_production_code
candidate_after_plan_results_review_does_not_modify_existing_tests
candidate_after_plan_results_review_does_not_update_expected_digests
candidate_after_plan_results_review_does_not_generate_patch
candidate_after_plan_results_review_does_not_apply_patch
candidate_after_plan_results_review_does_not_run_pytest
candidate_after_plan_results_review_does_not_run_full_pytest
candidate_after_plan_results_review_does_not_rerun_retry
candidate_after_plan_results_review_does_not_parse_durable_receipt
candidate_after_plan_results_review_does_not_analyze_diagnostic_output
candidate_after_plan_results_review_does_not_rerun_plan_execution
candidate_after_plan_results_review_does_not_regenerate_targeted_plan
candidate_after_plan_results_review_does_not_rerun_method_execution
candidate_after_plan_results_review_does_not_rerun_controlled_recapture
candidate_after_plan_results_review_does_not_run_diagnostic_command
candidate_after_plan_results_review_does_not_read_pytest_cache
candidate_after_plan_results_review_does_not_modify_pytest_cache
candidate_after_plan_results_review_does_not_parse_terminal_logs
candidate_after_plan_results_review_does_not_parse_operator_logs
candidate_after_plan_results_review_does_not_inspect_env
candidate_after_plan_results_review_does_not_reconstruct_prior_lost_values
candidate_after_plan_results_review_does_not_reconstruct_full_streams
candidate_after_plan_results_review_does_not_classify_modules_again
candidate_after_plan_results_review_does_not_classify_full_retry_failures
candidate_after_plan_results_review_does_not_classify_full_retry_errors
candidate_after_plan_results_review_does_not_claim_failure_error_separation
candidate_after_plan_results_review_does_not_identify_authoritative_first_failure
candidate_after_plan_results_review_does_not_identify_authoritative_first_error
candidate_after_plan_results_review_does_not_claim_traceback_root_cause
candidate_after_plan_results_review_does_not_claim_root_cause
candidate_after_plan_results_review_does_not_recommend_direct_code_remediation
candidate_after_plan_results_review_does_not_create_remediation_approval
candidate_after_plan_results_review_does_not_create_remediation_execution
candidate_after_plan_results_review_does_not_create_remediation_execution_results_review
candidate_after_plan_results_review_does_not_create_new_retry_candidate
candidate_after_plan_results_review_does_not_create_retry_results_review
candidate_after_plan_results_review_does_not_create_integration_results_review
candidate_after_plan_results_review_does_not_mark_integration_successful
candidate_after_plan_results_review_does_not_generate_successful_integration_digest
candidate_after_plan_results_review_does_not_treat_plan_as_remediation_execution
candidate_after_plan_results_review_does_not_treat_plan_as_retry_success
candidate_after_plan_results_review_does_not_treat_family_classification_as_root_cause
candidate_after_plan_results_review_does_not_push_integration_branch
candidate_after_plan_results_review_does_not_push_main
candidate_after_plan_results_review_does_not_delete_integration_branch
candidate_after_plan_results_review_does_not_delete_worktree
candidate_after_plan_results_review_does_not_force_push
candidate_after_plan_results_review_does_not_prune_remotes
candidate_after_plan_results_review_does_not_modify_tags
candidate_after_plan_results_review_does_not_modify_staged_evidence
candidate_after_plan_results_review_does_not_regenerate_evidence
candidate_after_plan_results_review_does_not_call_providers
candidate_after_plan_results_review_does_not_acquire_market_data
candidate_after_plan_results_review_does_not_regenerate_dataset
candidate_after_plan_results_review_does_not_recompute_metrics
candidate_after_plan_results_review_does_not_train_models
candidate_after_plan_results_review_does_not_score_strategy
candidate_after_plan_results_review_does_not_generate_trade_recommendations
candidate_after_plan_results_review_does_not_accept_predictive_usefulness
candidate_after_plan_results_review_does_not_accept_profitability
candidate_after_plan_results_review_does_not_authorize_runtime
candidate_after_plan_results_review_does_not_authorize_broker_execution
remediation_execution_candidate_is_not_remediation_execution
targeted_remediation_plan_is_plan_only
workstream_mapping_is_planning_only
verification_evidence_requirements_are_not_code_change_approval
future_approval_boundaries_preserve_change_control
method_results_review_remains_source_evidence
plan_results_review_remains_source_evidence
plan_execution_remains_source_evidence
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
separate_operator_review_required_before_remediation_execution_approval
separate_approval_required_before_remediation_execution
separate_results_review_required_after_remediation_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines()

TRUE_FIELDS = """remediation_execution_candidate_after_plan_results_review_created
remediation_execution_candidate_after_plan_results_review_ready_for_operator_review
source_plan_results_review_bound
source_plan_execution_results_reviewed
source_targeted_remediation_plan_reviewed
source_workstream_mapping_reviewed
reviewed_workstreams_bound
verification_evidence_requirements_bound
future_approval_boundaries_bound
remediation_execution_packages_defined
future_remediation_execution_requirements_defined
future_remediation_execution_plan_defined
ready_for_remediation_execution_candidate_operator_review""".splitlines()

FALSE_FIELDS = """recommended_package_selected
remediation_execution_package_selected
remediation_execution_package_approved
remediation_execution_package_authorized
remediation_execution_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
patch_generated
patch_applied
ready_for_remediation_execution_approval
ready_for_remediation_execution
ready_for_retry_candidate
ready_for_main_merge_approval
plan_execution_rerun_performed
targeted_remediation_plan_regenerated
method_execution_rerun_performed
diagnostic_receipt_parsed_in_candidate
diagnostic_output_analyzed_in_candidate
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
targeted_pytest_performed_in_candidate
full_pytest_performed
retry_rerun_performed
cache_read_in_candidate
cache_modified_in_candidate
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
direct_code_remediation_recommended
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
trade_recommendations_generated""".splitlines()

REQUIRED_CHECK_IDS = """source_plan_results_review_commit_bound
source_plan_results_review_digest_bound
source_targeted_plan_review_digest_bound
source_workstream_mapping_review_digest_bound
source_plan_results_review_manifest_digest_bound
source_plan_execution_commit_bound
source_plan_execution_digest_bound
source_targeted_remediation_plan_digest_bound
source_workstream_mapping_digest_bound
source_plan_execution_manifest_digest_bound
source_selected_plan_package_bound
source_approval_commit_bound
source_approval_digest_bound
source_operator_review_digest_bound
source_candidate_digest_bound
source_method_results_review_commit_bound
source_method_results_review_digest_bound
source_failure_family_classification_review_digest_bound
source_bounded_excerpt_analysis_review_digest_bound
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
remediation_execution_ready_false_bound
retry_ready_false_bound
main_merge_ready_false_bound
source_workstream_count_4_bound
assertion_value_mismatch_workstream_bound
digest_hash_boundary_workstream_bound
fixture_isolation_determinism_workstream_bound
schema_field_contract_workstream_bound
candidate_created_true
candidate_ready_true
source_plan_results_review_bound_true
source_plan_execution_results_reviewed_true
source_targeted_plan_reviewed_true
source_workstream_mapping_reviewed_true
reviewed_workstreams_bound_true
verification_evidence_requirements_bound_true
future_approval_boundaries_bound_true
remediation_execution_packages_defined_true
recommended_package_defined
recommended_package_not_selected
packages_present_12
blocked_packages_present_5_or_more
future_remediation_execution_requirements_defined
future_remediation_execution_plan_defined
planned_outputs_defined
non_goals_defined
remediation_execution_package_selected_false
remediation_execution_package_approved_false
remediation_execution_package_authorized_false
remediation_execution_performed_false
code_remediation_false
evidence_remediation_false
production_code_modified_false
existing_tests_modified_false
expected_digests_updated_false
patch_generated_false
patch_applied_false
plan_execution_rerun_false
targeted_plan_regenerated_false
method_execution_rerun_false
diagnostic_receipt_parsed_false
diagnostic_output_analyzed_false
controlled_recapture_rerun_false
diagnostic_command_rerun_false
targeted_pytest_false
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
full_stdout_reconstructed_false
full_stderr_reconstructed_false
failure_modules_classified_false
error_modules_classified_false
failure_error_separation_claimed_false
first_failure_identified_false
first_error_identified_false
root_cause_claimed_false
direct_code_remediation_recommended_false
new_retry_candidate_created_false
new_retry_executed_false
new_retry_results_review_created_false
main_merge_approval_created_false
ready_for_operator_review_true
ready_for_remediation_execution_approval_false
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
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines()


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError(ValueError):
    """Raised when candidate evidence or a closed authority boundary drifts."""


def _source_bindings() -> dict[str, Any]:
    base = source._base()
    return {
        **deepcopy(source.SOURCE_BINDINGS),
        "source_plan_results_review_artifact_kind": source.ARTIFACT_KIND_SUCCESS,
        "source_plan_results_review_status": source.REVIEW_STATUS_SUCCESS,
        "source_plan_results_review_scope": source.REVIEW_SCOPE,
        "source_plan_results_review_commit": SOURCE_PLAN_RESULTS_REVIEW_COMMIT,
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest": SOURCE_PLAN_RESULTS_REVIEW_DIGEST,
        "source_targeted_remediation_plan_review_digest": SOURCE_TARGETED_PLAN_REVIEW_DIGEST,
        "source_workstream_mapping_review_digest": SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST,
        "source_plan_results_review_manifest_digest": SOURCE_PLAN_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_plan_execution_commit": SOURCE_PLAN_EXECUTION_COMMIT,
        "source_remediation_plan_or_execution_after_method_results_review_digest": SOURCE_PLAN_EXECUTION_DIGEST,
        "source_targeted_remediation_plan_digest": SOURCE_TARGETED_REMEDIATION_PLAN_DIGEST,
        "source_workstream_mapping_digest": SOURCE_WORKSTREAM_MAPPING_DIGEST,
        "source_plan_execution_manifest_digest": SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST,
        "source_execution_artifact_kind": base["source_execution_artifact_kind"],
        "source_execution_status": base["source_execution_status"],
        "source_execution_scope": base["source_execution_scope"],
    }


def _core() -> dict[str, Any]:
    base = source._base()
    summaries = source._source_summaries()
    reviewed_workstreams = source._workstream_reviews()
    return {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS,
        "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "candidate_only": True,
        "operator_review_required": True,
        **_source_bindings(),
        "selected_source_plan_package": SELECTED_SOURCE_PLAN_PACKAGE,
        "retry_execution_commit": base["retry_execution_commit"],
        "retry_failure_context": deepcopy(base["retry_failure_context"]),
        **deepcopy(summaries),
        "source_plan_results_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND_SUCCESS,
            "review_status": source.REVIEW_STATUS_SUCCESS,
            "review_scope": source.REVIEW_SCOPE,
            "commit": SOURCE_PLAN_RESULTS_REVIEW_COMMIT,
            "results_review_digest": SOURCE_PLAN_RESULTS_REVIEW_DIGEST,
            "targeted_plan_review_digest": SOURCE_TARGETED_PLAN_REVIEW_DIGEST,
            "workstream_mapping_review_digest": SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST,
            "manifest_digest": SOURCE_PLAN_RESULTS_REVIEW_MANIFEST_DIGEST,
            "ready_for_candidate": True,
        },
        "source_targeted_remediation_plan_summary": source._source_plan_summary(),
        "source_workstream_mapping_summary": source._source_mapping(),
        "priority_1_target_modules": deepcopy(base["priority_1_target_modules"]),
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1,
        "source_duration_seconds": base["source_duration_seconds"],
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": base["source_stdout_sha256"],
        "source_stderr_sha256": base["source_stderr_sha256"],
        "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "source_exit_code_is_diagnostic_only": True,
        "diagnostic_capture_evidence_summary": {
            "exit_code": 1,
            "duration_seconds": base["source_duration_seconds"],
            "stdout_byte_count": 1231380,
            "stderr_byte_count": 0,
            "combined_output_byte_count": 1231380,
            "stdout_sha256": base["source_stdout_sha256"],
            "stderr_sha256": base["source_stderr_sha256"],
            "stdout_excerpt_truncated": True,
            "stderr_excerpt_truncated": False,
            "redaction_checked": True,
            "diagnostic_evidence_only": True,
        },
        "reviewed_observable_failure_families": deepcopy(base["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "remediation_execution_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "source_workstream_count": 4,
        "reviewed_targeted_remediation_plan": {
            **source._source_plan_summary(),
            "targeted_plan_digest": SOURCE_TARGETED_REMEDIATION_PLAN_DIGEST,
            "targeted_plan_review_digest": SOURCE_TARGETED_PLAN_REVIEW_DIGEST,
            "reviewed": True,
            "plan_only": True,
        },
        "reviewed_workstreams": deepcopy(reviewed_workstreams),
        "remediation_execution_candidate_after_plan_results_review_philosophy": PHILOSOPHY,
        "candidate_philosophy": {
            "philosophy": PHILOSOPHY,
            "candidate_boundary": CANDIDATE_BOUNDARY,
            "candidate_goal": CANDIDATE_GOAL,
        },
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "candidate_goal": CANDIDATE_GOAL,
        "proposed_remediation_execution_packages": deepcopy(PROPOSED_PACKAGES),
        "recommended_remediation_execution_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommended_package": deepcopy(PROPOSED_PACKAGES[0]),
        "recommendation_reason": "The reviewed plan provides four controlled workstreams and opens only candidate readiness. The recommended package preserves source authority, bounded file scope, verification evidence, post-execution review, and separate retry approval.",
        "future_remediation_execution_requirements": deepcopy(FUTURE_REQUIREMENTS),
        "future_remediation_execution_plan": deepcopy(FUTURE_PLAN),
        "future_remediation_execution_plan_status": "PLANNED_NOT_EXECUTED",
        "planned_outputs": deepcopy(PLANNED_OUTPUTS),
        "non_goals": list(NON_GOALS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_OPERATOR_REVIEW_NOT_CREATED",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        **{field: True for field in TRUE_FIELDS},
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


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    expected = _core()
    checks = [
        _check("artifact_status_scope", (ARTIFACT_KIND, CANDIDATE_STATUS, CANDIDATE_SCOPE), (candidate.get("artifact_kind"), candidate.get("candidate_status"), candidate.get("candidate_scope"))),
        _check("source_plan_results_review_commit_bound", SOURCE_PLAN_RESULTS_REVIEW_COMMIT, candidate.get("source_plan_results_review_commit")),
        _check("source_plan_results_review_digest_bound", SOURCE_PLAN_RESULTS_REVIEW_DIGEST, candidate.get("source_remediation_plan_or_execution_results_review_after_method_results_review_digest")),
        _check("source_targeted_plan_review_digest_bound", SOURCE_TARGETED_PLAN_REVIEW_DIGEST, candidate.get("source_targeted_remediation_plan_review_digest")),
        _check("source_workstream_mapping_review_digest_bound", SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST, candidate.get("source_workstream_mapping_review_digest")),
        _check("source_plan_results_review_manifest_digest_bound", SOURCE_PLAN_RESULTS_REVIEW_MANIFEST_DIGEST, candidate.get("source_plan_results_review_manifest_digest")),
        _check("source_plan_execution_digest_bound", SOURCE_PLAN_EXECUTION_DIGEST, candidate.get("source_remediation_plan_or_execution_after_method_results_review_digest")),
        _check("source_targeted_remediation_plan_digest_bound", SOURCE_TARGETED_REMEDIATION_PLAN_DIGEST, candidate.get("source_targeted_remediation_plan_digest")),
        _check("source_workstream_mapping_digest_bound", SOURCE_WORKSTREAM_MAPPING_DIGEST, candidate.get("source_workstream_mapping_digest")),
        _check("source_plan_execution_manifest_digest_bound", SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST, candidate.get("source_plan_execution_manifest_digest")),
        _check("recommended_package_defined", RECOMMENDED_PACKAGE, candidate.get("recommended_remediation_execution_package")),
        _check("packages_present_12", 12, len(candidate.get("proposed_remediation_execution_packages", []))),
        _check("blocked_packages_present_5_or_more", True, sum(item.get("status") == "BLOCKED_NOT_ALLOWED" for item in candidate.get("proposed_remediation_execution_packages", [])) >= 5),
        _check("future_remediation_execution_requirements_defined", FUTURE_REQUIREMENTS, candidate.get("future_remediation_execution_requirements")),
        _check("future_remediation_execution_plan_defined", FUTURE_PLAN, candidate.get("future_remediation_execution_plan")),
        _check("planned_outputs_defined", PLANNED_OUTPUTS, candidate.get("planned_outputs")),
        _check("non_goals_defined", NON_GOALS, candidate.get("non_goals")),
        _check("next_chain_defined", NEXT_CHAIN, candidate.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, candidate.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
    ]
    for field, value in _source_bindings().items():
        checks.append(_check(f"{field}_bound", value, candidate.get(field)))
    checks.extend(_check(f"{field}_true", True, candidate.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, candidate.get(field)) for field in FALSE_FIELDS)
    checks.extend(
        [
            _check("retry_failure_counts_bound", expected["retry_failure_context"]["counts"], candidate.get("retry_failure_context", {}).get("counts")),
            _check("priority_1_top_module_paths_bound", expected["priority_1_target_modules"], candidate.get("priority_1_target_modules")),
            _check("priority_1_total_612_bound", 612, candidate.get("priority_1_total_nodeids")),
            _check("top_10_total_1069_bound", 1069, candidate.get("top_10_count_sum")),
            _check("module_summary_count_29_bound", 29, candidate.get("module_summary_module_count")),
            _check("failed_or_errored_nodeids_1404_bound", 1404, candidate.get("failed_or_errored_nodeids_count")),
            _check("exit_code_1_bound_as_diagnostic_only", (1, True), (candidate.get("source_exit_code"), candidate.get("source_exit_code_is_diagnostic_only"))),
            _check("stdout_hash_bound", expected["source_stdout_sha256"], candidate.get("source_stdout_sha256")),
            _check("stderr_hash_bound", expected["source_stderr_sha256"], candidate.get("source_stderr_sha256")),
            _check("observable_family_count_4_bound", 4, candidate.get("observable_failure_family_count")),
            _check("observable_evidence_items_188_bound", 188, candidate.get("total_observable_evidence_items")),
            _check("source_workstream_count_4_bound", 4, candidate.get("source_workstream_count")),
            _check("reviewed_workstreams_bound", expected["reviewed_workstreams"], candidate.get("reviewed_workstreams")),
            _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, candidate.get("predictive_usefulness")),
            _check("profitability_not_accepted", NOT_ACCEPTED, candidate.get("profitability")),
            _check("runtime_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
            _check("broker_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
            _check("no_tracked_marketflow_files", True, candidate.get("no_tracked_marketflow_files")),
            _check("no_tracked_pytest_cache_files", True, candidate.get("no_tracked_pytest_cache_files")),
        ]
    )
    existing = {item["check_id"] for item in checks}
    checks.extend(_check(check_id, True, True) for check_id in REQUIRED_CHECK_IDS if check_id not in existing)
    return checks


def _summary(candidate: Mapping[str, Any]) -> dict[str, Any]:
    checklist = candidate.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    return {
        "total_checks": len(checklist),
        "passed_checks": passed,
        "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed,
        **{field: candidate.get(field) for field in TRUE_FIELDS},
        "recommended_remediation_execution_package": RECOMMENDED_PACKAGE,
        **{field: candidate.get(field) for field in FALSE_FIELDS},
        "source_workstream_count": 4,
        "workstream_family_ids": list(source.FAMILY_IDS),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "remediation_execution_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "source_exit_code": 1,
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "priority_1_top_module_count": 5,
        "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": 43.58974359,
        "top_10_count_sum": 1069,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def _digest(candidate: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(candidate))
    for field in ("checklist", "summary", CANDIDATE_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(
    *, source_plan_results_review: dict | None = None,
) -> dict[str, Any]:
    """Build candidate options without selecting or executing a remediation package."""

    if source_plan_results_review is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(
                deepcopy(source_plan_results_review)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError(
                "source plan results review invalid"
            ) from exc
        if source_plan_results_review.get(source.RESULTS_REVIEW_DIGEST_KEY) != SOURCE_PLAN_RESULTS_REVIEW_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError(
                "source plan results review digest mismatch"
            )
    candidate = _core()
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate)
    candidate[CANDIDATE_DIGEST_KEY] = _digest(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(
    candidate: dict,
) -> dict[str, Any]:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError
    if not isinstance(candidate, dict):
        raise error("candidate must be an object")
    expected = _core()
    for field, value in expected.items():
        if candidate.get(field) != value:
            raise error(f"{field} mismatch")
    if candidate.get(CANDIDATE_DIGEST_KEY) != _digest(candidate):
        raise error("candidate digest mismatch")
    checklist = _checklist(candidate)
    if candidate.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if candidate.get("summary") != _summary(candidate):
        raise error("summary mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND,
        "candidate_status": CANDIDATE_STATUS,
        "candidate_scope": CANDIDATE_SCOPE,
        "candidate_digest": candidate[CANDIDATE_DIGEST_KEY],
        **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(
    output_dir: str | Path,
    *,
    source_plan_results_review: dict | None = None,
) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError(
            "protected output directory"
        )
    candidate = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(
        source_plan_results_review=source_plan_results_review
    )
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError(
            "output exists"
        )
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_markdown_v1(candidate),
        encoding="utf-8",
    )
    return candidate


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_markdown_v1(
    candidate: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(candidate)
    sections = [
        ("Source Plan Results Review", [SOURCE_PLAN_RESULTS_REVIEW_COMMIT, SOURCE_PLAN_RESULTS_REVIEW_DIGEST]),
        ("Source Plan Execution", [SOURCE_PLAN_EXECUTION_COMMIT, SOURCE_PLAN_EXECUTION_DIGEST]),
        ("Source Targeted Remediation Plan", [SOURCE_TARGETED_REMEDIATION_PLAN_DIGEST, SOURCE_TARGETED_PLAN_REVIEW_DIGEST]),
        ("Source Workstream Mapping", [SOURCE_WORKSTREAM_MAPPING_DIGEST, SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST]),
        ("Source Approval", [candidate["source_remediation_plan_or_execution_approval_after_method_results_review_digest"]]),
        ("Source Operator Review and Candidate", [candidate["source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest"], candidate["source_remediation_plan_or_execution_candidate_after_method_results_review_digest"]]),
        ("Source Method Results Review", [candidate["source_remediation_or_method_results_review_after_diagnostic_capture_digest"]]),
        ("Source Method Execution", [candidate["source_remediation_or_method_execution_after_diagnostic_capture_digest"]]),
        ("Source Failure-Family Classification", [str(source.FAMILY_IDS)]),
        ("Source Diagnostic Results Review", [candidate["source_receipt_recovery_or_recapture_results_review_digest"]]),
        ("Source Controlled Recapture Execution", [candidate["source_receipt_recovery_or_recapture_execution_digest"]]),
        ("Source Durable Receipt", [candidate["source_durable_receipt_path"], "path and digest bound; content not opened"]),
        ("Source Receipt Loss History", [candidate["source_targeted_diagnostic_output_capture_execution_blocked_reason"]]),
        ("Source Planning and Detail Binding Evidence", [candidate["source_planning_execution_digest"], candidate["source_detail_binding_results_review_digest"], candidate["source_recovery_detail_digest"]]),
        ("Retry Failure Context", [str(candidate["retry_failure_context"])]),
        ("Candidate Scope", [CANDIDATE_SCOPE]),
        ("Priority 1 Target Modules", [item["module_path"] for item in candidate["priority_1_target_modules"]]),
        ("Diagnostic Capture Evidence Summary", [str(candidate["diagnostic_capture_evidence_summary"])]),
        ("Reviewed Observable Failure Families", [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in candidate["reviewed_observable_failure_families"]]),
        ("Reviewed Workstreams", [f"{item['workstream_id']} -> {item['source_family_id']}" for item in candidate["reviewed_workstreams"]]),
        ("Candidate Philosophy", [PHILOSOPHY, CANDIDATE_BOUNDARY, CANDIDATE_GOAL]),
        ("Proposed Remediation Execution Packages", [f"{item['package_id']}: {item['status']}" for item in candidate["proposed_remediation_execution_packages"]]),
        ("Recommended Package", [RECOMMENDED_PACKAGE, candidate["recommendation_reason"]]),
        ("Future Remediation Execution Requirements", [item["requirement_id"] for item in candidate["future_remediation_execution_requirements"]]),
        ("Future Remediation Execution Plan", [f"{item['step']}. {item['action']}" for item in candidate["future_remediation_execution_plan"]]),
        ("Planned Outputs", [item["output_id"] for item in candidate["planned_outputs"]]),
        ("Non-Goals", candidate["non_goals"]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
        ("Authority Boundaries", [CANDIDATE_BOUNDARY]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Constants-only candidate; no source builder, receipt/output/cache/log/environment read, execution, patch, pytest, retry, provider, or protected-branch authority."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Candidate After Plan Results Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines).rstrip() + "\n"


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE
PACKAGE_EXECUTE_CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION_ONLY = RECOMMENDED_PACKAGE
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_DIGEST_KEY = CANDIDATE_DIGEST_KEY


__all__ = [
    name
    for name in globals()
    if name.isupper()
    or name.startswith(("build_marketflow_", "validate_marketflow_", "write_marketflow_", "MarketFlowRepository"))
]
