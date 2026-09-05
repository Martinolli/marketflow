"""Approve source-authority enrichment planning for future execution only."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVED_AFTER_BLOCKED_EXECUTION_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVED_AFTER_BLOCKED_EXECUTION"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_digest"
SOURCE_OPERATOR_REVIEW_COMMIT = "3c8fbf8fe4ac11c2122455d05fa0d82c67e05ddf"
SOURCE_OPERATOR_REVIEW_DIGEST = "8c3715141f8a52643dd7262406dce003a4868db279d66b74164c7b0c9d7baf51"
SELECTED_PACKAGE = source.RECOMMENDED_PACKAGE
OPERATOR_DECISION = "APPROVE_SOURCE_AUTHORITY_ENRICHMENT_AFTER_BLOCKED_REMEDIATION_EXECUTION"
OPERATOR_ATTESTATION_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_attestation_v1"
REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1 = (
    "APPROVE MARKETFLOW RETRY FAILURE SOURCE AUTHORITY ENRICHMENT "
    "PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION AFTER BLOCKED REMEDIATION EXECUTION "
    "FOR FUTURE EXECUTION ONLY NO SOURCE AUTHORITY ENRICHMENT NOW NO NO CHANGE DISPOSITION NOW "
    "NO ALTERNATE DIAGNOSTICS NOW NO REMEDIATION NOW NO CODE CHANGES NOW NO TEST CHANGES NOW "
    "NO DIGEST UPDATES NOW NO PATCH NOW NO PYTEST NOW NO RETRY NO MAIN PUSH "
    "SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)
APPROVED_ONLY = "APPROVED_FOR_FUTURE_SOURCE_AUTHORITY_ENRICHMENT_EXECUTION_AFTER_BLOCKED_REMEDIATION_ONLY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_AFTER_BLOCKED_EXECUTION_V1"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION = source.PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION
PACKAGE_CREATE_NO_CHANGE_DISPOSITION_REVIEW_FOR_CURRENT_ROOT_PRIORITY1_PASSING_STATE = source.PACKAGE_CREATE_NO_CHANGE_DISPOSITION_REVIEW_FOR_CURRENT_ROOT_PRIORITY1_PASSING_STATE
PACKAGE_REQUEST_ALTERNATE_BOUNDED_DIAGNOSTIC_CAPTURE_FOR_DETACHED_RETRY_FAILURES = source.PACKAGE_REQUEST_ALTERNATE_BOUNDED_DIAGNOSTIC_CAPTURE_FOR_DETACHED_RETRY_FAILURES
PACKAGE_COMPARE_CURRENT_ROOT_PRIORITY1_PASSING_STATE_TO_DETACHED_RETRY_CONTEXT = source.PACKAGE_COMPARE_CURRENT_ROOT_PRIORITY1_PASSING_STATE_TO_DETACHED_RETRY_CONTEXT
PACKAGE_CREATE_NO_CHANGE_RETRY_CANDIDATE_CRITERIA_ONLY = source.PACKAGE_CREATE_NO_CHANGE_RETRY_CANDIDATE_CRITERIA_ONLY
PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_EXTERNAL_SOURCE_AUTHORITY = source.PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_EXTERNAL_SOURCE_AUTHORITY
PACKAGE_DIRECT_REMEDIATION_DESPITE_NO_SOURCE_AUTHORITY = source.PACKAGE_DIRECT_REMEDIATION_DESPITE_NO_SOURCE_AUTHORITY
PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_TO_MATCH_CURRENT_ROOT_PASSING_STATE = source.PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_TO_MATCH_CURRENT_ROOT_PASSING_STATE
PACKAGE_REWRITE_TESTS_OR_SKIP_FAILURES_WITHOUT_SOURCE_AUTHORITY = source.PACKAGE_REWRITE_TESTS_OR_SKIP_FAILURES_WITHOUT_SOURCE_AUTHORITY
PACKAGE_NEW_RETRY_BECAUSE_PRIORITY1_CURRENT_ROOT_PASSES = source.PACKAGE_NEW_RETRY_BECAUSE_PRIORITY1_CURRENT_ROOT_PASSES
PACKAGE_MAIN_MERGE_BECAUSE_CURRENT_ROOT_REGRESSION_PREVIOUSLY_PASSED = source.PACKAGE_MAIN_MERGE_BECAUSE_CURRENT_ROOT_REGRESSION_PREVIOUSLY_PASSED
PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY = source.PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY

ATTESTATION_VALUE_FIELDS = {
    "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_failure_diagnosis_digest": source.source.SOURCE_FAILURE_DIAGNOSIS_DIGEST,
    "operator_confirms_source_blocked_execution_commit": source.source.source.SOURCE_BLOCKED_EXECUTION_COMMIT,
    "operator_confirms_source_blocked_reason": source.source.source.SOURCE_BLOCKED_REASON,
    "operator_confirms_source_blocked_manifest_digest": source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
    "operator_confirms_primary_failure_class": source.source.source.PRIMARY_FAILURE_CLASS,
    "operator_confirms_source_approval_digest": source.source.source.source.SOURCE_APPROVAL_DIGEST,
    "operator_confirms_selected_remediation_execution_package": source.source.source.source.SELECTED_PACKAGE,
    "operator_confirms_source_plan_results_review_digest": source.source.SOURCE_BINDINGS["source_remediation_plan_or_execution_results_review_after_method_results_review_digest"],
    "operator_confirms_source_targeted_plan_review_digest": source.source.SOURCE_BINDINGS["source_targeted_remediation_plan_review_digest"],
    "operator_confirms_source_workstream_mapping_review_digest": source.source.SOURCE_BINDINGS["source_workstream_mapping_review_digest"],
    "operator_confirms_source_plan_execution_digest": source.source.SOURCE_BINDINGS["source_remediation_plan_or_execution_after_method_results_review_digest"],
    "operator_confirms_source_targeted_remediation_plan_digest": source.source.SOURCE_BINDINGS["source_targeted_remediation_plan_digest"],
    "operator_confirms_source_workstream_mapping_digest": source.source.SOURCE_BINDINGS["source_workstream_mapping_digest"],
    "operator_confirms_source_method_results_review_digest": source.source.SOURCE_BINDINGS["source_remediation_or_method_results_review_after_diagnostic_capture_digest"],
    "operator_confirms_source_method_execution_digest": source.source.SOURCE_BINDINGS["source_remediation_or_method_execution_after_diagnostic_capture_digest"],
    "operator_confirms_source_diagnostic_results_review_digest": source.source.SOURCE_BINDINGS["source_receipt_recovery_or_recapture_results_review_digest"],
    "operator_confirms_source_controlled_recapture_execution_digest": source.source.SOURCE_BINDINGS["source_receipt_recovery_or_recapture_execution_digest"],
    "operator_confirms_source_durable_receipt_digest": source.source.SOURCE_BINDINGS["source_receipt_recovery_or_recapture_receipt_digest"],
    "operator_confirms_source_durable_receipt_path": source.source.SOURCE_BINDINGS["source_durable_receipt_path"],
    "operator_confirms_source_prior_diagnostic_failure_diagnosis_digest": source.source.SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
    "operator_confirms_source_prior_diagnostic_blocked_reason": source.source.SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"],
    "operator_confirms_source_planning_execution_digest": source.source.SOURCE_BINDINGS["source_planning_execution_digest"],
    "operator_confirms_source_complete_29_row_binding_digest": source.source.SOURCE_BINDINGS["source_complete_29_row_binding_digest"],
    "operator_confirms_source_materialized_payload_digest": source.source.SOURCE_BINDINGS["source_materialized_payload_digest"],
    "operator_confirms_source_recovery_detail_digest": source.source.SOURCE_BINDINGS["source_recovery_detail_digest"],
    "operator_confirms_source_module_grouping_digest": source.source.SOURCE_BINDINGS["source_module_grouping_digest"],
    "operator_confirms_retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
    "operator_confirms_source_stdout_hash": source.source.SOURCE_CORE["source_stdout_sha256"],
    "operator_confirms_source_stderr_hash": source.source.SOURCE_CORE["source_stderr_sha256"],
    "operator_confirms_selected_source_authority_enrichment_package": SELECTED_PACKAGE,
}

ATTESTATION_BOOLEAN_FIELDS = tuple(
    """operator_confirms_secondary_failure_classes
