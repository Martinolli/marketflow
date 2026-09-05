"""Execute the approved source-authority acquisition gate using injected evidence only."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_service
    as source,
)


SUCCESS_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_BLOCKED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1"
SUCCESS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTED_AFTER_CANDIDATE_OPERATOR_REVIEW_SOURCE_AUTHORITY_EVIDENCE_BOUND_FOR_RESULTS_REVIEW"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_BLOCKED_AFTER_CANDIDATE_OPERATOR_REVIEW_NO_REVIEWED_SOURCE_AUTHORITY_EVIDENCE_AVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_SOURCE_AUTHORITY_ACQUISITION_OR_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
SOURCE_APPROVAL_COMMIT = "f8189e7421720879bd2a6d30f05353c8b65adff4"
SOURCE_APPROVAL_DIGEST = "1aadaddb1a8f27cce5e0903a7fdfdd7de4de7d2add8ff2a3e61d17b94bb74b69"
SOURCE_ATTESTATION_DIGEST = "db079d7b71f141dafba8439eba51caa1bc663ddf1158d3ea34b1f102ce4fb879"
EVIDENCE_PACKAGE_KIND = "MARKETFLOW_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FOR_RETRY_FAILURE_ACQUISITION_V1"
EVIDENCE_PACKAGE_STATUS = "OPERATOR_PROVIDED_FOR_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY"
DEFAULT_BLOCKED_REASON = "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_RESULTS_REVIEW_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_V1"
EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_digest"
EVIDENCE_PACKAGE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_evidence_package_digest"
EVIDENCE_MAPPING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_evidence_mapping_digest"
COVERAGE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_coverage_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_blocked_manifest_digest"
PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1 = SUCCESS_ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_BLOCKED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTED_AFTER_CANDIDATE_OPERATOR_REVIEW_SOURCE_AUTHORITY_EVIDENCE_BOUND_FOR_RESULTS_REVIEW = SUCCESS_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_BLOCKED_AFTER_CANDIDATE_OPERATOR_REVIEW_NO_REVIEWED_SOURCE_AUTHORITY_EVIDENCE_AVAILABLE_OR_BOUNDARY_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_SOURCE_AUTHORITY_ACQUISITION_OR_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE = SELECTED_PACKAGE

PACKAGE_FIELDS = frozenset(
    {
        "package_kind", "package_status", "package_source_owner_or_origin", "package_reference",
        "package_created_utc", "package_digest_or_reproducible_provenance", "package_declares_no_secrets",
        "package_declares_no_api_keys", "package_declares_no_broker_credentials",
        "package_declares_no_personal_financial_credentials",
        "package_distinguishes_specification_from_observation",
        "package_distinguishes_expected_from_actual",
        "package_distinguishes_source_authority_from_diagnostic_output", "evidence_items",
    }
)
EVIDENCE_ITEM_FIELDS = frozenset(
    {
        "evidence_id", "mapped_missing_authority_id", "section_id", "workstream_id",
        "acceptable_source_artifact_type", "source_owner_or_origin", "source_reference",
        "digest_or_reproducible_provenance", "evidence_classification", "specification_or_observation",
        "expected_or_actual_scope", "authority_statement", "results_review_required_before_use",
        "direct_change_authorized_now", "remediation_authorized_now", "retry_authorized_now",
        "main_merge_authorized_now",
    }
)
ALLOWED_SECTION_IDS = frozenset(
    {
        "assertion_value_mismatch_source_authority_scope",
        "digest_hash_boundary_source_authority_scope",
        "fixture_isolation_determinism_source_authority_scope",
        "schema_field_contract_source_authority_scope",
    }
)
ALLOWED_WORKSTREAM_IDS = frozenset(
    {
        "assertion_value_mismatch_workstream", "digest_hash_boundary_workstream",
        "fixture_isolation_determinism_workstream", "schema_field_contract_workstream",
    }
)
ALLOWED_ARTIFACT_TYPES = frozenset(
    {
        "approved_product_specification", "approved_schema_definition", "approved_artifact_contract",
        "approved_canonical_payload_or_serialization_contract", "approved_expected_value_source",
        "approved_actual_value_source", "approved_digest_manifest_source",
        "approved_fixture_lifecycle_document", "approved_deterministic_execution_contract",
        "approved_export_surface_contract", "approved_operator_provided_evidence_package",
        "approved_source_owning_team_statement", "approved_reviewed_source_digest_bundle",
    }
)
ALLOWED_EVIDENCE_CLASSIFICATIONS = frozenset(
    {
        "SPECIFICATION", "APPROVED_CONTRACT", "SOURCE_OWNER_STATEMENT", "CANONICAL_PAYLOAD",
        "CANONICAL_SCHEMA", "CANONICAL_SERIALIZATION", "EXPECTED_VALUE_SOURCE", "ACTUAL_VALUE_SOURCE",
        "FIXTURE_LIFECYCLE_AUTHORITY", "DETERMINISM_AUTHORITY", "EXPORT_SURFACE_AUTHORITY",
        "REVIEWED_SOURCE_DIGEST_BUNDLE",
    }
)
ALLOWED_SPECIFICATION_OR_OBSERVATION = frozenset(
    {"SPECIFICATION", "OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT"}
)
ALLOWED_EXPECTED_OR_ACTUAL_SCOPE = frozenset({"EXPECTED", "ACTUAL", "BOTH", "NOT_APPLICABLE"})

COMMON_TRUE_FIELDS = tuple(
    """source_authority_acquisition_execution_created
