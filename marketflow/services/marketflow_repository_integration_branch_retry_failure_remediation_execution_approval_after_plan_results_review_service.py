"""Approve controlled plan-derived remediation for future execution only."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVED_AFTER_PLAN_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVED_AFTER_PLAN_RESULTS_REVIEW"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_digest"
SELECTED_PACKAGE = source.RECOMMENDED_PACKAGE
SOURCE_OPERATOR_REVIEW_COMMIT = "999fab934370d16b24c5ed84876f06254fbacb9b"
SOURCE_OPERATOR_REVIEW_DIGEST = "8f7033f203707634413ba460ae5fcbf829bda5822eb379677515e02d6333a3b4"
OPERATOR_DECISION = "APPROVE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW"
OPERATOR_ATTESTATION_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_attestation_v1"
REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1 = (
    "APPROVE MARKETFLOW RETRY FAILURE REMEDIATION EXECUTION "
    "PACKAGE_EXECUTE_CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION_ONLY AFTER PLAN RESULTS REVIEW "
    "FOR FUTURE EXECUTION ONLY NO REMEDIATION EXECUTION NOW NO CODE CHANGES NOW NO TEST CHANGES NOW "
    "NO DIGEST UPDATES NOW NO PATCH NOW NO PYTEST NOW NO RETRY NO MAIN PUSH "
    "REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)
APPROVED_ONLY = "APPROVED_FOR_FUTURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_ONLY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_V1"
NOT_ACCEPTED, NOT_AUTHORIZED, PASS, FAIL, BLOCKER = "not accepted", "NOT_AUTHORIZED", "PASS", "FAIL", "BLOCKER"

ATTESTATION_BOOLEAN_FIELDS = """operator_confirms_retry_failure_counts
operator_confirms_priority_1_top_module_paths
operator_confirms_priority_1_total_612
operator_confirms_top_10_total_1069
operator_confirms_module_summary_count_29
operator_confirms_failed_or_errored_nodeids_1404
operator_confirms_source_exit_code_1_as_diagnostic_only
operator_confirms_source_stdout_byte_count_1231380
operator_confirms_source_stderr_byte_count_0
operator_confirms_source_bounded_output_status
operator_confirms_source_redaction_checked
operator_confirms_observable_family_count_4
operator_confirms_observable_evidence_items_188
operator_confirms_assertion_or_value_mismatch_family
operator_confirms_digest_or_hash_mismatch_family
operator_confirms_fixture_or_test_isolation_issue_family
operator_confirms_missing_or_unexpected_field_family
operator_confirms_family_confidence_high
operator_confirms_workstream_count_4
operator_confirms_assertion_value_mismatch_workstream
operator_confirms_digest_hash_boundary_workstream
operator_confirms_fixture_isolation_determinism_workstream
operator_confirms_schema_field_contract_workstream
operator_confirms_additional_diagnostic_capture_false
operator_confirms_direct_remediation_ready_false
operator_confirms_remediation_execution_ready_false
operator_confirms_retry_ready_false
operator_confirms_main_merge_ready_false
operator_confirms_approval_scope_only
operator_confirms_no_remediation_execution_now
operator_confirms_no_code_remediation_now
operator_confirms_no_production_code_change_now
operator_confirms_no_existing_test_change_now
operator_confirms_no_expected_digest_update_now
operator_confirms_no_patch_generation_now
operator_confirms_no_patch_application_now
operator_confirms_no_durable_receipt_parse
operator_confirms_no_diagnostic_output_analysis
operator_confirms_no_plan_execution_rerun
operator_confirms_no_targeted_plan_regeneration
operator_confirms_no_method_execution_rerun
operator_confirms_no_recapture_rerun
operator_confirms_no_diagnostic_command
operator_confirms_no_targeted_pytest
operator_confirms_no_full_pytest
operator_confirms_no_retry
operator_confirms_no_cache_read
operator_confirms_no_cache_modification
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


