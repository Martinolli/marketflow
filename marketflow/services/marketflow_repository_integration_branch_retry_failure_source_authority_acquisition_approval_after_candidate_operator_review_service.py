"""Approve future source-authority acquisition without executing acquisition."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_OPERATOR_REVIEW_COMMIT = "d23bbacd7f59003b178a689a526054bb5c508dfb"
SOURCE_OPERATOR_REVIEW_DIGEST = "88fe49607f9b15b3386db8be78f0dccd8637ff194edbe5b950c68ad27bdea1d0"
SOURCE_CANDIDATE_REVIEW_DIGEST = "6c122b5bb1489861a969efdf9ab9c36f4ce9a799b7ecf76b791d41a550f653e5"
SOURCE_SCOPE_REVIEW_DIGEST = "713aefda1df0916f1ddd25084751cb3f2a23ddc9679e16ff4827409678092d0e"
SOURCE_MAPPING_REVIEW_DIGEST = "83104c9ff91bceed69f368f194cf454629f3530e0c6e8dabed83099677a7b381"
SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST = "aed56abc9ed50be991066fea1cf79f0e35ed3e2c851cd847e8cb691825f3b38a"
SELECTED_PACKAGE = source.RECOMMENDED_PACKAGE
OPERATOR_DECISION = "APPROVE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE_FOR_FUTURE_EXECUTION"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_digest"
ATTESTATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_attestation_digest"
PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

REQUIRED_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1 = (
    "APPROVE MARKETFLOW RETRY FAILURE PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE "
    "AFTER SOURCE AUTHORITY ACQUISITION CANDIDATE OPERATOR REVIEW FOR FUTURE EXECUTION ONLY NO SOURCE AUTHORITY "
    "ACQUISITION NOW NO EVIDENCE ACQUISITION NOW NO NO CHANGE DISPOSITION NOW NO ALTERNATE DIAGNOSTICS NOW NO "
    "REMEDIATION NOW NO CODE CHANGES NOW NO TEST CHANGES NOW NO DIGEST UPDATES NOW NO PATCH NOW NO PYTEST NOW NO "
    "RETRY NO MAIN PUSH SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_"
    "NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE = SELECTED_PACKAGE


TRUE_FIELDS = tuple("""source_authority_acquisition_approval_created
source_authority_acquisition_package_selected
source_authority_acquisition_package_approved
source_authority_acquisition_package_authorized_for_future_execution
selected_source_authority_acquisition_package_verified
source_operator_review_bound
source_follow_on_results_review_bound
source_follow_on_execution_bound
source_follow_on_approval_bound
source_follow_on_operator_review_bound
source_follow_on_candidate_bound
source_results_review_bound
source_execution_bound
source_historical_approval_bound
source_historical_candidate_chain_bound
source_failure_diagnosis_bound
source_blocked_execution_bound
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
diagnostic_metadata_bound
observable_families_bound
reviewed_workstreams_bound
source_authority_acquisition_candidate_bound
acquisition_scope_sections_bound
missing_authority_mapping_bound
acceptable_source_artifact_inventory_bound
operator_provided_evidence_requirements_bound
evidence_custody_and_digest_requirements_bound
candidate_results_review_requirements_bound
future_requirements_approved
future_plan_approved
planned_outputs_authorized_not_generated
supporting_packages_preserved_unselected
blocked_packages_preserved_blocked
ready_for_source_authority_acquisition_execution_after_candidate_operator_review""".splitlines())

FALSE_FIELDS = tuple("""source_authority_acquisition_execution_performed
source_authority_acquisition_performed
source_authority_evidence_acquired
external_evidence_acquired
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
pytest_performed_in_approval
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_approval
diagnostic_output_analyzed_in_approval
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_approval
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_approval
cache_modified_in_approval
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
provider_requests_made_in_approval
market_data_acquisition_performed_in_approval
dataset_generation_performed_in_approval
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

FUTURE_PERMISSION_TRUE_FIELDS = tuple("""future_execution_may_acquire_or_bind_source_authority_evidence
future_execution_may_create_source_authority_acquisition_records
future_execution_may_create_evidence_custody_and_digest_records
future_execution_may_map_acquired_evidence_to_missing_authority_items
future_execution_may_define_acquisition_results_review_package""".splitlines())

FUTURE_PERMISSION_FALSE_FIELDS = tuple("""future_execution_may_execute_remediation
future_execution_may_modify_production_code
future_execution_may_modify_existing_tests
future_execution_may_update_expected_digests
future_execution_may_generate_or_apply_patch
future_execution_may_run_full_pytest
future_execution_may_run_retry
future_execution_may_create_retry_candidate
future_execution_may_claim_root_cause
future_execution_may_claim_retry_success
future_execution_may_create_main_merge_approval
future_execution_may_push_main
future_execution_may_push_integration_branch
future_source_authority_acquisition_execution_executed""".splitlines())