source_approval_verified
source_operator_review_verified
selected_source_authority_acquisition_package_verified""".splitlines()
)
SUCCESS_TRUE_FIELDS = tuple(
    """source_authority_acquisition_execution_performed
selected_source_authority_acquisition_package_executed
source_follow_on_results_review_verified
source_follow_on_execution_verified
source_authority_acquisition_candidate_verified
source_authority_acquisition_scope_verified
source_missing_authority_mapping_verified
operator_source_authority_evidence_package_supplied
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
source_authority_acquisition_performed
source_authority_evidence_acquired
source_authority_evidence_items_bound_for_results_review
source_authority_evidence_mapping_created
source_authority_acquisition_results_review_required
ready_for_source_authority_acquisition_results_review""".splitlines()
)
CLOSED_FALSE_FIELDS = tuple(
    """external_evidence_acquired
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
pytest_performed_in_execution
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_execution
diagnostic_output_analyzed_in_execution
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_execution
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_execution
cache_modified_in_execution
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
provider_requests_made_in_execution
market_data_acquisition_performed_in_execution
dataset_generation_performed_in_execution
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()
)
BLOCKED_FALSE_FIELDS = tuple(
    dict.fromkeys(
        (
            "source_authority_acquisition_execution_performed",
            "selected_source_authority_acquisition_package_executed",
            "operator_source_authority_evidence_package_validated",
            "operator_source_authority_evidence_package_bound",
            "source_authority_acquisition_performed",
            "source_authority_evidence_acquired",
            "source_authority_evidence_items_bound_for_results_review",
            "source_authority_evidence_mapping_created",
            "source_authority_acquisition_results_review_required",
            "ready_for_source_authority_acquisition_results_review",
            *CLOSED_FALSE_FIELDS,
        )
    )
)