operator_confirms_retry_failure_counts
operator_confirms_priority_1_top_module_paths
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
operator_confirms_approval_scope_only
operator_confirms_no_source_authority_enrichment_now
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
operator_confirms_no_new_retry_candidate
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
operator_confirms_no_secret_capture_or_commit""".splitlines()
)

TRUE_FIELDS = (
    "source_authority_or_no_change_disposition_approval_after_blocked_execution_created",
    "source_authority_or_no_change_disposition_package_selected",
    "source_authority_or_no_change_disposition_package_approved",
    "source_authority_or_no_change_disposition_package_authorized",
    "ready_for_source_authority_or_no_change_disposition_execution_after_blocked_execution",
)

FALSE_FIELDS = tuple(
    """source_authority_or_no_change_disposition_execution_performed
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
pytest_performed_in_approval
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_approval
diagnostic_output_analyzed_in_approval
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
trade_recommendations_generated""".splitlines()
)

FUTURE_PERMISSION_TRUE_FIELDS = (
    "future_execution_may_create_source_authority_enrichment_plan",
    "future_execution_may_create_missing_authority_inventory",
    "future_execution_may_map_reviewed_workstreams_to_missing_source_authority",
    "future_execution_may_define_evidence_requirements",
    "future_execution_may_define_no_change_disposition_inputs",
    "future_execution_may_define_alternate_diagnostic_inputs",
    "future_execution_may_define_reviewed_basis_needed_before_retry_candidate",
)
FUTURE_PERMISSION_FALSE_FIELDS = (
    "future_execution_may_execute_remediation",
    "future_execution_may_modify_production_code",
    "future_execution_may_modify_existing_tests",
    "future_execution_may_update_expected_digests",
    "future_execution_may_generate_or_apply_patch",
    "future_execution_may_run_pytest",
    "future_execution_may_run_full_pytest",
    "future_execution_may_run_retry",
    "future_execution_may_push_main",
    "future_execution_may_push_integration_branch",
    "future_execution_may_create_retry_candidate",
    "future_execution_may_claim_root_cause",
    "future_execution_may_claim_retry_success",
    "future_execution_may_create_main_merge_approval",
    "future_source_authority_or_no_change_disposition_execution_executed",
)

APPROVED_FUTURE_REQUIREMENTS = tuple(source.source.FUTURE_REQUIREMENT_IDS)
APPROVED_FUTURE_PLAN = (
    "Bind this approval and source operator-review evidence.",
    "Bind source candidate, failure diagnosis, blocked execution reason, manifest, and Priority 1 validation facts.",
    "Bind approval, operator-review, candidate, plan review, plan execution, method, diagnostic, receipt, planning, detail-binding, recovery, module-grouping, and staged-inventory digests.",
    "Bind retry failure counts, Priority 1 modules, observable families, and reviewed workstreams.",
    "Preserve the no-source-authority failure class and confirm no retained remediation change exists.",
    "Execute the selected source-authority enrichment package only under a separate execution task.",
    "Create missing-authority inventory and evidence requirements without remediation.",
    "Do not perform no-change disposition, alternate diagnostics, remediation, retry, or main merge in the enrichment execution unless separately approved.",
    "Preserve that Priority 1 focused validation is not retry evidence.",
    "Require results review before any remediation, retry candidate, no-change retry path, or main-merge path.",
    "Preserve the failed detached retry as authoritative.",
    "Keep provider, runtime, broker, and trading authority closed.",
)
AUTHORIZED_OUTPUT_IDS = tuple(
    """source_authority_or_no_change_disposition_approval_after_blocked_execution_manifest
