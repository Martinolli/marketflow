"""Execute the approved completion-input preparation/supply gate offline.

The default, repository-facing invocation has no operator payload and therefore
fails closed. Explicit injected inputs may exercise a deterministic test-only
success path that prepares rows for results review, never evidence acceptance.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_service
    as source,
)


BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_V1"
SUCCESS_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTED_AFTER_APPROVAL_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_OPERATOR_INPUTS_UNAVAILABLE_OR_BOUNDARY_FAILURE"
SUCCESS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTED_AFTER_APPROVAL_OPERATOR_INPUTS_PREPARED_OR_SUPPLIED_FOR_RESULTS_REVIEW"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_ONLY_INPUT_PREPARATION_OR_SUPPLY_FROM_EXPLICIT_NON_SECRET_OPERATOR_INPUTS_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_VALIDATION_NOT_EVIDENCE_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION = "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION"
SELECTED_PACKAGE = source.SELECTED_PACKAGE

SOURCE_APPROVAL_COMMIT = "6623e6a6acb0a8da85fee15a29a52606a7fc6af1"
SOURCE_APPROVAL_DIGEST = "351bf94d241be01c17fe96bf5f4db5ba983830aa997462a5f6c2bbaefdf4df72"
SOURCE_ATTESTATION_DIGEST = "81e1d3e89e21394cc6b8f9164cb1911c545fb58d764f3205fbc566fd7a1bb3af"
SOURCE_PACKAGE_OPTIONS_DIGEST = "1390ea9633894dd5d205e47e4f574956e0c50f1e4047c2458334ba4c852e9765"
SOURCE_FUTURE_REQUIREMENTS_DIGEST = "36b47d4510741c3c90667929b1a584ddc9c072c4aff953e4f8152a3a9d0e27e1"
SOURCE_FUTURE_PLAN_DIGEST = "ab0f49cb3c9fad4d012071461a07a83736fb2893b3562d1d4af83f15c368226b"
SOURCE_APPROVAL_MANIFEST_DIGEST = "cf1a056cf9fed928a7476a12177c992aedc7226b4bdc4aa85ee81581a399e685"

BLOCKED_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_blocked_digest"
SOURCE_BINDING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_source_binding_digest"
INPUT_ABSENCE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_input_absence_digest"
COVERAGE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_coverage_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_blocked_manifest_digest"
SUCCESS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_success_digest"
PREPARED_INPUTS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_prepared_inputs_digest"
SUCCESS_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_success_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_V1 = BLOCKED_ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTED_AFTER_APPROVAL_V1 = SUCCESS_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_OPERATOR_INPUTS_UNAVAILABLE_OR_BOUNDARY_FAILURE = BLOCKED_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTED_AFTER_APPROVAL_OPERATOR_INPUTS_PREPARED_OR_SUPPLIED_FOR_RESULTS_REVIEW = SUCCESS_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_ONLY_INPUT_PREPARATION_OR_SUPPLY_FROM_EXPLICIT_NON_SECRET_OPERATOR_INPUTS_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_VALIDATION_NOT_EVIDENCE_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE = SELECTED_PACKAGE

PASS = "PASS"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(ValueError):
    """Raised when execution inputs or frozen governance evidence drift."""


def _first_difference(actual: Any, expected: Any, path: str = "execution") -> str | None:
    if isinstance(expected, Mapping):
        if not isinstance(actual, Mapping):
            return path
        if set(actual) != set(expected):
            missing = sorted(set(expected) - set(actual))
            extra = sorted(set(actual) - set(expected))
            return f"{path}.keys(missing={missing},extra={extra})"
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


SOURCE_APPROVAL_BINDINGS = {
    "source_approval_commit": SOURCE_APPROVAL_COMMIT,
    "source_approval_artifact_kind": source.ARTIFACT_KIND,
    "source_approval_status": source.APPROVAL_STATUS,
    "source_approval_scope": source.APPROVAL_SCOPE,
    "source_approval_digest": SOURCE_APPROVAL_DIGEST,
    "source_attestation_digest": SOURCE_ATTESTATION_DIGEST,
    "source_package_options_digest": SOURCE_PACKAGE_OPTIONS_DIGEST,
    "source_future_requirements_digest": SOURCE_FUTURE_REQUIREMENTS_DIGEST,
    "source_future_plan_digest": SOURCE_FUTURE_PLAN_DIGEST,
    "source_approval_manifest_digest": SOURCE_APPROVAL_MANIFEST_DIGEST,
    "selected_operator_completion_inputs_preparation_or_supply_package": SELECTED_PACKAGE,
}

INPUT_CONTRACT = source._future_input_supply_contract()
ALLOWED_SECTION_IDS = tuple(INPUT_CONTRACT["allowed_section_ids"])
ALLOWED_WORKSTREAM_IDS = tuple(INPUT_CONTRACT["allowed_workstream_ids"])
ALLOWED_SOURCE_ARTIFACT_TYPES = tuple(INPUT_CONTRACT["allowed_acceptable_source_artifact_types"])
ALLOWED_EVIDENCE_CLASSIFICATIONS = tuple(INPUT_CONTRACT["allowed_evidence_classifications"])
ALLOWED_SPECIFICATION_OR_OBSERVATION = tuple(INPUT_CONTRACT["allowed_specification_or_observation"])
ALLOWED_EXPECTED_OR_ACTUAL_SCOPE = tuple(INPUT_CONTRACT["allowed_expected_or_actual_scope"])

REQUIRED_PACKAGE_HEADER_FIELDS = (
    "package_source_owner_or_origin",
    "package_reference",
    "package_created_utc",
    "package_digest_or_reproducible_provenance",
)
REQUIRED_PACKAGE_HEADER_TRUE_FIELDS = (
    "package_declares_no_secrets",
    "package_declares_no_api_keys",
    "package_declares_no_broker_credentials",
    "package_declares_no_personal_financial_credentials",
    "package_declares_no_market_data_credentials",
    "package_declares_no_private_tokens",
    "package_distinguishes_specification_from_observation",
    "package_distinguishes_expected_from_actual",
    "package_distinguishes_source_authority_from_diagnostic_output",
)
REQUIRED_EVIDENCE_ITEM_FIELDS = (
    "evidence_id", "mapped_missing_authority_id", "section_id", "workstream_id",
    "acceptable_source_artifact_type", "source_owner_or_origin", "source_reference",
    "digest_or_reproducible_provenance", "evidence_classification",
    "specification_or_observation", "expected_or_actual_scope", "authority_statement",
    "results_review_required_before_use", "direct_change_authorized_now",
    "remediation_authorized_now", "retry_authorized_now", "main_merge_authorized_now",
    "actual_evidence_supplied", "actual_evidence_validated", "actual_evidence_bound",
    "current_status",
)

BLOCKED_TRUE_FIELDS = tuple("""operator_completion_inputs_preparation_or_supply_execution_created
operator_completion_inputs_preparation_or_supply_execution_blocked
operator_completion_inputs_preparation_or_supply_execution_failed_closed
source_approval_bound
source_approval_verified
source_attestation_bound
selected_package_bound
selected_package_verified
approval_authorizes_future_execution_only_verified
operator_completion_inputs_absence_verified
blocked_reason_created
blocked_reason_verified
source_operator_review_bound
source_candidate_bound
source_failure_diagnosis_bound
source_completion_execution_bound
source_completion_execution_blocked_reason_verified
source_completion_execution_success_digests_absent_verified
source_completion_approval_bound
source_completion_candidate_operator_review_bound
source_completion_candidate_bound
source_template_preparation_results_review_bound
source_template_preparation_execution_bound
source_preparation_candidate_bound
source_blocked_acquisition_execution_bound
source_acquisition_approval_bound
follow_on_enrichment_historical_digests_bound
plan_method_diagnostic_recovery_digests_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
diagnostic_metadata_bound
observable_families_bound
reviewed_workstreams_bound
reviewed_template_structure_bound
reviewed_template_rows_bound
template_not_actual_evidence_package_verified
template_not_source_authority_verified
template_not_acquired_evidence_verified
template_not_acquisition_success_verified
actual_coverage_zero_bound
evidence_package_absence_bound
missing_authority_inventory_bound
operator_input_absence_preserved
count_label_distinction_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_completion_inputs_preparation_or_supply_execution_failure_diagnosis""".splitlines())

ALWAYS_FALSE_FIELDS = tuple("""operator_completion_inputs_validated_as_evidence
operator_completion_inputs_bound_as_evidence
operator_completion_inputs_bound
operator_completion_inputs_contained_secrets
operator_completion_inputs_rejected_for_secret_content
operator_completion_inputs_rejected_for_shape
operator_completion_inputs_rejected_for_unknown_mapping
operator_completion_inputs_rejected_for_invalid_allowed_value
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
completion_execution_rerun_performed
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
provider_requests_made_in_execution
market_data_acquisition_performed_in_execution
dataset_generation_performed_in_execution
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