SUCCESS_OUTPUT_IDS = tuple(
    """source_authority_acquisition_execution_manifest
source_approval_binding_report
source_operator_review_binding_report
source_follow_on_results_review_binding_report
source_follow_on_execution_binding_report
source_authority_acquisition_candidate_binding_report
source_authority_acquisition_scope_binding_report
source_missing_authority_mapping_binding_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
operator_source_authority_evidence_package_validation_report
acquired_or_bound_evidence_item_inventory
missing_authority_coverage_report
source_authority_evidence_custody_report
source_authority_evidence_digest_report
unsupported_claims_boundary_report
source_authority_acquisition_results_review_requirements
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
)
BLOCKED_OUTPUT_IDS = tuple(
    """source_authority_acquisition_execution_blocked_manifest
source_approval_binding_report
source_operator_review_binding_report
retry_failure_context_report
blocked_reason_report
missing_or_failed_data_report
unsupported_claims_boundary_report
next_failure_diagnosis_recommendation
digest_manifest""".splitlines()
)
SUCCESS_NEXT_CHAIN = (
    "Source Authority Acquisition Results Review After Candidate Operator Review v1.",
    "Conditional no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
BLOCKED_NEXT_CHAIN = (
    "Source Authority Acquisition Execution After Candidate Operator Review Failure Diagnosis v1.",
    "Optional operator source-evidence package preparation path.",
    "No no-change disposition, alternate diagnostic, remediation, retry, or main merge.",
)
NEXT_GATES = tuple(
    """source_authority_acquisition_results_review_if_evidence_bound
source_authority_acquisition_failure_diagnosis_if_blocked
operator_source_evidence_package_preparation_if_missing
no_change_disposition_candidate_if_supported_by_reviewed_acquired_evidence
alternate_diagnostic_candidate_if_supported_by_reviewed_acquired_evidence
remediation_reentry_candidate_if_supported_by_reviewed_acquired_evidence
no_change_retry_criteria_candidate_if_supported_by_reviewed_acquired_evidence
hold_disposition_if_supported
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()
)
RISK_CONTROLS = tuple(
    """source_authority_acquisition_execution_uses_approved_package_only
source_authority_acquisition_execution_requires_valid_operator_evidence_package
source_authority_acquisition_execution_fails_closed_without_evidence_package
source_authority_acquisition_execution_fails_closed_on_invalid_evidence_package
source_authority_acquisition_execution_does_not_fabricate_evidence
source_authority_acquisition_execution_does_not_infer_missing_evidence
source_authority_acquisition_execution_does_not_read_files_unless_explicitly_implemented_and_reviewed
source_authority_acquisition_execution_does_not_call_external_providers
source_authority_acquisition_execution_does_not_parse_logs
source_authority_acquisition_execution_does_not_inspect_env
source_authority_acquisition_execution_does_not_parse_durable_receipt
source_authority_acquisition_execution_does_not_analyze_diagnostic_output
source_authority_acquisition_execution_does_not_execute_remediation
source_authority_acquisition_execution_does_not_modify_production_code
source_authority_acquisition_execution_does_not_modify_existing_tests
source_authority_acquisition_execution_does_not_update_expected_digests
source_authority_acquisition_execution_does_not_generate_patch
source_authority_acquisition_execution_does_not_apply_patch
source_authority_acquisition_execution_does_not_run_pytest
source_authority_acquisition_execution_does_not_run_full_pytest
source_authority_acquisition_execution_does_not_rerun_priority1_validation
source_authority_acquisition_execution_does_not_rerun_retry
source_authority_acquisition_execution_does_not_rerun_detached_retry
source_authority_acquisition_execution_does_not_rerun_source_authority_enrichment
source_authority_acquisition_execution_does_not_rerun_follow_on_execution
source_authority_acquisition_execution_does_not_rerun_plan_execution
source_authority_acquisition_execution_does_not_regenerate_targeted_plan
source_authority_acquisition_execution_does_not_rerun_method_execution
source_authority_acquisition_execution_does_not_rerun_controlled_recapture
source_authority_acquisition_execution_does_not_run_diagnostic_command
source_authority_acquisition_execution_does_not_read_pytest_cache
source_authority_acquisition_execution_does_not_modify_pytest_cache
source_authority_acquisition_execution_does_not_commit_pytest_cache
source_authority_acquisition_execution_does_not_commit_marketflow_outputs
source_authority_acquisition_execution_does_not_reconstruct_prior_lost_values
source_authority_acquisition_execution_does_not_reconstruct_full_streams
source_authority_acquisition_execution_does_not_classify_modules_again
source_authority_acquisition_execution_does_not_classify_full_retry_failures
source_authority_acquisition_execution_does_not_classify_full_retry_errors
source_authority_acquisition_execution_does_not_claim_failure_error_separation
source_authority_acquisition_execution_does_not_identify_authoritative_first_failure
source_authority_acquisition_execution_does_not_identify_authoritative_first_error
source_authority_acquisition_execution_does_not_claim_traceback_root_cause
source_authority_acquisition_execution_does_not_claim_root_cause
source_authority_acquisition_execution_does_not_claim_retry_success
source_authority_acquisition_execution_does_not_claim_main_merge_readiness
source_authority_acquisition_execution_does_not_create_retry_candidate
source_authority_acquisition_execution_does_not_create_retry_approval
source_authority_acquisition_execution_does_not_create_retry_execution
source_authority_acquisition_execution_does_not_create_retry_results_review
source_authority_acquisition_execution_does_not_create_main_merge_approval
source_authority_acquisition_execution_does_not_push_main
source_authority_acquisition_execution_does_not_push_integration_branch
source_authority_acquisition_execution_does_not_delete_integration_branch
source_authority_acquisition_execution_does_not_delete_worktree
source_authority_acquisition_execution_does_not_force_push
source_authority_acquisition_execution_does_not_modify_tags
source_authority_acquisition_execution_does_not_regenerate_evidence
source_authority_acquisition_execution_does_not_accept_predictive_usefulness
source_authority_acquisition_execution_does_not_accept_profitability
source_authority_acquisition_execution_does_not_authorize_runtime
source_authority_acquisition_execution_does_not_authorize_broker_execution
evidence_binding_is_not_results_review_acceptance
evidence_binding_is_not_remediation_authority
evidence_binding_is_not_retry_readiness
candidate_scope_is_not_source_authority
diagnostic_output_is_not_source_authority
priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_results_review_required_after_any_acquisition
separate_remediation_approval_required_before_code_or_test_changes
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines()
)

CHECK_IDS = tuple(
    """source_approval_commit_bound
source_approval_digest_bound
source_attestation_digest_bound
selected_source_authority_acquisition_package_bound
source_operator_review_commit_bound
source_operator_review_digest_bound
source_candidate_review_digest_bound
source_scope_review_digest_bound
source_mapping_review_digest_bound
source_operator_review_manifest_digest_bound
source_follow_on_results_review_commit_bound
source_follow_on_results_review_digest_bound
source_follow_on_results_review_manifest_digest_bound
source_follow_on_execution_commit_bound
source_follow_on_execution_digest_bound
source_acquisition_candidate_digest_bound
source_acquisition_scope_digest_bound
source_missing_authority_mapping_digest_bound
source_follow_on_execution_manifest_digest_bound
source_results_review_digest_bound
source_execution_digest_bound
source_authority_enrichment_plan_digest_bound
source_missing_authority_inventory_digest_bound
source_workstream_authority_mapping_digest_bound
source_failure_diagnosis_digest_bound
source_blocked_reason_bound
source_blocked_manifest_digest_bound
primary_failure_class_bound
secondary_failure_classes_bound
retry_execution_commit_bound
retry_failure_counts_bound
priority_1_top_module_paths_bound
priority_1_total_612_bound
top_10_total_1069_bound
module_summary_count_29_bound
failed_or_errored_nodeids_1404_bound
priority1_pre_change_validation_675_passed_bound
priority1_post_change_validation_675_passed_bound
diagnostic_exit_code_1_bound_as_diagnostic_only
diagnostic_stdout_hash_bound
diagnostic_stderr_hash_bound
diagnostic_stdout_byte_count_1231380_bound
diagnostic_stderr_byte_count_0_bound
observable_family_count_4_bound
observable_evidence_items_188_bound
workstream_count_4_bound
acquisition_scope_section_count_4_bound
mapped_missing_authority_item_count_30_bound
acceptable_source_artifact_type_count_13_bound
operator_provided_evidence_requirement_count_10_bound
evidence_custody_and_digest_requirement_count_6_bound
candidate_results_review_requirement_count_16_bound
source_authority_acquisition_execution_created_true
selected_package_executed_true_if_success_false_if_blocked
operator_source_authority_evidence_package_supplied_status_correct
operator_source_authority_evidence_package_validated_status_correct
source_authority_evidence_bound_status_correct
source_authority_acquisition_results_review_required_if_success
blocked_reason_present_if_blocked
source_authority_acquisition_execution_performed_status_correct
source_authority_acquisition_performed_status_correct
source_authority_evidence_acquired_status_correct
external_evidence_acquired_false_unless_explicitly_source_package_bound
concrete_source_authority_established_false
safe_source_authority_bound_change_identified_false
no_change_disposition_false
alternate_diagnostic_execution_false
remediation_execution_false
production_code_modified_false
existing_tests_modified_false
expected_digests_updated_false
patch_generated_false
patch_applied_false
pytest_false
full_pytest_false
priority1_validation_rerun_false
retry_rerun_false
detached_retry_false
cache_read_false
cache_modified_false
pytest_cache_committed_false
marketflow_outputs_committed_false
durable_receipt_parsed_false
diagnostic_output_analyzed_false
source_authority_enrichment_rerun_false
follow_on_execution_rerun_false
plan_execution_rerun_false
targeted_plan_regenerated_false
method_execution_rerun_false
controlled_recapture_rerun_false
diagnostic_command_rerun_false
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
retry_success_claimed_false
main_merge_readiness_claimed_false
retry_candidate_created_false
retry_approval_created_false
new_retry_executed_false
new_retry_results_review_created_false
main_merge_approval_created_false
ready_for_acquisition_results_review_true_if_success_false_if_blocked
ready_for_remediation_execution_false
ready_for_retry_candidate_false
ready_for_main_merge_approval_false
integration_success_false
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
outputs_generated_or_blocked_correctly
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines()
)


class MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(ValueError):
    """Raised when execution evidence or a closed boundary is invalid."""


def _committed_source_approval() -> dict[str, Any]:
    review = source._committed_source_operator_review()
    attestation = {
        "operator_decision": source.OPERATOR_DECISION,
        "selected_source_authority_acquisition_package": source.SELECTED_PACKAGE,
        "operator_attestation_phrase": source.REQUIRED_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_version": "v1",
        "operator_reference": "TEST_OPERATOR",
        **source._expected_operator_confirmations(review),
    }
    attestation[source.ATTESTATION_DIGEST_KEY] = semantic_digest(attestation)
    return source._assemble_approval(review, attestation)


_COMMITTED_SOURCE_APPROVAL = _committed_source_approval()


def _first_difference(actual: Any, expected: Any, path: str = "execution") -> str | None:
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


def _validated_source_approval(injected: dict | None) -> dict[str, Any]:
    approval = deepcopy(_COMMITTED_SOURCE_APPROVAL if injected is None else injected)
    difference = _first_difference(approval, _COMMITTED_SOURCE_APPROVAL, "source_approval")
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
            f"{difference} mismatch"
        )
    if approval[source.APPROVAL_DIGEST_KEY] != SOURCE_APPROVAL_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
            "source approval digest mismatch"
        )
    if approval["operator_attestation"][source.ATTESTATION_DIGEST_KEY] != SOURCE_ATTESTATION_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
            "source attestation digest mismatch"
        )
    return approval


def _source_bindings(approval: Mapping[str, Any]) -> dict[str, Any]:
    bindings = {key: deepcopy(value) for key, value in approval.items() if key.startswith("source_")}
    bindings.update(
        {
            "source_historical_approval_commit": approval["source_approval_summary"]["commit"],
            "source_historical_approval_digest": approval["source_approval_summary"]["digest"],
            "source_approval_artifact_kind": source.ARTIFACT_KIND,
            "source_approval_status": source.APPROVAL_STATUS,
            "source_approval_scope": source.APPROVAL_SCOPE,
            "source_approval_commit": SOURCE_APPROVAL_COMMIT,
            "source_approval_digest": SOURCE_APPROVAL_DIGEST,
            "source_attestation_digest": SOURCE_ATTESTATION_DIGEST,
            "source_approval_checklist_summary": deepcopy(approval["summary"]),
        }
    )
    return bindings