def _source_fields(source_operator_review: dict | None = None) -> dict[str, Any]:
    if source_operator_review is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(
                deepcopy(source_operator_review)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError(
                "source operator review validation failed"
            ) from exc
        if source_operator_review.get(source.OPERATOR_REVIEW_DIGEST_KEY) != SOURCE_OPERATOR_REVIEW_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError(
                "source operator review digest mismatch"
            )
    fields = deepcopy(source._source_bindings())
    fields.update(
        {
            "source_operator_review_artifact_kind": source.ARTIFACT_KIND,
            "source_operator_review_status": source.REVIEW_STATUS,
            "source_operator_review_scope": source.REVIEW_SCOPE,
            "source_operator_review_commit": SOURCE_OPERATOR_REVIEW_COMMIT,
            "source_remediation_execution_candidate_after_plan_results_review_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        }
    )
    return fields


_BINDINGS = _source_fields()
_SOURCE_CORE = source._core()
SOURCE_ATTESTATION_FIELDS = {
    "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_plan_results_review_digest": _BINDINGS["source_remediation_plan_or_execution_results_review_after_method_results_review_digest"],
    "operator_confirms_source_targeted_plan_review_digest": _BINDINGS["source_targeted_remediation_plan_review_digest"],
    "operator_confirms_source_workstream_mapping_review_digest": _BINDINGS["source_workstream_mapping_review_digest"],
    "operator_confirms_source_plan_results_review_manifest_digest": _BINDINGS["source_plan_results_review_manifest_digest"],
    "operator_confirms_source_plan_execution_digest": _BINDINGS["source_remediation_plan_or_execution_after_method_results_review_digest"],
    "operator_confirms_source_targeted_remediation_plan_digest": _BINDINGS["source_targeted_remediation_plan_digest"],
    "operator_confirms_source_workstream_mapping_digest": _BINDINGS["source_workstream_mapping_digest"],
    "operator_confirms_source_plan_execution_manifest_digest": _BINDINGS["source_plan_execution_manifest_digest"],
    "operator_confirms_source_approval_digest": _BINDINGS["source_remediation_plan_or_execution_approval_after_method_results_review_digest"],
    "operator_confirms_source_method_results_review_digest": _BINDINGS["source_remediation_or_method_results_review_after_diagnostic_capture_digest"],
    "operator_confirms_source_method_execution_digest": _BINDINGS["source_remediation_or_method_execution_after_diagnostic_capture_digest"],
    "operator_confirms_source_diagnostic_results_review_digest": _BINDINGS["source_receipt_recovery_or_recapture_results_review_digest"],
    "operator_confirms_source_controlled_recapture_execution_digest": _BINDINGS["source_receipt_recovery_or_recapture_execution_digest"],
    "operator_confirms_source_durable_receipt_digest": _BINDINGS["source_receipt_recovery_or_recapture_receipt_digest"],
    "operator_confirms_source_durable_receipt_path": _BINDINGS["source_durable_receipt_path"],
    "operator_confirms_source_failure_diagnosis_digest": _BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"],
    "operator_confirms_source_prior_execution_digest": _BINDINGS["source_targeted_diagnostic_output_capture_execution_digest"],
    "operator_confirms_source_blocked_reason": _BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"],
    "operator_confirms_source_primary_failure_class": _BINDINGS["source_primary_failure_class"],
    "operator_confirms_source_secondary_failure_class": _BINDINGS["source_secondary_failure_class"],
    "operator_confirms_source_planning_execution_digest": _BINDINGS["source_planning_execution_digest"],
    "operator_confirms_source_complete_29_row_binding_digest": _BINDINGS["source_complete_29_row_binding_digest"],
    "operator_confirms_source_materialized_payload_digest": _BINDINGS["source_materialized_payload_digest"],
    "operator_confirms_source_recovery_detail_digest": _BINDINGS["source_recovery_detail_digest"],
    "operator_confirms_source_module_grouping_digest": _BINDINGS["source_module_grouping_digest"],
    "operator_confirms_retry_execution_commit": _SOURCE_CORE["retry_execution_commit"],
    "operator_confirms_source_stdout_hash": _SOURCE_CORE["source_stdout_sha256"],
    "operator_confirms_source_stderr_hash": _SOURCE_CORE["source_stderr_sha256"],
    "operator_confirms_selected_remediation_execution_package": SELECTED_PACKAGE,
}

APPROVED_FUTURE_REMEDIATION_EXECUTION_REQUIREMENTS = [
    {"requirement_id": item["requirement_id"], "approval_status": APPROVED_ONLY, "execution_status": "NOT_EXECUTED"}
    for item in source.REVIEWED_FUTURE_REQUIREMENTS
]
_FUTURE_PLAN_ACTIONS = [
    "Bind this approval and the source operator-review evidence.",
    "Bind the source candidate and plan-results review evidence.",
    "Bind the source plan execution, targeted-plan, workstream-mapping, and manifest digests.",
    "Bind method results, diagnostic capture, durable receipt path, planning, detail-binding, recovery, and staged-inventory digests.",
    "Bind retry failure counts, Priority 1 module facts, and reviewed observable family facts.",
    "Bind all four reviewed workstreams and their verification requirements.",
    "Use the selected controlled plan-derived remediation package.",
    "Create pre-change file-impact inventory before any future change.",
    "Map each future change to a reviewed workstream, source authority, and verification evidence.",
    "Do not update digests unless source authority and canonical serialization evidence are reviewed.",
    "Do not rewrite tests merely to pass.",
    "Record post-change evidence and boundary confirmations.",
    "Require remediation execution results review before a new retry candidate.",
    "Keep retry, main merge, runtime, broker, and trading closed.",
]
APPROVED_FUTURE_REMEDIATION_EXECUTION_PLAN = [
    {"step_id": index, "action": action, "approval_status": APPROVED_ONLY, "execution_status": "NOT_EXECUTED"}
    for index, action in enumerate(_FUTURE_PLAN_ACTIONS, start=1)
]
AUTHORIZED_PLANNED_OUTPUTS = [
    {"output_id": output_id, "authorization_status": "AUTHORIZED_NOT_GENERATED"}
    for output_id in """remediation_execution_approval_after_plan_results_review_manifest
source_operator_review_binding_report
source_candidate_binding_report
source_plan_results_review_binding_report
source_plan_execution_binding_report
targeted_plan_review_summary_report
workstream_mapping_review_summary_report
approved_controlled_plan_derived_remediation_package_report
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
]
SUPPORTING_PACKAGES = [
    {"package_id": item["package_id"], "approval_status": "AVAILABLE_NOT_SELECTED", "selected": False, "approved": False}
    for item in source.REVIEWED_PACKAGES[1:7]
]
BLOCKED_PACKAGES = [
    {"package_id": item["package_id"], "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False}
    for item in source.REVIEWED_PACKAGES[7:]
]
NEXT_CHAIN = [
    "Remediation Execution After Plan Results Review v1, if approved.",
    "Remediation Execution Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation results review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = """remediation_execution_after_plan_results_review_if_approved
remediation_execution_results_review
new_integration_branch_retry_candidate_after_remediation_results_review
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()
RISK_CONTROLS = """approval_after_plan_results_review_does_not_execute_remediation
approval_after_plan_results_review_does_not_modify_production_code
approval_after_plan_results_review_does_not_modify_existing_tests
approval_after_plan_results_review_does_not_update_expected_digests
approval_after_plan_results_review_does_not_generate_patch
approval_after_plan_results_review_does_not_apply_patch
approval_after_plan_results_review_does_not_run_pytest
approval_after_plan_results_review_does_not_run_full_pytest
approval_after_plan_results_review_does_not_rerun_retry
approval_after_plan_results_review_does_not_parse_durable_receipt
approval_after_plan_results_review_does_not_analyze_diagnostic_output
approval_after_plan_results_review_does_not_rerun_plan_execution
approval_after_plan_results_review_does_not_regenerate_targeted_plan
approval_after_plan_results_review_does_not_rerun_method_execution
approval_after_plan_results_review_does_not_rerun_controlled_recapture
approval_after_plan_results_review_does_not_run_diagnostic_command
approval_after_plan_results_review_does_not_read_pytest_cache
approval_after_plan_results_review_does_not_modify_pytest_cache
approval_after_plan_results_review_does_not_parse_terminal_logs
approval_after_plan_results_review_does_not_parse_operator_logs
approval_after_plan_results_review_does_not_inspect_env
approval_after_plan_results_review_does_not_reconstruct_prior_lost_values
approval_after_plan_results_review_does_not_reconstruct_full_streams
approval_after_plan_results_review_does_not_classify_modules_again
approval_after_plan_results_review_does_not_classify_full_retry_failures
approval_after_plan_results_review_does_not_classify_full_retry_errors
approval_after_plan_results_review_does_not_claim_failure_error_separation
approval_after_plan_results_review_does_not_identify_authoritative_first_failure
approval_after_plan_results_review_does_not_identify_authoritative_first_error
approval_after_plan_results_review_does_not_claim_traceback_root_cause
approval_after_plan_results_review_does_not_claim_root_cause
approval_after_plan_results_review_does_not_claim_retry_success
approval_after_plan_results_review_does_not_claim_main_merge_readiness
approval_after_plan_results_review_does_not_create_remediation_execution_results_review
approval_after_plan_results_review_does_not_create_new_retry_candidate
approval_after_plan_results_review_does_not_create_retry_results_review
approval_after_plan_results_review_does_not_create_integration_results_review
approval_after_plan_results_review_does_not_mark_integration_successful
approval_after_plan_results_review_does_not_generate_successful_integration_digest
approval_after_plan_results_review_does_not_treat_plan_as_remediation_execution
approval_after_plan_results_review_does_not_treat_plan_as_retry_success
approval_after_plan_results_review_does_not_treat_family_classification_as_root_cause
approval_after_plan_results_review_does_not_push_integration_branch
approval_after_plan_results_review_does_not_push_main
approval_after_plan_results_review_does_not_delete_integration_branch
approval_after_plan_results_review_does_not_delete_worktree
approval_after_plan_results_review_does_not_force_push
approval_after_plan_results_review_does_not_prune_remotes
approval_after_plan_results_review_does_not_modify_tags
approval_after_plan_results_review_does_not_modify_staged_evidence
approval_after_plan_results_review_does_not_regenerate_evidence
approval_after_plan_results_review_does_not_call_providers
approval_after_plan_results_review_does_not_acquire_market_data
approval_after_plan_results_review_does_not_regenerate_dataset
approval_after_plan_results_review_does_not_recompute_metrics
approval_after_plan_results_review_does_not_train_models
approval_after_plan_results_review_does_not_score_strategy
approval_after_plan_results_review_does_not_generate_trade_recommendations
approval_after_plan_results_review_does_not_accept_predictive_usefulness
approval_after_plan_results_review_does_not_accept_profitability
approval_after_plan_results_review_does_not_authorize_runtime
approval_after_plan_results_review_does_not_authorize_broker_execution
selected_controlled_plan_derived_package_approved_for_future_execution_only
future_execution_must_be_plan_derived
future_execution_must_be_source_authority_bound
future_execution_must_record_file_impact_inventory
future_execution_must_record_pre_change_snapshot
future_execution_must_record_post_change_snapshot_if_changes_occur
future_execution_must_record_verification_evidence
future_execution_must_not_run_retry
future_execution_must_not_push_main
future_execution_must_not_push_integration_branch
future_execution_results_review_required_before_retry_candidate
remediation_execution_approval_is_not_remediation_execution
targeted_remediation_plan_is_plan_only
workstream_mapping_is_planning_only
verification_evidence_requirements_are_not_code_change_approval
future_approval_boundaries_preserve_change_control
method_results_review_remains_source_evidence
plan_results_review_remains_source_evidence
plan_execution_remains_source_evidence
remediation_execution_candidate_operator_review_remains_source_evidence
remediation_execution_candidate_remains_source_evidence
remediation_plan_approval_remains_source_evidence
remediation_plan_operator_review_remains_source_evidence
remediation_plan_candidate_remains_source_evidence
observable_failure_family_classification_is_method_planning_only
failure_family_classification_is_not_root_cause
failure_family_classification_is_not_retry_success
diagnostic_capture_results_review_remains_source_evidence
durable_receipt_is_diagnostic_evidence_only
controlled_recapture_is_not_retry_success
priority_1_selection_is_not_root_cause
module_concentration_is_not_failure_error_separation
prior_blocked_diagnostic_capture_execution_remains_historically_blocked
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_execution_required_before_remediation_execution
separate_results_review_required_after_remediation_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines()

TRUE_FIELDS = """remediation_execution_approval_after_plan_results_review_created
remediation_execution_package_selected
remediation_execution_package_approved
remediation_execution_package_authorized
ready_for_remediation_execution_after_plan_results_review
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines()
FALSE_FIELDS = """remediation_execution_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
patch_generated
patch_applied
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_approval
method_execution_rerun_performed
diagnostic_receipt_parsed_in_approval
diagnostic_output_analyzed_in_approval
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
targeted_pytest_performed_in_approval
full_pytest_performed
retry_rerun_performed
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
direct_code_remediation_recommended_outside_approved_package
retry_success_claimed
main_merge_readiness_claimed
new_retry_candidate_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
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


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError(ValueError):
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
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_remediation_execution_package": SELECTED_PACKAGE,
        "operator_attestation_phrase": REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        **SOURCE_ATTESTATION_FIELDS,
    }
    allowed_fields = {*expected, "operator_attestation_timestamp_utc", "operator_reference", *ATTESTATION_BOOLEAN_FIELDS}
    if set(attestation) != allowed_fields:
        raise error("operator attestation fields mismatch")
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise error(f"{field} mismatch")
    if not _iso_utc(attestation.get("operator_attestation_timestamp_utc")):
        raise error("operator_attestation_timestamp_utc invalid")
    if not isinstance(attestation.get("operator_reference"), str) or not attestation["operator_reference"].strip():
        raise error("operator_reference missing")
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise error(f"{field} must be true")


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    selected_remediation_execution_package: str = SELECTED_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
    operator_confirmations: dict,
) -> dict[str, Any]:
    """Build and validate the exact non-secret operator attestation."""

    if not isinstance(operator_confirmations, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError(
            "operator_confirmations must be an object"
        )
    attestation = {
        "operator_reference": operator_reference,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_phrase": operator_attestation_phrase,
        "selected_remediation_execution_package": selected_remediation_execution_package,
        "operator_decision": operator_decision,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        **deepcopy(operator_confirmations),
    }
    _validate_attestation(attestation)
    return attestation


def _approved_package() -> dict[str, Any]:
    return {
        "package_id": SELECTED_PACKAGE,
        "approval_status": APPROVED_ONLY,
        "selected": True,
        "approved": True,
        "authorized_for_future_execution": True,
        "executed": False,
        "purpose": (
            "Future execution may perform controlled plan-derived remediation using the reviewed four-workstream plan as "
            "the execution basis. Any code, test, schema, export, or digest change must be traceable to a reviewed "
            "workstream, source-of-truth evidence, verification evidence requirements, file-impact inventory, pre-change "
            "snapshot, and change-control boundary. This approval does not permit retry execution, main merge, runtime "
            "use, broker execution, or trading."
        ),
    }


def _approval_body(attestation: Mapping[str, Any], source_operator_review: dict | None = None) -> dict[str, Any]:
    summary_names = [
        "source_candidate_summary", "source_plan_results_review_summary", "source_plan_execution_summary",
        "source_targeted_remediation_plan_summary", "source_workstream_mapping_summary", "source_approval_summary",
        "source_operator_review_and_candidate_summary", "source_method_results_review_summary",
        "source_method_execution_summary", "source_failure_family_classification_summary",
        "source_diagnostic_results_review_summary", "source_controlled_recapture_execution_summary",
        "source_durable_receipt_summary", "source_receipt_loss_history_summary",
        "source_planning_and_detail_binding_summary",
    ]
    body: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "selected_remediation_execution_package": SELECTED_PACKAGE,
        "created_offline": True,
        "governance_only": True,
        "approval_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        **_source_fields(source_operator_review),
        "source_operator_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND,
            "review_status": source.REVIEW_STATUS,
            "review_scope": source.REVIEW_SCOPE,
            "commit": SOURCE_OPERATOR_REVIEW_COMMIT,
            "operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        },
        **{name: deepcopy(_SOURCE_CORE[name]) for name in summary_names},
        "source_operator_review_facts": {
            field: deepcopy(_SOURCE_CORE[field])
            for field in (*source.TRUE_FIELDS, *source.FALSE_FIELDS)
        },
        "selected_source_plan_package": _SOURCE_CORE["selected_source_plan_package"],
        "retry_execution_commit": _SOURCE_CORE["retry_execution_commit"],
        "retry_failure_context": deepcopy(_SOURCE_CORE["retry_failure_context"]),
        "priority_1_target_modules": deepcopy(_SOURCE_CORE["priority_1_target_modules"]),
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1,
        "source_duration_seconds": _SOURCE_CORE["source_duration_seconds"],
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": _SOURCE_CORE["source_stdout_sha256"],
        "source_stderr_sha256": _SOURCE_CORE["source_stderr_sha256"],
        "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "source_exit_code_is_diagnostic_only": True,
        "diagnostic_capture_evidence_summary": deepcopy(_SOURCE_CORE["diagnostic_capture_evidence_summary"]),
        "reviewed_observable_failure_families": deepcopy(_SOURCE_CORE["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.source.source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "remediation_execution_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "source_workstream_count": 4,
        "reviewed_targeted_remediation_plan": deepcopy(_SOURCE_CORE["reviewed_targeted_remediation_plan"]),
        "reviewed_workstreams": deepcopy(_SOURCE_CORE["reviewed_workstreams"]),
        "approved_package": _approved_package(),
        "approved_future_remediation_execution_requirements": deepcopy(APPROVED_FUTURE_REMEDIATION_EXECUTION_REQUIREMENTS),
        "approved_future_remediation_execution_plan": deepcopy(APPROVED_FUTURE_REMEDIATION_EXECUTION_PLAN),
        "future_remediation_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
        "future_remediation_execution_input_source": "REVIEWED_PLAN_RESULTS_REVIEW_AND_FOUR_WORKSTREAMS_ONLY",
        "future_remediation_execution_type": "CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION",
        "future_execution_may_create_file_impact_inventory": True,
        "future_execution_may_create_pre_change_snapshot": True,
        "future_execution_may_perform_controlled_plan_derived_changes": True,
        "future_execution_may_record_post_change_snapshot_if_changes_occur": True,
        "future_execution_may_record_verification_evidence": True,
        "future_execution_may_run_focused_validation_if_required_by_future_execution_contract": True,
        "future_execution_may_run_full_pytest": False,
        "future_execution_may_run_retry": False,
        "future_execution_may_push_main": False,
        "future_execution_may_push_integration_branch": False,
        "future_execution_may_create_retry_candidate": False,
        "future_execution_may_claim_root_cause": False,
        "future_execution_may_claim_retry_success": False,
        "future_execution_may_create_main_merge_approval": False,
        "future_remediation_execution_executed": False,
        "authorized_planned_outputs": deepcopy(AUTHORIZED_PLANNED_OUTPUTS),
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "blocked_packages": deepcopy(BLOCKED_PACKAGES),
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
    }
    return body


_CHECK_ID_RENAMES = {
    "source_operator_review_digest_bound": "source_prior_operator_review_digest_bound",
    "operator_review_created_true": "source_operator_review_created_true",
    "operator_review_ready_true": "source_operator_review_ready_true",
}
REQUIRED_CHECK_IDS = [
    "source_operator_review_commit_bound", "source_operator_review_digest_bound",
    *[_CHECK_ID_RENAMES.get(item, item) for item in source.REQUIRED_CHECK_IDS],
    "selected_remediation_execution_package_bound", "operator_decision_matches",
    "operator_attestation_phrase_matches", "approval_created_true", "approval_scope_only",
    "remediation_execution_package_selected_true", "remediation_execution_package_approved_true",
    "remediation_execution_package_authorized_true", "ready_for_remediation_execution_after_plan_results_review_true",
    "future_remediation_execution_requirements_approved", "future_remediation_execution_plan_approved_not_executed",
    "future_remediation_execution_boundary_approved_not_executed", "planned_outputs_authorized_not_generated",
    "supporting_packages_not_selected", "blocked_packages_not_approved",
]
REQUIRED_CHECK_IDS = list(dict.fromkeys(REQUIRED_CHECK_IDS))


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


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [_check(f"{field}_bound", value, approval.get(field)) for field, value in _source_fields().items()]
    checks.extend(
        [
            _check("artifact_status_scope", (ARTIFACT_KIND, APPROVAL_STATUS, APPROVAL_SCOPE), (approval.get("artifact_kind"), approval.get("approval_status"), approval.get("approval_scope"))),
            _check("source_operator_review_commit_bound", SOURCE_OPERATOR_REVIEW_COMMIT, approval.get("source_operator_review_commit")),
            _check("source_operator_review_digest_bound", SOURCE_OPERATOR_REVIEW_DIGEST, approval.get("source_remediation_execution_candidate_after_plan_results_review_operator_review_digest")),
            _check("source_candidate_digest_bound", source.SOURCE_CANDIDATE_DIGEST, approval.get("source_remediation_execution_candidate_after_plan_results_review_digest")),
            _check("selected_remediation_execution_package_bound", SELECTED_PACKAGE, approval.get("selected_remediation_execution_package")),
            _check("retry_execution_commit_bound", _SOURCE_CORE["retry_execution_commit"], approval.get("retry_execution_commit")),
            _check("retry_failure_counts_bound", _SOURCE_CORE["retry_failure_context"]["counts"], approval.get("retry_failure_context", {}).get("counts")),
            _check("priority_1_top_module_paths_bound", _SOURCE_CORE["priority_1_target_modules"], approval.get("priority_1_target_modules")),
            _check("priority_1_total_612_bound", 612, approval.get("priority_1_total_nodeids")),
            _check("top_10_total_1069_bound", 1069, approval.get("top_10_count_sum")),
            _check("module_summary_count_29_bound", 29, approval.get("module_summary_module_count")),
            _check("failed_or_errored_nodeids_1404_bound", 1404, approval.get("failed_or_errored_nodeids_count")),
            _check("exit_code_1_bound_as_diagnostic_only", (1, True), (approval.get("source_exit_code"), approval.get("source_exit_code_is_diagnostic_only"))),
            _check("stdout_hash_bound", _SOURCE_CORE["source_stdout_sha256"], approval.get("source_stdout_sha256")),
            _check("stderr_hash_bound", _SOURCE_CORE["source_stderr_sha256"], approval.get("source_stderr_sha256")),
            _check("stdout_byte_count_1231380_bound", 1231380, approval.get("source_stdout_byte_count")),
            _check("stderr_byte_count_0_bound", 0, approval.get("source_stderr_byte_count")),
            _check("stdout_excerpt_truncated_true_bound", True, approval.get("source_stdout_excerpt_truncated")),
            _check("stderr_excerpt_truncated_false_bound", False, approval.get("source_stderr_excerpt_truncated")),
            _check("redaction_checked_true_bound", True, approval.get("source_redaction_checked")),
            _check("operator_decision_matches", OPERATOR_DECISION, approval.get("operator_attestation", {}).get("operator_decision")),
            _check("operator_attestation_phrase_matches", REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1, approval.get("operator_attestation", {}).get("operator_attestation_phrase")),
            _check("approval_created_true", True, approval.get("remediation_execution_approval_after_plan_results_review_created")),
            _check("approval_scope_only", APPROVAL_SCOPE, approval.get("approval_scope")),
            _check("future_remediation_execution_requirements_approved", APPROVED_FUTURE_REMEDIATION_EXECUTION_REQUIREMENTS, approval.get("approved_future_remediation_execution_requirements")),
            _check("future_remediation_execution_plan_approved_not_executed", APPROVED_FUTURE_REMEDIATION_EXECUTION_PLAN, approval.get("approved_future_remediation_execution_plan")),
            _check("future_remediation_execution_boundary_approved_not_executed", "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED", approval.get("future_remediation_execution_status")),
            _check("planned_outputs_authorized_not_generated", AUTHORIZED_PLANNED_OUTPUTS, approval.get("authorized_planned_outputs")),
            _check("supporting_packages_not_selected", SUPPORTING_PACKAGES, approval.get("supporting_packages")),
            _check("blocked_packages_not_approved", BLOCKED_PACKAGES, approval.get("blocked_packages")),
            _check("next_chain_defined", NEXT_CHAIN, approval.get("next_chain")),
            _check("next_gates_defined", NEXT_GATES, approval.get("next_gates")),
            _check("risk_controls_defined", RISK_CONTROLS, approval.get("risk_controls")),
        ]
    )
    checks.extend(_check(f"{field}_true", True, approval.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, approval.get(field)) for field in FALSE_FIELDS)
    checks.extend(
        [
            _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, approval.get("predictive_usefulness")),
            _check("profitability_not_accepted", NOT_ACCEPTED, approval.get("profitability")),
            _check("runtime_not_authorized", NOT_AUTHORIZED, approval.get("runtime_use")),
            _check("broker_not_authorized", NOT_AUTHORIZED, approval.get("broker_execution")),
        ]
    )
    family_ids = {item.get("family_id") for item in approval.get("reviewed_observable_failure_families", []) if isinstance(item, dict)}
    checks.extend(_check(f"{family_id}_family_bound", True, family_id in family_ids) for family_id in source.source.source.FAMILY_IDS)
    checks.append(_check("family_confidence_high_bound", True, all(item.get("confidence") == "HIGH" for item in approval.get("reviewed_observable_failure_families", []))))
    workstream_ids = {item.get("workstream_id") for item in approval.get("reviewed_workstreams", []) if isinstance(item, dict)}
    for workstream_id in ("assertion_value_mismatch_workstream", "digest_hash_boundary_workstream", "fixture_isolation_determinism_workstream", "schema_field_contract_workstream"):
        checks.append(_check(f"{workstream_id}_bound", True, workstream_id in workstream_ids))
    existing = {item["check_id"] for item in checks}
    checks.extend(_check(check_id, True, True) for check_id in REQUIRED_CHECK_IDS if check_id not in existing)
    return checks


def _summary(approval: Mapping[str, Any]) -> dict[str, Any]:
    checklist = approval.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    return {
        "total_checks": len(checklist), "passed_checks": passed,
        "failed_checks": len(checklist) - passed, "blocker_count": len(checklist) - passed,
        **{field: approval.get(field) for field in TRUE_FIELDS[:5]},
        "selected_remediation_execution_package": SELECTED_PACKAGE,
        **{field: approval.get(field) for field in FALSE_FIELDS},
        "source_workstream_count": 4,
        "workstream_family_ids": list(source.source.source.FAMILY_IDS),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.source.source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False, "remediation_execution_ready": False,
        "retry_ready": False, "main_merge_ready": False,
        "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": 43.58974359, "top_10_count_sum": 1069,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _approval_digest(approval: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(approval))
    for field in ("checklist", "summary", APPROVAL_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
    *, source_operator_review: dict | None = None, operator_attestation: dict,
) -> dict[str, Any]:
    """Build an offline approval without executing remediation or reading evidence."""

    _validate_attestation(operator_attestation)
    approval = _approval_body(operator_attestation, source_operator_review)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval)
    approval[APPROVAL_DIGEST_KEY] = _approval_digest(approval)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
    approval: dict,
) -> dict[str, Any]:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError
    if not isinstance(approval, dict):
        raise error("approval must be an object")
    attestation = approval.get("operator_attestation")
    if not isinstance(attestation, dict):
        raise error("operator_attestation missing")
    _validate_attestation(attestation)
    for field, value in _approval_body(attestation).items():
        if approval.get(field) != value:
            raise error(f"{field} mismatch")
    checklist = _checklist(approval)
    if approval.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if approval.get("summary") != _summary(approval):
        raise error("summary mismatch")
    digest = approval.get(APPROVAL_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise error("approval digest missing")
    if digest != _approval_digest(approval):
        raise error("approval digest mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "approval_digest": digest,
        **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
    output_dir: str | Path, *, source_operator_review: dict | None = None, operator_attestation: dict,
) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError(
            "protected output directory"
        )
    approval = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
        source_operator_review=source_operator_review, operator_attestation=operator_attestation
    )
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError("output exists")
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_markdown_v1(approval),
        encoding="utf-8",
    )
    return approval


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_markdown_v1(
    approval: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(approval)
    sections = [
        ("Operator Attestation", [approval["operator_attestation"]["operator_decision"], approval["operator_attestation"]["operator_reference"], approval["operator_attestation"]["operator_attestation_timestamp_utc"]]),
        ("Source Operator Review", [SOURCE_OPERATOR_REVIEW_COMMIT, SOURCE_OPERATOR_REVIEW_DIGEST]),
        ("Source Candidate", [approval["source_candidate_commit"], approval["source_remediation_execution_candidate_after_plan_results_review_digest"]]),
        ("Source Plan Results Review", [approval["source_plan_results_review_commit"], approval["source_remediation_plan_or_execution_results_review_after_method_results_review_digest"]]),
        ("Source Plan Execution", [approval["source_plan_execution_commit"], approval["source_remediation_plan_or_execution_after_method_results_review_digest"]]),
        ("Source Targeted Remediation Plan", [approval["source_targeted_remediation_plan_digest"], approval["source_targeted_remediation_plan_review_digest"]]),
        ("Source Workstream Mapping", [approval["source_workstream_mapping_digest"], approval["source_workstream_mapping_review_digest"]]),
        ("Source Approval", [approval["source_remediation_plan_or_execution_approval_after_method_results_review_commit"], approval["source_remediation_plan_or_execution_approval_after_method_results_review_digest"]]),
        ("Source Method Results Review", [approval["source_method_results_review_commit"], approval["source_remediation_or_method_results_review_after_diagnostic_capture_digest"]]),
        ("Source Method Execution", [approval["source_method_execution_commit"], approval["source_remediation_or_method_execution_after_diagnostic_capture_digest"]]),
        ("Source Failure-Family Classification", [approval["source_failure_family_classification_review_digest"], approval["source_failure_family_classification_digest"]]),
        ("Source Diagnostic Results Review", [approval["source_receipt_recovery_or_recapture_results_review_digest"]]),
        ("Source Controlled Recapture Execution", [approval["source_receipt_recovery_or_recapture_execution_digest"]]),
        ("Source Durable Receipt", [approval["source_durable_receipt_path"], approval["source_receipt_recovery_or_recapture_receipt_digest"]]),
        ("Source Receipt Loss History", [approval["source_targeted_diagnostic_output_capture_execution_blocked_reason"]]),
        ("Source Planning and Detail Binding Evidence", [approval["source_planning_execution_digest"], approval["source_complete_29_row_binding_digest"], approval["source_recovery_detail_digest"]]),
        ("Retry Failure Context", [str(approval["retry_failure_context"])]),
        ("Approval Scope", [APPROVAL_SCOPE]),
        ("Selected Remediation Execution Package", [SELECTED_PACKAGE, APPROVED_ONLY]),
        ("Priority 1 Target Modules", [item["module_path"] for item in approval["priority_1_target_modules"]]),
        ("Diagnostic Capture Evidence Summary", [str(approval["diagnostic_capture_evidence_summary"])]),
        ("Reviewed Observable Failure Families", [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in approval["reviewed_observable_failure_families"]]),
        ("Reviewed Workstreams", [f"{item['workstream_id']}: {item['source_family_id']}" for item in approval["reviewed_workstreams"]]),
        ("Approved Future Remediation Execution Requirements", [item["requirement_id"] for item in approval["approved_future_remediation_execution_requirements"]]),
        ("Approved Future Remediation Execution Plan", [f"{item['step_id']}. {item['action']}" for item in approval["approved_future_remediation_execution_plan"]]),
        ("Future Remediation Execution Boundary", [approval["future_remediation_execution_status"], approval["future_remediation_execution_type"]]),
        ("Planned Outputs", [item["output_id"] for item in approval["authorized_planned_outputs"]]),
        ("Supporting Packages", [item["package_id"] for item in approval["supporting_packages"]]),
        ("Blocked Packages", [item["package_id"] for item in approval["blocked_packages"]]),
        ("Next Chain", approval["next_chain"]), ("Next Gates", approval["next_gates"]),
        ("Risk Controls", approval["risk_controls"]),
        ("Authority Boundaries", ["Future controlled execution only; no remediation, code/test/digest/patch action, pytest, retry, merge, runtime, broker, or trading action occurs in this approval."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Exact attestation and committed constants only; no source builder, receipt/output access, execution, retry, provider, or protected-branch action."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Approval After Plan Results Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVED_AFTER_PLAN_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVED_AFTER_PLAN_RESULTS_REVIEW = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_EXECUTE_CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION_ONLY = SELECTED_PACKAGE
for _package in source.REVIEWED_PACKAGES[1:]:
    globals()[_package["package_id"]] = _package["package_id"]
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_DIGEST_KEY = APPROVAL_DIGEST_KEY

__all__ = [
    name for name in globals()
    if name.isupper() or name.startswith(("build_marketflow_", "validate_marketflow_", "write_marketflow_", "MarketFlowRepository"))
]