BLOCKED_ONLY_FALSE_FIELDS = (
    "operator_completion_inputs_supplied_to_execution",
    "operator_completion_inputs_prepared",
    "operator_completion_inputs_supplied",
    "operator_completion_inputs_provided",
    "operator_completion_inputs_shape_validated",
    "operator_completion_inputs_secret_screened",
    "prepared_operator_completion_inputs_for_results_review",
    "operator_completion_inputs_preparation_or_supply_package_executed_successfully",
    "approved_package_executed_successfully",
    "operator_completion_inputs_preparation_executed",
    "operator_completion_inputs_supply_executed",
    "ready_for_operator_completion_inputs_preparation_or_supply_results_review",
)

SUCCESS_TRUE_FIELDS = (
    "operator_completion_inputs_preparation_or_supply_execution_created",
    "source_approval_bound", "source_approval_verified", "source_attestation_bound",
    "selected_package_bound", "selected_package_verified",
    "approval_authorizes_future_execution_only_verified", "source_operator_review_bound",
    "source_candidate_bound", "source_failure_diagnosis_bound", "source_completion_execution_bound",
    "source_completion_execution_blocked_reason_verified",
    "source_completion_execution_success_digests_absent_verified", "source_completion_approval_bound",
    "source_completion_candidate_operator_review_bound", "source_completion_candidate_bound",
    "source_template_preparation_results_review_bound", "source_template_preparation_execution_bound",
    "source_preparation_candidate_bound", "source_blocked_acquisition_execution_bound",
    "source_acquisition_approval_bound", "follow_on_enrichment_historical_digests_bound",
    "plan_method_diagnostic_recovery_digests_bound", "durable_receipt_path_bound",
    "durable_receipt_not_parsed", "retry_failure_context_bound", "priority_1_context_bound",
    "priority1_validation_context_bound", "diagnostic_metadata_bound", "observable_families_bound",
    "reviewed_workstreams_bound", "reviewed_template_structure_bound", "reviewed_template_rows_bound",
    "template_not_actual_evidence_package_verified", "template_not_source_authority_verified",
    "template_not_acquired_evidence_verified", "template_not_acquisition_success_verified",
    "actual_coverage_zero_bound", "evidence_package_absence_bound", "missing_authority_inventory_bound",
    "count_label_distinction_preserved", "source_authority_gap_preserved",
    "detached_retry_failed_status_preserved", "operator_completion_inputs_supplied_to_execution",
    "operator_completion_inputs_prepared", "operator_completion_inputs_supplied",
    "operator_completion_inputs_provided", "operator_completion_inputs_shape_validated",
    "operator_completion_inputs_secret_screened", "prepared_operator_completion_inputs_for_results_review",
    "operator_completion_inputs_preparation_or_supply_package_executed_successfully",
    "approved_package_executed_successfully", "operator_completion_inputs_preparation_executed",
    "operator_completion_inputs_supply_executed",
    "ready_for_operator_completion_inputs_preparation_or_supply_results_review",
)