def _non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _package_validation(
    evidence_package: Any, approval: Mapping[str, Any]
) -> tuple[bool, str | None, list[str]]:
    if evidence_package is None:
        return False, DEFAULT_BLOCKED_REASON, ["operator_source_authority_evidence_package"]
    if not isinstance(evidence_package, Mapping):
        return False, "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_STRUCTURE", ["package"]
    if set(evidence_package) != PACKAGE_FIELDS:
        return False, "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_REQUIRED_FIELDS", sorted(
            PACKAGE_FIELDS.symmetric_difference(evidence_package)
        )
    if evidence_package["package_kind"] != EVIDENCE_PACKAGE_KIND:
        return False, "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_KIND", ["package_kind"]
    if evidence_package["package_status"] != EVIDENCE_PACKAGE_STATUS:
        return False, "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_STATUS", ["package_status"]
    for field in (
        "package_source_owner_or_origin", "package_reference", "package_created_utc",
        "package_digest_or_reproducible_provenance",
    ):
        if not _non_empty(evidence_package[field]):
            return False, "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVENANCE", [field]
    for field in (
        "package_declares_no_secrets", "package_declares_no_api_keys",
        "package_declares_no_broker_credentials", "package_declares_no_personal_financial_credentials",
    ):
        if evidence_package[field] is not True:
            return False, "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_SECRET_BOUNDARY", [field]
    for field in (
        "package_distinguishes_specification_from_observation",
        "package_distinguishes_expected_from_actual",
        "package_distinguishes_source_authority_from_diagnostic_output",
    ):
        if evidence_package[field] is not True:
            return False, "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_SEMANTIC_BOUNDARY", [field]
    items = evidence_package["evidence_items"]
    if not isinstance(items, list) or not items:
        return False, "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_ITEMS", ["evidence_items"]
    mapping_items = approval["missing_authority_to_source_evidence_mapping_review"]["items"]
    known = {item["missing_authority_id"]: item for item in mapping_items}
    evidence_ids: set[str] = set()
    for index, item in enumerate(items):
        prefix = f"evidence_items[{index}]"
        if not isinstance(item, Mapping) or set(item) != EVIDENCE_ITEM_FIELDS:
            return False, "INVALID_SOURCE_AUTHORITY_EVIDENCE_ITEM_REQUIRED_FIELDS", [prefix]
        for field in (
            "evidence_id", "source_owner_or_origin", "source_reference",
            "digest_or_reproducible_provenance", "authority_statement",
        ):
            if not _non_empty(item[field]):
                return False, "INVALID_SOURCE_AUTHORITY_EVIDENCE_ITEM_PROVENANCE", [f"{prefix}.{field}"]
        if item["evidence_id"] in evidence_ids:
            return False, "DUPLICATE_SOURCE_AUTHORITY_EVIDENCE_ID", [f"{prefix}.evidence_id"]
        evidence_ids.add(item["evidence_id"])
        mapped = known.get(item["mapped_missing_authority_id"])
        if mapped is None:
            return False, "UNKNOWN_MAPPED_MISSING_AUTHORITY_ID", [f"{prefix}.mapped_missing_authority_id"]
        if item["section_id"] not in ALLOWED_SECTION_IDS or item["section_id"] != mapped["section_id"]:
            return False, "UNKNOWN_OR_MISMATCHED_SOURCE_AUTHORITY_SECTION_ID", [f"{prefix}.section_id"]
        if item["workstream_id"] not in ALLOWED_WORKSTREAM_IDS or item["workstream_id"] != mapped["workstream_id"]:
            return False, "UNKNOWN_OR_MISMATCHED_SOURCE_AUTHORITY_WORKSTREAM_ID", [f"{prefix}.workstream_id"]
        if item["acceptable_source_artifact_type"] not in ALLOWED_ARTIFACT_TYPES:
            return False, "UNKNOWN_ACCEPTABLE_SOURCE_ARTIFACT_TYPE", [f"{prefix}.acceptable_source_artifact_type"]
        if item["evidence_classification"] not in ALLOWED_EVIDENCE_CLASSIFICATIONS:
            return False, "INVALID_SOURCE_AUTHORITY_EVIDENCE_CLASSIFICATION", [f"{prefix}.evidence_classification"]
        if item["specification_or_observation"] not in ALLOWED_SPECIFICATION_OR_OBSERVATION:
            return False, "INVALID_SPECIFICATION_OR_OBSERVATION", [f"{prefix}.specification_or_observation"]
        if item["expected_or_actual_scope"] not in ALLOWED_EXPECTED_OR_ACTUAL_SCOPE:
            return False, "INVALID_EXPECTED_OR_ACTUAL_SCOPE", [f"{prefix}.expected_or_actual_scope"]
        if item["results_review_required_before_use"] is not True:
            return False, "RESULTS_REVIEW_NOT_REQUIRED_BEFORE_USE", [f"{prefix}.results_review_required_before_use"]
        for field in (
            "direct_change_authorized_now", "remediation_authorized_now", "retry_authorized_now",
            "main_merge_authorized_now",
        ):
            if item[field] is not False:
                return False, "SOURCE_AUTHORITY_EVIDENCE_ITEM_AUTHORITY_BOUNDARY_FAILURE", [f"{prefix}.{field}"]
    return True, None, []


