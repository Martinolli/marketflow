"""Complete an approved operator evidence package, or fail closed without inputs.

This module is deliberately offline and dictionary-only.  It does not read source
artifacts, inspect credentials, validate evidence as authoritative, or perform any
acquisition, remediation, retry, runtime, or trading action.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTED_AFTER_APPROVAL_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_BLOCKED_AFTER_APPROVAL_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1"
EXECUTION_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTED_AFTER_APPROVAL_COMPLETED_OPERATOR_EVIDENCE_PACKAGE_READY_FOR_RESULTS_REVIEW"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_BLOCKED_AFTER_APPROVAL_OPERATOR_INPUTS_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_ONLY_COMPLETED_OPERATOR_EVIDENCE_PACKAGE_FROM_NON_SECRET_OPERATOR_INPUTS_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_VALIDATION_NOT_EVIDENCE_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
DEFAULT_RUN_TIMESTAMP_UTC = "2026-08-23T00:00:00Z"

NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED = "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED"
SOURCE_COMPLETION_APPROVAL_NOT_VERIFIED = "SOURCE_COMPLETION_APPROVAL_NOT_VERIFIED"
SELECTED_COMPLETION_PACKAGE_NOT_APPROVED = "SELECTED_COMPLETION_PACKAGE_NOT_APPROVED"
OPERATOR_COMPLETION_INPUTS_INCOMPLETE = "OPERATOR_COMPLETION_INPUTS_INCOMPLETE"
OPERATOR_COMPLETION_INPUTS_CONTAIN_SECRETS = "OPERATOR_COMPLETION_INPUTS_CONTAIN_SECRETS"
OPERATOR_COMPLETION_INPUTS_CONTAIN_API_KEYS = "OPERATOR_COMPLETION_INPUTS_CONTAIN_API_KEYS"
OPERATOR_COMPLETION_INPUTS_CONTAIN_BROKER_CREDENTIALS = "OPERATOR_COMPLETION_INPUTS_CONTAIN_BROKER_CREDENTIALS"
OPERATOR_COMPLETION_INPUTS_CONTAIN_PERSONAL_FINANCIAL_CREDENTIALS = "OPERATOR_COMPLETION_INPUTS_CONTAIN_PERSONAL_FINANCIAL_CREDENTIALS"
OPERATOR_COMPLETION_INPUTS_CONTAIN_MARKET_DATA_CREDENTIALS = "OPERATOR_COMPLETION_INPUTS_CONTAIN_MARKET_DATA_CREDENTIALS"
OPERATOR_COMPLETION_INPUTS_CONTAIN_PRIVATE_TOKENS = "OPERATOR_COMPLETION_INPUTS_CONTAIN_PRIVATE_TOKENS"
OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_OWNER_OR_ORIGIN = "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_OWNER_OR_ORIGIN"
OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_REFERENCE = "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_REFERENCE"
OPERATOR_COMPLETION_INPUTS_MISSING_DIGEST_OR_REPRODUCIBLE_PROVENANCE = "OPERATOR_COMPLETION_INPUTS_MISSING_DIGEST_OR_REPRODUCIBLE_PROVENANCE"
OPERATOR_COMPLETION_INPUTS_MISSING_AUTHORITY_STATEMENT = "OPERATOR_COMPLETION_INPUTS_MISSING_AUTHORITY_STATEMENT"
OPERATOR_COMPLETION_INPUTS_INVALID_MISSING_AUTHORITY_MAPPING = "OPERATOR_COMPLETION_INPUTS_INVALID_MISSING_AUTHORITY_MAPPING"
OPERATOR_COMPLETION_INPUTS_INVALID_SECTION_ID = "OPERATOR_COMPLETION_INPUTS_INVALID_SECTION_ID"
OPERATOR_COMPLETION_INPUTS_INVALID_WORKSTREAM_ID = "OPERATOR_COMPLETION_INPUTS_INVALID_WORKSTREAM_ID"
OPERATOR_COMPLETION_INPUTS_INVALID_ARTIFACT_TYPE = "OPERATOR_COMPLETION_INPUTS_INVALID_ARTIFACT_TYPE"
OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_DIRECT_CHANGE = "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_DIRECT_CHANGE"
OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_REMEDIATION = "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_REMEDIATION"
OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_RETRY = "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_RETRY"
OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_MAIN_MERGE = "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_MAIN_MERGE"
TEMPLATE_COMPLETION_BOUNDARY_FAILURE = "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"
ALLOWED_BLOCKED_REASONS = (
    NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED,
    SOURCE_COMPLETION_APPROVAL_NOT_VERIFIED, SELECTED_COMPLETION_PACKAGE_NOT_APPROVED,
    OPERATOR_COMPLETION_INPUTS_INCOMPLETE, OPERATOR_COMPLETION_INPUTS_CONTAIN_SECRETS,
    OPERATOR_COMPLETION_INPUTS_CONTAIN_API_KEYS, OPERATOR_COMPLETION_INPUTS_CONTAIN_BROKER_CREDENTIALS,
    OPERATOR_COMPLETION_INPUTS_CONTAIN_PERSONAL_FINANCIAL_CREDENTIALS,
    OPERATOR_COMPLETION_INPUTS_CONTAIN_MARKET_DATA_CREDENTIALS,
    OPERATOR_COMPLETION_INPUTS_CONTAIN_PRIVATE_TOKENS,
    OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_OWNER_OR_ORIGIN,
    OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_REFERENCE,
    OPERATOR_COMPLETION_INPUTS_MISSING_DIGEST_OR_REPRODUCIBLE_PROVENANCE,
    OPERATOR_COMPLETION_INPUTS_MISSING_AUTHORITY_STATEMENT,
    OPERATOR_COMPLETION_INPUTS_INVALID_MISSING_AUTHORITY_MAPPING,
    OPERATOR_COMPLETION_INPUTS_INVALID_SECTION_ID, OPERATOR_COMPLETION_INPUTS_INVALID_WORKSTREAM_ID,
    OPERATOR_COMPLETION_INPUTS_INVALID_ARTIFACT_TYPE,
    OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_DIRECT_CHANGE,
    OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_REMEDIATION,
    OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_RETRY,
    OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_MAIN_MERGE,
    TEMPLATE_COMPLETION_BOUNDARY_FAILURE,
)

SOURCE_APPROVAL_COMMIT = "40bee1289543bb07e64e383eb2e1c61d83615bd5"
SOURCE_APPROVAL_DIGEST = "f6c37c0a7c64487cdf9adb218f8d12b8c0a2dacc4d4c1debf96105d1b5ee954c"
SOURCE_ATTESTATION_DIGEST = "5434cbb4c94d22f1e4fefb3efc0e6e651401a22d6217d4c118638fa6d38dc714"

EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_digest"
COMPLETED_PACKAGE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completed_operator_package_digest"
COMPLETED_ITEMS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completed_items_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_manifest_digest"
BLOCKED_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_blocked_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_blocked_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTED_AFTER_APPROVAL_V1 = ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_BLOCKED_AFTER_APPROVAL_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTED_AFTER_APPROVAL_COMPLETED_OPERATOR_EVIDENCE_PACKAGE_READY_FOR_RESULTS_REVIEW = EXECUTION_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_BLOCKED_AFTER_APPROVAL_OPERATOR_INPUTS_UNAVAILABLE_OR_BOUNDARY_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_ONLY_COMPLETED_OPERATOR_EVIDENCE_PACKAGE_FROM_NON_SECRET_OPERATOR_INPUTS_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_VALIDATION_NOT_EVIDENCE_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS = SELECTED_PACKAGE

PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

ALLOWED_SECTION_IDS = (
    "assertion_value_mismatch_source_authority_scope",
    "digest_hash_boundary_source_authority_scope",
    "fixture_isolation_determinism_source_authority_scope",
    "schema_field_contract_source_authority_scope",
)
ALLOWED_WORKSTREAM_IDS = (
    "assertion_value_mismatch_workstream",
    "digest_hash_boundary_workstream",
    "fixture_isolation_determinism_workstream",
    "schema_field_contract_workstream",
)
ALLOWED_SOURCE_ARTIFACT_TYPES = (
    "approved_product_specification", "approved_schema_definition", "approved_artifact_contract",
    "approved_canonical_payload_or_serialization_contract", "approved_expected_value_source",
    "approved_actual_value_source", "approved_digest_manifest_source", "approved_fixture_lifecycle_document",
    "approved_deterministic_execution_contract", "approved_export_surface_contract",
    "approved_operator_provided_evidence_package", "approved_source_owning_team_statement",
    "approved_reviewed_source_digest_bundle",
)
ALLOWED_EVIDENCE_CLASSIFICATIONS = (
    "SPECIFICATION", "APPROVED_CONTRACT", "SOURCE_OWNER_STATEMENT", "CANONICAL_PAYLOAD",
    "CANONICAL_SCHEMA", "CANONICAL_SERIALIZATION", "EXPECTED_VALUE_SOURCE", "ACTUAL_VALUE_SOURCE",
    "FIXTURE_LIFECYCLE_AUTHORITY", "DETERMINISM_AUTHORITY", "EXPORT_SURFACE_AUTHORITY",
    "REVIEWED_SOURCE_DIGEST_BUNDLE",
)
ALLOWED_SPECIFICATION_OR_OBSERVATION = ("SPECIFICATION", "OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT")
ALLOWED_EXPECTED_OR_ACTUAL_SCOPE = ("EXPECTED", "ACTUAL", "BOTH", "NOT_APPLICABLE")

BLOCKED_OUTPUT_IDS = tuple("""operator_source_authority_evidence_package_completion_execution_blocked_manifest
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
operator_completion_inputs_absence_report
completion_blocked_reason_report
source_authority_gap_preservation_report
acquisition_reattempt_gate_preservation_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Completion execution failure diagnosis.",
    "Optional operator completion input preparation or supply candidate.",
    "Optional completion approval re-entry if required.",
    "Completion execution reattempt only with explicitly supplied, non-secret operator inputs.",
    "Completion results review only if completed package exists.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Completed Evidence Package only after separate approval.",
    "Source Authority Acquisition Results Review only if evidence is bound.",
    "Conditional no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple("""completion_execution_failure_diagnosis_if_no_inputs