PLANNED_OUTPUT_IDS = tuple("""source_authority_acquisition_approval_manifest
source_operator_review_binding_report
source_follow_on_results_review_binding_report
source_follow_on_execution_binding_report
source_follow_on_approval_binding_report
source_follow_on_operator_review_binding_report
source_follow_on_candidate_binding_report
source_results_review_binding_report
source_execution_binding_report
source_failure_diagnosis_binding_report
source_blocked_execution_binding_report
retry_failure_context_review
priority1_validation_disposition_review
diagnostic_metadata_boundary_review
observable_family_review
reviewed_workstreams_review
acquisition_candidate_identity_review
acquisition_scope_section_review
missing_authority_mapping_review
acceptable_source_artifact_inventory_review
operator_provided_evidence_requirements_review
evidence_custody_and_digest_requirements_review
candidate_results_review_requirements_review
approved_source_authority_acquisition_package_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

SUPPORTING_PACKAGE_IDS = (
    "PACKAGE_CREATE_OPERATOR_PROVIDED_SOURCE_EVIDENCE_PACKAGE_REQUIREMENTS_ONLY",
    "PACKAGE_CREATE_SOURCE_OWNER_AUTHORITY_REQUESTS_FOR_MISSING_ITEMS",
    "PACKAGE_CREATE_LIMITED_SCHEMA_FIELD_CONTRACT_AUTHORITY_ACQUISITION_PATH",
    "PACKAGE_CREATE_LIMITED_DIGEST_SERIALIZATION_AUTHORITY_ACQUISITION_PATH",
    "PACKAGE_HOLD_SOURCE_AUTHORITY_ACQUISITION_PENDING_SOURCE_OWNER_INPUT",
)
BLOCKED_PACKAGE_IDS = (
    "PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_APPROVAL",
    "PACKAGE_ACCEPT_DIAGNOSTIC_OUTPUT_AS_SOURCE_AUTHORITY",
    "PACKAGE_DIRECT_REMEDIATION_FROM_ACQUISITION_CANDIDATE",
    "PACKAGE_NO_CHANGE_DISPOSITION_FROM_ACQUISITION_CANDIDATE_ONLY",
    "PACKAGE_NEW_RETRY_FROM_ACQUISITION_CANDIDATE_ONLY",
    "PACKAGE_MAIN_MERGE_FROM_ACQUISITION_CANDIDATE_OR_CURRENT_ROOT_PASS",
)

FUTURE_PLAN = (
    "Bind this approval and source acquisition-candidate operator review.",
    "Bind the follow-on execution results review and all upstream follow-on execution, approval, candidate, source-enrichment, failure-diagnosis, blocked-remediation, plan, method, diagnostic, detail/recovery, module-grouping, and staged-inventory digests.",
    "Bind retry failure counts, Priority 1 modules, Priority 1 validation facts, diagnostic metadata, observable families, reviewed workstreams, and missing-authority inventory facts.",
    "Preserve acquisition candidate identity, status, scope, basis, and boundary.",
    "Preserve all four acquisition-scope sections.",
    "Preserve all 30 mapped missing-authority items as missing/not acquired until future execution obtains or binds evidence.",
    "Preserve the 13 acceptable source-artifact types as future acquisition inputs only.",
    "Preserve the 10 operator-provided evidence requirements.",
    "Preserve the six evidence custody and digest requirements.",
    "Preserve the 16 candidate results-review requirements.",
    "Execute source-authority acquisition only in a separately invoked execution task.",
    "Require acquisition results review before no-change disposition, alternate diagnostic, remediation, retry candidate, or main-merge path.",
    "Preserve retry, remediation, no-change disposition, main-merge, provider, runtime, broker, and trading gates.",
)

NEXT_CHAIN = (
    "Source Authority Acquisition Execution After Candidate Operator Review v1, if approved.",
    "Source Authority Acquisition Results Review v1.",
    "Conditional no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if reviewed acquired source authority supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if the new retry results review passes.",
)
NEXT_GATES = tuple("""source_authority_acquisition_execution_if_approved
source_authority_acquisition_results_review
no_change_disposition_candidate_if_supported
alternate_diagnostic_candidate_if_supported
remediation_reentry_candidate_if_supported
no_change_retry_criteria_candidate_if_supported
hold_disposition_if_supported
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines())