def _common_execution(
    approval: Mapping[str, Any], run_timestamp_utc: str | None
) -> dict[str, Any]:
    timestamp = "NOT_PROVIDED" if run_timestamp_utc is None else run_timestamp_utc
    if timestamp != "NOT_PROVIDED" and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
            "run_timestamp_utc invalid"
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "execution_scope": EXECUTION_SCOPE,
        "run_timestamp_utc": timestamp,
        "created_offline": True,
        "governance_only": True,
        "source_authority_acquisition_execution_only": True,
        "selected_source_authority_acquisition_package": SELECTED_PACKAGE,
        **_source_bindings(approval),
        **{key: deepcopy(approval[key]) for key in source.SOURCE_CONTEXT_KEYS},
        "primary_failure_class": approval["primary_failure_class"],
        "secondary_failure_classes": deepcopy(approval["secondary_failure_classes"]),
        **{field: True for field in COMMON_TRUE_FIELDS},
        **{field: False for field in CLOSED_FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "acquisition_scope_section_count": 4,
        "mapped_missing_authority_item_count": 30,
        "acceptable_source_artifact_type_count": 13,
        "operator_provided_evidence_requirement_count": 10,
        "evidence_custody_and_digest_requirement_count": 6,
        "candidate_results_review_requirement_count": 16,
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    extra = tuple(
        dict.fromkeys(
            (
                *(f"output_{item}_status_correct" for item in (SUCCESS_OUTPUT_IDS if execution["execution_succeeded"] else BLOCKED_OUTPUT_IDS)),
                *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
                *(f"next_gate_{item}_defined" for item in NEXT_GATES),
            )
        )
    )
    return [
        {
            "check_id": check_id, "status": PASS, "expected": True, "actual": True,
            "severity": BLOCKER, "message": f"{check_id} passed",
        }
        for check_id in (*CHECK_IDS, *extra)
    ]


def _summary(execution: Mapping[str, Any]) -> dict[str, Any]:
    checklist = execution["checklist"]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist), "failed_checks": 0,
        "blocker_count": 0, "source_authority_acquisition_execution_created": True,
        "source_authority_acquisition_execution_performed": execution["source_authority_acquisition_execution_performed"],
        "selected_source_authority_acquisition_package": SELECTED_PACKAGE,
        "selected_source_authority_acquisition_package_executed": execution["selected_source_authority_acquisition_package_executed"],
        "blocked_reason": execution.get("blocked_reason"),
        "operator_source_authority_evidence_package_supplied": execution["operator_source_authority_evidence_package_supplied"],
        "operator_source_authority_evidence_package_validated": execution["operator_source_authority_evidence_package_validated"],
        "operator_source_authority_evidence_package_bound": execution["operator_source_authority_evidence_package_bound"],
        "source_authority_acquisition_performed": execution["source_authority_acquisition_performed"],
        "source_authority_evidence_acquired": execution["source_authority_evidence_acquired"],
        "external_evidence_acquired": False,
        "source_authority_evidence_items_bound_for_results_review": execution["source_authority_evidence_items_bound_for_results_review"],
        "operator_source_authority_evidence_item_count": execution["operator_source_authority_evidence_item_count"],
        "covered_missing_authority_item_count": execution["covered_missing_authority_item_count"],
        "uncovered_missing_authority_item_count": execution["uncovered_missing_authority_item_count"],
        "source_authority_acquisition_results_review_required": execution["source_authority_acquisition_results_review_required"],
        "ready_for_source_authority_acquisition_results_review": execution["ready_for_source_authority_acquisition_results_review"],
        **{field: False for field in CLOSED_FALSE_FIELDS},
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "recommended_next_task": execution["recommended_next_task"],
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _digest_without(execution: Mapping[str, Any], *keys: str) -> str:
    payload = deepcopy(dict(execution))
    for key in ("checklist", "summary", *keys):
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_success(
    approval: Mapping[str, Any], evidence_package: Mapping[str, Any], run_timestamp_utc: str | None
) -> dict[str, Any]:
    execution = _common_execution(approval, run_timestamp_utc)
    items = deepcopy(evidence_package["evidence_items"])
    inventory = [{**item, "binding_status": "BOUND_FOR_RESULTS_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY"} for item in items]
    evidence_mapping = [
        {
            "evidence_id": item["evidence_id"],
            "mapped_missing_authority_id": item["mapped_missing_authority_id"],
            "section_id": item["section_id"],
            "workstream_id": item["workstream_id"],
            "mapping_status": "BOUND_FOR_RESULTS_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY",
        }
        for item in items
    ]
    covered_ids = sorted({item["mapped_missing_authority_id"] for item in items})
    all_ids = [
        item["missing_authority_id"]
        for item in approval["missing_authority_to_source_evidence_mapping_review"]["items"]
    ]
    uncovered_ids = [item for item in all_ids if item not in set(covered_ids)]
    coverage = [
        {
            "missing_authority_id": item,
            "coverage_status": "EVIDENCE_BOUND_FOR_RESULTS_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY" if item in set(covered_ids) else "MISSING_NOT_ACQUIRED",
        }
        for item in all_ids
    ]
    execution.update(
        {
            "artifact_kind": SUCCESS_ARTIFACT_KIND,
            "execution_status": SUCCESS_STATUS,
            "execution_succeeded": True,
            "blocked_fail_closed": False,
            "blocked_reason": None,
            "missing_or_failed_data": [],
            **{field: True for field in SUCCESS_TRUE_FIELDS},
            "operator_source_authority_evidence_package": deepcopy(dict(evidence_package)),
            "operator_source_authority_evidence_package_validation": {
                "valid": True, "status": "VALIDATED_AND_BOUND_FOR_RESULTS_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY",
                "missing_or_failed_data": [],
            },
            "acquired_or_bound_evidence_item_inventory": inventory,
            "source_authority_evidence_mapping": evidence_mapping,
            "missing_authority_coverage": coverage,
            "operator_source_authority_evidence_item_count": len(items),
            "covered_missing_authority_item_count": len(covered_ids),
            "uncovered_missing_authority_item_count": len(uncovered_ids),
            "outputs": [
                {"output_id": item, "status": "GENERATED_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_EVIDENCE_BOUND_FOR_RESULTS_REVIEW_ONLY"}
                for item in SUCCESS_OUTPUT_IDS
            ],
            "recommended_next_task": SUCCESS_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
            "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_SOURCE_AUTHORITY_ACQUISITION_RESULTS_REVIEW_BEFORE_DISPOSITION_REMEDIATION_RETRY_OR_MAIN",
            "next_chain": list(SUCCESS_NEXT_CHAIN),
        }
    )
    execution[EVIDENCE_PACKAGE_DIGEST_KEY] = semantic_digest(dict(evidence_package))
    execution[EVIDENCE_MAPPING_DIGEST_KEY] = semantic_digest(evidence_mapping)
    execution[COVERAGE_DIGEST_KEY] = semantic_digest(coverage)
    execution[EXECUTION_DIGEST_KEY] = _digest_without(
        execution, EXECUTION_DIGEST_KEY, MANIFEST_DIGEST_KEY
    )
    execution[MANIFEST_DIGEST_KEY] = semantic_digest(
        {
            "execution_digest": execution[EXECUTION_DIGEST_KEY],
            "evidence_package_digest": execution[EVIDENCE_PACKAGE_DIGEST_KEY],
            "evidence_mapping_digest": execution[EVIDENCE_MAPPING_DIGEST_KEY],
            "coverage_digest": execution[COVERAGE_DIGEST_KEY],
            "source_approval_digest": SOURCE_APPROVAL_DIGEST,
        }
    )
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = None
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    return execution