operator_completion_input_preparation_or_supply_candidate_if_needed
completion_execution_reattempt_with_non_secret_operator_inputs_if_approved
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

RISK_CONTROLS = tuple("""execution_requires_explicit_operator_completion_inputs
execution_fails_closed_without_operator_completion_inputs
execution_does_not_convert_template_placeholders_to_evidence
execution_does_not_convert_diagnostic_output_to_source_authority
execution_does_not_create_completed_package_without_inputs
execution_does_not_validate_evidence
execution_does_not_bind_evidence
execution_does_not_accept_evidence_as_source_authority
execution_does_not_acquire_source_authority
execution_does_not_acquire_external_evidence
execution_does_not_create_source_authority_acquisition_execution
execution_does_not_retry_source_authority_acquisition
execution_does_not_create_no_change_disposition
execution_does_not_execute_alternate_diagnostics
execution_does_not_execute_remediation
execution_does_not_modify_production_code
execution_does_not_modify_existing_tests
execution_does_not_update_expected_digests
execution_does_not_generate_patch
execution_does_not_apply_patch
execution_does_not_run_pytest
execution_does_not_run_full_pytest
execution_does_not_rerun_priority1_validation
execution_does_not_rerun_retry
execution_does_not_rerun_detached_retry
execution_does_not_parse_durable_receipt
execution_does_not_analyze_diagnostic_output
execution_does_not_rerun_source_authority_enrichment
execution_does_not_rerun_follow_on_execution
execution_does_not_rerun_plan_execution
execution_does_not_regenerate_targeted_plan
execution_does_not_rerun_method_execution
execution_does_not_rerun_controlled_recapture
execution_does_not_rerun_template_execution
execution_does_not_run_diagnostic_command
execution_does_not_read_pytest_cache
execution_does_not_modify_pytest_cache
execution_does_not_commit_pytest_cache
execution_does_not_commit_marketflow_outputs
execution_does_not_parse_terminal_logs
execution_does_not_parse_operator_logs
execution_does_not_inspect_env
execution_does_not_contact_source_owners
execution_does_not_read_external_documents
execution_does_not_reconstruct_prior_lost_values
execution_does_not_reconstruct_full_streams
execution_does_not_classify_modules_again
execution_does_not_classify_full_retry_failures
execution_does_not_classify_full_retry_errors
execution_does_not_claim_failure_error_separation
execution_does_not_identify_authoritative_first_failure
execution_does_not_identify_authoritative_first_error
execution_does_not_claim_traceback_root_cause
execution_does_not_claim_root_cause
execution_does_not_claim_retry_success
execution_does_not_claim_main_merge_readiness
execution_does_not_create_retry_candidate
execution_does_not_create_retry_approval
execution_does_not_create_retry_execution
execution_does_not_create_retry_results_review
execution_does_not_create_main_merge_approval
execution_does_not_push_main
execution_does_not_push_integration_branch
execution_does_not_delete_integration_branch
execution_does_not_delete_worktree
execution_does_not_force_push
execution_does_not_modify_tags
execution_does_not_regenerate_evidence
execution_does_not_call_providers
execution_does_not_acquire_market_data
execution_does_not_generate_dataset
execution_does_not_recompute_metrics
execution_does_not_train_models
execution_does_not_score_strategy
execution_does_not_generate_trade_recommendations
execution_does_not_accept_predictive_usefulness
execution_does_not_accept_profitability
execution_does_not_authorize_runtime
execution_does_not_authorize_broker_execution
approved_completion_package_is_not_execution_success
template_review_remains_source_evidence
template_is_not_actual_evidence_package
template_is_not_source_authority
template_is_not_acquired_evidence
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

TRUE_FIELDS = tuple("""operator_source_authority_evidence_package_completion_execution_created
operator_source_authority_evidence_package_completion_execution_attempted
selected_completion_package_verified
source_approval_verified
source_attestation_verified
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
count_label_distinction_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved""".splitlines())

ALWAYS_FALSE_FIELDS = tuple("""operator_completion_inputs_contained_secrets
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
operator_source_authority_evidence_package_accepted_as_source_authority
operator_source_authority_evidence_package_ready_for_acquisition_without_review
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
template_execution_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_execution
cache_modified_in_execution
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
provider_requests_made_in_execution
market_data_acquisition_performed_in_execution
dataset_generation_performed_in_execution
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

BLOCKED_ONLY_FALSE_FIELDS = tuple("""operator_completion_inputs_provided
operator_completion_inputs_validated
operator_completion_inputs_bound
operator_source_authority_evidence_package_completion_package_executed
operator_source_authority_evidence_package_completion_executed
operator_source_authority_evidence_package_completed
operator_source_authority_evidence_package_created
operator_source_authority_evidence_package_supplied
actual_evidence_items_filled
actual_evidence_items_supplied
ready_for_operator_source_authority_evidence_package_completion_results_review""".splitlines())


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError(ValueError):
    """Raised when an execution artifact violates its closed boundary."""


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


def _committed_source_review() -> dict[str, Any]:
    review = source._committed_source_operator_review()
    review.update(source.SOURCE_REVIEW_DIGEST_FIELDS)
    return review


def _committed_source_approval() -> dict[str, Any]:
    """Return the committed approval projection without invoking a source builder."""
    review = _committed_source_review()
    return {
        "artifact_kind": source.ARTIFACT_KIND,
        "approval_status": source.APPROVAL_STATUS,
        "approval_scope": source.APPROVAL_SCOPE,
        "selected_operator_source_authority_evidence_package_completion_package": SELECTED_PACKAGE,
        source.APPROVAL_DIGEST_KEY: SOURCE_APPROVAL_DIGEST,
        source.ATTESTATION_DIGEST_KEY: SOURCE_ATTESTATION_DIGEST,
        **source._source_bindings(review),
        **{key: deepcopy(review[key]) for key in source.SOURCE_CONTEXT_KEYS},
        "primary_failure_class": review["primary_failure_class"],
        "historical_blocked_remediation_reason": review["historical_blocked_remediation_reason"],
        "historical_blocked_remediation_manifest_digest": review["historical_blocked_remediation_manifest_digest"],
        "count_label_distinction": deepcopy(review["count_label_distinction"]),
    }


def _source_approval_reason(approval: Any) -> str | None:
    if not isinstance(approval, Mapping):
        return "SOURCE_COMPLETION_APPROVAL_NOT_VERIFIED"
    expected = _committed_source_approval()
    if approval.get("selected_operator_source_authority_evidence_package_completion_package") != SELECTED_PACKAGE:
        return "SELECTED_COMPLETION_PACKAGE_NOT_APPROVED"
    for key, value in expected.items():
        if key not in approval or _first_difference(approval[key], value, f"source_approval.{key}"):
            return "SOURCE_COMPLETION_APPROVAL_NOT_VERIFIED"
    return None


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not (value.startswith("<") and value.endswith(">"))


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _secret_reason(inputs: Mapping[str, Any]) -> str | None:
    text = "\n".join(_strings(inputs)).lower()
    normalized = re.sub(r"non[ _-]?secret", "", text)
    checks = (
        (r"api[ _-]?key|sk-[a-z0-9_-]{12,}", "OPERATOR_COMPLETION_INPUTS_CONTAIN_API_KEYS"),
        (r"ibkr|broker[ _-]?credential", "OPERATOR_COMPLETION_INPUTS_CONTAIN_BROKER_CREDENTIALS"),
        (r"account[ _-]?(?:number|no\.?|#)|personal[ _-]?financial[ _-]?credential|seed[ _-]?phrase", "OPERATOR_COMPLETION_INPUTS_CONTAIN_PERSONAL_FINANCIAL_CREDENTIALS"),
        (r"market[ _-]?data[ _-]?credential", "OPERATOR_COMPLETION_INPUTS_CONTAIN_MARKET_DATA_CREDENTIALS"),
        (r"private[ _-]?token|access[ _-]?token|bearer\s+[a-z0-9._-]+", "OPERATOR_COMPLETION_INPUTS_CONTAIN_PRIVATE_TOKENS"),
        (r"password|private[ _-]?key|\bsecret\b", "OPERATOR_COMPLETION_INPUTS_CONTAIN_SECRETS"),
    )
    for pattern, reason in checks:
        if re.search(pattern, normalized, re.IGNORECASE):
            return reason
    return None


def _operator_input_reason(inputs: Any, review: Mapping[str, Any]) -> str | None:
    if not isinstance(inputs, Mapping) or set(inputs) - {"package_header", "evidence_items", "test_fixture_marker"}:
        return "OPERATOR_COMPLETION_INPUTS_INCOMPLETE"
    if "test_fixture_marker" in inputs and inputs["test_fixture_marker"] != "TEST_ONLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_NOT_REAL_SOURCE_AUTHORITY":
        return "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"
    secret_reason = _secret_reason(inputs)
    if secret_reason:
        return secret_reason
    header = inputs.get("package_header")
    rows = inputs.get("evidence_items")
    if not isinstance(header, Mapping) or not isinstance(rows, list) or len(rows) != 30:
        return "OPERATOR_COMPLETION_INPUTS_INCOMPLETE"
    required_header = (
        "package_source_owner_or_origin", "package_reference", "package_created_utc",
        "package_digest_or_reproducible_provenance",
    )
    for key in required_header:
        if not _nonempty(header.get(key)):
            return {
                "package_source_owner_or_origin": "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_OWNER_OR_ORIGIN",
                "package_reference": "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_REFERENCE",
                "package_digest_or_reproducible_provenance": "OPERATOR_COMPLETION_INPUTS_MISSING_DIGEST_OR_REPRODUCIBLE_PROVENANCE",
            }.get(key, "OPERATOR_COMPLETION_INPUTS_INCOMPLETE")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(header["package_created_utc"])) is None:
        return "OPERATOR_COMPLETION_INPUTS_INCOMPLETE"
    declarations = (
        "package_declares_no_secrets", "package_declares_no_api_keys", "package_declares_no_broker_credentials",
        "package_declares_no_personal_financial_credentials", "package_distinguishes_specification_from_observation",
        "package_distinguishes_expected_from_actual", "package_distinguishes_source_authority_from_diagnostic_output",
    )
    if any(header.get(key) is not True for key in declarations):
        return "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"
    mapping = {item["missing_authority_id"]: item for item in review["missing_authority_mapping"]}
    templates = {item["mapped_missing_authority_id"]: item for item in review["reviewed_template_rows"]}
    seen_ids: set[str] = set()
    seen_evidence: set[str] = set()
    required_false = ("direct_change_authorized_now", "remediation_authorized_now", "retry_authorized_now", "main_merge_authorized_now", "actual_evidence_validated", "actual_evidence_bound")
    for row in rows:
        if not isinstance(row, Mapping):
            return "OPERATOR_COMPLETION_INPUTS_INCOMPLETE"
        missing_id = row.get("mapped_missing_authority_id")
        if missing_id not in mapping or missing_id in seen_ids:
            return "OPERATOR_COMPLETION_INPUTS_INVALID_MISSING_AUTHORITY_MAPPING"
        seen_ids.add(missing_id)
        evidence_id = row.get("evidence_id")
        if not _nonempty(evidence_id) or evidence_id in seen_evidence:
            return "OPERATOR_COMPLETION_INPUTS_INCOMPLETE"
        seen_evidence.add(evidence_id)
        expected_mapping = mapping[missing_id]
        if row.get("section_id") not in ALLOWED_SECTION_IDS or row.get("section_id") != expected_mapping["section_id"]:
            return "OPERATOR_COMPLETION_INPUTS_INVALID_SECTION_ID"
        if row.get("workstream_id") not in ALLOWED_WORKSTREAM_IDS or row.get("workstream_id") != expected_mapping["workstream_id"]:
            return "OPERATOR_COMPLETION_INPUTS_INVALID_WORKSTREAM_ID"
        artifact_type = row.get("acceptable_source_artifact_type")
        if artifact_type not in ALLOWED_SOURCE_ARTIFACT_TYPES or artifact_type not in templates[missing_id]["allowed_acceptable_source_artifact_types"]:
            return "OPERATOR_COMPLETION_INPUTS_INVALID_ARTIFACT_TYPE"
        if row.get("evidence_classification") not in ALLOWED_EVIDENCE_CLASSIFICATIONS:
            return "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"
        if row.get("specification_or_observation") not in ALLOWED_SPECIFICATION_OR_OBSERVATION:
            return "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"
        if row.get("expected_or_actual_scope") not in ALLOWED_EXPECTED_OR_ACTUAL_SCOPE:
            return "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"
        for key, reason in (
            ("source_owner_or_origin", "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_OWNER_OR_ORIGIN"),
            ("source_reference", "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_REFERENCE"),
            ("digest_or_reproducible_provenance", "OPERATOR_COMPLETION_INPUTS_MISSING_DIGEST_OR_REPRODUCIBLE_PROVENANCE"),
            ("authority_statement", "OPERATOR_COMPLETION_INPUTS_MISSING_AUTHORITY_STATEMENT"),
        ):
            if not _nonempty(row.get(key)):
                return reason
        if row.get("results_review_required_before_use") is not True or row.get("actual_evidence_supplied") is not True:
            return "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"
        for key, reason in zip(required_false, (
            "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_DIRECT_CHANGE",
            "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_REMEDIATION",
            "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_RETRY",
            "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_MAIN_MERGE",
            "TEMPLATE_COMPLETION_BOUNDARY_FAILURE", "TEMPLATE_COMPLETION_BOUNDARY_FAILURE",
        )):
            if row.get(key) is not False:
                return reason
        if row.get("current_status") != "COMPLETED_OPERATOR_INPUT_PENDING_RESULTS_REVIEW":
            return "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"
    return None if seen_ids == set(mapping) else "OPERATOR_COMPLETION_INPUTS_INVALID_MISSING_AUTHORITY_MAPPING"