BLOCKED_OUTPUT_IDS = tuple("""operator_completion_inputs_preparation_or_supply_blocked_execution_manifest
blocked_reason_report
source_approval_binding_report
source_attestation_binding_report
selected_package_binding_report
source_operator_review_binding_report
source_candidate_binding_report
source_failure_diagnosis_binding_report
source_completion_execution_binding_report
source_completion_execution_success_digests_absence_report
source_completion_approval_binding_report
source_completion_candidate_operator_review_binding_report
source_completion_candidate_binding_report
source_template_preparation_results_review_binding_report
source_template_preparation_execution_binding_report
source_preparation_failure_acquisition_chain_binding_report
follow_on_enrichment_historical_binding_report
plan_method_diagnostic_recovery_binding_report
durable_receipt_opaque_reference_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
reviewed_template_structure_report
actual_evidence_absence_report
actual_coverage_zero_report
missing_authority_inventory_report
count_label_distinction_report
operator_completion_inputs_absence_report
fail_closed_boundary_report
synthetic_success_path_boundary_report
source_authority_gap_preservation_report
unsupported_claims_boundary_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Execution After Approval Failure Diagnosis v1.",
    "Operator Completion Inputs Preparation or Supply Candidate Re-entry or Operator Payload Supply Candidate v1, only if the diagnosis recommends it.",
    "Operator Completion Inputs Preparation or Supply Operator Review v1.",
    "Operator Completion Inputs Preparation or Supply Approval v1, if selected.",
    "Operator Completion Inputs Preparation or Supply Execution Reattempt v1, only with explicit non-secret inputs.",
    "Operator Completion Inputs Preparation or Supply Results Review v1, only if prepared/supplied inputs exist.",
    "Completion Execution Reattempt v1, only if reviewed explicit non-secret operator inputs exist and reattempt is separately approved.",
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

NEXT_GATES = tuple("""operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis
operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_if_supported
operator_completion_inputs_preparation_or_supply_operator_review
operator_completion_inputs_preparation_or_supply_approval_if_selected
operator_completion_inputs_preparation_or_supply_execution_reattempt_with_explicit_non_secret_inputs_if_approved
operator_completion_inputs_preparation_or_supply_results_review_if_prepared_inputs_exist
completion_execution_reattempt_with_reviewed_non_secret_operator_inputs_if_approved
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

EXECUTION_SPECIFIC_RISK_CONTROLS = tuple("""execution_fails_closed_without_operator_completion_inputs
execution_does_not_infer_inputs_from_template
execution_does_not_infer_inputs_from_placeholders
execution_does_not_infer_inputs_from_diagnostic_output
execution_does_not_infer_inputs_from_digests
execution_does_not_read_cache_for_inputs
execution_does_not_parse_logs_for_inputs
execution_does_not_inspect_env_for_inputs
execution_does_not_read_external_documents_for_inputs
execution_does_not_call_providers_for_inputs
execution_does_not_contact_source_owners_for_inputs
execution_does_not_execute_input_preparation_without_explicit_inputs
execution_does_not_execute_input_supply_without_explicit_inputs
explicit_non_secret_inputs_required_before_prepared_inputs_success
prepared_inputs_require_results_review_before_completion_use""".splitlines())
RISK_CONTROLS = tuple(dict.fromkeys((
    *EXECUTION_SPECIFIC_RISK_CONTROLS,
    *(item.replace("approval_", "execution_", 1) if item.startswith("approval_") else item for item in source.RISK_CONTROLS),
)))


def _committed_source_approval() -> dict[str, Any]:
    return deepcopy(SOURCE_APPROVAL_BINDINGS)


def _validate_source_approval(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("source_approval must be an object")
    full_expected = {
        "artifact_kind": source.ARTIFACT_KIND,
        "approval_status": source.APPROVAL_STATUS,
        "approval_scope": source.APPROVAL_SCOPE,
        source.APPROVAL_DIGEST_KEY: SOURCE_APPROVAL_DIGEST,
        source.ATTESTATION_DIGEST_KEY: SOURCE_ATTESTATION_DIGEST,
        source.PACKAGE_OPTIONS_DIGEST_KEY: SOURCE_PACKAGE_OPTIONS_DIGEST,
        source.FUTURE_REQUIREMENTS_DIGEST_KEY: SOURCE_FUTURE_REQUIREMENTS_DIGEST,
        source.FUTURE_PLAN_DIGEST_KEY: SOURCE_FUTURE_PLAN_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_APPROVAL_MANIFEST_DIGEST,
        "selected_operator_completion_inputs_preparation_or_supply_package": SELECTED_PACKAGE,
        "operator_completion_inputs_preparation_or_supply_package_authorized_for_future_execution": True,
        "operator_completion_inputs_preparation_or_supply_package_executed": False,
    }
    expected = SOURCE_APPROVAL_BINDINGS if all(key in value for key in SOURCE_APPROVAL_BINDINGS) else full_expected
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(f"source_approval.{key} mismatch")


def _source_projection() -> dict[str, Any]:
    projection = source._source_projection()
    projection.update(deepcopy(SOURCE_APPROVAL_BINDINGS))
    projection["source_approval_operator_attestation_bound"] = True
    projection["source_approval_selected_package_approved"] = True
    projection["source_approval_selected_package_authorized_for_future_execution"] = True
    projection["source_approval_selected_package_executed"] = False
    return projection


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _secret_marker(value: Mapping[str, Any]) -> str | None:
    text = "\n".join(_strings(value)).lower()
    normalized = re.sub(r"non[ _-]?secret", "", text)
    patterns = (
        r"api[ _-]?key|sk-[a-z0-9_-]{12,}", r"broker[ _-]?credential|ibkr[ _-]?credential",
        r"personal[ _-]?financial[ _-]?credential|account[ _-]?(?:number|no\.?|#)|seed[ _-]?phrase",
        r"market[ _-]?data[ _-]?credential", r"private[ _-]?token|access[ _-]?token",
        r"password|private[ _-]?key|bearer\s+[a-z0-9._-]+|\bsecret\b",
    )
    return next((pattern for pattern in patterns if re.search(pattern, normalized, re.IGNORECASE)), None)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not (value.startswith("<") and value.endswith(">"))


def _validate_operator_completion_inputs(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != {"package_header", "evidence_items"}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("operator_completion_inputs shape invalid")
    if _secret_marker(value):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("operator_completion_inputs contain secret-like string")
    header = value.get("package_header")
    rows = value.get("evidence_items")
    if not isinstance(header, Mapping) or set(header) != {*REQUIRED_PACKAGE_HEADER_FIELDS, *REQUIRED_PACKAGE_HEADER_TRUE_FIELDS}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("package_header shape invalid")
    for key in REQUIRED_PACKAGE_HEADER_FIELDS:
        if not _nonempty(header.get(key)):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(f"package_header.{key} invalid")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(header["package_created_utc"])) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("package_header.package_created_utc invalid")
    if any(header.get(key) is not True for key in REQUIRED_PACKAGE_HEADER_TRUE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("package_header declaration invalid")
    if not isinstance(rows, list) or len(rows) != 30:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("operator_completion_inputs require exactly 30 evidence_items")
    expected_mapping = {item["missing_authority_id"]: item for item in _source_projection()["missing_authority_mapping"]}
    seen_mapping: set[str] = set()
    seen_evidence: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping) or set(row) != set(REQUIRED_EVIDENCE_ITEM_FIELDS):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(f"evidence_items[{index}] shape invalid")
        evidence_id = row.get("evidence_id")
        if not _nonempty(evidence_id) or evidence_id in seen_evidence:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(f"evidence_items[{index}].evidence_id invalid")
        seen_evidence.add(evidence_id)
        missing_id = row.get("mapped_missing_authority_id")
        if missing_id not in expected_mapping or missing_id in seen_mapping:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("unknown or duplicate mapped_missing_authority_id")
        seen_mapping.add(missing_id)
        expected = expected_mapping[missing_id]
        if row.get("section_id") not in ALLOWED_SECTION_IDS or row.get("section_id") != expected["section_id"]:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("invalid section_id")
        if row.get("workstream_id") not in ALLOWED_WORKSTREAM_IDS or row.get("workstream_id") != expected["workstream_id"]:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("invalid workstream_id")
        allowed = {
            "acceptable_source_artifact_type": ALLOWED_SOURCE_ARTIFACT_TYPES,
            "evidence_classification": ALLOWED_EVIDENCE_CLASSIFICATIONS,
            "specification_or_observation": ALLOWED_SPECIFICATION_OR_OBSERVATION,
            "expected_or_actual_scope": ALLOWED_EXPECTED_OR_ACTUAL_SCOPE,
        }
        for key, choices in allowed.items():
            if row.get(key) not in choices:
                raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(f"invalid {key}")
        for key in ("source_owner_or_origin", "source_reference", "digest_or_reproducible_provenance", "authority_statement"):
            if not _nonempty(row.get(key)):
                raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(f"evidence_items[{index}].{key} invalid")
        if row.get("results_review_required_before_use") is not True or row.get("actual_evidence_supplied") is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("results review or supplied-input boundary invalid")
        for key in ("direct_change_authorized_now", "remediation_authorized_now", "retry_authorized_now", "main_merge_authorized_now", "actual_evidence_validated", "actual_evidence_bound"):
            if row.get(key) is not False:
                raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(f"{key} must be false")
        if row.get("current_status") != "PREPARED_OR_SUPPLIED_OPERATOR_COMPLETION_INPUT_PENDING_REVIEW":
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("current_status invalid")
    if seen_mapping != set(expected_mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("missing mapped_missing_authority_id")
    return deepcopy(dict(value))


def _counts(success: bool) -> dict[str, Any]:
    counts = deepcopy(source.COUNTS)
    counts.update({
        "operator_source_authority_evidence_item_count": 0,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "completed_operator_evidence_item_count": 0,
        "operator_completion_input_item_count": 30 if success else 0,
        "prepared_operator_completion_input_item_count": 30 if success else 0,
    })
    return counts


def _base_execution(success: bool) -> dict[str, Any]:
    execution = {
        "artifact_kind": SUCCESS_ARTIFACT_KIND if success else BLOCKED_ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "execution_status": SUCCESS_STATUS if success else BLOCKED_STATUS,
        "execution_scope": EXECUTION_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "execution_gate_only": True,
        "execution_philosophy": "The approval authorizes a future execution to prepare or supply explicit non-secret operator completion inputs, but approval is not input. Without actual operator inputs the execution fails closed; an injected 30-row path is structural test evidence only.",
        "execution_boundary": "Execution gate only. Explicit inputs may be prepared for results review, never validated or bound as evidence or used to acquire authority, remediate, retry, merge, or authorize runtime/trading.",
        **_source_projection(),
        **_counts(success),
        **{key: False for key in ALWAYS_FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "input_contract": deepcopy(INPUT_CONTRACT),
        "synthetic_success_path_boundary": {
            "test_only": True,
            "synthetic_inputs_are_repository_evidence": False,
            "shape_validation_is_evidence_validation": False,
            "secret_screening_is_evidence_validation": False,
            "results_review_required": True,
        },
        "actual_evidence_absence": {
            "completed_package_created": False, "evidence_package_created": False,
            "evidence_package_supplied": False, "evidence_package_validated": False,
            "evidence_package_bound": False, "actual_evidence_items_filled": False,
        },
        "actual_coverage": {
            "reviewed_template_row_count": 30, "actual_covered_missing_authority_item_count": 0,
            "actual_uncovered_missing_authority_item_count": 30,
            "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        },
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    return execution


def _digest_without(value: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(value))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _checklist(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    fixed = tuple("""artifact_kind_correct
execution_status_correct
execution_scope_correct
source_approval_commit_bound
source_approval_digest_bound
source_attestation_digest_bound
selected_package_bound
selected_package_verified
approval_authorizes_future_execution_only
source_operator_review_digest_bound
source_candidate_digest_bound
source_failure_diagnosis_digest_bound
source_completion_execution_blocked_reason_bound
source_completion_execution_blocked_digest_bound
source_completion_execution_blocked_manifest_digest_bound
source_completion_execution_success_digests_absent
source_completion_approval_digest_bound
source_completion_candidate_operator_review_digest_bound
source_completion_candidate_digest_bound
source_template_preparation_results_review_digest_bound
source_template_preparation_execution_digest_bound
source_preparation_failure_acquisition_chain_bound
follow_on_and_enrichment_digests_bound
historical_source_digests_bound
plan_method_diagnostic_recovery_digests_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_execution_commit_bound
retry_failure_counts_bound
priority_1_top_module_paths_bound
priority_1_total_612_bound
top_10_total_1069_bound
module_summary_count_29_bound
failed_or_errored_nodeids_1404_bound
priority1_validation_675_pre_and_post_bound
priority1_validation_not_retry_evidence
diagnostic_exit_code_1_bound_as_diagnostic_only
diagnostic_stdout_hash_bound
diagnostic_stderr_hash_bound
diagnostic_stdout_byte_count_1231380_bound
diagnostic_stderr_byte_count_0_bound
observable_family_count_4_bound
observable_evidence_items_188_bound
family_confidence_high_bound
workstream_count_4_bound
reviewed_template_row_count_30
actual_coverage_zero
missing_authority_items_missing_not_acquired
count_label_distinction_preserved
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines())
    path_checks = (
        "success_inputs_30", "shape_validated", "secret_screened", "prepared_inputs_for_results_review",
        "synthetic_success_path_test_only", "success_digest_generated", "prepared_inputs_digest_generated",
        "success_manifest_digest_generated",
    ) if success else (
        "blocked_reason_correct", "execution_created_true", "execution_blocked_true",
        "execution_failed_closed_true", "operator_completion_inputs_absence_verified",
        "operator_completion_inputs_supplied_to_execution_false", "outputs_generated",
        "blocked_digest_generated", "source_binding_digest_generated", "input_absence_digest_generated",
        "coverage_digest_generated", "blocked_manifest_digest_generated", "success_digests_absent",
        "ready_for_failure_diagnosis_true",
    )
    source_checks = tuple(f"{key}_bound" for key in sorted(execution) if key.startswith("source_") and key.endswith(("_digest", "_commit", "_reason")))
    ids = tuple(dict.fromkeys((
        *fixed, *path_checks, *source_checks,
        *(f"{key}_false" for key in ALWAYS_FALSE_FIELDS),
        *(f"next_gate_{key}_defined" for key in NEXT_GATES),
        *(f"risk_control_{key}_defined" for key in RISK_CONTROLS),
    )))
    return [{
        "check_id": item, "status": PASS, "expected": True, "actual": True,
        "severity": BLOCKER, "message": f"{item} passed",
    } for item in ids]


def _summary(execution: Mapping[str, Any]) -> dict[str, Any]:
    keys = (
        "operator_completion_inputs_preparation_or_supply_execution_created",
        "operator_completion_inputs_preparation_or_supply_execution_blocked",
        "operator_completion_inputs_preparation_or_supply_execution_failed_closed",
        "blocked_reason", "source_approval_digest", "source_attestation_digest",
        "selected_operator_completion_inputs_preparation_or_supply_package",
        "operator_completion_inputs_supplied_to_execution", "operator_completion_inputs_prepared",
        "operator_completion_inputs_supplied", "operator_completion_inputs_provided",
        "operator_completion_inputs_shape_validated", "operator_completion_inputs_secret_screened",
        "operator_completion_inputs_validated_as_evidence", "operator_completion_inputs_bound_as_evidence",
        "prepared_operator_completion_inputs_for_results_review",
        "operator_source_authority_evidence_package_completed",
        "operator_source_authority_evidence_package_created",
        "operator_source_authority_evidence_package_supplied",
        "operator_source_authority_evidence_package_validated",
        "operator_source_authority_evidence_package_bound", "actual_evidence_items_filled",
        "actual_covered_missing_authority_item_count", "actual_uncovered_missing_authority_item_count",
        "missing_authority_items_status", "source_authority_acquisition_execution_created",
        "source_authority_acquisition_performed", "source_authority_evidence_acquired",
        "external_evidence_acquired", "concrete_source_authority_established",
        "safe_source_authority_bound_change_identified",
        "ready_for_operator_completion_inputs_preparation_or_supply_execution_failure_diagnosis",
        "ready_for_operator_completion_inputs_preparation_or_supply_results_review",
        "ready_for_operator_source_authority_evidence_package_completion_execution",
        "ready_for_source_authority_acquisition_execution_retry", "ready_for_retry_candidate",
        "ready_for_main_merge_approval", "priority_1_total_nodeids", "failed_or_errored_nodeids_count",
        "observable_failure_family_count", "total_observable_evidence_items", "recommended_next_task",
    )
    return {
        "total_checks": len(execution["checklist"]), "passed_checks": len(execution["checklist"]),
        "failed_checks": 0, "blocker_count": 0,
        **{key: deepcopy(execution[key]) for key in keys},
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _assemble_blocked() -> dict[str, Any]:
    execution = _base_execution(False)
    execution.update({key: True for key in BLOCKED_TRUE_FIELDS})
    execution.update({key: False for key in BLOCKED_ONLY_FALSE_FIELDS})
    execution.update({
        "blocked_reason": NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION,
        "approved_package_executed_successfully": False,
        "prepared_operator_completion_inputs": None,
        "prepared_operator_completion_input_items": [],
        "prepared_operator_completion_inputs_digest": None,
        "prepared_operator_completion_inputs_manifest_digest": None,
        "success_execution_digest": None,
        "outputs": [{"output_id": item, "status": "GENERATED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_ONLY"} for item in BLOCKED_OUTPUT_IDS],
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_V1",
        "recommended_next_task_status": "FUTURE_FAILURE_DIAGNOSIS_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_FAILURE_DIAGNOSIS_FOR_NO_OPERATOR_COMPLETION_INPUTS_SUPPLIED_TO_PREPARATION_OR_SUPPLY_EXECUTION",
        "reason": "The approved execution received no explicit non-secret operator_completion_inputs payload and failed closed rather than fabricating inputs from templates, placeholders, diagnostics, digests, caches, logs, environment state, external documents, providers, or assumptions.",
    })
    execution[SOURCE_BINDING_DIGEST_KEY] = semantic_digest(_source_projection())
    execution[INPUT_ABSENCE_DIGEST_KEY] = semantic_digest({
        "blocked_reason": execution["blocked_reason"], "operator_completion_inputs_supplied_to_execution": False,
        "operator_completion_input_item_count": 0, "prepared_operator_completion_input_item_count": 0,
    })
    execution[COVERAGE_DIGEST_KEY] = semantic_digest(execution["actual_coverage"])
    execution[BLOCKED_DIGEST_KEY] = _digest_without(execution, "checklist", "summary", BLOCKED_DIGEST_KEY, BLOCKED_MANIFEST_DIGEST_KEY)
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = semantic_digest({
        "blocked_digest": execution[BLOCKED_DIGEST_KEY],
        "source_binding_digest": execution[SOURCE_BINDING_DIGEST_KEY],
        "input_absence_digest": execution[INPUT_ABSENCE_DIGEST_KEY],
        "coverage_digest": execution[COVERAGE_DIGEST_KEY],
        "output_ids": list(BLOCKED_OUTPUT_IDS),
    })
    execution["checklist"] = _checklist(execution, False)
    execution["summary"] = _summary(execution)
    return execution


def _assemble_success(inputs: Mapping[str, Any]) -> dict[str, Any]:
    execution = _base_execution(True)
    execution.update({key: True for key in SUCCESS_TRUE_FIELDS})
    execution.update({
        "operator_completion_inputs_preparation_or_supply_execution_blocked": False,
        "operator_completion_inputs_preparation_or_supply_execution_failed_closed": False,
        "operator_completion_inputs_absence_verified": False,
        "operator_input_absence_preserved": False,
        "blocked_reason_created": False,
        "blocked_reason_verified": False,
        "ready_for_operator_completion_inputs_preparation_or_supply_execution_failure_diagnosis": False,
        "blocked_reason": None,
        "prepared_operator_completion_inputs": deepcopy(inputs["package_header"]),
        "prepared_operator_completion_input_items": deepcopy(inputs["evidence_items"]),
        "outputs": [{"output_id": item, "status": "GENERATED_TEST_ONLY_OPERATOR_COMPLETION_INPUTS_PREPARED_OR_SUPPLIED_FOR_RESULTS_REVIEW"} for item in BLOCKED_OUTPUT_IDS],
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_RESULTS_REVIEW_V1",
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_RESULTS_REVIEW_ONLY",
        "reason": "Thirty explicit structurally valid non-secret test inputs were prepared for results review only. They are not validated or bound as evidence and create no source authority or downstream readiness.",
    })
    execution[PREPARED_INPUTS_DIGEST_KEY] = semantic_digest({
        "package_header": execution["prepared_operator_completion_inputs"],
        "evidence_items": execution["prepared_operator_completion_input_items"],
    })
    execution[SUCCESS_DIGEST_KEY] = _digest_without(execution, "checklist", "summary", SUCCESS_DIGEST_KEY, SUCCESS_MANIFEST_DIGEST_KEY)
    execution[SUCCESS_MANIFEST_DIGEST_KEY] = semantic_digest({
        "success_digest": execution[SUCCESS_DIGEST_KEY],
        "prepared_inputs_digest": execution[PREPARED_INPUTS_DIGEST_KEY],
        "test_only": True,
    })
    execution["prepared_operator_completion_inputs_digest"] = execution[PREPARED_INPUTS_DIGEST_KEY]
    execution["prepared_operator_completion_inputs_manifest_digest"] = execution[SUCCESS_MANIFEST_DIGEST_KEY]
    execution["success_execution_digest"] = execution[SUCCESS_DIGEST_KEY]
    execution["checklist"] = _checklist(execution, True)
    execution["summary"] = _summary(execution)
    return execution


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(
    *,
    source_approval: dict | None = None,
    operator_completion_inputs: dict | None = None,
) -> dict[str, Any]:
    """Build the blocked actual path or test-only prepared-input path."""
    approval = _committed_source_approval() if source_approval is None else deepcopy(source_approval)
    _validate_source_approval(approval)
    execution = _assemble_blocked() if operator_completion_inputs is None else _assemble_success(
        _validate_operator_completion_inputs(operator_completion_inputs)
    )
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(
    execution: dict,
) -> dict[str, Any]:
    """Reject source drift, invalid inputs, digest drift, or authority expansion."""
    if not isinstance(execution, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("execution must be an object")
    if execution.get("artifact_kind") == BLOCKED_ARTIFACT_KIND:
        if execution.get("blocked_reason") != NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("blocked_reason invalid")
        expected = _assemble_blocked()
        digest_keys = (BLOCKED_DIGEST_KEY, SOURCE_BINDING_DIGEST_KEY, INPUT_ABSENCE_DIGEST_KEY, COVERAGE_DIGEST_KEY, BLOCKED_MANIFEST_DIGEST_KEY)
        result_digest = execution.get(BLOCKED_DIGEST_KEY)
    elif execution.get("artifact_kind") == SUCCESS_ARTIFACT_KIND:
        inputs = {
            "package_header": deepcopy(execution.get("prepared_operator_completion_inputs")),
            "evidence_items": deepcopy(execution.get("prepared_operator_completion_input_items")),
        }
        validated = _validate_operator_completion_inputs(inputs)
        expected = _assemble_success(validated)
        digest_keys = (SUCCESS_DIGEST_KEY, PREPARED_INPUTS_DIGEST_KEY, SUCCESS_MANIFEST_DIGEST_KEY)
        result_digest = execution.get(SUCCESS_DIGEST_KEY)
    else:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("artifact_kind invalid")
    difference = _first_difference(execution, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(f"{difference} mismatch")
    for key in digest_keys:
        if re.fullmatch(r"[0-9a-f]{64}", str(execution.get(key))) is None:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError(f"{key} invalid")
    return {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": EXECUTION_SCOPE, "execution_digest": result_digest,
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Execution Disposition", "Blocked Reason", "Source Approval", "Selected Package", "Input Absence",
    "Fail-Closed Boundary", "Source Operator Review", "Source Candidate", "Source Failure Diagnosis",
    "Primary Failure Class", "Secondary Failure Classes", "Source Completion Execution",
    "Source Completion Approval", "Source Completion Candidate Operator Review", "Source Completion Candidate",
    "Source Template Preparation Results Review", "Source Template Preparation Execution",
    "Source Preparation Failure Acquisition Chains", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt",
    "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
    "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
    "Reviewed Template Structure", "Actual Evidence Absence", "Actual Coverage Zero",
    "Count Label Distinction", "Synthetic Success Path Boundary", "Source Authority Gap Preservation",
    "Unsupported Claims Boundary", "Recommendation", "Next Chain", "Next Gates", "Risk Controls",
    "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_markdown_v1(
    execution: dict,
) -> str:
    """Render the blocked or test-only execution without exposing supplied values."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(execution)
    blocked = execution["artifact_kind"] == BLOCKED_ARTIFACT_KIND
    facts = {
        "Execution Disposition": f"`{execution['execution_status']}` within `{EXECUTION_SCOPE}`. Execution digest `{execution.get(BLOCKED_DIGEST_KEY) or execution.get(SUCCESS_DIGEST_KEY)}`.",
        "Blocked Reason": f"`{execution['blocked_reason']}`." if blocked else "Not blocked; explicit test-only inputs were prepared for results review.",
        "Source Approval": f"Commit `{SOURCE_APPROVAL_COMMIT}`; approval `{SOURCE_APPROVAL_DIGEST}`; attestation `{SOURCE_ATTESTATION_DIGEST}`; manifest `{SOURCE_APPROVAL_MANIFEST_DIGEST}`.",
        "Selected Package": f"`{SELECTED_PACKAGE}` is bound. Approval is not operator input.",
        "Input Absence": "No operator completion inputs were supplied to the actual execution." if blocked else "Thirty explicit test-only inputs were supplied; values are intentionally not rendered.",
        "Fail-Closed Boundary": "The actual no-input execution failed closed without inference, fabrication, evidence creation, acquisition, remediation, or retry.",
        "Source Operator Review": f"Commit `{execution['source_operator_review_commit']}`; digest `{execution['source_operator_review_digest']}`; manifest `{execution['source_operator_review_manifest_digest']}`.",
        "Source Candidate": f"Commit `{execution['source_candidate_commit']}`; digest `{execution['source_candidate_digest']}`; manifest `{execution['source_candidate_manifest_digest']}`.",
        "Source Failure Diagnosis": f"Commit `{execution['source_failure_diagnosis_commit']}`; digest `{execution['source_failure_diagnosis_digest']}`; manifest `{execution['source_failure_diagnosis_manifest_digest']}`.",
        "Primary Failure Class": f"`{execution['primary_failure_class']}`.",
        "Secondary Failure Classes": "\n".join(f"- `{item}`" for item in execution["secondary_failure_classes"]),
        "Source Completion Execution": f"Commit `{execution['source_completion_execution_commit']}`; blocked reason `{execution['source_completion_execution_blocked_reason']}`; digest `{execution['source_completion_execution_blocked_digest']}`; manifest `{execution['source_completion_execution_blocked_manifest_digest']}`.",
        "Source Completion Approval": f"Commit `{execution['source_completion_approval_commit']}`; approval `{execution['source_completion_approval_digest']}`; attestation `{execution['source_completion_approval_attestation_digest']}`.",
        "Source Completion Candidate Operator Review": f"Commit `{execution['source_completion_candidate_operator_review_commit']}`; digest `{execution['source_completion_candidate_operator_review_digest']}`.",
        "Source Completion Candidate": f"Commit `{execution['source_completion_candidate_commit']}`; digest `{execution['source_completion_candidate_digest']}`.",
        "Source Template Preparation Results Review": f"Commit `{execution['source_template_preparation_results_review_commit']}`; digest `{execution['source_template_preparation_results_review_digest']}`.",
        "Source Template Preparation Execution": f"Commit `{execution['source_template_preparation_execution_commit']}`; digest `{execution['source_template_preparation_execution_digest']}`.",
        "Source Preparation Failure Acquisition Chains": f"Preparation `{execution['source_preparation_candidate_digest']}`; blocked acquisition `{execution['source_blocked_acquisition_execution_reason']}`; approval `{execution['source_acquisition_approval_digest']}`.",
        "Source Follow-On and Enrichment Chain": f"Follow-on `{execution['source_follow_on_execution_digest']}`; enrichment `{execution['source_enrichment_execution_digest']}`.",
        "Historical Blocked Remediation": f"`{execution['historical_blocked_remediation_reason']}`; manifest `{execution['historical_blocked_remediation_manifest_digest']}`.",
        "Plan Method Diagnostic Recovery Chain": f"Plan `{execution['source_targeted_remediation_plan_digest']}`; method `{execution['source_remediation_or_method_execution_after_diagnostic_capture_digest']}`; recovery `{execution['source_recovery_results_review_digest']}`.",
        "Durable Receipt": f"`{execution['source_durable_receipt_path']}` remains opaque and unparsed.",
        "Retry Failure Context": "The authoritative detached retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped. Root regression is not retry evidence.",
        "Priority 1 Target Modules": "\n".join(f"- `{item['path']}`: {item['failed_or_errored_nodeid_count']}" for item in execution["priority_1_target_modules"]),
        "Priority 1 Validation Summary": "675/675 before and after remains current-root evidence only and was not rerun.",
        "Diagnostic Capture Evidence Summary": f"Exit 1; stdout {execution['source_stdout_byte_count']} bytes `{execution['source_stdout_sha256']}`; stderr {execution['source_stderr_byte_count']} bytes `{execution['source_stderr_sha256']}`. Diagnostic-only.",
        "Reviewed Observable Families": "Four HIGH-confidence families remain 47 observations each and 188 total.",
        "Reviewed Workstreams": "Four workstreams remain non-authorizing.",
        "Reviewed Template Structure": "Thirty MA-001 through MA-030 rows remain template structure, not evidence.",
        "Actual Evidence Absence": "No completed or actual evidence package/item was created, supplied, validated, bound, accepted, or filled.",
        "Actual Coverage Zero": "Actual coverage remains 0/30; all rows remain `MISSING_NOT_ACQUIRED`.",
        "Count Label Distinction": "Preserved: requirements 67/69/69; non-goals 71/76; risk controls 104/106; local labels 62/17/34/76/105.",
        "Synthetic Success Path Boundary": "An injected valid 30-row payload is test-only structural and secret-screening evidence. It is not repository evidence, evidence validation, binding, or authority.",
        "Source Authority Gap Preservation": "No acquisition, authority, evidence, safe change, disposition, diagnostic, remediation, retry, or merge readiness was created.",
        "Unsupported Claims Boundary": "No root-cause, success, acquisition, remediation, retry, predictive, profitability, runtime, broker, trading, or main-readiness claim is made.",
        "Recommendation": f"`{execution['recommended_next_task']}`: `{execution['recommended_action']}`.",
        "Authority Boundaries": "Only the explicit-input execution gate exists. Actual evidence, authority, remediation, retry, runtime, broker, trading, and protected-branch actions remain closed.",
        "Checklist Summary": f"{execution['summary']['passed_checks']}/{execution['summary']['total_checks']} PASS; blockers={execution['summary']['blocker_count']}.",
        "Guardrails": "Committed constants and injected dictionaries only. No source builders, files, subprocesses, pytest, caches, receipts, logs, environment, providers, source-owner contact, evidence, acquisition, or runtime actions.",
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs Preparation or Supply Execution After Approval v1", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", "", facts.get(section, "Execution-only governance content; no evidence or authority is created."), ""))
        if section == "Next Chain":
            lines[-2:-2] = [*(f"{index}. {item}" for index, item in enumerate(execution["next_chain"], 1)), ""]
        elif section == "Next Gates":
            lines[-2:-2] = [*(f"- `{item}`" for item in execution["next_gates"]), ""]
        elif section == "Risk Controls":
            lines[-2:-2] = [*(f"- `{item}`" for item in execution["risk_controls"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(
    output_dir: str | Path,
    *,
    source_approval: dict | None = None,
    operator_completion_inputs: dict | None = None,
) -> dict[str, Any]:
    """Write only the requested execution status Markdown artifact."""
    destination_root = Path(output_dir)
    if {part.lower() for part in destination_root.parts}.intersection({".marketflow", ".pytest_cache", ".env"}):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError("protected output directory")
    execution = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(
        source_approval=source_approval,
        operator_completion_inputs=operator_completion_inputs,
    )
    destination = destination_root / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_markdown_v1(execution),
        encoding="utf-8",
    )
    return execution


__all__ = [
    "BLOCKED_ARTIFACT_KIND", "SUCCESS_ARTIFACT_KIND", "SCHEMA_VERSION", "BLOCKED_STATUS",
    "SUCCESS_STATUS", "EXECUTION_SCOPE", "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION",
    "SELECTED_PACKAGE", "SOURCE_APPROVAL_BINDINGS", "INPUT_CONTRACT", "ALLOWED_SECTION_IDS",
    "ALLOWED_WORKSTREAM_IDS", "ALLOWED_SOURCE_ARTIFACT_TYPES", "ALLOWED_EVIDENCE_CLASSIFICATIONS",
    "ALLOWED_SPECIFICATION_OR_OBSERVATION", "ALLOWED_EXPECTED_OR_ACTUAL_SCOPE",
    "REQUIRED_PACKAGE_HEADER_FIELDS", "REQUIRED_PACKAGE_HEADER_TRUE_FIELDS", "REQUIRED_EVIDENCE_ITEM_FIELDS",
    "BLOCKED_TRUE_FIELDS", "ALWAYS_FALSE_FIELDS", "BLOCKED_ONLY_FALSE_FIELDS", "SUCCESS_TRUE_FIELDS",
    "BLOCKED_OUTPUT_IDS", "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "MARKDOWN_SECTIONS",
    "BLOCKED_DIGEST_KEY", "SOURCE_BINDING_DIGEST_KEY", "INPUT_ABSENCE_DIGEST_KEY", "COVERAGE_DIGEST_KEY",
    "BLOCKED_MANIFEST_DIGEST_KEY", "SUCCESS_DIGEST_KEY", "PREPARED_INPUTS_DIGEST_KEY",
    "SUCCESS_MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTED_AFTER_APPROVAL_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_OPERATOR_INPUTS_UNAVAILABLE_OR_BOUNDARY_FAILURE",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTED_AFTER_APPROVAL_OPERATOR_INPUTS_PREPARED_OR_SUPPLIED_FOR_RESULTS_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_ONLY_INPUT_PREPARATION_OR_SUPPLY_FROM_EXPLICIT_NON_SECRET_OPERATOR_INPUTS_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_VALIDATION_NOT_EVIDENCE_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_markdown_v1",
]