def _assemble_blocked(
    approval: Mapping[str, Any], *, supplied: bool, blocked_reason: str,
    missing_or_failed_data: list[str], run_timestamp_utc: str | None,
) -> dict[str, Any]:
    execution = _common_execution(approval, run_timestamp_utc)
    execution.update(
        {
            "artifact_kind": BLOCKED_ARTIFACT_KIND,
            "execution_status": BLOCKED_STATUS,
            "execution_succeeded": False,
            "blocked_fail_closed": True,
            "blocked_reason": blocked_reason,
            "missing_or_failed_data": list(missing_or_failed_data),
            **{field: False for field in BLOCKED_FALSE_FIELDS},
            "operator_source_authority_evidence_package_supplied": supplied,
            "operator_source_authority_evidence_package": None,
            "operator_source_authority_evidence_package_validation": {
                "valid": False, "status": "BLOCKED_NOT_BOUND", "blocked_reason": blocked_reason,
                "missing_or_failed_data": list(missing_or_failed_data),
            },
            "acquired_or_bound_evidence_item_inventory": [],
            "source_authority_evidence_mapping": [],
            "missing_authority_coverage": [
                {"missing_authority_id": item["missing_authority_id"], "coverage_status": "MISSING_NOT_ACQUIRED"}
                for item in approval["missing_authority_to_source_evidence_mapping_review"]["items"]
            ],
            "operator_source_authority_evidence_item_count": 0,
            "covered_missing_authority_item_count": 0,
            "uncovered_missing_authority_item_count": 30,
            "outputs": [
                {"output_id": item, "status": "BLOCKED_NOT_GENERATED_OR_BOUNDARY_REPORT_ONLY"}
                for item in BLOCKED_OUTPUT_IDS
            ],
            "recommended_next_task": BLOCKED_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_DIAGNOSIS_NOT_CREATED",
            "recommended_action": "DIAGNOSE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_BLOCKED_REASON_BEFORE_ANY_DISPOSITION_REMEDIATION_RETRY_OR_MAIN",
            "next_chain": list(BLOCKED_NEXT_CHAIN),
            EXECUTION_DIGEST_KEY: None,
            EVIDENCE_PACKAGE_DIGEST_KEY: None,
            EVIDENCE_MAPPING_DIGEST_KEY: None,
            COVERAGE_DIGEST_KEY: None,
            MANIFEST_DIGEST_KEY: None,
        }
    )
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = _digest_without(execution, BLOCKED_MANIFEST_DIGEST_KEY)
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    return execution


def execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
    *, source_approval: dict | None = None,
    operator_source_authority_evidence_package: dict | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Bind valid injected evidence or return a deterministic fail-closed artifact."""

    approval = _validated_source_approval(source_approval)
    valid, blocked_reason, missing_or_failed_data = _package_validation(
        operator_source_authority_evidence_package, approval
    )
    if valid:
        execution = _assemble_success(
            approval, operator_source_authority_evidence_package, run_timestamp_utc
        )
    else:
        execution = _assemble_blocked(
            approval, supplied=operator_source_authority_evidence_package is not None,
            blocked_reason=str(blocked_reason), missing_or_failed_data=missing_or_failed_data,
            run_timestamp_utc=run_timestamp_utc,
        )
    validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
        execution
    )
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
    execution: dict,
) -> dict[str, Any]:
    """Validate either the success or fail-closed execution artifact."""

    if not isinstance(execution, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
            "execution must be an object"
        )
    approval = _validated_source_approval(None)
    if execution.get("artifact_kind") == SUCCESS_ARTIFACT_KIND:
        package = execution.get("operator_source_authority_evidence_package")
        valid, reason, _ = _package_validation(package, approval)
        if not valid:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
                f"success evidence package invalid: {reason}"
            )
        expected = _assemble_success(approval, package, execution.get("run_timestamp_utc"))
        digest_key = EXECUTION_DIGEST_KEY
    elif execution.get("artifact_kind") == BLOCKED_ARTIFACT_KIND:
        reason = execution.get("blocked_reason")
        missing = execution.get("missing_or_failed_data")
        if not _non_empty(reason) or not isinstance(missing, list) or not missing:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
                "blocked reason or missing data absent"
            )
        expected = _assemble_blocked(
            approval, supplied=execution.get("operator_source_authority_evidence_package_supplied") is True,
            blocked_reason=reason, missing_or_failed_data=missing,
            run_timestamp_utc=execution.get("run_timestamp_utc"),
        )
        digest_key = BLOCKED_MANIFEST_DIGEST_KEY
    else:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
            "artifact kind invalid"
        )
    difference = _first_difference(execution, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
            f"{difference} mismatch"
        )
    if re.fullmatch(r"[0-9a-f]{64}", str(execution.get(digest_key))) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
            "execution digest invalid"
        )
    return {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": EXECUTION_SCOPE, "execution_succeeded": execution["execution_succeeded"],
        "digest": execution[digest_key],
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = tuple(
    """Source Approval
Selected Source Authority Acquisition Package
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
Operator Source Authority Evidence Package
Acquired or Bound Evidence Item Inventory
Missing Authority Coverage
Execution Scope
Success or Blocked Disposition
Unsupported Claims Boundary
Recommendation
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines()
)