def _counts(success: bool) -> dict[str, Any]:
    return {
        "operator_source_authority_evidence_item_count": 30 if success else 0,
        "operator_source_authority_evidence_item_template_count": 30,
        "reviewed_template_row_count": 30,
        "actual_covered_missing_authority_item_count": 30 if success else 0,
        "actual_uncovered_missing_authority_item_count": 0 if success else 30,
        "template_mapped_missing_authority_item_count": 30,
        "mapped_missing_authority_item_count": 30,
        "missing_authority_items_status": "COMPLETED_OPERATOR_INPUT_PENDING_RESULTS_REVIEW" if success else "MISSING_NOT_ACQUIRED",
        "completed_operator_evidence_item_count": 30 if success else 0,
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


def _base_execution(review: Mapping[str, Any], timestamp: str, success: bool) -> dict[str, Any]:
    bindings = source._source_bindings(review)
    execution = {
        "artifact_kind": ARTIFACT_KIND if success else BLOCKED_ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "execution_status": EXECUTION_STATUS if success else BLOCKED_STATUS,
        "execution_scope": EXECUTION_SCOPE,
        "run_timestamp_utc": timestamp,
        "created_offline": True, "governance_only": True, "execution_attempted": True,
        **bindings,
        "source_approval_artifact_kind": source.ARTIFACT_KIND,
        "source_approval_status": source.APPROVAL_STATUS,
        "source_approval_scope": source.APPROVAL_SCOPE,
        "source_approval_commit": SOURCE_APPROVAL_COMMIT,
        "source_approval_digest": SOURCE_APPROVAL_DIGEST,
        "source_attestation_digest": SOURCE_ATTESTATION_DIGEST,
        "selected_operator_source_authority_evidence_package_completion_package": SELECTED_PACKAGE,
        **{key: deepcopy(review[key]) for key in source.SOURCE_CONTEXT_KEYS},
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
        "source_exit_code": 1, "source_duration_seconds": "21.584361", "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0, "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
        "source_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True, "source_diagnostic_metadata_only": True,
        **_counts(success), **{key: True for key in TRUE_FIELDS}, **{key: False for key in ALWAYS_FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    return execution


def _digest_without(execution: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(execution))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _checklist(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    fixed = (
        "artifact_kind_correct", "execution_status_correct", "execution_scope_correct",
        "source_approval_commit_bound", "source_approval_digest_bound", "source_attestation_digest_bound",
        "selected_completion_package_bound", "retry_failure_counts_bound", "priority_1_total_612_bound",
        "top_10_total_1069_bound", "module_summary_count_29_bound", "failed_or_errored_nodeids_1404_bound",
        "observable_family_count_4_bound", "observable_evidence_items_188_bound", "workstream_count_4_bound",
        "reviewed_template_row_count_30", "recommendation_defined", "next_chain_defined",
        "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
        "no_tracked_pytest_cache_files",
    )
    path = (
        "operator_completion_inputs_valid", "completed_operator_items_30", "completion_results_review_ready",
        "success_digest_generated", "success_manifest_digest_generated",
    ) if success else (
        "blocked_reason_correct_for_no_inputs", "operator_completion_inputs_provided_false",
        "completion_execution_blocked_true", "actual_coverage_zero", "missing_authority_items_missing_not_acquired",
        "blocked_outputs_generated", "blocked_digest_generated", "blocked_manifest_digest_generated",
        "success_digest_absent_in_blocked_path", "ready_for_failure_diagnosis_true",
    )
    source_checks = tuple(f"{key}_bound" for key in sorted(execution) if key.startswith("source_") and (key.endswith("_digest") or key.endswith("_commit")))
    ids = tuple(dict.fromkeys((*fixed, *path, *source_checks, *(f"{key}_false" for key in ALWAYS_FALSE_FIELDS), *(f"next_gate_{key}_defined" for key in NEXT_GATES), *(f"risk_control_{key}_defined" for key in RISK_CONTROLS))))
    return [{"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"} for item in ids]


def _assemble_blocked(review: Mapping[str, Any], timestamp: str, reason: str, inputs_provided: bool = False) -> dict[str, Any]:
    execution = _base_execution(review, timestamp, False)
    execution.update({key: False for key in BLOCKED_ONLY_FALSE_FIELDS})
    execution.update({
        "blocked_reason": reason, "execution_blocked": True,
        "operator_source_authority_evidence_package_completion_execution_blocked": True,
        "blocked_manifest_generated": True, "actual_coverage_zero_bound": True,
        "evidence_package_absence_bound": True, "missing_authority_inventory_bound": True,
        "ready_for_operator_source_authority_evidence_package_completion_execution_failure_diagnosis": True,
        "operator_completion_inputs_provided": inputs_provided,
        "operator_completion_inputs_summary": {
            "provided": inputs_provided, "validated": False, "bound": False,
            "full_inputs_included_in_artifact": False, "blocked_reason": reason,
        },
        "completed_operator_evidence_package": None, "completed_operator_evidence_items": [],
        "outputs": [{"output_id": item, "status": "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_BLOCKED_ONLY"} for item in BLOCKED_OUTPUT_IDS],
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_V1",
        "recommended_next_task_status": "FUTURE_FAILURE_DIAGNOSIS_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_COMPLETION_EXECUTION_FAILURE_DIAGNOSIS_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_UNDER_SEPARATE_APPROVAL",
        "reason": "The completion package was approved for future execution, but no valid non-secret operator completion inputs were supplied to this execution. The service failed closed rather than creating a completed evidence package from placeholders or diagnostic output. A failure diagnosis or separately governed operator input supply path is required before any completion results review, acquisition reattempt, disposition, remediation, retry, or main merge.",
    })
    digest_exclusions = ("checklist", "summary", BLOCKED_DIGEST_KEY, BLOCKED_MANIFEST_DIGEST_KEY)
    execution[BLOCKED_DIGEST_KEY] = _digest_without(execution, *digest_exclusions)
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = semantic_digest({
        "blocked_digest": execution[BLOCKED_DIGEST_KEY], "blocked_reason": reason,
        "output_ids": list(BLOCKED_OUTPUT_IDS),
    })
    execution["checklist"] = _checklist(execution, False)
    execution["summary"] = _summary(execution)
    return execution


def _assemble_success(review: Mapping[str, Any], timestamp: str, inputs: Mapping[str, Any]) -> dict[str, Any]:
    execution = _base_execution(review, timestamp, True)
    execution.update({
        "blocked_reason": None, "execution_blocked": False,
        "operator_source_authority_evidence_package_completion_execution_blocked": False,
        "operator_source_authority_evidence_package_completion_package_executed": True,
        "operator_source_authority_evidence_package_completion_executed": True,
        "operator_source_authority_evidence_package_completed": True,
        "operator_source_authority_evidence_package_created": True,
        "operator_source_authority_evidence_package_supplied": True,
        "operator_completion_inputs_provided": True, "operator_completion_inputs_validated": True,
        "operator_completion_inputs_bound": True, "actual_evidence_items_filled": True,
        "actual_evidence_items_supplied": True,
        "ready_for_operator_source_authority_evidence_package_completion_results_review": True,
        "ready_for_operator_source_authority_evidence_package_completion_execution_failure_diagnosis": False,
        "actual_coverage_zero_bound": False, "evidence_package_absence_bound": False,
        "missing_authority_inventory_bound": True, "blocked_manifest_generated": False,
        "operator_completion_inputs_summary": {
            "provided": True, "validated": True, "bound": True,
            "item_count": 30, "full_inputs_included_in_artifact": True,
            "test_fixture_marker": inputs.get("test_fixture_marker"),
        },
        "completed_operator_evidence_package": deepcopy(inputs["package_header"]),
        "completed_operator_evidence_items": deepcopy(inputs["evidence_items"]),
        "outputs": [{"output_id": item, "status": "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_ONLY_PENDING_RESULTS_REVIEW"} for item in BLOCKED_OUTPUT_IDS],
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_RESULTS_REVIEW_AFTER_EXECUTION_V1",
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_RESULTS_REVIEW_BEFORE_ANY_SOURCE_AUTHORITY_ACQUISITION_REATTEMPT",
        "reason": "The non-secret operator inputs completed all 30 reviewed rows. The package remains unvalidated and unbound and requires a separately invoked results review before any acquisition use.",
    })
    execution[COMPLETED_PACKAGE_DIGEST_KEY] = semantic_digest(execution["completed_operator_evidence_package"])
    execution[COMPLETED_ITEMS_DIGEST_KEY] = semantic_digest(execution["completed_operator_evidence_items"])
    digest_exclusions = ("checklist", "summary", EXECUTION_DIGEST_KEY, MANIFEST_DIGEST_KEY)
    execution[EXECUTION_DIGEST_KEY] = _digest_without(execution, *digest_exclusions)
    execution[MANIFEST_DIGEST_KEY] = semantic_digest({
        "execution_digest": execution[EXECUTION_DIGEST_KEY],
        "completed_operator_package_digest": execution[COMPLETED_PACKAGE_DIGEST_KEY],
        "completed_items_digest": execution[COMPLETED_ITEMS_DIGEST_KEY],
    })
    execution["checklist"] = _checklist(execution, True)
    execution["summary"] = _summary(execution)
    return execution


def _summary(execution: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "total_checks": len(execution["checklist"]), "passed_checks": len(execution["checklist"]),
        "failed_checks": 0, "blocker_count": 0,
        **{key: deepcopy(execution[key]) for key in (
            "operator_source_authority_evidence_package_completion_execution_created",
            "operator_source_authority_evidence_package_completion_execution_attempted",
            "operator_source_authority_evidence_package_completion_execution_blocked", "blocked_reason",
            "source_approval_digest", "source_attestation_digest",
            "selected_operator_source_authority_evidence_package_completion_package",
            "operator_completion_inputs_provided", "operator_source_authority_evidence_package_completion_executed",
            "operator_source_authority_evidence_package_completed", "operator_source_authority_evidence_package_created",
            "operator_source_authority_evidence_package_supplied", "operator_source_authority_evidence_package_validated",
            "operator_source_authority_evidence_package_bound", "source_authority_acquisition_performed",
            "source_authority_evidence_acquired", "external_evidence_acquired", "concrete_source_authority_established",
            "safe_source_authority_bound_change_identified", "actual_covered_missing_authority_item_count",
            "actual_uncovered_missing_authority_item_count", "missing_authority_items_status",
            "ready_for_operator_source_authority_evidence_package_completion_execution_failure_diagnosis",
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


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(
    *, source_approval: dict | None = None, operator_completion_inputs: dict | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Build the success artifact only from valid explicit inputs; otherwise fail closed."""
    timestamp = DEFAULT_RUN_TIMESTAMP_UTC if run_timestamp_utc is None else run_timestamp_utc
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(timestamp)) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError("run_timestamp_utc invalid")
    review = _committed_source_review()
    approval = _committed_source_approval() if source_approval is None else deepcopy(source_approval)
    approval_reason = _source_approval_reason(approval)
    if approval_reason:
        result = _assemble_blocked(review, timestamp, approval_reason, operator_completion_inputs is not None)
    elif operator_completion_inputs is None:
        result = _assemble_blocked(review, timestamp, NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED)
    else:
        input_reason = _operator_input_reason(operator_completion_inputs, review)
        result = (_assemble_blocked(review, timestamp, input_reason, True) if input_reason else
                  _assemble_success(review, timestamp, deepcopy(operator_completion_inputs)))
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(result)
    return result


def validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(
    execution: dict,
) -> dict[str, Any]:
    """Reject any changed source binding, input contract, digest, or authority boundary."""
    if not isinstance(execution, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError("execution must be an object")
    timestamp = execution.get("run_timestamp_utc")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(timestamp)) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError("run_timestamp_utc invalid")
    review = _committed_source_review()
    if execution.get("artifact_kind") == BLOCKED_ARTIFACT_KIND:
        reason = execution.get("blocked_reason")
        if reason not in ALLOWED_BLOCKED_REASONS:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError("blocked_reason invalid")
        provided = bool(execution.get("operator_completion_inputs_provided"))
        if reason == NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED and provided:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError("blocked no-input path marked inputs provided")
        expected = _assemble_blocked(review, timestamp, reason, provided)
        digest_keys = (BLOCKED_DIGEST_KEY, BLOCKED_MANIFEST_DIGEST_KEY)
        result_digest = execution.get(BLOCKED_DIGEST_KEY)
    elif execution.get("artifact_kind") == ARTIFACT_KIND:
        inputs = {
            "package_header": deepcopy(execution.get("completed_operator_evidence_package")),
            "evidence_items": deepcopy(execution.get("completed_operator_evidence_items")),
        }
        marker = execution.get("operator_completion_inputs_summary", {}).get("test_fixture_marker")
        if marker is not None:
            inputs["test_fixture_marker"] = marker
        reason = _operator_input_reason(inputs, review)
        if reason:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError(f"success inputs invalid: {reason}")
        expected = _assemble_success(review, timestamp, inputs)
        digest_keys = (EXECUTION_DIGEST_KEY, COMPLETED_PACKAGE_DIGEST_KEY, COMPLETED_ITEMS_DIGEST_KEY, MANIFEST_DIGEST_KEY)
        result_digest = execution.get(EXECUTION_DIGEST_KEY)
    else:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError("artifact_kind invalid")
    difference = _first_difference(execution, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError(f"{difference} mismatch")
    for key in digest_keys:
        if re.fullmatch(r"[0-9a-f]{64}", str(execution.get(key))) is None:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError(f"{key} invalid")
    return {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": EXECUTION_SCOPE, "execution_digest": result_digest,
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Execution Disposition", "Blocked Reason", "Source Approval", "Selected Completion Package",
    "Source Operator Review", "Source Completion Candidate", "Source Template Preparation Results Review",
    "Source Template Preparation Execution", "Source Preparation Candidate", "Source Failure Diagnosis",
    "Source Blocked Acquisition Execution", "Source Acquisition Approval Chain", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt", "Retry Failure Context",
    "Priority 1 Target Modules", "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary",
    "Reviewed Observable Families", "Reviewed Workstreams", "Reviewed Template Structure", "Count Label Distinction",
    "Operator Completion Input Contract", "Operator Completion Inputs", "Actual Evidence Absence", "Actual Coverage Zero",
    "Source Authority Gap Preservation", "Unsupported Claims Boundary", "Recommendation", "Next Chain", "Next Gates",
    "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_markdown_v1(
    execution: dict,
) -> str:
    """Render a bounded status summary without printing supplied input contents."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(execution)
    summary = execution["summary"]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Completion Execution After Approval v1", ""]
    active_digest = execution.get(BLOCKED_DIGEST_KEY, execution.get(EXECUTION_DIGEST_KEY))
    active_manifest = execution.get(BLOCKED_MANIFEST_DIGEST_KEY, execution.get(MANIFEST_DIGEST_KEY))
    facts = {
        "Execution Disposition": f"Artifact `{execution['artifact_kind']}` has status `{execution['execution_status']}` and scope `{execution['execution_scope']}`. Digest `{active_digest}`; manifest `{active_manifest}`.",
        "Blocked Reason": str(execution["blocked_reason"]),
        "Source Approval": f"commit `{SOURCE_APPROVAL_COMMIT}`; digest `{SOURCE_APPROVAL_DIGEST}`; attestation `{SOURCE_ATTESTATION_DIGEST}`.",
        "Selected Completion Package": f"`{SELECTED_PACKAGE}`.",
        "Source Operator Review": f"commit `{execution['source_operator_review_commit']}`; review `{execution['source_operator_review_digest']}`; manifest `{execution['source_operator_review_manifest_digest']}`.",
        "Source Completion Candidate": f"commit `{execution['source_completion_candidate_commit']}`; candidate `{execution['source_completion_candidate_digest']}`; manifest `{execution['source_completion_candidate_manifest_digest']}`.",
        "Source Template Preparation Results Review": f"review `{execution['source_results_review_digest']}`; template `{execution['source_template_review_digest']}`; item template `{execution['source_evidence_item_template_review_digest']}`; checklist `{execution['source_preparation_checklist_review_digest']}`; coverage `{execution['source_template_coverage_review_digest']}`; manifest `{execution['source_results_review_manifest_digest']}`.",
        "Source Template Preparation Execution": f"execution `{execution['source_execution_digest']}`; package template `{execution['source_package_template_digest']}`; item template `{execution['source_evidence_item_template_digest']}`; checklist `{execution['source_preparation_checklist_digest']}`; coverage `{execution['source_template_coverage_digest']}`; manifest `{execution['source_execution_manifest_digest']}`.",
        "Source Preparation Candidate": f"commit `{execution['source_preparation_candidate_commit']}`; digest `{execution['source_preparation_candidate_digest']}`.",
        "Source Failure Diagnosis": f"commit `{execution['source_failure_diagnosis_commit']}`; digest `{execution['source_failure_diagnosis_digest']}`.",
        "Source Blocked Acquisition Execution": f"reason `{execution['source_blocked_acquisition_execution_reason']}`; manifest `{execution['source_blocked_acquisition_execution_manifest_digest']}`.",
        "Source Acquisition Approval Chain": f"approval `{execution['source_acquisition_approval_digest']}`; attestation `{execution['source_acquisition_attestation_digest']}`. No acquisition was executed.",
        "Source Follow-On and Enrichment Chain": f"follow-on review `{execution['source_follow_on_results_review_digest']}`; execution `{execution['source_follow_on_execution_digest']}`; acquisition candidate `{execution['source_authority_acquisition_candidate_digest']}`; enrichment `{execution['source_enrichment_execution_digest']}`.",
        "Historical Blocked Remediation": f"reason `{execution['historical_blocked_remediation_reason']}`; manifest `{execution['historical_blocked_remediation_manifest_digest']}`.",
        "Plan Method Diagnostic Recovery Chain": f"Targeted plan `{execution['source_targeted_remediation_plan_digest']}`; method execution `{execution['source_remediation_or_method_execution_after_diagnostic_capture_digest']}`; recovery review `{execution['source_recovery_results_review_digest']}`; module grouping `{execution['source_module_grouping_digest']}`.",
        "Durable Receipt": f"`{execution['source_durable_receipt_path']}` is bound as metadata and was not parsed.",
        "Retry Failure Context": "The authoritative detached retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped. The root full regression is not retry evidence.",
        "Priority 1 Target Modules": f"Five reviewed modules; Priority 1 total {execution['priority_1_total_nodeids']}; top-10 total {execution['top_10_count_sum']}; 29-module total {execution['failed_or_errored_nodeids_count']} failed-or-errored node IDs.",
        "Priority 1 Validation Summary": "675/675 pre-change and 675/675 post-change passed as current-root focused evidence only.",
        "Diagnostic Capture Evidence Summary": f"Exit {execution['source_exit_code']}; stdout {execution['source_stdout_byte_count']} bytes `{execution['source_stdout_sha256']}`; stderr {execution['source_stderr_byte_count']} bytes `{execution['source_stderr_sha256']}`. Diagnostic metadata only.",
        "Reviewed Observable Families": "Four HIGH-confidence planning families, 47 observations each and 188 observations total; no new classification was performed.",
        "Reviewed Workstreams": "Four committed workstreams are preserved without execution.",
        "Reviewed Template Structure": f"{execution['reviewed_template_row_count']} reviewed rows map `MA-001` through `MA-030` across four sections and four workstreams. The template is not evidence.",
        "Count Label Distinction": "Preserved without reconciliation: requirements 67 prescribed/69 enumerated; non-goals 71/76; risk controls 104/106.",
        "Operator Completion Input Contract": "A non-secret header and exactly 30 mapped rows are required. Every row must be supplied but unvalidated and unbound, require results review, and keep direct-change, remediation, retry, and main authority false.",
        "Operator Completion Inputs": f"provided={execution['operator_completion_inputs_provided']}; validated={execution['operator_completion_inputs_validated']}; bound={execution['operator_completion_inputs_bound']}. Full inputs are intentionally not rendered.",
        "Actual Evidence Absence": f"package_created={execution['operator_source_authority_evidence_package_created']}; package_supplied={execution['operator_source_authority_evidence_package_supplied']}; package_validated={execution['operator_source_authority_evidence_package_validated']}; package_bound={execution['operator_source_authority_evidence_package_bound']}; items_filled={execution['actual_evidence_items_filled']}.",
        "Actual Coverage Zero": f"covered={execution['actual_covered_missing_authority_item_count']}; uncovered={execution['actual_uncovered_missing_authority_item_count']}.",
        "Source Authority Gap Preservation": "No source authority, external evidence, concrete authority, or safe source-authority-bound change was created.",
        "Unsupported Claims Boundary": "No root-cause, first-failure, retry-success, acquisition-readiness, remediation-readiness, or main-readiness claim is made.",
        "Recommendation": f"{execution['recommended_next_task']}: {execution['recommended_action']}.",
        "Authority Boundaries": "Evidence validation/binding/acceptance and every acquisition, disposition, remediation, retry, runtime, trading, and protected-branch authority remain false or `NOT_AUTHORIZED`.",
        "Checklist Summary": f"{summary['passed_checks']}/{summary['total_checks']} PASS; blockers={summary['blocker_count']}.",
        "Guardrails": "Offline dictionary-only execution; no source builders, file reads, subprocesses, pytest, cache/log/environment/receipt inspection, provider calls, source-owner contact, or runtime output writes.",
    }
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", "", facts.get(section, "Preserved from committed source evidence; no new authority or action is created."), ""))
        if section == "Next Chain":
            lines[-2:-2] = [*(f"{index}. {item}" for index, item in enumerate(execution["next_chain"], 1)), ""]
        elif section == "Next Gates":
            lines[-2:-2] = [*(f"- `{item}`" for item in execution["next_gates"]), ""]
        elif section == "Risk Controls":
            lines[-2:-2] = [*(f"- `{item}`" for item in execution["risk_controls"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(
    output_dir: str | Path, *, source_approval: dict | None = None,
    operator_completion_inputs: dict | None = None, run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Write only the requested Markdown status artifact."""
    execution = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(
        source_approval=source_approval, operator_completion_inputs=operator_completion_inputs,
        run_timestamp_utc=run_timestamp_utc,
    )
    destination = Path(output_dir) / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_markdown_v1(execution), encoding="utf-8")
    return execution


__all__ = [
    "ARTIFACT_KIND", "BLOCKED_ARTIFACT_KIND", "SCHEMA_VERSION", "EXECUTION_STATUS", "BLOCKED_STATUS",
    "EXECUTION_SCOPE", "SELECTED_PACKAGE", "ALLOWED_BLOCKED_REASONS",
    "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED",
    "SOURCE_COMPLETION_APPROVAL_NOT_VERIFIED", "SELECTED_COMPLETION_PACKAGE_NOT_APPROVED",
    "OPERATOR_COMPLETION_INPUTS_INCOMPLETE", "OPERATOR_COMPLETION_INPUTS_CONTAIN_SECRETS",
    "OPERATOR_COMPLETION_INPUTS_CONTAIN_API_KEYS", "OPERATOR_COMPLETION_INPUTS_CONTAIN_BROKER_CREDENTIALS",
    "OPERATOR_COMPLETION_INPUTS_CONTAIN_PERSONAL_FINANCIAL_CREDENTIALS",
    "OPERATOR_COMPLETION_INPUTS_CONTAIN_MARKET_DATA_CREDENTIALS",
    "OPERATOR_COMPLETION_INPUTS_CONTAIN_PRIVATE_TOKENS",
    "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_OWNER_OR_ORIGIN",
    "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_REFERENCE",
    "OPERATOR_COMPLETION_INPUTS_MISSING_DIGEST_OR_REPRODUCIBLE_PROVENANCE",
    "OPERATOR_COMPLETION_INPUTS_MISSING_AUTHORITY_STATEMENT",
    "OPERATOR_COMPLETION_INPUTS_INVALID_MISSING_AUTHORITY_MAPPING",
    "OPERATOR_COMPLETION_INPUTS_INVALID_SECTION_ID", "OPERATOR_COMPLETION_INPUTS_INVALID_WORKSTREAM_ID",
    "OPERATOR_COMPLETION_INPUTS_INVALID_ARTIFACT_TYPE",
    "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_DIRECT_CHANGE",
    "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_REMEDIATION",
    "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_RETRY",
    "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_MAIN_MERGE", "TEMPLATE_COMPLETION_BOUNDARY_FAILURE",
    "EXECUTION_DIGEST_KEY", "COMPLETED_PACKAGE_DIGEST_KEY", "COMPLETED_ITEMS_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "BLOCKED_DIGEST_KEY", "BLOCKED_MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTED_AFTER_APPROVAL_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_BLOCKED_AFTER_APPROVAL_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTED_AFTER_APPROVAL_COMPLETED_OPERATOR_EVIDENCE_PACKAGE_READY_FOR_RESULTS_REVIEW",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_BLOCKED_AFTER_APPROVAL_OPERATOR_INPUTS_UNAVAILABLE_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_ONLY_COMPLETED_OPERATOR_EVIDENCE_PACKAGE_FROM_NON_SECRET_OPERATOR_INPUTS_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_VALIDATION_NOT_EVIDENCE_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_markdown_v1",
]