source_operator_review_binding_report
source_candidate_binding_report
source_failure_diagnosis_binding_report
source_blocked_execution_binding_report
source_approval_binding_report
source_plan_results_review_binding_report
source_plan_execution_binding_report
source_method_and_diagnostic_binding_report
source_planning_detail_recovery_binding_report
retry_failure_context_report
priority1_validation_disposition_report
reviewed_workstream_authority_gap_report
approved_source_authority_enrichment_package_report
missing_authority_inventory_placeholder
source_evidence_requirements_placeholder
no_change_disposition_input_requirements_report
alternate_diagnostic_input_requirements_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
)
SUPPORTING_PACKAGE_IDS = (
    PACKAGE_CREATE_NO_CHANGE_DISPOSITION_REVIEW_FOR_CURRENT_ROOT_PRIORITY1_PASSING_STATE,
    PACKAGE_REQUEST_ALTERNATE_BOUNDED_DIAGNOSTIC_CAPTURE_FOR_DETACHED_RETRY_FAILURES,
    PACKAGE_COMPARE_CURRENT_ROOT_PRIORITY1_PASSING_STATE_TO_DETACHED_RETRY_CONTEXT,
    PACKAGE_CREATE_NO_CHANGE_RETRY_CANDIDATE_CRITERIA_ONLY,
    PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_EXTERNAL_SOURCE_AUTHORITY,
)
BLOCKED_PACKAGE_IDS = (
    PACKAGE_DIRECT_REMEDIATION_DESPITE_NO_SOURCE_AUTHORITY,
    PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_TO_MATCH_CURRENT_ROOT_PASSING_STATE,
    PACKAGE_REWRITE_TESTS_OR_SKIP_FAILURES_WITHOUT_SOURCE_AUTHORITY,
    PACKAGE_NEW_RETRY_BECAUSE_PRIORITY1_CURRENT_ROOT_PASSES,
    PACKAGE_MAIN_MERGE_BECAUSE_CURRENT_ROOT_REGRESSION_PREVIOUSLY_PASSED,
    PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY,
)
NEXT_CHAIN = (
    "Source Authority or No-Change Disposition Execution After Blocked Execution v1, if approved.",
    "Source Authority or No-Change Disposition Results Review v1.",
    "Conditional remediation execution candidate, alternate diagnostic candidate, no-change retry candidate, or hold disposition only if results review supports it.",
    "New Integration Branch Retry Candidate v1, only after a reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple(
    """source_authority_or_no_change_disposition_execution_after_blocked_execution_if_approved
source_authority_or_no_change_disposition_results_review
conditional_follow_on_candidate_if_results_review_supports
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()
)
_REVIEW_PREFIX = "operator_review_after_blocked_execution_does_not_"
_APPROVAL_PREFIX = "approval_after_blocked_execution_does_not_"
RISK_CONTROLS = tuple(
    item.replace(_REVIEW_PREFIX, _APPROVAL_PREFIX, 1)
    for item in source.RISK_CONTROLS
    if item.startswith(_REVIEW_PREFIX)
    and item not in {
        f"{_REVIEW_PREFIX}select_package",
        f"{_REVIEW_PREFIX}approve_package",
        f"{_REVIEW_PREFIX}authorize_package",
    }
) + tuple(
    """selected_source_authority_enrichment_package_approved_for_future_execution_only
future_execution_limited_to_source_authority_enrichment_plan
future_execution_must_not_perform_remediation_without_separate_review_and_approval
future_execution_must_not_create_retry_candidate_without_reviewed_basis
future_execution_must_preserve_detached_retry_failed_status
future_execution_results_review_required_before_follow_on_path
source_authority_approval_is_not_source_authority_enrichment_execution
source_authority_candidate_is_not_source_authority_enrichment_execution
no_change_disposition_option_is_not_no_change_disposition_execution
alternate_diagnostic_option_is_not_diagnostic_execution
blocked_remediation_execution_remains_source_evidence
failure_diagnosis_remains_source_evidence
source_candidate_operator_review_remains_source_evidence
blocked_reason_remains_authoritative_for_approval
source_authority_gap_is_not_root_cause
passing_priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
no_change_records_means_no_remediation_success
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_execution_required_after_approval
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


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError(ValueError):
    """Raised when attestation, evidence, or approval boundaries are invalid."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() is not None


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
        "operator_attestation_phrase": REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        **ATTESTATION_VALUE_FIELDS,
    }
    allowed_fields = {*expected, "operator_attestation_timestamp_utc", "operator_reference", *ATTESTATION_BOOLEAN_FIELDS}
    if set(attestation) != allowed_fields:
        raise error("operator attestation fields mismatch")
    for field, expected_value in expected.items():
        if attestation.get(field) != expected_value:
            raise error(f"{field} mismatch")
    if not _iso_utc(attestation.get("operator_attestation_timestamp_utc")):
        raise error("operator_attestation_timestamp_utc invalid")
    if not isinstance(attestation.get("operator_reference"), str) or not attestation["operator_reference"].strip():
        raise error("operator_reference missing")
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise error(f"{field} must be true")


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirmations: dict,
    selected_source_authority_or_no_change_disposition_package: str = SELECTED_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict[str, Any]:
    """Build and validate the exact non-secret operator attestation."""

    if not isinstance(operator_confirmations, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError("operator_confirmations must be an object")
    attestation = {
        "operator_reference": operator_reference,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_phrase": operator_attestation_phrase,
        "selected_source_authority_or_no_change_disposition_package": selected_source_authority_or_no_change_disposition_package,
        "operator_decision": operator_decision,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        **deepcopy(operator_confirmations),
    }
    _validate_attestation(attestation)
    return attestation


def _validated_source_review(source_operator_review: dict | None) -> dict[str, Any]:
    review = (
        source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1()
        if source_operator_review is None
        else deepcopy(source_operator_review)
    )
    try:
        source.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(review)
    except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError("source operator review validation failed") from exc
    if review.get(source.OPERATOR_REVIEW_DIGEST_KEY) != SOURCE_OPERATOR_REVIEW_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError("source operator review digest mismatch")
    return review


def _approved_package() -> dict[str, Any]:
    return {
        "package_id": SELECTED_PACKAGE,
        "approval_status": APPROVED_ONLY,
        "selected": True,
        "approved": True,
        "authorized_for_future_execution": True,
        "executed": False,
        "purpose": "Future execution may create a source-authority enrichment plan to identify what evidence would be required before any concrete source, test, digest, fixture, schema, export, remediation, no-change disposition, alternate diagnostic, retry candidate, or main-merge path can be justified. This approval does not authorize remediation, retry, full pytest, main merge, runtime use, broker execution, or trading.",
    }


def _approved_requirements() -> list[dict[str, Any]]:
    return [{"requirement_id": item, "approval_status": APPROVED_ONLY, "execution_status": "NOT_EXECUTED"} for item in APPROVED_FUTURE_REQUIREMENTS]


def _approved_plan() -> list[dict[str, Any]]:
    return [{"step_id": index, "action": action, "approval_status": APPROVED_ONLY, "execution_status": "NOT_EXECUTED"} for index, action in enumerate(APPROVED_FUTURE_PLAN, 1)]


def _authorized_outputs() -> list[dict[str, Any]]:
    return [{"output_id": item, "authorization_status": "AUTHORIZED_NOT_GENERATED"} for item in AUTHORIZED_OUTPUT_IDS]


def _supporting_packages() -> list[dict[str, Any]]:
    return [{"package_id": item, "approval_status": "AVAILABLE_NOT_SELECTED", "selected": False, "approved": False, "authorized": False, "executed": False} for item in SUPPORTING_PACKAGE_IDS]


def _blocked_packages() -> list[dict[str, Any]]:
    return [{"package_id": item, "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False, "authorized": False, "executed": False} for item in BLOCKED_PACKAGE_IDS]


def _source_bindings() -> dict[str, Any]:
    bindings = deepcopy(source.SOURCE_BINDINGS)
    bindings.update(
        {
            "source_operator_review_artifact_kind": source.ARTIFACT_KIND,
            "source_operator_review_status": source.REVIEW_STATUS,
            "source_operator_review_scope": source.REVIEW_SCOPE,
            "source_operator_review_commit": SOURCE_OPERATOR_REVIEW_COMMIT,
            "source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        }
    )
    return bindings


SOURCE_BINDINGS = _source_bindings()


def _approval_body(attestation: Mapping[str, Any], source_review: Mapping[str, Any]) -> dict[str, Any]:
    summary_fields = (
        "source_candidate_summary", "source_failure_diagnosis_summary", "source_blocked_execution_summary",
        "source_approval_summary", "source_operator_review_and_candidate_summary", "source_plan_results_review_summary",
        "source_plan_execution_summary", "source_targeted_remediation_plan_summary", "source_workstream_mapping_summary",
        "source_method_results_review_summary", "source_method_execution_summary", "source_diagnostic_results_review_summary",
        "source_controlled_recapture_summary", "source_durable_receipt_summary", "source_receipt_loss_history_summary",
        "source_planning_and_detail_binding_summary",
    )
    body: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
        "historical_selected_remediation_execution_package": source.source.source.source.SELECTED_PACKAGE,
        "created_offline": True,
        "governance_only": True,
        "approval_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        **SOURCE_BINDINGS,
        "source_operator_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND,
            "review_status": source.REVIEW_STATUS,
            "review_scope": source.REVIEW_SCOPE,
            "commit": SOURCE_OPERATOR_REVIEW_COMMIT,
            "digest": SOURCE_OPERATOR_REVIEW_DIGEST,
            "checklist": "256/256 PASS",
        },
        **{field: deepcopy(source_review[field]) for field in summary_fields},
        "retry_failure_context": deepcopy(source_review["retry_failure_context"]),
        "priority_1_target_modules": deepcopy(source_review["priority_1_target_modules"]),
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "priority1_validation_summary": deepcopy(source_review["priority1_validation_summary"]),
        "priority1_pre_change_validation_passed": True,
        "priority1_pre_change_validation_passed_count": 675,
        "priority1_post_change_validation_passed": True,
        "priority1_post_change_validation_passed_count": 675,
        "priority1_post_change_stdout_sha256": source_review["priority1_post_change_stdout_sha256"],
        "priority1_post_change_stderr_sha256": source_review["priority1_post_change_stderr_sha256"],
        "source_exit_code": 1,
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_stdout_sha256": source_review["source_stdout_sha256"],
        "source_stderr_sha256": source_review["source_stderr_sha256"],
        "diagnostic_capture_evidence_summary": deepcopy(source_review["diagnostic_capture_evidence_summary"]),
        "primary_failure_class": source_review["primary_failure_class"],
        "secondary_failure_classes": deepcopy(source_review["secondary_failure_classes"]),
        "reviewed_observable_failure_families": deepcopy(source_review["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "reviewed_workstreams": deepcopy(source_review["reviewed_workstreams"]),
        "source_workstream_count": 4,
        "approved_package": _approved_package(),
        "approved_future_requirements": _approved_requirements(),
        "approved_future_plan": _approved_plan(),
        "future_source_authority_or_no_change_disposition_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
        "future_source_authority_or_no_change_disposition_execution_input_source": "REVIEWED_OPERATOR_REVIEW_AND_FAILURE_DIAGNOSIS_AFTER_BLOCKED_REMEDIATION",
        "future_source_authority_or_no_change_disposition_execution_type": "SOURCE_AUTHORITY_ENRICHMENT_PLAN_AFTER_BLOCKED_REMEDIATION",
        **{field: True for field in FUTURE_PERMISSION_TRUE_FIELDS},
        **{field: False for field in FUTURE_PERMISSION_FALSE_FIELDS},
        "authorized_planned_outputs": _authorized_outputs(),
        "supporting_packages": _supporting_packages(),
        "blocked_packages": _blocked_packages(),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
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
    return body


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [_check(f"{field}_bound", expected, approval.get(field)) for field, expected in SOURCE_BINDINGS.items()]
    checks.extend(
        (
            _check("selected_package", SELECTED_PACKAGE, approval.get("selected_source_authority_or_no_change_disposition_package")),
            _check("operator_decision", OPERATOR_DECISION, approval.get("operator_attestation", {}).get("operator_decision")),
            _check("attestation_phrase", REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1, approval.get("operator_attestation", {}).get("operator_attestation_phrase")),
            _check("approved_package", _approved_package(), approval.get("approved_package")),
            _check("approved_requirements_50", _approved_requirements(), approval.get("approved_future_requirements")),
            _check("approved_plan_12", _approved_plan(), approval.get("approved_future_plan")),
            _check("authorized_outputs_21", _authorized_outputs(), approval.get("authorized_planned_outputs")),
            _check("supporting_packages_5", _supporting_packages(), approval.get("supporting_packages")),
            _check("blocked_packages_6", _blocked_packages(), approval.get("blocked_packages")),
            _check("priority_1_total_612", 612, approval.get("priority_1_total_nodeids")),
            _check("top_10_total_1069", 1069, approval.get("top_10_count_sum")),
            _check("module_summary_29", 29, approval.get("module_summary_module_count")),
            _check("failed_or_errored_1404", 1404, approval.get("failed_or_errored_nodeids_count")),
            _check("priority1_pre_675", 675, approval.get("priority1_pre_change_validation_passed_count")),
            _check("priority1_post_675", 675, approval.get("priority1_post_change_validation_passed_count")),
            _check("families_4", 4, approval.get("observable_failure_family_count")),
            _check("observable_items_188", 188, approval.get("total_observable_evidence_items")),
            _check("workstreams_4", 4, approval.get("source_workstream_count")),
            _check("future_execution_boundary", "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED", approval.get("future_source_authority_or_no_change_disposition_execution_status")),
            _check("next_chain", list(NEXT_CHAIN), approval.get("next_chain")),
            _check("next_gates", list(NEXT_GATES), approval.get("next_gates")),
            _check("risk_controls", list(RISK_CONTROLS), approval.get("risk_controls")),
            _check("no_tracked_marketflow_files", True, approval.get("no_tracked_marketflow_files")),
            _check("no_tracked_pytest_cache_files", True, approval.get("no_tracked_pytest_cache_files")),
        )
    )
    checks.extend(_check(f"{field}_true", True, approval.get(field)) for field in TRUE_FIELDS + FUTURE_PERMISSION_TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, approval.get(field)) for field in FALSE_FIELDS + FUTURE_PERMISSION_FALSE_FIELDS)
    checks.extend(_check(f"attestation_{field}", expected, approval.get("operator_attestation", {}).get(field)) for field, expected in ATTESTATION_VALUE_FIELDS.items())
    checks.extend(_check(f"attestation_{field}", True, approval.get("operator_attestation", {}).get(field)) for field in ATTESTATION_BOOLEAN_FIELDS)
    return checks


def _summary(approval: Mapping[str, Any]) -> dict[str, Any]:
    checks = approval["checklist"]
    passed = sum(item["status"] == PASS for item in checks)
    summary = {"total_checks": len(checks), "passed_checks": passed, "failed_checks": len(checks) - passed, "blocker_count": len(checks) - passed}
    for field in TRUE_FIELDS + FALSE_FIELDS + FUTURE_PERMISSION_TRUE_FIELDS + FUTURE_PERMISSION_FALSE_FIELDS:
        summary[field] = approval[field]
    summary.update(
        {
            "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
            "approved_package_status": APPROVED_ONLY,
            "source_blocked_reason": source.source.source.SOURCE_BLOCKED_REASON,
            "primary_failure_class": source.source.source.PRIMARY_FAILURE_CLASS,
            "secondary_failure_classes": list(source.source.source.SECONDARY_FAILURE_CLASSES),
            "approved_future_requirement_count": 50,
            "approved_future_plan_step_count": 12,
            "authorized_planned_output_count": 21,
            "supporting_package_count": 5,
            "blocked_package_count": 6,
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
            "predictive_usefulness_accepted": False,
            "profitability_accepted": False,
            "runtime_authorized": False,
            "broker_execution_authorized": False,
        }
    )
    return summary


def _approval_digest(approval: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(approval))
    for field in ("checklist", "summary", APPROVAL_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(
    *, operator_attestation: dict, source_operator_review: dict | None = None,
) -> dict[str, Any]:
    """Build an attestation-bound approval without executing enrichment."""

    _validate_attestation(operator_attestation)
    source_review = _validated_source_review(source_operator_review)
    approval = _approval_body(operator_attestation, source_review)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval)
    approval[APPROVAL_DIGEST_KEY] = _approval_digest(approval)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(
    approval: dict,
) -> dict[str, Any]:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError
    if not isinstance(approval, dict):
        raise error("approval must be an object")
    attestation = approval.get("operator_attestation")
    if not isinstance(attestation, dict):
        raise error("operator_attestation missing")
    _validate_attestation(attestation)
    source_review = _validated_source_review(None)
    expected = _approval_body(attestation, source_review)
    for field, expected_value in expected.items():
        if approval.get(field) != expected_value:
            raise error(f"{field} mismatch")
    checklist = _checklist(approval)
    if approval.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if approval.get("summary") != _summary(approval):
        raise error("summary mismatch")
    digest = approval.get(APPROVAL_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _approval_digest(approval):
        raise error("approval digest missing or changed")
    return {"artifact_kind": ARTIFACT_KIND, "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE, "approval_digest": digest, **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


MARKDOWN_SECTIONS = (
    "Operator Attestation", "Source Operator Review", "Source Candidate", "Source Failure Diagnosis",
    "Source Blocked Execution", "Blocked Reason", "Failure Classification", "Source Approval",
    "Source Plan Results Review", "Source Plan Execution", "Source Targeted Remediation Plan",
    "Source Workstream Mapping", "Source Method Results Review", "Source Method Execution",
    "Source Diagnostic Results Review", "Source Controlled Recapture", "Source Durable Receipt",
    "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Priority 1 Target Modules",
    "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "Approval Scope", "Selected Source Authority Package",
    "Approved Future Requirements", "Approved Future Plan", "Future Execution Boundary",
    "Planned Outputs", "Supporting Packages", "Blocked Packages", "Next Chain", "Next Gates",
    "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_markdown_v1(
    approval: dict,
) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(deepcopy(approval))
    sections = {
        "Operator Attestation": {key: approval["operator_attestation"][key] for key in ("operator_decision", "operator_reference", "operator_attestation_timestamp_utc", "operator_attestation_version")},
        "Source Operator Review": approval["source_operator_review_summary"],
        "Source Candidate": approval["source_candidate_summary"],
        "Source Failure Diagnosis": approval["source_failure_diagnosis_summary"],
        "Source Blocked Execution": approval["source_blocked_execution_summary"],
        "Blocked Reason": approval["source_blocked_reason"],
        "Failure Classification": {"primary": approval["primary_failure_class"], "secondary": approval["secondary_failure_classes"], "approval_digest": approval[APPROVAL_DIGEST_KEY]},
        "Source Approval": approval["source_approval_summary"],
        "Source Plan Results Review": approval["source_plan_results_review_summary"],
        "Source Plan Execution": approval["source_plan_execution_summary"],
        "Source Targeted Remediation Plan": approval["source_targeted_remediation_plan_summary"],
        "Source Workstream Mapping": approval["source_workstream_mapping_summary"],
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
        "Approval Scope": approval["approval_scope"],
        "Selected Source Authority Package": approval["approved_package"],
        "Approved Future Requirements": approval["approved_future_requirements"],
        "Approved Future Plan": approval["approved_future_plan"],
        "Future Execution Boundary": {field: approval[field] for field in ("future_source_authority_or_no_change_disposition_execution_status", "future_source_authority_or_no_change_disposition_execution_input_source", "future_source_authority_or_no_change_disposition_execution_type", *FUTURE_PERMISSION_TRUE_FIELDS, *FUTURE_PERMISSION_FALSE_FIELDS)},
        "Planned Outputs": approval["authorized_planned_outputs"],
        "Supporting Packages": approval["supporting_packages"],
        "Blocked Packages": approval["blocked_packages"],
        "Next Chain": approval["next_chain"],
        "Next Gates": approval["next_gates"],
        "Risk Controls": approval["risk_controls"],
        "Authority Boundaries": {"approval_only": True, "future_execution_ready": True, "execution_performed": False, "retry_ready": False, "runtime_use": approval["runtime_use"]},
        "Checklist Summary": approval["summary"],
        "Guardrails": list(FALSE_FIELDS + FUTURE_PERMISSION_FALSE_FIELDS),
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Approval After Blocked Execution v1", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", f"```text\n{sections[title]!r}\n```", ""))
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(
    output_dir: str | Path, *, operator_attestation: dict, source_operator_review: dict | None = None,
) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError("protected output directory")
    approval = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(operator_attestation=operator_attestation, source_operator_review=source_operator_review)
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError("output exists")
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_markdown_v1(approval), encoding="utf-8")
    return approval


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVED_AFTER_BLOCKED_EXECUTION_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVED_AFTER_BLOCKED_EXECUTION = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_DIGEST_KEY = APPROVAL_DIGEST_KEY