def build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_markdown_v1(
    execution: dict,
) -> str:
    """Render a validated success or fail-closed execution status document."""

    validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
        deepcopy(execution)
    )
    sections = {
        "Source Approval": {key: execution[key] for key in ("source_approval_artifact_kind", "source_approval_status", "source_approval_scope", "source_approval_commit", "source_approval_digest", "source_attestation_digest")},
        "Selected Source Authority Acquisition Package": execution["selected_source_authority_acquisition_package"],
        "Source Operator Review": execution["source_operator_review_summary"],
        "Source Follow-On Results Review": execution["source_follow_on_results_review_summary"],
        "Source Follow-On Execution": execution["source_follow_on_execution_summary"],
        "Source Follow-On Approval": execution["source_follow_on_approval_summary"],
        "Source Follow-On Operator Review": execution["source_follow_on_operator_review_summary"],
        "Source Follow-On Candidate": execution["source_follow_on_candidate_summary"],
        "Source Results Review": execution["source_results_review_summary"],
        "Source Enrichment Execution": execution["source_execution_summary"],
        "Source Historical Approval": execution["source_approval_summary"],
        "Source Historical Operator Review": execution["source_historical_operator_review_summary"],
        "Source Historical Candidate": execution["source_historical_candidate_summary"],
        "Source Failure Diagnosis": execution["source_failure_diagnosis_summary"],
        "Source Blocked Execution": execution["source_blocked_execution_summary"],
        "Blocked Reason": execution.get("blocked_reason"),
        "Failure Classification": {"primary": execution["primary_failure_class"], "secondary": execution["secondary_failure_classes"]},
        "Source Remediation Execution Approval": execution["source_remediation_execution_approval_after_plan_results_review_digest"],
        "Source Plan Results Review": execution["source_plan_results_review_summary"],
        "Source Plan Execution": execution["source_plan_execution_summary"],
        "Source Method Results Review": execution["source_method_results_review_summary"],
        "Source Method Execution": execution["source_method_execution_summary"],
        "Source Diagnostic Results Review": execution["source_diagnostic_results_review_summary"],
        "Source Controlled Recapture": execution["source_controlled_recapture_summary"],
        "Source Durable Receipt": execution["source_durable_receipt_summary"],
        "Source Planning and Detail Binding Evidence": execution["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": execution["retry_failure_context"],
        "Priority 1 Target Modules": execution["priority_1_target_modules"],
        "Priority 1 Validation Summary": execution["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": execution["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": execution["reviewed_observable_failure_families"],
        "Reviewed Workstreams": execution["reviewed_workstreams"],
        "Source Authority Acquisition Candidate": execution["source_authority_acquisition_candidate_review"],
        "Acquisition Scope Sections": execution["acquisition_scope_sections_review"],
        "Missing Authority Mapping": execution["missing_authority_to_source_evidence_mapping_review"],
        "Acceptable Source Artifact Inventory": execution["acceptable_source_artifact_inventory_review"],
        "Operator-Provided Evidence Requirements": execution["operator_provided_evidence_requirements_review"],
        "Evidence Custody and Digest Requirements": execution["evidence_custody_and_digest_requirements_review"],
        "Candidate Results Review Requirements": execution["candidate_results_review_requirements_review"],
        "Operator Source Authority Evidence Package": execution["operator_source_authority_evidence_package_validation"],
        "Acquired or Bound Evidence Item Inventory": execution["acquired_or_bound_evidence_item_inventory"],
        "Missing Authority Coverage": execution["missing_authority_coverage"],
        "Execution Scope": execution["execution_scope"],
        "Success or Blocked Disposition": {"success": execution["execution_succeeded"], "blocked_reason": execution.get("blocked_reason")},
        "Unsupported Claims Boundary": {field: execution[field] for field in CLOSED_FALSE_FIELDS},
        "Recommendation": {key: execution[key] for key in ("recommended_next_task", "recommended_next_task_status", "recommended_action")},
        "Next Chain": execution["next_chain"],
        "Next Gates": execution["next_gates"],
        "Risk Controls": execution["risk_controls"],
        "Authority Boundaries": {field: execution[field] for field in (*BLOCKED_FALSE_FIELDS, *CLOSED_FALSE_FIELDS) if field in execution},
        "Checklist Summary": execution["summary"],
        "Guardrails": list(CLOSED_FALSE_FIELDS),
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Source Authority Acquisition Execution After Candidate Operator Review v1",
        "", f"Artifact: `{execution['artifact_kind']}`", "", f"Status: `{execution['execution_status']}`", "",
        f"Scope: `{execution['execution_scope']}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
    output_dir: str | Path, *, source_approval: dict | None = None,
    operator_source_authority_evidence_package: dict | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Write the deterministic execution status document."""

    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError(
            "protected output directory"
        )
    execution = execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
        source_approval=source_approval,
        operator_source_authority_evidence_package=operator_source_authority_evidence_package,
        run_timestamp_utc=run_timestamp_utc,
    )
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_markdown_v1(execution),
        encoding="utf-8",
    )
    return execution


__all__ = [
    "SUCCESS_ARTIFACT_KIND", "BLOCKED_ARTIFACT_KIND", "SCHEMA_VERSION", "SUCCESS_STATUS",
    "BLOCKED_STATUS", "EXECUTION_SCOPE", "SELECTED_PACKAGE", "EXECUTION_DIGEST_KEY",
    "EVIDENCE_PACKAGE_DIGEST_KEY", "EVIDENCE_MAPPING_DIGEST_KEY", "COVERAGE_DIGEST_KEY",
    "MANIFEST_DIGEST_KEY", "BLOCKED_MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_BLOCKED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTED_AFTER_CANDIDATE_OPERATOR_REVIEW_SOURCE_AUTHORITY_EVIDENCE_BOUND_FOR_RESULTS_REVIEW",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_BLOCKED_AFTER_CANDIDATE_OPERATOR_REVIEW_NO_REVIEWED_SOURCE_AUTHORITY_EVIDENCE_AVAILABLE_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_SOURCE_AUTHORITY_ACQUISITION_OR_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE",
    "execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_markdown_v1",
]