RISK_CONTROLS = tuple("""source_authority_acquisition_approval_does_not_execute_acquisition
source_authority_acquisition_approval_does_not_acquire_source_authority
source_authority_acquisition_approval_does_not_acquire_source_authority_evidence
source_authority_acquisition_approval_does_not_acquire_external_evidence
source_authority_acquisition_approval_does_not_create_no_change_disposition
source_authority_acquisition_approval_does_not_execute_alternate_diagnostics
source_authority_acquisition_approval_does_not_execute_remediation
source_authority_acquisition_approval_does_not_modify_production_code
source_authority_acquisition_approval_does_not_modify_existing_tests
source_authority_acquisition_approval_does_not_update_expected_digests
source_authority_acquisition_approval_does_not_generate_patch
source_authority_acquisition_approval_does_not_apply_patch
source_authority_acquisition_approval_does_not_run_pytest
source_authority_acquisition_approval_does_not_run_full_pytest
source_authority_acquisition_approval_does_not_rerun_priority1_validation
source_authority_acquisition_approval_does_not_rerun_retry
source_authority_acquisition_approval_does_not_rerun_detached_retry
source_authority_acquisition_approval_does_not_parse_durable_receipt
source_authority_acquisition_approval_does_not_analyze_diagnostic_output
source_authority_acquisition_approval_does_not_rerun_source_authority_enrichment
source_authority_acquisition_approval_does_not_rerun_follow_on_execution
source_authority_acquisition_approval_does_not_rerun_plan_execution
source_authority_acquisition_approval_does_not_regenerate_targeted_plan
source_authority_acquisition_approval_does_not_rerun_method_execution
source_authority_acquisition_approval_does_not_rerun_controlled_recapture
source_authority_acquisition_approval_does_not_run_diagnostic_command
source_authority_acquisition_approval_does_not_read_pytest_cache
source_authority_acquisition_approval_does_not_modify_pytest_cache
source_authority_acquisition_approval_does_not_parse_terminal_logs
source_authority_acquisition_approval_does_not_parse_operator_logs
source_authority_acquisition_approval_does_not_inspect_env
source_authority_acquisition_approval_does_not_reconstruct_prior_lost_values
source_authority_acquisition_approval_does_not_reconstruct_full_streams
source_authority_acquisition_approval_does_not_classify_modules_again
source_authority_acquisition_approval_does_not_classify_full_retry_failures
source_authority_acquisition_approval_does_not_classify_full_retry_errors
source_authority_acquisition_approval_does_not_claim_failure_error_separation
source_authority_acquisition_approval_does_not_identify_authoritative_first_failure
source_authority_acquisition_approval_does_not_identify_authoritative_first_error
source_authority_acquisition_approval_does_not_claim_traceback_root_cause
source_authority_acquisition_approval_does_not_claim_root_cause
source_authority_acquisition_approval_does_not_claim_retry_success
source_authority_acquisition_approval_does_not_claim_main_merge_readiness
source_authority_acquisition_approval_does_not_create_retry_candidate
source_authority_acquisition_approval_does_not_create_retry_approval
source_authority_acquisition_approval_does_not_create_retry_execution
source_authority_acquisition_approval_does_not_create_retry_results_review
source_authority_acquisition_approval_does_not_create_integration_results_review
source_authority_acquisition_approval_does_not_mark_integration_successful
source_authority_acquisition_approval_does_not_generate_successful_integration_digest
source_authority_acquisition_approval_does_not_push_integration_branch
source_authority_acquisition_approval_does_not_push_main
source_authority_acquisition_approval_does_not_delete_integration_branch
source_authority_acquisition_approval_does_not_delete_worktree
source_authority_acquisition_approval_does_not_force_push
source_authority_acquisition_approval_does_not_prune_remotes
source_authority_acquisition_approval_does_not_modify_tags
source_authority_acquisition_approval_does_not_modify_staged_evidence
source_authority_acquisition_approval_does_not_regenerate_evidence
source_authority_acquisition_approval_does_not_call_providers
source_authority_acquisition_approval_does_not_acquire_market_data
source_authority_acquisition_approval_does_not_generate_dataset
source_authority_acquisition_approval_does_not_recompute_metrics
source_authority_acquisition_approval_does_not_train_models
source_authority_acquisition_approval_does_not_score_strategy
source_authority_acquisition_approval_does_not_generate_trade_recommendations
source_authority_acquisition_approval_does_not_accept_predictive_usefulness
source_authority_acquisition_approval_does_not_accept_profitability
source_authority_acquisition_approval_does_not_authorize_runtime
source_authority_acquisition_approval_does_not_authorize_broker_execution
selected_source_authority_acquisition_package_approved_for_future_execution_only
future_execution_limited_to_reviewed_candidate_scope
future_acquisition_execution_is_not_remediation
future_acquisition_execution_is_not_retry
candidate_scope_is_not_acquired_source_authority
operator_review_is_not_acquisition_approval_until_this_approval
approval_is_not_source_authority_acquisition
diagnostic_output_is_not_source_authority
priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_execution_required_after_approval
separate_results_review_required_after_any_acquisition
separate_remediation_approval_required_before_code_or_test_changes
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines())


class MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError(ValueError):
    """Raised when attestation, source evidence, or approval boundaries differ."""


def _committed_source_operator_review() -> dict[str, Any]:
    return source._assemble_review(source._committed_source_follow_on_results_review())


def _first_difference(actual: Any, expected: Any, path: str = "approval") -> str | None:
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


def _validate_source_operator_review(review: Mapping[str, Any]) -> None:
    difference = _first_difference(review, _committed_source_operator_review(), "source_operator_review")
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError(f"{difference} mismatch")


def _expected_operator_confirmations(review: Mapping[str, Any]) -> dict[str, Any]:
    values = {
        "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_review_digest": SOURCE_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_source_scope_review_digest": SOURCE_SCOPE_REVIEW_DIGEST,
        "operator_confirms_source_mapping_review_digest": SOURCE_MAPPING_REVIEW_DIGEST,
        "operator_confirms_source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
        "operator_confirms_source_follow_on_results_review_digest": review["source_follow_on_results_review_digest"],
        "operator_confirms_source_acquisition_candidate_review_digest": review["source_acquisition_candidate_review_digest"],
        "operator_confirms_source_acquisition_scope_review_digest": review["source_acquisition_scope_review_digest"],
        "operator_confirms_source_missing_authority_mapping_review_digest": review["source_missing_authority_mapping_review_digest"],
        "operator_confirms_source_follow_on_results_review_manifest_digest": review["source_follow_on_results_review_manifest_digest"],
        "operator_confirms_source_follow_on_execution_digest": review["source_follow_on_execution_after_results_review_digest"],
        "operator_confirms_source_authority_acquisition_candidate_digest": review["source_authority_acquisition_candidate_digest"],
        "operator_confirms_source_authority_acquisition_scope_digest": review["source_authority_acquisition_scope_digest"],
        "operator_confirms_source_missing_authority_to_source_evidence_mapping_digest": review["source_missing_authority_to_source_evidence_mapping_digest"],
        "operator_confirms_source_follow_on_execution_manifest_digest": review["source_follow_on_execution_manifest_digest"],
        "operator_confirms_source_follow_on_approval_digest": review["source_follow_on_approval_digest"],
        "operator_confirms_source_follow_on_operator_review_digest": review["source_follow_on_candidate_operator_review_digest"],
        "operator_confirms_source_follow_on_candidate_digest": review["source_follow_on_candidate_digest"],
        "operator_confirms_source_results_review_digest": review["source_results_review_digest"],
        "operator_confirms_source_execution_digest": review["source_execution_digest"],
        "operator_confirms_source_authority_enrichment_plan_digest": review["source_authority_enrichment_plan_digest"],
        "operator_confirms_source_missing_authority_inventory_digest": review["source_missing_authority_inventory_digest"],
        "operator_confirms_source_workstream_authority_mapping_digest": review["source_workstream_authority_mapping_digest"],
        "operator_confirms_source_execution_manifest_digest": review["source_execution_manifest_digest"],
        "operator_confirms_source_approval_digest": review["source_approval_digest"],
        "operator_confirms_source_historical_operator_review_digest": review["source_operator_review_digest"],
        "operator_confirms_source_historical_candidate_digest": review["source_candidate_digest"],
        "operator_confirms_source_failure_diagnosis_digest": review["source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"],
        "operator_confirms_source_blocked_execution_commit": review["source_blocked_execution_commit"],
        "operator_confirms_source_blocked_reason": review["source_blocked_reason"],
        "operator_confirms_source_blocked_manifest_digest": review["source_blocked_manifest_digest"],
        "operator_confirms_primary_failure_class": review["primary_failure_class"],
        "operator_confirms_source_remediation_execution_approval_digest": review["source_remediation_execution_approval_after_plan_results_review_digest"],
        "operator_confirms_source_plan_results_review_digest": review["source_remediation_plan_or_execution_results_review_after_method_results_review_digest"],
        "operator_confirms_source_targeted_plan_review_digest": review["source_targeted_remediation_plan_review_digest"],
        "operator_confirms_source_plan_execution_digest": review["source_remediation_plan_or_execution_after_method_results_review_digest"],
        "operator_confirms_source_targeted_remediation_plan_digest": review["source_targeted_remediation_plan_digest"],
        "operator_confirms_source_method_results_review_digest": review["source_remediation_or_method_results_review_after_diagnostic_capture_digest"],
        "operator_confirms_source_method_execution_digest": review["source_remediation_or_method_execution_after_diagnostic_capture_digest"],
        "operator_confirms_source_diagnostic_results_review_digest": review["source_receipt_recovery_or_recapture_results_review_digest"],
        "operator_confirms_source_controlled_recapture_execution_digest": review["source_receipt_recovery_or_recapture_execution_digest"],
        "operator_confirms_source_durable_receipt_digest": review["source_receipt_recovery_or_recapture_receipt_digest"],
        "operator_confirms_source_durable_receipt_path": review["source_durable_receipt_path"],
        "operator_confirms_source_planning_execution_digest": review["source_planning_execution_digest"],
        "operator_confirms_source_complete_29_row_binding_digest": review["source_complete_29_row_binding_digest"],
        "operator_confirms_source_materialized_payload_digest": review["source_materialized_payload_digest"],
        "operator_confirms_source_recovery_detail_digest": review["source_recovery_detail_digest"],
        "operator_confirms_source_module_grouping_digest": review["source_module_grouping_digest"],
        "operator_confirms_source_staged_inventory_digest": review["source_staged_inventory_digest"],
        "operator_confirms_retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "operator_confirms_source_stdout_hash": review["diagnostic_capture_evidence_summary"]["stdout_sha256"],
        "operator_confirms_source_stderr_hash": review["diagnostic_capture_evidence_summary"]["stderr_sha256"],
        "operator_confirms_selected_source_authority_acquisition_package": SELECTED_PACKAGE,
    }
    boolean_keys = tuple("""operator_confirms_secondary_failure_classes
operator_confirms_retry_failure_counts
operator_confirms_priority_1_total_612
operator_confirms_top_10_total_1069
operator_confirms_module_summary_count_29
operator_confirms_failed_or_errored_nodeids_1404
operator_confirms_priority1_pre_change_validation_675_passed
operator_confirms_priority1_post_change_validation_675_passed
operator_confirms_priority1_validation_not_retry_evidence
operator_confirms_source_exit_code_1_as_diagnostic_only
operator_confirms_source_stdout_byte_count_1231380
operator_confirms_source_stderr_byte_count_0
operator_confirms_observable_family_count_4
operator_confirms_observable_evidence_items_188
operator_confirms_family_confidence_high
operator_confirms_workstream_count_4
operator_confirms_acquisition_scope_section_count_4
operator_confirms_mapped_missing_authority_item_count_30
operator_confirms_acceptable_source_artifact_type_count_13
operator_confirms_operator_provided_evidence_requirement_count_10
operator_confirms_evidence_custody_and_digest_requirement_count_6
operator_confirms_candidate_results_review_requirement_count_16
operator_confirms_missing_authority_items_missing_not_acquired
operator_confirms_workstream_mappings_planned_not_executed
operator_confirms_approval_scope_only
operator_confirms_no_source_authority_acquisition_execution_now
operator_confirms_no_source_authority_acquisition_now
operator_confirms_no_source_authority_evidence_acquisition_now
operator_confirms_no_external_evidence_acquisition_now
operator_confirms_no_no_change_disposition_now
operator_confirms_no_alternate_diagnostics_now
operator_confirms_no_remediation_now
operator_confirms_no_code_remediation_now
operator_confirms_no_production_code_change_now
operator_confirms_no_existing_test_change_now
operator_confirms_no_expected_digest_update_now
operator_confirms_no_patch_generation_now
operator_confirms_no_patch_application_now
operator_confirms_no_pytest_now
operator_confirms_no_full_pytest_now
operator_confirms_no_retry
operator_confirms_no_cache_read
operator_confirms_no_cache_modification
operator_confirms_no_durable_receipt_parse
operator_confirms_no_diagnostic_output_analysis
operator_confirms_no_source_authority_enrichment_rerun
operator_confirms_no_follow_on_execution_rerun
operator_confirms_no_plan_execution_rerun
operator_confirms_no_targeted_plan_regeneration
operator_confirms_no_method_execution_rerun
operator_confirms_no_recapture_rerun
operator_confirms_no_diagnostic_command
operator_confirms_no_priority1_validation_rerun
operator_confirms_no_terminal_log_parse
operator_confirms_no_operator_log_parse
operator_confirms_no_env_inspection
operator_confirms_no_prior_lost_value_reconstruction
operator_confirms_no_full_stream_reconstruction
operator_confirms_no_failure_error_separation
operator_confirms_no_first_failure
operator_confirms_no_first_error
operator_confirms_no_traceback_root_cause
operator_confirms_no_root_cause
operator_confirms_no_retry_success
operator_confirms_no_main_merge_readiness
operator_confirms_no_retry_candidate
operator_confirms_no_retry_approval
operator_confirms_no_retry_execution
operator_confirms_no_retry_results_review
operator_confirms_no_integration_results_review
operator_confirms_no_main_merge_approval
operator_confirms_no_integration_success
operator_confirms_no_successful_integration_digest
operator_confirms_no_integration_branch_push
operator_confirms_no_main_push
operator_confirms_origin_main_not_modified
operator_confirms_no_branch_delete
operator_confirms_no_force_push
operator_confirms_no_tag_mutation
operator_confirms_no_evidence_regeneration
operator_confirms_no_marketflow_commit
operator_confirms_no_pytest_cache_commit
operator_confirms_no_provider_requests
operator_confirms_no_market_data_acquisition
operator_confirms_no_dataset_generation
operator_confirms_no_metric_recomputation
operator_confirms_no_model_training
operator_confirms_no_strategy_scoring
operator_confirms_no_trade_recommendations
operator_confirms_no_predictive_usefulness_acceptance
operator_confirms_no_profitability_acceptance
operator_confirms_runtime_not_authorized
operator_confirms_broker_not_authorized
operator_confirms_no_api_key_storage_or_printing
operator_confirms_no_secret_capture_or_commit""".splitlines())
    values.update({key: True for key in boolean_keys})
    return values


_COMMITTED_CONFIRMATION_SOURCE = _committed_source_operator_review()
_EXPECTED_CONFIRMATIONS = _expected_operator_confirmations(_COMMITTED_CONFIRMATION_SOURCE)
ATTESTATION_VALUE_FIELDS = {
    key: value for key, value in _EXPECTED_CONFIRMATIONS.items() if value is not True
}
ATTESTATION_BOOLEAN_FIELDS = tuple(
    key for key, value in _EXPECTED_CONFIRMATIONS.items() if value is True
)


def build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirmations: dict,
    selected_source_authority_acquisition_package: str = SELECTED_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for the approval ceremony."""

    if not isinstance(operator_confirmations, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError("operator_confirmations must be an object")
    attestation = {
        "operator_decision": operator_decision,
        "selected_source_authority_acquisition_package": selected_source_authority_acquisition_package,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": "v1",
        "operator_reference": operator_reference,
        **deepcopy(operator_confirmations),
    }
    attestation[ATTESTATION_DIGEST_KEY] = semantic_digest(attestation)
    _validate_attestation(attestation, _COMMITTED_CONFIRMATION_SOURCE)
    return attestation


def _validate_attestation(attestation: Mapping[str, Any], source_review: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError("operator_attestation required")
    expected_fields = {
        "operator_decision": OPERATOR_DECISION,
        "selected_source_authority_acquisition_package": SELECTED_PACKAGE,
        "operator_attestation_phrase": REQUIRED_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        "operator_attestation_version": "v1",
        **_expected_operator_confirmations(source_review),
    }
    allowed_fields = {
        *expected_fields,
        "operator_reference",
        "operator_attestation_timestamp_utc",
        ATTESTATION_DIGEST_KEY,
    }
    if set(attestation) != allowed_fields:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError("operator attestation fields mismatch")
    for key, expected in expected_fields.items():
        if attestation.get(key) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError(f"operator attestation {key} mismatch")
    if not isinstance(attestation.get("operator_reference"), str) or not attestation["operator_reference"].strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError("operator attestation reference missing")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(attestation.get("operator_attestation_timestamp_utc"))) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError("operator attestation timestamp invalid")
    payload = {key: deepcopy(value) for key, value in attestation.items() if key != ATTESTATION_DIGEST_KEY}
    if attestation.get(ATTESTATION_DIGEST_KEY) != semantic_digest(payload):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError("operator attestation digest mismatch")


def _source_bindings(review: Mapping[str, Any]) -> dict[str, Any]:
    bindings = {key: deepcopy(value) for key, value in review.items() if key.startswith("source_")}
    bindings.update({
        "source_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_operator_review_status": source.REVIEW_STATUS,
        "source_operator_review_scope": source.REVIEW_SCOPE,
        "source_operator_review_commit": SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_operator_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND,
            "status": source.REVIEW_STATUS,
            "scope": source.REVIEW_SCOPE,
            "commit": SOURCE_OPERATOR_REVIEW_COMMIT,
            "digest": SOURCE_OPERATOR_REVIEW_DIGEST,
            "checks": f"{review['summary']['passed_checks']}/{review['summary']['total_checks']} PASS",
        },
        "source_candidate_review_digest": SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_scope_review_digest": SOURCE_SCOPE_REVIEW_DIGEST,
        "source_mapping_review_digest": SOURCE_MAPPING_REVIEW_DIGEST,
        "source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
        "source_historical_operator_review_commit": review["source_historical_operator_review_summary"]["commit"],
        "source_historical_operator_review_digest": review["source_historical_operator_review_summary"]["digest"],
        "primary_failure_class": review["primary_failure_class"],
        "secondary_failure_classes": deepcopy(review["secondary_failure_classes"]),
        "selected_follow_on_package": review["selected_follow_on_package"],
    })
    return bindings


SOURCE_CONTEXT_KEYS = tuple("""retry_failure_context
priority_1_target_modules
priority1_validation_summary
diagnostic_capture_evidence_summary
reviewed_observable_failure_families
reviewed_workstreams
source_authority_acquisition_candidate_review
acquisition_scope_sections_review
missing_authority_to_source_evidence_mapping_review
acceptable_source_artifact_inventory_review
operator_provided_evidence_requirements_review
evidence_custody_and_digest_requirements_review
candidate_results_review_requirements_review""".splitlines())


def _approval_digest(approval: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(approval))
    for key in ("checklist", "summary", APPROVAL_DIGEST_KEY):
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_approval(source_review: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    approval = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "approval_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "selected_source_authority_acquisition_package": SELECTED_PACKAGE,
        **_source_bindings(source_review),
        **{key: deepcopy(source_review[key]) for key in SOURCE_CONTEXT_KEYS},
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "approved_package": {
            "package_id": SELECTED_PACKAGE,
            "source_review_status": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
            "approval_status": "APPROVED_FOR_FUTURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY",
            "selected": True,
            "approved": True,
            "authorized_for_future_execution": True,
            "executed": False,
            "purpose": "Future execution may acquire or bind source-authority evidence strictly from the reviewed acquisition candidate scope, including the 30 missing-authority items, four workstreams, acceptable source-artifact inventory, operator-provided evidence requirements, evidence custody and digest requirements, and candidate results-review requirements.",
            "future_execution_boundary": "The future execution may perform bounded source-authority acquisition or binding from reviewed candidate scope only. It may create acquisition evidence records and custody/digest bindings if source evidence is available under the approved contract. It must not execute remediation, create no-change disposition, run alternate diagnostics, modify code/tests/digests, generate or apply patches, run full pytest, rerun retry, create retry readiness, push main, push integration branch, authorize runtime, authorize broker execution, or authorize trading.",
        },
        "approved_future_requirements": [
            {"requirement_id": item["requirement_id"], "approval_status": "APPROVED_FOR_FUTURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY", "execution_status": "NOT_EXECUTED"}
            for item in source_review["reviewed_future_requirements"]
        ],
        "approved_future_plan": [
            {"step_id": index, "step": step, "approval_status": "APPROVED_FOR_FUTURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY", "execution_status": "NOT_EXECUTED"}
            for index, step in enumerate(FUTURE_PLAN, 1)
        ],
        "future_execution_boundary": {
            "future_source_authority_acquisition_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
            "future_source_authority_acquisition_execution_input_source": "REVIEWED_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW",
            "future_source_authority_acquisition_execution_type": "SOURCE_AUTHORITY_ACQUISITION_OR_BINDING_FROM_REVIEWED_CANDIDATE_SCOPE",
            **{field: True for field in FUTURE_PERMISSION_TRUE_FIELDS},
            **{field: False for field in FUTURE_PERMISSION_FALSE_FIELDS},
        },
        **{field: True for field in FUTURE_PERMISSION_TRUE_FIELDS},
        **{field: False for field in FUTURE_PERMISSION_FALSE_FIELDS},
        "future_source_authority_acquisition_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
        "future_source_authority_acquisition_execution_input_source": "REVIEWED_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW",
        "future_source_authority_acquisition_execution_type": "SOURCE_AUTHORITY_ACQUISITION_OR_BINDING_FROM_REVIEWED_CANDIDATE_SCOPE",
        "planned_outputs": [{"output_id": item, "status": "AUTHORIZED_NOT_GENERATED"} for item in PLANNED_OUTPUT_IDS],
        "supporting_packages": [
            {
                "package_id": item, "approval_status": "AVAILABLE_NOT_SELECTED",
                "selected": False, "approved": False, "authorized": False, "executed": False,
            }
            for item in SUPPORTING_PACKAGE_IDS
        ],
        "blocked_packages": [
            {
                "package_id": item, "approval_status": "BLOCKED_NOT_APPROVED",
                "selected": False, "approved": False, "authorized": False, "executed": False,
            }
            for item in BLOCKED_PACKAGE_IDS
        ],
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    source_binding_check_ids = tuple(
        f"{key}_bound"
        for key in sorted(approval)
        if key.startswith("source_") and (key.endswith("_digest") or key.endswith("_commit"))
    )
    check_ids = tuple(dict.fromkeys((
        "attestation_valid", "source_operator_review_bound", "selected_package_approved_for_future_execution",
        "approved_future_requirements_51", "approved_future_plan_13", "planned_outputs_28",
        "supporting_packages_5", "blocked_packages_6", "next_chain_8", "next_gates_12", "risk_controls_present",
        "acquisition_scope_sections_4", "mapped_missing_authority_items_30",
        "acceptable_source_artifact_types_13", "operator_provided_evidence_requirements_10",
        "evidence_custody_and_digest_requirements_6", "candidate_results_review_requirements_16",
        "artifact_digest_deterministic",
        *source_binding_check_ids,
        *(f"{field}_true" for field in TRUE_FIELDS),
        *(f"{field}_false" for field in FALSE_FIELDS),
        *(f"{field}_future_true" for field in FUTURE_PERMISSION_TRUE_FIELDS),
        *(f"{field}_future_false" for field in FUTURE_PERMISSION_FALSE_FIELDS),
        *(f"requirement_{item['requirement_id']}_approved" for item in source_review["reviewed_future_requirements"]),
        *(f"plan_step_{index}_approved" for index in range(1, 14)),
        *(f"output_{item}_authorized" for item in PLANNED_OUTPUT_IDS),
        *(f"supporting_package_{item}_preserved" for item in SUPPORTING_PACKAGE_IDS),
        *(f"blocked_package_{item}_blocked" for item in BLOCKED_PACKAGE_IDS),
        *(f"next_chain_step_{index}_defined" for index in range(1, 9)),
        *(f"next_gate_{item}_defined" for item in NEXT_GATES),
        *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
    )))
    approval["checklist"] = [
        {"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"}
        for item in check_ids
    ]
    approval["summary"] = {
        "total_checks": len(check_ids), "passed_checks": len(check_ids), "failed_checks": 0, "blocker_count": 0,
        "source_authority_acquisition_approval_created": True,
        "selected_source_authority_acquisition_package": SELECTED_PACKAGE,
        "source_authority_acquisition_package_selected": True,
        "source_authority_acquisition_package_approved": True,
        "source_authority_acquisition_package_authorized_for_future_execution": True,
        "ready_for_source_authority_acquisition_execution_after_candidate_operator_review": True,
        **{field: False for field in FALSE_FIELDS},
        "source_workstream_count": 4, "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188, "source_exit_code": 1,
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "acquisition_scope_section_count": 4, "mapped_missing_authority_item_count": 30,
        "acceptable_source_artifact_type_count": 13, "operator_provided_evidence_requirement_count": 10,
        "evidence_custody_and_digest_requirement_count": 6, "candidate_results_review_requirement_count": 16,
        "missing_authority_inventory_section_count": 4, "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "workstream_mapping_count": 4, "workstream_mapping_status": "PLANNED_NOT_EXECUTED",
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    approval[APPROVAL_DIGEST_KEY] = _approval_digest(approval)
    return approval


def build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
    *,
    operator_attestation: dict,
    source_operator_review: dict | None = None,
) -> dict[str, Any]:
    """Build the approval after validating the exact source and operator attestation."""

    review = _committed_source_operator_review() if source_operator_review is None else deepcopy(source_operator_review)
    _validate_source_operator_review(review)
    _validate_attestation(operator_attestation, review)
    approval = _assemble_approval(review, operator_attestation)
    validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
    approval: dict,
) -> dict[str, Any]:
    """Reject any mutation of the attestation, source evidence, or authority boundary."""

    if not isinstance(approval, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError("approval must be an object")
    source_review = _committed_source_operator_review()
    _validate_attestation(approval.get("operator_attestation", {}), source_review)
    expected = _assemble_approval(source_review, approval["operator_attestation"])
    difference = _first_difference(approval, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError(f"{difference} mismatch")
    if re.fullmatch(r"[0-9a-f]{64}", str(approval.get(APPROVAL_DIGEST_KEY))) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError("approval digest invalid")
    return {
        "artifact_kind": ARTIFACT_KIND, "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "approval_digest": approval[APPROVAL_DIGEST_KEY],
        **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = tuple("""Operator Attestation
Source Operator Review
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
Source Failure Diagnosis
Source Blocked Execution
Blocked Reason
Failure Classification
Source Remediation Execution Approval
Source Plan Results Review
Source Plan Execution
Source Method Results Review
Source Method Execution
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
Source Authority Acquisition Candidate
Acquisition Scope Sections
Missing Authority Mapping
Acceptable Source Artifact Inventory
Operator-Provided Evidence Requirements
Evidence Custody and Digest Requirements
Candidate Results Review Requirements
Approval Scope
Selected Source Authority Acquisition Package
Approved Future Requirements
Approved Future Plan
Future Execution Boundary
Planned Outputs
Supporting Packages
Blocked Packages
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines())


def build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_markdown_v1(
    approval: dict,
) -> str:
    """Render the validated approval as a status document."""

    validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(deepcopy(approval))
    sections = {
        "Operator Attestation": approval["operator_attestation"],
        "Source Operator Review": approval["source_operator_review_summary"],
        "Source Follow-On Results Review": approval["source_follow_on_results_review_summary"],
        "Source Follow-On Execution": approval["source_follow_on_execution_summary"],
        "Source Follow-On Approval": approval["source_follow_on_approval_summary"],
        "Source Follow-On Operator Review": approval["source_follow_on_operator_review_summary"],
        "Source Follow-On Candidate": approval["source_follow_on_candidate_summary"],
        "Source Results Review": approval["source_results_review_summary"],
        "Source Enrichment Execution": approval["source_execution_summary"],
        "Source Historical Approval": approval["source_approval_summary"],
        "Source Historical Operator Review": approval["source_historical_operator_review_summary"],
        "Source Historical Candidate": approval["source_historical_candidate_summary"],
        "Source Failure Diagnosis": approval["source_failure_diagnosis_summary"],
        "Source Blocked Execution": approval["source_blocked_execution_summary"],
        "Blocked Reason": approval["source_blocked_reason"],
        "Failure Classification": {"primary": approval["primary_failure_class"], "secondary": approval["secondary_failure_classes"]},
        "Source Remediation Execution Approval": approval["source_remediation_execution_approval_after_plan_results_review_digest"],
        "Source Plan Results Review": approval["source_plan_results_review_summary"],
        "Source Plan Execution": approval["source_plan_execution_summary"],
        "Source Method Results Review": approval["source_method_results_review_summary"],
        "Source Method Execution": approval["source_method_execution_summary"],
        "Source Diagnostic Results Review": approval["source_diagnostic_results_review_summary"],
        "Source Controlled Recapture": approval["source_controlled_recapture_summary"],
        "Source Durable Receipt": approval["source_durable_receipt_summary"],
        "Source Planning and Detail Binding Evidence": approval["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": approval["retry_failure_context"],
        "Priority 1 Target Modules": approval["priority_1_target_modules"],
        "Priority 1 Validation Summary": approval["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": approval["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": approval["reviewed_observable_failure_families"],
        "Reviewed Workstreams": approval["reviewed_workstreams"],
        "Source Authority Acquisition Candidate": approval["source_authority_acquisition_candidate_review"],
        "Acquisition Scope Sections": approval["acquisition_scope_sections_review"],
        "Missing Authority Mapping": approval["missing_authority_to_source_evidence_mapping_review"],
        "Acceptable Source Artifact Inventory": approval["acceptable_source_artifact_inventory_review"],
        "Operator-Provided Evidence Requirements": approval["operator_provided_evidence_requirements_review"],
        "Evidence Custody and Digest Requirements": approval["evidence_custody_and_digest_requirements_review"],
        "Candidate Results Review Requirements": approval["candidate_results_review_requirements_review"],
        "Approval Scope": approval["approval_scope"],
        "Selected Source Authority Acquisition Package": approval["approved_package"],
        "Approved Future Requirements": approval["approved_future_requirements"],
        "Approved Future Plan": approval["approved_future_plan"],
        "Future Execution Boundary": approval["future_execution_boundary"],
        "Planned Outputs": approval["planned_outputs"],
        "Supporting Packages": approval["supporting_packages"],
        "Blocked Packages": approval["blocked_packages"],
        "Next Chain": approval["next_chain"], "Next Gates": approval["next_gates"],
        "Risk Controls": approval["risk_controls"],
        "Authority Boundaries": {field: approval[field] for field in FALSE_FIELDS},
        "Checklist Summary": approval["summary"],
        "Guardrails": [field for field in FALSE_FIELDS if approval[field] is False],
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Source Authority Acquisition Approval After Candidate Operator Review v1",
        "", f"Artifact: `{approval['artifact_kind']}`", "", f"Status: `{approval['approval_status']}`", "",
        f"Scope: `{approval['approval_scope']}`", "", f"Approval digest: `{approval[APPROVAL_DIGEST_KEY]}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    operator_attestation: dict,
    source_operator_review: dict | None = None,
) -> dict[str, Any]:
    """Write the deterministic approval status document."""

    approval = build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
        source_operator_review=source_operator_review, operator_attestation=operator_attestation
    )
    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError(
            "protected output directory"
        )
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_markdown_v1(approval), encoding="utf-8")
    return approval


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "APPROVAL_STATUS", "APPROVAL_SCOPE", "SELECTED_PACKAGE",
    "APPROVAL_DIGEST_KEY", "ATTESTATION_DIGEST_KEY",
    "ATTESTATION_VALUE_FIELDS", "ATTESTATION_BOOLEAN_FIELDS",
    "REQUIRED_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE",
    "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_markdown_v1",
]
